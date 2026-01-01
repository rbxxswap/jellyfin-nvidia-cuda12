#!/usr/bin/env python3
"""
Jellyfin API - LiveTv Group
Endpoints: 41
- Channels, Programs, Recordings, Timers, Tuners, Listings
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class LiveTvAPI(JellyfinAPIBase):
    """Live TV API endpoints"""
    
    GROUP_NAME = 'livetv'
    
    # =========================================================================
    # LIVE TV INFO (2 endpoints)
    # =========================================================================
    
    def get_livetv_info(self) -> Optional[Dict]:
        """GET /LiveTv/Info - Get live TV info"""
        return self._get('/LiveTv/Info')
    
    def get_guide_info(self) -> Optional[Dict]:
        """GET /LiveTv/GuideInfo - Get guide info"""
        return self._get('/LiveTv/GuideInfo')
    
    # =========================================================================
    # CHANNELS (3 endpoints)
    # =========================================================================
    
    def get_livetv_channels(self, channel_type: str = None, user_id: str = None,
                            start_index: int = None, limit: int = None,
                            is_favorite: bool = None, is_liked: bool = None,
                            is_disabled: bool = None, **kwargs) -> Optional[Dict]:
        """GET /LiveTv/Channels - Get live TV channels"""
        params = {k: v for k, v in {
            'type': channel_type, 'userId': user_id,
            'startIndex': start_index, 'limit': limit,
            'isFavorite': is_favorite, 'isLiked': is_liked,
            'isDisabled': is_disabled, **kwargs
        }.items() if v is not None}
        return self._get('/LiveTv/Channels', params)
    
    def get_livetv_channel(self, channel_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Channels/{channelId} - Get channel"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/LiveTv/Channels/{channel_id}', params)
    
    def get_channel_mapping_options(self, provider_id: str) -> Optional[Dict]:
        """GET /LiveTv/ChannelMappingOptions - Get channel mapping options"""
        return self._get('/LiveTv/ChannelMappingOptions', params={'providerId': provider_id})
    
    def set_channel_mapping(self, provider_id: str, tuner_channel_id: str,
                            provider_channel_id: str) -> bool:
        """POST /LiveTv/ChannelMappings - Set channel mapping"""
        return self._post('/LiveTv/ChannelMappings', json_data={
            'ProviderId': provider_id,
            'TunerChannelId': tuner_channel_id,
            'ProviderChannelId': provider_channel_id
        }) is not None
    
    # =========================================================================
    # PROGRAMS (4 endpoints)
    # =========================================================================
    
    def get_livetv_programs(self, channel_ids: List[str] = None,
                            user_id: str = None, min_start_date: str = None,
                            max_start_date: str = None, **kwargs) -> Optional[Dict]:
        """GET /LiveTv/Programs - Get programs"""
        params = {k: v for k, v in {
            'userId': user_id, 'minStartDate': min_start_date,
            'maxStartDate': max_start_date, **kwargs
        }.items() if v is not None}
        if channel_ids:
            params['channelIds'] = ','.join(channel_ids)
        return self._get('/LiveTv/Programs', params)
    
    def get_livetv_programs_post(self, body: Dict) -> Optional[Dict]:
        """POST /LiveTv/Programs - Get programs (POST version)"""
        return self._post('/LiveTv/Programs', json_data=body)
    
    def get_recommended_programs(self, user_id: str = None, limit: int = None,
                                  is_airing: bool = None, has_aired: bool = None,
                                  is_movie: bool = None, is_sports: bool = None,
                                  is_news: bool = None, is_kids: bool = None,
                                  is_series: bool = None) -> Optional[Dict]:
        """GET /LiveTv/Programs/Recommended - Get recommended programs"""
        params = {k: v for k, v in {
            'userId': user_id, 'limit': limit, 'isAiring': is_airing,
            'hasAired': has_aired, 'isMovie': is_movie, 'isSports': is_sports,
            'isNews': is_news, 'isKids': is_kids, 'isSeries': is_series
        }.items() if v is not None}
        return self._get('/LiveTv/Programs/Recommended', params)
    
    def get_livetv_program(self, program_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Programs/{programId} - Get program"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/LiveTv/Programs/{program_id}', params)
    
    # =========================================================================
    # RECORDINGS (7 endpoints)
    # =========================================================================
    
    def get_livetv_recordings(self, channel_id: str = None, user_id: str = None,
                              start_index: int = None, limit: int = None,
                              status: str = None, is_in_progress: bool = None,
                              **kwargs) -> Optional[Dict]:
        """GET /LiveTv/Recordings - Get recordings"""
        params = {k: v for k, v in {
            'channelId': channel_id, 'userId': user_id,
            'startIndex': start_index, 'limit': limit,
            'status': status, 'isInProgress': is_in_progress, **kwargs
        }.items() if v is not None}
        return self._get('/LiveTv/Recordings', params)
    
    def get_livetv_recording(self, recording_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Recordings/{recordingId} - Get recording"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/LiveTv/Recordings/{recording_id}', params)
    
    def delete_livetv_recording(self, recording_id: str) -> bool:
        """DELETE /LiveTv/Recordings/{recordingId} - Delete recording"""
        return self._delete(f'/LiveTv/Recordings/{recording_id}') is not None
    
    def get_recording_folders(self, user_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Recordings/Folders - Get recording folders"""
        params = {'userId': user_id} if user_id else {}
        return self._get('/LiveTv/Recordings/Folders', params)
    
    def get_recording_groups(self, user_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Recordings/Groups - Get recording groups"""
        params = {'userId': user_id} if user_id else {}
        return self._get('/LiveTv/Recordings/Groups', params)
    
    def get_recording_group(self, group_id: str) -> Optional[Dict]:
        """GET /LiveTv/Recordings/Groups/{groupId} - Get recording group"""
        return self._get(f'/LiveTv/Recordings/Groups/{group_id}')
    
    def get_recording_series(self, **kwargs) -> Optional[Dict]:
        """GET /LiveTv/Recordings/Series - Get recording series"""
        return self._get('/LiveTv/Recordings/Series', {k: v for k, v in kwargs.items() if v is not None})

    
    # =========================================================================
    # TIMERS (6 endpoints)
    # =========================================================================
    
    def get_livetv_timers(self, channel_id: str = None, series_timer_id: str = None,
                          is_active: bool = None, is_scheduled: bool = None) -> Optional[Dict]:
        """GET /LiveTv/Timers - Get timers"""
        params = {k: v for k, v in {
            'channelId': channel_id, 'seriesTimerId': series_timer_id,
            'isActive': is_active, 'isScheduled': is_scheduled
        }.items() if v is not None}
        return self._get('/LiveTv/Timers', params)
    
    def get_default_timer_info(self, program_id: str = None) -> Optional[Dict]:
        """GET /LiveTv/Timers/Defaults - Get default timer info"""
        params = {'programId': program_id} if program_id else {}
        return self._get('/LiveTv/Timers/Defaults', params)
    
    def get_livetv_timer(self, timer_id: str) -> Optional[Dict]:
        """GET /LiveTv/Timers/{timerId} - Get timer"""
        return self._get(f'/LiveTv/Timers/{timer_id}')
    
    def create_livetv_timer(self, timer_info: Dict) -> bool:
        """POST /LiveTv/Timers - Create timer"""
        return self._post('/LiveTv/Timers', json_data=timer_info) is not None
    
    def update_livetv_timer(self, timer_id: str, timer_info: Dict) -> bool:
        """POST /LiveTv/Timers/{timerId} - Update timer"""
        return self._post(f'/LiveTv/Timers/{timer_id}', json_data=timer_info) is not None
    
    def cancel_livetv_timer(self, timer_id: str) -> bool:
        """DELETE /LiveTv/Timers/{timerId} - Cancel timer"""
        return self._delete(f'/LiveTv/Timers/{timer_id}') is not None
    
    # =========================================================================
    # SERIES TIMERS (5 endpoints)
    # =========================================================================
    
    def get_series_timers(self, sort_by: str = None, sort_order: str = None) -> Optional[Dict]:
        """GET /LiveTv/SeriesTimers - Get series timers"""
        params = {k: v for k, v in {'sortBy': sort_by, 'sortOrder': sort_order}.items() if v is not None}
        return self._get('/LiveTv/SeriesTimers', params)
    
    def get_series_timer(self, timer_id: str) -> Optional[Dict]:
        """GET /LiveTv/SeriesTimers/{timerId} - Get series timer"""
        return self._get(f'/LiveTv/SeriesTimers/{timer_id}')
    
    def create_series_timer(self, timer_info: Dict) -> bool:
        """POST /LiveTv/SeriesTimers - Create series timer"""
        return self._post('/LiveTv/SeriesTimers', json_data=timer_info) is not None
    
    def update_series_timer(self, timer_id: str, timer_info: Dict) -> bool:
        """POST /LiveTv/SeriesTimers/{timerId} - Update series timer"""
        return self._post(f'/LiveTv/SeriesTimers/{timer_id}', json_data=timer_info) is not None
    
    def cancel_series_timer(self, timer_id: str) -> bool:
        """DELETE /LiveTv/SeriesTimers/{timerId} - Cancel series timer"""
        return self._delete(f'/LiveTv/SeriesTimers/{timer_id}') is not None
    
    # =========================================================================
    # TUNERS (5 endpoints)
    # =========================================================================
    
    def get_tuner_host_types(self) -> Optional[List]:
        """GET /LiveTv/TunerHosts/Types - Get tuner host types"""
        return self._get('/LiveTv/TunerHosts/Types')
    
    def discover_tuners(self, new_devices_only: bool = False) -> Optional[List]:
        """GET /LiveTv/Tuners/Discover - Discover tuners"""
        return self._get('/LiveTv/Tuners/Discover', params={'newDevicesOnly': new_devices_only})
    
    def add_tuner_host(self, tuner_info: Dict) -> Optional[Dict]:
        """POST /LiveTv/TunerHosts - Add tuner host"""
        return self._post('/LiveTv/TunerHosts', json_data=tuner_info)
    
    def delete_tuner_host(self, tuner_id: str) -> bool:
        """DELETE /LiveTv/TunerHosts - Delete tuner host"""
        return self._delete('/LiveTv/TunerHosts', params={'id': tuner_id}) is not None
    
    def reset_tuner(self, tuner_id: str) -> bool:
        """POST /LiveTv/Tuners/{tunerId}/Reset - Reset tuner"""
        return self._post(f'/LiveTv/Tuners/{tuner_id}/Reset') is not None
    
    # =========================================================================
    # LISTING PROVIDERS (5 endpoints)
    # =========================================================================
    
    def get_default_listing_provider(self) -> Optional[Dict]:
        """GET /LiveTv/ListingProviders/Default - Get default listing provider"""
        return self._get('/LiveTv/ListingProviders/Default')
    
    def get_lineups(self, listing_provider_id: str, country: str = None,
                    location: str = None) -> Optional[List]:
        """GET /LiveTv/ListingProviders/Lineups - Get lineups"""
        params = {'id': listing_provider_id}
        if country:
            params['country'] = country
        if location:
            params['location'] = location
        return self._get('/LiveTv/ListingProviders/Lineups', params)
    
    def add_listing_provider(self, provider_info: Dict, validate_listings: bool = False,
                             validate_login: bool = False) -> Optional[Dict]:
        """POST /LiveTv/ListingProviders - Add listing provider"""
        return self._post('/LiveTv/ListingProviders',
                         params={'validateListings': validate_listings,
                                'validateLogin': validate_login},
                         json_data=provider_info)
    
    def delete_listing_provider(self, provider_id: str) -> bool:
        """DELETE /LiveTv/ListingProviders - Delete listing provider"""
        return self._delete('/LiveTv/ListingProviders', params={'id': provider_id}) is not None
    
    def get_schedules_direct_countries(self) -> Optional[str]:
        """GET /LiveTv/ListingProviders/SchedulesDirect/Countries - Get SD countries"""
        return self._get('/LiveTv/ListingProviders/SchedulesDirect/Countries')
