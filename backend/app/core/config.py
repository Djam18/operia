import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "OpérIA Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Dual-Mode: "auto", "local", "online"
    AGENT_MODE: str = os.getenv("AGENT_MODE", "auto")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./operia.db")
    
    # JWT Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "operia-dev-secret-key-change-me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours
    
    # Online API Keys (Optional - if missing, falls back to local mode)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    RESEND_API_KEY: Optional[str] = os.getenv("RESEND_API_KEY", None)
    
    # Mailing (Mailpit default for dev/infra, Resend fallback)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "mailpit")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "1025"))
    
    # Safeguards HITL defaults
    REQUIRE_HITL_EMAILS: bool = True
    REQUIRE_HITL_DATA_MUTATION: bool = True
    REQUIRE_HITL_EXPORTS: bool = True
    
    # Rate Limiting & Concurrency Quotas
    AGENT_RATE_LIMIT_PER_MINUTE: int = int(os.getenv("AGENT_RATE_LIMIT_PER_MINUTE", "10"))
    AGENT_MAX_CONCURRENCY: int = int(os.getenv("AGENT_MAX_CONCURRENCY", "3"))
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()

