from __future__ import annotations

import json

import httpx
from eoip.connectors.github import GitHubConnector
from eoip.contracts.source_registry import SourceRegistryEntry
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.github import GitHubIngestionService, run_registered_github_operation
from eoip.ingestion.jira import FileEventCapture


def _connector() -> GitHubConnector:
    return GitHubConnector(
        "github-prod",
        "https://api.github.com",
        "test-token",
        repositories=["acme/app"],
        client=httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(500))),
    )


def test_github_ingestion_builds_temporal_engineering_graph_and_evidence(tmp_path) -> None:
    connector = _connector()
    repo = {
        "id": 1,
        "node_id": "repo-1",
        "name": "app",
        "full_name": "acme/app",
        "html_url": "https://github.com/acme/app",
        "default_branch": "main",
        "updated_at": "2026-10-01T00:00:00Z",
        "owner": {"login": "acme", "id": 99, "html_url": "https://github.com/acme"},
    }
    events = [
        connector._event("acme/app", "repository", "1", repo),
        connector._event("acme/app", "branch", "main", {"name": "main", "commit": {"sha": "abc"}}),
        connector._event(
            "acme/app",
            "commit",
            "abc",
            {
                "sha": "abc",
                "commit": {
                    "message": "EOIP-1 implement feature",
                    "author": {"name": "Dev", "email": "dev@example.test", "date": "2026-10-01T01:00:00Z"},
                },
            },
        ),
        connector._event(
            "acme/app",
            "pull_request",
            "7",
            {
                "id": 7,
                "node_id": "pr-7",
                "number": 7,
                "title": "EOIP-1 ship feature",
                "state": "open",
                "updated_at": "2026-10-01T02:00:00Z",
                "head": {"ref": "feature", "sha": "abc"},
                "base": {"ref": "main"},
            },
        ),
        connector._event(
            "acme/app",
            "issue",
            "8",
            {"id": 8, "number": 8, "title": "Bug", "state": "open", "updated_at": "2026-10-01T03:00:00Z"},
        ),
        connector._event(
            "acme/app",
            "workflow_run",
            "50",
            {"id": 50, "name": "CI", "status": "completed", "conclusion": "success", "head_sha": "abc", "created_at": "2026-10-01T04:00:00Z"},
        ),
        connector._event(
            "acme/app",
            "release",
            "60",
            {"id": 60, "node_id": "release-60", "tag_name": "v1.0", "name": "Version 1", "published_at": "2026-10-01T05:00:00Z"},
        ),
        connector._event(
            "acme/app",
            "pages",
            "acme/app",
            {"html_url": "https://acme.example/app", "source": {"branch": "pages", "path": "/"}},
        ),
    ]
    store = MemoryGraphStore()
    store.upsert_vertex(
        "WorkItem",
        {"canonical_id": "urn:eoip:work:item:jira:EOIP-1", "issue_key": "EOIP-1", "summary": "Requirement"},
    )
    service = GitHubIngestionService(
        store, connector, FileEventCapture(tmp_path / "raw"), tmp_path / "dlq"
    )

    first = service.ingest(events)
    second = service.ingest(events)

    assert first["run_status"] == second["run_status"] == "SUCCEEDED"
    assert store.count_vertices("Repository") == 1
    assert store.count_vertices("Organization") == 1
    assert store.count_vertices("Branch") == 1
    assert store.count_vertices("Commit") == 1
    assert store.count_vertices("MergeRequest") == 1
    assert store.count_vertices("PipelineRun") == 1
    assert store.count_vertices("Release") == 1
    assert store.count_vertices("Document") == 1
    assert store.count_vertices("Evidence") == len(events)
    assert store.count_edges("HAS_MERGE_REQUEST") == 1
    assert store.count_edges("HAS_RELEASE") == 1
    assert store.count_edges("IMPLEMENTS") == 2
    assert store.count_edges("PRODUCED_BY") == 1
    assert len(list((tmp_path / "raw" / "github").glob("*.json"))) == len(events)


def test_github_delete_event_tombstones_branch_and_closes_revision(tmp_path) -> None:
    connector = _connector()
    store = MemoryGraphStore()
    service = GitHubIngestionService(
        store, connector, FileEventCapture(tmp_path / "raw"), tmp_path / "dlq"
    )
    created = connector._event(
        "acme/app", "branch", "obsolete", {"name": "obsolete", "commit": {"sha": "old"}}
    )
    service.ingest([created])
    deleted = next(
        connector.handle_event(
            {
                "_event_name": "delete",
                "ref": "obsolete",
                "ref_type": "branch",
                "repository": {"full_name": "acme/app"},
            }
        )
    )

    result = service.ingest([deleted])

    assert result["run_status"] == "SUCCEEDED"
    branch = store.get_vertex_by_canonical_id(
        "urn:eoip:code:branch:github:github-prod:acme/app:obsolete"
    )
    assert branch["properties"]["deleted_at"]
    revisions = store.find_vertices(
        label="EntityRevision", filters={"subject_id": branch["canonical_id"]}, limit=10
    )
    assert revisions[0]["properties"]["is_current"] is False


def test_registered_github_baseline_runs_common_checkpoint_and_manifest_flow(
    monkeypatch, tmp_path
) -> None:
    def handler(request):
        if request.url.path.endswith("/repos/acme/app"):
            return httpx.Response(
                200,
                json={
                    "id": 1,
                    "node_id": "repo-1",
                    "name": "app",
                    "full_name": "acme/app",
                    "updated_at": "2026-10-03T01:00:00Z",
                    "owner": {"login": "acme", "id": 99},
                },
            )
        if request.url.path.endswith("/actions/runs"):
            return httpx.Response(200, json={"workflow_runs": []})
        return httpx.Response(200, json=[])

    connector = GitHubConnector(
        "github-prod",
        "https://api.github.com",
        "token",
        repositories=["acme/app"],
        include_readme=False,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    entry = SourceRegistryEntry(
        source_id="github-prod",
        source_type="github",
        name="GitHub Production",
        base_url="https://api.github.com",
        capabilities={"polling": True, "webhooks": True, "reconciliation": True},
        config={"repositories": ["acme/app"]},
        secret_refs={"token": "env://EOIP_GITHUB_TOKEN"},
    )
    monkeypatch.setattr(
        "eoip.connectors.config.connector_from_registry", lambda *_args, **_kwargs: connector
    )
    store = MemoryGraphStore()

    result = run_registered_github_operation(
        entry,
        {"operation": "BASELINE", "dry_run": False},
        store,
        str(tmp_path),
        "correlation-1",
    )

    assert result["run_status"] == "SUCCEEDED"
    assert result["records_accepted"] == 1
    checkpoint = json.loads(
        (tmp_path / "state" / "connectors" / "github-prod.json").read_text()
    )
    assert checkpoint["checkpoint"] == "2026-10-03T01:00:00Z"
    manifest = json.loads(
        (tmp_path / "state" / "baselines" / "github-prod" / "correlation-1.json").read_text()
    )
    assert manifest["stage"] == "COMPLETE"
    assert store.count_vertices("Repository") == 1
