from fastapi import APIRouter, Request, HTTPException
from core.config import settings
import hashlib, hmac
router = APIRouter(tags=["billing"])

@router.post("/webhook/lemonsqueezy")
async def lemonsqueezy_webhook(request: Request):
    signature = request.headers.get("X-Signature", "")
    body = await request.body()
    expected = hmac.new(settings.LEMONSQUEEZY_WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(401, "Invalid signature")
    return {"status": "received"}
