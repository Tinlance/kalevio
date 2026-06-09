from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_SECRET_KEY: str = "dev-secret-change-in-production"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://kalevioai.com"]
    DATABASE_URL: str = "postgresql+asyncpg://kalevio:kalevio@localhost:5432/kalevio_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    ANTHROPIC_API_KEY: str = ""
    GROK_API_KEY: str = ""
    LLM_TIMEOUT_SECONDS: int = 10
    LLM_PRIMARY: str = "claude-sonnet-4-5"
    LLM_FALLBACK: str = "grok-3"
    CLERK_SECRET_KEY: str = ""
    RESEND_API_KEY: str = ""
    RESEND_FROM_EMAIL: str = "alerts@kalevioai.com"
    LEMONSQUEEZY_API_KEY: str = ""
    LEMONSQUEEZY_STORE_ID: str = ""
    LEMONSQUEEZY_WEBHOOK_SECRET: str = ""
    SENTRY_DSN: str = ""
    GEMINI_API_KEY: str = ""
    THREATFADE_ZSCORE_THRESHOLD: float = 2.5
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
