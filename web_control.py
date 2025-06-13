#!/usr/bin/env python3
"""
Web Control Panel for mmWave Radar
Allows remote start/stop and configuration of radar parameters
"""

import os
import sys
import json
import subprocess
import signal
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
import threading
import queue

app = Flask(__name__)

# Global variables
radar_process = None
radar_data_queue = queue.Queue()
current_config = {
    'ID': 1,
    'X': 0.0,
    'Y': 0.0,
    'Z': 1.0,
    'sensor_delay': 0.1,
    'yaw_psi': 0.0,
    'pitch_theta': 0.0,
    'roll_phi': 0.0,
    'name': 'Radar Sensor 1',
    'description': 'Main entrance radar'
}

CONFIG_FILE = 'radar_config.json'

def load_config():
    """Load configuration from JSON file"""
    global current_config
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                current_config.update(json.load(f))
    except Exception as e:
        print(f"Error loading config: {e}")

def save_config():
    """Save configuration to JSON file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(current_config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def is_radar_running():
    """Check if radar process is running"""
    global radar_process
    return radar_process is not None and radar_process.poll() is None

def start_radar():
    """Start the radar process"""
    global radar_process
    try:
        if is_radar_running():
            return False, "Radar is already running"
        
        # Create a modified radar script with current config
        create_radar_script_with_config()
        
        # Start the radar process (allow output to terminal)
        radar_process = subprocess.Popen(
            ['python3', 'radar_configured.py'],
            stdout=None,  # Let output go to terminal
            stderr=None,  # Let errors go to terminal  
            text=True
        )
        
        time.sleep(1)  # Give it a moment to start
        
        if radar_process.poll() is None:
            return True, "Radar started successfully"
        else:
            return False, "Radar failed to start"
            
    except Exception as e:
        return False, f"Error starting radar: {str(e)}"

def stop_radar():
    """Stop the radar process"""
    global radar_process
    try:
        if not is_radar_running():
            return False, "Radar is not running"
        
        radar_process.terminate()
        time.sleep(2)
        
        if radar_process.poll() is None:
            radar_process.kill()
            
        radar_process = None
        return True, "Radar stopped successfully"
        
    except Exception as e:
        return False, f"Error stopping radar: {str(e)}"

def create_radar_script_with_config():
    """Create a radar script with current configuration"""
    script_content = f'''#!/usr/bin/env python3
# Auto-generated radar script with current configuration
# Generated at: {datetime.now()}

import os
import sys
import serial
import time
import numpy as np
from datetime import datetime
from parcer_XY_test import parser_one_mmw_demo_output_packet

# Current sensor configuration
SENSOR_CONFIG = {current_config}

def setup_radar_ports():
    """Setup serial connections to radar"""
    try:
        cli_port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        data_port = serial.Serial('/dev/ttyACM1', 921600, timeout=1)
        print("✓ Serial ports connected successfully")
        return cli_port, data_port
    except Exception as e:
        print(f"✗ Error connecting to serial ports: {{e}}")
        return None, None

def send_config_to_radar(cli_port, config_file):
    """Send configuration commands to radar"""
    try:
        with open(config_file, 'r') as f:
            config_lines = [line.rstrip('\\r\\n') for line in f]
        
        print(f"Sending {{len(config_lines)}} configuration commands...")
        for i, line in enumerate(config_lines):
            if line.strip() and not line.startswith('%'):
                cli_port.write((line + '\\n').encode())
                print(f"  {{i+1:2d}}: {{line}}")
                time.sleep(0.01)
        
        print("✓ Configuration sent successfully")
        return True
    except Exception as e:
        print(f"✗ Error sending configuration: {{e}}")
        return False

def main():
    """Main radar processing loop"""
    config_file = 'xwr18xx_profile_2023_07_26T08_46_17_507.cfg'
    
    print("=" * 60)
    print("mmWave Radar - Web Controlled")
    print("=" * 60)
    print(f"Sensor: {{SENSOR_CONFIG['name']}}")
    print(f"Position: X={{SENSOR_CONFIG['X']}}, Y={{SENSOR_CONFIG['Y']}}, Z={{SENSOR_CONFIG['Z']}}")
    print(f"Orientation: Yaw={{SENSOR_CONFIG['yaw_psi']}}°, Pitch={{SENSOR_CONFIG['pitch_theta']}}°, Roll={{SENSOR_CONFIG['roll_phi']}}°")
    print("=" * 60)
    
    if not os.path.exists(config_file):
        print(f"✗ Configuration file '{{config_file}}' not found!")
        return
    
    cli_port, data_port = setup_radar_ports()
    if not cli_port or not data_port:
        return
    
    try:
        if not send_config_to_radar(cli_port, config_file):
            return
        
        print("\\nStarting radar data acquisition...")
        print("Use web interface to stop")
        print("=" * 60)
        
        frame_count = 0
        no_data_count = 0
        data_buffer = bytearray()
        
        while True:
            byte_count = data_port.inWaiting()
            if byte_count > 0:
                new_data = data_port.read(byte_count)
                data_buffer.extend(new_data)
                no_data_count = 0
                
                if len(data_buffer) > 40:
                    try:
                        result = parser_one_mmw_demo_output_packet(
                            data_buffer, 
                            len(data_buffer),
                            SENSOR_CONFIG['ID'],
                            SENSOR_CONFIG['X'],
                            SENSOR_CONFIG['Y'], 
                            SENSOR_CONFIG['Z'],
                            SENSOR_CONFIG['yaw_psi'],
                            SENSOR_CONFIG['pitch_theta'],
                            SENSOR_CONFIG['roll_phi']
                        )
                        
                        (parser_result, header_start, total_bytes, num_objects, 
                         num_tlv, subframe, x_array, y_array, z_array, v_array,
                         range_array, azimuth_array, elevation_array, 
                         snr_array, noise_array) = result
                        
                        if parser_result == 0:
                            frame_count += 1
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            
                            if header_start >= 0 and total_bytes > 0:
                                bytes_to_remove = header_start + total_bytes
                                data_buffer = data_buffer[bytes_to_remove:]
                            
                            if num_objects > 0:
                                print(f"\\n[{{timestamp}}] Frame #{{frame_count}} - {{num_objects}} objects detected:")
                                print("-" * 80)
                                print(f"{{'Obj':<4}} {{'X(m)':<8}} {{'Y(m)':<8}} {{'Z(m)':<8}} {{'V(m/s)':<8}} {{'Range(m)':<8}} {{'Az(°)':<7}} {{'El(°)':<7}}")
                                print("-" * 80)
                                
                                for i in range(num_objects):
                                    print(f"{{i:<4}} {{x_array[i]:<8.3f}} {{y_array[i]:<8.3f}} {{z_array[i]:<8.3f}} "
                                          f"{{v_array[i]:<8.3f}} {{range_array[i]:<8.3f}} {{azimuth_array[i]:<7.1f}} "
                                          f"{{elevation_array[i]:<7.1f}}")
                            else:
                                if frame_count % 50 == 0:
                                    print(f"[{{timestamp}}] Frame #{{frame_count}} - No objects detected")
                        else:
                            if len(data_buffer) > 10000:
                                data_buffer = data_buffer[-5000:]
                    
                    except Exception as e:
                        print(f"Parser error: {{e}}")
                        data_buffer = bytearray()
            else:
                no_data_count += 1
                if no_data_count % 100 == 0:
                    print(".", end="", flush=True)
            
            time.sleep(SENSOR_CONFIG['sensor_delay'])
    
    except KeyboardInterrupt:
        print(f"\\n\\nStopping radar... Processed {{frame_count}} frames")
    except Exception as e:
        print(f"Error during operation: {{e}}")
    finally:
        if cli_port:
            cli_port.close()
        if data_port:
            data_port.close()
        print("✓ Serial ports closed")

if __name__ == "__main__":
    main()
'''
    
    with open('radar_configured.py', 'w') as f:
        f.write(script_content)
    
    os.chmod('radar_configured.py', 0o755)

# Web Routes
@app.route('/')
def index():
    """Main control panel"""
    return render_template('index.html', 
                         config=current_config, 
                         radar_running=is_radar_running(),
                         current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/status')
def api_status():
    """Get current radar status"""
    return jsonify({
        'running': is_radar_running(),
        'config': current_config,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/start', methods=['POST'])
def api_start():
    """Start radar"""
    success, message = start_radar()
    return jsonify({'success': success, 'message': message})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    """Stop radar"""
    success, message = stop_radar()
    return jsonify({'success': success, 'message': message})

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """Get or update configuration"""
    global current_config
    
    if request.method == 'GET':
        return jsonify(current_config)
    
    elif request.method == 'POST':
        try:
            new_config = request.json
            
            # Validate numeric values
            for key in ['ID', 'X', 'Y', 'Z', 'sensor_delay', 'yaw_psi', 'pitch_theta', 'roll_phi']:
                if key in new_config:
                    current_config[key] = float(new_config[key])
            
            # Update string values
            for key in ['name', 'description']:
                if key in new_config:
                    current_config[key] = str(new_config[key])
            
            # Save to file
            if save_config():
                return jsonify({'success': True, 'message': 'Configuration updated successfully'})
            else:
                return jsonify({'success': False, 'message': 'Failed to save configuration'})
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error updating configuration: {str(e)}'})

@app.route('/config')
def config_page():
    """Configuration page"""
    return render_template('config.html', config=current_config)

def init_app():
    """Initialize the application"""
    load_config()
    
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')

if __name__ == '__main__':
    init_app()
    # Try different ports if 5000 is in use (common on macOS due to AirPlay)
    ports_to_try = [5000, 5001, 8000, 8080, 8888]
    
    print("=" * 60)
    print("mmWave Radar Web Control Panel")
    print("=" * 60)
    print("Starting web server...")
    
    for port in ports_to_try:
        try:
            import socket
            # Test if port is available
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result != 0:  # Port is available
                print(f"Access at: http://your-device-ip:{port}")
                print(f"Local access: http://localhost:{port}")
                print("=" * 60)
                app.run(host='0.0.0.0', port=port, debug=False)
                break
            else:
                print(f"Port {port} is in use, trying next...")
        except Exception as e:
            print(f"Error testing port {port}: {e}")
            continue
    else:
        print("ERROR: No available ports found!")
        print("On macOS, try disabling AirPlay Receiver in System Settings") 