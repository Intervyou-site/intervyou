# IntervYou Docker Management Script
# Quick commands to manage your Docker containers

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "restart", "logs", "status", "clean", "rebuild")]
    [string]$Action
)

$composeFile = "docker-compose.production.yml"

Write-Host ""
Write-Host "IntervYou Docker Manager" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

switch ($Action) {
    "start" {
        Write-Host "Starting containers..." -ForegroundColor Yellow
        docker-compose -f $composeFile up -d
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Containers started" -ForegroundColor Green
            Write-Host "Access at: http://localhost:8000" -ForegroundColor Cyan
        }
    }
    
    "stop" {
        Write-Host "Stopping containers..." -ForegroundColor Yellow
        docker-compose -f $composeFile down
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Containers stopped" -ForegroundColor Green
        }
    }
    
    "restart" {
        Write-Host "Restarting containers..." -ForegroundColor Yellow
        docker-compose -f $composeFile restart
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Containers restarted" -ForegroundColor Green
            Write-Host "Access at: http://localhost:8000" -ForegroundColor Cyan
        }
    }
    
    "logs" {
        Write-Host "Showing logs (Ctrl+C to exit)..." -ForegroundColor Yellow
        docker-compose -f $composeFile logs -f
    }
    
    "status" {
        Write-Host "Container status:" -ForegroundColor Yellow
        docker-compose -f $composeFile ps
        Write-Host ""
        Write-Host "Docker images:" -ForegroundColor Yellow
        docker images | Select-String "intervyou"
    }
    
    "clean" {
        Write-Host "Cleaning up containers and volumes..." -ForegroundColor Yellow
        $confirm = Read-Host "This will remove all data. Continue? (yes/no)"
        if ($confirm -eq "yes") {
            docker-compose -f $composeFile down -v
            docker rmi intervyou:latest 2>&1 | Out-Null
            Write-Host "[OK] Cleanup complete" -ForegroundColor Green
        } else {
            Write-Host "Cancelled" -ForegroundColor Yellow
        }
    }
    
    "rebuild" {
        Write-Host "Rebuilding containers..." -ForegroundColor Yellow
        docker-compose -f $composeFile down
        docker-compose -f $composeFile build --no-cache
        docker-compose -f $composeFile up -d
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Rebuild complete" -ForegroundColor Green
            Write-Host "Access at: http://localhost:8000" -ForegroundColor Cyan
        }
    }
}

Write-Host ""
