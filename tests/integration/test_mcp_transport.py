import json

import httpx
import pytest
from eoip.graph.memory import MemoryGraphStore
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from apps.api import main as api_main
from apps.mcp import main as mcp_main


@pytest.mark.asyncio
async def test_mcp_streamable_http_searches_the_authenticated_api(monkeypatch, tmp_path):
    token = "integration-test-token-with-at-least-24-characters"
    store = MemoryGraphStore()
    store.upsert_vertex(
        "WorkItem",
        {"canonical_id": "issue:EOIP-1", "name": "EOIP-1", "summary": "Demo issue"},
    )
    monkeypatch.setenv("EOIP_API_TOKEN", token)
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("EOIP_API_URL", "http://eoip-api.test")
    monkeypatch.setattr(api_main, "create_store", lambda: store)
    api = api_main.create_app()
    real_async_client = httpx.AsyncClient

    def api_client(*args, **kwargs):
        return real_async_client(
            *args,
            transport=httpx.ASGITransport(app=api),
            **kwargs,
        )

    monkeypatch.setattr(mcp_main.httpx, "AsyncClient", api_client)
    mcp = mcp_main.create_app()

    async with (
        mcp.router.lifespan_context(mcp),
        real_async_client(
            transport=httpx.ASGITransport(app=mcp),
            base_url="http://localhost:8123",
            headers={"Authorization": f"Bearer {token}"},
        ) as mcp_http_client,
        streamable_http_client(
            "http://localhost:8123/mcp",
            http_client=mcp_http_client,
        ) as (read_stream, write_stream, _),
        ClientSession(read_stream, write_stream) as session,
    ):
        await session.initialize()
        listed_tools = await session.list_tools()
        result = await session.call_tool("search", {"q": "EOIP-1", "limit": 5})

    expected_tools = {
        "search", "entity", "path", "impact", "lineage", "trace_impact",
        "code_symbol", "jira_issue", "evidence", "query",
        "run_agent", "list_agents", "agent_explanation",
        "neighbors", "document",
    }
    assert expected_tools == {tool.name for tool in listed_tools.tools}
    assert not result.isError
    search_result = json.loads(result.content[0].text)
    assert [node["id"] for node in search_result["nodes"]] == ["issue:EOIP-1"]
    assert search_result["nodes"][0]["properties"]["summary"] == "Demo issue"


@pytest.mark.asyncio
async def test_mcp_streamable_http_rejects_unauthenticated_requests(monkeypatch):
    monkeypatch.setenv("EOIP_API_TOKEN", "integration-test-token-with-at-least-24-characters")
    mcp = mcp_main.create_app()

    async with (
        mcp.router.lifespan_context(mcp),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=mcp),
            base_url="http://localhost:8123",
        ) as client,
    ):
        response = await client.get("/mcp")

    assert response.status_code == 401
