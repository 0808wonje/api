import time, os, time, hashlib, hmac
from fastapi import HTTPException

webhook_secret_key = os.environ['WEBHOOK_SECRET_KEY']

def verify_signature(body: bytes, signature: str, timestamp: str):
    if abs(time.time() - int(timestamp)) > 5:
        raise HTTPException(status_code=400, detail="Timestamp too old")
    signed_payload = timestamp.encode() + b"." + body
    expected_signature = hmac.new(
        webhook_secret_key.encode(),
        signed_payload,
        hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

def create_signature(body: bytes, timestamp: str) -> str:
    signed_payload = timestamp.encode() + b"." + body
    signature = hmac.new(
        key=webhook_secret_key.encode(),
        msg=signed_payload,
        digestmod=hashlib.sha256
    ).hexdigest()
    return signature