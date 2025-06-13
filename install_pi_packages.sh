#!/bin/bash

# Pi-specific installation using system packages
# This avoids the externally-managed-environment issue

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo "Installing Web Dependencies for Raspberry Pi"
echo "Using system packages (apt)"
echo -e "==========================================${NC}"

# Update package list
echo -e "${BLUE}Updating package list...${NC}"
if sudo apt update; then
    echo -e "${GREEN}✓ Package list updated${NC}"
else
    echo -e "${RED}✗ Failed to update package list${NC}"
    exit 1
fi

# Install Python packages via apt
echo -e "${BLUE}Installing Python packages via apt...${NC}"
if sudo apt install -y python3-serial python3-flask python3-numpy; then
    echo -e "${GREEN}✓ All packages installed successfully:${NC}"
    echo -e "${GREEN}  ✓ python3-serial (pyserial)${NC}"
    echo -e "${GREEN}  ✓ python3-flask${NC}"
    echo -e "${GREEN}  ✓ python3-numpy${NC}"
else
    echo -e "${RED}✗ Failed to install packages${NC}"
    exit 1
fi

# Verify installations
echo -e "${BLUE}Verifying installations...${NC}"

if python3 -c "import serial" 2>/dev/null; then
    echo -e "${GREEN}✓ pyserial working${NC}"
else
    echo -e "${RED}✗ pyserial not working${NC}"
fi

if python3 -c "import flask" 2>/dev/null; then
    echo -e "${GREEN}✓ Flask working${NC}"
else
    echo -e "${RED}✗ Flask not working${NC}"
fi

if python3 -c "import numpy" 2>/dev/null; then
    echo -e "${GREEN}✓ numpy working${NC}"
else
    echo -e "${RED}✗ numpy not working${NC}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo "Installation Complete!"
echo -e "==========================================${NC}"
echo ""
echo "All dependencies are now installed using system packages."
echo "You can now run: ./start_web_control.sh"
echo ""
echo -e "${YELLOW}Note: Using system packages avoids the 'externally-managed-environment' issue${NC}"
echo "" 