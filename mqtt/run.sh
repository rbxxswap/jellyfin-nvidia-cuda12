#!/bin/bash
# Jellyfin MQTT Container Startup Script
# Starts MQTT Bridge (if enabled) and Jellyfin server

set -e

echo "=============================================="
echo "  Jellyfin NVIDIA CUDA12 - MQTT Edition"
echo "=============================================="

# Start MQTT Bridge if enabled
if [ "${MQTT_ENABLE}" = "true" ]; then
    echo "[Startup] MQTT_ENABLE=true, checking configuration..."
    
    if [ -z "${MQTT_HOST}" ]; then
        echo "[Startup] WARNING: MQTT_ENABLE=true but MQTT_HOST not set!"
        echo "[Startup] MQTT Bridge will NOT start."
    elif [ -z "${JELLYFIN_API_KEY}" ]; then
        echo "[Startup] WARNING: MQTT_ENABLE=true but JELLYFIN_API_KEY not set!"
        echo "[Startup] MQTT Bridge will NOT start."
    else
        echo "[Startup] Starting MQTT Bridge..."
        echo "[Startup]   Broker: ${MQTT_HOST}:${MQTT_PORT:-1883}"
        echo "[Startup]   Topic:  ${MQTT_TOPIC:-jellyfin}"
        
        # Start MQTT Bridge in background
        python3 /usr/local/bin/mqtt/mqtt_bridge.py &
        MQTT_PID=$!
        echo "[Startup] MQTT Bridge started with PID: $MQTT_PID"
    fi
else
    echo "[Startup] MQTT_ENABLE not set or false, MQTT Bridge disabled"
fi

echo "[Startup] Starting Jellyfin server..."
echo "=============================================="

# Execute Jellyfin as main process
exec /usr/bin/jellyfin
