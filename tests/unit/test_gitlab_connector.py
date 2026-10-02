from __future__ import annotations

import httpx
import pytest
from eoip.connectors.base import DiscoveryScope, SourceConnector
from eoip.connectors.errors import ConnectorError
from eoip.connectors.gitlab import GitLabConnector


def _project():
    return {
        "id": 10,
        "name": "app",
        "path_with_namespace": "acme/app",
        "visibility": "private",
        "archived": False,
        "default_branch": "main",
        "wiki_enabled": True,
        "pages_access_level": "enabled",
        "updated_at": "2026-10-03T00:00:00Z",
        "namespace": {"id": 2, "name": "Acme", "path": "acme", "full_path": "acme"},
    }


def test_gitlab_baseline_emits_repository_delivery_and_knowledge_events() -> None:
    requests = []

    def handler(request):
        requests.append(request)
        path = request.url.path
        if path.endswith("/projects/acme/app"):
            return httpx.Response(200, json=_project())
        if path.endswith("/repository/branches"):
            if request.url.params.get("page") == "1":
                return httpx.Response(
                    200,
                    json=[{"name": "main", "commit": {"id": "abc"}}],
                    headers={"x-next-page": "2"},
                )
            return httpx.Response(200, json=[])
        if path.endswith("/repository/tags"):
            return httpx.Response(200, json=[{"name": "v1.0", "commit": {"id": "abc"}}])
        if path.endswith("/repository/commits"):
            return httpx.Response(
                200,
                json=[
                    {
                        "id": "abc",
                        "message": "EOIP-1 implement",
                        "author_name": "Dev",
                        "author_email": "dev@example.test",
                        "committed_date": "2026-10-02T10:00:00Z",
                    }
                ],
            )
        if path.endswith("/merge_requests"):
            return httpx.Response(
                200,
                json=[
                    {
                        "id": 20,
                        "iid": 7,
                        "title": "EOIP-1 feature",
                        "state": "opened",
                        "sha": "abc",
                        "updated_at": "2026-10-02T11:00:00Z",
                    }
                ],
            )
        if path.endswith("/merge_requests/7/diffs"):
            return httpx.Response(200, json=[{"old_path": "old.py", "new_path": "src/app.py"}])
        if path.endswith("/issues"):
            return httpx.Response(
                200,
                json=[{"id": 30, "iid": 8, "title": "Bug", "state": "opened", "updated_at": "2026-10-02T12:00:00Z"}],
            )
        if path.endswith("/pipelines"):
            return httpx.Response(
                200,
                json=[{"id": 40, "name": "CI", "status": "success", "sha": "abc", "updated_at": "2026-10-02T13:00:00Z"}],
            )
        if path.endswith("/jobs"):
            return httpx.Response(
                200,
                json=[
                    {
                        "id": 50,
                        "name": "build",
                        "status": "success",
                        "sha": "abc",
                        "pipeline": {"id": 40},
                        "created_at": "2026-10-02T14:00:00Z",
                        "artifacts": [
                            {"file_type": "archive", "filename": "build.zip", "size": 123}
                        ],
                    }
                ],
            )
        if path.endswith("/deployments"):
            return httpx.Response(
                200,
                json=[
                    {
                        "id": 60,
                        "status": "success",
                        "environment": {"name": "production"},
                        "deployable": {"id": 50, "pipeline": {"id": 40}},
                        "updated_at": "2026-10-02T15:00:00Z",
                    }
                ],
            )
        if path.endswith("/releases"):
            return httpx.Response(
                200,
                json=[{"tag_name": "v1.0", "name": "Version 1", "released_at": "2026-10-02T16:00:00Z"}],
            )
        if path.endswith("/wikis"):
            return httpx.Response(
                200,
                json=[{"slug": "runbook", "title": "Runbook", "content": "Operate it"}],
            )
        if path.endswith("/pages/domains"):
            return httpx.Response(
                200,
                json=[{"domain": "docs.example.test", "url": "https://docs.example.test", "verified": True}],
            )
        if path.endswith("/pages"):
            return httpx.Response(200, json={"url": "https://acme.gitlab.io/app"})
        if "/repository/files/README.md" in path:
            return httpx.Response(
                200,
                json={
                    "file_path": "README.md",
                    "blob_id": "readme-1",
                    "encoding": "base64",
                    "content": "IyBHdWlkZQ==",
                },
            )
        raise AssertionError(path)

    connector = GitLabConnector(
        "gitlab-prod",
        "https://gitlab.example/api/v4",
        "test-token",
        projects=["acme/app"],
        pages_scopes={
            "acme/app": {
                "start_urls": ["https://docs.example.test/"],
                "allowed_hosts": ["docs.example.test"],
                "max_depth": 0,
                "page_limit": 1,
            }
        },
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        pages_client=httpx.Client(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(
                    200,
                    text="<html><title>Production guide</title><h1>Operate</h1></html>",
                    headers={"content-type": "text/html"},
                )
            )
        ),
        pages_resolver=lambda _host: ["93.184.216.34"],
    )

    discovery = connector.discover(DiscoveryScope())
    events = list(connector.baseline())

    assert isinstance(connector, SourceConnector)
    assert discovery.resources[0].resource_id == "acme/app"
    assert {event.metadata["record_kind"] for event in events} == {
        "project",
        "branch",
        "tag",
        "commit",
        "merge_request",
        "file_change",
        "issue",
        "pipeline",
        "job",
        "artifact",
        "deployment",
        "release",
        "wiki",
        "pages",
        "pages_domain",
        "pages_content",
        "readme",
    }
    assert all(event.schema_version == "2.0" for event in events)
    readme = next(event for event in events if event.metadata["record_kind"] == "readme")
    assert readme.payload["text"] == "# Guide"
    pages_content = next(
        event for event in events if event.metadata["record_kind"] == "pages_content"
    )
    assert pages_content.payload["text"] == "Production guide Operate"
    assert any(request.url.params.get("page") == "2" for request in requests)
    assert all(request.headers["authorization"] == "Bearer test-token" for request in requests)


