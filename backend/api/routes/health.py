from fastapi import APIRouter
from datetime import datetime, timezone
router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    return {"status": "operational", "service": "KalevioAI", "version": "0.1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(), "threatfade": "online"}
