"""Tests for simulation workspace, extended what-if, and causal hypothesis engine (G2-P9)."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.simulation import Mutation, SimulationOverlay, SimulationWorkspace
from eoip.graph.whatif import (
    WhatIfEngine, parse_whatif_intent, confirm_scenario, execute_scenario, MutationPlan,
)
from eoip.graph.causal import (
    find_temporal_correlations, check_causal_prerequisites,
    generate_hypotheses, review_hypothesis, CausalHypothesis,
)
from fastapi.testclient import TestClient
from apps.api.app import create_app


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _base_store():
    store = MemoryGraphStore()
    svc = store.upsert_vertex("Service", {
        "canonical_id": "urn:svc:auth", "service_id": "auth", "name": "Auth Service",
        "created_at": "2026-01-01T00:00:00Z",
    })
    f1 = store.upsert_vertex("File", {
        "canonical_id": "urn:f:auth", "repo_id": "r1", "path": "src/auth.py",
        "created_at": "2026-01-02T00:00:00Z",
    })
    store.upsert_edge("DEPENDS_ON", f1["vid"], svc["vid"], {"fact_key": "dep:f:svc"})
    tc = store.upsert_vertex("TestCase", {
        "canonical_id": "urn:tc:1", "name": "test_auth",
        "created_at": "2026-01-03T00:00:00Z",
    })
    store.upsert_edge("TESTS", tc["vid"], f1["vid"], {"fact_key": "tests:tc:f"})
    return store


def _incident_store():
    store = MemoryGraphStore()
    deploy = store.upsert_vertex("Deployment", {
        "canonical_id": "urn:deploy:v1", "name": "v1.0",
        "created_at": "2026-01-10T08:00:00Z",
    })
    commit = store.upsert_vertex("Commit", {
        "canonical_id": "urn:commit:abc", "commit_sha": "abc123",
        "message": "Break auth", "created_at": "2026-01-10T07:00:00Z",
    })
    inc = store.upsert_vertex("Incident", {
        "canonical_id": "urn:inc:1", "incident_number": "INC-001",
        "summary": "Auth outage", "created_at": "2026-01-10T10:00:00Z",
    })
    store.upsert_edge("TRIGGERED_BY", inc["vid"], deploy["vid"], {"fact_key": "trig:inc:deploy"})
    store.upsert_edge("RESOLVES", commit["vid"], inc["vid"], {"fact_key": "res:commit:inc"})
    alert = store.upsert_vertex("AlertEvent", {
        "canonical_id": "urn:alert:1", "name": "Auth 500s",
        "created_at": "2026-01-10T09:30:00Z",
    })
    store.upsert_edge("CORRELATES_WITH", inc["vid"], alert["vid"], {"fact_key": "corr:inc:alert"})
    return store


# ---------------------------------------------------------------------------
# SimulationOverlay tests
# ---------------------------------------------------------------------------

def test_overlay_add_vertex():
    store = _base_store()
    overlay = SimulationOverlay(store)
    v = overlay.add_vertex("Service", {"canonical_id": "urn:svc:new", "service_id": "new", "name": "New"})
    assert v["canonical_id"] == "urn:svc:new"
    found = overlay.get_vertex_by_canonical_id("urn:svc:new")
    assert found is not None


def test_overlay_remove_vertex():
    store = _base_store()
    overlay = SimulationOverlay(store)
    assert overlay.remove_vertex("urn:svc:auth")
    assert overlay.get_vertex_by_canonical_id("urn:svc:auth") is None


def test_overlay_remove_hides_edges():
    store = _base_store()
    overlay = SimulationOverlay(store)
    overlay.remove_vertex("urn:svc:auth")
    svc = store.get_vertex_by_canonical_id("urn:svc:auth")
    edges = overlay.find_edges(in_v=svc["vid"])
    assert len(edges) == 0


def test_overlay_add_edge():
    store = _base_store()
    overlay = SimulationOverlay(store)
    e = overlay.add_edge("DEPENDS_ON", "urn:f:auth", "urn:tc:1")
    assert e is not None
    assert e["label"] == "DEPENDS_ON"


def test_overlay_modify_vertex():
    store = _base_store()
    overlay = SimulationOverlay(store)
    overlay.modify_vertex("urn:svc:auth", {"name": "Auth Service v2"})
    v = overlay.get_vertex_by_canonical_id("urn:svc:auth")
    assert v["properties"]["name"] == "Auth Service v2"


def test_overlay_find_vertices_combined():
    store = _base_store()
    overlay = SimulationOverlay(store)
    overlay.add_vertex("Service", {"canonical_id": "urn:svc:new", "service_id": "new2", "name": "New"})
    services = overlay.find_vertices(label="Service")
    cids = {v["canonical_id"] for v in services}
    assert "urn:svc:auth" in cids
    assert "urn:svc:new" in cids


def test_overlay_edges_from():
    store = _base_store()
    overlay = SimulationOverlay(store)
    f1 = store.get_vertex_by_canonical_id("urn:f:auth")
    edges = overlay.edges_from(f1["vid"])
    assert any(e["label"] == "DEPENDS_ON" for e in edges)


def test_overlay_edges_to():
    store = _base_store()
    overlay = SimulationOverlay(store)
    svc = store.get_vertex_by_canonical_id("urn:svc:auth")
    edges = overlay.edges_to(svc["vid"])
    assert any(e["label"] == "DEPENDS_ON" for e in edges)


def test_overlay_mutation_count():
    store = _base_store()
    overlay = SimulationOverlay(store)
    assert overlay.mutation_count == 0
    overlay.add_vertex("Service", {"canonical_id": "urn:x", "service_id": "x", "name": "X"})
    overlay.remove_vertex("urn:svc:auth")
    assert overlay.mutation_count == 2


# ---------------------------------------------------------------------------
# SimulationWorkspace tests
# ---------------------------------------------------------------------------

def test_workspace_create_and_list():
    store = _base_store()
    ws = SimulationWorkspace(store)
    sim_id = ws.create("test scenario")
    sims = ws.list_simulations()
    assert len(sims) == 1
    assert sims[0]["simulation_id"] == sim_id


def test_workspace_apply_mutation():
    store = _base_store()
    ws = SimulationWorkspace(store)
    sim_id = ws.create()
    result = ws.apply_mutation(sim_id, Mutation(
        kind="add_vertex", label="Service",
        properties={"canonical_id": "urn:svc:sim1", "service_id": "sim1", "name": "Sim Service"},
    ))
    assert result["success"]
    overlay = ws.get_overlay(sim_id)
    assert overlay.get_vertex_by_canonical_id("urn:svc:sim1") is not None


def test_workspace_apply_mutations_batch():
    store = _base_store()
    ws = SimulationWorkspace(store)
    sim_id = ws.create()
    results = ws.apply_mutations(sim_id, [
        Mutation(kind="remove_vertex", target_id="urn:svc:auth"),
        Mutation(kind="add_vertex", label="Service",
                 properties={"canonical_id": "urn:svc:new", "service_id": "n", "name": "N"}),
    ])
    assert len(results) == 2
    assert all(r["success"] for r in results)


def test_workspace_run_impact_analysis():
    store = _base_store()
    ws = SimulationWorkspace(store)
    sim_id = ws.create()
    ws.apply_mutation(sim_id, Mutation(kind="remove_vertex", target_id="urn:svc:auth"))
    analysis = ws.run_analysis(sim_id, "impact")
    assert analysis["delta"]["vertices"] == -1
    assert "urn:svc:auth" in analysis["removed_entities"]
    assert len(analysis["affected_entities"]) > 0


def test_workspace_compare():
    store = _base_store()
    ws = SimulationWorkspace(store)
    sim_id = ws.create()
    ws.apply_mutation(sim_id, Mutation(kind="remove_vertex", target_id="urn:svc:auth"))
    comp = ws.compare(sim_id)
    assert comp["removed_vertices"] == 1
    assert comp["total_mutations"] >= 1


def test_workspace_manifest():
    store = _base_store()
    ws = SimulationWorkspace(store)
    sim_id = ws.create("test manifest")
    ws.apply_mutation(sim_id, Mutation(kind="remove_vertex", target_id="urn:svc:auth"))
    manifest = ws.get_manifest(sim_id)
    assert manifest is not None
    assert manifest["simulation_id"] == sim_id
    assert len(manifest["mutations"]) == 1


def test_workspace_nonexistent_simulation():
    store = _base_store()
    ws = SimulationWorkspace(store)
    result = ws.apply_mutation("nonexistent", Mutation(kind="remove_vertex", target_id="x"))
    assert "error" in result


# ---------------------------------------------------------------------------
# What-If Mutation Plan tests
# ---------------------------------------------------------------------------

def test_parse_intent_remove():
    plan = parse_whatif_intent("remove Service urn:svc:auth")
    assert len(plan.mutations) == 1
    assert plan.mutations[0].kind == "remove_vertex"
    assert plan.mutations[0].target_id == "urn:svc:auth"


def test_parse_intent_add():
    plan = parse_whatif_intent("add Service named New Auth")
    assert len(plan.mutations) == 1
    assert plan.mutations[0].kind == "add_vertex"
    assert plan.mutations[0].label == "Service"


def test_parse_intent_connect():
    plan = parse_whatif_intent("connect urn:f:auth to urn:svc:auth via DEPENDS_ON")
    assert len(plan.mutations) == 1
    assert plan.mutations[0].kind == "add_edge"
    assert plan.mutations[0].label == "DEPENDS_ON"


def test_parse_intent_disconnect():
    plan = parse_whatif_intent("disconnect urn:f:auth from urn:svc:auth")
    assert len(plan.mutations) == 1
    assert plan.mutations[0].kind == "remove_edge_between"


def test_parse_intent_modify():
    plan = parse_whatif_intent("modify urn:svc:auth set name=AuthV2,status=active")
    assert len(plan.mutations) == 1
    assert plan.mutations[0].kind == "modify_vertex"
    assert plan.mutations[0].properties["name"] == "AuthV2"


def test_parse_intent_unrecognised():
    plan = parse_whatif_intent("something totally unknown")
    assert len(plan.mutations) == 0
    assert "Unrecognised" in plan.description


def test_confirm_scenario():
    plan = parse_whatif_intent("remove Service urn:svc:auth")
    confirmation = confirm_scenario(plan)
    assert confirmation["requires_confirmation"]
    assert confirmation["breakdown"]["removals"] == 1


def test_execute_scenario_remove():
    store = _base_store()
    plan = parse_whatif_intent("remove Service urn:svc:auth")
    plan.confirmed = True
    result = execute_scenario(store, plan)
    assert result["simulation_id"]
    assert result["manifest"] is not None
    affected = result["analysis"].get("affected_entities", [])
    assert "urn:f:auth" in affected


def test_execute_scenario_add():
    store = _base_store()
    plan = parse_whatif_intent("add Service named Cache Layer")
    plan.confirmed = True
    result = execute_scenario(store, plan)
    assert any(r.get("success") for r in result["mutation_results"])


# ---------------------------------------------------------------------------
# Causal Hypothesis Engine tests
# ---------------------------------------------------------------------------

def test_find_temporal_correlations():
    store = _incident_store()
    correlations = find_temporal_correlations(store, "urn:inc:1", time_window_hours=24)
    assert len(correlations) >= 1
    cids = [c["canonical_id"] for c in correlations]
    assert "urn:deploy:v1" in cids


def test_temporal_correlations_direction():
    store = _incident_store()
    correlations = find_temporal_correlations(store, "urn:inc:1", time_window_hours=24)
    deploy = next(c for c in correlations if c["canonical_id"] == "urn:deploy:v1")
    assert deploy["direction"] == "before"


def test_temporal_correlations_not_found():
    store = _incident_store()
    result = find_temporal_correlations(store, "urn:nonexistent")
    assert result == []


def test_temporal_correlations_narrow_window():
    store = _incident_store()
    correlations = find_temporal_correlations(store, "urn:inc:1", time_window_hours=0.001)
    assert len(correlations) == 0


def test_check_prerequisites_valid():
    store = _incident_store()
    result = check_causal_prerequisites(store, "urn:deploy:v1", "urn:inc:1")
    assert result["valid"]
    assert result["time_order_ok"]
    assert result["has_evidence"]
    assert result["confidence"] >= 0.5


def test_check_prerequisites_missing_entity():
    store = _incident_store()
    result = check_causal_prerequisites(store, "urn:nonexistent", "urn:inc:1")
    assert not result["valid"]
    assert "missing" in result


def test_check_prerequisites_reverse_time():
    store = _incident_store()
    result = check_causal_prerequisites(store, "urn:inc:1", "urn:deploy:v1")
    assert not result["time_order_ok"]


def test_generate_hypotheses_for_incident():
    store = _incident_store()
    result = generate_hypotheses(store, "urn:inc:1", time_window_hours=24)
    assert result["total_hypotheses"] >= 1
    assert result["status_note"]
    for h in result["hypotheses"]:
        assert h["status"] in ("CORRELATION", "HYPOTHESIS", "NEEDS_REVIEW")
        assert h["status"] != "HUMAN_CONFIRMED_CAUSE"


def test_generate_hypotheses_not_found():
    store = _incident_store()
    result = generate_hypotheses(store, "urn:nonexistent")
    assert "error" in result


def test_generate_hypotheses_with_alternatives():
    store = _incident_store()
    result = generate_hypotheses(store, "urn:inc:1", time_window_hours=24)
    if result["total_hypotheses"] > 1:
        assert result["hypotheses"][0]["alternatives"]


def test_review_hypothesis_confirm():
    h = CausalHypothesis(
        hypothesis_id="hyp-001", cause_cid="urn:deploy:v1", effect_cid="urn:inc:1",
        status="HYPOTHESIS", confidence=0.7,
    )
    reviewed = review_hypothesis(h, "HUMAN_CONFIRMED_CAUSE", notes="Confirmed by oncall")
    assert reviewed.status == "HUMAN_CONFIRMED_CAUSE"
    assert reviewed.reviewer_notes == "Confirmed by oncall"


def test_review_hypothesis_reject():
    h = CausalHypothesis(
        hypothesis_id="hyp-002", cause_cid="urn:x", effect_cid="urn:y",
        status="CORRELATION",
    )
    reviewed = review_hypothesis(h, "REJECTED", notes="Coincidence")
    assert reviewed.status == "REJECTED"


def test_review_hypothesis_invalid_decision():
    h = CausalHypothesis(
        hypothesis_id="hyp-003", cause_cid="urn:x", effect_cid="urn:y",
    )
    try:
        review_hypothesis(h, "BOGUS")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_never_auto_confirmed_cause():
    """Ensure generate_hypotheses never produces HUMAN_CONFIRMED_CAUSE."""
    store = _incident_store()
    result = generate_hypotheses(store, "urn:inc:1", time_window_hours=168)
    for h in result["hypotheses"]:
        assert h["status"] != "HUMAN_CONFIRMED_CAUSE"


# ---------------------------------------------------------------------------
# API Endpoint tests
# ---------------------------------------------------------------------------

def test_api_simulation_create_and_list():
    store = _base_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/simulation/create", json={"description": "test"})
    assert resp.status_code == 200
    sim_id = resp.json()["simulation_id"]
    resp2 = client.get("/api/v1/simulation/list")
    assert any(s["simulation_id"] == sim_id for s in resp2.json()["simulations"])


def test_api_simulation_mutate():
    store = _base_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/simulation/create", json={})
    sim_id = resp.json()["simulation_id"]
    resp2 = client.post(f"/api/v1/simulation/{sim_id}/mutate", json={
        "kind": "remove_vertex", "target_id": "urn:svc:auth",
    })
    assert resp2.status_code == 200
    assert resp2.json()["results"][0]["success"]


def test_api_simulation_analyze():
    store = _base_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/simulation/create", json={})
    sim_id = resp.json()["simulation_id"]
    client.post(f"/api/v1/simulation/{sim_id}/mutate", json={
        "kind": "remove_vertex", "target_id": "urn:svc:auth",
    })
    resp2 = client.get(f"/api/v1/simulation/{sim_id}/analyze")
    assert resp2.status_code == 200
    assert "delta" in resp2.json()


def test_api_simulation_compare():
    store = _base_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/simulation/create", json={})
    sim_id = resp.json()["simulation_id"]
    resp2 = client.get(f"/api/v1/simulation/{sim_id}/compare")
    assert resp2.status_code == 200
    assert "total_mutations" in resp2.json()


def test_api_simulation_manifest():
    store = _base_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/simulation/create", json={})
    sim_id = resp.json()["simulation_id"]
    resp2 = client.get(f"/api/v1/simulation/{sim_id}/manifest")
    assert resp2.status_code == 200
    assert resp2.json()["simulation_id"] == sim_id


def test_api_whatif_plan():
    store = _base_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/whatif/plan", json={"intent": "remove Service urn:svc:auth"})
    assert resp.status_code == 200
    assert resp.json()["requires_confirmation"]


def test_api_whatif_execute():
    store = _base_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/whatif/execute", json={"intent": "remove Service urn:svc:auth"})
    assert resp.status_code == 200
    assert "simulation_id" in resp.json()


def test_api_whatif_plan_no_intent():
    store = _base_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/whatif/plan", json={})
    assert resp.status_code == 400


def test_api_causal_correlations():
    store = _incident_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/causal/correlations/urn:inc:1", json={"time_window_hours": 24})
    assert resp.status_code == 200
    assert "correlations" in resp.json()


def test_api_causal_prerequisites():
    store = _incident_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/causal/prerequisites", json={
        "cause_cid": "urn:deploy:v1", "effect_cid": "urn:inc:1",
    })
    assert resp.status_code == 200
    assert resp.json()["valid"]


def test_api_causal_prerequisites_missing():
    store = _incident_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/causal/prerequisites", json={})
    assert resp.status_code == 400


def test_api_causal_hypotheses():
    store = _incident_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/causal/hypotheses/urn:inc:1", json={"time_window_hours": 24})
    assert resp.status_code == 200
    assert "hypotheses" in resp.json()
