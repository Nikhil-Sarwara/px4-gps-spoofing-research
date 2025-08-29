# Use official PX4 development image as base
FROM px4io/px4-dev-simulation-focal:latest

# Set maintainer info
LABEL maintainer="nikhilsarwara01@gmail.com"
LABEL description="PX4 SITL with GPS Spoofing Research Tools"

# Set working directory
WORKDIR /workspace

# Install additional Python packages for GPS spoofing research
RUN pip3 install --no-cache-dir \
    pymavlink>=2.4.37 \
    numpy>=1.21.0 \
    pandas>=1.3.0 \
    matplotlib>=3.4.0 \
    scipy>=1.7.0 \
    scikit-learn>=1.0.0 \
    geopy>=2.2.0 \
    pyyaml>=6.0 \
    click>=8.0.0 \
    loguru>=0.6.0 \
    jupyter>=1.0.0 \
    plotly>=5.0.0 \
    seaborn>=0.11.0

# Install additional system tools for GPS analysis
RUN apt-get update && apt-get install -y \
    gpsd \
    gpsd-clients \
    python3-gps \
    tcpdump \
    wireshark-common \
    vim \
    nano \
    htop \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install additional Python packages for network analysis
RUN pip3 install --no-cache-dir \
    scapy \
    networkx \
    psutil

# Create directories for research
RUN mkdir -p /workspace/src /workspace/logs /workspace/data

# Set environment variables
ENV PX4_HOME_LAT=42.3898
ENV PX4_HOME_LON=-71.1476
ENV PX4_HOME_ALT=14.2
ENV PYTHONPATH=/workspace/src:$PYTHONPATH

# Expose necessary ports
EXPOSE 5760 14550 14540 18570 8888

# Create entrypoint script
COPY entrypoint.sh /workspace/entrypoint.sh
RUN chmod +x /workspace/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/workspace/entrypoint.sh"]

# Default command
CMD ["sitl"]

