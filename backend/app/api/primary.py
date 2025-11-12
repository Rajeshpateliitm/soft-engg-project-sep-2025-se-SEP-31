"""Primary user endpoints."""
from flask import Blueprint, request, jsonify
from app.models import (
    User, UserCategory, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer,
    WasteLog, Campaign, CampaignRegistration, Engagement, PickupRequest, Ward, db
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
    
    # Community leaderboard rank - only among PRIMARY users in the same ward
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    if primary_category and user.ward_id:
        users_above = User.query.filter(
            and_(
                User.points > user.points,
                User.is_active == True,
                User.user_category_id == primary_category.id,
                User.ward_id == user.ward_id
            )
        ).count()
        rank = users_above + 1
    else:
        rank = 1
    
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
    
    # Get all past quizzes (no limit to show all historical data)
    past_quizzes = []
    for attempt in attempts:  # All quiz attempts
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
    
    # Create pickup request first (if waste is logged)
    total_waste = data["wet_waste"] + data["dry_waste"] + data["hazardous_waste"]
    pickup_request = None
    pickup_request_id = None
    
    if total_waste > 0:
        # Generate request code
        import random
        import string
        request_code = "REQ-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Set scheduled date/time (default to log_date at 10:00 AM)
        from datetime import time as dt_time
        scheduled_datetime = datetime.combine(log_date, dt_time(hour=10, minute=0))
        
        # Create pickup location from user's address with ward information
        location_parts = []
        
        # Add house number
        if user.house_number:
            location_parts.append(user.house_number)
        else:
            # Fallback to username if no house number
            location_parts.append(user.username or user.email.split('@')[0])
        
        # Add ward information if available
        if user.ward_id:
            ward = Ward.query.get(user.ward_id)
            if ward:
                # Use ward name if available, otherwise use ward number
                ward_display = ward.name if ward.name else f"Ward {ward.ward_number}"
                location_parts.append(ward_display)
        
        # Add pincode
        if user.pincode:
            location_parts.append(user.pincode)
        
        # Join all parts with commas
        pickup_location = ", ".join(location_parts)
        
        pickup_request = PickupRequest(
            request_code=request_code,
            requester_id=user.id,
            scheduled_at=scheduled_datetime,
            pickup_location=pickup_location,
            pincode=user.pincode,
            quantity=total_waste,
            notes=f"Waste logged: Wet={data['wet_waste']}kg, Dry={data['dry_waste']}kg, Hazardous={data['hazardous_waste']}kg. Separated={data['separated']}, Recycled={data['recycled']}",
            status="pending"
        )
        db.session.add(pickup_request)
        db.session.flush()  # Flush to get pickup_request.id
        pickup_request_id = pickup_request.id
    
    # Create waste log entries and link them to pickup request
    waste_categories = [
        ("wet", data["wet_waste"]),
        ("dry", data["dry_waste"]),
        ("hazardous", data["hazardous_waste"])
    ]
    
    waste_logs_created = []
    for category, quantity in waste_categories:
        if quantity > 0:
            # Store pickup_request_id in notes field (format: "PICKUP_REQ_ID:123|other notes")
            notes_text = f"PICKUP_REQ_ID:{pickup_request_id}" if pickup_request_id else ""
            if data.get("questions_doubts"):
                notes_text = f"{notes_text}|{data['questions_doubts']}" if notes_text else data["questions_doubts"]
            
            waste_log = WasteLog(
                user_id=user.id,
                log_date=log_date,
                category=category,
                quantity_kg=quantity,
                separated=data["separated"],
                recycled=data["recycled"],
                notes=notes_text if notes_text else None,
                questions_doubts=data.get("questions_doubts"),
                feedback=data.get("feedback")
            )
            db.session.add(waste_log)
            waste_logs_created.append(waste_log)
    
    # Update engagement (count waste logs, but don't award points yet)
    current_month = date.today().replace(day=1)
    engagement = Engagement.query.filter(
        and_(
            Engagement.user_id == user.id,
            Engagement.month == current_month,
            Engagement.engagement_type == "waste_logs"
        )
    ).first()
    
    if engagement:
        engagement.value += len(waste_logs_created)
    else:
        engagement = Engagement(
            user_id=user.id,
            month=current_month,
            engagement_type="waste_logs",
            value=len(waste_logs_created)
        )
        db.session.add(engagement)
    
    # DO NOT award points here - points will be awarded when collector accepts
    # Points will be: +5 if separated, +10 if recycled (when accepted)
    # If rejected: -5 points
    
    db.session.commit()
    
    return jsonify({
        "message": "Waste logged successfully. Waiting for collector approval.",
        "points": user.points,
        "pickup_request_id": pickup_request_id,
        "status": "pending"
    }), 201


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
    months_param = request.args.get("months", "1", type=str)
    
    # Parse months parameter (can be float like 0.25 for weekly, or int)
    try:
        if months_param == "all":
            months = 120  # 10 years
        else:
            months = float(months_param)
    except (ValueError, TypeError):
        months = 1
    
    # Calculate date range based on time range
    today = date.today()
    
    if months_param == "weekly":
        # Last 7 days
        start_date = today - timedelta(days=7)
    elif months_param == "yearly":
        # Last 12 months
        start_date = date(today.year - 1, today.month, 1)
    elif months_param == "all":
        # Last 10 years (or all available data)
        start_date = date(today.year - 10, 1, 1)
    else:
        # Monthly (default) - last 30 days
        start_date = today - timedelta(days=30)
    
    # Get waste logs in date range
    waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id == user.id,
            WasteLog.log_date >= start_date,
            WasteLog.log_date <= today,
            WasteLog.is_active == True
        )
    ).order_by(WasteLog.log_date).all()
    
    # Category breakdown with actual amounts
    category_totals = {}
    total_waste = 0
    recycled_amount = 0
    separated_amount = 0
    
    for log in waste_logs:
        category = log.category.lower()
        category_totals[category] = category_totals.get(category, 0) + log.quantity_kg
        total_waste += log.quantity_kg
        
        if log.recycled:
            recycled_amount += log.quantity_kg
        if log.separated:
            separated_amount += log.quantity_kg
    
    # Calculate category percentages and amounts
    category_breakdown = {}
    for category, amount in category_totals.items():
        category_breakdown[category] = {
            "amount": round(amount, 1),
            "percentage": round((amount / total_waste * 100), 1) if total_waste > 0 else 0
        }
    
    # Calculate recycling rate
    recycling_rate = round((recycled_amount / total_waste * 100), 1) if total_waste > 0 else 0
    
    # Calculate carbon footprint (estimated: ~2.2 kg CO2 per kg of waste)
    carbon_footprint = round(total_waste * 2.2, 1)
    
    # Get previous period for comparison
    if months_param == "weekly":
        prev_start_date = start_date - timedelta(days=7)
        prev_end_date = start_date
    elif months_param == "yearly":
        prev_start_date = date(today.year - 2, today.month, 1)
        prev_end_date = date(today.year - 1, today.month, 1)
    elif months_param == "all":
        prev_start_date = date(today.year - 20, 1, 1)
        prev_end_date = date(today.year - 10, 1, 1)
    else:
        # Monthly - compare with previous 30 days
        prev_start_date = start_date - timedelta(days=30)
        prev_end_date = start_date
    
    prev_waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id == user.id,
            WasteLog.log_date >= prev_start_date,
            WasteLog.log_date < prev_end_date,
            WasteLog.is_active == True
        )
    ).all()
    
    prev_total_waste = sum(log.quantity_kg for log in prev_waste_logs)
    prev_recycled_amount = sum(log.quantity_kg for log in prev_waste_logs if log.recycled)
    prev_carbon_footprint = round(prev_total_waste * 2.2, 1) if prev_total_waste > 0 else 0
    
    # Calculate changes
    waste_change = 0
    if prev_total_waste > 0:
        waste_change = round(((total_waste - prev_total_waste) / prev_total_waste) * 100, 1)
    elif total_waste > 0:
        waste_change = 100
    
    carbon_change = 0
    if prev_carbon_footprint > 0:
        carbon_change = round(((carbon_footprint - prev_carbon_footprint) / prev_carbon_footprint) * 100, 1)
    elif carbon_footprint > 0:
        carbon_change = 100
    
    # Calculate waste reduction (based on recycling rate improvement)
    prev_recycling_rate = round((prev_recycled_amount / prev_total_waste * 100), 1) if prev_total_waste > 0 else 0
    waste_reduction = max(0, recycling_rate - prev_recycling_rate) if recycling_rate > prev_recycling_rate else 0
    
    # Daily trends with actual dates
    daily_trends = {}
    current_date = start_date
    while current_date <= today:
        date_str = current_date.isoformat()
        daily_trends[date_str] = {
            "date": date_str,
            "total": 0,
            "recycled": 0,
            "separated": 0,
            "landfill": 0,
            "by_category": {}
        }
        current_date += timedelta(days=1)
    
    # Populate daily trends from waste logs
    for log in waste_logs:
        date_str = log.log_date.isoformat()
        if date_str in daily_trends:
            daily_trends[date_str]["total"] += log.quantity_kg
            category = log.category.lower()
            if category not in daily_trends[date_str]["by_category"]:
                daily_trends[date_str]["by_category"][category] = 0
            daily_trends[date_str]["by_category"][category] += log.quantity_kg
            
            if log.recycled:
                daily_trends[date_str]["recycled"] += log.quantity_kg
            if log.separated:
                daily_trends[date_str]["separated"] += log.quantity_kg
            if not log.recycled and not log.separated:
                daily_trends[date_str]["landfill"] += log.quantity_kg
    
    # Convert daily trends to list sorted by date
    daily_trends_list = [
        {
            "date": date_str,
            "total": round(data["total"], 1),
            "recycled": round(data["recycled"], 1),
            "separated": round(data["separated"], 1),
            "landfill": round(data["landfill"], 1),
            "by_category": {k: round(v, 1) for k, v in data["by_category"].items()}
        }
        for date_str, data in sorted(daily_trends.items())
    ]
    
    # Monthly breakdown (for backward compatibility and monthly view)
    monthly_data = {}
    for log in waste_logs:
        month_key = log.log_date.strftime("%Y-%m")
        if month_key not in monthly_data:
            monthly_data[month_key] = {"disposed": 0, "undisposed": 0, "recycled": 0}
        
        if log.separated:
            monthly_data[month_key]["disposed"] += log.quantity_kg
        else:
            monthly_data[month_key]["undisposed"] += log.quantity_kg
        
        if log.recycled:
            monthly_data[month_key]["recycled"] += log.quantity_kg
    
    # Get recent waste logs (last 20)
    recent_logs = []
    recent_waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id == user.id,
            WasteLog.is_active == True
        )
    ).order_by(desc(WasteLog.log_date), desc(WasteLog.created_at)).limit(20).all()
    
    for log in recent_waste_logs:
        disposal_method = "Recycling" if log.recycled else ("Separated" if log.separated else "Landfill")
        carbon_impact = round(log.quantity_kg * 2.2, 1)
        
        recent_logs.append({
            "id": log.id,
            "date": log.log_date.isoformat(),
            "category": log.category,
            "quantity_kg": log.quantity_kg,
            "disposal_method": disposal_method,
            "carbon_impact": carbon_impact,
            "separated": log.separated,
            "recycled": log.recycled
        })
    
    return jsonify({
        "summary": {
            "total_waste": round(total_waste, 1),
            "waste_change": waste_change,
            "recycling_rate": recycling_rate,
            "carbon_footprint": carbon_footprint,
            "carbon_change": carbon_change,
            "waste_reduction": round(waste_reduction, 1),
            "separated_amount": round(separated_amount, 1),
            "recycled_amount": round(recycled_amount, 1)
        },
        "category_breakdown": category_breakdown,
        "daily_trends": daily_trends_list,
        "monthly_trends": monthly_data,
        "recent_logs": recent_logs
    }), 200


