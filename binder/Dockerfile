# Dockerfile of the base image: https://github.com/IntEL4CoRo/jupyter-ros2/blob/main/Dockerfile
FROM intel4coro/jupyter-ros2:jazzy-py3.12

USER root
#============= Install extra software packages =============#
# RUN apt update && apt install -y curl

# Install python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
#===========================================================#
# ------------------------------------------------------------
# Required
# ------------------------------------------------------------
USER root
RUN apt update && apt install -y --no-install-recommends \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    ros-jazzy-hardware-interface \
    ros-jazzy-controller-manager \
    ros-jazzy-control-msgs \
    ros-jazzy-xacro \
    ros-jazzy-rqt-joint-trajectory-controller \
    graphviz graphviz-dev \
    python3-vcstool \
    nodejs \
    npm \
    wmctrl && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Install demo repository and cram code
# ------------------------------------------------------------

RUN python3 -m pip install poetry
RUN set -ex && \
    poetry config virtualenvs.create false && \
    mkdir -p ${HOME}/libs && cd ${HOME}/libs && \
    git clone --branch thesis --single-branch https://github.com/sunava/cognitive_robot_abstract_machine.git && \
    cd cognitive_robot_abstract_machine && \
    python3 -m pip install owlready2 && \
    python3 -m pip install SPARQLWrapper && \
    git clone https://github.com/sunava/pycram_object_gap_demo.git pycram/resources/pycram_object_gap_demo && \
    sed -i '/^[[:space:]]*random_events[[:space:]]*=.*$/d' pyproject.toml && \
    poetry install



# ------------------------------------------------------------
# ROS2 workspace: giskardpy_ros (clone, deps, build)
# ------------------------------------------------------------
RUN python3 -m pip install xacro

ARG ROS_DISTRO=jazzy
ENV ROS_DISTRO=${ROS_DISTRO}
ENV OVERLAY_WS=/root/ros2_ws

RUN apt update && apt install -y --no-install-recommends \
    python3.12-venv \
    ros-jazzy-navigation2 \
    ros-dev-tools \
    default-jre \
    ros-jazzy-rclpy-message-converter \
    python3-colcon-common-extensions && \
    rm -rf /var/lib/apt/lists/*

RUN set -ex && \
    mkdir -p ${OVERLAY_WS}/src && \
    cd ${OVERLAY_WS}/src && \
    git clone -b ros-jazzy --single-branch https://github.com/code-iai/iai_maps.git && \
    git clone -b ros-jazzy-main --single-branch https://github.com/code-iai/iai_pr2.git && \
    git clone -b ros2-jazzy --single-branch https://github.com/code-iai/hsr_description.git && \
    git clone -b ros2-jazzy --single-branch https://github.com/code-iai/iai_tracy.git && \
    rm -rf iai_tracy/iai_tracy_bringup iai_tracy/iai_tracy_ur && \
    git clone --single-branch https://github.com/maltehue/ros2_robotiq_gripper.git && \
    rm -rf ros2_robotiq_gripper/robotiq_controllers \
           ros2_robotiq_gripper/robotiq_drivers \
           ros2_robotiq_gripper/robotiq_hardware_tests \
           ros2_robotiq_gripper/robotiq_driver && \
    git clone -b jazzy --single-branch https://github.com/UniversalRobots/Universal_Robots_ROS2_Description.git && \
    git clone -b ros2-jazzy --single-branch https://github.com/code-iai/iai_stretch.git && \
    rm -rf iai_stretch/iai_stretch_bringup && \
    git clone -b ros2-master --single-branch https://github.com/realsenseai/realsense-ros.git && \
    rm -rf realsense-ros/realsense2_camera \
           realsense-ros/realsense2_camera_msgs \
           realsense-ros/realsense2_rgbd_plugin \
           realsense-ros/realsense2_ros_mqtt_bridge && \
    git clone -b ros2-main --single-branch https://github.com/code-iai/iai_tiago_description.git && \
    git clone -b humble-devel --single-branch https://github.com/pal-robotics/pmb2_robot.git && \
    rm -rf pmb2_robot/pmb2_bringup pmb2_robot/pmb2_controller_configuration && \
    git clone -b humble-devel --single-branch https://github.com/pal-robotics/pal_gripper.git && \
    rm -rf pal_gripper/pal_grippper_controller_configuration \
           pal_gripper/pal_gripper_gazeboo \
           pal_gripper/pal_gripper_simulation \
           pal_gripper/pal_parallel_gripper_wrapper && \
    . /opt/ros/${ROS_DISTRO}/setup.sh && \
    cd ${OVERLAY_WS} && \
    colcon build --merge-install

RUN grep -qxF "source ${OVERLAY_WS}/install/setup.bash" /root/.bashrc || \
    echo "source ${OVERLAY_WS}/install/setup.bash" >> /root/.bashrc

RUN python3 -m pip install "setuptools<81"

USER root
# Copy content to the image
ENV REPO_DIR=/home/repo
RUN mkdir -p ${REPO_DIR}
COPY . ${REPO_DIR}/
RUN git config --global --add safe.directory ${REPO_DIR}

# Set JupyterLab default directory
WORKDIR ${REPO_DIR}

# Set VSCODE default directory
ENV CODE_WORKING_DIRECTORY=${REPO_DIR}

# Copy RViz config
COPY default.rviz /home/jovyan/.rviz2/default.rviz
RUN mkdir -p /home/jovyan/.ipython/profile_default/startup /root/.ipython/profile_default/startup
RUN cd ${REPO_DIR}/binder/desktop-widget && \
    npm install && \
    npm run build && \
    jupyter labextension install . --no-build && \
    jupyter lab build --minimize=False

# The entrypoint of the docker image
COPY binder/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
