"""
Spotify OAuth utilities and helper functions
"""
import secrets
import httpx
import logging
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlencode

from config import settings
from models import SpotifyToken, SpotifyUser

logger = logging.getLogger(__name__)

class SpotifyOAuth:
    """Spotify OAuth client"""
    
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.redirect_uri = settings.SPOTIFY_REDIRECT_URI
        self.scopes = settings.SPOTIFY_SCOPES.split()
        
        if not self.client_id or not self.client_secret:
            logger.warning("Spotify OAuth credentials not configured")
    
    def get_authorization_url(self, state: Optional[str] = None) -> tuple[str, str]:
        """
        Generate Spotify authorization URL
        
        Returns:
            tuple: (authorization_url, state)
        """
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes),
            'state': state,
            'show_dialog': 'true'  # Force consent screen
        }
        
        auth_url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
        return auth_url, state
    
    async def exchange_code_for_token(self, code: str) -> Optional[SpotifyToken]:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from Spotify
            
        Returns:
            SpotifyToken or None if failed
        """
        if not self.client_id or not self.client_secret:
            logger.error("Spotify OAuth credentials not configured")
            return None
        
        token_url = "https://accounts.spotify.com/api/token"
        
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data, headers=headers)
                response.raise_for_status()
                
                token_data = response.json()
                
                # Calculate expiration timestamp
                expires_at = datetime.utcnow() + timedelta(seconds=token_data['expires_in'])
                
                return SpotifyToken(
                    access_token=token_data['access_token'],
                    token_type=token_data.get('token_type', 'Bearer'),
                    expires_in=token_data['expires_in'],
                    refresh_token=token_data.get('refresh_token'),
                    scope=token_data.get('scope'),
                    expires_at=expires_at
                )
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to exchange code for token: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during token exchange: {e}")
            return None
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[SpotifyToken]:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: Refresh token from previous authentication
            
        Returns:
            SpotifyToken or None if failed
        """
        if not self.client_id or not self.client_secret:
            logger.error("Spotify OAuth credentials not configured")
            return None
        
        token_url = "https://accounts.spotify.com/api/token"
        
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data, headers=headers)
                response.raise_for_status()
                
                token_data = response.json()
                
                # Calculate expiration timestamp
                expires_at = datetime.utcnow() + timedelta(seconds=token_data['expires_in'])
                
                return SpotifyToken(
                    access_token=token_data['access_token'],
                    token_type=token_data.get('token_type', 'Bearer'),
                    expires_in=token_data['expires_in'],
                    refresh_token=token_data.get('refresh_token', refresh_token),  # Keep old refresh token if not provided
                    scope=token_data.get('scope'),
                    expires_at=expires_at
                )
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to refresh access token: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {e}")
            return None
    
    async def get_user_profile(self, access_token: str) -> Optional[SpotifyUser]:
        """
        Get user profile from Spotify API
        
        Args:
            access_token: Valid Spotify access token
            
        Returns:
            SpotifyUser or None if failed
        """
        profile_url = "https://api.spotify.com/v1/me"
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(profile_url, headers=headers)
                response.raise_for_status()
                
                user_data = response.json()
                
                return SpotifyUser(
                    id=user_data['id'],
                    display_name=user_data.get('display_name'),
                    email=user_data.get('email'),
                    country=user_data.get('country'),
                    followers=user_data.get('followers'),
                    images=user_data.get('images'),
                    product=user_data.get('product')
                )
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to get user profile: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting user profile: {e}")
            return None
    
    async def get_user_playlists(self, access_token: str, limit: int = 50) -> Optional[list]:
        """
        Get user's playlists from Spotify API
        
        Args:
            access_token: Valid Spotify access token
            limit: Maximum number of playlists to retrieve
            
        Returns:
            List of playlists or None if failed
        """
        playlists_url = "https://api.spotify.com/v1/me/playlists"
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        params = {
            'limit': limit
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(playlists_url, headers=headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                return data.get('items', [])
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to get user playlists: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting user playlists: {e}")
            return None

# Global OAuth client instance
spotify_oauth = SpotifyOAuth()
