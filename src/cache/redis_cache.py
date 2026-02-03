"""Redis-based caching for prediction results."""

import json
import hashlib
from typing import Any, Callable, Optional
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis cache manager for weather predictions."""

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        default_ttl: int = 3600,
        prefix: str = "weather"
    ):
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self.prefix = prefix
        self._client = None

    def _get_client(self):
        """Get or create Redis client."""
        if self._client is None:
            try:
                import redis
                self._client = redis.from_url(self.redis_url)
            except ImportError:
                logger.warning("Redis not installed")
        return self._client

    def _make_key(self, key: str) -> str:
        """Create prefixed cache key."""
        return f"{self.prefix}:{key}"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        client = self._get_client()
        if client is None:
            return None
        
        try:
            data = client.get(self._make_key(key))
            if data:
                return json.loads(data)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        return None

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache."""
        client = self._get_client()
        if client is None:
            return False
        
        try:
            data = json.dumps(value)
            client.setex(
                self._make_key(key),
                ttl or self.default_ttl,
                data
            )
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        client = self._get_client()
        if client is None:
            return False
        
        try:
            client.delete(self._make_key(key))
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        client = self._get_client()
        if client is None:
            return 0
        
        try:
            keys = client.keys(self._make_key(pattern))
            if keys:
                return client.delete(*keys)
        except Exception as e:
            logger.error(f"Cache invalidate error: {e}")
        return 0


def cached(
    cache: RedisCache,
    ttl: Optional[int] = None,
    key_func: Optional[Callable] = None
):
    """Decorator for caching function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                key_data = f"{func.__name__}:{args}:{kwargs}"
                cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
