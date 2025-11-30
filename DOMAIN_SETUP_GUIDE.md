# Connecting Intervyou.site to Your App

## 🎯 Overview

You have: **Intervyou.site** domain  
You need: Deploy app + Connect domain

---

## 🚀 Recommended: Railway (Easiest)

### Step 1: Deploy to Railway

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/intervyou.git
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Sign in with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your intervyou repository
   - Railway will auto-detect Python and deploy!

3. **Add Environment Variables:**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add all variables from your `.env` file:
     ```
     SECRET_KEY=your-secret-key
     DATABASE_URL=your-database-url
     OPENAI_API_KEY=your-openai-key
     MAIL_USERNAME=your-email
     MAIL_PASSWORD=your-password
     GOOGLE_CLIENT_ID=your-google-id
     GOOGLE_CLIENT_SECRET=your-google-secret
     ```

4. **Get Railway URL:**
   - You'll get a URL like: `intervyou-production.up.railway.app`
   - Test it to make sure it works!

### Step 2: Connect Your Domain

1. **In Railway Dashboard:**
   - Go to your project
   - Click "Settings" → "Domains"
   - Click "Custom Domain"
   - Enter: `intervyou.site`
   - Railway will show you DNS records to add

2. **In Your Domain Registrar (where you bought intervyou.site):**
   
   **Add these DNS records:**
   
   | Type | Name | Value | TTL |
   |------|------|-------|-----|
   | CNAME | www | `YOUR-APP.up.railway.app` | 3600 |
   | A | @ | Railway's IP (they'll provide) | 3600 |
   
   **OR simpler (recommended):**
   
   | Type | Name | Value | TTL |
   |------|------|-------|-----|
   | CNAME | @ | `YOUR-APP.up.railway.app` | 3600 |
   | CNAME | www | `YOUR-APP.up.railway.app` | 3600 |

3. **Wait for DNS propagation (5-30 minutes)**

4. **Done!** Your app will be live at:
   - https://intervyou.site
   - https://www.intervyou.site

**Railway automatically provides SSL/HTTPS for free!**

---

## 🔄 Alternative: Render (Also Easy)

### Step 1: Deploy to Render

