# View IntervYou Logs

Write-Host "Viewing IntervYou logs (Press Ctrl+C to exit)" -ForegroundColor Cyan
Write-Host ""

docker logs intervyou-app -f
