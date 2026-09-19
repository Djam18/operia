import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.database import engine, Base, AsyncSessionLocal
from app.db.seed import seed_database

from sqlalchemy import update
from app.db.models import StagedAction, DataSource, Customer

@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await seed_database(session)
        # Reset mutable states between tests
        await session.execute(
            update(StagedAction)
            .where(StagedAction.action_id.in_(["act-4820", "act-4821", "act-4822", "act-4817"]))
            .values(status="PENDING", resolved_at=None)
        )
        await session.execute(
            update(DataSource).values(is_connected=True, status="COMPLETED")
        )
        await session.execute(
            update(Customer).where(Customer.name == "Atelier N7").values(credit_limit=25000.0)
        )
        await session.commit()

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_data_sources():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/data-sources")
    assert response.status_code == 200
    sources = response.json()
    assert len(sources) == 5
    source_names = [s["name"] for s in sources]
    assert any("Clients" in s for s in source_names)
    assert any("financière" in s for s in source_names)

@pytest.mark.asyncio
async def test_operations_listing_and_filtering():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # All operations
        res_all = await ac.get("/api/v1/operations")
        assert res_all.status_code == 200
        ops = res_all.json()
        assert len(ops) >= 7

        # Filter by Pending
        res_pending = await ac.get("/api/v1/operations?status=PENDING")
        assert res_pending.status_code == 200
        pending_ops = res_pending.json()
        assert all(o["status"] == "PENDING" for o in pending_ops)

@pytest.mark.asyncio
async def test_validate_operation_human_in_the_loop():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Validate act-4821
        res = await ac.post("/api/v1/operations/act-4821/validate")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "COMPLETED"

        # Check in history that audit log was registered
        hist_res = await ac.get("/api/v1/history")
        assert hist_res.status_code == 200
        history_items = hist_res.json()
        assert any("Relance" in item["action"] or "act-4821" in item["query"] for item in history_items)

        # Check outbox has local delivered emails
        outbox_res = await ac.get("/api/v1/operations/outbox")
        assert outbox_res.status_code == 200
        outbox_emails = outbox_res.json()
        assert len(outbox_emails) > 0
        assert outbox_emails[0]["delivery_mode"] in ["local_outbox", "online_resend", "smtp_mailpit"]

@pytest.mark.asyncio
async def test_refuse_operation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/operations/act-4817/refuse", json={"reason": "Attente retour fournisseur"})
        assert res.status_code == 200
        assert res.json()["status"] == "REFUSED"

@pytest.mark.asyncio
async def test_batch_validate_operations():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/operations/batch-validate", json={"action_ids": ["act-4816", "act-4815"]})
        assert res.status_code == 200
        data = res.json()
        assert data["validated_count"] == 2

@pytest.mark.asyncio
async def test_connectivity_status():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/status/connectivity")
        assert res.status_code == 200
        data = res.json()
        assert "mode" in data
        assert "database_type" in data

@pytest.mark.asyncio
async def test_agent_chat_stream():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/agent/chat/stream", json={"query": "Donne-moi les factures impayées depuis plus de 30 jours."})
        assert res.status_code == 200
        assert "text/event-stream" in res.headers["content-type"]
        body = res.text
        assert "erp.factures.query" in body
        assert "crm.comptes.enrich" in body
        assert "act-4821" in body

@pytest.mark.asyncio
async def test_analytics_and_templates_and_version_header():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Check X-API-Version header
        res_health = await ac.get("/health")
        assert res_health.headers.get("X-API-Version") == "1.0.0"

        # Check analytics endpoint
        res_analytics = await ac.get("/api/v1/analytics")
        assert res_analytics.status_code == 200
        data_a = res_analytics.json()
        assert data_a["recovered_amount_eur"] >= 86420.0
        assert data_a["hours_saved"] >= 46
        assert len(data_a["aging_buckets"]) == 4

        # Check templates endpoint
        res_templates = await ac.get("/api/v1/templates")
        assert res_templates.status_code == 200
        data_t = res_templates.json()
        assert len(data_t) == 6
        assert data_t[0]["id"] == "pb-1"

