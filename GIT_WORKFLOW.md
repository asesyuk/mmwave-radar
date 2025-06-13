# Git Workflow for mmWave Radar Project

This guide explains how to use Git to easily update your radar code between your development machine and Raspberry Pi.

## 🚀 Quick Setup

### 1. Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `mmwave-radar` 
3. Make it **public** (easier for Pi access) or **private** (more secure)
4. **Don't** initialize with README (we already have files)

### 2. Connect Your Local Repository
```bash
# Add your GitHub repo as remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/mmwave-radar.git

# Set main branch
git branch -M main

# Make initial commit and push
./deploy.sh
```

### 3. Clone on Raspberry Pi
```bash
# On your Raspberry Pi
cd ~
git clone https://github.com/yourusername/mmwave-radar.git
cd mmwave-radar
chmod +x *.sh
```

## 📝 Daily Workflow

### On Your Development Machine:
```bash
# Make changes to your code
# When ready to deploy:
./deploy.sh
```
This script will:
- Show you what changed
- Ask for a commit message
- Commit and push to GitHub

### On Your Raspberry Pi:
```bash
# Update to latest code
./update_radar.sh
```
This script will:
- Pull latest changes from GitHub
- Install any new Python packages
- Set file permissions
- Handle conflicts gracefully

### Run the Radar:
```bash
python3 radar_test_simple.py
```

## 🛠 Advanced Usage

### Manual Git Commands

**Development Machine:**
```bash
# Check status
git status

# Add specific files
git add filename.py

# Commit with message
git commit -m "Fix radar parsing bug"

# Push to GitHub
git push origin main
```

**Raspberry Pi:**
```bash
# Check for updates
git fetch origin
git status

# Pull updates
git pull origin main

# View commit history
git log --oneline
```

### Handle Local Changes on Pi

If you made changes on the Pi and want to save them:
```bash
# Save your changes
git stash push -m "My Pi changes"

# Update
git pull origin main

# Apply your changes back (if desired)
git stash pop
```

## 🔧 Troubleshooting

### Permission Denied (GitHub)
**Option A: Use Personal Access Token**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate a new token with repo permissions
3. Use token as password when pushing

**Option B: Use SSH Keys**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub (copy the public key)
cat ~/.ssh/id_ed25519.pub

# Use SSH URL instead
git remote set-url origin git@github.com:yourusername/mmwave-radar.git
```

### Merge Conflicts
```bash
# If conflicts occur during pull
git status  # Shows conflicted files
# Edit files to resolve conflicts
git add .
git commit -m "Resolve merge conflicts"
```

### Reset to Clean State
```bash
# Discard all local changes (careful!)
git reset --hard origin/main
```

## 📁 Repository Structure

```
mmwave-radar/
├── .git/                      # Git repository data
├── .gitignore                 # Files to ignore
├── README.md                  # Main project documentation
├── GIT_WORKFLOW.md           # This file
├── RADAR_STATUS_GUIDE.md     # Radar behavior guide
├── requirements.txt           # Python dependencies
├── install_radar.sh          # Initial setup script
├── deploy.sh                 # Development deployment script
├── update_radar.sh           # Pi update script
├── radar_test_simple.py      # Simplified radar script
├── demo_XY_test.py           # Original full script
├── parcer_XY_test.py         # Data parser module
└── xwr18xx_profile_*.cfg     # Radar configuration
```

## 🎯 Benefits of This Workflow

✅ **Easy Updates**: One command to deploy from dev machine  
✅ **Version Control**: Track all changes and revert if needed  
✅ **Backup**: Your code is safely stored on GitHub  
✅ **Collaboration**: Share with others easily  
✅ **Rollback**: Go back to previous working versions  
✅ **Multiple Pi's**: Update multiple Raspberry Pi's from same repo  

## 🚨 Best Practices

1. **Test locally first** before deploying
2. **Use descriptive commit messages**
3. **Commit frequently** (small changes)
4. **Pull before pushing** to avoid conflicts
5. **Backup important data** before major updates 