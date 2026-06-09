from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
router = APIRouter(tags=["compliance"])

@router.get("/score")
async def compliance_score(db: AsyncSession = Depends(get_db)):
    return {"nis2_score": 0, "dora_score": 0, "overall_score": 0, "gaps": []}

@router.get("/scope-check")
async def scope_check():
    return {"questions": [
        {"id": 1, "text": "Does your organisation operate in the EU?", "key": "eu_operations"},
        {"id": 2, "text": "What sector does your organisation operate in?", "key": "sector"},
        {"id": 3, "text": "How many employees?", "key": "employee_count"},
        {"id": 4, "text": "Annual turnover (€)?", "key": "annual_turnover"},
        {"id": 5, "text": "Do you provide digital infrastructure or managed services?", "key": "digital_services"},
    ]}
