"""Primary user endpoints."""
from flask import Blueprint, request, jsonify
from app.models import (
    User, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer,
    WasteLog, Campaign, CampaignRegistration, Engagement, db
)
from app.core.security import token_required
from sqlalchemy import func, desc, and_
from datetime import datetime, date, timedelta
from calendar import monthrange

bp = Blueprint("primary", __name__)


@bp.route("/dashboard", methods=["GET"])
@token_required
def get_dashboard(user):
    """Get primary user dashboard data."""
    # Quiz performance
    quiz_attempts = QuizAttempt.query.filter_by(user_id=user.id, is_active=True).all()
    avg_score = 0
    if quiz_attempts:
        total_score = sum(attempt.score for attempt in quiz_attempts)
        total_questions = sum(attempt.total_questions for attempt in quiz_attempts)
        if total_questions > 0:
            avg_score = round((total_score / total_questions) * 100, 1)
    
    # Community leaderboard rank
    users_above = User.query.filter(
        User.points > user.points,
        User.is_active == True
    ).count()
    rank = users_above + 1
    
    # Monthly engagement
    current_month = date.today().replace(day=1)
    month_engagements = Engagement.query.filter(
        and_(
            Engagement.user_id == user.id,
            Engagement.month == current_month,
            Engagement.is_active == True
        )
    ).all()
    
    quiz_count = next((e.value for e in month_engagements if e.engagement_type == "quizzes"), 0)
    log_count = next((e.value for e in month_engagements if e.engagement_type == "waste_logs"), 0)
    # Get campaign registrations for current month
    month_start = datetime.combine(current_month, datetime.min.time())
    if current_month.month == 12:
        month_end = datetime(current_month.year + 1, 1, 1)
    else:
        month_end = datetime(current_month.year, current_month.month + 1, 1)
    
    campaign_count = CampaignRegistration.query.filter(
        and_(
            CampaignRegistration.user_id == user.id,
            CampaignRegistration.is_active == True,
            CampaignRegistration.created_at >= month_start,
            CampaignRegistration.created_at < month_end
        )
    ).count()
    
    # Waste summary (last 30 days)
    thirty_days_ago = date.today() - timedelta(days=30)
    waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id == user.id,
            WasteLog.log_date >= thirty_days_ago,
            WasteLog.is_active == True
        )
    ).all()
    
    wet_waste = sum(log.quantity_kg for log in waste_logs if log.category.lower() == "wet")
    dry_waste = sum(log.quantity_kg for log in waste_logs if log.category.lower() == "dry")
    hazardous_waste = sum(log.quantity_kg for log in waste_logs if log.category.lower() == "hazardous")
    
    return jsonify({
        "quiz_performance": {
            "average_score": avg_score,
            "message": "Great performance in daily quizzes." if avg_score >= 80 else "Keep practicing!"
        },
        "leaderboard": {
            "rank": rank,
            "points": user.points,
            "message": f"Keep climbing for #{rank-1}!" if rank > 1 else "You're at the top!"
        },
        "monthly_engagement": {
            "quizzes": quiz_count,
            "waste_logs": log_count,
            "campaigns": campaign_count,
            "message": "Your active participation."
        },
        "waste_summary": {
            "wet_kg": round(wet_waste, 1),
            "dry_kg": round(dry_waste, 1),
            "hazardous_kg": round(hazardous_waste, 1)
        }
    }), 200


@bp.route("/quiz/questions", methods=["GET"])
@token_required
def get_quiz_questions(user):
    """Get quiz questions for a quiz session."""
    limit = request.args.get("limit", 10, type=int)
    category = request.args.get("category", None)
    
    query = QuizQuestion.query.filter_by(is_active=True)
    if category:
        query = query.filter_by(category=category)
    
    questions = query.limit(limit).all()
    
    result = []
    for question in questions:
        options = QuizOption.query.filter_by(question_id=question.id, is_active=True).all()
        result.append({
            "id": question.id,
            "question_text": question.question_text,
            "category": question.category,
            "options": [
                {
                    "id": opt.id,
                    "option_text": opt.option_text,
                    "is_correct": opt.is_correct
                }
                for opt in options
            ]
        })
    
    return jsonify({"questions": result}), 200


