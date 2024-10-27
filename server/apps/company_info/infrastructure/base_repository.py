from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class CacheRepository:
    """Cache repository base class"""

    CACHE_TIME = 3600

    def get_from_cache(self, key):
        """Get data from cache"""
        return cache.get(key)