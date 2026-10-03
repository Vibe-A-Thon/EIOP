"""Exercise the actual service boundary, not just standalone helper calls."""

import json
from contextvars import ContextVar
from pathlib import Path
from unittest.mock import Mock

import pytest
from eoip.codegraph.parser import CodeParser
from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.github import GitHubConnector
from eoip.connectors.gitlab import GitLabConnector
from eoip.connectors.gitlab_json import GitLabJsonConnector
from eoip.connectors.jira import JiraConnector
from eoip.connectors.jira_json import JiraJsonConnector
from eoip.connectors.local_code import LocalCodeConnector
from eoip.connectors.sync import SyncBatch
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion import pipeline
from eoip.ingestion.code import CodeIngestionService
from eoip.ingestion.github import GitHubIngestionService
from eoip.ingestion.gitlab import GitLabIngestionService
from eoip.ingestion.gitlab_rest import GitLabTemporalIngestionService
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.ingestion.jira_rest import JiraTemporalIngestionService
from eoip.ingestion.repository import RepositoryIngestionService
from eoip.ingestion.source_sync import SourceSyncIngestionService
from jsonschema import validate


@pytest.mark.parametrize(
    "kind", ["jira-json", "gitlab-json", "code", "repository", "github", "gitlab", "jira", "confluence"]
)
def test_every_service_consumes_contracts_after_capture(kind, tmp_path, monkeypatch):
    consuming = ContextVar("consuming", default=False)
    mutations = []
    raw_root = tmp_path / "raw"
    schema_root = Path(__file__).resolve().parents[2] / "schemas"
    schemas = {
        name: json.loads((schema_root / f"{name}.schema.json").read_text(encoding="utf-8"))
        for name in ("graph_mutation", "normalized_entity", "normalized_relationship")
    }

    class GuardedStore(MemoryGraphStore):
        def _guard(self):
            assert consuming.get(), "ingestion bypassed the GraphMutation consumer"
            assert list(raw_root.rglob("*.json")), "graph write preceded durable event capture"

        def upsert_vertex(self, label, properties):
            self._guard()
            return super().upsert_vertex(label, properties)

        def upsert_edge(self, label, out_v, in_v, properties):
            self._guard()
            return super().upsert_edge(label, out_v, in_v, properties)

        def tombstone_vertex(self, canonical_id):
            self._guard()
            return super().tombstone_vertex(canonical_id)

    consume = pipeline.apply_graph_mutation

    def recording_consumer(store, mutation):
        validate(mutation.model_dump(), schemas["graph_mutation"])
        payload_schema = "normalized_entity" if mutation.target_kind == "VERTEX" else "normalized_relationship"
        validate(mutation.payload, schemas[payload_schema])
        token = consuming.set(True)
        try:
            result = consume(store, mutation)
        finally:
            consuming.reset(token)
        mutations.append(mutation)
        return result

    monkeypatch.setattr(pipeline, "apply_graph_mutation", recording_consumer)
    store = GuardedStore()
    capture = FileEventCapture(raw_root)
    dlq = tmp_path / "dlq"
    if kind == "jira-json":
        service = JiraIngestionService(store, JiraJsonConnector(), capture, dlq)
        result = service.ingest({"issues": [{"key": "EOIP-1", "fields": {"summary": "Test"}}]})
    elif kind == "gitlab-json":
        service = GitLabIngestionService(store, "demo", GitLabJsonConnector(), capture, dlq)
        result = service.ingest({"pipelines": [{"id": 1, "name": "CI", "status": "success"}]})
    elif kind == "code":
        root = tmp_path / "repo"
        root.mkdir()
        (root / "main.py").write_text("def run():\n    return 1\n", encoding="utf-8")
        service = CodeIngestionService(store, LocalCodeConnector(), CodeParser(), capture, dlq)
        result = service.ingest(root, "demo")
    elif kind == "repository":
        # Repository metadata must also be captured before its first vertex.
        root = tmp_path / "repo"
        root.mkdir()
        service = RepositoryIngestionService(store, capture)
        monkeypatch.setattr(
            "eoip.ingestion.repository.subprocess.check_output",
            lambda args, **kwargs: {
                "rev-parse": b"abc\n", "log": b"", "diff-tree": b"", "ls-files": b"",
            }[args[3]],
        )
        result = service.ingest(root)
    elif kind in {"github", "gitlab", "jira"}:
        if kind == "github":
            connector = GitHubConnector(
                "test", "https://api.github.com", "test-token", repositories=["acme/app"]
            )
            service = GitHubIngestionService(store, connector, capture, dlq)
            event = connector._event("acme/app", "repository", "1", {"id": 1, "name": "app"})
        elif kind == "gitlab":
            connector = GitLabConnector(
                "test", "https://gitlab.example/api/v4", "test-token", projects=["acme/app"]
            )
            service = GitLabTemporalIngestionService(store, connector, capture, dlq)
            event = connector._event("acme/app", "project", "1", {"id": 1, "name": "app"})
        else:
            connector = JiraConnector(
                "test", "https://jira.example", token="test-token", projects=["EOIP"]
            )
            service = JiraTemporalIngestionService(store, connector, capture, dlq)
            event = connector._event("EOIP", "project", "1", {"id": "1", "key": "EOIP", "name": "Test"})
        result = service.ingest([event])
        assert service.evolution.store is service.store
    else:
        connector = ConfluenceConnector("https://confluence.example/wiki", token="test-token")
        service = SourceSyncIngestionService(store, connector, capture, str(dlq))
        event = connector.make_event(
            "space", f"{connector.instance_id}:space:ENG", {"key": "ENG", "name": "Engineering"}, 1
        )
        result = service.ingest(SyncBatch(events=[event], next_checkpoint=None))
        assert service.evolution.store is service.store

    assert mutations
    assert {mutation.ingestion_run_id for mutation in mutations} == {result["run_id"]}
    assert {mutation.target_kind for mutation in mutations} == {"VERTEX", "EDGE"}
    assert store.count_vertices("GraphDomain") > 0
    if kind in {"github", "gitlab", "jira", "confluence"}:
        assert any(mutation.payload.get("entity_type") == "EntityRevision" for mutation in mutations)


