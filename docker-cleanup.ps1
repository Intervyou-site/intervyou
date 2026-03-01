# Docker Cleanup Script for IntervYou
# Removes old images and keeps only essential ones

param(
    [switch]$Force,
    [switch]$All
)

$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
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

Write-Host "🧹 Docker Cleanup for IntervYou" -ForegroundColor $Blue
Write-Host "===============================" -ForegroundColor $Blue

# Show current images
Write-Status "Current Docker images:"
docker images

Write-Host ""

if ($All) {
    Write-Warning "This will remove ALL Docker images except postgres:15-alpine"
} else {
    Write-Warning "This will remove old IntervYou images (aipowere, old intervyou versions)"
}

if (-not $Force) {
    $continue = Read-Host "Continue? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Status "Cleanup cancelled."
        exit 0
    }
}

# Stop any running containers first
Write-Status "Stopping running containers..."
docker-compose down 2>$null

if ($All) {
    # Remove all images except postgres
    Write-Status "Removing all images except postgres:15-alpine..."
    $allImages = docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" | Where-Object { $_ -notmatch "postgres:15-alpine" }
    
    foreach ($imageInfo in $allImages) {
        if ($imageInfo) {
            $parts = $imageInfo -split " "
            $imageName = $parts[0]
            $imageId = $parts[1]
            Write-Warning "Removing: $imageName"
            docker rmi $imageId --force 2>$null
        }
    }
} else {
    # Remove only old IntervYou images
    Write-Status "Removing old IntervYou images..."
    
    # Remove aipowere images
    $aipowereImages = docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" | Where-Object { $_ -match "^aipowere" }
    foreach ($imageInfo in $aipowereImages) {
        if ($imageInfo) {
            $parts = $imageInfo -split " "
            $imageName = $parts[0]
            $imageId = $parts[1]
            Write-Warning "Removing aipowere image: $imageName"
            docker rmi $imageId --force 2>$null
        }
    }
    
    # Remove old intervyou images (keep intervyou-cleaned)
    $oldIntervyouImages = docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" | Where-Object { $_ -match "^intervyou:latest" }
    foreach ($imageInfo in $oldIntervyouImages) {
        if ($imageInfo) {
            $parts = $imageInfo -split " "
            $imageName = $parts[0]
            $imageId = $parts[1]
            Write-Warning "Removing old intervyou image: $imageName"
            docker rmi $imageId --force 2>$null
        }
    }
}

# Remove dangling images
Write-Status "Removing dangling images..."
docker image prune -f

# Remove unused volumes
Write-Status "Removing unused volumes..."
docker volume prune -f

# Remove unused networks
Write-Status "Removing unused networks..."
docker network prune -f

Write-Host ""
Write-Success "Cleanup completed!"

# Show remaining images
Write-Status "Remaining Docker images:"
docker images

Write-Host ""
Write-Status "Essential images kept:"
Write-Host "  - postgres:15-alpine (database)"
if (-not $All) {
    Write-Host "  - intervyou-cleaned:latest (if built)"
}

Write-Host ""
Write-Status "To rebuild the application:"
Write-Host "  .\docker-build.ps1"