@bp.route("/quiz/submit", methods=["POST"])
@token_required
def submit_quiz(user):
    """Submit quiz answers and calculate score."""
    data = request.get_json()
    
    if "answers" not in data:
        return jsonify({"error": "Answers required"}), 400
    
    answers = data["answers"]  # List of {question_id, selected_option_id}
    
    # Create quiz attempt
    attempt = QuizAttempt(
        user_id=user.id,
        total_questions=len(answers),
        score=0
    )
    db.session.add(attempt)
    db.session.flush()
    
    correct_count = 0
    for answer_data in answers:
        question_id = answer_data.get("question_id")
        selected_option_id = answer_data.get("selected_option_id")
        
        if not question_id:
            continue
        
        # Get the selected option
        selected_option = None
        if selected_option_id:
            selected_option = QuizOption.query.get(selected_option_id)
        
        is_correct = selected_option.is_correct if selected_option else False
        if is_correct:
            correct_count += 1
        
        # Create answer record
        quiz_answer = QuizAnswer(
            attempt_id=attempt.id,
            question_id=question_id,
            selected_option_id=selected_option_id,
            is_correct=is_correct
        )
        db.session.add(quiz_answer)
    
    # Update attempt score
    attempt.score = correct_count
    
    # Award points (10 points per correct answer)
    points_earned = correct_count * 10
    user.points += points_earned
    
    # Update engagement
    current_month = date.today().replace(day=1)
    engagement = Engagement.query.filter(
        and_(
            Engagement.user_id == user.id,
            Engagement.month == current_month,
            Engagement.engagement_type == "quizzes"
        )
    ).first()
    
    if engagement:
        engagement.value += 1
    else:
        engagement = Engagement(
            user_id=user.id,
            month=current_month,
            engagement_type="quizzes",
            value=1
        )
        db.session.add(engagement)
    
    db.session.commit()
    
    return jsonify({
        "attempt_id": attempt.id,
        "score": correct_count,
        "total_questions": len(answers),
        "percentage": round((correct_count / len(answers)) * 100, 1) if answers else 0,
        "points_earned": points_earned,
        "total_points": user.points
    }), 200


@bp.route("/quiz/performance", methods=["GET"])
@token_required
def get_quiz_performance(user):
    """Get detailed quiz performance."""
    attempts = QuizAttempt.query.filter_by(user_id=user.id, is_active=True).order_by(desc(QuizAttempt.created_at)).all()
    
    if not attempts:
        return jsonify({
            "quiz_score": 0,
            "average_quiz_score": 0,
            "overall_accuracy": 0,
            "category_breakdown": {},
            "past_quizzes": []
        }), 200
    
    # Calculate overall accuracy
    total_correct = sum(attempt.score for attempt in attempts)
    total_questions = sum(attempt.total_questions for attempt in attempts)
    overall_accuracy = round((total_correct / total_questions) * 100, 1) if total_questions > 0 else 0
    
    # Average quiz score
    avg_score = round((total_correct / len(attempts)) / (total_questions / len(attempts)) * 100, 1) if attempts else 0
    
    # Category breakdown (simplified - would need to track categories in attempts)
    category_breakdown = {
        "Recycling": 0,
        "Composting": 0,
        "Conservation": 0,
        "Sustainability": 0
    }
    
    # Get past quizzes
    past_quizzes = []
    for attempt in attempts[:18]:  # Last 18 quizzes
        percentage = round((attempt.score / attempt.total_questions) * 100, 1) if attempt.total_questions > 0 else 0
        past_quizzes.append({
            "id": attempt.id,
            "score": attempt.score,
            "total_questions": attempt.total_questions,
            "percentage": percentage,
            "date": attempt.created_at.isoformat()
        })
    
    return jsonify({
        "quiz_score": attempts[0].score if attempts else 0,
        "average_quiz_score": avg_score,
        "overall_accuracy": overall_accuracy,
        "category_breakdown": category_breakdown,
        "past_quizzes": past_quizzes
    }), 200


