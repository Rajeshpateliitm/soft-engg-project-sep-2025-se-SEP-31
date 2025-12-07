"""Test script to send the actual email templates to MailHog."""
import os
from dotenv import load_dotenv
from app import create_app
from app.core.email_service import send_waste_log_reminder, send_quiz_reminder
from app.models import User, UserCategory, db
from sqlalchemy import and_

# Load environment variables
load_dotenv()

def test_email_templates():
    """Test the actual email templates by sending them to PRIMARY users."""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Testing Actual Email Templates")
        print("=" * 60)
        
        # Get PRIMARY category
        primary_category = UserCategory.query.filter_by(key="PRIMARY").first()
        if not primary_category:
            print("ERROR: PRIMARY user category not found!")
            return
        
        # Get all active PRIMARY users with emails
        primary_users = User.query.filter(
            and_(
                User.is_active == True,
                User.user_category_id == primary_category.id,
                User.email.isnot(None)
            )
        ).all()
        
        print(f"\nFound {len(primary_users)} active PRIMARY users with emails")
        
        if len(primary_users) == 0:
            print("\nERROR: No PRIMARY users found with email addresses!")
            return
        
        # Check MailHog connection
        print(f"\n Mail Server: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
        print(f" Mail Sender: {app.config['MAIL_DEFAULT_SENDER']}")
        
        # Send waste log reminder
        print("\n" + "-" * 60)
        print("Sending Waste Log Reminder (with HTML template)...")
        print("-" * 60)
        
        waste_sent = 0
        for user in primary_users:
            username = user.username or user.email.split('@')[0]
            print(f"   Sending to {user.email}...", end=" ")
            if send_waste_log_reminder(user.email, username):
                waste_sent += 1
                print("SUCCESS")
            else:
                print("FAILURE")
        
        print(f"\n Sent {waste_sent} waste log reminder emails")
        
        # Send quiz reminder
        print("\n" + "-" * 60)
        print("Sending Quiz Reminder (with HTML template)...")
        print("-" * 60)
        
        quiz_sent = 0
        for user in primary_users:
            username = user.username or user.email.split('@')[0]
            print(f"   Sending to {user.email}...", end=" ")
            if send_quiz_reminder(user.email, username):
                quiz_sent += 1
                print("SUCCESS")
            else:
                print("FAILURE")
        
        print(f"\nSent {quiz_sent} quiz reminder emails")
        
        print("\n" + "=" * 60)
        print(f"Total: {waste_sent + quiz_sent} emails sent!")
        print("Check MailHog at: http://localhost:8025")
        print("=" * 60)
        print("\n Look for emails with subjects:")
        print("   - 'Daily Waste Log Reminder - WasteWise'")
        print("   - 'Daily Quiz Reminder - WasteWise'")
        print("\nThese will have the beautiful HTML templates!")

if __name__ == "__main__":
    test_email_templates()

