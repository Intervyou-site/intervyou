# 🚂 Railway Deployment - Quick Reference Card

## 🚀 Deploy in 5 Steps

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to Railway
https://railway.app

# 3. Deploy from GitHub repo
Click "New Project" → "Deploy from GitHub repo"

# 4. Add PostgreSQL
Click "+ New" → "Database" → "PostgreSQL"

# 5. Set Variables
SECRET_KEY=<generate-random-string>
ENVIRONMENT=production
PORT=8000
```

---

## 🔑 Generate SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📚 Documentation Quick Links

| Need | File |
|------|------|
| **Start Here** | START_HERE_RAILWAY.md |
| **5-Min Guide** | RAILWAY_QUICK_START.md |
| **Full Guide** | RAILWAY_DEPLOYMENT.md |
| **Checklist** | RAILWAY_CHECKLIST.md |
| **Reference** | README_RAILWAY.md |
| **Architecture** | RAILWAY_ARCHITECTURE.md |
| **Comparison** | HOSTING_COMPARISON.md |

---

## 🔧 Setup Scripts

**Windows:**
```powershell
.\railway-setup.ps1
```

**Linux/Mac:**
```bash
chmod +x railway-setup.sh
./railway-setup.sh
```

---

## ✅ Required Environment Variables

```env
SECRET_KEY=<your-generated-secret-key>
ENVIRONMENT=production
PORT=8000
```

---

## 🎯 Optional Environment Variables

### AI Features:
```env
OPENAI_API_KEY=sk-your-openai-key
SERPAPI_KEY=your-serpapi-key
```

### Email:
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### OAuth:
```env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

---

## 🧪 Test Deployment

```bash
curl https://your-app.up.railway.app/health
```

Expected:
```json
{"status": "healthy", "version": "2.0.0"}
```

---

## 💰 Pricing

| App Size | Cost/Month |
|----------|------------|
| Small | $10-15 |
| Medium | $20-40 |
| Large | $50-100 |

**Free $5 credit** to start!

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check Railway logs |
| DB connection | Verify PostgreSQL running |
| App crashes | Check env variables |
| Slow | Upgrade resources |

---

## 📞 Support

- **Docs**: https://docs.railway.app
- **Discord**: https://discord.gg/railway
- **Status**: https://status.railway.app

---

## 🎉 You're Ready!

**Start with**: START_HERE_RAILWAY.md

**Deploy in**: 5 minutes

**Your app**: https://your-app.up.railway.app
