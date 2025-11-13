"""Test script for email notifications."""
from app.tasks.email_tasks import send_quiz_reminder, send_waste_log_reminder, send_daily_reminders

if __name__ == '__main__':
    print("Testing email notifications...")
    print("\n1. Testing quiz reminder for user ID 1...")
    result = send_quiz_reminder.delay(1)
    print(f"Task ID: {result.id}")
    print(f"Task State: {result.state}")
    
    print("\n2. Testing waste log reminder for user ID 1...")
    result = send_waste_log_reminder.delay(1)
    print(f"Task ID: {result.id}")
    print(f"Task State: {result.state}")
    
    print("\n3. Testing daily reminders for all users...")
    result = send_daily_reminders.delay()
    print(f"Task ID: {result.id}")
    print(f"Task State: {result.state}")
    
    print("\nCheck MailHog at http://localhost:8025 to see the emails!")
    print("Make sure Redis and MailHog are running before testing.")

