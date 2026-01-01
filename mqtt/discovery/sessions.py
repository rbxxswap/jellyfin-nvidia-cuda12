#!/usr/bin/env python3
"""
Discovery - Sessions Group - ALLE ENTITIES
Für jeden Endpoint und jedes Feld
"""

from .base import DiscoveryBase


class SessionsDiscovery(DiscoveryBase):
    """Sessions group - ALLE Entities"""
    
    GROUP_NAME = 'sessions'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registered_sessions = set()
    
    def register_all(self):
        """Register ALLE session entities"""
        
        # =====================================================================
        # GET /Sessions - Session Counts
        # =====================================================================
        self.sensor("sessions_total", "Sessions Total", "sessions/count", "mdi:account-multiple")
        self.sensor("sessions_playing", "Sessions Playing", "sessions/playing_count", "mdi:play-circle")
        self.sensor("sessions_paused", "Sessions Paused", "sessions/paused_count", "mdi:pause-circle")
        self.sensor("sessions_idle", "Sessions Idle", "sessions/idle_count", "mdi:account-clock")
        self.sensor("sessions_transcoding", "Sessions Transcoding", "sessions/transcoding_count", "mdi:cog-sync")
        self.sensor("sessions_direct_play", "Sessions Direct Play", "sessions/direct_play_count", "mdi:play")
        self.sensor("sessions_direct_stream", "Sessions Direct Stream", "sessions/direct_stream_count", "mdi:play-network")
        self.binary_sensor("any_playing", "Any Playing", "sessions/any_playing", "mdi:play-circle")
        self.binary_sensor("any_transcoding", "Any Transcoding", "sessions/any_transcoding", "mdi:cog-sync")
        
        # =====================================================================
        # GET /Auth/Providers
        # =====================================================================
        self.sensor("auth_providers_count", "Auth Providers Count", "sessions/auth_providers/count", "mdi:shield-account")
        self.sensor("auth_providers_list", "Auth Providers List", "sessions/auth_providers/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /Auth/PasswordResetProviders  
        # =====================================================================
        self.sensor("password_reset_providers_count", "Password Reset Providers Count", "sessions/password_reset_providers/count", "mdi:lock-reset")
        self.sensor("password_reset_providers_list", "Password Reset Providers List", "sessions/password_reset_providers/list", "mdi:format-list-bulleted")
        
        return self.entity_count
    
    def register_session(self, session_id, device_name, user_name, client_name):
        """Register ALLE Entities für eine spezifische Session"""
        if session_id in self.registered_sessions:
            return 0
        
        short_id = session_id[:8]
        prefix = f"session_{short_id}"
        base_topic = f"sessions/{session_id}"
        
        # =====================================================================
        # Session Basic Info
        # =====================================================================
        self.sensor(f"{prefix}_id", f"{device_name} Session ID", f"{base_topic}/Id", "mdi:identifier")
        self.sensor(f"{prefix}_user_id", f"{device_name} User ID", f"{base_topic}/UserId", "mdi:account")
        self.sensor(f"{prefix}_user_name", f"{device_name} User Name", f"{base_topic}/UserName", "mdi:account")
        self.sensor(f"{prefix}_client", f"{device_name} Client", f"{base_topic}/Client", "mdi:application")
        self.sensor(f"{prefix}_device_name", f"{device_name} Device Name", f"{base_topic}/DeviceName", "mdi:devices")
        self.sensor(f"{prefix}_device_id", f"{device_name} Device ID", f"{base_topic}/DeviceId", "mdi:identifier")
        self.sensor(f"{prefix}_device_type", f"{device_name} Device Type", f"{base_topic}/DeviceType", "mdi:devices")
        self.sensor(f"{prefix}_app_version", f"{device_name} App Version", f"{base_topic}/ApplicationVersion", "mdi:tag")
        self.sensor(f"{prefix}_last_activity", f"{device_name} Last Activity", f"{base_topic}/LastActivityDate", "mdi:clock")
        self.sensor(f"{prefix}_last_playback_check_in", f"{device_name} Last Playback Check-in", f"{base_topic}/LastPlaybackCheckIn", "mdi:clock-check")
        
        # =====================================================================
        # Session State
        # =====================================================================
        self.sensor(f"{prefix}_state", f"{device_name} State", f"{base_topic}/state", "mdi:play-circle")
        self.binary_sensor(f"{prefix}_is_active", f"{device_name} Is Active", f"{base_topic}/IsActive", "mdi:account-check")
        self.binary_sensor(f"{prefix}_supports_media_control", f"{device_name} Supports Media Control", f"{base_topic}/SupportsMediaControl", "mdi:remote")
        self.binary_sensor(f"{prefix}_supports_remote_control", f"{device_name} Supports Remote Control", f"{base_topic}/SupportsRemoteControl", "mdi:remote")
        
        # =====================================================================
        # PlayState
        # =====================================================================
        self.binary_sensor(f"{prefix}_is_paused", f"{device_name} Is Paused", f"{base_topic}/PlayState/IsPaused", "mdi:pause")
        self.binary_sensor(f"{prefix}_is_muted", f"{device_name} Is Muted", f"{base_topic}/PlayState/IsMuted", "mdi:volume-mute")
        self.sensor(f"{prefix}_position_ticks", f"{device_name} Position Ticks", f"{base_topic}/PlayState/PositionTicks", "mdi:timer")
        self.sensor(f"{prefix}_position", f"{device_name} Position", f"{base_topic}/position", "mdi:timer-outline")
        self.sensor(f"{prefix}_volume", f"{device_name} Volume", f"{base_topic}/PlayState/VolumeLevel", "mdi:volume-high", unit="%")
        self.sensor(f"{prefix}_audio_stream_index", f"{device_name} Audio Stream", f"{base_topic}/PlayState/AudioStreamIndex", "mdi:volume-high")
        self.sensor(f"{prefix}_subtitle_stream_index", f"{device_name} Subtitle Stream", f"{base_topic}/PlayState/SubtitleStreamIndex", "mdi:subtitles")
        self.sensor(f"{prefix}_media_source_id", f"{device_name} Media Source ID", f"{base_topic}/PlayState/MediaSourceId", "mdi:identifier")
        self.sensor(f"{prefix}_play_method", f"{device_name} Play Method", f"{base_topic}/PlayState/PlayMethod", "mdi:play-network")
        self.sensor(f"{prefix}_repeat_mode", f"{device_name} Repeat Mode", f"{base_topic}/PlayState/RepeatMode", "mdi:repeat")
        self.sensor(f"{prefix}_playback_order", f"{device_name} Playback Order", f"{base_topic}/PlayState/PlaybackOrder", "mdi:shuffle")
        self.sensor(f"{prefix}_progress", f"{device_name} Progress", f"{base_topic}/progress", "mdi:percent", unit="%")
        self.sensor(f"{prefix}_duration", f"{device_name} Duration", f"{base_topic}/duration", "mdi:timer")
        
        # =====================================================================
        # NowPlayingItem
        # =====================================================================
        self.sensor(f"{prefix}_now_playing_name", f"{device_name} Now Playing", f"{base_topic}/NowPlayingItem/Name", "mdi:filmstrip")
        self.sensor(f"{prefix}_now_playing_id", f"{device_name} Now Playing ID", f"{base_topic}/NowPlayingItem/Id", "mdi:identifier")
        self.sensor(f"{prefix}_now_playing_type", f"{device_name} Media Type", f"{base_topic}/NowPlayingItem/Type", "mdi:tag")
        self.sensor(f"{prefix}_now_playing_media_type", f"{device_name} Media Type 2", f"{base_topic}/NowPlayingItem/MediaType", "mdi:tag")
        self.sensor(f"{prefix}_now_playing_runtime", f"{device_name} Runtime", f"{base_topic}/NowPlayingItem/RunTimeTicks", "mdi:timer")
        self.sensor(f"{prefix}_now_playing_year", f"{device_name} Year", f"{base_topic}/NowPlayingItem/ProductionYear", "mdi:calendar")
        self.sensor(f"{prefix}_now_playing_series", f"{device_name} Series", f"{base_topic}/NowPlayingItem/SeriesName", "mdi:television-classic")
        self.sensor(f"{prefix}_now_playing_series_id", f"{device_name} Series ID", f"{base_topic}/NowPlayingItem/SeriesId", "mdi:identifier")
        self.sensor(f"{prefix}_now_playing_season", f"{device_name} Season", f"{base_topic}/NowPlayingItem/ParentIndexNumber", "mdi:numeric")
        self.sensor(f"{prefix}_now_playing_episode", f"{device_name} Episode", f"{base_topic}/NowPlayingItem/IndexNumber", "mdi:numeric")
        self.sensor(f"{prefix}_now_playing_album", f"{device_name} Album", f"{base_topic}/NowPlayingItem/Album", "mdi:album")
        self.sensor(f"{prefix}_now_playing_album_id", f"{device_name} Album ID", f"{base_topic}/NowPlayingItem/AlbumId", "mdi:identifier")
        self.sensor(f"{prefix}_now_playing_artists", f"{device_name} Artists", f"{base_topic}/NowPlayingItem/Artists", "mdi:account-music")
        self.sensor(f"{prefix}_now_playing_overview", f"{device_name} Overview", f"{base_topic}/NowPlayingItem/Overview", "mdi:text")
        self.sensor(f"{prefix}_now_playing_container", f"{device_name} Container", f"{base_topic}/NowPlayingItem/Container", "mdi:file-video")
        self.binary_sensor(f"{prefix}_now_playing_has_subtitles", f"{device_name} Has Subtitles", f"{base_topic}/NowPlayingItem/HasSubtitles", "mdi:subtitles")
        
        # =====================================================================
        # TranscodingInfo
        # =====================================================================
        self.binary_sensor(f"{prefix}_is_transcoding", f"{device_name} Is Transcoding", f"{base_topic}/is_transcoding", "mdi:cog-sync")
        self.sensor(f"{prefix}_transcode_audio_codec", f"{device_name} Transcode Audio Codec", f"{base_topic}/TranscodingInfo/AudioCodec", "mdi:volume-high")
        self.sensor(f"{prefix}_transcode_video_codec", f"{device_name} Transcode Video Codec", f"{base_topic}/TranscodingInfo/VideoCodec", "mdi:video")
        self.sensor(f"{prefix}_transcode_container", f"{device_name} Transcode Container", f"{base_topic}/TranscodingInfo/Container", "mdi:file-video")
        self.binary_sensor(f"{prefix}_transcode_is_video_direct", f"{device_name} Video Direct", f"{base_topic}/TranscodingInfo/IsVideoDirect", "mdi:video")
        self.binary_sensor(f"{prefix}_transcode_is_audio_direct", f"{device_name} Audio Direct", f"{base_topic}/TranscodingInfo/IsAudioDirect", "mdi:volume-high")
        self.sensor(f"{prefix}_transcode_bitrate", f"{device_name} Transcode Bitrate", f"{base_topic}/TranscodingInfo/Bitrate", "mdi:speedometer", unit="kbps")
        self.sensor(f"{prefix}_transcode_framerate", f"{device_name} Transcode Framerate", f"{base_topic}/TranscodingInfo/Framerate", "mdi:filmstrip", unit="fps")
        self.sensor(f"{prefix}_transcode_completion", f"{device_name} Transcode Completion", f"{base_topic}/TranscodingInfo/CompletionPercentage", "mdi:percent", unit="%")
        self.sensor(f"{prefix}_transcode_width", f"{device_name} Transcode Width", f"{base_topic}/TranscodingInfo/Width", "mdi:arrow-left-right")
        self.sensor(f"{prefix}_transcode_height", f"{device_name} Transcode Height", f"{base_topic}/TranscodingInfo/Height", "mdi:arrow-up-down")
        self.sensor(f"{prefix}_transcode_audio_channels", f"{device_name} Audio Channels", f"{base_topic}/TranscodingInfo/AudioChannels", "mdi:surround-sound")
        self.sensor(f"{prefix}_transcode_hw_type", f"{device_name} HW Accel Type", f"{base_topic}/TranscodingInfo/HardwareAccelerationType", "mdi:expansion-card")
        self.sensor(f"{prefix}_transcode_reasons", f"{device_name} Transcode Reasons", f"{base_topic}/TranscodingInfo/TranscodeReasons", "mdi:information")
        
        # =====================================================================
        # Session Control Buttons
        # =====================================================================
        self.button(f"{prefix}_play", f"{device_name} Play", f"{base_topic}/command", "play", "mdi:play")
        self.button(f"{prefix}_pause", f"{device_name} Pause", f"{base_topic}/command", "pause", "mdi:pause")
        self.button(f"{prefix}_playpause", f"{device_name} Play/Pause", f"{base_topic}/command", "playpause", "mdi:play-pause")
        self.button(f"{prefix}_stop", f"{device_name} Stop", f"{base_topic}/command", "stop", "mdi:stop")
        self.button(f"{prefix}_next", f"{device_name} Next Track", f"{base_topic}/command", "next", "mdi:skip-next")
        self.button(f"{prefix}_previous", f"{device_name} Previous Track", f"{base_topic}/command", "previous", "mdi:skip-previous")
        self.button(f"{prefix}_seek_forward", f"{device_name} Seek Forward", f"{base_topic}/command", "seek_forward", "mdi:fast-forward")
        self.button(f"{prefix}_seek_backward", f"{device_name} Seek Backward", f"{base_topic}/command", "seek_backward", "mdi:rewind")
        self.button(f"{prefix}_mute", f"{device_name} Mute", f"{base_topic}/command", "mute", "mdi:volume-mute")
        self.button(f"{prefix}_unmute", f"{device_name} Unmute", f"{base_topic}/command", "unmute", "mdi:volume-high")
        self.button(f"{prefix}_toggle_mute", f"{device_name} Toggle Mute", f"{base_topic}/command", "toggle_mute", "mdi:volume-off")
        self.button(f"{prefix}_volume_up", f"{device_name} Volume Up", f"{base_topic}/command", "volume_up", "mdi:volume-plus")
        self.button(f"{prefix}_volume_down", f"{device_name} Volume Down", f"{base_topic}/command", "volume_down", "mdi:volume-minus")
        
        # =====================================================================
        # Volume Number Slider
        # =====================================================================
        self.number(f"{prefix}_volume_set", f"{device_name} Volume", f"{base_topic}/PlayState/VolumeLevel", 
                   f"{base_topic}/volume/set", 0, 100, 1, "mdi:volume-high", unit="%")
        
        # =====================================================================
        # Seek Number Slider
        # =====================================================================
        self.number(f"{prefix}_seek_position", f"{device_name} Seek Position", f"{base_topic}/position_seconds",
                   f"{base_topic}/seek/set", 0, 86400, 1, "mdi:timer", unit="s")
        
        # =====================================================================
        # Message Text Input
        # =====================================================================
        self.text(f"{prefix}_message", f"{device_name} Send Message", f"{base_topic}/message/text",
                 f"{base_topic}/message/send", "mdi:message-text")
        
        self.registered_sessions.add(session_id)
        return self.entity_count
    
    def unregister_session(self, session_id):
        """Remove ALL session entities"""
        if session_id not in self.registered_sessions:
            return
        
        short_id = session_id[:8]
        prefix = f"session_{short_id}"
        
        # ALL entity suffixes
        entities = [
            ('sensor', 'id'), ('sensor', 'user_id'), ('sensor', 'user_name'), ('sensor', 'client'),
            ('sensor', 'device_name'), ('sensor', 'device_id'), ('sensor', 'device_type'), ('sensor', 'app_version'),
            ('sensor', 'last_activity'), ('sensor', 'last_playback_check_in'), ('sensor', 'state'),
            ('binary_sensor', 'is_active'), ('binary_sensor', 'supports_media_control'), ('binary_sensor', 'supports_remote_control'),
            ('binary_sensor', 'is_paused'), ('binary_sensor', 'is_muted'), ('sensor', 'position_ticks'),
            ('sensor', 'position'), ('sensor', 'volume'), ('sensor', 'audio_stream_index'), ('sensor', 'subtitle_stream_index'),
            ('sensor', 'media_source_id'), ('sensor', 'play_method'), ('sensor', 'repeat_mode'), ('sensor', 'playback_order'),
            ('sensor', 'progress'), ('sensor', 'duration'),
            ('sensor', 'now_playing_name'), ('sensor', 'now_playing_id'), ('sensor', 'now_playing_type'),
            ('sensor', 'now_playing_media_type'), ('sensor', 'now_playing_runtime'), ('sensor', 'now_playing_year'),
            ('sensor', 'now_playing_series'), ('sensor', 'now_playing_series_id'), ('sensor', 'now_playing_season'),
            ('sensor', 'now_playing_episode'), ('sensor', 'now_playing_album'), ('sensor', 'now_playing_album_id'),
            ('sensor', 'now_playing_artists'), ('sensor', 'now_playing_overview'), ('sensor', 'now_playing_container'),
            ('binary_sensor', 'now_playing_has_subtitles'),
            ('binary_sensor', 'is_transcoding'), ('sensor', 'transcode_audio_codec'), ('sensor', 'transcode_video_codec'),
            ('sensor', 'transcode_container'), ('binary_sensor', 'transcode_is_video_direct'), ('binary_sensor', 'transcode_is_audio_direct'),
            ('sensor', 'transcode_bitrate'), ('sensor', 'transcode_framerate'), ('sensor', 'transcode_completion'),
            ('sensor', 'transcode_width'), ('sensor', 'transcode_height'), ('sensor', 'transcode_audio_channels'),
            ('sensor', 'transcode_hw_type'), ('sensor', 'transcode_reasons'),
            ('button', 'play'), ('button', 'pause'), ('button', 'playpause'), ('button', 'stop'),
            ('button', 'next'), ('button', 'previous'), ('button', 'seek_forward'), ('button', 'seek_backward'),
            ('button', 'mute'), ('button', 'unmute'), ('button', 'toggle_mute'), ('button', 'volume_up'), ('button', 'volume_down'),
            ('number', 'volume_set'), ('number', 'seek_position'), ('text', 'message')
        ]
        
        for component, suffix in entities:
            self._remove(component, f"{prefix}_{suffix}")
        
        self.registered_sessions.discard(session_id)
    
    def cleanup_stale_sessions(self, active_session_ids):
        """Cleanup sessions that are no longer active"""
        stale = self.registered_sessions - set(active_session_ids)
        for session_id in stale:
            self.unregister_session(session_id)
