# Resend Email Service Setup Guide

## 🎯 Why Resend?

**Railway blocks SMTP ports (465 and 587)**, so we can't use Gmail SMTP directly.

**Resend uses HTTPS API** instead of SMTP, which works perfectly on Railway!

---

## ✅ Benefits of Resend

- ✅ **Free tier**: 3,000 emails/month
- ✅ **No credit card required**
- ✅ **Works on Railway** (uses HTTPS, not SMTP)
- ✅ **5 minutes to set up**
- ✅ **Simple API**
- ✅ **Reliable delivery**

---

## 🚀 Setup Steps (5 minutes)

### Step 1: Create Resend Account

1. Go to: https://resend.com/signup
2. Sign up with your email
3. Verify your email address
4. Login to Resend dashboard

### Step 2: Get API Key

1. In Resend dashboard, click **"API Keys"** in sidebar
2. Click **"Create API Key"**
3. Name: `IntervYou Railway Production`
4. Permission: **"Sending access"**
5. Click **"Add"**
6. **Copy the API key** (starts with `re_`)
   - Example: `re_123abc456def789ghi`
   - ⚠️ **Save it now** - you won't see it again!

### Step 3: Add Domain (Optional but Recommended)

**Option A: Use Resend's Test Domain** (Quick Start)
- From: `onboarding@resend.dev`
- ✅ Works immediately
- ⚠️ Limited to 100 emails/day
- ⚠️ May go to spam

**Option B: Use Your Own Domain** (Recommended for Production)
1. In Resend dashboard, click **"Domains"**
2. Click **"Add Domain"**
3. Enter your domain (e.g., `intervyou.com`)
4. Add DNS records (Resend will show you what to add)
5. Wait for verification (usually 5-10 minutes)
6. From: `noreply@intervyou.com` or `support@intervyou.com`

### Step 4: Add to Railway Environment Variables

1. Go to Railway Dashboard: https://railway.app/dashboard
2. Click on your project → Click on your service
3. Click **"Variables"** tab
4. Add these variables:

```
RESEND_API_KEY=re_your_api_key_here
RESEND_FROM_EMAIL=onboarding@resend.dev
```

**If using your own domain**:
```
RESEND_API_KEY=re_your_api_key_here
RESEND_FROM_EMAIL=noreply@intervyou.com
```

5. Click **"Add"** for each variable
6. Railway will automatically redeploy

### Step 5: Wait for Deployment (2-3 minutes)

Watch Railway dashboard until status shows "Online"

### Step 6: Test Email

1. Go to: https://intervyou-production-5a2d.up.railway.app/forgot_password
2. Enter: `nayeemabisharan@gmail.com`
3. Click "Send Verification Code"
4. **CHECK YOUR EMAIL INBOX** 📧

**Expected in Railway Logs**:
```
✅ Resend email service imported successfully
📧 Using Resend email service
📧 Attempting to send email via Resend...
✅ Email sent successfully via Resend to nayeemabisharan@gmail.com
✅ Resend email ID: abc123...
```

**Expected in Your Inbox**:
- Email from "IntervYou Support"
- Subject: "IntervYou - Password Reset Code"
- 6-digit OTP code
- Beautiful HTML design

---

## 📋 Environment Variables Summary

### Required:
```
RESEND_API_KEY=re_your_api_key_here
```

### Optional (with defaults):
```
RESEND_FROM_EMAIL=onboarding@resend.dev
MAIL_FROM_NAME=IntervYou Support
```

---

## 🧪 Testing Checklist

After Railway deploys:

- [ ] Railway deployment status: "Online"
- [ ] Railway logs show: "✅ Resend email service imported successfully"
- [ ] Railway logs show: "📧 Using Resend email service"
- [ ] Test password reset at /forgot_password
- [ ] Railway logs show: "✅ Email sent successfully via Resend"
- [ ] Email received in inbox (check spam if not in inbox)
- [ ] OTP code visible in email
- [ ] OTP works when entered
- [ ] Password reset successful

---

## 🐛 Troubleshooting

### "Resend not configured - missing RESEND_API_KEY"

**Solution**: Add RESEND_API_KEY to Railway variables
1. Go to Railway → Variables
2. Add: `RESEND_API_KEY=re_your_key`
3. Redeploy

### "Resend API error: 401"

**Solution**: Invalid API key
1. Generate new API key in Resend dashboard
2. Update RESEND_API_KEY in Railway
3. Redeploy

### "Resend API error: 403"

**Solution**: API key doesn't have sending permission
1. Create new API key with "Sending access"
2. Update RESEND_API_KEY in Railway
3. Redeploy

### Email goes to spam

**Solution**: Use your own verified domain
1. Add domain in Resend dashboard
2. Add DNS records
3. Wait for verification
4. Update RESEND_FROM_EMAIL to use your domain

### Email not received

**Check 1**: Spam folder
**Check 2**: Railway logs for Resend errors
**Check 3**: Resend dashboard → Logs (shows all sent emails)

---

## 📊 Resend Free Tier Limits

- **3,000 emails/month** (plenty for most apps)
- **100 emails/day** with test domain
- **Unlimited** with verified domain
- **No credit card required**

---

## 🔄 Fallback Behavior

The app is smart:
1. **On Railway**: Uses Resend API (HTTPS)
2. **On Localhost**: Uses Gmail SMTP (works locally)
3. **If both fail**: Shows OTP in logs (fallback)

---

## ✅ Success Indicators

When Resend is working:

**Railway Logs**:
```
✅ Resend email service imported successfully
📧 Using Resend email service
📧 Email service configured: True
✅ Email sent successfully via Resend
✅ Resend email ID: abc123...
```

**Your Inbox**:
```
📧 Email from IntervYou Support
📧 Subject: IntervYou - Password Reset Code
📧 6-digit OTP code
```

**Password Reset**:
```
✅ OTP accepted
✅ Password reset successful
```

---

## 🎉 Why This Works

**Problem**: Railway blocks SMTP ports (465, 587)
**Solution**: Resend uses HTTPS API (port 443)
**Result**: Email works on Railway! 📧

---

## 📞 Support

If you need help:
1. Check Resend dashboard → Logs
2. Check Railway logs for errors
3. Verify API key is correct
4. Verify from email is correct

---

## 🔗 Useful Links

- **Resend Dashboard**: https://resend.com/dashboard
- **Resend Docs**: https://resend.com/docs
- **Resend API Keys**: https://resend.com/api-keys
- **Resend Domains**: https://resend.com/domains

---

**Setup time**: 5 minutes
**Cost**: Free (3,000 emails/month)
**Reliability**: ✅ Works on Railway!
