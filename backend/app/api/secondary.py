"""Secondary user (RWA/Collector) endpoints."""
from flask import Blueprint, request, jsonify
from app.models import (
    User, UserCategory, Ward, RwaGroup, RwaMembership, PickupRequest, WasteLog,
    Campaign, CampaignRegistration, Engagement, db
)
from app.core.security import token_required
from sqlalchemy import func, desc, and_, or_
from datetime import datetime, date, timedelta

bp = Blueprint("secondary", __name__)


def get_primary_users_for_secondary_user(user):
    """Helper function to get primary users in the same area as secondary user."""
    secondary_ward_id = user.ward_id
    secondary_pincode = user.pincode
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    
    if not primary_category:
        return []
    
    if secondary_ward_id:
        primary_users = User.query.filter(
            and_(
                User.user_category_id == primary_category.id,
                User.ward_id == secondary_ward_id,
                User.is_active == True
            )
        ).all()
        return primary_users
    elif secondary_pincode:
        primary_users = User.query.filter(
            and_(
                User.user_category_id == primary_category.id,
                User.pincode == secondary_pincode,
                User.is_active == True
            )
        ).all()
        return primary_users
    
    return []


@bp.route("/dashboard", methods=["GET"])
@token_required
def get_dashboard(user):
    """Get RWA manager dashboard - only for users with admin role in RWA."""
    # Get RWA membership (if exists)
    membership = RwaMembership.query.filter_by(user_id=user.id, is_active=True).first()
    
    # Check if user is an RWA admin, if not return error or collector dashboard redirect
    if not membership or membership.role != "admin":
        return jsonify({
            "error": "This dashboard is for RWA managers only. Collectors should use the collector dashboard.",
            "user_role": membership.role if membership else None,
            "redirect_to": "collector-dashboard"
        }), 403
    
    rwa_group = membership.rwa_group
    secondary_ward_id = user.ward_id
    
    # RWA Leaderboard rank - calculate based on all primary users in the ward
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    rwa_groups = RwaGroup.query.filter_by(is_active=True).all()
    rwa_scores = []
    for group in rwa_groups:
        # Get ward for this RWA group
        ward = None
        if group.ward_number:
            ward = Ward.query.filter_by(ward_number=group.ward_number).first()
        
        # Get all primary users in this RWA's ward
        total_points = 0
        if ward and primary_category:
            primary_users = User.query.filter(
                and_(
                    User.user_category_id == primary_category.id,
                    User.ward_id == ward.id,
                    User.is_active == True
                )
            ).all()
            total_points = sum(u.points for u in primary_users)
        
        rwa_scores.append((group.id, total_points))
    
    rwa_scores.sort(key=lambda x: x[1], reverse=True)
    rwa_rank = next((idx + 1 for idx, (gid, _) in enumerate(rwa_scores) if gid == rwa_group.id), len(rwa_scores))
    
    # Household count - count primary users in the same ward
    household_count = 0
    if primary_category:
        household_count = User.query.filter(
            and_(
                User.user_category_id == primary_category.id,
                User.ward_id == secondary_ward_id,
                User.is_active == True
            )
        ).count()
    
    return jsonify({
        "user_role": "rwa_manager",
        "rwa_leaderboard": {
            "rank": rwa_rank,
            "households": household_count,
            "rwa_name": rwa_group.name if rwa_group else None
        }
    }), 200


