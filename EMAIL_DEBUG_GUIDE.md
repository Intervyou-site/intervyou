# Email OTP Debugging Guide

## 🐛 Issue: OTP Showing in Logs But Not Sent to Email

### Current Status:
- ✅ Email variables are set in Railway
- ✅ OTP is being generated
- ❌ Email is NOT being sent via SMTP
- ❌ OTP only appears in logs

---

## 🔍 Diagnosis Steps

### Step 1: Check Railway Logs for Email Service Status

Look for these log messages when app starts:

**If Email is Configured Correctly:**
```
✅ Email service configured - SMTP: smtp.gmail.com:587
✅ Sending from: nayeemabisharan@gmail.com
```

**If Email is NOT Configured:**
```
⚠️  Email service not configured - missing MAIL_USERNAME or MAIL_PASSWORD
⚠️  MAIL_USERNAME present: False
⚠️  MAIL_PASSWORD present: False
```

### Step 2: Check Railway Logs When Requesting OTP

Look for these messages when you request password reset:

**If Email Sending is Attempted:**
```
📧 Email service configured: True
📧 MAIL_USERNAME: True
📧 MAIL_PASSWORD: True
📧 Attempting to send email via SMTP...
📧 Attempting to send email to nayeemabisharan@gmail.com
📧 SMTP: smtp.gmail.com:587
📧 Connecting to SMTP server...
📧 Starting TLS...
📧 Logging in as nayeemabisharan@gmail.com...
📧 Sending message...
✅ Email sent successfully to nayeemabisharan@gmail.com
```

**If Email Sending Fails:**
```
❌ SMTP Authentication failed: (535, b'5.7.8 Username and Password not accepted')
❌ Check MAIL_USERNAME and MAIL_PASSWORD in Railway
```

---

## 🔧 Solutions

### Solution 1: Verify Railway Environment Variables

1. Go to Railway Dashboard → Your Service → Variables
2. Verify these EXACT variable names (case-sensitive):

```
MAIL_USERNAME=nayeemabisharan@gmail.com
MAIL_PASSWORD=msuk zwrm magy sbfd
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
MAIL_FROM=nayeemabisharan@gmail.com
MAIL_FROM_NAME=IntervYou Support
```

**Common Mistakes:**
- ❌ `EMAIL_USERNAME` (wrong - should be `MAIL_USERNAME`)
- ❌ `MAIL_USER` (wrong - should be `MAIL_USERNAME`)
- ❌ Extra spaces in values
- ❌ Wrong password (not Gmail App Password)

### Solution 2: Generate New Gmail App Password

The current password might be expired or revoked.

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in with `nayeemabisharan@gmail.com`
3. Click **"Select app"** → Choose **"Mail"**
4. Click **"Select device"** → Choose **"Other (Custom name)"**
5. Enter: **"IntervYou Railway Production"**
6. Click **"Generate"**
7. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)
8. **Remove all spaces**: `abcdefghijklmnop`
9. Update `MAIL_PASSWORD` in Railway with this new password
10. Wait for Railway to redeploy (2-3 minutes)

### Solution 3: Check Gmail Account Settings

1. Go to: https://myaccount.google.com/security
2. Verify **"2-Step Verification"** is **ON**
3. If OFF, enable it first
4. Then generate App Password (Solution 2)

### Solution 4: Test with Different Email

Try using a different Gmail account:

1. Create new Gmail account or use another one
2. Enable 2FA on that account
3. Generate App Password
4. Update Railway variables:
   ```
   MAIL_USERNAME=new-email@gmail.com
   MAIL_PASSWORD=new-app-password
   MAIL_FROM=new-email@gmail.com
   ```
5. Test password reset

### Solution 5: Check for Gmail Security Blocks

1. Go to: https://myaccount.google.com/notifications
2. Check for any security alerts
3. If you see "Blocked sign-in attempt", click "Yes, it was me"
4. Try sending email again

### Solution 6: Force Redeploy Railway

Sometimes variables don't load properly:

