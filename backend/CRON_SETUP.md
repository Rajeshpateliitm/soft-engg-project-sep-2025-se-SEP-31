# Cron Job Setup for Email Reminders

This guide explains how to set up a cron job to send daily email reminders for quizzes and waste logs using the standalone email reminder script.

## Prerequisites

1. MailHog running (for development/testing)
2. Flask-Mail configured in `app/core/config.py`
3. Python 3.9+ installed
4. All dependencies installed: `pip install -r requirements.txt`

## Script Overview

The `send_email_reminders.py` script:
- Checks all active primary users
- Sends quiz reminders to users who haven't completed a quiz today
- Sends waste log reminders to users who haven't logged waste today
- Uses MailHog for development/testing

## Testing the Script

### Manual Test

Run the script directly to test:

```bash
cd backend
python3 send_email_reminders.py
```

### Continuous Testing (Every 5 Seconds)

For testing purposes, you can use the provided loop script:

```bash
cd backend
./test_email_loop.sh 5
```

This will run the script every 5 seconds. Press `Ctrl+C` to stop.

**Alternative:** If you have `watch` installed (Linux) or install it on macOS:
```bash
# Install watch on macOS
brew install watch

# Then use:
watch -n 5 python3 send_email_reminders.py
```

## Setting Up Cron Job

### Step 1: Find Python Path

First, find the full path to your Python interpreter:

```bash
which python3
# Output example: /usr/bin/python3 or /usr/local/bin/python3
```

### Step 2: Edit Crontab

Open the crontab editor:

```bash
crontab -e
```

### Step 3: Add Cron Job

Add one of the following entries depending on your needs:

#### Daily at 9:00 AM (Recommended)

```cron
0 9 * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /var/log/wastewise_emails.log 2>&1
```

**Important:** Replace `/path/to/backend` with the actual path to your backend directory.

Example:
```cron
0 9 * * * cd /Users/username/Desktop/soft-engg-project-sep-2025-se-SEP-31-dev/backend && /usr/bin/python3 send_email_reminders.py >> /var/log/wastewise_emails.log 2>&1
```

#### For Testing (Every 5 Minutes)

```cron
*/5 * * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /tmp/wastewise_emails.log 2>&1
```

#### For Testing (Every Minute)

```cron
* * * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /tmp/wastewise_emails.log 2>&1
```

### Step 4: Verify Cron Job

Check that your cron job was added:

```bash
crontab -l
```

## Cron Schedule Format

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sunday = 0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

### Common Examples

- `0 9 * * *` - Every day at 9:00 AM
- `0 9 * * 1` - Every Monday at 9:00 AM
- `0 9 1 * *` - First day of every month at 9:00 AM
- `*/5 * * * *` - Every 5 minutes
- `0 */2 * * *` - Every 2 hours
- `0 9,17 * * *` - At 9:00 AM and 5:00 PM daily

## Logging

### Default Log Location

The cron job outputs logs to `/var/log/wastewise_emails.log`. If you don't have write permissions, use `/tmp/wastewise_emails.log` instead.

### View Logs

```bash
# View recent logs
tail -f /var/log/wastewise_emails.log

# Or for /tmp
tail -f /tmp/wastewise_emails.log

# View last 50 lines
tail -n 50 /var/log/wastewise_emails.log
```

### Custom Log Location

To use a custom log location:

```cron
0 9 * * * cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /path/to/custom/log.log 2>&1
```

## Environment Variables

If you need to set environment variables for the cron job, add them before the command:

```cron
0 9 * * * export MAIL_SERVER=localhost && export MAIL_PORT=1025 && cd /path/to/backend && /usr/bin/python3 send_email_reminders.py >> /var/log/wastewise_emails.log 2>&1
```

Or create a wrapper script:

**`backend/run_email_reminders.sh`:**
```bash
#!/bin/bash
export MAIL_SERVER=localhost
export MAIL_PORT=1025
cd /path/to/backend
/usr/bin/python3 send_email_reminders.py
```

Make it executable:
```bash
chmod +x backend/run_email_reminders.sh
```

Then in crontab:
```cron
0 9 * * * /path/to/backend/run_email_reminders.sh >> /var/log/wastewise_emails.log 2>&1
```

## Troubleshooting

### Script Not Running

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

3. **Test script manually:**
   ```bash
   cd /path/to/backend
   python3 send_email_reminders.py
   ```

4. **Check file permissions:**
   ```bash
   ls -l send_email_reminders.py
   # Should show: -rwxr-xr-x or executable permissions
   ```

5. **Verify Python path:**
   ```bash
   which python3
   # Make sure the path in crontab matches this
   ```

### Script Runs But No Emails

1. **Check MailHog is running:**
   ```bash
   # Check if MailHog is listening on port 1025
   lsof -i :1025
   # or
   netstat -an | grep 1025
   ```

2. **Check script output:**
   ```bash
   tail -f /var/log/wastewise_emails.log
   ```

3. **Check Flask-Mail configuration in `config.py`**

### Permission Denied

If you get "Permission denied" errors:

1. **Use full paths** in cron job
2. **Ensure script is executable:**
   ```bash
   chmod +x send_email_reminders.py
   ```
3. **Check log directory permissions:**
   ```bash
   sudo touch /var/log/wastewise_emails.log
   sudo chmod 666 /var/log/wastewise_emails.log
   ```
   Or use `/tmp/wastewise_emails.log` instead

## Testing Workflow

1. **Start MailHog:**
   ```bash
   # Download and run MailHog
   # Or use: mailhog
   ```

2. **Test script manually:**
   ```bash
   cd backend
   python3 send_email_reminders.py
   ```

3. **Check MailHog UI:**
   - Open http://localhost:8025
   - Verify emails were received

4. **Set up cron for testing (every 5 minutes):**
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

## Production Considerations

1. **Use proper log rotation** to prevent log files from growing too large
2. **Monitor email delivery** to ensure reminders are being sent
3. **Set up error alerts** if the script fails
4. **Use absolute paths** in crontab
5. **Test thoroughly** before deploying to production

## Alternative: Systemd Timer (Linux)

For Linux systems, you might prefer systemd timers over cron:

**`/etc/systemd/system/wastewise-email-reminders.service`:**
```ini
[Unit]
Description=WasteWise Email Reminders
After=network.target

[Service]
Type=oneshot
User=your-user
WorkingDirectory=/path/to/backend
ExecStart=/usr/bin/python3 send_email_reminders.py
```

**`/etc/systemd/system/wastewise-email-reminders.timer`:**
```ini
[Unit]
Description=Run WasteWise Email Reminders Daily
Requires=wastewise-email-reminders.service

[Timer]
OnCalendar=daily
OnCalendar=09:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl enable wastewise-email-reminders.timer
sudo systemctl start wastewise-email-reminders.timer
```

## Support

For issues or questions:
1. Check the logs first
2. Verify MailHog is running
3. Test the script manually
4. Review cron job syntax
5. Check file permissions and paths

