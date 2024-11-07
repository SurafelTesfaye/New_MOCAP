# Use ROS base image
FROM ros:noetic-ros-base-focal

# Install MAVROS packages
RUN apt-get update && apt-get install -y \
    ros-noetic-mavros \
    ros-noetic-mavros-extras

# Source the ROS setup script and then run the geographiclib installer
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && rosrun mavros install_geographiclib_datasets.sh"
