# auth_routes.py
"""
OAuth Social Login Routes and Secure Password Reset Implementation
Enhanced with rate limiting, secure token generation, and proper security measures
"""

from fastapi import APIRouter, Request, Depends, Form, BackgroundTasks, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
import logging

# Import from main app
from oauth_config import oauth

# Import security services
from rate_limiter import rate_limiter

logger = logging.getLogger(__name__)

# Simple session helper (since SessionSecurity doesn't exist)
def create_secure_session(request, user_id: int, remember_me: bool = False):
    """Create a secure session for the user"""
    request.session["user_id"] = user_id
    request.session["logged_in"] = True
    request.session["login_time"] = datetime.utcnow().isoformat()
    if remember_me:
        request.session["remember_me"] = True

# Import password reset service (if available)
try:
    from password_reset_service import (
        password_reset_storage, 
        send_password_reset_email
    )
    PASSWORD_RESET_AVAILABLE = True
except ImportError as e:
    PASSWORD_RESET_AVAILABLE = False
    password_reset_storage = None
    send_password_reset_email = None
    logger.warning(f"⚠️  Password reset service not available: {e}")

logger = logging.getLogger(__name__)

router = APIRouter()

# Helper to get DB session (will be injected from main app)
def get_db():
    from fastapi_app_cleaned import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db):
    from fastapi_app_cleaned import User
    uid = request.session.get("user_id")
    if not uid:
        return None
    return db.query(User).filter_by(id=uid).first()

def add_flash(request: Request, message: str, category: str = "info"):
    flashes = request.session.setdefault("_flashes", [])
    flashes.append({"msg": message, "cat": category})
    request.session["_flashes"] = flashes


# ==================== GOOGLE OAUTH ====================

@router.get("/auth/google")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth callback with enhanced security"""
    from fastapi_app_cleaned import User, get_password_hash
    
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            add_flash(request, "Failed to get user info from Google", "danger")
            return RedirectResponse("/login", status_code=303)
        
        email = user_info.get('email')
        name = user_info.get('name') or email.split('@')[0]
        
        # Validate email
        if not email:
            add_flash(request, "No email provided by Google", "danger")
            return RedirectResponse("/login", status_code=303)
        
        # Check if user exists
        user = db.query(User).filter_by(email=email).first()
        
        if not user:
            # Create new user with OAuth
            # Generate secure random password for OAuth users
            import secrets
            random_password = secrets.token_urlsafe(32)
            
            user = User(
                name=name,
                email=email,
                password=get_password_hash(random_password),
                email_verified=1  # OAuth emails are pre-verified
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            add_flash(request, f"Welcome {name}! Account created via Google.", "success")
            logger.info(f"✅ New user created via Google OAuth: {email}")
        else:
            # Mark email as verified if not already
            if not user.email_verified:
                user.email_verified = 1
                db.commit()
            add_flash(request, f"Welcome back {name}!", "success")
            logger.info(f"✅ User logged in via Google OAuth: {email}")
        
        # Create secure session
        create_secure_session(request, user.id, remember_me=False)
        request.session["oauth_provider"] = "google"
        
        return RedirectResponse("/", status_code=303)
        
    except Exception as e:
        logger.error(f"❌ Google OAuth error: {e}")
        add_flash(request, "Google login failed. Please try again.", "danger")
        return RedirectResponse("/login", status_code=303)


# ==================== SECURE PASSWORD RESET (OTP-based) ====================

@router.get("/forgot_password")
async def forgot_password_page(request: Request):
    """Display forgot password form"""
    if not PASSWORD_RESET_AVAILABLE:
        raise HTTPException(status_code=503, detail="Password reset service not available")
    from fastapi_app_cleaned import templates
    return templates.TemplateResponse(request=request, name="forgot_password.html")


@router.get("/forgot_password/verify")
async def forgot_password_verify_page(request: Request):
    """Display OTP verification form"""
    if not PASSWORD_RESET_AVAILABLE:
        raise HTTPException(status_code=503, detail="Password reset service not available")
    from fastapi_app_cleaned import templates
    return templates.TemplateResponse(request=request, name="forgot_password_verify.html")


@router.post("/forgot_password/request_otp")
async def request_password_reset_otp(
    request: Request,
    email: str = Form(...),
    background: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Request OTP for password reset with rate limiting and security measures.
    """
    if not PASSWORD_RESET_AVAILABLE:
        raise HTTPException(status_code=503, detail="Password reset service not available")
    from fastapi_app_cleaned import User
    
    email = email.strip().lower()
    
    # Rate limiting - 100 requests per 5 minutes per IP (essentially unlimited for dev)
    is_limited, retry_after = rate_limiter.check_rate_limit(
        request, 
        max_requests=100, 
        window_seconds=300,
        endpoint="password_reset"
    )
    
    if is_limited:
        add_flash(
            request, 
            f"Too many password reset requests. Please try again in {retry_after // 60} minutes.", 
            "danger"
        )
        return RedirectResponse("/forgot_password", status_code=303)
    
    # Check cooldown (60 seconds between requests for same email)
    is_in_cooldown, remaining = password_reset_storage.check_cooldown(email, cooldown_seconds=60)
    if is_in_cooldown:
        add_flash(
            request,
            f"Please wait {remaining} seconds before requesting another code.",
            "warning"
        )
        return RedirectResponse("/forgot_password", status_code=303)
    
    # Check if user exists (but don't reveal this for security)
    user = db.query(User).filter_by(email=email).first()
    
    # Generate OTP (8 digits for better security)
    otp = password_reset_storage.create_otp(email, expiry_minutes=10)
    
    # Set cooldown
    password_reset_storage.set_cooldown(email, cooldown_seconds=60)
    
    # Send email (only if user exists, but don't reveal this)
    if user:
        if background:
            background.add_task(send_password_reset_email, email, otp, 10)
        else:
            send_password_reset_email(email, otp, 10)
        
        logger.info(f"🔐 Password reset OTP sent to {email}")
    else:
        logger.info(f"🔐 Password reset requested for non-existent email: {email}")
    
    # Always return success (security best practice - don't reveal if email exists)
    add_flash(request, "If an account exists, a verification code has been sent to your email.", "info")
    return RedirectResponse("/forgot_password/verify", status_code=303)


