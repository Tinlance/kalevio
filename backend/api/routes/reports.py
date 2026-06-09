from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
router = APIRouter(tags=["reports"])

@router.get("/")
async def list_reports(db: AsyncSession = Depends(get_db)):
    return {"reports": [], "total": 0}
