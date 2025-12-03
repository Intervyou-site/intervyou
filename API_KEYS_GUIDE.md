# 🔑 API Key System - Complete Guide

## Overview

Your web app now has a complete API key management system that allows users to:
- Generate secure API keys
- Use API keys to authenticate API requests
- Manage and revoke keys
- Track key usage

## Setup

### 1. Run the Migration

First, create the API keys table in your database:

```bash
python migrate_api_keys.py
```

### 2. Start Your Server

```bash
python start.py
```

## Using the API Key System

### For Users (Web Interface)

1. **Login to your account**
   - Go to `http://localhost:8000/login`

2. **Navigate to API Keys page**
   - Visit `http://localhost:8000/api/keys/manage`

3. **Create a new API key**
   - Enter a name (e.g., "Production Server", "Mobile App")
   - Optionally set expiration (in days)
   - Click "Generate API Key"
   - **IMPORTANT**: Copy the key immediately - it won't be shown again!

4. **Manage your keys**
   - View all your keys
   - See when they were last used
   - Revoke keys you no longer need

### For Developers (API Usage)

#### Authentication with API Key

Include your API key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: iv_your_api_key_here" \
     http://localhost:8000/api/keys/test
```

#### Example: Python Requests

```python
import requests

API_KEY = "iv_your_api_key_here"
BASE_URL = "http://localhost:8000"

headers = {
    "X-API-Key": API_KEY
}

# Test the API key
response = requests.get(f"{BASE_URL}/api/keys/test", headers=headers)
print(response.json())
# Output: {"success": true, "message": "Hello John! Your API key works.", ...}
```

#### Example: JavaScript/Fetch

```javascript
const API_KEY = 'iv_your_api_key_here';
const BASE_URL = 'http://localhost:8000';

fetch(`${BASE_URL}/api/keys/test`, {
    headers: {
        'X-API-Key': API_KEY
    }
})
.then(response => response.json())
.then(data => console.log(data));
```

## Creating Protected API Endpoints

### Method 1: Using the Dependency

```python
from fastapi import APIRouter, Depends
from api_key_system import get_current_user_from_api_key
from fastapi_app import User

router = APIRouter()

@router.get("/api/my-protected-endpoint")
async def my_endpoint(user: User = Depends(get_current_user_from_api_key)):
    """This endpoint requires a valid API key"""
    return {
        "message": f"Hello {user.name}!",
        "user_id": user.id,
        "data": "your protected data here"
    }
```

### Method 2: Manual Verification

```python
from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from api_key_system import verify_api_key
from fastapi_app import get_db

router = APIRouter()

@router.get("/api/another-endpoint")
async def another_endpoint(
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    """Manual API key verification"""
    user = verify_api_key(x_api_key, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return {"message": "Success", "user": user.name}
```

## API Endpoints Reference

### Web UI Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/keys/manage` | GET | API key management page (requires login) |

### API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/keys/create` | POST | Session | Create new API key |
| `/api/keys/list` | GET | Session | List user's API keys |
| `/api/keys/revoke` | POST | Session | Revoke an API key |
| `/api/keys/test` | GET | API Key | Test API key authentication |

## Security Features

✅ **Secure Key Generation**: Uses `secrets.token_urlsafe()` for cryptographically secure random keys

✅ **Hashed Storage**: API keys are hashed with SHA-256 before storage (never stored in plain text)

✅ **Key Prefixes**: First 8 characters stored for user identification without exposing full key

✅ **Expiration Support**: Optional expiration dates for temporary access

✅ **Usage Tracking**: Last used timestamp updated on each request

✅ **Revocation**: Keys can be instantly revoked

✅ **Rate Limiting Ready**: Structure supports adding rate limiting per key

## Example: Complete API Integration

Here's a complete example of using your API:

```python
import requests
import json

class InterVyouAPI:
    def __init__(self, api_key, base_url="http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key}
    
    def test_connection(self):
        """Test if API key is valid"""
        response = requests.get(
            f"{self.base_url}/api/keys/test",
            headers=self.headers
        )
        return response.json()
    
    def submit_answer(self, question, answer):
        """Submit an interview answer"""
        response = requests.post(
            f"{self.base_url}/submit_answer",
            headers=self.headers,
            data={"question": question, "answer": answer}
        )
        return response.json()
    
    def get_question(self, category="Python"):
        """Get a new interview question"""
        response = requests.get(
            f"{self.base_url}/generate_question",
            headers=self.headers,
            params={"category": category}
        )
        return response.json()

# Usage
api = InterVyouAPI("iv_your_api_key_here")

# Test connection
print(api.test_connection())

# Get a question
question = api.get_question("Python")
print(f"Question: {question}")

# Submit answer
result = api.submit_answer(question, "My answer here...")
print(f"Score: {result['score']}")
```

## Best Practices

1. **Never commit API keys to version control**
   - Use environment variables
   - Add to `.gitignore`

2. **Use different keys for different environments**
   - Development key
   - Production key
   - Testing key

3. **Rotate keys regularly**
   - Set expiration dates
   - Create new keys periodically
   - Revoke old keys

4. **Monitor key usage**
   - Check "last used" timestamps
   - Revoke unused keys

5. **Limit key permissions** (future enhancement)
   - Consider adding scope/permissions to keys
   - Restrict what each key can access

## Troubleshooting

### "API key required" error
- Make sure you're including the `X-API-Key` header
- Check that the header name is exactly `X-API-Key` (case-sensitive)

### "Invalid or expired API key" error
- Verify the key is correct (copy-paste carefully)
- Check if the key has been revoked
- Check if the key has expired

### Key not working after creation
- Make sure you copied the full key (starts with `iv_`)
- The key is only shown once - if you lost it, create a new one

## Next Steps

You can enhance this system by adding:

- **Rate limiting** per API key
- **Scopes/permissions** for different access levels
- **Usage analytics** and quotas
- **IP whitelisting** for additional security
- **Webhook support** for key events
- **Team/organization** keys for shared access

## Support

For issues or questions, check your application logs or contact support.
