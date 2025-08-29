from pymavlink import mavutil
import time

# Connect to PX4 SITL (default TCP port for jmavsim)
master = mavutil.mavlink_connection('tcp:127.0.0.1:4560')
master.wait_heartbeat()
print("Connected to PX4 SITL.")

# Sample spoofed GPS coordinates (Sydney Opera House)
latitude = -33.8568 * 1e7  # degrees * 1e7 (PX4 expects degrees * 1e7)
longitude = 151.2153 * 1e7
altitude = 20 * 1000        # meters to millimeters

while True:
    master.mav.hil_gps_send(
        int(time.time() * 1e6), # UNIX time in microseconds
        3,                      # fix_type: 3D fix
        int(latitude),          # lat: degrees * 1e7
        int(longitude),         # lon: degrees * 1e7
        int(altitude),          # alt: millimeters
        100,                    # eph: HDOP * 100 (centimeters)
        100,                    # epv: VDOP * 100 (centimeters)
        1000,                   # vel: cm/s ground speed
        0, 0, 0,                # vn, ve, vd: velocity components
        0,                      # cog: course over ground
        10,                     # satellites_visible
        0,                      # id
        36000                   # yaw: 36000 means north
    )
    print("Sent spoofed GPS data.")
    time.sleep(0.2)  # Send at 5Hz

