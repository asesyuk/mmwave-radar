#!/usr/bin/env python3
"""
Simplified mmWave Radar Test Script for Raspberry Pi
This version prints detected objects locally for testing
"""

import os
import sys
import serial
import time
import numpy as np
from datetime import datetime
from parcer_XY_test import parser_one_mmw_demo_output_packet

# Default sensor parameters (can be modified as needed)
DEFAULT_SENSOR_CONFIG = {
    'ID': 1,
    'X': 0.0,      # X position in meters
    'Y': 0.0,      # Y position in meters  
    'Z': 1.0,      # Z position in meters (height)
    'sensor_delay': 0.1,  # Processing delay in seconds
    'yaw_psi': 0.0,       # Yaw angle in degrees
    'pitch_theta': 0.0,   # Pitch angle in degrees
    'roll_phi': 0.0       # Roll angle in degrees
}

def setup_radar_ports():
    """Setup serial connections to radar"""
    try:
        # CLI port for configuration
        cli_port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        # Data port for radar data
        data_port = serial.Serial('/dev/ttyACM1', 921600, timeout=1)
        print("✓ Serial ports connected successfully")
        return cli_port, data_port
    except Exception as e:
        print(f"✗ Error connecting to serial ports: {e}")
        print("Make sure radar is connected and ports are available")
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

def parse_radar_config(config_file):
    """Parse configuration file to extract radar parameters"""
    config_params = {}
    
    try:
        with open(config_file, 'r') as f:
            config_lines = [line.rstrip('\r\n') for line in f]
        
        for line in config_lines:
            if line.strip() and not line.startswith('%'):
                parts = line.split()
                if len(parts) > 1:
                    if "profileCfg" in parts[0]:
                        config_params['numAdcSamples'] = int(parts[10])
                    elif "frameCfg" in parts[0]:
                        config_params['framePeriodicity'] = int(parts[5])
        
        return config_params
    except Exception as e:
        print(f"Warning: Could not parse config file: {e}")
        return {}

def main():
    """Main radar data processing loop"""
    config_file = 'xwr18xx_profile_2023_07_26T08_46_17_507.cfg'
    
    print("=" * 60)
    print("mmWave Radar Data Extraction - Raspberry Pi")
    print("=" * 60)
    
    # Check if config file exists
    if not os.path.exists(config_file):
        print(f"✗ Configuration file '{config_file}' not found!")
        return
    
    # Setup serial ports
    cli_port, data_port = setup_radar_ports()
    if not cli_port or not data_port:
        return
    
    try:
        # Send configuration to radar
        if not send_config_to_radar(cli_port, config_file):
            return
        
        # Parse config parameters
        config_params = parse_radar_config(config_file)
        
        # Get sensor configuration
        sensor_config = DEFAULT_SENSOR_CONFIG.copy()
        
        print("\nSensor Configuration:")
        for key, value in sensor_config.items():
            print(f"  {key}: {value}")
        
        print(f"\n{'='*60}")
        print("Starting radar data acquisition...")
        print("Press Ctrl+C to stop")
        print(f"{'='*60}")
        print()
        
        frame_count = 0
        no_data_count = 0
        data_buffer = bytearray()  # Buffer to accumulate data
        
        while True:
            # Read available data from radar
            byte_count = data_port.inWaiting()
            if byte_count > 0:
                new_data = data_port.read(byte_count)
                data_buffer.extend(new_data)  # Add to buffer
                no_data_count = 0  # Reset counter when we get data
                
                # Only process if we have enough data for at least a header
                if len(data_buffer) > 40:
                    # Parse the radar data
                    try:
                        result = parser_one_mmw_demo_output_packet(
                            data_buffer, 
                            len(data_buffer),
                            sensor_config['ID'],
                            sensor_config['X'],
                            sensor_config['Y'], 
                            sensor_config['Z'],
                            sensor_config['yaw_psi'],
                            sensor_config['pitch_theta'],
                            sensor_config['roll_phi']
                        )
                        
                        (parser_result, header_start, total_bytes, num_objects, 
                         num_tlv, subframe, x_array, y_array, z_array, v_array,
                         range_array, azimuth_array, elevation_array, 
                         snr_array, noise_array) = result
                        
                        if parser_result == 0:
                            frame_count += 1
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            
                            # Remove processed data from buffer
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
                                # Only show "no objects" message occasionally to avoid spam
                                if frame_count % 50 == 0:  # Show every 50th frame
                                    print(f"[{timestamp}] Frame #{frame_count} - No objects detected")
                        else:
                            # Parser failed - might be incomplete data, just continue
                            # Keep buffer but limit its size to prevent memory issues
                            if len(data_buffer) > 10000:  # 10KB limit
                                data_buffer = data_buffer[-5000:]  # Keep last 5KB
                    
                    except Exception as e:
                        print(f"Parser error: {e}")
                        # Clear buffer on serious errors
                        data_buffer = bytearray()
            
            else:
                # No data available, increment counter
                no_data_count += 1
                if no_data_count % 100 == 0:  # Show status every 10 seconds (100 * 0.1s)
                    print(".", end="", flush=True)  # Show we're still running
            
            # Small delay to prevent overwhelming the system
            time.sleep(sensor_config['sensor_delay'])
    
    except KeyboardInterrupt:
        print(f"\n\nStopping radar... Processed {frame_count} frames")
    
    except Exception as e:
        print(f"Error during operation: {e}")
    
    finally:
        # Clean up
        if cli_port:
            cli_port.close()
        if data_port:
            data_port.close()
        print("✓ Serial ports closed")

if __name__ == "__main__":
    main() 