from fastapi import APIRouter, Depends, Request
from pydantic import EmailStr
from .mail import send_email
from ..auth.dependencies import get_current_user_id
import asyncio
import uuid
import httpx


router = APIRouter(
    prefix='/core',
    tags=['Core']
)

@router.post("/mail")
async def send_mail(
    mail_addr: EmailStr,
    token: str =  Depends(get_current_user_id)):
    await send_email(mail_addr)


@router.post("/webhooks/consumer")
async def webhook_receive(request: Request):
    data = await request.json()
    print("webhook received:", data)
    return {"ok": True}

@router.post("/webhooks/producer")
async def webhook_send(request: Request):
    data = await request.json()
    event_id = str(uuid.uuid4())
    async def _do_send():
        await asyncio.sleep(10)
        payload = {
            'callback_url' : data['callback_url'],
            'event_type': data['event_type'], 
            'event_id': event_id
            }
        await send_email('wonje.j1996@gmail.com')
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(url=data['callback_url'], json=payload)
    asyncio.create_task(_do_send())
    return {"ok": True, "scheduled": True, "event_id": event_id}