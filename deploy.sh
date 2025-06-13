#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo "mmWave Radar - Deploy Script"
echo -e "==========================================${NC}"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not in a git repository!${NC}"
    exit 1
fi

# Check if there are changes to commit
if git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}No changes to commit.${NC}"
    
    # Check if we're ahead of remote
    git fetch origin > /dev/null 2>&1
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null || echo "no-remote")
    
    if [ "$LOCAL" != "$REMOTE" ] && [ "$REMOTE" != "no-remote" ]; then
        echo -e "${BLUE}Pushing existing commits to remote...${NC}"
        git push origin main 2>/dev/null || git push origin master 2>/dev/null
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Push successful!${NC}"
        else
            echo -e "${RED}✗ Push failed!${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✓ Everything up to date.${NC}"
    fi
    exit 0
fi

# Show status
echo -e "${BLUE}Current changes:${NC}"
git status --porcelain

echo ""
read -p "Enter commit message (or press Enter for auto-message): " commit_msg

if [ -z "$commit_msg" ]; then
    commit_msg="Update radar code - $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Add all changes
echo -e "${BLUE}Adding changes...${NC}"
git add -A

# Commit changes
echo -e "${BLUE}Committing changes...${NC}"
git commit -m "$commit_msg"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Commit failed!${NC}"
    exit 1
fi

# Push to remote (if remote exists)
echo -e "${BLUE}Pushing to remote...${NC}"
git push origin main 2>/dev/null || git push origin master 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Deploy successful!${NC}"
    echo ""
    echo -e "${BLUE}To update on Raspberry Pi, run:${NC}"
    echo "  ./update_radar.sh"
else
    echo -e "${YELLOW}⚠ Commit successful but push failed.${NC}"
    echo "You may need to set up a remote repository first."
    echo ""
    echo "To add a remote repository:"
    echo "  git remote add origin <your-repo-url>"
    echo "  git push -u origin main"
fi

echo ""
echo -e "${BLUE}=========================================="
echo "Deploy complete!"
echo -e "==========================================${NC}" 