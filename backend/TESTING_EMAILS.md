# Testing Email Reminders

This guide explains how to test the email reminder system using the cron-based script.

## Quick Start

### 1. Start MailHog (for email testing)

```bash
# macOS
brew services start mailhog

# Or run directly
mailhog

# Access web interface at: http://localhost:8025
```

### 2. Test Email Script Manually

Run the script directly to test:

```bash
cd backend
python3 send_email_reminders.py
```

You should see output showing:
- Number of primary users found
- Quiz reminders sent
- Waste log reminders sent

### 3. Check MailHog

Open http://localhost:8025 in your browser. You should see the emails that were sent.

## Testing with Cron (Every 5 Minutes)

For testing, set up a cron job that runs every 5 minutes:

1. **Edit crontab:**
   ```bash
   crontab -e
   ```

2. **Add this line (replace `/path/to/backend` with your actual path):**
   ```cron
   */5 * * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /tmp/wastewise_test.log 2>&1
   ```

3. **Monitor logs:**
   ```bash
   # Watch logs in real-time
   watch -n 1 tail -n 20 /tmp/wastewise_test.log
   
   # Or view once
   tail -n 50 /tmp/wastewise_test.log
   ```

4. **Check MailHog** periodically to see new emails coming in

## Testing with Loop Script (Every 5 Seconds)

For rapid testing, use the provided loop script:

```bash
cd backend
./test_email_loop.sh 5
```

This will run the email reminder script every 5 seconds. Press `Ctrl+C` to stop.

**Alternative:** If you have `watch` installed (Linux) or install it on macOS:
```bash
# Install watch on macOS
brew install watch

# Then use:
watch -n 5 python3 send_email_reminders.py
```

**Note:** This will send emails every 5 seconds if users haven't completed quizzes or logged waste. Use with caution in production!

## What to Verify

1. **Script Execution:**
   - Script runs without errors
   - Output shows users processed and emails sent

2. **Email Content:**
   - Emails appear in MailHog
   - Subject lines are correct
   - Email body contains correct information
   - Sign-in links work correctly
   - User names are displayed correctly

3. **Email Timing:**
   - Quiz reminders sent to users who haven't taken quiz today
   - Waste log reminders sent to users who haven't logged waste today
   - Users who have completed both activities don't receive emails

4. **Logs:**
   - Check logs for any errors
   - Verify email sending success/failure messages

## Troubleshooting

### Script Not Running

1. **Check Python path:**
   ```bash
   which python3
   ```

2. **Test script manually:**
   ```bash
   cd /path/to/backend
   python3 send_email_reminders.py
   ```

3. **Check file permissions:**
   ```bash
   chmod +x send_email_reminders.py
   ```

### No Emails Being Sent

1. **Check MailHog is running:**
   ```bash
   lsof -i :1025
   # or
   curl http://localhost:8025/api/v2/messages
   ```

2. **Check script output:**
   ```bash
   python3 send_email_reminders.py
   # Look for error messages
   ```

3. **Verify Flask-Mail configuration** in `app/core/config.py`

4. **Check user emails** in database:
   ```python
   from app import create_app
   from app.models import User
   
   app = create_app()
   with app.app_context():
       users = User.query.filter_by(is_active=True).all()
       for user in users:
           print(f"User {user.id}: {user.email}")
   ```

### Emails Going to Wrong Recipients

1. **Verify user data** in database
2. **Check email addresses** are correct
3. **Review script logic** in `send_email_reminders.py`

### Cron Job Not Running

1. **Check cron service is running:**
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

4. **Test with absolute paths:**
   ```cron
   */5 * * * * cd /full/path/to/backend && /full/path/to/python3 send_email_reminders.py >> /tmp/test.log 2>&1
   ```

## Production Testing

Before deploying to production:

1. **Test with real SMTP server** (not MailHog)
2. **Verify email delivery** to actual email addresses
3. **Test at production schedule** (e.g., daily at 9 AM)
4. **Monitor logs** for several days
5. **Check error handling** by temporarily breaking configuration
6. **Verify timezone settings** are correct

## Stopping Tests

To stop testing:

1. **Stop cron job:**
   ```bash
   crontab -e
   # Comment out or remove the cron job line
   ```

2. **Stop MailHog:**
   ```bash
   # macOS
   brew services stop mailhog
   
   # Or kill the process
   pkill -f mailhog
   ```

3. **Stop watch command:**
   - Press `Ctrl+C` in the terminal

## Next Steps

Once testing is complete:
- Set up production cron job (see `CRON_SETUP.md`)
- Configure production SMTP server
- Set up monitoring and alerts
- Configure log rotation

For more details, see `CRON_SETUP.md` and `README_EMAIL.md`.
