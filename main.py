from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.routes import health, threats, incidents, compliance, reports, audit, billing

app = FastAPI(title="KalevioAI", version="0.1.0",
    description="NIS2/DORA Compliance Copilot — Detect threats. File reports. Automatically.",
    docs_url="/api/docs" if settings.APP_ENV != "production" else None, redoc_url=None)

app.add_middleware(CORSMiddleware, allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(health.router,     prefix="/api/v1")
app.include_router(threats.router,    prefix="/api/v1/threats")
app.include_router(incidents.router,  prefix="/api/v1/incidents")
app.include_router(compliance.router, prefix="/api/v1/compliance")
app.include_router(reports.router,    prefix="/api/v1/reports")
app.include_router(audit.router,      prefix="/api/v1/audit")
app.include_router(billing.router,    prefix="/api/v1/billing")

@app.on_event("startup")
async def startup():
    print("✅ KalevioAI started — ThreatFade online")
