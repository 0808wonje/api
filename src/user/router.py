from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.user.schemas import *
from src.user.dependencies import UserService, get_user_service
from src.core.database import get_db
from pydantic import EmailStr
from src.core.mail import send_email

router = APIRouter()

@router.post("/user/join", response_model=UserCreateResponse)
async def join(
    data: UserCreate, 
    db: Session = Depends(get_db), 
    service: UserService = Depends(get_user_service)):
    user = service.create_user(db, data)
    return user

@router.post("/user/quit")
async def quit(data: DeleteUser, 
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)):
    service.delete_user(db, data)
    return DeleteUserResponse(msg='Your account is deleted!')

@router.get("/user/find", response_model=FindUsernameResponse)
async def find_username(
    data: str, 
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)):
    user = service.search_username(db, data)
    return user

@router.post("/user/change", response_model=UpdateUsernameResponse)
async def change_username(
    data: UpdateUsername,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)):
    user = service.modify_name(db, data)
    return user

@router.post("/mail")
async def send_mail(
    mail_addr: EmailStr):
    await send_email(mail_addr)
