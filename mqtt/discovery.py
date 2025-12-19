#!/usr/bin/env python3
"""
Home Assistant MQTT Discovery Payloads
Generates discovery configs for all entities
"""

import json
import logging
from config import get_config

logger = logging.getLogger(__name__)


class DiscoveryManager:
    """Manages MQTT Discovery for Home Assistant"""
    
    def __init__(self, mqtt_client):
        self.mqtt = mqtt_client
        self.config = get_config()
        self.base_topic = self.config.mqtt_topic
        self.discovery_prefix = self.config.mqtt_discovery_prefix
        self.server_id = self.config.server_id
        
        # Track registered sessions for cleanup
        self.registered_sessions = set()
    
    def _device_info(self, server_info=None):
        """Generate device info block for all entities"""
        version = server_info.get('Version', 'Unknown') if server_info else 'Unknown'
        url = self.config.jellyfin_host
        
        return {
            "identifiers": [f"jellyfin_{self.server_id}"],
            "name": "Jellyfin Media Server",
            "manufacturer": "Jellyfin",
            "model": f"Jellyfin {version}",
            "sw_version": "MQTT Bridge 1.0",
            "configuration_url": url
        }
    
    def _publish_discovery(self, component, object_id, payload):
        """Publish a discovery message"""
        topic = f"{self.discovery_prefix}/{component}/jellyfin_{self.server_id}_{object_id}/config"
        self.mqtt.publish(topic, json.dumps(payload), retain=True)
        logger.debug("Published discovery: %s", topic)
    
    def _remove_discovery(self, component, object_id):
        """Remove a discovery message (empty payload)"""
        topic = f"{self.discovery_prefix}/{component}/jellyfin_{self.server_id}_{object_id}/config"
        self.mqtt.publish(topic, "", retain=True)
        logger.debug("Removed discovery: %s", topic)
    
    def publish_static_discovery(self, server_info=None):
        """Publish all static entity discoveries"""
        device = self._device_info(server_info)
        
        # 1. Server Status (Binary Sensor)
        self._publish_discovery("binary_sensor", "status", {
            "name": "Server Status",
            "unique_id": f"jellyfin_{self.server_id}_status",
            "state_topic": f"{self.base_topic}/status",
            "payload_on": "online",
            "payload_off": "offline",
            "device_class": "connectivity",
            "device": device
        })
        
        # 2. Active Sessions (Sensor)
        self._publish_discovery("sensor", "active_sessions", {
            "name": "Active Sessions",
            "unique_id": f"jellyfin_{self.server_id}_active_sessions",
            "state_topic": f"{self.base_topic}/sessions/count",
            "icon": "mdi:account-multiple",
            "device": device
        })
        
        # 3. Playing Sessions (Sensor)
        self._publish_discovery("sensor", "playing_sessions", {
            "name": "Playing Sessions",
            "unique_id": f"jellyfin_{self.server_id}_playing_sessions",
            "state_topic": f"{self.base_topic}/sessions/playing_count",
            "icon": "mdi:play-circle",
            "device": device
        })
        
        # 4. Transcoding Active (Binary Sensor)
        self._publish_discovery("binary_sensor", "transcoding", {
            "name": "Transcoding Active",
            "unique_id": f"jellyfin_{self.server_id}_transcoding",
            "state_topic": f"{self.base_topic}/transcoding/active",
            "payload_on": "true",
            "payload_off": "false",
            "icon": "mdi:cog-sync",
            "device": device
        })
        
        # 5. GPU Utilization (Sensor)
        self._publish_discovery("sensor", "gpu_utilization", {
            "name": "GPU Utilization",
            "unique_id": f"jellyfin_{self.server_id}_gpu_utilization",
            "state_topic": f"{self.base_topic}/gpu/utilization",
            "unit_of_measurement": "%",
            "icon": "mdi:chart-line",
            "device": device
        })
        
        # 6. GPU Temperature (Sensor)
        self._publish_discovery("sensor", "gpu_temperature", {
            "name": "GPU Temperature",
            "unique_id": f"jellyfin_{self.server_id}_gpu_temperature",
            "state_topic": f"{self.base_topic}/gpu/temperature",
            "unit_of_measurement": "°C",
            "device_class": "temperature",
            "device": device
        })
        
        # 7. GPU Memory (Sensor)
        self._publish_discovery("sensor", "gpu_memory", {
            "name": "GPU Memory Used",
            "unique_id": f"jellyfin_{self.server_id}_gpu_memory",
            "state_topic": f"{self.base_topic}/gpu/memory_percent",
            "unit_of_measurement": "%",
            "icon": "mdi:memory",
            "device": device
        })
        
        # 8. Container CPU (Sensor)
        self._publish_discovery("sensor", "container_cpu", {
            "name": "Container CPU",
            "unique_id": f"jellyfin_{self.server_id}_container_cpu",
            "state_topic": f"{self.base_topic}/container/cpu_percent",
            "unit_of_measurement": "%",
            "icon": "mdi:cpu-64-bit",
            "device": device
        })
        
        # 9. Container Memory (Sensor)
        self._publish_discovery("sensor", "container_memory", {
            "name": "Container Memory",
            "unique_id": f"jellyfin_{self.server_id}_container_memory",
            "state_topic": f"{self.base_topic}/container/memory_percent",
            "unit_of_measurement": "%",
            "icon": "mdi:memory",
            "device": device
        })
        
        # 10. Library Scan Button
        self._publish_discovery("button", "library_scan", {
            "name": "Library Scan",
            "unique_id": f"jellyfin_{self.server_id}_library_scan",
            "command_topic": f"{self.base_topic}/library/command",
            "payload_press": "scan",
            "icon": "mdi:refresh",
            "device": device
        })
        
        # 11. Library Scanning (Binary Sensor)
        self._publish_discovery("binary_sensor", "library_scanning", {
            "name": "Library Scanning",
            "unique_id": f"jellyfin_{self.server_id}_library_scanning",
            "state_topic": f"{self.base_topic}/library/scanning",
            "payload_on": "true",
            "payload_off": "false",
            "icon": "mdi:magnify-scan",
            "device": device
        })
        
        logger.info("Published static discovery for 11 entities")
    
    def publish_session_discovery(self, session_id, device_name, server_info=None):
        """Publish discovery for a media player session"""
        if session_id in self.registered_sessions:
            return  # Already registered
        
        device = self._device_info(server_info)
        device_slug = device_name.lower().replace(' ', '_').replace('-', '_')
        
        self._publish_discovery("media_player", f"session_{session_id[:8]}", {
            "name": f"Jellyfin - {device_name}",
            "unique_id": f"jellyfin_{self.server_id}_session_{session_id[:8]}",
            "object_id": f"jellyfin_{device_slug}",
            "state_topic": f"{self.base_topic}/sessions/{session_id}/state",
            "json_attributes_topic": f"{self.base_topic}/sessions/{session_id}/media",
            "command_topic": f"{self.base_topic}/sessions/{session_id}/command",
            "payload_play": "play",
            "payload_pause": "pause",
            "payload_stop": "stop",
            "icon": "mdi:plex",
            "device": device,
            "availability": [
                {
                    "topic": f"{self.base_topic}/status",
                    "payload_available": "online",
                    "payload_not_available": "offline"
                }
            ]
        })
        
        self.registered_sessions.add(session_id)
        logger.info("Registered session media player: %s (%s)", device_name, session_id[:8])
    
    def remove_session_discovery(self, session_id):
        """Remove discovery for a session that ended"""
        if session_id not in self.registered_sessions:
            return
        
        self._remove_discovery("media_player", f"session_{session_id[:8]}")
        self.registered_sessions.discard(session_id)
        logger.info("Removed session media player: %s", session_id[:8])
    
    def cleanup_stale_sessions(self, active_session_ids):
        """Remove sessions that are no longer active"""
        stale = self.registered_sessions - set(active_session_ids)
        for session_id in stale:
            self.remove_session_discovery(session_id)
