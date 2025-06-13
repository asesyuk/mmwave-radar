#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================================="
echo "Setting Up Raspberry Pi for Remote Radar Control"
echo -e "==================================================${NC}"

# Check if we're on a Pi or need to connect to one
if [[ $(uname -m) == "arm"* ]] || [[ $(uname -m) == "aarch64" ]]; then
    echo -e "${GREEN}✓ Running on Raspberry Pi${NC}"
    
    # Update the code
    echo -e "${BLUE}Updating radar code...${NC}"
    ./update_radar.sh
    
    # Install dependencies
    echo -e "${BLUE}Installing dependencies...${NC}"
    ./install_web_deps.sh
    
    # Get Pi's IP address
    PI_IP=$(hostname -I | awk '{print $1}')
    
    echo -e "${GREEN}=================================================="
    echo "Pi Setup Complete!"
    echo -e "==================================================${NC}"
    echo -e "${YELLOW}To start remote control:${NC}"
    echo "1. Run: ./start_web_control.sh"
    echo "2. Access from laptop: http://$PI_IP:5001"
    echo ""
    echo -e "${YELLOW}From your laptop, open browser and go to:${NC}"
    echo -e "${GREEN}http://$PI_IP:5001${NC}"
    
else
    echo -e "${YELLOW}This script should be run ON the Raspberry Pi.${NC}"
    echo ""
    echo -e "${BLUE}From your laptop, SSH to your Pi and run:${NC}"
    echo "ssh pi@your-pi-ip"
    echo "cd /path/to/mmwave-data"
    echo "./setup_pi_remote.sh"
    echo ""
    echo -e "${BLUE}Or copy this entire project to your Pi and run:${NC}"
    echo "scp -r . pi@your-pi-ip:/home/pi/mmwave-data"
fi 