# IntervYou Docker Management Script
# Complete Docker management for the cleaned FastAPI application

param(
    [Parameter(Position=0)]
    [ValidateSet("build", "start", "stop", "restart", "logs", "cleanup", "status", "help")]
    [string]$Action = "help",
    
    [switch]$Force,
    [switch]$Follow
)

$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
$Blue = "Cyan"
$Magenta = "Magenta"

function Write-Status {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Blue
}

function Write-Success {
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

function Write-Header {
    param($Message)
    Write-Host ""
    Write-Host "🚀 $Message" -ForegroundColor $Magenta
    Write-Host ("=" * ($Message.Length + 3)) -ForegroundColor $Magenta
}

function Show-Help {
    Write-Header "IntervYou Docker Management"
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor $Yellow
    Write-Host "  .\manage-docker.ps1 <action> [options]"
    Write-Host ""
    Write-Host "ACTIONS:" -ForegroundColor $Yellow
    Write-Host "  build     - Build the cleaned IntervYou application"
    Write-Host "  start     - Start the application services"
    Write-Host "  stop      - Stop all services"
    Write-Host "  restart   - Restart all services"
    Write-Host "  logs      - Show application logs"
    Write-Host "  cleanup   - Clean up old Docker images"
    Write-Host "  status    - Show current status"
    Write-Host "  help      - Show this help message"
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor $Yellow
    Write-Host "  -Force    - Skip confirmations"
    Write-Host "  -Follow   - Follow logs in real-time (for logs action)"
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor $Yellow
    Write-Host "  .\manage-docker.ps1 build"
    Write-Host "  .\manage-docker.ps1 start"
    Write-Host "  .\manage-docker.ps1 logs -Follow"
    Write-Host "  .\manage-docker.ps1 cleanup -Force"
}

function Test-DockerRunning {
    try {
        docker info | Out-Null
        return $true
    } catch {
        Write-Error "Docker is not running. Please start Docker Desktop and try again."
        return $false
    }
}

function Build-Application {
    Write-Header "Building IntervYou Application"
    
    if (-not (Test-DockerRunning)) { return }
    
    Write-Status "Stopping existing containers..."
    docker-compose down 2>$null
    
    Write-Status "Building optimized Docker image..."
    docker build -t intervyou-cleaned:latest . --no-cache
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Docker image built successfully!"
        
        Write-Status "Building with docker-compose..."
        docker-compose build --no-cache
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Application ready to start!"
            Write-Status "Use '.\manage-docker.ps1 start' to run the application"
        } else {
            Write-Error "Docker-compose build failed"
        }
    } else {
        Write-Error "Docker build failed"
    }
}

function Start-Application {
    Write-Header "Starting IntervYou Application"
    
    if (-not (Test-DockerRunning)) { return }
    
    Write-Status "Starting services with docker-compose..."
    docker-compose up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Services started successfully!"
        
        Write-Status "Waiting for services to be ready..."
        Start-Sleep -Seconds 5
        
        # Check service health
        $services = docker-compose ps --format json | ConvertFrom-Json
        $allHealthy = $true
        
        foreach ($service in $services) {
            if ($service.State -eq "running") {
                Write-Success "$($service.Service) is running"
            } else {
                Write-Warning "$($service.Service) is $($service.State)"
                $allHealthy = $false
            }
        }
        
        if ($allHealthy) {
            Write-Host ""
            Write-Success "🎉 IntervYou is ready!"
            Write-Status "Application: http://localhost:8000"
            Write-Status "Health Check: http://localhost:8000/health"
            Write-Status "Database: localhost:5432"
        } else {
            Write-Warning "Some services may not be ready. Check logs with: .\manage-docker.ps1 logs"
        }
    } else {
        Write-Error "Failed to start services"
    }
}

function Stop-Application {
    Write-Header "Stopping IntervYou Application"
    
    if (-not (Test-DockerRunning)) { return }
    
    Write-Status "Stopping all services..."
    docker-compose down
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "All services stopped successfully!"
    } else {
        Write-Error "Failed to stop some services"
    }
}

function Restart-Application {
    Write-Header "Restarting IntervYou Application"
    Stop-Application
    Start-Sleep -Seconds 2
    Start-Application
}

function Show-Logs {
    Write-Header "IntervYou Application Logs"
    
    if (-not (Test-DockerRunning)) { return }
    
    if ($Follow) {
        Write-Status "Following logs (Press Ctrl+C to stop)..."
        docker-compose logs -f
    } else {
        Write-Status "Recent logs:"
        docker-compose logs --tail=50
    }
}

function Cleanup-Docker {
    Write-Header "Docker Cleanup"
    
    if (-not (Test-DockerRunning)) { return }
    
    Write-Warning "This will remove old Docker images and free up space"
    
    if (-not $Force) {
        $continue = Read-Host "Continue? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            Write-Status "Cleanup cancelled."
            return
        }
    }
    
    Write-Status "Stopping services..."
    docker-compose down 2>$null
    
    Write-Status "Removing old IntervYou images..."
    $oldImages = docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" | Where-Object { 
        $_ -match "^(aipowere|intervyou:latest)" 
    }
    
    foreach ($imageInfo in $oldImages) {
        if ($imageInfo) {
            $parts = $imageInfo -split " "
            $imageName = $parts[0]
            $imageId = $parts[1]
            Write-Status "Removing: $imageName"
            docker rmi $imageId --force 2>$null
        }
    }
    
    Write-Status "Cleaning up dangling images..."
    docker image prune -f
    
    Write-Status "Cleaning up unused volumes..."
    docker volume prune -f
    
    Write-Success "Cleanup completed!"
}

function Show-Status {
    Write-Header "IntervYou Status"
    
    if (-not (Test-DockerRunning)) { return }
    
    Write-Status "Docker Images:"
    docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    
    Write-Host ""
    Write-Status "Running Containers:"
    docker-compose ps
    
    Write-Host ""
    Write-Status "System Information:"
    $dockerInfo = docker system df
    Write-Host $dockerInfo
    
    # Check if application is accessible
    Write-Host ""
    Write-Status "Application Health:"
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Success "Application is healthy and accessible"
        } else {
            Write-Warning "Application responded with status: $($response.StatusCode)"
        }
    } catch {
        Write-Warning "Application is not accessible at http://localhost:8000"
    }
}

# Main script execution
switch ($Action.ToLower()) {
    "build" { Build-Application }
    "start" { Start-Application }
    "stop" { Stop-Application }
    "restart" { Restart-Application }
    "logs" { Show-Logs }
    "cleanup" { Cleanup-Docker }
    "status" { Show-Status }
    "help" { Show-Help }
    default { Show-Help }
}