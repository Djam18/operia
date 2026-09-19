from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.queue import app_queue
from app.db.database import engine, Base, AsyncSessionLocal
from app.db.seed import seed_database
from app.api.v1.router import router as api_v1_router
from app.admin import setup_admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema & seed data
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as session:
        await seed_database(session)
        
    # Start background task queue worker
    await app_queue.start_worker()
    
    yield
    
    # Stop background task queue worker and dispose DB
    await app_queue.stop_worker()
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_api_version_header(request, call_next):
    response = await call_next(request)
    response.headers["X-API-Version"] = settings.VERSION
    return response

# Versioned API Router
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

# Django-style Backoffice Admin (/admin)
setup_admin(app, engine)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME, "version": settings.VERSION}

@app.get("/api/versions")
async def list_api_versions():
    """Root version discovery endpoint adhering to Enterprise API versioning standards."""
    return {
        "current_version": settings.VERSION,
        "supported_versions": [
            {
                "version": "v1",
                "status": "CURRENT",
                "prefix": "/api/v1",
                "docs_url": "/docs",
                "released_at": "2026-09-01",
                "deprecated": False
            }
        ],
        "features": {
            "caching": "TTL in-memory async cache with live telemetry",
            "task_queue": "Async background worker queue with retries",
            "resilient_streaming": "SSE with heartbeats and event IDs",
            "heavy_queries": "Indexed multi-aggregation queries over 18k+ records"
        }
    }
