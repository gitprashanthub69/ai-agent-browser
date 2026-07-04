"""
Week 5 — Gmail / Email Helper
Sends emails via Gmail SMTP (simpler than OAuth for the assignment).
Uses environment variables for credentials — never hardcode them.

Setup:
  1. Enable 2FA on your Google account
  2. Go to Google Account → Security → App Passwords
  3. Create an app password for "Mail"
  4. Set environment variables:
       GMAIL_USER=your@gmail.com
       GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to: str, subject: str, body: str) -> dict:
    """
    Sends an email via Gmail SMTP.
    Returns {"success": True} or {"success": False, "error": "..."}
    """
    sender    = os.environ.get("GMAIL_USER")
    password  = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender or not password:
        return {
            "success": False,
            "error": "Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables."
        }

    try:
        msg = MIMEMultipart()
        msg["From"]    = sender
        msg["To"]      = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, to, msg.as_string())

        return {"success": True, "message": f"Email sent to {to}"}

    except smtplib.SMTPAuthenticationError:
        return {"success": False, "error": "Gmail authentication failed. Check your app password."}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── FastAPI route (add to main.py if needed) ──────────────────────────────────

class EmailRequest:
    def __init__(self, to: str, subject: str, body: str):
        self.to      = to
        self.subject = subject
        self.body    = body


if __name__ == "__main__":
    # Quick test
    result = send_email(
        to="test@example.com",
        subject="Test from AI Agent",
        body="This is a test email sent by the AI Browser Agent."
    )
    print(result)
