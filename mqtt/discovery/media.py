#!/usr/bin/env python3
"""
Discovery - Media Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class MediaDiscovery(DiscoveryBase):
    """Media group - ALLE Entities"""
    
    GROUP_NAME = 'media'
    
    def register_all(self):
        """Register ALLE media entities"""
        
        # =====================================================================
        # GET /Search/Hints - Search
        # =====================================================================
        self.sensor("search_hints_count", "Search Results Count", "media/search/TotalRecordCount", "mdi:magnify")
        
        # =====================================================================
        # GET /Artists - Artists
        # =====================================================================
        self.sensor("artists_count", "Artists Count", "media/artists/count", "mdi:account-music")
        self.sensor("artists_total_record_count", "Artists Total", "media/artists/TotalRecordCount", "mdi:account-music")
        self.sensor("artists_list", "Artists List", "media/artists/list", "mdi:format-list-bulleted")
        
        # Artist details (first 10)
        for i in range(10):
            self.sensor(f"artist_{i}_name", f"Artist {i+1} Name", f"media/artists/{i}/Name", "mdi:account-music")
            self.sensor(f"artist_{i}_id", f"Artist {i+1} ID", f"media/artists/{i}/Id", "mdi:identifier")
            self.sensor(f"artist_{i}_album_count", f"Artist {i+1} Albums", f"media/artists/{i}/AlbumCount", "mdi:album")
            self.sensor(f"artist_{i}_song_count", f"Artist {i+1} Songs", f"media/artists/{i}/SongCount", "mdi:music")
        
        # =====================================================================
        # GET /Artists/AlbumArtists - Album Artists
        # =====================================================================
        self.sensor("album_artists_count", "Album Artists Count", "media/album_artists/count", "mdi:account-music-outline")
        self.sensor("album_artists_total_record_count", "Album Artists Total", "media/album_artists/TotalRecordCount", "mdi:account-music-outline")
        
        # =====================================================================
        # GET /Genres - Genres
        # =====================================================================
        self.sensor("genres_count", "Genres Count", "media/genres/count", "mdi:tag-multiple")
        self.sensor("genres_total_record_count", "Genres Total", "media/genres/TotalRecordCount", "mdi:tag-multiple")
        self.sensor("genres_list", "Genres List", "media/genres/list", "mdi:format-list-bulleted")
        
        # Genre details (first 20)
        for i in range(20):
            self.sensor(f"genre_{i}_name", f"Genre {i+1} Name", f"media/genres/{i}/Name", "mdi:tag")
            self.sensor(f"genre_{i}_id", f"Genre {i+1} ID", f"media/genres/{i}/Id", "mdi:identifier")
        
        # =====================================================================
        # GET /MusicGenres - Music Genres
        # =====================================================================
        self.sensor("music_genres_count", "Music Genres Count", "media/music_genres/count", "mdi:music-note")
        self.sensor("music_genres_total_record_count", "Music Genres Total", "media/music_genres/TotalRecordCount", "mdi:music-note")
        self.sensor("music_genres_list", "Music Genres List", "media/music_genres/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /Studios - Studios
        # =====================================================================
        self.sensor("studios_count", "Studios Count", "media/studios/count", "mdi:domain")
        self.sensor("studios_total_record_count", "Studios Total", "media/studios/TotalRecordCount", "mdi:domain")
        self.sensor("studios_list", "Studios List", "media/studios/list", "mdi:format-list-bulleted")
        
        # Studio details (first 10)
        for i in range(10):
            self.sensor(f"studio_{i}_name", f"Studio {i+1} Name", f"media/studios/{i}/Name", "mdi:domain")
            self.sensor(f"studio_{i}_id", f"Studio {i+1} ID", f"media/studios/{i}/Id", "mdi:identifier")
        
        # =====================================================================
        # GET /Persons - Persons (Actors, Directors, etc.)
        # =====================================================================
        self.sensor("persons_count", "Persons Count", "media/persons/count", "mdi:account-multiple")
        self.sensor("persons_total_record_count", "Persons Total", "media/persons/TotalRecordCount", "mdi:account-multiple")
        self.sensor("persons_list", "Persons List", "media/persons/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /Tags - Tags
        # =====================================================================
        self.sensor("tags_count", "Tags Count", "media/tags/count", "mdi:tag")
        self.sensor("tags_total_record_count", "Tags Total", "media/tags/TotalRecordCount", "mdi:tag")
        
        # =====================================================================
        # GET /Years - Years
        # =====================================================================
        self.sensor("years_count", "Years Count", "media/years/count", "mdi:calendar-range")
        self.sensor("years_list", "Years List", "media/years/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /Shows/NextUp - Next Up Episodes
        # =====================================================================
        self.sensor("next_up_count", "Next Up Count", "media/nextup/count", "mdi:play-box-multiple")
        self.sensor("next_up_total_record_count", "Next Up Total", "media/nextup/TotalRecordCount", "mdi:play-box-multiple")
        self.sensor("next_up_list", "Next Up List", "media/nextup/list", "mdi:format-list-bulleted")
        
        # Next Up details (first 10)
        for i in range(10):
            self.sensor(f"next_up_{i}_name", f"Next Up {i+1} Name", f"media/nextup/{i}/Name", "mdi:play-box")
            self.sensor(f"next_up_{i}_id", f"Next Up {i+1} ID", f"media/nextup/{i}/Id", "mdi:identifier")
            self.sensor(f"next_up_{i}_series_name", f"Next Up {i+1} Series", f"media/nextup/{i}/SeriesName", "mdi:television-classic")
            self.sensor(f"next_up_{i}_season", f"Next Up {i+1} Season", f"media/nextup/{i}/ParentIndexNumber", "mdi:numeric")
            self.sensor(f"next_up_{i}_episode", f"Next Up {i+1} Episode", f"media/nextup/{i}/IndexNumber", "mdi:numeric")
        
        # =====================================================================
        # GET /Shows/Upcoming - Upcoming Episodes
        # =====================================================================
        self.sensor("upcoming_count", "Upcoming Episodes Count", "media/upcoming/count", "mdi:calendar-clock")
        self.sensor("upcoming_total_record_count", "Upcoming Total", "media/upcoming/TotalRecordCount", "mdi:calendar-clock")
        self.sensor("upcoming_list", "Upcoming Episodes List", "media/upcoming/list", "mdi:format-list-bulleted")
        
        # Upcoming details (first 10)
        for i in range(10):
            self.sensor(f"upcoming_{i}_name", f"Upcoming {i+1} Name", f"media/upcoming/{i}/Name", "mdi:calendar-clock")
            self.sensor(f"upcoming_{i}_series_name", f"Upcoming {i+1} Series", f"media/upcoming/{i}/SeriesName", "mdi:television-classic")
            self.sensor(f"upcoming_{i}_premiere_date", f"Upcoming {i+1} Date", f"media/upcoming/{i}/PremiereDate", "mdi:calendar")
        
        # =====================================================================
        # GET /Items/{itemId}/Similar - Similar Items
        # =====================================================================
        self.sensor("similar_count", "Similar Items Count", "media/similar/count", "mdi:movie-search")
        
        # =====================================================================
        # GET /Items/{itemId}/ThemeSongs - Theme Songs
        # =====================================================================
        self.sensor("theme_songs_count", "Theme Songs Count", "media/theme_songs/count", "mdi:music")
        
        # =====================================================================
        # GET /Items/{itemId}/ThemeVideos - Theme Videos
        # =====================================================================
        self.sensor("theme_videos_count", "Theme Videos Count", "media/theme_videos/count", "mdi:video")
        
        # =====================================================================
        # GET /Artists/{artistId}/InstantMix - Instant Mix
        # =====================================================================
        self.sensor("instant_mix_count", "Instant Mix Count", "media/instantmix/count", "mdi:shuffle-variant")
        
        # =====================================================================
        # GET /Movies/Recommendations - Movie Recommendations
        # =====================================================================
        self.sensor("recommendations_count", "Recommendations Count", "media/recommendations/count", "mdi:lightbulb")
        self.sensor("recommendations_list", "Recommendations List", "media/recommendations/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /Trailers - Trailers
        # =====================================================================
        self.sensor("trailers_count", "Trailers Count", "media/trailers/count", "mdi:movie-roll")
        self.sensor("trailers_total_record_count", "Trailers Total", "media/trailers/TotalRecordCount", "mdi:movie-roll")
        
        # =====================================================================
        # GET /Collections - Collections
        # =====================================================================
        self.sensor("collections_count", "Collections Count", "media/collections/count", "mdi:folder-star")
        
        # =====================================================================
        # POST /Collections - Create Collection
        # =====================================================================
        self.button("create_collection", "Create Collection", "media/collections/command", "create", "mdi:folder-plus")
        
        return self.entity_count
