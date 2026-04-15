from typing import Dict, Optional


class CacheService:
    """Simple in-memory cache service."""

    def __init__(self):
        self._cache: Dict[str, str] = {}

    def get(self, key: str) -> Optional[str]:
        return self._cache.get(key)

    def set(self, key: str, value: str) -> None:
        self._cache[key] = value

    def clear(self) -> None:
        self._cache.clear()

cache_service = CacheService() # global cache instance