@pytest.mark.asyncio
async def test_dashboard_stats(init_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/dashboard/stats")
        assert res.status_code == 200
        data = res.json()
        assert "queries_count" in data
        assert "actions_count" in data
        assert "pending_count" in data
        assert "completed_count" in data
        assert data["queries_count"] >= 128
        assert data["actions_count"] >= 1

@pytest.mark.asyncio
async def test_advanced_analytics(init_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/analytics/advanced")
        assert res.status_code == 200
        data = res.json()
        assert "dso" in data
        assert "pareto" in data
        assert "top_risk_clients" in data
        assert "pareto_insight" in data
        assert data["dso"]["current_dso_days"] == 48.2
        assert data["dso"]["prior_dso_days"] == 64.5
        assert len(data["pareto"]) == 5
        assert len(data["top_risk_clients"]) > 0
        assert "80/20" in data["pareto_insight"]

@pytest.mark.asyncio
async def test_auth_login_and_me(init_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Login with valid credentials
        login_res = await ac.post("/api/v1/auth/login", json={
            "email": "admin@operia.io",
            "password": "admin123"
        })
        assert login_res.status_code == 200
        login_data = login_res.json()
        assert "access_token" in login_data
        assert login_data["user"]["email"] == "admin@operia.io"
        token = login_data["access_token"]

        # 2. Get /auth/me with Bearer token
        me_res = await ac.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_res.status_code == 200
        me_data = me_res.json()
        assert me_data["email"] == "admin@operia.io"
        assert me_data["role"] == "ADMIN"

@pytest.mark.asyncio
async def test_auth_invalid_credentials(init_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/auth/login", json={
            "email": "admin@operia.io",
            "password": "wrongpassword"
        })
        assert res.status_code == 401

@pytest.mark.asyncio
async def test_toggle_data_source_circuit_breaker(init_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Disconnect src-fin
        res = await ac.post("/api/v1/data-sources/src-fin/toggle")
        assert res.status_code == 200
        data = res.json()
        assert data["is_connected"] is False
        assert data["status"] == "DISCONNECTED"

        # 2. Verify agent chat blocks query with circuit breaker
        chat_res = await ac.post("/api/v1/agent/chat/stream", json={"query": "Factures impayées"})
        assert chat_res.status_code == 200
        assert "Coupe-circuit" in chat_res.text or "déconnectée" in chat_res.text

        # 3. Reconnect src-fin
        res_reconnect = await ac.post("/api/v1/data-sources/src-fin/toggle")
        assert res_reconnect.status_code == 200
        assert res_reconnect.json()["is_connected"] is True

@pytest.mark.asyncio
async def test_validate_export_csv_operation(init_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/operations/act-4820/validate")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "COMPLETED"
        assert data["execution"]["status"] == "success"
        download_url = data["execution"]["download_url"]

        # Download generated file
        dl_res = await ac.get(download_url)
        assert dl_res.status_code == 200
        assert "ID Client" in dl_res.text
        assert "Nova Conseil" in dl_res.text

@pytest.mark.asyncio
async def test_validate_ajustement_encours(init_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Validate act-4822 (adjust Atelier N7 credit limit to 35,000)
        res = await ac.post("/api/v1/operations/act-4822/validate")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "COMPLETED"
        assert data["execution"]["new_credit_limit"] == 35000.0

@pytest.mark.asyncio
async def test_sqladmin_login_and_redirect():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", follow_redirects=False) as ac:
        # 1. Unauthenticated request redirects to /admin/login
        res = await ac.get("/admin/")
        assert res.status_code in [302, 303, 307]
        assert "/login" in res.headers.get("location", "")

@pytest.mark.asyncio
async def test_conversations_api_lifecycle(init_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. List conversations (should include seeded conv-factures)
        res = await ac.get("/api/v1/conversations")
        assert res.status_code == 200
        convs = res.json()
        assert any(c["id"] == "conv-factures" for c in convs)

        # 2. Get messages for conv-factures
        msg_res = await ac.get("/api/v1/conversations/conv-factures/messages")
        assert msg_res.status_code == 200
        msgs = msg_res.json()
        assert len(msgs) >= 2
        assert any(m["sender"] == "user" for m in msgs)
        assert any(m["sender"] == "assistant" for m in msgs)

        # 3. Post a chat to a new conversation
        new_conv_id = "conv-test-cycle"
        stream_res = await ac.post("/api/v1/agent/chat/stream", json={"query": "Bonjour OpérIA", "conversation_id": new_conv_id})
        assert stream_res.status_code == 200

        # 4. Verify new conversation exists
        list_again = await ac.get("/api/v1/conversations")
        assert any(c["id"] == new_conv_id for c in list_again.json())

        # 5. Delete test conversation
        del_res = await ac.delete(f"/api/v1/conversations/{new_conv_id}")
        assert del_res.status_code == 200
        assert del_res.json()["deleted"] == new_conv_id

        # 6. Verify deleted
        list_after_del = await ac.get("/api/v1/conversations")
        assert not any(c["id"] == new_conv_id for c in list_after_del.json())



