#!/usr/bin/env python3

from pymavlink import mavutil
import time

class DroneController:
    def __init__(self, connection_string='udp:127.0.0.1:14540'):
        """Initialize MAVLink connection to PX4 SITL"""
        print(f"🔗 Connecting to {connection_string}...")
        self.master = mavutil.mavlink_connection(connection_string)
        
        # Wait for heartbeat
        print("⏳ Waiting for heartbeat...")
        self.master.wait_heartbeat()
        print(f"✅ Connected! System {self.master.target_system}, Component {self.master.target_component}")
    
    def get_status(self):
        """Get current drone status"""
        msg = self.master.recv_match(type='HEARTBEAT', blocking=True, timeout=5)
        if msg:
            armed = msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
            mode = mavutil.mode_string_v10(msg)
            print(f"📊 Status: {'ARMED' if armed else 'DISARMED'}, Mode: {mode}")
            return armed, mode
        return None, None
    
    def arm(self):
        """Arm the drone"""
        print("🔓 Arming drone...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 1, 0, 0, 0, 0, 0, 0)
        
        # Wait for acknowledgment
        ack = self.master.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
        if ack and ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
            print("✅ Drone ARMED successfully!")
        else:
            print(f"❌ Failed to arm: {ack.result if ack else 'No response'}")
    
    def disarm(self):
        """Disarm the drone"""
        print("🔒 Disarming drone...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 0, 0, 0, 0, 0, 0, 0)
        print("✅ Drone DISARMED")
    
    def takeoff(self, altitude=5.0):
        """Takeoff to specified altitude"""
        print(f"🚁 Taking off to {altitude}m...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0, 0, 0, 0, 0, 0, 0, altitude)
        print("✅ Takeoff command sent")
    
    def land(self):
        """Land the drone"""
        print("🛬 Landing...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0, 0, 0, 0, 0, 0, 0, 0)
        print("✅ Land command sent")
    
    def get_gps_position(self):
        """Get current GPS position"""
        msg = self.master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
        if msg:
            lat = msg.lat / 1e7
            lon = msg.lon / 1e7
            alt = msg.alt / 1000.0
            print(f"📍 GPS Position: Lat={lat:.6f}, Lon={lon:.6f}, Alt={alt:.1f}m")
            return lat, lon, alt
        else:
            print("❌ No GPS data received")
            return None, None, None
    
    def monitor_gps(self, duration=10):
        """Monitor GPS data for specified duration"""
        print(f"📡 Monitoring GPS for {duration} seconds...")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            self.get_gps_position()
            time.sleep(1)

# Example usage
if __name__ == "__main__":
    try:
        # Create drone controller
        drone = DroneController()
        
        # Check initial status
        drone.get_status()
        
        # Get current GPS position
        drone.get_gps_position()
        
        # Basic flight test
        print("\n🧪 Starting basic flight test...")
        
        # Arm the drone
        drone.arm()
        time.sleep(2)
        
        # Check status after arming
        drone.get_status()
        
        # Takeoff
        drone.takeoff(3.0)
        time.sleep(5)
        
        # Monitor GPS during flight
        drone.monitor_gps(10)
        
        # Land
        drone.land()
        time.sleep(5)
        
        # Disarm
        drone.disarm()
        
        print("✅ Flight test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure PX4 SITL is running and accessible on port 14540")