@bp.route("/waste-log", methods=["POST"])
@token_required
def log_waste(user):
    """Log waste entry."""
    data = request.get_json()
    
    required_fields = ["wet_waste", "dry_waste", "hazardous_waste", "separated", "recycled"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    log_date = datetime.strptime(data.get("log_date", date.today().isoformat()), "%Y-%m-%d").date()
    
    # Create waste log entries
    waste_categories = [
        ("wet", data["wet_waste"]),
        ("dry", data["dry_waste"]),
        ("hazardous", data["hazardous_waste"])
    ]
    
    for category, quantity in waste_categories:
        if quantity > 0:
            waste_log = WasteLog(
                user_id=user.id,
                log_date=log_date,
                category=category,
                quantity_kg=quantity,
                separated=data["separated"],
                recycled=data["recycled"],
                questions_doubts=data.get("questions_doubts"),
                feedback=data.get("feedback")
            )
            db.session.add(waste_log)
    
    # Update engagement
    current_month = date.today().replace(day=1)
    engagement = Engagement.query.filter(
        and_(
            Engagement.user_id == user.id,
            Engagement.month == current_month,
            Engagement.engagement_type == "waste_logs"
        )
    ).first()
    
    if engagement:
        engagement.value += 1
    else:
        engagement = Engagement(
            user_id=user.id,
            month=current_month,
            engagement_type="waste_logs",
            value=1
        )
        db.session.add(engagement)
    
    # Award points for proper segregation
    if data["separated"]:
        user.points += 5
    if data["recycled"]:
        user.points += 10
    
    db.session.commit()
    
    return jsonify({"message": "Waste logged successfully", "points": user.points}), 201


@bp.route("/waste-logs", methods=["GET"])
@token_required
def get_waste_logs(user):
    """Get user's waste log entries."""
    limit = request.args.get("limit", 20, type=int)
    offset = request.args.get("offset", 0, type=int)
    
    waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id == user.id,
            WasteLog.is_active == True
        )
    ).order_by(desc(WasteLog.log_date), desc(WasteLog.created_at)).limit(limit).offset(offset).all()
    
    result = []
    for log in waste_logs:
        result.append({
            "id": log.id,
            "log_date": log.log_date.isoformat(),
            "category": log.category,
            "quantity_kg": log.quantity_kg,
            "separated": log.separated,
            "recycled": log.recycled,
            "notes": log.notes,
            "questions_doubts": log.questions_doubts,
            "feedback": log.feedback
        })
    
    return jsonify({"waste_logs": result}), 200


@bp.route("/waste-summary", methods=["GET"])
@token_required
def get_waste_summary(user):
    """Get detailed waste summary."""
    months = request.args.get("months", 7, type=int)
    
    # Calculate date range
    end_date = date.today()
    start_date = date(end_date.year, end_date.month, 1) - timedelta(days=30 * months)
    
    waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id == user.id,
            WasteLog.log_date >= start_date,
            WasteLog.is_active == True
        )
    ).all()
    
    # Category breakdown
    category_totals = {}
    for log in waste_logs:
        category = log.category.lower()
        category_totals[category] = category_totals.get(category, 0) + log.quantity_kg
    
    total_waste = sum(category_totals.values())
    category_percentages = {
        category: round((amount / total_waste * 100), 1) if total_waste > 0 else 0
        for category, amount in category_totals.items()
    }
    
    # Monthly breakdown
    monthly_data = {}
    for log in waste_logs:
        month_key = log.log_date.strftime("%Y-%m")
        if month_key not in monthly_data:
            monthly_data[month_key] = {"disposed": 0, "undisposed": 0}
        
        if log.separated:
            monthly_data[month_key]["disposed"] += log.quantity_kg
        else:
            monthly_data[month_key]["undisposed"] += log.quantity_kg
    
    return jsonify({
        "category_breakdown": category_percentages,
        "monthly_trends": monthly_data
    }), 200


@bp.route("/leaderboard", methods=["GET"])
@token_required
def get_leaderboard(user):
    """Get community leaderboard."""
    users = User.query.filter_by(is_active=True).order_by(desc(User.points)).limit(100).all()
    
    user_rank = None
    for idx, u in enumerate(users, 1):
        if u.id == user.id:
            user_rank = idx
            break
    
    if user_rank is None:
        # User not in top 100, calculate rank
        users_above = User.query.filter(User.points > user.points, User.is_active == True).count()
        user_rank = users_above + 1
    
    # Determine remarks based on rank
    if user_rank == 1:
        remarks = "ECO CHAMPION"
    elif user_rank <= 3:
        remarks = "RECYCLE STAR"
    elif user_rank <= 10:
        remarks = "RECYCLE WARRIOR"
    else:
        remarks = "ECO FRIEND"
    
    leaderboard = []
    for idx, u in enumerate(users, 1):
        if idx == 1:
            u_remarks = "ECO CHAMPION"
        elif idx <= 3:
            u_remarks = "RECYCLE STAR"
        elif idx <= 10:
            u_remarks = "RECYCLE WARRIOR"
        else:
            u_remarks = "ECO FRIEND"
        
        # Extract name from username or email
        username = u.username or u.email
        name = u.username or (u.email.split('@')[0] if u.email else "User")
        
        leaderboard.append({
            "id": u.id,
            "rank": idx,
            "user": username,
            "name": name,
            "points": u.points,
            "remarks": u_remarks
        })
    
    return jsonify({
        "user_rank": user_rank,
        "user_score": user.points,
        "remarks": remarks,
        "leaderboard": leaderboard
    }), 200


