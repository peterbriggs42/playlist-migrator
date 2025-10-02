from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class HealthResponse(BaseModel):
    """Health check response model"""
    message: str = Field(..., description="Health status message")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Response timestamp")
    status: str = Field(..., description="Service status")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(..., description="Error timestamp")
    details: Optional[dict] = Field(None, description="Additional error details")

# OAuth Models
class SpotifyToken(BaseModel):
    """Spotify OAuth token model"""
    access_token: str = Field(..., description="Spotify access token")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    refresh_token: Optional[str] = Field(None, description="Refresh token")
    scope: Optional[str] = Field(None, description="Granted scopes")
    expires_at: Optional[datetime] = Field(None, description="Token expiration timestamp")

class SpotifyUser(BaseModel):
    """Spotify user profile model"""
    id: str = Field(..., description="Spotify user ID")
    display_name: Optional[str] = Field(None, description="User's display name")
    email: Optional[str] = Field(None, description="User's email")
    country: Optional[str] = Field(None, description="User's country")
    followers: Optional[Dict[str, Any]] = Field(None, description="User's followers info")
    images: Optional[list] = Field(None, description="User's profile images")
    product: Optional[str] = Field(None, description="User's subscription type")

class AuthResponse(BaseModel):
    """Authentication response model"""
    success: bool = Field(..., description="Authentication success status")
    message: str = Field(..., description="Response message")
    user: Optional[SpotifyUser] = Field(None, description="User profile data")
    access_token: Optional[str] = Field(None, description="Access token (if needed)")

class AuthUrlResponse(BaseModel):
    """Authentication URL response model"""
    auth_url: str = Field(..., description="Spotify authorization URL")
    state: str = Field(..., description="OAuth state parameter for security")

class PlaylistBase(BaseModel):
    """Base playlist model"""
    name: str = Field(..., min_length=1, max_length=200, description="Playlist name")
    description: Optional[str] = Field(None, max_length=500, description="Playlist description")
    is_public: bool = Field(default=False, description="Whether playlist is public")

class PlaylistCreate(PlaylistBase):
    """Model for creating a new playlist"""
    pass

class PlaylistUpdate(BaseModel):
    """Model for updating a playlist"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Playlist name")
    description: Optional[str] = Field(None, max_length=500, description="Playlist description")
    is_public: Optional[bool] = Field(None, description="Whether playlist is public")

class Playlist(PlaylistBase):
    """Complete playlist model"""
    id: int = Field(..., description="Unique playlist identifier")
    owner_id: int = Field(..., description="ID of the playlist owner")
    created_at: datetime = Field(..., description="Playlist creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Playlist last update timestamp")
    track_count: int = Field(default=0, description="Number of tracks in playlist")
    
    class Config:
        from_attributes = True

class PlaylistResponse(PlaylistBase):
    """Playlist response model for API responses"""
    id: int = Field(..., description="Unique playlist identifier")
    owner_id: int = Field(..., description="ID of the playlist owner")
    created_at: datetime = Field(..., description="Playlist creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Playlist last update timestamp")
    track_count: int = Field(default=0, description="Number of tracks in playlist")
    
    class Config:
        from_attributes = True

class TrackBase(BaseModel):
    """Base track model"""
    title: str = Field(..., min_length=1, max_length=200, description="Track title")
    artist: str = Field(..., min_length=1, max_length=200, description="Track artist")
    album: Optional[str] = Field(None, max_length=200, description="Track album")
    duration: Optional[int] = Field(None, ge=0, description="Track duration in seconds")
    external_id: Optional[str] = Field(None, description="External service track ID")

class TrackCreate(TrackBase):
    """Model for creating a new track"""
    pass

class Track(TrackBase):
    """Complete track model"""
    id: int = Field(..., description="Unique track identifier")
    playlist_id: int = Field(..., description="ID of the playlist containing this track")
    position: int = Field(..., ge=0, description="Position in playlist")
    added_at: datetime = Field(..., description="When track was added to playlist")
    
    class Config:
        from_attributes = True

class TrackResponse(TrackBase):
    """Track response model for API responses"""
    id: int = Field(..., description="Unique track identifier")
    playlist_id: int = Field(..., description="ID of the playlist containing this track")
    position: int = Field(..., ge=0, description="Position in playlist")
    added_at: datetime = Field(..., description="When track was added to playlist")
    
    class Config:
        from_attributes = True
