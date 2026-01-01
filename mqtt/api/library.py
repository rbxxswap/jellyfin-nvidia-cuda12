#!/usr/bin/env python3
"""
Jellyfin API - Library Group
Endpoints: 33
- Library management, virtual folders, media paths, refresh
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class LibraryAPI(JellyfinAPIBase):
    """Library API endpoints"""
    
    GROUP_NAME = 'library'
    
    # =========================================================================
    # LIBRARY (25 endpoints)
    # =========================================================================
    
    def delete_items(self, ids: List[str]) -> bool:
        """DELETE /Items - Delete items"""
        return self._delete('/Items', params={'ids': ','.join(ids)}) is not None
    
    def delete_item(self, item_id: str) -> bool:
        """DELETE /Items/{itemId} - Delete single item"""
        return self._delete(f'/Items/{item_id}') is not None
    
    def get_similar_albums(self, item_id: str, user_id: str = None,
                           limit: int = None) -> Optional[Dict]:
        """GET /Albums/{itemId}/Similar - Get similar albums"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Albums/{item_id}/Similar', params)
    
    def get_similar_artists(self, item_id: str, user_id: str = None,
                            limit: int = None) -> Optional[Dict]:
        """GET /Artists/{itemId}/Similar - Get similar artists"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Artists/{item_id}/Similar', params)
    
    def get_item_counts(self, user_id: str = None, is_favorite: bool = None) -> Optional[Dict]:
        """GET /Items/Counts - Get item counts"""
        params = {k: v for k, v in {'userId': user_id, 'isFavorite': is_favorite}.items() if v is not None}
        return self._get('/Items/Counts', params)
    
    def get_ancestors(self, item_id: str, user_id: str = None) -> Optional[List]:
        """GET /Items/{itemId}/Ancestors - Get item ancestors"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/Ancestors', params)
    
    def get_critic_reviews(self, item_id: str) -> Optional[Dict]:
        """GET /Items/{itemId}/CriticReviews - Get critic reviews"""
        return self._get(f'/Items/{item_id}/CriticReviews')
    
    def get_download_url(self, item_id: str) -> str:
        """GET /Items/{itemId}/Download - Get download URL"""
        return f"{self.base_url}/Items/{item_id}/Download?api_key={self.api_key}"
    
    def get_file_url(self, item_id: str) -> str:
        """GET /Items/{itemId}/File - Get file URL"""
        return f"{self.base_url}/Items/{item_id}/File?api_key={self.api_key}"
    
    def get_similar_items(self, item_id: str, user_id: str = None,
                          limit: int = None) -> Optional[Dict]:
        """GET /Items/{itemId}/Similar - Get similar items"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Items/{item_id}/Similar', params)
    
    def get_theme_media(self, item_id: str, user_id: str = None,
                        inherit_from_parent: bool = True) -> Optional[Dict]:
        """GET /Items/{itemId}/ThemeMedia - Get theme media"""
        params = {'userId': user_id, 'inheritFromParent': inherit_from_parent}
        params = {k: v for k, v in params.items() if v is not None}
        return self._get(f'/Items/{item_id}/ThemeMedia', params)
    
    def get_theme_songs(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /Items/{itemId}/ThemeSongs - Get theme songs"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/ThemeSongs', params)
    
    def get_theme_videos(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /Items/{itemId}/ThemeVideos - Get theme videos"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/ThemeVideos', params)
    
    def get_library_options(self) -> Optional[Dict]:
        """GET /Libraries/AvailableOptions - Get library options"""
        return self._get('/Libraries/AvailableOptions')
    
    def get_media_folders(self, is_hidden: bool = None) -> Optional[Dict]:
        """GET /Library/MediaFolders - Get media folders"""
        params = {'isHidden': is_hidden} if is_hidden is not None else {}
        return self._get('/Library/MediaFolders', params)
    
    def get_physical_paths(self) -> Optional[List]:
        """GET /Library/PhysicalPaths - Get physical paths"""
        return self._get('/Library/PhysicalPaths')
    
    def get_similar_movies(self, item_id: str, user_id: str = None,
                           limit: int = None) -> Optional[Dict]:
        """GET /Movies/{itemId}/Similar - Get similar movies"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Movies/{item_id}/Similar', params)
    
    def get_similar_shows(self, item_id: str, user_id: str = None,
                          limit: int = None) -> Optional[Dict]:
        """GET /Shows/{itemId}/Similar - Get similar shows"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Shows/{item_id}/Similar', params)
    
    def get_similar_trailers(self, item_id: str, user_id: str = None,
                             limit: int = None) -> Optional[Dict]:
        """GET /Trailers/{itemId}/Similar - Get similar trailers"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Trailers/{item_id}/Similar', params)
    
    def report_media_updated(self, updates: Dict) -> bool:
        """POST /Library/Media/Updated - Report media updated"""
        return self._post('/Library/Media/Updated', json_data=updates) is not None
    
    def report_movies_added(self, updates: Dict) -> bool:
        """POST /Library/Movies/Added - Report movies added"""
        return self._post('/Library/Movies/Added', json_data=updates) is not None
    
    def report_movies_updated(self, updates: Dict) -> bool:
        """POST /Library/Movies/Updated - Report movies updated"""
        return self._post('/Library/Movies/Updated', json_data=updates) is not None
    
    def refresh_library(self) -> bool:
        """POST /Library/Refresh - Refresh entire library"""
        return self._post('/Library/Refresh') is not None
    
    def start_library_scan(self) -> bool:
        """Trigger a library scan (alias for refresh_library)"""
        return self.refresh_library()
    
    def report_series_added(self, updates: Dict) -> bool:
        """POST /Library/Series/Added - Report series added"""
        return self._post('/Library/Series/Added', json_data=updates) is not None
    
    def report_series_updated(self, updates: Dict) -> bool:
        """POST /Library/Series/Updated - Report series updated"""
        return self._post('/Library/Series/Updated', json_data=updates) is not None
    
    # =========================================================================
    # LIBRARY STRUCTURE (8 endpoints)
    # =========================================================================
    
    def get_virtual_folders(self) -> Optional[List]:
        """GET /Library/VirtualFolders - Get virtual folders (libraries)"""
        return self._get('/Library/VirtualFolders')
    
    def add_virtual_folder(self, name: str, collection_type: str = None,
                           paths: List[str] = None, refresh_library: bool = False) -> bool:
        """POST /Library/VirtualFolders - Add virtual folder"""
        params = {'name': name, 'refreshLibrary': refresh_library}
        if collection_type:
            params['collectionType'] = collection_type
        body = {}
        if paths:
            body['PathInfos'] = [{'Path': p} for p in paths]
        return self._post('/Library/VirtualFolders', params=params, json_data=body) is not None
    
    def delete_virtual_folder(self, name: str, refresh_library: bool = False) -> bool:
        """DELETE /Library/VirtualFolders - Delete virtual folder"""
        return self._delete('/Library/VirtualFolders',
                           params={'name': name, 'refreshLibrary': refresh_library}) is not None
    
    def update_library_options(self, library_options: Dict) -> bool:
        """POST /Library/VirtualFolders/LibraryOptions - Update library options"""
        return self._post('/Library/VirtualFolders/LibraryOptions',
                         json_data=library_options) is not None
    
    def rename_virtual_folder(self, name: str, new_name: str,
                              refresh_library: bool = False) -> bool:
        """POST /Library/VirtualFolders/Name - Rename virtual folder"""
        return self._post('/Library/VirtualFolders/Name',
                         params={'name': name, 'newName': new_name,
                                'refreshLibrary': refresh_library}) is not None
    
    def add_media_path(self, name: str, path: str, path_info: Dict = None) -> bool:
        """POST /Library/VirtualFolders/Paths - Add media path"""
        body = path_info or {}
        body['Path'] = path
        return self._post('/Library/VirtualFolders/Paths',
                         params={'name': name}, json_data=body) is not None
    
    def remove_media_path(self, name: str, path: str,
                          refresh_library: bool = False) -> bool:
        """DELETE /Library/VirtualFolders/Paths - Remove media path"""
        return self._delete('/Library/VirtualFolders/Paths',
                           params={'name': name, 'path': path,
                                  'refreshLibrary': refresh_library}) is not None
    
    def update_media_path(self, name: str, path_info: Dict) -> bool:
        """POST /Library/VirtualFolders/Paths/Update - Update media path"""
        return self._post('/Library/VirtualFolders/Paths/Update',
                         params={'name': name}, json_data=path_info) is not None
