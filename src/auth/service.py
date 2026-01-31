from src.auth.schemas import UserLoginInput, SocialLoginInput, SocialAccountCreateInput
from src.user.schemas import UserCreate
from src.core.security.hashing import verify_password
from src.user.exceptions import IncorrectPasswordException
from src.core.security.jwt import create_access_token, decode_token
from src.auth.constants import EXPIRE_MINUTES
from .ports import UserQueryPort
from redis.asyncio import Redis
from ..user.exceptions import UserNotFoundException
import time


class AuthService:
    def __init__(self, user_port: UserQueryPort, redis: Redis):
        self.user_port = user_port
        self.redis = redis

    def procede_local_login(self, data: UserLoginInput) -> dict:
        user = self.user_port.fetch_user_by_username(data.username)
        if not user:
            raise UserNotFoundException
        is_verified = verify_password(data.password, user.password_hash) 
        if is_verified:
            return {
                'access_token' : self._issue_token(user.id),
                'token_type' : 'bearer',
                'expire_in' : EXPIRE_MINUTES
                }
        else:
            raise IncorrectPasswordException()  
    
    def procede_social_login(self, data: SocialLoginInput) -> dict:
        user = self.user_port.fetch_social_user_by_provider_id(data.provider, data.provider_id)
        if not user:
            user_value = UserCreate().model_dump()
            user = self.user_port.persist_user(user_value)
            social_user_values = data.model_dump()
            self.user_port.persist_social_user(user, social_user_values)
        return {
                'access_token' : self._issue_token(user.id),
                'token_type' : 'bearer',
                'expire_in' : EXPIRE_MINUTES
                }
    
    async def procede_logout(self, jwt: dict):
        now = int(time.time())
        ttl = jwt['exp'] - now
        if ttl > 0: 
            await self.redis.set(f'jwt:blacklist:{jwt['jti']}', "1", ex=ttl)
        return

    def _issue_token(self, user_id) -> str:
        access_token = create_access_token(user_id)
        return access_token

    def authenticate_user(self):
        pass