@bp.route("/collector/dashboard", methods=["GET"])
@token_required
def get_collector_dashboard(user):
    """Get collector dashboard - only pickup-related data."""
    # Get RWA membership to verify user is a collector
    membership = RwaMembership.query.filter_by(user_id=user.id, is_active=True).first()
    
    # Verify user is a collector (role == "collector")
    if not membership or membership.role != "collector":
        return jsonify({
            "error": "This dashboard is for waste collectors only.",
            "user_role": membership.role if membership else None
        }), 403
    
    # Get primary users in the same area
    primary_users = get_primary_users_for_secondary_user(user)
    primary_user_ids = [u.id for u in primary_users]
    
    # Today's pickup summary
    today = date.today()
    pickup_query = PickupRequest.query.filter(
        and_(
            func.date(PickupRequest.scheduled_at) == today,
            PickupRequest.is_active == True
        )
    )
    
    if primary_user_ids:
        pickup_query = pickup_query.filter(PickupRequest.requester_id.in_(primary_user_ids))
    else:
        pickup_query = pickup_query.filter(False)
    
    today_pickups = pickup_query.all()
    
    total_pickups = len(today_pickups)
    completed = len([p for p in today_pickups if p.status in ["completed", "accepted"]])
    pending = len([p for p in today_pickups if p.status == "pending"])
    accepted = len([p for p in today_pickups if p.status == "accepted"])
    rejected = len([p for p in today_pickups if p.status == "rejected"])
    
    # Get ward information
    ward = None
    if user.ward_id:
        ward = Ward.query.get(user.ward_id)
    
    return jsonify({
        "user_role": "collector",
        "ward": {
            "id": ward.id if ward else None,
            "name": ward.name if ward else None,
            "ward_number": ward.ward_number if ward else None,
            "pincode": ward.pincode if ward else user.pincode
        },
        "pickup_summary": {
            "date": today.isoformat(),
            "total_pickups": total_pickups,
            "completed": completed,
            "pending": pending,
            "accepted": accepted,
            "rejected": rejected,
            "left": total_pickups - completed
        },
        "household_count": len(primary_users)
    }), 200


