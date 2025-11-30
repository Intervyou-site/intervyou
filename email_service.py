# email_service.py
"""
Email Service for Password Reset
Sends OTP emails using SMTP
"""

import os
import smtplib
from email.message import EmailMessage
from typing import Optional

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME or "no-reply@intervyou.com")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "IntervYou Support")


def send_otp_email(to_email: str, otp: str, expiry_minutes: int = 10) -> bool:
    """
    Send OTP email for password reset
    Returns True if successful, False otherwise
    """
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        print("⚠️  Email not configured. OTP:", otp)
        return False
    
    subject = "Your IntervYou Password Reset Code"
    body = f"""Hello,

You requested to reset your IntervYou password.

Your verification code is: {otp}

This code will expire in {expiry_minutes} minutes.

If you didn't request this, please ignore this email.

Best regards,
IntervYou Team
"""
    
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{MAIL_FROM_NAME} <{MAIL_FROM}>"
        msg["To"] = to_email
        msg.set_content(body)
        
        if SMTP_PORT == 587:
            # TLS
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
        elif SMTP_PORT == 465:
            # SSL
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=15)
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
        else:
            # Plain (not recommended)
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
            server.send_message(msg)
            server.quit()
        
        print(f"✅ OTP email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


def send_welcome_email(to_email: str, name: str) -> bool:
    """Send welcome email to new users"""
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        return False
    
    subject = "Welcome to IntervYou!"
    body = f"""Hello {name},

Welcome to IntervYou - Your AI Interview Coach!

We're excited to have you on board. Here's what you can do:

🎯 Practice interview questions
🧠 Get AI-powered feedback
📊 Track your progress
🏆 Compete on the leaderboard

Get started now: http://localhost:8000

Best regards,
IntervYou Team
"""
    
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{MAIL_FROM_NAME} <{MAIL_FROM}>"
        msg["To"] = to_email
        msg.set_content(body)
        
        if SMTP_PORT == 587:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
        elif SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=15)
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
        
        return True
    except Exception as e:
        print(f"❌ Failed to send welcome email: {e}")
        return False
