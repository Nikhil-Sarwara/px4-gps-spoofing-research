#!/bin/bash
set -e

echo "Setting up Docker environment for PX4 GPS Spoofing Research..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
mkdir -p logs/{simulation,attacks,detection}
mkdir -p data/{raw,processed,models}
mkdir -p notebooks

# Create .gitkeep files
touch logs/simulation/.gitkeep
touch logs/attacks/.gitkeep
touch logs/detection/.gitkeep
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/models/.gitkeep

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file from template."
fi

# Build the Docker image
echo "Building Docker image..."
docker-compose -f docker/docker-compose.yml build

echo "Docker environment setup complete!"
echo ""
echo "Usage:"
echo "  docker-compose -f docker/docker-compose.yml up          # Start PX4 SITL"
echo "  docker-compose -f docker/docker-compose.yml run px4-gps-spoofing bash"
echo "  docker-compose -f docker/docker-compose.dev.yml up     # Start with Jupyter"
echo ""

