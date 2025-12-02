# Wait for IntervYou to be ready

Write-Host "⏳ Waiting for IntervYou to start..." -ForegroundColor Cyan
Write-Host ""

$maxAttempts = 30
$attempt = 0
$url = "http://localhost:8000"

while ($attempt -lt $maxAttempts) {
    $attempt++
    Write-Host "Attempt $attempt/$maxAttempts..." -ForegroundColor Yellow
    
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host ""
            Write-Host "✅ IntervYou is ready!" -ForegroundColor Green
            Write-Host "🌐 Opening browser..." -ForegroundColor Cyan
            Start-Process $url
            exit 0
        }
    } catch {
        # Connection refused or timeout - app still starting
        Start-Sleep -Seconds 2
    }
}

Write-Host ""
Write-Host "❌ App didn't start in time. Checking logs..." -ForegroundColor Red
Write-Host ""
docker logs intervyou-app --tail 50
Write-Host ""
Write-Host "💡 Try running: .\diagnose.ps1" -ForegroundColor Yellow
