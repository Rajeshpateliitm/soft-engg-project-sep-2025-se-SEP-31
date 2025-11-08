"""Secondary user (RWA/Collector) endpoints."""
from flask import Blueprint, request, jsonify
from app.models import (
    User, RwaGroup, RwaMembership, PickupRequest, WasteLog,
    Campaign, CampaignRegistration, db
)
from app.core.security import token_required
from sqlalchemy import func, desc, and_, or_
from datetime import datetime, date, timedelta

bp = Blueprint("secondary", __name__)


@bp.route("/dashboard", methods=["GET"])
@token_required
def get_dashboard(user):
    """Get secondary user dashboard."""
    # Get RWA membership
    membership = RwaMembership.query.filter_by(user_id=user.id, is_active=True).first()
    
    if not membership:
        return jsonify({"error": "User is not a member of any RWA"}), 403
    
    rwa_group = membership.rwa_group
    
    # RWA Leaderboard rank
    rwa_groups = RwaGroup.query.filter_by(is_active=True).all()
    rwa_scores = []
    for group in rwa_groups:
        members = RwaMembership.query.filter_by(rwa_group_id=group.id, is_active=True).all()
        total_points = sum(User.query.get(m.user_id).points for m in members if User.query.get(m.user_id))
        rwa_scores.append((group.id, total_points))
    
    rwa_scores.sort(key=lambda x: x[1], reverse=True)
    rwa_rank = next((idx + 1 for idx, (gid, _) in enumerate(rwa_scores) if gid == rwa_group.id), len(rwa_scores))
    
    # Household count
    household_count = RwaMembership.query.filter_by(
        rwa_group_id=rwa_group.id,
        is_active=True
    ).count()
    
    # Today's pickup summary
    today = date.today()
    today_pickups = PickupRequest.query.filter(
        func.date(PickupRequest.scheduled_at) == today
    ).all()
    
    total_pickups = len(today_pickups)
    completed = len([p for p in today_pickups if p.status == "completed"])
    pending = len([p for p in today_pickups if p.status == "pending"])
    accepted = len([p for p in today_pickups if p.status == "accepted"])
    rejected = len([p for p in today_pickups if p.status == "rejected"])
    
    return jsonify({
        "rwa_leaderboard": {
            "rank": rwa_rank,
            "households": household_count,
            "rwa_name": rwa_group.name
        },
        "pickup_summary": {
            "date": today.isoformat(),
            "total_pickups": total_pickups,
            "completed": completed,
            "pending": pending,
            "accepted": accepted,
            "rejected": rejected,
            "left": total_pickups - completed
        }
    }), 200


@bp.route("/rwa-leaderboard", methods=["GET"])
@token_required
def get_rwa_leaderboard(user):
    """Get RWA leaderboard."""
    rwa_groups = RwaGroup.query.filter_by(is_active=True).all()
    
    rwa_data = []
    for group in rwa_groups:
        members = RwaMembership.query.filter_by(rwa_group_id=group.id, is_active=True).all()
        total_points = 0
        for member in members:
            member_user = User.query.get(member.user_id)
            if member_user:
                total_points += member_user.points
        
        rwa_data.append({
            "rwa_id": group.id,
            "rwa_name": group.name,
            "points": total_points
        })
    
    rwa_data.sort(key=lambda x: x["points"], reverse=True)
    
    # Add rank and remarks
    for idx, rwa in enumerate(rwa_data, 1):
        if idx == 1:
            rwa["remarks"] = "TOP PERFORMER"
        elif idx <= 3:
            rwa["remarks"] = "EXCELLENT"
        elif idx <= 10:
            rwa["remarks"] = "GOOD"
        else:
            rwa["remarks"] = "IMPROVING"
        rwa["rank"] = idx
    
    return jsonify({"leaderboard": rwa_data}), 200


