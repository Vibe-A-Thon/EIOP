"""Tests for knowledge debt catalog and SLO evaluator (G2-P7/P8)."""

from eoip.graph.knowledge_debt import (
    SLORule,
    detect_knowledge_debt,
    evaluate_slos,
    parse_slo_rules,
)
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app


def test_detect_unowned_service():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:lonely", "service_id": "s1", "name": "Lonely"})
    result = detect_knowledge_debt(store)
    unowned = [f for f in result["findings"] if f["category"] == "unowned_component"]
    assert unowned
    assert unowned[0]["canonical_id"] == "urn:svc:lonely"


def test_detect_undocumented_api():
    store = MemoryGraphStore()
    store.upsert_vertex("APIEndpoint", {
        "canonical_id": "urn:api:ep1", "api_name": "users", "api_method": "GET", "api_path": "/users",
    })
    result = detect_knowledge_debt(store)
    undoc = [f for f in result["findings"] if f["category"] == "undocumented_api"]
    assert undoc


def test_detect_unlinked_requirement():
    store = MemoryGraphStore()
    store.upsert_vertex("Requirement", {"canonical_id": "urn:req:1", "name": "Auth feature"})
    result = detect_knowledge_debt(store)
    unlinked = [f for f in result["findings"] if f["category"] == "unlinked_requirement"]
    assert unlinked


def test_detect_missing_test():
    store = MemoryGraphStore()
    store.upsert_vertex("APIEndpoint", {
        "canonical_id": "urn:api:ep2", "api_name": "orders", "api_method": "POST", "api_path": "/orders",
    })
    result = detect_knowledge_debt(store)
    missing = [f for f in result["findings"] if f["category"] == "missing_test"]
    assert missing


def test_detect_low_confidence():
    store = MemoryGraphStore()
    store.upsert_vertex("File", {
        "canonical_id": "urn:f:low", "repo_id": "r1", "path": "x.py",
        "creation_status": "INFERRED", "confidence": 0.3,
    })
    result = detect_knowledge_debt(store)
    low = [f for f in result["findings"] if f["category"] == "low_confidence_inference"]
    assert low
    assert low[0]["severity"] == "ERROR"


def test_no_debt_in_clean_graph():
    store = MemoryGraphStore()
    result = detect_knowledge_debt(store)
    assert result["total_debt"] == 0


def test_debt_by_category():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:1", "service_id": "s1", "name": "Svc1"})
    store.upsert_vertex("Requirement", {"canonical_id": "urn:req:1", "name": "Req1"})
    result = detect_knowledge_debt(store)
    assert "unowned_component" in result["by_category"]
    assert "unlinked_requirement" in result["by_category"]


import pytest
from eoip.graph.knowledge_debt import (
    DEBT_CATEGORIES,
    DebtFinding,
    DebtTrendTracker,
    compute_debt_by_dimensions,
    compute_multidimensional_debt,
)