@router.post("/forgot_password/verify_otp")
async def verify_otp_and_reset(
    request: Request,
    email: str = Form(...),
    otp: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Verify OTP and reset password with enhanced security validation.
    """
    if not PASSWORD_RESET_AVAILABLE:
        raise HTTPException(status_code=503, detail="Password reset service not available")
    from fastapi_app_cleaned import User, get_password_hash, PasswordValidator
    
    email = email.strip().lower()
    otp = otp.strip()
    
    # Rate limiting for verification attempts
    is_limited, retry_after = rate_limiter.check_rate_limit(
        request,
        max_requests=10,
        window_seconds=300,
        endpoint="otp_verification"
    )
    
    if is_limited:
        add_flash(
            request,
            f"Too many verification attempts. Please try again in {retry_after // 60} minutes.",
            "danger"
        )
        return RedirectResponse("/forgot_password", status_code=303)
    
    # Verify OTP
    is_valid, error_msg = password_reset_storage.verify_otp(email, otp, max_attempts=3)
    
    if not is_valid:
        add_flash(request, error_msg, "danger")
        return RedirectResponse("/forgot_password/verify", status_code=303)
    
    # Validate password confirmation
    if new_password != confirm_password:
        add_flash(request, "Passwords do not match", "danger")
        return RedirectResponse("/forgot_password/verify", status_code=303)
    
    # Validate password strength
    is_strong, strength_error = PasswordValidator.validate_password_strength(new_password)
    if not is_strong:
        add_flash(request, strength_error, "danger")
        return RedirectResponse("/forgot_password/verify", status_code=303)
    
    # OTP is valid - reset password
    user = db.query(User).filter_by(email=email).first()
    
    if not user:
        # This shouldn't happen if OTP was valid, but handle gracefully
        add_flash(request, "Account not found.", "danger")
        return RedirectResponse("/login", status_code=303)
    
    # Update password
    user.password = get_password_hash(new_password)
    user.password_changed_at = datetime.utcnow()  # Track password changes
    db.add(user)
    db.commit()
    
    logger.info(f"✅ Password reset successful for {email}")
    
    add_flash(request, "Password reset successful! Please login with your new password.", "success")
    return RedirectResponse("/login", status_code=303)