@bp.route("/leaderboard", methods=["GET"])
@token_required
def get_leaderboard(user):
    """Get community leaderboard - only PRIMARY users in the same ward."""
    # Get PRIMARY user category
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    if not primary_category:
        return jsonify({"error": "PRIMARY user category not found"}), 500
    
    # Get current user's ward_id
    user_ward_id = user.ward_id
    
    # Build query to filter PRIMARY users in the same ward
    query = User.query.filter(
        and_(
            User.is_active == True,
            User.user_category_id == primary_category.id
        )
    )
    
    # Filter by ward if user has a ward assigned
    if user_ward_id:
        query = query.filter(User.ward_id == user_ward_id)
    else:
        # If user doesn't have a ward, return empty leaderboard with a message
        return jsonify({
            "user_rank": 0,
            "user_score": user.points,
            "user_quiz_count": QuizAttempt.query.filter_by(user_id=user.id, is_active=True).count(),
            "remarks": "No ward assigned",
            "leaderboard": [],
            "message": "You need to be assigned to a ward to view the leaderboard."
        }), 200
    
    # Get all users in the same ward, ordered by points
    users = query.order_by(desc(User.points)).all()
    
    # Calculate user's rank within the ward
    users_above = User.query.filter(
        and_(
            User.points > user.points,
            User.is_active == True,
            User.user_category_id == primary_category.id,
            User.ward_id == user_ward_id
        )
    ).count()
    user_rank = users_above + 1
    
    # Get quiz count for current user
    quiz_count = QuizAttempt.query.filter_by(user_id=user.id, is_active=True).count()
    
    # Determine remarks based on rank
    if user_rank == 1:
        remarks = "ECO CHAMPION"
    elif user_rank <= 3:
        remarks = "RECYCLE STAR"
    elif user_rank <= 10:
        remarks = "RECYCLE WARRIOR"
    else:
        remarks = "ECO FRIEND"
    
    # Build leaderboard with ranks
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
        "user_quiz_count": quiz_count,
        "remarks": remarks,
        "leaderboard": leaderboard
    }), 200


