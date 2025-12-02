# Quick Fix for Database Connection Issue

## Problem
Your Docker container can't connect to Supabase database due to IPv6 network issue.

## ✅ SOLUTION: Use Local PostgreSQL Database

I've added a local PostgreSQL database to your Docker setup!

### Run This Command:

```powershell
.\start-with-local-db.ps1
```

This will:
1. ✅ Stop existing containers
2. ✅ Start PostgreSQL database (local)
3. ✅ Start IntervYou app
4. ✅ Initialize database tables
5. ✅ Open your browser automatically

### What Changed:

- Added PostgreSQL 15 container to docker-compose.yml
- Database runs locally (no internet needed)
- Data persists in Docker volume
- Automatic health checks

---

## Access Your App

After running the script, open:
```
http://localhost:8000
```

---

## Database Info

**Local PostgreSQL:**
- Host: localhost:5432
- Database: intervyou
- User: intervyou
- Password: intervyou123

**Connect with psql:**
```powershell
docker exec -it intervyou-db psql -U intervyou
```

---

## Still Want to Use Supabase?

If you want to use Supabase instead of local database:

1. Edit `docker-compose.yml`
2. Change the DATABASE_URL back to Supabase
3. Restart: `.\restart-app.ps1`

But for local development, the local database is faster and more reliable!

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
