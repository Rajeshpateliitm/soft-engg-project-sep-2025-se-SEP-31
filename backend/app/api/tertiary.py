"""Tertiary user (Government/NGO) endpoints."""
from flask import Blueprint, request, jsonify
from app.models import Ward, WardMonthlySummary, User, WasteLog, db
from app.core.security import token_required
from sqlalchemy import func, and_
from datetime import date, timedelta

bp = Blueprint("tertiary", __name__)


@bp.route("/ward-performance", methods=["GET"])
@token_required
def get_ward_performance(user):
    """Get ward-wise performance summary."""
    # Get all wards
    wards = Ward.query.filter_by(is_active=True).all()
    
    # Get current month
    current_month = date.today().replace(day=1)
    
    ward_data = []
    for ward in wards:
        # Get users in this ward
        users = User.query.filter_by(ward_id=ward.id, is_active=True).all()
        total_households = len(users)
        
        if total_households == 0:
            continue
        
        # Get waste logs for current month
        month_start = current_month
        if current_month.month == 12:
            month_end = date(current_month.year + 1, 1, 1)
        else:
            month_end = date(current_month.year, current_month.month + 1, 1)
        
        user_ids = [u.id for u in users]
        waste_logs = WasteLog.query.filter(
            and_(
                WasteLog.user_id.in_(user_ids),
                WasteLog.log_date >= month_start,
                WasteLog.log_date < month_end,
                WasteLog.is_active == True
            )
        ).all()
        
        # Calculate averages
        total_wet = sum(log.quantity_kg for log in waste_logs if log.category.lower() == "wet")
        total_dry = sum(log.quantity_kg for log in waste_logs if log.category.lower() == "dry")
        total_hazardous = sum(log.quantity_kg for log in waste_logs if log.category.lower() == "hazardous")
        
        # Average per day (assuming 30 days in month)
        days_in_month = 30
        avg_wet_per_day = total_wet / days_in_month if days_in_month > 0 else 0
        avg_dry_per_day = total_dry / days_in_month if days_in_month > 0 else 0
        avg_hazardous_per_day = total_hazardous / days_in_month if days_in_month > 0 else 0
        
        # Segregation compliance
        segregated_logs = len([log for log in waste_logs if log.separated])
        segregation_pct = (segregated_logs / len(waste_logs) * 100) if waste_logs else 0
        
        # Determine remarks
        if segregation_pct >= 80:
            remarks = "Good segregation; increase composting outreach"
        elif segregation_pct >= 60:
            remarks = "Moderate segregation; needs awareness campaigns"
        elif segregation_pct >= 40:
            remarks = "Low segregation; urgent intervention needed"
        else:
            remarks = "Very low segregation; intensive training required"
        
        ward_data.append({
            "ward": f"{ward.ward_number} - {ward.name or ''}",
            "total_households": total_households,
            "avg_wet_waste_kg_per_day": round(avg_wet_per_day, 2),
            "avg_dry_waste_kg_per_day": round(avg_dry_per_day, 2),
            "avg_hazardous_waste_kg_per_day": round(avg_hazardous_per_day, 2),
            "segregation_compliance_pct": round(segregation_pct, 1),
            "remarks": remarks
        })
    
    return jsonify({"ward_performance": ward_data}), 200


@bp.route("/ward/<int:ward_id>/summary", methods=["GET"])
@token_required
def get_ward_summary(user, ward_id):
    """Get detailed summary for a specific ward."""
    ward = Ward.query.get_or_404(ward_id)
    
    months = request.args.get("months", 12, type=int)
    
    # Get summaries for the requested period
    summaries = WardMonthlySummary.query.filter(
        and_(
            WardMonthlySummary.ward_id == ward_id,
            WardMonthlySummary.is_active == True
        )
    ).order_by(
        WardMonthlySummary.year.desc(),
        WardMonthlySummary.month.desc()
    ).limit(months).all()
    
    result = []
    for summary in summaries:
        result.append({
            "year": summary.year,
            "month": summary.month,
            "total_households": summary.total_households,
            "avg_wet_kg_per_day": summary.avg_wet_kg_per_day,
            "avg_dry_kg_per_day": summary.avg_dry_kg_per_day,
            "avg_hazardous_kg_per_day": summary.avg_hazardous_kg_per_day,
            "segregation_compliance_pct": summary.segregation_compliance_pct,
            "remarks": summary.remarks
        })
    
    return jsonify({
        "ward": {
            "id": ward.id,
            "ward_number": ward.ward_number,
            "name": ward.name
        },
        "summaries": result
    }), 200


@bp.route("/ward/<int:ward_id>/update-summary", methods=["POST"])
@token_required
def update_ward_summary(user, ward_id):
    """Create or update ward monthly summary."""
    data = request.get_json()
    
    required_fields = ["year", "month"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Check if summary exists
    summary = WardMonthlySummary.query.filter_by(
        ward_id=ward_id,
        year=data["year"],
        month=data["month"],
        is_active=True
    ).first()
    
    if summary:
        # Update existing
        summary.total_households = data.get("total_households", summary.total_households)
        summary.avg_wet_kg_per_day = data.get("avg_wet_kg_per_day", summary.avg_wet_kg_per_day)
        summary.avg_dry_kg_per_day = data.get("avg_dry_kg_per_day", summary.avg_dry_kg_per_day)
        summary.avg_hazardous_kg_per_day = data.get("avg_hazardous_kg_per_day", summary.avg_hazardous_kg_per_day)
        summary.segregation_compliance_pct = data.get("segregation_compliance_pct", summary.segregation_compliance_pct)
        summary.remarks = data.get("remarks", summary.remarks)
    else:
        # Create new
        summary = WardMonthlySummary(
            ward_id=ward_id,
            year=data["year"],
            month=data["month"],
            total_households=data.get("total_households", 0),
            avg_wet_kg_per_day=data.get("avg_wet_kg_per_day", 0.0),
            avg_dry_kg_per_day=data.get("avg_dry_kg_per_day", 0.0),
            avg_hazardous_kg_per_day=data.get("avg_hazardous_kg_per_day", 0.0),
            segregation_compliance_pct=data.get("segregation_compliance_pct", 0.0),
            remarks=data.get("remarks")
        )
        db.session.add(summary)
    
    db.session.commit()
    
    return jsonify({
        "message": "Ward summary updated successfully",
        "summary": {
            "id": summary.id,
            "ward_id": summary.ward_id,
            "year": summary.year,
            "month": summary.month
        }
    }), 200

