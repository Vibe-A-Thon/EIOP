"""
Unit Tests for Graffin Doctor, Curator, and Lifecycle Worker (GRF-REQ-*).
"""

import pytest

from reva.agents.graffin.doctor import GraffinDoctorDaemon
from reva.agents.graffin.curator import GraffinCurator
from reva.agents.graffin.worker import GraffinLifecycleWorker

pytestmark = pytest.mark.reva_depth("unit")


@pytest.fixture
def mock_graph_with_issues():
    return {
        "vertices": [
            {"id": "mod:auth.py", "kind": "kg_Module", "properties": {}},
            {"id": "cls:auth.py::AuthService", "kind": "kg_Class", "properties": {"docstring": ""}},
            {"id": "fn:auth.py::login", "kind": "kg_Function", "properties": {"docstring": ""}},
            {"id": "orphan:dangling_node", "kind": "kg_Module", "properties": {}},
            # Duplicate vertex
            {"id": "mod:auth.py", "kind": "kg_Module", "properties": {}},
        ],
        "edges": [
            {"source_id": "mod:auth.py", "target_id": "cls:auth.py::AuthService", "relation": "CONTAINS"},
            {"source_id": "cls:auth.py::AuthService", "target_id": "fn:auth.py::login", "relation": "CONTAINS"},
            # Dangling edge pointing to non-existent vertex
            {"source_id": "fn:auth.py::login", "target_id": "fn:non_existent::call", "relation": "CALLS"},
        ],
    }


def test_graffin_doctor_audit_and_compaction(mock_graph_with_issues):
    doctor = GraffinDoctorDaemon()
    audit = doctor.audit_graph(mock_graph_with_issues)

    assert not audit.is_healthy
    assert len(audit.duplicate_vertices) >= 1
    assert "mod:auth.py" in audit.duplicate_vertices
    assert len(audit.dangling_edges) >= 1
    assert any(e["target"] == "fn:non_existent::call" for e in audit.dangling_edges)

    # Compact graph
    compacted = doctor.compact_graph(mock_graph_with_issues)
    audit2 = doctor.audit_graph(compacted)
    assert audit2.is_healthy
    assert len(audit2.dangling_edges) == 0
    assert len(audit2.duplicate_vertices) == 0


def test_graffin_curator(mock_graph_with_issues):
    curator = GraffinCurator(tenant_id="tenant_alpha")
    gaps = curator.scan_for_gaps(mock_graph_with_issues)

    # Should flag missing docstrings on auth class and function
    assert len(gaps) >= 1
    assert any("AuthService" in g.target_entity for g in gaps)
    assert gaps[0].gap_id.startswith("gap1_")

    # Test contradiction quarantine
    quarantine = curator.quarantine_contradiction(
        conflict_key="auth.strategy",
        conflicting_warrant_ids=["wr1_1111111111111111111111111111111111111111111111111111111111111111", "wr1_2222222222222222222222222222222222222222222222222222222222222222"],
    )
    assert quarantine.contradiction_id.startswith("cx1_")
    assert quarantine.is_active
    assert len(quarantine.conflicting_warrants) == 2


def test_graffin_lifecycle_worker(mock_graph_with_issues):
    worker = GraffinLifecycleWorker(tenant_id="tenant_alpha")
    compacted, report = worker.run_curation_cycle(mock_graph_with_issues)

    assert report.status == "COMPLETED"
    assert report.cycle_index == 1
    assert report.ledger_id.startswith("ldg1_")
    assert report.remaining_budget < 1000.0  # consumed kappa
    assert report.duration_ms > 0.0
    assert len(compacted["vertices"]) == 4  # duplicates pruned
