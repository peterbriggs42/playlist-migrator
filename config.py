from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional

class Settings(BaseSettings):
    """Application settings configuration"""
    
    # Application settings
    APP_NAME: str = "Playlist Migrator API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse comma-separated origins string into list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    # Database settings (for future use)
    DATABASE_URL: Optional[str] = None
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "playlist_migrator"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "password"
    
    # Redis settings (for caching, if needed)
    REDIS_URL: Optional[str] = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    
    # External API settings
    SPOTIFY_CLIENT_ID: Optional[str] = None
    SPOTIFY_CLIENT_SECRET: Optional[str] = None
    YOUTUBE_API_KEY: Optional[str] = None
    
    # OAuth settings
    SPOTIFY_REDIRECT_URI: str = "http://127.0.0.1:8000/auth/spotify/callback"
    SPOTIFY_SCOPES: str = "playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-read-private user-read-email"
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Environment-specific configurations
if settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "WARNING"
    # Override with production-specific settings
    settings.ALLOWED_ORIGINS = [
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ]
elif settings.ENVIRONMENT == "testing":
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
    # Use test database
    settings.DATABASE_NAME = f"{settings.DATABASE_NAME}_test"

# Validate required settings
def validate_settings():
    """Validate that all required settings are properly configured"""
    required_settings = [
        "SECRET_KEY",
        "APP_NAME",
        "VERSION"
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting):
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")
    
    # Validate secret key strength in production
    if settings.ENVIRONMENT == "production" and settings.SECRET_KEY == "your-secret-key-change-in-production":
        raise ValueError("SECRET_KEY must be changed in production environment")

# Run validation
try:
    validate_settings()
except ValueError as e:
    print(f"Configuration error: {e}")
    exit(1)
