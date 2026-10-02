"""Read-only MCP façade using the same authenticated REST/query API."""

import hmac
import os

import httpx
from eoip.runtime import api_token
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route


def create_app():
    token = api_token()
    mcp = FastMCP(
        "EOIP",
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(
            allowed_hosts=["localhost:*", "127.0.0.1:*", "eoip-mcp:*"],
            allowed_origins=["http://localhost:*", "http://127.0.0.1:*"],
        ),
    )

    async def call(method, path, **kwargs):
        async with httpx.AsyncClient(
            base_url=os.getenv("EOIP_API_URL", "http://eoip-api:8000"),
            timeout=60,
            headers={"Authorization": f"Bearer {token}"},
            trust_env=False,
        ) as client:
            response = await client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()

    @mcp.tool()
    async def search(q: str, limit: int = 25) -> dict:
        """Search persisted entities by identifier, name, or source path."""
        return await call("GET", "/api/v1/search", params={"q": q, "limit": limit})

    @mcp.tool()
    async def entity(canonical_id: str) -> dict:
        """Read an entity and its incoming/outgoing evidence relationships."""
        from urllib.parse import quote

        return await call("GET", "/api/v1/entities/" + quote(canonical_id, safe=""))

    @mcp.tool()
    async def path(source_id: str, target_id: str, max_depth: int = 8) -> dict:
        """Find a bounded shortest path with source evidence."""
        return await call(
            "POST",
            "/api/v1/path",
            json={"source_id": source_id, "target_id": target_id, "max_depth": max_depth},
        )

    @mcp.tool()
    async def impact(canonical_id: str, max_depth: int = 4) -> dict:
        """Return bounded graph impact and evidence paths."""
        return await call(
            "POST", "/api/v1/impact", json={"canonical_id": canonical_id, "max_depth": max_depth}
        )

    @mcp.tool()
    async def lineage(
        canonical_id: str,
        max_depth: int = 4,
        result_limit: int = 100,
    ) -> dict:
        """Trace an entity to its source evidence and ingestion run."""
        return await call(
            "POST",
            "/api/v1/lineage",
            json={
                "canonical_id": canonical_id,
                "max_depth": max_depth,
                "result_limit": result_limit,
            },
        )

    @mcp.tool()
    async def trace_impact(canonical_id: str, max_depth: int = 4) -> dict:
        """Run the deterministic, read-only TraceImpact agent."""
        return await call(
            "POST", "/api/v1/agents/trace-impact", json={"canonical_id": canonical_id, "max_depth": max_depth}
        )

    app = mcp.streamable_http_app()

    class TokenBoundary(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            if request.url.path != "/health/live" and not hmac.compare_digest(
                request.headers.get("authorization", "").removeprefix("Bearer "), token
            ):
                return JSONResponse({"detail": "A valid Bearer token is required"}, status_code=401)
            return await call_next(request)

    async def health(request):
        return JSONResponse({"status": "ok"})

    app.routes.append(Route("/health/live", health))
    app.add_middleware(TokenBoundary)
    return app
