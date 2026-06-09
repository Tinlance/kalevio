from sqlalchemy import Column, String, Float, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.core.database import Base

class ThreatDetection(Base):
    __tablename__ = "threat_detections"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id        = Column(UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False, index=True)
    incident_id   = Column(UUID(as_uuid=True), ForeignKey("incidents.id"), nullable=True)
    threat_name   = Column(String(255))
    threat_family = Column(String(100))
    z_score       = Column(Float, nullable=False)
    packet_count  = Column(Integer, default=0)
    source_ip     = Column(String(45))
    dest_ip       = Column(String(45))
    protocol      = Column(String(20))
    mitre_ttps    = Column(JSON, default=list)
    raw_features  = Column(JSON, default=dict)
    pcap_filename = Column(String(500), nullable=True)
    detected_at   = Column(DateTime(timezone=True), server_default=func.now())
