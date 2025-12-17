#!/bin/bash
echo "================================================"
echo "JELLYFIN NVIDIA GPU DIAGNOSTICS"
echo "Container Start: $(date)"
echo "================================================"

echo "[SYSTEM]"
echo "Image: $(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2)"
echo ""

echo "[GPU]"
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=name,driver_version,temperature.gpu,utilization.gpu,memory.total,memory.used --format=csv
else
  echo "ERROR: nvidia-smi not found!"
fi
echo ""

echo "[FFMPEG]"
if command -v ffmpeg >/dev/null 2>&1; then
  echo "Version: $(ffmpeg -version | head -1 | cut -d" " -f1-3)"
  echo "NVENC encoders: $(ffmpeg -encoders 2>&1 | grep -c _nvenc)"
  echo "CUVID decoders: $(ffmpeg -decoders 2>&1 | grep -c _cuvid)"
  echo "Hardware acceleration methods:"
  ffmpeg -hwaccels 2>&1 | tail -n +2
else
  echo "ERROR: ffmpeg not found!"
fi
echo ""

echo "[DEVICES]"
DEVICE_COUNT=$(ls -1 /dev/nvidia* 2>/dev/null | wc -l)
echo "NVIDIA devices found: $DEVICE_COUNT"
echo ""

echo "================================================"
echo "Starting Jellyfin..."
echo "================================================"
exec /usr/bin/jellyfin