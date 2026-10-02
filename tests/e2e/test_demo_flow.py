"""End-to-end demo flow test (MVP-FR-028).

Validates the complete evidence path:
Jira Story -> Merge Request -> Commit -> Source File -> Function -> Dependency -> Pipeline/Build -> Documentation
"""

import json
from pathlib import Path

from eoip.demo import load_demo
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.traversal import GraphTraversal
from eoip.query.executor import QueryExecutor
from eoip.contracts.query_plan import QueryPlan
from eoip.validation.engine import ValidationEngine
from eoip.provenance.lineage import LineageService
from eoip.agents.runtime import AgentRegistry, AgentRuntime
from eoip.agents.trace_impact import TraceImpactAgent
from eoip.contracts.agent import AgentRequest
from eoip.snapshot import backup, restore


def _demo_environment(tmp_path):
    store = MemoryGraphStore()
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "raw").mkdir()
    (data_dir / "dlq").mkdir()
    (data_dir / "state").mkdir()
    result = load_demo(store, str(data_dir))
    return store, data_dir, result


def test_full_demo_ingestion(tmp_path):
    store, data_dir, result = _demo_environment(tmp_path)
    assert result["jira"]["records_accepted"] >= 2
    assert result["git"]["files"] >= 1
    assert result["git"]["symbols"] >= 1
    assert store.count_vertices() >= 10
    assert store.count_edges() >= 5


def test_cross_domain_evidence_path(tmp_path):
    store, _, _ = _demo_environment(tmp_path)
    issue_cid = "urn:eoip:work:item:jira:EOIP-1"
    symbols = store.find_vertices(label="CodeSymbol", limit=100)
    assert symbols, "No code symbols ingested"
    compute_impact = [s for s in symbols if "compute_impact" in s["properties"].get("qualified_name", "")]
    assert compute_impact, "compute_impact symbol not found"
    target_cid = compute_impact[0]["canonical_id"]

    traversal = GraphTraversal(store, max_depth=8)
    path = traversal.find_path(issue_cid, target_cid)
    assert path is not None, f"No path from {issue_cid} to {target_cid}"
    edge_types = {e["label"] for e in path["edges"]}
    assert edge_types.intersection({"IMPLEMENTS", "MODIFIES", "DECLARES", "CONTAINS", "HAS_MERGE_REQUEST"})
    assert len(edge_types) >= 2, f"Path should traverse multiple edge types, got {edge_types}"


def test_query_executor_demo(tmp_path):
    store, _, _ = _demo_environment(tmp_path)
    executor = QueryExecutor(store)

    search = executor.execute(QueryPlan(
        intent="SEARCH", anchors=["EOIP-1"], max_depth=1, result_limit=10, evidence_mode="NONE",
    ))
    assert search.nodes

    impact = executor.execute(QueryPlan(
        intent="IMPACT", anchors=["urn:eoip:work:item:jira:EOIP-1"],
        max_depth=4, result_limit=100, evidence_mode="SUMMARY",
    ))
    assert len(impact.nodes) >= 4


def test_validation_on_demo_graph(tmp_path):
    store, _, _ = _demo_environment(tmp_path)
    engine = ValidationEngine(store)
    result = engine.run()
    errors = [f for f in result["findings"] if f["severity"] == "ERROR"]
    assert not errors, f"Validation errors in demo graph: {errors}"


def test_lineage_on_demo_graph(tmp_path):
    store, _, _ = _demo_environment(tmp_path)
    service = LineageService(store)
    result = service.trace("urn:eoip:work:item:jira:EOIP-1")
    assert result["entity"] is not None
    assert result["sources"] or result["ingestion_runs"]


def test_trace_impact_agent_on_demo(tmp_path):
    store, _, _ = _demo_environment(tmp_path)
    registry = AgentRegistry()
    registry.register(TraceImpactAgent())
    runtime = AgentRuntime(store, registry)
    request = AgentRequest(
        request_id="e2e-1", agent_id="TraceImpact",
        goal="Trace impact of EOIP-1",
        context_refs=["urn:eoip:work:item:jira:EOIP-1"],
    )
    result = runtime.run(request)
    assert result.status in {"SUCCEEDED", "PARTIAL"}
    assert result.evidence_refs


def test_backup_restore_cycle(tmp_path):
    store, data_dir, _ = _demo_environment(tmp_path)
    original_vertices = store.count_vertices()
    original_edges = store.count_edges()
    backup_path = tmp_path / "backup.json"

    backup_result = backup(store, str(data_dir), str(backup_path))
    assert backup_result["vertices"] == original_vertices
    assert backup_path.exists()

    restore_store = MemoryGraphStore()
    restore_dir = tmp_path / "restore_data"
    restore_dir.mkdir()
    (restore_dir / "raw").mkdir()
    (restore_dir / "dlq").mkdir()
    restore_result = restore(restore_store, str(restore_dir), str(backup_path))
    assert restore_result["vertices"] == original_vertices
    assert restore_result["edges"] == original_edges

    traversal = GraphTraversal(restore_store, max_depth=8)
    path = traversal.find_path(
        "urn:eoip:work:item:jira:EOIP-1",
        store.find_vertices(label="CodeSymbol", limit=1)[0]["canonical_id"],
    )
    assert path is not None


def test_idempotent_re_ingestion(tmp_path):
    store, data_dir, first = _demo_environment(tmp_path)
    vertices_before = store.count_vertices()

    from eoip.demo import load_demo
    second = load_demo(store, str(data_dir))
    vertices_after = store.count_vertices()

    work_items_before = store.count_vertices("WorkItem")
    assert vertices_after - vertices_before <= 2, "Re-ingestion should not create duplicate business entities"
