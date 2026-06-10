from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
router = APIRouter(tags=["audit"])

@router.get("/log")
async def get_audit_log(db: AsyncSession = Depends(get_db)):
    return {"events": [], "total": 0, "chain_intact": True}
