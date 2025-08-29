#!/usr/bin/env python3

from pymavlink import mavutil
import time

def test_connection():
    print("=== Basic MAVLink Connection Test ===")
    
    # Try different connection methods
    connections_to_try = [
        'udp:127.0.0.1:14540',  # Offboard API
        'udp:127.0.0.1:14550',  # QGroundControl port
        'tcp:127.0.0.1:5760',   # TCP connection
        'udp:127.0.0.1:18570'   # Additional MAVLink stream
    ]
    
    for conn_str in connections_to_try:
        print(f"\n🔍 Testing connection: {conn_str}")
        try:
            # Create connection with timeout
            master = mavutil.mavlink_connection(conn_str, timeout=5)
            
            # Try to get a heartbeat
            print("   ⏳ Waiting for heartbeat...")
            msg = master.recv_match(type='HEARTBEAT', blocking=True, timeout=10)
            
            if msg:
                print(f"   ✅ SUCCESS! Heartbeat received from system {msg.get_srcSystem()}")
                print(f"      - System ID: {msg.get_srcSystem()}")
                print(f"      - Component ID: {msg.get_srcComponent()}")
                print(f"      - Vehicle Type: {msg.type}")
                print(f"      - Autopilot: {msg.autopilot}")
                
                # Try to get more data
                print("   📡 Testing data reception...")
                for i in range(3):
                    any_msg = master.recv_match(blocking=True, timeout=3)
                    if any_msg:
                        print(f"      📨 Received: {any_msg.get_type()}")
                    else:
                        print(f"      ❌ No data on attempt {i+1}")
                
                return master, conn_str
            else:
                print("   ❌ No heartbeat received")
                
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
        
        # Clean up
        try:
            master.close()
        except:
            pass
    
    print("\n❌ All connection attempts failed!")
    return None, None

if __name__ == "__main__":
    connection, connection_string = test_connection()
    
    if connection:
        print(f"\n🎉 Successfully connected via: {connection_string}")
        print("\nPress Ctrl+C to exit...")
        
        # Keep listening for messages
        try:
            while True:
                msg = connection.recv_match(blocking=True, timeout=5)
                if msg:
                    print(f"📨 {msg.get_type()}: {msg}")
                else:
                    print("⏳ No messages...")
                    
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
    else:
        print("\n❌ Could not establish MAVLink connection")
        print("\nTroubleshooting steps:")
        print("1. Make sure PX4 SITL is running")
        print("2. Check Docker port mappings")
        print("3. Verify PX4 MAVLink configuration")
