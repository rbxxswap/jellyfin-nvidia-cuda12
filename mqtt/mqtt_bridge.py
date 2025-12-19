#!/usr/bin/env python3
"""
Jellyfin MQTT Bridge for Home Assistant
Main entry point and event loop
"""

import sys
import time
import json
import signal
import logging
import paho.mqtt.client as mqtt

from config import get_config
from discovery import DiscoveryManager
from jellyfin_api import JellyfinAPI, parse_session
from gpu_monitor import get_gpu_monitor
from container_stats import get_container_stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[MQTT Bridge] %(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)

# Also log to file if /config/logs exists
try:
    import os
    if os.path.exists('/config/logs'):
        file_handler = logging.FileHandler('/config/logs/mqtt-bridge.log')
        file_handler.setFormatter(logging.Formatter('[MQTT Bridge] %(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(file_handler)
except:
    pass


class MQTTBridge:
    """Main MQTT Bridge class"""
    
    def __init__(self):
        self.config = get_config()
        self.running = False
        self.mqtt_client = None
        self.discovery = None
        self.jellyfin = None
        self.gpu = None
        self.container = None
        
        # State tracking
        self.last_sessions = {}
        self.server_info = None
    
    def setup_mqtt(self):
        """Initialize MQTT client"""
        self.mqtt_client = mqtt.Client(
            client_id=self.config.mqtt_client_id,
            protocol=mqtt.MQTTv311
        )
        
        # Set credentials if provided
        if self.config.mqtt_user:
            self.mqtt_client.username_pw_set(
                self.config.mqtt_user,
                self.config.mqtt_password
            )
        
        # Set Last Will and Testament
        self.mqtt_client.will_set(
            f"{self.config.mqtt_topic}/status",
            payload="offline",
            qos=1,
            retain=True
        )
        
        # Set callbacks
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_disconnect = self._on_disconnect
        self.mqtt_client.on_message = self._on_message
        
        return self.mqtt_client
    
    def _on_connect(self, client, userdata, flags, rc):
        """MQTT connection callback"""
        if rc == 0:
            logger.info("Connected to MQTT broker at %s:%d", 
                       self.config.mqtt_host, self.config.mqtt_port)
            
            # Publish online status
            client.publish(
                f"{self.config.mqtt_topic}/status",
                payload="online",
                qos=1,
                retain=True
            )
            
            # Subscribe to command topics
            base = self.config.mqtt_topic
            client.subscribe(f"{base}/command")
            client.subscribe(f"{base}/library/command")
            client.subscribe(f"{base}/sessions/+/command")
            logger.info("Subscribed to command topics")
            
            # Send discovery after connection
            if self.discovery:
                self.discovery.publish_static_discovery(self.server_info)
        else:
            logger.error("MQTT connection failed with code: %d", rc)
    
    def _on_disconnect(self, client, userdata, rc):
        """MQTT disconnect callback"""
        if rc != 0:
            logger.warning("Unexpected MQTT disconnect (code: %d), will reconnect", rc)
    
    def _on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages (commands)"""
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        logger.info("Received command: %s = %s", topic, payload)
        
        base = self.config.mqtt_topic
        
        try:
            # Library commands
            if topic == f"{base}/library/command":
                if payload == "scan":
                    self.jellyfin.start_library_scan()
            
            # Global server commands
            elif topic == f"{base}/command":
                logger.info("Global command: %s (not implemented)", payload)
            
            # Session commands
            elif "/sessions/" in topic and topic.endswith("/command"):
                # Extract session ID from topic
                parts = topic.split('/')
                session_idx = parts.index('sessions') + 1
                session_id = parts[session_idx]
                
                # Find full session ID
                full_session_id = None
                for sid in self.last_sessions.keys():
                    if sid.startswith(session_id) or session_id in sid:
                        full_session_id = sid
                        break
                
                if full_session_id:
                    self._handle_session_command(full_session_id, payload)
                else:
                    logger.warning("Session not found: %s", session_id)
        
        except Exception as e:
            logger.error("Command handling error: %s", str(e))
    
    def _handle_session_command(self, session_id, command):
        """Handle playback commands for a session"""
        cmd_map = {
            'play': 'Unpause',
            'pause': 'Pause',
            'stop': 'Stop',
            'next': 'NextTrack',
            'previous': 'PreviousTrack',
            'playpause': 'PlayPause',
        }
        
        if command.lower() in cmd_map:
            self.jellyfin.send_playstate_command(session_id, cmd_map[command.lower()])
        elif command.startswith('seek:'):
            try:
                seconds = int(command.split(':')[1])
                ticks = seconds * 10_000_000
                self.jellyfin.send_seek_command(session_id, ticks)
            except ValueError:
                logger.error("Invalid seek value: %s", command)
        else:
            logger.warning("Unknown session command: %s", command)
    
    def publish(self, topic_suffix, payload, retain=False):
        """Publish a message to MQTT"""
        topic = f"{self.config.mqtt_topic}/{topic_suffix}"
        
        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload)
        elif isinstance(payload, bool):
            payload = "true" if payload else "false"
        else:
            payload = str(payload)
        
        self.mqtt_client.publish(topic, payload, retain=retain)
    
    def poll_and_publish(self):
        """Main polling loop - fetch data and publish"""
        
        # 1. Server Info (occasionally)
        if not self.server_info:
            self.server_info = self.jellyfin.get_system_info()
            if self.server_info:
                self.publish("server/info", self.server_info, retain=True)
                self.publish("server/version", self.server_info.get('Version', 'Unknown'), retain=True)
                self.publish("server/url", self.config.jellyfin_host, retain=True)
        
        # 2. Sessions
        sessions = self.jellyfin.get_sessions()
        current_sessions = {}
        playing_count = 0
        transcoding_count = 0
        
        for session in sessions:
            parsed = parse_session(session)
            session_id = parsed['session_id']
            current_sessions[session_id] = parsed
            
            # Count stats
            if parsed['now_playing']:
                playing_count += 1
                if parsed['is_transcoding']:
                    transcoding_count += 1
            
            # Register new session in discovery
            if session_id not in self.last_sessions:
                self.discovery.publish_session_discovery(
                    session_id, 
                    parsed['device'],
                    self.server_info
                )
            
            # Publish session data
            self.publish(f"sessions/{session_id}/state", parsed['state'])
            self.publish(f"sessions/{session_id}/user", parsed['user'])
            self.publish(f"sessions/{session_id}/client", parsed['client'])
            self.publish(f"sessions/{session_id}/device", parsed['device'])
            self.publish(f"sessions/{session_id}/progress", parsed['progress'])
            self.publish(f"sessions/{session_id}/position", parsed['position'])
            self.publish(f"sessions/{session_id}/duration", parsed['duration'])
            self.publish(f"sessions/{session_id}/play_method", parsed['play_method'])
            self.publish(f"sessions/{session_id}/media", parsed['media'])
        
        # Cleanup ended sessions
        self.discovery.cleanup_stale_sessions(current_sessions.keys())
        self.last_sessions = current_sessions
        
        # Publish session counts
        self.publish("sessions/count", len(current_sessions))
        self.publish("sessions/playing_count", playing_count)
        
        # 3. Transcoding status
        self.publish("transcoding/active", transcoding_count > 0)
        self.publish("transcoding/count", transcoding_count)
        
        # 4. GPU Metrics
        gpu_metrics = self.gpu.get_metrics()
        if gpu_metrics:
            self.publish("gpu/name", gpu_metrics['name'])
            self.publish("gpu/utilization", gpu_metrics['utilization'])
            self.publish("gpu/temperature", gpu_metrics['temperature'])
            self.publish("gpu/memory_used", gpu_metrics['memory_used'])
            self.publish("gpu/memory_total", gpu_metrics['memory_total'])
            self.publish("gpu/memory_percent", gpu_metrics['memory_percent'])
            self.publish("gpu/encoder", gpu_metrics['encoder'])
            self.publish("gpu/decoder", gpu_metrics['decoder'])
            self.publish("gpu/power", gpu_metrics['power'])
        
        # 5. Container Stats
        container = self.container.get_all_stats()
        if container.get('memory'):
            self.publish("container/memory_used", container['memory']['used_mb'])
            self.publish("container/memory_limit", container['memory']['limit_mb'])
            self.publish("container/memory_percent", container['memory']['percent'])
        if container.get('network'):
            self.publish("container/network_rx", container['network']['rx_bytes'])
            self.publish("container/network_tx", container['network']['tx_bytes'])
        
        # 6. Library scan status
        running_tasks = self.jellyfin.get_running_tasks()
        is_scanning = any('scan' in t.get('Name', '').lower() or 'library' in t.get('Key', '').lower() 
                         for t in running_tasks)
        self.publish("library/scanning", is_scanning)
        self.publish("tasks/running_count", len(running_tasks))
    
    def run(self):
        """Main entry point"""
        logger.info("=" * 50)
        logger.info("Jellyfin MQTT Bridge starting...")
        logger.info("=" * 50)
        
        # Validate config
        valid, error = self.config.validate()
        if not valid:
            logger.error("Configuration error: %s", error)
            logger.info("MQTT Bridge disabled, exiting gracefully")
            return 0
        
        self.config.log_config()
        
        # Initialize components
        self.jellyfin = JellyfinAPI()
        self.gpu = get_gpu_monitor()
        self.container = get_container_stats()
        
        # Wait for Jellyfin to be ready
        logger.info("Waiting for Jellyfin API...")
        for i in range(30):
            if self.jellyfin.ping():
                logger.info("Jellyfin API responding")
                break
            time.sleep(2)
        else:
            logger.error("Jellyfin API not responding after 60s")
            return 1
        
        # Get initial server info
        self.server_info = self.jellyfin.get_system_info()
        if self.server_info:
            logger.info("Connected to Jellyfin %s", self.server_info.get('Version'))
        
        # Setup MQTT
        self.setup_mqtt()
        self.discovery = DiscoveryManager(self.mqtt_client)
        
        # Connect to MQTT broker
        try:
            self.mqtt_client.connect(
                self.config.mqtt_host,
                self.config.mqtt_port,
                keepalive=60
            )
        except Exception as e:
            logger.error("Failed to connect to MQTT broker: %s", str(e))
            return 1
        
        # Start MQTT loop in background
        self.mqtt_client.loop_start()
        
        # Setup signal handlers
        self.running = True
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Main loop
        logger.info("Starting main loop (poll interval: %ds)", self.config.mqtt_poll_interval)
        
        while self.running:
            try:
                self.poll_and_publish()
            except Exception as e:
                logger.error("Poll error: %s", str(e))
            
            # Sleep in small increments to allow quick shutdown
            for _ in range(self.config.mqtt_poll_interval * 10):
                if not self.running:
                    break
                time.sleep(0.1)
        
        # Cleanup
        logger.info("Shutting down...")
        self.publish("status", "offline", retain=True)
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        logger.info("MQTT Bridge stopped")
        
        return 0
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info("Received signal %d, shutting down...", signum)
        self.running = False


def main():
    """Entry point"""
    bridge = MQTTBridge()
    sys.exit(bridge.run())


if __name__ == '__main__':
    main()
