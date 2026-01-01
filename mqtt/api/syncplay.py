#!/usr/bin/env python3
"""
Jellyfin API - SyncPlay Group
Endpoints: 22
- Synchronized playback sessions
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class SyncPlayAPI(JellyfinAPIBase):
    """SyncPlay API endpoints"""
    
    GROUP_NAME = 'syncplay'
    
    # =========================================================================
    # SYNC PLAY GROUPS (3 endpoints)
    # =========================================================================
    
    def get_sync_play_groups(self) -> Optional[List]:
        """GET /SyncPlay/List - Get sync play groups"""
        return self._get('/SyncPlay/List')
    
    def sync_play_create_group(self, group_name: str = None) -> bool:
        """POST /SyncPlay/New - Create sync play group"""
        body = {'GroupName': group_name} if group_name else {}
        return self._post('/SyncPlay/New', json_data=body) is not None
    
    def sync_play_join(self, group_id: str) -> bool:
        """POST /SyncPlay/Join - Join sync play group"""
        return self._post('/SyncPlay/Join', json_data={'GroupId': group_id}) is not None
    
    def sync_play_leave(self) -> bool:
        """POST /SyncPlay/Leave - Leave sync play group"""
        return self._post('/SyncPlay/Leave') is not None
    
    # =========================================================================
    # SYNC PLAY BUFFERING/READY (2 endpoints)
    # =========================================================================
    
    def sync_play_buffering(self, when: str, position_ticks: int,
                            is_playing: bool, playlist_item_id: str) -> bool:
        """POST /SyncPlay/Buffering - Report buffering"""
        return self._post('/SyncPlay/Buffering', json_data={
            'When': when, 'PositionTicks': position_ticks,
            'IsPlaying': is_playing, 'PlaylistItemId': playlist_item_id
        }) is not None
    
    def sync_play_ready(self, when: str, position_ticks: int,
                        is_playing: bool, playlist_item_id: str) -> bool:
        """POST /SyncPlay/Ready - Report ready"""
        return self._post('/SyncPlay/Ready', json_data={
            'When': when, 'PositionTicks': position_ticks,
            'IsPlaying': is_playing, 'PlaylistItemId': playlist_item_id
        }) is not None
    
    # =========================================================================
    # SYNC PLAY CONTROLS (5 endpoints)
    # =========================================================================
    
    def sync_play_pause(self) -> bool:
        """POST /SyncPlay/Pause - Pause playback"""
        return self._post('/SyncPlay/Pause') is not None
    
    def sync_play_unpause(self) -> bool:
        """POST /SyncPlay/Unpause - Unpause playback"""
        return self._post('/SyncPlay/Unpause') is not None
    
    def sync_play_stop(self) -> bool:
        """POST /SyncPlay/Stop - Stop playback"""
        return self._post('/SyncPlay/Stop') is not None
    
    def sync_play_seek(self, position_ticks: int) -> bool:
        """POST /SyncPlay/Seek - Seek to position"""
        return self._post('/SyncPlay/Seek', json_data={'PositionTicks': position_ticks}) is not None
    
    def sync_play_ping(self, ping: int) -> bool:
        """POST /SyncPlay/Ping - Send ping"""
        return self._post('/SyncPlay/Ping', json_data={'Ping': ping}) is not None
    
    # =========================================================================
    # SYNC PLAY QUEUE (6 endpoints)
    # =========================================================================
    
    def sync_play_set_new_queue(self, play_queue: Dict) -> bool:
        """POST /SyncPlay/SetNewQueue - Set new queue"""
        return self._post('/SyncPlay/SetNewQueue', json_data=play_queue) is not None
    
    def sync_play_queue(self, item_ids: List[str], mode: str = 'Queue') -> bool:
        """POST /SyncPlay/Queue - Add to queue"""
        return self._post('/SyncPlay/Queue', json_data={
            'ItemIds': item_ids, 'Mode': mode
        }) is not None
    
    def sync_play_remove_from_playlist(self, playlist_item_ids: List[str]) -> bool:
        """POST /SyncPlay/RemoveFromPlaylist - Remove from playlist"""
        return self._post('/SyncPlay/RemoveFromPlaylist',
                         json_data={'PlaylistItemIds': playlist_item_ids}) is not None
    
    def sync_play_move_playlist_item(self, playlist_item_id: str, new_index: int) -> bool:
        """POST /SyncPlay/MovePlaylistItem - Move playlist item"""
        return self._post('/SyncPlay/MovePlaylistItem', json_data={
            'PlaylistItemId': playlist_item_id, 'NewIndex': new_index
        }) is not None
    
    def sync_play_set_playlist_item(self, playlist_item_id: str) -> bool:
        """POST /SyncPlay/SetPlaylistItem - Set current playlist item"""
        return self._post('/SyncPlay/SetPlaylistItem',
                         json_data={'PlaylistItemId': playlist_item_id}) is not None
    
    def sync_play_next_item(self, playlist_item_id: str = None) -> bool:
        """POST /SyncPlay/NextItem - Play next item"""
        body = {'PlaylistItemId': playlist_item_id} if playlist_item_id else {}
        return self._post('/SyncPlay/NextItem', json_data=body) is not None
    
    def sync_play_previous_item(self, playlist_item_id: str = None) -> bool:
        """POST /SyncPlay/PreviousItem - Play previous item"""
        body = {'PlaylistItemId': playlist_item_id} if playlist_item_id else {}
        return self._post('/SyncPlay/PreviousItem', json_data=body) is not None
    
    # =========================================================================
    # SYNC PLAY SETTINGS (3 endpoints)
    # =========================================================================
    
    def sync_play_set_repeat_mode(self, mode: str) -> bool:
        """POST /SyncPlay/SetRepeatMode - Set repeat mode"""
        return self._post('/SyncPlay/SetRepeatMode', json_data={'Mode': mode}) is not None
    
    def sync_play_set_shuffle_mode(self, mode: str) -> bool:
        """POST /SyncPlay/SetShuffleMode - Set shuffle mode"""
        return self._post('/SyncPlay/SetShuffleMode', json_data={'Mode': mode}) is not None
    
    def sync_play_set_ignore_wait(self, ignore_wait: bool) -> bool:
        """POST /SyncPlay/SetIgnoreWait - Set ignore wait"""
        return self._post('/SyncPlay/SetIgnoreWait',
                         json_data={'IgnoreWait': ignore_wait}) is not None
