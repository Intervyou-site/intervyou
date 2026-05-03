"""
Email Service for Sending OTP and Notifications
Uses Gmail SMTP with app password
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

logger = logging.getLogger(__name__)

# Check if we're in production by looking for Railway-specific env vars
# Railway always sets DATABASE_URL, so we can use that as a marker
IS_PRODUCTION = bool(os.environ.get("DATABASE_URL", "").startswith("postgres"))

# Only load .env for local development
if not IS_PRODUCTION:
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
        logger.info("📝 Loaded .env file for local development")
    except ImportError:
        logger.warning("⚠️  dotenv not available, using system environment variables")
else:
    logger.info("🚀 Production mode - using Railway environment variables")

class EmailService:
    """Email service for sending OTP and notifications"""
    
    def __init__(self):
        # Get environment variables directly from os.environ (Railway way)
        self.smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        self.mail_username = os.environ.get("MAIL_USERNAME")
        self.mail_password = os.environ.get("MAIL_PASSWORD")
        self.mail_from = os.environ.get("MAIL_FROM", self.mail_username)
        self.mail_from_name = os.environ.get("MAIL_FROM_NAME", "IntervYou Support")
        
        # Debug logging
        logger.info(f"🔍 Email Service Initialization:")
        logger.info(f"🔍 ENVIRONMENT: {os.environ.get('ENVIRONMENT', 'not set')}")
        logger.info(f"🔍 SMTP_HOST: {self.smtp_host}")
        logger.info(f"🔍 SMTP_PORT: {self.smtp_port}")
        logger.info(f"🔍 MAIL_USERNAME present: {bool(self.mail_username)}")
        logger.info(f"🔍 MAIL_USERNAME value: {self.mail_username if self.mail_username else 'NOT SET'}")
        logger.info(f"🔍 MAIL_PASSWORD present: {bool(self.mail_password)}")
        logger.info(f"🔍 MAIL_PASSWORD length: {len(self.mail_password) if self.mail_password else 0}")
        logger.info(f"🔍 MAIL_FROM: {self.mail_from}")
        
        # Check if email is configured
        self.is_configured = bool(self.mail_username and self.mail_password)
        
        if not self.is_configured:
            logger.warning("⚠️  Email service not configured - missing MAIL_USERNAME or MAIL_PASSWORD")
            logger.warning(f"⚠️  MAIL_USERNAME present: {bool(self.mail_username)}")
            logger.warning(f"⚠️  MAIL_PASSWORD present: {bool(self.mail_password)}")
        else:
            logger.info(f"✅ Email service configured - SMTP: {self.smtp_host}:{self.smtp_port}")
            logger.info(f"✅ Sending from: {self.mail_from}")
    
    def send_email(self, to_email: str, subject: str, body_html: str, body_text: str = None) -> bool:
        """
        Send an email using Gmail SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: HTML body content
            body_text: Plain text body (optional, will use HTML if not provided)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.is_configured:
            logger.error("❌ Cannot send email - email service not configured")
            logger.error(f"❌ MAIL_USERNAME: {bool(self.mail_username)}")
            logger.error(f"❌ MAIL_PASSWORD: {bool(self.mail_password)}")
            return False
        
        try:
            logger.info(f"📧 Attempting to send email to {to_email}")
            logger.info(f"📧 SMTP: {self.smtp_host}:{self.smtp_port}")
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.mail_from_name} <{self.mail_from}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text version
            if body_text:
                part1 = MIMEText(body_text, 'plain')
                msg.attach(part1)
            
            # Add HTML version
            part2 = MIMEText(body_html, 'html')
            msg.attach(part2)
            
            # Connect to SMTP server and send
            logger.info(f"📧 Connecting to SMTP server...")
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:
                logger.info(f"📧 Starting TLS...")
                server.starttls()  # Secure the connection
                logger.info(f"📧 Logging in as {self.mail_username}...")
                server.login(self.mail_username, self.mail_password)
                logger.info(f"📧 Sending message...")
                server.send_message(msg)
            
            logger.info(f"✅ Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ SMTP Authentication failed: {e}")
            logger.error(f"❌ Check MAIL_USERNAME and MAIL_PASSWORD in Railway")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to send email to {to_email}: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            return False
    
    def send_password_reset_otp(self, to_email: str, otp: str, expiry_minutes: int = 10) -> bool:
        """
        Send password reset OTP email
        
        Args:
            to_email: Recipient email address
            otp: One-time password code
            expiry_minutes: How long the OTP is valid
        
        Returns:
            bool: True if email sent successfully
        """
        subject = "IntervYou - Password Reset Code"
        
        # HTML email body
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .otp-code {{
                    background: white;
                    border: 2px dashed #667eea;
                    padding: 20px;
                    text-align: center;
                    font-size: 32px;
                    font-weight: bold;
                    letter-spacing: 8px;
                    color: #667eea;
                    margin: 20px 0;
                    border-radius: 5px;
                }}
                .warning {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Password Reset Request</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>You requested to reset your password for your IntervYou account. Use the verification code below to complete the process:</p>
                    
                    <div class="otp-code">
                        {otp}
                    </div>
                    
                    <p><strong>This code will expire in {expiry_minutes} minutes.</strong></p>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong><br>
                        If you didn't request this password reset, please ignore this email. Your password will remain unchanged.
                    </div>
                    
                    <p>For security reasons, never share this code with anyone.</p>
                    
                    <p>Best regards,<br>
                    The IntervYou Team</p>
                </div>
                <div class="footer">
                    <p>This is an automated email. Please do not reply.</p>
                    <p>&copy; {datetime.now().year} IntervYou. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        body_text = f"""
        Password Reset Request
        
        Hello,
        
        You requested to reset your password for your IntervYou account.
        
        Your verification code is: {otp}
        
        This code will expire in {expiry_minutes} minutes.
        
        If you didn't request this password reset, please ignore this email.
        Your password will remain unchanged.
        
        For security reasons, never share this code with anyone.
        
        Best regards,
        The IntervYou Team
        
        ---
        This is an automated email. Please do not reply.
        © {datetime.now().year} IntervYou. All rights reserved.
        """
        
        return self.send_email(to_email, subject, body_html, body_text)
    
    def send_welcome_email(self, to_email: str, name: str) -> bool:
        """Send welcome email to new users"""
        subject = "Welcome to IntervYou! 🎉"
        
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to IntervYou! 🎉</h1>
                </div>
                <div class="content">
                    <p>Hi {name},</p>
                    <p>Thank you for joining IntervYou! We're excited to help you ace your interviews.</p>
                    <p>Get started by exploring our features:</p>
                    <ul>
                        <li>AI-powered interview practice</li>
                        <li>Resume builder</li>
                        <li>Coding challenges</li>
                        <li>Progress tracking</li>
                    </ul>
                    <p>Best of luck with your interview preparation!</p>
                    <p>The IntervYou Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        body_text = f"Hi {name},\n\nWelcome to IntervYou! We're excited to help you ace your interviews.\n\nBest regards,\nThe IntervYou Team"
        
        return self.send_email(to_email, subject, body_html, body_text)


# Global email service instance
email_service = EmailService()

# Convenience function for backward compatibility
def send_password_reset_email(email: str, otp: str, expiry_minutes: int = 10) -> bool:
    """Send password reset OTP email"""
    return email_service.send_password_reset_otp(email, otp, expiry_minutes)
