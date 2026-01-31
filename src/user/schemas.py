from pydantic import BaseModel, EmailStr
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

class FindUserResponse(BaseModel):
    username: str

class UpdateUsername(BaseModel):
    after_name: str

class UpdateUsernameResponse(BaseModel):
    username: str
    updated_at: datetime

class UpdateUsernameResponse(BaseModel):
    username: str

class DeleteUser(BaseModel):
    username: str

class DeleteUserResponse(BaseModel):
    msg: str