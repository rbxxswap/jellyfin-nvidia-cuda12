#!/usr/bin/env python3
"""
Discovery Module - Manages MQTT Discovery for Home Assistant
Coordinates all group-specific discovery modules
"""

import logging
from config import get_config

from .base import DiscoveryBase
from .system import SystemDiscovery
from .sessions import SessionsDiscovery
from .library import LibraryDiscovery
from .items import ItemsDiscovery
from .users import UsersDiscovery
from .playstate import PlaystateDiscovery
from .tasks import TasksDiscovery
from .devices import DevicesDiscovery
from .plugins import PluginsDiscovery
from .livetv import LiveTVDiscovery
from .syncplay import SyncPlayDiscovery
from .playlists import PlaylistsDiscovery
from .media import MediaDiscovery
from .images import ImagesDiscovery
from .misc import MiscDiscovery

logger = logging.getLogger(__name__)


class DiscoveryManager:
    """Main discovery manager - coordinates all discovery modules"""
    
    def __init__(self, mqtt_client, server_info=None):
        self.mqtt = mqtt_client
        self.config = get_config()
        self.base_topic = self.config.mqtt_topic
        self.discovery_prefix = self.config.mqtt_discovery_prefix
        self.server_id = self.config.server_id
        self.server_info = server_info
        
        # Build device info
        self.device_info = self._build_device_info()
        
        # Initialize all discovery modules
        args = (mqtt_client, self.base_topic, self.discovery_prefix, self.server_id, self.device_info)
        
        self.system = SystemDiscovery(*args)
        self.sessions = SessionsDiscovery(*args)
        self.library = LibraryDiscovery(*args)
        self.items = ItemsDiscovery(*args)
        self.users = UsersDiscovery(*args)
        self.playstate = PlaystateDiscovery(*args)
        self.tasks = TasksDiscovery(*args)
        self.devices = DevicesDiscovery(*args)
        self.plugins = PluginsDiscovery(*args)
        self.livetv = LiveTVDiscovery(*args)
        self.syncplay = SyncPlayDiscovery(*args)
        self.playlists = PlaylistsDiscovery(*args)
        self.media = MediaDiscovery(*args)
        self.images = ImagesDiscovery(*args)
        self.misc = MiscDiscovery(*args)
        
        # Module mapping
        self.modules = {
            'system': self.system,
            'sessions': self.sessions,
            'library': self.library,
            'items': self.items,
            'users': self.users,
            'playstate': self.playstate,
            'tasks': self.tasks,
            'devices': self.devices,
            'plugins': self.plugins,
            'livetv': self.livetv,
            'syncplay': self.syncplay,
            'playlists': self.playlists,
            'media': self.media,
            'images': self.images,
            'misc': self.misc
        }
    
    def _build_device_info(self):
        """Build HA device info block"""
        version = 'Unknown'
        if self.server_info:
            version = self.server_info.get('Version', 'Unknown')
        
        return {
            "identifiers": [f"jellyfin_{self.server_id}"],
            "name": "Jellyfin Media Server",
            "manufacturer": "Jellyfin",
            "model": f"Jellyfin {version}",
            "sw_version": "MQTT Bridge 2.0",
            "configuration_url": self.config.jellyfin_host
        }
    
    def update_server_info(self, server_info):
        """Update server info and rebuild device info"""
        self.server_info = server_info
        self.device_info = self._build_device_info()
        
        # Update all modules
        for module in self.modules.values():
            module.device_info = self.device_info
    
    def register_all_static(self):
        """Register all static entities from all modules"""
        total = 0
        for name, module in self.modules.items():
            count = module.register_all()
            logger.debug("Registered %d entities for %s", count, name)
            total += count
        
        logger.info("Published discovery for %d static entities", total)
        return total
    
    def register_group_switches(self, groups):
        """Register switches for API group enable/disable"""
        base = DiscoveryBase(self.mqtt, self.base_topic, self.discovery_prefix, 
                            self.server_id, self.device_info)
        
        for group_name, description in groups.items():
            base.switch(
                f"group_{group_name}",
                f"Jellyfin {group_name.title()} Polling",
                f"groups/{group_name}/state",
                f"groups/{group_name}/set",
                "mdi:api"
            )
        
        logger.info("Published discovery for %d group switches", len(groups))
        return len(groups)
    
    # === Dynamic Registration Methods ===
    
    def register_session(self, session_id, device_name, user_name, client_name):
        """Register a specific session"""
        return self.sessions.register_session(session_id, device_name, user_name, client_name)
    
    def unregister_session(self, session_id):
        """Unregister a session"""
        return self.sessions.unregister_session(session_id)
    
    def cleanup_stale_sessions(self, active_session_ids):
        """Cleanup stale sessions"""
        return self.sessions.cleanup_stale_sessions(active_session_ids)
    
    def register_library(self, library_id, library_name, library_type, locations=None):
        """Register a specific library"""
        return self.library.register_library(library_id, library_name, library_type, locations)
    
    def register_user(self, user_id, user_name, is_admin=False):
        """Register a specific user"""
        return self.users.register_user(user_id, user_name, is_admin)
    
    def register_task(self, task_id, task_name, task_key):
        """Register a specific task"""
        return self.tasks.register_task(task_id, task_name, task_key)
    
    def register_device(self, device_id, device_name, app_name):
        """Register a specific device"""
        return self.devices.register_device(device_id, device_name, app_name)
    
    def register_plugin(self, plugin_id, plugin_name, version):
        """Register a specific plugin"""
        return self.plugins.register_plugin(plugin_id, plugin_name, version)
    
    def register_playlist(self, playlist_id, playlist_name, media_type):
        """Register a specific playlist"""
        return self.playlists.register_playlist(playlist_id, playlist_name, media_type)
    
    def register_syncplay_group(self, group_id, group_name):
        """Register a specific syncplay group"""
        return self.syncplay.register_group(group_id, group_name)
