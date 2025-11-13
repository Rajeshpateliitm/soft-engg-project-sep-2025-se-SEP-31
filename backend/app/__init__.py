"""Flask application factory."""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from app.core.config import Config

# Initialize Flask-Mail
mail = Mail()

def create_app(config_class=Config):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Import db here to avoid circular imports and namespace conflicts
    # Import models module first, then get db from it
    # This avoids conflict with app.db directory
    import sys
    import os
    
    # Ensure we're importing from the correct path
    backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    
    # Import models module explicitly
    from app import models
    # Get db instance from models module (not from app.db directory)
    db = models.db
    
    # Verify db is the SQLAlchemy instance, not a module
    from flask_sqlalchemy import SQLAlchemy
    if not isinstance(db, SQLAlchemy):
        raise ImportError("db is not a SQLAlchemy instance. Check for namespace conflicts with app.db directory.")
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Store db on app for easier access
    app.extensions['sqlalchemy'] = db

    # Register blueprints
    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.api.primary import bp as primary_bp
    app.register_blueprint(primary_bp, url_prefix="/api/primary")

    from app.api.secondary import bp as secondary_bp
    app.register_blueprint(secondary_bp, url_prefix="/api/secondary")

    from app.api.tertiary import bp as tertiary_bp
    app.register_blueprint(tertiary_bp, url_prefix="/api/tertiary")

    from app.api.common import bp as common_bp
    app.register_blueprint(common_bp, url_prefix="/api/common")

    @app.route("/")
    def root():
        return jsonify({"message": "Welcome to WasteWise API!"})

    @app.route("/api/health")
    def health():
        return jsonify({"status": "healthy"})

    # Create tables and initialize sample data
    with app.app_context():
        db.create_all()
        # Initialize sample data if database is empty
        from app.db.init_data import init_sample_data
        init_sample_data()
    
    # Register CLI command for updating recyclers
    @app.cli.command("update-recyclers")
    def update_recyclers_command():
        """Update recyclers with coordinates."""
        from app.db.init_data import update_recyclers_data
        update_recyclers_data()

    return app
