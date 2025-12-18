# =============================================================================
# MAIN VARIANT: Produktions-Image
# =============================================================================
# Minimales Image für den normalen Betrieb.
# Startet Jellyfin direkt ohne Diagnostik.
#
# Build: docker build -t drshyper/jellyfin-nvidia-cuda12:main ./main
# =============================================================================

ARG BASE_IMAGE=drshyper/jellyfin-nvidia-cuda12:base
FROM ${BASE_IMAGE}

LABEL variant="main"
LABEL description="Jellyfin CUDA 12.9.1 - Production"

# Direkter Start von Jellyfin
ENTRYPOINT ["/usr/bin/jellyfin"]