@pytest.mark.req("G2-KD-002")
def test_all_twelve_debt_categories_detected_g2_kd_002():
    store = MemoryGraphStore()
    # 1. unowned component
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:unowned", "name": "SvcA"})
    # 2. undocumented api
    store.upsert_vertex("APIEndpoint", {"canonical_id": "urn:api:undoc", "api_name": "listItems"})
    # 3. unlinked requirement
    store.upsert_vertex("Requirement", {"canonical_id": "urn:req:unlinked", "name": "ReqA"})
    # 4. unlinked implementation
    store.upsert_vertex("CodeSymbol", {"canonical_id": "urn:sym:orphan", "qualified_name": "orphan_func"})
    # 5. stale document
    store.upsert_vertex("Document", {"canonical_id": "urn:doc:stale", "name": "Old Arch", "status": "stale"})
    # 6. unresolved identity
    store.upsert_vertex("Person", {"canonical_id": "urn:unresolved:bob", "name": "Bob"})
    # 7. broken provenance
    store.upsert_vertex("Project", {"canonical_id": "urn:p:noprov", "name": "Proj", "ingestion_run_id": "run-99"})
    # 8. low confidence
    store.upsert_vertex("File", {"canonical_id": "urn:f:lowconf", "repo_id": "r1", "path": "f.py", "creation_status": "INFERRED", "confidence": 0.2})
    # 9. missing test
    store.upsert_vertex("APIEndpoint", {"canonical_id": "urn:api:notest", "api_name": "deleteAccount"})
    # 10. missing architecture mapping
    store.upsert_vertex("DesignComponent", {"canonical_id": "urn:comp:noarch", "name": "BillingComponent"})
    # 11. unknown production owner
    store.upsert_vertex("Deployment", {"canonical_id": "urn:dep:prod", "name": "ProdDep", "environment": "production"})
    # 12. stale runbook
    store.upsert_vertex("Document", {"canonical_id": "urn:doc:rb", "name": "Failover Runbook", "status": "stale"})

    result = detect_knowledge_debt(store)
    detected_categories = set(result["by_category"].keys())
    assert len(detected_categories) == 12
    for cat in DEBT_CATEGORIES:
        assert cat in detected_categories


@pytest.mark.req("G2-KD-003")
def test_debt_computed_by_dimensions_g2_kd_003():
    findings = [
        DebtFinding(
            category="unowned_component",
            canonical_id="urn:svc:1",
            label="Service",
            name="S1",
            description="No owner",
            dimension={"project": "proj-alpha", "team": "platform", "service": "s1", "application": "app1", "domain": "core", "release": "v1.0"},
        ),
        DebtFinding(
            category="missing_test",
            canonical_id="urn:svc:2",
            label="Service",
            name="S2",
            description="No test",
            dimension={"project": "proj-alpha", "team": "sec", "service": "s2", "application": "app1", "domain": "core", "release": "v1.1"},
        ),
    ]
    dims = compute_debt_by_dimensions(findings)
    assert dims["project"]["proj-alpha"] == 2
    assert dims["team"]["platform"] == 1
    assert dims["team"]["sec"] == 1
    assert dims["application"]["app1"] == 2
    assert dims["domain"]["core"] == 2
    assert dims["release"]["v1.0"] == 1
    assert dims["release"]["v1.1"] == 1


@pytest.mark.req("G2-KD-004")
def test_multidimensional_debt_facets_g2_kd_004():
    findings = [
        DebtFinding(category="unowned_component", canonical_id="1", label="Service", name="S1", description="desc"),
        DebtFinding(category="undocumented_api", canonical_id="2", label="APIEndpoint", name="A1", description="desc"),
        DebtFinding(category="missing_test", canonical_id="3", label="Service", name="S2", description="desc"),
    ]
    multi = compute_multidimensional_debt(findings)
    assert multi["total_findings"] == 3
    assert "ownership" in multi["dimensional_facets"]
    assert "documentation" in multi["dimensional_facets"]
    assert "testing" in multi["dimensional_facets"]
    assert multi["dimensional_facets"]["ownership"] >= 1
    assert multi["dimensional_facets"]["documentation"] >= 1
    assert multi["dimensional_facets"]["testing"] >= 1


@pytest.mark.req("G2-KD-005")
def test_debt_trend_tracking_g2_kd_005():
    tracker = DebtTrendTracker()
    f1 = [DebtFinding(category="unowned_component", canonical_id="1", label="Service", name="S1", description="desc")]
    f2 = [
        DebtFinding(category="unowned_component", canonical_id="1", label="Service", name="S1", description="desc"),
        DebtFinding(category="missing_test", canonical_id="2", label="Service", name="S2", description="desc"),
    ]
    tracker.record_snapshot(f1, timestamp="2026-10-01T00:00:00Z", label="T1")
    tracker.record_snapshot(f2, timestamp="2026-10-02T00:00:00Z", label="T2")

    trends = tracker.get_trends()
    assert trends["direction"] == "degrading"
    assert trends["delta_total"] == 1
    assert trends["category_deltas"]["missing_test"] == 1


