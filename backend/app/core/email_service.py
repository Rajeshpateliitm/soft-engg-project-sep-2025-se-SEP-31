"""Email service for sending notifications."""
from flask import current_app
from flask_mail import Mail, Message
from datetime import date

mail = Mail()


def init_mail(app):
    """Initialize Flask-Mail extension."""
    mail.init_app(app)


def send_email(to, subject, body, html=None):
    """
    Send an email.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Plain text email body
        html: Optional HTML email body
    """
    try:
        msg = Message(
            subject=subject,
            recipients=[to],
            body=body,
            html=html,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        current_app.logger.info(f"Email sent successfully to {to}")
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email to {to}: {str(e)}")
        return False


def send_waste_log_reminder(user_email, username):
    """
    Send daily waste log reminder email.
    
    Args:
        user_email: User's email address
        username: User's username or name
    """
    subject = "Daily Waste Log Reminder - WasteWise"
    
    body = f"""
Hello {username or 'User'},

This is a friendly reminder to log your daily waste entry in WasteWise.

Logging your waste helps:
- Track your environmental impact
- Earn points and climb the leaderboard
- Contribute to community sustainability goals

Visit the app to log today's waste: http://localhost:5173/primary/waste-log

Thank you for being part of the WasteWise community!

Best regards,
WasteWise Team
"""
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #28a745;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border-radius: 0 0 5px 5px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 30px;
            background-color: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌱 WasteWise Daily Reminder</h1>
    </div>
    <div class="content">
        <p>Hello <strong>{username or 'User'}</strong>,</p>
        
        <p>This is a friendly reminder to log your daily waste entry in WasteWise.</p>
        
        <h3>Why log your waste?</h3>
        <ul>
            <li>Track your environmental impact</li>
            <li>Earn points and climb the leaderboard</li>
            <li>Contribute to community sustainability goals</li>
        </ul>
        
        <div style="text-align: center;">
            <a href="http://localhost:5173/primary/waste-log" class="button">Log Your Waste Now</a>
        </div>
        
        <p>Thank you for being part of the WasteWise community!</p>
    </div>
    <div class="footer">
        <p>WasteWise Team</p>
        <p>This is an automated reminder. Please do not reply to this email.</p>
    </div>
</body>
</html>
"""
    
    return send_email(user_email, subject, body, html)


def send_quiz_reminder(user_email, username):
    """
    Send daily quiz reminder email.
    
    Args:
        user_email: User's email address
        username: User's username or name
    """
    subject = "Daily Quiz Reminder - WasteWise"
    
    body = f"""
Hello {username or 'User'},

Don't forget to take today's waste management quiz in WasteWise!

Taking the daily quiz helps you:
- Learn about sustainable waste management
- Earn points (10 points per correct answer)
- Improve your ranking on the leaderboard
- Build your knowledge streak

Visit the app to take today's quiz: http://localhost:5173/primary/quiz

Keep up the great work!

Best regards,
WasteWise Team
"""
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #007bff;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border-radius: 0 0 5px 5px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 30px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }}
        .benefits {{
            background-color: #e7f3ff;
            padding: 15px;
            border-left: 4px solid #007bff;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 WasteWise Quiz Reminder</h1>
    </div>
    <div class="content">
        <p>Hello <strong>{username or 'User'}</strong>,</p>
        
        <p>Don't forget to take today's waste management quiz in WasteWise!</p>
        
        <div class="benefits">
            <h3>Benefits of taking the quiz:</h3>
            <ul>
                <li>Learn about sustainable waste management</li>
                <li>Earn points (10 points per correct answer)</li>
                <li>Improve your ranking on the leaderboard</li>
                <li>Build your knowledge streak</li>
            </ul>
        </div>
        
        <div style="text-align: center;">
            <a href="http://localhost:5173/primary/quiz" class="button">Take Quiz Now</a>
        </div>
        
        <p>Keep up the great work!</p>
    </div>
    <div class="footer">
        <p>WasteWise Team</p>
        <p>This is an automated reminder. Please do not reply to this email.</p>
    </div>
</body>
</html>
"""
    
    return send_email(user_email, subject, body, html)