@bp.route("/monthly-engagement", methods=["GET"])
@token_required
def get_monthly_engagement(user):
    """Get monthly engagement analytics."""
    current_month = date.today().replace(day=1)
    today = date.today()
    
    # Get engagement data for current month
    engagements = Engagement.query.filter(
        and_(
            Engagement.user_id == user.id,
            Engagement.month == current_month,
            Engagement.is_active == True
        )
    ).all()
    
    # Get quiz count for current month
    month_start = datetime(current_month.year, current_month.month, 1)
    if current_month.month == 12:
        month_end = datetime(current_month.year + 1, 1, 1)
    else:
        month_end = datetime(current_month.year, current_month.month + 1, 1)
    
    quiz_count_current_month = QuizAttempt.query.filter(
        and_(
            QuizAttempt.user_id == user.id,
            QuizAttempt.created_at >= month_start,
            QuizAttempt.created_at < month_end,
            QuizAttempt.is_active == True
        )
    ).count()
    
    # Get quiz count for previous month for comparison
    if current_month.month == 1:
        prev_month = date(current_month.year - 1, 12, 1)
    else:
        prev_month = date(current_month.year, current_month.month - 1, 1)
    prev_month_start = datetime(prev_month.year, prev_month.month, 1)
    prev_month_end = datetime(current_month.year, current_month.month, 1)
    
    quiz_count_prev_month = QuizAttempt.query.filter(
        and_(
            QuizAttempt.user_id == user.id,
            QuizAttempt.created_at >= prev_month_start,
            QuizAttempt.created_at < prev_month_end,
            QuizAttempt.is_active == True
        )
    ).count()
    
    # Calculate quiz count change percentage
    quiz_change = 0
    if quiz_count_prev_month > 0:
        quiz_change = round(((quiz_count_current_month - quiz_count_prev_month) / quiz_count_prev_month) * 100, 1)
    elif quiz_count_current_month > 0:
        quiz_change = 100
    
    # Get average quiz score for current month
    quiz_attempts_current_month = QuizAttempt.query.filter(
        and_(
            QuizAttempt.user_id == user.id,
            QuizAttempt.created_at >= month_start,
            QuizAttempt.created_at < month_end,
            QuizAttempt.is_active == True
        )
    ).all()
    
    avg_score_current_month = 0
    if quiz_attempts_current_month:
        total_score = sum(attempt.score for attempt in quiz_attempts_current_month)
        total_questions = sum(attempt.total_questions for attempt in quiz_attempts_current_month)
        if total_questions > 0:
            avg_score_current_month = round((total_score / total_questions) * 100, 1)
    
    # Get average quiz score for previous month
    quiz_attempts_prev_month = QuizAttempt.query.filter(
        and_(
            QuizAttempt.user_id == user.id,
            QuizAttempt.created_at >= prev_month_start,
            QuizAttempt.created_at < prev_month_end,
            QuizAttempt.is_active == True
        )
    ).all()
    
    avg_score_prev_month = 0
    if quiz_attempts_prev_month:
        total_score = sum(attempt.score for attempt in quiz_attempts_prev_month)
        total_questions = sum(attempt.total_questions for attempt in quiz_attempts_prev_month)
        if total_questions > 0:
            avg_score_prev_month = round((total_score / total_questions) * 100, 1)
    
    # Calculate score change
    score_change = 0
    if avg_score_prev_month > 0:
        score_change = round(avg_score_current_month - avg_score_prev_month, 1)
    elif avg_score_current_month > 0:
        score_change = avg_score_current_month
    
    # Get ranking
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    rank = 1
    if primary_category:
        users_above = User.query.filter(
            and_(
                User.points > user.points,
                User.is_active == True,
                User.user_category_id == primary_category.id
            )
        ).count()
        rank = users_above + 1
    
    # Calculate current streak (consecutive days with quiz attempts)
    current_streak = 0
    streak_active = False
    check_date = today
    while True:
        day_start = datetime(check_date.year, check_date.month, check_date.day, 0, 0, 0)
        next_day = check_date + timedelta(days=1)
        day_end = datetime(next_day.year, next_day.month, next_day.day, 0, 0, 0)
        
        has_quiz = QuizAttempt.query.filter(
            and_(
                QuizAttempt.user_id == user.id,
                QuizAttempt.created_at >= day_start,
                QuizAttempt.created_at < day_end,
                QuizAttempt.is_active == True
            )
        ).first() is not None
        
        if has_quiz:
            current_streak += 1
            if check_date == today:
                streak_active = True
            check_date -= timedelta(days=1)
        else:
            if check_date == today:
                break
            else:
                break
    
    # Get daily trends with actual dates (last 30 days)
    thirty_days_ago = today - timedelta(days=30)
    daily_trends = {}
    
    # Get quiz attempts in last 30 days
    quiz_attempts = QuizAttempt.query.filter(
        and_(
            QuizAttempt.user_id == user.id,
            func.date(QuizAttempt.created_at) >= thirty_days_ago,
            QuizAttempt.is_active == True
        )
    ).all()
    
    # Get waste logs in last 30 days
    waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id == user.id,
            WasteLog.log_date >= thirty_days_ago,
            WasteLog.is_active == True
        )
    ).all()
    
    # Initialize all dates in range
    current_date = thirty_days_ago
    while current_date <= today:
        date_str = current_date.isoformat()
        daily_trends[date_str] = {
            "date": date_str,
            "quizzes": 0,
            "waste_logs": 0,
            "points": 0
        }
        current_date += timedelta(days=1)
    
    # Group quiz attempts by date
    for attempt in quiz_attempts:
        attempt_date = attempt.created_at.date()
        date_str = attempt_date.isoformat()
        if date_str in daily_trends:
            daily_trends[date_str]["quizzes"] += 1
            # Calculate points: 10 points per correct answer
            points_earned = attempt.score * 10
            daily_trends[date_str]["points"] += points_earned
    
    # Track processed pickup requests per date to avoid double-counting
    processed_pickups_per_date = {}
    
    # Group waste logs by date
    for log in waste_logs:
        date_str = log.log_date.isoformat()
        if date_str in daily_trends:
            daily_trends[date_str]["waste_logs"] += 1
            # Calculate points based on pickup request status
            log_points = 0
            pickup_status = "pending"
            pickup_request_id = None
            
            # Find pickup request status from notes
            if log.notes and "PICKUP_REQ_ID:" in log.notes:
                try:
                    pickup_id_str = log.notes.split("PICKUP_REQ_ID:")[1].split("|")[0].split()[0]
                    pickup_request_id = int(pickup_id_str)
                    
                    # Initialize set for this date if not exists
                    if date_str not in processed_pickups_per_date:
                        processed_pickups_per_date[date_str] = set()
                    
                    # Skip if we've already processed this pickup request for this date
                    if pickup_request_id in processed_pickups_per_date[date_str]:
                        continue
                    
                    # Query fresh from database to get latest status
                    pickup_request = db.session.query(PickupRequest).filter(
                        and_(
                            PickupRequest.id == pickup_request_id,
                            PickupRequest.is_active == True
                        )
                    ).first()
                    if pickup_request:
                        pickup_status = pickup_request.status if pickup_request.status else "pending"
                        
                        # Mark this pickup request as processed for this date
                        processed_pickups_per_date[date_str].add(pickup_request_id)
                        
                        # Only award points if accepted or completed (once per pickup request per date)
                        # Handle both "accepted" and "completed" statuses (they mean the same thing)
                        if pickup_status in ["accepted", "completed"]:
                            if log.separated:
                                log_points += 5
                            if log.recycled:
                                log_points += 10
                        elif pickup_status == "rejected":
                            log_points = -5
                except (ValueError, IndexError, AttributeError):
                    pass
            
            daily_trends[date_str]["points"] += log_points
    
    # Get time of day activity (group by hour)
    time_of_day = {hour: 0 for hour in range(24)}
    for attempt in quiz_attempts:
        hour = attempt.created_at.hour
        time_of_day[hour] = time_of_day.get(hour, 0) + 1
    
    # Get recent activities (last 20 quiz attempts, waste logs, and campaign registrations)
    recent_activities = []
    
    # Get recent quiz attempts
    recent_quiz_attempts = QuizAttempt.query.filter(
        and_(
            QuizAttempt.user_id == user.id,
            QuizAttempt.is_active == True
        )
    ).order_by(desc(QuizAttempt.created_at)).limit(10).all()
    
    for attempt in recent_quiz_attempts:
        percentage = round((attempt.score / attempt.total_questions) * 100, 1) if attempt.total_questions > 0 else 0
        # Calculate points: 10 points per correct answer (as per quiz submission logic)
        points_earned = attempt.score * 10
        recent_activities.append({
            "type": "quiz",
            "title": "Quiz Completed",
            "subtitle": "Waste Management Quiz",
            "details": f"Score: {percentage}% ({attempt.score}/{attempt.total_questions})",
            "points": points_earned,
            "timestamp": attempt.created_at.isoformat(),
            "icon": "bi-check-circle",
            "variant": "primary"
        })
    
    # Get recent campaign registrations
    recent_campaign_registrations = CampaignRegistration.query.filter(
        and_(
            CampaignRegistration.user_id == user.id,
            CampaignRegistration.is_active == True
        )
    ).order_by(desc(CampaignRegistration.created_at)).limit(10).all()
    
    for registration in recent_campaign_registrations:
        campaign = Campaign.query.get(registration.campaign_id)
        if campaign:
            recent_activities.append({
                "type": "campaign",
                "title": "Campaign Registered",
                "subtitle": campaign.name,
                "details": f"Status: {registration.status.capitalize()}",
                "points": 5,  # +5 points for campaign registration
                "timestamp": registration.created_at.isoformat(),
                "icon": "bi-calendar-event",
                "variant": "info"
            })
    
    # Get recent waste logs
    recent_waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id == user.id,
            WasteLog.is_active == True
        )
    ).order_by(desc(WasteLog.log_date), desc(WasteLog.created_at)).limit(10).all()
    
    for log in recent_waste_logs:
        # Find pickup request status from notes (PICKUP_REQ_ID:123)
        pickup_request_id = None
        pickup_status = "pending"
        log_points = 0
        
        if log.notes and "PICKUP_REQ_ID:" in log.notes:
            # Extract pickup_request_id from notes
            try:
                # Handle different note formats: "PICKUP_REQ_ID:123" or "PICKUP_REQ_ID:123|other text"
                # Split by "PICKUP_REQ_ID:" and take the part after it
                after_prefix = log.notes.split("PICKUP_REQ_ID:")[1]
                # Split by "|" to get just the ID part (if pipe exists)
                pickup_id_str = after_prefix.split("|")[0].strip()
                # Remove any whitespace and get just the number
                pickup_id_str = ''.join(pickup_id_str.split())  # Remove all whitespace
                pickup_request_id = int(pickup_id_str)
                
                # Get pickup request status - query fresh from database to get latest status
                # Expire any cached objects first to ensure we get fresh data
                db.session.expire_all()
                # Use a fresh query to bypass any session caching
                pickup_request = db.session.query(PickupRequest).filter(
                    and_(
                        PickupRequest.id == pickup_request_id,
                        PickupRequest.is_active == True
                    )
                ).first()
                if pickup_request:
                    # Get the status directly (this should be fresh from the database)
                    pickup_status = pickup_request.status if pickup_request.status else "pending"
                    
                    # Handle both "accepted" and "completed" statuses (they mean the same thing)
                    if pickup_status in ["accepted", "completed"]:
                        if log.separated:
                            log_points += 5
                        if log.recycled:
                            log_points += 10
                        # Normalize status to "accepted" for display
                        pickup_status = "accepted"
                    elif pickup_status == "rejected":
                        log_points = -5
                    # If pending, points remain 0
                else:
                    # Pickup request not found - might have been deleted
                    pickup_status = "pending"
            except (ValueError, IndexError, AttributeError, TypeError) as e:
                # Log error for debugging but continue processing
                print(f"Error parsing pickup_request_id from waste log {log.id}, notes: '{log.notes}', error: {e}")
                pass
        
        # Determine variant based on status
        variant = "success"
        if pickup_status == "pending":
            variant = "warning"
        elif pickup_status == "rejected":
            variant = "danger"
        
        status_text = pickup_status.capitalize()
        if pickup_status == "pending":
            status_text = "Pending Approval"
        elif pickup_status in ["accepted", "completed"]:
            status_text = "Accepted"
        elif pickup_status == "rejected":
            status_text = "Rejected"
        
        recent_activities.append({
            "type": "waste_log",
            "title": "Waste Logged",
            "subtitle": f"{log.category.capitalize()} Waste - {status_text}",
            "details": f"{log.quantity_kg} kg",
            "points": log_points,
            "timestamp": datetime(log.log_date.year, log.log_date.month, log.log_date.day, 0, 0, 0).isoformat(),
            "icon": "bi-trash",
            "variant": variant,
            "pickup_status": pickup_status
        })
    
    # Sort by timestamp (most recent first) and limit to 20
    recent_activities.sort(key=lambda x: x["timestamp"], reverse=True)
    recent_activities = recent_activities[:20]
    
    # Get campaign count for current month (needed for points calculation)
    campaign_count = CampaignRegistration.query.filter(
        and_(
            CampaignRegistration.user_id == user.id,
            CampaignRegistration.created_at >= month_start,
            CampaignRegistration.created_at < month_end,
            CampaignRegistration.is_active == True
        )
    ).count()
    
    # Get points earned this month (from quiz attempts, waste logs, and campaign registrations)
    points_this_month = 0
    for attempt in quiz_attempts_current_month:
        # Calculate points: 10 points per correct answer
        points_this_month += attempt.score * 10
    
    # Add points from campaign registrations (+5 points per registration)
    points_this_month += campaign_count * 5
    
    # Get waste logs for current month and calculate points (only for accepted requests)
    month_waste_logs_all = WasteLog.query.filter(
        and_(
            WasteLog.user_id == user.id,
            WasteLog.log_date >= current_month,
            WasteLog.log_date < month_end.date(),
            WasteLog.is_active == True
        )
    ).all()
    
    # Track processed pickup requests to avoid double-counting points
    processed_pickup_requests = set()
    
    # Calculate points based on pickup request status
    for log in month_waste_logs_all:
        pickup_status = "pending"
        pickup_request_id = None
        
        # Find pickup request status from notes
        if log.notes and "PICKUP_REQ_ID:" in log.notes:
            try:
                pickup_id_str = log.notes.split("PICKUP_REQ_ID:")[1].split("|")[0].split()[0]
                pickup_request_id = int(pickup_id_str)
                
                # Skip if we've already processed this pickup request
                if pickup_request_id in processed_pickup_requests:
                    continue
                
                # Query fresh from database to get latest status
                pickup_request = db.session.query(PickupRequest).filter(
                    and_(
                        PickupRequest.id == pickup_request_id,
                        PickupRequest.is_active == True
                    )
                ).first()
                if pickup_request:
                    pickup_status = pickup_request.status if pickup_request.status else "pending"
                    
                    # Mark this pickup request as processed
                    processed_pickup_requests.add(pickup_request_id)
                    
                    # Only award points if accepted or completed (once per pickup request)
                    # Handle both "accepted" and "completed" statuses (they mean the same thing)
                    if pickup_status in ["accepted", "completed"]:
                        if log.separated:
                            points_this_month += 5
                        if log.recycled:
                            points_this_month += 10
                    elif pickup_status == "rejected":
                        points_this_month -= 5  # Deduct 5 points for rejection (once per pickup request)
            except (ValueError, IndexError, AttributeError):
                pass
    
    # Convert daily_trends to list sorted by date
    daily_trends_list = [
        {
            "date": date_str,
            "quizzes": data["quizzes"],
            "waste_logs": data["waste_logs"],
            "points": data["points"]
        }
        for date_str, data in sorted(daily_trends.items())
    ]
    
    return jsonify({
        "monthly_engagement": {
            "quizzes": quiz_count_current_month,
            "waste_logs": next((e.value for e in engagements if e.engagement_type == "waste_logs"), 0),
            "campaigns": campaign_count,
            "points": points_this_month
        },
        "stats": {
            "quizzes_completed": quiz_count_current_month,
            "quizzes_change": quiz_change,
            "average_score": avg_score_current_month,
            "score_change": score_change,
            "current_streak": current_streak,
            "streak_active": streak_active,
            "ranking": rank,
            "ranking_change": 0  # Could calculate from previous month if needed
        },
        "daily_trends": daily_trends_list,
        "time_of_day": time_of_day,
        "recent_activities": recent_activities
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
        # Count total registrations
        registration_count = CampaignRegistration.query.filter_by(
            campaign_id=campaign.id,
            is_active=True
        ).count()
        
        result.append({
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "event_datetime": campaign.event_datetime.isoformat() if campaign.event_datetime else None,
            "location": campaign.location,
            "pincode": campaign.pincode,
            "image_url": campaign.image_url,
            "is_registered": is_registered,
            "registration_count": registration_count
        })
    
    return jsonify({"campaigns": result}), 200


@bp.route("/campaigns/<int:campaign_id>/register", methods=["POST"])
@token_required
def register_campaign(user, campaign_id):
    """Register for a campaign. Awards +5 points."""
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
    
    # Create registration
    registration = CampaignRegistration(
        user_id=user.id,
        campaign_id=campaign_id,
        status="registered"
    )
    db.session.add(registration)
    
    # Award +5 points for campaign registration
    user.points += 5
    
    # Update engagement
    current_month = date.today().replace(day=1)
    engagement = Engagement.query.filter(
        and_(
            Engagement.user_id == user.id,
            Engagement.month == current_month,
            Engagement.engagement_type == "campaigns"
        )
    ).first()
    
    if engagement:
        engagement.value += 1
    else:
        engagement = Engagement(
            user_id=user.id,
            month=current_month,
            engagement_type="campaigns",
            value=1
        )
        db.session.add(engagement)
    
    db.session.commit()
    
    return jsonify({
        "message": "Successfully registered for campaign",
        "points_awarded": 5,
        "total_points": user.points
    }), 201