@bp.route("/rwa-leaderboard", methods=["GET"])
@token_required
def get_rwa_leaderboard(user):
    """Get RWA leaderboard - includes all primary users in each RWA's ward."""
    rwa_groups = RwaGroup.query.filter_by(is_active=True).all()
    
    # Get PRIMARY user category
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    
    rwa_data = []
    for group in rwa_groups:
        # Get ward for this RWA group
        ward = None
        if group.ward_number:
            ward = Ward.query.filter_by(ward_number=group.ward_number).first()
        
        # Calculate total points from all primary users in this ward
        total_points = 0
        if ward and primary_category:
            primary_users = User.query.filter(
                and_(
                    User.user_category_id == primary_category.id,
                    User.ward_id == ward.id,
                    User.is_active == True
                )
            ).all()
            total_points = sum(u.points for u in primary_users)
        
        rwa_data.append({
            "rwa_id": group.id,
            "rwa_name": group.name,
            "ward_number": group.ward_number,
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
    """Get monthly pickup summary - filtered by secondary user's ward/pincode."""
    months = request.args.get("months", 1, type=int)
    
    # Get secondary user's ward and pincode
    secondary_ward_id = user.ward_id
    secondary_pincode = user.pincode
    
    # Get PRIMARY user category
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    
    if not primary_category:
        return jsonify({"error": "Primary user category not found"}), 500
    
    # Get primary users in secondary user's area
    primary_user_ids = []
    if secondary_ward_id:
        primary_users = User.query.filter(
            and_(
                User.user_category_id == primary_category.id,
                User.ward_id == secondary_ward_id,
                User.is_active == True
            )
        ).all()
        primary_user_ids = [u.id for u in primary_users]
    elif secondary_pincode:
        primary_users = User.query.filter(
            and_(
                User.user_category_id == primary_category.id,
                User.pincode == secondary_pincode,
                User.is_active == True
            )
        ).all()
        primary_user_ids = [u.id for u in primary_users]
    
    # Calculate date range (last 30 days)
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    # Filter pickups by date and primary users in the area
    pickup_query = PickupRequest.query.filter(
        and_(
            func.date(PickupRequest.scheduled_at) >= start_date,
            func.date(PickupRequest.scheduled_at) <= end_date,
            PickupRequest.is_active == True
        )
    )
    
    if primary_user_ids:
        pickup_query = pickup_query.filter(PickupRequest.requester_id.in_(primary_user_ids))
    else:
        # No primary users in area - return empty data
        return jsonify({
            "total_scheduled": 0,
            "total_completed": 0,
            "total_pending": 0,
            "total_rejected": 0,
            "total_waste_collected": 0,
            "average_daily_pickup": 0,
            "completion_rate": 0,
            "rejection_rate": 0,
            "pending_rate": 0,
            "peak_pickup_day": None,
            "lowest_pickup_day": None,
            "waste_type_distribution": {
                "wet": 0,
                "dry": 0,
                "hazardous": 0
            },
            "daily_breakdown": {}
        }), 200
    
    pickups = pickup_query.all()
    
    # Calculate pickup statistics
    # Note: "accepted" and "completed" are treated as the same - both mean the pickup was accepted/completed
    total_scheduled = len(pickups)
    total_completed = len([p for p in pickups if p.status in ["completed", "accepted"]])
    total_pending = len([p for p in pickups if p.status == "pending"])
    total_rejected = len([p for p in pickups if p.status == "rejected"])
    total_accepted = len([p for p in pickups if p.status == "accepted"])
    
    # Calculate rates (completed includes both accepted and completed statuses)
    completion_rate = round((total_completed / total_scheduled * 100), 2) if total_scheduled > 0 else 0
    rejection_rate = round((total_rejected / total_scheduled * 100), 2) if total_scheduled > 0 else 0
    pending_rate = round((total_pending / total_scheduled * 100), 2) if total_scheduled > 0 else 0
    
    # Calculate total waste (from all scheduled pickup requests)
    # This represents all waste that was logged/requested for pickup
    total_waste_collected = sum([float(p.quantity) for p in pickups if p.quantity])
    average_daily_pickup = round(total_waste_collected / 30, 2) if 30 > 0 else 0
    
    # Get waste logs for the same period to calculate waste type distribution
    waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id.in_(primary_user_ids),
            WasteLog.log_date >= start_date,
            WasteLog.log_date <= end_date,
            WasteLog.is_active == True
        )
    ).all()
    
    # Calculate waste type distribution
    wet_waste = sum([log.quantity_kg for log in waste_logs if log.category.lower() == "wet"])
    dry_waste = sum([log.quantity_kg for log in waste_logs if log.category.lower() == "dry"])
    hazardous_waste = sum([log.quantity_kg for log in waste_logs if log.category.lower() == "hazardous"])
    total_waste_from_logs = wet_waste + dry_waste + hazardous_waste
    
    # Calculate percentages for waste type distribution
    waste_type_distribution = {
        "wet": round((wet_waste / total_waste_from_logs * 100), 1) if total_waste_from_logs > 0 else 0,
        "dry": round((dry_waste / total_waste_from_logs * 100), 1) if total_waste_from_logs > 0 else 0,
        "hazardous": round((hazardous_waste / total_waste_from_logs * 100), 1) if total_waste_from_logs > 0 else 0
    }
    
    # Daily pickups by status with waste quantities
    daily_data = {}
    daily_waste_totals = {}  # Track waste per day
    
    for i in range(30):
        day = end_date - timedelta(days=i)
        day_str = day.isoformat()
        day_pickups = [p for p in pickups if p.scheduled_at and p.scheduled_at.date() == day]
        
        # Calculate waste for this day (from all pickups for that day)
        day_waste = sum([float(p.quantity) for p in day_pickups if p.quantity])
        daily_waste_totals[day_str] = day_waste
        
        # Count completed as both accepted and completed statuses (they mean the same thing)
        completed_count = len([p for p in day_pickups if p.status in ["completed", "accepted"]])
        
        daily_data[day_str] = {
            "completed": completed_count,  # Includes both accepted and completed
            "pending": len([p for p in day_pickups if p.status == "pending"]),
            "accepted": len([p for p in day_pickups if p.status == "accepted"]),  # Keep for reference
            "rejected": len([p for p in day_pickups if p.status == "rejected"]),
            "scheduled": len(day_pickups),
            "waste_kg": round(day_waste, 2)
        }
    
    # Find peak and lowest pickup days
    peak_pickup_day = None
    lowest_pickup_day = None
    peak_waste = 0
    lowest_waste = float('inf')
    
    for day_str, waste_amount in daily_waste_totals.items():
        if waste_amount > peak_waste:
            peak_waste = waste_amount
            peak_pickup_day = {
                "date": day_str,
                "waste_kg": round(waste_amount, 2),
                "pickup_count": daily_data[day_str]["scheduled"]
            }
        if waste_amount < lowest_waste and waste_amount > 0:
            lowest_waste = waste_amount
            lowest_pickup_day = {
                "date": day_str,
                "waste_kg": round(waste_amount, 2),
                "pickup_count": daily_data[day_str]["scheduled"]
            }
    
    # If no waste was collected, set lowest to None
    if lowest_waste == float('inf'):
        lowest_pickup_day = None
    
    return jsonify({
        "total_scheduled": total_scheduled,
        "total_completed": total_completed,
        "total_pending": total_pending,
        "total_rejected": total_rejected,
        "total_waste_collected": round(total_waste_collected, 2),
        "average_daily_pickup": average_daily_pickup,
        "completion_rate": completion_rate,
        "rejection_rate": rejection_rate,
        "pending_rate": pending_rate,
        "peak_pickup_day": peak_pickup_day,
        "lowest_pickup_day": lowest_pickup_day,
        "waste_type_distribution": waste_type_distribution,
        "daily_breakdown": daily_data
    }), 200


