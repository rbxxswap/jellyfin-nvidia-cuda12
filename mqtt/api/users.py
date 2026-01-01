#!/usr/bin/env python3
"""
Jellyfin API - Users Group
Endpoints: 26
- User, UserLibrary, UserViews
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class UsersAPI(JellyfinAPIBase):
    """Users API endpoints"""
    
    GROUP_NAME = 'users'
    
    def __init__(self, base_url: str, api_key: str):
        super().__init__(base_url, api_key)
        self._user_id_cache = None
    
    # =========================================================================
    # USER (14 endpoints)
    # =========================================================================
    
    def get_users(self, is_hidden: bool = None, is_disabled: bool = None) -> Optional[List]:
        """GET /Users - Get users"""
        params = {k: v for k, v in {'isHidden': is_hidden, 'isDisabled': is_disabled}.items() if v is not None}
        return self._get('/Users', params)
    
    def get_public_users(self) -> Optional[List]:
        """GET /Users/Public - Get public users"""
        return self._get('/Users/Public')
    
    def get_current_user(self) -> Optional[Dict]:
        """GET /Users/Me - Get current user"""
        return self._get('/Users/Me')
    
    def get_current_user_id(self) -> Optional[str]:
        """Get current user ID (cached)"""
        if self._user_id_cache:
            return self._user_id_cache
        me = self.get_current_user()
        if me:
            self._user_id_cache = me.get('Id')
            return self._user_id_cache
        return None
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """GET /Users/{userId} - Get user by ID"""
        return self._get(f'/Users/{user_id}')
    
    def delete_user(self, user_id: str) -> bool:
        """DELETE /Users/{userId} - Delete user"""
        return self._delete(f'/Users/{user_id}') is not None
    
    def create_user_by_name(self, name: str, password: str = None) -> Optional[Dict]:
        """POST /Users/New - Create user by name"""
        body = {'Name': name}
        if password:
            body['Password'] = password
        return self._post('/Users/New', json_data=body)
    
    def authenticate_user(self, username: str, pw: str) -> Optional[Dict]:
        """POST /Users/AuthenticateByName - Authenticate user"""
        return self._post('/Users/AuthenticateByName', json_data={
            'Username': username, 'Pw': pw
        })
    
    def authenticate_with_quick_connect(self, secret: str) -> Optional[Dict]:
        """POST /Users/AuthenticateWithQuickConnect - Authenticate with quick connect"""
        return self._post('/Users/AuthenticateWithQuickConnect',
                         json_data={'Secret': secret})
    
    def update_user_configuration(self, user_id: str = None, config: Dict = None) -> bool:
        """POST /Users/Configuration - Update user configuration"""
        params = {'userId': user_id} if user_id else {}
        return self._post('/Users/Configuration', params=params, json_data=config) is not None
    
    def update_user_password(self, user_id: str = None, current_pw: str = None,
                              new_pw: str = None, reset_password: bool = None) -> bool:
        """POST /Users/Password - Update user password"""
        params = {'userId': user_id} if user_id else {}
        body = {}
        if current_pw:
            body['CurrentPw'] = current_pw
        if new_pw:
            body['NewPw'] = new_pw
        if reset_password is not None:
            body['ResetPassword'] = reset_password
        return self._post('/Users/Password', params=params, json_data=body) is not None
    
    def forgot_password(self, entered_username: str) -> Optional[Dict]:
        """POST /Users/ForgotPassword - Initiate forgot password"""
        return self._post('/Users/ForgotPassword',
                         json_data={'EnteredUsername': entered_username})
    
    def forgot_password_pin(self, pin: str) -> Optional[Dict]:
        """POST /Users/ForgotPassword/Pin - Redeem forgot password pin"""
        return self._post('/Users/ForgotPassword/Pin', json_data={'Pin': pin})
    
    def update_user_policy(self, user_id: str, policy: Dict) -> bool:
        """POST /Users/{userId}/Policy - Update user policy"""
        return self._post(f'/Users/{user_id}/Policy', json_data=policy) is not None
    
    def create_user(self, name: str, password: str = None) -> Optional[Dict]:
        """POST /Users - Create user (legacy)"""
        body = {'Name': name}
        if password:
            body['Password'] = password
        return self._post('/Users', json_data=body)
    
    # =========================================================================
    # USER LIBRARY (10 endpoints)
    # =========================================================================
    
    def get_latest_media(self, user_id: str = None, parent_id: str = None,
                         include_item_types: List[str] = None, limit: int = None,
                         is_played: bool = None, enable_images: bool = None,
                         image_type_limit: int = None, **kwargs) -> Optional[List]:
        """GET /Items/Latest - Get latest media"""
        params = {}
        if user_id:
            params['userId'] = user_id
        if parent_id:
            params['parentId'] = parent_id
        if include_item_types:
            params['includeItemTypes'] = ','.join(include_item_types)
        if limit is not None:
            params['limit'] = limit
        if is_played is not None:
            params['isPlayed'] = is_played
        if enable_images is not None:
            params['enableImages'] = enable_images
        if image_type_limit is not None:
            params['imageTypeLimit'] = image_type_limit
        params.update({k: v for k, v in kwargs.items() if v is not None})
        return self._get('/Items/Latest', params)
    
    def get_root_folder(self, user_id: str = None) -> Optional[Dict]:
        """GET /Items/Root - Get root folder"""
        params = {'userId': user_id} if user_id else {}
        return self._get('/Items/Root', params)
    
    def get_item(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /Items/{itemId} - Get item"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}', params)
    
    def get_intros(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """GET /Items/{itemId}/Intros - Get intros"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/Intros', params)
    
    def get_local_trailers(self, item_id: str, user_id: str = None) -> Optional[List]:
        """GET /Items/{itemId}/LocalTrailers - Get local trailers"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/LocalTrailers', params)
    
    def get_special_features(self, item_id: str, user_id: str = None) -> Optional[List]:
        """GET /Items/{itemId}/SpecialFeatures - Get special features"""
        params = {'userId': user_id} if user_id else {}
        return self._get(f'/Items/{item_id}/SpecialFeatures', params)
    
    def mark_favorite(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """POST /UserFavoriteItems/{itemId} - Mark as favorite"""
        params = {'userId': user_id} if user_id else {}
        return self._post(f'/UserFavoriteItems/{item_id}', params=params)
    
    def unmark_favorite(self, item_id: str, user_id: str = None) -> Optional[Dict]:
        """DELETE /UserFavoriteItems/{itemId} - Unmark as favorite"""
        params = {'userId': user_id} if user_id else {}
        return self._delete(f'/UserFavoriteItems/{item_id}', params=params)
    
    def update_item_rating(self, item_id: str, likes: bool, user_id: str = None) -> Optional[Dict]:
        """POST /UserItems/{itemId}/Rating - Update item rating"""
        params = {'likes': likes}
        if user_id:
            params['userId'] = user_id
        return self._post(f'/UserItems/{item_id}/Rating', params=params)
    
    def delete_item_rating(self, item_id: str, user_id: str = None) -> bool:
        """DELETE /UserItems/{itemId}/Rating - Delete item rating"""
        params = {'userId': user_id} if user_id else {}
        return self._delete(f'/UserItems/{item_id}/Rating', params=params) is not None
    
    # =========================================================================
    # USER VIEWS (2 endpoints)
    # =========================================================================
    
    def get_user_views(self, user_id: str = None, include_external_content: bool = None,
                       preset_views: List[str] = None, include_hidden: bool = None) -> Optional[Dict]:
        """GET /UserViews - Get user views (libraries)"""
        params = {}
        if user_id:
            params['userId'] = user_id
        if include_external_content is not None:
            params['includeExternalContent'] = include_external_content
        if preset_views:
            params['presetViews'] = ','.join(preset_views)
        if include_hidden is not None:
            params['includeHidden'] = include_hidden
        return self._get('/UserViews', params)
    
    def get_grouping_options(self, user_id: str = None) -> Optional[List]:
        """GET /UserViews/GroupingOptions - Get grouping options"""
        params = {'userId': user_id} if user_id else {}
        return self._get('/UserViews/GroupingOptions', params)
