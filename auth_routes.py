# auth_routes.py
"""
OAuth Social Login Routes and Forgot Password Implementation
"""

from fastapi import APIRouter, Request, Depends, Form, BackgroundTasks, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import os

# Import from main app
from oauth_config import oauth
from email_service import send_otp_email

router = APIRouter()

# Helper to get DB session (will be injected from main app)
def get_db():
    from fastapi_app import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db):
    from fastapi_app import User
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
    """Handle Google OAuth callback"""
    from fastapi_app import User, get_password_hash
    
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            add_flash(request, "Failed to get user info from Google", "danger")
            return RedirectResponse("/login", status_code=303)
        
        email = user_info.get('email')
        name = user_info.get('name') or email.split('@')[0]
        
        # Check if user exists
        user = db.query(User).filter_by(email=email).first()
        
        if not user:
            # Create new user with OAuth
            # Use a shorter random password (bcrypt has 72 byte limit)
            random_password = os.urandom(16).hex()[:50]  # Max 50 chars to be safe
            user = User(
                name=name,
                email=email,
                password=get_password_hash(random_password)
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            add_flash(request, f"Welcome {name}! Account created via Google.", "success")
        else:
            add_flash(request, f"Welcome back {name}!", "success")
        
        # Log user in
        request.session["user_id"] = user.id
        request.session["oauth_provider"] = "google"
        
        return RedirectResponse("/", status_code=303)
        
    except Exception as e:
        print(f"Google OAuth error: {e}")
        add_flash(request, "Google login failed. Please try again.", "danger")
        return RedirectResponse("/login", status_code=303)


# ==================== FORGOT PASSWORD (OTP-based) ====================

# In-memory OTP storage (for development - use Redis in production)
otp_storage = {}

def generate_otp(length=6):
    """Generate numeric OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


@router.get("/forgot_password")
async def forgot_password_page(request: Request):
    """Display forgot password form"""
    from fastapi_app import templates
    return templates.TemplateResponse("forgot_password.html", {"request": request})


@router.get("/forgot_password/verify")
async def forgot_password_verify_page(request: Request):
    """Display OTP verification form"""
    from fastapi_app import templates
    return templates.TemplateResponse("forgot_password_verify.html", {"request": request})


@router.post("/forgot_password/request_otp")
async def request_password_reset_otp(
    request: Request,
    email: str = Form(...),
    background: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Request OTP for password reset"""
    from fastapi_app import User
    
    email = email.strip().lower()
    
    # Check if user exists (but don't reveal this for security)
    user = db.query(User).filter_by(email=email).first()
    
    # Generate OTP
    otp = generate_otp(6)
    expiry = datetime.utcnow() + timedelta(minutes=10)
    
    # Store OTP (in production, use Redis with TTL)
    otp_storage[email] = {
        'otp': otp,
        'expiry': expiry,
        'attempts': 0
    }
    
    # Send email (only if user exists, but don't reveal this)
    if user:
        if background:
            background.add_task(send_otp_email, email, otp, 10)
        else:
            send_otp_email(email, otp, 10)
    
    # Always return success (security best practice)
    add_flash(request, "If an account exists, an OTP has been sent to your email.", "info")
    return RedirectResponse("/forgot_password/verify", status_code=303)


@router.post("/forgot_password/verify_otp")
async def verify_otp_and_reset(
    request: Request,
    email: str = Form(...),
    otp: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Verify OTP and reset password"""
    from fastapi_app import User, get_password_hash
    
    email = email.strip().lower()
    otp = otp.strip()
    
    # Check OTP
    stored = otp_storage.get(email)
    
    if not stored:
        add_flash(request, "No OTP request found. Please request a new one.", "danger")
        return RedirectResponse("/forgot_password", status_code=303)
    
    # Check expiry
    if datetime.utcnow() > stored['expiry']:
        del otp_storage[email]
        add_flash(request, "OTP expired. Please request a new one.", "danger")
        return RedirectResponse("/forgot_password", status_code=303)
    
    # Check attempts
    if stored['attempts'] >= 3:
        del otp_storage[email]
        add_flash(request, "Too many attempts. Please request a new OTP.", "danger")
        return RedirectResponse("/forgot_password", status_code=303)
    
    # Verify OTP
    if stored['otp'] != otp:
        stored['attempts'] += 1
        add_flash(request, f"Invalid OTP. {3 - stored['attempts']} attempts remaining.", "danger")
        return RedirectResponse("/forgot_password/verify", status_code=303)
    
    # OTP is valid - reset password
    user = db.query(User).filter_by(email=email).first()
    
    if not user:
        add_flash(request, "Account not found.", "danger")
        return RedirectResponse("/login", status_code=303)
    
    # Update password
    user.password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    
    # Clear OTP
    del otp_storage[email]
    
    add_flash(request, "Password reset successful! Please login with your new password.", "success")
    return RedirectResponse("/login", status_code=303)
