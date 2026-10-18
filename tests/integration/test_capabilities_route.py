"""Integration tests for GET /api/v1/capabilities (CRA-001.A)."""
from __future__ import annotations
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from eoip.capabilities.model import CapabilityState
from eoip.capabilities.registry import CapabilityRegistry, get_capability_registry
from eoip.capabilities.router import router as capabilities_router

@pytest.fixture
def test_client(tmp_path):
    app = FastAPI(title="EOIP Capability Route Test")
    app.include_router(capabilities_router)

    reg = get_capability_registry()
    reg.reset()

    # Create dummy ledger to qualify one capability
    ledger = {
        "schema": "eoip-ledger-v3",
        "created_at": "2026-10-18T00:00:00Z",
        "items": [
            {"id": "CRA-001.1", "kind": "clause", "state": "ACCEPTED", "receipts": [{"path": "rcpt1.json", "sha256": "abc"}], "updated_at": "2026-10-18T00:00:00Z"},
        ],
    }
    led_file = tmp_path / "ledger.json"
    led_file.write_text(json.dumps(ledger), encoding="utf-8")
    reg.set_ledger_path(led_file)

    # 1. SUPPORTED_QUALIFIED
    reg.register("cap.qualified", "p1", "1.0", qualifying_clauses=["CRA-001.1"])

    # 2. SUPPORTED_UNQUALIFIED
    reg.register("cap.unqualified", "p2", "1.0", qualifying_clauses=["CRA-001.2"])

    # 3. DISABLED
    reg.register("cap.disabled", "p3", "1.0")
    reg.configure_state("cap.disabled", CapabilityState.DISABLED)

    # 4. UNAVAILABLE
    def failing_probe():
        return False
    reg.register("cap.unavailable", "p4", "1.0", probe=failing_probe)
    reg.probe_all()

    # 5. UNLICENSED
    reg.register("cap.unlicensed", "p5", "1.0")
    reg.configure_state("cap.unlicensed", CapabilityState.UNLICENSED)

    # 6. UNSUPPORTED
    reg.register("cap.unsupported", "p6", "1.0", initial_state=CapabilityState.UNSUPPORTED)

    return TestClient(app)

def test_list_all_six_states(test_client):
    res = test_client.get("/api/v1/capabilities")
    assert res.status_code == 200
    data = res.json()
    assert "capabilities" in data
    caps = {c["capability_id"]: c["state"] for c in data["capabilities"]}

    assert caps.get("cap.qualified") == "SUPPORTED_QUALIFIED"
    assert caps.get("cap.unqualified") == "SUPPORTED_UNQUALIFIED"
    assert caps.get("cap.disabled") == "DISABLED"
    assert caps.get("cap.unavailable") == "UNAVAILABLE"
    assert caps.get("cap.unlicensed") == "UNLICENSED"
    assert caps.get("cap.unsupported") == "UNSUPPORTED"

def test_get_capability_by_id(test_client):
    res = test_client.get("/api/v1/capabilities/cap.qualified")
    assert res.status_code == 200
    assert res.json()["capability_id"] == "cap.qualified"
    assert res.json()["state"] == "SUPPORTED_QUALIFIED"

    res404 = test_client.get("/api/v1/capabilities/nonexistent")
    assert res404.status_code == 404
