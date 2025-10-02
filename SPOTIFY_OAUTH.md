# Spotify OAuth Implementation

This document explains how to set up and use the Spotify OAuth flow in your FastAPI application.

## Setup

### 1. Create a Spotify App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the app details:
   - App name: Your app name
   - App description: Description of your app
   - Website: Your website URL
   - Redirect URI: `http://localhost:8000/auth/spotify/callback` (for development)
5. Accept the terms and create the app

### 2. Configure Environment Variables

Copy `env.example` to `.env` and update the following values:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8000/auth/spotify/callback
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## API Endpoints

### 1. Initiate OAuth Flow

**GET** `/auth/spotify/login`

Returns the Spotify authorization URL and state parameter.

**Response:**
```json
{
  "auth_url": "https://accounts.spotify.com/authorize?...",
  "state": "random_state_string"
}
```

### 2. OAuth Callback

**GET** `/auth/spotify/callback`

Handles the callback from Spotify after user authorization.

**Query Parameters:**
- `code`: Authorization code from Spotify
- `state`: State parameter for security
- `error`: Error message (if any)

**Response:**
```json
{
  "success": true,
  "message": "Successfully authenticated with Spotify",
  "user": {
    "id": "spotify_user_id",
    "display_name": "User Name",
    "email": "user@example.com",
    "country": "US",
    "product": "premium"
  },
  "access_token": "spotify_access_token"
}
```

### 3. Refresh Token

**POST** `/auth/spotify/refresh`

Refreshes an expired access token.

**Body:**
```json
{
  "refresh_token": "your_refresh_token"
}
```

### 4. Get User Playlists

**GET** `/spotify/playlists`

Retrieves the authenticated user's playlists.

**Query Parameters:**
- `access_token`: Valid Spotify access token

**Response:**
```json
{
  "success": true,
  "playlists": [...],
  "count": 10
}
```

## Usage Example

### Frontend Integration

```javascript
// 1. Get authorization URL
const response = await fetch('/auth/spotify/login');
const { auth_url } = await response.json();

// 2. Redirect user to Spotify
window.location.href = auth_url;

// 3. Handle callback (user will be redirected back to your app)
// The callback endpoint will return user data and access token
```

### Backend Usage

```python
from oauth import spotify_oauth

# Get user playlists
playlists = await spotify_oauth.get_user_playlists(access_token)

# Get user profile
user = await spotify_oauth.get_user_profile(access_token)

# Refresh token
new_token = await spotify_oauth.refresh_access_token(refresh_token)
```

## Security Considerations

1. **Store tokens securely**: In production, store access tokens in a secure database or session store
2. **Use HTTPS**: Always use HTTPS in production
3. **Validate state parameter**: The state parameter helps prevent CSRF attacks
4. **Token expiration**: Access tokens expire after 1 hour, use refresh tokens to get new ones
5. **Scope limitations**: Only request the scopes you actually need

## Scopes

The current implementation requests these scopes:
- `playlist-read-private`: Read user's private playlists
- `playlist-read-collaborative`: Read user's collaborative playlists
- `playlist-modify-public`: Modify user's public playlists
- `playlist-modify-private`: Modify user's private playlists
- `user-read-private`: Read user's subscription details
- `user-read-email`: Read user's email address

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- `400`: Bad request (invalid parameters)
- `401`: Unauthorized (invalid or expired token)
- `500`: Internal server error

All errors include descriptive messages to help with debugging.
