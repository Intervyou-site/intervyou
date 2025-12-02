# Check IntervYou Docker Status

Write-Host "🔍 Checking IntervYou Status..." -ForegroundColor Cyan
Write-Host ""

# Get container status
Write-Host "Container Status:" -ForegroundColor Yellow
docker ps -a --filter "name=intervyou-app" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host ""
Write-Host "Recent Logs (last 50 lines):" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Gray
docker logs intervyou-app --tail 50

Write-Host ""
Write-Host "================================" -ForegroundColor Gray
Write-Host ""
Write-Host "Commands:" -ForegroundColor Cyan
Write-Host "  View live logs:  docker logs intervyou-app -f" -ForegroundColor White
Write-Host "  Restart:         docker compose restart" -ForegroundColor White
Write-Host "  Stop:            docker compose down" -ForegroundColor White
