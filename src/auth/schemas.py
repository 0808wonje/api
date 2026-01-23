from pydantic import BaseModel

class UserLoginInput(BaseModel):
    user_id: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    expires_in: int