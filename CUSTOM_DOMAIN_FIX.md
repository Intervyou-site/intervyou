# Custom Domain 502 Bad Gateway Fix

## Problem
Custom domain `www.intervyou.site` shows "502 Bad Gateway" error while Railway default domain works fine.

## Root Cause
Railway's custom domain requires:
1. Health check endpoint to be enabled
2. Application to respond within timeout period
3. Correct port binding (Railway injects PORT env variable)

## Solution Applied

### 1. ✅ Enabled Health Check in railway.toml
```toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
```

### 2. ✅ Health Endpoint Already Exists
The app has a working health endpoint at `/health` that returns:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-03T...",
  "version": "2.0.0"
}
```

### 3. ✅ Port Binding is Correct
Dockerfile uses Railway's PORT environment variable:
```dockerfile
CMD ["sh", "-c", "python -m gunicorn fastapi_app_cleaned:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000} --timeout 120"]
```

## Steps to Fix

### Step 1: Commit and Push Changes
```bash
git add railway.toml
git commit -m "Enable health check for custom domain"
git push origin main
```

### Step 2: Wait for Railway Deployment
- Railway will automatically redeploy with the new configuration
- Check deployment logs in Railway dashboard
- Wait for "Deployment successful" message

### Step 3: Verify Health Check
Once deployed, test the health endpoint:
```bash
curl https://intervyou-production-5a2d.up.railway.app/health
```

Should return:
```json
{"status":"healthy","timestamp":"...","version":"2.0.0"}
```

### Step 4: Test Custom Domain
After successful deployment, test your custom domain:
```bash
curl https://www.intervyou.site/health
```

### Step 5: Clear DNS Cache (if needed)
If still not working after deployment:

**Windows:**
```powershell
ipconfig /flushdns
```

**Mac/Linux:**
```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

## Additional Troubleshooting

### Check Railway Logs
1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click on latest deployment
5. Check logs for errors

### Common Issues

#### Issue 1: Application Not Starting
**Symptoms:** Logs show startup errors
**Solution:** Check for missing environment variables or dependencies

#### Issue 2: Health Check Timeout
**Symptoms:** Logs show "Health check failed"
**Solution:** Increase `healthcheckTimeout` in railway.toml (already set to 300s)

#### Issue 3: Port Binding Error
**Symptoms:** Logs show "Address already in use"
**Solution:** Verify Dockerfile uses `${PORT}` variable (already correct)

#### Issue 4: DNS Not Propagated
**Symptoms:** Domain doesn't resolve
**Solution:** Wait 24-48 hours for DNS propagation, check DNS records

### Verify DNS Records
Check if DNS is correctly configured:
```bash
nslookup www.intervyou.site
```

Should point to Railway's proxy domain: `switchyard.proxy.rlwy.net`

### Check Railway Service Status
1. Verify service is "Active" in Railway dashboard
2. Check if custom domain shows green checkmark
3. Verify DNS records are correct (click "DNS records" in Railway)

## Expected Timeline
- **Immediate:** Code changes pushed to GitHub
- **2-5 minutes:** Railway redeploys with new configuration
- **5-10 minutes:** Health check starts working
- **10-30 minutes:** Custom domain becomes accessible
- **Up to 48 hours:** Full DNS propagation worldwide

## Verification Checklist
- [ ] railway.toml updated with health check
- [ ] Changes committed and pushed to GitHub
- [ ] Railway deployment successful
- [ ] Health endpoint returns 200 OK
- [ ] Railway default domain works
- [ ] Custom domain works
- [ ] DNS cache cleared
- [ ] Tested in incognito/private browser

## Contact Support
If issue persists after 30 minutes:
1. Check Railway status page: https://status.railway.app
2. Contact Railway support with deployment logs
3. Verify domain registrar DNS settings

## Success Indicators
✅ Railway deployment shows "Active"
✅ Health check returns `{"status":"healthy"}`
✅ Default domain loads correctly
✅ Custom domain loads correctly
✅ No 502 errors in browser
