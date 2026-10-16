"""Comprehensive Unit & Integration Tests for Advanced Enterprise Cognitive Capabilities.

Verifies:
1. Live Causal Digital Twin & Counterfactual Blast Radius Engine
2. Multi-Paradigm Query Dispatcher (5 Heterogeneous Kernels)
3. Domain Pack Lifecycle & Deployment Manager (Real Schema Extension & Entity Provisioning)
4. Verifiable Zero-Knowledge XAI Decision Factor Attribution Ledger (Merkle & HMAC Proofs)
5. Resilient Agent Mesh Supervisor & Auto-Recovery
6. FastAPI Endpoints Integration
"""

from __future__ import annotations

import pytest
from eoip.agents.mesh_supervisor import ResilientAgentMeshSupervisor
from eoip.audit.xai_ledger import VerifiableXAIAttributionLedger
from eoip.graph.memory import MemoryGraphStore
from eoip.moonshot.live_causal_engine import LiveCausalGraphEngine
from eoip.ontology.domain_pack_manager import DomainPackLifecycleManager
from eoip.query.multi_paradigm_dispatcher import MultiParadigmQueryDispatcher
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def populated_store() -> MemoryGraphStore:
    store = MemoryGraphStore()

    # Create real enterprise topology
    v1 = store.upsert_vertex(
        "Service",
        {
            "canonical_id": "svc-api-gw",
            "name": "API Gateway Service",
            "criticality": "CRITICAL",
            "resilience": 0.5,
            "status": "OPERATIONAL",
        },
    )
    v2 = store.upsert_vertex(
        "Service",
        {
            "canonical_id": "svc-auth",
            "name": "Authentication & Session Service",
            "criticality": "HIGH",
            "resilience": 0.4,
            "status": "OPERATIONAL",
        },
    )
    v3 = store.upsert_vertex(
        "Database",
        {
            "canonical_id": "db-users",
            "name": "Postgres User Database Cluster",
            "criticality": "CRITICAL",
            "resilience": 0.7,
            "status": "OPERATIONAL",
        },
    )
    v4 = store.upsert_vertex(
        "Service",
        {
            "canonical_id": "svc-billing",
            "name": "Payment & Ledger Processor",
            "criticality": "HIGH",
            "resilience": 0.6,
            "status": "OPERATIONAL",
        },
    )

    # Establish dependency relationships
    store.upsert_edge("DEPENDS_ON", v1["vid"], v2["vid"], {"coupling": 0.95})
    store.upsert_edge("DEPENDS_ON", v2["vid"], v3["vid"], {"coupling": 0.90})
    store.upsert_edge("CALLS", v1["vid"], v4["vid"], {"coupling": 0.85})
    store.upsert_edge("DEPENDS_ON", v4["vid"], v3["vid"], {"coupling": 0.90})

    return store


# -------------------------------------------------------------
# Test 1: Live Causal Digital Twin & Counterfactual Blast Radius
# -------------------------------------------------------------
def test_live_causal_blast_radius(populated_store: MemoryGraphStore):
    engine = LiveCausalGraphEngine(populated_store)

    # Shock the root database
    blast = engine.compute_blast_radius(
        shock_entities={"db-users": 1.0},
        max_depth=3,
        failure_threshold=0.4,
    )

    assert blast["total_nodes_evaluated"] >= 3
    assert blast["total_steps"] >= 1
    assert "db-users" in blast["collapsed_nodes"]
    assert blast["systemic_loss_score"] > 0.0

    # Counterfactual intervention: harden svc-auth resilience to 0.95
    cf = engine.evaluate_counterfactual(
        shock_entities={"db-users": 0.9},
        interventions={"svc-auth": 0.95},
        max_depth=3,
    )

    assert "baseline_loss" in cf
    assert "mitigated_loss" in cf
    assert cf["baseline_loss"] >= cf["mitigated_loss"]
    assert "effective_roi" in cf


# -------------------------------------------------------------
# Test 2: Multi-Paradigm Query Dispatcher
# -------------------------------------------------------------
def test_multi_paradigm_query_dispatcher(populated_store: MemoryGraphStore):
    dispatcher = MultiParadigmQueryDispatcher(populated_store)

    response = dispatcher.execute(
        query="What is the architecture and dependency impact of the API Gateway and User Database?",
        seed_canonical_ids=["svc-api-gw", "db-users"],
        max_depth=2,
        monte_carlo_samples=30,
    )

    assert response.query is not None
    assert len(response.deterministic_subgraph["nodes"]) >= 2
    assert len(response.probabilistic_matches) >= 1
    assert len(response.heuristic_paths) >= 1
    assert "monte_carlo_trials" in response.stochastic_metrics
    assert "executive_summary" in response.cognitive_narration

    # Verify all 5 kernel paradigms executed
    paradigms = [k["paradigm"] for k in response.kernel_breakdown]
    assert "DETERMINISTIC" in paradigms
    assert "PROBABILISTIC" in paradigms
    assert "HEURISTIC" in paradigms
    assert "STOCHASTIC" in paradigms
    assert "NON_DETERMINISTIC" in paradigms


