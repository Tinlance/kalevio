from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from core.database import get_db
from core.llm_gateway import llm
from schemas.report import ReportCreate
from models.report import ComplianceReport, ReportType, ReportStatus
from compliance.frameworks.nis2 import get_csirt
import uuid
from datetime import datetime, timezone

router = APIRouter(tags=["reports"])

NIS2_SYSTEM = """You are a senior NIS2 compliance officer generating official incident
reports for submission to EU national CSIRTs. Your reports must meet NIS2 Article 23
requirements exactly. Use formal regulatory language. Be precise and legally defensible."""

def report_to_out(r: ComplianceReport) -> dict:
    return {
        "id": str(r.id),
        "report_type": r.report_type.value if r.report_type else None,
        "status": r.status.value if r.status else None,
        "framework": r.framework,
        "content": r.content,
        "llm_model": r.llm_model,
        "csirt_country": r.csirt_country,
        "incident_id": str(r.incident_id) if r.incident_id else None,
        "requires_review": r.status == ReportStatus.DRAFT,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }

@router.post("/generate")
async def generate_report(
    payload: ReportCreate,
    db: AsyncSession = Depends(get_db)
):
    """Generate AI-powered NIS2/DORA report and persist to DB."""
    csirt = get_csirt(payload.csirt_country)

    # Map report_type string to enum
    try:
        report_type_enum = ReportType(payload.report_type)
    except ValueError:
        report_type_enum = ReportType.EARLY_WARNING

    prompt = f"""Generate a NIS2 Article 23 {payload.report_type.upper()} report.

Framework: {payload.framework.upper()}
CSIRT Authority: {csirt["name"]}
Report Type: {payload.report_type}
Incident ID: {payload.incident_id}

Include all mandatory NIS2 Article 23 fields:
- Incident description and initial classification
- Affected systems and services
- Geographic scope and cross-border impact assessment
- Measures taken and planned
- Preliminary cause assessment
- Regulatory obligations timeline (24h/72h/30d)

Format as an official regulatory document ready for CSIRT submission."""

    content, model_used = await llm.complete(
        prompt,
        system=NIS2_SYSTEM,
        max_tokens=2048
    )

    # Persist to DB
    report = ComplianceReport(
        id=uuid.uuid4(),
        org_id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        incident_id=payload.incident_id,
        report_type=report_type_enum,
        status=ReportStatus.DRAFT,
        framework=payload.framework,
        content=content,
        csirt_country=payload.csirt_country,
        llm_model=model_used,
        created_at=datetime.now(timezone.utc),
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)

    return {
        "id": str(report.id),
        "status": "generated",
        "report_type": payload.report_type,
        "framework": payload.framework,
        "csirt": csirt["name"],
        "csirt_email": csirt["email"],
        "content": content,
        "llm_model": model_used,
        "requires_review": True,
        "incident_id": str(payload.incident_id),
        "saved_to_db": True,
    }

@router.get("/")
async def list_reports(db: AsyncSession = Depends(get_db)):
    """List all generated reports ordered by created_at desc."""
    result = await db.execute(
        select(ComplianceReport).order_by(ComplianceReport.created_at.desc()).limit(50)
    )
    reports = result.scalars().all()
    total = await db.execute(select(func.count(ComplianceReport.id)))
    return {
        "reports": [report_to_out(r) for r in reports],
        "total": total.scalar() or 0
    }

@router.get("/{report_id}")
async def get_report(report_id: str, db: AsyncSession = Depends(get_db)):
    """Get single report by ID."""
    try:
        uid = uuid.UUID(report_id)
    except ValueError:
        raise HTTPException(400, "Invalid report ID format")
    result = await db.execute(
        select(ComplianceReport).where(ComplianceReport.id == uid)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(404, f"Report {report_id} not found")
    return report_to_out(report)

@router.patch("/{report_id}/approve")
async def approve_report(report_id: str, db: AsyncSession = Depends(get_db)):
    """Mark report as approved and ready for CSIRT submission."""
    try:
        uid = uuid.UUID(report_id)
    except ValueError:
        raise HTTPException(400, "Invalid report ID format")
    result = await db.execute(
        select(ComplianceReport).where(ComplianceReport.id == uid)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(404, f"Report {report_id} not found")
    report.status = ReportStatus.APPROVED
    await db.commit()
    return {"id": report_id, "status": "approved", "message": "Report approved for CSIRT submission."}