@bp.route("/pickup-details", methods=["GET"])
@token_required
def get_pickup_details(user):
    """Get daily pickup details - filtered by secondary user's ward/pincode."""
    date_str = request.args.get("date", date.today().isoformat())
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    # Get secondary user's ward and pincode
    secondary_ward_id = user.ward_id
    secondary_pincode = user.pincode
    
    # Get PRIMARY user category
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    
    # Get primary users in secondary user's area
    primary_user_ids = []
    if secondary_ward_id and primary_category:
        primary_users = User.query.filter(
            and_(
                User.user_category_id == primary_category.id,
                User.ward_id == secondary_ward_id,
                User.is_active == True
            )
        ).all()
        primary_user_ids = [u.id for u in primary_users]
    elif secondary_pincode and primary_category:
        primary_users = User.query.filter(
            and_(
                User.user_category_id == primary_category.id,
                User.pincode == secondary_pincode,
                User.is_active == True
            )
        ).all()
        primary_user_ids = [u.id for u in primary_users]
    
    # Filter pickups by date and primary users in the area
    pickup_query = PickupRequest.query.filter(
        and_(
            func.date(PickupRequest.scheduled_at) == target_date,
            PickupRequest.is_active == True
        )
    )
    
    if primary_user_ids:
        pickup_query = pickup_query.filter(PickupRequest.requester_id.in_(primary_user_ids))
    else:
        # If no primary users in area, return empty list
        return jsonify({
            "date": target_date.isoformat(),
            "pickups": []
        }), 200
    
    pickups = pickup_query.order_by(PickupRequest.scheduled_at).all()
    
    result = []
    for pickup in pickups:
        requester = User.query.get(pickup.requester_id)
        if not requester:
            continue  # Skip if requester not found
        
        # Use pickup_location if available, otherwise build it from requester info
        if pickup.pickup_location:
            pickup_location = pickup.pickup_location
        else:
            # Build location from requester information with ward
            location_parts = []
            if requester.house_number:
                location_parts.append(requester.house_number)
            else:
                location_parts.append(requester.username or requester.email.split('@')[0] if requester.email else "N/A")
            
            # Add ward information if available
            if requester.ward_id:
                ward = Ward.query.get(requester.ward_id)
                if ward:
                    ward_display = ward.name if ward.name else f"Ward {ward.ward_number}"
                    location_parts.append(ward_display)
            
            # Add pincode
            if requester.pincode:
                location_parts.append(requester.pincode)
            
            pickup_location = ", ".join(location_parts) if location_parts else "N/A"
            
        result.append({
            "pickup_id": pickup.id,
            "request_no": pickup.request_code or f"REQ-{pickup.id}",
            "user_id": pickup.requester_id,
            "user_name": requester.username or requester.email.split('@')[0] if requester.email else "Unknown",
            "user_email": requester.email if requester else "N/A",
            "house_number": requester.house_number if requester else "N/A",
            "pickup_location": pickup_location,
            "date_of_pickup": pickup.scheduled_at.date().isoformat() if pickup.scheduled_at else None,
            "time_of_pickup": pickup.scheduled_at.time().isoformat()[:5] if pickup.scheduled_at else None,  # Format as HH:MM
            "disposal_quantity": float(pickup.quantity) if pickup.quantity else 0.0,
            "status": pickup.status or "pending"
        })
    
    return jsonify({
        "date": target_date.isoformat(),
        "pickups": result
    }), 200


