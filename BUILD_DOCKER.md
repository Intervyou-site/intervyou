# 🐳 Build IntervYou Docker Image - Quick Guide

## Step 1: Prepare Environment

Make sure you have:
- ✅ Docker Desktop running (I can see it's running!)
- ✅ `.env` file configured with your API keys

## Step 2: Build Docker Image

### Option A: Automated (Recommended)
```powershell
.\docker-build-production.ps1
```

This will:
1. Check Docker is running
2. Verify .env file exists
3. Build the Docker image (~5-10 minutes)
4. Start the container
5. Wait for application to be ready
6. Show you the URL

### Option B: Manual
```powershell
# Build image
docker-compose -f docker-compose.production.yml build

# Start container
docker-compose -f docker-compose.production.yml up -d

# Check logs
docker-compose -f docker-compose.production.yml logs -f
```

## Step 3: Access Application

Once built, access at: **http://localhost:8000**

## Quick Commands

```powershell
# Start
.\docker-manage.ps1 start

# Stop
.\docker-manage.ps1 stop

# View logs
.\docker-manage.ps1 logs

# Check status
.\docker-manage.ps1 status
```

## What Gets Built?

- **Image Name**: intervyou:latest
- **Base**: Python 3.11 slim
- **Size**: ~500MB
- **Includes**: All dependencies, application code, security features
- **Port**: 8000

## Troubleshooting

**If build fails:**
```powershell
# Clean and rebuild
.\docker-build-production.ps1 -Clean
```

**If container won't start:**
```powershell
# Check logs
docker-compose -f docker-compose.production.yml logs

# Restart
docker-compose -f docker-compose.production.yml restart
```

---

**Ready to build? Run:**
```powershell
.\docker-build-production.ps1
```
