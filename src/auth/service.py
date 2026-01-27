from src.auth.schemas import UserLoginInput
from src.core.security.hashing import verify_password
from src.user.exceptions import IncorrectPasswordException
from src.core.security.jwt import create_access_token, decode_token
from src.auth.constants import EXPIRE_MINUTES
from .ports import UserReader
from redis import Redis
from sqlalchemy.orm import Session
from ..user.exceptions import UserNotFoundException



class AuthService:
    def __init__(self, db: Session, user_reader: UserReader, redis: Redis):
        self.user_reader = user_reader
        self.redis = redis
        self.db = db

    def procede_login(self, data: UserLoginInput) -> dict:
        user = self.user_reader.fetch_user_by_username(self.db, data.username)
        if not user:
            raise UserNotFoundException
        is_verified = verify_password(data.password, user.password_hash) 
        if is_verified:
            return {
                'access_token' : self.issue_token(user.id),
                'token_type' : 'bearer',
                'expire_in' : EXPIRE_MINUTES
                }
        else:
            raise IncorrectPasswordException()  

    def authenticate_user(self):
        pass

    def issue_token(self, user_id) -> str:
        access_token = create_access_token(user_id)
        return access_token
