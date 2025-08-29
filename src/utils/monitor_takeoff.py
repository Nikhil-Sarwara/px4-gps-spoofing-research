#!/usr/bin/env python3
# File: monitor_takeoff.py

from pymavlink import mavutil
import time

# Connect to PX4 SITL
master = mavutil.mavlink_connection('udp:127.0.0.1:14540')
master.wait_heartbeat()

print("✅ Connected to PX4 SITL - Monitoring takeoff...")
print("📋 Start takeoff manually in PX4 console with: commander takeoff")
print("=" * 50)

# Monitor altitude and status
start_time = time.time()
max_alt = 0

while True:
    try:
        # Get position data
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=2)
        if msg:
            relative_alt = msg.relative_alt / 1000.0  # mm to meters
            lat = msg.lat / 1e7
            lon = msg.lon / 1e7
            
            if relative_alt > max_alt:
                max_alt = relative_alt
            
            print(f"🚁 Alt: {relative_alt:.2f}m | Max: {max_alt:.2f}m | GPS: {lat:.6f}, {lon:.6f}")
        
        # Get heartbeat for status
        heartbeat = master.recv_match(type='HEARTBEAT', blocking=False)
        if heartbeat:
            armed = heartbeat.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
            mode = mavutil.mode_string_v10(heartbeat)
            print(f"📊 Status: {'ARMED' if armed else 'DISARMED'} | Mode: {mode}")
            
        time.sleep(1)
        
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(1)

