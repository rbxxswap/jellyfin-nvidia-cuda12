#!/usr/bin/env python3
"""
Discovery - Playlists Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class PlaylistsDiscovery(DiscoveryBase):
    """Playlists group - ALLE Entities"""
    
    GROUP_NAME = 'playlists'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registered_playlists = set()
    
    def register_all(self):
        """Register ALLE playlist entities"""
        
        # =====================================================================
        # Playlist Counts
        # =====================================================================
        self.sensor("playlists_count", "Playlists Count", "playlists/count", "mdi:playlist-music")
        self.sensor("playlists_music_count", "Music Playlists Count", "playlists/music/count", "mdi:playlist-music")
        self.sensor("playlists_video_count", "Video Playlists Count", "playlists/video/count", "mdi:playlist-play")
        self.sensor("playlists_list", "Playlists List", "playlists/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # POST /Playlists - Create Playlist
        # =====================================================================
        self.button("create_playlist", "Create Playlist", "playlists/command", "create", "mdi:playlist-plus")
        
        # =====================================================================
        # Playlist details (first 10)
        # =====================================================================
        for i in range(10):
            self.sensor(f"playlist_{i}_name", f"Playlist {i+1} Name", f"playlists/{i}/Name", "mdi:playlist-music")
            self.sensor(f"playlist_{i}_id", f"Playlist {i+1} ID", f"playlists/{i}/Id", "mdi:identifier")
            self.sensor(f"playlist_{i}_item_count", f"Playlist {i+1} Items", f"playlists/{i}/ChildCount", "mdi:numeric")
            self.sensor(f"playlist_{i}_media_type", f"Playlist {i+1} Type", f"playlists/{i}/MediaType", "mdi:tag")
            self.sensor(f"playlist_{i}_runtime", f"Playlist {i+1} Runtime", f"playlists/{i}/RunTimeTicks", "mdi:timer")
        
        return self.entity_count
    
    def register_playlist(self, playlist_id, playlist_name, media_type=None, item_count=None, runtime_ticks=None):
        """Register ALLE Entities für eine spezifische Playlist"""
        if playlist_id in self.registered_playlists:
            return 0
        
        safe_name = playlist_name.replace(" ", "_").lower()[:20]
        prefix = f"playlist_{safe_name}"
        base_topic = f"playlists/{playlist_id}"
        
        icon = "mdi:playlist-music" if media_type == "Audio" else "mdi:playlist-play"
        
        # =====================================================================
        # Playlist Info
        # =====================================================================
        self.sensor(f"{prefix}_name", f"Playlist: {playlist_name}", f"{base_topic}/Name", icon)
        self.sensor(f"{prefix}_id", f"{playlist_name} ID", f"{base_topic}/Id", "mdi:identifier")
        self.sensor(f"{prefix}_media_type", f"{playlist_name} Media Type", f"{base_topic}/MediaType", "mdi:tag")
        self.sensor(f"{prefix}_child_count", f"{playlist_name} Item Count", f"{base_topic}/ChildCount", "mdi:numeric")
        self.sensor(f"{prefix}_runtime_ticks", f"{playlist_name} Runtime Ticks", f"{base_topic}/RunTimeTicks", "mdi:timer")
        self.sensor(f"{prefix}_runtime", f"{playlist_name} Runtime", f"{base_topic}/runtime", "mdi:timer")
        self.sensor(f"{prefix}_date_created", f"{playlist_name} Created", f"{base_topic}/DateCreated", "mdi:calendar")
        self.sensor(f"{prefix}_overview", f"{playlist_name} Overview", f"{base_topic}/Overview", "mdi:text")
        
        # =====================================================================
        # Playlist Items
        # =====================================================================
        self.sensor(f"{prefix}_items_count", f"{playlist_name} Items Count", f"{base_topic}/Items/count", "mdi:numeric")
        self.sensor(f"{prefix}_items_list", f"{playlist_name} Items List", f"{base_topic}/Items/list", "mdi:format-list-bulleted")
        
        # First 5 items in playlist
        for i in range(5):
            self.sensor(f"{prefix}_item_{i}_name", f"{playlist_name} Item {i+1}", f"{base_topic}/Items/{i}/Name", "mdi:music")
            self.sensor(f"{prefix}_item_{i}_id", f"{playlist_name} Item {i+1} ID", f"{base_topic}/Items/{i}/Id", "mdi:identifier")
        
        # =====================================================================
        # Playlist User Data
        # =====================================================================
        self.sensor(f"{prefix}_play_count", f"{playlist_name} Play Count", f"{base_topic}/UserData/PlayCount", "mdi:play-circle")
        self.binary_sensor(f"{prefix}_is_favorite", f"{playlist_name} Is Favorite", f"{base_topic}/UserData/IsFavorite", "mdi:heart")
        self.binary_sensor(f"{prefix}_played", f"{playlist_name} Played", f"{base_topic}/UserData/Played", "mdi:check")
        
        # =====================================================================
        # Playlist Control Buttons
        # =====================================================================
        self.button(f"{prefix}_play", f"Play: {playlist_name}", f"{base_topic}/command", "play", "mdi:play")
        self.button(f"{prefix}_shuffle", f"Shuffle: {playlist_name}", f"{base_topic}/command", "shuffle", "mdi:shuffle")
        self.button(f"{prefix}_delete", f"Delete: {playlist_name}", f"{base_topic}/command", "delete", "mdi:delete")
        self.button(f"{prefix}_add_item", f"Add Item: {playlist_name}", f"{base_topic}/command", "add_item", "mdi:plus")
        self.button(f"{prefix}_remove_item", f"Remove Item: {playlist_name}", f"{base_topic}/command", "remove_item", "mdi:minus")
        self.button(f"{prefix}_move_item", f"Move Item: {playlist_name}", f"{base_topic}/command", "move_item", "mdi:arrow-up-down")
        
        self.registered_playlists.add(playlist_id)
        return self.entity_count
