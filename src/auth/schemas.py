from pydantic import BaseModel, EmailStr

class UserLoginInput(BaseModel):
    username: str
    password: str

class SocialLoginInput(BaseModel):
    provider: str
    provider_id: str
    social_email: EmailStr

class SocialAccountCreateInput(BaseModel):
    user_id: int
    provider: str
    provider_id: str
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    expire_in: int