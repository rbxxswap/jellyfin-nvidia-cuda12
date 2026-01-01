#!/usr/bin/env python3
"""
Discovery - Playstate Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class PlaystateDiscovery(DiscoveryBase):
    """Playstate group - ALLE Entities"""
    
    GROUP_NAME = 'playstate'
    
    def register_all(self):
        """Register ALLE playstate entities"""
        
        # =====================================================================
        # POST /Users/{userId}/PlayedItems/{itemId} - Mark Played
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # DELETE /Users/{userId}/PlayedItems/{itemId} - Mark Unplayed
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # POST /Users/{userId}/FavoriteItems/{itemId} - Mark Favorite
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # DELETE /Users/{userId}/FavoriteItems/{itemId} - Unmark Favorite
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # POST /Users/{userId}/Items/{itemId}/Rating - Update Rating
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # DELETE /Users/{userId}/Items/{itemId}/Rating - Delete Rating
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # POST /Users/{userId}/PlayingItems/{itemId} - Report Playback Start
        # =====================================================================
        # Internal use
        
        # =====================================================================
        # POST /Users/{userId}/PlayingItems/{itemId}/Progress - Report Progress
        # =====================================================================
        # Internal use
        
        # =====================================================================
        # DELETE /Users/{userId}/PlayingItems/{itemId} - Report Playback Stop
        # =====================================================================
        # Internal use
        
        # =====================================================================
        # Computed/Aggregated Stats
        # =====================================================================
        self.sensor("last_played_item_name", "Last Played Item", "playstate/last_played/Name", "mdi:play-circle")
        self.sensor("last_played_item_id", "Last Played Item ID", "playstate/last_played/Id", "mdi:identifier")
        self.sensor("last_played_item_type", "Last Played Type", "playstate/last_played/Type", "mdi:tag")
        self.sensor("last_played_user", "Last Played By User", "playstate/last_played/UserName", "mdi:account")
        self.sensor("last_played_user_id", "Last Played User ID", "playstate/last_played/UserId", "mdi:identifier")
        self.sensor("last_played_time", "Last Played Time", "playstate/last_played/Time", "mdi:clock")
        self.sensor("last_played_device", "Last Played Device", "playstate/last_played/DeviceName", "mdi:devices")
        self.sensor("last_played_client", "Last Played Client", "playstate/last_played/Client", "mdi:application")
        
        # =====================================================================
        # Playback Statistics
        # =====================================================================
        self.sensor("total_plays_today", "Total Plays Today", "playstate/stats/today/count", "mdi:play-circle-outline")
        self.sensor("total_plays_week", "Total Plays This Week", "playstate/stats/week/count", "mdi:play-circle-outline")
        self.sensor("total_plays_month", "Total Plays This Month", "playstate/stats/month/count", "mdi:play-circle-outline")
        self.sensor("total_watch_time_today", "Watch Time Today", "playstate/stats/today/watch_time", "mdi:clock", unit="min")
        self.sensor("total_watch_time_week", "Watch Time This Week", "playstate/stats/week/watch_time", "mdi:clock", unit="min")
        self.sensor("total_watch_time_month", "Watch Time This Month", "playstate/stats/month/watch_time", "mdi:clock", unit="min")
        
        # =====================================================================
        # Playback by Type
        # =====================================================================
        self.sensor("plays_movies_today", "Movie Plays Today", "playstate/stats/today/movies", "mdi:movie")
        self.sensor("plays_episodes_today", "Episode Plays Today", "playstate/stats/today/episodes", "mdi:filmstrip")
        self.sensor("plays_songs_today", "Song Plays Today", "playstate/stats/today/songs", "mdi:music")
        
        return self.entity_count
