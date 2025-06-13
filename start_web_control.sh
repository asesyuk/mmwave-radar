#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo "Starting mmWave Radar Web Control Panel"
echo -e "==========================================${NC}"

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Flask not found. Installing requirements..."
    pip3 install -r requirements.txt
fi

# Get Pi's IP address
PI_IP=$(hostname -I | awk '{print $1}')

echo -e "${GREEN}Starting web server...${NC}"
echo ""
echo "Access the control panel at:"
echo "  Local:   http://localhost:5000"
echo "  Network: http://$PI_IP:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the web application
python3 web_control.py 