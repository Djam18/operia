import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_api_versions_discovery():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/versions")
        assert response.status_code == 200
        data = response.json()
        assert "current_version" in data
        assert len(data["supported_versions"]) >= 1
        assert data["supported_versions"][0]["prefix"] == "/api/v1"
        assert "caching" in data["features"]

@pytest.mark.asyncio
async def test_admin_system_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/admin/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"]["invoices_count"] > 0
        assert "memory_usage_mb" in data["system"]
        assert "hit_ratio_percent" in data["cache"]
        assert "total_tasks" in data["queue"]

@pytest.mark.asyncio
async def test_admin_cache_lifecycle():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Trigger analytics call which populates cache
        res_analytics = await ac.get("/api/v1/analytics")
        assert res_analytics.status_code == 200
        
        # 2. Get cache metrics
        res_cache = await ac.get("/api/v1/admin/cache")
        assert res_cache.status_code == 200
        cache_data = res_cache.json()
        assert cache_data["total_cached_entries"] >= 1
        
        # 3. Flush cache
        res_flush = await ac.post("/api/v1/admin/cache/flush")
        assert res_flush.status_code == 200
        assert res_flush.json()["stats"]["total_cached_entries"] == 0

@pytest.mark.asyncio
async def test_admin_queue_enqueue_and_stats():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Enqueue demo task
        res_enqueue = await ac.post("/api/v1/admin/queue/enqueue-demo", json={"task_name": "test_batch_export"})
        assert res_enqueue.status_code == 200
        task_id = res_enqueue.json()["task_id"]
        assert task_id.startswith("task-")
        
        # Check queue status
        res_queue = await ac.get("/api/v1/admin/queue")
        assert res_queue.status_code == 200
        q_data = res_queue.json()
        assert q_data["stats"]["total_tasks"] >= 1
        task_ids = [t["id"] for t in q_data["recent_tasks"]]
        assert task_id in task_ids

@pytest.mark.asyncio
async def test_admin_runtime_config():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Get config
        res = await ac.get("/api/v1/admin/config")
        assert res.status_code == 200
        cfg = res.json()
        assert "model_name" in cfg
        assert "hitl_financial_threshold" in cfg
        
        # Update config
        res_update = await ac.post("/api/v1/admin/config", json={
            "model_name": "gemini-1.5-flash",
            "temperature": 0.4,
            "hitl_financial_threshold": 8000.0,
            "allowed_channels": ["Email", "Webhook"],
            "auto_enrich_crm": True,
            "strict_guardrails": True
        })
        assert res_update.status_code == 200
        updated = res_update.json()
        assert updated["model_name"] == "gemini-1.5-flash"
        assert updated["temperature"] == 0.4
        assert updated["hitl_financial_threshold"] == 8000.0
