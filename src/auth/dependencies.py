from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from src.core.security.jwt import decode_token
from src.auth.service import AuthService
from src.user.service import UserService
from src.user.repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        print('get_current_user_id success')
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def get_auth_service() -> AuthService:
    return AuthService(UserService(UserRepository()))
