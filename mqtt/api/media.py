#!/usr/bin/env python3
"""
Jellyfin API - Media Group
Endpoints: ~25
- Search, Artists, Genres, Studios, MusicGenres, Persons, TVShows, Movies, Collections
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class MediaAPI(JellyfinAPIBase):
    """Media API endpoints (Search, Artists, Genres, etc.)"""
    
    GROUP_NAME = 'media'
    
    # =========================================================================
    # SEARCH (1 endpoint)
    # =========================================================================
    
    def search(self, search_term: str, user_id: str = None, start_index: int = None,
               limit: int = None, include_item_types: List[str] = None,
               exclude_item_types: List[str] = None, media_types: List[str] = None,
               parent_id: str = None, is_movie: bool = None, is_series: bool = None,
               is_news: bool = None, is_kids: bool = None, is_sports: bool = None,
               include_people: bool = None, include_media: bool = None,
               include_genres: bool = None, include_studios: bool = None,
               include_artists: bool = None) -> Optional[Dict]:
        """GET /Search/Hints - Search for items"""
        params = {'searchTerm': search_term}
        if user_id:
            params['userId'] = user_id
        if start_index is not None:
            params['startIndex'] = start_index
        if limit is not None:
            params['limit'] = limit
        if include_item_types:
            params['includeItemTypes'] = ','.join(include_item_types)
        if exclude_item_types:
            params['excludeItemTypes'] = ','.join(exclude_item_types)
        if media_types:
            params['mediaTypes'] = ','.join(media_types)
        if parent_id:
            params['parentId'] = parent_id
        for key, val in [('isMovie', is_movie), ('isSeries', is_series),
                         ('isNews', is_news), ('isKids', is_kids), ('isSports', is_sports),
                         ('includePeople', include_people), ('includeMedia', include_media),
                         ('includeGenres', include_genres), ('includeStudios', include_studios),
                         ('includeArtists', include_artists)]:
            if val is not None:
                params[key] = val
        return self._get('/Search/Hints', params)
    
    # =========================================================================
    # ARTISTS (3 endpoints)
    # =========================================================================
    
    def get_artists(self, user_id: str = None, search_term: str = None,
                    parent_id: str = None, limit: int = None,
                    start_index: int = None, **kwargs) -> Optional[Dict]:
        """GET /Artists - Get all artists"""
        params = {k: v for k, v in {
            'userId': user_id, 'searchTerm': search_term,
            'parentId': parent_id, 'limit': limit, 'startIndex': start_index,
            **kwargs
        }.items() if v is not None}
        return self._get('/Artists', params)
    
    def get_album_artists(self, user_id: str = None, **kwargs) -> Optional[Dict]:
        """GET /Artists/AlbumArtists - Get all album artists"""
        params = {k: v for k, v in {'userId': user_id, **kwargs}.items() if v is not None}
        return self._get('/Artists/AlbumArtists', params)
    
    def get_artist_by_name(self, name: str, user_id: str = None) -> Optional[Dict]:
        """GET /Artists/{name} - Get artist by name"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Artists/{name}', params)
    
    # =========================================================================
    # GENRES (2 endpoints)
    # =========================================================================
    
    def get_genres(self, user_id: str = None, start_index: int = None,
                   limit: int = None, parent_id: str = None) -> Optional[Dict]:
        """GET /Genres - Get all genres"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index,
            'limit': limit, 'parentId': parent_id
        }.items() if v is not None}
        return self._get('/Genres', params)
    
    def get_genre(self, genre_name: str, user_id: str = None) -> Optional[Dict]:
        """GET /Genres/{genreName} - Get genre by name"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Genres/{genre_name}', params)
    
    # =========================================================================
    # MUSIC GENRES (2 endpoints)
    # =========================================================================
    
    def get_music_genres(self, user_id: str = None, start_index: int = None,
                         limit: int = None, parent_id: str = None) -> Optional[Dict]:
        """GET /MusicGenres - Get music genres"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index,
            'limit': limit, 'parentId': parent_id
        }.items() if v is not None}
        return self._get('/MusicGenres', params)
    
    def get_music_genre(self, genre_name: str, user_id: str = None) -> Optional[Dict]:
        """GET /MusicGenres/{genreName} - Get music genre"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/MusicGenres/{genre_name}', params)
    
    # =========================================================================
    # STUDIOS (2 endpoints)
    # =========================================================================
    
    def get_studios(self, user_id: str = None, start_index: int = None,
                    limit: int = None, parent_id: str = None) -> Optional[Dict]:
        """GET /Studios - Get studios"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index,
            'limit': limit, 'parentId': parent_id
        }.items() if v is not None}
        return self._get('/Studios', params)
    
    def get_studio(self, name: str, user_id: str = None) -> Optional[Dict]:
        """GET /Studios/{name} - Get studio by name"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Studios/{name}', params)
    
    # =========================================================================
    # PERSONS (2 endpoints)
    # =========================================================================
    
    def get_persons(self, user_id: str = None, start_index: int = None,
                    limit: int = None, **kwargs) -> Optional[Dict]:
        """GET /Persons - Get persons"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit, **kwargs
        }.items() if v is not None}
        return self._get('/Persons', params)
    
    def get_person(self, name: str, user_id: str = None) -> Optional[Dict]:
        """GET /Persons/{name} - Get person by name"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Persons/{name}', params)
    
    # =========================================================================
    # TV SHOWS (4 endpoints)
    # =========================================================================
    
    def get_next_up(self, user_id: str = None, start_index: int = None,
                    limit: int = None, parent_id: str = None,
                    enable_images: bool = None, enable_total_record_count: bool = None,
                    disable_first_episode: bool = None, **kwargs) -> Optional[Dict]:
        """GET /Shows/NextUp - Get next up episodes"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit,
            'parentId': parent_id, 'enableImages': enable_images,
            'enableTotalRecordCount': enable_total_record_count,
            'disableFirstEpisode': disable_first_episode, **kwargs
        }.items() if v is not None}
        return self._get('/Shows/NextUp', params)
    
    def get_upcoming_episodes(self, user_id: str = None, start_index: int = None,
                               limit: int = None, parent_id: str = None,
                               enable_images: bool = None) -> Optional[Dict]:
        """GET /Shows/Upcoming - Get upcoming episodes"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit,
            'parentId': parent_id, 'enableImages': enable_images
        }.items() if v is not None}
        return self._get('/Shows/Upcoming', params)
    
    def get_episodes(self, series_id: str, user_id: str = None,
                     season_id: str = None, season: int = None,
                     start_index: int = None, limit: int = None,
                     is_missing: bool = None, adjacent_to: str = None,
                     enable_images: bool = None, **kwargs) -> Optional[Dict]:
        """GET /Shows/{seriesId}/Episodes - Get episodes"""
        params = {k: v for k, v in {
            'userId': user_id, 'seasonId': season_id, 'season': season,
            'startIndex': start_index, 'limit': limit, 'isMissing': is_missing,
            'adjacentTo': adjacent_to, 'enableImages': enable_images, **kwargs
        }.items() if v is not None}
        return self._get(f'/Shows/{series_id}/Episodes', params)
    
    def get_seasons(self, series_id: str, user_id: str = None,
                    is_special_season: bool = None, is_missing: bool = None,
                    adjacent_to: str = None, enable_images: bool = None) -> Optional[Dict]:
        """GET /Shows/{seriesId}/Seasons - Get seasons"""
        params = {k: v for k, v in {
            'userId': user_id, 'isSpecialSeason': is_special_season,
            'isMissing': is_missing, 'adjacentTo': adjacent_to,
            'enableImages': enable_images
        }.items() if v is not None}
        return self._get(f'/Shows/{series_id}/Seasons', params)
    
    # =========================================================================
    # MOVIES (1 endpoint)
    # =========================================================================
    
    def get_movie_recommendations(self, user_id: str = None, parent_id: str = None,
                                   category_limit: int = None, item_limit: int = None) -> Optional[List]:
        """GET /Movies/Recommendations - Get movie recommendations"""
        params = {k: v for k, v in {
            'userId': user_id, 'parentId': parent_id,
            'categoryLimit': category_limit, 'itemLimit': item_limit
        }.items() if v is not None}
        return self._get('/Movies/Recommendations', params)
    
    # =========================================================================
    # COLLECTIONS (3 endpoints)
    # =========================================================================
    
    def create_collection(self, name: str, ids: List[str] = None,
                          parent_id: str = None) -> Optional[Dict]:
        """POST /Collections - Create collection"""
        params = {'name': name}
        if ids:
            params['ids'] = ','.join(ids)
        if parent_id:
            params['parentId'] = parent_id
        return self._post('/Collections', params=params)
    
    def add_to_collection(self, collection_id: str, ids: List[str]) -> bool:
        """POST /Collections/{collectionId}/Items - Add items to collection"""
        return self._post(f'/Collections/{collection_id}/Items',
                         params={'ids': ','.join(ids)}) is not None
    
    def remove_from_collection(self, collection_id: str, ids: List[str]) -> bool:
        """DELETE /Collections/{collectionId}/Items - Remove items from collection"""
        return self._delete(f'/Collections/{collection_id}/Items',
                           params={'ids': ','.join(ids)}) is not None
    
    # =========================================================================
    # YEARS (2 endpoints)
    # =========================================================================
    
    def get_years(self, user_id: str = None, start_index: int = None,
                  limit: int = None, **kwargs) -> Optional[Dict]:
        """GET /Years - Get years"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit, **kwargs
        }.items() if v is not None}
        return self._get('/Years', params)
    
    def get_year(self, year: int, user_id: str = None) -> Optional[Dict]:
        """GET /Years/{year} - Get year"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Years/{year}', params)
    
    # =========================================================================
    # SUGGESTIONS (1 endpoint)
    # =========================================================================
    
    def get_suggestions(self, user_id: str = None, media_type: List[str] = None,
                        type: List[str] = None, start_index: int = None,
                        limit: int = None, enable_total_record_count: bool = None) -> Optional[Dict]:
        """GET /Items/Suggestions - Get suggestions"""
        params = {}
        if user_id:
            params['userId'] = user_id
        if media_type:
            params['mediaType'] = ','.join(media_type)
        if type:
            params['type'] = ','.join(type)
        if start_index is not None:
            params['startIndex'] = start_index
        if limit is not None:
            params['limit'] = limit
        if enable_total_record_count is not None:
            params['enableTotalRecordCount'] = enable_total_record_count
        return self._get('/Items/Suggestions', params)
    
    # =========================================================================
    # TRAILERS (1 endpoint)
    # =========================================================================
    
    def get_trailers(self, user_id: str = None, start_index: int = None,
                     limit: int = None, **kwargs) -> Optional[Dict]:
        """GET /Trailers - Get trailers"""
        params = {k: v for k, v in {
            'userId': user_id, 'startIndex': start_index, 'limit': limit, **kwargs
        }.items() if v is not None}
        return self._get('/Trailers', params)
