#!/usr/bin/env python3
"""
Jellyfin API - Sessions Group
Endpoints: 16
- Active sessions, commands, messages, playstate control
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class SessionsAPI(JellyfinAPIBase):
    """Sessions API endpoints"""
    
    GROUP_NAME = 'sessions'
    
    # =========================================================================
    # SESSION (16 endpoints)
    # =========================================================================
    
    def get_sessions(self, controllable_by_user_id: str = None,
                     device_id: str = None, active_within_seconds: int = None) -> Optional[List]:
        """GET /Sessions - Get active sessions"""
        params = {k: v for k, v in {
            'controllableByUserId': controllable_by_user_id,
            'deviceId': device_id, 'activeWithinSeconds': active_within_seconds
        }.items() if v is not None}
        result = self._get('/Sessions', params)
        return result if result else []
    
    def get_auth_providers(self) -> Optional[List]:
        """GET /Auth/Providers - Get auth providers"""
        return self._get('/Auth/Providers')
    
    def get_password_reset_providers(self) -> Optional[List]:
        """GET /Auth/PasswordResetProviders - Get password reset providers"""
        return self._get('/Auth/PasswordResetProviders')
    
    def post_capabilities(self, capabilities: Dict) -> bool:
        """POST /Sessions/Capabilities - Post session capabilities"""
        return self._post('/Sessions/Capabilities', json_data=capabilities) is not None
    
    def post_full_capabilities(self, capabilities: Dict) -> bool:
        """POST /Sessions/Capabilities/Full - Post full capabilities"""
        return self._post('/Sessions/Capabilities/Full', json_data=capabilities) is not None
    
    def logout(self) -> bool:
        """POST /Sessions/Logout - Logout current session"""
        return self._post('/Sessions/Logout') is not None
    
    def report_viewing(self, item_id: str, session_id: str = None) -> bool:
        """POST /Sessions/Viewing - Report item being viewed"""
        params = {'itemId': item_id}
        if session_id:
            params['sessionId'] = session_id
        return self._post('/Sessions/Viewing', params=params) is not None
    
    def send_general_command(self, session_id: str, command: Dict) -> bool:
        """POST /Sessions/{sessionId}/Command - Send general command"""
        return self._post(f'/Sessions/{session_id}/Command', json_data=command) is not None
    
    def send_command(self, session_id: str, command: str) -> bool:
        """POST /Sessions/{sessionId}/Command/{command} - Send simple command"""
        return self._post(f'/Sessions/{session_id}/Command/{command}') is not None
    
    def send_message(self, session_id: str, text: str, header: str = None,
                     timeout_ms: int = None) -> bool:
        """POST /Sessions/{sessionId}/Message - Send message to session"""
        body = {'Text': text}
        if header:
            body['Header'] = header
        if timeout_ms:
            body['TimeoutMs'] = timeout_ms
        return self._post(f'/Sessions/{session_id}/Message', json_data=body) is not None
    
    def send_play_command(self, session_id: str, item_ids: List[str],
                          play_command: str = 'PlayNow', start_position_ticks: int = None) -> bool:
        """POST /Sessions/{sessionId}/Playing - Send play command"""
        params = {
            'itemIds': ','.join(item_ids),
            'playCommand': play_command
        }
        if start_position_ticks is not None:
            params['startPositionTicks'] = start_position_ticks
        return self._post(f'/Sessions/{session_id}/Playing', params=params) is not None
    
    def send_playstate_command(self, session_id: str, command: str,
                                seek_position_ticks: int = None,
                                controlling_user_id: str = None) -> bool:
        """POST /Sessions/{sessionId}/Playing/{command} - Send playstate command
        Commands: PlayPause, Pause, Unpause, Stop, NextTrack, PreviousTrack, Seek
        """
        params = {}
        if seek_position_ticks is not None:
            params['seekPositionTicks'] = seek_position_ticks
        if controlling_user_id:
            params['controllingUserId'] = controlling_user_id
        return self._post(f'/Sessions/{session_id}/Playing/{command}', params=params) is not None
    
    def send_system_command(self, session_id: str, command: str) -> bool:
        """POST /Sessions/{sessionId}/System/{command} - Send system command"""
        return self._post(f'/Sessions/{session_id}/System/{command}') is not None
    
    def add_user_to_session(self, session_id: str, user_id: str) -> bool:
        """POST /Sessions/{sessionId}/User/{userId} - Add user to session"""
        return self._post(f'/Sessions/{session_id}/User/{user_id}') is not None
    
    def remove_user_from_session(self, session_id: str, user_id: str) -> bool:
        """DELETE /Sessions/{sessionId}/User/{userId} - Remove user from session"""
        return self._delete(f'/Sessions/{session_id}/User/{user_id}') is not None
    
    def display_content(self, session_id: str, item_type: str, item_id: str,
                        item_name: str) -> bool:
        """POST /Sessions/{sessionId}/Viewing - Display content on session"""
        return self._post(f'/Sessions/{session_id}/Viewing',
                         params={'itemType': item_type, 'itemId': item_id,
                                'itemName': item_name}) is not None


def parse_session(session: Dict) -> Dict:
    """Parse session data into simplified format for MQTT"""
    now_playing = session.get('NowPlayingItem', {})
    play_state = session.get('PlayState', {})
    
    # Determine state
    if now_playing:
        state = 'paused' if play_state.get('IsPaused') else 'playing'
    else:
        state = 'idle'
    
    # Calculate progress
    position_ticks = play_state.get('PositionTicks', 0) or 0
    duration_ticks = now_playing.get('RunTimeTicks', 0) or 0
    
    position_sec = position_ticks // 10_000_000
    duration_sec = duration_ticks // 10_000_000
    progress = int((position_ticks / duration_ticks * 100)) if duration_ticks > 0 else 0
    
    # Determine play method
    play_method = 'DirectPlay'
    transcode_reasons = session.get('TranscodingInfo', {}).get('TranscodeReasons', [])
    if transcode_reasons:
        play_method = 'Transcode'
    elif session.get('TranscodingInfo'):
        play_method = 'DirectStream'
    
    # Build media info
    media_type = now_playing.get('Type', '')
    media_info = {
        'title': now_playing.get('Name', ''),
        'type': media_type,
        'artist': '',
        'album': '',
        'series': '',
        'season': None,
        'episode': None,
    }
    
    if media_type == 'Episode':
        media_info['series'] = now_playing.get('SeriesName', '')
        media_info['season'] = now_playing.get('ParentIndexNumber')
        media_info['episode'] = now_playing.get('IndexNumber')
    elif media_type == 'Audio':
        media_info['artist'] = ', '.join(now_playing.get('Artists', []))
        media_info['album'] = now_playing.get('Album', '')
    
    return {
        'session_id': session.get('Id', ''),
        'user': session.get('UserName', 'Unknown'),
        'client': session.get('Client', 'Unknown'),
        'device': session.get('DeviceName', 'Unknown'),
        'device_id': session.get('DeviceId', ''),
        'state': state,
        'position': position_sec,
        'duration': duration_sec,
        'progress': progress,
        'play_method': play_method,
        'is_transcoding': play_method == 'Transcode',
        'media': media_info,
        'now_playing': bool(now_playing)
    }
