#!/bin/bash

# IntervYou Docker Build and Cleanup Script
# This script builds the cleaned FastAPI application and manages Docker images

set -e  # Exit on any error

echo "🚀 IntervYou Docker Build Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running ✓"

# Show current Docker images
print_status "Current Docker images:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

echo ""
print_warning "This script will:"
echo "  1. Clean up old/unused Docker images"
echo "  2. Build the new optimized IntervYou application"
echo "  3. Keep only essential images (postgres:15-alpine, intervyou-cleaned:latest)"

read -p "Do you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Operation cancelled."
    exit 0
fi

# Step 1: Remove old IntervYou images (keep postgres)
print_status "Cleaning up old Docker images..."

# Remove old intervyou images but keep postgres
docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" | grep -E "^(intervyou|aipowere)" | while read image id; do
    print_warning "Removing old image: $image"
    docker rmi "$id" --force 2>/dev/null || true
done

# Remove dangling images
print_status "Removing dangling images..."
docker image prune -f

# Step 2: Build the new cleaned application
print_status "Building the cleaned IntervYou application..."

# Build the new image
docker build -t intervyou-cleaned:latest . --no-cache

if [ $? -eq 0 ]; then
    print_success "Successfully built intervyou-cleaned:latest"
else
    print_error "Failed to build the Docker image"
    exit 1
fi

# Step 3: Build with docker-compose to ensure everything works
print_status "Testing with docker-compose..."
docker-compose build --no-cache

if [ $? -eq 0 ]; then
    print_success "Docker-compose build successful"
else
    print_error "Docker-compose build failed"
    exit 1
fi

# Step 4: Show final image list
echo ""
print_status "Final Docker images:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

# Step 5: Calculate space saved
echo ""
print_success "Docker cleanup and build completed!"
print_status "Kept essential images:"
echo "  - postgres:15-alpine (database)"
echo "  - intervyou-cleaned:latest (optimized application)"

# Step 6: Provide next steps
echo ""
print_status "Next steps:"
echo "  1. Start the application: docker-compose up -d"
echo "  2. Check logs: docker-compose logs -f web"
echo "  3. Access application: http://localhost:8000"
echo "  4. Health check: http://localhost:8000/health"

# Optional: Start the application
echo ""
read -p "Do you want to start the application now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Starting IntervYou application..."
    docker-compose up -d
    
    print_status "Waiting for services to start..."
    sleep 10
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Application started successfully!"
        print_status "Access your application at: http://localhost:8000"
        print_status "View logs with: docker-compose logs -f"
    else
        print_error "Some services failed to start. Check logs with: docker-compose logs"
    fi
fi

print_success "Script completed successfully! 🎉"