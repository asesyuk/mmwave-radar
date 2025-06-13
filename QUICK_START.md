# 🚀 Quick Start - Web Control Panel

This guide helps you get the web control panel running quickly.

## ⚡ **Super Quick Setup**

### **1. Install Dependencies**
```bash
# Run the automated installer
./install_web_deps.sh
```

### **2. Start Web Server**
```bash
# Start the control panel
./start_web_control.sh
```

### **3. Access Control Panel**
- **Local**: http://localhost:5000
- **Network**: http://your-device-ip:5000

## 🔧 **If Installation Fails**

### **Option 1: Manual Installation**
```bash
# Install packages individually
pip3 install pyserial>=3.5
pip3 install flask>=2.0.0
pip3 install numpy>=1.19.0
```

### **Option 2: System Package Manager**

**On Raspberry Pi/Ubuntu:**
```bash
sudo apt update
sudo apt install python3-flask python3-numpy python3-serial
```

**On macOS with Homebrew:**
```bash
brew install python3
pip3 install flask pyserial numpy
```

## 📱 **Using the Web Interface**

### **Main Control Panel** (`/`)
- ✅ **Start/Stop** radar remotely
- 📊 **Monitor status** in real-time
- 📍 **View current** sensor configuration
- ⚙️ **Quick access** to settings

### **Configuration Page** (`/config`)
- 📍 **Set position**: X, Y, Z coordinates
- 🧭 **Set orientation**: Yaw, Pitch, Roll angles
- 📝 **Name & description**: Identify your sensor
- ⏱️ **Timing settings**: Processing delay

## 🔧 **API Endpoints**

- `GET /api/status` - Current radar status
- `POST /api/start` - Start radar
- `POST /api/stop` - Stop radar
- `GET/POST /api/config` - Configuration management

## 🚨 **Troubleshooting**

### **Common Issues:**

**1. "Flask not found"**
```bash
./install_web_deps.sh
```

**2. "Permission denied" on serial ports**
```bash
sudo usermod -a -G dialout $USER
# Then logout and login again
```

**3. "Cannot connect to radar"**
- Check USB connections
- Verify ports: `ls -la /dev/ttyACM*`
- Try: `sudo ./start_web_control.sh`

**4. Web interface not accessible**
- Check firewall settings
- Try local access first: http://localhost:5000
- Ensure port 5000 is not blocked

## 🎯 **Features Overview**

✅ **Remote Control** - Start/stop from any device  
✅ **Real-time Status** - Live updates every 5 seconds  
✅ **Easy Configuration** - Web forms for all settings  
✅ **Mobile Friendly** - Works on phones and tablets  
✅ **Git Integration** - Deploy changes instantly  
✅ **Auto-save Settings** - Configuration persists between restarts  

## 📱 **Mobile Usage**

The web interface is fully responsive:
- **Phone**: Optimized touch controls
- **Tablet**: Perfect for monitoring
- **Desktop**: Full feature access

Access from anywhere on your network!

---

**Need help?** Check the full documentation in `README.md` and `GIT_WORKFLOW.md` 