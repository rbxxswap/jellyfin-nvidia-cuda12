#!/usr/bin/env python3
"""
Jellyfin API - Plugins Group
Endpoints: 15
- Plugins, Packages, Repositories
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class PluginsAPI(JellyfinAPIBase):
    """Plugins API endpoints"""
    
    GROUP_NAME = 'plugins'
    
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
