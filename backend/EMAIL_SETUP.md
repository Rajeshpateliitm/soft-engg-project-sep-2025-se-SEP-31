# Email Notification Setup Guide

This guide explains how to set up and run the daily email notification system using cron jobs and MailHog.

## Prerequisites

1. **MailHog** - For local email testing (development) or real SMTP server for production
2. **Python 3.9+** - Required to run the email reminder script
3. **Python dependencies** - Install from requirements.txt

## Installation

### 1. Install MailHog (for development/testing)

**macOS (using Homebrew):**
```bash
brew install mailhog
brew services start mailhog
```

**Linux:**
```bash
# Download MailHog
wget https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64
chmod +x MailHog_linux_amd64
sudo mv MailHog_linux_amd64 /usr/local/bin/mailhog

# Start MailHog
mailhog
```

**Windows:**
Download from: https://github.com/mailhog/MailHog/releases
Run: `MailHog.exe`

Access MailHog web interface at: **http://localhost:8025**

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Email Settings

The email configuration is in `backend/app/core/config.py`. Default settings for MailHog:

```python
MAIL_SERVER = "localhost"
MAIL_PORT = 1025
MAIL_DEFAULT_SENDER = "noreply@wastewise.com"
```

For production, update with your SMTP server details or use environment variables:

```python
MAIL_SERVER = os.environ.get("MAIL_SERVER") or "smtp.example.com"
MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
```

### 4. Configure Application URL

Edit `backend/app/core/config.py`:

```python
APP_URL = os.environ.get("APP_URL") or "http://localhost:5173"
SIGNIN_URL = f"{APP_URL}/signin"
```

## Running the System

### 1. Start MailHog (for testing)

Make sure MailHog is running:

```bash
# Check if running
lsof -i :1025
# or
curl http://localhost:8025/api/v2/messages

# Start if not running
mailhog
```

Access MailHog web interface at: http://localhost:8025

### 2. Test Email Script Manually

Test the email reminder script:

```bash
cd backend
python3 send_email_reminders.py
```

You should see output showing:
- Number of primary users found
- Quiz reminders sent
- Waste log reminders sent

### 3. Set Up Cron Job

For automated daily reminders, set up a cron job:

1. **Edit crontab:**
   ```bash
   crontab -e
   ```

2. **Add cron job (daily at 9:00 AM):**
   ```cron
   0 9 * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /var/log/wastewise_emails.log 2>&1
   ```
   
   **Important:** Replace `/path/to/backend` with your actual backend directory path.

3. **Verify:**
   ```bash
   crontab -l
   ```

For detailed cron setup instructions, see `CRON_SETUP.md`.

## Testing

### Manual Test

Run the script directly:

```bash
cd backend
python3 send_email_reminders.py
```

### Check MailHog

1. Open http://localhost:8025 in your browser
2. You should see the emails that were sent
3. Click on an email to view its contents
4. Verify the sign-in links work correctly

### Test with Cron (Every 5 Minutes)

For testing, set up a cron job that runs every 5 minutes:

```cron
*/5 * * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /tmp/wastewise_test.log 2>&1
```

Monitor the logs:

```bash
tail -f /tmp/wastewise_test.log
```

## How It Works

The email reminder system:

1. **Checks all active primary users** in the database
2. **Sends quiz reminders** to users who haven't completed a quiz today
3. **Sends waste log reminders** to users who haven't logged waste today
4. **Uses MailHog** (development) or real SMTP server (production) to send emails

## Email Templates

The system uses HTML email templates for:
- **Quiz Reminders**: Encourages users to take daily quizzes
- **Waste Log Reminders**: Encourages users to log their waste

Both templates include:
- Sign-in links with redirects to relevant pages
- Motivational content
- WasteWise branding

## Production Setup

For production deployment:

1. **Use a real SMTP server:**
   - Gmail SMTP
   - SendGrid
   - Mailgun
   - AWS SES
   - Your organization's SMTP server

2. **Update email configuration** in `app/core/config.py`:
   ```python
   MAIL_SERVER = "smtp.example.com"
   MAIL_PORT = 587
   MAIL_USE_TLS = True
   MAIL_USERNAME = "your-email@example.com"
   MAIL_PASSWORD = "your-password"
   ```

3. **Set up cron job** for daily execution:
   ```cron
   0 9 * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /var/log/wastewise_emails.log 2>&1
   ```

4. **Configure log rotation** to prevent log files from growing too large

5. **Set up monitoring** and alerts for failed email sends

6. **Test thoroughly** before deploying

## Troubleshooting

### Script Not Running

1. **Test manually:**
   ```bash
   cd /path/to/backend
   python3 send_email_reminders.py
   ```

2. **Check Python path:**
   ```bash
   which python3
   ```

3. **Verify file permissions:**
   ```bash
   chmod +x send_email_reminders.py
   ```

4. **Use absolute paths** in crontab

### No Emails Being Sent

1. **Check MailHog is running:**
   ```bash
   lsof -i :1025
   ```

2. **Check script output** for errors:
   ```bash
   python3 send_email_reminders.py
   ```

3. **Verify Flask-Mail configuration** in `config.py`

4. **Check database** for primary users with email addresses

### Cron Job Not Running

1. **Check cron service:**
   ```bash
   # Linux
   sudo systemctl status cron
   
   # macOS
   sudo launchctl list | grep cron
   ```

2. **Check cron logs:**
   ```bash
   # Linux
   grep CRON /var/log/syslog
   
   # macOS
   grep CRON /var/log/system.log
   ```

3. **Verify crontab entry:**
   ```bash
   crontab -l
   ```

### Emails Not Appearing in MailHog

1. **Verify MailHog is running** on port 1025
2. **Check script logs** for email sending errors
3. **Verify MAIL_SERVER** is set to `localhost` and MAIL_PORT is `1025`

## Configuration Options

### Email Server Configuration

Edit `backend/app/core/config.py`:

```python
# MailHog (development)
MAIL_SERVER = "localhost"
MAIL_PORT = 1025

# Production SMTP
MAIL_SERVER = "smtp.example.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "your-email@example.com"
MAIL_PASSWORD = "your-password"
```

### Application URL

```python
APP_URL = "http://localhost:5173"  # Development
APP_URL = "https://yourdomain.com"  # Production
```

### Cron Schedule

Adjust the cron schedule based on your needs:

```cron
# Daily at 9:00 AM
0 9 * * *

# Daily at 9:00 AM and 5:00 PM
0 9,17 * * *

# Every Monday at 9:00 AM
0 9 * * 1

# Every 5 minutes (for testing)
*/5 * * * *
```

## Documentation

For more details, see:
- **CRON_SETUP.md** - Detailed cron job setup guide
- **TESTING_EMAILS.md** - Testing guide
- **README_EMAIL.md** - Quick start guide

## Support

For issues or questions:
1. Check the logs first
2. Verify MailHog is running
3. Test the script manually
4. Review cron job syntax
5. Check file permissions and paths
