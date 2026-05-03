"""
Simple Password Reset Service with OTP
Stores OTP codes in memory (for production, use Redis or database)
"""

import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Try to import Resend email service first (Railway-compatible)
try:
    from email_service_resend import resend_email_service
    EMAIL_SERVICE_AVAILABLE = True
    EMAIL_SERVICE_TYPE = "Resend"
    logger.info("✅ Resend email service imported successfully")
except ImportError as e:
    # Fallback to SMTP email service (for localhost)
    try:
        from email_service import email_service as resend_email_service
        EMAIL_SERVICE_AVAILABLE = True
        EMAIL_SERVICE_TYPE = "SMTP"
        logger.info("✅ SMTP email service imported successfully")
    except ImportError as e2:
        EMAIL_SERVICE_AVAILABLE = False
        EMAIL_SERVICE_TYPE = "None"
        logger.error(f"❌ Failed to import any email service: {e}, {e2}")
except Exception as e:
    EMAIL_SERVICE_AVAILABLE = False
    EMAIL_SERVICE_TYPE = "None"
    logger.error(f"❌ Error importing email service: {e}")

class PasswordResetStorage:
    """In-memory storage for password reset OTPs"""
    
    def __init__(self):
        self.otps: Dict[str, dict] = {}
        self.cooldowns: Dict[str, datetime] = {}
    
    def create_otp(self, email: str, expiry_minutes: int = 10, length: int = 6) -> str:
        """Generate and store a random OTP"""
        otp = ''.join(secrets.choice(string.digits) for _ in range(length))
        
        # Store OTP with expiry
        self.otps[email] = {
            'otp': otp,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(minutes=expiry_minutes),
            'attempts': 0
        }
        
        logger.info(f"✅ OTP created for {email}")
        logger.info(f"✅ OTP will expire at: {self.otps[email]['expires_at'].strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        return otp
    
    def verify_otp(self, email: str, otp: str, max_attempts: int = 3) -> Tuple[bool, str]:
        """Verify OTP and return (is_valid, error_message)"""
        
        if email not in self.otps:
            return False, "No OTP found. Please request a new one."
        
        otp_data = self.otps[email]
        
        # Check if expired
        if datetime.utcnow() > otp_data['expires_at']:
            del self.otps[email]
            return False, "OTP has expired. Please request a new one."
        
        # Check attempts
        if otp_data['attempts'] >= max_attempts:
            del self.otps[email]
            return False, "Too many failed attempts. Please request a new OTP."
        
        # Verify OTP
        if otp_data['otp'] == otp:
            del self.otps[email]  # Remove after successful verification
            return True, ""
        else:
            otp_data['attempts'] += 1
            remaining = max_attempts - otp_data['attempts']
            return False, f"Invalid OTP. {remaining} attempts remaining."
    
    def check_cooldown(self, email: str, cooldown_seconds: int = 60) -> Tuple[bool, int]:
        """Check if email is in cooldown period. Returns (in_cooldown, seconds_remaining)"""
        
        if email not in self.cooldowns:
            return False, 0
        
        last_request = self.cooldowns[email]
        elapsed = (datetime.utcnow() - last_request).total_seconds()
        
        if elapsed < cooldown_seconds:
            remaining = int(cooldown_seconds - elapsed)
            return True, remaining
        else:
            del self.cooldowns[email]
            return False, 0
    
    def set_cooldown(self, email: str, cooldown_seconds: int = 60):
        """Set cooldown for email"""
        self.cooldowns[email] = datetime.utcnow()
    
    def cleanup_expired(self):
        """Remove expired OTPs (call periodically)"""
        now = datetime.utcnow()
        expired = [email for email, data in self.otps.items() if now > data['expires_at']]
        for email in expired:
            del self.otps[email]

# Global instance
password_reset_storage = PasswordResetStorage()

def send_password_reset_email(email: str, otp: str, expiry_minutes: int = 10) -> bool:
    """
    Send password reset email with OTP
    Uses Resend API on Railway, SMTP on localhost
    Falls back to logging if email service is not configured
    """
    email_sent = False
    
    if not EMAIL_SERVICE_AVAILABLE:
        logger.error("❌ Email service not available - import failed at module level")
        logger.error("❌ Check Railway logs for import errors")
        # Fall through to logging fallback
    else:
        try:
            logger.info(f"📧 Using {EMAIL_SERVICE_TYPE} email service")
            logger.info(f"📧 Email service configured: {resend_email_service.is_configured}")
            
            if resend_email_service.is_configured:
                logger.info(f"📧 Attempting to send email via {EMAIL_SERVICE_TYPE}...")
                # Send actual email
                success = resend_email_service.send_password_reset_otp(email, otp, expiry_minutes)
                
                if success:
                    logger.info(f"✅ Password reset OTP email sent to {email} via {EMAIL_SERVICE_TYPE}")
                    email_sent = True
                    return True
                else:
                    logger.error(f"❌ Failed to send OTP email to {email}")
                    logger.error(f"❌ Check Railway logs for {EMAIL_SERVICE_TYPE} errors")
                    # Fall through to logging fallback
            else:
                logger.warning(f"⚠️  {EMAIL_SERVICE_TYPE} email service not configured - falling back to logs")
                # Fall through to logging fallback
        
        except Exception as e:
            logger.error(f"❌ Email service error: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            # Fall through to logging fallback
    
    # Fallback: Log OTP if email fails or is not configured
    logger.info("")
    logger.info("=" * 80)
    logger.info("📧 📧 📧  PASSWORD RESET OTP CODE (EMAIL FALLBACK)  📧 📧 📧")
    logger.info("=" * 80)
    logger.info(f"📧 Email: {email}")
    logger.info(f"📧 OTP Code: {otp}")
    logger.info(f"📧 Valid for: {expiry_minutes} minutes")
    logger.info(f"📧 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    logger.info("=" * 80)
    logger.info("⚠️  Email service not available - check Railway logs for OTP")
    logger.info("⚠️  Configure MAIL_USERNAME and MAIL_PASSWORD to enable email")
    logger.info("=" * 80)
    logger.info("")
    
    # Also print to stdout
    print("")
    print("=" * 80)
    print("📧 PASSWORD RESET OTP (CHECK YOUR EMAIL)")
    print("=" * 80)
    print(f"📧 Email: {email}")
    print(f"📧 OTP Code: {otp}")
    print("=" * 80)
    print("")
    
    return True
