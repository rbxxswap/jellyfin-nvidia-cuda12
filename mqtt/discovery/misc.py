#!/usr/bin/env python3
"""
Discovery - Misc Group - ALLE ENTITIES (60 Endpoints)
"""

from .base import DiscoveryBase


class MiscDiscovery(DiscoveryBase):
    """Misc group - ALLE Entities"""
    
    GROUP_NAME = 'misc'
    
    def register_all(self):
        """Register ALLE misc entities"""
        
        # =====================================================================
        # SUBTITLES
        # =====================================================================
        # GET /FallbackFont/Fonts - Fallback Fonts
        self.sensor("fallback_fonts_count", "Fallback Fonts Count", "misc/fonts/count", "mdi:format-font")
        self.sensor("fallback_fonts_list", "Fallback Fonts List", "misc/fonts/list", "mdi:format-list-bulleted")
        
        # GET /Providers/Subtitles/Subtitles/{itemId} - Subtitle Providers
        self.sensor("subtitle_providers_count", "Subtitle Providers Count", "misc/subtitle_providers/count", "mdi:subtitles")
        
        # POST /Videos/{itemId}/Subtitles - Upload Subtitle
        self.button("upload_subtitle", "Upload Subtitle", "misc/subtitles/command", "upload", "mdi:subtitles")
        
        # DELETE /Videos/{itemId}/Subtitles/{index} - Delete Subtitle
        self.button("delete_subtitle", "Delete Subtitle", "misc/subtitles/command", "delete", "mdi:close")
        
        # POST /Items/{itemId}/RemoteSearch/Subtitles/{language} - Search Subtitles
        self.button("search_subtitles", "Search Subtitles", "misc/subtitles/command", "search", "mdi:magnify")
        
        # POST /Items/{itemId}/RemoteSearch/Subtitles/Download - Download Subtitle
        self.button("download_subtitle", "Download Subtitle", "misc/subtitles/command", "download", "mdi:download")
        
        # =====================================================================
        # CHANNELS
        # =====================================================================
        # GET /Channels - Channels
        self.sensor("channels_count", "Channels Count", "misc/channels/count", "mdi:youtube-tv")
        self.sensor("channels_total_record_count", "Channels Total", "misc/channels/TotalRecordCount", "mdi:youtube-tv")
        self.sensor("channels_list", "Channels List", "misc/channels/list", "mdi:format-list-bulleted")
        
        # GET /Channels/{channelId}/Features - Channel Features
        self.sensor("channel_features_count", "Channel Features Count", "misc/channel_features/count", "mdi:star")
        
        # GET /Channels/{channelId}/Items - Channel Items
        self.sensor("channel_items_count", "Channel Items Count", "misc/channel_items/count", "mdi:folder-play")
        
        # GET /Channels/Features - All Channel Features
        self.sensor("all_channel_features_count", "All Channel Features Count", "misc/all_channel_features/count", "mdi:star-box-multiple")
        
        # =====================================================================
        # ENVIRONMENT / DRIVES
        # =====================================================================
        # GET /Environment/Drives - Drives
        self.sensor("drives_count", "Drives Count", "misc/drives/count", "mdi:harddisk")
        self.sensor("drives_list", "Drives List", "misc/drives/list", "mdi:format-list-bulleted")
        
        # Drive details (first 10)
        for i in range(10):
            self.sensor(f"drive_{i}_name", f"Drive {i+1} Name", f"misc/drives/{i}/Name", "mdi:harddisk")
            self.sensor(f"drive_{i}_path", f"Drive {i+1} Path", f"misc/drives/{i}/Path", "mdi:folder")
            self.sensor(f"drive_{i}_type", f"Drive {i+1} Type", f"misc/drives/{i}/Type", "mdi:tag")
        
        # GET /Environment/DirectoryContents - Directory Contents
        self.sensor("directory_contents_count", "Directory Contents Count", "misc/directory_contents/count", "mdi:folder-open")
        
        # GET /Environment/ParentPath - Parent Path
        self.sensor("parent_path", "Parent Path", "misc/parent_path", "mdi:folder-arrow-up")
        
        # GET /Environment/DefaultDirectoryBrowser - Default Browser
        self.sensor("default_directory_browser", "Default Directory Browser", "misc/default_browser", "mdi:folder")
        
        # POST /Environment/ValidatePath - Validate Path
        self.button("validate_path", "Validate Path", "misc/command", "validate_path", "mdi:folder-check")
        
        # GET /System/Drives - Network Drives
        self.sensor("network_drives_count", "Network Drives Count", "misc/network_drives/count", "mdi:nas")
        
        # =====================================================================
        # QUICK CONNECT
        # =====================================================================
        # GET /QuickConnect/Enabled - Quick Connect Enabled
        self.binary_sensor("quick_connect_enabled", "Quick Connect Enabled", "misc/quick_connect/enabled", "mdi:qrcode")
        
        # GET /QuickConnect/State - Quick Connect State
        self.sensor("quick_connect_state", "Quick Connect State", "misc/quick_connect/state", "mdi:qrcode")
        
        # POST /QuickConnect/Initiate - Initiate Quick Connect
        self.button("quick_connect_initiate", "Initiate Quick Connect", "misc/quick_connect/command", "initiate", "mdi:qrcode-scan")
        
        # POST /QuickConnect/Authorize - Authorize Quick Connect
        self.button("quick_connect_authorize", "Authorize Quick Connect", "misc/quick_connect/command", "authorize", "mdi:check")
        
        # POST /QuickConnect/Activate - Activate Quick Connect
        self.button("quick_connect_activate", "Activate Quick Connect", "misc/quick_connect/command", "activate", "mdi:power")
        
        # POST /QuickConnect/Deactivate - Deactivate Quick Connect
        self.button("quick_connect_deactivate", "Deactivate Quick Connect", "misc/quick_connect/command", "deactivate", "mdi:power-off")
        
        # POST /QuickConnect/Connect - Connect Quick Connect
        self.button("quick_connect_connect", "Connect Quick Connect", "misc/quick_connect/command", "connect", "mdi:lan-connect")
        
        # GET /QuickConnect/Available - Quick Connect Available
        self.binary_sensor("quick_connect_available", "Quick Connect Available", "misc/quick_connect/available", "mdi:qrcode")

        
        # =====================================================================
        # LOCALIZATION
        # =====================================================================
        # GET /Localization/Countries - Countries
        self.sensor("countries_count", "Countries Count", "misc/countries/count", "mdi:earth")
        self.sensor("countries_list", "Countries List", "misc/countries/list", "mdi:format-list-bulleted")
        
        # GET /Localization/Cultures - Cultures
        self.sensor("cultures_count", "Cultures Count", "misc/cultures/count", "mdi:translate")
        self.sensor("cultures_list", "Cultures List", "misc/cultures/list", "mdi:format-list-bulleted")
        
        # GET /Localization/Options - Localization Options
        self.sensor("localization_options_count", "Localization Options Count", "misc/localization/count", "mdi:translate")
        
        # GET /Localization/ParentalRatings - Parental Ratings
        self.sensor("parental_ratings_count", "Parental Ratings Count", "misc/parental_ratings/count", "mdi:account-child")
        self.sensor("parental_ratings_list", "Parental Ratings List", "misc/parental_ratings/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # BRANDING
        # =====================================================================
        # GET /Branding/Configuration - Branding Configuration
        self.sensor("branding_login_disclaimer", "Branding Login Disclaimer", "misc/branding/LoginDisclaimer", "mdi:text")
        self.sensor("branding_custom_css", "Branding Custom CSS", "misc/branding/CustomCss", "mdi:language-css3")
        self.sensor("branding_custom_css_length", "Custom CSS Length", "misc/branding/CustomCssLength", "mdi:counter")
        self.binary_sensor("branding_splashscreen_enabled", "Splashscreen Enabled", "misc/branding/SplashscreenEnabled", "mdi:image")
        
        # GET /Branding/Css - Branding CSS
        self.sensor("branding_css", "Branding CSS", "misc/branding/css", "mdi:language-css3")
        
        # GET /Branding/Css.css - Branding CSS File
        self.sensor("branding_css_file", "Branding CSS File", "misc/branding/css_file", "mdi:file")
        
        # =====================================================================
        # API KEYS
        # =====================================================================
        # GET /Auth/Keys - API Keys
        self.sensor("api_keys_count", "API Keys Count", "misc/api_keys/count", "mdi:key-chain")
        self.sensor("api_keys_list", "API Keys List", "misc/api_keys/list", "mdi:format-list-bulleted")
        
        # API Key details (first 5)
        for i in range(5):
            self.sensor(f"api_key_{i}_app_name", f"API Key {i+1} App", f"misc/api_keys/{i}/AppName", "mdi:key")
            self.sensor(f"api_key_{i}_access_token", f"API Key {i+1} Token", f"misc/api_keys/{i}/AccessToken", "mdi:key-variant")
            self.sensor(f"api_key_{i}_date_created", f"API Key {i+1} Created", f"misc/api_keys/{i}/DateCreated", "mdi:calendar")
            self.sensor(f"api_key_{i}_date_last_activity", f"API Key {i+1} Last Activity", f"misc/api_keys/{i}/DateLastActivity", "mdi:clock")
        
        # POST /Auth/Keys - Create API Key
        self.button("create_api_key", "Create API Key", "misc/api_keys/command", "create", "mdi:key-plus")
        
        # DELETE /Auth/Keys/{key} - Delete API Key
        self.button("delete_api_key", "Delete API Key", "misc/api_keys/command", "delete", "mdi:key-remove")
        
        # =====================================================================
        # DASHBOARD / CONFIG PAGES
        # =====================================================================
        # GET /web/ConfigurationPages - Configuration Pages
        self.sensor("config_pages_count", "Config Pages Count", "misc/config_pages/count", "mdi:view-dashboard")
        self.sensor("config_pages_list", "Config Pages List", "misc/config_pages/list", "mdi:format-list-bulleted")
        
        # GET /Dashboard/ConfigurationPages - Dashboard Config Pages
        self.sensor("dashboard_config_pages_count", "Dashboard Config Pages Count", "misc/dashboard_config_pages/count", "mdi:view-dashboard-variant")
        
        # =====================================================================
        # NOTIFICATIONS
        # =====================================================================
        # GET /Notifications/Services - Notification Services
        self.sensor("notification_services_count", "Notification Services Count", "misc/notification_services/count", "mdi:bell")
        self.sensor("notification_services_list", "Notification Services List", "misc/notification_services/list", "mdi:format-list-bulleted")
        
        # GET /Notifications/Types - Notification Types
        self.sensor("notification_types_count", "Notification Types Count", "misc/notification_types/count", "mdi:bell-badge")
        
        # GET /Notifications/{userId} - User Notifications
        self.sensor("user_notifications_count", "User Notifications Count", "misc/user_notifications/count", "mdi:bell-ring")
        self.sensor("user_notifications_unread", "Unread Notifications", "misc/user_notifications/unread", "mdi:bell-alert")
        
        # POST /Notifications/Admin - Send Admin Notification
        self.button("send_admin_notification", "Send Admin Notification", "misc/notifications/command", "send_admin", "mdi:bell-plus")
        
        # POST /Notifications/{userId}/Read - Mark Notifications Read
        self.button("mark_notifications_read", "Mark Notifications Read", "misc/notifications/command", "mark_read", "mdi:bell-check")
        
        # POST /Notifications/{userId}/Unread - Mark Notifications Unread
        self.button("mark_notifications_unread", "Mark Notifications Unread", "misc/notifications/command", "mark_unread", "mdi:bell-minus")
        
        # =====================================================================
        # ENCODINGS
        # =====================================================================
        # GET /Encoding/CodecInformation/Video - Video Codec Info
        self.sensor("video_codec_info", "Video Codec Info", "misc/video_codec_info", "mdi:video")
        
        # GET /Encoding/MediaInfo/Audio - Audio Media Info
        self.sensor("audio_media_info", "Audio Media Info", "misc/audio_media_info", "mdi:volume-high")
        
        # GET /Encoding/MediaInfo/Video - Video Media Info
        self.sensor("video_media_info", "Video Media Info", "misc/video_media_info", "mdi:video")
        
        # GET /Encoding/CodecTitanium/Codecs - Encodings/Codecs
        self.sensor("encodings_count", "Encodings Count", "misc/encodings/count", "mdi:alphabetical")
        
        # =====================================================================
        # DLNA
        # =====================================================================
        # GET /Dlna/ProfileInfos - DLNA Profile Infos
        self.sensor("dlna_profile_infos_count", "DLNA Profile Infos Count", "misc/dlna/profile_infos/count", "mdi:dlna")
        self.sensor("dlna_profile_infos_list", "DLNA Profile Infos List", "misc/dlna/profile_infos/list", "mdi:format-list-bulleted")
        
        # GET /Dlna/Profiles - DLNA Profiles
        self.sensor("dlna_profiles_count", "DLNA Profiles Count", "misc/dlna/profiles/count", "mdi:dlna")
        
        # GET /Dlna/Profiles/Default - Default DLNA Profile
        self.sensor("dlna_default_profile", "DLNA Default Profile", "misc/dlna/default_profile", "mdi:dlna")
        
        # POST /Dlna/Profiles - Create DLNA Profile
        self.button("create_dlna_profile", "Create DLNA Profile", "misc/dlna/command", "create", "mdi:plus")
        
        # DELETE /Dlna/Profiles/{profileId} - Delete DLNA Profile
        self.button("delete_dlna_profile", "Delete DLNA Profile", "misc/dlna/command", "delete", "mdi:delete")

        
        # =====================================================================
        # DISPLAY PREFERENCES
        # =====================================================================
        # GET /DisplayPreferences/{displayPreferencesId} - Display Preferences
        self.sensor("display_preferences_id", "Display Preferences ID", "misc/display_preferences/Id", "mdi:monitor")
        self.sensor("display_preferences_view_type", "Display View Type", "misc/display_preferences/ViewType", "mdi:view-grid")
        self.sensor("display_preferences_sort_by", "Display Sort By", "misc/display_preferences/SortBy", "mdi:sort")
        self.sensor("display_preferences_sort_order", "Display Sort Order", "misc/display_preferences/SortOrder", "mdi:sort-ascending")
        self.sensor("display_preferences_index_by", "Display Index By", "misc/display_preferences/IndexBy", "mdi:format-list-numbered")
        self.binary_sensor("display_preferences_remember_indexing", "Remember Indexing", "misc/display_preferences/RememberIndexing", "mdi:memory")
        self.binary_sensor("display_preferences_remember_sorting", "Remember Sorting", "misc/display_preferences/RememberSorting", "mdi:memory")
        self.sensor("display_preferences_scroll_direction", "Scroll Direction", "misc/display_preferences/ScrollDirection", "mdi:arrow-up-down")
        self.binary_sensor("display_preferences_show_backdrop", "Show Backdrop", "misc/display_preferences/ShowBackdrop", "mdi:image")
        self.binary_sensor("display_preferences_show_sidebar", "Show Sidebar", "misc/display_preferences/ShowSidebar", "mdi:page-layout-sidebar-left")
        self.sensor("display_preferences_client", "Display Client", "misc/display_preferences/Client", "mdi:application")
        
        # POST /DisplayPreferences/{displayPreferencesId} - Update Display Preferences
        self.button("update_display_preferences", "Update Display Preferences", "misc/display_preferences/command", "update", "mdi:content-save")
        
        # =====================================================================
        # ITEM COUNTS (MISC)
        # =====================================================================
        self.sensor("item_counts_movie", "Item Count: Movies", "misc/item_counts/MovieCount", "mdi:movie")
        self.sensor("item_counts_series", "Item Count: Series", "misc/item_counts/SeriesCount", "mdi:television")
        self.sensor("item_counts_episode", "Item Count: Episodes", "misc/item_counts/EpisodeCount", "mdi:filmstrip")
        self.sensor("item_counts_artist", "Item Count: Artists", "misc/item_counts/ArtistCount", "mdi:account-music")
        self.sensor("item_counts_program", "Item Count: Programs", "misc/item_counts/ProgramCount", "mdi:television-guide")
        self.sensor("item_counts_trailer", "Item Count: Trailers", "misc/item_counts/TrailerCount", "mdi:movie-roll")
        self.sensor("item_counts_song", "Item Count: Songs", "misc/item_counts/SongCount", "mdi:music")
        self.sensor("item_counts_album", "Item Count: Albums", "misc/item_counts/AlbumCount", "mdi:album")
        self.sensor("item_counts_music_video", "Item Count: Music Videos", "misc/item_counts/MusicVideoCount", "mdi:music-box")
        self.sensor("item_counts_box_set", "Item Count: Box Sets", "misc/item_counts/BoxSetCount", "mdi:folder-star")
        self.sensor("item_counts_book", "Item Count: Books", "misc/item_counts/BookCount", "mdi:book")
        self.sensor("item_counts_item", "Item Count: Total", "misc/item_counts/ItemCount", "mdi:database")
        
        # =====================================================================
        # STARTUP INFO
        # =====================================================================
        # GET /Startup/Configuration - Startup Configuration
        self.sensor("startup_ui_culture", "Startup UI Culture", "misc/startup/UICulture", "mdi:translate")
        self.sensor("startup_metadata_country_code", "Startup Metadata Country", "misc/startup/MetadataCountryCode", "mdi:earth")
        self.sensor("startup_preferred_metadata_language", "Startup Metadata Language", "misc/startup/PreferredMetadataLanguage", "mdi:translate")
        
        # GET /Startup/FirstUser - First User
        self.sensor("startup_first_user", "Startup First User", "misc/startup/first_user", "mdi:account")
        
        # GET /Startup/User - Startup User
        self.sensor("startup_user_name", "Startup User Name", "misc/startup/user/Name", "mdi:account")
        self.sensor("startup_user_password", "Startup User Has Password", "misc/startup/user/Password", "mdi:lock")
        
        # POST /Startup/Complete - Complete Startup Wizard
        self.button("complete_startup", "Complete Startup Wizard", "misc/startup/command", "complete", "mdi:check-circle")
        
        # POST /Startup/Configuration - Update Startup Config
        self.button("update_startup_config", "Update Startup Config", "misc/startup/command", "update", "mdi:content-save")
        
        # POST /Startup/FirstUser - Set First User
        self.button("set_first_user", "Set First User", "misc/startup/command", "set_first_user", "mdi:account-plus")
        
        # POST /Startup/User - Update Startup User
        self.button("update_startup_user", "Update Startup User", "misc/startup/command", "update_user", "mdi:account-edit")
        
        # =====================================================================
        # CLIENT LOG
        # =====================================================================
        # POST /ClientLog/Document - Upload Client Log
        self.button("upload_client_log", "Upload Client Log", "misc/client_log/command", "upload", "mdi:upload")
        
        # =====================================================================
        # DYNAMIC HLS
        # =====================================================================
        # GET /Audio/{itemId}/hls/{segmentId}/stream.mp3 - HLS Audio
        self.sensor("hls_audio_active", "HLS Audio Active", "misc/hls/audio_active", "mdi:music")
        
        # GET /Videos/{itemId}/hls/{playlistId}/stream.m3u8 - HLS Video Playlist
        self.sensor("hls_video_active", "HLS Video Active", "misc/hls/video_active", "mdi:video")
        
        # GET /Videos/{itemId}/hls/{playlistId}/{segmentId}.{segmentContainer} - HLS Segment
        self.sensor("hls_segments_count", "HLS Segments Count", "misc/hls/segments_count", "mdi:filmstrip-box-multiple")
        
        # =====================================================================
        # UNIVERSAL AUDIO/VIDEO
        # =====================================================================
        self.sensor("universal_audio_active", "Universal Audio Active", "misc/universal/audio_active", "mdi:music")
        self.sensor("universal_video_active", "Universal Video Active", "misc/universal/video_active", "mdi:video")
        
        # =====================================================================
        # TRICKPLAY (for seeking thumbnails)
        # =====================================================================
        self.sensor("trickplay_enabled", "Trickplay Enabled", "misc/trickplay/enabled", "mdi:image-multiple")
        
        # =====================================================================
        # GPU / HARDWARE (NVIDIA)
        # =====================================================================
        self.sensor("gpu_name", "GPU Name", "gpu/name", "mdi:expansion-card")
        self.sensor("gpu_driver_version", "GPU Driver Version", "gpu/driver_version", "mdi:tag")
        self.sensor("gpu_cuda_version", "GPU CUDA Version", "gpu/cuda_version", "mdi:tag")
        self.sensor("gpu_utilization", "GPU Utilization", "gpu/utilization", "mdi:gauge", unit="%")
        self.sensor("gpu_temperature", "GPU Temperature", "gpu/temperature", "mdi:thermometer", unit="°C", device_class="temperature")
        self.sensor("gpu_fan_speed", "GPU Fan Speed", "gpu/fan_speed", "mdi:fan", unit="%")
        self.sensor("gpu_memory_total", "GPU Memory Total", "gpu/memory_total", "mdi:memory", unit="MB")
        self.sensor("gpu_memory_used", "GPU Memory Used", "gpu/memory_used", "mdi:memory", unit="MB")
        self.sensor("gpu_memory_free", "GPU Memory Free", "gpu/memory_free", "mdi:memory", unit="MB")
        self.sensor("gpu_memory_percent", "GPU Memory %", "gpu/memory_percent", "mdi:memory", unit="%")
        self.sensor("gpu_encoder_utilization", "GPU Encoder", "gpu/encoder", "mdi:video", unit="%")
        self.sensor("gpu_decoder_utilization", "GPU Decoder", "gpu/decoder", "mdi:video-outline", unit="%")
        self.sensor("gpu_power_draw", "GPU Power Draw", "gpu/power", "mdi:flash", unit="W", device_class="power")
        self.sensor("gpu_power_limit", "GPU Power Limit", "gpu/power_limit", "mdi:flash-outline", unit="W")
        self.sensor("gpu_clock_graphics", "GPU Graphics Clock", "gpu/clock_graphics", "mdi:speedometer", unit="MHz")
        self.sensor("gpu_clock_memory", "GPU Memory Clock", "gpu/clock_memory", "mdi:speedometer", unit="MHz")
        self.sensor("gpu_clock_sm", "GPU SM Clock", "gpu/clock_sm", "mdi:speedometer", unit="MHz")
        self.sensor("gpu_pcie_link_gen", "GPU PCIe Gen", "gpu/pcie_gen", "mdi:expansion-card-variant")
        self.sensor("gpu_pcie_link_width", "GPU PCIe Width", "gpu/pcie_width", "mdi:expansion-card-variant")
        self.sensor("gpu_processes_count", "GPU Processes Count", "gpu/processes_count", "mdi:application")
        
        # =====================================================================
        # CONTAINER STATS
        # =====================================================================
        self.sensor("container_name", "Container Name", "container/name", "mdi:docker")
        self.sensor("container_id", "Container ID", "container/id", "mdi:identifier")
        self.sensor("container_status", "Container Status", "container/status", "mdi:checkbox-marked-circle")
        self.sensor("container_uptime", "Container Uptime", "container/uptime", "mdi:clock-outline")
        self.sensor("container_cpu_percent", "Container CPU %", "container/cpu_percent", "mdi:cpu-64-bit", unit="%")
        self.sensor("container_memory_usage", "Container Memory Usage", "container/memory_used", "mdi:memory", unit="MB")
        self.sensor("container_memory_limit", "Container Memory Limit", "container/memory_limit", "mdi:memory", unit="MB")
        self.sensor("container_memory_percent", "Container Memory %", "container/memory_percent", "mdi:memory", unit="%")
        self.sensor("container_network_rx_bytes", "Container Network RX", "container/network_rx", "mdi:download", unit="B")
        self.sensor("container_network_tx_bytes", "Container Network TX", "container/network_tx", "mdi:upload", unit="B")
        self.sensor("container_network_rx_rate", "Container Network RX Rate", "container/network_rx_rate", "mdi:download-network", unit="B/s")
        self.sensor("container_network_tx_rate", "Container Network TX Rate", "container/network_tx_rate", "mdi:upload-network", unit="B/s")
        self.sensor("container_block_read", "Container Block Read", "container/block_read", "mdi:harddisk", unit="B")
        self.sensor("container_block_write", "Container Block Write", "container/block_write", "mdi:harddisk", unit="B")
        self.sensor("container_pids", "Container PIDs", "container/pids", "mdi:application-cog")
        
        return self.entity_count
