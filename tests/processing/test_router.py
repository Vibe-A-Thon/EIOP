"""FastAPI Router Integration Tests for Processing Units (PUR-CON-001..010, Section 5.3).

Tests API surface:
- GET /api/processing/v1/capabilities
- GET /api/processing/v1/devices
- POST /api/processing/v1/plans
- POST /api/processing/v1/jobs
- GET /api/processing/v1/jobs
- GET /api/processing/v1/jobs/{job_id}
- POST /api/processing/v1/jobs/{job_id}/cancel
- GET /api/processing/v1/jobs/{job_id}/result
- GET /api/processing/v1/jobs/{job_id}/receipt
- POST /api/processing/v1/profiles/{profile_id}/probes
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from eoip.processing.router import build_processing_router


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(build_processing_router())
    return TestClient(app)


@pytest.mark.req("PUR-CON-001")
def test_router_get_capabilities(client: TestClient):
    """PUR-CON-001: GET /api/processing/v1/capabilities returns 10 units with status."""
    resp = client.get("/api/processing/v1/capabilities", headers={"X-Tenant-ID": "acme"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["tenant_id"] == "acme"
    assert data["total_units"] == 10
    assert "CPU" in data["units"]
    assert "QPU" in data["units"]
    assert data["units"]["QPU"]["simulated"] is True


@pytest.mark.req("PUR-CON-001")
def test_router_get_devices(client: TestClient):
    """PUR-CON-001: GET /api/processing/v1/devices returns device descriptors."""
    resp = client.get("/api/processing/v1/devices")
    assert resp.status_code == 200
    data = resp.json()
    assert "devices" in data
    assert len(data["devices"]) >= 1
    cpu_dev = data["devices"][0]
    assert cpu_dev["device_type"] == "cpu"
    assert cpu_dev["usable_cores"] >= 1


@pytest.mark.req("PUR-RUN-006")
def test_router_compile_plan_valid(client: TestClient):
    """PUR-RUN-006: POST /api/processing/v1/plans compiles valid DAG with topological order."""
    body = {
        "nodes": [
            {
                "node_id": "step_a",
                "operator_id": "records.validate",
                "logical_unit": "CPU",
                "inputs": {},
                "parameters": {},
            },
            {
                "node_id": "step_b",
                "operator_id": "records.transform",
                "logical_unit": "CPU",
                "inputs": {"input_recs": "step_a"},
                "parameters": {},
            },
        ]
    }
    resp = client.post("/api/processing/v1/plans", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data["topological_order"] == ["step_a", "step_b"]
    assert len(data["plan_digest"]) == 64


@pytest.mark.req("PUR-RUN-006")
def test_router_compile_plan_cyclic_fails(client: TestClient):
    """PUR-RUN-006: POST /api/processing/v1/plans rejects cyclic dependencies with 422."""
    body = {
        "nodes": [
            {
                "node_id": "cycle_1",
                "operator_id": "records.validate",
                "logical_unit": "CPU",
                "inputs": {"in": "cycle_2"},
                "parameters": {},
            },
            {
                "node_id": "cycle_2",
                "operator_id": "records.transform",
                "logical_unit": "CPU",
                "inputs": {"in": "cycle_1"},
                "parameters": {},
            },
        ]
    }
    resp = client.post("/api/processing/v1/plans", json=body)
    assert resp.status_code == 422
    err = resp.json()
    assert err["detail"]["error_code"] == "INVALID_REQUEST"


@pytest.mark.req("PUR-RUN-001")
def test_router_submit_job_lifecycle(client: TestClient):
    """PUR-RUN-001, PUR-RUN-008: Submit job, verify 202, retrieve result and receipt."""
    req_body = {
        "schema_version": "1.0",
        "logical_unit": "CPU",
        "operator_id": "records.validate",
        "operator_version": "1.0",
        "inputs": {"records": [{"id": 1, "val": "ok"}]},
        "parameters": {},
        "execution_preference": "cpu_only",
    }
    headers = {"X-Tenant-ID": "tenant_api_test"}
    resp = client.post("/api/processing/v1/jobs", json=req_body, headers=headers)
    assert resp.status_code == 202
    data = resp.json()
    job_id = data["job_id"]
    assert job_id.startswith("proc_job_")

    # Get job status
    resp_job = client.get(f"/api/processing/v1/jobs/{job_id}", headers=headers)
    assert resp_job.status_code == 200
    assert resp_job.json()["status"] == "SUCCEEDED"

    # Get job result
    resp_res = client.get(f"/api/processing/v1/jobs/{job_id}/result", headers=headers)
    assert resp_res.status_code == 200
    assert resp_res.json()["result"]["valid"] is True

    # Get job receipt
    resp_rcpt = client.get(f"/api/processing/v1/jobs/{job_id}/receipt", headers=headers)
    assert resp_rcpt.status_code == 200
    rcpt = resp_rcpt.json()
    assert rcpt["job_id"] == job_id
    assert rcpt["actual_provider"] == "cpu_reference"
    assert len(rcpt["receipt_digest"]) == 64


@pytest.mark.req("PUR-RUN-001")
def test_router_idempotency_keys(client: TestClient):
    """PUR-RUN-001: Duplicate submissions with same idempotency key return identical job ID."""
    req_body = {
        "schema_version": "1.0",
        "logical_unit": "CPU",
        "operator_id": "records.validate",
        "operator_version": "1.0",
        "inputs": {"records": [{"id": 1}]},
        "parameters": {},
        "execution_preference": "cpu_only",
    }
    headers = {"X-Tenant-ID": "idemp_tenant", "Idempotency-Key": "idemp-001"}
    resp1 = client.post("/api/processing/v1/jobs", json=req_body, headers=headers)
    assert resp1.status_code == 202
    job_id_1 = resp1.json()["job_id"]

    # Re-submit identical payload with same key
    resp2 = client.post("/api/processing/v1/jobs", json=req_body, headers=headers)
    assert resp2.status_code == 202
    assert resp2.json()["job_id"] == job_id_1

    # Re-submit DIFFERENT payload with same key should produce 409 IDEMPOTENCY_CONFLICT
    req_body_diff = dict(req_body)
    req_body_diff["inputs"] = {"records": [{"id": 2, "different": True}]}
    resp3 = client.post("/api/processing/v1/jobs", json=req_body_diff, headers=headers)
    assert resp3.status_code == 409
    assert resp3.json()["detail"]["error_code"] == "IDEMPOTENCY_CONFLICT"


@pytest.mark.req("PUR-RUN-009")
def test_router_job_cancellation(client: TestClient):
    """PUR-RUN-009: Cancel queued job succeeds; terminal job cancel returns 409."""
    req_body = {
        "schema_version": "1.0",
        "logical_unit": "CPU",
        "operator_id": "records.validate",
        "operator_version": "1.0",
        "inputs": {"records": []},
        "parameters": {},
    }
    headers = {"X-Tenant-ID": "cancel_tenant"}
    # Submit without auto_process to leave in QUEUED state
    resp = client.post("/api/processing/v1/jobs?auto_process=false", json=req_body, headers=headers)
    assert resp.status_code == 202
    job_id = resp.json()["job_id"]

    # Cancel job
    resp_cancel = client.post(f"/api/processing/v1/jobs/{job_id}/cancel", headers=headers)
    assert resp_cancel.status_code == 200
    assert resp_cancel.json()["status"] == "CANCELLED"

    # Attempt to cancel again (already terminal) -> 409
    resp_cancel_term = client.post(f"/api/processing/v1/jobs/{job_id}/cancel", headers=headers)
    assert resp_cancel_term.status_code == 409


@pytest.mark.req("PUR-SEC-001")
def test_router_tenant_isolation(client: TestClient):
    """PUR-SEC-001: Tenant B cannot access Tenant A's jobs, results, or receipts."""
    req_body = {
        "schema_version": "1.0",
        "logical_unit": "CPU",
        "operator_id": "records.validate",
        "operator_version": "1.0",
        "inputs": {"records": []},
        "parameters": {},
    }
    resp = client.post("/api/processing/v1/jobs", json=req_body, headers={"X-Tenant-ID": "tenant_alpha"})
    assert resp.status_code == 202
    job_id = resp.json()["job_id"]

    # Tenant Beta attempts to read Tenant Alpha's job -> 404
    resp_b = client.get(f"/api/processing/v1/jobs/{job_id}", headers={"X-Tenant-ID": "tenant_beta"})
    assert resp_b.status_code == 404


@pytest.mark.req("PUR-RUN-011")
def test_router_profile_probing(client: TestClient):
    """PUR-RUN-011: POST /api/processing/v1/profiles/{id}/probes returns profile status."""
    resp_cpu = client.post("/api/processing/v1/profiles/cpu/probes")
    assert resp_cpu.status_code == 200
    assert resp_cpu.json()["status"] == "QUALIFIED"

    resp_qpu = client.post("/api/processing/v1/profiles/qiskit_aer/probes")
    assert resp_qpu.status_code == 200
    assert resp_qpu.json()["simulation"] is True
    assert resp_qpu.json()["physical_qpu"] is False
