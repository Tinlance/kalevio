from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
router = APIRouter(tags=["threats"])

@router.post("/scan")
async def upload_pcap(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith(('.pcap', '.pcapng')):
        raise HTTPException(400, "Only .pcap and .pcapng files accepted")
    return {"status": "queued", "filename": file.filename}

@router.get("/")
async def list_threats(db: AsyncSession = Depends(get_db)):
    return {"threats": [], "total": 0}
