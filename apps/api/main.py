"""Uvicorn factory for the persistent deployment."""

import hashlib
import hmac
import json
import logging
import os
import re
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from time import perf_counter
from uuid import uuid4

import httpx
from eoip.agents.catalog import build_agent_registry
from eoip.agents.memory import MAX_TTL_SECONDS, FileMemoryStore, MemoryStorageError
from eoip.agents.runtime import AgentRuntime
from eoip.audit.sink import AuditSink
from eoip.config import load_agent_config, load_memory_policy
from eoip.connectors.acquisition import AcquisitionPolicy, AcquisitionScheduler
from eoip.connectors.base import DiscoveryScope
from eoip.connectors.config import connector_from_registry
from eoip.connectors.errors import ConnectorError
from eoip.connectors.registry import (
    SourceAlreadyExistsError,
    SourceNotFoundError,
    SourceRegistry,
)
from eoip.connectors.webhook import WebhookGateway
from eoip.contracts.agent import AgentRequest
from eoip.contracts.audit import AuditEvent
from eoip.contracts.source_event import SourceEvent, SourceEventV2
from eoip.contracts.source_registry import SourceCapabilities, SourceRegistryEntry, SourceType
from eoip.events.emitter import GraphEventEmitter
from eoip.graph.evolution import ChangeJournal, GraphEvolutionEngine
from eoip.jobs import JobQueue, write_json
from eoip.models.provider import LocalModelProvider
from eoip.observability import configure_json_logging
from eoip.ontology.manifest import VERTEX_LABELS
from eoip.ontology.rdf import export_jsonld
from eoip.runtime import api_token, create_store, data_root
from eoip.validation.engine import ValidationEngine
from fastapi import Depends, HTTPException, Query, Request, WebSocket, WebSocketDisconnect
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
    if path.startswith("/api/v1/agents/"):
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
        "/api/v1/query/nl",
        "/api/v1/path",
        "/api/v1/impact",
        "/api/v1/lineage",
        "/api/v1/neighborhood",
        "/api/v1/traceability",
        "/api/v1/ontology/export",
        "/api/v1/ontology/diff",
        "/api/v1/knowledge/freshness",
        "/api/v1/query/cache/stats",
        "/api/v1/graph/blast-radius",
        "/api/v1/graph/reverse-impact",
        "/api/v1/graph/metrics",
        "/api/v1/graph/schema",
        "/api/v1/graph/statistics",
        "/api/v1/change-journal",
        "/api/v1/demo/scenarios",
    } or path.startswith(("/api/v1/entities/", "/api/v1/graph/", "/api/v1/capsules", "/api/v1/experts/")):
        return "query"
    if path.startswith(("/api/v1/admin/", "/api/v1/sources", "/api/v1/identity/")):
        return "admin"
    return "other"


def _safe_path(path: str) -> str:
    if path.startswith("/api/v1/entities/"):
        return "/api/v1/entities/{canonical_id:path}"
    if path.startswith("/api/v1/admin/entities/"):
        return "/api/v1/admin/entities/{canonical_id:path}/delete"
    if path.startswith("/api/v1/admin/jobs/"):
        return "/api/v1/admin/jobs/{job_id}"
    return path


class IngestionRequest(BaseModel):
    document: dict | list
    dry_run: bool = False


class GitLabIngestionRequest(IngestionRequest):
    repository_id: str = Field(
        default="demo",
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._/-]*$",
    )


class IncrementalSyncRequest(BaseModel):
    checkpoint: str | None = Field(default=None, max_length=128)
    watermark: str | None = Field(default=None, max_length=128)
    dry_run: bool = False


class ReplayRequest(BaseModel):
    source_system: str = Field(pattern=r"^(jira|gitlab|git)$")
    event_ids: list[str] = Field(default_factory=list, max_length=1000)
    repository_id: str = Field(
        default="demo",
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._/-]*$",
    )
    dry_run: bool = False


class TraceRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    max_depth: int = Field(default=4, ge=1, le=8)


class AgentRunRequest(BaseModel):
    goal: str = Field(min_length=1, max_length=4096)
    context_refs: list[str] = Field(default_factory=list, max_length=100)
    budgets: dict = Field(default_factory=dict)
    dry_run: bool = False
    synthesize: bool = False
    memory_ttl_seconds: int | None = Field(default=None, ge=1, le=MAX_TTL_SECONDS, strict=True)


class ProposalDecisionRequest(BaseModel):
    actor_id: str = Field(min_length=1, max_length=256)


class RetrievalRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    question: str = Field(
        default="Explain the implementation and its evidence", min_length=1, max_length=2048
    )
    synthesize: bool = False


