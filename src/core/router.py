from fastapi import APIRouter, Depends
from pydantic import EmailStr
from .mail import send_email
from ..auth.dependencies import get_current_user_id


router = APIRouter(
    prefix='/core',
    tags=['Core']
)

@router.post("/mail")
async def send_mail(
    mail_addr: EmailStr,
    token: str =  Depends(get_current_user_id)):
    await send_email(mail_addr)
