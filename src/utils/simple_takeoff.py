#!/usr/bin/env python3

from pymavlink import mavutil
import time

# Connect to PX4 SITL MAVLink
master = mavutil.mavlink_connection('udp:127.0.0.1:14540', source_system=255, source_component=0)

print("🔗 Connecting to PX4 SITL...")
master.wait_heartbeat()
print("✅ Heartbeat received - connected to system", master.target_system)

# Send heartbeat to establish communication with PX4
def send_heartbeat():
    master.mav.heartbeat_send(
        mavutil.mavlink.MAV_TYPE_GCS,      # Ground Control Station
        mavutil.mavlink.MAV_AUTOPILOT_INVALID,
        0, 0, mavutil.mavlink.MAV_STATE_ACTIVE
    )

send_heartbeat()
time.sleep(1)

# Arm the drone
print("🔓 Arming the drone...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 1, 0, 0, 0, 0, 0, 0
)

# Wait for acknowledgement
ack = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=5)
if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
    print("✅ Drone armed successfully!")
else:
    print("❌ Failed to arm drone")
    exit(1)

# Takeoff command
altitude = 5.0  # meters
print(f"🚁 Taking off to {altitude} meters...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0, 0, 0, 0, 0, 0, 0, altitude
)

print("✅ Takeoff command sent. Waiting for the drone to ascend...")

# Monitor altitude for 15 seconds
start_time = time.time()
while time.time() - start_time < 15:
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=2)
    if msg:
        relative_alt = msg.relative_alt / 1000.0  # convert mm to meters
        print(f"📈 Altitude: {relative_alt:.2f} m")
    else:
        print("❌ No altitude data received")
    time.sleep(1)

print("✅ Takeoff sequence complete!")
