#!/usr/bin/env python3
# File: move_forward_stable.py

from pymavlink import mavutil
import time
import threading

# Global variables
master = None
keep_connection = True

def heartbeat_thread():
    """Continuously send heartbeats to maintain connection"""
    global master, keep_connection
    
    while keep_connection:
        if master:
            master.mav.heartbeat_send(
                mavutil.mavlink.MAV_TYPE_GCS,
                mavutil.mavlink.MAV_AUTOPILOT_INVALID,
                0, 0, mavutil.mavlink.MAV_STATE_ACTIVE
            )
        time.sleep(1)  # Send heartbeat every second

def send_position_target(x, y, z):
    """Send position target in NED coordinates"""
    master.mav.set_position_target_local_ned_send(
        0, master.target_system, master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111111000,  # Position only
        x, y, z, 0, 0, 0, 0, 0, 0, 0, 0
    )

def main():
    global master, keep_connection
    
    print("🚁 Stable Forward Movement Script")
    
    # Connect to PX4 SITL
    master = mavutil.mavlink_connection('udp:127.0.0.1:14540', source_system=255)
    master.wait_heartbeat()
    
    print("✅ Connected to PX4 SITL")
    
    # Start heartbeat thread to maintain connection
    heartbeat_worker = threading.Thread(target=heartbeat_thread, daemon=True)
    heartbeat_worker.start()
    
    print("💓 Heartbeat thread started - connection should be stable now")
    time.sleep(3)  # Let connection stabilize
    
    try:
        print("📍 Moving drone 5 meters forward...")
        
        # Send position commands continuously for 10 seconds
        for i in range(100):  # 100 commands at 10Hz = 10 seconds
            send_position_target(5.0, 0.0, -5.0)  # 5m North, 0m East, 5m Up
            time.sleep(0.1)
            
            if i % 10 == 0:
                print(f"   Sending command {i+1}/100...")
        
        print("✅ Movement commands complete!")
        print("🎯 Drone should now be 5 meters forward")
        
        # Keep connection alive for a bit longer
        print("⏳ Maintaining connection for 5 more seconds...")
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("\n🛑 Movement interrupted by user")
    
    finally:
        keep_connection = False
        print("👋 Ending connection")

if __name__ == "__main__":
    main()

