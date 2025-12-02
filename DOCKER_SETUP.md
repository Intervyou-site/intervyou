# Docker Setup for IntervYou

## 📦 What's Included

Your IntervYou app is now fully Dockerized with:

- ✅ **Dockerfile** - Optimized multi-stage build
- ✅ **docker-compose.yml** - Development setup
- ✅ **docker-compose.prod.yml** - Production setup with Nginx
- ✅ **.dockerignore** - Excludes unnecessary files
- ✅ **nginx.conf** - Reverse proxy configuration
- ✅ **Build & run scripts** - Easy deployment

---

## 🚀 Installation

### Windows

1. **Download Docker Desktop**:
   - Go to: https://www.docker.com/products/docker-desktop/
   - Download Docker Desktop for Windows
   - Run the installer

2. **Enable WSL 2** (if prompted):
   ```powershell
   wsl --install
   ```

3. **Verify installation**:
   ```powershell
   docker --version
   docker-compose --version
   ```

### Mac

```bash
# Install via Homebrew
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop/
```

### Linux

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
```

---

## 🎯 Quick Start

### 1. Prepare Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your actual values
notepad .env  # Windows
nano .env     # Linux/Mac
```

### 2. Build & Run

**Option A: Using Docker Compose (Recommended)**

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

**Option B: Using Scripts**

```bash
# Windows (PowerShell)
.\docker-build.sh
.\docker-run.sh

# Linux/Mac
chmod +x docker-build.sh docker-run.sh
./docker-build.sh
./docker-run.sh
```

**Option C: Manual Docker Commands**

```bash
# Build
docker build -t intervyou:latest .

# Run
docker run -d \
  --name intervyou \
  -p 8000:8000 \
  --env-file .env \
  -v ${PWD}/uploads:/app/uploads \
  intervyou:latest
```

### 3. Access Your App

Open browser: **http://localhost:8000**

---

## 🔧 Common Commands

### Development

```bash
# Start in foreground (see logs)
docker-compose up

# Start in background
docker-compose up -d

# Rebuild after code changes
docker-compose up -d --build

# View logs
docker-compose logs -f web

# Stop everything
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Production

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Scale workers
docker-compose -f docker-compose.prod.yml up -d --scale web=3
```

### Debugging

```bash
# Access container shell
docker-compose exec web bash

# Check environment variables
docker-compose exec web env

# Test database connection
docker-compose exec web python -c "from fastapi_app import engine; print(engine)"

# View container stats
docker stats intervyou-app
```

---

## 🌐 Deploy to Cloud

### Azure Container Instances

```bash
# Login
az login

# Create container registry
az acr create --resource-group intervyou-rg --name intervyouacr --sku Basic

# Build and push
az acr build --registry intervyouacr --image intervyou:latest .

# Deploy
az container create \
  --resource-group intervyou-rg \
  --name intervyou \
  --image intervyouacr.azurecr.io/intervyou:latest \
  --dns-name-label intervyou \
  --ports 8000 \
  --environment-variables \
    DATABASE_URL="${DATABASE_URL}" \
    SECRET_KEY="${SECRET_KEY}"
```

### AWS ECS (Fargate)

```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker tag intervyou:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/intervyou:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/intervyou:latest

# Create ECS task and service via AWS Console or CLI
```

### Google Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/intervyou
gcloud run deploy intervyou --image gcr.io/PROJECT_ID/intervyou --platform managed
```

### DigitalOcean

```bash
# Push to Docker Hub
docker tag intervyou:latest YOUR_USERNAME/intervyou:latest
docker push YOUR_USERNAME/intervyou:latest

# Create app in DigitalOcean dashboard using the image
```

### Heroku

```bash
# Login to Heroku container registry
heroku container:login

# Push and release
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name
```

---

## 🔐 Production Best Practices

### 1. Use Secrets Management

**Azure Key Vault:**
```bash
az keyvault secret set --vault-name intervyou-vault --name DATABASE-URL --value "your-db-url"
```

**AWS Secrets Manager:**
```bash
aws secretsmanager create-secret --name intervyou/database-url --secret-string "your-db-url"
```

### 2. Enable HTTPS

```bash
# Get SSL certificate (Let's Encrypt)
docker run -it --rm \
  -v /etc/letsencrypt:/etc/letsencrypt \
  certbot/certbot certonly --standalone \
  -d intervyou.site -d www.intervyou.site

# Copy certificates to ssl/ directory
cp /etc/letsencrypt/live/intervyou.site/fullchain.pem ssl/
cp /etc/letsencrypt/live/intervyou.site/privkey.pem ssl/

# Uncomment HTTPS section in nginx.conf
# Restart: docker-compose -f docker-compose.prod.yml restart nginx
```

### 3. Set Up Monitoring

```yaml
# Add to docker-compose.prod.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

### 4. Configure Backups

```bash
# Backup volumes
docker run --rm \
  -v intervyou_uploads:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/uploads-$(date +%Y%m%d).tar.gz /data
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Container Keeps Restarting

```bash
# Check logs
docker-compose logs web

# Common issues:
# - Missing environment variables
# - Database connection failed
# - Port conflict
```

### Out of Disk Space

```bash
# Clean up
docker system prune -a --volumes

# Remove unused images
docker image prune -a
```

### Permission Denied

```bash
# Fix upload directories
chmod -R 755 uploads static/audio static/uploads

# Or run as root (not recommended for production)
docker-compose exec --user root web bash
```

---

## 📊 Performance Tuning

### Optimize Image Size

```dockerfile
# Use multi-stage builds
FROM python:3.11-slim as builder
# ... build dependencies

FROM python:3.11-slim
COPY --from=builder /app /app
```

### Increase Resources

```yaml
# docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Enable Caching

```bash
# Use BuildKit for better caching
DOCKER_BUILDKIT=1 docker build -t intervyou:latest .
```

---

## 📝 Next Steps

1. ✅ Install Docker Desktop
2. ✅ Build and test locally
3. ✅ Push to container registry
4. ✅ Deploy to cloud platform
5. ✅ Set up CI/CD pipeline
6. ✅ Configure monitoring
7. ✅ Enable HTTPS
8. ✅ Set up automated backups

---

## 🆘 Need Help?

- Docker Docs: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- FastAPI + Docker: https://fastapi.tiangolo.com/deployment/docker/

**Check logs first:**
```bash
docker-compose logs -f
```
