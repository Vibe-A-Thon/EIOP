"""Tests for architecture conformance engine (G2-P7)."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.conformance import parse_rules, compile_rule, check_conformance, ArchRule, RuleKind
from fastapi.testclient import TestClient
from apps.api.app import create_app


def test_parse_rules_basic():
    dsl = "RULE R1: CodeSymbol MUST_NOT_DEPEND Service"
    rules = parse_rules(dsl)
    assert len(rules) == 1
    assert rules[0].id == "R1"
    assert rules[0].kind == RuleKind.MUST_NOT_DEPEND


def test_parse_rules_with_severity_and_depth():
    dsl = "RULE R2: File MUST_HAVE TestCase SEVERITY WARNING DEPTH 3"
    rules = parse_rules(dsl)
    assert len(rules) == 1
    assert rules[0].severity == "WARNING"
    assert rules[0].max_depth == 3


def test_parse_rules_multiple():
    dsl = """
    RULE R1: CodeSymbol MUST_NOT_DEPEND Service
    RULE R2: File MUST_HAVE TestCase
    RULE R3: CODE MUST_NOT_CROSS OPS
    """
    rules = parse_rules(dsl)
    assert len(rules) == 3


def test_must_not_depend_no_violation():
    store = MemoryGraphStore()
    store.upsert_vertex("File", {"canonical_id": "urn:f1", "repo_id": "r1", "path": "a.py"})
    store.upsert_vertex("File", {"canonical_id": "urn:f2", "repo_id": "r1", "path": "b.py"})
    rule = ArchRule(id="R1", kind=RuleKind.MUST_NOT_DEPEND, source="File", target="Service")
    findings = compile_rule(rule, store)
    assert len(findings) == 0


def test_must_not_depend_with_violation():
    store = MemoryGraphStore()
    f1 = store.upsert_vertex("File", {"canonical_id": "urn:f1", "repo_id": "r1", "path": "a.py"})
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:1", "service_id": "s1", "name": "DB"})
    store.upsert_edge("DEPENDS_ON", f1["vid"], svc["vid"], {"fact_key": "dep:f1:svc1"})
    rule = ArchRule(id="R1", kind=RuleKind.MUST_NOT_DEPEND, source="File", target="Service")
    findings = compile_rule(rule, store)
    assert len(findings) == 1
    assert findings[0].rule_id == "R1"
    assert findings[0].violating_path


def test_must_have_satisfied():
    store = MemoryGraphStore()
    f1 = store.upsert_vertex("File", {"canonical_id": "urn:f1", "repo_id": "r1", "path": "a.py"})
    tc = store.upsert_vertex("TestCase", {"canonical_id": "urn:tc1", "name": "test_a"})
    store.upsert_edge("TESTS", tc["vid"], f1["vid"], {"fact_key": "tests:tc1:f1"})
    rule = ArchRule(id="R2", kind=RuleKind.MUST_HAVE, source="File", target="TestCase")
    findings = compile_rule(rule, store)
    assert len(findings) == 0


def test_must_have_missing():
    store = MemoryGraphStore()
    store.upsert_vertex("File", {"canonical_id": "urn:f1", "repo_id": "r1", "path": "a.py"})
    rule = ArchRule(id="R2", kind=RuleKind.MUST_HAVE, source="File", target="TestCase")
    findings = compile_rule(rule, store)
    assert len(findings) == 1
    assert "missing" in findings[0].message.lower()


def test_must_not_cross_violation():
    store = MemoryGraphStore()
    commit = store.upsert_vertex("Commit", {"canonical_id": "urn:c:1", "commit_sha": "abc123"})
    inc = store.upsert_vertex("Incident", {"canonical_id": "urn:inc:1", "incident_number": "INC001", "summary": "Outage"})
    store.upsert_edge("RESOLVES", commit["vid"], inc["vid"], {"fact_key": "res:c1:inc1"})
    rule = ArchRule(id="R3", kind=RuleKind.MUST_NOT_CROSS, source="Commit", target="OPS")
    findings = compile_rule(rule, store)
    assert len(findings) >= 1


def test_check_conformance_all_pass():
    store = MemoryGraphStore()
    store.upsert_vertex("File", {"canonical_id": "urn:f1", "repo_id": "r1", "path": "a.py"})
    rules = [ArchRule(id="R1", kind=RuleKind.MUST_NOT_DEPEND, source="File", target="Incident")]
    result = check_conformance(store, rules)
    assert result["conformant"] is True
    assert result["errors"] == 0


def test_check_conformance_with_failure():
    store = MemoryGraphStore()
    f1 = store.upsert_vertex("File", {"canonical_id": "urn:f1", "repo_id": "r1", "path": "a.py"})
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:1", "service_id": "s1", "name": "DB"})
    store.upsert_edge("DEPENDS_ON", f1["vid"], svc["vid"], {"fact_key": "dep:1"})
    rules = [ArchRule(id="R1", kind=RuleKind.MUST_NOT_DEPEND, source="File", target="Service")]
    result = check_conformance(store, rules)
    assert result["conformant"] is False
    assert result["errors"] >= 1


def test_api_conformance_check_dsl():
    store = MemoryGraphStore()
    store.upsert_vertex("File", {"canonical_id": "urn:f1", "repo_id": "r1", "path": "a.py"})
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/conformance/check", json={
        "rules_dsl": "RULE R1: File MUST_NOT_DEPEND Incident"
    })
    assert resp.status_code == 200
    assert resp.json()["conformant"] is True


def test_api_conformance_check_rules_list():
    store = MemoryGraphStore()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/conformance/check", json={
        "rules": [{"id": "R1", "kind": "MUST_NOT_DEPEND", "source": "File", "target": "Service"}]
    })
    assert resp.status_code == 200


def test_api_conformance_no_rules():
    store = MemoryGraphStore()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/conformance/check", json={})
    assert resp.status_code == 400
