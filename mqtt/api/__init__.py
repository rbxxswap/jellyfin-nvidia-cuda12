#!/usr/bin/env python3
"""
Jellyfin API - Modular API Client
Each group can be enabled/disabled via MQTT switches
Total: ~315 Endpoints in 14 modules
"""

from .base import JellyfinAPIBase
from .system import SystemAPI
from .sessions import SessionsAPI, parse_session
from .library import LibraryAPI
from .items import ItemsAPI
from .users import UsersAPI
from .playstate import PlaystateAPI
from .tasks import TasksAPI
from .devices import DevicesAPI
from .plugins import PluginsAPI
from .livetv import LiveTvAPI
from .syncplay import SyncPlayAPI
from .playlists import PlaylistsAPI
from .media import MediaAPI
from .images import ImagesAPI
from .misc import MiscAPI


class JellyfinAPI:
    """
    Main Jellyfin API client with modular groups
    Each group can be enabled/disabled for polling
    """
    
    # Available API groups with descriptions
    GROUPS = {
        'system': 'Server info, logs, restart, shutdown, configuration',
        'sessions': 'Active sessions, playback control, messages',
        'library': 'Library management, virtual folders, refresh',
        'items': 'Item queries, metadata updates',
        'users': 'User management, authentication, views',
        'playstate': 'Playback reporting, mark played/unplayed',
        'tasks': 'Scheduled tasks management',
        'devices': 'Device management',
        'plugins': 'Plugins and packages management',
        'livetv': 'Live TV channels, recordings, timers',
        'syncplay': 'Synchronized playback sessions',
        'playlists': 'Playlist management',
        'media': 'Search, artists, genres, TV shows, movies',
        'images': 'Image management and retrieval',
        'misc': 'Subtitles, channels, backup, localization, etc.',
    }
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        
        # Group enabled states (all enabled by default)
        self._group_enabled = {group: False for group in self.GROUPS}
        
        # Initialize API modules
        self.system = SystemAPI(base_url, api_key)
        self.sessions = SessionsAPI(base_url, api_key)
        self.library = LibraryAPI(base_url, api_key)
        self.items = ItemsAPI(base_url, api_key)
        self.users = UsersAPI(base_url, api_key)
        self.playstate = PlaystateAPI(base_url, api_key)
        self.tasks = TasksAPI(base_url, api_key)
        self.devices = DevicesAPI(base_url, api_key)
        self.plugins = PluginsAPI(base_url, api_key)
        self.livetv = LiveTvAPI(base_url, api_key)
        self.syncplay = SyncPlayAPI(base_url, api_key)
        self.playlists = PlaylistsAPI(base_url, api_key)
        self.media = MediaAPI(base_url, api_key)
        self.images = ImagesAPI(base_url, api_key)
        self.misc = MiscAPI(base_url, api_key)
    
    def is_group_enabled(self, group: str) -> bool:
        """Check if a group is enabled for polling"""
        return self._group_enabled.get(group, False)
    
    def set_group_enabled(self, group: str, enabled: bool):
        """Enable/disable a group for polling"""
        if group in self._group_enabled:
            self._group_enabled[group] = enabled
    
    def get_enabled_groups(self) -> list:
        """Get list of enabled groups"""
        return [g for g, enabled in self._group_enabled.items() if enabled]
    
    def get_disabled_groups(self) -> list:
        """Get list of disabled groups"""
        return [g for g, enabled in self._group_enabled.items() if not enabled]
    
    def get_all_group_states(self) -> dict:
        """Get all group states"""
        return self._group_enabled.copy()
    
    def enable_all_groups(self):
        """Enable all groups"""
        for group in self._group_enabled:
            self._group_enabled[group] = True
    
    def disable_all_groups(self):
        """Disable all groups"""
        for group in self._group_enabled:
            self._group_enabled[group] = False
    
    def get_module(self, group: str):
        """Get API module by group name"""
        return getattr(self, group, None)
    
    # =========================================================================
    # CONVENIENCE METHODS (delegate to modules)
    # =========================================================================
    
    def get_system_info(self):
        """Get system info (delegates to system module)"""
        return self.system.get_system_info()
    
    def ping(self) -> bool:
        """Ping server (delegates to system module)"""
        return self.system.ping()
    
    def get_sessions(self):
        """Get active sessions (delegates to sessions module)"""
        return self.sessions.get_sessions()
    
    def get_scheduled_tasks(self):
        """Get scheduled tasks (delegates to tasks module)"""
        return self.tasks.get_scheduled_tasks()
    
    def refresh_library(self) -> bool:
        """Refresh library (delegates to library module)"""
        return self.library.refresh_library()
    
    def start_library_scan(self) -> bool:
        """Start library scan (alias for refresh_library)"""
        return self.library.start_library_scan()
    
    def send_playstate_command(self, session_id: str, command: str) -> bool:
        """Send playstate command (delegates to sessions module)"""
        return self.sessions.send_playstate_command(session_id, command)
    
    def get_server_id(self) -> str:
        """Get server ID (delegates to system module)"""
        return self.system.get_server_id()


__all__ = [
    'JellyfinAPI',
    'JellyfinAPIBase',
    'SystemAPI',
    'SessionsAPI',
    'LibraryAPI',
    'ItemsAPI',
    'UsersAPI',
    'PlaystateAPI',
    'TasksAPI',
    'DevicesAPI',
    'PluginsAPI',
    'LiveTvAPI',
    'SyncPlayAPI',
    'PlaylistsAPI',
    'MediaAPI',
    'ImagesAPI',
    'MiscAPI',
    'parse_session',
]
