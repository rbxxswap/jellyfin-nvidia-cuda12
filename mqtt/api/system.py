#!/usr/bin/env python3
"""
Jellyfin API - System Group
Endpoints: 10
- Server info, ping, restart, shutdown, logs, storage
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class SystemAPI(JellyfinAPIBase):
    """System API endpoints"""
    
    GROUP_NAME = 'system'
    
    def __init__(self, base_url: str, api_key: str):
        super().__init__(base_url, api_key)
        self._server_info_cache = None
    
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
    # CONFIGURATION (6 endpoints)
    # =========================================================================
    
    def get_configuration(self) -> Optional[Dict]:
        """GET /System/Configuration - Get server configuration"""
        return self._get('/System/Configuration')
    
    def update_configuration(self, config: Dict) -> bool:
        """POST /System/Configuration - Update server configuration"""
        return self._post('/System/Configuration', json_data=config) is not None
    
    def get_default_metadata_options(self) -> Optional[Dict]:
        """GET /System/Configuration/MetadataOptions/Default"""
        return self._get('/System/Configuration/MetadataOptions/Default')
    
    def get_named_configuration(self, key: str) -> Optional[Dict]:
        """GET /System/Configuration/{key} - Get named configuration"""
        return self._get(f'/System/Configuration/{key}')
    
    def update_named_configuration(self, key: str, config: Dict) -> bool:
        """POST /System/Configuration/{key} - Update named configuration"""
        return self._post(f'/System/Configuration/{key}', json_data=config) is not None
    
    # =========================================================================
    # TIME SYNC (1 endpoint)
    # =========================================================================
    
    def get_utc_time(self) -> Optional[Dict]:
        """GET /GetUtcTime - Get UTC time"""
        return self._get('/GetUtcTime')
