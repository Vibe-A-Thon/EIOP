"""Tests for the graph-assertion test framework (GAP-GRAPHTEST-001..011)."""

import json

import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.graphtest import (
    GraphTestRunner,
    GraphTestSuite,
    load_suite,
    load_suite_file,
    run_suite,
)


@pytest.fixture()
def store() -> MemoryGraphStore:
    s = MemoryGraphStore()
    svc = s.upsert_vertex("Service", {
        "canonical_id": "urn:eoip:eng:service:svc-1", "service_id": "svc-1",
        "name": "svc-1", "valid_from": "2026-01-01", "source_system": "crawl",
    })
    api = s.upsert_vertex("File", {
        "canonical_id": "urn:eoip:eng:file:api", "repo_id": "r1", "path": "api.py",
        "valid_from": "2026-01-01",
    })
    db = s.upsert_vertex("File", {
        "canonical_id": "urn:eoip:eng:file:db", "repo_id": "r1", "path": "db.py",
        "valid_from": "2026-01-01",
    })
    s.upsert_vertex("File", {
        "canonical_id": "urn:eoip:eng:file:orphan", "repo_id": "r1",
        "path": "orphan.py", "valid_from": "2027-01-01",
    })
    person = s.upsert_vertex("Person", {
        "canonical_id": "urn:eoip:identity:person:alpha", "display_name": "alpha",
    })
    s.upsert_vertex("WorkItem", {
        "canonical_id": "urn:eoip:work:item:unassigned", "name": "unassigned",
    })
    req = s.upsert_vertex("Requirement", {
        "canonical_id": "urn:eoip:req:req-1", "name": "must serve",
    })

    s.upsert_edge("DEPENDS_ON", api["vid"], svc["vid"], {})
    s.upsert_edge("DEPENDS_ON", api["vid"], db["vid"], {})
    s.upsert_edge("ASSIGNED_TO", api["vid"], person["vid"], {})
    s.upsert_edge("ASSIGNED_TO", db["vid"], person["vid"], {})
    s.upsert_edge("TRACES_TO", req["vid"], svc["vid"], {})
    return s


def _assertion(data: dict):
    return load_suite({"id": "S", "assertions": [data]}).assertions[0]


def _run(store, data: dict):
    return GraphTestRunner(store).run_assertion(_assertion(data))


def test_path_exists(store):
    r = _run(store, {"id": "a", "type": "path_exists",
                     "source_label": "File", "target_label": "Service"})
    assert r.passed


def test_path_exists_missing(store):
    r = _run(store, {"id": "a", "type": "path_exists", "max_depth": 1,
                     "source_label": "Service", "target_label": "File"})
    assert not r.passed
    assert "urn:eoip:eng:service:svc-1" in r.violating_nodes


def test_path_forbidden(store):
    r = _run(store, {"id": "a", "type": "path_forbidden",
                     "source_label": "File", "target_label": "Service",
                     "via": ["ASSIGNED_TO"]})
    assert r.passed


def test_path_forbidden_violation(store):
    r = _run(store, {"id": "a", "type": "path_forbidden",
                     "source_label": "File", "target_label": "Service",
                     "via": ["DEPENDS_ON"]})
    assert not r.passed


def test_cardinality(store):
    r = _run(store, {"id": "a", "type": "cardinality",
                     "source_label": "File", "min_count": 1, "max_count": 2})
    assert r.passed


def test_cardinality_violation(store):
    r = _run(store, {"id": "a", "type": "cardinality",
                     "source_label": "File", "min_count": 3})
    assert not r.passed


def test_required_relationship(store):
    r = _run(store, {"id": "a", "type": "required_relationship",
                     "source_label": "File", "target_label": "Person",
                     "relationship": "ASSIGNED_TO"})
    assert r.passed


def test_required_relationship_missing(store):
    r = _run(store, {"id": "a", "type": "required_relationship",
                     "source_label": "File", "relationship": "MODIFIES"})
    assert not r.passed


def test_no_orphan(store):
    r = _run(store, {"id": "a", "type": "no_orphan", "label": "File"})
    assert not r.passed
    assert "urn:eoip:eng:file:orphan" in r.violating_nodes


def test_no_cycle(store):
    r = _run(store, {"id": "a", "type": "no_cycle", "label": "File"})
    assert r.passed


def test_no_cycle_detected(store):
    api = store.get_vertex_by_canonical_id("urn:eoip:eng:file:api")
    db = store.get_vertex_by_canonical_id("urn:eoip:eng:file:db")
    store.upsert_edge("DEPENDS_ON", db["vid"], api["vid"], {})
    r = _run(store, {"id": "a", "type": "no_cycle", "label": "File",
                     "via": ["DEPENDS_ON"]})
    assert not r.passed
    assert r.violating_nodes


def test_data_type(store):
    r = _run(store, {"id": "a", "type": "data_type", "label": "File",
                     "property": "path", "expected_type": "string"})
    assert r.passed


