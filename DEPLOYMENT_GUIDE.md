# IntervYou - Deployment & Remote Access Guide

## 🚀 Quick Start (Local)

Your server is now running at:
- **Local:** http://localhost:8000
- **Network:** http://0.0.0.0:8000

---

## 🌐 Access from Anywhere - Options

### Option 1: ngrok (Easiest - Free)

**Best for:** Quick testing, demos, temporary access

1. **Install ngrok:**
   ```bash
   # Download from https://ngrok.com/download
   # Or use chocolatey on Windows:
   choco install ngrok
   ```

2. **Start ngrok tunnel:**
   ```bash
   ngrok http 8000
   ```

3. **You'll get a public URL:**
   ```
   Forwarding: https://abc123.ngrok.io -> http://localhost:8000
   ```

4. **Share the URL** - anyone can access your app!

**Pros:** Instant, no configuration, HTTPS included  
**Cons:** URL changes on restart (free tier), session limits

---

### Option 2: Cloudflare Tunnel (Free, Permanent)

**Best for:** Permanent free hosting, custom domains

1. **Install Cloudflare Tunnel:**
   ```bash
   # Download from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   ```

2. **Login and create tunnel:**
   ```bash
   cloudflared tunnel login
   cloudflared tunnel create intervyou
   ```

3. **Start tunnel:**
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```

4. **Get permanent URL** or connect custom domain

**Pros:** Free forever, permanent URL, custom domains  
**Cons:** Requires Cloudflare account

---

### Option 3: Deploy to Cloud (Production)

#### A. Deploy to Railway (Easiest Cloud)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Add environment variables from `.env`
   - Railway will auto-deploy!

**Cost:** Free tier available, then ~$5-20/month

---

#### B. Deploy to Render (Free Tier)

1. **Create `render.yaml`:**
   ```yaml
   services:
     - type: web
       name: intervyou
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn fastapi_app:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
       envVars:
         - key: DATABASE_URL
           sync: false
         - key: SECRET_KEY
           generateValue: true
         - key: OPENAI_API_KEY
           sync: false
   ```

2. **Deploy:**
   - Push to GitHub
   - Go to https://render.com
   - Connect repository
   - Deploy!

**Cost:** Free tier available (spins down after inactivity)

---

#### C. Deploy to AWS/Azure/GCP

**AWS (Elastic Beanstalk):**
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 intervyou

# Create environment
eb create intervyou-env

# Deploy
eb deploy
```

**Azure (App Service):**
```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create app
az webapp up --name intervyou --runtime "PYTHON:3.9"
```

**GCP (Cloud Run):**
```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Build and deploy
gcloud run deploy intervyou --source . --platform managed --region us-central1 --allow-unauthenticated
```

**Cost:** ~$10-50/month depending on usage

---

### Option 4: Local Network Access

**Access from devices on same WiFi:**

1. **Find your local IP:**
   ```bash
   ipconfig
   # Look for IPv4 Address (e.g., 192.168.1.100)
   ```

2. **Access from other devices:**
   ```
   http://192.168.1.100:8000
   ```

**Pros:** Free, fast, no internet required  
**Cons:** Only works on same network

---

### Option 5: Port Forwarding (Home Router)

**Best for:** Permanent home hosting

1. **Find your public IP:**
   - Visit https://whatismyipaddress.com

2. **Configure router port forwarding:**
   - Login to router (usually 192.168.1.1)
   - Forward port 8000 → your computer's local IP
   - Enable port 8000 in Windows Firewall

3. **Access via:**
   ```
   http://YOUR_PUBLIC_IP:8000
   ```

4. **Optional - Get free domain:**
   - Use DuckDNS (https://www.duckdns.org)
   - Get domain like: intervyou.duckdns.org

**Pros:** Free, full control  
**Cons:** Security risks, dynamic IP changes, requires router access

---

## 🔒 Security Checklist (Before Going Public)

Before making your app accessible from anywhere:

- [ ] Change `SECRET_KEY` in `.env` to a strong random value
- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Enable HTTPS (ngrok/Cloudflare provide this automatically)
- [ ] Update `ALLOWED_ORIGINS` in `.env` for CORS
- [ ] Use strong database password
- [ ] Enable rate limiting (add to fastapi_app.py)
- [ ] Review all API keys and credentials
- [ ] Set up monitoring/logging
- [ ] Configure firewall rules

---

## 📊 Recommended Setup by Use Case

| Use Case | Recommended Option | Cost | Setup Time |
|----------|-------------------|------|------------|
| **Quick Demo** | ngrok | Free | 2 minutes |
| **Development/Testing** | Cloudflare Tunnel | Free | 10 minutes |
| **Small Project** | Railway/Render | Free-$10/mo | 15 minutes |
| **Production** | AWS/Azure/GCP | $20-100/mo | 1-2 hours |
| **Home Lab** | Port Forwarding + DuckDNS | Free | 30 minutes |

---

## 🛠️ Quick Commands

**Check if server is running:**
```bash
curl http://localhost:8000/health
```

**Stop server:**
- Press `Ctrl+C` in the terminal

**Restart server:**
```bash
python start.py
```

**View logs:**
- Check terminal output where server is running

---

## 🌍 Current Server Status

Your server is configured to listen on:
- **Host:** 0.0.0.0 (all network interfaces)
- **Port:** 8000
- **Protocol:** HTTP

This means it's already accessible from:
- ✅ localhost:8000 (your computer)
- ✅ Your local IP:8000 (same network devices)
- ❌ Internet (need one of the options above)

---

## 💡 My Recommendation

**For immediate testing:**
1. Install ngrok: https://ngrok.com/download
2. Run: `ngrok http 8000`
3. Share the https URL with anyone!

**For permanent free hosting:**
1. Push code to GitHub
2. Deploy on Railway.app (free tier)
3. Get permanent URL like: intervyou.up.railway.app

**For production:**
1. Deploy to AWS/Azure/GCP
2. Set up proper database (PostgreSQL)
3. Configure domain and SSL
4. Set up monitoring

---

## 📞 Need Help?

- **ngrok docs:** https://ngrok.com/docs
- **Railway docs:** https://docs.railway.app
- **Render docs:** https://render.com/docs
- **Cloudflare Tunnel:** https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/

---

**Last Updated:** November 24, 2025