@bp.route("/pickup/<int:pickup_id>/accept", methods=["POST"])
@token_required
def accept_pickup(user, pickup_id):
    """Accept a pickup request - only for collectors. Awards points to the primary user."""
    # Verify user is a collector
    membership = RwaMembership.query.filter_by(user_id=user.id, is_active=True).first()
    if not membership or membership.role != "collector":
        return jsonify({
            "error": "Only waste collectors can accept pickup requests. RWA managers have read-only access."
        }), 403
    
    pickup = PickupRequest.query.get_or_404(pickup_id)
    
    if pickup.status != "pending":
        return jsonify({"error": "Pickup request is not pending"}), 400
    
    # Find related waste logs by pickup_request_id stored in notes
    waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id == pickup.requester_id,
            WasteLog.is_active == True,
            WasteLog.notes.like(f"%PICKUP_REQ_ID:{pickup_id}%")
        )
    ).all()
    
    # Award points based on waste log data
    points_awarded = 0
    if waste_logs:
        # Get the first waste log to check separated/recycled flags
        # (all waste logs for the same pickup request should have the same flags)
        first_log = waste_logs[0]
        if first_log.separated:
            points_awarded += 5
        if first_log.recycled:
            points_awarded += 10
        
        # Award points to the requester
        requester = User.query.get(pickup.requester_id)
        if requester:
            requester.points += points_awarded
    
    # Update pickup request status
    pickup.status = "accepted"
    pickup.assigned_collector_id = user.id
    pickup.decision_by_user_id = user.id
    pickup.decision_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        "message": "Pickup request accepted",
        "points_awarded": points_awarded
    }), 200


@bp.route("/pickup/<int:pickup_id>/reject", methods=["POST"])
@token_required
def reject_pickup(user, pickup_id):
    """Reject a pickup request - only for collectors. Deducts 5 points from the primary user."""
    # Verify user is a collector
    membership = RwaMembership.query.filter_by(user_id=user.id, is_active=True).first()
    if not membership or membership.role != "collector":
        return jsonify({
            "error": "Only waste collectors can reject pickup requests. RWA managers have read-only access."
        }), 403
    
    pickup = PickupRequest.query.get_or_404(pickup_id)
    
    if pickup.status != "pending":
        return jsonify({"error": "Pickup request is not pending"}), 400
    
    # Deduct 5 points from the requester
    requester = User.query.get(pickup.requester_id)
    if requester:
        requester.points = max(0, requester.points - 5)  # Ensure points don't go below 0
    
    # Update pickup request status
    pickup.status = "rejected"
    pickup.decision_by_user_id = user.id
    pickup.decision_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        "message": "Pickup request rejected",
        "points_deducted": 5
    }), 200


