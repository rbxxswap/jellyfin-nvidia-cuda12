#!/usr/bin/env python3
"""
Jellyfin REST API Client
Handles all communication with Jellyfin server
"""

import logging
import requests
from config import get_config

logger = logging.getLogger(__name__)


class JellyfinAPI:
    """Jellyfin REST API Client"""
    
    def __init__(self):
        self.config = get_config()
        self.base_url = self.config.jellyfin_host.rstrip('/')
        self.api_key = self.config.jellyfin_api_key
        self.headers = {
            'X-Emby-Token': self.api_key,
            'Content-Type': 'application/json'
        }
        self._server_info_cache = None
    
    def _request(self, method, endpoint, **kwargs):
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method, 
                url, 
                headers=self.headers,
                params={'api_key': self.api_key},
                timeout=10,
                **kwargs
            )
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.Timeout:
            logger.error("API request timeout: %s", endpoint)
            return None
        except requests.exceptions.RequestException as e:
            logger.error("API request failed: %s - %s", endpoint, str(e))
            return None
    
    def get_system_info(self):
        """Get server system information"""
        result = self._request('GET', '/System/Info')
        if result:
            self._server_info_cache = result
        return result
    
    def get_public_info(self):
        """Get public server info (no auth required)"""
        return self._request('GET', '/System/Info/Public')
    
    def ping(self):
        """Check if server is responding"""
        try:
            response = requests.get(
                f"{self.base_url}/System/Ping",
                headers=self.headers,
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def get_sessions(self):
        """Get all active sessions"""
        result = self._request('GET', '/Sessions')
        return result if result else []
    
    def get_scheduled_tasks(self):
        """Get scheduled tasks status"""
        result = self._request('GET', '/ScheduledTasks')
        return result if result else []
    
    def get_running_tasks(self):
        """Get only running tasks"""
        tasks = self.get_scheduled_tasks()
        return [t for t in tasks if t.get('State') == 'Running']
    
    def get_activity_log(self, limit=10):
        """Get recent activity log entries"""
        result = self._request('GET', f'/System/ActivityLog/Entries?limit={limit}')
        return result.get('Items', []) if result else []
    
    def start_library_scan(self):
        """Trigger a library scan"""
        result = self._request('POST', '/Library/Refresh')
        if result is not None:
            logger.info("Library scan triggered")
            return True
        return False
    
    def send_playstate_command(self, session_id, command):
        """
        Send playstate command to a session
        Commands: PlayPause, Pause, Unpause, Stop, NextTrack, PreviousTrack
        """
        result = self._request(
            'POST', 
            f'/Sessions/{session_id}/Playing/{command}'
        )
        if result is not None:
            logger.info("Sent %s to session %s", command, session_id[:8])
            return True
        return False
    
    def send_seek_command(self, session_id, position_ticks):
        """Seek to position (in ticks, 10000 ticks = 1ms)"""
        result = self._request(
            'POST',
            f'/Sessions/{session_id}/Playing/Seek',
            params={'seekPositionTicks': position_ticks}
        )
        return result is not None
    
    def get_server_id(self):
        """Get server ID from cached info"""
        if self._server_info_cache:
            return self._server_info_cache.get('Id', 'unknown')
        info = self.get_system_info()
        return info.get('Id', 'unknown') if info else 'unknown'


def parse_session(session):
    """Parse session data into simplified format"""
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
