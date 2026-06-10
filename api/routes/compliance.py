from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from compliance.frameworks.nis2 import (
    NIS2_ARTICLE_21_MEASURES, calculate_compliance_score, CSIRT_ENDPOINTS
)
from pydantic import BaseModel
from typing import Dict, Optional

router = APIRouter(tags=["compliance"])

NIS2_SECTORS = [
    "energy", "transport", "banking", "financial_markets", "health",
    "drinking_water", "wastewater", "digital_infrastructure", "ict_services",
    "public_administration", "space", "postal", "waste_management",
    "chemicals", "food", "manufacturing", "digital_providers", "research"
]

class ScopeAnswers(BaseModel):
    eu_operations: bool
    sector: str
    employee_count: int
    annual_turnover_eur: float
    digital_services: bool

class ComplianceScoreRequest(BaseModel):
    measures: Dict[str, str]  # {"a": "compliant", "b": "partial", ...}

@router.get("/scope-check")
async def scope_check():
    """Return the 5-question NIS2 scope wizard."""
    return {"questions": [
        {"id": 1, "text": "Does your organisation operate in the EU?", "key": "eu_operations", "type": "boolean"},
        {"id": 2, "text": "What sector does your organisation operate in?", "key": "sector", "type": "select", "options": NIS2_SECTORS},
        {"id": 3, "text": "How many employees does your organisation have?", "key": "employee_count", "type": "number"},
        {"id": 4, "text": "What is your annual turnover in EUR?", "key": "annual_turnover_eur", "type": "number"},
        {"id": 5, "text": "Do you provide digital infrastructure or managed ICT services?", "key": "digital_services", "type": "boolean"},
    ]}

@router.post("/scope-evaluate")
async def evaluate_scope(answers: ScopeAnswers):
    """Evaluate NIS2 scope based on wizard answers. Returns in-scope verdict + entity type."""
    if not answers.eu_operations:
        return {"in_scope": False, "reason": "Organisation does not operate in the EU. NIS2 does not apply.", "entity_type": None}

    essential_sectors = ["energy", "transport", "banking", "financial_markets", "health",
                         "drinking_water", "wastewater", "digital_infrastructure", "ict_services",
                         "public_administration", "space"]
    important_sectors = ["postal", "waste_management", "chemicals", "food",
                         "manufacturing", "digital_providers", "research"]

    is_essential_sector = answers.sector in essential_sectors
    is_important_sector = answers.sector in important_sectors
    is_large = answers.employee_count >= 250 or answers.annual_turnover_eur >= 50_000_000
    is_medium = answers.employee_count >= 50 or answers.annual_turnover_eur >= 10_000_000

    if answers.digital_services and is_large:
        entity_type = "essential"
        in_scope = True
    elif is_essential_sector and is_large:
        entity_type = "essential"
        in_scope = True
    elif (is_essential_sector or is_important_sector) and is_medium:
        entity_type = "important"
        in_scope = True
    elif answers.digital_services and is_medium:
        entity_type = "important"
        in_scope = True
    else:
        entity_type = None
        in_scope = False

    if not in_scope:
        return {
            "in_scope": False,
            "reason": "Organisation falls below NIS2 size thresholds (50+ employees or €10M+ turnover required).",
            "entity_type": None
        }

    fine_max = "€10M or 2% global turnover" if entity_type == "essential" else "€7M or 1.4% global turnover"
    return {
        "in_scope": True,
        "entity_type": entity_type,
        "sector": answers.sector,
        "fine_max": fine_max,
        "deadlines": {
            "early_warning_hours": 24,
            "notification_hours": 72,
            "final_report_days": 30
        },
        "required_measures": len(NIS2_ARTICLE_21_MEASURES),
        "message": f"Your organisation is an {entity_type.upper()} entity under NIS2. Compliance is mandatory by October 2026."
    }

@router.post("/score")
async def compliance_score(request: ComplianceScoreRequest):
    """Calculate NIS2 Article 21 compliance score from self-assessment."""
    score = calculate_compliance_score(request.measures)
    gaps = [
        {"measure": m["title"], "article": m["article"], "weight": m["weight"]}
        for m in NIS2_ARTICLE_21_MEASURES
        if request.measures.get(m["id"]) != "compliant"
    ]
    if score >= 80:
        status = "compliant"
        message = "Strong compliance posture. Minor gaps remain."
    elif score >= 50:
        status = "partial"
        message = "Significant gaps. Enforcement risk is moderate."
    else:
        status = "non_compliant"
        message = "Critical gaps. Immediate action required before October 2026."
    return {
        "nis2_score": score,
        "dora_score": 0,
        "overall_score": score,
        "status": status,
        "message": message,
        "gaps": gaps,
        "measures_evaluated": len(NIS2_ARTICLE_21_MEASURES)
    }

@router.get("/csirts")
async def list_csirts():
    """Return all 10 pre-built CSIRT endpoints."""
    return {"csirts": CSIRT_ENDPOINTS, "total": len(CSIRT_ENDPOINTS)}
