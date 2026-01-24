from jose import jwt
from datetime import datetime, timezone, timedelta
from ...auth.constants import ALG, EXPIRE_MINUTES
import os

secret_key = os.environ['SECRET_KEY']

def create_access_token(data: dict, expires_minutes: int = EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    print(f'to_encode ===== {to_encode}')
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    print(f'to_encode ===== {to_encode}')
    return jwt.encode(to_encode, secret_key, algorithm=ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=ALG)
