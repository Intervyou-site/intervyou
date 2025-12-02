# IntervYou Docker Stop Script

Write-Host "🛑 Stopping IntervYou..." -ForegroundColor Yellow

docker compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ IntervYou stopped successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to stop containers!" -ForegroundColor Red
    exit 1
}
