from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    username: str | None = None
    password_hash: str | None = None
    email: EmailStr | None = None
    age: int | None = None

class UserCreateResponse(BaseModel):
    username: str
    email: EmailStr
    age: int
    created_at: datetime

class FindUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    age: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime

class UpdateUserProfile(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    age: int | None = None

class UpdateUsernameResponse(BaseModel):
    username: str
    email: EmailStr
    age: int
    updated_at: datetime
