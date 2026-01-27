from pydantic import BaseModel

class UserLoginInput(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    expire_in: int