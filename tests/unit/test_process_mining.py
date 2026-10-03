"""Tests for process mining engine (G2-P7)."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.process_mining import (
    extract_cases_from_graph, discover_process_paths,
    compare_to_designed_flow, deviation_report, ProcessCase,
)
from fastapi.testclient import TestClient
from apps.api.app import create_app


def _process_store():
    store = MemoryGraphStore()
    wi = store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:wi:1", "issue_key": "PROJ-1", "summary": "Feature A",
        "ingestion_run_id": "run-1",
    })
    c1 = store.upsert_vertex("WorkItemChange", {
        "canonical_id": "urn:change:1", "change_id": "c1",
        "field_name": "status", "from_value": "Open", "to_value": "In Progress",
        "created_at": "2026-01-01T10:00:00Z",
    })
    c2 = store.upsert_vertex("WorkItemChange", {
        "canonical_id": "urn:change:2", "change_id": "c2",
        "field_name": "status", "from_value": "In Progress", "to_value": "Review",
        "created_at": "2026-01-02T10:00:00Z",
    })
    c3 = store.upsert_vertex("WorkItemChange", {
        "canonical_id": "urn:change:3", "change_id": "c3",
        "field_name": "status", "from_value": "Review", "to_value": "Done",
        "created_at": "2026-01-03T10:00:00Z",
    })
    store.upsert_edge("HAS_CHANGE", wi["vid"], c1["vid"], {"fact_key": "hc:1"})
    store.upsert_edge("HAS_CHANGE", wi["vid"], c2["vid"], {"fact_key": "hc:2"})
    store.upsert_edge("HAS_CHANGE", wi["vid"], c3["vid"], {"fact_key": "hc:3"})
    return store


def test_extract_cases():
    store = _process_store()
    cases = extract_cases_from_graph(store)
    assert len(cases) == 1
    assert cases[0].case_id == "urn:wi:1"
    assert len(cases[0].events) == 3


def test_extract_cases_sorted_by_timestamp():
    store = _process_store()
    cases = extract_cases_from_graph(store)
    timestamps = [e["timestamp"] for e in cases[0].events]
    assert timestamps == sorted(timestamps)


def test_discover_paths():
    store = _process_store()
    cases = extract_cases_from_graph(store)
    result = discover_process_paths(cases)
    assert result["total_cases"] == 1
    assert result["unique_paths"] >= 1
    assert len(result["paths"]) >= 1


def test_discover_paths_transitions():
    store = _process_store()
    cases = extract_cases_from_graph(store)
    result = discover_process_paths(cases)
    transitions = result["transitions"]
    assert any(t["from"] == "In Progress" and t["to"] == "Review" for t in transitions)


def test_compare_to_designed_no_deviation():
    cases = [ProcessCase("c1", [
        {"field": "status", "to_value": "Open"},
        {"field": "status", "to_value": "In Progress"},
        {"field": "status", "to_value": "Done"},
    ])]
    observed = discover_process_paths(cases)
    result = compare_to_designed_flow(observed, ["Open", "In Progress", "Done"])
    skipped = [d for d in result["deviations"] if d["type"] == "skipped_steps"]
    assert not skipped


def test_compare_to_designed_with_skipped():
    cases = [ProcessCase("c1", [
        {"field": "status", "to_value": "Open"},
        {"field": "status", "to_value": "Done"},
    ])]
    observed = discover_process_paths(cases)
    result = compare_to_designed_flow(observed, ["Open", "In Progress", "Review", "Done"])
    skipped = [d for d in result["deviations"] if d["type"] == "skipped_steps"]
    assert skipped
    assert "In Progress" in skipped[0]["skipped"]


def test_compare_to_designed_with_rework():
    cases = [ProcessCase("c1", [
        {"field": "status", "to_value": "Open"},
        {"field": "status", "to_value": "In Progress"},
        {"field": "status", "to_value": "Open"},
        {"field": "status", "to_value": "In Progress"},
        {"field": "status", "to_value": "Done"},
    ])]
    observed = discover_process_paths(cases)
    result = compare_to_designed_flow(observed, ["Open", "In Progress", "Done"])
    rework = [d for d in result["deviations"] if d["type"] == "rework_loop"]
    assert rework


def test_deviation_report():
    store = _process_store()
    result = deviation_report(store, designed_steps=["In Progress", "Review", "Done"])
    assert "cases" in result
    assert "observed_paths" in result
    assert "comparison" in result


def test_deviation_report_no_designed_steps():
    store = _process_store()
    result = deviation_report(store)
    assert result["comparison"]["conformance_rate"] == 1.0


def test_empty_store():
    store = MemoryGraphStore()
    cases = extract_cases_from_graph(store)
    assert cases == []


def test_api_process_cases():
    store = _process_store()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/process/cases")
    assert resp.status_code == 200
    assert "cases" in resp.json()


def test_api_process_paths():
    store = _process_store()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/process/paths")
    assert resp.status_code == 200
    assert "total_cases" in resp.json()


def test_api_process_deviations():
    store = _process_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/process/deviations", json={
        "designed_steps": ["In Progress", "Review", "Done"]
    })
    assert resp.status_code == 200
    assert "comparison" in resp.json()
