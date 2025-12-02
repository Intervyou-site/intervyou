# IntervYou Docker Startup Script
# Run this in a NEW PowerShell window after Docker Desktop is running

Write-Host "🐳 IntervYou Docker Startup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found! Please:" -ForegroundColor Red
    Write-Host "   1. Make sure Docker Desktop is running" -ForegroundColor Red
    Write-Host "   2. Restart PowerShell" -ForegroundColor Red
    Write-Host "   3. Run this script again" -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env created. Please edit it with your configuration." -ForegroundColor Green
    Write-Host ""
    Write-Host "Press any key to open .env file..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    notepad .env
    Write-Host ""
    Write-Host "After editing .env, run this script again." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build -t intervyou:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build successful!" -ForegroundColor Green
Write-Host ""

Write-Host "Starting containers..." -ForegroundColor Yellow
docker compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start containers!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ IntervYou is running!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access your app at: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  View logs:        docker compose logs -f" -ForegroundColor White
Write-Host "  Stop app:         docker compose down" -ForegroundColor White
Write-Host "  Restart app:      docker compose restart" -ForegroundColor White
Write-Host "  View status:      docker compose ps" -ForegroundColor White
Write-Host ""

# Wait a few seconds and check if container is running
Start-Sleep -Seconds 3
Write-Host "Checking container status..." -ForegroundColor Yellow
docker compose ps

Write-Host ""
Write-Host "Opening browser in 5 seconds..." -ForegroundColor Cyan
Start-Sleep -Seconds 5
Start-Process "http://localhost:8000"
