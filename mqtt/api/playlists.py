#!/usr/bin/env python3
"""
Jellyfin API - Playlists Group
Endpoints: 11
- Playlist management
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class PlaylistsAPI(JellyfinAPIBase):
    """Playlists API endpoints"""
    
    GROUP_NAME = 'playlists'
    
    # =========================================================================
    # PLAYLISTS (11 endpoints)
    # =========================================================================
    
    def create_playlist(self, name: str = None, ids: List[str] = None,
                        user_id: str = None, media_type: str = None) -> Optional[Dict]:
        """POST /Playlists - Create playlist"""
        body = {}
        if name:
            body['Name'] = name
        if ids:
            body['Ids'] = ids
        if user_id:
            body['UserId'] = user_id
        if media_type:
            body['MediaType'] = media_type
        return self._post('/Playlists', json_data=body)
    
    def get_playlist(self, playlist_id: str) -> Optional[Dict]:
        """GET /Playlists/{playlistId} - Get playlist"""
        return self._get(f'/Playlists/{playlist_id}')
    
    def update_playlist(self, playlist_id: str, playlist: Dict) -> bool:
        """POST /Playlists/{playlistId} - Update playlist"""
        return self._post(f'/Playlists/{playlist_id}', json_data=playlist) is not None
    
    def get_playlist_items(self, playlist_id: str, user_id: str = None,
                           start_index: int = None, limit: int = None) -> Optional[Dict]:
        """GET /Playlists/{playlistId}/Items - Get playlist items"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit
        }.items() if v is not None}
        return self._get(f'/Playlists/{playlist_id}/Items', params)
    
    def add_playlist_items(self, playlist_id: str, ids: List[str],
                           user_id: str = None) -> bool:
        """POST /Playlists/{playlistId}/Items - Add items to playlist"""
        params = {'ids': ','.join(ids)}
        if user_id:
            params['userId'] = user_id
        return self._post(f'/Playlists/{playlist_id}/Items', params=params) is not None
    
    def remove_playlist_items(self, playlist_id: str, entry_ids: List[str]) -> bool:
        """DELETE /Playlists/{playlistId}/Items - Remove items from playlist"""
        return self._delete(f'/Playlists/{playlist_id}/Items',
                           params={'entryIds': ','.join(entry_ids)}) is not None
    
    def move_playlist_item(self, playlist_id: str, item_id: str, new_index: int) -> bool:
        """POST /Playlists/{playlistId}/Items/{itemId}/Move/{newIndex} - Move playlist item"""
        return self._post(f'/Playlists/{playlist_id}/Items/{item_id}/Move/{new_index}') is not None
    
    def get_playlist_users(self, playlist_id: str) -> Optional[List]:
        """GET /Playlists/{playlistId}/Users - Get playlist users"""
        return self._get(f'/Playlists/{playlist_id}/Users')
    
    def get_playlist_user(self, playlist_id: str, user_id: str) -> Optional[Dict]:
        """GET /Playlists/{playlistId}/Users/{userId} - Get playlist user"""
        return self._get(f'/Playlists/{playlist_id}/Users/{user_id}')
    
    def add_playlist_user(self, playlist_id: str, user_id: str, can_edit: bool = None) -> bool:
        """POST /Playlists/{playlistId}/Users/{userId} - Add user to playlist"""
        body = {'CanEdit': can_edit} if can_edit is not None else {}
        return self._post(f'/Playlists/{playlist_id}/Users/{user_id}', json_data=body) is not None
    
    def remove_playlist_user(self, playlist_id: str, user_id: str) -> bool:
        """DELETE /Playlists/{playlistId}/Users/{userId} - Remove user from playlist"""
        return self._delete(f'/Playlists/{playlist_id}/Users/{user_id}') is not None