def test_run_context_is_isolated_and_required():
    from contextvars import Context

    store = pipeline.IngestionGraphStore(MemoryGraphStore())
    left, right = Context(), Context()
    left.run(store.begin_run, "left-run")
    right.run(store.begin_run, "right-run")
    assert left.run(store._run) == "left-run"
    assert right.run(store._run) == "right-run"
    with pytest.raises(RuntimeError, match="begin_run"):
        store.upsert_vertex("WorkItem", {"canonical_id": "urn:test"})


def test_tombstone_preserves_missing_entity_noop_and_existing_entity_behavior(monkeypatch):
    underlying = MemoryGraphStore()
    store = pipeline.IngestionGraphStore(underlying)
    store.begin_run("run-1")
    consume = Mock(wraps=pipeline.apply_graph_mutation)
    monkeypatch.setattr(pipeline, "apply_graph_mutation", consume)
    assert store.tombstone_vertex("urn:missing") is False
    consume.assert_not_called()
    store.upsert_vertex("WorkItem", {"canonical_id": "urn:existing"})
    assert store.tombstone_vertex("urn:existing") is True
    assert consume.call_args.args[1].operation == "TOMBSTONE"
    assert underlying.get_vertex_by_canonical_id("urn:existing")["properties"]["deleted_at"]


def test_invalid_normalized_mutation_does_not_reach_store():
    from eoip.contracts.graph_mutation import GraphMutation
    from eoip.validation.gate import MutationBlocked

    store = Mock(spec=MemoryGraphStore)
    mutation = GraphMutation(
        mutation_id="mutation-1", operation="UPSERT", target_kind="VERTEX", ingestion_run_id="run-1",
        payload={
            "canonical_id": "urn:test", "entity_type": "WorkItem", "graph_domain": "CODE",
            "source_refs": [], "properties": {},
        },
    )
    with pytest.raises(MutationBlocked, match="graph_domain"):
        pipeline.apply_graph_mutation(store, mutation)
    store.upsert_vertex.assert_not_called()


def test_contract_failure_is_explicit_and_preserves_captured_record(tmp_path, monkeypatch):
    connector = JiraConnector(
        "test", "https://jira.example", token="test-token", projects=["EOIP"]
    )
    store = MemoryGraphStore()
    service = JiraTemporalIngestionService(
        store, connector, FileEventCapture(tmp_path / "raw"), tmp_path / "dlq"
    )
    event = connector._event(
        "EOIP", "project", "1", {"id": "1", "key": "EOIP", "name": "Test"}
    )
    mapper = service._map

    def invalid_mapper(event):
        mapped = mapper(event)
        mapped["properties"]["confidence"] = 1.1
        return mapped

    monkeypatch.setattr(service, "_map", invalid_mapper)
    with pytest.raises(ValueError, match="confidence"):
        service.ingest([event])
    assert store.count_vertices("Project") == 0
    assert list((tmp_path / "raw").rglob("*.json"))
