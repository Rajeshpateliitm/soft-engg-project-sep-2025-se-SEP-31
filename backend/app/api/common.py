"""Common endpoints for all users."""
from flask import Blueprint, request, jsonify
from app.models import RecyclerLocation, Ward, PickupRequest, db
from app.core.security import token_required
from datetime import datetime
from sqlalchemy import or_, and_

bp = Blueprint("common", __name__)


@bp.route("/recyclers", methods=["GET"])
def get_recyclers():
    """Get recycler locations by pincode."""
    pincode = request.args.get("pincode")
    
    if not pincode:
        return jsonify({"error": "Pincode required"}), 400
    
    recyclers = RecyclerLocation.query.filter(
        and_(
            RecyclerLocation.pincode == pincode,
            RecyclerLocation.is_active == True
        )
    ).all()
    
    # Mapping of recycler names to materials they recycle (can be moved to database later)
    materials_mapping = {
        "GreenCycle Recyclers": ["Paper", "Plastics"],
        "Hazardous E-Waste Solutions Hub": ["Electronics"],
        "Goonj": ["Clothes"],
        "Green Recyclers": ["Paper", "Plastics", "Metal"],
        "Eco Waste Solutions": ["Plastics", "Glass", "Metal"],
        "EcoRecycle Solutions": ["Plastic", "Paper", "Metal"],
        "Green Earth Recyclers": ["Organic", "Inorganic", "Hazardous"],
        "Waste Warriors": ["Paper", "Plastics", "Organic"],
        "Urban Waste Solutions": ["Plastics", "Paper", "Glass"],
        "Eco Friendly Disposal": ["Organic", "Plastics", "Paper"],
        "Sustainable Recycling Hub": ["Paper", "Plastics", "Metal", "Glass"]
    }
    
    result = []
    for recycler in recyclers:
        # Get materials from mapping or use default
        materials = materials_mapping.get(recycler.name, ["General Waste"])
        
        result.append({
            "id": recycler.id,
            "name": recycler.name,
            "address": recycler.address,
            "pincode": recycler.pincode,
            "phone": recycler.phone,
            "website": recycler.website,
            "latitude": recycler.latitude,
            "longitude": recycler.longitude,
            "materials": materials
        })
    
    return jsonify({"recyclers": result}), 200


@bp.route("/pickup-request", methods=["POST"])
@token_required
def create_pickup_request(user):
    """Create a pickup request."""
    data = request.get_json()
    
    required_fields = ["scheduled_at", "pickup_location"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        scheduled_at = datetime.fromisoformat(data["scheduled_at"].replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return jsonify({"error": "Invalid scheduled_at format"}), 400
    
    # Generate request code
    import random
    import string
    request_code = "REQ-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    pickup_request = PickupRequest(
        request_code=request_code,
        requester_id=user.id,
        scheduled_at=scheduled_at,
        pickup_location=data["pickup_location"],
        pincode=data.get("pincode") or user.pincode,
        quantity=data.get("quantity"),
        notes=data.get("notes"),
        status="pending"
    )
    
    db.session.add(pickup_request)
    db.session.commit()
    
    return jsonify({
        "message": "Pickup request created successfully",
        "request": {
            "id": pickup_request.id,
            "request_code": pickup_request.request_code,
            "scheduled_at": pickup_request.scheduled_at.isoformat(),
            "status": pickup_request.status
        }
    }), 201


@bp.route("/wards", methods=["GET"])
def get_wards():
    """Get all wards."""
    wards = Ward.query.filter_by(is_active=True).all()
    
    result = []
    for ward in wards:
        result.append({
            "id": ward.id,
            "ward_number": ward.ward_number,
            "name": ward.name,
            "pincode": ward.pincode
        })
    
    return jsonify({"wards": result}), 200

