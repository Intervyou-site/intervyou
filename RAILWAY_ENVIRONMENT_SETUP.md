# Railway Environment Variables Setup Guide

## 🚀 Critical: Set These Variables in Railway

### Step 1: Access Railway Variables

1. Go to: https://railway.app/dashboard
2. Click on your project
3. Click on your service (intervyou)
4. Click **"Variables"** tab
5. Click **"+ New Variable"** for each variable below

---

## 📋 Required Environment Variables

### 1. Security & Session

```bash
SECRET_KEY=8GSoa5jZBNgP_zZbczd685Xs473CD0kP86BTS2XiGKA
ENVIRONMENT=production
```

### 2. Google OAuth

```bash
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

**⚠️ Use your actual Google OAuth credentials from Google Cloud Console**

### 3. Email Configuration (CRITICAL FOR OTP)

```bash
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_FROM=your-email@gmail.com
MAIL_FROM_NAME=IntervYou Support
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

**⚠️ IMPORTANT**: The `MAIL_PASSWORD` is your Gmail App Password (not your regular Gmail password)

### 4. OpenAI API (Optional but Recommended)

```bash
OPENAI_API_KEY=your-openai-api-key
```

### 5. SerpAPI (Optional)

```bash
SERPAPI_KEY=your-serpapi-key
```

### 6. Database (Automatically Set by Railway)

Railway automatically provides:
```bash
DATABASE_URL=postgresql://...
```

**Do NOT manually set this** - Railway manages it automatically.

---

## 🔧 How to Add Variables in Railway

### Method 1: One by One (Recommended)

1. Click **"+ New Variable"**
2. Enter variable name (e.g., `MAIL_USERNAME`)
3. Enter variable value (e.g., `nayeemabisharan@gmail.com`)
4. Click **"Add"**
5. Repeat for each variable

### Method 2: Bulk Import (Faster)

1. Click **"RAW Editor"** button
2. Paste all variables at once (replace with your actual values):

```bash
SECRET_KEY=your-secret-key-at-least-32-characters
ENVIRONMENT=production
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_FROM=your-email@gmail.com
MAIL_FROM_NAME=IntervYou Support
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
OPENAI_API_KEY=your-openai-api-key
SERPAPI_KEY=your-serpapi-key
```

3. Click **"Update Variables"**

**⚠️ IMPORTANT**: Replace all placeholder values with your actual credentials!

---

## 📧 Gmail App Password Setup

If email is not working, you need to generate a new Gmail App Password:

### Step 1: Enable 2-Factor Authentication

1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification" if not already enabled

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in with your Gmail account
3. Select app: **Mail**
4. Select device: **Other (Custom name)**
5. Enter name: **IntervYou Railway**
6. Click **Generate**
7. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)
8. Remove spaces: `abcdefghijklmnop`

### Step 3: Update Railway Variable

1. Go to Railway Variables
2. Find `MAIL_PASSWORD`
3. Update with the new app password (no spaces)
4. Click **Save**

---

## 🔍 Verify Variables Are Set

After adding variables, verify they're set correctly:

1. In Railway, click **"Deployments"** tab
2. Click **"View Logs"**
3. Look for these log entries on startup:

```
✅ Email service configured - SMTP: smtp.gmail.com:587
✅ Sending from: nayeemabisharan@gmail.com
```

If you see:
```
⚠️  Email service not configured - missing MAIL_USERNAME or MAIL_PASSWORD
```

Then the variables are NOT set correctly in Railway.

---

## 🔄 After Setting Variables

Railway will automatically redeploy when you change variables:

1. Wait 2-3 minutes for redeployment
2. Check logs for "✅ Email service configured"
3. Test password reset again

---

## 🧪 Test Email After Setup

1. Go to: https://intervyou-production-5a2d.up.railway.app/forgot_password
2. Enter your registered email address
3. Click "Send Verification Code"
4. **Check your email inbox**
5. Should receive email with OTP code

---

## 🐛 Troubleshooting

### Email Not Received?

**Check 1**: Verify variables in Railway
- All email variables must be set
- No typos in variable names
- MAIL_PASSWORD is the app password (not regular password)

**Check 2**: Check Railway logs
```
Look for:
✅ Email service configured - SMTP: smtp.gmail.com:587
✅ Sending from: nayeemabisharan@gmail.com
📧 Attempting to send email to [email]
✅ Email sent successfully to [email]
```

**Check 3**: Check spam folder
- Gmail might filter it initially
- Mark as "Not Spam"

**Check 4**: Generate new app password
- Old app password might be expired
- Follow steps above to generate new one

### Still Not Working?

Check logs for specific errors:
- `❌ SMTP Authentication failed` → Wrong MAIL_PASSWORD
- `❌ Cannot send email - email service not configured` → Variables not set
- `❌ SMTP error` → Network or SMTP issue

---

## ✅ Success Indicators

When email is working correctly, you'll see in logs:

```
✅ Email service configured - SMTP: smtp.gmail.com:587
✅ Sending from: your-email@gmail.com
📧 Attempting to send email to recipient@example.com
📧 SMTP: smtp.gmail.com:587
📧 Connecting to SMTP server...
📧 Starting TLS...
📧 Logging in as your-email@gmail.com...
📧 Sending message...
✅ Email sent successfully to recipient@example.com
```

And user receives email in inbox! 📧
