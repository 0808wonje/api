from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from .service import AuthService
from ..core.security.jwt import decode_token
from ..user.repository import UserRepository
from ..core.database import get_db
from ..core.dependencies import Redis, get_redis
from fastapi import Depends
from sqlalchemy.orm import Session
from src.auth.service import AuthService
from src.user.repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except (JWTError, ExpiredSignatureError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def get_auth_service(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)) -> AuthService:
    user_repo = UserRepository()
    return AuthService(db, user_repo, redis)