from .repository import UserRepository
from .models import Users
from .schemas import UserCreate, UpdateUserProfile, FindUserResponse
from .exceptions import UserNotFoundException, DuplicateUsernameException
from ..core.security.hashing import hash_password
from ..core.constants import REDIS_TTL_SECONDS
from redis.asyncio import Redis
from datetime import datetime, timezone
import json
from sqlalchemy.exc import IntegrityError



def user_cache_key(user_id: int) -> str:
    return f"cache:user:{user_id}"
    
class UserService:
    def __init__(self, repo: UserRepository, redis: Redis):
        self.repo = repo
        self.redis = redis

    def register_user(self, data: UserCreate) -> Users:
        is_exist = self.repo.is_username_exist(data.username)
        if is_exist:
            raise DuplicateUsernameException()
        else:
            values = data.model_dump()
            values['password_hash'] = hash_password(values['password_hash'])
            user = self.repo.add(values)
            return user


    async def get_user_profile(self, user_id: int) -> FindUserResponse:
        key = user_cache_key(user_id)
        try:
            cached = await self.redis.get(key)
            if cached:
                return json.loads(cached)
            user = self.repo.get_by_id(user_id)
            if user:
                response = FindUserResponse.model_validate(user)
                await self.redis.set(key, response.model_dump_json(), ex=REDIS_TTL_SECONDS)
                return response
            else:
                raise UserNotFoundException()
        except Exception:
            raise

    async def change_profile(self, user_id: int, data: UpdateUserProfile) -> Users:
        user = self.repo.get_by_id(user_id)
        values = data.model_dump(exclude_unset=True)
        for key, value in values.items():
            setattr(user, key, value)
        user.updated_at = datetime.now(timezone.utc)
        try:
            self.repo.db.flush()
        except IntegrityError:
            self.repo.db.rollback()
            raise
        await self.redis.unlink(user_cache_key(user_id))
        return user

    async def delete_user(self, user_id) -> None:
        try:
            self.repo.delete(int(user_id))
            await self.redis.unlink(user_cache_key(user_id))
        except Exception:
            raise