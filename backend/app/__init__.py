"""Flask application factory."""
from flask import Flask, jsonify
from flask_cors import CORS
from app.models import db
from app.core.config import Config
from app.core.email_service import init_mail
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit


def create_app(config_class=Config):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize email service
    init_mail(app)

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
    
    # Register CLI command for updating recyclers
    @app.cli.command("update-recyclers")
    def update_recyclers_command():
        """Update recyclers with coordinates."""
        from app.db.init_data import update_recyclers_data
        update_recyclers_data()
    
    # Initialize and start scheduler for cron jobs
    if app.config.get('SCHEDULER_API_ENABLED', True):
        scheduler = BackgroundScheduler()
        scheduler.start()
        
        # Schedule daily waste log reminders at 9:00 AM
        from app.core.cron_jobs import send_daily_waste_log_reminders, send_daily_quiz_reminders
        scheduler.add_job(
            func=send_daily_waste_log_reminders,
            trigger=CronTrigger(hour=9, minute=0),  # 9:00 AM daily
            id='daily_waste_log_reminders',
            name='Send daily waste log reminders',
            replace_existing=True
        )
        
        # Schedule daily quiz reminders at 10:00 AM
        scheduler.add_job(
            func=send_daily_quiz_reminders,
            trigger=CronTrigger(hour=10, minute=0),  # 10:00 AM daily
            id='daily_quiz_reminders',
            name='Send daily quiz reminders',
            replace_existing=True
        )
        
        # Shut down scheduler when app exits
        atexit.register(lambda: scheduler.shutdown())
        
        app.logger.info("Scheduler initialized with daily email reminders")

    return app
