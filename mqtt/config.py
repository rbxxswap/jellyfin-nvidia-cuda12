#!/usr/bin/env python3
"""
MQTT Bridge Configuration
Reads and validates environment variables
"""

import os
import sys
import logging

logger = logging.getLogger(__name__)


class MQTTConfig:
    """Configuration from environment variables"""
    
    def __init__(self):
        # MQTT Settings
        self.mqtt_enable = os.getenv('MQTT_ENABLE', 'false').lower() == 'true'
        self.mqtt_host = os.getenv('MQTT_HOST', '')
        self.mqtt_port = int(os.getenv('MQTT_PORT', '1883'))
        self.mqtt_user = os.getenv('MQTT_USER', '')
        self.mqtt_password = os.getenv('MQTT_PASSWORD', '')
        self.mqtt_topic = os.getenv('MQTT_TOPIC', 'jellyfin')
        self.mqtt_discovery_prefix = os.getenv('MQTT_DISCOVERY_PREFIX', 'homeassistant')
        self.mqtt_client_id = os.getenv('MQTT_CLIENT_ID', 'jellyfin-mqtt')
        self.mqtt_poll_interval = int(os.getenv('MQTT_POLL_INTERVAL', '5'))
        
        # Jellyfin Settings
        self.jellyfin_api_key = os.getenv('JELLYFIN_API_KEY', '')
        self.jellyfin_host = os.getenv('JELLYFIN_HOST', 'http://localhost:8096')
        
        # Derived settings
        self.server_id = self._generate_server_id()
    
    def _generate_server_id(self):
        """Generate unique server ID from client ID"""
        # Use client_id as base for server identifier
        return self.mqtt_client_id.replace('-', '_')
    
    def validate(self):
        """
        Validate configuration.
        Returns tuple: (is_valid, error_message)
        """
        if not self.mqtt_enable:
            return False, "MQTT_ENABLE is not set to 'true'"
        
        if not self.mqtt_host:
            return False, "MQTT_HOST is required when MQTT is enabled"
        
        if not self.jellyfin_api_key:
            return False, "JELLYFIN_API_KEY is required when MQTT is enabled"
        
        if self.mqtt_poll_interval < 1:
            return False, "MQTT_POLL_INTERVAL must be at least 1 second"
        
        if self.mqtt_poll_interval > 60:
            logger.warning("MQTT_POLL_INTERVAL is set to %d seconds, this is quite high", 
                          self.mqtt_poll_interval)
        
        return True, None
    
    def log_config(self):
        """Log current configuration (without sensitive data)"""
        logger.info("MQTT Configuration:")
        logger.info("  MQTT_HOST: %s", self.mqtt_host)
        logger.info("  MQTT_PORT: %d", self.mqtt_port)
        logger.info("  MQTT_USER: %s", self.mqtt_user if self.mqtt_user else "(none)")
        logger.info("  MQTT_PASSWORD: %s", "****" if self.mqtt_password else "(none)")
        logger.info("  MQTT_TOPIC: %s", self.mqtt_topic)
        logger.info("  MQTT_DISCOVERY_PREFIX: %s", self.mqtt_discovery_prefix)
        logger.info("  MQTT_CLIENT_ID: %s", self.mqtt_client_id)
        logger.info("  MQTT_POLL_INTERVAL: %d seconds", self.mqtt_poll_interval)
        logger.info("  JELLYFIN_HOST: %s", self.jellyfin_host)
        logger.info("  JELLYFIN_API_KEY: %s", "****" if self.jellyfin_api_key else "(none)")


# Singleton instance
_config = None

def get_config():
    """Get configuration singleton"""
    global _config
    if _config is None:
        _config = MQTTConfig()
    return _config
