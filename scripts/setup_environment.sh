#!/bin/bash
set -e

echo "Setting up PX4 GPS Spoofing Research Environment..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements/dev.txt

# Copy environment file
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file. Please review and modify as needed."
fi

# Initialize PX4 submodule if needed
if [ ! -f "PX4-Autopilot/CMakeLists.txt" ]; then
    echo "Initializing PX4-Autopilot submodule..."
    git submodule update --init --recursive
fi

# Create .gitkeep files for empty directories
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/models/.gitkeep

echo "Environment setup complete!"
echo "To activate the environment, run: source venv/bin/activate"
