#!/usr/bin/env python3
"""
Discovery - Users Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class UsersDiscovery(DiscoveryBase):
    """Users group - ALLE Entities"""
    
    GROUP_NAME = 'users'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registered_users = set()
    
    def register_all(self):
        """Register ALLE user entities"""
        
        # =====================================================================
        # GET /Users - Users List
        # =====================================================================
        self.sensor("users_count", "Users Count", "users/count", "mdi:account-group")
        self.sensor("users_online_count", "Users Online", "users/online_count", "mdi:account-multiple-check")
        self.sensor("users_disabled_count", "Users Disabled", "users/disabled_count", "mdi:account-cancel")
        self.sensor("users_admin_count", "Admin Users", "users/admin_count", "mdi:shield-account")
        self.sensor("users_list", "Users List", "users/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /Users/Public - Public Users
        # =====================================================================
        self.sensor("public_users_count", "Public Users Count", "users/public/count", "mdi:account-multiple")
        self.sensor("public_users_list", "Public Users List", "users/public/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /Users/Me - Current User
        # =====================================================================
        self.sensor("current_user_name", "Current User Name", "users/me/Name", "mdi:account")
        self.sensor("current_user_id", "Current User ID", "users/me/Id", "mdi:identifier")
        self.sensor("current_user_server_id", "Current User Server ID", "users/me/ServerId", "mdi:server")
        self.binary_sensor("current_user_has_password", "Current User Has Password", "users/me/HasPassword", "mdi:lock")
        self.binary_sensor("current_user_has_configured_password", "Current User Configured Password", "users/me/HasConfiguredPassword", "mdi:lock-check")
        self.binary_sensor("current_user_has_configured_easy_password", "Current User Easy Password", "users/me/HasConfiguredEasyPassword", "mdi:lock-open")
        self.binary_sensor("current_user_enable_auto_login", "Current User Auto Login", "users/me/EnableAutoLogin", "mdi:login")
        self.sensor("current_user_last_login_date", "Current User Last Login", "users/me/LastLoginDate", "mdi:clock")
        self.sensor("current_user_last_activity_date", "Current User Last Activity", "users/me/LastActivityDate", "mdi:clock")
        
        # =====================================================================
        # POST /Users/New - Create User
        # =====================================================================
        self.button("create_user", "Create User", "users/command", "create", "mdi:account-plus")
        
        # =====================================================================
        # POST /Users/ForgotPassword - Forgot Password
        # =====================================================================
        self.button("forgot_password", "Forgot Password", "users/command", "forgot_password", "mdi:lock-question")
        
        # =====================================================================
        # POST /Users/ForgotPassword/Pin - Forgot Password Pin
        # =====================================================================
        self.button("forgot_password_pin", "Forgot Password Pin", "users/command", "forgot_password_pin", "mdi:lock-reset")
        
        # =====================================================================
        # GET /Users/Query - Query Users
        # =====================================================================
        self.sensor("query_users_total", "Query Users Total", "users/query/TotalRecordCount", "mdi:account-search")
        
        return self.entity_count
    
    def register_user(self, user_id, user_name, is_admin):
        """Register ALLE Entities für einen spezifischen User"""
        if user_id in self.registered_users:
            return 0
        
        safe_name = user_name.replace(" ", "_").lower()[:20]
        prefix = f"user_{safe_name}"
        base_topic = f"users/{user_id}"
        
        # =====================================================================
        # User Basic Info
        # =====================================================================
        self.sensor(f"{prefix}_name", f"{user_name}", f"{base_topic}/Name", "mdi:account")
        self.sensor(f"{prefix}_id", f"{user_name} ID", f"{base_topic}/Id", "mdi:identifier")
        self.sensor(f"{prefix}_server_id", f"{user_name} Server ID", f"{base_topic}/ServerId", "mdi:server")
        self.binary_sensor(f"{prefix}_has_password", f"{user_name} Has Password", f"{base_topic}/HasPassword", "mdi:lock")
        self.binary_sensor(f"{prefix}_has_configured_password", f"{user_name} Configured Password", f"{base_topic}/HasConfiguredPassword", "mdi:lock-check")
        self.binary_sensor(f"{prefix}_has_configured_easy_password", f"{user_name} Easy Password", f"{base_topic}/HasConfiguredEasyPassword", "mdi:lock-open")
        self.binary_sensor(f"{prefix}_enable_auto_login", f"{user_name} Auto Login", f"{base_topic}/EnableAutoLogin", "mdi:login")
        self.sensor(f"{prefix}_last_login_date", f"{user_name} Last Login", f"{base_topic}/LastLoginDate", "mdi:clock")
        self.sensor(f"{prefix}_last_activity_date", f"{user_name} Last Activity", f"{base_topic}/LastActivityDate", "mdi:clock")
        self.sensor(f"{prefix}_primary_image_tag", f"{user_name} Image Tag", f"{base_topic}/PrimaryImageTag", "mdi:image")
        
        # =====================================================================
        # User Policy
        # =====================================================================
        self.binary_sensor(f"{prefix}_is_admin", f"{user_name} Is Admin", f"{base_topic}/Policy/IsAdministrator", "mdi:shield-account")
        self.binary_sensor(f"{prefix}_is_hidden", f"{user_name} Is Hidden", f"{base_topic}/Policy/IsHidden", "mdi:eye-off")
        self.binary_sensor(f"{prefix}_is_hidden_remotely", f"{user_name} Is Hidden Remotely", f"{base_topic}/Policy/IsHiddenRemotely", "mdi:eye-off")
        self.binary_sensor(f"{prefix}_is_disabled", f"{user_name} Is Disabled", f"{base_topic}/Policy/IsDisabled", "mdi:account-cancel")
        self.sensor(f"{prefix}_max_parental_rating", f"{user_name} Max Rating", f"{base_topic}/Policy/MaxParentalRating", "mdi:account-child")
        self.sensor(f"{prefix}_blocked_tags", f"{user_name} Blocked Tags", f"{base_topic}/Policy/BlockedTags", "mdi:tag-off")
        self.binary_sensor(f"{prefix}_enable_user_preference_access", f"{user_name} Pref Access", f"{base_topic}/Policy/EnableUserPreferenceAccess", "mdi:cog")
        self.sensor(f"{prefix}_access_schedules", f"{user_name} Access Schedules", f"{base_topic}/Policy/AccessSchedules", "mdi:calendar")
        self.sensor(f"{prefix}_blocked_media_folders", f"{user_name} Blocked Folders", f"{base_topic}/Policy/BlockedMediaFolders", "mdi:folder-lock")
        self.sensor(f"{prefix}_enabled_devices", f"{user_name} Enabled Devices", f"{base_topic}/Policy/EnabledDevices", "mdi:devices")
        self.binary_sensor(f"{prefix}_enable_all_devices", f"{user_name} All Devices", f"{base_topic}/Policy/EnableAllDevices", "mdi:devices")
        self.sensor(f"{prefix}_enabled_channels", f"{user_name} Enabled Channels", f"{base_topic}/Policy/EnabledChannels", "mdi:television")
        self.binary_sensor(f"{prefix}_enable_all_channels", f"{user_name} All Channels", f"{base_topic}/Policy/EnableAllChannels", "mdi:television")
        self.sensor(f"{prefix}_enabled_folders", f"{user_name} Enabled Folders", f"{base_topic}/Policy/EnabledFolders", "mdi:folder-multiple")
        self.binary_sensor(f"{prefix}_enable_all_folders", f"{user_name} All Folders", f"{base_topic}/Policy/EnableAllFolders", "mdi:folder-multiple")
        self.sensor(f"{prefix}_invalid_login_attempt_count", f"{user_name} Invalid Logins", f"{base_topic}/Policy/InvalidLoginAttemptCount", "mdi:alert")
        self.sensor(f"{prefix}_login_attempts_before_lockout", f"{user_name} Login Attempts", f"{base_topic}/Policy/LoginAttemptsBeforeLockout", "mdi:lock")
        self.sensor(f"{prefix}_max_active_sessions", f"{user_name} Max Sessions", f"{base_topic}/Policy/MaxActiveSessions", "mdi:account-multiple")
        self.binary_sensor(f"{prefix}_enable_public_sharing", f"{user_name} Public Sharing", f"{base_topic}/Policy/EnablePublicSharing", "mdi:share")
        self.sensor(f"{prefix}_blocked_channels", f"{user_name} Blocked Channels", f"{base_topic}/Policy/BlockedChannels", "mdi:television-off")
        self.sensor(f"{prefix}_remote_client_bitrate_limit", f"{user_name} Bitrate Limit", f"{base_topic}/Policy/RemoteClientBitrateLimit", "mdi:speedometer")
        self.sensor(f"{prefix}_authentication_provider_id", f"{user_name} Auth Provider", f"{base_topic}/Policy/AuthenticationProviderId", "mdi:shield")
        self.sensor(f"{prefix}_password_reset_provider_id", f"{user_name} Password Provider", f"{base_topic}/Policy/PasswordResetProviderId", "mdi:lock-reset")
        self.sensor(f"{prefix}_sync_play_access", f"{user_name} SyncPlay Access", f"{base_topic}/Policy/SyncPlayAccess", "mdi:sync")
        
        # =====================================================================
        # User Permissions
        # =====================================================================
        self.binary_sensor(f"{prefix}_enable_audio_playback_transcoding", f"{user_name} Audio Transcode", f"{base_topic}/Policy/EnableAudioPlaybackTranscoding", "mdi:volume-high")
        self.binary_sensor(f"{prefix}_enable_video_playback_transcoding", f"{user_name} Video Transcode", f"{base_topic}/Policy/EnableVideoPlaybackTranscoding", "mdi:video")
        self.binary_sensor(f"{prefix}_enable_playback_remuxing", f"{user_name} Remuxing", f"{base_topic}/Policy/EnablePlaybackRemuxing", "mdi:video-switch")
        self.binary_sensor(f"{prefix}_force_remote_source_transcoding", f"{user_name} Force Remote Transcode", f"{base_topic}/Policy/ForceRemoteSourceTranscoding", "mdi:video-wireless")
        self.binary_sensor(f"{prefix}_enable_live_tv_management", f"{user_name} LiveTV Management", f"{base_topic}/Policy/EnableLiveTvManagement", "mdi:television")
        self.binary_sensor(f"{prefix}_enable_live_tv_access", f"{user_name} LiveTV Access", f"{base_topic}/Policy/EnableLiveTvAccess", "mdi:television-play")
        self.binary_sensor(f"{prefix}_enable_media_playback", f"{user_name} Media Playback", f"{base_topic}/Policy/EnableMediaPlayback", "mdi:play")
        self.binary_sensor(f"{prefix}_enable_content_deletion", f"{user_name} Content Deletion", f"{base_topic}/Policy/EnableContentDeletion", "mdi:delete")
        self.sensor(f"{prefix}_enable_content_deletion_from_folders", f"{user_name} Delete From Folders", f"{base_topic}/Policy/EnableContentDeletionFromFolders", "mdi:folder-remove")
        self.binary_sensor(f"{prefix}_enable_content_downloading", f"{user_name} Content Download", f"{base_topic}/Policy/EnableContentDownloading", "mdi:download")
        self.binary_sensor(f"{prefix}_enable_sync_transcoding", f"{user_name} Sync Transcoding", f"{base_topic}/Policy/EnableSyncTranscoding", "mdi:sync")
        self.binary_sensor(f"{prefix}_enable_media_conversion", f"{user_name} Media Conversion", f"{base_topic}/Policy/EnableMediaConversion", "mdi:swap-horizontal")
        self.binary_sensor(f"{prefix}_enable_remote_access", f"{user_name} Remote Access", f"{base_topic}/Policy/EnableRemoteAccess", "mdi:remote")
        self.binary_sensor(f"{prefix}_enable_remote_control_of_other_users", f"{user_name} Control Others", f"{base_topic}/Policy/EnableRemoteControlOfOtherUsers", "mdi:remote")
        self.binary_sensor(f"{prefix}_enable_shared_device_control", f"{user_name} Shared Device Control", f"{base_topic}/Policy/EnableSharedDeviceControl", "mdi:devices")
        self.binary_sensor(f"{prefix}_enable_collection_management", f"{user_name} Collection Mgmt", f"{base_topic}/Policy/EnableCollectionManagement", "mdi:folder-star")
        self.binary_sensor(f"{prefix}_enable_subtitle_management", f"{user_name} Subtitle Mgmt", f"{base_topic}/Policy/EnableSubtitleManagement", "mdi:subtitles")
        self.binary_sensor(f"{prefix}_enable_lyric_management", f"{user_name} Lyric Mgmt", f"{base_topic}/Policy/EnableLyricManagement", "mdi:microphone")
        
        # =====================================================================
        # User Configuration  
        # =====================================================================
        self.sensor(f"{prefix}_audio_language_preference", f"{user_name} Audio Lang", f"{base_topic}/Configuration/AudioLanguagePreference", "mdi:translate")
        self.binary_sensor(f"{prefix}_play_default_audio_track", f"{user_name} Default Audio", f"{base_topic}/Configuration/PlayDefaultAudioTrack", "mdi:volume-high")
        self.sensor(f"{prefix}_subtitle_language_preference", f"{user_name} Subtitle Lang", f"{base_topic}/Configuration/SubtitleLanguagePreference", "mdi:translate")
        self.binary_sensor(f"{prefix}_display_missing_episodes", f"{user_name} Missing Episodes", f"{base_topic}/Configuration/DisplayMissingEpisodes", "mdi:eye")
        self.sensor(f"{prefix}_grouped_folders", f"{user_name} Grouped Folders", f"{base_topic}/Configuration/GroupedFolders", "mdi:folder-multiple")
        self.sensor(f"{prefix}_subtitle_mode", f"{user_name} Subtitle Mode", f"{base_topic}/Configuration/SubtitleMode", "mdi:subtitles")
        self.binary_sensor(f"{prefix}_display_collections_view", f"{user_name} Collections View", f"{base_topic}/Configuration/DisplayCollectionsView", "mdi:folder-star")
        self.binary_sensor(f"{prefix}_enable_local_password", f"{user_name} Local Password", f"{base_topic}/Configuration/EnableLocalPassword", "mdi:lock")
        self.sensor(f"{prefix}_ordered_views", f"{user_name} Ordered Views", f"{base_topic}/Configuration/OrderedViews", "mdi:sort")
        self.sensor(f"{prefix}_latest_items_excludes", f"{user_name} Latest Excludes", f"{base_topic}/Configuration/LatestItemsExcludes", "mdi:eye-off")
        self.sensor(f"{prefix}_my_media_excludes", f"{user_name} Media Excludes", f"{base_topic}/Configuration/MyMediaExcludes", "mdi:eye-off")
        self.binary_sensor(f"{prefix}_hide_played_in_latest", f"{user_name} Hide Played", f"{base_topic}/Configuration/HidePlayedInLatest", "mdi:eye-off")
        self.binary_sensor(f"{prefix}_remember_audio_selections", f"{user_name} Remember Audio", f"{base_topic}/Configuration/RememberAudioSelections", "mdi:memory")
        self.binary_sensor(f"{prefix}_remember_subtitle_selections", f"{user_name} Remember Subs", f"{base_topic}/Configuration/RememberSubtitleSelections", "mdi:memory")
        self.binary_sensor(f"{prefix}_enable_next_episode_auto_play", f"{user_name} Auto Next", f"{base_topic}/Configuration/EnableNextEpisodeAutoPlay", "mdi:skip-next")
        self.sensor(f"{prefix}_cast_receiver_id", f"{user_name} Cast Receiver", f"{base_topic}/Configuration/CastReceiverId", "mdi:cast")
        
        # =====================================================================
        # User Stats (computed)
        # =====================================================================
        self.binary_sensor(f"{prefix}_online", f"{user_name} Online", f"{base_topic}/online", "mdi:account-check")
        self.sensor(f"{prefix}_active_session", f"{user_name} Active Session", f"{base_topic}/active_session", "mdi:play-circle")
        self.sensor(f"{prefix}_watch_count", f"{user_name} Watch Count", f"{base_topic}/watch_count", "mdi:eye")
        self.sensor(f"{prefix}_watch_time", f"{user_name} Watch Time", f"{base_topic}/watch_time", "mdi:clock")
        
        # =====================================================================
        # User Control Buttons
        # =====================================================================
        self.button(f"{prefix}_delete", f"Delete {user_name}", f"{base_topic}/command", "delete", "mdi:account-remove")
        self.button(f"{prefix}_reset_password", f"Reset {user_name} Password", f"{base_topic}/command", "reset_password", "mdi:lock-reset")
        self.button(f"{prefix}_update_policy", f"Update {user_name} Policy", f"{base_topic}/command", "update_policy", "mdi:cog")
        self.button(f"{prefix}_authenticate", f"Authenticate {user_name}", f"{base_topic}/command", "authenticate", "mdi:login")
        
        self.registered_users.add(user_id)
        return self.entity_count
