from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import hashlib
import secrets
import string
import re
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def generate_api_key(length: int = 32) -> str:
    """Generate a secure API key"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 (in production, use bcrypt or similar)"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(password) == hashed_password

def is_valid_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize string input"""
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', text)
    
    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object to string"""
    return dt.strftime(format_str)

def parse_datetime(date_string: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """Parse string to datetime object"""
    try:
        return datetime.strptime(date_string, format_str)
    except ValueError:
        return None

def get_utc_now() -> datetime:
    """Get current UTC datetime"""
    return datetime.utcnow()

def add_timezone_awareness(dt: datetime) -> datetime:
    """Add timezone awareness to datetime (assumes UTC)"""
    from datetime import timezone
    return dt.replace(tzinfo=timezone.utc)

def calculate_age(birth_date: datetime) -> int:
    """Calculate age from birth date"""
    today = datetime.utcnow()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def paginate_results(items: list, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """Paginate a list of items"""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_items = items[start:end]
    
    return {
        "items": paginated_items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
        "has_next": end < total,
        "has_prev": page > 1
    }

def retry_on_exception(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry function on exception"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        import asyncio
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed")
            
            raise last_exception
        return wrapper
    return decorator

def validate_pagination_params(page: int, per_page: int, max_per_page: int = 100) -> tuple[int, int]:
    """Validate and normalize pagination parameters"""
    page = max(1, page)
    per_page = max(1, min(per_page, max_per_page))
    return page, per_page

def create_response_metadata(
    total: int,
    page: int,
    per_page: int,
    **kwargs
) -> Dict[str, Any]:
    """Create standardized response metadata"""
    pages = (total + per_page - 1) // per_page
    
    return {
        "pagination": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1
        },
        **kwargs
    }

def mask_sensitive_data(data: Dict[str, Any], sensitive_fields: list = None) -> Dict[str, Any]:
    """Mask sensitive data in dictionaries"""
    if sensitive_fields is None:
        sensitive_fields = ["password", "token", "secret", "key", "api_key"]
    
    masked_data = data.copy()
    
    for key, value in masked_data.items():
        if any(field in key.lower() for field in sensitive_fields):
            if isinstance(value, str) and len(value) > 4:
                masked_data[key] = value[:2] + "*" * (len(value) - 4) + value[-2:]
            else:
                masked_data[key] = "***"
    
    return masked_data

def log_function_call(func_name: str, args: tuple = None, kwargs: dict = None, result: Any = None):
    """Log function call details"""
    log_data = {
        "function": func_name,
        "timestamp": get_utc_now().isoformat()
    }
    
    if args:
        log_data["args"] = str(args)
    if kwargs:
        log_data["kwargs"] = mask_sensitive_data(kwargs)
    if result is not None:
        log_data["result"] = str(result)
    
    logger.info(f"Function call: {log_data}")

def validate_required_fields(data: Dict[str, Any], required_fields: list) -> list:
    """Validate that required fields are present in data"""
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    
    return missing_fields

def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values and empty strings from dictionary"""
    return {k: v for k, v in data.items() if v is not None and v != ""}
