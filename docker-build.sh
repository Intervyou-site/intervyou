#!/bin/bash
# Build Docker image for IntervYou

echo "🐳 Building IntervYou Docker image..."

docker build -t intervyou:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "To run the container:"
    echo "  docker-compose up -d"
    echo ""
    echo "Or manually:"
    echo "  docker run -p 8000:8000 --env-file .env intervyou:latest"
else
    echo "❌ Docker build failed!"
    exit 1
fi
