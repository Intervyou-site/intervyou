# 🚂 Railway Deployment Guide for IntervYou

## Why Railway?

✅ **Easiest deployment** - One-click deploy from GitHub  
✅ **Automatic PostgreSQL** - Database included  
✅ **Auto SSL/HTTPS** - Secure by default  
✅ **Git-based deployments** - Push to deploy  
✅ **Free $5 credit** - Test before you pay  
✅ **Perfect for FastAPI** - Optimized for Python apps  

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub** (if not already done):
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

2. **Ensure these files exist** (they already do ✅):
   - `Dockerfile` ✅
   - `requirements-docker.txt` ✅
   - `.env.example` ✅

---

### Step 2: Deploy to Railway

1. **Go to Railway**: https://railway.app
2. **Sign up** with your GitHub account
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your IntervYou repository**
6. Railway will automatically:
   - Detect your Dockerfile
   - Build your application
   - Deploy it

---

### Step 3: Add PostgreSQL Database

1. In your Railway project dashboard
2. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically:
   - Create a PostgreSQL database
   - Generate a `DATABASE_URL` environment variable
   - Connect it to your app

---

### Step 4: Configure Environment Variables

In Railway project → **Variables** tab, add these:

#### Required Variables:
```env
SECRET_KEY=your-super-secret-key-change-this-to-random-string
ENVIRONMENT=production
PORT=8000
```

#### Optional but Recommended (AI Features):
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
SERPAPI_KEY=your-serpapi-key-here
```

#### Optional (Email Features):
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

#### Optional (OAuth Login):
```env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

**Note**: Railway automatically provides `DATABASE_URL` when you add PostgreSQL - **don't override it!**

---

### Step 5: Deploy & Access Your App

1. Railway will automatically deploy after adding variables
2. Go to **Settings** → **Networking** → **Generate Domain**
3. Your app will be available at: `https://your-app-name.up.railway.app`

---

## 🌐 Custom Domain Setup (Optional)

### Add Your Own Domain:

1. In Railway project → **Settings** → **Domains**
2. Click **"Custom Domain"**
3. Enter your domain: `yourdomain.com`
4. Railway will show DNS records to add

### Update Your DNS:

Add these records at your domain registrar (Namecheap, GoDaddy, etc.):

**For root domain (yourdomain.com):**
```
Type: CNAME
Name: @
Value: your-app-name.up.railway.app
```

**For www subdomain:**
```
Type: CNAME
Name: www
Value: your-app-name.up.railway.app
```

**SSL Certificate**: Railway automatically provides free SSL certificates! 🔒

---

## 💰 Pricing

Railway uses a **usage-based pricing** model:

- **$5 free credit** per month (hobby plan)
- **$0.000231/GB-hour** for RAM
- **$0.000463/vCPU-hour** for CPU
- **PostgreSQL**: ~$5-10/month for small apps

**Estimated monthly cost**: $10-20 for a small to medium app

---

## 🔧 Advanced Configuration

### Environment-Specific Settings

Railway automatically sets `RAILWAY_ENVIRONMENT=production`. Your app already handles this in the Dockerfile.

### Scaling

1. Go to **Settings** → **Resources**
2. Adjust:
   - **Memory**: 512MB - 8GB
   - **CPU**: 0.5 - 8 vCPU
   - **Replicas**: 1-10 instances

### Monitoring

Railway provides built-in monitoring:
- **Logs**: Real-time application logs
- **Metrics**: CPU, Memory, Network usage
- **Deployments**: History and rollback options

---

## 🐛 Troubleshooting

### Build Fails

**Problem**: Docker build times out or fails

**Solution**:
1. Check Railway build logs
2. Ensure `requirements-docker.txt` has all dependencies
3. Try reducing dependencies if build is too large

### Database Connection Issues

**Problem**: App can't connect to PostgreSQL

**Solution**:
1. Verify PostgreSQL service is running
2. Check `DATABASE_URL` is automatically set
3. Ensure your app uses the Railway-provided `DATABASE_URL`

### App Crashes on Startup

**Problem**: App starts but immediately crashes

**Solution**:
1. Check Railway logs for errors
2. Verify all required environment variables are set
3. Test locally with Docker first:
```bash
docker-compose up
```

### Port Issues

**Problem**: App not accessible

**Solution**:
Railway automatically maps to port 8000 (defined in your Dockerfile). No changes needed!

---

## 🔄 Continuous Deployment

Railway automatically deploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Railway automatically:
# 1. Detects the push
# 2. Builds new Docker image
# 3. Deploys with zero downtime
```

---

## 📊 Health Checks

Your app already has a health endpoint at `/health`. Railway uses this to monitor your app.

Test it:
```bash
curl https://your-app-name.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-02T...",
  "version": "2.0.0",
  "features": {...}
}
```

---

## 🔐 Security Best Practices

### 1. Generate a Strong SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use this value for `SECRET_KEY` in Railway variables.

### 2. Enable HTTPS Only

Your app already enforces HTTPS in production mode (via `security_config.py`).

### 3. Secure Environment Variables

- Never commit `.env` files to Git
- Use Railway's encrypted variable storage
- Rotate secrets regularly

---

## 📈 Monitoring & Logs

### View Logs:
1. Railway dashboard → Your project
2. Click on the service
3. **Logs** tab shows real-time logs

### Key Logs to Monitor:
- `✅ Application startup complete` - App started successfully
- `🚀 Starting IntervYou application...` - Initialization
- Any `ERROR` or `WARNING` messages

---

## 🎯 Next Steps After Deployment

1. **Test your app**: Visit your Railway URL
2. **Create admin account**: Register and test features
3. **Set up custom domain** (optional)
4. **Configure monitoring alerts** in Railway
5. **Set up backups** for PostgreSQL (Railway provides automatic backups)

---

## 📞 Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app

---

## ✅ Deployment Checklist

Before deploying, ensure:

- [ ] Code pushed to GitHub
- [ ] Railway account created
- [ ] Project created from GitHub repo
- [ ] PostgreSQL database added
- [ ] Environment variables configured
- [ ] Domain generated (or custom domain added)
- [ ] App is accessible and healthy
- [ ] Admin account created
- [ ] Features tested

---

## 🎉 You're Done!

Your IntervYou app is now live on Railway! 🚀

**Your app URL**: `https://your-app-name.up.railway.app`

Share it with users and start helping people prepare for interviews! 💼
