# 🚀 Docker Quick Start for IntervYou

## ✅ Docker is Installed!

You've successfully installed Docker Desktop. Now let's run your IntervYou app.

---

## 🎯 Run Your App (3 Easy Steps)

### Step 1: Open PowerShell in Project Directory

```powershell
# Right-click in your project folder and select "Open in Terminal"
# Or navigate to your project:
cd "C:\AI POWERED INTERVIEW COACH"
```

### Step 2: Run the Startup Script

```powershell
.\docker-start.ps1
```

This will:
- ✅ Check if Docker is running
- ✅ Build your app image
- ✅ Start the containers
- ✅ Open your browser automatically

### Step 3: Access Your App

Your app will open automatically at: **http://localhost:8000**

---

## 📋 Quick Commands

### Start the App
```powershell
.\docker-start.ps1
```

### Stop the App
```powershell
.\docker-stop.ps1
```

### View Logs
```powershell
.\docker-logs.ps1
```

### Manual Commands
```powershell
# Build
docker build -t intervyou:latest .

# Start
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f

# Check status
docker compose ps

# Restart
docker compose restart
```

---

## 🔧 If You Get Errors

### "Execution of scripts is disabled"

Run this in PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Docker daemon is not running"

1. Open Docker Desktop from Start Menu
2. Wait for it to say "Docker Desktop is running"
3. Try again

### "Port 8000 is already in use"

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### ".env file missing"

The script will create it automatically from `.env.example`. Just edit it with your values.

---

## 🌐 Deploy to Cloud

Once your app works locally, deploy to:

### Azure Container Instances
```powershell
# See DOCKER_DEPLOYMENT.md for full guide
az acr build --registry intervyouacr --image intervyou:latest .
```

### AWS ECS
```powershell
# Push to ECR
docker tag intervyou:latest ACCOUNT.dkr.ecr.region.amazonaws.com/intervyou:latest
docker push ACCOUNT.dkr.ecr.region.amazonaws.com/intervyou:latest
```

### Google Cloud Run
```powershell
gcloud builds submit --tag gcr.io/PROJECT_ID/intervyou
gcloud run deploy intervyou --image gcr.io/PROJECT_ID/intervyou
```

---

## 📊 Monitor Your App

### Check Container Health
```powershell
docker compose ps
```

### View Resource Usage
```powershell
docker stats intervyou-app
```

### Access Container Shell
```powershell
docker compose exec web bash
```

---

## 🎉 You're Ready!

Your IntervYou app is now Dockerized and ready to deploy anywhere!

**Next Steps:**
1. ✅ Test locally with Docker
2. ✅ Push to GitHub (already done)
3. ✅ Deploy to Azure/AWS/GCP
4. ✅ Set up custom domain
5. ✅ Enable HTTPS

---

**Need help?** Check the full guides:
- `DOCKER_SETUP.md` - Complete Docker setup
- `DOCKER_DEPLOYMENT.md` - Cloud deployment guides
- `AZURE_DEPLOYMENT.md` - Azure-specific deployment
