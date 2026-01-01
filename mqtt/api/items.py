#!/usr/bin/env python3
"""
Jellyfin API - Items Group
Endpoints: 8
- Items, ItemUpdate, ItemRefresh
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class ItemsAPI(JellyfinAPIBase):
    """Items API endpoints"""
    
    GROUP_NAME = 'items'
    
    # =========================================================================
    # ITEMS (4 endpoints)
    # =========================================================================
    
    def get_items(self, user_id: str = None, parent_id: str = None,
                  include_item_types: List[str] = None, exclude_item_types: List[str] = None,
                  start_index: int = None, limit: int = None,
                  sort_by: str = None, sort_order: str = None,
                  recursive: bool = None, search_term: str = None,
                  is_favorite: bool = None, is_played: bool = None,
                  **kwargs) -> Optional[Dict]:
        """GET /Items - Get items"""
        params = {}
        if user_id:
            params['userId'] = user_id
        if parent_id:
            params['parentId'] = parent_id
        if include_item_types:
            params['includeItemTypes'] = ','.join(include_item_types)
        if exclude_item_types:
            params['excludeItemTypes'] = ','.join(exclude_item_types)
        if start_index is not None:
            params['startIndex'] = start_index
        if limit is not None:
            params['limit'] = limit
        if sort_by:
            params['sortBy'] = sort_by
        if sort_order:
            params['sortOrder'] = sort_order
        if recursive is not None:
            params['recursive'] = recursive
        if search_term:
            params['searchTerm'] = search_term
        if is_favorite is not None:
            params['isFavorite'] = is_favorite
        if is_played is not None:
            params['isPlayed'] = is_played
        params.update({k: v for k, v in kwargs.items() if v is not None})
        return self._get('/Items', params)
    
    def get_resume_items(self, user_id: str = None, start_index: int = None,
                         limit: int = None, media_types: List[str] = None,
                         parent_id: str = None) -> Optional[Dict]:
        """GET /UserItems/Resume - Get resume items"""
        params = {}
        if user_id:
            params['userId'] = user_id
        if start_index is not None:
            params['startIndex'] = start_index
        if limit is not None:
            params['limit'] = limit
        if media_types:
            params['mediaTypes'] = ','.join(media_types)
        if parent_id:
            params['parentId'] = parent_id
        return self._get('/UserItems/Resume', params)
    
    def get_user_item_data(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /UserItems/{itemId}/UserData - Get user data for item"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/UserItems/{item_id}/UserData', params)
    
    def update_user_item_data(self, item_id: str, user_data: Dict,
                              user_id: str = None) -> bool:
        """POST /UserItems/{itemId}/UserData - Update user data for item"""
        params = {'userId': user_id} if user_id else {}
        return self._post(f'/UserItems/{item_id}/UserData', 
                         params=params, json_data=user_data) is not None
    
    # =========================================================================
    # ITEM UPDATE (3 endpoints)
    # =========================================================================
    
    def get_metadata_editor_info(self, item_id: str) -> Optional[Dict]:
        """GET /Items/{itemId}/MetadataEditor - Get metadata editor info"""
        return self._get(f'/Items/{item_id}/MetadataEditor')
    
    def update_item(self, item_id: str, item: Dict) -> bool:
        """POST /Items/{itemId} - Update item"""
        return self._post(f'/Items/{item_id}', json_data=item) is not None
    
    def update_item_content_type(self, item_id: str, content_type: str) -> bool:
        """POST /Items/{itemId}/ContentType - Update item content type"""
        return self._post(f'/Items/{item_id}/ContentType',
                         params={'contentType': content_type}) is not None
    
    # =========================================================================
    # ITEM REFRESH (1 endpoint)
    # =========================================================================
    
    def refresh_item(self, item_id: str, metadata_refresh_mode: str = 'Default',
                     image_refresh_mode: str = 'Default',
                     replace_all_metadata: bool = False,
                     replace_all_images: bool = False) -> bool:
        """POST /Items/{itemId}/Refresh - Refresh item metadata"""
        params = {
            'metadataRefreshMode': metadata_refresh_mode,
            'imageRefreshMode': image_refresh_mode,
            'replaceAllMetadata': replace_all_metadata,
            'replaceAllImages': replace_all_images
        }
        return self._post(f'/Items/{item_id}/Refresh', params=params) is not None
