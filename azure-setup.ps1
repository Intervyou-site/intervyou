# Azure Container Apps Deployment Script (PowerShell)
# Run this script to deploy your application to Azure

$ErrorActionPreference = "Stop"

# Configuration - UPDATE THESE VALUES
$RESOURCE_GROUP = "intervyou-rg"
$LOCATION = "centralus"  # Changed from eastus - better for Azure Student
$CONTAINER_APP_ENV = "intervyou-env"
$CONTAINER_APP_NAME = "intervyou-app"
$ACR_NAME = "intervyouacr$(Get-Random -Maximum 9999)"  # Auto-generate unique name
$DB_SERVER_NAME = "intervyou-db-$(Get-Random -Maximum 9999)"  # Auto-generate unique name
$DB_NAME = "intervyou"
$DB_ADMIN_USER = "intervyouadmin"
$DB_ADMIN_PASSWORD = "ChangeThisPassword123!"  # CHANGE THIS!
$STORAGE_ACCOUNT = "intervyoustor$(Get-Random -Maximum 9999)"  # Auto-generate unique name

Write-Host "Starting Azure deployment..." -ForegroundColor Green

# Register required resource providers first
Write-Host "Registering required resource providers..." -ForegroundColor Cyan
az provider register --namespace Microsoft.App --wait
az provider register --namespace Microsoft.OperationalInsights --wait
az provider register --namespace Microsoft.ContainerRegistry --wait

# 1. Login to Azure (if not already logged in)
Write-Host "Checking Azure login..." -ForegroundColor Cyan
try {
    az account show | Out-Null
} catch {
    az login
}

# 2. Create Resource Group
Write-Host "Creating resource group..." -ForegroundColor Cyan
az group create `
  --name $RESOURCE_GROUP `
  --location $LOCATION

Write-Host "Using ACR name: $ACR_NAME" -ForegroundColor Yellow
Write-Host "Using DB server name: $DB_SERVER_NAME" -ForegroundColor Yellow
Write-Host "Using Storage account: $STORAGE_ACCOUNT" -ForegroundColor Yellow

# 3. Create Azure Container Registry (try multiple regions if needed)
Write-Host "Creating Azure Container Registry..." -ForegroundColor Cyan
$acrCreated = $false
$regions = @("centralus", "westus2", "eastus2", "westus")

foreach ($region in $regions) {
    Write-Host "Trying region: $region" -ForegroundColor Yellow
    try {
        az acr create `
          --resource-group $RESOURCE_GROUP `
          --name $ACR_NAME `
          --sku Basic `
          --location $region `
          --admin-enabled true 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "ACR created successfully in $region" -ForegroundColor Green
            $acrCreated = $true
            break
        }
    } catch {
        Write-Host "Failed in $region, trying next..." -ForegroundColor Yellow
    }
}

if (-not $acrCreated) {
    Write-Host "ERROR: Could not create ACR in any region. Your Azure Student subscription may have restrictions." -ForegroundColor Red
    Write-Host "Alternative: Use Docker Hub instead of ACR" -ForegroundColor Yellow
    exit 1
}

# 4. Build and push Docker image to ACR
Write-Host "Building and pushing Docker image..." -ForegroundColor Cyan
Write-Host "This may take 5-10 minutes..." -ForegroundColor Yellow
az acr build `
  --registry $ACR_NAME `
  --image intervyou:latest `
  --file Dockerfile .

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to build image. Check your Dockerfile and try again." -ForegroundColor Red
    exit 1
}

# 5. Create Azure Database for PostgreSQL
Write-Host "Creating PostgreSQL database..." -ForegroundColor Cyan
$dbCreated = $false
$dbRegions = @("centralus", "westus2", "eastus2", "westus", "northeurope")

foreach ($region in $dbRegions) {
    Write-Host "Trying PostgreSQL in region: $region" -ForegroundColor Yellow
    try {
        az postgres flexible-server create `
          --resource-group $RESOURCE_GROUP `
          --name $DB_SERVER_NAME `
          --location $region `
          --admin-user $DB_ADMIN_USER `
          --admin-password $DB_ADMIN_PASSWORD `
          --sku-name Standard_B1ms `
          --tier Burstable `
          --version 15 `
          --storage-size 32 `
          --public-access 0.0.0.0-255.255.255.255 `
          --yes 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "PostgreSQL created successfully in $region" -ForegroundColor Green
            $dbCreated = $true
            
            # Create database
            az postgres flexible-server db create `
              --resource-group $RESOURCE_GROUP `
              --server-name $DB_SERVER_NAME `
              --database-name $DB_NAME
            break
        }
    } catch {
        Write-Host "Failed in $region, trying next..." -ForegroundColor Yellow
    }
}

