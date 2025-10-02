from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime

from models import HealthResponse, AuthUrlResponse, AuthResponse
from config import settings
from middleware import LoggingMiddleware, SecurityHeadersMiddleware, ErrorHandlingMiddleware
from oauth import spotify_oauth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Playlist Migrator API",
    description="A FastAPI template for playlist migration services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add custom middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting Playlist Migrator API...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down Playlist Migrator API...")

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with basic API information"""
    return HealthResponse(
        message="Playlist Migrator API is running",
        version="1.0.0",
        timestamp=datetime.utcnow(),
        status="healthy"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        message="Service is healthy",
        version="1.0.0",
        timestamp=datetime.utcnow(),
        status="healthy"
    )

# OAuth Routes 
# TODO move these to separate file
@app.get("/auth/spotify/login", response_model=AuthUrlResponse)
async def spotify_login():
    """Initiate Spotify OAuth flow"""
    try:
        auth_url, state = spotify_oauth.get_authorization_url()
        return AuthUrlResponse(auth_url=auth_url, state=state)
    except Exception as e:
        logger.error(f"Failed to generate Spotify auth URL: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate Spotify authentication")

@app.get("/auth/spotify/callback", response_model=AuthResponse)
async def spotify_callback(
    code: str = Query(..., description="Authorization code from Spotify"),
    state: str = Query(..., description="State parameter for security"),
    error: str = Query(None, description="Error from Spotify if any")
):
    """Handle Spotify OAuth callback"""
    try:
        # Check for OAuth errors
        if error:
            logger.error(f"Spotify OAuth error: {error}")
            return AuthResponse(
                success=False,
                message=f"Spotify authentication failed: {error}"
            )
        
        # Exchange code for token
        token = await spotify_oauth.exchange_code_for_token(code)
        if not token:
            return AuthResponse(
                success=False,
                message="Failed to exchange authorization code for access token"
            )
        
        # Get user profile
        user = await spotify_oauth.get_user_profile(token.access_token)
        if not user:
            return AuthResponse(
                success=False,
                message="Failed to retrieve user profile"
            )
        
        logger.info(f"Successfully authenticated user: {user.display_name} ({user.id})")
        
        return AuthResponse(
            success=True,
            message="Successfully authenticated with Spotify",
            user=user,
            access_token=token.access_token  # In production, store this securely
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in Spotify callback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during authentication")

@app.post("/auth/spotify/refresh", response_model=AuthResponse)
async def spotify_refresh_token(refresh_token: str):
    """Refresh Spotify access token"""
    try:
        token = await spotify_oauth.refresh_access_token(refresh_token)
        if not token:
            return AuthResponse(
                success=False,
                message="Failed to refresh access token"
            )
        
        # Get user profile with new token
        user = await spotify_oauth.get_user_profile(token.access_token)
        if not user:
            return AuthResponse(
                success=False,
                message="Failed to retrieve user profile with refreshed token"
            )
        
        return AuthResponse(
            success=True,
            message="Successfully refreshed access token",
            user=user,
            access_token=token.access_token
        )
        
    except Exception as e:
        logger.error(f"Unexpected error refreshing token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during token refresh")

@app.get("/spotify/playlists")
async def get_spotify_playlists(access_token: str = Query(..., description="Spotify access token")):
    """Get user's Spotify playlists"""
    try:
        playlists = await spotify_oauth.get_user_playlists(access_token)
        if playlists is None:
            raise HTTPException(status_code=400, detail="Failed to retrieve playlists")
        
        return {
            "success": True,
            "playlists": playlists,
            "count": len(playlists)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting playlists: {e}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving playlists")


@app.get("/spotify/playlist/{playlist_id}")
async def get_spotify_playlist(playlist_id: str):
    """Get a specific Spotify playlist"""
    try:
        # TODO implement the get_playlist function
        x = 1
        return x
        # playlist = await spotify_oauth.get_playlist(playlist_id)
        # return playlist
    except Exception as e:
        logger.error(f"Unexpected error getting playlist: {e}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving playlist")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
