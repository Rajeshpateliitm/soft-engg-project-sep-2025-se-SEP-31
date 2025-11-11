"""Flask application factory."""
from flask import Flask, jsonify
from flask_cors import CORS
from app.models import db
from app.core.config import Config


def create_app(config_class=Config):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

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

    from app.api.genai import bp as genai_bp
    app.register_blueprint(genai_bp, url_prefix="/api/genai")

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

    return app
