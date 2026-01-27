from src.core import redis_config
from redis import Redis

def get_redis() -> Redis:
    if redis_config.redis_client is None:
        raise RuntimeError("Redis is not initialized")
    return redis_config.redis_client
