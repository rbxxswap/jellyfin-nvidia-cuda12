# =============================================================================
# DEBUG VARIANT: Mit Diagnostik beim Start
# =============================================================================
# Zeigt GPU-Info, FFmpeg-Encoder und NVIDIA-Devices beim Container-Start.
# Nützlich für Troubleshooting und Verifizierung der GPU-Passthrough.
#
# Build: docker build -t drshyper/jellyfin-nvidia-cuda12:debug ./debug
# =============================================================================

ARG BASE_IMAGE=drshyper/jellyfin-nvidia-cuda12:base
FROM ${BASE_IMAGE}

LABEL variant="debug"
LABEL description="Jellyfin CUDA 12.9.1 - Debug with GPU diagnostics"

# Diagnostik-Script kopieren
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# Start über Diagnostik-Script (führt am Ende exec jellyfin aus)
ENTRYPOINT ["/startup.sh"]
