# Initialize Database for IntervYou

Write-Host "Initializing IntervYou database..." -ForegroundColor Cyan
Write-Host ""

# Wait for database to be ready
Write-Host "Waiting for PostgreSQL to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Run Alembic migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
docker exec intervyou-app alembic upgrade head

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Database initialized successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Database initialization failed. Check logs:" -ForegroundColor Red
    Write-Host "  docker logs intervyou-app" -ForegroundColor Yellow
}
