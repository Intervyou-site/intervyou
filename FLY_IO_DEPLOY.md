# Deploy to Fly.io (FREE & WORKS!)

## ✅ Why Fly.io?
- **FREE tier**: 3 VMs, 3GB storage
- **Works perfectly** with your app
- **Custom domain** support (intervyou.site)
- **Free SSL/HTTPS**
- **No credit card** required for free tier

---

## 🚀 Quick Deploy (5 minutes)

### Step 1: Install Fly CLI

**Windows:**
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

**Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

### Step 2: Sign Up & Login

```bash
fly auth signup
# Or if you have an account:
fly auth login
```

### Step 3: Create fly.toml

I'll create this for you...

### Step 4: Deploy!

```bash
fly launch --no-deploy
fly deploy
```

### Step 5: Add Environment Variables

```bash
fly secrets set SECRET_KEY="your-secret-key"
fly secrets set OPENAI_API_KEY="your-openai-key"
fly secrets set MAIL_USERNAME="your-email"
fly secrets set MAIL_PASSWORD="your-password"
fly secrets set GOOGLE_CLIENT_ID="your-google-id"
fly secrets set GOOGLE_CLIENT_SECRET="your-google-secret"
```

### Step 6: Connect Your Domain

```bash
fly certs add intervyou.site
fly certs add www.intervyou.site
```

Fly will show you DNS records to add:

| Type | Name | Value |
|------|------|-------|
| A | @ | [Fly's IPv4] |
| AAAA | @ | [Fly's IPv6] |
| A | www | [Fly's IPv4] |
| AAAA | www | [Fly's IPv6] |

### Step 7: Done!

Visit: https://intervyou.site 🎉

---

## 📊 Free Tier Limits

- **3 VMs** (shared CPU)
- **256MB RAM** per VM
- **3GB storage**
- **160GB bandwidth/month**
- **Free SSL**

Perfect for your app!

---

## 🔄 Update Your App

```bash
git push
fly deploy
```

That's it!

---

## 💡 Alternative: Use Your Own Server

If you have a VPS or want to use your own server:

```bash
# On your server
git clone https://github.com/Intervyou-site/intervyou.git
cd intervyou
docker-compose up -d
```

Then point intervyou.site to your server's IP!

