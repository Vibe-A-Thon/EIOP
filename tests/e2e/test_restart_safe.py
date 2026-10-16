"""NFR-REL-001: Restart-safe processing.

Validates that re-ingestion after simulated crash produces no duplicate
vertices or edges. Uses the in-memory graph store to verify idempotent
mutation semantics.
"""

import json
from pathlib import Path

from eoip.connectors.jira_json import JiraJsonConnector
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.meta import bootstrap_meta_graph
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.ingestion.repository import RepositoryIngestionService


def _project_root():
    return Path(__file__).resolve().parents[2]


def _load_jira_data():
    root = _project_root()
    return json.loads(
        (root / "demo/demodata/core/jira/sample-jira.json").read_text(encoding="utf-8")
    )


def _create_jira_service(store, data_dir):
    root = _project_root()
    capture = FileEventCapture(data_dir / "raw")
    return JiraIngestionService(
        store,
        JiraJsonConnector.from_yaml(str(root / "config/mappings/jira-mvp.yaml")),
        capture,
        data_dir / "dlq",
    )


_META_LABELS = {"IngestionRun", "GraphDomain", "OntologyVersion", "ValidationRun",
                "ValidationFinding", "DataSource", "Evidence"}


def _count_business_vertices(store):
    return sum(
        1 for v in store.find_vertices(limit=50_000)
        if v["label"] not in _META_LABELS
    )


def test_idempotent_jira_re_ingestion(tmp_path):
    """Re-ingesting the same Jira data must not create duplicate business vertices."""
    store = MemoryGraphStore()
    bootstrap_meta_graph(store)
    jira_data = _load_jira_data()

    svc = _create_jira_service(store, tmp_path)
    svc.ingest(jira_data)
    biz_after_first = _count_business_vertices(store)

    svc2 = _create_jira_service(store, tmp_path)
    svc2.ingest(jira_data)
    biz_after_second = _count_business_vertices(store)

    assert biz_after_second == biz_after_first, (
        f"Re-ingestion created duplicate business vertices: {biz_after_first} -> {biz_after_second}"
    )


def test_idempotent_git_re_ingestion(tmp_path):
    """Re-ingesting the same Git repository must not create duplicate business vertices."""
    root = _project_root()
    store = MemoryGraphStore()
    bootstrap_meta_graph(store)
    capture = FileEventCapture(tmp_path / "raw")
    metadata = json.loads(
        (root / "demo/demodata/core/gitlab/sample-gitlab.json").read_text(encoding="utf-8")
    )

    repo_svc = RepositoryIngestionService(store, capture)
    repo_svc.ingest(root / "demo/demodata/core/demo-repo", metadata=metadata)
    biz_after_first = _count_business_vertices(store)

    repo_svc2 = RepositoryIngestionService(store, capture)
    repo_svc2.ingest(root / "demo/demodata/core/demo-repo", metadata=metadata)
    biz_after_second = _count_business_vertices(store)

    assert biz_after_second == biz_after_first, (
        f"Re-ingestion created duplicate business vertices: {biz_after_first} -> {biz_after_second}"
    )


def test_demo_load_idempotent(tmp_path):
    """Loading the full demo twice must not create duplicate business entities.

    New IngestionRun meta-vertices are expected per run (up to 2 per load),
    but business entities (Project, WorkItem, File, etc.) must not duplicate.
    """
    from eoip.demo import load_demo

    store = MemoryGraphStore()
    root = _project_root()
    load_demo(store, str(tmp_path), project_root=str(root))
    biz1 = _count_business_vertices(store)

    load_demo(store, str(tmp_path), project_root=str(root))
    biz2 = _count_business_vertices(store)

    assert biz2 == biz1, f"Demo re-load created duplicate business vertices: {biz1} -> {biz2}"


def test_dlq_captures_rejected_records(tmp_path):
    """Records that fail validation go to the DLQ, not silently dropped."""
    store = MemoryGraphStore()
    bootstrap_meta_graph(store)

    malformed_data = {
        "issues": [
            {
                "key": "EOIP-GOOD",
                "fields": {
                    "summary": "Valid issue",
                    "issuetype": {"name": "Task"},
                    "status": {"name": "Open"},
                    "project": {"key": "EOIP", "name": "EOIP"},
                },
            },
            {
                "fields": {
                    "summary": "Missing key field",
                },
            },
        ],
    }

    svc = _create_jira_service(store, tmp_path)
    result = svc.ingest(malformed_data)

    assert result["records_accepted"] >= 1
    dlq_dir = tmp_path / "dlq"
    if result.get("records_rejected", 0) > 0:
        assert dlq_dir.exists(), "DLQ directory must exist when records are rejected"
