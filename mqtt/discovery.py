#!/usr/bin/env python3
"""
Home Assistant MQTT Discovery Payloads
Generates discovery configs for ALL 318 API endpoints
"""

import json
import logging
from config import get_config

logger = logging.getLogger(__name__)


class DiscoveryManager:
    """Manages MQTT Discovery for Home Assistant - ALL Entities"""
    
    def __init__(self, mqtt_client):
        self.mqtt = mqtt_client
        self.config = get_config()
        self.base_topic = self.config.mqtt_topic
        self.discovery_prefix = self.config.mqtt_discovery_prefix
        self.server_id = self.config.server_id
        self.registered_sessions = set()
        self.entity_count = 0
    
    def _device_info(self, server_info=None):
        """Generate device info block"""
        version = server_info.get('Version', 'Unknown') if server_info else 'Unknown'
        return {
            "identifiers": [f"jellyfin_{self.server_id}"],
            "name": "Jellyfin Media Server",
            "manufacturer": "Jellyfin",
            "model": f"Jellyfin {version}",
            "sw_version": "MQTT Bridge 2.0",
            "configuration_url": self.config.jellyfin_host
        }
    
    def _publish(self, component, object_id, payload):
        """Publish discovery message"""
        topic = f"{self.discovery_prefix}/{component}/jellyfin_{self.server_id}_{object_id}/config"
        self.mqtt.publish(topic, json.dumps(payload), retain=True)
        self.entity_count += 1
    
    def _sensor(self, object_id, name, state_topic, icon="mdi:information", unit=None, device_class=None, extra=None, device=None):
        """Create sensor entity"""
        payload = {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "icon": icon,
            "device": device
        }
        if unit:
            payload["unit_of_measurement"] = unit
        if device_class:
            payload["device_class"] = device_class
        if extra:
            payload.update(extra)
        self._publish("sensor", object_id, payload)
    
    def _binary_sensor(self, object_id, name, state_topic, icon=None, device_class=None, device=None):
        """Create binary sensor entity"""
        payload = {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "payload_on": "true",
            "payload_off": "false",
            "device": device
        }
        if icon:
            payload["icon"] = icon
        if device_class:
            payload["device_class"] = device_class
        self._publish("binary_sensor", object_id, payload)
    
    def _button(self, object_id, name, command_topic, payload_press, icon="mdi:button-pointer", device=None):
        """Create button entity"""
        self._publish("button", object_id, {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "command_topic": f"{self.base_topic}/{command_topic}",
            "payload_press": payload_press,
            "icon": icon,
            "device": device
        })
    
    def _switch(self, object_id, name, state_topic, command_topic, icon="mdi:toggle-switch", device=None):
        """Create switch entity"""
        self._publish("switch", object_id, {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "command_topic": f"{self.base_topic}/{command_topic}",
            "payload_on": "ON",
            "payload_off": "OFF",
            "icon": icon,
            "device": device
        })
    
    def _number(self, object_id, name, state_topic, command_topic, min_val, max_val, icon="mdi:numeric", unit=None, device=None):
        """Create number entity"""
        payload = {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "command_topic": f"{self.base_topic}/{command_topic}",
            "min": min_val,
            "max": max_val,
            "icon": icon,
            "device": device
        }
        if unit:
            payload["unit_of_measurement"] = unit
        self._publish("number", object_id, payload)
    
    def _select(self, object_id, name, state_topic, command_topic, options, icon="mdi:format-list-bulleted", device=None):
        """Create select entity"""
        self._publish("select", object_id, {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "command_topic": f"{self.base_topic}/{command_topic}",
            "options": options,
            "icon": icon,
            "device": device
        })
    
    def _text(self, object_id, name, state_topic, command_topic, icon="mdi:text", device=None):
        """Create text entity"""
        self._publish("text", object_id, {
            "name": name,
            "unique_id": f"jellyfin_{self.server_id}_{object_id}",
            "state_topic": f"{self.base_topic}/{state_topic}",
            "command_topic": f"{self.base_topic}/{command_topic}",
            "icon": icon,
            "device": device
        })

    
    def publish_static_discovery(self, server_info=None):
        """Publish ALL entity discoveries"""
        device = self._device_info(server_info)
        self.entity_count = 0
        
        # =====================================================================
        # SYSTEM GROUP - Server Info, Status, Control
        # =====================================================================
        
        # Binary Sensors
        self._binary_sensor("status", "Server Status", "status", device_class="connectivity", device=device)
        self._binary_sensor("has_pending_restart", "Pending Restart", "server/has_pending_restart", "mdi:restart-alert", device=device)
        self._binary_sensor("has_update_available", "Update Available", "server/has_update_available", "mdi:update", device_class="update", device=device)
        self._binary_sensor("startup_wizard_completed", "Startup Wizard Completed", "server/startup_wizard_completed", "mdi:wizard-hat", device=device)
        self._binary_sensor("can_self_restart", "Can Self Restart", "server/can_self_restart", "mdi:restart", device=device)
        self._binary_sensor("can_launch_web_browser", "Can Launch Browser", "server/can_launch_web_browser", "mdi:web", device=device)
        
        # Server Info Sensors
        self._sensor("server_name", "Server Name", "server/name", "mdi:server", device=device)
        self._sensor("server_id", "Server ID", "server/id", "mdi:identifier", device=device)
        self._sensor("version", "Version", "server/version", "mdi:tag", device=device)
        self._sensor("product_name", "Product Name", "server/product_name", "mdi:package-variant", device=device)
        self._sensor("operating_system", "Operating System", "server/os", "mdi:linux", device=device)
        self._sensor("os_display_name", "OS Display Name", "server/os_display_name", "mdi:information", device=device)
        self._sensor("architecture", "Architecture", "server/architecture", "mdi:chip", device=device)
        self._sensor("local_address", "Local Address", "server/local_address", "mdi:ip-network", device=device)
        self._sensor("wan_address", "WAN Address", "server/wan_address", "mdi:earth", device=device)
        self._sensor("cache_path", "Cache Path", "server/cache_path", "mdi:folder-cog", device=device)
        self._sensor("log_path", "Log Path", "server/log_path", "mdi:folder-text", device=device)
        self._sensor("internal_metadata_path", "Metadata Path", "server/internal_metadata_path", "mdi:folder-information", device=device)
        self._sensor("transcoding_temp_path", "Transcoding Temp Path", "server/transcoding_temp_path", "mdi:folder-sync", device=device)
        self._sensor("web_socket_port", "WebSocket Port", "server/web_socket_port", "mdi:lan-connect", device=device)
        self._sensor("system_update_level", "Update Level", "server/system_update_level", "mdi:update", device=device)
        self._sensor("package_name", "Package Name", "server/package_name", "mdi:package", device=device)
        
        # Server Control Buttons
        self._button("restart_server", "Restart Server", "command", "restart", "mdi:restart", device=device)
        self._button("shutdown_server", "Shutdown Server", "command", "shutdown", "mdi:power", device=device)
        
        # Activity Log Sensor
        self._sensor("activity_log_count", "Activity Log Entries", "activity/count", "mdi:clipboard-list", device=device)
        
        # Server Time
        self._sensor("server_time_utc", "Server Time UTC", "server/time_utc", "mdi:clock-outline", device=device)
        self._sensor("server_time_local", "Server Time Local", "server/time_local", "mdi:clock", device=device)
        
        # =====================================================================
        # SESSIONS GROUP - Active Sessions, Playback Control
        # =====================================================================
        
        self._sensor("active_sessions", "Active Sessions", "sessions/count", "mdi:account-multiple", device=device)
        self._sensor("playing_sessions", "Playing Sessions", "sessions/playing_count", "mdi:play-circle", device=device)
        self._binary_sensor("transcoding_active", "Transcoding Active", "transcoding/active", "mdi:cog-sync", device=device)
        self._sensor("transcoding_count", "Transcoding Count", "transcoding/count", "mdi:cog-sync-outline", device=device)
        self._sensor("sessions_json", "Sessions Data", "sessions/json", "mdi:code-json", device=device)
        
        # =====================================================================
        # LIBRARY GROUP - Media Library Stats
        # =====================================================================
        
        # Library Scan Control
        self._button("library_scan", "Start Library Scan", "library/command", "scan", "mdi:magnify-scan", device=device)
        self._binary_sensor("library_scanning", "Library Scanning", "library/scanning", "mdi:magnify-scan", device=device)
        
        # Library Counts
        self._sensor("library_movie_count", "Movies", "library/movies/count", "mdi:movie", device=device)
        self._sensor("library_series_count", "Series", "library/series/count", "mdi:television-classic", device=device)
        self._sensor("library_episode_count", "Episodes", "library/episodes/count", "mdi:filmstrip", device=device)
        self._sensor("library_album_count", "Albums", "library/albums/count", "mdi:album", device=device)
        self._sensor("library_song_count", "Songs", "library/songs/count", "mdi:music", device=device)
        self._sensor("library_artist_count", "Artists", "library/artists/count", "mdi:account-music", device=device)
        self._sensor("library_musicvideo_count", "Music Videos", "library/musicvideos/count", "mdi:music-box", device=device)
        self._sensor("library_book_count", "Books", "library/books/count", "mdi:book-open-page-variant", device=device)
        self._sensor("library_boxset_count", "Box Sets", "library/boxsets/count", "mdi:package-variant-closed", device=device)
        self._sensor("library_trailer_count", "Trailers", "library/trailers/count", "mdi:movie-roll", device=device)
        self._sensor("library_total_count", "Total Items", "library/total/count", "mdi:database", device=device)
        self._sensor("library_total_size", "Library Size", "library/total/size", "mdi:harddisk", unit="GB", device=device)
        
        # Virtual Folders
        self._sensor("virtual_folders_count", "Virtual Folders", "library/virtual_folders/count", "mdi:folder-multiple", device=device)
        self._sensor("virtual_folders_json", "Virtual Folders Data", "library/virtual_folders/json", "mdi:code-json", device=device)
        
        # Media Folders
        self._sensor("media_folders_count", "Media Folders", "library/media_folders/count", "mdi:folder-play", device=device)
        
        # =====================================================================
        # ITEMS GROUP - Item Queries
        # =====================================================================
        
        self._sensor("resume_items_count", "Resume Items", "items/resume/count", "mdi:play-pause", device=device)
        self._sensor("latest_movies_json", "Latest Movies", "items/latest/movies", "mdi:new-box", device=device)
        self._sensor("latest_episodes_json", "Latest Episodes", "items/latest/episodes", "mdi:new-box", device=device)
        self._sensor("latest_music_json", "Latest Music", "items/latest/music", "mdi:new-box", device=device)
        
        # =====================================================================
        # USERS GROUP - User Management
        # =====================================================================
        
        self._sensor("users_count", "Users Count", "users/count", "mdi:account-group", device=device)
        self._sensor("users_json", "Users Data", "users/json", "mdi:code-json", device=device)
        self._sensor("current_user", "Current User", "users/current/name", "mdi:account", device=device)
        self._sensor("current_user_id", "Current User ID", "users/current/id", "mdi:identifier", device=device)
        
        # Per-User Sensors (dynamic, created in publish_user_discovery)
        
        # =====================================================================
        # PLAYSTATE GROUP - Playback Reporting
        # =====================================================================
        
        # Playstate is mostly used for reporting, but we can show last played
        self._sensor("last_played_item", "Last Played Item", "playstate/last_played/name", "mdi:play-circle", device=device)
        self._sensor("last_played_user", "Last Played By", "playstate/last_played/user", "mdi:account", device=device)
        self._sensor("last_played_time", "Last Played Time", "playstate/last_played/time", "mdi:clock", device=device)

        
        # =====================================================================
        # TASKS GROUP - Scheduled Tasks
        # =====================================================================
        
        self._sensor("tasks_count", "Scheduled Tasks", "tasks/count", "mdi:calendar-check", device=device)
        self._sensor("tasks_running_count", "Running Tasks", "tasks/running_count", "mdi:run", device=device)
        self._sensor("tasks_json", "Tasks Data", "tasks/json", "mdi:code-json", device=device)
        
        # Common Task Buttons
        self._button("task_scan_library", "Task: Scan Library", "tasks/command", "scan_library", "mdi:magnify-scan", device=device)
        self._button("task_refresh_guide", "Task: Refresh Guide", "tasks/command", "refresh_guide", "mdi:television-guide", device=device)
        self._button("task_clean_cache", "Task: Clean Cache", "tasks/command", "clean_cache", "mdi:broom", device=device)
        self._button("task_clean_transcode", "Task: Clean Transcode", "tasks/command", "clean_transcode", "mdi:folder-remove", device=device)
        self._button("task_refresh_people", "Task: Refresh People", "tasks/command", "refresh_people", "mdi:account-sync", device=device)
        self._button("task_update_plugins", "Task: Update Plugins", "tasks/command", "update_plugins", "mdi:puzzle", device=device)
        self._button("task_optimize_db", "Task: Optimize Database", "tasks/command", "optimize_db", "mdi:database-cog", device=device)
        
        # =====================================================================
        # DEVICES GROUP - Device Management
        # =====================================================================
        
        self._sensor("devices_count", "Devices Count", "devices/count", "mdi:devices", device=device)
        self._sensor("devices_json", "Devices Data", "devices/json", "mdi:code-json", device=device)
        
        # =====================================================================
        # PLUGINS GROUP - Plugin Management
        # =====================================================================
        
        self._sensor("plugins_count", "Plugins Count", "plugins/count", "mdi:puzzle", device=device)
        self._sensor("plugins_json", "Plugins Data", "plugins/json", "mdi:code-json", device=device)
        self._sensor("packages_count", "Available Packages", "plugins/packages/count", "mdi:package-variant", device=device)
        self._sensor("repositories_count", "Repositories", "plugins/repositories/count", "mdi:source-repository", device=device)
        
        # =====================================================================
        # LIVETV GROUP - Live TV, Recordings, Timers
        # =====================================================================
        
        self._sensor("livetv_channels_count", "Live TV Channels", "livetv/channels/count", "mdi:television", device=device)
        self._sensor("livetv_recordings_count", "Recordings", "livetv/recordings/count", "mdi:record-rec", device=device)
        self._sensor("livetv_timers_count", "Timers", "livetv/timers/count", "mdi:timer", device=device)
        self._sensor("livetv_series_timers_count", "Series Timers", "livetv/series_timers/count", "mdi:timer-sync", device=device)
        self._sensor("livetv_programs_count", "Programs", "livetv/programs/count", "mdi:television-guide", device=device)
        self._binary_sensor("livetv_enabled", "Live TV Enabled", "livetv/enabled", "mdi:television-classic", device=device)
        self._sensor("livetv_tuners_count", "Tuners", "livetv/tuners/count", "mdi:antenna", device=device)
        self._sensor("livetv_json", "Live TV Data", "livetv/json", "mdi:code-json", device=device)
        
        # =====================================================================
        # SYNCPLAY GROUP - Synchronized Playback
        # =====================================================================
        
        self._sensor("syncplay_groups_count", "SyncPlay Groups", "syncplay/groups/count", "mdi:account-group-outline", device=device)
        self._sensor("syncplay_json", "SyncPlay Data", "syncplay/json", "mdi:code-json", device=device)
        
        # SyncPlay Control Buttons
        self._button("syncplay_pause", "SyncPlay Pause", "syncplay/command", "pause", "mdi:pause", device=device)
        self._button("syncplay_unpause", "SyncPlay Play", "syncplay/command", "unpause", "mdi:play", device=device)
        self._button("syncplay_stop", "SyncPlay Stop", "syncplay/command", "stop", "mdi:stop", device=device)
        
        # =====================================================================
        # PLAYLISTS GROUP - Playlist Management
        # =====================================================================
        
        self._sensor("playlists_count", "Playlists Count", "playlists/count", "mdi:playlist-music", device=device)
        self._sensor("playlists_json", "Playlists Data", "playlists/json", "mdi:code-json", device=device)
        
        # =====================================================================
        # MEDIA GROUP - Search, Artists, Genres, Studios, TV Shows, Movies
        # =====================================================================
        
        # Artists
        self._sensor("artists_count", "Artists Count", "media/artists/count", "mdi:account-music", device=device)
        self._sensor("album_artists_count", "Album Artists Count", "media/album_artists/count", "mdi:account-music-outline", device=device)
        
        # Genres
        self._sensor("genres_count", "Genres Count", "media/genres/count", "mdi:tag-multiple", device=device)
        self._sensor("music_genres_count", "Music Genres Count", "media/music_genres/count", "mdi:music-note", device=device)
        
        # Studios
        self._sensor("studios_count", "Studios Count", "media/studios/count", "mdi:domain", device=device)
        
        # Persons
        self._sensor("persons_count", "Persons Count", "media/persons/count", "mdi:account-multiple", device=device)
        
        # Years
        self._sensor("years_count", "Years Count", "media/years/count", "mdi:calendar-range", device=device)
        
        # TV Shows
        self._sensor("next_up_count", "Next Up Count", "media/nextup/count", "mdi:play-box-multiple", device=device)
        self._sensor("next_up_json", "Next Up Data", "media/nextup/json", "mdi:code-json", device=device)
        self._sensor("upcoming_episodes_count", "Upcoming Episodes", "media/upcoming/count", "mdi:calendar-clock", device=device)
        
        # Movies
        self._sensor("movie_recommendations_json", "Movie Recommendations", "media/movies/recommendations", "mdi:movie-star", device=device)
        
        # Collections
        self._sensor("collections_count", "Collections Count", "media/collections/count", "mdi:folder-star", device=device)
        
        # Suggestions
        self._sensor("suggestions_json", "Suggestions", "media/suggestions/json", "mdi:lightbulb", device=device)
        
        # Trailers
        self._sensor("trailers_count", "Trailers Count", "media/trailers/count", "mdi:movie-roll", device=device)

        
        # =====================================================================
        # IMAGES GROUP - Image Management
        # =====================================================================
        
        self._sensor("splashscreen_url", "Splashscreen URL", "images/splashscreen/url", "mdi:image", device=device)
        self._button("delete_splashscreen", "Delete Splashscreen", "images/command", "delete_splashscreen", "mdi:image-remove", device=device)
        
        # =====================================================================
        # MISC GROUP - Various Endpoints
        # =====================================================================
        
        # Subtitles
        self._sensor("fallback_fonts_count", "Fallback Fonts", "misc/fallback_fonts/count", "mdi:format-font", device=device)
        
        # Channels
        self._sensor("channels_count", "Channels Count", "misc/channels/count", "mdi:youtube-tv", device=device)
        
        # Environment
        self._sensor("drives_count", "Drives Count", "misc/drives/count", "mdi:harddisk", device=device)
        self._sensor("drives_json", "Drives Data", "misc/drives/json", "mdi:code-json", device=device)
        
        # Quick Connect
        self._binary_sensor("quick_connect_enabled", "Quick Connect Enabled", "misc/quick_connect/enabled", "mdi:qrcode", device=device)
        self._button("quick_connect_initiate", "Initiate Quick Connect", "misc/command", "quick_connect", "mdi:qrcode-scan", device=device)
        
        # Backup
        self._sensor("backups_count", "Backups Count", "misc/backups/count", "mdi:backup-restore", device=device)
        self._sensor("backups_json", "Backups Data", "misc/backups/json", "mdi:code-json", device=device)
        self._button("create_backup", "Create Backup", "misc/command", "create_backup", "mdi:cloud-upload", device=device)
        
        # Localization
        self._sensor("countries_count", "Countries Count", "misc/countries/count", "mdi:earth", device=device)
        self._sensor("cultures_count", "Cultures Count", "misc/cultures/count", "mdi:translate", device=device)
        self._sensor("parental_ratings_count", "Parental Ratings", "misc/parental_ratings/count", "mdi:account-child", device=device)
        
        # Branding
        self._sensor("branding_css", "Custom CSS", "misc/branding/css", "mdi:language-css3", device=device)
        
        # API Keys
        self._sensor("api_keys_count", "API Keys Count", "misc/api_keys/count", "mdi:key-chain", device=device)
        
        # Dashboard
        self._sensor("config_pages_count", "Config Pages", "misc/config_pages/count", "mdi:view-dashboard", device=device)
        
        # =====================================================================
        # GPU GROUP - GPU Monitoring (Hardware)
        # =====================================================================
        
        self._sensor("gpu_name", "GPU Name", "gpu/name", "mdi:expansion-card", device=device)
        self._sensor("gpu_utilization", "GPU Utilization", "gpu/utilization", "mdi:gauge", unit="%", device=device)
        self._sensor("gpu_temperature", "GPU Temperature", "gpu/temperature", "mdi:thermometer", unit="°C", device_class="temperature", device=device)
        self._sensor("gpu_memory_used", "GPU Memory Used", "gpu/memory_used", "mdi:memory", unit="MB", device=device)
        self._sensor("gpu_memory_total", "GPU Memory Total", "gpu/memory_total", "mdi:memory", unit="MB", device=device)
        self._sensor("gpu_memory_percent", "GPU Memory %", "gpu/memory_percent", "mdi:memory", unit="%", device=device)
        self._sensor("gpu_encoder", "GPU Encoder", "gpu/encoder", "mdi:video", unit="%", device=device)
        self._sensor("gpu_decoder", "GPU Decoder", "gpu/decoder", "mdi:video-outline", unit="%", device=device)
        self._sensor("gpu_power", "GPU Power", "gpu/power", "mdi:flash", unit="W", device_class="power", device=device)
        
        # =====================================================================
        # CONTAINER GROUP - Docker Container Stats
        # =====================================================================
        
        self._sensor("container_memory_used", "Container Memory Used", "container/memory_used", "mdi:memory", unit="MB", device=device)
        self._sensor("container_memory_limit", "Container Memory Limit", "container/memory_limit", "mdi:memory", unit="MB", device=device)
        self._sensor("container_memory_percent", "Container Memory %", "container/memory_percent", "mdi:memory", unit="%", device=device)
        self._sensor("container_network_rx", "Container Network RX", "container/network_rx", "mdi:download", unit="B", device=device)
        self._sensor("container_network_tx", "Container Network TX", "container/network_tx", "mdi:upload", unit="B", device=device)
        
        # =====================================================================
        # STORAGE GROUP - Storage Info
        # =====================================================================
        
        self._sensor("storage_json", "Storage Data", "storage/json", "mdi:code-json", device=device)
        
        # =====================================================================
        # LOGS GROUP - Server Logs
        # =====================================================================
        
        self._sensor("logs_json", "Server Logs", "logs/json", "mdi:text-box-multiple", device=device)
        
        logger.info("Published static discovery for %d entities", self.entity_count)

    
    def publish_session_discovery(self, session_id, device_name, server_info=None):
        """Publish discovery for a specific session"""
        device = self._device_info(server_info)
        short_id = session_id[:8]
        safe_name = device_name.replace(" ", "_").replace("-", "_").lower()[:20]
        
        # Session State
        self._sensor(f"session_{short_id}_state", f"Session {device_name} State", 
                    f"sessions/{session_id}/state", "mdi:play-circle", device=device)
        
        # Session User
        self._sensor(f"session_{short_id}_user", f"Session {device_name} User",
                    f"sessions/{session_id}/user", "mdi:account", device=device)
        
        # Session Client
        self._sensor(f"session_{short_id}_client", f"Session {device_name} Client",
                    f"sessions/{session_id}/client", "mdi:application", device=device)
        
        # Session Device
        self._sensor(f"session_{short_id}_device", f"Session {device_name} Device",
                    f"sessions/{session_id}/device", "mdi:devices", device=device)
        
        # Progress
        self._sensor(f"session_{short_id}_progress", f"Session {device_name} Progress",
                    f"sessions/{session_id}/progress", "mdi:percent", unit="%", device=device)
        
        # Position
        self._sensor(f"session_{short_id}_position", f"Session {device_name} Position",
                    f"sessions/{session_id}/position", "mdi:timer-outline", device=device)
        
        # Duration
        self._sensor(f"session_{short_id}_duration", f"Session {device_name} Duration",
                    f"sessions/{session_id}/duration", "mdi:timer", device=device)
        
        # Play Method
        self._sensor(f"session_{short_id}_play_method", f"Session {device_name} Play Method",
                    f"sessions/{session_id}/play_method", "mdi:play-network", device=device)
        
        # Media Title
        self._sensor(f"session_{short_id}_media", f"Session {device_name} Media",
                    f"sessions/{session_id}/media", "mdi:filmstrip", device=device)
        
        # Session Control Buttons
        self._button(f"session_{short_id}_play", f"Session {device_name} Play",
                    f"sessions/{session_id}/command", "play", "mdi:play", device=device)
        self._button(f"session_{short_id}_pause", f"Session {device_name} Pause",
                    f"sessions/{session_id}/command", "pause", "mdi:pause", device=device)
        self._button(f"session_{short_id}_stop", f"Session {device_name} Stop",
                    f"sessions/{session_id}/command", "stop", "mdi:stop", device=device)
        self._button(f"session_{short_id}_next", f"Session {device_name} Next",
                    f"sessions/{session_id}/command", "next", "mdi:skip-next", device=device)
        self._button(f"session_{short_id}_previous", f"Session {device_name} Previous",
                    f"sessions/{session_id}/command", "previous", "mdi:skip-previous", device=device)
        
        self.registered_sessions.add(session_id)
        logger.debug("Published session discovery for %s", device_name)
    
    def publish_user_discovery(self, user_id, user_name, server_info=None):
        """Publish discovery for a specific user"""
        device = self._device_info(server_info)
        safe_name = user_name.replace(" ", "_").lower()[:20]
        short_id = user_id[:8]
        
        # User Online Status
        self._binary_sensor(f"user_{short_id}_online", f"User {user_name} Online",
                           f"users/{user_id}/online", "mdi:account-check", device=device)
        
        # Last Activity
        self._sensor(f"user_{short_id}_last_activity", f"User {user_name} Last Activity",
                    f"users/{user_id}/last_activity", "mdi:clock-outline", device=device)
        
        # Last Played Item
        self._sensor(f"user_{short_id}_last_played", f"User {user_name} Last Played",
                    f"users/{user_id}/last_played", "mdi:play-circle-outline", device=device)
        
        # Is Admin
        self._binary_sensor(f"user_{short_id}_is_admin", f"User {user_name} Is Admin",
                           f"users/{user_id}/is_admin", "mdi:shield-account", device=device)
        
        # Is Disabled
        self._binary_sensor(f"user_{short_id}_is_disabled", f"User {user_name} Is Disabled",
                           f"users/{user_id}/is_disabled", "mdi:account-cancel", device=device)
    
    def publish_task_discovery(self, task_id, task_name, server_info=None):
        """Publish discovery for a specific scheduled task"""
        device = self._device_info(server_info)
        safe_name = task_name.replace(" ", "_").replace("/", "_").lower()[:30]
        short_id = task_id[:8] if len(task_id) > 8 else task_id
        
        # Task State
        self._sensor(f"task_{safe_name}_state", f"Task: {task_name} State",
                    f"tasks/{task_id}/state", "mdi:progress-check", device=device)
        
        # Task Progress
        self._sensor(f"task_{safe_name}_progress", f"Task: {task_name} Progress",
                    f"tasks/{task_id}/progress", "mdi:percent", unit="%", device=device)
        
        # Last Run Time
        self._sensor(f"task_{safe_name}_last_run", f"Task: {task_name} Last Run",
                    f"tasks/{task_id}/last_run", "mdi:clock-outline", device=device)
        
        # Start Button
        self._button(f"task_{safe_name}_start", f"Start: {task_name}",
                    f"tasks/{task_id}/command", "start", "mdi:play", device=device)
        
        # Stop Button
        self._button(f"task_{safe_name}_stop", f"Stop: {task_name}",
                    f"tasks/{task_id}/command", "stop", "mdi:stop", device=device)
    
    def publish_library_discovery(self, library_id, library_name, library_type, server_info=None):
        """Publish discovery for a specific library"""
        device = self._device_info(server_info)
        safe_name = library_name.replace(" ", "_").lower()[:20]
        short_id = library_id[:8]
        
        # Library Item Count
        self._sensor(f"library_{safe_name}_count", f"Library: {library_name} Items",
                    f"library/{library_id}/count", "mdi:folder-play", device=device)
        
        # Library Size
        self._sensor(f"library_{safe_name}_size", f"Library: {library_name} Size",
                    f"library/{library_id}/size", "mdi:harddisk", unit="GB", device=device)
        
        # Library Type
        self._sensor(f"library_{safe_name}_type", f"Library: {library_name} Type",
                    f"library/{library_id}/type", "mdi:tag", device=device)
        
        # Refresh Library Button
        self._button(f"library_{safe_name}_refresh", f"Refresh: {library_name}",
                    f"library/{library_id}/command", "refresh", "mdi:refresh", device=device)
    
    def publish_plugin_discovery(self, plugin_id, plugin_name, server_info=None):
        """Publish discovery for a specific plugin"""
        device = self._device_info(server_info)
        safe_name = plugin_name.replace(" ", "_").replace("-", "_").lower()[:25]
        short_id = plugin_id[:8]
        
        # Plugin Version
        self._sensor(f"plugin_{safe_name}_version", f"Plugin: {plugin_name} Version",
                    f"plugins/{plugin_id}/version", "mdi:tag", device=device)
        
        # Plugin Status
        self._sensor(f"plugin_{safe_name}_status", f"Plugin: {plugin_name} Status",
                    f"plugins/{plugin_id}/status", "mdi:information", device=device)
        
        # Plugin Enabled
        self._binary_sensor(f"plugin_{safe_name}_enabled", f"Plugin: {plugin_name} Enabled",
                           f"plugins/{plugin_id}/enabled", "mdi:puzzle-check", device=device)
    
    def publish_device_discovery(self, device_id, device_name, server_info=None):
        """Publish discovery for a specific client device"""
        device = self._device_info(server_info)
        safe_name = device_name.replace(" ", "_").replace("-", "_").lower()[:20]
        short_id = device_id[:8]
        
        # Device Last User
        self._sensor(f"device_{safe_name}_last_user", f"Device: {device_name} Last User",
                    f"devices/{device_id}/last_user", "mdi:account", device=device)
        
        # Device Last Seen
        self._sensor(f"device_{safe_name}_last_seen", f"Device: {device_name} Last Seen",
                    f"devices/{device_id}/last_seen", "mdi:clock-outline", device=device)
        
        # Device App Name
        self._sensor(f"device_{safe_name}_app", f"Device: {device_name} App",
                    f"devices/{device_id}/app", "mdi:application", device=device)
        
        # Delete Device Button
        self._button(f"device_{safe_name}_delete", f"Delete: {device_name}",
                    f"devices/{device_id}/command", "delete", "mdi:delete", device=device)
    
    def cleanup_stale_sessions(self, active_session_ids):
        """Remove discovery for sessions that are no longer active"""
        stale = self.registered_sessions - set(active_session_ids)
        for session_id in stale:
            short_id = session_id[:8]
            # Remove all session entities
            for entity in ['state', 'user', 'client', 'device', 'progress', 
                          'position', 'duration', 'play_method', 'media',
                          'play', 'pause', 'stop', 'next', 'previous']:
                component = "button" if entity in ['play', 'pause', 'stop', 'next', 'previous'] else "sensor"
                topic = f"{self.discovery_prefix}/{component}/jellyfin_{self.server_id}_session_{short_id}_{entity}/config"
                self.mqtt.publish(topic, "", retain=True)
            self.registered_sessions.discard(session_id)
            logger.debug("Cleaned up session discovery for %s", session_id)
