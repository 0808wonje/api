from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import os


conf = ConnectionConfig(
    MAIL_USERNAME=os.environ["MAIL_USERNAME"],
    MAIL_PASSWORD=os.environ["MAIL_PASSWORD"],
    MAIL_FROM=os.environ["MAIL_FROM"],
    MAIL_SERVER=os.environ["MAIL_SERVER"],
    MAIL_PORT=int(os.environ["MAIL_PORT"]),
    MAIL_STARTTLS=True,   
    MAIL_SSL_TLS=False,   
)

async def send_email(email: EmailStr):
    message = MessageSchema(
        subject="Hello",
        recipients=[email],
        body="FastAPI email test", 
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
