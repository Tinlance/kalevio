from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class ReportCreate(BaseModel):
    incident_id: UUID4
    report_type: str
    framework: str = "nis2"
    csirt_country: str = "EE"

class ReportResponse(BaseModel):
    id: UUID4
    report_type: str
    status: str
    framework: str
    content: Optional[str]
    llm_model: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
