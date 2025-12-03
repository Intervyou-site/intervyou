# 🪟 API Keys - Windows Guide

## Quick Setup

### 1. Start Your Server
```powershell
python start.py
```

### 2. Create an API Key
1. Open browser: http://localhost:8000/login
2. Login to your account
3. Go to: http://localhost:8000/api/keys/manage
4. Click "Generate API Key"
5. **Copy the key immediately** (starts with `iv_`)

### 3. Test Your API Key

#### Option A: Use the PowerShell Test Script
```powershell
.\test-api-key.ps1
```

#### Option B: Manual PowerShell Command
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/keys/test" -Headers @{"X-API-Key"="iv_your_key_here"}
```

#### Option C: Short Version
```powershell
iwr -Uri "http://localhost:8000/api/keys/test" -Headers @{"X-API-Key"="iv_your_key_here"}
```

## Common PowerShell Commands

### Test API Key
```powershell
$apiKey = "iv_your_key_here"
$headers = @{"X-API-Key" = $apiKey}
Invoke-WebRequest -Uri "http://localhost:8000/api/keys/test" -Headers $headers
```

### Get Response as JSON
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/keys/test" -Headers @{"X-API-Key"="iv_your_key_here"}
$data = $response.Content | ConvertFrom-Json
$data
```

### Save API Key in Variable
```powershell
# Save your key
$apiKey = "iv_your_actual_key_here"

# Use it in requests
$headers = @{"X-API-Key" = $apiKey}
Invoke-WebRequest -Uri "http://localhost:8000/api/keys/test" -Headers $headers
```

## Using API Keys in Python (Windows)

```python
import requests

API_KEY = "iv_your_key_here"
BASE_URL = "http://localhost:8000"

headers = {"X-API-Key": API_KEY}

# Test the key
response = requests.get(f"{BASE_URL}/api/keys/test", headers=headers)
print(response.json())
```

## Using API Keys in JavaScript

```javascript
const API_KEY = 'iv_your_key_here';
const BASE_URL = 'http://localhost:8000';

fetch(`${BASE_URL}/api/keys/test`, {
    headers: {
        'X-API-Key': API_KEY
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## Troubleshooting

### Error: "Cannot bind parameter 'Headers'"
❌ **Wrong:**
```powershell
curl -H "X-API-Key: your_key" http://localhost:8000/api/keys/test
```

✅ **Correct:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/keys/test" -Headers @{"X-API-Key"="your_key"}
```

### Error: "404 Not Found"
- Make sure your server is running: `python start.py`
- Check the URL is correct: `http://localhost:8000/api/keys/test`
- Verify the routes are loaded (check server startup logs)

### Error: "401 Unauthorized"
- Check your API key is correct
- Make sure the key hasn't been revoked
- Verify the key hasn't expired
- Ensure you're including the full key (starts with `iv_`)

### Server Not Starting
```powershell
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# Kill process if needed (replace PID with actual process ID)
taskkill /PID <PID> /F
```

## Complete Example Script

Save this as `test-my-api.ps1`:

```powershell
# Configuration
$API_KEY = "iv_your_key_here"  # Replace with your actual key
$BASE_URL = "http://localhost:8000"

# Create headers
$headers = @{
    "X-API-Key" = $API_KEY
}

Write-Host "Testing API Key..." -ForegroundColor Cyan

try {
    # Test the API key
    $response = Invoke-WebRequest -Uri "$BASE_URL/api/keys/test" -Headers $headers
    $data = $response.Content | ConvertFrom-Json
    
    Write-Host "✅ Success!" -ForegroundColor Green
    Write-Host "User: $($data.user_email)" -ForegroundColor Yellow
    Write-Host "Message: $($data.message)" -ForegroundColor Yellow
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}
```

Run it:
```powershell
.\test-my-api.ps1
```

## Next Steps

- Read the full guide: `API_KEYS_GUIDE.md`
- See code examples: `example_protected_endpoints.py`
- Check quick reference: `API_KEYS_QUICK_START.md`
