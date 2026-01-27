from redis import Redis
from typing import Optional
import os


redis_url = os.environ['REDIS_URL']

redis_client: Optional[Redis] = None 

def init_redis():
    global redis_client
    redis_client = Redis.from_url(redis_url, decode_responses=True)
    
def close_redis():
    redis_client.close()

