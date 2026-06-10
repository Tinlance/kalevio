from sqlalchemy import Column, String, Float, DateTime, JSON, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid, enum
from core.database import Base

class IncidentSeverity(str, enum.Enum):
    LOW = "low"; MEDIUM = "medium"; HIGH = "high"; CRITICAL = "critical"

class IncidentStatus(str, enum.Enum):
    DETECTED = "detected"; CLASSIFYING = "classifying"; REPORTING = "reporting"
    NOTIFIED = "notified"; RESOLVED = "resolved"

class Incident(Base):
    __tablename__ = "incidents"
    id                 = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id             = Column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False, index=True)
    reference_id       = Column(String(50), unique=True)
    threat_type        = Column(String(255))
    severity           = Column(Enum(IncidentSeverity))
    status             = Column(Enum(IncidentStatus), default=IncidentStatus.DETECTED)
    z_score            = Column(Float)
    mitre_ttps         = Column(JSON, default=list)
    source_ip          = Column(String(45))
    affected_systems   = Column(JSON, default=list)
    nis2_reportable    = Column(Boolean, default=False)
    dora_reportable    = Column(Boolean, default=False)
    early_warning_due  = Column(DateTime(timezone=True))
    notification_due   = Column(DateTime(timezone=True))
    final_report_due   = Column(DateTime(timezone=True))
    early_warning_sent = Column(DateTime(timezone=True), nullable=True)
    notification_sent  = Column(DateTime(timezone=True), nullable=True)
    final_report_sent  = Column(DateTime(timezone=True), nullable=True)
    raw_data           = Column(JSON, default=dict)
    detected_at        = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at        = Column(DateTime(timezone=True), nullable=True)
