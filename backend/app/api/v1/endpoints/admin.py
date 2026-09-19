import os
import resource
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.db.database import get_db
from app.db.models import Invoice, StagedAction, AuditLog, DataSource
from app.core.cache import app_cache
from app.core.queue import app_queue
from app.core.config import settings

router = APIRouter(prefix="/admin", tags=["admin"])

class AdminAgentConfigDTO(BaseModel):
    model_name: str = Field(default="gemini-1.5-pro")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    hitl_financial_threshold: float = Field(default=5000.0, ge=0.0)
    allowed_channels: List[str] = Field(default=["Email", "SMS", "Webhook"])
    auto_enrich_crm: bool = Field(default=True)
    strict_guardrails: bool = Field(default=True)

# In-memory runtime config that can be hot-reloaded
runtime_agent_config = AdminAgentConfigDTO()

class DemoTaskRequest(BaseModel):
    task_name: str = Field(default="reconcile_erp_batch")
    payload: Optional[Dict[str, Any]] = None

@router.get("/health")
async def get_admin_system_health(db: AsyncSession = Depends(get_db)):
    # 1. Database records count
    inv_count = (await db.execute(select(func.count(Invoice.id)))).scalar() or 0
    act_count = (await db.execute(select(func.count(StagedAction.action_id)))).scalar() or 0
    log_count = (await db.execute(select(func.count(AuditLog.id)))).scalar() or 0
    ds_count = (await db.execute(select(func.count(DataSource.id)))).scalar() or 0

    # 2. System memory usage (in MB via standard library resource)
    # ru_maxrss is in kilobytes on Linux
    max_rss_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    memory_mb = round(max_rss_kb / 1024, 1)

    cache_stats = await app_cache.get_stats()
    queue_stats = app_queue.get_stats()

    return {
        "status": "healthy",
        "app_version": settings.VERSION,
        "database": {
            "type": "SQLite (embarquée)",
            "invoices_count": inv_count,
            "staged_actions_count": act_count,
            "audit_logs_count": log_count,
            "data_sources_count": ds_count,
        },
        "system": {
            "memory_usage_mb": memory_mb,
            "cpu_threads": os.cpu_count() or 4,
            "uptime": "Nominal"
        },
        "cache": cache_stats,
        "queue": queue_stats
    }

@router.get("/cache")
async def get_cache_metrics():
    return await app_cache.get_stats()

@router.post("/cache/flush")
async def flush_cache():
    await app_cache.clear()
    new_stats = await app_cache.get_stats()
    return {"message": "Cache invalidé avec succès.", "stats": new_stats}

@router.get("/queue")
async def get_queue_dashboard():
    return {
        "stats": app_queue.get_stats(),
        "recent_tasks": app_queue.get_recent_tasks(limit=15)
    }

@router.post("/queue/retry")
async def retry_failed_tasks():
    count = await app_queue.retry_failed()
    return {"message": f"{count} tâche(s) relancée(s).", "retried_count": count}

@router.post("/queue/enqueue-demo")
async def enqueue_demo_task(req: DemoTaskRequest):
    task_id = await app_queue.enqueue(req.task_name, req.payload or {"source": "admin_panel"})
    return {"message": f"Tâche '{req.task_name}' ajoutée à la file.", "task_id": task_id}

@router.get("/config", response_model=AdminAgentConfigDTO)
async def get_runtime_config():
    return runtime_agent_config

@router.post("/config", response_model=AdminAgentConfigDTO)
async def update_runtime_config(req: AdminAgentConfigDTO):
    global runtime_agent_config
    runtime_agent_config = req
    # Invalidate cached analytics & agent settings on change
    await app_cache.invalidate("settings")
    return runtime_agent_config
