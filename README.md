# mmWave Radar Data Extraction for Raspberry Pi

This project processes live data from Texas Instruments mmWave radar sensors on Raspberry Pi.

## Hardware Requirements

- Raspberry Pi (3B+ or 4 recommended)
- Texas Instruments mmWave radar (xWR18xx series)
- USB cables for radar connection

## Quick Start

### 1. Transfer Files to Raspberry Pi
Copy all files to your Raspberry Pi:
```bash
scp -r ./* pi@your-pi-ip:~/mmwave-radar/
```

### 2. Run Installation Script
On your Raspberry Pi:
```bash
cd ~/mmwave-radar
chmod +x install_radar.sh
./install_radar.sh
```

### 3. Connect Hardware
- Connect radar's CLI port to Pi (usually appears as `/dev/ttyACM0`)
- Connect radar's data port to Pi (usually appears as `/dev/ttyACM1`)

### 4. Test Connection
```bash
ls -la /dev/ttyACM*
```
You should see both `/dev/ttyACM0` and `/dev/ttyACM1`

### 5. Run the Radar Test
```bash
python3 radar_test_simple.py
```

## Expected Output

When objects are detected, you'll see output like:
```
[14:23:45.123] Frame #1 - 2 objects detected:
--------------------------------------------------------------------------------
Obj  X(m)    Y(m)    Z(m)    V(m/s)  Range(m) Az(°)  El(°)
--------------------------------------------------------------------------------
0    1.234   2.456   0.123   -0.456  2.789    45.6   12.3
1    -0.987  1.654   0.321   0.234   1.987    -23.4  8.7
```

## Configuration

### Sensor Parameters
Edit `DEFAULT_SENSOR_CONFIG` in `radar_test_simple.py`:
- `X`, `Y`, `Z`: Sensor position in meters
- `yaw_psi`, `pitch_theta`, `roll_phi`: Sensor orientation in degrees
- `sensor_delay`: Processing delay between frames

### Radar Parameters
Modify `xwr18xx_profile_2023_07_26T08_46_17_507.cfg` for:
- Detection range and resolution
- Frame rate
- Antenna configuration

## Troubleshooting

### Permission Denied
```bash
sudo python3 radar_test_simple.py
```

### Serial Port Not Found
```bash
# Check USB connections
lsusb
# Check serial ports
ls -la /dev/tty*
```

### No Data Received
1. Verify radar is powered and connected
2. Check configuration file is valid
3. Ensure radar firmware is compatible

## File Descriptions

- `radar_test_simple.py` - Main test script (simplified version)
- `demo_XY_test.py` - Original full-featured script with networking
- `parcer_XY_test.py` - Radar data parser module
- `xwr18xx_profile_2023_07_26T08_46_17_507.cfg` - Radar configuration
- `requirements.txt` - Python dependencies
- `install_radar.sh` - Installation script

## Advanced Usage

For the full networking version with TCP/UDP:
```bash
python3 demo_XY_test.py
```

This requires proper network configuration and sensor parameter server. 