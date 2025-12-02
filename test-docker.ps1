# Quick Docker Test Script

Write-Host "🐳 Testing Docker Installation..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Docker command
Write-Host "Test 1: Docker command..." -ForegroundColor Yellow
try {
    $version = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $version" -ForegroundColor Green
    } else {
        throw "Docker command failed"
    }
} catch {
    Write-Host "❌ Docker command not found!" -ForegroundColor Red
    Write-Host "   Please restart PowerShell and try again" -ForegroundColor Yellow
    exit 1
}

# Test 2: Docker Compose
Write-Host "Test 2: Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker compose version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $composeVersion" -ForegroundColor Green
    } else {
        throw "Docker Compose failed"
    }
} catch {
    Write-Host "❌ Docker Compose not available!" -ForegroundColor Red
    exit 1
}

# Test 3: Docker daemon
Write-Host "Test 3: Docker daemon..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker daemon is running" -ForegroundColor Green
    } else {
        throw "Docker daemon not running"
    }
} catch {
    Write-Host "❌ Docker daemon is not running!" -ForegroundColor Red
    Write-Host "   Please start Docker Desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🎉 All tests passed! Docker is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Next step: Run .\docker-start.ps1 to start your app" -ForegroundColor Cyan
