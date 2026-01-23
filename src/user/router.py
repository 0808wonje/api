from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.user.schemas import *
from src.user.dependencies import UserService, get_user_service
from src.core.database import get_db
from pydantic import EmailStr
from src.core.mail import send_email
from src.auth.dependencies import get_current_user_id


router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post("/join", response_model=UserCreateResponse)
def join(
    data: UserCreate, 
    db: Session = Depends(get_db), 
    service: UserService = Depends(get_user_service)):
    user = service.create_user(db, data)
    return user

@router.post("/quit")
def quit(data: DeleteUser, 
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)):
    service.delete_user(db, data)
    return DeleteUserResponse(msg='Your account is deleted!')

@router.get("/find", response_model=FindUsernameResponse)
def find_username(
    data: str, 
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
    token: str =  Depends(get_current_user_id)
    ):
    user = service.get_user(db, data)
    return user

@router.post("/change", response_model=UpdateUsernameResponse)
def change_username(
    data: UpdateUsername,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)):
    user = service.modify_name(db, data)
    return user

@router.post("/mail")
async def send_mail(
    mail_addr: EmailStr):
    await send_email(mail_addr)
