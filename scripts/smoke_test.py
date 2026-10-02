"""Container smoke test: persisted data, worker replay, policies, web, and MCP."""

import asyncio
import json
import os
import time

import httpx
from eoip.runtime import api_token
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


def main():
    headers = {"Authorization": f"Bearer {api_token()}"}
    base = os.getenv("EOIP_API_URL", "http://eoip-api:8000")
    with httpx.Client(base_url=base, headers=headers, timeout=120, trust_env=False) as client:

        def get(path, **kwargs):
            response = client.get(path, **kwargs)
            response.raise_for_status()
            return response.json()

        def post(path, body):
            response = client.post(path, json=body)
            response.raise_for_status()
            return response.json()

        assert get("/health/ready")["status"] == "ready"
        unauthorized = httpx.get(base + "/api/v1/search?q=EOIP-1", trust_env=False)
        assert unauthorized.status_code == 401
        assert (
            client.post(
                "/api/v1/path", json={"source_id": "a", "target_id": "b", "max_depth": 99}
            ).status_code
            == 422
        )
        print("PASS: readiness, authentication, query limits", flush=True)
        for attempt in range(120):
            jobs = get("/api/v1/admin/jobs")
            if any(j["kind"] == "DEMO" and j["status"] == "SUCCEEDED" for j in jobs):
                break
            if any(j["kind"] == "DEMO" and j["status"] == "FAILED" for j in jobs):
                raise AssertionError(f"Demo ingestion failed: {jobs}")
            time.sleep(2)
        else:
            raise AssertionError("Demo worker did not finish")
        issue = "urn:eoip:work:item:jira:EOIP-1"
        symbols = get("/api/v1/search", params={"q": "compute_impact", "label": "CodeSymbol"})["nodes"]
        assert symbols, "Code symbol was not ingested"
        symbol = symbols[0]["id"]
        path = post("/api/v1/path", {"source_id": issue, "target_id": symbol})
        assert path["paths"] and path["evidence"]
        assert {e["type"] for e in path["edges"]}.issuperset({"IMPLEMENTS", "MODIFIES", "DECLARES"})
        impact = post("/api/v1/impact", {"canonical_id": issue})
        assert len(impact["nodes"]) >= 4
        trace = post("/api/v1/agents/trace-impact", {"canonical_id": issue})
        assert trace["evidence_refs"]
        rag = post("/api/v1/rag", {"canonical_id": issue, "synthesize": True})
        assert rag["facts"] and rag["evidence_refs"]
        validation = post("/api/v1/admin/validation", {})
        assert validation["valid"], validation
        print("PASS: Jira → commit → file → symbol, impact, evidence, validation", flush=True)
        before = get("/api/v1/admin/stats")["labels"]
        replay = post("/api/v1/admin/demo", {})
        for attempt in range(120):
            job = get(f"/api/v1/admin/jobs/{replay['job_id']}")
            if job["status"] in {"SUCCEEDED", "FAILED"}:
                break
            time.sleep(2)
        assert job["status"] == "SUCCEEDED", job
        after = get("/api/v1/admin/stats")["labels"]
        assert all(after[k] == v for k, v in before.items() if k != "IngestionRun")
        print("PASS: durable worker replay preserves logical entity counts", flush=True)
    response = httpx.get("http://eoip-web:8080/app", trust_env=False)
    assert response.status_code == 200 and '<div id="root"></div>' in response.text
    asyncio.run(check_mcp(headers, symbol))
    print("PASS: web frontend and real MCP search/path tools", flush=True)


async def check_mcp(headers, symbol):
    async with (
        httpx.AsyncClient(headers=headers, timeout=120, trust_env=False) as client,
        streamable_http_client("http://eoip-mcp:8001/mcp", http_client=client) as (read, write, _),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        tools = await session.list_tools()
        assert {tool.name for tool in tools.tools} == {
            "search",
            "entity",
            "path",
            "impact",
            "trace_impact",
        }
        result = await session.call_tool("search", {"q": "EOIP-1"})
        assert not result.isError
        result = await session.call_tool(
            "path", {"source_id": "urn:eoip:work:item:jira:EOIP-1", "target_id": symbol}
        )
        assert not result.isError
        envelope = result.structuredContent or json.loads(result.content[0].text)
        assert envelope["paths"]


if __name__ == "__main__":
    main()
