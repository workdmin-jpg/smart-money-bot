# core/rate_limiter.py

import time


class RateLimiter:
    def __init__(self, min_interval=2):
        """
        min_interval = أقل مدة بين كل طلب API (بالثواني)
        """
        self.min_interval = min_interval
        self.last_call = {}

    def wait(self, source_name):
        now = time.time()
        last = self.last_call.get(source_name, 0)

        elapsed = now - last
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)

        self.last_call[source_name] = time.time()