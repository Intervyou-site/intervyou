# 🆓 Deploy IntervYou to Render (100% FREE)

## ✅ Why Render?

- ✅ **Completely FREE** tier (no credit card required)
- ✅ Free SSL/HTTPS
- ✅ Custom domain support (intervyou.site)
- ✅ Auto-deploys from GitHub
- ✅ 750 hours/month free (enough for 24/7)

**Note:** Free tier spins down after 15 minutes of inactivity (takes ~30 seconds to wake up)

---

## 🚀 Step-by-Step Deployment

### Step 1: Push render.yaml to GitHub (1 minute)

```bash
git add render.yaml
git commit -m "Add Render config"
git push
```

---

### Step 2: Deploy to Render (3 minutes)

1. **Go to Render:**
   - Visit: https://render.com
   - Click "Get Started for Free"
   - Sign in with GitHub

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Click "Connect account" (authorize GitHub)
   - Select repository: `Intervyou-site/intervyou`
   - Click "Connect"

3. **Configure (Auto-filled from render.yaml):**
   - Name: `intervyou`
   - Region: Oregon (US West)
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn fastapi_app:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - Plan: **Free**
   - Click "Create Web Service"

---

### Step 3: Add Environment Variables (2 minutes)

While it's deploying:

1. **Go to "Environment" tab**
2. **Add these variables:**

   Click "Add Environment Variable" for each:

   | Key | Value |
   |-----|-------|
   | `OPENAI_API_KEY` | Your OpenAI key |
   | `MAIL_USERNAME` | Your Gmail address |
   | `MAIL_PASSWORD` | Your Gmail app password |
   | `GOOGLE_CLIENT_ID` | Your Google OAuth ID |
   | `GOOGLE_CLIENT_SECRET` | Your Google OAuth secret |
   | `DATABASE_URL` | `sqlite:///./database.db` (or PostgreSQL) |
   | `ENVIRONMENT` | `production` |

3. **Click "Save Changes"**
   - Render will automatically redeploy

---

### Step 4: Get Your URL (Instant)

After deployment completes (~5 minutes):

- You'll get a URL like: `https://intervyou.onrender.com`
- Test it! Click the URL to see your app

---

### Step 5: Connect Your Domain intervyou.site (5 minutes)

1. **In Render Dashboard:**
   - Go to your service
   - Click "Settings" tab
   - Scroll to "Custom Domain"
   - Click "Add Custom Domain"
   - Enter: `intervyou.site`
   - Click "Save"

2. **Render will show DNS records like:**
   ```
   Add these CNAME records to your domain:
   
   Name: intervyou.site
   Type: CNAME
   Value: intervyou.onrender.com
   
   Name: www
   Type: CNAME  
   Value: intervyou.onrender.com
   ```

3. **Go to Your Domain Registrar:**

   **If using GoDaddy:**
   - Login → My Products → Domains
   - Click intervyou.site → Manage DNS
   - Delete any existing A records for @ and www
   - Add New Record:
     - Type: CNAME
     - Name: @
     - Value: `intervyou.onrender.com`
     - TTL: 600
   - Add another:
     - Type: CNAME
     - Name: www
     - Value: `intervyou.onrender.com`
     - TTL: 600

   **If using Namecheap:**
   - Dashboard → Domain List → Manage
   - Advanced DNS
   - Delete existing A records
   - Add New Record:
     - Type: CNAME Record
     - Host: @
     - Value: `intervyou.onrender.com`
     - TTL: Automatic
   - Add another for www

   **If using Cloudflare:**
   - Select intervyou.site
   - DNS → Add record
   - Type: CNAME
   - Name: @
   - Target: `intervyou.onrender.com`
   - Proxy status: DNS only (gray cloud)
   - Add another for www

4. **Wait 5-30 minutes for DNS propagation**

5. **Verify SSL:**
   - Render automatically provisions SSL
   - Visit: https://intervyou.site
   - Should show secure padlock 🔒

---

## 🔄 Alternative: Use Apex Domain with A Record

Some registrars don't support CNAME for apex domain (@). Use A record instead:

**Get Render's IP:**
```bash
nslookup intervyou.onrender.com
```

