#!/usr/bin/env python3

from mavlink_control import DroneController
import time

def main():
    print("🚁 PX4 SITL Interactive Control")
    print("="*40)
    
    # Connect to drone
    drone = DroneController()
    
    while True:
        print("\nCommands:")
        print("1. Status")
        print("2. GPS Position") 
        print("3. Arm")
        print("4. Disarm")
        print("5. Takeoff")
        print("6. Land")
        print("7. Monitor GPS")
        print("0. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            drone.get_status()
        elif choice == '2':
            drone.get_gps_position()
        elif choice == '3':
            drone.arm()
        elif choice == '4':
            drone.disarm()
        elif choice == '5':
            alt = input("Enter altitude (default 5m): ").strip()
            alt = float(alt) if alt else 5.0
            drone.takeoff(alt)
        elif choice == '6':
            drone.land()
        elif choice == '7':
            duration = input("Monitor duration (default 10s): ").strip()
            duration = int(duration) if duration else 10
            drone.monitor_gps(duration)
        elif choice == '0':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