@bp.route("/monthly-engagement", methods=["GET"])
@token_required
def get_monthly_engagement(user):
    """Get monthly engagement analytics."""
    current_month = date.today().replace(day=1)
    
    # Get engagement data for current month
    engagements = Engagement.query.filter(
        and_(
            Engagement.user_id == user.id,
            Engagement.month == current_month,
            Engagement.is_active == True
        )
    ).all()
    
    # Get daily usage trends (last 7 days)
    seven_days_ago = date.today() - timedelta(days=7)
    
    # Get quiz attempts in last 7 days
    quiz_attempts = QuizAttempt.query.filter(
        and_(
            QuizAttempt.user_id == user.id,
            func.date(QuizAttempt.created_at) >= seven_days_ago,
            QuizAttempt.is_active == True
        )
    ).all()
    
    # Get waste logs in last 7 days
    waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id == user.id,
            WasteLog.log_date >= seven_days_ago,
            WasteLog.is_active == True
        )
    ).all()
    
    # Group by day of week
    daily_trends = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        daily_trends[day] = {"quizzes": 0, "waste_logs": 0}
    
    for attempt in quiz_attempts:
        day_name = attempt.created_at.strftime("%A")
        if day_name in daily_trends:
            daily_trends[day_name]["quizzes"] += 1
    
    for log in waste_logs:
        day_name = log.log_date.strftime("%A")
        if day_name in daily_trends:
            daily_trends[day_name]["waste_logs"] += 1
    
    return jsonify({
        "monthly_engagement": {
            "quizzes": next((e.value for e in engagements if e.engagement_type == "quizzes"), 0),
            "waste_logs": next((e.value for e in engagements if e.engagement_type == "waste_logs"), 0),
            "campaigns": CampaignRegistration.query.filter(
                and_(
                    CampaignRegistration.user_id == user.id,
                    CampaignRegistration.is_active == True
                )
            ).count()
        },
        "daily_trends": daily_trends
    }), 200


@bp.route("/campaigns", methods=["GET"])
@token_required
def get_campaigns(user):
    """Get available campaigns."""
    # For now, show all active campaigns to ensure visibility
    # In the future, we can add location-based filtering if needed
    campaigns = Campaign.query.filter_by(is_active=True).order_by(Campaign.event_datetime).all()
    
    # Get user's registered campaigns
    registered_ids = {
        reg.campaign_id
        for reg in CampaignRegistration.query.filter_by(
            user_id=user.id,
            is_active=True
        ).all()
    }
    
    result = []
    for campaign in campaigns:
        is_registered = campaign.id in registered_ids
        result.append({
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "event_datetime": campaign.event_datetime.isoformat() if campaign.event_datetime else None,
            "location": campaign.location,
            "image_url": campaign.image_url,
            "is_registered": is_registered
        })
    
    return jsonify({"campaigns": result}), 200


@bp.route("/campaigns/<int:campaign_id>/register", methods=["POST"])
@token_required
def register_campaign(user, campaign_id):
    """Register for a campaign."""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    if not campaign.is_active:
        return jsonify({"error": "Campaign not available"}), 404
    
    # Check if already registered
    existing = CampaignRegistration.query.filter_by(
        user_id=user.id,
        campaign_id=campaign_id,
        is_active=True
    ).first()
    
    if existing:
        return jsonify({"error": "Already registered for this campaign"}), 400
    
    registration = CampaignRegistration(
        user_id=user.id,
        campaign_id=campaign_id,
        status="registered"
    )
    db.session.add(registration)
    db.session.commit()
    
    return jsonify({"message": "Successfully registered for campaign"}), 201

