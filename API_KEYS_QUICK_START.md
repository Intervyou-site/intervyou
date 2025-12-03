# 🚀 API Keys - Quick Start

## What You Got

A complete API key authentication system for your web app!

## Setup (One Time)

```bash
# 1. Migration already done ✅
python migrate_api_keys.py

# 2. Start your server
python start.py
```

## Create Your First API Key

1. **Login** → http://localhost:8000/login
2. **Go to API Keys** → http://localhost:8000/api/keys/manage
3. **Click "Generate API Key"**
4. **Copy the key** (starts with `iv_`) - you won't see it again!

## Use Your API Key

### PowerShell (Windows)
```powershell
# Method 1: Using Invoke-WebRequest
Invoke-WebRequest -Uri "http://localhost:8000/api/keys/test" -Headers @{"X-API-Key"="iv_your_key_here"}

# Method 2: Using the test script
.\test-api-key.ps1
```

### cURL (Linux/Mac)
```bash
curl -H "X-API-Key: iv_your_key_here" \
     http://localhost:8000/api/keys/test
```

### Python
```python
import requests

headers = {"X-API-Key": "iv_your_key_here"}
response = requests.get("http://localhost:8000/api/keys/test", headers=headers)
print(response.json())
```

### JavaScript
```javascript
fetch('http://localhost:8000/api/keys/test', {
    headers: {'X-API-Key': 'iv_your_key_here'}
})
.then(r => r.json())
.then(console.log);
```

## Protect Your Own Endpoints

```python
from fastapi import APIRouter, Depends
from api_key_system import get_current_user_from_api_key

router = APIRouter()

@router.get("/api/my-endpoint")
async def my_endpoint(user = Depends(get_current_user_from_api_key)):
    return {"message": f"Hello {user.name}!"}
```

## Files Created

- `api_key_system.py` - Core API key logic
- `api_key_routes.py` - API endpoints
- `templates/api_keys.html` - Management UI
- `migrate_api_keys.py` - Database setup
- `API_KEYS_GUIDE.md` - Full documentation

## Key Features

✅ Secure key generation (cryptographically random)
✅ Hashed storage (keys never stored in plain text)
✅ Web UI for management
✅ Optional expiration dates
✅ Usage tracking
✅ Easy revocation
✅ Ready to use in your API

## Need Help?

Read the full guide: `API_KEYS_GUIDE.md`
