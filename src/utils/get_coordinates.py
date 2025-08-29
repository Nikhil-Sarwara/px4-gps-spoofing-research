#!/usr/bin/env python3
"""
Print PX4 GPS coordinates (latitude, longitude, altitude AGL).

Prerequisites
-------------
1. pip install pymavlink
2. PX4 SITL running (default UDP port 14540).

Usage
-----
python3 print_gps.py
"""

from pymavlink import mavutil
import time

def main():
    # Connect to PX4 SITL (adjust port if you changed it)
    master = mavutil.mavlink_connection('udp:127.0.0.1:14540')
    print("🔗 Waiting for vehicle heartbeat …")
    master.wait_heartbeat()
    print(f"✅ Heartbeat received from system {master.target_system}")

    while True:
        # Wait for a GLOBAL_POSITION_INT message (has lat/lon/alt) [215]
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if not msg:
            continue

        # Convert to human-readable units
        lat_deg = msg.lat / 1e7      # degrees
        lon_deg = msg.lon / 1e7      # degrees
        alt_m  = msg.relative_alt / 1000.0   # millimetres → metres (relative to home)

        print(f"🌍  Lat: {lat_deg:.7f}°,  Lon: {lon_deg:.7f}°,  Alt: {alt_m:.2f} m")
        time.sleep(1)  # print at 1 Hz

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Exiting.")