# -------------------------------------------------------------
# Test 3: Domain Pack Lifecycle & Deployment Manager
# -------------------------------------------------------------
def test_domain_pack_lifecycle_manager(populated_store: MemoryGraphStore, tmp_path):
    manager = DomainPackLifecycleManager(populated_store)

    packs = manager.list_packs()
    assert len(packs) >= 1

    # Activate cybersecurity pack
    activation = manager.activate_pack("cybersecurity", seed_live_topology=True)
    assert activation["status"] == "ACTIVATED"
    assert "Asset" in activation["classes_registered"]
    assert activation["entities_seeded"] >= 2
    assert "cybersecurity" in manager.get_active_packs()

    # Query newly seeded vertex directly from GraphStore
    seeded_v = populated_store.get_vertex_by_canonical_id("cyber-asset-gw-01")
    assert seeded_v is not None
    assert seeded_v["label"] == "Asset"
    assert seeded_v["properties"]["criticality"] == "CRITICAL"


# -------------------------------------------------------------
# Test 4: Verifiable Zero-Knowledge XAI Decision Ledger
# -------------------------------------------------------------
def test_verifiable_xai_attribution_ledger():
    ledger = VerifiableXAIAttributionLedger(signing_secret="test-secret-salt-12345")

    evidence = [
        {"canonical_id": "svc-api-gw", "properties": {"criticality": "CRITICAL", "resilience": 0.5}},
        {"canonical_id": "db-users", "properties": {"criticality": "CRITICAL", "status": "OPERATIONAL"}},
    ]

    cert = ledger.certify_decision(
        decision_id="dec-audit-001",
        agent_id="remediation-agent",
        decision_summary="Rerouted API traffic to redundant cluster due to database saturation",
        evidence_entities=evidence,
        private_reasoning_trace="Internal prompt tokens: DO NOT DISCLOSE",
    )

    assert cert.certificate_id.startswith("xai-cert-")
    assert cert.factor_count >= 2
    assert cert.merkle_root is not None
    assert cert.signature is not None

    # Verify mathematical validity
    assert ledger.verify_certificate(cert.to_dict()) is True

    # Tampering test: modify a factor attribution weight
    tampered_data = cert.to_dict()
    tampered_data["factors"][0]["attribution_weight"] = 999.99
    assert ledger.verify_certificate(tampered_data) is False


# -------------------------------------------------------------
# Test 5: Resilient Agent Mesh & Auto-Recovery
# -------------------------------------------------------------
def test_resilient_agent_mesh_supervisor(tmp_path):
    supervisor = ResilientAgentMeshSupervisor(storage_dir=tmp_path)

    # Start session
    bundle = supervisor.start_session(
        agent_id="incident-triage-agent",
        request_id="req-9918",
        goal="Diagnose and mitigate payment failure cascade",
        initial_state={"step": "DISCOVERY", "discovered_nodes": ["svc-billing"]},
    )

    assert bundle.status == "IN_PROGRESS"

    # Checkpoint step
    supervisor.checkpoint_step(
        bundle.recovery_id,
        step_name="ANALYZE_LOGS",
        state_update={"logs_analyzed": 1420},
    )

    # Simulate unexpected failure
    failed_bundle = supervisor.mark_failed(
        bundle.recovery_id,
        error="ConnectionResetError: External provider timed out during payment verification",
    )
    assert failed_bundle.status == "FAILED"
    assert failed_bundle.error_message is not None

    # Recover session
    recovered = supervisor.recover(
        bundle.recovery_id,
        resume_handler=lambda b: {"action": "RESUMED_FROM_CHECKPOINT", "resumed_from": b.last_completed_step},
    )

    assert recovered["status"] == "RECOVERED"
    assert recovered["result"]["resumed_from"] == "ANALYZE_LOGS"


# -------------------------------------------------------------
# Test 6: FastAPI Integration Endpoints
# -------------------------------------------------------------
def test_advanced_capabilities_api_endpoints(populated_store: MemoryGraphStore):
    from eoip.enterprise.advanced_router import build_advanced_capabilities_router

    app = FastAPI()
    app.include_router(build_advanced_capabilities_router(populated_store))
    client = TestClient(app)

    # 1. Causal Blast Radius
    r_blast = client.post(
        "/api/v1/causal/live-blast-radius",
        json={"shock_entities": {"svc-api-gw": 1.0}, "max_depth": 2},
    )
    assert r_blast.status_code == 200
    assert "collapsed_nodes" in r_blast.json()

    # 2. Multi-Paradigm Query
    r_query = client.post(
        "/api/v1/query/multi-paradigm",
        json={"query": "Explain API gateway dependencies", "seed_canonical_ids": ["svc-api-gw"]},
    )
    assert r_query.status_code == 200
    assert "deterministic_subgraph" in r_query.json()
    assert "kernel_breakdown" in r_query.json()

    # 3. Domain Packs
    r_packs = client.get("/api/v1/domain-packs")
    assert r_packs.status_code == 200
    assert "packs" in r_packs.json()

    # 4. XAI Certify & Verify
    r_cert = client.post(
        "/api/v1/xai/certify-decision",
        json={
            "decision_id": "dec-api-test",
            "agent_id": "sentinel",
            "decision_summary": "Throttled high-risk connection",
            "evidence_entities": [{"canonical_id": "svc-api-gw", "properties": {"tier": "1"}}],
        },
    )
    assert r_cert.status_code == 200
    cert_data = r_cert.json()
    assert "merkle_root" in cert_data

    r_verify = client.post("/api/v1/xai/verify-certificate", json=cert_data)
    assert r_verify.status_code == 200
    assert r_verify.json()["valid"] is True
