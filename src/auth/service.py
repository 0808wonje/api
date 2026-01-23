from sqlalchemy.orm import Session
from src.auth.schemas import UserLoginInput
from src.core.security.hashing import verify_password
from src.user.exceptions import IncorrectPasswordException
from src.core.security.jwt import create_access_token, decode_token
from src.auth.constants import EXPIRE_MINUTES
from src.user.service import UserService



class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def procede_login(self, db: Session, data: UserLoginInput) -> dict:
        user = self.user_service.get_user(db, data.user_id)
        try:
            is_verified = verify_password(data.password, user.password_hash) 
            if is_verified:
               return {
                    'access_token' : self.issue_token(user.username),
                    'token_type' : 'bearer',
                    'expire_in' : EXPIRE_MINUTES
                    }
            else:
                raise IncorrectPasswordException()  
        except Exception:
            raise

    def authenticate_user(self):
        pass

    def issue_token(self, username) -> dict:
        access_token = create_access_token({'user_id': username}, EXPIRE_MINUTES)
        return access_token
