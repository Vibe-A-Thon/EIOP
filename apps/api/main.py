"""Uvicorn factory for the persistent deployment."""

import hmac
import logging
from contextlib import asynccontextmanager

import httpx
from eoip.jobs import JobQueue, write_json
from eoip.ontology.manifest import EDGE_LABELS, VERTEX_LABELS, edge_endpoints_valid
from eoip.runtime import api_token, create_store, data_root
from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPBearer
from prometheus_client import CollectorRegistry, Counter, generate_latest
from pydantic import BaseModel, Field

from apps.api.app import create_app as query_app

log = logging.getLogger("eoip.api")


class IngestionRequest(BaseModel):
    document: dict | list
    dry_run: bool = False


class TraceRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    max_depth: int = Field(default=4, ge=1, le=8)


class RetrievalRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    question: str = Field(
        default="Explain the implementation and its evidence", min_length=1, max_length=2048
    )
    synthesize: bool = False


def create_app():
    token = api_token()
    store = create_store()
    queue = JobQueue(data_root())
    app = query_app(store, dependencies=[Depends(HTTPBearer(auto_error=False))])
    registry = CollectorRegistry()
    requests = Counter(
        "eoip_http_requests_total", "Completed HTTP requests", ["method", "status"], registry=registry
    )

    @asynccontextmanager
    async def lifespan(app):
        yield
        store.close()

    app.router.lifespan_context = lifespan

    @app.middleware("http")
    async def boundary(request: Request, call_next):
        if request.url.path not in {
            "/health/live",
            "/health/ready",
            "/metrics",
            "/docs",
            "/openapi.json",
            "/docs/oauth2-redirect",
        }:
            supplied = request.headers.get("authorization", "").removeprefix("Bearer ")
            if not hmac.compare_digest(supplied, token):
                return JSONResponse({"detail": "A valid Bearer token is required"}, status_code=401)
        body = bytearray()
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > 4_000_000:
                return JSONResponse({"detail": "Request body too large"}, status_code=413)
        request._body = bytes(body)
        response = await call_next(request)
        requests.labels(request.method, response.status_code).inc()
        log.info(
            "method=%s path=%s status=%s correlation=%s",
            request.method,
            request.url.path,
            response.status_code,
            response.headers.get("x-correlation-id"),
        )
        return response

    @app.exception_handler(httpx.HTTPError)
    async def graph_unavailable(request, exc):
        log.error("Graph request failed (%s)", type(exc).__name__)
        return JSONResponse(
            {
                "detail": "Graph service unavailable",
                "correlation_id": getattr(request.state, "correlation_id", None),
            },
            status_code=503,
        )

    @app.get("/metrics", include_in_schema=False)
    def metrics():
        return Response(generate_latest(registry), media_type="text/plain; version=0.0.4")

    @app.get("/api/v1/entities/{canonical_id:path}")
    def entity(canonical_id: str):
        result = store.get_vertex_by_canonical_id(canonical_id)
        if result is None:
            raise HTTPException(404, "Entity not found")
        return {
            "entity": result,
            "outgoing": store.edges_from(result["vid"]),
            "incoming": store.edges_to(result["vid"]),
        }

    @app.get("/api/v1/admin/stats")
    def stats():
        return {
            "backend": "hugegraph",
            "schema": store.schema_status(),
            "vertices": store.count_vertices(),
            "edges": store.count_edges(),
            "labels": {label: store.count_vertices(label) for label in VERTEX_LABELS},
            "worker": worker_status(),
        }

    @app.get("/api/v1/admin/worker")
    def worker_status():
        import json

        path = data_root() / "state/worker.json"
        return json.loads(path.read_text()) if path.exists() else {"status": "starting"}

    @app.get("/api/v1/admin/jobs")
    def jobs():
        return queue.list()

    @app.get("/api/v1/admin/jobs/{job_id}")
    def job(job_id: str):
        try:
            result = queue.get(job_id)
            return {k: v for k, v in result.items() if k != "payload"}
        except (ValueError, FileNotFoundError):
            raise HTTPException(404, "Job not found")

    @app.post("/api/v1/admin/ingestion/jira", status_code=202)
    def ingest(payload: IngestionRequest):
        return queue.submit("JIRA_JSON", payload.model_dump())

    @app.post("/api/v1/admin/demo", status_code=202)
    def demo():
        return queue.submit("DEMO")

    @app.post("/api/v1/admin/validation")
    def validate():
        findings = []
        vertices = store.find_vertices(limit=10_001)
        for vertex in vertices:
            missing = [
                key for key in VERTEX_LABELS[vertex["label"]][1] if vertex["properties"].get(key) is None
            ]
            if missing:
                findings.append(
                    {
                        "canonical_id": vertex["canonical_id"],
                        "rule": "required_properties",
                        "missing": missing,
                    }
                )
        edges = store.find_edges(limit=10_001)
        for edge in edges:
            out_node, in_node = store.get_vertex(edge["out_v"]), store.get_vertex(edge["in_v"])
            if edge["label"] not in EDGE_LABELS or not edge_endpoints_valid(
                edge["label"], out_node["label"], in_node["label"]
            ):
                findings.append({"edge_id": edge["eid"], "rule": "endpoint_types"})
            if edge["label"] in {
                "IMPLEMENTS",
                "REFERENCES",
                "DOCUMENTS",
                "MODIFIES",
                "DECLARES",
            } and not edge["properties"].get("evidence_key"):
                findings.append({"edge_id": edge["eid"], "rule": "missing_evidence"})
        result = {
            "findings": findings,
            "valid": not findings,
            "partial": len(vertices) > 10_000 or len(edges) > 10_000,
            "vertices_checked": len(vertices),
            "edges_checked": len(edges),
        }
        write_json(data_root() / "state/validation.json", result)
        return result

    @app.post("/api/v1/agents/trace-impact")
    def trace(payload: TraceRequest):
        from eoip.graph.traversal import GraphTraversal

        result = GraphTraversal(store, max_results=100).impact(
            payload.canonical_id, max_depth=payload.max_depth
        )
        if not result["source"]:
            raise HTTPException(404, "Entity not found")
        refs = sorted(
            {
                e["properties"]["source_ref"]
                for item in result["impacted"]
                for e in item["path"]["edges"]
                if e["properties"].get("source_ref")
            }
        )
        return {
            "agent_id": "TraceImpact",
            "summary": f"Found {len(result['impacted'])} connected entities within {payload.max_depth} hops.",
            "evidence_refs": refs,
            "result": result,
            "generation": "deterministic",
            "partial": result["truncated"],
        }

    @app.post("/api/v1/rag")
    def rag(payload: RetrievalRequest):
        from eoip.retrieval.service import retrieve

        try:
            return retrieve(store, payload.canonical_id, payload.question, synthesize=payload.synthesize)
        except ValueError as exc:
            raise HTTPException(404, str(exc)) from exc

    return app
