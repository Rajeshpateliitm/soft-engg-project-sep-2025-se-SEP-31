# Email and Cron Job Setup Guide

This guide explains how to set up the email functionality with MailHog and configure the daily reminder cron jobs.

## Overview

The WasteWise application includes:
- **Daily Waste Log Reminders**: Sent at 9:00 AM to users who haven't logged waste today
- **Daily Quiz Reminders**: Sent at 10:00 AM to users who haven't taken a quiz today

Both reminders are only sent to PRIMARY users who haven't completed the respective activity for the day.

## Prerequisites

1. **Python 3.8+** installed
2. **MailHog** installed and running (for email testing/development)

## Step 1: Install MailHog

MailHog is a development email testing tool that captures all emails sent by the application.

### On macOS (using Homebrew):
```bash
brew install mailhog
```

### On Linux:
```bash
# Download MailHog binary
wget https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64
chmod +x MailHog_linux_amd64
sudo mv MailHog_linux_amd64 /usr/local/bin/mailhog
```

### On Windows:
Download from: https://github.com/mailhog/MailHog/releases

### Using Docker:
```bash
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

## Step 2: Start MailHog

Start MailHog before running the Flask application:

```bash
# If installed via package manager
mailhog

# If using Docker (already running from above)
# No need to start separately
```

MailHog will be available at:
- **SMTP Server**: `localhost:1025` (for sending emails)
- **Web UI**: `http://localhost:8025` (to view captured emails)

## Step 3: Install Python Dependencies

Make sure you have installed the updated requirements:

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `Flask-Mail==0.10.0` - For sending emails
- `APScheduler==3.10.4` - For scheduling cron jobs

## Step 4: Configure Email Settings (Optional)

The application is pre-configured to use MailHog by default. If you need to customize settings, you can set environment variables:

```bash
export MAIL_SERVER=localhost
export MAIL_PORT=1025
export MAIL_USE_TLS=False
export MAIL_USE_SSL=False
export MAIL_DEFAULT_SENDER=wastewise@example.com
```

Or create a `.env` file in the backend directory:

```env
MAIL_SERVER=localhost
MAIL_PORT=1025
MAIL_USE_TLS=False
MAIL_USE_SSL=False
MAIL_DEFAULT_SENDER=wastewise@example.com
```

## Step 5: Run the Application

Start the Flask backend as usual:

```bash
cd backend
python main.py
```

The scheduler will automatically start and schedule the daily email reminders:
- **Waste Log Reminders**: 9:00 AM daily
- **Quiz Reminders**: 10:00 AM daily

You should see a log message:
```
Scheduler initialized with daily email reminders
```

## Step 6: View Emails in MailHog

1. Open your browser and navigate to: `http://localhost:8025`
2. You'll see all emails sent by the application
3. Click on any email to view its contents (both plain text and HTML)

## Testing the Email Functionality

### Manual Testing

You can test the email functionality by manually triggering the cron jobs. Create a test script:

```python
# test_emails.py
from app import create_app
from app.core.cron_jobs import send_daily_waste_log_reminders, send_daily_quiz_reminders

app = create_app()
with app.app_context():
    send_daily_waste_log_reminders()
    send_daily_quiz_reminders()
```

Run it:
```bash
python test_emails.py
```

### Testing with Different Times

To test immediately without waiting for the scheduled time, you can temporarily modify the cron schedule in `app/__init__.py`:

```python
# For testing: run every minute
scheduler.add_job(
    func=send_daily_waste_log_reminders,
    trigger=CronTrigger(minute='*'),  # Every minute
    id='daily_waste_log_reminders',
    name='Send daily waste log reminders',
    replace_existing=True
)
```

**Remember to change it back to the production schedule!**

## Production Setup

For production, you'll need to:

1. **Replace MailHog with a real SMTP server** (Gmail, SendGrid, AWS SES, etc.)
2. **Update email configuration** in `.env` or environment variables:
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=wastewise@yourdomain.com
   ```

3. **Adjust cron schedule** if needed (currently 9:00 AM and 10:00 AM)

## Cron Job Schedule

The default schedule is:
- **Waste Log Reminders**: Daily at 9:00 AM
- **Quiz Reminders**: Daily at 10:00 AM

To change the schedule, modify the `CronTrigger` in `app/__init__.py`:

```python
# Example: Run at 8:00 AM
trigger=CronTrigger(hour=8, minute=0)

# Example: Run at 2:00 PM
trigger=CronTrigger(hour=14, minute=0)

# Example: Run every 6 hours
trigger=CronTrigger(hour='*/6')
```

## Troubleshooting

### Emails not being sent?

1. **Check MailHog is running**: Visit `http://localhost:8025`
2. **Check application logs**: Look for error messages in the Flask console
3. **Verify MailHog SMTP port**: Should be `1025` (not `8025`)
4. **Check user emails**: Ensure users have valid email addresses in the database

### Scheduler not starting?

1. **Check logs**: Look for "Scheduler initialized" message
2. **Verify SCHEDULER_API_ENABLED**: Should be `True` in config
3. **Check for errors**: Look for any import or initialization errors

### Emails going to spam?

This is normal with MailHog (development tool). In production with a real SMTP server:
- Use proper SPF/DKIM records
- Use a reputable email service
- Include unsubscribe links
- Follow email best practices

## Email Templates

The email templates are defined in `app/core/email_service.py`:
- `send_waste_log_reminder()` - Waste log reminder email
- `send_quiz_reminder()` - Quiz reminder email

Both functions send HTML emails with styling. You can customize the templates by editing these functions.

## Files Modified/Created

- `requirements.txt` - Added Flask-Mail and APScheduler
- `app/core/config.py` - Added email configuration
- `app/core/email_service.py` - Email service module (NEW)
- `app/core/cron_jobs.py` - Cron job tasks (NEW)
- `app/__init__.py` - Initialize email service and scheduler

## Additional Notes

- Emails are only sent to **PRIMARY** users
- Reminders are only sent if the user **hasn't completed** the activity today
- The scheduler runs in the background and doesn't block the Flask application
- All email sending is logged for debugging purposes

