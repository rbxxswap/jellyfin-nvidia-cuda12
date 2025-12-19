# Jellyfin NVIDIA CUDA12 - MQTT Variant
# Builds on debug image (includes GPU diagnostics)
#
# Hierarchy: base → debug → mqtt

FROM drshyper/jellyfin-nvidia-cuda12:debug

LABEL maintainer="DrShyper"
LABEL description="Jellyfin with NVIDIA CUDA12 + MQTT Bridge for Home Assistant"
LABEL version="1.0"

# Install Python and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create mqtt directory
RUN mkdir -p /usr/local/bin/mqtt

# Copy MQTT Bridge scripts
COPY requirements.txt /usr/local/bin/mqtt/
COPY config.py /usr/local/bin/mqtt/
COPY discovery.py /usr/local/bin/mqtt/
COPY jellyfin_api.py /usr/local/bin/mqtt/
COPY gpu_monitor.py /usr/local/bin/mqtt/
COPY container_stats.py /usr/local/bin/mqtt/
COPY mqtt_bridge.py /usr/local/bin/mqtt/

# Install Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r /usr/local/bin/mqtt/requirements.txt

# Copy startup script
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Create log directory
RUN mkdir -p /config/logs

EXPOSE 8096 8920

ENTRYPOINT ["/run.sh"]
