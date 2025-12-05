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
    # Only PRIMARY users can register through public sign-up
    # SECONDARY and TERTIARY users are provisioned by administrators
    user_category_key = data.get("user_category", "PRIMARY")
    
    # Restrict registration to PRIMARY users only
    if user_category_key not in ["PRIMARY", None]:
        return jsonify({"error": "Only primary users can register through public sign-up. Secondary and Tertiary users are provisioned by administrators."}), 403
    
    # Ensure it's PRIMARY
    user_category_key = "PRIMARY"
    user_category = UserCategory.query.filter_by(key=user_category_key).first()
    if not user_category:
        user_category = UserCategory(key=user_category_key, label=user_category_key.title())
        db.session.add(user_category)
        db.session.flush()
    
    # Get ward_id from ward_number if provided
    ward_id = None
    if data.get("ward_number"):
        from app.models import Ward
        ward = Ward.query.filter_by(ward_number=data["ward_number"]).first()
        if ward:
            ward_id = ward.id
    
    # Create new user
    user = User(
        email=data["email"],
        username=data.get("username") or data["email"].split("@")[0],
        house_number=data["house_number"],
        ward_number=data["ward_number"],
        ward_id=ward_id,
        family_members_count=data["family_members"],
        pincode=data["pincode"],
        user_category_id=user_category.id
    )
    user.set_password(data["password"])
    
    try:
        db.session.add(user)
        db.session.flush()  # Flush to get user.id
        
        # Auto-add primary user to RWA group based on ward
        if ward_id:
            from app.models import RwaGroup, RwaMembership
            # Find RWA group for this ward
            rwa_group = RwaGroup.query.filter_by(ward_number=data["ward_number"]).first()
            if rwa_group:
                # Check if membership already exists
                existing_membership = RwaMembership.query.filter_by(
                    user_id=user.id,
                    rwa_group_id=rwa_group.id
                ).first()
                
                if not existing_membership:
                    membership = RwaMembership(
                        rwa_group_id=rwa_group.id,
                        user_id=user.id,
                        role="member"
                    )
                    db.session.add(membership)
        
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
    
    # Get RWA membership role if user is secondary
    rwa_role = None
    if user.user_category and user.user_category.key == "SECONDARY":
        from app.models import RwaMembership
        membership = RwaMembership.query.filter_by(user_id=user.id, is_active=True).first()
        if membership:
            rwa_role = membership.role
    
    return jsonify({
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "user_category": user.user_category.key if user.user_category else None,
            "points": user.points,
            "rwa_role": rwa_role  # "admin", "collector", or None
        }
    }), 200


@bp.route("/me", methods=["GET"])
@token_required
def get_current_user_info(user):
    """Get current user information."""
    # Get RWA membership role if user is secondary
    rwa_role = None
    if user.user_category and user.user_category.key == "SECONDARY":
        from app.models import RwaMembership
        membership = RwaMembership.query.filter_by(user_id=user.id, is_active=True).first()
        if membership:
            rwa_role = membership.role
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "house_number": user.house_number,
        "ward_number": user.ward_number,
        "family_members_count": user.family_members_count,
        "pincode": user.pincode,
        "points": user.points,
        "user_category": user.user_category.key if user.user_category else None,
        "rwa_role": rwa_role  # "admin", "collector", or None
    }), 200


@bp.route("/reset-password", methods=["POST"])
def reset_password():
    """Reset user password.
    
    Request body:
    {
        "email": "user@example.com",
        "new_password": "newPassword123",
        "confirm_password": "newPassword123"
    }
    """
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    email = data.get("email", "").strip()
    new_password = data.get("new_password", "").strip()
    confirm_password = data.get("confirm_password", "").strip()
    
    # Validate all fields are provided
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    if not new_password:
        return jsonify({"error": "New password is required"}), 400
    
    if not confirm_password:
        return jsonify({"error": "Password confirmation is required"}), 400
    
    # Validate email format
    if "@" not in email or "." not in email:
        return jsonify({"error": "Invalid email format"}), 400
    
    # Validate password length
    if len(new_password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400
    
    # Validate passwords match
    if new_password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400
    
    # Check if user exists
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # For security, don't reveal if email exists or not
        # Return generic message
        return jsonify({"error": "If an account with this email exists, the password has been reset. Please check your email."}), 200
    
    # Check if user account is active
    if not user.is_active:
        return jsonify({"error": "This user account is inactive. Please contact support."}), 403
    
    try:
        # Set new password
        user.set_password(new_password)
        
        # Update the user in database
        db.session.commit()
        
        # Log the password reset (optional - for audit trail)
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Password reset successful for user: {user.email} (ID: {user.id})")
        
        return jsonify({
            "message": "Password has been successfully reset. You can now sign in with your new password.",
            "success": True
        }), 200
        
    except Exception as e:
        db.session.rollback()
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error resetting password for user {email}: {str(e)}")
        
        return jsonify({
            "error": "An error occurred while resetting your password. Please try again later."
        }), 500

