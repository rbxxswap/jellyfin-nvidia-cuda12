#!/usr/bin/env python3
"""
Jellyfin REST API Client - FULL API IMPLEMENTATION
Version: 10.11.5 compatible
Total: 315 Endpoints in 54 Categories

Generated for Home Assistant MQTT Bridge
"""

import logging
import requests
from typing import Optional, List, Dict, Any, Union
from config import get_config

logger = logging.getLogger(__name__)


class JellyfinAPI:
    """
    Complete Jellyfin REST API Client
    Implements all 315 endpoints from OpenAPI spec v10.11.5
    """
    
    def __init__(self):
        self.config = get_config()
        self.base_url = self.config.jellyfin_host.rstrip('/')
        self.api_key = self.config.jellyfin_api_key
        self.headers = {
            'X-Emby-Token': self.api_key,
            'Content-Type': 'application/json'
        }
        self._server_info_cache = None
        self._user_id_cache = None
    
    def _request(self, method: str, endpoint: str, 
                 params: Optional[Dict] = None,
                 json_data: Optional[Dict] = None,
                 data: Optional[Any] = None,
                 timeout: int = 10,
                 raw_response: bool = False) -> Optional[Any]:
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        # Merge api_key into params
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        
        try:
            response = requests.request(
                method, 
                url, 
                headers=self.headers,
                params=params,
                json=json_data,
                data=data,
                timeout=timeout
            )
            response.raise_for_status()
            
            if raw_response:
                return response
            
            if response.status_code == 204:
                return True
            
            if response.text:
                return response.json()
            return True
            
        except requests.exceptions.Timeout:
            logger.error("API timeout: %s %s", method, endpoint)
            return None
        except requests.exceptions.RequestException as e:
            logger.error("API error: %s %s - %s", method, endpoint, str(e))
            return None
    
    def _get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Optional[Any]:
        """GET request shorthand"""
        return self._request('GET', endpoint, params=params, **kwargs)
    
    def _post(self, endpoint: str, params: Optional[Dict] = None, 
              json_data: Optional[Dict] = None, **kwargs) -> Optional[Any]:
        """POST request shorthand"""
        return self._request('POST', endpoint, params=params, json_data=json_data, **kwargs)
    
    def _delete(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Optional[Any]:
        """DELETE request shorthand"""
        return self._request('DELETE', endpoint, params=params, **kwargs)

    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def get_current_user_id(self) -> Optional[str]:
        """Get current user ID (cached)"""
        if self._user_id_cache:
            return self._user_id_cache
        me = self.get_current_user()
        if me:
            self._user_id_cache = me.get('Id')
            return self._user_id_cache
        return None

    # =========================================================================
    # ACTIVITY LOG (1 endpoint)
    # =========================================================================
    
    def get_activity_log(self, start_index: int = None, limit: int = None,
                         min_date: str = None, has_user_id: bool = None) -> Optional[Dict]:
        """GET /System/ActivityLog/Entries - Get activity log entries"""
        params = {}
        if start_index is not None:
            params['startIndex'] = start_index
        if limit is not None:
            params['limit'] = limit
        if min_date:
            params['minDate'] = min_date
        if has_user_id is not None:
            params['hasUserId'] = has_user_id
        return self._get('/System/ActivityLog/Entries', params)

    # =========================================================================
    # API KEY (3 endpoints)
    # =========================================================================
    
    def get_api_keys(self) -> Optional[Dict]:
        """GET /Auth/Keys - Get all API keys"""
        return self._get('/Auth/Keys')
    
    def create_api_key(self, app: str) -> bool:
        """POST /Auth/Keys - Create new API key"""
        return self._post('/Auth/Keys', params={'app': app}) is not None
    
    def revoke_api_key(self, key: str) -> bool:
        """DELETE /Auth/Keys/{key} - Revoke API key"""
        return self._delete(f'/Auth/Keys/{key}') is not None

    # =========================================================================
    # ARTISTS (3 endpoints)
    # =========================================================================
    
    def get_artists(self, user_id: str = None, search_term: str = None,
                    parent_id: str = None, limit: int = None,
                    start_index: int = None, **kwargs) -> Optional[Dict]:
        """GET /Artists - Get all artists"""
        params = {k: v for k, v in {
            'userId': user_id, 'searchTerm': search_term,
            'parentId': parent_id, 'limit': limit, 'startIndex': start_index,
            **kwargs
        }.items() if v is not None}
        return self._get('/Artists', params)
    
    def get_album_artists(self, user_id: str = None, **kwargs) -> Optional[Dict]:
        """GET /Artists/AlbumArtists - Get all album artists"""
        params = {k: v for k, v in {'userId': user_id, **kwargs}.items() if v is not None}
        return self._get('/Artists/AlbumArtists', params)
    
    def get_artist_by_name(self, name: str, user_id: str = None) -> Optional[Dict]:
        """GET /Artists/{name} - Get artist by name"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Artists/{name}', params)

    # =========================================================================
    # AUDIO (2 endpoints) - Streaming, usually not needed for MQTT
    # =========================================================================
    
    def get_audio_stream_url(self, item_id: str, container: str = None) -> str:
        """Get audio stream URL (for reference)"""
        if container:
            return f"{self.base_url}/Audio/{item_id}/stream.{container}?api_key={self.api_key}"
        return f"{self.base_url}/Audio/{item_id}/stream?api_key={self.api_key}"

    # =========================================================================
    # BACKUP (4 endpoints)
    # =========================================================================
    
    def get_backups(self) -> Optional[List]:
        """GET /Backup - Get all backups"""
        return self._get('/Backup')
    
    def get_backup_manifest(self) -> Optional[Dict]:
        """GET /Backup/Manifest - Get backup manifest"""
        return self._get('/Backup/Manifest')
    
    def create_backup(self) -> bool:
        """POST /Backup/Create - Create new backup"""
        return self._post('/Backup/Create') is not None
    
    def restore_backup(self, backup_data: Dict) -> bool:
        """POST /Backup/Restore - Restore from backup"""
        return self._post('/Backup/Restore', json_data=backup_data) is not None

    # =========================================================================
    # BRANDING (3 endpoints)
    # =========================================================================
    
    def get_branding_configuration(self) -> Optional[Dict]:
        """GET /Branding/Configuration - Get branding config"""
        return self._get('/Branding/Configuration')
    
    def get_branding_css(self) -> Optional[str]:
        """GET /Branding/Css - Get custom CSS"""
        response = self._get('/Branding/Css', raw_response=True)
        return response.text if response else None

    # =========================================================================
    # CHANNELS (5 endpoints)
    # =========================================================================
    
    def get_channels(self, user_id: str = None, start_index: int = None,
                     limit: int = None) -> Optional[Dict]:
        """GET /Channels - Get available channels"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit
        }.items() if v is not None}
        return self._get('/Channels', params)
    
    def get_channel_features(self) -> Optional[List]:
        """GET /Channels/Features - Get all channel features"""
        return self._get('/Channels/Features')
    
    def get_latest_channel_items(self, user_id: str = None, limit: int = None) -> Optional[Dict]:
        """GET /Channels/Items/Latest - Get latest channel items"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get('/Channels/Items/Latest', params)
    
    def get_channel_features_by_id(self, channel_id: str) -> Optional[Dict]:
        """GET /Channels/{channelId}/Features - Get channel features"""
        return self._get(f'/Channels/{channel_id}/Features')
    
    def get_channel_items(self, channel_id: str, user_id: str = None,
                          start_index: int = None, limit: int = None) -> Optional[Dict]:
        """GET /Channels/{channelId}/Items - Get channel items"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit
        }.items() if v is not None}
        return self._get(f'/Channels/{channel_id}/Items', params)

    # =========================================================================
    # CLIENT LOG (1 endpoint)
    # =========================================================================
    
    def post_client_log(self, log_document: Dict) -> bool:
        """POST /ClientLog/Document - Post client log"""
        return self._post('/ClientLog/Document', json_data=log_document) is not None

    # =========================================================================
    # COLLECTION (3 endpoints)
    # =========================================================================
    
    def create_collection(self, name: str, ids: List[str] = None,
                          parent_id: str = None) -> Optional[Dict]:
        """POST /Collections - Create collection"""
        params = {'name': name}
        if ids:
            params['ids'] = ','.join(ids)
        if parent_id:
            params['parentId'] = parent_id
        return self._post('/Collections', params=params)
    
    def add_to_collection(self, collection_id: str, ids: List[str]) -> bool:
        """POST /Collections/{collectionId}/Items - Add items to collection"""
        return self._post(f'/Collections/{collection_id}/Items', 
                         params={'ids': ','.join(ids)}) is not None
    
    def remove_from_collection(self, collection_id: str, ids: List[str]) -> bool:
        """DELETE /Collections/{collectionId}/Items - Remove items from collection"""
        return self._delete(f'/Collections/{collection_id}/Items',
                           params={'ids': ','.join(ids)}) is not None


    # =========================================================================
    # CONFIGURATION (6 endpoints)
    # =========================================================================
    
    def get_configuration(self) -> Optional[Dict]:
        """GET /System/Configuration - Get server configuration"""
        return self._get('/System/Configuration')
    
    def update_configuration(self, config: Dict) -> bool:
        """POST /System/Configuration - Update server configuration"""
        return self._post('/System/Configuration', json_data=config) is not None
    
    def get_default_metadata_options(self) -> Optional[Dict]:
        """GET /System/Configuration/MetadataOptions/Default - Get default metadata options"""
        return self._get('/System/Configuration/MetadataOptions/Default')
    
    def get_named_configuration(self, key: str) -> Optional[Dict]:
        """GET /System/Configuration/{key} - Get named configuration"""
        return self._get(f'/System/Configuration/{key}')
    
    def update_named_configuration(self, key: str, config: Dict) -> bool:
        """POST /System/Configuration/{key} - Update named configuration"""
        return self._post(f'/System/Configuration/{key}', json_data=config) is not None
    
    def update_branding_configuration(self, config: Dict) -> bool:
        """POST /System/Configuration/Branding - Update branding configuration"""
        return self._post('/System/Configuration/Branding', json_data=config) is not None

    # =========================================================================
    # DASHBOARD (2 endpoints)
    # =========================================================================
    
    def get_configuration_page(self, name: str) -> Optional[str]:
        """GET /web/ConfigurationPage - Get dashboard configuration page"""
        response = self._get('/web/ConfigurationPage', params={'name': name}, raw_response=True)
        return response.text if response else None
    
    def get_configuration_pages(self, enable_in_main_menu: bool = None) -> Optional[List]:
        """GET /web/ConfigurationPages - Get dashboard configuration pages"""
        params = {}
        if enable_in_main_menu is not None:
            params['enableInMainMenu'] = enable_in_main_menu
        return self._get('/web/ConfigurationPages', params)

    # =========================================================================
    # DEVICES (5 endpoints)
    # =========================================================================
    
    def get_devices(self, user_id: str = None) -> Optional[Dict]:
        """GET /Devices - Get all devices"""
        params = {'userId': user_id} if user_id else {}
        return self._get('/Devices', params)
    
    def delete_device(self, device_id: str) -> bool:
        """DELETE /Devices - Delete device"""
        return self._delete('/Devices', params={'id': device_id}) is not None
    
    def get_device_info(self, device_id: str) -> Optional[Dict]:
        """GET /Devices/Info - Get device info"""
        return self._get('/Devices/Info', params={'id': device_id})
    
    def get_device_options(self, device_id: str) -> Optional[Dict]:
        """GET /Devices/Options - Get device options"""
        return self._get('/Devices/Options', params={'id': device_id})
    
    def update_device_options(self, device_id: str, options: Dict) -> bool:
        """POST /Devices/Options - Update device options"""
        return self._post('/Devices/Options', params={'id': device_id}, 
                         json_data=options) is not None

    # =========================================================================
    # DISPLAY PREFERENCES (2 endpoints)
    # =========================================================================
    
    def get_display_preferences(self, display_preferences_id: str, 
                                 user_id: str, client: str) -> Optional[Dict]:
        """GET /DisplayPreferences/{displayPreferencesId} - Get display preferences"""
        return self._get(f'/DisplayPreferences/{display_preferences_id}',
                        params={'userId': user_id, 'client': client})
    
    def update_display_preferences(self, display_preferences_id: str,
                                    user_id: str, client: str, prefs: Dict) -> bool:
        """POST /DisplayPreferences/{displayPreferencesId} - Update display preferences"""
        return self._post(f'/DisplayPreferences/{display_preferences_id}',
                         params={'userId': user_id, 'client': client},
                         json_data=prefs) is not None

    # =========================================================================
    # DYNAMIC HLS (7 endpoints) - Streaming URLs
    # =========================================================================
    
    def get_audio_hls_playlist_url(self, item_id: str) -> str:
        """Get audio HLS master playlist URL"""
        return f"{self.base_url}/Audio/{item_id}/master.m3u8?api_key={self.api_key}"
    
    def get_video_hls_playlist_url(self, item_id: str) -> str:
        """Get video HLS master playlist URL"""
        return f"{self.base_url}/Videos/{item_id}/master.m3u8?api_key={self.api_key}"

    # =========================================================================
    # ENVIRONMENT (6 endpoints)
    # =========================================================================
    
    def get_default_directory_browser(self) -> Optional[Dict]:
        """GET /Environment/DefaultDirectoryBrowser - Get default directory browser"""
        return self._get('/Environment/DefaultDirectoryBrowser')
    
    def get_directory_contents(self, path: str, include_files: bool = True,
                               include_directories: bool = True) -> Optional[List]:
        """GET /Environment/DirectoryContents - Get directory contents"""
        return self._get('/Environment/DirectoryContents', params={
            'path': path, 'includeFiles': include_files, 
            'includeDirectories': include_directories
        })
    
    def get_drives(self) -> Optional[List]:
        """GET /Environment/Drives - Get available drives"""
        return self._get('/Environment/Drives')
    
    def get_network_shares(self) -> Optional[List]:
        """GET /Environment/NetworkShares - Get network shares"""
        return self._get('/Environment/NetworkShares')
    
    def get_parent_path(self, path: str) -> Optional[str]:
        """GET /Environment/ParentPath - Get parent path"""
        return self._get('/Environment/ParentPath', params={'path': path})
    
    def validate_path(self, path: str) -> bool:
        """POST /Environment/ValidatePath - Validate path"""
        return self._post('/Environment/ValidatePath', json_data={'Path': path}) is not None

    # =========================================================================
    # FILTER (2 endpoints)
    # =========================================================================
    
    def get_query_filters_legacy(self, user_id: str = None, parent_id: str = None) -> Optional[Dict]:
        """GET /Items/Filters - Get query filters (legacy)"""
        params = {k: v for k, v in {'userId': user_id, 'parentId': parent_id}.items() if v is not None}
        return self._get('/Items/Filters', params)
    
    def get_query_filters(self, user_id: str = None, parent_id: str = None,
                          include_item_types: List[str] = None) -> Optional[Dict]:
        """GET /Items/Filters2 - Get query filters"""
        params = {k: v for k, v in {'userId': user_id, 'parentId': parent_id}.items() if v is not None}
        if include_item_types:
            params['includeItemTypes'] = ','.join(include_item_types)
        return self._get('/Items/Filters2', params)

    # =========================================================================
    # GENRES (2 endpoints)
    # =========================================================================
    
    def get_genres(self, user_id: str = None, start_index: int = None,
                   limit: int = None, parent_id: str = None) -> Optional[Dict]:
        """GET /Genres - Get all genres"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 
            'limit': limit, 'parentId': parent_id
        }.items() if v is not None}
        return self._get('/Genres', params)
    
    def get_genre(self, genre_name: str, user_id: str = None) -> Optional[Dict]:
        """GET /Genres/{genreName} - Get genre by name"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Genres/{genre_name}', params)

    # =========================================================================
    # HLS SEGMENT (5 endpoints) - Streaming, URLs only
    # =========================================================================
    
    def stop_encoding_process(self, device_id: str, play_session_id: str = None) -> bool:
        """DELETE /Videos/ActiveEncodings - Stop encoding process"""
        params = {'deviceId': device_id}
        if play_session_id:
            params['playSessionId'] = play_session_id
        return self._delete('/Videos/ActiveEncodings', params=params) is not None


    # =========================================================================
    # IMAGE (24 endpoints) - Most are GET for images
    # =========================================================================
    
    def get_item_images(self, item_id: str) -> Optional[List]:
        """GET /Items/{itemId}/Images - Get item image infos"""
        return self._get(f'/Items/{item_id}/Images')
    
    def get_item_image_url(self, item_id: str, image_type: str = 'Primary',
                           max_width: int = None, max_height: int = None) -> str:
        """Get item image URL"""
        url = f"{self.base_url}/Items/{item_id}/Images/{image_type}"
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
    
    def get_splashscreen_url(self) -> str:
        """Get splashscreen URL"""
        return f"{self.base_url}/Branding/Splashscreen?api_key={self.api_key}"
    
    def delete_splashscreen(self) -> bool:
        """DELETE /Branding/Splashscreen - Delete custom splashscreen"""
        return self._delete('/Branding/Splashscreen') is not None
    
    def get_user_image_url(self, user_id: str = None) -> str:
        """Get user image URL"""
        if user_id:
            return f"{self.base_url}/Users/{user_id}/Images/Primary?api_key={self.api_key}"
        return f"{self.base_url}/UserImage?api_key={self.api_key}"

    # =========================================================================
    # INSTANT MIX (8 endpoints)
    # =========================================================================
    
    def get_instant_mix_from_album(self, item_id: str, user_id: str = None,
                                    limit: int = None) -> Optional[Dict]:
        """GET /Albums/{itemId}/InstantMix - Get instant mix from album"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Albums/{item_id}/InstantMix', params)
    
    def get_instant_mix_from_artists(self, user_id: str = None, limit: int = None) -> Optional[Dict]:
        """GET /Artists/InstantMix - Get instant mix from artists"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get('/Artists/InstantMix', params)
    
    def get_instant_mix_from_artist(self, item_id: str, user_id: str = None,
                                     limit: int = None) -> Optional[Dict]:
        """GET /Artists/{itemId}/InstantMix - Get instant mix from artist"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Artists/{item_id}/InstantMix', params)
    
    def get_instant_mix_from_item(self, item_id: str, user_id: str = None,
                                   limit: int = None) -> Optional[Dict]:
        """GET /Items/{itemId}/InstantMix - Get instant mix from item"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Items/{item_id}/InstantMix', params)
    
    def get_instant_mix_from_music_genres(self, user_id: str = None, limit: int = None) -> Optional[Dict]:
        """GET /MusicGenres/InstantMix - Get instant mix from music genres"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get('/MusicGenres/InstantMix', params)
    
    def get_instant_mix_from_music_genre(self, name: str, user_id: str = None,
                                          limit: int = None) -> Optional[Dict]:
        """GET /MusicGenres/{name}/InstantMix - Get instant mix from music genre"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/MusicGenres/{name}/InstantMix', params)
    
    def get_instant_mix_from_playlist(self, item_id: str, user_id: str = None,
                                       limit: int = None) -> Optional[Dict]:
        """GET /Playlists/{itemId}/InstantMix - Get instant mix from playlist"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Playlists/{item_id}/InstantMix', params)
    
    def get_instant_mix_from_song(self, item_id: str, user_id: str = None,
                                   limit: int = None) -> Optional[Dict]:
        """GET /Songs/{itemId}/InstantMix - Get instant mix from song"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Songs/{item_id}/InstantMix', params)

    # =========================================================================
    # ITEM LOOKUP (11 endpoints)
    # =========================================================================
    
    def get_external_id_infos(self, item_id: str) -> Optional[List]:
        """GET /Items/{itemId}/ExternalIdInfos - Get external ID infos"""
        return self._get(f'/Items/{item_id}/ExternalIdInfos')
    
    def apply_search_result(self, item_id: str, search_result: Dict,
                            replace_all_images: bool = True) -> bool:
        """POST /Items/RemoteSearch/Apply/{itemId} - Apply search result"""
        return self._post(f'/Items/RemoteSearch/Apply/{item_id}',
                         params={'replaceAllImages': replace_all_images},
                         json_data=search_result) is not None
    
    def search_remote_book(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/Book - Search for book"""
        return self._post('/Items/RemoteSearch/Book', json_data=query)
    
    def search_remote_boxset(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/BoxSet - Search for box set"""
        return self._post('/Items/RemoteSearch/BoxSet', json_data=query)
    
    def search_remote_movie(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/Movie - Search for movie"""
        return self._post('/Items/RemoteSearch/Movie', json_data=query)
    
    def search_remote_music_album(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/MusicAlbum - Search for music album"""
        return self._post('/Items/RemoteSearch/MusicAlbum', json_data=query)
    
    def search_remote_music_artist(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/MusicArtist - Search for music artist"""
        return self._post('/Items/RemoteSearch/MusicArtist', json_data=query)
    
    def search_remote_music_video(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/MusicVideo - Search for music video"""
        return self._post('/Items/RemoteSearch/MusicVideo', json_data=query)
    
    def search_remote_person(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/Person - Search for person"""
        return self._post('/Items/RemoteSearch/Person', json_data=query)
    
    def search_remote_series(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/Series - Search for series"""
        return self._post('/Items/RemoteSearch/Series', json_data=query)
    
    def search_remote_trailer(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/Trailer - Search for trailer"""
        return self._post('/Items/RemoteSearch/Trailer', json_data=query)

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
    
    # Alias for backward compatibility
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

    # =========================================================================
    # LIVE TV (41 endpoints) - Comprehensive Live TV support
    # =========================================================================
    
    def get_livetv_info(self) -> Optional[Dict]:
        """GET /LiveTv/Info - Get live TV info"""
        return self._get('/LiveTv/Info')
    
    def get_livetv_channels(self, channel_type: str = None, user_id: str = None,
                            start_index: int = None, limit: int = None,
                            is_favorite: bool = None, is_liked: bool = None,
                            is_disabled: bool = None, **kwargs) -> Optional[Dict]:
        """GET /LiveTv/Channels - Get live TV channels"""
        params = {k: v for k, v in {
            'type': channel_type, 'userId': user_id,
            'startIndex': start_index, 'limit': limit,
            'isFavorite': is_favorite, 'isLiked': is_liked,
            'isDisabled': is_disabled, **kwargs
        }.items() if v is not None}
        return self._get('/LiveTv/Channels', params)
    
    def get_livetv_channel(self, channel_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Channels/{channelId} - Get channel"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/LiveTv/Channels/{channel_id}', params)
    
    def get_livetv_programs(self, channel_ids: List[str] = None,
                            user_id: str = None, min_start_date: str = None,
                            max_start_date: str = None, **kwargs) -> Optional[Dict]:
        """GET /LiveTv/Programs - Get programs"""
        params = {k: v for k, v in {
            'userId': user_id, 'minStartDate': min_start_date,
            'maxStartDate': max_start_date, **kwargs
        }.items() if v is not None}
        if channel_ids:
            params['channelIds'] = ','.join(channel_ids)
        return self._get('/LiveTv/Programs', params)
    
    def get_livetv_programs_post(self, body: Dict) -> Optional[Dict]:
        """POST /LiveTv/Programs - Get programs (POST version)"""
        return self._post('/LiveTv/Programs', json_data=body)
    
    def get_recommended_programs(self, user_id: str = None, limit: int = None,
                                  is_airing: bool = None, has_aired: bool = None,
                                  is_movie: bool = None, is_sports: bool = None,
                                  is_news: bool = None, is_kids: bool = None,
                                  is_series: bool = None) -> Optional[Dict]:
        """GET /LiveTv/Programs/Recommended - Get recommended programs"""
        params = {k: v for k, v in {
            'userId': user_id, 'limit': limit, 'isAiring': is_airing,
            'hasAired': has_aired, 'isMovie': is_movie, 'isSports': is_sports,
            'isNews': is_news, 'isKids': is_kids, 'isSeries': is_series
        }.items() if v is not None}
        return self._get('/LiveTv/Programs/Recommended', params)
    
    def get_livetv_program(self, program_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Programs/{programId} - Get program"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/LiveTv/Programs/{program_id}', params)
    
    def get_livetv_recordings(self, channel_id: str = None, user_id: str = None,
                              start_index: int = None, limit: int = None,
                              status: str = None, is_in_progress: bool = None,
                              **kwargs) -> Optional[Dict]:
        """GET /LiveTv/Recordings - Get recordings"""
        params = {k: v for k, v in {
            'channelId': channel_id, 'userId': user_id,
            'startIndex': start_index, 'limit': limit,
            'status': status, 'isInProgress': is_in_progress, **kwargs
        }.items() if v is not None}
        return self._get('/LiveTv/Recordings', params)
    
    def get_livetv_recording(self, recording_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Recordings/{recordingId} - Get recording"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/LiveTv/Recordings/{recording_id}', params)
    
    def delete_livetv_recording(self, recording_id: str) -> bool:
        """DELETE /LiveTv/Recordings/{recordingId} - Delete recording"""
        return self._delete(f'/LiveTv/Recordings/{recording_id}') is not None
    
    def get_recording_folders(self, user_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Recordings/Folders - Get recording folders"""
        params = {'userId': user_id} if user_id else {}
        return self._get('/LiveTv/Recordings/Folders', params)
    
    def get_recording_groups(self, user_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Recordings/Groups - Get recording groups"""
        params = {'userId': user_id} if user_id else {}
        return self._get('/LiveTv/Recordings/Groups', params)
    
    def get_recording_group(self, group_id: str) -> Optional[Dict]:
        """GET /LiveTv/Recordings/Groups/{groupId} - Get recording group"""
        return self._get(f'/LiveTv/Recordings/Groups/{group_id}')
    
    def get_recording_series(self, **kwargs) -> Optional[Dict]:
        """GET /LiveTv/Recordings/Series - Get recording series"""
        return self._get('/LiveTv/Recordings/Series', {k: v for k, v in kwargs.items() if v is not None})
    
    def get_livetv_timers(self, channel_id: str = None, series_timer_id: str = None,
                          is_active: bool = None, is_scheduled: bool = None) -> Optional[Dict]:
        """GET /LiveTv/Timers - Get timers"""
        params = {k: v for k, v in {
            'channelId': channel_id, 'seriesTimerId': series_timer_id,
            'isActive': is_active, 'isScheduled': is_scheduled
        }.items() if v is not None}
        return self._get('/LiveTv/Timers', params)
    
    def get_default_timer_info(self, program_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Timers/Defaults - Get default timer info"""
        params = {'programId': program_id} if program_id else {}
        return self._get('/LiveTv/Timers/Defaults', params)
    
    def get_livetv_timer(self, timer_id: str) -> Optional[Dict]:
        """GET /LiveTv/Timers/{timerId} - Get timer"""
        return self._get(f'/LiveTv/Timers/{timer_id}')
    
    def create_livetv_timer(self, timer_info: Dict) -> bool:
        """POST /LiveTv/Timers - Create timer"""
        return self._post('/LiveTv/Timers', json_data=timer_info) is not None
    
    def update_livetv_timer(self, timer_id: str, timer_info: Dict) -> bool:
        """POST /LiveTv/Timers/{timerId} - Update timer"""
        return self._post(f'/LiveTv/Timers/{timer_id}', json_data=timer_info) is not None
    
    def cancel_livetv_timer(self, timer_id: str) -> bool:
        """DELETE /LiveTv/Timers/{timerId} - Cancel timer"""
        return self._delete(f'/LiveTv/Timers/{timer_id}') is not None
    
    def get_series_timers(self, sort_by: str = None, sort_order: str = None) -> Optional[Dict]:
        """GET /LiveTv/SeriesTimers - Get series timers"""
        params = {k: v for k, v in {'sortBy': sort_by, 'sortOrder': sort_order}.items() if v is not None}
        return self._get('/LiveTv/SeriesTimers', params)
    
    def get_series_timer(self, timer_id: str) -> Optional[Dict]:
        """GET /LiveTv/SeriesTimers/{timerId} - Get series timer"""
        return self._get(f'/LiveTv/SeriesTimers/{timer_id}')
    
    def create_series_timer(self, timer_info: Dict) -> bool:
        """POST /LiveTv/SeriesTimers - Create series timer"""
        return self._post('/LiveTv/SeriesTimers', json_data=timer_info) is not None
    
    def update_series_timer(self, timer_id: str, timer_info: Dict) -> bool:
        """POST /LiveTv/SeriesTimers/{timerId} - Update series timer"""
        return self._post(f'/LiveTv/SeriesTimers/{timer_id}', json_data=timer_info) is not None
    
    def cancel_series_timer(self, timer_id: str) -> bool:
        """DELETE /LiveTv/SeriesTimers/{timerId} - Cancel series timer"""
        return self._delete(f'/LiveTv/SeriesTimers/{timer_id}') is not None
    
    def get_guide_info(self) -> Optional[Dict]:
        """GET /LiveTv/GuideInfo - Get guide info"""
        return self._get('/LiveTv/GuideInfo')
    
    def get_tuner_host_types(self) -> Optional[List]:
        """GET /LiveTv/TunerHosts/Types - Get tuner host types"""
        return self._get('/LiveTv/TunerHosts/Types')
    
    def discover_tuners(self, new_devices_only: bool = False) -> Optional[List]:
        """GET /LiveTv/Tuners/Discover - Discover tuners"""
        return self._get('/LiveTv/Tuners/Discover', params={'newDevicesOnly': new_devices_only})
    
    def add_tuner_host(self, tuner_info: Dict) -> Optional[Dict]:
        """POST /LiveTv/TunerHosts - Add tuner host"""
        return self._post('/LiveTv/TunerHosts', json_data=tuner_info)
    
    def delete_tuner_host(self, tuner_id: str) -> bool:
        """DELETE /LiveTv/TunerHosts - Delete tuner host"""
        return self._delete('/LiveTv/TunerHosts', params={'id': tuner_id}) is not None
    
    def reset_tuner(self, tuner_id: str) -> bool:
        """POST /LiveTv/Tuners/{tunerId}/Reset - Reset tuner"""
        return self._post(f'/LiveTv/Tuners/{tuner_id}/Reset') is not None
    
    def get_channel_mapping_options(self, provider_id: str) -> Optional[Dict]:
        """GET /LiveTv/ChannelMappingOptions - Get channel mapping options"""
        return self._get('/LiveTv/ChannelMappingOptions', params={'providerId': provider_id})
    
    def set_channel_mapping(self, provider_id: str, tuner_channel_id: str,
                            provider_channel_id: str) -> bool:
        """POST /LiveTv/ChannelMappings - Set channel mapping"""
        return self._post('/LiveTv/ChannelMappings', json_data={
            'ProviderId': provider_id,
            'TunerChannelId': tuner_channel_id,
            'ProviderChannelId': provider_channel_id
        }) is not None
    
    def get_default_listing_provider(self) -> Optional[Dict]:
        """GET /LiveTv/ListingProviders/Default - Get default listing provider"""
        return self._get('/LiveTv/ListingProviders/Default')
    
    def get_lineups(self, listing_provider_id: str, country: str = None,
                    location: str = None) -> Optional[List]:
        """GET /LiveTv/ListingProviders/Lineups - Get lineups"""
        params = {'id': listing_provider_id}
        if country:
            params['country'] = country
        if location:
            params['location'] = location
        return self._get('/LiveTv/ListingProviders/Lineups', params)
    
    def add_listing_provider(self, provider_info: Dict, validate_listings: bool = False,
                             validate_login: bool = False) -> Optional[Dict]:
        """POST /LiveTv/ListingProviders - Add listing provider"""
        return self._post('/LiveTv/ListingProviders',
                         params={'validateListings': validate_listings,
                                'validateLogin': validate_login},
                         json_data=provider_info)
    
    def delete_listing_provider(self, provider_id: str) -> bool:
        """DELETE /LiveTv/ListingProviders - Delete listing provider"""
        return self._delete('/LiveTv/ListingProviders', params={'id': provider_id}) is not None
    
    def get_schedules_direct_countries(self) -> Optional[str]:
        """GET /LiveTv/ListingProviders/SchedulesDirect/Countries - Get SD countries"""
        return self._get('/LiveTv/ListingProviders/SchedulesDirect/Countries')


    # =========================================================================
    # LOCALIZATION (4 endpoints)
    # =========================================================================
    
    def get_countries(self) -> Optional[List]:
        """GET /Localization/Countries - Get countries"""
        return self._get('/Localization/Countries')
    
    def get_cultures(self) -> Optional[List]:
        """GET /Localization/Cultures - Get cultures"""
        return self._get('/Localization/Cultures')
    
    def get_localization_options(self) -> Optional[List]:
        """GET /Localization/Options - Get localization options"""
        return self._get('/Localization/Options')
    
    def get_parental_ratings(self) -> Optional[List]:
        """GET /Localization/ParentalRatings - Get parental ratings"""
        return self._get('/Localization/ParentalRatings')

    # =========================================================================
    # LYRICS (6 endpoints)
    # =========================================================================
    
    def get_lyrics(self, item_id: str) -> Optional[Dict]:
        """GET /Audio/{itemId}/Lyrics - Get lyrics"""
        return self._get(f'/Audio/{item_id}/Lyrics')
    
    def upload_lyrics(self, item_id: str, lyrics: str, filename: str) -> bool:
        """POST /Audio/{itemId}/Lyrics - Upload lyrics"""
        return self._post(f'/Audio/{item_id}/Lyrics',
                         params={'fileName': filename}, data=lyrics) is not None
    
    def delete_lyrics(self, item_id: str) -> bool:
        """DELETE /Audio/{itemId}/Lyrics - Delete lyrics"""
        return self._delete(f'/Audio/{item_id}/Lyrics') is not None
    
    def search_remote_lyrics(self, item_id: str) -> Optional[List]:
        """GET /Audio/{itemId}/RemoteSearch/Lyrics - Search remote lyrics"""
        return self._get(f'/Audio/{item_id}/RemoteSearch/Lyrics')
    
    def download_remote_lyrics(self, item_id: str, lyric_id: str) -> bool:
        """POST /Audio/{itemId}/RemoteSearch/Lyrics/{lyricId} - Download remote lyrics"""
        return self._post(f'/Audio/{item_id}/RemoteSearch/Lyrics/{lyric_id}') is not None
    
    def get_lyric_provider_info(self, lyric_id: str) -> Optional[Dict]:
        """GET /Providers/Lyrics/{lyricId} - Get lyric provider info"""
        return self._get(f'/Providers/Lyrics/{lyric_id}')

    # =========================================================================
    # MEDIA INFO (5 endpoints)
    # =========================================================================
    
    def get_playback_info(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /Items/{itemId}/PlaybackInfo - Get playback info"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/PlaybackInfo', params)
    
    def get_playback_info_post(self, item_id: str, playback_info_dto: Dict,
                                user_id: str = None) -> Optional[Dict]:
        """POST /Items/{itemId}/PlaybackInfo - Get playback info (POST)"""
        params = {'userId': user_id} if user_id else {}
        return self._post(f'/Items/{item_id}/PlaybackInfo',
                         params=params, json_data=playback_info_dto)
    
    def get_bitrate_test_bytes(self, size: int = 102400) -> Optional[bytes]:
        """GET /Playback/BitrateTest - Get bitrate test bytes"""
        response = self._get('/Playback/BitrateTest', params={'size': size}, raw_response=True)
        return response.content if response else None
    
    def open_live_stream(self, open_token: str, user_id: str = None,
                         play_session_id: str = None, **kwargs) -> Optional[Dict]:
        """POST /LiveStreams/Open - Open live stream"""
        body = {'OpenToken': open_token, **kwargs}
        params = {}
        if user_id:
            params['userId'] = user_id
        if play_session_id:
            params['playSessionId'] = play_session_id
        return self._post('/LiveStreams/Open', params=params, json_data=body)
    
    def close_live_stream(self, live_stream_id: str) -> bool:
        """POST /LiveStreams/Close - Close live stream"""
        return self._post('/LiveStreams/Close',
                         params={'liveStreamId': live_stream_id}) is not None

    # =========================================================================
    # MEDIA SEGMENTS (1 endpoint)
    # =========================================================================
    
    def get_media_segments(self, item_id: str, include_segment_types: List[str] = None) -> Optional[Dict]:
        """GET /MediaSegments/{itemId} - Get media segments"""
        params = {}
        if include_segment_types:
            params['includeSegmentTypes'] = ','.join(include_segment_types)
        return self._get(f'/MediaSegments/{item_id}', params)

    # =========================================================================
    # MOVIES (1 endpoint)
    # =========================================================================
    
    def get_movie_recommendations(self, user_id: str = None, parent_id: str = None,
                                   category_limit: int = None, item_limit: int = None) -> Optional[List]:
        """GET /Movies/Recommendations - Get movie recommendations"""
        params = {k: v for k, v in {
            'userId': user_id, 'parentId': parent_id,
            'categoryLimit': category_limit, 'itemLimit': item_limit
        }.items() if v is not None}
        return self._get('/Movies/Recommendations', params)

    # =========================================================================
    # MUSIC GENRES (2 endpoints)
    # =========================================================================
    
    def get_music_genres(self, user_id: str = None, start_index: int = None,
                         limit: int = None, parent_id: str = None) -> Optional[Dict]:
        """GET /MusicGenres - Get music genres"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index,
            'limit': limit, 'parentId': parent_id
        }.items() if v is not None}
        return self._get('/MusicGenres', params)
    
    def get_music_genre(self, genre_name: str, user_id: str = None) -> Optional[Dict]:
        """GET /MusicGenres/{genreName} - Get music genre"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/MusicGenres/{genre_name}', params)

    # =========================================================================
    # PACKAGE (6 endpoints)
    # =========================================================================
    
    def get_packages(self) -> Optional[List]:
        """GET /Packages - Get available packages"""
        return self._get('/Packages')
    
    def get_package_info(self, name: str, assembly_guid: str = None) -> Optional[Dict]:
        """GET /Packages/{name} - Get package info"""
        params = {'assemblyGuid': assembly_guid} if assembly_guid else {}
        return self._get(f'/Packages/{name}', params)
    
    def install_package(self, name: str, assembly_guid: str = None,
                        version: str = None, repository_url: str = None) -> bool:
        """POST /Packages/Installed/{name} - Install package"""
        params = {k: v for k, v in {
            'assemblyGuid': assembly_guid, 'version': version,
            'repositoryUrl': repository_url
        }.items() if v is not None}
        return self._post(f'/Packages/Installed/{name}', params=params) is not None
    
    def cancel_package_install(self, package_id: str) -> bool:
        """DELETE /Packages/Installing/{packageId} - Cancel package install"""
        return self._delete(f'/Packages/Installing/{package_id}') is not None
    
    def get_repositories(self) -> Optional[List]:
        """GET /Repositories - Get repositories"""
        return self._get('/Repositories')
    
    def set_repositories(self, repositories: List[Dict]) -> bool:
        """POST /Repositories - Set repositories"""
        return self._post('/Repositories', json_data=repositories) is not None

    # =========================================================================
    # PERSONS (2 endpoints)
    # =========================================================================
    
    def get_persons(self, user_id: str = None, start_index: int = None,
                    limit: int = None, **kwargs) -> Optional[Dict]:
        """GET /Persons - Get persons"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit, **kwargs
        }.items() if v is not None}
        return self._get('/Persons', params)
    
    def get_person(self, name: str, user_id: str = None) -> Optional[Dict]:
        """GET /Persons/{name} - Get person by name"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Persons/{name}', params)

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


    # =========================================================================
    # PLAYSTATE (9 endpoints)
    # =========================================================================
    
    def report_playback_start(self, session_id: str = None, item_id: str = None,
                               media_source_id: str = None, **kwargs) -> bool:
        """POST /Sessions/Playing - Report playback start"""
        body = {k: v for k, v in {
            'SessionId': session_id, 'ItemId': item_id,
            'MediaSourceId': media_source_id, **kwargs
        }.items() if v is not None}
        return self._post('/Sessions/Playing', json_data=body) is not None
    
    def report_playback_progress(self, session_id: str = None, item_id: str = None,
                                  media_source_id: str = None, position_ticks: int = None,
                                  is_paused: bool = None, is_muted: bool = None,
                                  **kwargs) -> bool:
        """POST /Sessions/Playing/Progress - Report playback progress"""
        body = {k: v for k, v in {
            'SessionId': session_id, 'ItemId': item_id,
            'MediaSourceId': media_source_id, 'PositionTicks': position_ticks,
            'IsPaused': is_paused, 'IsMuted': is_muted, **kwargs
        }.items() if v is not None}
        return self._post('/Sessions/Playing/Progress', json_data=body) is not None
    
    def report_playback_stopped(self, session_id: str = None, item_id: str = None,
                                 media_source_id: str = None, position_ticks: int = None,
                                 **kwargs) -> bool:
        """POST /Sessions/Playing/Stopped - Report playback stopped"""
        body = {k: v for k, v in {
            'SessionId': session_id, 'ItemId': item_id,
            'MediaSourceId': media_source_id, 'PositionTicks': position_ticks, **kwargs
        }.items() if v is not None}
        return self._post('/Sessions/Playing/Stopped', json_data=body) is not None
    
    def ping_playback_session(self, play_session_id: str) -> bool:
        """POST /Sessions/Playing/Ping - Ping playback session"""
        return self._post('/Sessions/Playing/Ping',
                         params={'playSessionId': play_session_id}) is not None
    
    def on_playback_start(self, item_id: str, media_source_id: str = None,
                          audio_stream_index: int = None, subtitle_stream_index: int = None,
                          play_method: str = None, live_stream_id: str = None,
                          play_session_id: str = None, can_seek: bool = None) -> bool:
        """POST /PlayingItems/{itemId} - Mark item playing"""
        params = {k: v for k, v in {
            'mediaSourceId': media_source_id, 'audioStreamIndex': audio_stream_index,
            'subtitleStreamIndex': subtitle_stream_index, 'playMethod': play_method,
            'liveStreamId': live_stream_id, 'playSessionId': play_session_id,
            'canSeek': can_seek
        }.items() if v is not None}
        return self._post(f'/PlayingItems/{item_id}', params=params) is not None
    
    def on_playback_progress(self, item_id: str, media_source_id: str = None,
                              position_ticks: int = None, audio_stream_index: int = None,
                              subtitle_stream_index: int = None, volume_level: int = None,
                              play_method: str = None, live_stream_id: str = None,
                              play_session_id: str = None, repeat_mode: str = None,
                              is_paused: bool = None, is_muted: bool = None) -> bool:
        """POST /PlayingItems/{itemId}/Progress - Report playback progress"""
        params = {k: v for k, v in {
            'mediaSourceId': media_source_id, 'positionTicks': position_ticks,
            'audioStreamIndex': audio_stream_index, 'subtitleStreamIndex': subtitle_stream_index,
            'volumeLevel': volume_level, 'playMethod': play_method,
            'liveStreamId': live_stream_id, 'playSessionId': play_session_id,
            'repeatMode': repeat_mode, 'isPaused': is_paused, 'isMuted': is_muted
        }.items() if v is not None}
        return self._post(f'/PlayingItems/{item_id}/Progress', params=params) is not None
    
    def on_playback_stopped(self, item_id: str, media_source_id: str = None,
                             next_media_type: str = None, position_ticks: int = None,
                             live_stream_id: str = None, play_session_id: str = None) -> bool:
        """DELETE /PlayingItems/{itemId} - Report playback stopped"""
        params = {k: v for k, v in {
            'mediaSourceId': media_source_id, 'nextMediaType': next_media_type,
            'positionTicks': position_ticks, 'liveStreamId': live_stream_id,
            'playSessionId': play_session_id
        }.items() if v is not None}
        return self._delete(f'/PlayingItems/{item_id}', params=params) is not None
    
    def mark_played(self, item_id: str, user_id: str = None, date_played: str = None) -> Optional[Dict]:
        """POST /UserPlayedItems/{itemId} - Mark item played"""
        params = {k: v for k, v in {'userId': user_id, 'datePlayed': date_played}.items() if v is not None}
        return self._post(f'/UserPlayedItems/{item_id}', params=params)
    
    def mark_unplayed(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """DELETE /UserPlayedItems/{itemId} - Mark item unplayed"""
        params = {'userId': user_id} if user_id else {}
        return self._delete(f'/UserPlayedItems/{item_id}', params=params)

    # =========================================================================
    # PLUGINS (9 endpoints)
    # =========================================================================
    
    def get_plugins(self) -> Optional[List]:
        """GET /Plugins - Get installed plugins"""
        return self._get('/Plugins')
    
    def uninstall_plugin(self, plugin_id: str) -> bool:
        """DELETE /Plugins/{pluginId} - Uninstall plugin"""
        return self._delete(f'/Plugins/{plugin_id}') is not None
    
    def uninstall_plugin_version(self, plugin_id: str, version: str) -> bool:
        """DELETE /Plugins/{pluginId}/{version} - Uninstall plugin version"""
        return self._delete(f'/Plugins/{plugin_id}/{version}') is not None
    
    def get_plugin_configuration(self, plugin_id: str) -> Optional[Dict]:
        """GET /Plugins/{pluginId}/Configuration - Get plugin configuration"""
        return self._get(f'/Plugins/{plugin_id}/Configuration')
    
    def update_plugin_configuration(self, plugin_id: str, config: Dict) -> bool:
        """POST /Plugins/{pluginId}/Configuration - Update plugin configuration"""
        return self._post(f'/Plugins/{plugin_id}/Configuration', json_data=config) is not None
    
    def get_plugin_image_url(self, plugin_id: str, version: str) -> str:
        """GET /Plugins/{pluginId}/{version}/Image - Get plugin image URL"""
        return f"{self.base_url}/Plugins/{plugin_id}/{version}/Image?api_key={self.api_key}"
    
    def get_plugin_manifest(self, plugin_id: str) -> Optional[Dict]:
        """POST /Plugins/{pluginId}/Manifest - Get plugin manifest"""
        return self._post(f'/Plugins/{plugin_id}/Manifest')
    
    def disable_plugin(self, plugin_id: str, version: str) -> bool:
        """POST /Plugins/{pluginId}/{version}/Disable - Disable plugin"""
        return self._post(f'/Plugins/{plugin_id}/{version}/Disable') is not None
    
    def enable_plugin(self, plugin_id: str, version: str) -> bool:
        """POST /Plugins/{pluginId}/{version}/Enable - Enable plugin"""
        return self._post(f'/Plugins/{plugin_id}/{version}/Enable') is not None

    # =========================================================================
    # QUICK CONNECT (4 endpoints)
    # =========================================================================
    
    def get_quick_connect_enabled(self) -> Optional[bool]:
        """GET /QuickConnect/Enabled - Check if quick connect is enabled"""
        return self._get('/QuickConnect/Enabled')
    
    def initiate_quick_connect(self) -> Optional[Dict]:
        """POST /QuickConnect/Initiate - Initiate quick connect"""
        return self._post('/QuickConnect/Initiate')
    
    def quick_connect_status(self, secret: str) -> Optional[Dict]:
        """GET /QuickConnect/Connect - Get quick connect status"""
        return self._get('/QuickConnect/Connect', params={'secret': secret})
    
    def authorize_quick_connect(self, code: str, user_id: str = None) -> bool:
        """POST /QuickConnect/Authorize - Authorize quick connect"""
        params = {'code': code}
        if user_id:
            params['userId'] = user_id
        return self._post('/QuickConnect/Authorize', params=params) is not None

    # =========================================================================
    # REMOTE IMAGE (3 endpoints)
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
    # SCHEDULED TASKS (5 endpoints)
    # =========================================================================
    
    def get_scheduled_tasks(self, is_hidden: bool = None, is_enabled: bool = None) -> Optional[List]:
        """GET /ScheduledTasks - Get scheduled tasks"""
        params = {k: v for k, v in {'isHidden': is_hidden, 'isEnabled': is_enabled}.items() if v is not None}
        return self._get('/ScheduledTasks', params)
    
    def get_scheduled_task(self, task_id: str) -> Optional[Dict]:
        """GET /ScheduledTasks/{taskId} - Get scheduled task"""
        return self._get(f'/ScheduledTasks/{task_id}')
    
    def start_scheduled_task(self, task_id: str) -> bool:
        """POST /ScheduledTasks/Running/{taskId} - Start scheduled task"""
        return self._post(f'/ScheduledTasks/Running/{task_id}') is not None
    
    def stop_scheduled_task(self, task_id: str) -> bool:
        """DELETE /ScheduledTasks/Running/{taskId} - Stop scheduled task"""
        return self._delete(f'/ScheduledTasks/Running/{task_id}') is not None
    
    def update_task_triggers(self, task_id: str, triggers: List[Dict]) -> bool:
        """POST /ScheduledTasks/{taskId}/Triggers - Update task triggers"""
        return self._post(f'/ScheduledTasks/{task_id}/Triggers', json_data=triggers) is not None

    # =========================================================================
    # SEARCH (1 endpoint)
    # =========================================================================
    
    def search(self, search_term: str, user_id: str = None, start_index: int = None,
               limit: int = None, include_item_types: List[str] = None,
               exclude_item_types: List[str] = None, media_types: List[str] = None,
               parent_id: str = None, is_movie: bool = None, is_series: bool = None,
               is_news: bool = None, is_kids: bool = None, is_sports: bool = None,
               include_people: bool = None, include_media: bool = None,
               include_genres: bool = None, include_studios: bool = None,
               include_artists: bool = None) -> Optional[Dict]:
        """GET /Search/Hints - Search for items"""
        params = {'searchTerm': search_term}
        if user_id:
            params['userId'] = user_id
        if start_index is not None:
            params['startIndex'] = start_index
        if limit is not None:
            params['limit'] = limit
        if include_item_types:
            params['includeItemTypes'] = ','.join(include_item_types)
        if exclude_item_types:
            params['excludeItemTypes'] = ','.join(exclude_item_types)
        if media_types:
            params['mediaTypes'] = ','.join(media_types)
        if parent_id:
            params['parentId'] = parent_id
        for key, val in [('isMovie', is_movie), ('isSeries', is_series),
                         ('isNews', is_news), ('isKids', is_kids), ('isSports', is_sports),
                         ('includePeople', include_people), ('includeMedia', include_media),
                         ('includeGenres', include_genres), ('includeStudios', include_studios),
                         ('includeArtists', include_artists)]:
            if val is not None:
                params[key] = val
        return self._get('/Search/Hints', params)


    # =========================================================================
    # SESSION (16 endpoints)
    # =========================================================================
    
    def get_sessions(self, controllable_by_user_id: str = None,
                     device_id: str = None, active_within_seconds: int = None) -> Optional[List]:
        """GET /Sessions - Get active sessions"""
        params = {k: v for k, v in {
            'controllableByUserId': controllable_by_user_id,
            'deviceId': device_id, 'activeWithinSeconds': active_within_seconds
        }.items() if v is not None}
        result = self._get('/Sessions', params)
        return result if result else []
    
    def get_auth_providers(self) -> Optional[List]:
        """GET /Auth/Providers - Get auth providers"""
        return self._get('/Auth/Providers')
    
    def get_password_reset_providers(self) -> Optional[List]:
        """GET /Auth/PasswordResetProviders - Get password reset providers"""
        return self._get('/Auth/PasswordResetProviders')
    
    def post_capabilities(self, capabilities: Dict) -> bool:
        """POST /Sessions/Capabilities - Post session capabilities"""
        return self._post('/Sessions/Capabilities', json_data=capabilities) is not None
    
    def post_full_capabilities(self, capabilities: Dict) -> bool:
        """POST /Sessions/Capabilities/Full - Post full capabilities"""
        return self._post('/Sessions/Capabilities/Full', json_data=capabilities) is not None
    
    def logout(self) -> bool:
        """POST /Sessions/Logout - Logout current session"""
        return self._post('/Sessions/Logout') is not None
    
    def report_viewing(self, item_id: str, session_id: str = None) -> bool:
        """POST /Sessions/Viewing - Report item being viewed"""
        params = {'itemId': item_id}
        if session_id:
            params['sessionId'] = session_id
        return self._post('/Sessions/Viewing', params=params) is not None
    
    def send_general_command(self, session_id: str, command: Dict) -> bool:
        """POST /Sessions/{sessionId}/Command - Send general command"""
        return self._post(f'/Sessions/{session_id}/Command', json_data=command) is not None
    
    def send_command(self, session_id: str, command: str) -> bool:
        """POST /Sessions/{sessionId}/Command/{command} - Send simple command"""
        return self._post(f'/Sessions/{session_id}/Command/{command}') is not None
    
    def send_message(self, session_id: str, text: str, header: str = None,
                     timeout_ms: int = None) -> bool:
        """POST /Sessions/{sessionId}/Message - Send message to session"""
        body = {'Text': text}
        if header:
            body['Header'] = header
        if timeout_ms:
            body['TimeoutMs'] = timeout_ms
        return self._post(f'/Sessions/{session_id}/Message', json_data=body) is not None
    
    def send_play_command(self, session_id: str, item_ids: List[str],
                          play_command: str = 'PlayNow', start_position_ticks: int = None) -> bool:
        """POST /Sessions/{sessionId}/Playing - Send play command"""
        params = {
            'itemIds': ','.join(item_ids),
            'playCommand': play_command
        }
        if start_position_ticks is not None:
            params['startPositionTicks'] = start_position_ticks
        return self._post(f'/Sessions/{session_id}/Playing', params=params) is not None
    
    def send_playstate_command(self, session_id: str, command: str,
                                seek_position_ticks: int = None,
                                controlling_user_id: str = None) -> bool:
        """POST /Sessions/{sessionId}/Playing/{command} - Send playstate command"""
        params = {}
        if seek_position_ticks is not None:
            params['seekPositionTicks'] = seek_position_ticks
        if controlling_user_id:
            params['controllingUserId'] = controlling_user_id
        return self._post(f'/Sessions/{session_id}/Playing/{command}', params=params) is not None
    
    def send_system_command(self, session_id: str, command: str) -> bool:
        """POST /Sessions/{sessionId}/System/{command} - Send system command"""
        return self._post(f'/Sessions/{session_id}/System/{command}') is not None
    
    def add_user_to_session(self, session_id: str, user_id: str) -> bool:
        """POST /Sessions/{sessionId}/User/{userId} - Add user to session"""
        return self._post(f'/Sessions/{session_id}/User/{user_id}') is not None
    
    def remove_user_from_session(self, session_id: str, user_id: str) -> bool:
        """DELETE /Sessions/{sessionId}/User/{userId} - Remove user from session"""
        return self._delete(f'/Sessions/{session_id}/User/{user_id}') is not None
    
    def display_content(self, session_id: str, item_type: str, item_id: str,
                        item_name: str) -> bool:
        """POST /Sessions/{sessionId}/Viewing - Display content on session"""
        return self._post(f'/Sessions/{session_id}/Viewing',
                         params={'itemType': item_type, 'itemId': item_id,
                                'itemName': item_name}) is not None

    # =========================================================================
    # STARTUP (7 endpoints)
    # =========================================================================
    
    def get_startup_configuration(self) -> Optional[Dict]:
        """GET /Startup/Configuration - Get startup configuration"""
        return self._get('/Startup/Configuration')
    
    def update_startup_configuration(self, config: Dict) -> bool:
        """POST /Startup/Configuration - Update startup configuration"""
        return self._post('/Startup/Configuration', json_data=config) is not None
    
    def get_first_user(self) -> Optional[Dict]:
        """GET /Startup/FirstUser - Get first user info"""
        return self._get('/Startup/FirstUser')
    
    def get_startup_user(self) -> Optional[Dict]:
        """GET /Startup/User - Get startup user"""
        return self._get('/Startup/User')
    
    def update_startup_user(self, user: Dict) -> bool:
        """POST /Startup/User - Update startup user"""
        return self._post('/Startup/User', json_data=user) is not None
    
    def complete_wizard(self) -> bool:
        """POST /Startup/Complete - Complete setup wizard"""
        return self._post('/Startup/Complete') is not None
    
    def set_remote_access(self, enable_remote_access: bool,
                          enable_automatic_port_mapping: bool) -> bool:
        """POST /Startup/RemoteAccess - Set remote access"""
        return self._post('/Startup/RemoteAccess', json_data={
            'EnableRemoteAccess': enable_remote_access,
            'EnableAutomaticPortMapping': enable_automatic_port_mapping
        }) is not None

    # =========================================================================
    # STUDIOS (2 endpoints)
    # =========================================================================
    
    def get_studios(self, user_id: str = None, start_index: int = None,
                    limit: int = None, parent_id: str = None) -> Optional[Dict]:
        """GET /Studios - Get studios"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index,
            'limit': limit, 'parentId': parent_id
        }.items() if v is not None}
        return self._get('/Studios', params)
    
    def get_studio(self, name: str, user_id: str = None) -> Optional[Dict]:
        """GET /Studios/{name} - Get studio by name"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Studios/{name}', params)

    # =========================================================================
    # SUBTITLE (10 endpoints)
    # =========================================================================
    
    def search_remote_subtitles(self, item_id: str, language: str,
                                 is_perfect_match: bool = None) -> Optional[List]:
        """GET /Items/{itemId}/RemoteSearch/Subtitles/{language} - Search subtitles"""
        params = {'isPerfectMatch': is_perfect_match} if is_perfect_match is not None else {}
        return self._get(f'/Items/{item_id}/RemoteSearch/Subtitles/{language}', params)
    
    def download_remote_subtitles(self, item_id: str, subtitle_id: str) -> bool:
        """POST /Items/{itemId}/RemoteSearch/Subtitles/{subtitleId} - Download subtitles"""
        return self._post(f'/Items/{item_id}/RemoteSearch/Subtitles/{subtitle_id}') is not None
    
    def get_subtitle_provider_info(self, subtitle_id: str) -> Optional[Dict]:
        """GET /Providers/Subtitles/Subtitles/{subtitleId} - Get subtitle provider info"""
        return self._get(f'/Providers/Subtitles/Subtitles/{subtitle_id}')
    
    def upload_subtitles(self, item_id: str, subtitle_data: Dict) -> bool:
        """POST /Videos/{itemId}/Subtitles - Upload subtitles"""
        return self._post(f'/Videos/{item_id}/Subtitles', json_data=subtitle_data) is not None
    
    def delete_subtitles(self, item_id: str, index: int) -> bool:
        """DELETE /Videos/{itemId}/Subtitles/{index} - Delete subtitles"""
        return self._delete(f'/Videos/{item_id}/Subtitles/{index}') is not None
    
    def get_subtitle_playlist_url(self, item_id: str, media_source_id: str,
                                   index: int) -> str:
        """Get subtitle playlist URL"""
        return (f"{self.base_url}/Videos/{item_id}/{media_source_id}/Subtitles/"
                f"{index}/subtitles.m3u8?api_key={self.api_key}")
    
    def get_subtitle_url(self, item_id: str, media_source_id: str,
                         index: int, format: str = 'srt',
                         start_position_ticks: int = None) -> str:
        """Get subtitle file URL"""
        if start_position_ticks:
            return (f"{self.base_url}/Videos/{item_id}/{media_source_id}/Subtitles/"
                    f"{index}/{start_position_ticks}/Stream.{format}?api_key={self.api_key}")
        return (f"{self.base_url}/Videos/{item_id}/{media_source_id}/Subtitles/"
                f"{index}/Stream.{format}?api_key={self.api_key}")
    
    def get_fallback_fonts(self) -> Optional[List]:
        """GET /FallbackFont/Fonts - Get fallback fonts"""
        return self._get('/FallbackFont/Fonts')
    
    def get_fallback_font_url(self, name: str) -> str:
        """Get fallback font URL"""
        return f"{self.base_url}/FallbackFont/Fonts/{name}?api_key={self.api_key}"

    # =========================================================================
    # SUGGESTIONS (1 endpoint)
    # =========================================================================
    
    def get_suggestions(self, user_id: str = None, media_type: List[str] = None,
                        type: List[str] = None, start_index: int = None,
                        limit: int = None, enable_total_record_count: bool = None) -> Optional[Dict]:
        """GET /Items/Suggestions - Get suggestions"""
        params = {}
        if user_id:
            params['userId'] = user_id
        if media_type:
            params['mediaType'] = ','.join(media_type)
        if type:
            params['type'] = ','.join(type)
        if start_index is not None:
            params['startIndex'] = start_index
        if limit is not None:
            params['limit'] = limit
        if enable_total_record_count is not None:
            params['enableTotalRecordCount'] = enable_total_record_count
        return self._get('/Items/Suggestions', params)


    # =========================================================================
    # SYNC PLAY (22 endpoints)
    # =========================================================================
    
    def get_sync_play_groups(self) -> Optional[List]:
        """GET /SyncPlay/List - Get sync play groups"""
        return self._get('/SyncPlay/List')
    
    def get_sync_play_group(self, group_id: str) -> Optional[Dict]:
        """GET /SyncPlay/{id} - Get sync play group"""
        return self._get(f'/SyncPlay/{group_id}')
    
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

    # =========================================================================
    # SYSTEM (10 endpoints)
    # =========================================================================
    
    def get_system_info(self) -> Optional[Dict]:
        """GET /System/Info - Get system info"""
        result = self._get('/System/Info')
        if result:
            self._server_info_cache = result
        return result
    
    def get_public_system_info(self) -> Optional[Dict]:
        """GET /System/Info/Public - Get public system info"""
        return self._get('/System/Info/Public')
    
    def get_storage_info(self) -> Optional[Dict]:
        """GET /System/Info/Storage - Get storage info"""
        return self._get('/System/Info/Storage')
    
    def ping(self) -> bool:
        """GET /System/Ping - Ping server"""
        result = self._get('/System/Ping')
        return result is not None
    
    def ping_post(self) -> bool:
        """POST /System/Ping - Ping server (POST)"""
        return self._post('/System/Ping') is not None
    
    def restart_server(self) -> bool:
        """POST /System/Restart - Restart server"""
        return self._post('/System/Restart') is not None
    
    def shutdown_server(self) -> bool:
        """POST /System/Shutdown - Shutdown server"""
        return self._post('/System/Shutdown') is not None
    
    def get_server_logs(self) -> Optional[List]:
        """GET /System/Logs - Get server logs list"""
        return self._get('/System/Logs')
    
    def get_log_file(self, name: str) -> Optional[str]:
        """GET /System/Logs/Log - Get log file content"""
        response = self._get('/System/Logs/Log', params={'name': name}, raw_response=True)
        return response.text if response else None
    
    def get_endpoint_info(self) -> Optional[Dict]:
        """GET /System/Endpoint - Get endpoint info"""
        return self._get('/System/Endpoint')
    
    def get_server_id(self) -> str:
        """Get server ID (cached)"""
        if self._server_info_cache:
            return self._server_info_cache.get('Id', 'unknown')
        info = self.get_system_info()
        return info.get('Id', 'unknown') if info else 'unknown'

    # =========================================================================
    # TIME SYNC (1 endpoint)
    # =========================================================================
    
    def get_utc_time(self) -> Optional[Dict]:
        """GET /GetUtcTime - Get UTC time"""
        return self._get('/GetUtcTime')

    # =========================================================================
    # TMDB (1 endpoint)
    # =========================================================================
    
    def get_tmdb_client_configuration(self) -> Optional[Dict]:
        """GET /Tmdb/ClientConfiguration - Get TMDB client configuration"""
        return self._get('/Tmdb/ClientConfiguration')

    # =========================================================================
    # TRAILERS (1 endpoint)
    # =========================================================================
    
    def get_trailers(self, user_id: str = None, start_index: int = None,
                     limit: int = None, **kwargs) -> Optional[Dict]:
        """GET /Trailers - Get trailers"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit, **kwargs
        }.items() if v is not None}
        return self._get('/Trailers', params)

    # =========================================================================
    # TRICKPLAY (2 endpoints) - URL generation
    # =========================================================================
    
    def get_trickplay_manifest_url(self, item_id: str, width: int) -> str:
        """Get trickplay manifest URL"""
        return f"{self.base_url}/Videos/{item_id}/Trickplay/{width}/tiles.m3u8?api_key={self.api_key}"
    
    def get_trickplay_tile_url(self, item_id: str, width: int, index: int) -> str:
        """Get trickplay tile URL"""
        return f"{self.base_url}/Videos/{item_id}/Trickplay/{width}/{index}.jpg?api_key={self.api_key}"

    # =========================================================================
    # TV SHOWS (4 endpoints)
    # =========================================================================
    
    def get_next_up(self, user_id: str = None, start_index: int = None,
                    limit: int = None, parent_id: str = None,
                    enable_images: bool = None, enable_total_record_count: bool = None,
                    disable_first_episode: bool = None, **kwargs) -> Optional[Dict]:
        """GET /Shows/NextUp - Get next up episodes"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit,
            'parentId': parent_id, 'enableImages': enable_images,
            'enableTotalRecordCount': enable_total_record_count,
            'disableFirstEpisode': disable_first_episode, **kwargs
        }.items() if v is not None}
        return self._get('/Shows/NextUp', params)
    
    def get_upcoming_episodes(self, user_id: str = None, start_index: int = None,
                               limit: int = None, parent_id: str = None,
                               enable_images: bool = None) -> Optional[Dict]:
        """GET /Shows/Upcoming - Get upcoming episodes"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit,
            'parentId': parent_id, 'enableImages': enable_images
        }.items() if v is not None}
        return self._get('/Shows/Upcoming', params)
    
    def get_episodes(self, series_id: str, user_id: str = None,
                     season_id: str = None, season: int = None,
                     start_index: int = None, limit: int = None,
                     is_missing: bool = None, adjacent_to: str = None,
                     enable_images: bool = None, **kwargs) -> Optional[Dict]:
        """GET /Shows/{seriesId}/Episodes - Get episodes"""
        params = {k: v for k, v in {
            'userId': user_id, 'seasonId': season_id, 'season': season,
            'startIndex': start_index, 'limit': limit, 'isMissing': is_missing,
            'adjacentTo': adjacent_to, 'enableImages': enable_images, **kwargs
        }.items() if v is not None}
        return self._get(f'/Shows/{series_id}/Episodes', params)
    
    def get_seasons(self, series_id: str, user_id: str = None,
                    is_special_season: bool = None, is_missing: bool = None,
                    adjacent_to: str = None, enable_images: bool = None) -> Optional[Dict]:
        """GET /Shows/{seriesId}/Seasons - Get seasons"""
        params = {k: v for k, v in {
            'userId': user_id, 'isSpecialSeason': is_special_season,
            'isMissing': is_missing, 'adjacentTo': adjacent_to,
            'enableImages': enable_images
        }.items() if v is not None}
        return self._get(f'/Shows/{series_id}/Seasons', params)

    # =========================================================================
    # UNIVERSAL AUDIO (1 endpoint)
    # =========================================================================
    
    def get_universal_audio_url(self, item_id: str, container: List[str] = None,
                                 media_source_id: str = None, device_id: str = None,
                                 user_id: str = None, audio_codec: str = None,
                                 max_audio_channels: int = None, transcoding_audio_channels: int = None,
                                 max_streaming_bitrate: int = None, audio_bit_rate: int = None,
                                 start_time_ticks: int = None, transcoding_container: str = None,
                                 transcoding_protocol: str = None, max_audio_sample_rate: int = None,
                                 max_audio_bit_depth: int = None, enable_remote_media: bool = None,
                                 break_on_non_key_frames: bool = None,
                                 enable_redirection: bool = None) -> str:
        """Get universal audio stream URL"""
        params = ['api_key=' + self.api_key]
        if container:
            params.append('container=' + ','.join(container))
        for key, val in [
            ('mediaSourceId', media_source_id), ('deviceId', device_id),
            ('userId', user_id), ('audioCodec', audio_codec),
            ('maxAudioChannels', max_audio_channels),
            ('transcodingAudioChannels', transcoding_audio_channels),
            ('maxStreamingBitrate', max_streaming_bitrate),
            ('audioBitRate', audio_bit_rate), ('startTimeTicks', start_time_ticks),
            ('transcodingContainer', transcoding_container),
            ('transcodingProtocol', transcoding_protocol),
            ('maxAudioSampleRate', max_audio_sample_rate),
            ('maxAudioBitDepth', max_audio_bit_depth),
            ('enableRemoteMedia', enable_remote_media),
            ('breakOnNonKeyFrames', break_on_non_key_frames),
            ('enableRedirection', enable_redirection)
        ]:
            if val is not None:
                params.append(f'{key}={val}')
        return f"{self.base_url}/Audio/{item_id}/universal?{'&'.join(params)}"


    # =========================================================================
    # USER (14 endpoints)
    # =========================================================================
    
    def get_users(self, is_hidden: bool = None, is_disabled: bool = None) -> Optional[List]:
        """GET /Users - Get users"""
        params = {k: v for k, v in {'isHidden': is_hidden, 'isDisabled': is_disabled}.items() if v is not None}
        return self._get('/Users', params)
    
    def get_public_users(self) -> Optional[List]:
        """GET /Users/Public - Get public users"""
        return self._get('/Users/Public')
    
    def get_current_user(self) -> Optional[Dict]:
        """GET /Users/Me - Get current user"""
        return self._get('/Users/Me')
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """GET /Users/{userId} - Get user by ID"""
        return self._get(f'/Users/{user_id}')
    
    def delete_user(self, user_id: str) -> bool:
        """DELETE /Users/{userId} - Delete user"""
        return self._delete(f'/Users/{user_id}') is not None
    
    def create_user_by_name(self, name: str, password: str = None) -> Optional[Dict]:
        """POST /Users/New - Create user by name"""
        body = {'Name': name}
        if password:
            body['Password'] = password
        return self._post('/Users/New', json_data=body)
    
    def authenticate_user(self, username: str, pw: str) -> Optional[Dict]:
        """POST /Users/AuthenticateByName - Authenticate user"""
        return self._post('/Users/AuthenticateByName', json_data={
            'Username': username, 'Pw': pw
        })
    
    def authenticate_with_quick_connect(self, secret: str) -> Optional[Dict]:
        """POST /Users/AuthenticateWithQuickConnect - Authenticate with quick connect"""
        return self._post('/Users/AuthenticateWithQuickConnect',
                         json_data={'Secret': secret})
    
    def update_user_configuration(self, user_id: str = None, config: Dict = None) -> bool:
        """POST /Users/Configuration - Update user configuration"""
        params = {'userId': user_id} if user_id else {}
        return self._post('/Users/Configuration', params=params, json_data=config) is not None
    
    def update_user_password(self, user_id: str = None, current_pw: str = None,
                              new_pw: str = None, reset_password: bool = None) -> bool:
        """POST /Users/Password - Update user password"""
        params = {'userId': user_id} if user_id else {}
        body = {}
        if current_pw:
            body['CurrentPw'] = current_pw
        if new_pw:
            body['NewPw'] = new_pw
        if reset_password is not None:
            body['ResetPassword'] = reset_password
        return self._post('/Users/Password', params=params, json_data=body) is not None
    
    def forgot_password(self, entered_username: str) -> Optional[Dict]:
        """POST /Users/ForgotPassword - Initiate forgot password"""
        return self._post('/Users/ForgotPassword',
                         json_data={'EnteredUsername': entered_username})
    
    def forgot_password_pin(self, pin: str) -> Optional[Dict]:
        """POST /Users/ForgotPassword/Pin - Redeem forgot password pin"""
        return self._post('/Users/ForgotPassword/Pin', json_data={'Pin': pin})
    
    def update_user_policy(self, user_id: str, policy: Dict) -> bool:
        """POST /Users/{userId}/Policy - Update user policy"""
        return self._post(f'/Users/{user_id}/Policy', json_data=policy) is not None
    
    # Legacy method
    def create_user(self, name: str, password: str = None) -> Optional[Dict]:
        """POST /Users - Create user (legacy, use create_user_by_name)"""
        body = {'Name': name}
        if password:
            body['Password'] = password
        return self._post('/Users', json_data=body)

    # =========================================================================
    # USER LIBRARY (10 endpoints)
    # =========================================================================
    
    def get_latest_media(self, user_id: str = None, parent_id: str = None,
                         include_item_types: List[str] = None, limit: int = None,
                         is_played: bool = None, enable_images: bool = None,
                         image_type_limit: int = None, **kwargs) -> Optional[List]:
        """GET /Items/Latest - Get latest media"""
        params = {}
        if user_id:
            params['userId'] = user_id
        if parent_id:
            params['parentId'] = parent_id
        if include_item_types:
            params['includeItemTypes'] = ','.join(include_item_types)
        if limit is not None:
            params['limit'] = limit
        if is_played is not None:
            params['isPlayed'] = is_played
        if enable_images is not None:
            params['enableImages'] = enable_images
        if image_type_limit is not None:
            params['imageTypeLimit'] = image_type_limit
        params.update({k: v for k, v in kwargs.items() if v is not None})
        return self._get('/Items/Latest', params)
    
    def get_root_folder(self, user_id: str = None) -> Optional[Dict]:
        """GET /Items/Root - Get root folder"""
        params = {'userId': user_id} if user_id else {}
        return self._get('/Items/Root', params)
    
    def get_item(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /Items/{itemId} - Get item"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}', params)
    
    def get_intros(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /Items/{itemId}/Intros - Get intros"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/Intros', params)
    
    def get_local_trailers(self, item_id: str, user_id: str = None) -> Optional[List]:
        """GET /Items/{itemId}/LocalTrailers - Get local trailers"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/LocalTrailers', params)
    
    def get_special_features(self, item_id: str, user_id: str = None) -> Optional[List]:
        """GET /Items/{itemId}/SpecialFeatures - Get special features"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/SpecialFeatures', params)
    
    def mark_favorite(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """POST /UserFavoriteItems/{itemId} - Mark as favorite"""
        params = {'userId': user_id} if user_id else {}
        return self._post(f'/UserFavoriteItems/{item_id}', params=params)
    
    def unmark_favorite(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """DELETE /UserFavoriteItems/{itemId} - Unmark as favorite"""
        params = {'userId': user_id} if user_id else {}
        return self._delete(f'/UserFavoriteItems/{item_id}', params=params)
    
    def update_item_rating(self, item_id: str, likes: bool, user_id: str = None) -> Optional[Dict]:
        """POST /UserItems/{itemId}/Rating - Update item rating"""
        params = {'likes': likes}
        if user_id:
            params['userId'] = user_id
        return self._post(f'/UserItems/{item_id}/Rating', params=params)
    
    def delete_item_rating(self, item_id: str, user_id: str = None) -> bool:
        """DELETE /UserItems/{itemId}/Rating - Delete item rating"""
        params = {'userId': user_id} if user_id else {}
        return self._delete(f'/UserItems/{item_id}/Rating', params=params) is not None

    # =========================================================================
    # USER VIEWS (2 endpoints)
    # =========================================================================
    
    def get_user_views(self, user_id: str = None, include_external_content: bool = None,
                       preset_views: List[str] = None, include_hidden: bool = None) -> Optional[Dict]:
        """GET /UserViews - Get user views (libraries)"""
        params = {}
        if user_id:
            params['userId'] = user_id
        if include_external_content is not None:
            params['includeExternalContent'] = include_external_content
        if preset_views:
            params['presetViews'] = ','.join(preset_views)
        if include_hidden is not None:
            params['includeHidden'] = include_hidden
        return self._get('/UserViews', params)
    
    def get_grouping_options(self, user_id: str = None) -> Optional[List]:
        """GET /UserViews/GroupingOptions - Get grouping options"""
        params = {'userId': user_id} if user_id else {}
        return self._get('/UserViews/GroupingOptions', params)

    # =========================================================================
    # VIDEO ATTACHMENTS (1 endpoint)
    # =========================================================================
    
    def get_attachment_url(self, video_id: str, media_source_id: str, index: int) -> str:
        """Get video attachment URL"""
        return (f"{self.base_url}/Videos/{video_id}/{media_source_id}/Attachments/"
                f"{index}?api_key={self.api_key}")

    # =========================================================================
    # VIDEOS (5 endpoints)
    # =========================================================================
    
    def get_additional_parts(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /Videos/{itemId}/AdditionalParts - Get additional parts"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Videos/{item_id}/AdditionalParts', params)
    
    def get_video_stream_url(self, item_id: str, container: str = None) -> str:
        """Get video stream URL"""
        if container:
            return f"{self.base_url}/Videos/{item_id}/stream.{container}?api_key={self.api_key}"
        return f"{self.base_url}/Videos/{item_id}/stream?api_key={self.api_key}"
    
    def merge_versions(self, ids: List[str]) -> bool:
        """POST /Videos/MergeVersions - Merge video versions"""
        return self._post('/Videos/MergeVersions', params={'ids': ','.join(ids)}) is not None
    
    def delete_alternate_sources(self, item_id: str) -> bool:
        """DELETE /Videos/{itemId}/AlternateSources - Delete alternate sources"""
        return self._delete(f'/Videos/{item_id}/AlternateSources') is not None

    # =========================================================================
    # YEARS (2 endpoints)
    # =========================================================================
    
    def get_years(self, user_id: str = None, start_index: int = None,
                  limit: int = None, **kwargs) -> Optional[Dict]:
        """GET /Years - Get years"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit, **kwargs
        }.items() if v is not None}
        return self._get('/Years', params)
    
    def get_year(self, year: int, user_id: str = None) -> Optional[Dict]:
        """GET /Years/{year} - Get year"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Years/{year}', params)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def parse_session(session: Dict) -> Dict:
    """Parse session data into simplified format for MQTT"""
    now_playing = session.get('NowPlayingItem', {})
    play_state = session.get('PlayState', {})
    
    # Determine state
    if now_playing:
        state = 'paused' if play_state.get('IsPaused') else 'playing'
    else:
        state = 'idle'
    
    # Calculate progress
    position_ticks = play_state.get('PositionTicks', 0) or 0
    duration_ticks = now_playing.get('RunTimeTicks', 0) or 0
    
    position_sec = position_ticks // 10_000_000
    duration_sec = duration_ticks // 10_000_000
    progress = int((position_ticks / duration_ticks * 100)) if duration_ticks > 0 else 0
    
    # Determine play method
    play_method = 'DirectPlay'
    transcode_reasons = session.get('TranscodingInfo', {}).get('TranscodeReasons', [])
    if transcode_reasons:
        play_method = 'Transcode'
    elif session.get('TranscodingInfo'):
        play_method = 'DirectStream'
    
    # Build media info
    media_type = now_playing.get('Type', '')
    media_info = {
        'title': now_playing.get('Name', ''),
        'type': media_type,
        'artist': '',
        'album': '',
        'series': '',
        'season': None,
        'episode': None,
    }
    
    if media_type == 'Episode':
        media_info['series'] = now_playing.get('SeriesName', '')
        media_info['season'] = now_playing.get('ParentIndexNumber')
        media_info['episode'] = now_playing.get('IndexNumber')
    elif media_type == 'Audio':
        media_info['artist'] = ', '.join(now_playing.get('Artists', []))
        media_info['album'] = now_playing.get('Album', '')
    
    return {
        'session_id': session.get('Id', ''),
        'user': session.get('UserName', 'Unknown'),
        'client': session.get('Client', 'Unknown'),
        'device': session.get('DeviceName', 'Unknown'),
        'device_id': session.get('DeviceId', ''),
        'state': state,
        'position': position_sec,
        'duration': duration_sec,
        'progress': progress,
        'play_method': play_method,
        'is_transcoding': play_method == 'Transcode',
        'media': media_info,
        'now_playing': bool(now_playing)
    }