@bp.route("/waste-summary", methods=["GET"])
@token_required
def get_waste_summary(user):
    """Get monthly household performance summary - shows primary users in secondary user's ward."""
    # Get secondary user's ward and pincode
    secondary_ward_id = user.ward_id
    secondary_pincode = user.pincode
    
    # Get PRIMARY user category
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    
    if not primary_category:
        return jsonify({"error": "Primary user category not found"}), 500
    
    # Get all primary users in secondary user's area
    primary_users_query = User.query.filter(
        and_(
            User.user_category_id == primary_category.id,
            User.is_active == True
        )
    )
    
    if secondary_ward_id:
        primary_users_query = primary_users_query.filter(User.ward_id == secondary_ward_id)
    elif secondary_pincode:
        primary_users_query = primary_users_query.filter(User.pincode == secondary_pincode)
    else:
        return jsonify({"error": "Secondary user must have ward or pincode assigned"}), 400
    
    primary_users = primary_users_query.all()
    
    # Get current month date range
    today = date.today()
    month_start = today.replace(day=1)
    if month_start.month == 12:
        month_end = date(month_start.year + 1, 1, 1)
    else:
        month_end = date(month_start.year, month_start.month + 1, 1)
    
    # Calculate number of days in current month (for per capita per day calculation)
    days_in_month = (month_end - month_start).days
    
    # Aggregate metrics across all households for overall rates
    all_waste_logs = []
    total_households = len(primary_users)
    
    # Calculate metrics for each household
    household_data = []
    
    for primary_user in primary_users:
        # Get waste logs for current month
        waste_logs = WasteLog.query.filter(
            and_(
                WasteLog.user_id == primary_user.id,
                WasteLog.log_date >= month_start,
                WasteLog.log_date < month_end,
                WasteLog.is_active == True
            )
        ).all()
        
        # Add to aggregate list for overall metrics
        all_waste_logs.extend(waste_logs)
        
        family_size = primary_user.family_members_count or 1
        
        if not waste_logs:
            # Still include household even if no waste logs
            household_data.append({
                "household_number": primary_user.house_number or f"HH-{primary_user.id}",
                "user_id": primary_user.id,
                "family_size": family_size,
                "segregation_percentage": 0.0,
                "per_capita_wet": 0.0,
                "per_capita_dry": 0.0,
                "per_capita_hazardous": 0.0,
                "recycle_reuse_donation_percentage": 0.0,
                "engagement_score": round(float(primary_user.points or 0), 1)
            })
            continue
        
        # Calculate total waste by category for this household
        total_wet = sum(log.quantity_kg for log in waste_logs if log.category and log.category.lower() == "wet")
        total_dry = sum(log.quantity_kg for log in waste_logs if log.category and log.category.lower() == "dry")
        total_hazardous = sum(log.quantity_kg for log in waste_logs if log.category and log.category.lower() == "hazardous")
        
        # Calculate segregation percentage for this household
        segregated_logs = [log for log in waste_logs if log.separated]
        segregation_pct = (len(segregated_logs) / len(waste_logs) * 100) if waste_logs else 0.0
        
        # Calculate recycle/reuse/donation percentage for this household
        recycled_logs = [log for log in waste_logs if log.recycled]
        recycle_pct = (len(recycled_logs) / len(waste_logs) * 100) if waste_logs else 0.0
        
        # Calculate per capita waste per day (divide total by family size and days in month)
        per_capita_wet_per_day = (total_wet / family_size / days_in_month) if family_size > 0 and days_in_month > 0 else 0.0
        per_capita_dry_per_day = (total_dry / family_size / days_in_month) if family_size > 0 and days_in_month > 0 else 0.0
        per_capita_hazardous_per_day = (total_hazardous / family_size / days_in_month) if family_size > 0 and days_in_month > 0 else 0.0
        
        # Engagement score - use user points
        engagement_score = round(float(primary_user.points or 0), 1)
        
        household_data.append({
            "household_number": primary_user.house_number or f"HH-{primary_user.id}",
            "user_id": primary_user.id,
            "family_size": family_size,
            "segregation_percentage": round(segregation_pct, 1),
            "per_capita_wet": round(per_capita_wet_per_day, 2),
            "per_capita_dry": round(per_capita_dry_per_day, 2),
            "per_capita_hazardous": round(per_capita_hazardous_per_day, 2),
            "recycle_reuse_donation_percentage": round(recycle_pct, 1),
            "engagement_score": engagement_score
        })
    
    # Calculate overall metrics from all waste logs
    overall_segregation_rate = 0.0
    overall_recycle_rate = 0.0
    
    if all_waste_logs:
        segregated_count = len([log for log in all_waste_logs if log.separated])
        overall_segregation_rate = (segregated_count / len(all_waste_logs) * 100)
        
        recycled_count = len([log for log in all_waste_logs if log.recycled])
        overall_recycle_rate = (recycled_count / len(all_waste_logs) * 100)
    
    return jsonify({
        "total_households": total_households,
        "segregation_rate": round(overall_segregation_rate, 1),
        "recycle_reuse_donations_rate": round(overall_recycle_rate, 1),
        "household_details": household_data
    }), 200


