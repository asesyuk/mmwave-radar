# 🌐 Remote Control Setup Guide

## 🎯 **Goal: Control Radar on Pi from Your Laptop**

This guide helps you set up remote control so you can:
- Run the web server on your **Raspberry Pi** (where the radar is connected)
- Access the control panel from your **laptop browser**
- Start/stop the radar sensor remotely

---

## 🚀 **Quick Setup (3 Steps)**

### **Step 1: Deploy from Laptop** ✅ DONE
```bash
# On your laptop (already completed)
./deploy.sh
```

### **Step 2: Setup on Raspberry Pi**
```bash
# SSH into your Pi from laptop
ssh pi@your-pi-ip-address

# Navigate to project (adjust path as needed)
cd /home/pi/mmwave-data

# Run the Pi setup script
./setup_pi_remote.sh

# Start the web server on Pi
./start_web_control.sh
```

### **Step 3: Access from Laptop**
Open browser on your laptop and go to:
```
http://your-pi-ip:5001
```

---

## 📋 **Detailed Instructions**

### **🔧 On Your Raspberry Pi:**

1. **Get the latest code:**
   ```bash
   ./update_radar.sh
   ```

2. **Install web dependencies:**
   ```bash
   ./install_web_deps.sh
   ```

3. **Start web server:**
   ```bash
   ./start_web_control.sh
   ```
   
   You'll see output like:
   ```
   Port 5000 is in use, trying next...
   Access at: http://your-device-ip:5001
   Local access: http://localhost:5001
   ```

4. **Note the IP and port** (e.g., `192.168.1.100:5001`)

### **💻 On Your Laptop:**

1. **Open any web browser**
2. **Navigate to:** `http://pi-ip-address:5001`
3. **You'll see the same interface** as before, but now it controls the Pi!

---

## 🌐 **Network Setup Tips**

### **Find Your Pi's IP Address:**
```bash
# On the Pi, run:
hostname -I

# Or from laptop:
ping raspberrypi.local
nmap -sn 192.168.1.0/24  # scan your network
```

### **Ensure Network Access:**
- Pi and laptop must be on **same network** (WiFi/Ethernet)
- Check Pi's firewall allows port 5001
- Router must allow internal network communication

---

## 🎮 **How Remote Control Works**

### **Architecture:**
```
[Your Laptop] → Browser → Network → [Raspberry Pi] → Web Server → Radar Hardware
     ↑                                                    ↓
   Control                                          Live Data
   Interface                                       Processing
```

### **What You Can Do Remotely:**
- ✅ **Start/Stop Radar** - Click buttons to control sensor
- ✅ **View Live Status** - See real-time detection data  
- ✅ **Configure Settings** - Adjust sensor position/orientation
- ✅ **Monitor Performance** - Track frame rates and detection counts
- ✅ **Update Configuration** - Change parameters without SSH

---

## 🔧 **Troubleshooting**

### **Can't Access Pi from Laptop:**
```bash
# Test connectivity
ping your-pi-ip

# Check if web server is running on Pi
curl http://your-pi-ip:5001

# Verify Pi's web server status
ssh pi@your-pi-ip
ps aux | grep web_control
```

### **"Connection Refused" Error:**
- Web server not running on Pi
- Wrong IP address
- Firewall blocking port 5001

### **"Radar Failed to Start" on Pi:**
- Check USB connections to radar
- Verify serial ports: `ls -la /dev/ttyACM*`
- Try with `sudo`: `sudo ./start_web_control.sh`

---

## 📱 **Mobile Access**

The web interface works great on mobile devices too!

From your **phone/tablet**:
- Connect to same WiFi as Pi  
- Open browser → `http://pi-ip:5001`
- Touch-friendly controls for start/stop

---

## 🎯 **Next Steps After Setup**

1. **Bookmark Pi's URL** in your laptop browser
2. **Test radar start/stop** functionality  
3. **Configure sensor position** for your setup
4. **Set up monitoring** for continuous operation
5. **Consider port forwarding** for internet access (advanced)

---

## ✅ **Success Indicators**

You know it's working when:
- ✅ Pi web server starts without errors
- ✅ Laptop can access Pi's IP:port  
- ✅ "Start Radar" button works (no "failed to start" error)
- ✅ Live detection data appears in interface
- ✅ Configuration changes take effect immediately

---

**🎊 Once set up, you have full remote control of your radar sensor from anywhere on your network!** 