from __future__ import annotations

import json

import httpx
from eoip.connectors.gitlab import GitLabConnector
from eoip.contracts.source_registry import SourceRegistryEntry
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.gitlab_rest import (
    GitLabTemporalIngestionService,
    run_registered_gitlab_operation,
)
from eoip.ingestion.jira import FileEventCapture


def _connector() -> GitLabConnector:
    return GitLabConnector(
        "gitlab-prod",
        "https://gitlab.example/api/v4",
        "test-token",
        projects=["acme/app"],
        client=httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(500))),
    )


def test_gitlab_ingestion_builds_temporal_delivery_chain_and_documents(tmp_path) -> None:
    connector = _connector()
    project = "acme/app"
    repo = {
        "id": 10,
        "name": "app",
        "path_with_namespace": project,
        "web_url": "https://gitlab.example/acme/app",
        "default_branch": "main",
        "namespace": {"id": 2, "name": "Acme", "full_path": "acme"},
        "updated_at": "2026-10-01T00:00:00Z",
    }
    events = [
        connector._event("acme", "group", "2", {"id": 2, "name": "Acme", "full_path": "acme"}),
        connector._event(project, "project", "10", repo),
        connector._event(project, "branch", "main", {"name": "main", "commit": {"id": "abc"}}),
        connector._event(project, "tag", "v1.0", {"name": "v1.0", "commit": {"id": "abc"}}),
        connector._event(
            project,
            "commit",
            "abc",
            {
                "id": "abc",
                "message": "EOIP-1 implement feature",
                "author_name": "Dev",
                "committed_date": "2026-10-01T01:00:00Z",
            },
        ),
        connector._event(
            project,
            "merge_request",
            "7",
            {
                "iid": 7,
                "title": "EOIP-1 ship feature",
                "description": "Implements EOIP-1",
                "state": "opened",
                "sha": "abc",
                "source_branch": "feature",
                "target_branch": "main",
            },
        ),
        connector._event(
            project,
            "file_change",
            "7:src/app.py",
            {"new_path": "src/app.py", "merge_request_iid": "7", "commit_sha": "abc"},
        ),
        connector._event(
            project,
            "issue",
            "8",
            {"id": 8, "iid": 8, "title": "Bug", "state": "opened"},
        ),
        connector._event(
            project,
            "pipeline",
            "40",
            {"id": 40, "name": "CI", "status": "success", "sha": "abc"},
        ),
        connector._event(
            project,
            "job",
            "50",
            {
                "id": 50,
                "name": "build",
                "status": "success",
                "sha": "abc",
                "pipeline": {"id": 40},
            },
        ),
        connector._event(
            project,
            "artifact",
            "50:build.zip",
            {"job_id": "50", "filename": "build.zip", "file_type": "archive", "size": 123},
        ),
        connector._event(
            project,
            "deployment",
            "60",
            {
                "id": 60,
                "status": "success",
                "environment": {"name": "production"},
                "deployable": {"id": 50, "pipeline": {"id": 40}},
            },
        ),
        connector._event(
            project,
            "release",
            "v1.0",
            {"tag_name": "v1.0", "name": "Version 1", "released_at": "2026-10-01T05:00:00Z"},
        ),
        connector._event(
            project,
            "wiki",
            "runbook",
            {"slug": "runbook", "title": "Runbook", "content": "Operate it"},
        ),
        connector._event(project, "pages", project, {"url": "https://acme.gitlab.io/app"}),
        connector._event(
            project,
            "pages_content",
            "https://acme.gitlab.io/app/guide",
            {
                "url": "https://acme.gitlab.io/app/guide",
                "title": "Guide",
                "text": "Production guide",
            },
        ),
        connector._event(
            project,
            "pages_domain",
            "docs.example.test",
            {"domain": "docs.example.test", "url": "https://docs.example.test", "verified": True},
        ),
    ]
    store = MemoryGraphStore()
    store.upsert_vertex(
        "WorkItem",
        {"canonical_id": "urn:eoip:work:item:jira:EOIP-1", "issue_key": "EOIP-1", "summary": "Requirement"},
    )
    service = GitLabTemporalIngestionService(
        store,
        connector,
        FileEventCapture(tmp_path / "raw"),
        tmp_path / "dlq",
    )

    first = service.ingest(events)
    second = service.ingest(events)

    assert first["run_status"] == second["run_status"] == "SUCCEEDED"
    assert store.count_vertices("Organization") == 1
    assert store.count_vertices("Repository") == 1
    assert store.count_vertices("Commit") == 1
    assert store.count_vertices("MergeRequest") == 1
    assert store.count_vertices("File") == 1
    assert store.count_vertices("PipelineRun") == 1
    assert store.count_vertices("Job") == 1
    assert store.count_vertices("Artifact") == 1
    assert store.count_vertices("Deployment") == 1
    assert store.count_vertices("Release") == 1
    assert store.count_vertices("Document") == 4
    assert store.count_edges("HAS_JOB") == 1
    assert store.count_edges("PRODUCES") == 1
    assert store.count_edges("DEPLOYS") == 1
    assert store.count_edges("MODIFIES") == 2
    assert store.count_edges("IMPLEMENTS") == 2
    assert len(list((tmp_path / "raw" / "gitlab").glob("*.json"))) == len(events)


def test_registered_gitlab_baseline_uses_common_checkpoint_and_manifest(monkeypatch, tmp_path) -> None:
    def handler(request):
        if request.url.path.endswith("/projects/acme/app"):
            return httpx.Response(
                200,
                json={
                    "id": 10,
                    "name": "app",
                    "path_with_namespace": "acme/app",
                    "updated_at": "2026-10-03T01:00:00Z",
                    "wiki_enabled": False,
                    "pages_access_level": "disabled",
                },
            )
        return httpx.Response(200, json=[])

    connector = GitLabConnector(
        "gitlab-prod",
        "https://gitlab.example/api/v4",
        "token",
        projects=["acme/app"],
        include_readme=False,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    entry = SourceRegistryEntry(
        source_id="gitlab-prod",
        source_type="gitlab",
        name="GitLab Production",
        base_url="https://gitlab.example/api/v4",
        capabilities={"polling": True, "webhooks": True, "reconciliation": True},
        config={"projects": ["acme/app"]},
        secret_refs={"token": "env://EOIP_GITLAB_TOKEN"},
    )
    monkeypatch.setattr(
        "eoip.connectors.config.connector_from_registry",
        lambda *_args, **_kwargs: connector,
    )
    store = MemoryGraphStore()

    result = run_registered_gitlab_operation(
        entry,
        {"operation": "BASELINE", "dry_run": False},
        store,
        str(tmp_path),
        "correlation-1",
    )

    assert result["run_status"] == "SUCCEEDED"
    assert result["records_accepted"] == 1
    checkpoint = json.loads(
        (tmp_path / "state" / "connectors" / "gitlab-prod.json").read_text()
    )
    assert checkpoint["checkpoint"] == "2026-10-03T01:00:00Z"
    manifest = json.loads(
        (tmp_path / "state" / "baselines" / "gitlab-prod" / "correlation-1.json").read_text()
    )
    assert manifest["stage"] == "COMPLETE"
    assert store.count_vertices("Repository") == 1
