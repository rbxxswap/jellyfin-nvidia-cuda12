#!/bin/bash
# =============================================================================
# JELLYFIN NVIDIA GPU DIAGNOSTICS
# =============================================================================
# Zeigt beim Container-Start wichtige GPU und FFmpeg Informationen.
# Startet danach Jellyfin mit exec (ersetzt diesen Prozess).
#
# Die Diagnostik-Ausgabe wird auch nach /config/debug-output.txt geschrieben,
# damit sie jederzeit über die Unraid Console gelesen werden kann:
#   cat /config/debug-output.txt
# =============================================================================

# Ausgabe auf Terminal UND in Datei schreiben
DEBUG_LOG="/config/debug-output.txt"

# Funktion für duale Ausgabe
log() {
    echo "$1"
    echo "$1" >> "$DEBUG_LOG"
}

# Log-Datei initialisieren
mkdir -p /config 2>/dev/null
echo "" > "$DEBUG_LOG"

log "================================================"
log "JELLYFIN NVIDIA GPU DIAGNOSTICS"
log "Container Start: $(date)"
log "================================================"

log "[SYSTEM]"
log "Image: $(grep PRETTY_NAME /etc/os-release | cut -d= -f2)"
log ""

log "[GPU]"
if command -v nvidia-smi >/dev/null 2>&1; then
  GPU_INFO=$(nvidia-smi --query-gpu=name,driver_version,temperature.gpu,utilization.gpu,memory.total,memory.used --format=csv)
  log "$GPU_INFO"
else
  log "ERROR: nvidia-smi not found!"
fi
log ""

log "[FFMPEG]"
if command -v ffmpeg >/dev/null 2>&1; then
  log "Version: $(ffmpeg -version | head -1 | cut -d" " -f1-3)"
  log "NVENC encoders: $(ffmpeg -encoders 2>&1 | grep -c _nvenc)"
  log "CUVID decoders: $(ffmpeg -decoders 2>&1 | grep -c _cuvid)"
  log "Hardware acceleration methods:"
  HWACCELS=$(ffmpeg -hwaccels 2>/dev/null | tail -n +2)
  log "$HWACCELS"
else
  log "ERROR: ffmpeg not found!"
fi
log ""

log "[DEVICES]"
DEVICE_COUNT=$(ls -1 /dev/nvidia* 2>/dev/null | wc -l)
log "NVIDIA devices found: $DEVICE_COUNT"
DEVICE_LIST=$(ls -la /dev/nvidia* 2>/dev/null || echo "No /dev/nvidia* devices found")
log "$DEVICE_LIST"
log ""

log "================================================"
log "Debug output saved to: $DEBUG_LOG"
log "View anytime with: cat /config/debug-output.txt"
log "================================================"
log "Starting Jellyfin..."
log "================================================"
exec /usr/bin/jellyfin
