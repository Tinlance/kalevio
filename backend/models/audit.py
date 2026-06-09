from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.sql import func
from backend.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id            = Column(Integer, primary_key=True, autoincrement=True)
    org_id        = Column(String(255), nullable=False, index=True)
    event_type    = Column(String(100), nullable=False, index=True)
    payload       = Column(JSON, default=dict)
    user_id       = Column(String(255), nullable=True)
    timestamp     = Column(String(50), nullable=False)
    previous_hash = Column(String(64), nullable=False)
    entry_hash    = Column(String(64), nullable=False, unique=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
