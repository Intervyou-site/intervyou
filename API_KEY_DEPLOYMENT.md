# 🚀 API Key System - Deployment Guide

## ✅ Changes Committed to Git

The API key system has been successfully committed and pushed to your repository:

```
Commit: Add API key authentication system with management UI and documentation
Files: 13 files changed, 1606 insertions(+)
```

## 📦 What Was Added

### Core Files
- `api_key_system.py` - API key generation, verification, and management
- `api_key_routes.py` - FastAPI routes for API key management
- `fastapi_app.py` - Updated with APIKey model
- `migrate_api_keys.py` - Database migration script
- `templates/api_keys.html` - Web UI for managing keys

### Documentation
- `API_KEYS_GUIDE.md` - Complete documentation
- `API_KEYS_QUICK_START.md` - Quick reference
- `WINDOWS_API_KEY_GUIDE.md` - Windows-specific commands
- `API_KEY_SETUP_COMPLETE.md` - Setup summary
- `API_KEY_STATUS.md` - System status
- `CREATE_YOUR_FIRST_API_KEY.md` - Step-by-step guide
- `API_KEY_SYSTEM_SUMMARY.md` - Feature summary

### Examples & Tests
- `example_protected_endpoints.py` - Code examples
- `test-api-key.ps1` - PowerShell test script

## 🐳 Docker Deployment

### 1. Database Migration

The API keys table needs to be created in your production database. You have two options:

#### Option A: Run Migration Script (Recommended)
```bash
# SSH into your production server or container
python migrate_api_keys.py
```

#### Option B: Manual SQL (if needed)
```sql
-- For PostgreSQL (Supabase)
CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    key_name VARCHAR(100) NOT NULL,
    key_hash VARCHAR(128) NOT NULL UNIQUE,
    key_prefix VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);
```

### 2. Rebuild Docker Image

Your Dockerfile already includes all necessary files. Just rebuild:

```bash
# Build new image
docker build -t intervyou:latest .

# Or if using docker-compose
docker-compose build
```

### 3. Deploy to Production

#### Local Docker
```bash
docker-compose down
docker-compose up -d
```

#### Azure Container Apps
```bash
# If using Azure
az acr build --registry <your-registry> --image intervyou:latest .
az containerapp update --name intervyou --resource-group <your-rg> --image <your-registry>.azurecr.io/intervyou:latest
```

### 4. Run Migration in Production

After deploying, run the migration:

```bash
# If using docker-compose
docker-compose exec web python migrate_api_keys.py

# If using Azure Container Apps
az containerapp exec --name intervyou --resource-group <your-rg> --command "python migrate_api_keys.py"
```

## 🔧 Environment Variables

No new environment variables are required! The API key system uses your existing:
- `DATABASE_URL` - For storing API keys
- `SECRET_KEY` - For session management

## ✅ Verification Checklist

After deployment, verify:

- [ ] Server starts without errors
- [ ] Can access `/api/keys/manage` (redirects to login if not authenticated)
- [ ] Can login and see API key management page
- [ ] Can create a new API key
- [ ] Can test API key with `/api/keys/test` endpoint
- [ ] Can revoke API keys

## 🧪 Testing in Production

### 1. Create an API Key
1. Login to your production site
2. Visit `https://your-domain.com/api/keys/manage`
3. Create a test API key

### 2. Test the Key
```bash
# Test with curl
curl -H "X-API-Key: your_key_here" https://your-domain.com/api/keys/test

# Expected response:
# {"success": true, "message": "Hello YourName! Your API key works.", ...}
```

### 3. Test with PowerShell
```powershell
Invoke-WebRequest -Uri "https://your-domain.com/api/keys/test" -Headers @{"X-API-Key"="your_key_here"}
```

## 📊 Monitoring

Check your application logs for:
- API key creation events
- Authentication attempts
- Failed authentication (invalid keys)

## 🔒 Security Notes

✅ **Already Implemented:**
- Keys are hashed with SHA-256 (never stored in plain text)
- Keys are only shown once at creation
- Keys can be instantly revoked
- Usage tracking (last used timestamp)
- Per-user limits (max 10 active keys)

🔐 **Additional Security (Optional):**
- Add rate limiting per API key
- Add IP whitelisting
- Add key scopes/permissions
- Set up alerts for suspicious activity

## 🆘 Troubleshooting

### Migration Fails
```bash
# Check if table already exists
# Connect to your database and run:
SELECT * FROM api_keys LIMIT 1;

# If table exists, migration is already done
```

### Can't Access Management Page
- Clear browser cache
- Try incognito/private window
- Check server logs for errors
- Verify you're logged in

### API Key Not Working
- Verify key is active (not revoked)
- Check key hasn't expired
- Ensure you're including the full key (starts with `iv_`)
- Check the `X-API-Key` header is set correctly

## 📚 Documentation Links

- **Quick Start**: `API_KEYS_QUICK_START.md`
- **Full Guide**: `API_KEYS_GUIDE.md`
- **Windows Guide**: `WINDOWS_API_KEY_GUIDE.md`
- **Examples**: `example_protected_endpoints.py`

## 🎉 Summary

✅ Code committed to Git
✅ Pushed to GitHub
✅ Docker-ready (no Dockerfile changes needed)
✅ Migration script ready
✅ Documentation complete

**Next Steps:**
1. Rebuild Docker image
2. Deploy to production
3. Run migration script
4. Test API key creation and usage

Your API key system is production-ready! 🚀
