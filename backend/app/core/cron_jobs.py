"""Cron job tasks for scheduled email reminders."""
from flask import current_app
from app.models import User, UserCategory, WasteLog, QuizAttempt, db
from app.core.email_service import send_waste_log_reminder, send_quiz_reminder
from sqlalchemy import and_
from datetime import date, datetime, timedelta


def send_daily_waste_log_reminders():
    """
    Send daily waste log reminders to users who haven't logged waste today.
    Only sends to PRIMARY users.
    """
    with current_app.app_context():
        try:
            today = date.today()
            
            # Get PRIMARY user category
            primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
            if not primary_category:
                current_app.logger.warning("PRIMARY user category not found")
                return
            
            # Get all active PRIMARY users
            primary_users = User.query.filter(
                and_(
                    User.is_active == True,
                    User.user_category_id == primary_category.id,
                    User.email.isnot(None)
                )
            ).all()
            
            reminders_sent = 0
            for user in primary_users:
                # Check if user has logged waste today
                has_logged_today = WasteLog.query.filter(
                    and_(
                        WasteLog.user_id == user.id,
                        WasteLog.log_date == today,
                        WasteLog.is_active == True
                    )
                ).first() is not None
                
                # Send reminder if user hasn't logged waste today
                if not has_logged_today:
                    username = user.username or user.email.split('@')[0]
                    if send_waste_log_reminder(user.email, username):
                        reminders_sent += 1
                        current_app.logger.info(f"Sent waste log reminder to {user.email}")
            
            current_app.logger.info(f"Daily waste log reminders: {reminders_sent} emails sent")
            
        except Exception as e:
            current_app.logger.error(f"Error sending daily waste log reminders: {str(e)}")


def send_daily_quiz_reminders():
    """
    Send daily quiz reminders to users who haven't taken a quiz today.
    Only sends to PRIMARY users.
    """
    with current_app.app_context():
        try:
            today = date.today()
            today_start = datetime.combine(today, datetime.min.time())
            tomorrow_start = datetime.combine(today + timedelta(days=1), datetime.min.time())
            
            # Get PRIMARY user category
            primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
            if not primary_category:
                current_app.logger.warning("PRIMARY user category not found")
                return
            
            # Get all active PRIMARY users
            primary_users = User.query.filter(
                and_(
                    User.is_active == True,
                    User.user_category_id == primary_category.id,
                    User.email.isnot(None)
                )
            ).all()
            
            reminders_sent = 0
            for user in primary_users:
                # Check if user has taken a quiz today
                has_quiz_today = QuizAttempt.query.filter(
                    and_(
                        QuizAttempt.user_id == user.id,
                        QuizAttempt.created_at >= today_start,
                        QuizAttempt.created_at < tomorrow_start,
                        QuizAttempt.is_active == True
                    )
                ).first() is not None
                
                # Send reminder if user hasn't taken quiz today
                if not has_quiz_today:
                    username = user.username or user.email.split('@')[0]
                    if send_quiz_reminder(user.email, username):
                        reminders_sent += 1
                        current_app.logger.info(f"Sent quiz reminder to {user.email}")
            
            current_app.logger.info(f"Daily quiz reminders: {reminders_sent} emails sent")
            
        except Exception as e:
            current_app.logger.error(f"Error sending daily quiz reminders: {str(e)}")

