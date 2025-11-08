"""Authentication endpoints."""
from flask import Blueprint, request, jsonify
from app.models import User, UserCategory, db
from app.core.security import create_access_token, token_required, get_current_user
from sqlalchemy.exc import IntegrityError

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.get_json()
    
    required_fields = ["email", "password", "house_number", "ward_number", "family_members", "pincode"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400
    
    # Get or create user category (default to PRIMARY)
    user_category_key = data.get("user_category", "PRIMARY")
    user_category = UserCategory.query.filter_by(key=user_category_key).first()
    if not user_category:
        user_category = UserCategory(key=user_category_key, label=user_category_key.title())
        db.session.add(user_category)
        db.session.flush()
    
    # Create new user
    user = User(
        email=data["email"],
        username=data.get("username") or data["email"].split("@")[0],
        house_number=data["house_number"],
        ward_number=data["ward_number"],
        family_members_count=data["family_members"],
        pincode=data["pincode"],
        user_category_id=user_category.id
    )
    user.set_password(data["password"])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(user.id)
        
        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "house_number": user.house_number,
                "ward_number": user.ward_number,
                "user_category": user_category.key
            },
            "access_token": access_token,
            "token_type": "bearer"
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route("/login", methods=["POST"])
def login():
    """Login user and return access token."""
    data = request.get_json()
    
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required"}), 400
    
    user = User.query.filter_by(email=data["email"]).first()
    
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401
    
    if not user.is_active:
        return jsonify({"error": "User account is inactive"}), 403
    
    # Create access token
    access_token = create_access_token(user.id)
    
    return jsonify({
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "user_category": user.user_category.key if user.user_category else None,
            "points": user.points
        }
    }), 200


@bp.route("/me", methods=["GET"])
@token_required
def get_current_user_info(user):
    """Get current user information."""
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "house_number": user.house_number,
        "ward_number": user.ward_number,
        "family_members_count": user.family_members_count,
        "pincode": user.pincode,
        "points": user.points,
        "user_category": user.user_category.key if user.user_category else None
    }), 200

