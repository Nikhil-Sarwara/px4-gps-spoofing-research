#!/usr/bin/env python3
# File: working_mavlink.py

from pymavlink import mavutil
import time

# Connect with specific source system/component IDs
master = mavutil.mavlink_connection(
    'udp:127.0.0.1:14540',
    source_system=255,      # Use standard GCS system ID
    source_component=0      # Use standard component ID
)

print("🔗 Waiting for heartbeat...")
master.wait_heartbeat()
print(f"✅ Connected to System {master.target_system}")

# IMPORTANT: Send initial heartbeat so PX4 knows where we are
def send_heartbeat():
    master.mav.heartbeat_send(
        mavutil.mavlink.MAV_TYPE_GCS,      # Type: Ground Control Station
        mavutil.mavlink.MAV_AUTOPILOT_INVALID,
        0, 0, mavutil.mavlink.MAV_STATE_ACTIVE
    )

# Send heartbeat first
print("💓 Sending heartbeat to establish connection...")
send_heartbeat()
time.sleep(1)

# Test command with acknowledgment
print("📋 Testing command with response...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES,
    0, 1, 0, 0, 0, 0, 0, 0
)

# Listen for acknowledgment
print("👂 Waiting for command acknowledgment...")
for i in range(10):
    msg = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=2)
    if msg:
        print(f"✅ Command acknowledged! Result: {msg.result}")
        break
    print(f"   Attempt {i+1}/10...")

# If we get here with acknowledgment, MAVLink is fully working
print("🎉 MAVLink communication is working!")

# Now test basic commands
def test_arm():
    print("\n🔓 Testing ARM command...")
    
    # Send heartbeat first
    send_heartbeat()
    time.sleep(0.5)
    
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 1, 0, 0, 0, 0, 0, 0
    )
    
    # Wait for ACK
    ack = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=5)
    if ack:
        if ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
            print("✅ ARM command ACCEPTED!")
            return True
        else:
            print(f"❌ ARM command rejected: {ack.result}")
            return False
    else:
        print("❌ No response to ARM command")
        return False

# Test the arm command
test_arm()

