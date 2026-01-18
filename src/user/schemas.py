from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password_hash: str
    age: int | None

class UserCreateResponse(BaseModel):
    username: str
    age: int

class FindUsername(BaseModel):
    username: str

class FindUsernameResponse(BaseModel):
    username: str

class UpdateUsername(BaseModel):
    cur_name: str
    after_name: str
    password: str

class UpdateUsernameResponse(BaseModel):
    username: str
    updated_at: datetime

class UpdateUsernameResponse(BaseModel):
    username: str

class DeleteUser(BaseModel):
    username: str

class DeleteUserResponse(BaseModel):
    msg: str