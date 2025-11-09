"""Security utilities for authentication."""
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from jose import jwt, JWTError
from app.models import User, db


def create_access_token(user_id: int, expires_delta: timedelta = None):
    """Create JWT access token."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=current_app.config["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"])
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode,
        current_app.config["JWT_SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"]
    )
    return encoded_jwt


def verify_token(token: str):
    """Verify JWT token and return user_id."""
    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=[current_app.config["JWT_ALGORITHM"]]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None


def get_current_user():
    """Get current user from token."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(" ")[1]  # Bearer <token>
    except IndexError:
        return None
    
    user_id = verify_token(token)
    if user_id is None:
        return None
    
    return User.query.get(user_id)


def token_required(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if user is None:
            return jsonify({"error": "Authentication required"}), 401
        if not user.is_active:
            return jsonify({"error": "User account is inactive"}), 403
        return f(user, *args, **kwargs)
    return decorated


def role_required(*allowed_roles):
    """Decorator to require specific user role/category."""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(user, *args, **kwargs):
            if user.user_category:
                user_role = user.user_category.key
                if user_role not in allowed_roles:
                    return jsonify({"error": "Insufficient permissions"}), 403
            else:
                return jsonify({"error": "User role not assigned"}), 403
            return f(user, *args, **kwargs)
        return decorated
    return decorator
