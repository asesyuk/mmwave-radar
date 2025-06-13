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
    echo -e "${YELLOW}Flask not found. Please run the dependency installer first:${NC}"
    echo "./install_web_deps.sh"
    echo ""
    read -p "Do you want to run the installer now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./install_web_deps.sh
        if [ $? -ne 0 ]; then
            echo -e "${RED}Installation failed. Please check errors above.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Cannot start without Flask. Exiting.${NC}"
        exit 1
    fi
fi

# Get IP address (works on both Linux and macOS)
if command -v hostname >/dev/null 2>&1; then
    # Try Linux style first
    PI_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
    if [ -z "$PI_IP" ]; then
        # Fall back to macOS/general method
        PI_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
    fi
else
    PI_IP="localhost"
fi

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