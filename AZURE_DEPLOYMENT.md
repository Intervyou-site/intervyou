# Azure Deployment Guide for IntervYou

This guide walks you through deploying your dockerized FastAPI application to Azure Container Apps.

## Prerequisites

1. **Azure CLI** - Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
2. **Azure Account** - Sign up at: https://azure.microsoft.com/free/
3. **Docker** - Already installed ✓

## Quick Start

### Option 1: Automated Deployment (Recommended)

**Windows (PowerShell):**
```powershell
.\azure-setup.ps1
```

**Linux/Mac:**
```bash
chmod +x azure-setup.sh
./azure-setup.sh
```

### Option 2: Manual Deployment

Follow the steps below for more control over the deployment process.

## Manual Deployment Steps

### 1. Configure Your Deployment

Edit `azure-setup.ps1` (or `azure-setup.sh`) and update these values:

```powershell
$RESOURCE_GROUP = "intervyou-rg"           # Your resource group name
$LOCATION = "eastus"                       # Azure region (eastus, westus2, etc.)
$ACR_NAME = "intervyouacr123"              # MUST BE GLOBALLY UNIQUE
$DB_SERVER_NAME = "intervyou-db-123"       # MUST BE GLOBALLY UNIQUE
$DB_ADMIN_PASSWORD = "YourSecurePass123!"  # CHANGE THIS!
$STORAGE_ACCOUNT = "intervyoustorage123"   # MUST BE GLOBALLY UNIQUE
```

### 2. Login to Azure

```bash
az login
```

### 3. Run the Deployment Script

The script will:
- Create a resource group
- Set up Azure Container Registry (ACR)
- Build and push your Docker image
- Create PostgreSQL database
- Create storage account for uploads
- Deploy your container app

### 4. Set Environment Secrets

After deployment, add your sensitive environment variables:

```bash
# Set secrets
az containerapp secret set \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --secrets \
    secret-key="your-secret-key-here" \
    openai-api-key="sk-your-openai-key" \
    mail-username="your-email@gmail.com" \
    mail-password="your-app-password" \
    google-client-id="your-google-client-id" \
    google-client-secret="your-google-client-secret"

# Update environment variables to use secrets
az containerapp update \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --set-env-vars \
    SECRET_KEY=secretref:secret-key \
    OPENAI_API_KEY=secretref:openai-api-key \
    MAIL_USERNAME=secretref:mail-username \
    MAIL_PASSWORD=secretref:mail-password \
    GOOGLE_CLIENT_ID=secretref:google-client-id \
    GOOGLE_CLIENT_SECRET=secretref:google-client-secret
```

### 5. Run Database Migrations

Connect to your container and run Alembic migrations:

```bash
# Get your app URL
APP_URL=$(az containerapp show \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --query properties.configuration.ingress.fqdn -o tsv)

# Execute migrations in the container
az containerapp exec \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --command "alembic upgrade head"
```

### 6. Get Your Application URL

```bash
az containerapp show \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --query properties.configuration.ingress.fqdn -o tsv
```

Your app will be available at: `https://<your-app-name>.azurecontainerapps.io`

## Storage Configuration

Your app uses Azure Blob Storage for file uploads. Update your code to use Azure Storage:

### Install Azure Storage SDK

Add to `requirements.txt`:
```
azure-storage-blob>=12.19.0
```

### Update File Upload Logic

Replace local file storage with Azure Blob Storage in your FastAPI app:

```python
from azure.storage.blob import BlobServiceClient
import os

# Initialize Azure Storage
storage_account = os.getenv("AZURE_STORAGE_ACCOUNT")
storage_key = os.getenv("AZURE_STORAGE_KEY")
blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account}.blob.core.windows.net",
    credential=storage_key
)

# Upload file example
def upload_to_azure(file_data, container_name, blob_name):
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file_data, overwrite=True)
    return blob_client.url
```

## Useful Commands

### View Logs
```bash
az containerapp logs show \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --follow
```

### Update Container Image
```bash
# Rebuild and push new image
az acr build \
  --registry intervyouacr \
  --image intervyou:latest \
  --file Dockerfile .

# Update container app
az containerapp update \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --image intervyouacr.azurecr.io/intervyou:latest
```

### Scale Your App
```bash
az containerapp update \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --min-replicas 2 \
  --max-replicas 5
```

### View App Status
```bash
az containerapp show \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --query properties.runningStatus
```

### Connect to Database
```bash
# Get connection string
az postgres flexible-server show-connection-string \
  --server-name intervyou-db-server \
  --database-name intervyou \
  --admin-user intervyouadmin
```

## Cost Optimization

### Development/Testing
- Use **Burstable** tier for PostgreSQL (B1ms)
- Set min replicas to 0 (scales to zero when idle)
- Use **Standard_LRS** storage

### Production
- Upgrade to **General Purpose** PostgreSQL (GP_Gen5_2)
- Set min replicas to 2 for high availability
- Enable geo-redundant backup
- Use **Standard_GRS** storage for redundancy

### Estimated Monthly Costs
- Container Apps: ~$30-50/month (1-3 replicas)
- PostgreSQL (Burstable): ~$15-25/month
- Storage: ~$5-10/month
- **Total: ~$50-85/month**

## Custom Domain & SSL

### Add Custom Domain
```bash
az containerapp hostname add \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --hostname yourdomain.com
```

SSL certificates are automatically managed by Azure.

## Monitoring & Alerts

### Enable Application Insights
```bash
az monitor app-insights component create \
  --app intervyou-insights \
  --location eastus \
  --resource-group intervyou-rg

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app intervyou-insights \
  --resource-group intervyou-rg \
  --query instrumentationKey -o tsv)

# Add to container app
az containerapp update \
  --name intervyou-app \
  --resource-group intervyou-rg \
  --set-env-vars APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=$INSTRUMENTATION_KEY"
```

## Troubleshooting

### Container Won't Start
```bash
# Check logs
az containerapp logs show --name intervyou-app --resource-group intervyou-rg --tail 100

# Check revision status
az containerapp revision list --name intervyou-app --resource-group intervyou-rg
```

### Database Connection Issues
- Ensure firewall rules allow Container Apps
- Verify DATABASE_URL format includes `?sslmode=require`
- Check database server is running

### Storage Access Issues
- Verify storage account key is correct
- Check container permissions (should be private)
- Ensure CORS is configured if accessing from browser

## Cleanup

To delete all resources and stop billing:

```bash
az group delete --name intervyou-rg --yes --no-wait
```

## Next Steps

1. Set up CI/CD with GitHub Actions
2. Configure custom domain
3. Enable Application Insights monitoring
4. Set up automated backups
5. Configure CDN for static assets

## Support

- Azure Container Apps Docs: https://learn.microsoft.com/en-us/azure/container-apps/
- Azure Database for PostgreSQL: https://learn.microsoft.com/en-us/azure/postgresql/
- Azure Storage: https://learn.microsoft.com/en-us/azure/storage/
