#!/bin/bash

# Customer Support Copilot Deployment Script

echo "🚀 Customer Support Copilot Deployment Script"
echo "=============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create one with your API keys."
    echo "📝 Example:"
    echo "COHERE_API_KEY=your_key_here"
    echo "USE_COHERE=true"
    exit 1
fi

# Build and run with Docker Compose
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting application..."
docker-compose up -d

echo "✅ Deployment complete!"
echo "📱 Application available at: http://localhost:8501"
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