@bp.route("/pickup-summary", methods=["GET"])
@token_required
def get_pickup_summary(user):
    """Get monthly pickup summary."""
    months = request.args.get("months", 1, type=int)
    
    # Calculate date range
    end_date = date.today()
    start_date = date(end_date.year, end_date.month, 1) - timedelta(days=30 * months)
    
    pickups = PickupRequest.query.filter(
        PickupRequest.scheduled_at >= datetime.combine(start_date, datetime.min.time())
    ).all()
    
    total_scheduled = len(pickups)
    total_completed = len([p for p in pickups if p.status == "completed"])
    total_pending = len([p for p in pickups if p.status == "pending"])
    total_rejected = len([p for p in pickups if p.status == "rejected"])
    
    # Daily pickups by status (last 30 days)
    daily_data = {}
    for i in range(30):
        day = end_date - timedelta(days=i)
        day_pickups = [p for p in pickups if p.scheduled_at.date() == day]
        daily_data[day.isoformat()] = {
            "completed": len([p for p in day_pickups if p.status == "completed"]),
            "pending": len([p for p in day_pickups if p.status == "pending"]),
            "rejected": len([p for p in day_pickups if p.status == "rejected"])
        }
    
    return jsonify({
        "total_scheduled": total_scheduled,
        "total_completed": total_completed,
        "total_pending": total_pending,
        "total_rejected": total_rejected,
        "daily_breakdown": daily_data
    }), 200


@bp.route("/pickup-details", methods=["GET"])
@token_required
def get_pickup_details(user):
    """Get daily pickup details."""
    date_str = request.args.get("date", date.today().isoformat())
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    pickups = PickupRequest.query.filter(
        func.date(PickupRequest.scheduled_at) == target_date
    ).order_by(PickupRequest.scheduled_at).all()
    
    result = []
    for pickup in pickups:
        requester = User.query.get(pickup.requester_id)
        result.append({
            "request_no": pickup.request_code or f"REQ-{pickup.id}",
            "user_id": pickup.requester_id,
            "user_name": requester.username if requester else "Unknown",
            "pickup_location": pickup.pickup_location or f"{requester.house_number}, {requester.pincode}" if requester else "N/A",
            "date_of_pickup": pickup.scheduled_at.date().isoformat() if pickup.scheduled_at else None,
            "time_of_pickup": pickup.scheduled_at.time().isoformat() if pickup.scheduled_at else None,
            "disposal_quantity": pickup.quantity or 0,
            "status": pickup.status
        })
    
    return jsonify({
        "date": target_date.isoformat(),
        "pickups": result
    }), 200


@bp.route("/pickup/<int:pickup_id>/accept", methods=["POST"])
@token_required
def accept_pickup(user, pickup_id):
    """Accept a pickup request."""
    pickup = PickupRequest.query.get_or_404(pickup_id)
    
    if pickup.status != "pending":
        return jsonify({"error": "Pickup request is not pending"}), 400
    
    pickup.status = "accepted"
    pickup.assigned_collector_id = user.id
    pickup.decision_by_user_id = user.id
    pickup.decision_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({"message": "Pickup request accepted"}), 200


@bp.route("/pickup/<int:pickup_id>/reject", methods=["POST"])
@token_required
def reject_pickup(user, pickup_id):
    """Reject a pickup request."""
    pickup = PickupRequest.query.get_or_404(pickup_id)
    
    if pickup.status != "pending":
        return jsonify({"error": "Pickup request is not pending"}), 400
    
    pickup.status = "rejected"
    pickup.decision_by_user_id = user.id
    pickup.decision_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({"message": "Pickup request rejected"}), 200


