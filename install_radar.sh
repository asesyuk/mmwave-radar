#!/bin/bash

echo "=========================================="
echo "mmWave Radar Setup for Raspberry Pi"
echo "=========================================="

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python3 and pip if not installed
echo "Installing Python3 and pip..."
sudo apt install -y python3 python3-pip

# Install required Python packages
echo "Installing Python packages..."
pip3 install -r requirements.txt

# Add user to dialout group for serial port access
echo "Adding user to dialout group..."
sudo usermod -a -G dialout $USER

# Set permissions for serial ports
echo "Setting up serial port permissions..."
sudo chmod 666 /dev/ttyACM*

# Make Python script executable
chmod +x radar_test_simple.py

echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Connect your mmWave radar to the Raspberry Pi"
echo "2. Restart your Pi or log out and back in"
echo "3. Check that ports are available: ls -la /dev/ttyACM*"
echo "4. Run the radar test: python3 radar_test_simple.py"
echo ""
echo "If you get permission errors, try:"
echo "  sudo python3 radar_test_simple.py"
echo "" 