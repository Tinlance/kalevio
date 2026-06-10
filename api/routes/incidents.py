from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timezone, timedelta
from core.database import get_db
from models.incident import Incident, IncidentSeverity, IncidentStatus
from pydantic import BaseModel
from typing import Optional, List
import uuid

router = APIRouter(tags=["incidents"])

class IncidentCreate(BaseModel):
    threat_type: str
    z_score: float
    mitre_ttps: Optional[List[str]] = []
    source_ip: Optional[str] = None
    affected_systems: Optional[List[str]] = []
    raw_data: Optional[dict] = {}

def classify_severity(z_score: float) -> IncidentSeverity:
    if z_score >= 10.0: return IncidentSeverity.CRITICAL
    if z_score >= 5.0:  return IncidentSeverity.HIGH
    if z_score >= 2.5:  return IncidentSeverity.MEDIUM
    return IncidentSeverity.LOW

def is_nis2_reportable(severity: IncidentSeverity) -> bool:
    return severity in (IncidentSeverity.HIGH, IncidentSeverity.CRITICAL)

def is_dora_reportable(severity: IncidentSeverity, threat_type: str) -> bool:
    dora_keywords = ["ransomware", "data breach", "system outage", "ddos", "supply chain"]
    return severity in (IncidentSeverity.HIGH, IncidentSeverity.CRITICAL) and \
           any(k in threat_type.lower() for k in dora_keywords)

def make_reference_id() -> str:
    now = datetime.now(timezone.utc)
    return f"KAL-{now.strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"

def incident_to_out(inc: Incident) -> dict:
    return {
        "id": str(inc.id),
        "reference_id": inc.reference_id,
        "threat_type": inc.threat_type,
        "severity": inc.severity.value if inc.severity else "unknown",
        "status": inc.status.value if inc.status else "detected",
        "z_score": inc.z_score or 0.0,
        "nis2_reportable": inc.nis2_reportable,
        "dora_reportable": inc.dora_reportable,
        "early_warning_due": inc.early_warning_due.isoformat() if inc.early_warning_due else None,
        "notification_due": inc.notification_due.isoformat() if inc.notification_due else None,
        "final_report_due": inc.final_report_due.isoformat() if inc.final_report_due else None,
        "detected_at": inc.detected_at.isoformat() if inc.detected_at else None,
        "mitre_ttps": inc.mitre_ttps or [],
        "affected_systems": inc.affected_systems or [],
    }

@router.post("/", status_code=201)
async def create_incident(payload: IncidentCreate, db: AsyncSession = Depends(get_db)):
    """Create incident — auto-calculates NIS2 deadlines and reportability."""
    now = datetime.now(timezone.utc)
    severity = classify_severity(payload.z_score)
    nis2 = is_nis2_reportable(severity)
    dora = is_dora_reportable(severity, payload.threat_type)
    inc = Incident(
        id=uuid.uuid4(),
        org_id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        reference_id=make_reference_id(),
        threat_type=payload.threat_type,
        severity=severity,
        status=IncidentStatus.DETECTED,
        z_score=payload.z_score,
        mitre_ttps=payload.mitre_ttps,
        source_ip=payload.source_ip,
        affected_systems=payload.affected_systems,
        nis2_reportable=nis2,
        dora_reportable=dora,
        early_warning_due=now + timedelta(hours=24) if nis2 else None,
        notification_due=now + timedelta(hours=72) if nis2 else None,
        final_report_due=now + timedelta(days=30) if nis2 else None,
        raw_data=payload.raw_data,
        detected_at=now,
    )
    db.add(inc)
    await db.commit()
    await db.refresh(inc)
    result = incident_to_out(inc)
    result["message"] = f"Incident created. {'NIS2 Article 23 early warning due in 24h.' if nis2 else 'Below NIS2 reporting threshold.'}"
    return result

@router.get("/")
async def list_incidents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Incident).order_by(Incident.detected_at.desc()).limit(50)
    )
    incidents = result.scalars().all()
    total = await db.execute(select(func.count(Incident.id)))
    return {"incidents": [incident_to_out(i) for i in incidents], "total": total.scalar() or 0}

@router.get("/{incident_id}")
async def get_incident(incident_id: str, db: AsyncSession = Depends(get_db)):
    try:
        uid = uuid.UUID(incident_id)
    except ValueError:
        raise HTTPException(400, "Invalid incident ID format")
    result = await db.execute(select(Incident).where(Incident.id == uid))
    inc = result.scalar_one_or_none()
    if not inc:
        raise HTTPException(404, f"Incident {incident_id} not found")
    return incident_to_out(inc)
