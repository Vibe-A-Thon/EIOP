"""Uvicorn factory for the persistent deployment."""

import hmac
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from time import perf_counter
from uuid import uuid4

import httpx
from eoip.agents.runtime import AgentRegistry, AgentRuntime
from eoip.agents.trace_impact import TraceImpactAgent
from eoip.audit.sink import AuditSink
from eoip.config import load_agent_config
from eoip.contracts.agent import AgentRequest
from eoip.contracts.audit import AuditEvent
from eoip.jobs import JobQueue, write_json
from eoip.models.provider import LocalModelProvider
from eoip.observability import configure_json_logging
from eoip.ontology.manifest import VERTEX_LABELS
from eoip.ontology.rdf import export_jsonld
from eoip.runtime import api_token, create_store, data_root
from eoip.validation.engine import ValidationEngine
from fastapi import Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPBearer
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest
from pydantic import BaseModel, Field

from apps.api.app import create_app as query_app

log = logging.getLogger("eoip.api")


def _operation(path: str, body: bytes) -> str:
    if (
        path.startswith("/api/v1/admin/ingestion/")
        or path == "/api/v1/ingestion/jira-json"
        or path == "/api/v1/admin/demo"
    ):
        return "ingestion"
    if path == "/api/v1/admin/validation":
        return "validation"
    if path == "/api/v1/agents/trace-impact":
        return "agent"
    if path == "/api/v1/rag":
        try:
            if json.loads(body).get("synthesize") is True:
                return "model"
        except (ValueError, AttributeError):
            pass
        return "query"
    if path in {
        "/api/v1/search",
        "/api/v1/query",
        "/api/v1/path",
        "/api/v1/impact",
        "/api/v1/lineage",
        "/api/v1/neighborhood",
        "/api/v1/traceability",
        "/api/v1/ontology/export",
    } or path.startswith("/api/v1/entities/"):
        return "query"
    if path.startswith("/api/v1/admin/"):
        return "admin"
    return "other"


def _safe_path(path: str) -> str:
    if path.startswith("/api/v1/entities/"):
        return "/api/v1/entities/{canonical_id:path}"
    if path.startswith("/api/v1/admin/jobs/"):
        return "/api/v1/admin/jobs/{job_id}"
    return path


class IngestionRequest(BaseModel):
    document: dict | list
    dry_run: bool = False


