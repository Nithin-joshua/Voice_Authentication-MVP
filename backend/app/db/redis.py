import redis
import numpy as np
import os


def get_redis():
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return None
    try:
        return redis.Redis.from_url(redis_url)
    except Exception:
        return None


def cache_features(user_id, features):
    r = get_redis()
    if r:
        r.set(user_id, features.tobytes())


def get_cached_features(user_id):
    r = get_redis()
    if not r:
        return None
    data = r.get(user_id)
    if data:
        return np.frombuffer(data, dtype=np.float32)
    return None
