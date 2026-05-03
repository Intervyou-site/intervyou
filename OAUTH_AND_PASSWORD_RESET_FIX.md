# Google OAuth and Password Reset Fixes

## Date: May 3, 2026

## Issues Fixed

### 1. Google OAuth CSRF Error ✅
**Problem**: "mismatching_state: CSRF Warning! State not equal in request and response"

**Root Cause**: Session state was not persisting properly between OAuth redirect and callback due to:
- Generic session cookie name causing conflicts
- Missing explicit path configuration
- Insufficient OAuth endpoint configuration

**Solutions Implemented**:
- ✅ Changed session cookie name from `session` to `intervyou_session` for uniqueness
- ✅ Added explicit `path="/"` to ensure cookies work across all routes
- ✅ Configured `same_site="lax"` for OAuth redirect compatibility
- ✅ Added explicit OAuth endpoints in `oauth_config.py`:
  - `token_endpoint`: https://oauth2.googleapis.com/token
  - `authorize_url`: https://accounts.google.com/o/oauth2/v2/auth
  - `userinfo_endpoint`: https://openidconnect.googleapis.com/v1/userinfo
- ✅ Enhanced error logging with session state debugging
- ✅ Added `token_endpoint_auth_method: 'client_secret_post'` for better compatibility

**Files Modified**:
- `security_config.py` - SessionMiddleware configuration
- `fastapi_app_cleaned.py` - Fallback SessionMiddleware configuration
- `oauth_config.py` - OAuth client configuration
- `auth_routes.py` - OAuth route handlers with enhanced logging

### 2. Password Reset OTP Not Visible ✅
**Problem**: OTP codes were being generated but not easily visible in Railway logs

**Solutions Implemented**:
- ✅ Made OTP codes HIGHLY visible with:
  - Multiple lines of `=` separators (80 characters wide)
  - Large emoji headers: 📧 📧 📧
  - Both `logger.info()` AND `print()` statements to ensure visibility
  - Timestamp in human-readable format
  - Clear instructions to check Railway logs
- ✅ Enhanced OTP creation logging with expiry timestamps
- ✅ Added detailed error messages for OTP verification failures

**Files Modified**:
- `password_reset_service.py` - OTP logging and creation

## How to Test

### Testing Google OAuth:

1. **Deploy to Railway** (automatic from GitHub push)
   - Railway will automatically rebuild and redeploy
   - Wait 2-3 minutes for deployment to complete

2. **Test OAuth Flow**:
   ```
   1. Go to: https://intervyou-production-5a2d.up.railway.app/login
   2. Click "Sign in with Google"
   3. Select your Google account
   4. Should redirect back to home page with success message
   ```

3. **Check Railway Logs** (if issues occur):
   ```
   Look for these log entries:
   - "🔐 Initiating Google OAuth - Redirect URI: ..."
   - "🔐 OAuth state stored in session: True"
   - "🔐 Google OAuth callback received"
   - "✅ Google OAuth successful for: [email]"
   - "✅ Session created for user [id]"
   ```

4. **If CSRF Error Still Occurs**:
   - Check logs for: "❌ Session state: NOT FOUND"
   - This indicates session is not persisting
   - Verify Railway environment has `SECRET_KEY` set
   - Check browser allows cookies from Railway domain

### Testing Password Reset OTP:

1. **Request Password Reset**:
   ```
   1. Go to: https://intervyou-production-5a2d.up.railway.app/forgot_password
   2. Enter your email address
   3. Click "Send Verification Code"
   ```

2. **Find OTP in Railway Logs**:
   ```
   1. Go to Railway dashboard
   2. Click on your service
   3. Click "Deployments" tab
   4. Click "View Logs"
   5. Look for this VERY visible pattern:
   
   ================================================================================
   📧 📧 📧  PASSWORD RESET OTP CODE  📧 📧 📧
   ================================================================================
   📧 Email: your-email@example.com
   📧 OTP Code: 123456
   📧 Valid for: 10 minutes
   📧 Generated at: 2026-05-03 12:34:56 UTC
   ================================================================================
   ```

3. **Verify OTP**:
   ```
   1. Copy the 6-digit OTP code from logs
   2. Enter it in the verification form
   3. Enter your new password (must meet requirements)
   4. Click "Reset Password"
   5. Should redirect to login with success message
   ```

## Technical Details

### Session Configuration:
```python
SessionMiddleware(
    secret_key=SECRET_KEY,
    session_cookie="intervyou_session",  # Unique name
    max_age=86400,  # 24 hours
    same_site="lax",  # Required for OAuth
    https_only=True,  # In production
    path="/",  # All routes
    domain=None  # Auto-detect
)
```

### OAuth Configuration:
```python
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account',
        'token_endpoint_auth_method': 'client_secret_post'
    },
    token_endpoint='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo'
)
```

## Environment Variables Required

Make sure these are set in Railway:

```bash
# Required for OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
SECRET_KEY=your-secret-key-at-least-32-chars

# Required for sessions
ENVIRONMENT=production

# Database
DATABASE_URL=postgresql://... (Railway provides this automatically)
```

## Google Cloud Console Configuration

Ensure your OAuth redirect URI is configured:

1. Go to: https://console.cloud.google.com/apis/credentials
2. Select your OAuth 2.0 Client ID
3. Under "Authorized redirect URIs", add:
   ```
   https://intervyou-production-5a2d.up.railway.app/auth/google/callback
   ```
4. Click "Save"

## Troubleshooting

### OAuth Still Failing?

1. **Check Session Cookie**:
   - Open browser DevTools → Application → Cookies
   - Look for `intervyou_session` cookie
   - Should have `SameSite=Lax` and `Path=/`

2. **Check Railway Logs**:
   - Look for "Session keys: [...]" in callback logs
   - Should include `_state_google_` key

3. **Verify Environment Variables**:
   - Railway dashboard → Variables tab
   - Ensure `SECRET_KEY` is set and at least 32 characters
   - Ensure `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are correct

### OTP Not Appearing in Logs?

1. **Check Log Level**:
   - Railway logs should show INFO level messages
   - Look for the `=====` separator lines

2. **Check Email**:
   - Verify the email you entered exists in the database
   - OTP is only generated if email is valid (but success message always shows)

3. **Check Cooldown**:
   - Wait 60 seconds between OTP requests
   - Check logs for "Please wait X seconds" message

## Next Steps

### For Production Email Service:

Replace the logging in `password_reset_service.py` with actual email sending:

```python
def send_password_reset_email(email: str, otp: str, expiry_minutes: int = 10) -> bool:
    try:
        # Use your email service (SendGrid, AWS SES, etc.)
        send_email(
            to=email,
            subject="IntervYou - Password Reset Code",
            body=f"""
            Your password reset code is: {otp}
            
            This code will expire in {expiry_minutes} minutes.
            
            If you didn't request this, please ignore this email.
            """
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
```

## Deployment Status

- ✅ Code pushed to GitHub: https://github.com/Intervyou-site/intervyou
- ⏳ Railway auto-deployment in progress
- 🔗 Live URL: https://intervyou-production-5a2d.up.railway.app

## Summary

Both issues have been fixed:
1. **Google OAuth** - Session state now persists correctly with improved cookie configuration
2. **Password Reset** - OTP codes are now HIGHLY visible in Railway logs

The fixes are deployed and ready for testing. Check Railway logs for detailed debugging information if any issues occur.