@bp.route("/waste-summary", methods=["GET"])
@token_required
def get_waste_summary(user):
    """Get monthly household performance summary."""
    # Get RWA membership
    membership = RwaMembership.query.filter_by(user_id=user.id, is_active=True).first()
    
    if not membership:
        return jsonify({"error": "User is not a member of any RWA"}), 403
    
    rwa_group = membership.rwa_group
    members = RwaMembership.query.filter_by(rwa_group_id=rwa_group.id, is_active=True).all()
    
    # Get current month
    current_month = date.today().replace(day=1)
    
    # Calculate metrics for all households
    household_data = []
    total_households = len(members)
    total_segregated = 0
    total_recycled = 0
    
    for member in members:
        member_user = User.query.get(member.user_id)
        if not member_user:
            continue
        
        # Get waste logs for current month
        month_start = current_month
        if current_month.month == 12:
            month_end = date(current_month.year + 1, 1, 1)
        else:
            month_end = date(current_month.year, current_month.month + 1, 1)
        
        waste_logs = WasteLog.query.filter(
            and_(
                WasteLog.user_id == member_user.id,
                WasteLog.log_date >= month_start,
                WasteLog.log_date < month_end,
                WasteLog.is_active == True
            )
        ).all()
        
        if not waste_logs:
            continue
        
        # Calculate metrics
        total_wet = sum(log.quantity_kg for log in waste_logs if log.category.lower() == "wet")
        total_dry = sum(log.quantity_kg for log in waste_logs if log.category.lower() == "dry")
        total_hazardous = sum(log.quantity_kg for log in waste_logs if log.category.lower() == "hazardous")
        
        segregated_count = len([log for log in waste_logs if log.separated])
        segregation_pct = (segregated_count / len(waste_logs) * 100) if waste_logs else 0
        
        recycled_count = len([log for log in waste_logs if log.recycled])
        recycle_pct = (recycled_count / len(waste_logs) * 100) if waste_logs else 0
        
        family_size = member_user.family_members_count or 1
        per_capita_wet = total_wet / family_size if family_size > 0 else 0
        per_capita_dry = total_dry / family_size if family_size > 0 else 0
        per_capita_hazardous = total_hazardous / family_size if family_size > 0 else 0
        
        # Engagement score (simplified)
        engagement_score = member_user.points
        
        if segregation_pct > 0:
            total_segregated += 1
        if recycle_pct > 0:
            total_recycled += 1
        
        household_data.append({
            "household_number": member_user.house_number or f"HH-{member_user.id}",
            "family_size": family_size,
            "segregation_percentage": round(segregation_pct, 1),
            "per_capita_wet": round(per_capita_wet, 2),
            "per_capita_dry": round(per_capita_dry, 2),
            "per_capita_hazardous": round(per_capita_hazardous, 2),
            "recycle_reuse_donation_percentage": round(recycle_pct, 1),
            "engagement_score": engagement_score
        })
    
    # Overall metrics
    segregation_rate = (total_segregated / total_households * 100) if total_households > 0 else 0
    recycle_rate = (total_recycled / total_households * 100) if total_households > 0 else 0
    
    return jsonify({
        "total_households": total_households,
        "segregation_rate": round(segregation_rate, 1),
        "recycle_reuse_donations_rate": round(recycle_rate, 1),
        "household_details": household_data
    }), 200


@bp.route("/campaigns", methods=["GET"])
@token_required
def get_campaigns(user):
    """Get all campaigns (secondary users can view all)."""
    campaigns = Campaign.query.filter_by(is_active=True).order_by(Campaign.event_datetime).all()
    
    result = []
    for campaign in campaigns:
        result.append({
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "event_datetime": campaign.event_datetime.isoformat() if campaign.event_datetime else None,
            "location": campaign.location,
            "image_url": campaign.image_url,
            "pincode": campaign.pincode
        })
    
    return jsonify({"campaigns": result}), 200


@bp.route("/campaigns/create", methods=["POST"])
@token_required
def create_campaign(user):
    """Create a new campaign."""
    data = request.get_json()
    
    required_fields = ["name", "description", "location", "event_datetime"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        event_datetime = datetime.fromisoformat(data["event_datetime"].replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return jsonify({"error": "Invalid event_datetime format"}), 400
    
    campaign = Campaign(
        name=data["name"],
        description=data["description"],
        location=data["location"],
        event_datetime=event_datetime,
        pincode=data.get("pincode"),
        ward_id=data.get("ward_id"),
        image_url=data.get("image_url")
    )
    
    db.session.add(campaign)
    db.session.commit()
    
    return jsonify({
        "message": "Campaign created successfully",
        "campaign": {
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "event_datetime": campaign.event_datetime.isoformat(),
            "location": campaign.location
        }
    }), 201

