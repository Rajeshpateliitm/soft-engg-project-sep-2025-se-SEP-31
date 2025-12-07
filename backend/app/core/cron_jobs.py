"""Cron job tasks for scheduled email reminders."""
from app.models import User, UserCategory, db
from app.core.email_service import send_waste_log_reminder, send_quiz_reminder
from sqlalchemy import and_


def send_daily_waste_log_reminders(app=None):
    """
    Send daily waste log reminders to all PRIMARY users (force send for testing).
    Uses the actual HTML email templates.
    
    Args:
        app: Flask application instance (required for scheduler context)
    """
    if app is None:
        from flask import current_app
        app = current_app
    
    with app.app_context():
        try:
            # Get PRIMARY user category
            primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
            if not primary_category:
                app.logger.warning("PRIMARY user category not found")
                return
            
            # Get all active PRIMARY users with emails
            primary_users = User.query.filter(
                and_(
                    User.is_active == True,
                    User.user_category_id == primary_category.id,
                    User.email.isnot(None)
                )
            ).all()
            
            if len(primary_users) == 0:
                app.logger.warning("No PRIMARY users found with email addresses")
                return
            
            # Force send emails to all PRIMARY users (using HTML templates)
            reminders_sent = 0
            for user in primary_users:
                username = user.username or user.email.split('@')[0]
                if send_waste_log_reminder(user.email, username):
                    reminders_sent += 1
                    app.logger.info(f"Sent waste log reminder to {user.email}")
                    print(f"Sent waste log reminder to {user.email}")
            
            summary = f"Waste log reminders: {reminders_sent} emails sent (HTML templates)"
            app.logger.info(summary)
            print(f"{summary}")
            
        except Exception as e:
            app.logger.error(f"Error sending daily waste log reminders: {str(e)}")
            print(f"Error sending daily waste log reminders: {str(e)}")


def send_daily_quiz_reminders(app=None):
    """
    Send daily quiz reminders to all PRIMARY users (force send for testing).
    Uses the actual HTML email templates.
    
    Args:
        app: Flask application instance (required for scheduler context)
    """
    if app is None:
        from flask import current_app
        app = current_app
    
    with app.app_context():
        try:
            # Get PRIMARY user category
            primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
            if not primary_category:
                app.logger.warning("PRIMARY user category not found")
                return
            
            # Get all active PRIMARY users with emails
            primary_users = User.query.filter(
                and_(
                    User.is_active == True,
                    User.user_category_id == primary_category.id,
                    User.email.isnot(None)
                )
            ).all()
            
            if len(primary_users) == 0:
                app.logger.warning("No PRIMARY users found with email addresses")
                return
            
            # Force send emails to all PRIMARY users (using HTML templates)
            reminders_sent = 0
            for user in primary_users:
                username = user.username or user.email.split('@')[0]
                if send_quiz_reminder(user.email, username):
                    reminders_sent += 1
                    app.logger.info(f"Sent quiz reminder to {user.email}")
                    print(f"Sent quiz reminder to {user.email}")
            
            summary = f"Quiz reminders: {reminders_sent} emails sent (HTML templates)"
            app.logger.info(summary)
            print(f"{summary}")
            
        except Exception as e:
            app.logger.error(f"Error sending daily quiz reminders: {str(e)}")
            print(f"Error sending daily quiz reminders: {str(e)}")

