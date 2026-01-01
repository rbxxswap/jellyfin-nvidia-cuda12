#!/usr/bin/env python3
"""
Discovery - LiveTV Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class LiveTVDiscovery(DiscoveryBase):
    """LiveTV group - ALLE Entities"""
    
    GROUP_NAME = 'livetv'
    
    def register_all(self):
        """Register ALLE livetv entities"""
        
        # =====================================================================
        # GET /LiveTv/Info - LiveTV Info
        # =====================================================================
        self.binary_sensor("livetv_is_enabled", "LiveTV Is Enabled", "livetv/info/IsEnabled", "mdi:television-classic")
        self.sensor("livetv_services_count", "LiveTV Services Count", "livetv/info/Services/count", "mdi:server")
        self.sensor("livetv_enabled_users_count", "LiveTV Enabled Users", "livetv/info/EnabledUsers/count", "mdi:account-multiple")
        
        # =====================================================================
        # GET /LiveTv/Channels - Channels
        # =====================================================================
        self.sensor("livetv_channels_count", "LiveTV Channels Count", "livetv/channels/count", "mdi:television")
        self.sensor("livetv_channels_total_record_count", "LiveTV Channels Total", "livetv/channels/TotalRecordCount", "mdi:television")
        self.sensor("livetv_channels_list", "LiveTV Channels List", "livetv/channels/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /LiveTv/Recordings - Recordings
        # =====================================================================
        self.sensor("livetv_recordings_count", "LiveTV Recordings Count", "livetv/recordings/count", "mdi:record-rec")
        self.sensor("livetv_recordings_total_record_count", "LiveTV Recordings Total", "livetv/recordings/TotalRecordCount", "mdi:record-rec")
        self.sensor("livetv_recordings_list", "LiveTV Recordings List", "livetv/recordings/list", "mdi:format-list-bulleted")
        self.sensor("livetv_recordings_size", "LiveTV Recordings Size", "livetv/recordings/size", "mdi:harddisk", unit="GB")
        
        # =====================================================================
        # GET /LiveTv/Recordings/Groups - Recording Groups
        # =====================================================================
        self.sensor("livetv_recording_groups_count", "Recording Groups Count", "livetv/recording_groups/count", "mdi:folder-play")
        self.sensor("livetv_recording_groups_list", "Recording Groups List", "livetv/recording_groups/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /LiveTv/Recordings/Folders - Recording Folders
        # =====================================================================
        self.sensor("livetv_recording_folders_count", "Recording Folders Count", "livetv/recording_folders/count", "mdi:folder")
        
        # =====================================================================
        # GET /LiveTv/Recordings/Series - Recording Series
        # =====================================================================
        self.sensor("livetv_recording_series_count", "Recording Series Count", "livetv/recording_series/count", "mdi:television-classic")
        
        # =====================================================================
        # GET /LiveTv/Timers - Timers
        # =====================================================================
        self.sensor("livetv_timers_count", "LiveTV Timers Count", "livetv/timers/count", "mdi:timer")
        self.sensor("livetv_timers_list", "LiveTV Timers List", "livetv/timers/list", "mdi:format-list-bulleted")
        
        # Timer details (first 5)
        for i in range(5):
            self.sensor(f"livetv_timer_{i}_name", f"Timer {i+1} Name", f"livetv/timers/{i}/Name", "mdi:timer")
            self.sensor(f"livetv_timer_{i}_channel", f"Timer {i+1} Channel", f"livetv/timers/{i}/ChannelName", "mdi:television")
            self.sensor(f"livetv_timer_{i}_start", f"Timer {i+1} Start", f"livetv/timers/{i}/StartDate", "mdi:clock-start")
            self.sensor(f"livetv_timer_{i}_end", f"Timer {i+1} End", f"livetv/timers/{i}/EndDate", "mdi:clock-end")
            self.sensor(f"livetv_timer_{i}_status", f"Timer {i+1} Status", f"livetv/timers/{i}/Status", "mdi:information")
        
        # =====================================================================
        # POST /LiveTv/Timers - Create Timer
        # =====================================================================
        self.button("livetv_create_timer", "Create Timer", "livetv/timers/command", "create", "mdi:timer-plus")
        
        # =====================================================================
        # DELETE /LiveTv/Timers/{timerId} - Delete Timer
        # =====================================================================
        # Dynamic per timer
        
        # =====================================================================
        # GET /LiveTv/SeriesTimers - Series Timers
        # =====================================================================
        self.sensor("livetv_series_timers_count", "Series Timers Count", "livetv/series_timers/count", "mdi:timer-sync")
        self.sensor("livetv_series_timers_list", "Series Timers List", "livetv/series_timers/list", "mdi:format-list-bulleted")
        
        # Series Timer details (first 5)
        for i in range(5):
            self.sensor(f"livetv_series_timer_{i}_name", f"Series Timer {i+1} Name", f"livetv/series_timers/{i}/Name", "mdi:timer-sync")
            self.sensor(f"livetv_series_timer_{i}_channel", f"Series Timer {i+1} Channel", f"livetv/series_timers/{i}/ChannelName", "mdi:television")
            self.binary_sensor(f"livetv_series_timer_{i}_record_any", f"Series Timer {i+1} Any Channel", f"livetv/series_timers/{i}/RecordAnyChannel", "mdi:television-classic")
        
        # =====================================================================
        # POST /LiveTv/SeriesTimers - Create Series Timer
        # =====================================================================
        self.button("livetv_create_series_timer", "Create Series Timer", "livetv/series_timers/command", "create", "mdi:timer-sync")
        
        # =====================================================================
        # GET /LiveTv/Programs - Programs / Guide
        # =====================================================================
        self.sensor("livetv_programs_count", "Programs Count", "livetv/programs/count", "mdi:television-guide")
        self.sensor("livetv_programs_total_record_count", "Programs Total", "livetv/programs/TotalRecordCount", "mdi:television-guide")
        
        # =====================================================================
        # GET /LiveTv/Programs/Recommended - Recommended Programs
        # =====================================================================
        self.sensor("livetv_recommended_count", "Recommended Programs Count", "livetv/recommended/count", "mdi:star")
        self.sensor("livetv_recommended_list", "Recommended Programs List", "livetv/recommended/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /LiveTv/GuideInfo - Guide Info
        # =====================================================================
        self.sensor("livetv_guide_start_date", "Guide Start Date", "livetv/guide/StartDate", "mdi:calendar-start")
        self.sensor("livetv_guide_end_date", "Guide End Date", "livetv/guide/EndDate", "mdi:calendar-end")
        
        # =====================================================================
        # POST /LiveTv/GuideInfo - Refresh Guide
        # =====================================================================
        self.button("livetv_refresh_guide", "Refresh Guide", "livetv/command", "refresh_guide", "mdi:refresh")
        
        # =====================================================================
        # GET /LiveTv/Tuners - Tuners
        # =====================================================================
        self.sensor("livetv_tuners_count", "Tuners Count", "livetv/tuners/count", "mdi:antenna")
        self.sensor("livetv_tuners_list", "Tuners List", "livetv/tuners/list", "mdi:format-list-bulleted")
        
        # Tuner details (first 3)
        for i in range(3):
            self.sensor(f"livetv_tuner_{i}_name", f"Tuner {i+1} Name", f"livetv/tuners/{i}/Name", "mdi:antenna")
            self.sensor(f"livetv_tuner_{i}_source_type", f"Tuner {i+1} Source Type", f"livetv/tuners/{i}/SourceType", "mdi:tag")
            self.sensor(f"livetv_tuner_{i}_type", f"Tuner {i+1} Type", f"livetv/tuners/{i}/Type", "mdi:tag")
            self.sensor(f"livetv_tuner_{i}_device_id", f"Tuner {i+1} Device ID", f"livetv/tuners/{i}/DeviceId", "mdi:identifier")
            self.sensor(f"livetv_tuner_{i}_url", f"Tuner {i+1} URL", f"livetv/tuners/{i}/Url", "mdi:web")
            self.binary_sensor(f"livetv_tuner_{i}_allow_stream_sharing", f"Tuner {i+1} Stream Sharing", f"livetv/tuners/{i}/AllowHWTranscoding", "mdi:share")
        
        # =====================================================================
        # POST /LiveTv/TunerHosts - Add Tuner Host
        # =====================================================================
        self.button("livetv_add_tuner", "Add Tuner Host", "livetv/tuners/command", "add", "mdi:antenna")
        
        # =====================================================================
        # DELETE /LiveTv/TunerHosts - Delete Tuner Host
        # =====================================================================
        # Dynamic per tuner
        
        # =====================================================================
        # POST /LiveTv/ListingProviders - Add Listing Provider
        # =====================================================================
        self.button("livetv_add_listing_provider", "Add Listing Provider", "livetv/listings/command", "add", "mdi:television-guide")
        
        # =====================================================================
        # DELETE /LiveTv/ListingProviders - Delete Listing Provider
        # =====================================================================
        self.button("livetv_delete_listing_provider", "Delete Listing Provider", "livetv/listings/command", "delete", "mdi:television-guide")
        
        # =====================================================================
        # GET /LiveTv/ListingProviders/Lineups - Lineups
        # =====================================================================
        self.sensor("livetv_lineups_count", "Lineups Count", "livetv/lineups/count", "mdi:format-list-numbered")
        
        # =====================================================================
        # POST /LiveTv/ChannelMappingOptions - Channel Mapping
        # =====================================================================
        self.button("livetv_channel_mapping", "Channel Mapping Options", "livetv/command", "channel_mapping", "mdi:sitemap")
        
        # =====================================================================
        # POST /LiveTv/ChannelMappings - Set Channel Mappings
        # =====================================================================
        self.button("livetv_set_channel_mappings", "Set Channel Mappings", "livetv/command", "set_mappings", "mdi:sitemap")
        
        return self.entity_count
