# Deploy IntervYou to Azure + Connect intervyou.site

## 🚀 Azure App Service Deployment

### Step 1: Create Azure Account

1. Go to https://portal.azure.com
2. Sign up (free tier available)
3. You get $200 credit for 30 days + free services

---

### Step 2: Create App Service (Web Portal Method)

1. **Login to Azure Portal:** https://portal.azure.com

2. **Create App Service:**
   - Click "Create a resource"
   - Search for "Web App"
   - Click "Create"

3. **Configure:**
   - **Subscription:** Free Trial or Pay-As-You-Go
   - **Resource Group:** Create new → "intervyou-rg"
   - **Name:** `intervyou` (this gives you: intervyou.azurewebsites.net)
   - **Publish:** Code
   - **Runtime stack:** Python 3.11
   - **Region:** Choose closest to you
   - **Pricing:** Free F1 (or Basic B1 for $13/month with custom domain)

4. Click **"Review + Create"** → **"Create"**

---

### Step 3: Deploy Your Code

**Option A: Deploy from GitHub (Easiest)**

1. In Azure Portal, go to your App Service
2. Click **"Deployment Center"**
3. **Source:** GitHub
4. Authorize GitHub
5. Select:
   - **Organization:** Intervyou-site
   - **Repository:** intervyou
   - **Branch:** main
6. Click **"Save"**

Azure will auto-deploy from GitHub!

**Option B: Deploy via Azure CLI**

```bash
# Login
az login

# Create resource group
az group create --name intervyou-rg --location eastus

# Create App Service plan (Free tier)
az appservice plan create --name intervyou-plan --resource-group intervyou-rg --sku F1 --is-linux

# Create web app
az webapp create --resource-group intervyou-rg --plan intervyou-plan --name intervyou --runtime "PYTHON:3.11" --deployment-local-git

# Deploy from GitHub
az webapp deployment source config --name intervyou --resource-group intervyou-rg --repo-url https://github.com/Intervyou-site/intervyou --branch main --manual-integration
```

---

### Step 4: Configure Environment Variables

1. In Azure Portal, go to your App Service
2. Click **"Configuration"** (left menu)
3. Click **"New application setting"** for each:

```
DATABASE_URL=<your-supabase-database-url>
SECRET_KEY=<your-secret-key>
OPENAI_API_KEY=<your-openai-api-key>
MAIL_USERNAME=<your-email>
MAIL_PASSWORD=<your-email-app-password>
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
ENVIRONMENT=production
SCM_DO_BUILD_DURING_DEPLOYMENT=true
WEBSITES_PORT=8000
```

4. Click **"Save"**
5. App will restart

---

### Step 5: Configure Startup Command

1. In **"Configuration"** → **"General settings"**
2. **Startup Command:**
   ```
   gunicorn fastapi_app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 120
   ```
3. Click **"Save"**

---

### Step 6: Test Your App

Visit: `https://intervyou.azurewebsites.net`

---

## 🌐 Connect Your Custom Domain (intervyou.site)

### Important: Custom Domains Require Paid Tier

**Free F1 tier does NOT support custom domains.**

You need to upgrade to:
- **Basic B1:** $13/month (supports custom domains + SSL)
- **Standard S1:** $55/month (more resources)

### Upgrade to Basic B1:

1. Go to your App Service
2. Click **"Scale up (App Service plan)"**
3. Select **"Basic B1"**
4. Click **"Apply"**

---

### Add Custom Domain:

1. **In Azure Portal:**
   - Go to your App Service
   - Click **"Custom domains"**
   - Click **"Add custom domain"**
   - Enter: `intervyou.site`
   - Azure will show you DNS records to add

2. **Azure will show something like:**
   ```
   Add these DNS records to your domain registrar:
   
   Type: CNAME
   Name: www
   Value: intervyou.azurewebsites.net
   
   Type: A
   Name: @
   Value: 20.xxx.xxx.xxx (Azure's IP)
   
   Type: TXT
   Name: asuid
   Value: xxxxxxxxxxxxx (verification)
   ```

3. **In Your Domain Registrar (GoDaddy/Namecheap/etc):**

   Add these DNS records:

   | Type | Name | Value | TTL |
   |------|------|-------|-----|
   | A | @ | [Azure IP] | 3600 |
   | CNAME | www | intervyou.azurewebsites.net | 3600 |
   | TXT | asuid | [Azure verification code] | 3600 |

4. **Wait 10-30 minutes** for DNS propagation

5. **Back in Azure:**
   - Click **"Validate"**
   - If successful, click **"Add"**

6. **Enable HTTPS:**
   - In "Custom domains", click on your domain
   - Click **"Add binding"**
   - Select **"SNI SSL"** (free)
   - Azure will provision SSL certificate automatically

---

## 🎯 Summary

### Free Tier (F1):
- ✅ Your app at: `intervyou.azurewebsites.net`
- ❌ No custom domain
- ❌ Limited resources (60 min/day CPU)
- **Cost:** FREE

### Basic Tier (B1):
- ✅ Your app at: `intervyou.site`
- ✅ Custom domain support
- ✅ Free SSL certificate
- ✅ Always on
- **Cost:** $13/month

---

## 🔧 Troubleshooting

### App won't start?

**Check logs:**
1. Azure Portal → Your App Service
2. Click **"Log stream"**
3. See real-time logs

**Or download logs:**
```bash
az webapp log download --name intervyou --resource-group intervyou-rg
```

### Can't connect to Supabase?

Add to Configuration:
```
WEBSITES_PORT=8000
```

### Need more memory?

Upgrade to B1 or higher tier.

---

## 💰 Pricing

| Tier | Cost/Month | Custom Domain | SSL | CPU Time |
|------|-----------|---------------|-----|----------|
| **F1 (Free)** | $0 | ❌ | ❌ | 60 min/day |
| **B1 (Basic)** | $13 | ✅ | ✅ | Unlimited |
| **S1 (Standard)** | $55 | ✅ | ✅ | More resources |

---

## 📞 Next Steps

1. **Deploy to Azure** (Free tier first)
2. **Test at:** `intervyou.azurewebsites.net`
3. **If it works, upgrade to B1** ($13/month)
4. **Add custom domain:** `intervyou.site`
5. **Enable SSL** (automatic)

---

**Start here:** https://portal.azure.com

Create your App Service and let me know when you're ready for the next step!
