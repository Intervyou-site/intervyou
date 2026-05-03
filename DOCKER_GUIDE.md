# IntervYou Docker Deployment Guide

## 🐳 Quick Start

### Option 1: Automated Build (Recommended)
```powershell
# Build and start containers
.\docker-build-production.ps1

# Build and show logs
.\docker-build-production.ps1 -Logs

# Clean build (remove old containers)
.\docker-build-production.ps1 -Clean
```

### Option 2: Manual Commands
```bash
# Build the image
docker-compose -f docker-compose.production.yml build

# Start containers
docker-compose -f docker-compose.production.yml up -d

# View logs
docker-compose -f docker-compose.production.yml logs -f
```

## 📋 Prerequisites

1. **Docker Desktop** installed and running
2. **Environment variables** configured in `.env` file
3. **Minimum 2GB RAM** available for Docker
4. **Port 8000** available

## ⚙️ Configuration

### 1. Environment Setup

Create/edit `.env` file:
```env
# Required
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key

# Email (Optional but recommended)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# Security
RATE_LIMIT_ENABLED=true
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_MINUTES=15
```

### 2. Generate Secret Key
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🚀 Deployment Steps

### Step 1: Build Docker Image
```powershell
# Using script (recommended)
.\docker-build-production.ps1

# Or manually
docker-compose -f docker-compose.production.yml build
```

**Build time**: 5-10 minutes (first time)

### Step 2: Start Containers
```powershell
# Using script
.\docker-manage.ps1 start

# Or manually
docker-compose -f docker-compose.production.yml up -d
```

### Step 3: Verify Deployment
```powershell
# Check status
.\docker-manage.ps1 status

# View logs
.\docker-manage.ps1 logs

# Test application
curl http://localhost:8000
```

### Step 4: Access Application
Open browser: **http://localhost:8000**

## 🛠️ Management Commands

### Using Management Script
```powershell
# Start containers
.\docker-manage.ps1 start

# Stop containers
.\docker-manage.ps1 stop

# Restart containers
.\docker-manage.ps1 restart

# View logs
.\docker-manage.ps1 logs

# Check status
.\docker-manage.ps1 status

# Clean up
.\docker-manage.ps1 clean

# Rebuild from scratch
.\docker-manage.ps1 rebuild
```

### Manual Docker Commands
```bash
# Start
docker-compose -f docker-compose.production.yml up -d

# Stop
docker-compose -f docker-compose.production.yml down

# Restart
docker-compose -f docker-compose.production.yml restart

# Logs
docker-compose -f docker-compose.production.yml logs -f

# Status
docker-compose -f docker-compose.production.yml ps

# Execute command in container
docker-compose -f docker-compose.production.yml exec web bash

# View resource usage
docker stats intervyou-app
```

## 📊 Monitoring

### View Logs
```bash
# All logs
docker-compose -f docker-compose.production.yml logs -f

# Last 100 lines
docker-compose -f docker-compose.production.yml logs --tail=100

# Specific service
docker-compose -f docker-compose.production.yml logs -f web
```

### Check Health
```bash
# Container health
docker ps

# Application health
curl http://localhost:8000/

# Resource usage
docker stats intervyou-app
```

## 🔧 Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose -f docker-compose.production.yml logs

# Check if port is in use
netstat -ano | findstr :8000

# Rebuild container
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml build --no-cache
docker-compose -f docker-compose.production.yml up -d
```

### Application Not Responding
```bash
# Check container status
docker ps

# Restart container
docker-compose -f docker-compose.production.yml restart

# Check logs for errors
docker-compose -f docker-compose.production.yml logs --tail=50
```

### Database Issues
```bash
# Access container
docker-compose -f docker-compose.production.yml exec web bash

# Check database file
ls -la database.db

# Backup database
docker cp intervyou-app:/app/database.db ./database.backup.db
```

### Out of Memory
```bash
# Check memory usage
docker stats intervyou-app

# Increase Docker memory limit in Docker Desktop settings
# Settings > Resources > Memory > Increase to 4GB
```

## 🔄 Updates & Maintenance

### Update Application Code
```bash
# Stop containers
docker-compose -f docker-compose.production.yml down

# Pull latest code (if using git)
git pull

# Rebuild and start
docker-compose -f docker-compose.production.yml build
docker-compose -f docker-compose.production.yml up -d
```

### Update Dependencies
```bash
# Update requirements.txt
# Then rebuild
docker-compose -f docker-compose.production.yml build --no-cache
docker-compose -f docker-compose.production.yml up -d
```

### Backup Data
```bash
# Backup database
docker cp intervyou-app:/app/database.db ./backups/database-$(date +%Y%m%d).db

# Backup uploads
docker cp intervyou-app:/app/uploads ./backups/uploads-$(date +%Y%m%d)
```

## 📦 Docker Image Details

### Image Information
- **Base Image**: python:3.11-slim
- **Size**: ~500MB (optimized)
- **Architecture**: Multi-stage build
- **User**: Non-root (appuser)
- **Port**: 8000

### Included Components
- Python 3.11
- FastAPI application
- All required dependencies
- Audio processing libraries (ffmpeg, libsndfile)
- Health check endpoint

### Volumes
- `./database.db` - SQLite database
- `./uploads` - User uploads
- `./static/audio` - Audio files
- `./static/uploads` - Static uploads
- `./logs` - Application logs

## 🌐 Production Deployment

### Cloud Platforms

#### AWS (ECS/Fargate)
```bash
# Tag image
docker tag intervyou:latest <account-id>.dkr.ecr.<region>.amazonaws.com/intervyou:latest

# Push to ECR
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/intervyou:latest
```

#### Azure (Container Instances)
```bash
# Tag image
docker tag intervyou:latest <registry>.azurecr.io/intervyou:latest

# Push to ACR
docker push <registry>.azurecr.io/intervyou:latest
```

#### Google Cloud (Cloud Run)
```bash
# Tag image
docker tag intervyou:latest gcr.io/<project-id>/intervyou:latest

# Push to GCR
docker push gcr.io/<project-id>/intervyou:latest
```

### Docker Hub
```bash
# Login
docker login

# Tag image
docker tag intervyou:latest <username>/intervyou:latest

# Push
docker push <username>/intervyou:latest
```

## 🔒 Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use strong SECRET_KEY** (32+ characters)
3. **Rotate secrets regularly**
4. **Keep Docker images updated**
5. **Use non-root user** (already configured)
6. **Limit container resources**
7. **Enable Docker Content Trust**
8. **Scan images for vulnerabilities**

## 📈 Performance Optimization

### Resource Limits
Edit `docker-compose.production.yml`:
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Multiple Workers
For production, increase workers:
```yaml
command: ["python", "-m", "uvicorn", "fastapi_app_cleaned:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## 🆘 Support

### Common Issues

**Issue**: Port 8000 already in use
**Solution**: 
```bash
# Find process using port
netstat -ano | findstr :8000
# Kill process or change port in docker-compose.production.yml
```

**Issue**: Docker build fails
**Solution**:
```bash
# Clean Docker cache
docker system prune -a
# Rebuild
docker-compose -f docker-compose.production.yml build --no-cache
```

**Issue**: Container keeps restarting
**Solution**:
```bash
# Check logs
docker-compose -f docker-compose.production.yml logs
# Fix configuration issue
# Restart
docker-compose -f docker-compose.production.yml restart
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Uvicorn Deployment](https://www.uvicorn.org/deployment/)

---

**Last Updated**: 2025-01-XX
**Version**: 1.0.0
