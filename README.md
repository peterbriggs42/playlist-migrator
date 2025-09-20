# Playlist Migrator API

A modern, production-ready FastAPI template for playlist migration services with comprehensive features including user management, playlist handling, and track management.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 📝 **Pydantic Models** - Data validation and serialization
- 🔧 **Configuration Management** - Environment-based settings
- 🛡️ **Security** - CORS, security headers, rate limiting
- 📊 **Logging** - Comprehensive request/response logging
- 🧪 **Testing Ready** - Structured for easy testing
- 📚 **Auto Documentation** - Interactive API docs with Swagger UI
- 🔄 **Error Handling** - Centralized error handling and responses

## Quick Start

### Prerequisites

- Python 3.8+
- pip or poetry

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd playlist-migrator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

   Or directly with uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Project Structure

```
playlist-migrator/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic models for data validation
├── config.py            # Configuration management
├── middleware.py        # Custom middleware (logging, security, rate limiting)
├── utils.py             # Utility functions
├── run.py               # Startup script
├── requirements.txt     # Python dependencies
├── env.example          # Environment variables template
└── README.md           # This file
```

## API Endpoints

### Health & Info
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

## Configuration

The application uses environment variables for configuration. Copy `env.example` to `.env` and modify as needed:

### Key Settings

- `ENVIRONMENT` - Set to `production`, `development`, or `testing`
- `DEBUG` - Enable/disable debug mode
- `SECRET_KEY` - Change in production!
- `ALLOWED_ORIGINS` - CORS allowed origins
- `DATABASE_URL` - Database connection string
- `REDIS_URL` - Redis connection string (optional)

## Development

### Code Style

The project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting

Run formatting:
```bash
black .
isort .
flake8 .
```

### Testing

Run tests (when implemented):
```bash
pytest
```

### Adding New Endpoints

1. Define Pydantic models in `models.py`
2. Add route handlers in `main.py`
3. Update this README with new endpoints

## Production Deployment

### Environment Setup

1. Set `ENVIRONMENT=production`
2. Set `DEBUG=false`
3. Change `SECRET_KEY` to a secure random string
4. Configure proper `ALLOWED_ORIGINS`
5. Set up database and Redis connections

### Docker (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run.py"]
```

### Security Considerations

- Change default `SECRET_KEY`
- Use HTTPS in production
- Configure proper CORS origins
- Set up rate limiting
- Use environment variables for secrets
- Enable security headers (already included)


## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue on GitHub.