class SourceRegistryPatch(BaseModel):
    source_type: SourceType | None = None
    name: str | None = Field(default=None, min_length=1, max_length=256)
    base_url: str | None = Field(default=None, max_length=2048)
    acquisition_modes: list[str] | None = Field(default=None, max_length=16)
    allowed_scopes: list[str] | None = Field(default=None, max_length=1000)
    excluded_scopes: list[str] | None = Field(default=None, max_length=1000)
    polling_frequency_seconds: int | None = Field(default=None, ge=1, le=31_536_000)
    webhook_status: str | None = Field(default=None, max_length=32)
    mapping_version: str | None = Field(default=None, max_length=128)
    parser_version: str | None = Field(default=None, max_length=128)
    checkpoint: str | None = Field(default=None, max_length=4096)
    last_successful_baseline: str | None = Field(default=None, max_length=64)
    last_incremental_run: str | None = Field(default=None, max_length=64)
    reconciliation_schedule: str | None = Field(default=None, max_length=256)
    health: str | None = Field(default=None, max_length=32)
    freshness_slo_seconds: int | None = Field(default=None, ge=1, le=31_536_000)
    compatibility: dict | None = None
    enabled: bool | None = None
    capabilities: SourceCapabilities | None = None
    config: dict | None = None
    secret_refs: dict[str, str] | None = None


class SourceOperationRequest(BaseModel):
    checkpoint: str | None = Field(default=None, max_length=4096)
    event_ids: list[str] = Field(default_factory=list, max_length=1000)
    dry_run: bool = False


class CapsuleRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    root_entities: list[str] = Field(min_length=1, max_length=100)
    max_depth: int = Field(default=2, ge=1, le=6)
    domains: list[str] | None = None
    trust_threshold: str | None = Field(default=None, max_length=32)
    include_evidence: bool = True
    result_limit: int = Field(default=200, ge=1, le=1000)


