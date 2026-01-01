#!/usr/bin/env python3
"""
Jellyfin API - Base Class
Provides core request methods for all API modules
"""

import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class JellyfinAPIBase:
    """Base class for Jellyfin API modules"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'X-Emby-Token': api_key,
            'Content-Type': 'application/json'
        }
    
    def _request(self, method: str, endpoint: str, 
                 params: Optional[Dict] = None,
                 json_data: Optional[Dict] = None,
                 data: Optional[Any] = None,
                 timeout: int = 10,
                 raw_response: bool = False) -> Optional[Any]:
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
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
        """GET request"""
        return self._request('GET', endpoint, params=params, **kwargs)
    
    def _post(self, endpoint: str, params: Optional[Dict] = None, 
              json_data: Optional[Dict] = None, **kwargs) -> Optional[Any]:
        """POST request"""
        return self._request('POST', endpoint, params=params, json_data=json_data, **kwargs)
    
    def _delete(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Optional[Any]:
        """DELETE request"""
        return self._request('DELETE', endpoint, params=params, **kwargs)
