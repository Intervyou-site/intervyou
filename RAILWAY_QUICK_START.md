# 🚂 Railway Quick Start - 5 Minutes to Deploy

## Step 1: Push to GitHub (1 min)
```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
```

## Step 2: Create Railway Project (2 min)
1. Go to **https://railway.app**
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your **IntervYou repository**

## Step 3: Add Database (1 min)
1. Click **"+ New"** in your project
2. Select **"Database"** → **"PostgreSQL"**
3. Done! `DATABASE_URL` is auto-configured

## Step 4: Set Environment Variables (1 min)
Click **"Variables"** tab and add:

```env
SECRET_KEY=<generate-random-string>
ENVIRONMENT=production
PORT=8000
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Step 5: Get Your URL (30 sec)
1. Go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. Your app is live at: `https://your-app.up.railway.app`

---

## 🎉 That's It!

Your IntervYou app is now live on Railway!

### Test Your Deployment:
```bash
curl https://your-app.up.railway.app/health
```

Expected response:
```json
{"status": "healthy", "version": "2.0.0"}
```

---

## Optional: Add Custom Domain

1. **Railway**: Settings → Domains → Add Custom Domain
2. **Your DNS**: Add CNAME record:
   ```
   Type: CNAME
   Name: @
   Value: your-app.up.railway.app
   ```

---

## Need Help?

- 📖 **Full Guide**: See `RAILWAY_DEPLOYMENT.md`
- ✅ **Checklist**: See `RAILWAY_CHECKLIST.md`
- 🔧 **Setup Script**: Run `./railway-setup.ps1` (Windows) or `./railway-setup.sh` (Linux/Mac)

---

## Estimated Costs

- **Free tier**: $5 credit/month
- **Small app**: ~$10-15/month
- **Includes**: App hosting + PostgreSQL database + SSL

---

## Common Issues

### Build fails?
- Check Railway logs for errors
- Verify `Dockerfile` and `requirements-docker.txt`

### Can't connect to database?
- Railway auto-sets `DATABASE_URL` - don't override it
- Ensure PostgreSQL service is running

### App crashes?
- Check environment variables are set
- View logs in Railway dashboard

---

## 🚀 You're Live!

Share your app and start helping people ace their interviews! 💼
