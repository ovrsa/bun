from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class CacheRepository:
    """Base class for cache handling"""

    CACHE_TIME = 3600

    def get_from_cache(self, key):
        """Retrieve data from cache"""
        logger.info(f"Fetching from cache: {key}")
        return cache.get(key)

    def set_to_cache(self, key, value):
        """Set data to cache"""
        logger.info(f"Setting cache: {key}")
        cache.set(key, value, timeout=self.CACHE_TIME)
