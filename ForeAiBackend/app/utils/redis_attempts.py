import time
import redis

class RedisAuthAttempts:
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self._redis = None

    def get_redis(self):
        if not self._redis:
            self._redis = redis.from_url(self.redis_url, decode_responses=True)
        return self._redis

    def record_failure(self, ip, max_attempts, max_backoff):
        redis = self.get_redis()
        count = int(redis.get(f"{ip}:fail") or 0) + 1
        backoff = int(redis.get(f"{ip}:backoff") or 1)
        if count >= max_attempts:
            backoff = min(backoff * 2, max_backoff)
            redis.set(f"{ip}:blocked_until", int(time.time() + backoff), ex=backoff)
            redis.delete(f"{ip}:fail")
            redis.set(f"{ip}:backoff", backoff, ex=backoff)
            return backoff
        else:
            redis.set(f"{ip}:fail", count, ex=600)
            return None

    def is_blocked(self, ip):
        redis = self.get_redis()
        blocked_until = int(redis.get(f"{ip}:blocked_until") or 0)
        now = int(time.time())
        return blocked_until if blocked_until > now else 0

    def reset(self, ip):
        redis = self.get_redis()
        redis.delete(f"{ip}:fail", f"{ip}:blocked_until", f"{ip}:backoff")
