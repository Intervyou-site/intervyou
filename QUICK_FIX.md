# Quick Fix for Database Connection Issue

## Problem
Your Docker container can't connect to Supabase database due to IPv6 network issue.

## Solution

### Step 1: Restart with New Configuration

Open PowerShell in project directory and run:

```powershell
.\restart-app.ps1
```

This will:
1. Stop the current container
2. Start with new DNS settings (Google DNS 8.8.8.8)
3. Wait 30 seconds
4. Show you the logs

### Step 2: Check if It's Working

After 30 seconds, open browser:
```
http://localhost:8000
```

### Step 3: View Logs (if needed)

```powershell
.\view-logs.ps1
```

Look for:
- ✅ "Uvicorn running on http://0.0.0.0:8000" = GOOD
- ❌ "Network is unreachable" = Still has issues

---

## Alternative: Use Local Database

If Supabase connection keeps failing, you can use a local PostgreSQL:

### Option A: Add PostgreSQL to Docker Compose

I can add a PostgreSQL container to your docker-compose.yml

### Option B: Use SQLite for Testing

Edit `.env`:
```env
DATABASE_URL=sqlite:///./database.db
```

Then restart:
```powershell
.\restart-app.ps1
```

---

## Manual Commands

If scripts don't work:

```powershell
# Stop
docker compose down

# Start
docker compose up -d

# View logs
docker logs intervyou-app -f

# Check status
docker ps

# Restart
docker compose restart
```

---

## What Changed

1. Added Google DNS (8.8.8.8) to docker-compose.yml
2. This forces IPv4 resolution for Supabase
3. Should fix "Network is unreachable" error

---

## Next Steps

1. Run `.\restart-app.ps1`
2. Wait 30 seconds
3. Try http://localhost:8000
4. If still not working, let me know and I'll add local PostgreSQL
