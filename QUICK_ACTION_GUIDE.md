# Quick Action Guide - Fix Email OTP & Create Admin

## 🚨 IMMEDIATE ACTIONS NEEDED

### Action 1: Fix Email OTP (5 minutes)

#### Step 1: Verify Railway Environment Variables

1. Go to: https://railway.app/dashboard
2. Click your project → Click your service
3. Click **"Variables"** tab
4. **VERIFY these variables exist**:

```
MAIL_USERNAME = nayeemabisharan@gmail.com
MAIL_PASSWORD = msuk zwrm magy sbfd
SMTP_HOST = smtp.gmail.com
SMTP_PORT = 587
MAIL_FROM = nayeemabisharan@gmail.com
```

#### Step 2: If Variables Are Missing - Add Them

Click **"+ New Variable"** and add each one:

| Variable Name | Value |
|--------------|-------|
| `MAIL_USERNAME` | `nayeemabisharan@gmail.com` |
| `MAIL_PASSWORD` | `msuk zwrm magy sbfd` |
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `MAIL_FROM` | `nayeemabisharan@gmail.com` |
| `MAIL_FROM_NAME` | `IntervYou Support` |

#### Step 3: Wait for Redeploy

- Railway will automatically redeploy (2-3 minutes)
- Watch the deployment progress

#### Step 4: Check Logs

1. Click **"Deployments"** tab
2. Click **"View Logs"**
3. Look for:
   ```
   ✅ Email service configured - SMTP: smtp.gmail.com:587
   ✅ Sending from: nayeemabisharan@gmail.com
   ```

#### Step 5: Test Email

1. Go to: https://intervyou-production-5a2d.up.railway.app/forgot_password
2. Enter: `nayeemabisharan@gmail.com`
3. Click "Send Verification Code"
4. **CHECK YOUR EMAIL INBOX** 📧
5. Should receive email with OTP code

---

### Action 2: Create Admin User (2 minutes)

#### Method A: Using Python Script (Recommended)

1. Open terminal in your project folder
2. Run:
   ```bash
   python create_admin.py
   ```
3. Follow prompts:
   ```
   Name: Admin
   Email: admin@intervyou.com
   Password: Admin@IntervYou2026!
   Confirm Password: Admin@IntervYou2026!
   ```
4. Done! ✅

#### Method B: Update Your Existing Account to Admin

1. Open terminal
2. Run:
   ```bash
   python create_admin.py
   ```
3. When asked for email, enter: `nayeemabisharan@gmail.com`
4. Script will ask: "Do you want to update this user to admin?"
5. Type: `yes`
6. Done! ✅

#### Method C: Direct SQL (Railway Dashboard)

1. Go to Railway Dashboard
2. Click on PostgreSQL database
3. Click **"Query"** tab
4. Run this SQL:
   ```sql
   UPDATE "user"
   SET role = 'admin', email_verified = 1
   WHERE email = 'nayeemabisharan@gmail.com';
   ```
5. Click **"Run Query"**
6. Done! ✅

---

## 🧪 Testing

### Test 1: Email OTP

1. Go to: https://intervyou-production-5a2d.up.railway.app/forgot_password
2. Enter your email
3. Click "Send Verification Code"
4. **Check email inbox** (not spam)
5. Should receive beautiful HTML email with 6-digit OTP
6. Enter OTP and reset password
7. ✅ Success!

### Test 2: Admin Access

1. Go to: https://intervyou-production-5a2d.up.railway.app/login
2. Login with admin credentials
3. Go to: https://intervyou-production-5a2d.up.railway.app/admin
4. Should see admin dashboard with:
   - Total users
   - User list
   - System statistics
5. ✅ Success!

---

## 🔍 Troubleshooting

### Email Not Working?

**Check 1**: Railway logs show:
```
⚠️  Email service not configured - missing MAIL_USERNAME or MAIL_PASSWORD
```
→ **Solution**: Add variables in Railway (see Action 1)

**Check 2**: Railway logs show:
```
❌ SMTP Authentication failed
```
→ **Solution**: Gmail App Password might be wrong. Generate new one:
1. Go to: https://myaccount.google.com/apppasswords
2. Create new app password
3. Update `MAIL_PASSWORD` in Railway
4. Wait for redeploy

**Check 3**: Email not in inbox
→ **Solution**: Check spam folder

### Admin Not Working?

**Check 1**: Cannot access `/admin`
→ **Solution**: Run `create_admin.py` again or use SQL method

**Check 2**: "Admin access required" error
→ **Solution**: Verify role in database:
```sql
SELECT email, role FROM "user" WHERE email = 'your-email@example.com';
```
Should show `role = 'admin'`

---

## 📋 Checklist

### Email OTP Setup:
- [ ] Verified MAIL_USERNAME in Railway
- [ ] Verified MAIL_PASSWORD in Railway
- [ ] Verified SMTP_HOST in Railway
- [ ] Verified SMTP_PORT in Railway
- [ ] Waited for Railway redeploy
- [ ] Checked logs for "✅ Email service configured"
- [ ] Tested password reset
- [ ] Received email with OTP
- [ ] Successfully reset password

### Admin Setup:
- [ ] Ran `create_admin.py` OR used SQL method
- [ ] Verified admin user created
- [ ] Logged in with admin credentials
- [ ] Accessed `/admin` dashboard
- [ ] Can see all users
- [ ] Can see system statistics

---

## ✅ Success Indicators

### Email Working:
- ✅ Railway logs show: "✅ Email service configured"
- ✅ Railway logs show: "✅ Email sent successfully to [email]"
- ✅ Email received in inbox
- ✅ OTP code visible in email
- ✅ OTP works when entered
- ✅ Password reset successful

### Admin Working:
- ✅ Can login with admin credentials
- ✅ Can access `/admin` route
- ✅ Can see admin dashboard
- ✅ Can see all users
- ✅ Can perform admin actions

---

## 📞 Current Status

### ✅ Working:
- Google OAuth login
- Home page
- Login/Register pages
- Database connection
- All static pages

### 🔄 Needs Setup:
- Email OTP (needs Railway variables)
- Admin user (needs creation)

---

## 🎯 Next Steps

1. **Fix Email** (5 min):
   - Add variables to Railway
   - Wait for redeploy
   - Test password reset

2. **Create Admin** (2 min):
   - Run `create_admin.py`
   - OR use SQL method
   - Test admin access

3. **Verify Everything Works**:
   - Test all features
   - Check Railway logs
   - Confirm no errors

---

## 📚 Detailed Guides

- **Email Setup**: See `RAILWAY_ENVIRONMENT_SETUP.md`
- **Admin Setup**: See `ADMIN_SETUP_GUIDE.md`
- **Google OAuth**: See `GOOGLE_OAUTH_SETUP_VERIFICATION.md`

---

**Deployment Status**: ✅ Code deployed to Railway  
**Live URL**: https://intervyou-production-5a2d.up.railway.app  
**Time to Complete**: ~7 minutes total
