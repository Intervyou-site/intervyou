#!/bin/bash
# Azure Container Apps Deployment Script
# Run this script to deploy your application to Azure

set -e

# Configuration - UPDATE THESE VALUES
RESOURCE_GROUP="intervyou-rg"
LOCATION="eastus"
CONTAINER_APP_ENV="intervyou-env"
CONTAINER_APP_NAME="intervyou-app"
ACR_NAME="intervyouacr"  # Must be globally unique, lowercase, no hyphens
DB_SERVER_NAME="intervyou-db-server"  # Must be globally unique
DB_NAME="intervyou"
DB_ADMIN_USER="intervyouadmin"
DB_ADMIN_PASSWORD="ChangeThisPassword123!"  # CHANGE THIS!
STORAGE_ACCOUNT="intervyoustorage"  # Must be globally unique

echo "🚀 Starting Azure deployment..."

# 1. Login to Azure (if not already logged in)
echo "📝 Checking Azure login..."
az account show || az login

# 2. Create Resource Group
echo "📦 Creating resource group..."
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# 3. Create Azure Container Registry
echo "🐳 Creating Azure Container Registry..."
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# 4. Build and push Docker image to ACR
echo "🔨 Building and pushing Docker image..."
az acr build \
  --registry $ACR_NAME \
  --image intervyou:latest \
  --file Dockerfile .

# 5. Create Azure Database for PostgreSQL
echo "🗄️  Creating PostgreSQL database..."
az postgres flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER_NAME \
  --location $LOCATION \
  --admin-user $DB_ADMIN_USER \
  --admin-password $DB_ADMIN_PASSWORD \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 15 \
  --storage-size 32 \
  --public-access 0.0.0.0-255.255.255.255

# Create database
az postgres flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER_NAME \
  --database-name $DB_NAME

# 6. Create Storage Account
echo "💾 Creating storage account..."
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS

# Create blob containers
STORAGE_KEY=$(az storage account keys list \
  --resource-group $RESOURCE_GROUP \
  --account-name $STORAGE_ACCOUNT \
  --query '[0].value' -o tsv)

az storage container create --name uploads --account-name $STORAGE_ACCOUNT --account-key $STORAGE_KEY
az storage container create --name audio --account-name $STORAGE_ACCOUNT --account-key $STORAGE_KEY
az storage container create --name static-uploads --account-name $STORAGE_ACCOUNT --account-key $STORAGE_KEY

# 7. Create Container Apps Environment
echo "🌍 Creating Container Apps environment..."
az containerapp env create \
  --name $CONTAINER_APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# 8. Get ACR credentials
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

# 9. Build DATABASE_URL
DB_HOST="${DB_SERVER_NAME}.postgres.database.azure.com"
DATABASE_URL="postgresql://${DB_ADMIN_USER}:${DB_ADMIN_PASSWORD}@${DB_HOST}:5432/${DB_NAME}?sslmode=require"

echo "⚙️  Please set your environment secrets now..."
echo "You'll need to provide:"
echo "  - SECRET_KEY"
echo "  - OPENAI_API_KEY"
echo "  - MAIL_USERNAME"
echo "  - MAIL_PASSWORD"
echo "  - GOOGLE_CLIENT_ID"
echo "  - GOOGLE_CLIENT_SECRET"
echo ""
read -p "Press enter when ready to continue..."

# 10. Create Container App
echo "🚢 Deploying container app..."
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image "${ACR_LOGIN_SERVER}/intervyou:latest" \
  --registry-server $ACR_LOGIN_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8000 \
  --ingress external \
  --cpu 1.0 \
  --memory 2Gi \
  --min-replicas 1 \
  --max-replicas 3 \
  --env-vars \
    DATABASE_URL="$DATABASE_URL" \
    ENVIRONMENT=production \
    PORT=8000 \
    AZURE_STORAGE_ACCOUNT="$STORAGE_ACCOUNT" \
    AZURE_STORAGE_KEY="$STORAGE_KEY"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set your secrets using: az containerapp secret set"
echo "2. Update environment variables with your API keys"
echo "3. Run database migrations"
echo "4. Get your app URL:"
echo "   az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv"
echo ""
echo "🔗 Useful commands:"
echo "  View logs: az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow"
echo "  Update app: az containerapp update --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --image ${ACR_LOGIN_SERVER}/intervyou:latest"
