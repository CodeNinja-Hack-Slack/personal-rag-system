from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


def truncate_text(text: str, max_length: int = 500) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def format_timestamp(dt: datetime) -> str:
    return dt.isoformat()


def get_time_range(days: int = 7) -> tuple[datetime, datetime]:
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    return start, end