@bp.route("/campaigns", methods=["GET"])
@token_required
def get_campaigns(user):
    """Get all campaigns (secondary users can view all)."""
    campaigns = Campaign.query.filter_by(is_active=True).order_by(Campaign.event_datetime).all()
    
    result = []
    for campaign in campaigns:
        # Count registrations
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
            "image_url": campaign.image_url,
            "pincode": campaign.pincode,
            "ward_id": campaign.ward_id,
            "registration_count": registration_count
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
        # Handle both ISO format and date+time format
        event_datetime_str = data["event_datetime"]
        if "T" in event_datetime_str:
            # ISO format: "2024-02-15T10:00:00" or "2024-02-15T10:00:00Z"
            event_datetime = datetime.fromisoformat(event_datetime_str.replace("Z", "+00:00"))
        elif " " in event_datetime_str:
            # Format: "YYYY-MM-DD HH:MM" or "YYYY-MM-DD HH:MM:SS"
            try:
                event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
        else:
            return jsonify({"error": "Invalid event_datetime format. Use YYYY-MM-DD HH:MM or ISO format"}), 400
    except (ValueError, AttributeError) as e:
        return jsonify({"error": f"Invalid event_datetime format: {str(e)}"}), 400
    
    # Validate that event_datetime is not in the past
    now = datetime.now()
    if event_datetime < now:
        return jsonify({"error": "Event date and time cannot be in the past. Please select a current or future date and time."}), 400
    
    # Get ward_id from secondary user if not provided
    ward_id = data.get("ward_id") or user.ward_id
    pincode = data.get("pincode") or user.pincode
    
    campaign = Campaign(
        name=data["name"],
        description=data["description"],
        location=data["location"],
        event_datetime=event_datetime,
        pincode=pincode,
        ward_id=ward_id,
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
            "location": campaign.location,
            "image_url": campaign.image_url
        }
    }), 201


@bp.route("/campaigns/<int:campaign_id>", methods=["PUT"])
@token_required
def update_campaign(user, campaign_id):
    """Update an existing campaign."""
    campaign = Campaign.query.get_or_404(campaign_id)
    data = request.get_json()
    
    if data.get("name"):
        campaign.name = data["name"]
    if data.get("description"):
        campaign.description = data["description"]
    if data.get("location"):
        campaign.location = data["location"]
    if data.get("event_datetime"):
        try:
            event_datetime_str = data["event_datetime"]
            if "T" in event_datetime_str:
                event_datetime = datetime.fromisoformat(event_datetime_str.replace("Z", "+00:00"))
            elif " " in event_datetime_str:
                try:
                    event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
            else:
                return jsonify({"error": "Invalid event_datetime format. Use YYYY-MM-DD HH:MM or ISO format"}), 400
            
            # Validate that event_datetime is not in the past
            now = datetime.now()
            if event_datetime < now:
                return jsonify({"error": "Event date and time cannot be in the past. Please select a current or future date and time."}), 400
            
            campaign.event_datetime = event_datetime
        except (ValueError, AttributeError) as e:
            return jsonify({"error": f"Invalid event_datetime format: {str(e)}"}), 400
    if data.get("pincode"):
        campaign.pincode = data["pincode"]
    if data.get("ward_id"):
        campaign.ward_id = data["ward_id"]
    if data.get("image_url") is not None:
        campaign.image_url = data["image_url"]
    
    db.session.commit()
    
    return jsonify({
        "message": "Campaign updated successfully",
        "campaign": {
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "event_datetime": campaign.event_datetime.isoformat() if campaign.event_datetime else None,
            "location": campaign.location,
            "image_url": campaign.image_url
        }
    }), 200


@bp.route("/campaigns/<int:campaign_id>", methods=["DELETE"])
@token_required
def delete_campaign(user, campaign_id):
    """Delete (deactivate) a campaign."""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # Soft delete - set is_active to False
    campaign.is_active = False
    db.session.commit()
    
    return jsonify({"message": "Campaign deleted successfully"}), 200


