from fastapi import APIRouter, Depends, Request
from pydantic import EmailStr
from .mail import send_email
from ..auth.dependencies import get_current_user_id
from .limiter import rate_limit
import time, json, httpx, uuid, asyncio
from .security.webhook_hmac import verify_signature, create_signature


router = APIRouter(
    prefix='/core',
    tags=['Core']
)

@router.post("/mail")
async def send_mail(
    mail_addr: EmailStr,
    token: str =  Depends(get_current_user_id),
    _: None = Depends(rate_limit)):
    await send_email(mail_addr)


@router.post("/webhooks/consumer")
async def webhook_receive(request: Request):
    body = await request.body()
    print("webhook received body:", body)
    signature = request.headers.get("X-Signature")
    timestamp = request.headers.get("X-Timestamp")
    verify_signature(body, signature, timestamp)
    data = await request.json()
    print("webhook received data:", data)
    return {"ok": True}

@router.post("/webhooks/producer")
async def webhook_send(request: Request):
    data = await request.json()
    event_id = str(uuid.uuid4())
    async def _do_send():
        payload = {
            'callback_url' : data['callback_url'],
            'event_type': data['event_type'], 
            'event_id': event_id
            }
        body = json.dumps(payload).encode()
        timestamp = str(int(time.time()))
        signature = create_signature(body, timestamp)
        headers = {
            "X-Signature": signature,
            "X-Timestamp": timestamp,
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True,
            verify=False) as client:
            await client.post(url=data['callback_url'], content=body, headers=headers)
    asyncio.create_task(_do_send())
    return {"ok": True, "scheduled": True, "event_id": event_id}