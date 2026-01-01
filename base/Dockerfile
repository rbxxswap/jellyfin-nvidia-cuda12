# =============================================================================
# BASE IMAGE: CUDA 12.9.1 + Jellyfin + FFmpeg
# =============================================================================
# Dieses Image enthält alle gemeinsamen Komponenten.
# Varianten (main, debug, mqtt) bauen darauf auf.
#
# Build: docker build -t drshyper/jellyfin-nvidia-cuda12:base ./base
# =============================================================================

FROM nvidia/cuda:12.9.1-base-ubuntu24.04

LABEL maintainer="drshyper"
LABEL description="Jellyfin Media Server with NVIDIA CUDA 12.9.1 support - BASE IMAGE"
LABEL version="1.0"

# 1. Notwendige Pakete und das Jellyfin-Repository hinzufügen
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ca-certificates \
    && curl -fsSL https://repo.jellyfin.org/ubuntu/jellyfin_team.gpg.key | gpg --dearmor -o /usr/share/keyrings/jellyfin.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/jellyfin.gpg] https://repo.jellyfin.org/ubuntu noble main" > /etc/apt/sources.list.d/jellyfin.list \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Jellyfin-SERVER, Web-Client, FFmpeg und Bibliotheken installieren
RUN apt-get update && apt-get install -y --no-install-recommends \
    jellyfin-server \
    jellyfin-web \
    ffmpeg \
    libass9 \
    libfreetype6 \
    libva2 \
    libvdpau1 \
    libfontconfig1 \
    libfribidi0 \
    libharfbuzz0b \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Symbolischen Link für den Web-Client erstellen
RUN mkdir -p /usr/lib/jellyfin/bin/ \
    && ln -sf /usr/share/jellyfin/web /usr/lib/jellyfin/bin/jellyfin-web

# Jellyfin Pfade konfigurieren (damit /config Volume genutzt wird)
ENV JELLYFIN_DATA_DIR=/config/data
ENV JELLYFIN_CONFIG_DIR=/config
ENV JELLYFIN_CACHE_DIR=/config/cache
ENV JELLYFIN_LOG_DIR=/config/log

# Port freigeben
EXPOSE 8096

# KEIN ENTRYPOINT hier - wird von Varianten gesetzt
