"""Unit tests for REVA REST API, MCP tools, and view budget engine."""

import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.reva_depth("unit")

from reva.api import reva_router, set_api_kernel
from reva.kernel.kernel import WarrantKernel
from reva.kernel.store import RevaStore
from reva.kernel.translog import MerkleLog
from reva.mcp.server import (
    reva_ground_answer,
    reva_list_trace_templates,
    reva_search_warrants,
    set_mcp_kernel,
)
from reva.views.budget import (
    create_continuation_token,
    estimate_tokens,
    verify_continuation_token,
)


@pytest.fixture
def api_client():
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(reva_router, prefix="/api/reva/v1")

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        store = RevaStore(str(db_path))
        kernel = WarrantKernel(store=store)
        set_api_kernel(kernel)
        set_mcp_kernel(kernel)
        client = TestClient(app)
        try:
            yield client
        finally:
            store.conn.close()


def test_api_health(api_client):
    resp = api_client.get("/api/reva/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "version": "1.0.0"}


def test_api_query_warrants_empty(api_client):
    resp = api_client.post("/api/reva/v1/warrants/query", json={"limit": 10})
    assert resp.status_code == 200
    assert resp.json()["total"] == 0


def test_api_gaps_lifecycle(api_client):
    create_resp = api_client.post(
        "/api/reva/v1/gaps",
        json={
            "domain": "security",
            "question": "What is the key rotation interval?",
            "scope": {"entity": "key:root"},
            "severity": "medium",
        },
    )
    assert create_resp.status_code == 200
    gap_data = create_resp.json()
    assert gap_data["status"] == "open"
    assert "gap_id" in gap_data

    # List gaps
    list_resp = api_client.get("/api/reva/v1/gaps")
    assert list_resp.status_code == 200
    assert list_resp.json()["total"] == 1


def test_continuation_tokens():
    key = b"secret_hmac_key_32_bytes_long_1234"
    tok = create_continuation_token(
        hmac_key=key,
        tenant_id="tenant_1",
        principal_id="alice",
        parent_id="vw1_test",
        view="collection",
        collection="items",
        offset=50,
    )
    assert "." in tok

    payload = verify_continuation_token(
        hmac_key=key,
        token=tok,
        expected_tenant="tenant_1",
        expected_principal="alice",
    )
    assert payload["offset"] == 50
    assert payload["collection"] == "items"


def test_mcp_tools():
    templates = reva_list_trace_templates()
    assert "impact.downstream" in templates

    ans = reva_ground_answer("What is the primary key?")
    assert "answer_text" in ans
    assert ans["epistemic_state"] == "unknown"