1. Go to Railway Dashboard
2. Click on your service
3. Click **"Settings"** tab
4. Scroll down to **"Danger Zone"**
5. Click **"Redeploy"**
6. Wait for deployment to complete
7. Test again

---

## 🧪 Manual Email Test

Create a test script to verify email works:

```python
# test_email.py
import os
from dotenv import load_dotenv
load_dotenv()

from email_service import email_service

print(f"Email configured: {email_service.is_configured}")
print(f"SMTP Host: {email_service.smtp_host}")
print(f"SMTP Port: {email_service.smtp_port}")
print(f"Mail Username: {email_service.mail_username}")
print(f"Mail Password: {'*' * len(email_service.mail_password) if email_service.mail_password else 'NOT SET'}")

# Try sending test email
if email_service.is_configured:
    success = email_service.send_password_reset_otp(
        "nayeemabisharan@gmail.com",
        "123456",
        10
    )
    print(f"Email sent: {success}")
else:
    print("Email service not configured!")
```

Run locally:
```bash
python test_email.py
```

---

## 📊 Expected vs Actual Behavior

### Expected (Working):
1. User requests password reset
2. OTP generated
3. Email service sends email via SMTP
4. User receives email in inbox
5. User enters OTP and resets password

### Actual (Current):
1. User requests password reset
2. OTP generated
3. Email service **NOT sending** (falling back to logs)
4. OTP only appears in Railway logs
5. User must check logs to get OTP

---

## 🎯 Root Cause Analysis

Based on the symptoms, the most likely causes are:

1. **Environment variables not loading** (60% probability)
   - Variables set in Railway but not loaded by app
   - Solution: Force redeploy

2. **Gmail App Password expired/wrong** (30% probability)
   - Password was revoked or changed
   - Solution: Generate new App Password

3. **Gmail security block** (5% probability)
   - Gmail blocking sign-in from Railway servers
   - Solution: Allow less secure apps or check security alerts

4. **SMTP port blocked** (5% probability)
   - Railway blocking port 587
   - Solution: Try port 465 with SSL

---

## 🚀 Quick Fix Checklist

Try these in order:

- [ ] Step 1: Verify variable names are EXACT (MAIL_USERNAME not EMAIL_USERNAME)
- [ ] Step 2: Generate NEW Gmail App Password
- [ ] Step 3: Update MAIL_PASSWORD in Railway
- [ ] Step 4: Force redeploy Railway service
- [ ] Step 5: Wait 3 minutes for deployment
- [ ] Step 6: Check Railway logs for "✅ Email service configured"
- [ ] Step 7: Test password reset
- [ ] Step 8: Check email inbox (and spam folder)

---

## 📞 If Still Not Working

Provide these details:

1. **Railway startup logs** (first 50 lines after deployment)
2. **Railway logs when requesting OTP** (look for 📧 emoji)
3. **Screenshot of Railway Variables tab**
4. **Confirmation that 2FA is enabled on Gmail**
5. **Confirmation that App Password was generated (not regular password)**

---

## ✅ Success Indicators

When email is working, you'll see:

```
✅ Email service configured - SMTP: smtp.gmail.com:587
✅ Sending from: nayeemabisharan@gmail.com
📧 Attempting to send email to nayeemabisharan@gmail.com
📧 Connecting to SMTP server...
📧 Starting TLS...
📧 Logging in as nayeemabisharan@gmail.com...
📧 Sending message...
✅ Email sent successfully to nayeemabisharan@gmail.com
✅ Password reset OTP email sent to nayeemabisharan@gmail.com
```

And user receives email in inbox! 📧

---

## 🔄 Alternative: Use Different Email Service

If Gmail continues to fail, consider:

1. **SendGrid** (Free tier: 100 emails/day)
2. **Mailgun** (Free tier: 5,000 emails/month)
3. **AWS SES** (Free tier: 62,000 emails/month)
4. **Resend** (Free tier: 3,000 emails/month)

These are more reliable for production use than Gmail SMTP.
