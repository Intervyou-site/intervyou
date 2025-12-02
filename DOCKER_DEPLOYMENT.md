# Docker Deployment Guide for IntervYou

## 🐳 Quick Start

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)

### 1. Build the Docker Image

```bash
# Build the image
docker build -t intervyou:latest .

# Or use the build script
chmod +x docker-build.sh
./docker-build.sh
```

### 2. Run with Docker Compose (Recommended)

```bash
# Make sure .env file exists with your configuration
cp .env.example .env
# Edit .env with your actual values

# Start the application
docker-compose up -d

# Or use the run script
chmod +x docker-run.sh
./docker-run.sh
```

Your app will be available at: **http://localhost:8000**

### 3. Run with Docker (Manual)

```bash
# Run container with environment variables
docker run -d \
  --name intervyou \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/uploads:/app/uploads \
  intervyou:latest
```

---

## 📋 Docker Commands

### View Logs
```bash
# All logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100 -f
```

### Stop Application
```bash
docker-compose down
```

### Restart Application
```bash
docker-compose restart
```

### Check Status
```bash
docker-compose ps
```

### Access Container Shell
```bash
docker-compose exec web bash
```

### Rebuild After Code Changes
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🚀 Deploy to Production

### Deploy to Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group (if not exists)
az group create --name intervyou-rg --location centralindia

# Create container registry
az acr create --resource-group intervyou-rg --name intervyouregistry --sku Basic

# Login to registry
az acr login --name intervyouregistry

# Tag and push image
docker tag intervyou:latest intervyouregistry.azurecr.io/intervyou:latest
docker push intervyouregistry.azurecr.io/intervyou:latest

# Deploy container
az container create \
  --resource-group intervyou-rg \
  --name intervyou-container \
  --image intervyouregistry.azurecr.io/intervyou:latest \
  --dns-name-label intervyou \
  --ports 8000 \
  --environment-variables \
    DATABASE_URL="your-database-url" \
    SECRET_KEY="your-secret-key" \
    OPENAI_API_KEY="your-openai-key" \
    ENVIRONMENT="production"
```

### Deploy to AWS ECS

```bash
# Install AWS CLI and configure
aws configure

# Create ECR repository
aws ecr create-repository --repository-name intervyou

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag intervyou:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/intervyou:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/intervyou:latest

# Create ECS task definition and service (use AWS Console or CLI)
```

### Deploy to Google Cloud Run

```bash
# Install gcloud CLI and configure
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/intervyou

# Deploy to Cloud Run
gcloud run deploy intervyou \
  --image gcr.io/YOUR_PROJECT_ID/intervyou \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="your-db-url",SECRET_KEY="your-secret"
```

### Deploy to DigitalOcean App Platform

```bash
# Push to Docker Hub
docker tag intervyou:latest YOUR_DOCKERHUB_USERNAME/intervyou:latest
docker push YOUR_DOCKERHUB_USERNAME/intervyou:latest

# Then create app in DigitalOcean dashboard using the Docker Hub image
```

---

## 🔧 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs web

# Check if port 8000 is already in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux
```

### Permission errors
```bash
# Fix upload directory permissions
chmod -R 755 uploads static/audio static/uploads
```

### Database connection issues
```bash
# Verify environment variables
docker-compose exec web env | grep DATABASE_URL

# Test database connection
docker-compose exec web python -c "import os; print(os.getenv('DATABASE_URL'))"
```

### Out of memory
```bash
# Increase Docker memory limit in Docker Desktop settings
# Or add to docker-compose.yml:
services:
  web:
    mem_limit: 2g
    memswap_limit: 2g
```

---

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/
```

### Container Stats
```bash
docker stats intervyou-app
```

### Disk Usage
```bash
docker system df
```

---

## 🧹 Cleanup

### Remove containers and images
```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi intervyou:latest

# Clean up unused resources
docker system prune -a
```

---

## 🔐 Security Best Practices

1. **Never commit .env files** - Use .env.example as template
2. **Use secrets management** - For production, use Azure Key Vault, AWS Secrets Manager, etc.
3. **Run as non-root user** - Already configured in Dockerfile
4. **Keep images updated** - Regularly rebuild with latest base images
5. **Scan for vulnerabilities**:
   ```bash
   docker scan intervyou:latest
   ```

---

## 📝 Environment Variables

Required environment variables in `.env`:

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-...
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
ENVIRONMENT=production
```

---

## 🎯 Next Steps

1. Test locally with Docker
2. Push to container registry
3. Deploy to your preferred cloud platform
4. Set up CI/CD pipeline for automatic deployments
5. Configure monitoring and logging
6. Set up automatic backups

---

**Need help?** Check the logs with `docker-compose logs -f`
