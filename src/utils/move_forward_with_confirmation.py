#!/usr/bin/env python3
# File: move_forward_confirmed.py

from pymavlink import mavutil
import time
import threading
import math

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
        time.sleep(1)

def send_position_target(x, y, z):
    """Send position target in NED coordinates"""
    master.mav.set_position_target_local_ned_send(
        0, master.target_system, master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111111000,
        x, y, z, 0, 0, 0, 0, 0, 0, 0, 0
    )

def get_current_position():
    """Get current drone position"""
    msg = master.recv_match(type='LOCAL_POSITION_NED', blocking=True, timeout=3)
    if msg:
        return (msg.x, msg.y, msg.z)  # NED coordinates
    return None

def get_current_gps():
    """Get current GPS position for confirmation"""
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=3)
    if msg:
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.relative_alt / 1000.0
        return (lat, lon, alt)
    return None

def calculate_distance(pos1, pos2):
    """Calculate 3D distance between two positions"""
    if pos1 is None or pos2 is None:
        return float('inf')
    
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1] 
    dz = pos1[2] - pos2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def move_and_confirm(target_x, target_y, target_z, timeout=30, tolerance=1.0):
    """Move drone to target position and confirm arrival"""
    print(f"📍 Moving to: North={target_x}m, East={target_y}m, Down={target_z}m")
    
    # Get starting position
    start_pos = get_current_position()
    start_gps = get_current_gps()
    
    if start_pos:
        print(f"🏁 Starting position: N={start_pos[0]:.2f}, E={start_pos[1]:.2f}, D={start_pos[2]:.2f}")
    if start_gps:
        print(f"🌍 Starting GPS: {start_gps[0]:.6f}, {start_gps[1]:.6f}, Alt={start_gps[2]:.1f}m")
    
    start_time = time.time()
    last_position = start_pos
    movement_detected = False
    target_reached = False
    
    while time.time() - start_time < timeout:
        # Send position command
        send_position_target(target_x, target_y, target_z)
        
        # Get current position
        current_pos = get_current_position()
        current_gps = get_current_gps()
        
        if current_pos:
            # Check if drone is moving
            if last_position and calculate_distance(current_pos, last_position) > 0.1:
                if not movement_detected:
                    print("✅ Movement detected!")
                    movement_detected = True
            
            # Display current position every 2 seconds
            elapsed = time.time() - start_time
            if int(elapsed) % 2 == 0 and elapsed > 1:
                print(f"📈 Current: N={current_pos[0]:.2f}, E={current_pos[1]:.2f}, D={current_pos[2]:.2f}")
                if current_gps:
                    print(f"🌍 GPS: {current_gps[0]:.6f}, {current_gps[1]:.6f}, Alt={current_gps[2]:.1f}m")
            
            # Check if target reached
            distance_to_target = calculate_distance(current_pos, (target_x, target_y, target_z))
            if distance_to_target < tolerance:
                target_reached = True
                print(f"🎯 Target reached! Distance to target: {distance_to_target:.2f}m")
                break
            
            last_position = current_pos
        
        time.sleep(0.2)  # 5Hz rate
    
    # Final status
    final_pos = get_current_position()
    final_gps = get_current_gps()
    
    if final_pos and start_pos:
        total_distance = calculate_distance(final_pos, start_pos)
        print(f"\n📊 Movement Summary:")
        print(f"   🏁 Start: N={start_pos[0]:.2f}, E={start_pos[1]:.2f}, D={start_pos[2]:.2f}")
        print(f"   🏁 End:   N={final_pos[0]:.2f}, E={final_pos[1]:.2f}, D={final_pos[2]:.2f}")
        print(f"   📏 Total distance moved: {total_distance:.2f}m")
        print(f"   🎯 Target reached: {'YES' if target_reached else 'NO'}")
    
    if final_gps and start_gps:
        print(f"📍 GPS Change:")
        print(f"   Start GPS: {start_gps[0]:.6f}, {start_gps[1]:.6f}")
        print(f"   End GPS:   {final_gps[0]:.6f}, {final_gps[1]:.6f}")
        
        # Calculate GPS distance (rough approximation)
        lat_diff = (final_gps[0] - start_gps[0]) * 111320  # meters per degree lat
        lon_diff = (final_gps[1] - start_gps[1]) * 111320 * math.cos(math.radians(start_gps[0]))
        gps_distance = math.sqrt(lat_diff**2 + lon_diff**2)
        print(f"   📏 GPS distance moved: {gps_distance:.2f}m")
    
    return target_reached, movement_detected

def main():
    global master, keep_connection
    
    print("🚁 Smart Forward Movement Script with Confirmation")
    
    # Connect to PX4 SITL
    master = mavutil.mavlink_connection('udp:127.0.0.1:14540', source_system=255)
    master.wait_heartbeat()
    
    print("✅ Connected to PX4 SITL")
    
    # Start heartbeat thread
    heartbeat_worker = threading.Thread(target=heartbeat_thread, daemon=True)
    heartbeat_worker.start()
    
    print("💓 Heartbeat started - stabilizing connection...")
    time.sleep(3)
    
    try:
        # Move forward 5 meters
        target_reached, movement_detected = move_and_confirm(
            target_x=5.0,   # 5 meters forward (North)
            target_y=0.0,   # 0 meters sideways
            target_z=-5.0,  # 5 meters altitude
            timeout=30,     # 30 second timeout
            tolerance=1.0   # 1 meter tolerance
        )
        
        if target_reached:
            print("\n🎉 SUCCESS: Drone reached target position!")
        elif movement_detected:
            print("\n⚠️ PARTIAL: Drone moved but didn't reach exact target")
        else:
            print("\n❌ FAILED: No movement detected")
            print("💡 Possible causes:")
            print("   - Drone not armed or in air")
            print("   - Position mode not available")
            print("   - MAVLink commands not accepted")
        
        # Keep connection alive briefly
        print("\n⏳ Maintaining connection for 5 seconds...")
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("\n🛑 Movement interrupted by user")
    
    finally:
        keep_connection = False
        print("👋 Ending connection")

if __name__ == "__main__":
    main()

