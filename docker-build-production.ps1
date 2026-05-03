# IntervYou Docker Build Script for Production
# This script builds and runs the IntervYou Docker container

param(
    [switch]$NoBuild,
    [switch]$Clean,
    [switch]$Logs
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  IntervYou Docker Build & Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "[1/5] Checking Docker..." -ForegroundColor Yellow
$dockerRunning = docker info 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] Docker is running" -ForegroundColor Green
Write-Host ""

# Check if .env file exists
Write-Host "[2/5] Checking environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "WARNING: .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "[OK] .env file created" -ForegroundColor Green
        Write-Host "IMPORTANT: Edit .env and add your API keys before continuing!" -ForegroundColor Red
        $continue = Read-Host "Continue anyway? (yes/no)"
        if ($continue -ne "yes") {
            exit 0
        }
    } else {
        Write-Host "ERROR: .env.example not found!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[OK] .env file exists" -ForegroundColor Green
}
Write-Host ""

# Clean up old containers if requested
if ($Clean) {
    Write-Host "[3/5] Cleaning up old containers..." -ForegroundColor Yellow
    docker-compose -f docker-compose.production.yml down -v 2>&1 | Out-Null
    docker rmi intervyou:latest 2>&1 | Out-Null
    Write-Host "[OK] Cleanup complete" -ForegroundColor Green
    Write-Host ""
}

# Build Docker image
if (-not $NoBuild) {
    Write-Host "[3/5] Building Docker image..." -ForegroundColor Yellow
    Write-Host "This may take 5-10 minutes on first build..." -ForegroundColor Cyan
    
    docker-compose -f docker-compose.production.yml build
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Docker build failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Docker image built successfully" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[3/5] Skipping build (using existing image)" -ForegroundColor Yellow
    Write-Host ""
}

# Start containers
Write-Host "[4/5] Starting containers..." -ForegroundColor Yellow
docker-compose -f docker-compose.production.yml up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to start containers!" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Containers started" -ForegroundColor Green
Write-Host ""

# Wait for application to be ready
Write-Host "[5/5] Waiting for application to be ready..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$ready = $false

while ($attempt -lt $maxAttempts -and -not $ready) {
    $attempt++
    Write-Host "  Attempt $attempt/$maxAttempts..." -ForegroundColor Cyan
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $ready = $true
        }
    } catch {
        Start-Sleep -Seconds 2
    }
}

Write-Host ""
if ($ready) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  SUCCESS! IntervYou is running!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Application URL: http://localhost:8000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Yellow
    Write-Host "  View logs:    docker-compose -f docker-compose.production.yml logs -f" -ForegroundColor White
    Write-Host "  Stop:         docker-compose -f docker-compose.production.yml down" -ForegroundColor White
    Write-Host "  Restart:      docker-compose -f docker-compose.production.yml restart" -ForegroundColor White
    Write-Host "  Status:       docker-compose -f docker-compose.production.yml ps" -ForegroundColor White
    Write-Host ""
    
    if ($Logs) {
        Write-Host "Showing logs (Ctrl+C to exit)..." -ForegroundColor Yellow
        docker-compose -f docker-compose.production.yml logs -f
    }
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  WARNING: Application may not be ready" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check logs with:" -ForegroundColor Yellow
    Write-Host "  docker-compose -f docker-compose.production.yml logs -f" -ForegroundColor White
    Write-Host ""
}
