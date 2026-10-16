from __future__ import annotations

import httpx
import pytest
from eoip.connectors.base import DiscoveryScope, SourceConnector
from eoip.connectors.errors import ConnectorError
from eoip.connectors.github import GitHubConnector


def _repo():
    return {
        "id": 10,
        "node_id": "repo-node-10",
        "name": "app",
        "full_name": "acme/app",
        "private": True,
        "archived": False,
        "default_branch": "main",
        "has_pages": True,
        "updated_at": "2026-10-03T00:00:00Z",
        "owner": {"login": "acme", "type": "Organization"},
    }


@pytest.mark.req("FR-CONN-003", "G2-SRC-GH-001", "G2-SRC-GH-003", "G2-SRC-GH-004")
def test_github_baseline_discovers_and_emits_versioned_engineering_events() -> None:
    requests = []

    def handler(request):
        requests.append(request)
        path, page = request.url.path, int(request.url.params.get("page", "1"))
        if path.endswith("/repos/acme/app"):
            return httpx.Response(200, json=_repo())
        if path.endswith("/branches"):
            records = (
                [{"name": "main", "commit": {"sha": "abc"}}, {"name": "release", "commit": {"sha": "def"}}]
                if page == 1
                else []
            )
            return httpx.Response(200, json=records)
        if path.endswith("/tags"):
            return httpx.Response(200, json=[])
        if path.endswith("/commits"):
            return httpx.Response(
                200,
                json=[
                    {
                        "sha": "abc",
                        "commit": {
                            "message": "EOIP-1 implement",
                            "author": {"name": "Dev", "email": "dev@example.test", "date": "2026-10-02T10:00:00Z"},
                        },
                    }
                ],
            )
        if path.endswith("/pulls"):
            return httpx.Response(
                200,
                json=[
                    {
                        "id": 20,
                        "node_id": "pr-node-20",
                        "number": 7,
                        "title": "EOIP-1 feature",
                        "state": "open",
                        "updated_at": "2026-10-02T11:00:00Z",
                        "head": {"ref": "feature", "sha": "abc"},
                        "base": {"ref": "main"},
                    }
                ],
            )
        if path.endswith("/issues"):
            if page > 1:
                return httpx.Response(200, json=[])
            return httpx.Response(
                200,
                json=[
                    {"id": 30, "number": 8, "title": "Bug", "state": "open", "updated_at": "2026-10-02T12:00:00Z"},
                    {"id": 20, "number": 7, "title": "PR shadow", "pull_request": {}, "updated_at": "2026-10-02T11:00:00Z"},
                ],
            )
        if path.endswith("/releases"):
            return httpx.Response(
                200,
                json=[{"id": 40, "node_id": "release-40", "tag_name": "v1.0", "name": "Version 1", "published_at": "2026-10-02T13:00:00Z"}],
            )
        if path.endswith("/actions/runs"):
            return httpx.Response(
                200,
                json={"workflow_runs": [{"id": 50, "node_id": "run-50", "name": "CI", "status": "completed", "conclusion": "success", "head_sha": "abc", "created_at": "2026-10-02T14:00:00Z"}]},
            )
        if path.endswith("/pages"):
            return httpx.Response(200, json={"html_url": "https://acme.example/app", "source": {"branch": "pages", "path": "/"}})
        if path.endswith("/readme"):
            return httpx.Response(
                200,
                json={
                    "path": "README.md",
                    "sha": "readme-sha",
                    "html_url": "https://github.example/acme/app/README.md",
                    "encoding": "base64",
                    "content": "IyBHdWlkZQ==",
                },
            )
        raise AssertionError(path)

    connector = GitHubConnector(
        "github-prod",
        "https://github.example/api/v3",
        "test-token",
        repositories=["acme/app"],
        include_pages=True,
        page_size=2,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    discovery = connector.discover(DiscoveryScope())
    events = list(connector.baseline())

    assert isinstance(connector, SourceConnector)
    assert discovery.resources[0].resource_id == "acme/app"
    assert {event.metadata["record_kind"] for event in events} == {
        "repository",
        "branch",
        "commit",
        "pull_request",
        "issue",
        "release",
        "workflow_run",
        "pages",
        "readme",
    }
    assert all(event.schema_version == "2.0" for event in events)
    assert all(event.source_instance_id == "github-prod" for event in events)
    readme = next(event for event in events if event.metadata["record_kind"] == "readme")
    assert readme.payload["text"] == "# Guide"
    assert "content" not in readme.payload
    assert any(request.url.params.get("page") == "2" for request in requests)
    assert all(request.headers["authorization"] == "Bearer test-token" for request in requests)
    assert all(request.headers["x-github-api-version"] == "2022-11-28" for request in requests)


def test_github_poll_filters_non_incremental_endpoints_and_uses_since_where_supported() -> None:
    seen = []

    def handler(request):
        seen.append(request)
        if request.url.path.endswith("/repos/acme/app"):
            return httpx.Response(200, json=_repo())
        if request.url.path.endswith("/pulls"):
            return httpx.Response(
                200,
                json=[
                    {"number": 1, "updated_at": "2026-09-01T00:00:00Z"},
                    {"number": 2, "updated_at": "2026-10-03T01:00:00Z"},
                ],
            )
        if request.url.path.endswith("/actions/runs"):
            return httpx.Response(200, json={"workflow_runs": []})
        return httpx.Response(200, json=[])

    connector = GitHubConnector(
        "github-prod",
        "https://api.github.com",
        "test-token",
        repositories=["acme/app"],
        include_readme=False,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    events = list(connector.poll_changes("2026-10-01T00:00:00Z"))

    pulls = [event for event in events if event.metadata["record_kind"] == "pull_request"]
    assert [event.source_record_id for event in pulls] == ["acme/app:pull_request:2"]
    commit_request = next(request for request in seen if request.url.path.endswith("/commits"))
    issue_request = next(request for request in seen if request.url.path.endswith("/issues"))
    assert commit_request.url.params["since"] == "2026-10-01T00:00:00Z"
    assert issue_request.url.params["since"] == "2026-10-01T00:00:00Z"


def test_github_webhook_delete_and_error_categories_are_safe() -> None:
    connector = GitHubConnector(
        "github-prod",
        "https://api.github.com",
        "secret-that-must-not-leak",
        repositories=["acme/app"],
        client=httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(401))),
    )
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
    assert deleted.operation == "DELETE"
    assert deleted.payload is None

    with pytest.raises(ConnectorError) as exc_info:
        connector.fetch_record("acme/app:repository:10")
    assert exc_info.value.category == "authentication_failed"
    assert "secret-that-must-not-leak" not in str(exc_info.value)
