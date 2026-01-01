#!/usr/bin/env python3
"""
Jellyfin API - Playstate Group
Endpoints: 9
- Playback reporting, mark played/unplayed
"""

from typing import Optional, Dict
from .base import JellyfinAPIBase


class PlaystateAPI(JellyfinAPIBase):
    """Playstate API endpoints"""
    
    GROUP_NAME = 'playstate'
    
    # =========================================================================
    # PLAYSTATE (9 endpoints)
    # =========================================================================
    
    def report_playback_start(self, session_id: str = None, item_id: str = None,
                               media_source_id: str = None, **kwargs) -> bool:
        """POST /Sessions/Playing - Report playback start"""
        body = {k: v for k, v in {
            'SessionId': session_id, 'ItemId': item_id,
            'MediaSourceId': media_source_id, **kwargs
        }.items() if v is not None}
        return self._post('/Sessions/Playing', json_data=body) is not None
    
    def report_playback_progress(self, session_id: str = None, item_id: str = None,
                                  media_source_id: str = None, position_ticks: int = None,
                                  is_paused: bool = None, is_muted: bool = None,
                                  **kwargs) -> bool:
        """POST /Sessions/Playing/Progress - Report playback progress"""
        body = {k: v for k, v in {
            'SessionId': session_id, 'ItemId': item_id,
            'MediaSourceId': media_source_id, 'PositionTicks': position_ticks,
            'IsPaused': is_paused, 'IsMuted': is_muted, **kwargs
        }.items() if v is not None}
        return self._post('/Sessions/Playing/Progress', json_data=body) is not None
    
    def report_playback_stopped(self, session_id: str = None, item_id: str = None,
                                 media_source_id: str = None, position_ticks: int = None,
                                 **kwargs) -> bool:
        """POST /Sessions/Playing/Stopped - Report playback stopped"""
        body = {k: v for k, v in {
            'SessionId': session_id, 'ItemId': item_id,
            'MediaSourceId': media_source_id, 'PositionTicks': position_ticks, **kwargs
        }.items() if v is not None}
        return self._post('/Sessions/Playing/Stopped', json_data=body) is not None
    
    def ping_playback_session(self, play_session_id: str) -> bool:
        """POST /Sessions/Playing/Ping - Ping playback session"""
        return self._post('/Sessions/Playing/Ping',
                         params={'playSessionId': play_session_id}) is not None
    
    def on_playback_start(self, item_id: str, media_source_id: str = None,
                          audio_stream_index: int = None, subtitle_stream_index: int = None,
                          play_method: str = None, live_stream_id: str = None,
                          play_session_id: str = None, can_seek: bool = None) -> bool:
        """POST /PlayingItems/{itemId} - Mark item playing"""
        params = {k: v for k, v in {
            'mediaSourceId': media_source_id, 'audioStreamIndex': audio_stream_index,
            'subtitleStreamIndex': subtitle_stream_index, 'playMethod': play_method,
            'liveStreamId': live_stream_id, 'playSessionId': play_session_id,
            'canSeek': can_seek
        }.items() if v is not None}
        return self._post(f'/PlayingItems/{item_id}', params=params) is not None
    
    def on_playback_progress(self, item_id: str, media_source_id: str = None,
                              position_ticks: int = None, audio_stream_index: int = None,
                              subtitle_stream_index: int = None, volume_level: int = None,
                              play_method: str = None, live_stream_id: str = None,
                              play_session_id: str = None, repeat_mode: str = None,
                              is_paused: bool = None, is_muted: bool = None) -> bool:
        """POST /PlayingItems/{itemId}/Progress - Report playback progress"""
        params = {k: v for k, v in {
            'mediaSourceId': media_source_id, 'positionTicks': position_ticks,
            'audioStreamIndex': audio_stream_index, 'subtitleStreamIndex': subtitle_stream_index,
            'volumeLevel': volume_level, 'playMethod': play_method,
            'liveStreamId': live_stream_id, 'playSessionId': play_session_id,
            'repeatMode': repeat_mode, 'isPaused': is_paused, 'isMuted': is_muted
        }.items() if v is not None}
        return self._post(f'/PlayingItems/{item_id}/Progress', params=params) is not None
    
    def on_playback_stopped(self, item_id: str, media_source_id: str = None,
                             next_media_type: str = None, position_ticks: int = None,
                             live_stream_id: str = None, play_session_id: str = None) -> bool:
        """DELETE /PlayingItems/{itemId} - Report playback stopped"""
        params = {k: v for k, v in {
            'mediaSourceId': media_source_id, 'nextMediaType': next_media_type,
            'positionTicks': position_ticks, 'liveStreamId': live_stream_id,
            'playSessionId': play_session_id
        }.items() if v is not None}
        return self._delete(f'/PlayingItems/{item_id}', params=params) is not None
    
    def mark_played(self, item_id: str, user_id: str = None, date_played: str = None) -> Optional[Dict]:
        """POST /UserPlayedItems/{itemId} - Mark item played"""
        params = {k: v for k, v in {'userId': user_id, 'datePlayed': date_played}.items() if v is not None}
        return self._post(f'/UserPlayedItems/{item_id}', params=params)
    
    def mark_unplayed(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """DELETE /UserPlayedItems/{itemId} - Mark item unplayed"""
        params = {'userId': user_id} if user_id else {}
        return self._delete(f'/UserPlayedItems/{item_id}', params=params)
