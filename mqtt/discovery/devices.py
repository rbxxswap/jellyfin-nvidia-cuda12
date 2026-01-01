#!/usr/bin/env python3
"""
Discovery - Devices Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class DevicesDiscovery(DiscoveryBase):
    """Devices group - ALLE Entities"""
    
    GROUP_NAME = 'devices'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registered_devices = set()
    
    def register_all(self):
        """Register ALLE device entities"""
        
        # =====================================================================
        # GET /Devices - Device List
        # =====================================================================
        self.sensor("devices_count", "Devices Count", "devices/count", "mdi:devices")
        self.sensor("devices_total_record_count", "Devices Total", "devices/TotalRecordCount", "mdi:devices")
        self.sensor("devices_start_index", "Devices Start Index", "devices/StartIndex", "mdi:numeric")
        self.sensor("devices_list", "Devices List", "devices/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /Devices/Info - Device Info (single)
        # =====================================================================
        # Dynamic per device
        
        # =====================================================================
        # GET /Devices/Options - Device Options
        # =====================================================================
        self.sensor("device_options_custom_name", "Device Options Custom Name", "devices/options/CustomName", "mdi:text")
        
        # =====================================================================
        # POST /Devices/Options - Update Device Options
        # =====================================================================
        # Dynamic per device
        
        # =====================================================================
        # DELETE /Devices - Delete Device
        # =====================================================================
        self.button("delete_all_devices", "Delete All Devices", "devices/command", "delete_all", "mdi:delete-sweep")
        
        return self.entity_count
    
    def register_device(self, device_id, device_name, app_name=None, app_version=None, last_user_name=None):
        """Register ALLE Entities für ein spezifisches Device"""
        if device_id in self.registered_devices:
            return 0
        
        safe_name = device_name.replace(" ", "_").replace("-", "_").lower()[:20]
        prefix = f"device_{safe_name}"
        base_topic = f"devices/{device_id}"
        
        # =====================================================================
        # Device Basic Info
        # =====================================================================
        self.sensor(f"{prefix}_name", f"Device: {device_name}", f"{base_topic}/Name", "mdi:devices")
        self.sensor(f"{prefix}_id", f"{device_name} ID", f"{base_topic}/Id", "mdi:identifier")
        self.sensor(f"{prefix}_custom_name", f"{device_name} Custom Name", f"{base_topic}/CustomName", "mdi:text")
        self.sensor(f"{prefix}_app_name", f"{device_name} App Name", f"{base_topic}/AppName", "mdi:application")
        self.sensor(f"{prefix}_app_version", f"{device_name} App Version", f"{base_topic}/AppVersion", "mdi:tag")
        self.sensor(f"{prefix}_last_user_name", f"{device_name} Last User", f"{base_topic}/LastUserName", "mdi:account")
        self.sensor(f"{prefix}_last_user_id", f"{device_name} Last User ID", f"{base_topic}/LastUserId", "mdi:identifier")
        self.sensor(f"{prefix}_date_last_activity", f"{device_name} Last Activity", f"{base_topic}/DateLastActivity", "mdi:clock")
        
        # =====================================================================
        # Device Capabilities
        # =====================================================================
        self.sensor(f"{prefix}_icon_url", f"{device_name} Icon URL", f"{base_topic}/IconUrl", "mdi:image")
        
        # =====================================================================
        # Device Control Buttons
        # =====================================================================
        self.button(f"{prefix}_delete", f"Delete: {device_name}", f"{base_topic}/command", "delete", "mdi:delete")
        
        self.registered_devices.add(device_id)
        return self.entity_count
