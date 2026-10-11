"""Tests for product-grade capability scanning without demo data."""

from __future__ import annotations

from pathlib import Path

from eoip.graph.memory import MemoryGraphStore
from eoip.product.intelligence import (
    PRODUCT_CAPABILITY_CATALOG,
    build_product_capability_report,
)
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _seed_runtime_facts(store: MemoryGraphStore) -> None:
    store.upsert_vertex(
        "BusinessCapability",
        {
            "canonical_id": "urn:test:capability:checkout",
            "name": "Checkout Intelligence",
            "source_system": "unit-test",
        },
    )
    store.upsert_vertex(
        "KnowledgeProduct",
        {
            "canonical_id": "urn:test:knowledge-product:risk",
            "name": "Risk Product",
            "owner": "platform",
        },
    )
    store.upsert_vertex(
        "DataSource",
        {
            "canonical_id": "urn:test:source:jira",
            "name": "Jira",
            "source_system": "jira",
        },
    )
    store.upsert_vertex(
        "IngestionRun",
        {
            "canonical_id": "urn:test:ingestion:1",
            "run_status": "SUCCEEDED",
            "run_kind": "BASELINE",
        },
    )
    store.upsert_vertex(
        "AgentRun",
        {
            "canonical_id": "urn:test:agent-run:1",
            "agent_id": "TraceImpact",
            "goal": "Explain impact",
        },
    )
    store.upsert_vertex(
        "EntityRevision",
        {
            "canonical_id": "urn:test:revision:entity:1",
            "revision_id": "r1",
            "subject_id": "urn:test:capability:checkout",
            "observed_at": "2026-10-10T00:00:00Z",
            "is_current": True,
            "payload_json": "{}",
            "source_event_id": "event-1",
        },
    )
    store.upsert_vertex(
        "GraphVersion",
        {
            "canonical_id": "urn:test:graph-version:1",
            "graph_version": "1",
            "created_at": "2026-10-10T00:00:00Z",
        },
    )


def test_product_capability_report_uses_real_repo_and_graph_evidence() -> None:
    store = MemoryGraphStore()
    _seed_runtime_facts(store)
    routes = {
        "/api/v1/rag/query",
        "/api/v1/retrieval/search",
        "/api/v1/evidence/manifest",
        "/api/v1/query/nl",
    }

    report = build_product_capability_report(
        repo_root=Path.cwd(),
        store=store,
        available_routes=routes,
    )

    assert report["source"] == "live-repository-and-runtime-scan"
    assert report["capability_count"] == len(PRODUCT_CAPABILITY_CATALOG)
    assert report["runtime_graph"]["vertices"] >= 7
    evidence = next(c for c in report["capabilities"] if c["capability_id"] == "PIC-001")
    assert evidence["checks_passed"] >= 1
    assert any(check["kind"] == "module" and check["present"] for check in evidence["checks"])
    assert report["next_requirements"]


def test_product_capability_api_and_materialization() -> None:
    store = MemoryGraphStore()
    _seed_runtime_facts(store)
    client = TestClient(create_app(store))

    report = client.get("/api/v1/product/capabilities")
    assert report.status_code == 200
    body = report.json()
    assert body["capability_count"] == len(PRODUCT_CAPABILITY_CATALOG)
    assert "first_choice_gate" in body

    gate = client.get("/api/v1/product/first-choice-gate")
    assert gate.status_code == 200
    assert "next_requirements" in gate.json()

    materialized = client.post("/api/v1/product/capabilities/materialize")
    assert materialized.status_code == 200
    assert materialized.json()["upserted_capabilities"] == len(PRODUCT_CAPABILITY_CATALOG)
    assert materialized.json()["upserted_requirements"] >= 1
    assert store.get_vertex_by_canonical_id("urn:eoip:product-capability:pic-001") is not None
    assert store.count_vertices(label="Requirement") >= 1


def test_deployed_route_surface_contains_product_gate_routes() -> None:
    store = MemoryGraphStore()
    client = TestClient(create_app(store))
    routes = {str(getattr(route, "path", "")) for route in client.app.routes}

    assert "/api/v1/loops/catalog" in routes
    assert "/api/v1/reports" in routes
