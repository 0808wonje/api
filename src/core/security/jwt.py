from jose import jwt
from datetime import datetime, timezone, timedelta
from ...auth.constants import ALG, EXPIRE_MINUTES
import os
import uuid

secret_key = os.environ['JWT_SECRET_KEY']

def create_access_token(user_id: int, expires_minutes: int = EXPIRE_MINUTES) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_minutes)
    payload = {
        "sub" : str(user_id),
        "iat" : int(now.timestamp()),
        "exp" : int(exp.timestamp()),
        "jti" : uuid.uuid4().hex

    }
    return jwt.encode(payload, secret_key, algorithm=ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=ALG)
