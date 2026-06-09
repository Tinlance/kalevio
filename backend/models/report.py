from sqlalchemy import Column, String, DateTime, JSON, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid, enum
from backend.core.database import Base

class ReportType(str, enum.Enum):
    EARLY_WARNING = "early_warning"; NOTIFICATION = "notification"
    FINAL_REPORT = "final_report"; COMPLIANCE_AUDIT = "compliance_audit"

class ReportStatus(str, enum.Enum):
    DRAFT = "draft"; REVIEW = "review"; APPROVED = "approved"; SUBMITTED = "submitted"

class ComplianceReport(Base):
    __tablename__ = "compliance_reports"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id        = Column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False, index=True)
    incident_id   = Column(UUID(as_uuid=True), ForeignKey("incidents.id"), nullable=True)
    report_type   = Column(Enum(ReportType))
    status        = Column(Enum(ReportStatus), default=ReportStatus.DRAFT)
    framework     = Column(String(50))
    content       = Column(Text)
    csirt_country = Column(String(2))
    submitted_at  = Column(DateTime(timezone=True), nullable=True)
    llm_model     = Column(String(100))
    approved_by   = Column(String(255), nullable=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
