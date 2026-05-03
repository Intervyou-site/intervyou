"""
Email Service using Resend API (Railway-compatible)
Resend works on Railway because it uses HTTPS, not SMTP
"""

import os
import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

# Check if we're in production
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


class ResendEmailService:
    """Email service using Resend API (works on Railway)"""
    
    def __init__(self):
        # Get Resend API key from environment
        self.api_key = os.environ.get("RESEND_API_KEY")
        self.from_email = os.environ.get("RESEND_FROM_EMAIL", "onboarding@resend.dev")
        self.from_name = os.environ.get("MAIL_FROM_NAME", "IntervYou Support")
        
        # Resend API endpoint
        self.api_url = "https://api.resend.com/emails"
        
        # Check if configured
        self.is_configured = bool(self.api_key)
        
        # Debug logging
        logger.info(f"🔍 Resend Email Service Initialization:")
        logger.info(f"🔍 RESEND_API_KEY present: {bool(self.api_key)}")
        logger.info(f"🔍 RESEND_FROM_EMAIL: {self.from_email}")
        
        if not self.is_configured:
            logger.warning("⚠️  Resend not configured - missing RESEND_API_KEY")
        else:
            logger.info(f"✅ Resend email service configured")
            logger.info(f"✅ Sending from: {self.from_email}")
    
    def send_email(self, to_email: str, subject: str, body_html: str, body_text: str = None) -> bool:
        """
        Send an email using Resend API
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: HTML body content
            body_text: Plain text body (optional)
        
        Returns:
            bool: True if email sent successfully
        """
        if not self.is_configured:
            logger.error("❌ Cannot send email - Resend not configured")
            logger.error("❌ Set RESEND_API_KEY in Railway environment variables")
            return False
        
        try:
            logger.info(f"📧 Attempting to send email via Resend API to {to_email}")
            
            # Prepare email data
            email_data = {
                "from": f"{self.from_name} <{self.from_email}>",
                "to": [to_email],
                "subject": subject,
                "html": body_html
            }
            
            # Add text version if provided
            if body_text:
                email_data["text"] = body_text
            
            # Send via Resend API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            logger.info(f"📧 Sending request to Resend API...")
            response = requests.post(
                self.api_url,
                json=email_data,
                headers=headers,
                timeout=30
            )
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Email sent successfully via Resend to {to_email}")
                logger.info(f"✅ Resend email ID: {result.get('id', 'unknown')}")
                return True
            else:
                logger.error(f"❌ Resend API error: {response.status_code}")
                logger.error(f"❌ Response: {response.text}")
                return False
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error calling Resend API: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to send email via Resend: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            return False
    
    def send_password_reset_otp(self, to_email: str, otp: str, expiry_minutes: int = 10) -> bool:
        """Send password reset OTP email"""
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


# Global instance
resend_email_service = ResendEmailService()

# Convenience function
def send_password_reset_email(email: str, otp: str, expiry_minutes: int = 10) -> bool:
    """Send password reset OTP email via Resend"""
    return resend_email_service.send_password_reset_otp(email, otp, expiry_minutes)
