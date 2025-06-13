#!/usr/bin/env python3
# Auto-generated radar script with current configuration
# Generated at: 2025-06-13 15:27:11.312188

import os
import sys
import serial
import time
import numpy as np
from datetime import datetime
from parcer_XY_test import parser_one_mmw_demo_output_packet

# Current sensor configuration
SENSOR_CONFIG = {'ID': 1, 'X': 0.0, 'Y': 0.0, 'Z': 1.0, 'sensor_delay': 0.1, 'yaw_psi': 0.0, 'pitch_theta': 0.0, 'roll_phi': 0.0, 'name': 'Radar Sensor 1', 'description': 'Main entrance radar'}

def setup_radar_ports():
    """Setup serial connections to radar"""
    try:
        cli_port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        data_port = serial.Serial('/dev/ttyACM1', 921600, timeout=1)
        print("✓ Serial ports connected successfully")
        return cli_port, data_port
    except Exception as e:
        print(f"✗ Error connecting to serial ports: {e}")
        return None, None

def send_config_to_radar(cli_port, config_file):
    """Send configuration commands to radar"""
    try:
        with open(config_file, 'r') as f:
            config_lines = [line.rstrip('\r\n') for line in f]
        
        print(f"Sending {len(config_lines)} configuration commands...")
        for i, line in enumerate(config_lines):
            if line.strip() and not line.startswith('%'):
                cli_port.write((line + '\n').encode())
                print(f"  {i+1:2d}: {line}")
                time.sleep(0.01)
        
        print("✓ Configuration sent successfully")
        return True
    except Exception as e:
        print(f"✗ Error sending configuration: {e}")
        return False

def main():
    """Main radar processing loop"""
    config_file = 'xwr18xx_profile_2023_07_26T08_46_17_507.cfg'
    
    print("=" * 60)
    print("mmWave Radar - Web Controlled")
    print("=" * 60)
    print(f"Sensor: {SENSOR_CONFIG['name']}")
    print(f"Position: X={SENSOR_CONFIG['X']}, Y={SENSOR_CONFIG['Y']}, Z={SENSOR_CONFIG['Z']}")
    print(f"Orientation: Yaw={SENSOR_CONFIG['yaw_psi']}°, Pitch={SENSOR_CONFIG['pitch_theta']}°, Roll={SENSOR_CONFIG['roll_phi']}°")
    print("=" * 60)
    
    if not os.path.exists(config_file):
        print(f"✗ Configuration file '{config_file}' not found!")
        return
    
    cli_port, data_port = setup_radar_ports()
    if not cli_port or not data_port:
        return
    
    try:
        if not send_config_to_radar(cli_port, config_file):
            return
        
        print("\nStarting radar data acquisition...")
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
                                print(f"\n[{timestamp}] Frame #{frame_count} - {num_objects} objects detected:")
                                print("-" * 80)
                                print(f"{'Obj':<4} {'X(m)':<8} {'Y(m)':<8} {'Z(m)':<8} {'V(m/s)':<8} {'Range(m)':<8} {'Az(°)':<7} {'El(°)':<7}")
                                print("-" * 80)
                                
                                for i in range(num_objects):
                                    print(f"{i:<4} {x_array[i]:<8.3f} {y_array[i]:<8.3f} {z_array[i]:<8.3f} "
                                          f"{v_array[i]:<8.3f} {range_array[i]:<8.3f} {azimuth_array[i]:<7.1f} "
                                          f"{elevation_array[i]:<7.1f}")
                            else:
                                if frame_count % 50 == 0:
                                    print(f"[{timestamp}] Frame #{frame_count} - No objects detected")
                        else:
                            if len(data_buffer) > 10000:
                                data_buffer = data_buffer[-5000:]
                    
                    except Exception as e:
                        print(f"Parser error: {e}")
                        data_buffer = bytearray()
            else:
                no_data_count += 1
                if no_data_count % 100 == 0:
                    print(".", end="", flush=True)
            
            time.sleep(SENSOR_CONFIG['sensor_delay'])
    
    except KeyboardInterrupt:
        print(f"\n\nStopping radar... Processed {frame_count} frames")
    except Exception as e:
        print(f"Error during operation: {e}")
    finally:
        if cli_port:
            cli_port.close()
        if data_port:
            data_port.close()
        print("✓ Serial ports closed")

if __name__ == "__main__":
    main()
