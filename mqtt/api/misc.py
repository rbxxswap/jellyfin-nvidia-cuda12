#!/usr/bin/env python3
"""
Jellyfin API - Misc Group
Endpoints: ~60
- Subtitles, InstantMix, Channels, Environment, QuickConnect, Backup, 
  Localization, Branding, ApiKey, Startup, Filter, Lyrics, MediaInfo, etc.
"""

from typing import Optional, Dict, List, Any
from .base import JellyfinAPIBase


class MiscAPI(JellyfinAPIBase):
    """Miscellaneous API endpoints"""
    
    GROUP_NAME = 'misc'
    
    # =========================================================================
    # SUBTITLES (6 endpoints)
    # =========================================================================
    
    def search_remote_subtitles(self, item_id: str, language: str,
                                 is_perfect_match: bool = None) -> Optional[List]:
        """GET /Items/{itemId}/RemoteSearch/Subtitles/{language} - Search subtitles"""
        params = {'isPerfectMatch': is_perfect_match} if is_perfect_match is not None else {}
        return self._get(f'/Items/{item_id}/RemoteSearch/Subtitles/{language}', params)
    
    def download_remote_subtitles(self, item_id: str, subtitle_id: str) -> bool:
        """POST /Items/{itemId}/RemoteSearch/Subtitles/{subtitleId} - Download subtitles"""
        return self._post(f'/Items/{item_id}/RemoteSearch/Subtitles/{subtitle_id}') is not None
    
    def upload_subtitles(self, item_id: str, subtitle_data: Dict) -> bool:
        """POST /Videos/{itemId}/Subtitles - Upload subtitles"""
        return self._post(f'/Videos/{item_id}/Subtitles', json_data=subtitle_data) is not None
    
    def delete_subtitles(self, item_id: str, index: int) -> bool:
        """DELETE /Videos/{itemId}/Subtitles/{index} - Delete subtitles"""
        return self._delete(f'/Videos/{item_id}/Subtitles/{index}') is not None
    
    def get_subtitle_url(self, item_id: str, media_source_id: str,
                         index: int, format: str = 'srt') -> str:
        """Get subtitle file URL"""
        return (f"{self.base_url}/Videos/{item_id}/{media_source_id}/Subtitles/"
                f"{index}/Stream.{format}?api_key={self.api_key}")
    
    def get_fallback_fonts(self) -> Optional[List]:
        """GET /FallbackFont/Fonts - Get fallback fonts"""
        return self._get('/FallbackFont/Fonts')
    
    # =========================================================================
    # INSTANT MIX (8 endpoints)
    # =========================================================================
    
    def get_instant_mix_from_album(self, item_id: str, user_id: str = None,
                                    limit: int = None) -> Optional[Dict]:
        """GET /Albums/{itemId}/InstantMix - Get instant mix from album"""
        params = {k: v for k, v in {'userId': user_id, 'limit': limit}.items() if v is not None}
        return self._get(f'/Albums/{item_id}/InstantMix', params)
    
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
    
    def get_channel_items(self, channel_id: str, user_id: str = None,
                          start_index: int = None, limit: int = None) -> Optional[Dict]:
        """GET /Channels/{channelId}/Items - Get channel items"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit
        }.items() if v is not None}
        return self._get(f'/Channels/{channel_id}/Items', params)
    
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
    # BRANDING (2 endpoints)
    # =========================================================================
    
    def get_branding_configuration(self) -> Optional[Dict]:
        """GET /Branding/Configuration - Get branding config"""
        return self._get('/Branding/Configuration')
    
    def get_branding_css(self) -> Optional[str]:
        """GET /Branding/Css - Get custom CSS"""
        response = self._get('/Branding/Css', raw_response=True)
        return response.text if response else None
    
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
    # LYRICS (4 endpoints)
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
    
    # =========================================================================
    # MEDIA INFO (4 endpoints)
    # =========================================================================
    
    def get_playback_info(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /Items/{itemId}/PlaybackInfo - Get playback info"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/PlaybackInfo', params)
    
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
    
    def stop_encoding_process(self, device_id: str, play_session_id: str = None) -> bool:
        """DELETE /Videos/ActiveEncodings - Stop encoding process"""
        params = {'deviceId': device_id}
        if play_session_id:
            params['playSessionId'] = play_session_id
        return self._delete('/Videos/ActiveEncodings', params=params) is not None
    
    # =========================================================================
    # VIDEOS (3 endpoints)
    # =========================================================================
    
    def get_additional_parts(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /Videos/{itemId}/AdditionalParts - Get additional parts"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Videos/{item_id}/AdditionalParts', params)
    
    def merge_versions(self, ids: List[str]) -> bool:
        """POST /Videos/MergeVersions - Merge video versions"""
        return self._post('/Videos/MergeVersions', params={'ids': ','.join(ids)}) is not None
    
    def delete_alternate_sources(self, item_id: str) -> bool:
        """DELETE /Videos/{itemId}/AlternateSources - Delete alternate sources"""
        return self._delete(f'/Videos/{item_id}/AlternateSources') is not None
    
    # =========================================================================
    # ITEM LOOKUP (6 endpoints)
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
    
    def search_remote_movie(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/Movie - Search for movie"""
        return self._post('/Items/RemoteSearch/Movie', json_data=query)
    
    def search_remote_series(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/Series - Search for series"""
        return self._post('/Items/RemoteSearch/Series', json_data=query)
    
    def search_remote_music_album(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/MusicAlbum - Search for music album"""
        return self._post('/Items/RemoteSearch/MusicAlbum', json_data=query)
    
    def search_remote_person(self, query: Dict) -> Optional[List]:
        """POST /Items/RemoteSearch/Person - Search for person"""
        return self._post('/Items/RemoteSearch/Person', json_data=query)
    
    # =========================================================================
    # DASHBOARD (2 endpoints)
    # =========================================================================
    
    def get_configuration_pages(self, enable_in_main_menu: bool = None) -> Optional[List]:
        """GET /web/ConfigurationPages - Get dashboard configuration pages"""
        params = {}
        if enable_in_main_menu is not None:
            params['enableInMainMenu'] = enable_in_main_menu
        return self._get('/web/ConfigurationPages', params)
    
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