if (-not $dbCreated) {
    Write-Host "WARNING: Could not create PostgreSQL. You may need to use external database." -ForegroundColor Yellow
    $DB_HOST = "your-external-db-host"
    $DATABASE_URL = "postgresql://${DB_ADMIN_USER}:${DB_ADMIN_PASSWORD}@${DB_HOST}:5432/${DB_NAME}"
} else {
    $DB_HOST = "${DB_SERVER_NAME}.postgres.database.azure.com"
    $DATABASE_URL = "postgresql://${DB_ADMIN_USER}:${DB_ADMIN_PASSWORD}@${DB_HOST}:5432/${DB_NAME}?sslmode=require"
}

# 6. Create Storage Account
Write-Host "Creating storage account..." -ForegroundColor Cyan
az storage account create `
  --name $STORAGE_ACCOUNT `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --sku Standard_LRS

if ($LASTEXITCODE -eq 0) {
    # Create blob containers
    $STORAGE_KEY = (az storage account keys list `
      --resource-group $RESOURCE_GROUP `
      --account-name $STORAGE_ACCOUNT `
      --query '[0].value' -o tsv)

    if ($STORAGE_KEY) {
        az storage container create --name uploads --account-name $STORAGE_ACCOUNT --account-key $STORAGE_KEY
        az storage container create --name audio --account-name $STORAGE_ACCOUNT --account-key $STORAGE_KEY
        az storage container create --name static-uploads --account-name $STORAGE_ACCOUNT --account-key $STORAGE_KEY
        Write-Host "Storage containers created successfully" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Could not get storage key" -ForegroundColor Yellow
        $STORAGE_KEY = ""
    }
} else {
    Write-Host "WARNING: Storage account creation failed" -ForegroundColor Yellow
    $STORAGE_KEY = ""
}

# 7. Create Container Apps Environment
Write-Host "Creating Container Apps environment..." -ForegroundColor Cyan
$envCreated = $false
$envRegions = @("centralus", "westus2", "eastus2", "canadacentral", "northeurope")

foreach ($region in $envRegions) {
    Write-Host "Trying Container Apps environment in: $region" -ForegroundColor Yellow
    try {
        az containerapp env create `
          --name $CONTAINER_APP_ENV `
          --resource-group $RESOURCE_GROUP `
          --location $region 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Container Apps environment created in $region" -ForegroundColor Green
            $LOCATION = $region  # Update location for container app
            $envCreated = $true
            break
        }
    } catch {
        Write-Host "Failed in $region, trying next..." -ForegroundColor Yellow
    }
}

if (-not $envCreated) {
    Write-Host "ERROR: Could not create Container Apps environment" -ForegroundColor Red
    exit 1
}

# 8. Get ACR credentials
Write-Host "Getting ACR credentials..." -ForegroundColor Cyan
$ACR_LOGIN_SERVER = (az acr show --name $ACR_NAME --query loginServer -o tsv)
$ACR_USERNAME = (az acr credential show --name $ACR_NAME --query username -o tsv)
$ACR_PASSWORD = (az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

if (-not $ACR_LOGIN_SERVER -or -not $ACR_USERNAME -or -not $ACR_PASSWORD) {
    Write-Host "ERROR: Could not get ACR credentials" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Please set your environment secrets now..." -ForegroundColor Yellow
Write-Host "You'll need to provide:"
Write-Host "  - SECRET_KEY"
Write-Host "  - OPENAI_API_KEY"
Write-Host "  - MAIL_USERNAME"
Write-Host "  - MAIL_PASSWORD"
Write-Host "  - GOOGLE_CLIENT_ID"
Write-Host "  - GOOGLE_CLIENT_SECRET"
Write-Host ""
Write-Host "DATABASE_URL will be: $DATABASE_URL" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press enter when ready to continue"

# 10. Create Container App
Write-Host "Deploying container app..." -ForegroundColor Cyan
Write-Host "This may take a few minutes..." -ForegroundColor Yellow

az containerapp create `
  --name $CONTAINER_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --environment $CONTAINER_APP_ENV `
  --image "${ACR_LOGIN_SERVER}/intervyou:latest" `
  --registry-server $ACR_LOGIN_SERVER `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --target-port 8000 `
  --ingress external `
  --cpu 1.0 `
  --memory 2Gi `
  --min-replicas 1 `
  --max-replicas 3 `
  --env-vars `
    "DATABASE_URL=$DATABASE_URL" `
    "ENVIRONMENT=production" `
    "PORT=8000" `
    "AZURE_STORAGE_ACCOUNT=$STORAGE_ACCOUNT" `
    "AZURE_STORAGE_KEY=$STORAGE_KEY"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Deployment complete!" -ForegroundColor Green
    Write-Host ""
    
    # Get the app URL
    $APP_URL = (az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)
    Write-Host "Your app is available at: https://$APP_URL" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Set your secrets using: az containerapp secret set"
    Write-Host "2. Update environment variables with your API keys"
    Write-Host "3. Run database migrations"
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Cyan
    Write-Host "  View logs: az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow"
    Write-Host "  Update app: az containerapp update --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --image ${ACR_LOGIN_SERVER}/intervyou:latest"
} else {
    Write-Host ""
    Write-Host "ERROR: Container app deployment failed" -ForegroundColor Red
    Write-Host "Check the error messages above for details" -ForegroundColor Yellow
}