def create_app():
    configure_json_logging()
    token = api_token()
    store = create_store()
    queue = JobQueue(data_root())
    source_registry = SourceRegistry(data_root() / "state" / "source-registry.json")
    acquisition_scheduler = AcquisitionScheduler(data_root(), source_registry, queue)
    webhook_gateway = WebhookGateway(data_root())
    change_journal = ChangeJournal(data_root() / "journal" / "semantic-changes.ndjson")
    evolution = GraphEvolutionEngine(store, change_journal)
    audit_sink = AuditSink(data_root() / "audit")
    validator = ValidationEngine(store)
    agent_registry = build_agent_registry(load_agent_config("trace-impact"))
    agent_runtime = AgentRuntime(
        store, agent_registry,
        memory_store=FileMemoryStore(data_root(), policy=load_memory_policy()),
    )
    event_emitter = GraphEventEmitter(buffer_size=1000)
    app = query_app(store, dependencies=[Depends(HTTPBearer(auto_error=False))])
    app.state.event_emitter = event_emitter
    from apps.api.extended import ensure_extended

    ensure_extended(app, store)
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
        terminal_statuses = {"SUCCEEDED", "PARTIAL", "FAILED", "CANCELLED"}
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
                denied = status_code in {401, 403, 413, 422}
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

        webhook_request = re.fullmatch(r"/api/v1/sources/[A-Za-z0-9][A-Za-z0-9._-]*/webhooks", request.url.path)
        if request.url.path not in {
            "/health/live",
            "/health/ready",
            "/metrics",
            "/docs",
            "/openapi.json",
            "/docs/oauth2-redirect",
        } and webhook_request is None:
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
        high_risk_admin = request.url.path.startswith(
            ("/api/v1/admin/", "/api/v1/sources")
        ) and request.method in {"POST", "PUT", "PATCH", "DELETE"}
        if high_risk_admin:
            try:
                audit_sink.emit(
                    AuditEvent(
                        audit_id=str(uuid4()),
                        event_type="admin_intent",
                        actor="local-user",
                        correlation_id=correlation_id,
                        outcome="authorized",
                        safe_summary="Authorized admin mutation accepted for execution",
                    ),
                    operation=operation,
                    path=request.url.path,
                )
            except Exception as exc:  # noqa: BLE001 - audit availability is a policy boundary
                status = "503"
                requests.labels(request.method, status).inc()
                operations.labels(operation, status).inc()
                failures.labels(operation, status).inc()
                operation_duration.labels(operation).observe(perf_counter() - started)
                log.error(
                    "audit.preflight_failed",
                    extra={
                        "event": "audit.preflight_failed",
                        "operation": operation,
                        "correlation_id": correlation_id,
                        "audit_id": request.state.audit_id,
                        "method": request.method,
                        "path": _safe_path(request.url.path),
                        "status_code": 503,
                        "error_type": type(exc).__name__,
                    },
                )
                response = JSONResponse(
                    {"detail": "Audit service unavailable; admin mutation was not executed"},
                    status_code=503,
                )
                response.headers["X-Correlation-ID"] = correlation_id
                response.headers["X-Audit-ID"] = request.state.audit_id
                return response
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
    def entity(canonical_id: str, include_deleted: bool = Query(default=False)):
        result = store.get_vertex_by_canonical_id(canonical_id)
        if result is None or (result["properties"].get("deleted_at") and not include_deleted):
            raise HTTPException(404, "Entity not found")
        return {
            "entity": result,
            "outgoing": store.edges_from(result["vid"]),
            "incoming": store.edges_to(result["vid"]),
        }

    @app.post("/api/v1/admin/entities/{canonical_id:path}/delete")
    def delete_entity(canonical_id: str):
        entity = store.get_vertex_by_canonical_id(canonical_id)
        if entity is None:
            raise HTTPException(404, "Entity not found")
        if entity["properties"].get("deleted_at"):
            return {
                "canonical_id": canonical_id,
                "status": "ALREADY_DELETED",
                "deleted_at": entity["properties"]["deleted_at"],
            }
        if not store.tombstone_vertex(canonical_id):
            raise HTTPException(409, "Entity could not be tombstoned")
        deleted = store.get_vertex_by_canonical_id(canonical_id)
        return {
            "canonical_id": canonical_id,
            "status": "DELETED",
            "deleted_at": deleted["properties"]["deleted_at"],
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

    @app.get("/api/v1/admin/event-consumers")
    def event_consumers():
        root = data_root() / "state" / "event-consumers"
        if not root.exists():
            return []
        return [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(root.glob("*.json"))
        ]

    @app.post("/api/v1/admin/event-consumers/run")
    def run_event_consumers():
        """Run semantic event consumers on demand (they normally run in the worker)."""
        from eoip.graph.consumers import run_default_consumers

        try:
            return run_default_consumers(store, data_root())
        except (OSError, ValueError, RuntimeError) as exc:
            raise HTTPException(500, f"Consumer run failed: {exc}") from exc

    @app.get("/api/v1/admin/timeline")
    def admin_timeline(limit: int = Query(default=100, ge=1, le=500)):
        path = data_root() / "state" / "admin-timeline.json"
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8")).get("events", [])[-limit:]

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

    @app.get("/api/v1/graph/versions")
    def graph_versions(limit: int = Query(default=100, ge=1, le=1000)):
        return evolution.versions(limit=limit)

    @app.get("/api/v1/graph/as-of")
    def graph_as_of(at: str = Query(min_length=1, max_length=64), limit: int = Query(default=500, ge=1, le=5000)):
        try:
            datetime.fromisoformat(at)
            return evolution.as_of(at, limit=limit)
        except ValueError as exc:
            raise HTTPException(422, "at must be an ISO-8601 timestamp") from exc

    @app.get("/api/v1/graph/diff")
    def graph_diff(
        from_at: str = Query(alias="from", min_length=1, max_length=64),
        to_at: str = Query(alias="to", min_length=1, max_length=64),
        limit: int = Query(default=500, ge=1, le=5000),
    ):
        try:
            datetime.fromisoformat(from_at)
            datetime.fromisoformat(to_at)
            return evolution.diff(from_at, to_at, limit=limit)
        except ValueError as exc:
            raise HTTPException(422, "from and to must be ISO-8601 timestamps") from exc

    @app.get("/api/v1/change-journal")
    def semantic_change_journal(
        after: int = Query(default=0, ge=0), limit: int = Query(default=100, ge=1, le=1000)
    ):
        return [event.model_dump() for event in change_journal.read(after=after, limit=limit)]

    @app.post("/api/v1/capsules", status_code=201)
    def build_capsule(payload: CapsuleRequest):
        """Build a reproducible bounded knowledge capsule (G2-CAP-001..006)."""
        from eoip.graph.capsules import CapsuleDefinition, KnowledgeCapsuleService

        service = KnowledgeCapsuleService(store, data_root() / "capsules")
        try:
            capsule = service.build(
                CapsuleDefinition(
                    name=payload.name,
                    root_entities=tuple(payload.root_entities),
                    max_depth=payload.max_depth,
                    domains=tuple(payload.domains) if payload.domains else None,
                    trust_threshold=payload.trust_threshold,
                    include_evidence=payload.include_evidence,
                    result_limit=payload.result_limit,
                )
            )
        except ValueError as exc:
            raise HTTPException(404, str(exc)) from exc
        return {
            "capsule_id": capsule.capsule_id,
            "manifest": capsule.manifest,
            "entities": capsule.entities,
            "relationships": capsule.relationships,
            "evidence_refs": capsule.evidence_refs,
            "truncated": capsule.truncated,
        }

    @app.get("/api/v1/capsules")
    def list_capsules():
        from eoip.graph.capsules import KnowledgeCapsuleService

        return KnowledgeCapsuleService(store, data_root() / "capsules").list_manifests()

    @app.get("/api/v1/capsules/{name}")
    def get_capsule(name: str):
        from eoip.graph.capsules import KnowledgeCapsuleService

        document = KnowledgeCapsuleService(store, data_root() / "capsules").get_manifest(name)
        if document is None:
            raise HTTPException(404, "Capsule not found")
        return document

    @app.post("/api/v1/sources", response_model=SourceRegistryEntry, status_code=201)
    def create_source(entry: SourceRegistryEntry):
        try:
            return source_registry.create(entry)
        except SourceAlreadyExistsError as exc:
            raise HTTPException(409, "Source already exists") from exc

    @app.get("/api/v1/sources", response_model=list[SourceRegistryEntry])
    def list_sources():
        return source_registry.list()

    @app.get("/api/v1/sources/{source_id}", response_model=SourceRegistryEntry)
    def get_source(source_id: str):
        try:
            return source_registry.get(source_id)
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc

    @app.patch("/api/v1/sources/{source_id}", response_model=SourceRegistryEntry)
    def update_source(source_id: str, patch: SourceRegistryPatch):
        changes = patch.model_dump(exclude_unset=True)
        if not changes:
            raise HTTPException(422, "At least one source field is required")
        try:
            return source_registry.update(source_id, changes)
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.delete("/api/v1/sources/{source_id}", status_code=204)
    def delete_source(source_id: str):
        try:
            source_registry.delete(source_id)
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc
        return Response(status_code=204)

    def submit_source_operation(
        source_id: str,
        operation: str,
        payload: SourceOperationRequest,
        request: Request,
    ):
        try:
            return acquisition_scheduler.submit(
                source_id,
                operation,
                checkpoint=payload.checkpoint,
                event_ids=payload.event_ids,
                dry_run=payload.dry_run,
                correlation_id=request.state.correlation_id,
            )
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(409, str(exc)) from exc

    @app.post("/api/v1/sources/{source_id}/baseline", status_code=202)
    def baseline_source(source_id: str, payload: SourceOperationRequest, request: Request):
        return submit_source_operation(source_id, "BASELINE", payload, request)

    @app.post("/api/v1/sources/{source_id}/discover")
    def discover_source(source_id: str, request: Request, scope: DiscoveryScope | None = None):
        try:
            entry = source_registry.get(source_id)
            if not entry.enabled or not entry.capabilities.discovery:
                raise HTTPException(409, "Source discovery capability is not enabled")
            connector = connector_from_registry(
                entry,
                correlation_id=getattr(getattr(request, "state", None), "correlation_id", None),
            )
            try:
                return connector.discover(scope or DiscoveryScope()).model_dump(mode="json")
            finally:
                close = getattr(connector, "close", None)
                if callable(close):
                    close()
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc
        except ConnectorError as exc:
            raise HTTPException(503, f"Connector discovery unavailable: {exc.category}") from exc
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.post("/api/v1/sources/{source_id}/dry-run", status_code=202)
    def dry_run_source(source_id: str, payload: SourceOperationRequest, request: Request):
        return submit_source_operation(
            source_id,
            "POLL" if payload.checkpoint else "BASELINE",
            payload.model_copy(update={"dry_run": True}),
            request,
        )

    @app.post("/api/v1/sources/{source_id}/sync", status_code=202)
    def sync_source(source_id: str, payload: SourceOperationRequest, request: Request):
        return submit_source_operation(source_id, "POLL", payload, request)

    @app.post("/api/v1/sources/{source_id}/reconcile", status_code=202)
    def reconcile_source(source_id: str, payload: SourceOperationRequest, request: Request):
        return submit_source_operation(source_id, "RECONCILE", payload, request)

    @app.get("/api/v1/sources/{source_id}/reconciliations")
    def reconciliation_runs(source_id: str, limit: int = Query(default=50, ge=1, le=500)):
        try:
            source_registry.get(source_id)
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc
        root = data_root() / "state" / "reconciliation" / source_id
        if not root.exists():
            return []
        paths = sorted(root.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True)
        return [json.loads(path.read_text(encoding="utf-8")) for path in paths[:limit]]

    @app.get("/api/v1/sources/{source_id}/checkpoint")
    def source_checkpoint(source_id: str):
        try:
            source = source_registry.get(source_id)
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc
        checkpoint_file = data_root() / "state" / "connectors" / f"{source_id}.json"
        state = json.loads(checkpoint_file.read_text(encoding="utf-8")) if checkpoint_file.exists() else {}
        return {
            "source_id": source_id,
            "registry_checkpoint": source.checkpoint,
            "baseline_complete": bool(source.last_successful_baseline or state.get("baseline_complete")),
            "state": state,
        }

    @app.post("/api/v1/sources/{source_id}/replay", status_code=202)
    def replay_source(source_id: str, payload: SourceOperationRequest, request: Request):
        return submit_source_operation(source_id, "REPLAY", payload, request)

    @app.get("/api/v1/sources/{source_id}/schedule", response_model=AcquisitionPolicy)
    def source_schedule(source_id: str):
        try:
            return acquisition_scheduler.policy(source_id)
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc

    @app.put("/api/v1/sources/{source_id}/schedule", response_model=AcquisitionPolicy)
    def update_source_schedule(source_id: str, policy: AcquisitionPolicy):
        try:
            return acquisition_scheduler.set_policy(source_id, policy)
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc

    @app.post("/api/v1/sources/{source_id}/pause", response_model=AcquisitionPolicy)
    def pause_source(source_id: str):
        try:
            return acquisition_scheduler.pause(source_id)
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc

    @app.post("/api/v1/sources/{source_id}/resume", response_model=AcquisitionPolicy)
    def resume_source(source_id: str):
        try:
            return acquisition_scheduler.resume(source_id)
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc

    @app.post("/api/v1/sources/{source_id}/webhooks", status_code=202)
    async def receive_source_webhook(source_id: str, request: Request):
        try:
            source = source_registry.get(source_id)
        except SourceNotFoundError as exc:
            raise HTTPException(404, "Source not found") from exc
        if not source.enabled or not source.capabilities.webhooks:
            raise HTTPException(409, "Source webhook capability is not enabled")
        if source.source_type not in {"jira", "gitlab", "github"}:
            raise HTTPException(422, "No webhook mapper is available for this source type")
        gitlab_standard = source.source_type == "gitlab" and bool(
            request.headers.get("webhook-signature")
        )
        secret_name = "webhook_signing" if gitlab_standard else "webhook_hmac"
        secret_ref = source.secret_refs.get(secret_name)
        if not secret_ref or not secret_ref.startswith("env://"):
            raise HTTPException(409, f"An env:// {secret_name} secret reference is required")
        secret = os.getenv(secret_ref.removeprefix("env://"), "")
        if not secret:
            raise HTTPException(503, "Webhook verification secret is unavailable")
        try:
            receipt = webhook_gateway.receive(
                source_id,
                await request.body(),
                signature=(
                    request.headers.get("webhook-signature", "")
                    if gitlab_standard
                    else request.headers.get("X-Gitlab-Token", "")
                    if source.source_type == "gitlab"
                    else request.headers.get("X-EOIP-Signature")
                    or request.headers.get("X-Hub-Signature-256", "")
                ),
                secret=secret,
                delivery_id=(
                    request.headers.get("webhook-id")
                    or request.headers.get("Idempotency-Key")
                    or request.headers.get("X-EOIP-Delivery")
                    or request.headers.get("X-GitHub-Delivery")
                ),
                metadata={
                    "event_name": request.headers.get("X-GitHub-Event")
                    or request.headers.get("X-Gitlab-Event")
                },
                verification=(
                    "standard_webhooks"
                    if gitlab_standard
                    else "plain_token"
                    if source.source_type == "gitlab"
                    else "sha256"
                ),
                timestamp=request.headers.get("webhook-timestamp"),
            )
        except PermissionError as exc:
            raise HTTPException(401, "Invalid webhook signature") from exc
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise HTTPException(422, str(exc)) from exc
        if receipt.duplicate:
            return receipt
        queued = queue.submit(
            "SOURCE_WEBHOOK",
            {
                "source_id": source_id,
                "delivery_id": receipt.delivery_id,
                "receipt_ref": receipt.payload_ref,
            },
            correlation_id=request.state.correlation_id,
        )
        return {**receipt.model_dump(), "job_id": queued["job_id"]}

    @app.get("/api/v1/admin/jobs/{job_id}")
    def job(job_id: str):
        try:
            result = queue.get(job_id)
            return {k: v for k, v in result.items() if k != "payload"}
        except (ValueError, FileNotFoundError):
            raise HTTPException(404, "Job not found")

    @app.post("/api/v1/admin/jobs/{job_id}/cancel")
    def cancel_job(job_id: str):
        try:
            return queue.cancel(job_id)
        except (ValueError, FileNotFoundError):
            raise HTTPException(404, "Job not found")
        except RuntimeError as exc:
            raise HTTPException(409, str(exc)) from exc

    def readmit_webhook_job(job_id: str, held: dict, correlation_id: str) -> dict:
        payload = held.get("payload")
        if not isinstance(payload, dict):
            raise TypeError("webhook recovery job payload is required")
        source_id = payload.get("source_id")
        delivery_id = payload.get("delivery_id")
        receipt_ref = payload.get("receipt_ref")
        if not all(isinstance(value, str) and value for value in (source_id, delivery_id, receipt_ref)):
            raise TypeError("webhook recovery requires source_id, delivery_id and receipt_ref")
        source = source_registry.get(source_id)
        if not source.enabled or not source.capabilities.webhooks:
            raise RuntimeError("source webhook capability is not enabled")
        if source.source_type not in {"jira", "gitlab", "github"}:
            raise ValueError("No webhook mapper is available for this source type")

        receipt_dir = (data_root() / "receipts" / source_id).resolve()
        original = Path(receipt_ref)
        if original.suffix != ".json":
            raise ValueError("webhook receipt reference must be a JSON file")
        safe_delivery = hashlib.sha256(delivery_id.encode("utf-8")).hexdigest()
        receipt_path = (receipt_dir / f"{safe_delivery}.json").resolve()
        if receipt_path.parent != receipt_dir or original.name != receipt_path.name:
            raise ValueError("webhook receipt reference does not match delivery id")
        receipt_document = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt = receipt_document.get("receipt")
        if (
            not isinstance(receipt, dict)
            or receipt.get("source_id") != source_id
            or receipt.get("delivery_id") != delivery_id
            or not isinstance(receipt_document.get("payload"), dict)
            or not isinstance(receipt_document.get("metadata", {}), dict)
        ):
            raise ValueError("webhook receipt does not match held job")

        receipt_document["receipt"] = {**receipt, "payload_ref": str(receipt_path)}
        write_json(receipt_path, receipt_document)
        write_json(
            queue.root / f"{job_id}.json",
            {**held, "payload": {**payload, "receipt_ref": str(receipt_path)}},
        )
        return queue.readmit(job_id, correlation_id=correlation_id)

    @app.post("/api/v1/admin/jobs/{job_id}/readmit", status_code=202)
    def readmit_job(job_id: str, request: Request):
        try:
            held = queue.get(job_id)
        except (ValueError, FileNotFoundError):
            raise HTTPException(404, "Job not found") from None
        try:
            if held["kind"] == "SOURCE_OPERATION":
                return acquisition_scheduler.readmit(
                    job_id, correlation_id=request.state.correlation_id
                )
            if held["kind"] == "SOURCE_WEBHOOK":
                return readmit_webhook_job(
                    job_id, held, correlation_id=request.state.correlation_id
                )
            if held["kind"] not in {
                "DEMO", "JIRA_JSON", "GITLAB_JSON", "REPLAY", "CONFLUENCE", "SERVICENOW",
            }:
                raise RuntimeError("Job kind cannot be re-admitted")
            return queue.readmit(job_id, correlation_id=request.state.correlation_id)
        except (SourceNotFoundError, FileNotFoundError):
            raise HTTPException(404, "Job or source not found") from None
        except (ValueError, TypeError) as exc:
            raise HTTPException(422, str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(409, str(exc)) from exc

    @app.post("/api/v1/admin/ingestion/jira", status_code=202)
    def ingest(payload: IngestionRequest, request: Request):
        return queue.submit(
            "JIRA_JSON",
            payload.model_dump(),
            correlation_id=request.state.correlation_id,
        )

    @app.post("/api/v1/admin/ingestion/gitlab", status_code=202)
    def ingest_gitlab(payload: GitLabIngestionRequest, request: Request):
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

    @app.post("/api/v1/admin/gremlin")
    def admin_gremlin(payload: dict, request: Request):
        if not os.getenv("EOIP_ADMIN_GREMLIN_ENABLED", "").lower() in ("1", "true", "yes"):
            raise HTTPException(
                403,
                "Raw Gremlin endpoint is disabled by policy. "
                "Set EOIP_ADMIN_GREMLIN_ENABLED=true to enable.",
            )
        gremlin = payload.get("gremlin", "")
        if not isinstance(gremlin, str) or not gremlin.strip():
            raise HTTPException(422, "A non-empty 'gremlin' string is required")
        bindings = payload.get("bindings", {})
        if not isinstance(bindings, dict):
            raise HTTPException(422, "'bindings' must be a JSON object")
        try:
            result = store.execute_gremlin(gremlin, bindings)
        except AttributeError:
            raise HTTPException(501, "Underlying graph store does not support raw Gremlin execution")
        except Exception as exc:
            raise HTTPException(400, f"Gremlin execution error: {exc}")
        return {"result": result}

    @app.get("/api/v1/agents")
    def list_agents():
        return {"agents": [contract.model_dump() for contract in agent_registry.list_contracts()]}

    @app.post("/api/v1/agents/{agent_id}/runs")
    def run_agent(agent_id: str, payload: AgentRunRequest, request: Request):
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{1,127}", agent_id):
            raise HTTPException(404, "Agent not found")
        if (
            payload.memory_ttl_seconds is not None
            and payload.memory_ttl_seconds > agent_runtime.memory_store.policy.ttl_seconds
        ):
            raise HTTPException(422, "Task memory TTL exceeds the configured maximum")
        result = agent_runtime.run(AgentRequest(
            request_id=str(uuid4()),
            agent_id=agent_id,
            goal=payload.goal,
            context_refs=payload.context_refs,
            budgets=payload.budgets,
            actor_id="local-user",
            correlation_id=request.state.correlation_id,
            dry_run=payload.dry_run,
            metadata={
                "synthesize": payload.synthesize,
                **({"memory_ttl_seconds": payload.memory_ttl_seconds}
                   if payload.memory_ttl_seconds is not None else {}),
            },
        ))
        if result.status == "DENIED" and result.summary.startswith("Unknown agent"):
            raise HTTPException(404, "Agent not found")
        return result.model_dump()

    @app.get("/api/v1/agents/runs/{run_id}")
    def get_agent_run(run_id: str):
        result = agent_runtime.get_result(run_id)
        trace = agent_runtime.trace_store.get(run_id)
        if result is None and trace is None:
            raise HTTPException(404, "Agent run not found")
        return {
            "result": result.model_dump() if result else None,
            "trace": trace.model_dump() if trace else None,
        }

    @app.get("/api/v1/agents/runs/{run_id}/memory")
    def get_agent_memory(run_id: str):
        try:
            memory = agent_runtime.get_memory(run_id)
        except MemoryStorageError as exc:
            raise HTTPException(503, "Task memory storage is unavailable") from exc
        if memory is None:
            raise HTTPException(404, "Agent task memory not found")
        return memory.model_dump()

    @app.get("/api/v1/agents/runs/{run_id}/explanation")
    def explain_agent_run(run_id: str):
        result = agent_runtime.get_result(run_id)
        if result and result.explanation:
            return result.explanation.model_dump()
        trace = agent_runtime.trace_store.get(run_id)
        if trace:
            for event in reversed(trace.events):
                if event.phase == "EXPLAIN" and event.metadata.get("explanation"):
                    return event.metadata["explanation"]
        raise HTTPException(404, "Agent explanation not found")

    @app.get("/api/v1/agents/proposals")
    def list_agent_proposals(status: str | None = None):
        if status and status not in {"PENDING", "APPROVED", "REJECTED", "EXPIRED"}:
            raise HTTPException(422, "Invalid proposal status")
        return {"proposals": [
            item.model_dump() for item in agent_runtime.proposal_store.list(status=status)
        ]}

    @app.post("/api/v1/agents/proposals/{proposal_id}/approve")
    def approve_agent_proposal(proposal_id: str, payload: ProposalDecisionRequest):
        try:
            return agent_runtime.proposal_store.decide(
                proposal_id, actor_id=payload.actor_id, approve=True
            ).model_dump()
        except KeyError as exc:
            raise HTTPException(404, "Proposal not found") from exc
        except ValueError as exc:
            raise HTTPException(409, str(exc)) from exc

    @app.post("/api/v1/agents/proposals/{proposal_id}/reject")
    def reject_agent_proposal(proposal_id: str, payload: ProposalDecisionRequest):
        try:
            return agent_runtime.proposal_store.decide(
                proposal_id, actor_id=payload.actor_id, approve=False
            ).model_dump()
        except KeyError as exc:
            raise HTTPException(404, "Proposal not found") from exc
        except ValueError as exc:
            raise HTTPException(409, str(exc)) from exc

    @app.get("/api/v1/ontology/drift")
    def ontology_drift():
        """Read-only scan for graph vocabulary missing from the ontology manifest."""
        from eoip.ontology.drift import detect_ontology_drift

        return detect_ontology_drift(store).to_dict()

    @app.post("/api/v1/ontology/diff")
    def ontology_diff(body: dict):
        """Semantic diff between two manifest snapshots (GAP-GITOPS-003).

        Body: {"old": <snapshot>|"current", "new": <snapshot>|"current"}.
        Returns the classified changes and a CI publish verdict.
        """
        from eoip.ontology.gitops import current_manifest_snapshot, validate_ontology_change

        def resolve(value) -> dict:
            if value in (None, "current"):
                return current_manifest_snapshot()
            if isinstance(value, dict):
                return value
            raise HTTPException(422, "manifest snapshots must be objects or 'current'")

        return validate_ontology_change(resolve(body.get("old")), resolve(body.get("new")))

    @app.get("/api/v1/identity/candidates")
    def list_identity_candidates(status: str | None = None):
        from eoip.identity.candidates import IdentityCandidateStore

        store_q = IdentityCandidateStore(data_root() / "state" / "identity-candidates.json")
        if status and status not in {"PENDING", "CONFIRMED", "REJECTED"}:
            raise HTTPException(422, "Invalid candidate status")
        return {"candidates": [item.to_dict() for item in store_q.list(status=status)]}

    @app.post("/api/v1/identity/candidates/{candidate_id}/decide")
    def decide_identity_candidate(candidate_id: str, payload: ProposalDecisionRequest):
        """Human review decision for an identity-merge candidate (GAP-ER-005/010)."""
        from eoip.identity.candidates import IdentityCandidateStore

        store_q = IdentityCandidateStore(data_root() / "state" / "identity-candidates.json")
        try:
            candidate = store_q.decide(candidate_id, approve=True, reviewer=payload.actor_id)
        except KeyError as exc:
            raise HTTPException(404, "Candidate not found") from exc
        except ValueError as exc:
            raise HTTPException(409, str(exc)) from exc
        return candidate.to_dict()

    @app.post("/api/v1/identity/candidates/{candidate_id}/reject")
    def reject_identity_candidate(candidate_id: str, payload: ProposalDecisionRequest):
        from eoip.identity.candidates import IdentityCandidateStore

        store_q = IdentityCandidateStore(data_root() / "state" / "identity-candidates.json")
        try:
            candidate = store_q.decide(candidate_id, approve=False, reviewer=payload.actor_id)
        except KeyError as exc:
            raise HTTPException(404, "Candidate not found") from exc
        except ValueError as exc:
            raise HTTPException(409, str(exc)) from exc
        return candidate.to_dict()

    @app.post("/api/v1/ontology/proposals", status_code=201)
    def generate_ontology_proposals():
        """Turn drift findings into governed, human-reviewable evolution proposals (G2-OEVO)."""
        from uuid import uuid4

        from eoip.contracts.agent import ChangeProposal
        from eoip.contracts.source_event import utc_now_iso
        from eoip.ontology.drift import build_evolution_proposal, detect_ontology_drift

        report = detect_ontology_drift(store)
        created = []
        existing = {
            proposal.target_ref for proposal in agent_runtime.proposal_store.list(status="PENDING")
        }
        for finding in report.findings:
            target = f"{finding.kind}:{finding.value}"
            if target in existing:
                continue
            payload = build_evolution_proposal(finding)
            proposal = ChangeProposal(
                proposal_id=str(uuid4()),
                run_id="ontology-drift-detector",
                proposed_by="OntologyDriftDetector",
                operation=payload["proposal_type"],
                target_ref=target,
                patch=payload["evidence"],
                rationale=f"{payload['summary']} — {payload['impact_analysis']}",
                evidence_refs=[f"{finding.kind}:{finding.value}"],
                risk_level="R2",
                created_at=utc_now_iso(),
            )
            agent_runtime.proposal_store.create(proposal)
            created.append(proposal.model_dump())
        return {"created": len(created), "proposals": created, "drift": report.to_dict()}

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
            "agent_id": "TraceImpact",
            "run_id": result.run_id,
            "status": result.status,
            "summary": result.summary,
            "evidence_refs": result.evidence_refs,
            "tool_calls": result.tool_calls,
            "explanation": result.explanation.model_dump() if result.explanation else None,
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

    @app.get("/api/v1/ingestion/dlq")
    def ingestion_dlq_list(limit: int = Query(default=50, ge=1, le=500)):
        return dlq_list(limit=limit)

    @app.post("/api/v1/admin/dlq/{event_id}/replay", status_code=202)
    def replay_dlq(event_id: str, request: Request):
        if not re.fullmatch(r"[a-f0-9]{64}", event_id):
            raise HTTPException(404, "Dead-letter record not found")
        record_path = data_root() / "dlq" / f"{event_id}.json"
        if not record_path.exists():
            raise HTTPException(404, "Dead-letter record not found")
        record = json.loads(record_path.read_text(encoding="utf-8"))
        source_system = record.get("source_system")
        if source_system not in {"jira", "gitlab", "git", "github", "confluence", "servicenow"}:
            raise HTTPException(422, "This dead-letter source does not support replay")
        raw_path = data_root() / "raw" / source_system / f"{event_id}.json"
        if not raw_path.exists():
            raise HTTPException(409, "Captured source event is unavailable")
        event_document = json.loads(raw_path.read_text(encoding="utf-8"))
        event_model = SourceEventV2 if event_document.get("schema_version") == "2.0" else SourceEvent
        source_event = event_model.model_validate(event_document)
        if source_event.event_id != event_id or source_event.payload_hash != record.get("payload_hash"):
            raise HTTPException(409, "Captured source event does not match the dead-letter record")
        if source_event.source_system != source_system:
            raise HTTPException(409, "Captured source event source does not match the dead-letter record")
        if isinstance(source_event, SourceEventV2):
            source_id = record.get("registry_source_id") or source_event.source_instance_id
            try:
                entry = source_registry.get(source_id)
            except SourceNotFoundError as exc:
                raise HTTPException(409, "Registered replay source is unavailable") from exc
            if entry.source_type != source_system:
                raise HTTPException(409, "Registered replay source type does not match the event")
            return submit_source_operation(
                source_id,
                "REPLAY",
                SourceOperationRequest(event_ids=[event_id], dry_run=False),
                request,
            )
        if source_system == "gitlab":
            record_kind = (source_event.metadata or {}).get("record_kind")
            if record_kind not in {"merge_request", "pipeline"}:
                raise HTTPException(409, "Captured GitLab event has no supported record kind")
        payload = {
            "source_system": source_system,
            "event_ids": [event_id],
            "dry_run": False,
            "repository_id": record.get("repository_id", "demo"),
        }
        return queue.submit("REPLAY", payload, correlation_id=request.state.correlation_id)

    @app.post("/api/v1/admin/ingestion/replay", status_code=202)
    def replay_ingestion(payload: ReplayRequest, request: Request):
        invalid = [event_id for event_id in payload.event_ids if not re.fullmatch(r"[a-f0-9]{64}", event_id)]
        if invalid:
            raise HTTPException(422, "Replay event IDs must be lowercase SHA-256 values")
        return queue.submit(
            "REPLAY",
            payload.model_dump(),
            correlation_id=request.state.correlation_id,
        )

    @app.post("/api/v1/ingestion/replay", status_code=202)
    def replay_ingestion_alias(payload: ReplayRequest, request: Request):
        return replay_ingestion(payload, request)

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

    @app.websocket("/ws/graph/events")
    async def graph_events(websocket: WebSocket):
        await websocket.accept()
        queue_ws = event_emitter.subscribe()
        try:
            while True:
                event = await queue_ws.get()
                await websocket.send_json(event.to_dict())
        except WebSocketDisconnect:
            pass
        finally:
            event_emitter.unsubscribe(queue_ws)

    @app.get("/api/v1/graph/events")
    def poll_events(
        since: str = Query(default="", max_length=64),
        since_id: int = Query(default=0, ge=0),
        limit: int = Query(default=100, ge=1, le=1000),
    ):
        if since_id > 0:
            return {"events": event_emitter.events_since_id(since_id, limit=limit)}
        if since:
            return {"events": event_emitter.events_since(since, limit=limit)}
        return {"events": event_emitter.recent_events(limit=limit)}

    return app
