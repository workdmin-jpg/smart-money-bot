# core/cache.py

import time


class SimpleCache:
    def __init__(self, ttl_seconds=900):
        """
        ttl_seconds = مدة صلاحية الكاش (افتراضي 15 دقيقة)
        """
        self.ttl = ttl_seconds
        self.store = {}

    def get(self, key):
        data = self.store.get(key)
        if not data:
            return None

        value, timestamp = data
        if time.time() - timestamp > self.ttl:
            del self.store[key]
            return None

        return value

    def set(self, key, value):
        self.store[key] = (value, time.time())