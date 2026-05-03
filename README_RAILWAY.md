# 🚂 IntervYou on Railway - Complete Guide

<div align="center">

![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Deploy your IntervYou AI Interview Platform to Railway in 5 minutes!**

[Quick Start](#-quick-start-5-minutes) • [Full Guide](#-complete-deployment-guide) • [Troubleshooting](#-troubleshooting) • [Costs](#-pricing)

</div>

---

## 🎯 Why Railway?

| Feature | Railway | Other Platforms |
|---------|---------|-----------------|
| **Setup Time** | 5 minutes | 30+ minutes |
| **Database** | Included (PostgreSQL) | Separate setup |
| **SSL/HTTPS** | Automatic | Manual config |
| **Git Deploy** | Auto on push | Manual deploy |
| **Pricing** | $5 free credit | Varies |
| **FastAPI Support** | Excellent | Varies |

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- GitHub account
- Your IntervYou code pushed to GitHub
- 5 minutes of your time ⏱️

### Step-by-Step

#### 1️⃣ Push to GitHub
```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
```

#### 2️⃣ Create Railway Project
1. Visit **https://railway.app**
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your **IntervYou repository**
5. Railway auto-detects your Dockerfile ✅

#### 3️⃣ Add PostgreSQL Database
1. In your project, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway automatically sets `DATABASE_URL` ✅

#### 4️⃣ Configure Environment Variables
Click **"Variables"** tab and add:

```env
SECRET_KEY=<your-generated-secret-key>
ENVIRONMENT=production
PORT=8000
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Optional (but recommended):**
```env
OPENAI_API_KEY=sk-your-openai-key
SERPAPI_KEY=your-serpapi-key
```

#### 5️⃣ Deploy & Access
1. Railway automatically deploys your app
2. Go to **"Settings"** → **"Networking"**
3. Click **"Generate Domain"**
4. Your app is live! 🎉

**Your URL**: `https://your-app-name.up.railway.app`

---

## 📋 Complete Deployment Guide

### Phase 1: Pre-Deployment Preparation

#### Check Your Files
Ensure these files exist (they should already):
- ✅ `Dockerfile`
- ✅ `requirements-docker.txt`
- ✅ `.env.example`
- ✅ `fastapi_app_cleaned.py`
- ✅ `railway.toml` (optional but helpful)

#### Run Setup Script (Optional)
**Windows:**
```powershell
.\railway-setup.ps1
```

**Linux/Mac:**
```bash
chmod +x railway-setup.sh
./railway-setup.sh
```

This script will:
- Check all required files
- Generate a SECRET_KEY
- Help you commit and push to GitHub

### Phase 2: Railway Configuration

#### Create Account
1. Go to https://railway.app
2. Click **"Login"** → **"Login with GitHub"**
3. Authorize Railway to access your repositories

#### Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your IntervYou repository
4. Railway will:
   - Clone your repository
   - Detect your Dockerfile
   - Start building your app

#### Monitor Build
1. Click on your service
2. Go to **"Deployments"** tab
3. Watch the build logs
4. Wait for "Build successful" ✅

### Phase 3: Database Setup

#### Add PostgreSQL
1. In your project dashboard, click **"+ New"**
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway will:
   - Create a PostgreSQL instance
   - Generate a `DATABASE_URL`
   - Automatically link it to your app

#### Verify Database Connection
Railway automatically injects `DATABASE_URL` into your app. You don't need to set it manually!

The format will be:
```
postgresql://postgres:password@host:port/railway
```

### Phase 4: Environment Variables

#### Required Variables

| Variable | Value | How to Get |
|----------|-------|------------|
| `SECRET_KEY` | Random string | `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `ENVIRONMENT` | `production` | Set manually |
| `PORT` | `8000` | Set manually |

#### Optional Variables (AI Features)

| Variable | Purpose | Where to Get |
|----------|---------|--------------|
| `OPENAI_API_KEY` | AI question generation | https://platform.openai.com/api-keys |
| `SERPAPI_KEY` | Web search | https://serpapi.com/manage-api-key |

#### Optional Variables (Email)

| Variable | Purpose | How to Get |
|----------|---------|------------|
| `MAIL_USERNAME` | Email address | Your Gmail |
| `MAIL_PASSWORD` | App password | https://myaccount.google.com/apppasswords |

#### Optional Variables (OAuth)

| Variable | Purpose | Where to Get |
|----------|---------|--------------|
| `GOOGLE_CLIENT_ID` | Google login | https://console.cloud.google.com/apis/credentials |
| `GOOGLE_CLIENT_SECRET` | Google login | Same as above |

#### How to Add Variables in Railway
1. Click on your service
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Enter variable name and value
5. Click **"Add"**
6. Railway will automatically redeploy

### Phase 5: Domain Configuration

#### Railway Domain (Free)
1. Go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. Your app will be available at:
   ```
   https://your-app-name.up.railway.app
   ```

#### Custom Domain (Optional)
1. In Railway: **Settings** → **"Domains"** → **"Custom Domain"**
2. Enter your domain: `yourdomain.com`
3. Railway will show DNS records to add

**At your domain registrar (Namecheap, GoDaddy, etc.):**

Add CNAME record:
```
Type: CNAME
Name: @ (or www)
Value: your-app-name.up.railway.app
TTL: Automatic
```

**SSL Certificate**: Railway automatically provides free SSL! 🔒

### Phase 6: Verification

#### Test Health Endpoint
```bash
curl https://your-app-name.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-02T...",
  "version": "2.0.0",
  "features": {
    "huggingface": true,
    "ai_detection": true,
    ...
  }
}
```

#### Test Main Application
1. Visit your Railway URL
2. Register a new account
3. Try the interview features
4. Check resume builder
5. Test admin panel (if applicable)

---

## 🔧 Troubleshooting

### Build Fails

**Symptom**: Build fails with timeout or error

**Solutions**:
1. Check Railway build logs for specific errors
2. Verify `Dockerfile` is correct
3. Ensure `requirements-docker.txt` has all dependencies
4. Try reducing dependencies if build is too large

**Check logs**:
```
Railway Dashboard → Your Service → Deployments → Click on deployment → View logs
```

### Database Connection Issues

**Symptom**: App crashes with database connection error

**Solutions**:
1. Verify PostgreSQL service is running in Railway
2. Check that `DATABASE_URL` is automatically set (don't override it!)
3. Ensure your app is using the Railway-provided `DATABASE_URL`

**Verify DATABASE_URL**:
```
Railway Dashboard → PostgreSQL service → Variables → DATABASE_URL
```

### App Crashes on Startup

**Symptom**: App starts but immediately crashes

**Solutions**:
1. Check Railway logs for error messages
2. Verify all required environment variables are set
3. Ensure `SECRET_KEY` is set
4. Test locally with Docker first:
   ```bash
   docker-compose up
   ```

### Port Issues

**Symptom**: App not accessible

**Solutions**:
1. Ensure `PORT=8000` is set in environment variables
2. Railway automatically maps to the correct port
3. Check that your Dockerfile exposes port 8000

### Slow Performance

**Symptom**: App is slow or times out

**Solutions**:
1. Upgrade Railway plan for more resources
2. Check Railway metrics for CPU/Memory usage
3. Optimize your code (reduce AI model loading)
4. Enable caching where possible

---

## 💰 Pricing

### Railway Pricing Model

Railway uses **usage-based pricing**:

| Resource | Cost |
|----------|------|
| **RAM** | $0.000231/GB-hour |
| **CPU** | $0.000463/vCPU-hour |
| **PostgreSQL** | ~$5-10/month |
| **Free Credit** | $5/month (hobby plan) |

### Estimated Monthly Costs

| App Size | Users | Estimated Cost |
|----------|-------|----------------|
| **Small** | <100 | $10-15/month |
| **Medium** | 100-1000 | $20-40/month |
| **Large** | 1000+ | $50-100/month |

### Cost Optimization Tips

1. **Use smaller AI models** - Reduce memory usage
2. **Enable sleep mode** - For low-traffic apps
3. **Optimize database queries** - Reduce CPU usage
4. **Use caching** - Reduce API calls
5. **Monitor usage** - Check Railway metrics regularly

---

## 📊 Monitoring & Maintenance

### View Logs
```
Railway Dashboard → Your Service → Logs
```

Key logs to monitor:
- `✅ Application startup complete` - App started
- `🚀 Starting IntervYou application...` - Initialization
- Any `ERROR` or `WARNING` messages

### Metrics
```
Railway Dashboard → Your Service → Metrics
```

Monitor:
- **CPU Usage** - Should be <80%
- **Memory Usage** - Should be <80%
- **Network** - Incoming/outgoing traffic
- **Response Time** - Should be <2s

### Alerts (Optional)
Set up alerts in Railway for:
- High CPU usage
- High memory usage
- App crashes
- Build failures

---

## 🔄 Continuous Deployment

Railway automatically deploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Add new feature"
git push origin main

# Railway automatically:
# 1. Detects the push
# 2. Builds new Docker image
# 3. Deploys with zero downtime
# 4. Rolls back if deployment fails
```

### Manual Deployment
If you need to manually trigger a deployment:
```
Railway Dashboard → Your Service → Deployments → Redeploy
```

---

## 🔐 Security Best Practices

### 1. Strong SECRET_KEY
Always generate a strong, random SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Environment Variables
- Never commit `.env` files to Git
- Use Railway's encrypted variable storage
- Rotate secrets regularly

### 3. HTTPS Only
Your app enforces HTTPS in production mode (via `security_config.py`).

### 4. Database Security
- Railway PostgreSQL is private by default
- Only accessible from your Railway services
- Automatic backups enabled

### 5. Regular Updates
```bash
# Update dependencies regularly
pip list --outdated
pip install --upgrade <package>
```

---

## 📈 Scaling Your App

### Vertical Scaling (More Resources)
```
Railway Dashboard → Your Service → Settings → Resources
```

Adjust:
- **Memory**: 512MB → 8GB
- **CPU**: 0.5 → 8 vCPU

### Horizontal Scaling (More Instances)
```
Railway Dashboard → Your Service → Settings → Replicas
```

Set replicas: 1 → 10 instances

**Note**: Horizontal scaling requires session management (Redis recommended)

---

## 🎓 Additional Resources

### Documentation
- **Railway Docs**: https://docs.railway.app
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

### Community
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app

### Tools
- **Railway CLI**: https://docs.railway.app/develop/cli
  ```bash
  npm i -g @railway/cli
  railway login
  railway status
  ```

---

## ✅ Deployment Checklist

Use this checklist to ensure everything is set up correctly:

- [ ] Code pushed to GitHub
- [ ] Railway account created
- [ ] Project created from GitHub repo
- [ ] PostgreSQL database added
- [ ] `SECRET_KEY` environment variable set
- [ ] `ENVIRONMENT=production` set
- [ ] `PORT=8000` set
- [ ] Optional API keys added (OpenAI, etc.)
- [ ] Domain generated or custom domain added
- [ ] Health check passing (`/health`)
- [ ] App accessible via URL
- [ ] User registration works
- [ ] User login works
- [ ] Interview features work
- [ ] Admin panel accessible
- [ ] Monitoring set up

---

## 🎉 Success!

Your IntervYou app is now live on Railway! 🚀

**Next Steps**:
1. Share your app URL with users
2. Create an admin account
3. Monitor logs and metrics
4. Gather user feedback
5. Iterate and improve

**Your App**: `https://your-app-name.up.railway.app`

---

## 📞 Need Help?

- 📖 **Full Checklist**: See `RAILWAY_CHECKLIST.md`
- 🚀 **Quick Start**: See `RAILWAY_QUICK_START.md`
- 🔧 **Setup Script**: Run `railway-setup.ps1` or `railway-setup.sh`
- 💬 **Railway Discord**: https://discord.gg/railway

---

<div align="center">

**Made with ❤️ for Interview Preparation**

[⬆ Back to Top](#-intervyou-on-railway---complete-guide)

</div>
