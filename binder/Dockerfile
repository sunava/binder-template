# Dockerfile of the base image: https://github.com/IntEL4CoRo/jupyter-ros2/blob/main/Dockerfile
FROM intel4coro/jupyter-ros2:jazzy-py3.12

USER root
#============= Install extra software packages =============#
# RUN apt update && apt install -y curl
RUN apt update && apt install -y --no-install-recommends     graphviz     libgraphviz-dev     pkg-config     python3-dev     build-essential &&     rm -rf /var/lib/apt/lists/*

# Install python packages
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt
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
    python3-vcstool \
    nodejs \
    npm \
    wmctrl && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Install demo repository and cram code
# ------------------------------------------------------------

RUN python3 -m pip install poetry
RUN set -ex &&     poetry config virtualenvs.create false &&     mkdir -p ${HOME}/libs && cd ${HOME}/libs && \
    git clone --branch thesis --single-branch https://github.com/sunava/cognitive_robot_abstract_machine.git && \
    cd cognitive_robot_abstract_machine &&     git clone https://github.com/sunava/pycram_object_gap_demo.git pycram/resources/pycram_object_gap_demo && \
    sed -i '/^[[:space:]]*random_events[[:space:]]*=.*$/d' pyproject.toml && \
    poetry install &&     mkdir -p /workspace/ros/src &&     cd /workspace/ros/src && \
    vcs import --input https://github.com/sunava/cognitive_robot_abstract_machine/blob/thesis/pycram/rosinstall/pycram-ros2-dependencies.rosinstall && \
    cd /workspace/ros &&     . /opt/ros/${ROS_DISTRO}/setup.sh &&     colcon build --symlink-install && \
    echo "source /workspace/ros/install/setup.bash" >> /root/.bashrc

# ------------------------------------------------------------
# ROS2 workspace: giskardpy_ros (clone, deps, build)
# ------------------------------------------------------------
RUN pip install xacro

ARG ROS_DISTRO=jazzy
ENV ROS_DISTRO=${ROS_DISTRO}


RUN pip install "setuptools<81"

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