class IncrementalSyncRequest(BaseModel):
    checkpoint: str | None = Field(default=None, max_length=128)
    watermark: str | None = Field(default=None, max_length=128)
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
    configure_json_logging()
    token = api_token()
    store = create_store()
    queue = JobQueue(data_root())
    audit_sink = AuditSink(data_root() / "audit")
    validator = ValidationEngine(store)
    agent_registry = AgentRegistry()
    agent_registry.register(TraceImpactAgent(load_agent_config("trace-impact")))
    agent_runtime = AgentRuntime(store, agent_registry)
    app = query_app(store, dependencies=[Depends(HTTPBearer(auto_error=False))])
    registry = CollectorRegistry()
    requests = Counter(
        "eoip_http_requests_total", "Completed HTTP requests", ["method", "status"], registry=registry
    )
    operations = Counter(
        "eoip_operations",
        "Completed EOIP operations",
        ["operation", "status"],
        registry=registry,
    )
    failures = Counter(
        "eoip_failures",
        "Failed EOIP operations",
        ["operation", "status"],
        registry=registry,
    )
    operation_duration = Histogram(
        "eoip_operation_duration_seconds",
        "EOIP operation latency in seconds",
        ["operation"],
        registry=registry,
    )
    job_status_transitions = Counter(
        "eoip_ingestion_job_status_transitions",
        "Observed ingestion job status transitions",
        ["kind", "status"],
        registry=registry,
    )
    job_duration = Histogram(
        "eoip_ingestion_job_duration_seconds",
        "Ingestion job runtime in seconds",
        ["kind"],
        registry=registry,
    )
    observed_job_states: dict[str, str] = {}

    def observe_ingestion_jobs() -> None:
        terminal_statuses = {"SUCCEEDED", "PARTIAL", "FAILED"}
        for path in queue.root.glob("*.json"):
            job = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(job, dict):
                raise TypeError(f"Invalid ingestion job record: {path.name}")
            job_id, kind, status = job.get("job_id"), job.get("kind"), job.get("status")
            if not all(isinstance(value, str) for value in (job_id, kind, status)):
                raise ValueError(f"Invalid ingestion job record: {path.name}")
            if status not in {"PENDING", "RUNNING", *terminal_statuses}:
                raise ValueError(f"Invalid ingestion job status in record: {path.name}")
            previous_status = observed_job_states.get(job_id)
            if previous_status != status:
                job_status_transitions.labels(kind, status).inc()
                observed_job_states[job_id] = status
            started_value, finished_value = job.get("started_at"), job.get("finished_at")
            if (
                status in terminal_statuses
                and previous_status not in terminal_statuses
                and isinstance(started_value, str)
                and isinstance(finished_value, str)
            ):
                started_at = datetime.fromisoformat(started_value)
                finished_at = datetime.fromisoformat(finished_value)
                duration = max(0.0, (finished_at - started_at).total_seconds())
                job_duration.labels(kind).observe(duration)

    @asynccontextmanager
    async def lifespan(app):
        log.info(
            "application.started",
            extra={
                "event": "application.started",
                "operation": "startup",
                "correlation_id": str(uuid4()),
            },
        )
        yield
        log.info(
            "application.stopped",
            extra={
                "event": "application.stopped",
                "operation": "shutdown",
                "correlation_id": str(uuid4()),
            },
        )
        store.close()

    app.router.lifespan_context = lifespan

    @app.middleware("http")
    async def boundary(request: Request, call_next):
        started = perf_counter()
        supplied_correlation_id = request.headers.get("X-Correlation-ID", "")
        correlation_id = (
            supplied_correlation_id
            if 0 < len(supplied_correlation_id) <= 128
            else str(uuid4())
        )
        request.state.correlation_id = correlation_id
        request.state.audit_id = str(uuid4())
        operation = _operation(request.url.path, b"")

        def record(status_code: int, response: Response | None = None) -> None:
            duration = perf_counter() - started
            status = str(status_code)
            audit = None
            if operation != "other":
                denied = status_code in {401, 403, 413}
                audit = AuditEvent(
                    audit_id=request.state.audit_id,
                    event_type="policy_denial" if denied else operation,
                    actor="anonymous" if status_code == 401 else "local-user",
                    correlation_id=correlation_id,
                    outcome="denied" if denied else "success" if status_code < 400 else "failure",
                    reason_code=f"http_{status_code}" if status_code >= 400 else None,
                    safe_summary=f"{operation} operation completed with status {status_code}",
                )
            requests.labels(request.method, status).inc()
            operations.labels(operation, status).inc()
            operation_duration.labels(operation).observe(duration)
            if status_code >= 400:
                failures.labels(operation, status).inc()
            if audit is not None:
                audit_sink.emit(audit, operation=operation, path=request.url.path)
            if response is not None:
                response.headers["X-Correlation-ID"] = correlation_id
                if operation != "other":
                    response.headers["X-Audit-ID"] = request.state.audit_id
            fields = {
                "event": "http.request.completed",
                "operation": operation,
                "correlation_id": correlation_id,
                "audit_id": request.state.audit_id if operation != "other" else None,
                "method": request.method,
                "path": getattr(request.scope.get("route"), "path", None)
                or _safe_path(request.url.path),
                "status_code": status_code,
                "duration_seconds": round(duration, 6),
            }
            if audit is not None:
                fields.update(audit.model_dump(exclude_none=True))
            log.log(
                logging.ERROR if status_code >= 500 else logging.INFO,
                "http.request.completed",
                extra=fields,
            )

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
                record(401)
                return JSONResponse({"detail": "A valid Bearer token is required"}, status_code=401)
        body = bytearray()
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > 4_000_000:
                record(413)
                return JSONResponse({"detail": "Request body too large"}, status_code=413)
        request._body = bytes(body)
        operation = _operation(request.url.path, request._body)
        try:
            response = await call_next(request)
        except Exception as exc:
            record(500)
            log.error(
                "http.request.failed",
                extra={
                    "event": "http.request.failed",
                    "operation": operation,
                    "correlation_id": correlation_id,
                    "audit_id": request.state.audit_id if operation != "other" else None,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": 500,
                    "error_type": type(exc).__name__,
                },
            )
            raise
        record(response.status_code, response)
        return response

    @app.exception_handler(httpx.HTTPError)
    async def graph_unavailable(request, exc):
        log.error(
            "graph.request.failed",
            extra={
                "event": "graph.request.failed",
                "operation": "graph",
                "correlation_id": getattr(request.state, "correlation_id", None),
                "error_type": type(exc).__name__,
            },
        )
        return JSONResponse(
            {
                "detail": "Graph service unavailable",
                "correlation_id": getattr(request.state, "correlation_id", None),
            },
            status_code=503,
        )

    @app.get("/metrics", include_in_schema=False)
    def metrics():
        observe_ingestion_jobs()
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

    @app.get("/api/v1/ontology/export")
    def ontology_export(limit: int = Query(default=5000, ge=1, le=10_000)):
        document = export_jsonld(store, limit=limit)
        return Response(
            content=json.dumps(document, ensure_ascii=False),
            media_type="application/ld+json",
        )

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

    @app.get("/api/v1/admin/system")
    def system_status():
        """Return real local-operability state used by the admin experience."""
        backup_dir = data_root() / "backups"
        backup_items = []
        for path in sorted(
            backup_dir.glob("*.json") if backup_dir.exists() else [],
            key=lambda item: item.stat().st_mtime,
            reverse=True,
        ):
            try:
                archive = json.loads(path.read_text(encoding="utf-8"))
                payload = archive.get("payload", {})
                backup_items.append(
                    {
                        "file": path.name,
                        "created_at": payload.get("created_at"),
                        "schema_version": payload.get("schema_version"),
                        "vertices": len(payload.get("vertices", [])),
                        "edges": len(payload.get("edges", [])),
                        "sha256": archive.get("sha256"),
                        "size_bytes": path.stat().st_size,
                    }
                )
            except (OSError, ValueError, TypeError):
                continue

        model = LocalModelProvider(timeout=2)
        model_status = "disabled"
        if model.available:
            model_status = "ready" if model.health() else "unavailable"

        connector_state = data_root() / "state/connectors"
        checkpoints = len(list(connector_state.glob("*.json"))) if connector_state.exists() else 0
        return {
            "graph": {"status": "ready" if store.health() else "unavailable"},
            "model": {
                "status": model_status,
                "configured": model.available,
                "name": model.model_name,
            },
            "backup": {
                "status": "available" if backup_items else "not_created",
                "count": len(backup_items),
                "latest": backup_items[0] if backup_items else None,
            },
            "connectors": {"checkpoint_count": checkpoints},
        }

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
    def ingest(payload: IngestionRequest, request: Request):
        return queue.submit(
            "JIRA_JSON",
            payload.model_dump(),
            correlation_id=request.state.correlation_id,
        )

    @app.post("/api/v1/admin/ingestion/gitlab", status_code=202)
    def ingest_gitlab(payload: IngestionRequest, request: Request):
        return queue.submit(
            "GITLAB_JSON",
            payload.model_dump(),
            correlation_id=request.state.correlation_id,
        )

    @app.post("/api/v1/admin/ingestion/confluence", status_code=202)
    def ingest_confluence(payload: IncrementalSyncRequest, request: Request):
        return queue.submit(
            "CONFLUENCE",
            payload.model_dump(),
            correlation_id=request.state.correlation_id,
        )

    @app.post("/api/v1/admin/ingestion/servicenow", status_code=202)
    def ingest_servicenow(payload: IncrementalSyncRequest, request: Request):
        return queue.submit(
            "SERVICENOW",
            payload.model_dump(),
            correlation_id=request.state.correlation_id,
        )

    @app.post("/api/v1/admin/demo", status_code=202)
    def demo(request: Request):
        return queue.submit("DEMO", correlation_id=request.state.correlation_id)

    @app.post("/api/v1/admin/validation")
    def validate():
        result = validator.run()
        write_json(data_root() / "state/validation.json", result)
        return result

    @app.post("/api/v1/agents/trace-impact")
    def trace(payload: TraceRequest):
        request = AgentRequest(
            request_id=str(uuid4()),
            agent_id="TraceImpact",
            goal=f"Trace impact of {payload.canonical_id}",
            context_refs=[payload.canonical_id],
            budgets={"max_depth": payload.max_depth},
        )
        result = agent_runtime.run(request)
        if result.status == "FAILED" and "not found" in result.summary.lower():
            raise HTTPException(404, "Entity not found")
        return {
            "agent_id": result.request_id,
            "summary": result.summary,
            "evidence_refs": result.evidence_refs,
            "tool_calls": result.tool_calls,
            "generation": "deterministic",
            "partial": result.status == "PARTIAL",
        }

    @app.post("/api/v1/rag")
    def rag(payload: RetrievalRequest):
        from eoip.retrieval.service import retrieve

        try:
            return retrieve(store, payload.canonical_id, payload.question, synthesize=payload.synthesize)
        except ValueError as exc:
            raise HTTPException(404, str(exc)) from exc

    @app.get("/api/v1/admin/dlq")
    def dlq_list(limit: int = Query(default=50, ge=1, le=500)):
        dlq_dir = data_root() / "dlq"
        if not dlq_dir.exists():
            return []
        items = []
        for path in sorted(dlq_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]:
            items.append(json.loads(path.read_text(encoding="utf-8")))
        return items

    @app.get("/api/v1/admin/audit")
    def audit_log(limit: int = Query(default=50, ge=1, le=500)):
        return audit_sink.read(limit=limit)

    def _run_summary(vertex: dict) -> dict:
        props = vertex["properties"]
        counts = {}
        if props.get("counts"):
            try:
                counts = json.loads(props["counts"])
            except (ValueError, TypeError):
                pass
        return {
            "canonical_id": props["canonical_id"],
            "run_kind": props.get("run_kind"),
            "run_status": props.get("run_status"),
            "source_system": props.get("source_system"),
            "started_at": props.get("started_at"),
            "finished_at": props.get("finished_at"),
            "counts": counts,
        }

    @app.get("/api/v1/validation/runs")
    def validation_runs(limit: int = Query(default=100, ge=1, le=500)):
        vertices = store.find_vertices(label="ValidationRun", limit=limit)
        return [_run_summary(v) for v in sorted(
            vertices,
            key=lambda v: v["properties"].get("started_at") or "",
            reverse=True,
        )]

    @app.get("/api/v1/ingestion/runs")
    def ingestion_runs(limit: int = Query(default=100, ge=1, le=500)):
        vertices = store.find_vertices(label="IngestionRun", limit=limit)
        return [_run_summary(v) for v in sorted(
            vertices,
            key=lambda v: v["properties"].get("started_at") or "",
            reverse=True,
        )]

    @app.post("/api/v1/ingestion/jira-json", status_code=202)
    def public_ingest_jira(payload: IngestionRequest, request: Request):
        return queue.submit(
            "JIRA_JSON",
            payload.model_dump(),
            correlation_id=request.state.correlation_id,
        )

    return app
