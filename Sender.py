# sender.py
import socket
import time
from vicon_dssdk import ViconDataStream

# Configuration
RPI_IP = "raspberrypi.local"  # Replace with your Raspberry Pi IP or hostname if known
UDP_PORT = 12345
subjectName = "s500"  # Replace with the Vicon subject name
segmentName = "root"  # Replace with the specific segment name if different

# Initialize Vicon Client
client = ViconDataStream.Client()
client.Connect("localhost")  # Connect to Vicon Tracker's IP or hostname
client.EnableSegmentData()
client.SetStreamMode(ViconDataStream.Client.StreamMode.EServerPush)
client.SetAxisMapping(ViconDataStream.Client.AxisMapping.EForward,
                      ViconDataStream.Client.AxisMapping.ERight,
                      ViconDataStream.Client.AxisMapping.EDown)

# Initialize UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"Sending data to {RPI_IP}:{UDP_PORT}")

try:
    while True:
        client.GetFrame()
        
        # Get position and orientation (quaternion)
        pos = client.GetSegmentGlobalTranslation(subjectName, segmentName)[0]
        quat = client.GetSegmentGlobalRotationQuaternion(subjectName, segmentName)[0]
        
        # Format message
        message = f"R,{time.time()},{pos[0]},{pos[1]},{pos[2]},{quat[0]},{quat[1]},{quat[2]},{quat[3]}"
        sock.sendto(message.encode(), (RPI_IP, UDP_PORT))
        print(f"Sent: {message}")

        time.sleep(0.1)  # Adjust the rate as needed
except KeyboardInterrupt:
    print("Terminated by user")
finally:
    client.Disconnect()