**Add A Record:**
- Type: A
- Name: @
- Value: [Render's IP address]
- TTL: 600

**Add CNAME for www:**
- Type: CNAME
- Name: www
- Value: intervyou.onrender.com

---

## 📊 Free Tier Limits

| Feature | Free Tier |
|---------|-----------|
| **Hours/month** | 750 (enough for 24/7) |
| **Bandwidth** | 100 GB/month |
| **Build minutes** | 500/month |
| **Spin down** | After 15 min inactivity |
| **Wake up time** | ~30 seconds |
| **SSL** | ✅ Free |
| **Custom domain** | ✅ Free |
| **Auto-deploy** | ✅ Free |

**Note:** App sleeps after 15 minutes of no traffic. First request after sleep takes ~30 seconds.

---

## 🚀 Keep Your App Awake (Optional)

To prevent spin-down, use a free uptime monitor:

### Option 1: UptimeRobot (Free)

1. Go to: https://uptimerobot.com
2. Sign up (free)
3. Add New Monitor:
   - Type: HTTP(s)
   - URL: `https://intervyou.site/health`
   - Interval: 5 minutes
4. Done! Your app stays awake

### Option 2: Cron-job.org (Free)

1. Go to: https://cron-job.org
2. Sign up
3. Create cronjob:
   - URL: `https://intervyou.site/health`
   - Interval: Every 5 minutes
4. Done!

---

## 🔧 Update Your App

Render auto-deploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Render automatically:
# 1. Detects push
# 2. Rebuilds
# 3. Deploys
# 4. Zero downtime!
```

---

## 📊 Monitor Your App

**Render Dashboard provides:**
- ✅ Real-time logs
- ✅ Metrics (CPU, Memory, Requests)
- ✅ Deployment history
- ✅ Environment variables
- ✅ Custom domains
- ✅ SSL certificates

**View logs:**
- Render Dashboard → Your Service → "Logs" tab

---

## 🐛 Troubleshooting

### App won't start?

**Check logs:**
- Render Dashboard → Logs tab
- Look for errors

**Common issues:**
1. Missing environment variables
2. Wrong Python version
3. Database connection error
4. Port binding (Render uses $PORT automatically)

### Domain not working?

**Check DNS:**
```bash
nslookup intervyou.site
# Should show Render's address
```

**Use DNS checker:**
- https://dnschecker.org
- Enter: intervyou.site

**Wait time:**
- Usually 5-15 minutes
- Can take up to 48 hours (rare)

### SSL not working?

- Render provides SSL automatically
- Wait 5-10 minutes after DNS propagates
- Check Render dashboard for SSL status

### App is slow?

- Free tier spins down after 15 minutes
- First request takes ~30 seconds to wake up
- Use UptimeRobot to keep it awake (see above)

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid |
|----------|-----------|------|
| **Render** | ✅ 750 hrs/mo | $7/mo (always on) |
| **Railway** | ❌ Trial only | $5/mo |
| **Vercel** | ✅ Limited | $20/mo |
| **Heroku** | ❌ Removed | $7/mo |

**Render is the best free option!**

---

## 🎯 Quick Checklist

- [ ] Code pushed to GitHub
- [ ] render.yaml added
- [ ] Deployed to Render
- [ ] Environment variables added
- [ ] Custom domain added in Render
- [ ] DNS records updated at registrar
- [ ] DNS propagated (check with nslookup)
- [ ] HTTPS working
- [ ] Test all features
- [ ] (Optional) Set up UptimeRobot

---

## 📞 Support

**Render:**
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

**DNS Help:**
- DNS Checker: https://dnschecker.org
- What's My DNS: https://whatsmydns.net

---

## 🎉 You're All Set!

After following these steps:

✅ Your app will be live at **https://intervyou.site**  
✅ 100% FREE hosting  
✅ Auto-deploys from GitHub  
✅ Free SSL/HTTPS  
✅ Professional hosting  

**Total time:** ~15-20 minutes + DNS wait time

---

**Next Steps:**
1. Push render.yaml to GitHub ✓
2. Deploy on Render (3 minutes)
3. Add environment variables (2 minutes)
4. Connect intervyou.site (5 minutes)
5. Wait for DNS (10-30 minutes)
6. Visit https://intervyou.site 🎉

