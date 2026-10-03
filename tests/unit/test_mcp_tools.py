import asyncio

from starlette.applications import Starlette

from apps.mcp import main as mcp_main


def test_mcp_exposes_read_only_lineage_using_the_shared_api(monkeypatch):
    tools = {}
    requests = []

    class RecordingMCP:
        def __init__(self, *args, **kwargs):
            pass

        def tool(self):
            def register(function):
                tools[function.__name__] = function
                return function

            return register

        def streamable_http_app(self):
            return Starlette()

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "query_id": "lineage-result",
                "nodes": [],
                "edges": [],
                "paths": [],
                "evidence": [],
                "partial": False,
            }

    class Client:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def request(self, method, path, **kwargs):
            requests.append((method, path, kwargs))
            return Response()

    monkeypatch.setenv("EOIP_API_TOKEN", "x" * 32)
    monkeypatch.setattr(mcp_main, "FastMCP", RecordingMCP)
    monkeypatch.setattr(mcp_main.httpx, "AsyncClient", Client)
    mcp_main.create_app()

    expected_tools = {
        "search", "entity", "path", "impact", "lineage", "trace_impact",
        "code_symbol", "jira_issue", "evidence", "query",
        "run_agent", "list_agents", "agent_explanation",
        "neighbors", "document",
    }
    assert expected_tools == set(tools)
    result = asyncio.run(
        tools["lineage"](
            canonical_id="urn:eoip:work:item:jira:EOIP-1",
            max_depth=3,
            result_limit=25,
        )
    )

    assert result["query_id"] == "lineage-result"
    assert requests == [
        (
            "POST",
            "/api/v1/lineage",
            {
                "json": {
                    "canonical_id": "urn:eoip:work:item:jira:EOIP-1",
                    "max_depth": 3,
                    "result_limit": 25,
                }
            },
        )
    ]
