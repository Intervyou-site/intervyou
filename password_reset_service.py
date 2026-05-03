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
        
        logger.info(f"📧 Generated OTP for {email}: {otp}")
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
    For now, just logs the OTP (in production, use actual email service)
    """
    try:
        logger.info("=" * 60)
        logger.info(f"📧 PASSWORD RESET OTP")
        logger.info(f"📧 Email: {email}")
        logger.info(f"📧 OTP Code: {otp}")
        logger.info(f"📧 Valid for: {expiry_minutes} minutes")
        logger.info("=" * 60)
        logger.info("⚠️  In production, this would be sent via email service")
        logger.info("⚠️  For now, check Railway logs to see the OTP")
        
        # TODO: Integrate with actual email service
        # Example with your existing email config:
        # from email_service import send_email
        # send_email(
        #     to=email,
        #     subject="Password Reset OTP",
        #     body=f"Your password reset code is: {otp}\nValid for {expiry_minutes} minutes."
        # )
        
        return True
    except Exception as e:
        logger.error(f"Failed to send password reset email: {e}")
        return False
