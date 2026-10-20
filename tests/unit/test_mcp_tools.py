from _principals import provision_api_token
import asyncio

import pytest

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
    provision_api_token(monkeypatch, "x" * 32)
    monkeypatch.setattr(mcp_main, "FastMCP", RecordingMCP)
    monkeypatch.setattr(mcp_main.httpx, "AsyncClient", Client)
    mcp_main.create_app()

    expected_tools = {
        "search", "entity", "path", "impact", "lineage", "trace_impact",
        "code_symbol", "jira_issue", "evidence", "query",
        "run_agent", "list_agents", "agent_explanation",
        "neighbors", "document", "blast_radius", "graph_surprises", "validate_ontology",
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


def _recording_app(monkeypatch, payload):
    tools = {}

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
            return payload

    class Client:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def request(self, method, path, **kwargs):
            return Response()

    monkeypatch.setenv("EOIP_API_TOKEN", "x" * 32)
    provision_api_token(monkeypatch, "x" * 32)
    monkeypatch.setattr(mcp_main, "FastMCP", RecordingMCP)
    monkeypatch.setattr(mcp_main.httpx, "AsyncClient", Client)
    mcp_main.create_app()
    return tools


def _call_with_dummies(fn):
    import inspect

    kwargs = {}
    for name, param in inspect.signature(fn).parameters.items():
        if param.default is not inspect.Parameter.empty:
            continue
        ann = str(param.annotation)
        kwargs[name] = {} if "dict" in ann else (1 if "int" in ann else "urn:eoip:x")
    return asyncio.run(fn(**kwargs))



@pytest.mark.req("KGR-G-019")
def test_every_mcp_tool_response_carries_the_five_uncertainty_fields(monkeypatch):
    payload = {"query_id": "q1", "nodes": [{"canonical_id": "urn:a"}, {"canonical_id": "urn:b"}],
               "evidence": [{"evidence_id": "ev-1"}], "partial": False}
    tools = _recording_app(monkeypatch, payload)
    assert tools
    for name, fn in sorted(tools.items()):
        result = _call_with_dummies(fn)
        unc = result["uncertainty"]
        assert isinstance(unc["confidence_score"], float) and 0.0 <= unc["confidence_score"] <= 1.0, name
        assert isinstance(unc["uncertainty_reason"], str) and unc["uncertainty_reason"], name
        assert isinstance(unc["abstain"], bool), name
        assert isinstance(unc["evidence_chain"], dict) and unc["evidence_chain"]["total_sources"] == 3, name
        assert isinstance(unc["coverage_percent"], float), name
        # backward compatible: the original payload is untouched for clients that ignore the envelope
        assert {k: v for k, v in result.items() if k != "uncertainty"} == payload, name


@pytest.mark.req("KGR-G-019")
def test_mcp_response_without_evidence_abstains_honestly(monkeypatch):
    tools = _recording_app(monkeypatch, {"query_id": "q2", "nodes": [], "evidence": []})
    unc = _call_with_dummies(tools["search"])["uncertainty"]
    assert unc["abstain"] is True
    assert unc["uncertainty_reason"] == "OUT_OF_SCOPE"
    assert unc["evidence_chain"]["total_sources"] == 0
