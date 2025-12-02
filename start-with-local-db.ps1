# Start IntervYou with Local PostgreSQL Database

Write-Host "Starting IntervYou with local PostgreSQL database..." -ForegroundColor Cyan
Write-Host ""

# Stop any existing containers
Write-Host "Stopping existing containers..." -ForegroundColor Yellow
docker compose down

# Start with local database
Write-Host "Starting PostgreSQL and IntervYou..." -ForegroundColor Yellow
docker compose up -d

Write-Host ""
Write-Host "Waiting for services to start (40 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 40

# Check status
Write-Host ""
Write-Host "Container Status:" -ForegroundColor Cyan
docker compose ps

Write-Host ""
Write-Host "Initializing database..." -ForegroundColor Yellow
docker exec intervyou-app alembic upgrade head 2>&1 | Out-Null

Write-Host ""
Write-Host "Recent logs:" -ForegroundColor Cyan
docker logs intervyou-app --tail 15

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "IntervYou is ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access your app at: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Database: PostgreSQL (local container)" -ForegroundColor Yellow
Write-Host "  Host: localhost:5432" -ForegroundColor White
Write-Host "  Database: intervyou" -ForegroundColor White
Write-Host "  User: intervyou" -ForegroundColor White
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  View logs:     docker compose logs -f" -ForegroundColor White
Write-Host "  Stop all:      docker compose down" -ForegroundColor White
Write-Host "  Restart:       docker compose restart" -ForegroundColor White
Write-Host "  DB shell:      docker exec -it intervyou-db psql -U intervyou" -ForegroundColor White
Write-Host ""

# Try to open browser
Start-Sleep -Seconds 2
Start-Process "http://localhost:8000"