@pytest.mark.req("G2-KD-006")
def test_findings_link_remediation_and_evidence_g2_kd_006():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:target", "name": "TargetSvc"})
    result = detect_knowledge_debt(store)
    findings = result["findings"]
    assert len(findings) > 0
    for finding in findings:
        assert finding["remediation_action"] != ""
        assert "evidence_ref" in finding
        assert finding["evidence_ref"].startswith("vertex:")


# --- SLO Evaluator ---

def test_parse_slo_rules():
    config = [{"id": "SLO-1", "metric": "evidence_coverage", "threshold": 0.8}]
    rules = parse_slo_rules(config)
    assert len(rules) == 1
    assert rules[0].metric == "evidence_coverage"


def test_evaluate_slo_met():
    store = MemoryGraphStore()
    proj = store.upsert_vertex("Project", {"canonical_id": "urn:p:1", "name": "P1"})
    ev = store.upsert_vertex("Evidence", {
        "canonical_id": "urn:ev:1", "source_system": "jira", "source_ref": "r1", "method": "api",
    })
    store.upsert_edge("EVIDENCED_BY", proj["vid"], ev["vid"], {"fact_key": "ev:1"})
    rules = [SLORule(id="SLO-1", metric="evidence_coverage", threshold=0.5)]
    result = evaluate_slos(store, rules)
    assert result["met"] >= 1


def test_evaluate_slo_breached():
    store = MemoryGraphStore()
    store.upsert_vertex("Project", {"canonical_id": "urn:p:1", "name": "P1"})
    rules = [SLORule(id="SLO-1", metric="evidence_coverage", threshold=0.99)]
    result = evaluate_slos(store, rules)
    breaches = [r for r in result["results"] if r["status"] == "BREACHED"]
    assert breaches


def test_evaluate_slo_unknown_metric():
    store = MemoryGraphStore()
    rules = [SLORule(id="SLO-1", metric="nonexistent_metric", threshold=0.5)]
    result = evaluate_slos(store, rules)
    assert result["unknown"] >= 1


def test_evaluate_slo_empty_graph():
    store = MemoryGraphStore()
    rules = [SLORule(id="SLO-1", metric="evidence_coverage", threshold=0.5)]
    result = evaluate_slos(store, rules)
    assert result["unknown"] >= 1


def test_evaluate_slo_health_score():
    store = MemoryGraphStore()
    proj = store.upsert_vertex("Project", {"canonical_id": "urn:p:1", "name": "P1"})
    ev = store.upsert_vertex("Evidence", {
        "canonical_id": "urn:ev:1", "source_system": "jira", "source_ref": "r1", "method": "api",
    })
    store.upsert_edge("EVIDENCED_BY", proj["vid"], ev["vid"], {"fact_key": "ev:1"})
    rules = [
        SLORule(id="SLO-1", metric="evidence_coverage", threshold=0.5),
        SLORule(id="SLO-2", metric="orphan_rate", threshold=0.5, operator="lte"),
    ]
    result = evaluate_slos(store, rules)
    assert 0 <= result["health_score"] <= 1


# --- API Tests ---

def test_api_knowledge_debt():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:1", "service_id": "s1", "name": "S1"})
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/knowledge/debt")
    assert resp.status_code == 200
    assert "total_debt" in resp.json()


def test_api_knowledge_slo():
    store = MemoryGraphStore()
    store.upsert_vertex("Project", {"canonical_id": "urn:p:1", "name": "P1"})
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/knowledge/slo", json={
        "rules": [{"id": "SLO-1", "metric": "evidence_coverage", "threshold": 0.5}]
    })
    assert resp.status_code == 200
    assert "results" in resp.json()


def test_api_knowledge_slo_no_rules():
    store = MemoryGraphStore()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/knowledge/slo", json={})
    assert resp.status_code == 400
