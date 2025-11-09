"""Tertiary user (Government/NGO) endpoints."""
from flask import Blueprint, request, jsonify
from app.models import Ward, WardMonthlySummary, User, WasteLog, UserCategory, db
from app.core.security import token_required
from sqlalchemy import func, and_
from datetime import date, timedelta

bp = Blueprint("tertiary", __name__)


def format_waste(value):
    """Format waste value for display."""
    if value == 0:
        return "0 kg"
    elif value < 1:
        return f"{value:.1f} kg"
    else:
        return f"{value:,.1f} kg"


def get_ward_performance_data():
    """Helper function to calculate ward performance data."""
    # Get all wards
    wards = Ward.query.filter_by(is_active=True).all()
    
    # Get current month
    current_month = date.today().replace(day=1)
    
    # Get PRIMARY user category
    primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
    
    ward_data = []
    for ward in wards:
        # Get primary users in this ward
        if primary_category:
            users = User.query.filter(
                and_(
                    User.ward_id == ward.id,
                    User.user_category_id == primary_category.id,
                    User.is_active == True
                )
            ).all()
        else:
            users = []
        
        total_households = len(users)
        
        # Initialize default values
        total_wet = 0
        total_dry = 0
        total_hazardous = 0
        waste_logs = []
        segregation_pct = 0
        remarks = "No data available - no primary users registered in this ward"
        
        # Only fetch waste logs if there are primary users
        if total_households > 0:
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
            
            # Calculate totals - check category with case-insensitive comparison
            # Categories are stored as "wet", "dry", "hazardous" (lowercase) based on primary.py
            for log in waste_logs:
                if log.category:
                    category_lower = log.category.lower().strip()
                    if category_lower == "wet":
                        total_wet += log.quantity_kg or 0
                    elif category_lower == "dry":
                        total_dry += log.quantity_kg or 0
                    elif category_lower == "hazardous":
                        total_hazardous += log.quantity_kg or 0
            
            # Calculate number of unique days where waste was logged
            unique_log_dates = set(log.log_date for log in waste_logs)
            days_with_logs = len(unique_log_dates) if unique_log_dates else 1  # Use at least 1 to avoid division by zero
            
            # Average per day based on actual days with logs
            # This gives a more accurate representation of daily waste generation
            avg_wet_per_day = total_wet / days_with_logs if days_with_logs > 0 else 0
            avg_dry_per_day = total_dry / days_with_logs if days_with_logs > 0 else 0
            avg_hazardous_per_day = total_hazardous / days_with_logs if days_with_logs > 0 else 0
            
            # Segregation compliance
            segregated_logs = len([log for log in waste_logs if log.separated])
            segregation_pct = (segregated_logs / len(waste_logs) * 100) if waste_logs else 0
            
            # Determine remarks based on compliance
            if waste_logs:
                if segregation_pct >= 85:
                    remarks = "Good segregation; increase composting outreach"
                elif segregation_pct >= 70:
                    remarks = "Moderate performance; improve dry waste recovery"
                elif segregation_pct >= 54:
                    remarks = "Low segregation; run awareness campaign"
                else:
                    remarks = "High wet load; train collectors on waste segregation"
            else:
                remarks = "No waste logs recorded for this month"
        else:
            # No primary users - set all values to 0
            avg_wet_per_day = 0
            avg_dry_per_day = 0
            avg_hazardous_per_day = 0
        
        # Format ward name
        ward_name = f"Ward {ward.ward_number}"
        if ward.name:
            ward_name += f" - {ward.name}"
        
        # Add pincode if available
        ward_details = {
            "id": ward.id,
            "wardNo": ward_name,
            "wardNumber": ward.ward_number,
            "wardName": ward.name or "",
            "pincode": ward.pincode or "",
            "totalHouseholds": total_households,
            "avgWetWaste": format_waste(avg_wet_per_day),
            "avgDryWaste": format_waste(avg_dry_per_day),
            "avgHazardousWaste": format_waste(avg_hazardous_per_day),
            "segregationCompliance": f"{segregation_pct:.0f}%",
            "remarks": remarks,
            # Raw values for calculations
            "_avgWetWaste": avg_wet_per_day,
            "_avgDryWaste": avg_dry_per_day,
            "_avgHazardousWaste": avg_hazardous_per_day,
            "_segregationCompliance": segregation_pct
        }
        
        ward_data.append(ward_details)
    
    return ward_data


