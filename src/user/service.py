from redis.asyncio import Redis
import json
from .repository import UserRepository
from .models import Users
from .schemas import UserCreate, UpdateUsername, DeleteUser
from .exceptions import UserNotFoundException, DuplicateUsernameException
from src.core.security.hashing import hash_password
from ..core.constants import REDIS_TTL_SECONDS

def user_cache_key(user_id: int) -> str:
    return f"cache:user:{user_id}"
    
class UserService:
    def __init__(self, repo: UserRepository, redis: Redis):
        self.repo = repo
        self.redis = redis

    def create_user(self, data: UserCreate) -> Users:
        is_exist = self.repo.is_username_exist(data.username)
        if is_exist:
            raise DuplicateUsernameException()
        else:
            values = data.model_dump()
            values['password_hash'] = hash_password(values['password_hash'])
            user = self.repo.persist_user(values)
            return user


    def get_user_from_db(self, data: str) -> Users:
        try:
            user = self.repo.fetch_user_by_username(data)
            if user:
                return user
            else:
                raise UserNotFoundException()
        except Exception:
            raise

    async def get_user_from_cache_first(self, user_id: int) -> dict:
        key = user_cache_key(user_id)
        try:
            cached = await self.redis.get(key)
            if cached:
                return json.loads(cached)
            user = self.repo.fetch_user_by_id(user_id)
            if user:
                data = json.dumps({
                    "id" : user.id,
                    "username" : user.username
                })
                await self.redis.set(key, data, ex=REDIS_TTL_SECONDS)
                return json.loads(data)
            else:
                raise UserNotFoundException()
        except Exception:
            raise

    async def modify_name(self, user_id: int, after_name: str) -> Users:
        try:
            user = self.repo.update_username(user_id, after_name)
            # self.redis.delete(user_id)
            await self.redis.unlink(user_cache_key(user_id))
            return user
        except Exception:
            raise

    async def delete_user(self, user_id) -> bool:
        try:
            self.repo.delete_user(int(user_id))
            # self.redis.delete(user_id)
            await self.redis.unlink(user_cache_key(user_id))
        except Exception:
            raise