def test_data_type_violation(store):
    store.upsert_vertex("File", {"canonical_id": "urn:eoip:eng:file:bad",
                                 "repo_id": "r1", "path": 123})
    r = _run(store, {"id": "a", "type": "data_type", "label": "File",
                     "property": "path", "expected_type": "string"})
    assert not r.passed
    assert "urn:eoip:eng:file:bad" in r.violating_nodes


def test_ownership(store):
    r = _run(store, {"id": "a", "type": "ownership", "label": "File",
                     "ownership_edge": "ASSIGNED_TO", "owner_label": "Person"})
    assert r.passed


def test_ownership_missing(store):
    s2 = MemoryGraphStore()
    f = s2.upsert_vertex("File", {"canonical_id": "urn:f:loose", "repo_id": "r1",
                                  "path": "loose.py"})
    s2.upsert_vertex("Person", {"canonical_id": "urn:p:1", "display_name": "p"})
    r = _run(s2, {"id": "a", "type": "ownership", "label": "File",
                  "ownership_edge": "ASSIGNED_TO", "owner_label": "Person"})
    assert not r.passed
    assert "urn:f:loose" in r.violating_nodes


def test_provenance_present(store):
    r = _run(store, {"id": "a", "type": "provenance_present", "label": "Service"})
    assert r.passed


def test_provenance_present_missing(store):
    store.upsert_vertex("Service", {"canonical_id": "urn:eoip:eng:service:orphan",
                                    "service_id": "orphan", "name": "orphan"})
    r = _run(store, {"id": "a", "type": "provenance_present", "label": "Service"})
    assert not r.passed


def test_temporal_validity(store):
    r = _run(store, {"id": "a", "type": "temporal_validity",
                     "label": "Service", "as_of": "2026-06-01"})
    assert r.passed


def test_temporal_validity_violation(store):
    r = _run(store, {"id": "a", "type": "temporal_validity",
                     "label": "File", "as_of": "2026-06-01"})
    assert not r.passed
    assert "urn:eoip:eng:file:orphan" in r.violating_nodes


def test_architecture_boundary(store):
    r = _run(store, {"id": "a", "type": "architecture_boundary",
                     "source_label": "File", "target_label": "Service"})
    assert not r.passed  # api.py DEPENDS_ON svc-1 -> dependency violation


def test_architecture_boundary_respected(store):
    s2 = MemoryGraphStore()
    s2.upsert_vertex("File", {"canonical_id": "urn:f:1", "repo_id": "r1",
                              "path": "a.py"})
    s2.upsert_vertex("File", {"canonical_id": "urn:f:2", "repo_id": "r1",
                              "path": "b.py"})
    r = _run(s2, {"id": "a", "type": "architecture_boundary",
                  "source_label": "File", "target_label": "Service"})
    assert r.passed


def test_traceability_coverage(store):
    r = _run(store, {"id": "a", "type": "traceability_coverage",
                     "source_label": "Requirement", "target_label": "Service",
                     "via": ["TRACES_TO"], "coverage_threshold": 100.0})
    assert r.passed
    assert r.measured["coverage_pct"] == 100.0


def test_traceability_coverage_below_threshold(store):
    store.upsert_vertex("Requirement", {"canonical_id": "urn:eoip:req:req-2",
                                        "name": "unlinked"})
    r = _run(store, {"id": "a", "type": "traceability_coverage",
                     "source_label": "Requirement", "target_label": "Service",
                     "via": ["TRACES_TO"], "coverage_threshold": 100.0})
    assert not r.passed
    assert r.measured["coverage_pct"] == 50.0
    assert "urn:eoip:req:req-2" in r.violating_nodes


def test_load_suite_from_dict():
    suite = load_suite({
        "id": "S", "name": "dict suite",
        "assertions": [{"id": "a1", "type": "no_orphan", "label": "File"}],
    })
    assert suite.assertions[0].type.value == "no_orphan"


def test_load_suite_file(tmp_path):
    path = tmp_path / "suite.json"
    path.write_text(json.dumps({
        "id": "S", "assertions": [
            {"id": "a1", "type": "path_exists", "source_label": "File",
             "target_label": "Service"},
            {"id": "a2", "type": "no_orphan", "label": "Service"},
        ],
    }))
    suite = load_suite_file(str(path))
    assert len(suite.assertions) == 2


def test_run_suite_report(store):
    suite = GraphTestSuite(id="S1", name="test suite", assertions=[
        _assertion({"id": "a1", "type": "path_exists", "source_label": "File",
                    "target_label": "Service"}),
        _assertion({"id": "a2", "type": "no_orphan", "label": "File"}),
    ])
    report = run_suite(store, suite)
    assert report.total == 2 and report.passed == 1 and report.failed == 1
    d = report.to_dict()
    assert d["conformant"] is False
    a2 = next(r for r in d["results"] if r["id"] == "a2")
    assert "urn:eoip:eng:file:orphan" in a2["violating_nodes"]
