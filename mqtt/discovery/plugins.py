#!/usr/bin/env python3
"""
Discovery - Plugins Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class PluginsDiscovery(DiscoveryBase):
    """Plugins group - ALLE Entities"""
    
    GROUP_NAME = 'plugins'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registered_plugins = set()
    
    def register_all(self):
        """Register ALLE plugin entities"""
        
        # =====================================================================
        # GET /Plugins - Plugins List
        # =====================================================================
        self.sensor("plugins_count", "Installed Plugins", "plugins/count", "mdi:puzzle")
        self.sensor("plugins_active_count", "Active Plugins", "plugins/active_count", "mdi:puzzle-check")
        self.sensor("plugins_disabled_count", "Disabled Plugins", "plugins/disabled_count", "mdi:puzzle-remove")
        self.sensor("plugins_needs_update_count", "Plugins Need Update", "plugins/needs_update_count", "mdi:puzzle-plus")
        self.sensor("plugins_list", "Plugins List", "plugins/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /Repositories - Package Repositories
        # =====================================================================
        self.sensor("repositories_count", "Repositories Count", "plugins/repositories/count", "mdi:source-repository")
        self.sensor("repositories_list", "Repositories List", "plugins/repositories/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # POST /Repositories - Add Repository
        # =====================================================================
        self.button("add_repository", "Add Repository", "plugins/repositories/command", "add", "mdi:source-repository-multiple")
        
        # =====================================================================
        # DELETE /Repositories - Remove Repository
        # =====================================================================
        self.button("remove_repository", "Remove Repository", "plugins/repositories/command", "remove", "mdi:source-repository-minus")
        
        # =====================================================================
        # GET /Packages - Available Packages
        # =====================================================================
        self.sensor("packages_count", "Available Packages", "plugins/packages/count", "mdi:package-variant")
        self.sensor("packages_list", "Packages List", "plugins/packages/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # POST /Packages/Installed/{name} - Install Package
        # =====================================================================
        # Dynamic per package
        
        # =====================================================================
        # DELETE /Packages/Installing/{packageId} - Cancel Install
        # =====================================================================
        self.button("cancel_package_install", "Cancel Package Install", "plugins/packages/command", "cancel", "mdi:cancel")
        
        # =====================================================================
        # Control Buttons
        # =====================================================================
        self.button("plugins_update_all", "Update All Plugins", "plugins/command", "update_all", "mdi:update")
        
        return self.entity_count
    
    def register_plugin(self, plugin_id, plugin_name, version=None, description=None, status=None, can_uninstall=None, has_image=None):
        """Register ALLE Entities für ein spezifisches Plugin"""
        if plugin_id in self.registered_plugins:
            return 0
        
        safe_name = plugin_name.replace(" ", "_").replace("-", "_").lower()[:25]
        prefix = f"plugin_{safe_name}"
        base_topic = f"plugins/{plugin_id}"
        
        # =====================================================================
        # Plugin Basic Info
        # =====================================================================
        self.sensor(f"{prefix}_name", f"Plugin: {plugin_name}", f"{base_topic}/Name", "mdi:puzzle")
        self.sensor(f"{prefix}_id", f"{plugin_name} ID", f"{base_topic}/Id", "mdi:identifier")
        self.sensor(f"{prefix}_version", f"{plugin_name} Version", f"{base_topic}/Version", "mdi:tag")
        self.sensor(f"{prefix}_assembly_file_path", f"{plugin_name} Assembly Path", f"{base_topic}/AssemblyFilePath", "mdi:file")
        self.sensor(f"{prefix}_data_folder_path", f"{plugin_name} Data Path", f"{base_topic}/DataFolderPath", "mdi:folder")
        self.sensor(f"{prefix}_description", f"{plugin_name} Description", f"{base_topic}/Description", "mdi:text")
        self.sensor(f"{prefix}_status", f"{plugin_name} Status", f"{base_topic}/Status", "mdi:information")
        self.sensor(f"{prefix}_configuration_file_name", f"{plugin_name} Config File", f"{base_topic}/ConfigurationFileName", "mdi:file-cog")
        
        # =====================================================================
        # Plugin State
        # =====================================================================
        self.binary_sensor(f"{prefix}_is_active", f"{plugin_name} Is Active", f"{base_topic}/is_active", "mdi:puzzle-check")
        self.binary_sensor(f"{prefix}_can_uninstall", f"{plugin_name} Can Uninstall", f"{base_topic}/CanUninstall", "mdi:delete")
        self.binary_sensor(f"{prefix}_has_image", f"{plugin_name} Has Image", f"{base_topic}/HasImage", "mdi:image")
        self.binary_sensor(f"{prefix}_has_update", f"{plugin_name} Has Update", f"{base_topic}/has_update", "mdi:update")
        
        # =====================================================================
        # Plugin Configuration
        # =====================================================================
        self.sensor(f"{prefix}_configuration", f"{plugin_name} Configuration", f"{base_topic}/Configuration", "mdi:cog")
        
        # =====================================================================
        # Plugin Control Buttons
        # =====================================================================
        self.button(f"{prefix}_enable", f"Enable: {plugin_name}", f"{base_topic}/command", "enable", "mdi:puzzle-check")
        self.button(f"{prefix}_disable", f"Disable: {plugin_name}", f"{base_topic}/command", "disable", "mdi:puzzle-remove")
        self.button(f"{prefix}_uninstall", f"Uninstall: {plugin_name}", f"{base_topic}/command", "uninstall", "mdi:delete")
        self.button(f"{prefix}_update", f"Update: {plugin_name}", f"{base_topic}/command", "update", "mdi:update")
        
        self.registered_plugins.add(plugin_id)
        return self.entity_count