@bp.route("/dashboard", methods=["GET"])
@token_required
def get_dashboard(user):
    """Get tertiary user dashboard with all statistics."""
    # Verify user is a tertiary user
    if not user.user_category or user.user_category.key != "TERTIARY":
        return jsonify({"error": "Access denied. Tertiary user access required."}), 403
    
    # Get ward performance data
    ward_data = get_ward_performance_data()
    
    # Calculate overall statistics
    total_wards = len(ward_data)
    total_households = sum(ward["totalHouseholds"] for ward in ward_data)
    
    # Calculate average segregation compliance
    compliance_values = [ward["_segregationCompliance"] for ward in ward_data if ward["totalHouseholds"] > 0]
    average_compliance = sum(compliance_values) / len(compliance_values) if compliance_values else 0
    
    # Calculate total daily waste collection
    total_wet_waste = sum(ward["_avgWetWaste"] for ward in ward_data)
    total_dry_waste = sum(ward["_avgDryWaste"] for ward in ward_data)
    total_hazardous_waste = sum(ward["_avgHazardousWaste"] for ward in ward_data)
    
    # Calculate performance indicators
    excellent_count = len([w for w in ward_data if w["_segregationCompliance"] >= 85])
    good_count = len([w for w in ward_data if 70 <= w["_segregationCompliance"] < 85])
    needs_improvement_count = len([w for w in ward_data if w["_segregationCompliance"] < 70])
    
    # Generate priority actions (wards with lowest compliance first)
    sorted_wards = sorted(ward_data, key=lambda x: x["_segregationCompliance"])
    priority_actions = []
    
    for ward in sorted_wards[:4]:  # Top 4 priority actions
        if ward["_segregationCompliance"] < 70:
            priority = "High"
        elif ward["_segregationCompliance"] < 85:
            priority = "Medium"
        else:
            priority = "Low"
        
        priority_actions.append({
            "ward": ward["wardNo"],
            "description": ward["remarks"],
            "priority": priority
        })
    
    return jsonify({
        "wardData": ward_data,
        "totalWards": total_wards,
        "totalHouseholds": total_households,
        "averageCompliance": round(average_compliance, 1),
        "totalWetWaste": round(total_wet_waste, 0),
        "totalDryWaste": round(total_dry_waste, 0),
        "totalHazardousWaste": round(total_hazardous_waste, 0),
        "excellentCount": excellent_count,
        "goodCount": good_count,
        "needsImprovementCount": needs_improvement_count,
        "priorityActions": priority_actions
    }), 200


@bp.route("/ward-performance", methods=["GET"])
@token_required
def get_ward_performance(user):
    """Get ward-wise performance summary."""
    # Verify user is a tertiary user
    if not user.user_category or user.user_category.key != "TERTIARY":
        return jsonify({"error": "Access denied. Tertiary user access required."}), 403
    
    ward_data = get_ward_performance_data()
    
    # Return in the format expected by the old endpoint
    ward_performance = []
    for ward in ward_data:
        ward_performance.append({
            "ward": ward["wardNo"],
            "total_households": ward["totalHouseholds"],
            "avg_wet_waste_kg_per_day": ward["_avgWetWaste"],
            "avg_dry_waste_kg_per_day": ward["_avgDryWaste"],
            "avg_hazardous_waste_kg_per_day": ward["_avgHazardousWaste"],
            "segregation_compliance_pct": ward["_segregationCompliance"],
            "remarks": ward["remarks"]
        })
    
    return jsonify({"ward_performance": ward_performance}), 200


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

