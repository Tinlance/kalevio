from sqlalchemy import Column, String, Boolean, DateTime, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid, enum
from backend.core.database import Base

class PlanTier(str, enum.Enum):
    FREE = "free"; PROFESSIONAL = "professional"; GUARDIAN = "guardian"; MSSP = "mssp"

class Organisation(Base):
    __tablename__ = "organisations"
    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name           = Column(String(255), nullable=False)
    country_code   = Column(String(2), nullable=False, default="EE")
    plan_tier      = Column(Enum(PlanTier), default=PlanTier.FREE)
    clerk_org_id   = Column(String(255), unique=True, index=True)
    ls_customer_id = Column(String(255), nullable=True)
    is_active      = Column(Boolean, default=True)
    nis2_in_scope  = Column(Boolean, nullable=True)
    dora_in_scope  = Column(Boolean, nullable=True)
    settings       = Column(JSON, default=dict)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
    updated_at     = Column(DateTime(timezone=True), onupdate=func.now())
