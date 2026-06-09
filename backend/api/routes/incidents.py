from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from backend.core.database import get_db
from backend.models.incident import Incident, IncidentSeverity, IncidentStatus
import uuid, random
router = APIRouter(tags=["incidents"])

def classify_severity(z_score: float) -> IncidentSeverity:
    if z_score >= 10.0: return IncidentSeverity.CRITICAL
    if z_score >= 5.0:  return IncidentSeverity.HIGH
    if z_score >= 2.5:  return IncidentSeverity.MEDIUM
    return IncidentSeverity.LOW

@router.get("/")
async def list_incidents(db: AsyncSession = Depends(get_db)):
    return {"incidents": [], "total": 0}
