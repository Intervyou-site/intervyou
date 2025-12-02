# IntervYou Docker Logs Viewer

Write-Host "📋 Viewing IntervYou logs..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to exit" -ForegroundColor Yellow
Write-Host ""

docker compose logs -f