@bp.route("/waste-logs", methods=["GET"])
@token_required
def get_waste_logs(user):
    """Get waste logs from primary users in secondary user's ward for a specific date."""
    date_str = request.args.get("date", date.today().isoformat())
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    # Get secondary user's ward and pincode
    secondary_ward_id = user.ward_id
    secondary_pincode = user.pincode
    
    # Get PRIMARY user category
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    
    if not primary_category:
        return jsonify({"error": "Primary user category not found"}), 500
    
    # Get all primary users in secondary user's area
    primary_users_query = User.query.filter(
        and_(
            User.user_category_id == primary_category.id,
            User.is_active == True
        )
    )
    
    if secondary_ward_id:
        primary_users_query = primary_users_query.filter(User.ward_id == secondary_ward_id)
    elif secondary_pincode:
        primary_users_query = primary_users_query.filter(User.pincode == secondary_pincode)
    else:
        return jsonify({"error": "Secondary user must have ward or pincode assigned"}), 400
    
    primary_users = primary_users_query.all()
    
    # Get waste logs for the target date from these primary users
    primary_user_ids = [u.id for u in primary_users]
    
    waste_logs = WasteLog.query.filter(
        and_(
            WasteLog.user_id.in_(primary_user_ids),
            WasteLog.log_date == target_date,
            WasteLog.is_active == True
        )
    ).order_by(WasteLog.user_id, WasteLog.category).all()
    
    # Group waste logs by household (user)
    household_waste = {}
    for log in waste_logs:
        user_id = log.user_id
        if user_id not in household_waste:
            # Get user details
            log_user = User.query.get(user_id)
            household_waste[user_id] = {
                "user_id": user_id,
                "user_name": log_user.username if log_user else "Unknown",
                "user_email": log_user.email if log_user else "N/A",
                "house_number": log_user.house_number if log_user else "N/A",
                "pincode": log_user.pincode if log_user else "N/A",
                "family_members": log_user.family_members_count or 1,
                "wet_waste": 0,
                "dry_waste": 0,
                "hazardous_waste": 0,
                "total_waste": 0,
                "separated": False,
                "recycled": False,
                "has_logged": False,
                "questions_doubts": None,
                "feedback": None
            }
        
        # Add waste quantities by category
        category = log.category.lower()
        if category == "wet":
            household_waste[user_id]["wet_waste"] += log.quantity_kg
        elif category == "dry":
            household_waste[user_id]["dry_waste"] += log.quantity_kg
        elif category == "hazardous":
            household_waste[user_id]["hazardous_waste"] += log.quantity_kg
        
        household_waste[user_id]["total_waste"] += log.quantity_kg
        household_waste[user_id]["has_logged"] = True
        
        # Update separated and recycled flags (if any log has these set)
        if log.separated:
            household_waste[user_id]["separated"] = True
        if log.recycled:
            household_waste[user_id]["recycled"] = True
        
        # Store questions/doubts and feedback (from last log entry)
        if log.questions_doubts:
            household_waste[user_id]["questions_doubts"] = log.questions_doubts
        if log.feedback:
            household_waste[user_id]["feedback"] = log.feedback
    
    # Include households that haven't logged waste for this date
    for primary_user in primary_users:
        if primary_user.id not in household_waste:
            household_waste[primary_user.id] = {
                "user_id": primary_user.id,
                "user_name": primary_user.username or "Unknown",
                "user_email": primary_user.email or "N/A",
                "house_number": primary_user.house_number or "N/A",
                "pincode": primary_user.pincode or "N/A",
                "family_members": primary_user.family_members_count or 1,
                "wet_waste": 0,
                "dry_waste": 0,
                "hazardous_waste": 0,
                "total_waste": 0,
                "separated": False,
                "recycled": False,
                "has_logged": False,
                "questions_doubts": None,
                "feedback": None
            }
    
    # Convert to list and sort by house number or user name
    result = list(household_waste.values())
    result.sort(key=lambda x: (x["house_number"] or x["user_name"]))
    
    # Calculate summary statistics
    total_households = len(result)
    households_logged = len([h for h in result if h["has_logged"]])
    total_wet = sum(h["wet_waste"] for h in result)
    total_dry = sum(h["dry_waste"] for h in result)
    total_hazardous = sum(h["hazardous_waste"] for h in result)
    total_waste = total_wet + total_dry + total_hazardous
    households_separated = len([h for h in result if h["separated"]])
    households_recycled = len([h for h in result if h["recycled"]])
    
    return jsonify({
        "date": target_date.isoformat(),
        "summary": {
            "total_households": total_households,
            "households_logged": households_logged,
            "households_not_logged": total_households - households_logged,
            "total_wet_waste": round(total_wet, 2),
            "total_dry_waste": round(total_dry, 2),
            "total_hazardous_waste": round(total_hazardous, 2),
            "total_waste": round(total_waste, 2),
            "households_separated": households_separated,
            "households_recycled": households_recycled
        },
        "household_waste": result
    }), 200

