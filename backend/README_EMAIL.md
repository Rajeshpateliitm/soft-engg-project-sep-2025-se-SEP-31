# Daily Email Notification System

This document provides a quick start guide for the daily email notification system using cron jobs.

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start MailHog (for email testing)

```bash
# macOS
brew services start mailhog

# Or run directly
mailhog

# Access web interface at: http://localhost:8025
```

### 3. Test Email Script Manually

```bash
cd backend
python3 send_email_reminders.py
```

You should see output like:
```
============================================================
WasteWise Email Reminder Script
============================================================
Time: 2025-01-XX

Found X primary users to check
✓ Quiz reminder sent to user@example.com
✓ Waste log reminder sent to user@example.com

✓ Daily reminders completed:
  - Quiz reminders sent: X
  - Waste log reminders sent: X

✓ Email reminder script completed successfully
```

### 4. Check MailHog

1. Open http://localhost:8025
2. You should see the emails in the MailHog interface
3. Click on an email to view its contents and verify the signin link

## Setting Up Cron Job

### Quick Setup (Daily at 9:00 AM)

1. **Edit crontab:**
   ```bash
   crontab -e
   ```

2. **Add this line (replace `/path/to/backend` with your actual path):**
   ```cron
   0 9 * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /var/log/wastewise_emails.log 2>&1
   ```

3. **Verify:**
   ```bash
   crontab -l
   ```

### For Testing (Every 5 Minutes)

```cron
*/5 * * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /tmp/wastewise_test.log 2>&1
```

### For Testing (Every Minute)

```cron
* * * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /tmp/wastewise_test.log 2>&1
```

## Configuration

### Change Application URL

Edit `backend/app/core/config.py`:

```python
APP_URL = "http://localhost:5173"  # Your frontend URL
SIGNIN_URL = f"{APP_URL}/signin"
```

### MailHog Configuration (Development)

Default configuration in `app/core/config.py`:
```python
MAIL_SERVER = "localhost"
MAIL_PORT = 1025
```

### Production SMTP Configuration

For production, update `app/core/config.py` or use environment variables:

```python
MAIL_SERVER = os.environ.get("MAIL_SERVER") or "smtp.example.com"
MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
```

## Monitoring

### Check Logs

```bash
# View recent logs
tail -f /var/log/wastewise_emails.log

# Or for /tmp (testing)
tail -f /tmp/wastewise_test.log

# View last 50 lines
tail -n 50 /var/log/wastewise_emails.log
```

### Verify Cron Job is Running

```bash
# List all cron jobs
crontab -l

# Check cron service (Linux)
sudo systemctl status cron

# Check cron logs (Linux)
grep CRON /var/log/syslog

# Check cron logs (macOS)
grep CRON /var/log/system.log
```

## Testing Workflow

1. **Start MailHog:**
   ```bash
   mailhog
   ```

2. **Test script manually:**
   ```bash
   cd backend
   python3 send_email_reminders.py
   ```

3. **Check MailHog UI** (http://localhost:8025) to verify emails

4. **Set up cron for testing** (every 5 minutes):
   ```cron
   */5 * * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /tmp/wastewise_test.log 2>&1
   ```

5. **Monitor logs:**
   ```bash
   watch -n 1 tail -n 20 /tmp/wastewise_test.log
   ```

6. **Update to production schedule** once tested:
   ```cron
   0 9 * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /var/log/wastewise_emails.log 2>&1
   ```

## Troubleshooting

### Script Not Running

1. **Test script manually:**
   ```bash
   cd /path/to/backend
   python3 send_email_reminders.py
   ```

2. **Check Python path in crontab:**
   ```bash
   which python3
   # Use this path in crontab
   ```

3. **Check file permissions:**
   ```bash
   chmod +x send_email_reminders.py
   ```

4. **Use absolute paths** in crontab

### No Emails Being Sent

1. **Check MailHog is running:**
   ```bash
   lsof -i :1025
   ```

2. **Check script output in logs:**
   ```bash
   tail -f /var/log/wastewise_emails.log
   ```

3. **Verify Flask-Mail configuration**

## Production

For production deployment:

1. Replace MailHog with a real SMTP server (SendGrid, Mailgun, AWS SES, Gmail SMTP)
2. Update email configuration in `app/core/config.py` or use environment variables
3. Set up proper log rotation for email logs
4. Configure monitoring and alerts for failed email sends
5. Use proper timezone settings in cron job

## Documentation

For detailed cron job setup instructions, see `CRON_SETUP.md`.

For email server setup (MailHog), see `EMAIL_SETUP.md`.
