#!/bin/bash
set -e

echo "========================================"
echo "PX4 GPS Spoofing Research Environment"
echo "========================================"

# Check if PX4-Autopilot exists
if [ ! -d "/workspace/PX4-Autopilot" ]; then
    echo "Error: PX4-Autopilot directory not found!"
    echo "Make sure you have initialized the PX4-Autopilot submodule."
    exit 1
fi

# Navigate to PX4-Autopilot directory
cd /workspace/PX4-Autopilot

# Build PX4 if not already built
if [ ! -d "build" ]; then
    echo "Building PX4 for the first time..."
    make px4_sitl_default
fi

# Function to start PX4 SITL
start_sitl() {
    echo "Starting PX4 SITL with Gazebo..."
    echo "Home coordinates: LAT=${PX4_HOME_LAT}, LON=${PX4_HOME_LON}, ALT=${PX4_HOME_ALT}"
    echo "MAVLink available on port 5760"
    echo "QGroundControl can connect to port 14550"
    make px4_sitl_default gazebo
}

# Function to start interactive bash
start_bash() {
    echo "Starting interactive bash session..."
    echo "Available research scripts in /workspace/src/"
    echo "PX4-Autopilot located at /workspace/PX4-Autopilot"
    exec /bin/bash
}

# Function to start Jupyter notebook
start_jupyter() {
    echo "Starting Jupyter notebook server..."
    cd /workspace
    exec jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=''
}

# Function to run attack simulation
run_attack() {
    echo "Running GPS spoofing attack simulation..."
    cd /workspace
    if [ -f "src/attacks/attack_simulation.py" ]; then
        python3 src/attacks/attack_simulation.py "$@"
    else
        echo "Attack simulation script not found. Make sure your scripts are mounted."
        start_bash
    fi
}

# Parse command line arguments
case "$1" in
    "sitl")
        start_sitl
        ;;
    "bash")
        start_bash
        ;;
    "jupyter")
        start_jupyter
        ;;
    "attack")
        shift
        run_attack "$@"
        ;;
    *)
        echo "Usage: $0 {sitl|bash|jupyter|attack}"
        echo ""
        echo "Commands:"
        echo "  sitl     - Start PX4 SITL with Gazebo (default)"
        echo "  bash     - Start interactive bash session"
        echo "  jupyter  - Start Jupyter notebook server on port 8888"
        echo "  attack   - Run attack simulation scripts"
        echo ""
        echo "Examples:"
        echo "  docker-compose up                    # Start SITL"
        echo "  docker-compose run px4-gps-spoofing bash    # Interactive session"
        echo "  docker-compose run px4-gps-spoofing jupyter # Jupyter server"
        echo "  docker-compose run px4-gps-spoofing attack  # Run attack simulation"
        start_bash
        ;;
esac

