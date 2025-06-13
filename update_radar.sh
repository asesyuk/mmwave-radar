#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo "mmWave Radar - Git Update Script"
echo -e "==========================================${NC}"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not in a git repository!${NC}"
    echo "Run this script from your mmwave-radar directory"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}Warning: You have uncommitted changes!${NC}"
    echo "Your local changes:"
    git status --porcelain
    echo ""
    read -p "Do you want to stash your changes and continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git stash push -m "Auto-stash before update $(date)"
        echo -e "${GREEN}Changes stashed successfully${NC}"
    else
        echo -e "${RED}Update cancelled${NC}"
        exit 1
    fi
fi

# Update from remote
echo -e "${BLUE}Fetching latest changes...${NC}"
git fetch origin

# Check if there are updates available
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}✓ Already up to date!${NC}"
else
    echo -e "${YELLOW}Updates available. Pulling changes...${NC}"
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Update successful!${NC}"
        
        # Check if requirements.txt was updated
        if git diff HEAD~1 --name-only | grep -q "requirements.txt"; then
            echo -e "${YELLOW}requirements.txt was updated. Installing new packages...${NC}"
            pip3 install -r requirements.txt
        fi
        
        # Make scripts executable
        chmod +x *.sh
        chmod +x radar_test_simple.py
        
        echo -e "${GREEN}✓ All files updated and permissions set${NC}"
    else
        echo -e "${RED}✗ Update failed!${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}=========================================="
echo "Update complete!"
echo -e "==========================================${NC}"
echo "To run the radar:"
echo "  python3 radar_test_simple.py"
echo "" 