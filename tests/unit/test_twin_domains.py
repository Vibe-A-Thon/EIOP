"""Tests for G2-P6 twin domain services: test intelligence, decisions, business intent, digital twin."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.test_intelligence import map_tests_to_code, map_test_runs_to_builds, select_tests_for_changes
from eoip.graph.decisions import ingest_decision, find_decisions_for_entity, extract_decisions_from_document
from eoip.graph.business_intent import ingest_objective, ingest_capability, link_to_capability, reverse_impact, intent_to_runtime_chain
from eoip.graph.twin import classify_facts, digital_thread_coverage, detect_missing_links
from fastapi.testclient import TestClient
from apps.api.app import create_app


def _test_intelligence_store():
    store = MemoryGraphStore()
    f1 = store.upsert_vertex("File", {"canonical_id": "urn:f1", "repo_id": "r1", "path": "src/main.py"})
    sym = store.upsert_vertex("CodeSymbol", {"canonical_id": "urn:sym1", "qualified_name": "main.handler", "symbol_kind": "function"})
    store.upsert_edge("DECLARES", f1["vid"], sym["vid"], {"fact_key": "decl:f1:sym1"})
    tc = store.upsert_vertex("TestCase", {"canonical_id": "urn:tc1", "name": "test_handler", "test_type": "unit"})
    store.upsert_edge("TESTS", tc["vid"], sym["vid"], {"fact_key": "tests:tc1:sym1"})
    tc2 = store.upsert_vertex("TestCase", {"canonical_id": "urn:tc2", "name": "test_file", "test_type": "integration"})
    store.upsert_edge("TESTS", tc2["vid"], f1["vid"], {"fact_key": "tests:tc2:f1"})
    suite = store.upsert_vertex("TestSuite", {"canonical_id": "urn:ts1", "name": "Unit Tests"})
    store.upsert_edge("PART_OF_SUITE", tc["vid"], suite["vid"], {"fact_key": "suite:tc1:ts1"})
    run = store.upsert_vertex("TestRun", {"canonical_id": "urn:tr1", "name": "Run 1", "execution_status": "passed", "passed_count": 5, "failed_count": 0})
    store.upsert_edge("EXECUTED_IN", tc["vid"], run["vid"], {"fact_key": "exec:tc1:tr1"})
    pipe = store.upsert_vertex("PipelineRun", {"canonical_id": "urn:pipe1", "name": "CI Build 42"})
    return store


# --- Test Intelligence ---

def test_map_tests_to_code():
    store = _test_intelligence_store()
    mappings = map_tests_to_code(store)
    assert len(mappings) >= 1
    handler_mapping = [m for m in mappings if m["test_id"] == "urn:tc1"]
    assert handler_mapping
    assert any(t["canonical_id"] == "urn:sym1" for t in handler_mapping[0]["code_targets"])


def test_map_tests_to_code_includes_file_tests():
    store = _test_intelligence_store()
    mappings = map_tests_to_code(store)
    file_mapping = [m for m in mappings if m["test_id"] == "urn:tc2"]
    assert file_mapping
    assert any(t["canonical_id"] == "urn:f1" for t in file_mapping[0]["code_targets"])


def test_map_test_runs_to_builds():
    store = _test_intelligence_store()
    mappings = map_test_runs_to_builds(store)
    assert len(mappings) >= 1
    run_mapping = [m for m in mappings if m["run_id"] == "urn:tr1"]
    assert run_mapping
    assert run_mapping[0]["execution_status"] == "passed"


def test_select_tests_for_changes():
    store = _test_intelligence_store()
    result = select_tests_for_changes(store, ["urn:f1"])
    assert result["total_tests"] >= 2
    test_ids = [t["test_id"] for t in result["selected_tests"]]
    assert "urn:tc1" in test_ids
    assert "urn:tc2" in test_ids


def test_select_tests_empty_changes():
    store = _test_intelligence_store()
    result = select_tests_for_changes(store, [])
    assert result["total_tests"] == 0


def test_select_tests_unknown_file():
    store = _test_intelligence_store()
    result = select_tests_for_changes(store, ["urn:nonexistent"])
    assert result["total_tests"] == 0


# --- Decision Graph ---

def test_ingest_decision():
    store = MemoryGraphStore()
    result = ingest_decision(store, "Use PostgreSQL", rationale="Better for OLTP", status="Accepted")
    assert result["decision"]["label"] == "Decision"
    assert result["decision"]["properties"]["decision_status"] == "Accepted"


def test_ingest_decision_with_alternatives():
    store = MemoryGraphStore()
    result = ingest_decision(store, "Choose DB", alternatives=[
        {"name": "PostgreSQL", "description": "Relational", "rationale": "ACID"},
        {"name": "MongoDB", "description": "Document", "rationale": "Flexible schema"},
    ])
    assert len(result["alternatives"]) == 2
    edges = store.find_edges(limit=100)
    alt_edges = [e for e in edges if e["label"] == "HAS_ALTERNATIVE"]
    assert len(alt_edges) == 2


def test_ingest_decision_with_linked_entities():
    store = MemoryGraphStore()
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:auth", "service_id": "auth", "name": "Auth Service"})
    result = ingest_decision(store, "Auth Design", linked_entities=["urn:svc:auth"])
    assert len(result["linked_entities"]) == 1
    assert result["linked_entities"][0]["edge"] == "DECIDES"


def test_find_decisions_for_entity():
    store = MemoryGraphStore()
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:api", "service_id": "api", "name": "API Service"})
    ingest_decision(store, "API Architecture", linked_entities=["urn:svc:api"])
    decisions = find_decisions_for_entity(store, "urn:svc:api")
    assert len(decisions) == 1
    assert decisions[0]["name"] == "API Architecture"


def test_find_decisions_for_unknown_entity():
    store = MemoryGraphStore()
    decisions = find_decisions_for_entity(store, "urn:nonexistent")
    assert decisions == []


def test_extract_decisions_from_document():
    store = MemoryGraphStore()
    store.upsert_vertex("Document", {
        "canonical_id": "urn:doc:adr1",
        "name": "ADR-001",
        "path": "/docs/adr-001.md",
        "description": "# ADR 1: Use HugeGraph\n\n**Status:** Accepted\n\n**Context:** We need a graph database.\n\n## Other stuff",
    })
    decisions = extract_decisions_from_document(store, "urn:doc:adr1")
    assert len(decisions) >= 1
    assert "HugeGraph" in decisions[0]["title"]


def test_extract_decisions_empty_document():
    store = MemoryGraphStore()
    store.upsert_vertex("Document", {"canonical_id": "urn:doc:empty", "name": "Empty", "path": "/docs/empty.md"})
    decisions = extract_decisions_from_document(store, "urn:doc:empty")
    assert decisions == []


# --- Business Intent ---

def test_ingest_objective():
    store = MemoryGraphStore()
    obj = ingest_objective(store, "Reduce TTM", objective_type="strategic", priority="high")
    assert obj["label"] == "BusinessObjective"
    assert obj["properties"]["strategic_priority"] == "high"


def test_ingest_capability():
    store = MemoryGraphStore()
    cap = ingest_capability(store, "Order Processing", level=2, business_domain="Commerce")
    assert cap["label"] == "BusinessCapability"
    assert cap["properties"]["capability_level"] == 2


def test_capability_with_parent():
    store = MemoryGraphStore()
    parent = ingest_capability(store, "Commerce Platform")
    child = ingest_capability(store, "Order Processing", parent_cid=parent["canonical_id"])
    edges = store.find_edges(limit=100)
    decompose = [e for e in edges if e["label"] == "DECOMPOSES_INTO"]
    assert len(decompose) == 1


def test_capability_with_objective():
    store = MemoryGraphStore()
    obj = ingest_objective(store, "Revenue Growth")
    cap = ingest_capability(store, "Payment Processing", objective_cid=obj["canonical_id"])
    edges = store.find_edges(limit=100)
    fulfills = [e for e in edges if e["label"] == "FULFILLS"]
    assert len(fulfills) == 1


def test_link_to_capability():
    store = MemoryGraphStore()
    cap = ingest_capability(store, "Authentication")
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:auth", "service_id": "auth", "name": "Auth Service"})
    result = link_to_capability(store, "urn:svc:auth", cap["canonical_id"])
    assert result is not None
    assert result["edge"] == "REALIZES"


def test_reverse_impact():
    store = MemoryGraphStore()
    obj = ingest_objective(store, "Customer Satisfaction")
    cap = ingest_capability(store, "User Management", objective_cid=obj["canonical_id"])
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:users", "service_id": "users", "name": "User Service"})
    link_to_capability(store, "urn:svc:users", cap["canonical_id"])
    result = reverse_impact(store, "urn:svc:users")
    assert len(result["capabilities"]) == 1
    assert result["capabilities"][0]["name"] == "User Management"
    assert len(result["objectives"]) == 1
    assert result["objectives"][0]["name"] == "Customer Satisfaction"


def test_reverse_impact_unknown_service():
    store = MemoryGraphStore()
    result = reverse_impact(store, "urn:nonexistent")
    assert result["capabilities"] == []
    assert result["objectives"] == []


def test_intent_to_runtime_chain():
    store = MemoryGraphStore()
    obj = ingest_objective(store, "Automate Billing")
    cap = ingest_capability(store, "Invoice Generation", objective_cid=obj["canonical_id"])
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:billing", "service_id": "billing", "name": "Billing Service"})
    link_to_capability(store, "urn:svc:billing", cap["canonical_id"])
    result = intent_to_runtime_chain(store, obj["canonical_id"])
    assert len(result["chain"]) >= 1
    labels = result["labels_present"]
    assert "BusinessObjective" in labels


# --- Digital Twin View ---

def test_classify_facts():
    store = MemoryGraphStore()
    store.upsert_vertex("BusinessObjective", {"canonical_id": "urn:obj:1", "name": "Obj1"})
    store.upsert_vertex("File", {"canonical_id": "urn:f:1", "repo_id": "r1", "path": "a.py"})
    store.upsert_vertex("Deployment", {"canonical_id": "urn:dep:1", "name": "Deploy1"})
    result = classify_facts(store)
    assert result["summary"]["intended"] >= 1
    assert result["summary"]["implemented"] >= 1
    assert result["summary"]["observed"] >= 1


def test_classify_inferred_facts():
    store = MemoryGraphStore()
    store.upsert_vertex("File", {"canonical_id": "urn:f:inf", "repo_id": "r1", "path": "b.py", "creation_status": "INFERRED"})
    result = classify_facts(store)
    assert result["summary"]["inferred"] >= 1


def test_digital_thread_coverage():
    store = MemoryGraphStore()
    f = store.upsert_vertex("File", {"canonical_id": "urn:f:1", "repo_id": "r1", "path": "a.py"})
    sym = store.upsert_vertex("CodeSymbol", {"canonical_id": "urn:sym:1", "qualified_name": "foo", "symbol_kind": "function"})
    store.upsert_edge("DECLARES", f["vid"], sym["vid"], {"fact_key": "decl:f1:sym1"})
    result = digital_thread_coverage(store)
    assert "File" in result["stages_present"]
    assert "CodeSymbol" in result["stages_present"]
    assert result["per_stage"]["File"]["connected"] >= 1


def test_digital_thread_coverage_empty():
    store = MemoryGraphStore()
    result = digital_thread_coverage(store)
    assert result["thread_completeness"] == 0
    assert result["stages_present"] == []


def test_detect_missing_links():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:lonely", "service_id": "lonely", "name": "Lonely Service"})
    result = detect_missing_links(store)
    assert result["total_gaps"] >= 1
    svc_gaps = [f for f in result["findings"] if f["canonical_id"] == "urn:svc:lonely"]
    assert svc_gaps
    assert "Deployment" in svc_gaps[0]["missing_connections"]


def test_detect_missing_links_connected():
    store = MemoryGraphStore()
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:connected", "service_id": "conn", "name": "Connected"})
    dep = store.upsert_vertex("Deployment", {"canonical_id": "urn:dep:1", "name": "Deploy"})
    pipe = store.upsert_vertex("PipelineRun", {"canonical_id": "urn:pipe:1", "name": "CI Build"})
    store.upsert_edge("DEPLOYS", pipe["vid"], dep["vid"], {"fact_key": "deploys:1"})
    result = detect_missing_links(store)
    dep_gaps = [f for f in result["findings"] if f["canonical_id"] == "urn:dep:1"]
    if dep_gaps:
        assert "PipelineRun" not in dep_gaps[0]["missing_connections"]


# --- API Endpoint Tests ---

def _twin_client():
    store = MemoryGraphStore()
    f1 = store.upsert_vertex("File", {"canonical_id": "urn:f1", "repo_id": "r1", "path": "src/main.py"})
    sym = store.upsert_vertex("CodeSymbol", {"canonical_id": "urn:sym1", "qualified_name": "main.handler", "symbol_kind": "function"})
    store.upsert_edge("DECLARES", f1["vid"], sym["vid"], {"fact_key": "decl:f1:sym1"})
    tc = store.upsert_vertex("TestCase", {"canonical_id": "urn:tc1", "name": "test_handler", "test_type": "unit"})
    store.upsert_edge("TESTS", tc["vid"], sym["vid"], {"fact_key": "tests:tc1:sym1"})
    return TestClient(create_app(store)), store


def test_api_test_mappings():
    client, _ = _twin_client()
    resp = client.get("/api/v1/twin/test-intelligence/mappings")
    assert resp.status_code == 200
    assert "mappings" in resp.json()


def test_api_test_runs():
    client, _ = _twin_client()
    resp = client.get("/api/v1/twin/test-intelligence/runs")
    assert resp.status_code == 200


def test_api_test_select():
    client, _ = _twin_client()
    resp = client.post("/api/v1/twin/test-intelligence/select", json={"changed_files": ["urn:f1"]})
    assert resp.status_code == 200
    assert resp.json()["total_tests"] >= 1


def test_api_test_select_missing_files():
    client, _ = _twin_client()
    resp = client.post("/api/v1/twin/test-intelligence/select", json={})
    assert resp.status_code == 400


def test_api_ingest_decision():
    client, _ = _twin_client()
    resp = client.post("/api/v1/twin/decisions/ingest", json={"name": "Use Graph DB", "status": "Accepted"})
    assert resp.status_code == 200
    assert resp.json()["decision"]["label"] == "Decision"


def test_api_decisions_for_entity():
    client, store = _twin_client()
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:test", "service_id": "test", "name": "Test"})
    ingest_decision(store, "Test Decision", linked_entities=["urn:svc:test"])
    resp = client.get("/api/v1/twin/decisions/urn:svc:test")
    assert resp.status_code == 200
    assert len(resp.json()["decisions"]) >= 1


def test_api_create_objective():
    client, _ = _twin_client()
    resp = client.post("/api/v1/twin/business/objectives", json={"name": "Revenue Growth"})
    assert resp.status_code == 200
    assert resp.json()["objective"]["label"] == "BusinessObjective"


def test_api_create_capability():
    client, _ = _twin_client()
    resp = client.post("/api/v1/twin/business/capabilities", json={"name": "Payment", "level": 2})
    assert resp.status_code == 200
    assert resp.json()["capability"]["label"] == "BusinessCapability"


def test_api_link_entity():
    client, store = _twin_client()
    from eoip.graph.business_intent import ingest_capability
    cap = ingest_capability(store, "Auth Capability")
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:auth2", "service_id": "auth2", "name": "Auth"})
    resp = client.post("/api/v1/twin/business/link", json={"entity_cid": "urn:svc:auth2", "capability_cid": cap["canonical_id"]})
    assert resp.status_code == 200


def test_api_reverse_impact():
    client, store = _twin_client()
    from eoip.graph.business_intent import ingest_objective, ingest_capability, link_to_capability
    obj = ingest_objective(store, "Uptime")
    cap = ingest_capability(store, "Monitoring", objective_cid=obj["canonical_id"])
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:mon", "service_id": "mon", "name": "Monitor"})
    link_to_capability(store, "urn:svc:mon", cap["canonical_id"])
    resp = client.get("/api/v1/twin/business/reverse-impact/urn:svc:mon")
    assert resp.status_code == 200
    assert resp.json()["total_affected"] >= 2


def test_api_twin_classify():
    client, _ = _twin_client()
    resp = client.get("/api/v1/twin/classify")
    assert resp.status_code == 200
    assert "summary" in resp.json()


def test_api_twin_coverage():
    client, _ = _twin_client()
    resp = client.get("/api/v1/twin/coverage")
    assert resp.status_code == 200
    assert "per_stage" in resp.json()


def test_api_twin_missing_links():
    client, _ = _twin_client()
    resp = client.get("/api/v1/twin/missing-links")
    assert resp.status_code == 200
    assert "total_gaps" in resp.json()