def test_gitlab_poll_uses_supported_incremental_filters_and_local_filtering() -> None:
    seen = []

    def handler(request):
        seen.append(request)
        if request.url.path.endswith("/projects/acme/app"):
            return httpx.Response(200, json={**_project(), "wiki_enabled": False, "pages_access_level": "disabled"})
        if request.url.path.endswith("/jobs"):
            return httpx.Response(
                200,
                json=[
                    {"id": 1, "created_at": "2026-09-01T00:00:00Z"},
                    {"id": 2, "created_at": "2026-10-03T01:00:00Z"},
                ],
            )
        return httpx.Response(200, json=[])

    connector = GitLabConnector(
        "gitlab-prod",
        "https://gitlab.example/api/v4",
        "test-token",
        projects=["acme/app"],
        include_readme=False,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    events = list(connector.poll_changes("2026-10-01T00:00:00Z"))

    jobs = [event for event in events if event.metadata["record_kind"] == "job"]
    assert [event.metadata["record_id"] for event in jobs] == ["2"]
    commit_request = next(request for request in seen if request.url.path.endswith("/repository/commits"))
    mr_request = next(request for request in seen if request.url.path.endswith("/merge_requests"))
    deployment_request = next(request for request in seen if request.url.path.endswith("/deployments"))
    assert commit_request.url.params["since"] == "2026-10-01T00:00:00Z"
    assert mr_request.url.params["updated_after"] == "2026-10-01T00:00:00Z"
    assert deployment_request.url.params["updated_after"] == "2026-10-01T00:00:00Z"


def test_gitlab_webhook_delete_and_safe_error_categories() -> None:
    connector = GitLabConnector(
        "gitlab-prod",
        "https://gitlab.example/api/v4",
        "secret-that-must-not-leak",
        projects=["acme/app"],
        client=httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(401))),
    )
    deleted = next(
        connector.handle_event(
            {
                "object_kind": "tag_push",
                "ref": "refs/tags/obsolete",
                "after": "0" * 40,
                "project": {"path_with_namespace": "acme/app"},
            }
        )
    )
    assert deleted.operation == "DELETE"
    assert deleted.payload is None

    with pytest.raises(ConnectorError) as exc_info:
        connector.fetch_record("acme/app:project:10")
    assert exc_info.value.category == "authentication_failed"
    assert "secret-that-must-not-leak" not in str(exc_info.value)
