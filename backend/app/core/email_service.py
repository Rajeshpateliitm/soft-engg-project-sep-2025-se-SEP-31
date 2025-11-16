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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
            background-color: #f4f4f4;
            padding: 20px;
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: #ffffff;
            padding: 40px 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }}
        .header .icon {{
            font-size: 48px;
            margin-bottom: 15px;
            display: block;
        }}
        .content {{
            padding: 40px 30px;
            background-color: #ffffff;
        }}
        .greeting {{
            font-size: 18px;
            color: #333333;
            margin-bottom: 20px;
            font-weight: 500;
        }}
        .greeting strong {{
            color: #28a745;
            font-weight: 600;
        }}
        .message {{
            font-size: 16px;
            color: #555555;
            margin-bottom: 30px;
            line-height: 1.8;
        }}
        .benefits-section {{
            background: linear-gradient(135deg, #f0f9f4 0%, #e8f5e9 100%);
            border-left: 4px solid #28a745;
            padding: 25px;
            margin: 30px 0;
            border-radius: 8px;
        }}
        .benefits-section h3 {{
            color: #1e7e34;
            font-size: 20px;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        .benefits-section ul {{
            list-style: none;
            padding-left: 0;
        }}
        .benefits-section li {{
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
            color: #2d5016;
            font-size: 15px;
        }}
        .benefits-section li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #28a745;
            font-weight: bold;
            font-size: 18px;
        }}
        .button-container {{
            text-align: center;
            margin: 35px 0;
        }}
        .button {{
            display: inline-block;
            padding: 16px 40px;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
            transition: transform 0.2s, box-shadow 0.2s;
            letter-spacing: 0.5px;
        }}
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
        }}
        .closing {{
            font-size: 16px;
            color: #555555;
            margin-top: 30px;
            text-align: center;
            font-style: italic;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 25px 30px;
            text-align: center;
            border-top: 1px solid #e9ecef;
        }}
        .footer p {{
            color: #6c757d;
            font-size: 13px;
            margin: 5px 0;
        }}
        .footer .brand {{
            color: #28a745;
            font-weight: 600;
            font-size: 14px;
        }}
        @media only screen and (max-width: 600px) {{
            .content {{
                padding: 30px 20px;
            }}
            .header {{
                padding: 30px 20px;
            }}
            .header h1 {{
                font-size: 24px;
            }}
            .button {{
                padding: 14px 30px;
                font-size: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <span class="icon">🌱</span>
            <h1>WasteWise Daily Reminder</h1>
            <p style="margin-top: 10px; opacity: 0.95; font-size: 15px;">Your daily waste logging reminder</p>
        </div>
        <div class="content">
            <div class="greeting">
                Hello <strong>{username or 'User'}</strong>! 👋
            </div>
            <div class="message">
                This is a friendly reminder to log your daily waste entry in WasteWise. 
                Your commitment to tracking waste helps create a cleaner, more sustainable community.
            </div>
            <div class="benefits-section">
                <h3>Why log your waste?</h3>
                <ul>
                    <li>Track your environmental impact and carbon footprint</li>
                    <li>Earn points and climb the leaderboard rankings</li>
                    <li>Contribute to community sustainability goals</li>
                    <li>Build positive environmental habits</li>
                </ul>
            </div>
            <div class="button-container">
                <a href="http://localhost:5173/primary/waste-log" class="button">Log Your Waste Now →</a>
            </div>
            <div class="closing">
                Thank you for being part of the WasteWise community! 🌍
            </div>
        </div>
        <div class="footer">
            <p class="brand">WasteWise Team</p>
            <p>Making waste management smarter, one log at a time.</p>
            <p style="margin-top: 15px; font-size: 12px; color: #adb5bd;">
                This is an automated reminder. Please do not reply to this email.
            </p>
        </div>
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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
            background-color: #f4f4f4;
            padding: 20px;
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: #ffffff;
            padding: 40px 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }}
        .header .icon {{
            font-size: 48px;
            margin-bottom: 15px;
            display: block;
        }}
        .content {{
            padding: 40px 30px;
            background-color: #ffffff;
        }}
        .greeting {{
            font-size: 18px;
            color: #333333;
            margin-bottom: 20px;
            font-weight: 500;
        }}
        .greeting strong {{
            color: #007bff;
            font-weight: 600;
        }}
        .message {{
            font-size: 16px;
            color: #555555;
            margin-bottom: 30px;
            line-height: 1.8;
        }}
        .benefits-section {{
            background: linear-gradient(135deg, #e7f3ff 0%, #d0e7ff 100%);
            border-left: 4px solid #007bff;
            padding: 25px;
            margin: 30px 0;
            border-radius: 8px;
        }}
        .benefits-section h3 {{
            color: #004085;
            font-size: 20px;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        .benefits-section ul {{
            list-style: none;
            padding-left: 0;
        }}
        .benefits-section li {{
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
            color: #004085;
            font-size: 15px;
        }}
        .benefits-section li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #007bff;
            font-weight: bold;
            font-size: 18px;
        }}
        .points-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%);
            color: #000000;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
            margin-top: 10px;
        }}
        .button-container {{
            text-align: center;
            margin: 35px 0;
        }}
        .button {{
            display: inline-block;
            padding: 16px 40px;
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
            transition: transform 0.2s, box-shadow 0.2s;
            letter-spacing: 0.5px;
        }}
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
        }}
        .closing {{
            font-size: 16px;
            color: #555555;
            margin-top: 30px;
            text-align: center;
            font-style: italic;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 25px 30px;
            text-align: center;
            border-top: 1px solid #e9ecef;
        }}
        .footer p {{
            color: #6c757d;
            font-size: 13px;
            margin: 5px 0;
        }}
        .footer .brand {{
            color: #007bff;
            font-weight: 600;
            font-size: 14px;
        }}
        @media only screen and (max-width: 600px) {{
            .content {{
                padding: 30px 20px;
            }}
            .header {{
                padding: 30px 20px;
            }}
            .header h1 {{
                font-size: 24px;
            }}
            .button {{
                padding: 14px 30px;
                font-size: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <span class="icon">📚</span>
            <h1>WasteWise Quiz Reminder</h1>
            <p style="margin-top: 10px; opacity: 0.95; font-size: 15px;">Test your knowledge and earn points!</p>
        </div>
        <div class="content">
            <div class="greeting">
                Hello <strong>{username or 'User'}</strong>! 👋
            </div>
            <div class="message">
                Don't forget to take today's waste management quiz in WasteWise! 
                Each quiz helps you learn more about sustainable waste practices and boosts your leaderboard ranking.
            </div>
            <div class="benefits-section">
                <h3>Benefits of taking the quiz:</h3>
                <ul>
                    <li>Learn about sustainable waste management practices</li>
                    <li>Earn points (10 points per correct answer) 🎯</li>
                    <li>Improve your ranking on the community leaderboard</li>
                    <li>Build your knowledge streak and daily habits</li>
                </ul>
                <div style="margin-top: 15px; text-align: center;">
                    <span class="points-badge">+10 Points per correct answer</span>
                </div>
            </div>
            <div class="button-container">
                <a href="http://localhost:5173/primary/quiz" class="button">Take Quiz Now →</a>
            </div>
            <div class="closing">
                Keep up the great work and keep learning! 🚀
            </div>
        </div>
        <div class="footer">
            <p class="brand">WasteWise Team</p>
            <p>Making waste management smarter, one quiz at a time.</p>
            <p style="margin-top: 15px; font-size: 12px; color: #adb5bd;">
                This is an automated reminder. Please do not reply to this email.
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    return send_email(user_email, subject, body, html)

