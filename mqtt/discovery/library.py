#!/usr/bin/env python3
"""
Discovery - Library Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class LibraryDiscovery(DiscoveryBase):
    """Library group - ALLE Entities"""
    
    GROUP_NAME = 'library'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registered_libraries = set()
    
    def register_all(self):
        """Register ALLE library entities"""
        
        # =====================================================================
        # GET /Library/MediaFolders
        # =====================================================================
        self.sensor("media_folders_count", "Media Folders Count", "library/media_folders/count", "mdi:folder-multiple")
        self.sensor("media_folders_total_record_count", "Media Folders Total", "library/media_folders/TotalRecordCount", "mdi:folder-multiple")
        
        # =====================================================================
        # GET /Library/VirtualFolders
        # =====================================================================
        self.sensor("virtual_folders_count", "Virtual Folders Count", "library/virtual_folders/count", "mdi:folder-star")
        
        # =====================================================================
        # POST /Library/Refresh - Library Scan
        # =====================================================================
        self.button("library_refresh_all", "Refresh All Libraries", "library/command", "refresh", "mdi:refresh")
        self.binary_sensor("library_scanning", "Library Scanning", "library/scanning", "mdi:magnify-scan")
        
        # =====================================================================
        # GET /Items/Counts - Item Counts
        # =====================================================================
        self.sensor("item_count_movie", "Movies Count", "library/counts/MovieCount", "mdi:movie")
        self.sensor("item_count_series", "Series Count", "library/counts/SeriesCount", "mdi:television-classic")
        self.sensor("item_count_episode", "Episodes Count", "library/counts/EpisodeCount", "mdi:filmstrip")
        self.sensor("item_count_artist", "Artists Count", "library/counts/ArtistCount", "mdi:account-music")
        self.sensor("item_count_program", "Programs Count", "library/counts/ProgramCount", "mdi:television-guide")
        self.sensor("item_count_trailer", "Trailers Count", "library/counts/TrailerCount", "mdi:movie-roll")
        self.sensor("item_count_song", "Songs Count", "library/counts/SongCount", "mdi:music")
        self.sensor("item_count_album", "Albums Count", "library/counts/AlbumCount", "mdi:album")
        self.sensor("item_count_music_video", "Music Videos Count", "library/counts/MusicVideoCount", "mdi:music-box")
        self.sensor("item_count_box_set", "Box Sets Count", "library/counts/BoxSetCount", "mdi:package-variant-closed")
        self.sensor("item_count_book", "Books Count", "library/counts/BookCount", "mdi:book")
        self.sensor("item_count_item", "Total Items Count", "library/counts/ItemCount", "mdi:database")
        
        # =====================================================================
        # GET /Library/PhysicalPaths
        # =====================================================================
        self.sensor("physical_paths_count", "Physical Paths Count", "library/physical_paths/count", "mdi:folder-marker")
        self.sensor("physical_paths_list", "Physical Paths List", "library/physical_paths/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # POST /Library/VirtualFolders - Add Virtual Folder
        # =====================================================================
        self.button("add_virtual_folder", "Add Virtual Folder", "library/virtual_folders/command", "add", "mdi:folder-plus")
        
        # =====================================================================
        # DELETE /Library/VirtualFolders - Remove Virtual Folder
        # =====================================================================
        self.button("remove_virtual_folder", "Remove Virtual Folder", "library/virtual_folders/command", "remove", "mdi:folder-remove")
        
        # =====================================================================
        # POST /Library/VirtualFolders/LibraryOptions
        # =====================================================================
        self.button("update_library_options", "Update Library Options", "library/virtual_folders/command", "update_options", "mdi:folder-cog")
        
        # =====================================================================
        # POST /Library/VirtualFolders/Name
        # =====================================================================
        self.button("rename_virtual_folder", "Rename Virtual Folder", "library/virtual_folders/command", "rename", "mdi:folder-edit")
        
        # =====================================================================
        # POST /Library/VirtualFolders/Paths - Add Path
        # =====================================================================
        self.button("add_media_path", "Add Media Path", "library/virtual_folders/paths/command", "add", "mdi:folder-plus")
        
        # =====================================================================
        # DELETE /Library/VirtualFolders/Paths - Remove Path
        # =====================================================================
        self.button("remove_media_path", "Remove Media Path", "library/virtual_folders/paths/command", "remove", "mdi:folder-remove")
        
        # =====================================================================
        # POST /Library/VirtualFolders/Paths/Update
        # =====================================================================
        self.button("update_media_path", "Update Media Path", "library/virtual_folders/paths/command", "update", "mdi:folder-sync")
        
        # =====================================================================
        # POST /Items/{itemId}/Refresh - Refresh Item
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # DELETE /Items - Delete Items
        # =====================================================================
        self.button("delete_items", "Delete Items", "library/command", "delete_items", "mdi:delete")
        
        # =====================================================================
        # DELETE /Items/{itemId} - Delete Item
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # GET /Libraries/AvailableOptions - Library Options
        # =====================================================================
        self.sensor("available_library_options", "Available Library Options", "library/available_options", "mdi:cog")
        
        # =====================================================================
        # Storage/Size Sensors (computed)
        # =====================================================================
        self.sensor("library_total_size", "Library Total Size", "library/size/total", "mdi:harddisk", unit="GB")
        self.sensor("library_movies_size", "Movies Size", "library/size/movies", "mdi:harddisk", unit="GB")
        self.sensor("library_series_size", "Series Size", "library/size/series", "mdi:harddisk", unit="GB")
        self.sensor("library_music_size", "Music Size", "library/size/music", "mdi:harddisk", unit="GB")
        
        return self.entity_count
    
    def register_library(self, library_id, library_name, collection_type, locations=None):
        """Register ALLE Entities für eine spezifische Library"""
        if library_id in self.registered_libraries:
            return 0
        
        safe_name = library_name.replace(" ", "_").lower()[:20]
        prefix = f"lib_{safe_name}"
        base_topic = f"library/{library_id}"
        
        # =====================================================================
        # Library Info
        # =====================================================================
        self.sensor(f"{prefix}_name", f"{library_name}", f"{base_topic}/Name", "mdi:folder-play")
        self.sensor(f"{prefix}_item_id", f"{library_name} Item ID", f"{base_topic}/ItemId", "mdi:identifier")
        self.sensor(f"{prefix}_collection_type", f"{library_name} Collection Type", f"{base_topic}/CollectionType", "mdi:tag")
        self.sensor(f"{prefix}_library_type", f"{library_name} Library Type", f"{base_topic}/LibraryType", "mdi:tag")
        self.sensor(f"{prefix}_content_type", f"{library_name} Content Type", f"{base_topic}/ContentType", "mdi:tag")
        self.sensor(f"{prefix}_primary_image_item_id", f"{library_name} Primary Image ID", f"{base_topic}/PrimaryImageItemId", "mdi:image")
        self.binary_sensor(f"{prefix}_refresh_progress", f"{library_name} Refresh Progress", f"{base_topic}/RefreshProgress", "mdi:refresh")
        self.sensor(f"{prefix}_refresh_status", f"{library_name} Refresh Status", f"{base_topic}/RefreshStatus", "mdi:refresh")
        
        # =====================================================================
        # Library Locations
        # =====================================================================
        self.sensor(f"{prefix}_locations_count", f"{library_name} Locations Count", f"{base_topic}/Locations/count", "mdi:folder-multiple")
        self.sensor(f"{prefix}_locations", f"{library_name} Locations", f"{base_topic}/Locations", "mdi:folder-multiple")
        
        # =====================================================================
        # Library Options
        # =====================================================================
        self.binary_sensor(f"{prefix}_enable_photos", f"{library_name} Enable Photos", f"{base_topic}/LibraryOptions/EnablePhotos", "mdi:image")
        self.binary_sensor(f"{prefix}_enable_realtime_monitor", f"{library_name} Realtime Monitor", f"{base_topic}/LibraryOptions/EnableRealtimeMonitor", "mdi:monitor")
        self.binary_sensor(f"{prefix}_enable_chapter_image_extraction", f"{library_name} Chapter Images", f"{base_topic}/LibraryOptions/EnableChapterImageExtraction", "mdi:image-multiple")
        self.binary_sensor(f"{prefix}_extract_chapter_images_during_scan", f"{library_name} Extract During Scan", f"{base_topic}/LibraryOptions/ExtractChapterImagesDuringLibraryScan", "mdi:image-search")
        self.sensor(f"{prefix}_path_infos_count", f"{library_name} Path Infos Count", f"{base_topic}/LibraryOptions/PathInfos/count", "mdi:folder")
        self.binary_sensor(f"{prefix}_save_local_metadata", f"{library_name} Save Local Metadata", f"{base_topic}/LibraryOptions/SaveLocalMetadata", "mdi:content-save")
        self.binary_sensor(f"{prefix}_enable_internet_providers", f"{library_name} Internet Providers", f"{base_topic}/LibraryOptions/EnableInternetProviders", "mdi:web")
        self.binary_sensor(f"{prefix}_enable_automatic_series_grouping", f"{library_name} Auto Series Grouping", f"{base_topic}/LibraryOptions/EnableAutomaticSeriesGrouping", "mdi:group")
        self.binary_sensor(f"{prefix}_enable_embedded_titles", f"{library_name} Embedded Titles", f"{base_topic}/LibraryOptions/EnableEmbeddedTitles", "mdi:format-title")
        self.binary_sensor(f"{prefix}_enable_embedded_episode_infos", f"{library_name} Embedded Episode Infos", f"{base_topic}/LibraryOptions/EnableEmbeddedEpisodeInfos", "mdi:information")
        self.sensor(f"{prefix}_automatic_refresh_interval_days", f"{library_name} Refresh Interval", f"{base_topic}/LibraryOptions/AutomaticRefreshIntervalDays", "mdi:calendar-refresh", unit="days")
        self.sensor(f"{prefix}_preferred_metadata_language", f"{library_name} Metadata Language", f"{base_topic}/LibraryOptions/PreferredMetadataLanguage", "mdi:translate")
        self.sensor(f"{prefix}_metadata_country_code", f"{library_name} Metadata Country", f"{base_topic}/LibraryOptions/MetadataCountryCode", "mdi:earth")
        self.sensor(f"{prefix}_season_zero_display_name", f"{library_name} Season Zero Name", f"{base_topic}/LibraryOptions/SeasonZeroDisplayName", "mdi:numeric-0")
        self.sensor(f"{prefix}_metadata_savers", f"{library_name} Metadata Savers", f"{base_topic}/LibraryOptions/MetadataSavers", "mdi:content-save")
        self.sensor(f"{prefix}_disabled_local_metadata_readers", f"{library_name} Disabled Readers", f"{base_topic}/LibraryOptions/DisabledLocalMetadataReaders", "mdi:file-hidden")
        self.sensor(f"{prefix}_local_metadata_reader_order", f"{library_name} Reader Order", f"{base_topic}/LibraryOptions/LocalMetadataReaderOrder", "mdi:sort")
        self.sensor(f"{prefix}_disabled_subtitle_fetchers", f"{library_name} Disabled Subtitle Fetchers", f"{base_topic}/LibraryOptions/DisabledSubtitleFetchers", "mdi:subtitles-outline")
        self.sensor(f"{prefix}_subtitle_fetcher_order", f"{library_name} Subtitle Fetcher Order", f"{base_topic}/LibraryOptions/SubtitleFetcherOrder", "mdi:sort")
        self.binary_sensor(f"{prefix}_skip_subtitles_if_embedded", f"{library_name} Skip If Embedded", f"{base_topic}/LibraryOptions/SkipSubtitlesIfEmbeddedSubtitlesPresent", "mdi:subtitles-outline")
        self.binary_sensor(f"{prefix}_skip_subtitles_if_audio_track_matches", f"{library_name} Skip If Audio Match", f"{base_topic}/LibraryOptions/SkipSubtitlesIfAudioTrackMatches", "mdi:subtitles-outline")
        self.sensor(f"{prefix}_subtitle_download_languages", f"{library_name} Subtitle Languages", f"{base_topic}/LibraryOptions/SubtitleDownloadLanguages", "mdi:translate")
        self.binary_sensor(f"{prefix}_require_perfect_subtitle_match", f"{library_name} Perfect Subtitle Match", f"{base_topic}/LibraryOptions/RequirePerfectSubtitleMatch", "mdi:check")
        self.binary_sensor(f"{prefix}_save_subtitles_with_media", f"{library_name} Save Subtitles", f"{base_topic}/LibraryOptions/SaveSubtitlesWithMedia", "mdi:content-save")
        self.binary_sensor(f"{prefix}_save_lyrics_with_media", f"{library_name} Save Lyrics", f"{base_topic}/LibraryOptions/SaveLyricsWithMedia", "mdi:content-save")
        self.sensor(f"{prefix}_type_options", f"{library_name} Type Options", f"{base_topic}/LibraryOptions/TypeOptions", "mdi:cog")
        
        # =====================================================================
        # Library Stats
        # =====================================================================
        self.sensor(f"{prefix}_item_count", f"{library_name} Items", f"{base_topic}/item_count", "mdi:numeric")
        self.sensor(f"{prefix}_size", f"{library_name} Size", f"{base_topic}/size", "mdi:harddisk", unit="GB")
        self.sensor(f"{prefix}_unplayed_count", f"{library_name} Unplayed", f"{base_topic}/unplayed_count", "mdi:eye-off")
        self.sensor(f"{prefix}_played_count", f"{library_name} Played", f"{base_topic}/played_count", "mdi:eye")
        self.sensor(f"{prefix}_favorite_count", f"{library_name} Favorites", f"{base_topic}/favorite_count", "mdi:heart")
        
        # =====================================================================
        # Library Control Buttons
        # =====================================================================
        self.button(f"{prefix}_refresh", f"Refresh {library_name}", f"{base_topic}/command", "refresh", "mdi:refresh")
        self.button(f"{prefix}_scan", f"Scan {library_name}", f"{base_topic}/command", "scan", "mdi:magnify-scan")
        
        self.registered_libraries.add(library_id)
        return self.entity_count
