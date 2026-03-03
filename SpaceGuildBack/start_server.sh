#!/bin/bash
# Space Guild Server Startup Script
# Launches the game loop in current shell and API server in separate WSL terminals

set -e  # Exit on error

echo "=== Space Guild Server Startup ==="
echo "Working directory: $(pwd)"
echo ""

# Check if game data is initialized
if [ ! -f "game_data/locations.json" ]; then
    echo "ERROR: Game world not initialized. Run setup.py first:"
    echo "  python3 setup.py"
    exit 1
fi

# Get current directory as Unix path for WSL
CURRENT_DIR=$(pwd)

echo "Starting API server in separate WSL terminal..."
echo "API will be available at: http://localhost:5000"
echo ""

# Launch gunicorn in a new PowerShell window with WSL
# This creates a new terminal window with better styling
powershell.exe -Command "Start-Process powershell -ArgumentList '-NoExit', '-Command', 'wsl bash -c ''cd $CURRENT_DIR && gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 api:app'''"

# Give the API server a moment to start
sleep 3

echo "=== Starting Game Loop ==="
echo "Note: Close the PowerShell windows manually to stop the servers"
echo ""

# Run the game loop in a new PowerShell window
powershell.exe -Command "Start-Process powershell -ArgumentList '-NoExit', '-Command', 'wsl bash -c ''cd $CURRENT_DIR && python3 program.py'''"

echo "Both servers started in separate PowerShell windows!"
echo "- API Server: http://localhost:5000"
echo "- Game Loop: Running in separate window"
