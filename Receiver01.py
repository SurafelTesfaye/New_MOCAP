# receiver.py
import socket
from datetime import datetime
from pymavlink import mavutil
import math

# Configuration
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 12345

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"Listening on port {UDP_PORT}...")

# Initialize MAVLink connection to Pixhawk
mav = mavutil.mavlink_connection('udpout:127.0.0.1:14550')  # Adjust if needed

def quaternion_to_yaw(q0, q1, q2, q3):
    yaw = math.atan2(2.0 * (q0 * q3 + q1 * q2), 1.0 - 2.0 * (q2 * q2 + q3 * q3))
    return yaw

while True:
    # Receive data
    data, addr = sock.recvfrom(1024)
    values = data.decode().split(',')
    
    if values[0] != 'R':
        continue  # Ignore invalid data

    # Extract position and orientation data
    t = float(values[1])
    x = float(values[2])
    y = float(values[3])
    z = float(values[4])
    q0 = float(values[5])
    q1 = float(values[6])
    q2 = float(values[7])
    q3 = float(values[8])

    # Convert to NED frame
    ned_x = x
    ned_y = y
    ned_z = -z  # Invert z for NED

    # Convert quaternion to yaw
    yaw = quaternion_to_yaw(q0, q1, q2, q3)

    # Send MAVLink VISION_POSITION_ESTIMATE message
    mav.mav.vision_position_estimate_send(
        int(t * 1e6),  # Timestamp in microseconds
        ned_x,         # X position in NED (m)
        ned_y,         # Y position in NED (m)
        ned_z,         # Z position in NED (m)
        0.0, 0.0, yaw  # Roll, pitch, yaw (set roll/pitch to 0 if not needed)
    )

    print(f"Sent MAVLink VISION_POSITION_ESTIMATE: {ned_x}, {ned_y}, {ned_z}, Yaw: {yaw}")
