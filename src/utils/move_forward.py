#!/usr/bin/env python3
# File: move_forward.py

from pymavlink import mavutil
import time

print("🚁 Forward Movement Script")

# Connect to PX4 SITL
master = mavutil.mavlink_connection('udp:127.0.0.1:14540', source_system=255)
master.wait_heartbeat()

print("✅ Connected to PX4 SITL")

def send_position_target(x, y, z):
    """Send position target in NED coordinates"""
    master.mav.set_position_target_local_ned_send(
        0,  # time_boot_ms
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111111000,  # Position only
        x, y, z,     # Position NED (North, East, Down)
        0, 0, 0,     # Velocity (ignored)
        0, 0, 0,     # Acceleration (ignored)
        0, 0         # yaw, yaw_rate (ignored)
    )

def send_heartbeat():
    """Send heartbeat to maintain connection"""
    master.mav.heartbeat_send(
        mavutil.mavlink.MAV_TYPE_GCS,
        mavutil.mavlink.MAV_AUTOPILOT_INVALID,
        0, 0, mavutil.mavlink.MAV_STATE_ACTIVE
    )

# Main movement sequence
print("📍 Moving drone 5 meters forward (North)")
print("⏳ Sending position commands for 5 seconds...")

# Send position commands continuously for 5 seconds
for i in range(50):  # 50 commands at 10Hz = 5 seconds
    send_heartbeat()
    send_position_target(5.0, 0.0, -5.0)  # 5m North, 0m East, 5m Up
    time.sleep(0.1)  # 10Hz rate
    
    if i % 10 == 0:  # Progress update every second
        print(f"   Sending command {i+1}/50...")

print("✅ Forward movement commands complete!")
print("🎯 Drone should now be 5 meters north of starting position")

