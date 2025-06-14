#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo "Installing Web Dependencies"
echo -e "==========================================${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python3
if ! command_exists python3; then
    echo -e "${RED}Error: Python3 is not installed!${NC}"
    echo "Please install Python3 first"
    exit 1
fi

echo -e "${GREEN}✓ Python3 found${NC}"

# Check pip3
if ! command_exists pip3; then
    echo -e "${YELLOW}pip3 not found, trying to install...${NC}"
    if command_exists apt; then
        sudo apt update && sudo apt install -y python3-pip
    elif command_exists brew; then
        # macOS with Homebrew
        echo "Please install pip3 manually or use: python3 -m ensurepip --upgrade"
        exit 1
    else
        echo -e "${RED}Please install pip3 manually${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓ pip3 found${NC}"

# Try to install packages one by one for better error handling
echo -e "${BLUE}Installing Python packages...${NC}"

# Check if we're on a system with externally managed Python (like newer Raspberry Pi OS)
echo "Installing pyserial..."
if pip3 install "pyserial>=3.5" 2>/dev/null; then
    echo -e "${GREEN}✓ pyserial installed${NC}"
elif command_exists apt; then
    echo -e "${YELLOW}Using system package manager (apt)...${NC}"
    if sudo apt update && sudo apt install -y python3-serial python3-flask python3-numpy; then
        echo -e "${GREEN}✓ All packages installed via apt${NC}"
        echo -e "${GREEN}✓ pyserial installed${NC}"
        echo -e "${GREEN}✓ Flask installed${NC}"
        echo -e "${GREEN}✓ numpy installed${NC}"
        echo ""
        echo -e "${GREEN}=========================================="
        echo "Installation Complete!"
        echo -e "==========================================${NC}"
        echo ""
        echo "All dependencies are now installed."
        echo "You can now run: ./start_web_control.sh"
        echo ""
        exit 0
    else
        echo -e "${RED}✗ Failed to install via apt${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠ pip install failed, trying with --break-system-packages...${NC}"
    if pip3 install --break-system-packages "pyserial>=3.5"; then
        echo -e "${GREEN}✓ pyserial installed${NC}"
    else
        echo -e "${RED}✗ Failed to install pyserial${NC}"
        exit 1
    fi
fi

# Only try individual Flask/numpy installation if we didn't use apt above
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing Flask..."
    if pip3 install "flask>=2.0.0" 2>/dev/null; then
        echo -e "${GREEN}✓ Flask installed${NC}"
    elif pip3 install --break-system-packages "flask>=2.0.0"; then
        echo -e "${GREEN}✓ Flask installed (system override)${NC}"
    else
        echo -e "${RED}✗ Failed to install Flask${NC}"
        exit 1
    fi
fi

if ! python3 -c "import numpy" 2>/dev/null; then
    echo "Installing numpy (this may take a while)..."
    if pip3 install "numpy>=1.19.0" 2>/dev/null; then
        echo -e "${GREEN}✓ numpy installed${NC}"
    elif pip3 install --break-system-packages "numpy>=1.19.0"; then
        echo -e "${GREEN}✓ numpy installed (system override)${NC}"
    else
        echo -e "${YELLOW}⚠ numpy installation failed, trying alternative...${NC}"
        # Try installing pre-compiled binary if available
        if pip3 install --break-system-packages --only-binary=numpy "numpy>=1.19.0"; then
            echo -e "${GREEN}✓ numpy installed (binary)${NC}"
        else
            echo -e "${RED}✗ Failed to install numpy${NC}"
            echo "You may need to install numpy manually or use system packages"
            exit 1
        fi
    fi
fi

echo ""
echo -e "${GREEN}=========================================="
echo "Installation Complete!"
echo -e "==========================================${NC}"
echo ""
echo "All dependencies are now installed."
echo "You can now run: ./start_web_control.sh"
echo "" 