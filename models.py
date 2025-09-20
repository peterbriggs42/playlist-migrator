from pydantic import BaseModel, Field
from typing import Optional
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
