#!/usr/bin/env python3
"""
Discovery - System Group - ALLE ENTITIES
Für jeden Endpoint alle möglichen Sensoren/Buttons
"""

from .base import DiscoveryBase


class SystemDiscovery(DiscoveryBase):
    """System group - ALLE Entities"""
    
    GROUP_NAME = 'system'
    
    def register_all(self):
        """Register ALLE system entities"""
        
        # =====================================================================
        # GET /System/Info - Server Info (ALLE Felder)
        # =====================================================================
        self.sensor("server_name", "Server Name", "system/ServerName", "mdi:server")
        self.sensor("server_id", "Server ID", "system/Id", "mdi:identifier")
        self.sensor("version", "Version", "system/Version", "mdi:tag")
        self.sensor("product_name", "Product Name", "system/ProductName", "mdi:package-variant")
        self.sensor("operating_system", "Operating System", "system/OperatingSystem", "mdi:linux")
        self.sensor("operating_system_display_name", "OS Display Name", "system/OperatingSystemDisplayName", "mdi:monitor")
        self.sensor("system_architecture", "Architecture", "system/SystemArchitecture", "mdi:chip")
        self.sensor("local_address", "Local Address", "system/LocalAddress", "mdi:ip-network")
        self.sensor("wan_address", "WAN Address", "system/WanAddress", "mdi:earth")
        self.sensor("program_data_path", "Program Data Path", "system/ProgramDataPath", "mdi:folder")
        self.sensor("web_path", "Web Path", "system/WebPath", "mdi:folder-network")
        self.sensor("items_by_name_path", "Items By Name Path", "system/ItemsByNamePath", "mdi:folder-account")
        self.sensor("cache_path", "Cache Path", "system/CachePath", "mdi:folder-cog")
        self.sensor("log_path", "Log Path", "system/LogPath", "mdi:folder-text")
        self.sensor("internal_metadata_path", "Internal Metadata Path", "system/InternalMetadataPath", "mdi:folder-information")
        self.sensor("transcoding_temp_path", "Transcoding Temp Path", "system/TranscodingTempPath", "mdi:folder-sync")
        self.binary_sensor("has_pending_restart", "Has Pending Restart", "system/HasPendingRestart", "mdi:restart-alert")
        self.binary_sensor("has_update_available", "Has Update Available", "system/HasUpdateAvailable", "mdi:update")
        self.binary_sensor("supports_library_monitor", "Supports Library Monitor", "system/SupportsLibraryMonitor", "mdi:monitor")
        self.sensor("encoder_location", "Encoder Location", "system/EncoderLocation", "mdi:video")
        self.binary_sensor("can_self_restart", "Can Self Restart", "system/CanSelfRestart", "mdi:restart")
        self.binary_sensor("can_launch_web_browser", "Can Launch Web Browser", "system/CanLaunchWebBrowser", "mdi:web")
        self.binary_sensor("startup_wizard_completed", "Startup Wizard Completed", "system/StartupWizardCompleted", "mdi:check-circle")
        self.sensor("http_server_port", "HTTP Server Port", "system/HttpServerPortNumber", "mdi:web")
        self.sensor("https_port", "HTTPS Port", "system/HttpsPortNumber", "mdi:web-check")
        self.binary_sensor("is_shutting_down", "Is Shutting Down", "system/IsShuttingDown", "mdi:power")
        self.sensor("package_name", "Package Name", "system/PackageName", "mdi:package")
        self.sensor("cast_receiver_application", "Cast Receiver App", "system/CastReceiverApplications", "mdi:cast")
        
        # =====================================================================
        # GET /System/Info/Public - Public System Info
        # =====================================================================
        self.sensor("public_local_address", "Public Local Address", "system/public/LocalAddress", "mdi:ip")
        self.sensor("public_server_name", "Public Server Name", "system/public/ServerName", "mdi:server")
        self.sensor("public_version", "Public Version", "system/public/Version", "mdi:tag")
        self.sensor("public_product_name", "Public Product Name", "system/public/ProductName", "mdi:package")
        self.sensor("public_operating_system", "Public OS", "system/public/OperatingSystem", "mdi:linux")
        self.sensor("public_server_id", "Public Server ID", "system/public/Id", "mdi:identifier")
        self.binary_sensor("public_startup_wizard_completed", "Public Startup Complete", "system/public/StartupWizardCompleted", "mdi:check")
        
        # =====================================================================
        # GET /System/Info/Storage - Storage Info
        # =====================================================================
        self.sensor("storage_total_size", "Storage Total Size", "system/storage/TotalSize", "mdi:harddisk", unit="GB")
        self.sensor("storage_free_space", "Storage Free Space", "system/storage/FreeSpace", "mdi:harddisk", unit="GB")
        self.sensor("storage_used_space", "Storage Used Space", "system/storage/UsedSpace", "mdi:harddisk", unit="GB")
        self.sensor("storage_used_percent", "Storage Used %", "system/storage/UsedPercent", "mdi:harddisk", unit="%")
        self.sensor("storage_path", "Storage Path", "system/storage/Path", "mdi:folder")
        
        # =====================================================================
        # GET /System/Ping - Ping
        # =====================================================================
        self.binary_sensor("ping", "Server Ping", "system/ping", "mdi:lan-connect", device_class="connectivity", payload_on="true", payload_off="false")
        self.binary_sensor("status", "Server Status", "status", device_class="connectivity", payload_on="online", payload_off="offline")
        
        # =====================================================================
        # POST /System/Restart - Restart Server
        # =====================================================================
        self.button("restart_server", "Restart Server", "system/command", "restart", "mdi:restart")
        
        # =====================================================================
        # POST /System/Shutdown - Shutdown Server
        # =====================================================================
        self.button("shutdown_server", "Shutdown Server", "system/command", "shutdown", "mdi:power")
        
        # =====================================================================
        # GET /System/Logs - Server Logs
        # =====================================================================
        self.sensor("logs_count", "Log Files Count", "system/logs/count", "mdi:file-document-multiple")
        self.sensor("logs_list", "Log Files List", "system/logs/list", "mdi:format-list-bulleted")
        self.sensor("logs_latest_name", "Latest Log Name", "system/logs/latest/name", "mdi:file-document")
        self.sensor("logs_latest_size", "Latest Log Size", "system/logs/latest/size", "mdi:file", unit="KB")
        self.sensor("logs_latest_date", "Latest Log Date", "system/logs/latest/date", "mdi:calendar")
        
        # =====================================================================
        # GET /System/Endpoint - Endpoint Info
        # =====================================================================
        self.binary_sensor("is_local", "Is Local", "system/endpoint/IsLocal", "mdi:lan")
        self.binary_sensor("is_in_network", "Is In Network", "system/endpoint/IsInNetwork", "mdi:lan-connect")
        
        # =====================================================================
        # GET /System/ActivityLog/Entries - Activity Log
        # =====================================================================
        self.sensor("activity_log_total", "Activity Log Total", "system/activity/TotalRecordCount", "mdi:clipboard-list")
        self.sensor("activity_log_latest_name", "Latest Activity", "system/activity/latest/Name", "mdi:clipboard-text")
        self.sensor("activity_log_latest_type", "Latest Activity Type", "system/activity/latest/Type", "mdi:tag")
        self.sensor("activity_log_latest_date", "Latest Activity Date", "system/activity/latest/Date", "mdi:calendar-clock")
        self.sensor("activity_log_latest_user", "Latest Activity User", "system/activity/latest/UserName", "mdi:account")
        self.sensor("activity_log_latest_severity", "Latest Activity Severity", "system/activity/latest/Severity", "mdi:alert")
        self.sensor("activity_log_latest_short_overview", "Latest Activity Overview", "system/activity/latest/ShortOverview", "mdi:text")
        
        # =====================================================================
        # GET /System/Configuration - Server Configuration
        # =====================================================================
        self.binary_sensor("config_enable_upnp", "Config: Enable UPnP", "system/config/EnableUPnP", "mdi:network")
        self.sensor("config_public_port", "Config: Public Port", "system/config/PublicPort", "mdi:web")
        self.sensor("config_public_https_port", "Config: Public HTTPS Port", "system/config/PublicHttpsPort", "mdi:web-check")
        self.sensor("config_server_name", "Config: Server Name", "system/config/ServerName", "mdi:server")
        self.binary_sensor("config_enable_https", "Config: Enable HTTPS", "system/config/EnableHttps", "mdi:shield-check")
        self.binary_sensor("config_enable_normalized_item_by_name_ids", "Config: Normalized IDs", "system/config/EnableNormalizedItemByNameIds", "mdi:identifier")
        self.sensor("config_certificate_path", "Config: Certificate Path", "system/config/CertificatePath", "mdi:certificate")
        self.sensor("config_certificate_password", "Config: Certificate Password Set", "system/config/CertificatePasswordSet", "mdi:key")
        self.binary_sensor("config_is_port_authorized", "Config: Port Authorized", "system/config/IsPortAuthorized", "mdi:check-network")
        self.binary_sensor("config_quick_connect_available", "Config: Quick Connect", "system/config/QuickConnectAvailable", "mdi:qrcode")
        self.binary_sensor("config_enable_case_sensitive_item_ids", "Config: Case Sensitive IDs", "system/config/EnableCaseSensitiveItemIds", "mdi:alphabetical")
        self.binary_sensor("config_disable_live_tv_channel_user_data_name", "Config: Disable LiveTV User Data", "system/config/DisableLiveTvChannelUserDataName", "mdi:television")
        self.sensor("config_metadata_path", "Config: Metadata Path", "system/config/MetadataPath", "mdi:folder-information")
        self.sensor("config_metadata_network_path", "Config: Metadata Network Path", "system/config/MetadataNetworkPath", "mdi:folder-network")
        self.sensor("config_preferred_metadata_language", "Config: Metadata Language", "system/config/PreferredMetadataLanguage", "mdi:translate")
        self.sensor("config_metadata_country_code", "Config: Metadata Country", "system/config/MetadataCountryCode", "mdi:earth")
        self.sensor("config_library_scan_fanout_concurrency", "Config: Scan Concurrency", "system/config/LibraryScanFanoutConcurrency", "mdi:numeric")
        self.sensor("config_library_metadata_refresh_concurrency", "Config: Refresh Concurrency", "system/config/LibraryMetadataRefreshConcurrency", "mdi:numeric")
        self.binary_sensor("config_remove_old_plugins", "Config: Remove Old Plugins", "system/config/RemoveOldPlugins", "mdi:puzzle-remove")
        self.binary_sensor("config_allow_client_log_upload", "Config: Allow Log Upload", "system/config/AllowClientLogUpload", "mdi:upload")
        
        # =====================================================================
        # GET /GetUtcTime - UTC Time
        # =====================================================================
        self.sensor("utc_time", "UTC Time", "system/utc_time", "mdi:clock-outline")
        self.sensor("local_time", "Local Time", "system/local_time", "mdi:clock")
        
        return self.entity_count
