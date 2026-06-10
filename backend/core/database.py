from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from backend.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def create_tables():
    """Auto-create all tables on startup. Safe to run repeatedly."""
    from backend.models.organisation import Organisation
    from backend.models.incident import Incident
    from backend.models.report import ComplianceReport
    from backend.models.audit import AuditLog
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
