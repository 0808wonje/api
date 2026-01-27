import time
from fastapi import Depends, HTTPException, status
from redis import Redis
from src.core.dependencies import get_redis
from src.auth.dependencies import get_current_user_id
from .constants import RATE_LIMIT, WINDOW_SECONDS


def rate_limit(
    user_id: str = Depends(get_current_user_id),
    r: Redis = Depends(get_redis),
):
    now = int(time.time())
    window = now // WINDOW_SECONDS
    key = f"rate:mail:{user_id}:{window}"

    count = r.incr(key)
    if count == 1:
        r.expire(key, WINDOW_SECONDS)

    if count > RATE_LIMIT:
        ttl = r.ttl(key)
        if ttl < 0:
            ttl = WINDOW_SECONDS

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {ttl} seconds.",
            headers={"Retry-After": str(ttl)},
        )
