from __future__ import annotations

from uuid import uuid4

from eoip.config import load_query_policy
from eoip.contracts.graph_result import GraphResult
from eoip.contracts.query_plan import QueryPlan
from eoip.graph.store import GraphStore
from eoip.query.executor import PolicyViolation, QueryExecutor, QueryTimeout
from fastapi import FastAPI, HTTPException, Query, Request, Response
from pydantic import BaseModel, Field


class PathRequest(BaseModel):
    source_id: str = Field(min_length=1, max_length=512)
    target_id: str = Field(min_length=1, max_length=512)
    max_depth: int = Field(default=8, ge=1, le=8)


class ImpactRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    max_depth: int = Field(default=4, ge=1, le=8)
    result_limit: int = Field(default=100, ge=1, le=500)


class LineageRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    max_depth: int = Field(default=4, ge=1, le=8)
    result_limit: int = Field(default=100, ge=1, le=500)


class NeighborhoodRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    max_depth: int = Field(default=1, ge=1, le=4)
    result_limit: int = Field(default=50, ge=1, le=500)


class TraceabilityRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    max_depth: int = Field(default=6, ge=1, le=8)
    result_limit: int = Field(default=100, ge=1, le=500)


def create_app(store: GraphStore, *, max_depth: int = 8, dependencies=None) -> FastAPI:
    app = FastAPI(title="EOIP API", version="1.0.0", dependencies=dependencies or [])
    executor = QueryExecutor(store, load_query_policy())
    app.state.graph_store = store

    @app.middleware("http")
    async def add_correlation_id(request: Request, call_next):
        supplied = request.headers.get("X-Correlation-ID", "")
        correlation_id = getattr(request.state, "correlation_id", None) or (
            supplied if 0 < len(supplied) <= 128 else str(uuid4())
        )
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response

    @app.exception_handler(QueryTimeout)
    async def handle_query_timeout(request, exc):
        return Response(
            content='{"detail":"' + str(exc) + '"}',
            status_code=504,
            media_type="application/json",
        )

    @app.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready")
    def ready(response: Response) -> dict[str, str]:
        if not store.health():
            response.status_code = 503
            return {"status": "not_ready"}
        return {"status": "ready"}

    @app.get("/api/v1/search", response_model=GraphResult)
    def search(
        q: str = Query(min_length=1, max_length=256),
        label: str | None = Query(default=None, max_length=64),
        limit: int = Query(default=25, ge=1, le=100),
    ) -> GraphResult:
        query = q.strip()
        if not query:
            raise HTTPException(status_code=422, detail="Search query must not be blank")
        plan = QueryPlan(
            intent="SEARCH",
            anchors=[query],
            max_depth=1,
            result_limit=limit,
            evidence_mode="NONE",
            label_filter=label,
        )
        try:
            return executor.execute(plan)
        except PolicyViolation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/v1/path", response_model=GraphResult)
    def find_path(payload: PathRequest) -> GraphResult:
        plan = QueryPlan(
            intent="PATH",
            anchors=[payload.source_id, payload.target_id],
            max_depth=payload.max_depth,
            result_limit=100,
            evidence_mode="SUMMARY",
        )
        try:
            return executor.execute(plan)
        except PolicyViolation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/v1/impact", response_model=GraphResult)
    def impact(payload: ImpactRequest) -> GraphResult:
        plan = QueryPlan(
            intent="IMPACT",
            anchors=[payload.canonical_id],
            max_depth=payload.max_depth,
            result_limit=payload.result_limit,
            evidence_mode="SUMMARY",
        )
        try:
            result = executor.execute(plan)
        except PolicyViolation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        if not result.nodes:
            raise HTTPException(status_code=404, detail="Entity not found")
        return result

    @app.post("/api/v1/lineage", response_model=GraphResult)
    def lineage(payload: LineageRequest) -> GraphResult:
        plan = QueryPlan(
            intent="LINEAGE",
            anchors=[payload.canonical_id],
            max_depth=payload.max_depth,
            result_limit=payload.result_limit,
            evidence_mode="SUMMARY",
        )
        try:
            result = executor.execute(plan)
        except PolicyViolation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        if not result.nodes:
            raise HTTPException(status_code=404, detail="Entity not found")
        return result

    @app.post("/api/v1/neighborhood", response_model=GraphResult)
    def neighborhood(payload: NeighborhoodRequest) -> GraphResult:
        plan = QueryPlan(
            intent="NEIGHBORHOOD",
            anchors=[payload.canonical_id],
            max_depth=payload.max_depth,
            result_limit=payload.result_limit,
            evidence_mode="SUMMARY",
        )
        try:
            result = executor.execute(plan)
        except PolicyViolation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        if not result.nodes:
            raise HTTPException(status_code=404, detail="Entity not found")
        return result

    @app.post("/api/v1/traceability", response_model=GraphResult)
    def traceability(payload: TraceabilityRequest) -> GraphResult:
        plan = QueryPlan(
            intent="TRACEABILITY",
            anchors=[payload.canonical_id],
            max_depth=payload.max_depth,
            result_limit=payload.result_limit,
            evidence_mode="FULL",
        )
        try:
            result = executor.execute(plan)
        except PolicyViolation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        if not result.nodes:
            raise HTTPException(status_code=404, detail="Entity not found")
        return result

    @app.post("/api/v1/query", response_model=GraphResult)
    def query_plan(payload: QueryPlan) -> GraphResult:
        try:
            return executor.execute(payload)
        except PolicyViolation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app