1. **Create `render.yaml` in your project:**
   ```yaml
   services:
     - type: web
       name: intervyou
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn fastapi_app:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

2. **Deploy:**
   - Push to GitHub
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Render auto-deploys!

3. **Add Environment Variables** (same as Railway)

### Step 2: Connect Domain

1. **In Render Dashboard:**
   - Go to your service
   - Click "Settings" → "Custom Domain"
   - Add: `intervyou.site`

2. **In Your Domain Registrar:**
   
   Add DNS records Render provides (similar to Railway)

---

## ☁️ Alternative: Vercel (For Static + API)

### Step 1: Deploy

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Step 2: Connect Domain

```bash
vercel domains add intervyou.site
```

Follow the DNS instructions Vercel provides.

---

## 🏢 Alternative: Traditional VPS (More Control)

### Option A: DigitalOcean

1. **Create Droplet:**
   - Go to https://digitalocean.com
   - Create Ubuntu 22.04 droplet ($6/month)
   - Note the IP address

2. **Setup Server:**
   ```bash
   # SSH into server
   ssh root@YOUR_SERVER_IP

   # Install dependencies
   apt update
   apt install python3-pip python3-venv nginx certbot python3-certbot-nginx

   # Clone your repo
   git clone https://github.com/YOUR_USERNAME/intervyou.git
   cd intervyou

   # Setup Python
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Create systemd service
   nano /etc/systemd/system/intervyou.service
   ```

   **Add this to the service file:**
   ```ini
   [Unit]
   Description=IntervYou FastAPI App
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/root/intervyou
   Environment="PATH=/root/intervyou/venv/bin"
   ExecStart=/root/intervyou/venv/bin/gunicorn fastapi_app:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   # Start service
   systemctl enable intervyou
   systemctl start intervyou

   # Setup Nginx
   nano /etc/nginx/sites-available/intervyou
   ```

   **Add this Nginx config:**
   ```nginx
   server {
       listen 80;
       server_name intervyou.site www.intervyou.site;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   ```bash
   # Enable site
   ln -s /etc/nginx/sites-available/intervyou /etc/nginx/sites-enabled/
   nginx -t
   systemctl restart nginx

   # Get SSL certificate
   certbot --nginx -d intervyou.site -d www.intervyou.site
   ```

3. **Configure DNS:**
   
   In your domain registrar:
   
   | Type | Name | Value | TTL |
   |------|------|-------|-----|
   | A | @ | YOUR_SERVER_IP | 3600 |
   | A | www | YOUR_SERVER_IP | 3600 |

---

## 📋 DNS Configuration Guide

### Where to Configure DNS

Go to where you bought **intervyou.site** (e.g., GoDaddy, Namecheap, Google Domains, Cloudflare)

### Common Registrars:

**GoDaddy:**
1. Login → My Products → Domains
2. Click intervyou.site → Manage DNS
3. Add records

**Namecheap:**
1. Dashboard → Domain List
2. Click "Manage" next to intervyou.site
3. Advanced DNS → Add records

**Google Domains:**
1. My Domains → intervyou.site
2. DNS → Custom records

**Cloudflare:**
1. Select intervyou.site
2. DNS → Add record

---

## ✅ Verification Checklist

After setup, verify:

- [ ] App is deployed and running
- [ ] Environment variables are set
- [ ] DNS records are added
- [ ] Wait 5-30 minutes for DNS propagation
- [ ] Test: `https://intervyou.site`
- [ ] Test: `https://www.intervyou.site`
- [ ] SSL certificate is active (https works)
- [ ] All features work (login, practice, etc.)

---

## 🔍 Troubleshooting

**Domain not working after 30 minutes?**
```bash
# Check DNS propagation
nslookup intervyou.site
# or visit: https://dnschecker.org
```

**SSL not working?**
- Railway/Render/Vercel provide SSL automatically
- For VPS, run: `certbot --nginx -d intervyou.site`

**App not loading?**
- Check deployment logs in Railway/Render dashboard
- Verify environment variables are set
- Check if server is running: `curl https://intervyou.site/health`

---

## 💰 Cost Comparison

| Platform | Cost/Month | SSL | Ease | Best For |
|----------|-----------|-----|------|----------|
| **Railway** | $5-20 | ✅ Free | ⭐⭐⭐⭐⭐ | Recommended |
| **Render** | Free-$7 | ✅ Free | ⭐⭐⭐⭐⭐ | Budget |
| **Vercel** | Free-$20 | ✅ Free | ⭐⭐⭐⭐ | Serverless |
| **DigitalOcean** | $6+ | ✅ Free | ⭐⭐⭐ | Full control |
| **AWS/Azure/GCP** | $10-50+ | ✅ Free | ⭐⭐ | Enterprise |

---

## 🎯 My Recommendation for You

**Best Option: Railway**

1. Deploy to Railway (10 minutes)
2. Add custom domain in Railway dashboard
3. Update DNS records at your registrar
4. Done! SSL included, auto-scaling, easy updates

**Why Railway?**
- ✅ Easiest setup
- ✅ Free SSL/HTTPS
- ✅ Auto-deploys from GitHub
- ✅ Built-in database options
- ✅ Great for Python/FastAPI
- ✅ $5/month (free trial available)

---

## 📞 Need Help?

**Railway Support:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

**DNS Help:**
- DNS Checker: https://dnschecker.org
- What's My DNS: https://whatsmydns.net

---

**Next Steps:**
1. Choose a platform (I recommend Railway)
2. Deploy your app
3. Add intervyou.site as custom domain
4. Update DNS records
5. Wait 10-30 minutes
6. Visit https://intervyou.site 🎉

