#!/usr/bin/env python3
"""
Jellyfin API - Devices Group
Endpoints: 5
- Device management
"""

from typing import Optional, Dict
from .base import JellyfinAPIBase


class DevicesAPI(JellyfinAPIBase):
    """Devices API endpoints"""
    
    GROUP_NAME = 'devices'
    
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
