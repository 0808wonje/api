from fastapi import Request
from redis import Redis


def get_redis(request: Request) -> Redis:
    if request.app.state.redis is None:
        raise RuntimeError("Redis is not initialized")
    return request.app.state.redis

