from fastapi import APIRouter
from app.api.endpoints import router as core_endpoints_router
from app.api.v1.endpoints.admin import router as admin_router

router = APIRouter()

# Include all core domain endpoints (agent, operations, analytics, history, settings)
router.include_router(core_endpoints_router)

# Include dedicated admin panel router (/admin/*)
router.include_router(admin_router)
