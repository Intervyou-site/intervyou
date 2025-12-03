# 🔑 Create Your First API Key - Step by Step

## ✅ Your System is Working!

The error `"Invalid or expired API key"` when testing with `"your_key_here"` is **correct behavior**! 
It means the authentication system is working - it's rejecting invalid keys as expected.

Now you just need to create a **real** API key.

## 📋 Step-by-Step Instructions

### Step 1: Login to Your Account

1. Open your browser
2. Go to: **http://localhost:8000/login**
3. Login with your credentials

If you don't have an account yet:
- Click "Sign Up" on the login page
- Create a new account
- Then login

### Step 2: Navigate to API Key Management

Once logged in, go to: **http://localhost:8000/api/keys/manage**

You should see a page titled "🔑 API Key Management"

### Step 3: Create a New API Key

On the API Keys page:

1. **Enter a name** for your key (e.g., "My First Key", "Testing", "Production")
2. **Optional**: Set expiration in days (leave empty for no expiration)
3. Click **"Generate API Key"** button

### Step 4: Copy Your API Key

⚠️ **IMPORTANT**: A popup will appear showing your new API key.

**This is the ONLY time you'll see the full key!**

The key will look like: `iv_xK9mP2nQ7vR4sT8wY3zA1bC5dE6fG0hJ`

- Click "Copy to Clipboard" button
- Save it somewhere safe (password manager, secure note, etc.)

### Step 5: Test Your Real API Key

Now test with your **actual** API key:

```powershell
# Replace with your actual key from Step 4
$apiKey = "iv_xK9mP2nQ7vR4sT8wY3zA1bC5dE6fG0hJ"

# Test it
Invoke-WebRequest -Uri "http://localhost:8000/api/keys/test" -Headers @{"X-API-Key"=$apiKey}
```

Or use the test script:
```powershell
.\test-api-key.ps1
# Then paste your real key when prompted
```

### Expected Success Response

When you use a **valid** API key, you should see:

```json
{
  "success": true,
  "message": "Hello YourName! Your API key works.",
  "user_id": 1,
  "user_email": "your@email.com"
}
```

## 🎯 Quick Test Commands

### Test with PowerShell (after creating key)
```powershell
# Save your key
$apiKey = "iv_your_actual_key_here"

# Test it
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/keys/test" -Headers @{"X-API-Key"=$apiKey}
$data = $response.Content | ConvertFrom-Json
Write-Host "✅ Success! User: $($data.user_email)"
```

### Test with Python
```python
import requests

API_KEY = "iv_your_actual_key_here"
response = requests.get(
    "http://localhost:8000/api/keys/test",
    headers={"X-API-Key": API_KEY}
)
print(response.json())
```

## 🔍 Troubleshooting

### "Invalid or expired API key" Error

This means:
- ✅ Your authentication system is working correctly
- ❌ The key you're using is not valid

**Solutions:**
1. Make sure you're using a **real** key (not the example "your_key_here")
2. Check you copied the **entire** key (starts with `iv_`)
3. Verify the key hasn't been revoked
4. Create a new key if you lost the original

### Can't Access /api/keys/manage

**Error**: Redirects to login page

**Solution**: You need to login first at http://localhost:8000/login

### Page Shows "Not Found"

**Solution**: Make sure your server is running:
```powershell
python start.py
```

## 📊 What You Should See

### 1. Login Page
- Email and password fields
- "Sign in with Google" option
- "Sign Up" link if you need to register

### 2. API Keys Management Page
After login, you'll see:
- "Create New API Key" section with form
- List of your existing API keys (empty at first)
- Each key shows: name, prefix, created date, status

### 3. After Creating a Key
- Popup modal with your new API key
- Warning: "Save this key now! It won't be shown again."
- Copy button to copy the key
- The key will be added to your list (but only showing prefix)

## ✅ Success Checklist

- [ ] Server is running (`python start.py`)
- [ ] You have an account and are logged in
- [ ] You visited `/api/keys/manage`
- [ ] You created a new API key
- [ ] You copied the full key (starts with `iv_`)
- [ ] You tested it and got a success response

## 🎉 Next Steps

Once you have a working API key:

1. **Use it in your applications** - See `example_protected_endpoints.py`
2. **Create more keys** - Different keys for different purposes
3. **Manage your keys** - View usage, revoke old keys
4. **Read the guides** - `WINDOWS_API_KEY_GUIDE.md` for more examples

## 💡 Pro Tips

1. **Name your keys descriptively**: "Production Server", "Mobile App", "Testing"
2. **Use different keys for different environments**: Dev, staging, production
3. **Set expiration dates** for temporary access
4. **Revoke unused keys** regularly for security
5. **Never commit keys to git** - use environment variables

---

**Need help?** Check the other guides:
- `WINDOWS_API_KEY_GUIDE.md` - Windows-specific commands
- `API_KEYS_GUIDE.md` - Complete documentation
- `API_KEYS_QUICK_START.md` - Quick reference
