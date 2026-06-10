from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
from backend.core.llm_gateway import llm
from backend.schemas.report import ReportCreate, ReportResponse

router = APIRouter(tags=["reports"])

NIS2_SYSTEM = """You are a senior NIS2 compliance officer generating official incident
reports for submission to EU national CSIRTs. Your reports must meet NIS2 Article 23
requirements exactly. Use formal regulatory language. Be precise and legally defensible."""

@router.post("/generate")
async def generate_report(
    payload: ReportCreate,
    db: AsyncSession = Depends(get_db)
):
    """Generate AI-powered NIS2/DORA compliance report using four-layer LLM gateway."""
    from backend.compliance.frameworks.nis2 import get_csirt
    csirt = get_csirt(payload.csirt_country)

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

    return {
        "status": "generated",
        "report_type": payload.report_type,
        "framework": payload.framework,
        "csirt": csirt["name"],
        "csirt_email": csirt["email"],
        "content": content,
        "llm_model": model_used,
        "requires_review": True,
        "incident_id": str(payload.incident_id)
    }

@router.get("/")
async def list_reports(db: AsyncSession = Depends(get_db)):
    return {"reports": [], "total": 0}
