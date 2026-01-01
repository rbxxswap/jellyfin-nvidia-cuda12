#!/usr/bin/env python3
"""
Discovery Base - Helper methods for creating HA entities
"""

import json
import logging

logger = logging.getLogger(__name__)


class DiscoveryBase:
    """Base class for discovery modules"""
    
    def __init__(self, mqtt_client, base_topic, discovery_prefix, server_id, device_info):
        self.mqtt = mqtt_client
        self.base_topic = base_topic
        self.discovery_prefix = discovery_prefix
        self.server_id = server_id
        self.device_info = device_info
        self.entity_count = 0
    
    def _publish(self, component, object_id, payload):
        """Publish discovery config"""
        topic = f"{self.discovery_prefix}/{component}/jellyfin_{self.server_id}_{object_id}/config"
        self.mqtt.publish(topic, json.dumps(payload), retain=True)
        self.entity_count += 1
    
    def _remove(self, component, object_id):
        """Remove discovery config"""
        topic = f"{self.discovery_prefix}/{component}/jellyfin_{self.server_id}_{object_id}/config"
        self.mqtt.publish(topic, "", retain=True)
    
    def sensor(self, object_id, name, state_topic, icon="mdi:information", unit=None, device_class=None, state_class=None, extra=None):
        """Create sensor entity"""
        payload = {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "icon": icon,
            "device": self.device_info
        }
        if unit:
            payload["unit_of_measurement"] = unit
        if device_class:
            payload["device_class"] = device_class
        if state_class:
            payload["state_class"] = state_class
        if extra:
            payload.update(extra)
        self._publish("sensor", object_id, payload)
    
    def binary_sensor(self, object_id, name, state_topic, icon=None, device_class=None, payload_on="true", payload_off="false"):
        """Create binary sensor entity"""
        payload = {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "payload_on": payload_on,
            "payload_off": payload_off,
            "device": self.device_info
        }
        if icon:
            payload["icon"] = icon
        if device_class:
            payload["device_class"] = device_class
        self._publish("binary_sensor", object_id, payload)
    
    def button(self, object_id, name, command_topic, payload_press, icon="mdi:button-pointer"):
        """Create button entity"""
        self._publish("button", object_id, {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "command_topic": f"{self.base_topic}/{command_topic}",
            "payload_press": payload_press,
            "icon": icon,
            "device": self.device_info
        })
    
    def switch(self, object_id, name, state_topic, command_topic, icon="mdi:toggle-switch"):
        """Create switch entity"""
        self._publish("switch", object_id, {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "command_topic": f"{self.base_topic}/{command_topic}",
            "payload_on": "ON",
            "payload_off": "OFF",
            "icon": icon,
            "device": self.device_info
        })
    
    def number(self, object_id, name, state_topic, command_topic, min_val, max_val, step=1, icon="mdi:numeric", unit=None):
        """Create number entity"""
        payload = {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "command_topic": f"{self.base_topic}/{command_topic}",
            "min": min_val,
            "max": max_val,
            "step": step,
            "icon": icon,
            "device": self.device_info
        }
        if unit:
            payload["unit_of_measurement"] = unit
        self._publish("number", object_id, payload)
    
    def select(self, object_id, name, state_topic, command_topic, options, icon="mdi:format-list-bulleted"):
        """Create select entity"""
        self._publish("select", object_id, {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "command_topic": f"{self.base_topic}/{command_topic}",
            "options": options,
            "icon": icon,
            "device": self.device_info
        })
    
    def text(self, object_id, name, state_topic, command_topic=None, icon="mdi:text", mode="text"):
        """Create text entity"""
        payload = {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "icon": icon,
            "mode": mode,
            "device": self.device_info
        }
        if command_topic:
            payload["command_topic"] = f"{self.base_topic}/{command_topic}"
        self._publish("text", object_id, payload)
    
    def media_player(self, object_id, name, state_topic, command_topic, icon="mdi:play-circle"):
        """Create media player entity"""
        self._publish("media_player", object_id, {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "command_topic": f"{self.base_topic}/{command_topic}",
            "icon": icon,
            "device": self.device_info
        })
