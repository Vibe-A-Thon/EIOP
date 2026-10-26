"""Exercise each MCP tool through the actual streamable HTTP protocol."""

import json

import httpx
import pytest
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from apps.mcp import main as mcp_main

TOKEN = "mcp-contract-test-token-with-at-least-24-chars"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool", "arguments", "method", "path", "params", "body"),
    [
        ("search", {"q": "EOIP-1", "limit": 3}, "GET", "/api/v1/search", {"q": "EOIP-1", "limit": "3"}, None),
        ("entity", {"canonical_id": "issue:A/B"}, "GET", "/api/v1/entities/issue%3AA%2FB", {}, None),
        ("path", {"source_id": "a", "target_id": "b", "max_depth": 2}, "POST", "/api/v1/path", {}, {"source_id": "a", "target_id": "b", "max_depth": 2}),
        ("impact", {"canonical_id": "a", "max_depth": 2}, "POST", "/api/v1/impact", {}, {"canonical_id": "a", "max_depth": 2}),
        ("lineage", {"canonical_id": "a", "max_depth": 2, "result_limit": 4}, "POST", "/api/v1/lineage", {}, {"canonical_id": "a", "max_depth": 2, "result_limit": 4}),
        ("trace_impact", {"canonical_id": "a", "max_depth": 2}, "POST", "/api/v1/agents/trace-impact", {}, {"canonical_id": "a", "max_depth": 2}),
        ("list_agents", {}, "GET", "/api/v1/agents", {}, None),
        ("run_agent", {"agent_id": "a/b", "goal": "inspect", "context_refs": ["x"], "dry_run": True}, "POST", "/api/v1/agents/a%2Fb/runs", {}, {"goal": "inspect", "context_refs": ["x"], "dry_run": True, "synthesize": False}),
        ("agent_explanation", {"run_id": "a/b"}, "GET", "/api/v1/agents/runs/a%2Fb/explanation", {}, None),
        ("blast_radius", {"canonical_id": "a", "max_depth": 2}, "POST", "/api/v1/graph/blast-radius", {}, {"canonical_id": "a", "max_depth": 2}),
        ("graph_surprises", {"limit": 3}, "POST", "/api/v1/graph/surprises", {}, {"limit": 3}),
        ("validate_ontology", {}, "POST", "/api/v1/admin/validation", {}, {}),
        ("neighbors", {"canonical_id": "a", "max_depth": 2, "result_limit": 4}, "POST", "/api/v1/neighborhood", {}, {"canonical_id": "a", "max_depth": 2, "result_limit": 4}),
        ("document", {"canonical_id": "doc:A/B"}, "GET", "/api/v1/entities/doc%3AA%2FB", {}, None),
        ("code_symbol", {"qualified_name": "pkg.Thing"}, "GET", "/api/v1/search", {"q": "pkg.Thing", "limit": "5"}, None),
        ("jira_issue", {"issue_key": "EOIP-1"}, "GET", "/api/v1/search", {"q": "EOIP-1", "limit": "5"}, None),
        ("evidence", {"canonical_id": "a"}, "POST", "/api/v1/lineage", {}, {"canonical_id": "a", "max_depth": 2, "result_limit": 50}),
        ("query", {"plan": {"limit": 2}}, "POST", "/api/v1/query", {}, {"limit": 2}),
    ],
)
async def test_every_mcp_tool_delegates_with_auth_and_arguments(
    monkeypatch, tool, arguments, method, path, params, body,
):
    monkeypatch.setenv("EOIP_API_TOKEN", TOKEN)
    monkeypatch.setenv("EOIP_API_URL", "http://eoip-api.test")
    requests = []
    real_client = httpx.AsyncClient

    def handler(request):
        requests.append(request)
        return httpx.Response(200, json={"tool": tool, "accepted": True})

    def api_client(*args, **kwargs):
        return real_client(*args, transport=httpx.MockTransport(handler), **kwargs)

    monkeypatch.setattr(mcp_main.httpx, "AsyncClient", api_client)
    app = mcp_main.create_app()
    async with (
        app.router.lifespan_context(app),
        real_client(
            transport=httpx.ASGITransport(app=app),
            base_url="http://localhost:8123",
            headers={"Authorization": f"Bearer {TOKEN}"},
        ) as client,
        streamable_http_client("http://localhost:8123/mcp", http_client=client) as (read, write, _),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        listed = await session.list_tools()
        assert len(listed.tools) == 18
        assert len({entry.name for entry in listed.tools}) == 18
        result = await session.call_tool(tool, arguments)

    assert not result.isError
    payload = json.loads(result.content[0].text)
    # KGR-G-019: the MCP layer adds the calibrated uncertainty envelope; the delegated API payload is unchanged.
    assert "uncertainty" in payload
    payload.pop("uncertainty")
    assert payload == {"tool": tool, "accepted": True}
    assert len(requests) == 1
    request = requests[0]
    assert request.method == method
    assert request.url.raw_path.split(b"?", 1)[0].decode("ascii") == path
    assert dict(request.url.params) == params
    assert request.headers["Authorization"] == f"Bearer {TOKEN}"
    assert (json.loads(request.content) if request.content else None) == body


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [400, 401, 403, 404, 429, 500])
async def test_mcp_upstream_failure_is_an_error_not_a_success(monkeypatch, status):
    monkeypatch.setenv("EOIP_API_TOKEN", TOKEN)
    real_client = httpx.AsyncClient

    def api_client(*args, **kwargs):
        return real_client(
            *args, transport=httpx.MockTransport(lambda _: httpx.Response(status, json={"detail": "denied"})),
            **kwargs,
        )

    monkeypatch.setattr(mcp_main.httpx, "AsyncClient", api_client)
    app = mcp_main.create_app()
    async with (
        app.router.lifespan_context(app),
        real_client(
            transport=httpx.ASGITransport(app=app),
            base_url="http://localhost:8123",
            headers={"Authorization": f"Bearer {TOKEN}"},
        ) as client,
        streamable_http_client("http://localhost:8123/mcp", http_client=client) as (read, write, _),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        result = await session.call_tool("search", {"q": "x"})

    assert result.isError
    assert str(status) in result.content[0].text
