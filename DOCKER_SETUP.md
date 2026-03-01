# IntervYou Docker Setup Guide

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- PowerShell (Windows) or Bash (Linux/Mac)

### Option 1: Automated Setup (Recommended)
```powershell
# Build and start everything automatically
.\manage-docker.ps1 build
.\manage-docker.ps1 start
```

### Option 2: Manual Steps
```powershell
# 1. Clean up old images
.\docker-cleanup.ps1 -Force

# 2. Build the application
docker build -t intervyou-cleaned:latest .

# 3. Start with docker-compose
docker-compose up -d
```

## 📋 Management Commands

### Using the Management Script
```powershell
# Build the application
.\manage-docker.ps1 build

# Start services
.\manage-docker.ps1 start

# Stop services
.\manage-docker.ps1 stop

# View logs
.\manage-docker.ps1 logs -Follow

# Check status
.\manage-docker.ps1 status

# Clean up old images
.\manage-docker.ps1 cleanup -Force

# Get help
.\manage-docker.ps1 help
```

### Direct Docker Commands
```powershell
# Build image
docker build -t intervyou-cleaned:latest .

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Check running containers
docker-compose ps
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
# Required
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://intervyou:intervyou123@db:5432/intervyou

# Optional AI Features
OPENAI_API_KEY=your-openai-key
SERPAPI_KEY=your-serpapi-key
COPYLEAKS_API_KEY=your-copyleaks-key
COPYLEAKS_EMAIL=your-copyleaks-email

# Optional Email
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Optional OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Docker Images Kept
After cleanup, you'll have these essential images:
- `postgres:15-alpine` (~390 MB) - Database
- `intervyou-cleaned:latest` (~1.5 GB) - Optimized application

## 🏗️ Architecture

### Services
- **web**: FastAPI application (port 8000)
- **db**: PostgreSQL database (port 5432)

### Volumes
- `./uploads` - User uploaded files
- `./static/audio` - Audio files
- `./static/uploads` - Static uploads
- `./services` - Service modules
- `postgres_data` - Database data

### Health Checks
- Application: http://localhost:8000/health
- Database: Built-in PostgreSQL health check

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```powershell
# Stop existing services
docker-compose down

# Check what's using port 8000
netstat -ano | findstr :8000

# Kill the process if needed
taskkill /PID <process-id> /F
```

#### 2. Database Connection Issues
```powershell
# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### 3. Build Failures
```powershell
# Clean build (no cache)
docker build --no-cache -t intervyou-cleaned:latest .

# Check disk space
docker system df

# Clean up if needed
docker system prune -f
```

#### 4. Permission Issues (Linux/Mac)
```bash
# Fix permissions
sudo chown -R $USER:$USER ./uploads ./static

# Make scripts executable
chmod +x docker-build.sh
```

### Logs and Debugging
```powershell
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f web

# Check container status
docker-compose ps

# Execute commands in container
docker-compose exec web bash
```

## 📊 Performance Optimization

### Image Size Optimization
- Multi-stage build reduces final image size
- Only production dependencies included
- Removed unnecessary development tools

### Resource Usage
- 2 Gunicorn workers for better performance
- Connection pooling for database
- Health checks for reliability

### Monitoring
```powershell
# Check resource usage
docker stats

# Check disk usage
docker system df

# Monitor logs
.\manage-docker.ps1 logs -Follow
```

## 🔄 Updates and Maintenance

### Updating the Application
```powershell
# 1. Stop services
.\manage-docker.ps1 stop

# 2. Pull latest code
git pull

# 3. Rebuild
.\manage-docker.ps1 build

# 4. Start services
.\manage-docker.ps1 start
```

### Database Migrations
```powershell
# Run migrations
docker-compose exec web alembic upgrade head

# Create new migration
docker-compose exec web alembic revision --autogenerate -m "description"
```

### Backup and Restore
```powershell
# Backup database
docker-compose exec db pg_dump -U intervyou intervyou > backup.sql

# Restore database
docker-compose exec -T db psql -U intervyou intervyou < backup.sql
```

## 🎯 Next Steps

1. **Access the application**: http://localhost:8000
2. **Check health**: http://localhost:8000/health
3. **View API docs**: http://localhost:8000/docs
4. **Monitor logs**: `.\manage-docker.ps1 logs -Follow`
5. **Configure environment variables** in `.env` file
6. **Set up SSL/HTTPS** for production deployment

## 📞 Support

If you encounter issues:
1. Check the logs: `.\manage-docker.ps1 logs`
2. Verify Docker is running: `docker info`
3. Check port availability: `netstat -ano | findstr :8000`
4. Try a clean rebuild: `.\manage-docker.ps1 cleanup -Force` then `.\manage-docker.ps1 build`