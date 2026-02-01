import time
from fastapi import Depends, HTTPException, status, Request
from redis.asyncio import Redis
from src.core.dependencies import get_redis
from src.auth.dependencies import get_current_user_id
from .constants import RATE_LIMIT, WINDOW_SECONDS

async def rate_limit(
    request: Request,
    user_id: str = Depends(get_current_user_id),
    r: Redis = Depends(get_redis)):
    router_name = request.scope['route'].name
    #Fixed Window Rate Limit
    now = int(time.time())
    window = now // WINDOW_SECONDS
    key = f"limit:{router_name}:{user_id}:{window}"

    count = await r.incr(key)
    if count == 1:
        await r.expire(key, WINDOW_SECONDS)

    if count > RATE_LIMIT:
        ttl = await r.ttl(key)
        if ttl < 0:
            ttl = WINDOW_SECONDS

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {ttl} seconds.",
            headers={"Retry-After": str(ttl)},
        )
