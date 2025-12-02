# Restart IntervYou Docker App

Write-Host "Stopping containers..." -ForegroundColor Yellow
docker compose down

Write-Host "Starting containers with new configuration..." -ForegroundColor Yellow
docker compose up -d

Write-Host ""
Write-Host "Waiting for app to start (30 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host ""
Write-Host "Checking status..." -ForegroundColor Yellow
docker ps --filter "name=intervyou-app"

Write-Host ""
Write-Host "Recent logs:" -ForegroundColor Yellow
docker logs intervyou-app --tail 20

Write-Host ""
Write-Host "Try accessing: http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "To view live logs: docker logs intervyou-app -f" -ForegroundColor Cyan
