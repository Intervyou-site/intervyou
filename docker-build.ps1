# IntervYou Docker Build and Cleanup Script (PowerShell)
# This script builds the cleaned FastAPI application and manages Docker images

param(
    [switch]$Force,
    [switch]$Start
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"

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

Write-Host "🚀 IntervYou Docker Build Script" -ForegroundColor $Blue
Write-Host "================================" -ForegroundColor $Blue

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Status "Docker is running ✓"
} catch {
    Write-Error "Docker is not running. Please start Docker Desktop and try again."
    exit 1
}

# Show current Docker images
Write-Status "Current Docker images:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

Write-Host ""
Write-Warning "This script will:"
Write-Host "  1. Clean up old/unused Docker images"
Write-Host "  2. Build the new optimized IntervYou application"
Write-Host "  3. Keep only essential images (postgres:15-alpine, intervyou-cleaned:latest)"

if (-not $Force) {
    $continue = Read-Host "Do you want to continue? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Status "Operation cancelled."
        exit 0
    }
}

# Step 1: Remove old IntervYou images (keep postgres)
Write-Status "Cleaning up old Docker images..."

# Get old intervyou and aipowere images
$oldImages = docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" | Where-Object { $_ -match "^(intervyou|aipowere)" }

foreach ($imageInfo in $oldImages) {
    if ($imageInfo) {
        $parts = $imageInfo -split " "
        $imageName = $parts[0]
        $imageId = $parts[1]
        Write-Warning "Removing old image: $imageName"
        try {
            docker rmi $imageId --force 2>$null
        } catch {
            # Ignore errors when removing images
        }
    }
}

# Remove dangling images
Write-Status "Removing dangling images..."
docker image prune -f

# Step 2: Build the new cleaned application
Write-Status "Building the cleaned IntervYou application..."

# Build the new image
Write-Status "Running: docker build -t intervyou-cleaned:latest . --no-cache"
$buildResult = docker build -t intervyou-cleaned:latest . --no-cache

if ($LASTEXITCODE -eq 0) {
    Write-Success "Successfully built intervyou-cleaned:latest"
} else {
    Write-Error "Failed to build the Docker image"
    exit 1
}

# Step 3: Build with docker-compose to ensure everything works
Write-Status "Testing with docker-compose..."
$composeResult = docker-compose build --no-cache

if ($LASTEXITCODE -eq 0) {
    Write-Success "Docker-compose build successful"
} else {
    Write-Error "Docker-compose build failed"
    exit 1
}

# Step 4: Show final image list
Write-Host ""
Write-Status "Final Docker images:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

# Step 5: Calculate space saved
Write-Host ""
Write-Success "Docker cleanup and build completed!"
Write-Status "Kept essential images:"
Write-Host "  - postgres:15-alpine (database)"
Write-Host "  - intervyou-cleaned:latest (optimized application)"

# Step 6: Provide next steps
Write-Host ""
Write-Status "Next steps:"
Write-Host "  1. Start the application: docker-compose up -d"
Write-Host "  2. Check logs: docker-compose logs -f web"
Write-Host "  3. Access application: http://localhost:8000"
Write-Host "  4. Health check: http://localhost:8000/health"

# Optional: Start the application
if ($Start -or (-not $Force)) {
    Write-Host ""
    if (-not $Start) {
        $startNow = Read-Host "Do you want to start the application now? (y/N)"
    } else {
        $startNow = "y"
    }
    
    if ($startNow -eq "y" -or $startNow -eq "Y") {
        Write-Status "Starting IntervYou application..."
        docker-compose up -d
        
        Write-Status "Waiting for services to start..."
        Start-Sleep -Seconds 10
        
        # Check if services are running
        $runningServices = docker-compose ps
        if ($runningServices -match "Up") {
            Write-Success "Application started successfully!"
            Write-Status "Access your application at: http://localhost:8000"
            Write-Status "View logs with: docker-compose logs -f"
        } else {
            Write-Error "Some services failed to start. Check logs with: docker-compose logs"
        }
    }
}

Write-Success "Script completed successfully! 🎉"

# Usage examples
Write-Host ""
Write-Status "Usage examples:"
Write-Host "  .\docker-build.ps1                    # Interactive mode"
Write-Host "  .\docker-build.ps1 -Force             # Skip confirmations"
Write-Host "  .\docker-build.ps1 -Force -Start      # Build and start automatically"