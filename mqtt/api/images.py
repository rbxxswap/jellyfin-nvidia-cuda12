#!/usr/bin/env python3
"""
Jellyfin API - Images Group
Endpoints: 24
- Item images, User images, Splashscreen, Remote images
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class ImagesAPI(JellyfinAPIBase):
    """Images API endpoints"""
    
    GROUP_NAME = 'images'
    
    # =========================================================================
    # ITEM IMAGES (6 endpoints)
    # =========================================================================
    
    def get_item_images(self, item_id: str) -> Optional[List]:
        """GET /Items/{itemId}/Images - Get item image infos"""
        return self._get(f'/Items/{item_id}/Images')
    
    def get_item_image_url(self, item_id: str, image_type: str = 'Primary',
                           max_width: int = None, max_height: int = None,
                           image_index: int = None) -> str:
        """Get item image URL"""
        url = f"{self.base_url}/Items/{item_id}/Images/{image_type}"
        if image_index is not None:
            url += f"/{image_index}"
        params = [f"api_key={self.api_key}"]
        if max_width:
            params.append(f"maxWidth={max_width}")
        if max_height:
            params.append(f"maxHeight={max_height}")
        return f"{url}?{'&'.join(params)}"
    
    def delete_item_image(self, item_id: str, image_type: str,
                          image_index: int = None) -> bool:
        """DELETE /Items/{itemId}/Images/{imageType} - Delete item image"""
        endpoint = f'/Items/{item_id}/Images/{image_type}'
        if image_index is not None:
            endpoint += f'/{image_index}'
        return self._delete(endpoint) is not None
    
    def set_item_image(self, item_id: str, image_type: str,
                       image_data: bytes, content_type: str = 'image/png') -> bool:
        """POST /Items/{itemId}/Images/{imageType} - Set item image"""
        import requests
        headers = {**self.headers, 'Content-Type': content_type}
        try:
            response = requests.post(
                f"{self.base_url}/Items/{item_id}/Images/{image_type}",
                headers=headers,
                params={'api_key': self.api_key},
                data=image_data,
                timeout=30
            )
            return response.status_code in [200, 204]
        except:
            return False
    
    def update_item_image_index(self, item_id: str, image_type: str,
                                 old_index: int, new_index: int) -> bool:
        """POST /Items/{itemId}/Images/{imageType}/{imageIndex}/Index - Update image index"""
        return self._post(f'/Items/{item_id}/Images/{image_type}/{old_index}/Index',
                         params={'newIndex': new_index}) is not None
    
    # =========================================================================
    # USER IMAGES (3 endpoints)
    # =========================================================================
    
    def get_user_image_url(self, user_id: str = None, image_type: str = 'Primary') -> str:
        """Get user image URL"""
        if user_id:
            return f"{self.base_url}/Users/{user_id}/Images/{image_type}?api_key={self.api_key}"
        return f"{self.base_url}/UserImage?api_key={self.api_key}"
    
    def delete_user_image(self, user_id: str, image_type: str = 'Primary',
                          image_index: int = None) -> bool:
        """DELETE /Users/{userId}/Images/{imageType} - Delete user image"""
        endpoint = f'/Users/{user_id}/Images/{image_type}'
        if image_index is not None:
            endpoint += f'/{image_index}'
        return self._delete(endpoint) is not None
    
    def set_user_image(self, user_id: str, image_type: str,
                       image_data: bytes, content_type: str = 'image/png') -> bool:
        """POST /Users/{userId}/Images/{imageType} - Set user image"""
        import requests
        headers = {**self.headers, 'Content-Type': content_type}
        try:
            response = requests.post(
                f"{self.base_url}/Users/{user_id}/Images/{image_type}",
                headers=headers,
                params={'api_key': self.api_key},
                data=image_data,
                timeout=30
            )
            return response.status_code in [200, 204]
        except:
            return False
    
    # =========================================================================
    # SPLASHSCREEN (3 endpoints)
    # =========================================================================
    
    def get_splashscreen_url(self) -> str:
        """Get splashscreen URL"""
        return f"{self.base_url}/Branding/Splashscreen?api_key={self.api_key}"
    
    def delete_splashscreen(self) -> bool:
        """DELETE /Branding/Splashscreen - Delete custom splashscreen"""
        return self._delete('/Branding/Splashscreen') is not None
    
    def upload_splashscreen(self, image_data: bytes, content_type: str = 'image/png') -> bool:
        """POST /Branding/Splashscreen - Upload custom splashscreen"""
        import requests
        headers = {**self.headers, 'Content-Type': content_type}
        try:
            response = requests.post(
                f"{self.base_url}/Branding/Splashscreen",
                headers=headers,
                params={'api_key': self.api_key},
                data=image_data,
                timeout=30
            )
            return response.status_code in [200, 204]
        except:
            return False
    
    # =========================================================================
    # REMOTE IMAGES (3 endpoints)
    # =========================================================================
    
    def get_remote_images(self, item_id: str, image_type: str = None,
                          start_index: int = None, limit: int = None,
                          provider_name: str = None, include_all_languages: bool = None) -> Optional[Dict]:
        """GET /Items/{itemId}/RemoteImages - Get remote images"""
        params = {k: v for k, v in {
            'type': image_type, 'startIndex': start_index, 'limit': limit,
            'providerName': provider_name, 'includeAllLanguages': include_all_languages
        }.items() if v is not None}
        return self._get(f'/Items/{item_id}/RemoteImages', params)
    
    def get_remote_image_providers(self, item_id: str) -> Optional[List]:
        """GET /Items/{itemId}/RemoteImages/Providers - Get remote image providers"""
        return self._get(f'/Items/{item_id}/RemoteImages/Providers')
    
    def download_remote_image(self, item_id: str, image_type: str, image_url: str) -> bool:
        """POST /Items/{itemId}/RemoteImages/Download - Download remote image"""
        return self._post(f'/Items/{item_id}/RemoteImages/Download',
                         params={'type': image_type, 'imageUrl': image_url}) is not None
    
    # =========================================================================
    # ARTIST/GENRE/STUDIO IMAGES (URL helpers)
    # =========================================================================
    
    def get_artist_image_url(self, artist_id: str, image_type: str = 'Primary',
                              max_width: int = None, max_height: int = None) -> str:
        """Get artist image URL"""
        return self.get_item_image_url(artist_id, image_type, max_width, max_height)
    
    def get_genre_image_url(self, genre_name: str, image_type: str = 'Primary') -> str:
        """Get genre image URL"""
        return f"{self.base_url}/Genres/{genre_name}/Images/{image_type}?api_key={self.api_key}"
    
    def get_studio_image_url(self, studio_name: str, image_type: str = 'Primary') -> str:
        """Get studio image URL"""
        return f"{self.base_url}/Studios/{studio_name}/Images/{image_type}?api_key={self.api_key}"
    
    def get_person_image_url(self, person_name: str, image_type: str = 'Primary') -> str:
        """Get person image URL"""
        return f"{self.base_url}/Persons/{person_name}/Images/{image_type}?api_key={self.api_key}"
    
    def get_music_genre_image_url(self, genre_name: str, image_type: str = 'Primary') -> str:
        """Get music genre image URL"""
        return f"{self.base_url}/MusicGenres/{genre_name}/Images/{image_type}?api_key={self.api_key}"
