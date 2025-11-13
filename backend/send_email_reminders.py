#!/usr/bin/env python3
"""
Standalone script to send daily email reminders for quizzes and waste logs.
This script can be run via cron job.

Usage:
    python send_email_reminders.py

For testing (send every 5 seconds):
    watch -n 5 python send_email_reminders.py

For cron (daily at 9:00 AM):
    0 9 * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /var/log/wastewise_emails.log 2>&1
"""
import sys
import os
from datetime import date

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, UserCategory, QuizAttempt, WasteLog, db
from app.core.config import Config
from flask import render_template_string
from flask_mail import Message


def get_quiz_reminder_template():
    """Get quiz reminder email template."""
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Quiz Reminder</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0;
            color: #27ae60;
        }
        .content {
            margin: 30px 0;
        }
        .content p {
            margin: 15px 0;
            font-size: 16px;
        }
        .button {
            display: inline-block;
            padding: 15px 30px;
            background-color: #27ae60;
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 20px 0;
            text-align: center;
        }
        .button:hover {
            background-color: #229954;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }
        .highlight {
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌱 WasteWise</h1>
            <p>Daily Quiz Reminder</p>
        </div>
        <div class="content">
            <p>Hello {{ user_name }},</p>
            <p>Don't forget to complete your daily quiz today! 🧠</p>
            <div class="highlight">
                <p><strong>Why take the quiz?</strong></p>
                <ul>
                    <li>Learn more about waste management</li>
                    <li>Earn points and climb the leaderboard</li>
                    <li>Stay engaged with your community</li>
                </ul>
            </div>
            <p>Click the button below to sign in and take today's quiz:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{{ signin_url }}" class="button" style="display: inline-block; padding: 15px 30px; background-color: #27ae60; color: #ffffff !important; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">Take Daily Quiz</a>
            </div>
            <p style="text-align: center; margin-top: 20px;">
                <a href="{{ signin_url }}" style="color: #3498db; text-decoration: underline;">Click here to sign in</a> or copy this link: <span style="color: #7f8c8d; font-size: 12px; word-break: break-all;">{{ signin_url }}</span>
            </p>
        </div>
        <div class="footer">
            <p>This is an automated reminder from WasteWise.</p>
            <p>© 2025 WasteWise. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
    """


def get_waste_log_reminder_template():
    """Get waste log reminder email template."""
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Waste Log Reminder</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0;
            color: #27ae60;
        }
        .content {
            margin: 30px 0;
        }
        .content p {
            margin: 15px 0;
            font-size: 16px;
        }
        .button {
            display: inline-block;
            padding: 15px 30px;
            background-color: #27ae60;
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 20px 0;
            text-align: center;
        }
        .button:hover {
            background-color: #229954;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }
        .highlight {
            background-color: #e8f5e9;
            padding: 15px;
            border-left: 4px solid #4caf50;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌱 WasteWise</h1>
            <p>Daily Waste Log Reminder</p>
        </div>
        <div class="content">
            <p>Hello {{ user_name }},</p>
            <p>Don't forget to log your waste for today! ♻️</p>
            <div class="highlight">
                <p><strong>Why log your waste?</strong></p>
                <ul>
                    <li>Track your waste management progress</li>
                    <li>Earn points for proper segregation</li>
                    <li>Help your community reach sustainability goals</li>
                </ul>
            </div>
            <p>Click the button below to sign in and log your waste:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{{ signin_url }}" class="button" style="display: inline-block; padding: 15px 30px; background-color: #27ae60; color: #ffffff !important; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">Log Waste</a>
            </div>
            <p style="text-align: center; margin-top: 20px;">
                <a href="{{ signin_url }}" style="color: #3498db; text-decoration: underline;">Click here to sign in</a> or copy this link: <span style="color: #7f8c8d; font-size: 12px; word-break: break-all;">{{ signin_url }}</span>
            </p>
        </div>
        <div class="footer">
            <p>This is an automated reminder from WasteWise.</p>
            <p>© 2025 WasteWise. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
    """


def send_quiz_reminder(app, user):
    """Send quiz reminder email to a specific user."""
    from app import mail
    
    try:
        if not user.email:
            print(f"Skipping user {user.id}: no email address")
            return False
        
        # Create signin URL with redirect to quiz page
        signin_url = f"{Config.APP_URL}/signin?redirect=/primary-dashboard/quiz"
        
        # Load email template
        template = get_quiz_reminder_template()
        
        # Render email content
        html_content = render_template_string(
            template,
            user_name=user.username or user.email.split('@')[0],
            signin_url=signin_url,
            app_url=Config.APP_URL,
            quiz_url=f"{Config.APP_URL}/primary-dashboard/quiz"
        )
        
        # Create email message
        msg = Message(
            subject="Daily Quiz Reminder - WasteWise",
            recipients=[user.email],
            html=html_content,
            sender=Config.MAIL_DEFAULT_SENDER
        )
        
        # Send email
        mail.send(msg)
        print(f"✓ Quiz reminder sent to {user.email}")
        return True
        
    except Exception as e:
        print(f"✗ Error sending quiz reminder to user {user.id} ({user.email}): {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def send_waste_log_reminder(app, user):
    """Send waste log reminder email to a specific user."""
    from app import mail
    
    try:
        if not user.email:
            print(f"Skipping user {user.id}: no email address")
            return False
        
        # Create signin URL with redirect to wastelog page
        signin_url = f"{Config.APP_URL}/signin?redirect=/primary-dashboard/wastelog"
        
        # Load email template
        template = get_waste_log_reminder_template()
        
        # Render email content
        html_content = render_template_string(
            template,
            user_name=user.username or user.email.split('@')[0],
            signin_url=signin_url,
            app_url=Config.APP_URL,
            wastelog_url=f"{Config.APP_URL}/primary-dashboard/wastelog"
        )
        
        # Create email message
        msg = Message(
            subject="Daily Waste Log Reminder - WasteWise",
            recipients=[user.email],
            html=html_content,
            sender=Config.MAIL_DEFAULT_SENDER
        )
        
        # Send email
        mail.send(msg)
        print(f"✓ Waste log reminder sent to {user.email}")
        return True
        
    except Exception as e:
        print(f"✗ Error sending waste log reminder to user {user.id} ({user.email}): {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def send_daily_reminders():
    """Send daily reminder emails to all primary users."""
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Get all active primary users
            primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
            if not primary_category:
                print("✗ Primary user category not found")
                return False
            
            primary_users = User.query.filter_by(
                user_category_id=primary_category.id,
                is_active=True
            ).all()
            
            print(f"Found {len(primary_users)} primary users to check")
            
            quiz_reminders_sent = 0
            waste_log_reminders_sent = 0
            
            # Send reminders to each user
            for user in primary_users:
                if user.email:
                    # Check if user has completed quiz today
                    today = date.today()
                    quiz_today = QuizAttempt.query.filter_by(
                        user_id=user.id,
                        is_active=True
                    ).filter(
                        db.func.date(QuizAttempt.created_at) == today
                    ).first()
                    
                    # Check if user has logged waste today
                    waste_log_today = WasteLog.query.filter_by(
                        user_id=user.id,
                        is_active=True
                    ).filter(
                        db.func.date(WasteLog.log_date) == today
                    ).first()
                    
                    # Send quiz reminder if not completed today
                    if not quiz_today:
                        if send_quiz_reminder(app, user):
                            quiz_reminders_sent += 1
                    
                    # Send waste log reminder if not logged today
                    if not waste_log_today:
                        if send_waste_log_reminder(app, user):
                            waste_log_reminders_sent += 1
            
            print(f"\n✓ Daily reminders completed:")
            print(f"  - Quiz reminders sent: {quiz_reminders_sent}")
            print(f"  - Waste log reminders sent: {waste_log_reminders_sent}")
            return True
            
        except Exception as e:
            print(f"✗ Error in send_daily_reminders: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    print("=" * 60)
    print("WasteWise Email Reminder Script")
    print("=" * 60)
    print(f"Time: {date.today()}\n")
    
    success = send_daily_reminders()
    
    if success:
        print("\n✓ Email reminder script completed successfully")
        sys.exit(0)
    else:
        print("\n✗ Email reminder script completed with errors")
        sys.exit(1)

