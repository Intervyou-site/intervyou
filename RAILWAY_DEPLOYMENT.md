# 🚂 Deploy IntervYou to Railway + Connect intervyou.site

## ✅ Files Ready for Deployment

I've created all necessary files:
- ✅ `railway.json` - Railway configuration
- ✅ `Procfile` - Start command
- ✅ `runtime.txt` - Python version
- ✅ `.gitignore` - Files to exclude

---

## 📋 Step-by-Step Deployment

### Step 1: Push to GitHub (5 minutes)

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial deployment to Railway"

# Create GitHub repository
# Go to https://github.com/new
# Name it: intervyou
# Don't initialize with README

# Add remote and push
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/intervyou.git
git push -u origin main
```

---

### Step 2: Deploy to Railway (3 minutes)

1. **Go to Railway:**
   - Visit: https://railway.app
   - Click "Login" → Sign in with GitHub

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `intervyou` repository
   - Click "Deploy Now"

3. **Railway will automatically:**
   - ✅ Detect Python
   - ✅ Install dependencies from requirements.txt
   - ✅ Run the start command from Procfile
   - ✅ Assign a public URL

---

### Step 3: Add Environment Variables (2 minutes)

In Railway dashboard:

1. Click on your deployed service
2. Go to "Variables" tab
3. Click "Raw Editor"
4. Paste these (update with your actual values):

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
ENVIRONMENT=production
DATABASE_URL=postgresql://user:password@host:port/database
OPENAI_API_KEY=sk-your-openai-api-key
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
ALLOWED_ORIGINS=https://intervyou.site,https://www.intervyou.site
OTP_LENGTH=6
OTP_EXPIRY_MINUTES=10
OTP_MAX_ATTEMPTS=3
```

4. Click "Update Variables"
5. Railway will automatically redeploy

---

### Step 4: Setup PostgreSQL Database (Optional but Recommended)

**Option A: Use Railway's PostgreSQL (Easiest)**

1. In Railway dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway creates database and adds `DATABASE_URL` automatically
4. Done! Your app will use it automatically

**Option B: Use External Database**

- Use your existing PostgreSQL
- Just set the `DATABASE_URL` in environment variables

---

### Step 5: Connect Your Domain intervyou.site (5 minutes)

1. **In Railway Dashboard:**
   - Click on your service
   - Go to "Settings" tab
   - Scroll to "Domains" section
   - Click "Custom Domain"
   - Enter: `intervyou.site`
   - Railway will show DNS records to add

2. **Railway will show something like:**
   ```
   Add these DNS records to your domain:
   
   Type: CNAME
   Name: @
   Value: your-app.up.railway.app
   
   Type: CNAME
   Name: www
   Value: your-app.up.railway.app
   ```

3. **Go to Your Domain Registrar** (where you bought intervyou.site):

   **If using GoDaddy:**
   - Login → My Products → Domains
   - Click intervyou.site → Manage DNS
   - Add New Record:
     - Type: CNAME
     - Name: @
     - Value: `your-app.up.railway.app`
     - TTL: 600 (or default)
   - Add another:
     - Type: CNAME
     - Name: www
     - Value: `your-app.up.railway.app`
     - TTL: 600

   **If using Namecheap:**
   - Dashboard → Domain List → Manage
   - Advanced DNS → Add New Record
   - Same CNAME records as above

   **If using Cloudflare:**
   - Select intervyou.site
   - DNS → Add record
   - Same CNAME records as above

4. **Wait 5-30 minutes** for DNS propagation

5. **Test your domain:**
   ```bash
   # Check DNS
   nslookup intervyou.site
   
   # Or visit
   https://dnschecker.org
   ```

6. **Visit your site:**
   - https://intervyou.site
   - https://www.intervyou.site

---

### Step 6: Enable SSL/HTTPS (Automatic!)

Railway automatically provides free SSL certificates for custom domains!

Once DNS propagates:
- ✅ https://intervyou.site will work automatically
- ✅ Certificate auto-renews
- ✅ HTTP redirects to HTTPS

---

## 🔍 Verify Deployment

### Check if app is running:

1. **Railway Dashboard:**
   - Check "Deployments" tab
   - Should show "Success" status
   - Click "View Logs" to see output

2. **Test the app:**
   ```bash
   # Test Railway URL first
   curl https://your-app.up.railway.app/health
   
   # Then test your domain (after DNS propagates)
   curl https://intervyou.site/health
   ```

3. **Visit in browser:**
   - https://intervyou.site
   - Try logging in, creating account, etc.

---

## 🔧 Update Your App (Future Deployments)

Railway auto-deploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update feature X"
git push

# Railway automatically:
# 1. Detects the push
# 2. Rebuilds the app
# 3. Deploys new version
# 4. Zero downtime!
```

---

## 📊 Monitor Your App

**Railway Dashboard provides:**
- ✅ Real-time logs
- ✅ Metrics (CPU, Memory, Network)
- ✅ Deployment history
- ✅ Environment variables
- ✅ Custom domains
- ✅ Database management

**Access logs:**
- Railway Dashboard → Your Service → "Logs" tab
- See real-time application output

---

## 💰 Pricing

**Railway Pricing:**
- **Free Trial:** $5 credit (good for testing)
- **Hobby Plan:** $5/month (500 hours)
- **Pro Plan:** $20/month (unlimited)

**What you'll need:**
- Hobby plan is perfect for your app (~$5-10/month)
- Includes: App hosting + PostgreSQL database + SSL

---

## 🐛 Troubleshooting

### App won't start?

**Check logs in Railway:**
```
Railway Dashboard → Logs tab
```

**Common issues:**
1. Missing environment variables
2. Database connection error
3. Port binding (Railway uses $PORT automatically)

### Domain not working?

**Check DNS propagation:**
```bash
nslookup intervyou.site
# Should show Railway's IP or CNAME
```

**Use DNS checker:**
- https://dnschecker.org
- Enter: intervyou.site
- Should show Railway's address globally

**Wait time:**
- Usually 5-15 minutes
- Can take up to 48 hours (rare)

### SSL not working?

- Railway provides SSL automatically
- Wait 5-10 minutes after DNS propagates
- Check Railway dashboard for SSL status

---

## 🎯 Quick Checklist

Before going live:

- [ ] Code pushed to GitHub
- [ ] Deployed to Railway
- [ ] Environment variables added
- [ ] PostgreSQL database connected (optional)
- [ ] Custom domain added in Railway
- [ ] DNS records updated at registrar
- [ ] DNS propagated (check with nslookup)
- [ ] HTTPS working
- [ ] Test all features (login, practice, etc.)
- [ ] Check logs for errors

---

## 📞 Support

**Railway:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Status: https://status.railway.app

**DNS Help:**
- DNS Checker: https://dnschecker.org
- What's My DNS: https://whatsmydns.net

---

## 🚀 You're All Set!

After following these steps:

✅ Your app will be live at **https://intervyou.site**  
✅ Auto-deploys from GitHub  
✅ Free SSL/HTTPS  
✅ Professional hosting  
✅ Easy to scale  

**Total time:** ~15-20 minutes + DNS wait time

---

**Need help?** Let me know which step you're on and I'll guide you through it!

