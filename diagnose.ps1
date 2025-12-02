# IntervYou Docker Diagnostics

Write-Host "🔍 IntervYou Diagnostics" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# Check 1: Container running?
Write-Host "1. Container Status:" -ForegroundColor Yellow
$container = docker ps -a --filter "name=intervyou-app" --format "{{.Status}}"
if ($container -match "Up") {
    Write-Host "   ✅ Container is running" -ForegroundColor Green
} else {
    Write-Host "   ❌ Container is not running: $container" -ForegroundColor Red
}
Write-Host ""

# Check 2: Port binding
Write-Host "2. Port Binding:" -ForegroundColor Yellow
$ports = docker ps --filter "name=intervyou-app" --format "{{.Ports}}"
if ($ports -match "8000") {
    Write-Host "   ✅ Port 8000 is bound: $ports" -ForegroundColor Green
} else {
    Write-Host "   ❌ Port 8000 not bound" -ForegroundColor Red
}
Write-Host ""

# Check 3: Recent logs
Write-Host "3. Recent Logs (last 30 lines):" -ForegroundColor Yellow
Write-Host "   ================================" -ForegroundColor Gray
docker logs intervyou-app --tail 30 2>&1
Write-Host "   ================================" -ForegroundColor Gray
Write-Host ""

# Check 4: Environment variables
Write-Host "4. Environment Check:" -ForegroundColor Yellow
$envVars = docker exec intervyou-app env 2>&1
if ($envVars -match "DATABASE_URL") {
    Write-Host "   ✅ DATABASE_URL is set" -ForegroundColor Green
} else {
    Write-Host "   ❌ DATABASE_URL not found" -ForegroundColor Red
}
if ($envVars -match "SECRET_KEY") {
    Write-Host "   ✅ SECRET_KEY is set" -ForegroundColor Green
} else {
    Write-Host "   ❌ SECRET_KEY not found" -ForegroundColor Red
}
Write-Host ""

# Check 5: Process inside container
Write-Host "5. Running Processes:" -ForegroundColor Yellow
docker exec intervyou-app ps aux 2>&1 | Select-Object -First 10
Write-Host ""

# Check 6: Health check
Write-Host "6. Health Status:" -ForegroundColor Yellow
$health = docker inspect intervyou-app --format='{{.State.Health.Status}}' 2>&1
Write-Host "   Status: $health" -ForegroundColor $(if ($health -eq "healthy") { "Green" } else { "Yellow" })
Write-Host ""

Write-Host "💡 Recommendations:" -ForegroundColor Cyan
Write-Host "   - If container keeps restarting, check logs above" -ForegroundColor White
Write-Host "   - If DATABASE_URL missing, check your .env file" -ForegroundColor White
Write-Host "   - Wait 30-60 seconds for app to fully start" -ForegroundColor White
Write-Host "   - Try: docker compose restart" -ForegroundColor White
