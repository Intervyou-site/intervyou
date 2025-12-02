# 🔧 IntervYou Docker Troubleshooting

## Issue: "This site can't be reached" or "Connection Refused"

This is normal! The app takes 30-60 seconds to start. Here's what to do:

### Quick Fix

**Option 1: Wait and Check**
```powershell
.\wait-for-app.ps1
```
This will automatically wait for the app to be ready and open your browser.

**Option 2: Run Diagnostics**
```powershell
.\diagnose.ps1
```
This will show you exactly what's happening.

**Option 3: Check Logs**
```powershell
.\check-status.ps1
```
View the container logs to see startup progress.

---

## Common Issues & Solutions

### 1. App is Still Starting

**Symptoms:**
- Browser shows "Connection refused"
- Container status shows "Up" but "health: starting"

**Solution:**
```powershell
# Wait 30-60 seconds, then try again
.\wait-for-app.ps1

# Or manually check:
docker logs intervyou-app -f
```

**What to look for in logs:**
- ✅ Good: "Uvicorn running on http://0.0.0.0:8000"
- ✅ Good: "Application startup complete"
- ❌ Bad: Python errors or tracebacks

---

### 2. Database Connection Error

**Symptoms:**
- Logs show "could not connect to server"
- Logs show "password authentication failed"

**Solution:**
```powershell
# Check if DATABASE_URL is set correctly
docker exec intervyou-app env | findstr DATABASE_URL

# If missing or wrong, update .env file and restart:
docker compose down
docker compose up -d
```

**Verify your DATABASE_URL format:**
```
postgresql://user:password@host:5432/dbname?sslmode=require
```

---

### 3. Missing Environment Variables

**Symptoms:**
- Logs show "SECRET_KEY not set"
- Logs show "OPENAI_API_KEY not set"

**Solution:**
```powershell
# Check .env file exists
Get-Content .env

# Restart with new environment
docker compose down
docker compose up -d
```

---

### 4. Port 8000 Already in Use

**Symptoms:**
- Error: "port is already allocated"
- Can't start container

**Solution:**
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml:
# ports:
#   - "8001:8000"  # Use 8001 instead
```

---

### 5. Container Keeps Restarting

**Symptoms:**
- Container status shows "Restarting"
- App never becomes accessible

**Solution:**
```powershell
# Check logs for errors
docker logs intervyou-app --tail 100

# Common causes:
# - Missing dependencies in requirements.txt
# - Python syntax errors
# - Database connection issues

# Try rebuilding:
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

### 6. Out of Memory

**Symptoms:**
- Container stops unexpectedly
- Logs show "Killed"

**Solution:**
```powershell
# Increase Docker memory in Docker Desktop:
# Settings > Resources > Memory > Increase to 4GB+

# Or limit in docker-compose.yml:
# deploy:
#   resources:
#     limits:
#       memory: 2G
```

---

### 7. File Permission Errors

**Symptoms:**
- Logs show "Permission denied"
- Can't write to uploads folder

**Solution:**
```powershell
# Fix permissions
docker exec -u root intervyou-app chmod -R 755 /app/uploads /app/static

# Or rebuild:
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## Diagnostic Commands

### Check Container Status
```powershell
docker ps -a
```

### View Logs (Live)
```powershell
docker logs intervyou-app -f
```

### View Last 50 Lines
```powershell
docker logs intervyou-app --tail 50
```

### Check Environment Variables
```powershell
docker exec intervyou-app env
```

### Access Container Shell
```powershell
docker exec -it intervyou-app bash
```

### Check Running Processes
```powershell
docker exec intervyou-app ps aux
```

### Test Database Connection
```powershell
docker exec intervyou-app python -c "from sqlalchemy import create_engine; import os; engine = create_engine(os.getenv('DATABASE_URL')); print('Connected!' if engine.connect() else 'Failed')"
```

---

## Complete Reset

If nothing works, do a complete reset:

```powershell
# Stop and remove everything
docker compose down -v

# Remove images
docker rmi intervyou:latest aipoweredinterviewcoach-web

# Clean Docker system
docker system prune -a

# Rebuild from scratch
docker compose build --no-cache
docker compose up -d

# Wait for startup
.\wait-for-app.ps1
```

---

## Still Not Working?

### 1. Check Docker Desktop
- Make sure Docker Desktop is running
- Check for updates
- Restart Docker Desktop

### 2. Check System Resources
```powershell
# Check Docker stats
docker stats intervyou-app

# Should show reasonable CPU/Memory usage
```

### 3. Try Without Docker
```powershell
# Install dependencies locally
pip install -r requirements.txt

# Run directly
python -m uvicorn fastapi_app:app --reload --port 8000
```

### 4. Check Firewall
- Windows Firewall might be blocking port 8000
- Add exception for Docker Desktop
- Try accessing: http://127.0.0.1:8000

---

## Success Indicators

When everything is working, you should see:

**Container Status:**
```
STATUS: Up X seconds (healthy)
PORTS: 0.0.0.0:8000->8000/tcp
```

**Logs:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Browser:**
- http://localhost:8000 loads the IntervYou homepage
- No connection errors

---

## Quick Reference

| Problem | Command |
|---------|---------|
| Wait for app | `.\wait-for-app.ps1` |
| Check status | `.\diagnose.ps1` |
| View logs | `.\check-status.ps1` |
| Restart | `docker compose restart` |
| Stop | `docker compose down` |
| Rebuild | `docker compose build --no-cache` |
| Full reset | `docker compose down -v && docker compose up -d --build` |

---

## Need More Help?

1. Run diagnostics: `.\diagnose.ps1`
2. Check logs: `docker logs intervyou-app --tail 100`
3. Look for error messages (usually in red)
4. Check the specific error section above

Most issues are resolved by:
- ✅ Waiting 30-60 seconds for startup
- ✅ Checking .env file is correct
- ✅ Restarting: `docker compose restart`
