#!/bin/bash
# Run IntervYou with Docker Compose

echo "🚀 Starting IntervYou with Docker Compose..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your configuration before running again."
    exit 1
fi

# Start services
docker-compose up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ IntervYou is running!"
    echo ""
    echo "🌐 Access your app at: http://localhost:8000"
    echo ""
    echo "Useful commands:"
    echo "  View logs:        docker-compose logs -f"
    echo "  Stop app:         docker-compose down"
    echo "  Restart app:      docker-compose restart"
    echo "  View status:      docker-compose ps"
else
    echo "❌ Failed to start Docker containers!"
    exit 1
fi
