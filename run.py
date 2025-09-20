#!/usr/bin/env python3
"""
Startup script for the Playlist Migrator API
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import settings

def main():
    """Main entry point for the application"""
    
    # Print startup information
    print("=" * 50)
    print(f"Starting {settings.APP_NAME}")
    print(f"Version: {settings.VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Host: {settings.HOST}")
    print(f"Port: {settings.PORT}")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = project_root / ".env"
    if not env_file.exists():
        print("Warning: .env file not found. Using default settings.")
        print("Copy env.example to .env and configure your settings.")
        print()
    
    # Start the server
    try:
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level=settings.LOG_LEVEL.lower(),
            access_log=True,
            reload_dirs=[str(project_root)] if settings.DEBUG else None
        )
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
