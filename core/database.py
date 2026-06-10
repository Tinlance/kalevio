from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

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
    """Auto-create all tables and seed default org."""
    try:
        from models.organisation import Organisation, PlanTier
        from models.incident import Incident
        from models.report import ComplianceReport
        from models.audit import AuditLog
        import uuid
        from sqlalchemy import select

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ DB tables created/verified")

        # Seed default org for pre-auth MVP
        default_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Organisation).where(Organisation.id == default_id)
            )
            existing = result.scalar_one_or_none()
            if not existing:
                org = Organisation(
                    id=default_id,
                    name="Default Organisation",
                    country_code="EE",
                    plan_tier=PlanTier.FREE,
                    is_active=True,
                )
                session.add(org)
                await session.commit()
                print("✅ Default org seeded")
            else:
                print("✅ Default org exists")
    except Exception as e:
        print(f"⚠️ DB setup failed: {e} — continuing")
