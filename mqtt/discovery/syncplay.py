#!/usr/bin/env python3
"""
Discovery - SyncPlay Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class SyncPlayDiscovery(DiscoveryBase):
    """SyncPlay group - ALLE Entities"""
    
    GROUP_NAME = 'syncplay'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registered_groups = set()
    
    def register_all(self):
        """Register ALLE syncplay entities"""
        
        # =====================================================================
        # GET /SyncPlay/List - SyncPlay Groups List
        # =====================================================================
        self.sensor("syncplay_groups_count", "SyncPlay Groups Count", "syncplay/groups/count", "mdi:account-group-outline")
        self.sensor("syncplay_groups_list", "SyncPlay Groups List", "syncplay/groups/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # POST /SyncPlay/New - Create SyncPlay Group
        # =====================================================================
        self.button("syncplay_create_group", "Create SyncPlay Group", "syncplay/command", "create", "mdi:account-group")
        
        # =====================================================================
        # POST /SyncPlay/Join - Join SyncPlay Group
        # =====================================================================
        self.button("syncplay_join_group", "Join SyncPlay Group", "syncplay/command", "join", "mdi:account-arrow-right")
        
        # =====================================================================
        # POST /SyncPlay/Leave - Leave SyncPlay Group
        # =====================================================================
        self.button("syncplay_leave_group", "Leave SyncPlay Group", "syncplay/command", "leave", "mdi:account-arrow-left")
        
        # =====================================================================
        # POST /SyncPlay/Play - SyncPlay Play
        # =====================================================================
        self.button("syncplay_play", "SyncPlay Play", "syncplay/control", "play", "mdi:play")
        
        # =====================================================================
        # POST /SyncPlay/Pause - SyncPlay Pause
        # =====================================================================
        self.button("syncplay_pause", "SyncPlay Pause", "syncplay/control", "pause", "mdi:pause")
        
        # =====================================================================
        # POST /SyncPlay/Unpause - SyncPlay Unpause
        # =====================================================================
        self.button("syncplay_unpause", "SyncPlay Unpause", "syncplay/control", "unpause", "mdi:play")
        
        # =====================================================================
        # POST /SyncPlay/Stop - SyncPlay Stop
        # =====================================================================
        self.button("syncplay_stop", "SyncPlay Stop", "syncplay/control", "stop", "mdi:stop")
        
        # =====================================================================
        # POST /SyncPlay/Seek - SyncPlay Seek
        # =====================================================================
        self.button("syncplay_seek", "SyncPlay Seek", "syncplay/control", "seek", "mdi:fast-forward")
        
        # =====================================================================
        # POST /SyncPlay/Buffering - SyncPlay Buffering
        # =====================================================================
        self.button("syncplay_buffering", "SyncPlay Buffering", "syncplay/control", "buffering", "mdi:buffer")
        
        # =====================================================================
        # POST /SyncPlay/Ready - SyncPlay Ready
        # =====================================================================
        self.button("syncplay_ready", "SyncPlay Ready", "syncplay/control", "ready", "mdi:check")
        
        # =====================================================================
        # POST /SyncPlay/SetIgnoreWait - Set Ignore Wait
        # =====================================================================
        self.button("syncplay_set_ignore_wait", "SyncPlay Ignore Wait", "syncplay/control", "ignore_wait", "mdi:timer-off")
        
        # =====================================================================
        # POST /SyncPlay/SetNewQueue - Set New Queue
        # =====================================================================
        self.button("syncplay_set_queue", "SyncPlay Set Queue", "syncplay/control", "set_queue", "mdi:playlist-play")
        
        # =====================================================================
        # POST /SyncPlay/SetPlaylistItem - Set Playlist Item
        # =====================================================================
        self.button("syncplay_set_playlist_item", "SyncPlay Set Item", "syncplay/control", "set_item", "mdi:playlist-check")
        
        # =====================================================================
        # POST /SyncPlay/RemoveFromPlaylist - Remove From Playlist
        # =====================================================================
        self.button("syncplay_remove_from_playlist", "SyncPlay Remove Item", "syncplay/control", "remove_item", "mdi:playlist-remove")
        
        # =====================================================================
        # POST /SyncPlay/MovePlaylistItem - Move Playlist Item
        # =====================================================================
        self.button("syncplay_move_playlist_item", "SyncPlay Move Item", "syncplay/control", "move_item", "mdi:playlist-edit")
        
        # =====================================================================
        # POST /SyncPlay/Queue - Add To Queue
        # =====================================================================
        self.button("syncplay_add_to_queue", "SyncPlay Add To Queue", "syncplay/control", "add_queue", "mdi:playlist-plus")
        
        # =====================================================================
        # POST /SyncPlay/NextItem - Next Item
        # =====================================================================
        self.button("syncplay_next_item", "SyncPlay Next", "syncplay/control", "next", "mdi:skip-next")
        
        # =====================================================================
        # POST /SyncPlay/PreviousItem - Previous Item
        # =====================================================================
        self.button("syncplay_previous_item", "SyncPlay Previous", "syncplay/control", "previous", "mdi:skip-previous")
        
        # =====================================================================
        # POST /SyncPlay/SetRepeatMode - Set Repeat Mode
        # =====================================================================
        self.button("syncplay_set_repeat", "SyncPlay Set Repeat", "syncplay/control", "set_repeat", "mdi:repeat")
        
        # =====================================================================
        # POST /SyncPlay/SetShuffleMode - Set Shuffle Mode
        # =====================================================================
        self.button("syncplay_set_shuffle", "SyncPlay Set Shuffle", "syncplay/control", "set_shuffle", "mdi:shuffle")
        
        # =====================================================================
        # POST /SyncPlay/Ping - SyncPlay Ping
        # =====================================================================
        # Internal use
        
        return self.entity_count
    
    def register_group(self, group_id, group_name, participants=None):
        """Register ALLE Entities für eine SyncPlay Group"""
        if group_id in self.registered_groups:
            return 0
        
        safe_name = group_name.replace(" ", "_").lower()[:20]
        prefix = f"syncplay_{safe_name}"
        base_topic = f"syncplay/{group_id}"
        
        # =====================================================================
        # Group Info
        # =====================================================================
        self.sensor(f"{prefix}_name", f"SyncPlay: {group_name}", f"{base_topic}/GroupName", "mdi:account-group")
        self.sensor(f"{prefix}_id", f"{group_name} ID", f"{base_topic}/GroupId", "mdi:identifier")
        self.sensor(f"{prefix}_participants_count", f"{group_name} Participants", f"{base_topic}/Participants/count", "mdi:account-multiple")
        self.sensor(f"{prefix}_participants", f"{group_name} Participants List", f"{base_topic}/Participants", "mdi:format-list-bulleted")
        
        # =====================================================================
        # Group State
        # =====================================================================
        self.sensor(f"{prefix}_state", f"{group_name} State", f"{base_topic}/State", "mdi:play-circle")
        self.sensor(f"{prefix}_position", f"{group_name} Position", f"{base_topic}/PositionTicks", "mdi:timer-outline")
        self.sensor(f"{prefix}_now_playing", f"{group_name} Now Playing", f"{base_topic}/NowPlaying", "mdi:filmstrip")
        
        # =====================================================================
        # Group Control Buttons
        # =====================================================================
        self.button(f"{prefix}_play", f"Play: {group_name}", f"{base_topic}/command", "play", "mdi:play")
        self.button(f"{prefix}_pause", f"Pause: {group_name}", f"{base_topic}/command", "pause", "mdi:pause")
        self.button(f"{prefix}_stop", f"Stop: {group_name}", f"{base_topic}/command", "stop", "mdi:stop")
        self.button(f"{prefix}_next", f"Next: {group_name}", f"{base_topic}/command", "next", "mdi:skip-next")
        self.button(f"{prefix}_previous", f"Previous: {group_name}", f"{base_topic}/command", "previous", "mdi:skip-previous")
        
        self.registered_groups.add(group_id)
        return self.entity_count
