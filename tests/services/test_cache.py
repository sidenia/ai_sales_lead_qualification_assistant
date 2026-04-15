import pytest
from app.services.cache import CacheService, cache_service


class TestCacheService:
    def test_cache_service_init(self):
        service = CacheService()
        assert service._cache == {}

    def test_get_nonexistent_key(self):
        service = CacheService()
        assert service.get("nonexistent") is None

    def test_set_and_get(self):
        service = CacheService()
        service.set("key1", "value1")
        assert service.get("key1") == "value1"

    def test_set_overwrite(self):
        service = CacheService()
        service.set("key1", "value1")
        service.set("key1", "value2")
        assert service.get("key1") == "value2"

    def test_clear_cache(self):
        service = CacheService()
        service.set("key1", "value1")
        service.set("key2", "value2")
        service.clear()
        assert service.get("key1") is None
        assert service.get("key2") is None

    def test_multiple_keys(self):
        service = CacheService()
        service.set("key1", "value1")
        service.set("key2", "value2")
        service.set("key3", "value3")
        assert service.get("key1") == "value1"
        assert service.get("key2") == "value2"
        assert service.get("key3") == "value3"


class TestGlobalCacheService:
    def test_global_cache_service_instance(self):
        assert isinstance(cache_service, CacheService)

    def test_global_cache_operations(self):
        cache_service.clear()
        cache_service.set("global_key", "global_value")
        assert cache_service.get("global_key") == "global_value"
        cache_service.clear()
        assert cache_service.get("global_key") is None