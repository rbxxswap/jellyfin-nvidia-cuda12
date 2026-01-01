#!/usr/bin/env python3
"""
Jellyfin MQTT Bridge for Home Assistant
Main entry point - Modular API with ALL entities
"""

import sys
import time
import json
import signal
import logging
import paho.mqtt.client as mqtt

from config import get_config
from discovery import DiscoveryManager
from api import JellyfinAPI
from gpu_monitor import get_gpu_monitor
from container_stats import get_container_stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[MQTT Bridge] %(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


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
        self.server_info = None
        self.last_sessions = {}
        self.registered_users = set()
        self.registered_libraries = set()
        self.registered_tasks = set()
        self.registered_devices = set()
        self.registered_plugins = set()

    def setup_mqtt(self):
        """Initialize MQTT client"""
        self.mqtt_client = mqtt.Client(
            client_id=self.config.mqtt_client_id,
            protocol=mqtt.MQTTv311
        )
        
        if self.config.mqtt_user:
            self.mqtt_client.username_pw_set(self.config.mqtt_user, self.config.mqtt_password)
        
        self.mqtt_client.will_set(f"{self.config.mqtt_topic}/status", "offline", qos=1, retain=True)
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_disconnect = self._on_disconnect
        self.mqtt_client.on_message = self._on_message
        
        return self.mqtt_client
    
    def _on_connect(self, client, userdata, flags, rc):
        """MQTT connection callback"""
        if rc == 0:
            logger.info("Connected to MQTT broker at %s:%d", self.config.mqtt_host, self.config.mqtt_port)
            client.publish(f"{self.config.mqtt_topic}/status", "online", qos=1, retain=True)
            
            # Subscribe to command topics
            base = self.config.mqtt_topic
            client.subscribe(f"{base}/+/command")
            client.subscribe(f"{base}/+/+/command")
            client.subscribe(f"{base}/groups/+/set")
            client.subscribe(f"{base}/sessions/+/command")
            client.subscribe(f"{base}/sessions/+/+/set")
            logger.info("Subscribed to command topics")
            
            # Publish discovery
            if self.discovery:
                self.discovery.register_all_static()
                self.discovery.register_group_switches(self.jellyfin.GROUPS)
                self._publish_group_states()
        else:
            logger.error("MQTT connection failed with code: %d", rc)
    
    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning("Unexpected MQTT disconnect (code: %d)", rc)

    def _on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages"""
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        logger.info("Command: %s = %s", topic, payload)
        
        try:
            parts = topic.split('/')
            
            # Group switches
            if '/groups/' in topic and topic.endswith('/set'):
                group_name = parts[parts.index('groups') + 1]
                self._handle_group_command(group_name, payload)
            
            # Session commands
            elif '/sessions/' in topic and topic.endswith('/command'):
                session_id = parts[parts.index('sessions') + 1]
                self._handle_session_command(session_id, payload)
            
            # Volume set
            elif '/sessions/' in topic and '/volume/set' in topic:
                session_id = parts[parts.index('sessions') + 1]
                self._handle_volume_set(session_id, payload)
            
            # System commands
            elif topic.endswith('/system/command'):
                self._handle_system_command(payload)
            
            # Library commands
            elif '/library/' in topic and topic.endswith('/command'):
                self._handle_library_command(payload)
            
            # Task commands
            elif '/tasks/' in topic and topic.endswith('/command'):
                task_id = None
                if 'tasks' in parts:
                    idx = parts.index('tasks')
                    if idx + 1 < len(parts) and parts[idx + 1] != 'command':
                        task_id = parts[idx + 1]
                self._handle_task_command(task_id, payload)
                
        except Exception as e:
            logger.error("Command error: %s", str(e))

    def _handle_group_command(self, group_name, payload):
        """Handle group enable/disable"""
        if group_name in self.jellyfin.GROUPS:
            enabled = payload.lower() in ('on', 'true', '1')
            self.jellyfin.set_group_enabled(group_name, enabled)
            logger.info("Group '%s' %s", group_name, "enabled" if enabled else "disabled")
            self.publish(f"groups/{group_name}/state", "ON" if enabled else "OFF", retain=True)
    
    def _handle_system_command(self, payload):
        """Handle system commands"""
        if payload == "restart":
            self.jellyfin.system.restart_server()
        elif payload == "shutdown":
            self.jellyfin.system.shutdown_server()
    
    def _handle_session_command(self, session_id, command):
        """Handle session playback commands"""
        full_id = None
        for sid in self.last_sessions.keys():
            if sid.startswith(session_id) or session_id in sid:
                full_id = sid
                break
        
        if not full_id:
            logger.warning("Session not found: %s", session_id)
            return
        
        cmd_map = {
            'play': 'Unpause', 'pause': 'Pause', 'stop': 'Stop',
            'playpause': 'PlayPause', 'next': 'NextTrack', 'previous': 'PreviousTrack',
            'mute': 'Mute', 'unmute': 'Unmute'
        }
        
        if command.lower() in cmd_map:
            self.jellyfin.sessions.send_playstate_command(full_id, cmd_map[command.lower()])
        elif command.startswith('seek:'):
            try:
                seconds = int(command.split(':')[1])
                self.jellyfin.sessions.send_playstate_command(full_id, 'Seek', seek_position_ticks=seconds * 10_000_000)
            except ValueError:
                pass
    
    def _handle_volume_set(self, session_id, payload):
        """Handle volume set command"""
        full_id = None
        for sid in self.last_sessions.keys():
            if sid.startswith(session_id) or session_id in sid:
                full_id = sid
                break
        
        if full_id:
            try:
                volume = int(float(payload))
                self.jellyfin.sessions.send_general_command(full_id, {'Name': 'SetVolume', 'Arguments': {'Volume': str(volume)}})
            except ValueError:
                pass

    def _handle_library_command(self, payload):
        """Handle library commands"""
        if payload == "scan" or payload == "refresh":
            self.jellyfin.library.refresh_library()
    
    def _handle_task_command(self, task_id, payload):
        """Handle task commands"""
        if task_id and payload == "start":
            self.jellyfin.tasks.start_scheduled_task(task_id)
        elif task_id and payload == "stop":
            self.jellyfin.tasks.stop_scheduled_task(task_id)
        elif payload in ['RefreshLibrary', 'DeleteCache', 'DeleteTranscode', 'RefreshPeople', 'OptimizeDatabase']:
            tasks = self.jellyfin.tasks.get_scheduled_tasks()
            if tasks:
                for task in tasks:
                    if task.get('Key') == payload:
                        self.jellyfin.tasks.start_scheduled_task(task.get('Id'))
                        break
    
    def _publish_group_states(self):
        """Publish current state of all groups"""
        for group_name in self.jellyfin.GROUPS:
            enabled = self.jellyfin.is_group_enabled(group_name)
            self.publish(f"groups/{group_name}/state", "ON" if enabled else "OFF", retain=True)
    
    def publish(self, topic_suffix, payload, retain=False):
        """Publish message to MQTT"""
        topic = f"{self.config.mqtt_topic}/{topic_suffix}"
        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload)
        elif isinstance(payload, bool):
            payload = "true" if payload else "false"
        elif payload is None:
            payload = ""
        else:
            payload = str(payload)
        self.mqtt_client.publish(topic, payload, retain=retain)
    
    def _ticks_to_time(self, ticks):
        """Convert ticks to HH:MM:SS"""
        if not ticks:
            return "00:00:00"
        seconds = ticks // 10_000_000
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    # ==========================================================================
    # POLLING METHODS
    # ==========================================================================
    
    def poll_system(self):
        """Poll system group data"""
        if not self.jellyfin.is_group_enabled('system'):
            return
        
        # Server Info - api/system.py: get_system_info()
        info = self.jellyfin.system.get_system_info()
        if info:
            self.server_info = info
            self.discovery.update_server_info(info)
            
            self.publish("system/server_name", info.get('ServerName', ''), retain=True)
            self.publish("system/server_id", info.get('Id', ''), retain=True)
            self.publish("system/version", info.get('Version', ''), retain=True)
            self.publish("system/operating_system", info.get('OperatingSystem', ''), retain=True)
            self.publish("system/architecture", info.get('SystemArchitecture', ''), retain=True)
            self.publish("system/has_pending_restart", info.get('HasPendingRestart', False))
            self.publish("system/has_update_available", info.get('HasUpdateAvailable', False))
        
        # Activity Log - api/system.py: get_activity_log()
        activity = self.jellyfin.system.get_activity_log(limit=10)
        if activity:
            items = activity.get('Items', [])
            self.publish("system/activity_log/count", activity.get('TotalRecordCount', 0))
            if items:
                self.publish("system/activity_log/latest", items[0].get('Name', ''))
        
        # Server Logs - api/system.py: get_server_logs()
        logs = self.jellyfin.system.get_server_logs()
        if logs:
            self.publish("system/logs/count", len(logs))

    def poll_sessions(self):
        """Poll sessions group data"""
        if not self.jellyfin.is_group_enabled('sessions'):
            return
        
        # api/sessions.py: get_sessions()
        sessions = self.jellyfin.sessions.get_sessions()
        current_sessions = {}
        playing = 0
        paused = 0
        transcoding = 0
        
        if sessions:
            for session in sessions:
                session_id = session.get('Id', '')
                if not session_id:
                    continue
                
                current_sessions[session_id] = session
                device_name = session.get('DeviceName', 'Unknown')
                user_name = session.get('UserName', 'Unknown')
                client = session.get('Client', '')
                
                # Register new session
                if session_id not in self.last_sessions:
                    self.discovery.register_session(session_id, device_name, user_name, client)
                
                # Parse session state
                now_playing = session.get('NowPlayingItem')
                is_paused = session.get('PlayState', {}).get('IsPaused', False)
                
                if now_playing:
                    if is_paused:
                        state = 'paused'
                        paused += 1
                    else:
                        state = 'playing'
                        playing += 1
                else:
                    state = 'idle'
                
                # Transcoding check
                transcode_info = session.get('TranscodingInfo', {})
                is_transcoding = bool(transcode_info)
                if is_transcoding and state == 'playing':
                    transcoding += 1
                
                # Publish session data
                prefix = f"sessions/{session_id}"
                self.publish(f"{prefix}/state", state)
                self.publish(f"{prefix}/user", user_name)
                self.publish(f"{prefix}/client", client)
                self.publish(f"{prefix}/device", device_name)

                if now_playing:
                    self.publish(f"{prefix}/media/title", now_playing.get('Name', ''))
                    self.publish(f"{prefix}/media/type", now_playing.get('Type', ''))
                    self.publish(f"{prefix}/media/series", now_playing.get('SeriesName', ''))
                    
                    duration = now_playing.get('RunTimeTicks', 0)
                    position = session.get('PlayState', {}).get('PositionTicks', 0)
                    progress = (position / duration * 100) if duration > 0 else 0
                    
                    self.publish(f"{prefix}/progress", round(progress, 1))
                    self.publish(f"{prefix}/position", self._ticks_to_time(position))
                    self.publish(f"{prefix}/duration", self._ticks_to_time(duration))
            
            self.publish("sessions/playing_count", playing)
            self.publish("sessions/paused_count", paused)
            self.publish("sessions/transcoding_count", transcoding)
            self.publish("sessions/total_count", len(sessions))
        
        self.last_sessions = current_sessions
    
    def poll_library(self):
        """Poll library group data"""
        if not self.jellyfin.is_group_enabled('library'):
            return
        
        # api/library.py: get_virtual_folders()
        folders = self.jellyfin.library.get_virtual_folders()
        if folders:
            self.publish("library/count", len(folders))
            for folder in folders:
                lib_id = folder.get('ItemId', '')
                lib_name = folder.get('Name', '')
                lib_type = folder.get('CollectionType', 'mixed')
                
                if lib_id and lib_id not in self.registered_libraries:
                    self.discovery.register_library(lib_id, lib_name, lib_type)
                    self.registered_libraries.add(lib_id)
                
                if lib_id:
                    self.publish(f"library/{lib_id}/name", lib_name)
                    self.publish(f"library/{lib_id}/type", lib_type)
        
        # api/library.py: get_media_folders()
        media_folders = self.jellyfin.library.get_media_folders()
        if media_folders:
            items = media_folders.get('Items', [])
            self.publish("library/media_folders/count", len(items))

    def poll_items(self):
        """Poll items group data"""
        if not self.jellyfin.is_group_enabled('items'):
            return
        
        # api/items.py: get_resume_items()
        resume = self.jellyfin.items.get_resume_items(limit=10)
        if resume:
            items = resume.get('Items', [])
            self.publish("items/resume/count", resume.get('TotalRecordCount', len(items)))
            names = [i.get('Name', '') for i in items[:5]]
            self.publish("items/resume/list", ', '.join(names))
        
        # api/users.py: get_latest_media() - Note: This is in users.py, not items.py
        latest = self.jellyfin.users.get_latest_media(limit=5)
        if latest:
            names = [i.get('Name', '') for i in latest[:5]]
            self.publish("items/latest/all", ', '.join(names))
    
    def poll_users(self):
        """Poll users group data"""
        if not self.jellyfin.is_group_enabled('users'):
            return
        
        # api/users.py: get_users()
        users = self.jellyfin.users.get_users()
        if users:
            self.publish("users/count", len(users))
            
            online_count = 0
            for user in users:
                user_id = user.get('Id', '')
                user_name = user.get('Name', '')
                is_admin = user.get('Policy', {}).get('IsAdministrator', False)
                
                is_online = any(s.get('UserId') == user_id for s in self.last_sessions.values())
                if is_online:
                    online_count += 1
                
                if user_id and user_id not in self.registered_users:
                    self.discovery.register_user(user_id, user_name, is_admin)
                    self.registered_users.add(user_id)
                
                if user_id:
                    self.publish(f"users/{user_id}/name", user_name)
                    self.publish(f"users/{user_id}/online", is_online)
                    self.publish(f"users/{user_id}/is_admin", is_admin)
            
            self.publish("users/online_count", online_count)
        
        # api/users.py: get_public_users()
        public = self.jellyfin.users.get_public_users()
        if public:
            self.publish("users/public/count", len(public))

    def poll_playstate(self):
        """Poll playstate group data"""
        if not self.jellyfin.is_group_enabled('playstate'):
            return
        # Playstate is mostly for reporting, minimal polling needed
        pass
    
    def poll_tasks(self):
        """Poll tasks group data"""
        if not self.jellyfin.is_group_enabled('tasks'):
            return
        
        # api/tasks.py: get_scheduled_tasks()
        tasks = self.jellyfin.tasks.get_scheduled_tasks()
        if tasks:
            self.publish("tasks/count", len(tasks))
            
            running = 0
            for task in tasks:
                task_id = task.get('Id', '')
                task_name = task.get('Name', '')
                task_key = task.get('Key', '')
                state = task.get('State', 'Idle')
                
                if state == 'Running':
                    running += 1
                
                if task_id and task_id not in self.registered_tasks:
                    self.discovery.register_task(task_id, task_name, task_key)
                    self.registered_tasks.add(task_id)
                
                if task_id:
                    self.publish(f"tasks/{task_id}/name", task_name)
                    self.publish(f"tasks/{task_id}/state", state)
                    self.publish(f"tasks/{task_id}/running", state == 'Running')
                    
                    progress = task.get('CurrentProgressPercentage', 0)
                    self.publish(f"tasks/{task_id}/progress", round(progress, 1) if progress else 0)
            
            self.publish("tasks/running_count", running)
    
    def poll_devices(self):
        """Poll devices group data"""
        if not self.jellyfin.is_group_enabled('devices'):
            return
        
        # api/devices.py: get_devices()
        devices = self.jellyfin.devices.get_devices()
        if devices:
            items = devices.get('Items', [])
            self.publish("devices/count", len(items))
            
            for device in items:
                device_id = device.get('Id', '')
                device_name = device.get('Name', 'Unknown')
                app_name = device.get('AppName', '')
                
                if device_id and device_id not in self.registered_devices:
                    self.discovery.register_device(device_id, device_name, app_name)
                    self.registered_devices.add(device_id)
                
                if device_id:
                    self.publish(f"devices/{device_id}/name", device_name)
                    self.publish(f"devices/{device_id}/app", app_name)

    def poll_plugins(self):
        """Poll plugins group data"""
        if not self.jellyfin.is_group_enabled('plugins'):
            return
        
        # api/plugins.py: get_plugins()
        plugins = self.jellyfin.plugins.get_plugins()
        if plugins:
            self.publish("plugins/count", len(plugins))
            
            enabled_count = 0
            for plugin in plugins:
                plugin_id = plugin.get('Id', '')
                plugin_name = plugin.get('Name', '')
                version = plugin.get('Version', '')
                status = plugin.get('Status', '')
                
                if status == 'Active':
                    enabled_count += 1
                
                if plugin_id and plugin_id not in self.registered_plugins:
                    self.discovery.register_plugin(plugin_id, plugin_name, version)
                    self.registered_plugins.add(plugin_id)
                
                if plugin_id:
                    self.publish(f"plugins/{plugin_id}/name", plugin_name)
                    self.publish(f"plugins/{plugin_id}/version", version)
                    self.publish(f"plugins/{plugin_id}/enabled", status == 'Active')
            
            self.publish("plugins/enabled_count", enabled_count)
        
        # api/plugins.py: get_repositories()
        repos = self.jellyfin.plugins.get_repositories()
        if repos:
            self.publish("plugins/repositories/count", len(repos))
    
    def poll_livetv(self):
        """Poll livetv group data"""
        if not self.jellyfin.is_group_enabled('livetv'):
            return
        
        # api/livetv.py: get_livetv_info()
        info = self.jellyfin.livetv.get_livetv_info()
        if info:
            self.publish("livetv/enabled", info.get('IsEnabled', False))
            services = info.get('Services', [])
            self.publish("livetv/tuners/count", len(services))
        
        # api/livetv.py: get_livetv_channels()
        channels = self.jellyfin.livetv.get_livetv_channels()
        if channels:
            self.publish("livetv/channels/count", channels.get('TotalRecordCount', 0))
        
        # api/livetv.py: get_livetv_recordings()
        recordings = self.jellyfin.livetv.get_livetv_recordings()
        if recordings:
            self.publish("livetv/recordings/count", recordings.get('TotalRecordCount', 0))
        
        # api/livetv.py: get_livetv_timers()
        timers = self.jellyfin.livetv.get_livetv_timers()
        if timers:
            self.publish("livetv/timers/count", timers.get('TotalRecordCount', 0))
        
        # api/livetv.py: get_series_timers()
        series_timers = self.jellyfin.livetv.get_series_timers()
        if series_timers:
            self.publish("livetv/series_timers/count", series_timers.get('TotalRecordCount', 0))
        
        # api/livetv.py: get_livetv_programs()
        programs = self.jellyfin.livetv.get_livetv_programs()
        if programs:
            self.publish("livetv/programs/count", programs.get('TotalRecordCount', 0))

    def poll_syncplay(self):
        """Poll syncplay group data"""
        if not self.jellyfin.is_group_enabled('syncplay'):
            return
        
        # api/syncplay.py: get_sync_play_groups()
        groups = self.jellyfin.syncplay.get_sync_play_groups()
        if groups:
            self.publish("syncplay/groups/count", len(groups))
        else:
            self.publish("syncplay/groups/count", 0)
    
    def poll_playlists(self):
        """Poll playlists group data"""
        if not self.jellyfin.is_group_enabled('playlists'):
            return
        # Playlists require item queries, minimal polling
        pass
    
    def poll_media(self):
        """Poll media group data"""
        if not self.jellyfin.is_group_enabled('media'):
            return
        
        # api/media.py: get_artists()
        artists = self.jellyfin.media.get_artists()
        if artists:
            self.publish("media/artists/count", artists.get('TotalRecordCount', 0))
        
        # api/media.py: get_album_artists()
        album_artists = self.jellyfin.media.get_album_artists()
        if album_artists:
            self.publish("media/album_artists/count", album_artists.get('TotalRecordCount', 0))
        
        # api/media.py: get_genres()
        genres = self.jellyfin.media.get_genres()
        if genres:
            self.publish("media/genres/count", genres.get('TotalRecordCount', 0))
        
        # api/media.py: get_music_genres()
        music_genres = self.jellyfin.media.get_music_genres()
        if music_genres:
            self.publish("media/music_genres/count", music_genres.get('TotalRecordCount', 0))
        
        # api/media.py: get_studios()
        studios = self.jellyfin.media.get_studios()
        if studios:
            self.publish("media/studios/count", studios.get('TotalRecordCount', 0))
        
        # api/media.py: get_persons()
        persons = self.jellyfin.media.get_persons()
        if persons:
            self.publish("media/persons/count", persons.get('TotalRecordCount', 0))
        
        # api/media.py: get_next_up()
        next_up = self.jellyfin.media.get_next_up()
        if next_up:
            items = next_up.get('Items', [])
            self.publish("media/nextup/count", next_up.get('TotalRecordCount', len(items)))

    def poll_images(self):
        """Poll images group data"""
        if not self.jellyfin.is_group_enabled('images'):
            return
        # Images are mostly action-based, minimal polling
        pass
    
    def poll_misc(self):
        """Poll misc group data"""
        if not self.jellyfin.is_group_enabled('misc'):
            return
        
        # api/misc.py: get_drives()
        drives = self.jellyfin.misc.get_drives()
        if drives:
            self.publish("misc/drives/count", len(drives))
        
        # api/misc.py: get_quick_connect_enabled()
        qc_enabled = self.jellyfin.misc.get_quick_connect_enabled()
        self.publish("misc/quick_connect/enabled", qc_enabled or False)
        
        # api/misc.py: get_api_keys()
        api_keys = self.jellyfin.misc.get_api_keys()
        if api_keys:
            self.publish("misc/api_keys/count", api_keys.get('TotalRecordCount', 0))
        
        # api/misc.py: get_branding_configuration()
        branding = self.jellyfin.misc.get_branding_configuration()
        if branding:
            css = branding.get('CustomCss', '')
            self.publish("misc/branding/css_length", len(css) if css else 0)
    
    def poll_hardware(self):
        """Poll GPU and container stats (always enabled)"""
        gpu_metrics = self.gpu.get_metrics()
        if gpu_metrics:
            self.publish("gpu/name", gpu_metrics.get('name', ''))
            self.publish("gpu/utilization", gpu_metrics.get('utilization', 0))
            self.publish("gpu/temperature", gpu_metrics.get('temperature', 0))
            self.publish("gpu/memory_used", gpu_metrics.get('memory_used', 0))
            self.publish("gpu/memory_total", gpu_metrics.get('memory_total', 0))
            self.publish("gpu/memory_percent", gpu_metrics.get('memory_percent', 0))
            self.publish("gpu/encoder", gpu_metrics.get('encoder', 0))
            self.publish("gpu/decoder", gpu_metrics.get('decoder', 0))
        
        container = self.container.get_all_stats()
        if container.get('memory'):
            self.publish("container/memory_used", container['memory'].get('used_mb', 0))
            self.publish("container/memory_limit", container['memory'].get('limit_mb', 0))
            self.publish("container/memory_percent", container['memory'].get('percent', 0))

    def poll_and_publish(self):
        """Main polling loop - call all group polls"""
        try:
            self.poll_system()
            self.poll_sessions()
            self.poll_library()
            self.poll_items()
            self.poll_users()
            self.poll_playstate()
            self.poll_tasks()
            self.poll_devices()
            self.poll_plugins()
            self.poll_livetv()
            self.poll_syncplay()
            self.poll_playlists()
            self.poll_media()
            self.poll_images()
            self.poll_misc()
            self.poll_hardware()
        except Exception as e:
            logger.error("Poll error: %s", str(e))
    
    def run(self):
        """Main entry point"""
        logger.info("=" * 60)
        logger.info("Jellyfin MQTT Bridge v2.0 - ALL ENTITIES")
        logger.info("=" * 60)
        
        # Validate config
        valid, error = self.config.validate()
        if not valid:
            logger.error("Configuration error: %s", error)
            return 1
        
        self.config.log_config()
        
        # Initialize components
        self.jellyfin = JellyfinAPI(self.config.jellyfin_host, self.config.jellyfin_api_key)
        self.gpu = get_gpu_monitor()
        self.container = get_container_stats()
        
        # Wait for Jellyfin
        logger.info("Waiting for Jellyfin API...")
        for i in range(30):
            if self.jellyfin.system.ping():
                logger.info("Jellyfin API responding")
                break
            time.sleep(2)
        else:
            logger.error("Jellyfin API not responding after 60s")
            return 1
        
        # Get server info
        self.server_info = self.jellyfin.system.get_system_info()
        if self.server_info:
            logger.info("Connected to Jellyfin %s", self.server_info.get('Version'))

        # Setup MQTT
        self.setup_mqtt()
        self.discovery = DiscoveryManager(self.mqtt_client, self.server_info)
        
        # Connect
        try:
            self.mqtt_client.connect(self.config.mqtt_host, self.config.mqtt_port, keepalive=60)
        except Exception as e:
            logger.error("MQTT connection failed: %s", str(e))
            return 1
        
        self.mqtt_client.loop_start()
        
        # Setup signals
        self.running = True
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Main loop
        logger.info("Starting main loop (poll interval: %ds)", self.config.mqtt_poll_interval)
        logger.info("Enabled groups: %s", self.jellyfin.get_enabled_groups())
        
        while self.running:
            self.poll_and_publish()
            
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
