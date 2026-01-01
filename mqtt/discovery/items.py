#!/usr/bin/env python3
"""
Discovery - Items Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class ItemsDiscovery(DiscoveryBase):
    """Items group - ALLE Entities"""
    
    GROUP_NAME = 'items'
    
    def register_all(self):
        """Register ALLE item entities"""
        
        # =====================================================================
        # GET /Items - Items Query
        # =====================================================================
        self.sensor("items_total", "Total Items", "items/total", "mdi:database")
        
        # =====================================================================
        # GET /Users/{userId}/Items/Resume - Resume Items
        # =====================================================================
        self.sensor("resume_items_count", "Resume Items Count", "items/resume/count", "mdi:play-pause")
        self.sensor("resume_items_total_record_count", "Resume Items Total", "items/resume/TotalRecordCount", "mdi:play-pause")
        self.sensor("resume_items_start_index", "Resume Items Start Index", "items/resume/StartIndex", "mdi:numeric")
        self.sensor("resume_items_list", "Resume Items List", "items/resume/list", "mdi:format-list-bulleted")
        
        # Resume Item Details (first 5)
        for i in range(5):
            self.sensor(f"resume_item_{i}_name", f"Resume Item {i+1} Name", f"items/resume/{i}/Name", "mdi:play-pause")
            self.sensor(f"resume_item_{i}_id", f"Resume Item {i+1} ID", f"items/resume/{i}/Id", "mdi:identifier")
            self.sensor(f"resume_item_{i}_type", f"Resume Item {i+1} Type", f"items/resume/{i}/Type", "mdi:tag")
            self.sensor(f"resume_item_{i}_series", f"Resume Item {i+1} Series", f"items/resume/{i}/SeriesName", "mdi:television")
            self.sensor(f"resume_item_{i}_progress", f"Resume Item {i+1} Progress", f"items/resume/{i}/progress", "mdi:percent", unit="%")
            self.sensor(f"resume_item_{i}_user_data_played_percentage", f"Resume Item {i+1} Played %", f"items/resume/{i}/UserData/PlayedPercentage", "mdi:percent", unit="%")
        
        # =====================================================================
        # GET /Users/{userId}/Items/Latest - Latest Items
        # =====================================================================
        self.sensor("latest_items_count", "Latest Items Count", "items/latest/count", "mdi:new-box")
        self.sensor("latest_items_list", "Latest Items List", "items/latest/list", "mdi:format-list-bulleted")
        
        # Latest Item Details (first 10)
        for i in range(10):
            self.sensor(f"latest_item_{i}_name", f"Latest Item {i+1} Name", f"items/latest/{i}/Name", "mdi:new-box")
            self.sensor(f"latest_item_{i}_id", f"Latest Item {i+1} ID", f"items/latest/{i}/Id", "mdi:identifier")
            self.sensor(f"latest_item_{i}_type", f"Latest Item {i+1} Type", f"items/latest/{i}/Type", "mdi:tag")
            self.sensor(f"latest_item_{i}_series", f"Latest Item {i+1} Series", f"items/latest/{i}/SeriesName", "mdi:television")
            self.sensor(f"latest_item_{i}_date_created", f"Latest Item {i+1} Date", f"items/latest/{i}/DateCreated", "mdi:calendar")
        
        # =====================================================================
        # GET /Items/{itemId} - Get Single Item
        # =====================================================================
        # Dynamic per item request
        
        # =====================================================================
        # POST /Items/{itemId} - Update Item
        # =====================================================================
        # Dynamic per item request
        
        # =====================================================================
        # DELETE /Items/{itemId} - Delete Item
        # =====================================================================
        # Dynamic per item request
        
        # =====================================================================
        # POST /Items/{itemId}/Refresh - Refresh Item Metadata
        # =====================================================================
        # Dynamic per item request
        
        # =====================================================================
        # GET /Items/{itemId}/Similar - Similar Items
        # =====================================================================
        self.sensor("similar_items_count", "Similar Items Count", "items/similar/count", "mdi:movie-search")
        
        # =====================================================================
        # GET /Items/{itemId}/ThemeSongs - Theme Songs
        # =====================================================================
        self.sensor("theme_songs_count", "Theme Songs Count", "items/theme_songs/count", "mdi:music")
        
        # =====================================================================
        # GET /Items/{itemId}/ThemeVideos - Theme Videos
        # =====================================================================
        self.sensor("theme_videos_count", "Theme Videos Count", "items/theme_videos/count", "mdi:video")
        
        # =====================================================================
        # Favorites
        # =====================================================================
        self.sensor("favorites_count", "Favorites Count", "items/favorites/count", "mdi:heart")
        self.sensor("favorites_movies", "Favorite Movies", "items/favorites/movies/count", "mdi:movie-star")
        self.sensor("favorites_series", "Favorite Series", "items/favorites/series/count", "mdi:television-classic")
        self.sensor("favorites_episodes", "Favorite Episodes", "items/favorites/episodes/count", "mdi:filmstrip")
        self.sensor("favorites_songs", "Favorite Songs", "items/favorites/songs/count", "mdi:music")
        self.sensor("favorites_albums", "Favorite Albums", "items/favorites/albums/count", "mdi:album")
        
        # =====================================================================
        # Recently Added (by type)
        # =====================================================================
        self.sensor("recent_movies_count", "Recent Movies Count", "items/recent/movies/count", "mdi:movie")
        self.sensor("recent_episodes_count", "Recent Episodes Count", "items/recent/episodes/count", "mdi:filmstrip")
        self.sensor("recent_music_count", "Recent Music Count", "items/recent/music/count", "mdi:music")
        
        for i in range(5):
            self.sensor(f"recent_movie_{i}_name", f"Recent Movie {i+1}", f"items/recent/movies/{i}/Name", "mdi:movie")
            self.sensor(f"recent_movie_{i}_year", f"Recent Movie {i+1} Year", f"items/recent/movies/{i}/ProductionYear", "mdi:calendar")
            self.sensor(f"recent_episode_{i}_name", f"Recent Episode {i+1}", f"items/recent/episodes/{i}/Name", "mdi:filmstrip")
            self.sensor(f"recent_episode_{i}_series", f"Recent Episode {i+1} Series", f"items/recent/episodes/{i}/SeriesName", "mdi:television")
        
        return self.entity_count
