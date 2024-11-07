FROM ros:noetic-ros-base-focal

RUN apt update && \
    apt install -y ros-noetic-mavros ros-noetic-mavros-extras && \
    rosrun mavros install_geographiclib_datasets.sh

CMD ["bash"]
