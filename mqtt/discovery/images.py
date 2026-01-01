#!/usr/bin/env python3
"""
Discovery - Images Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class ImagesDiscovery(DiscoveryBase):
    """Images group - ALLE Entities"""
    
    GROUP_NAME = 'images'
    
    def register_all(self):
        """Register ALLE image entities"""
        
        # =====================================================================
        # GET /Branding/Splashscreen - Splashscreen
        # =====================================================================
        self.sensor("splashscreen_url", "Splashscreen URL", "images/splashscreen/url", "mdi:image")
        self.binary_sensor("splashscreen_exists", "Splashscreen Exists", "images/splashscreen/exists", "mdi:image-check")
        
        # =====================================================================
        # POST /Branding/Splashscreen - Upload Splashscreen
        # =====================================================================
        self.button("upload_splashscreen", "Upload Splashscreen", "images/command", "upload_splashscreen", "mdi:image-plus")
        
        # =====================================================================
        # DELETE /Branding/Splashscreen - Delete Splashscreen
        # =====================================================================
        self.button("delete_splashscreen", "Delete Splashscreen", "images/command", "delete_splashscreen", "mdi:image-remove")
        
        # =====================================================================
        # GET /Images/General - General Images
        # =====================================================================
        self.sensor("general_images_count", "General Images Count", "images/general/count", "mdi:image-multiple")
        self.sensor("general_images_list", "General Images List", "images/general/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /Images/General/{name}/{type} - Get General Image
        # =====================================================================
        # Dynamic per image
        
        # =====================================================================
        # GET /Images/MediaInfo - Media Info Images
        # =====================================================================
        self.sensor("media_info_images_count", "Media Info Images Count", "images/mediainfo/count", "mdi:information")
        
        # =====================================================================
        # GET /Images/MediaInfo/{theme}/{name} - Get Media Info Image
        # =====================================================================
        # Dynamic per image
        
        # =====================================================================
        # GET /Images/Ratings - Rating Images
        # =====================================================================
        self.sensor("rating_images_count", "Rating Images Count", "images/ratings/count", "mdi:star")
        
        # =====================================================================
        # GET /Images/Ratings/{theme}/{name} - Get Rating Image
        # =====================================================================
        # Dynamic per image
        
        # =====================================================================
        # GET /Items/{itemId}/Images - Item Images
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # POST /Items/{itemId}/Images/{imageType} - Set Item Image
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # DELETE /Items/{itemId}/Images/{imageType} - Delete Item Image
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # POST /Items/{itemId}/Images/{imageType}/{imageIndex}/Index - Update Image Index
        # =====================================================================
        # Dynamic per item
        
        # =====================================================================
        # GET /Users/{userId}/Images/{imageType} - Get User Image
        # =====================================================================
        # Dynamic per user
        
        # =====================================================================
        # POST /Users/{userId}/Images/{imageType} - Set User Image
        # =====================================================================
        # Dynamic per user
        
        # =====================================================================
        # DELETE /Users/{userId}/Images/{imageType} - Delete User Image
        # =====================================================================
        # Dynamic per user
        
        # =====================================================================
        # GET /Items/{itemId}/RemoteImages - Remote Images
        # =====================================================================
        self.sensor("remote_images_count", "Remote Images Count", "images/remote/count", "mdi:cloud-download")
        
        # =====================================================================
        # GET /Items/{itemId}/RemoteImages/Providers - Remote Image Providers
        # =====================================================================
        self.sensor("remote_image_providers_count", "Remote Image Providers Count", "images/providers/count", "mdi:cloud-download")
        self.sensor("remote_image_providers_list", "Remote Image Providers List", "images/providers/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # POST /Items/{itemId}/RemoteImages/Download - Download Remote Image
        # =====================================================================
        self.button("download_remote_image", "Download Remote Image", "images/command", "download", "mdi:cloud-download")
        
        return self.entity_count
