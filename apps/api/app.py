from __future__ import annotations

from uuid import uuid4

from eoip.config import load_query_policy
from eoip.contracts.graph_result import GraphResult, TraversalGraphResult
from eoip.contracts.query_plan import QueryPlan
from eoip.graph.metrics import GraphMetricsEngine
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import VERTEX_LABELS
from eoip.query.executor import PolicyViolation, QueryExecutor, QueryTimeout
from eoip.query.nl import interpret
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


class BlastRadiusRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    max_depth: int = Field(default=4, ge=1, le=8)


class MetricsRequest(BaseModel):
    canonical_ids: list[str] = Field(min_length=1, max_length=50)


class FullCentralityRequest(BaseModel):
    canonical_ids: list[str] = Field(min_length=1, max_length=50)
    algorithms: list[str] = Field(default=["degree", "betweenness", "closeness", "pagerank", "eigenvector", "katz", "hits", "harmonic"])


class ClusterRequest(BaseModel):
    resolution: float = Field(default=1.0, ge=0.1, le=10.0)
    algorithm: str = Field(default="label_propagation", pattern="^(label_propagation|louvain|leiden)$")
    limit: int = Field(default=1000, ge=1, le=50000)


class ShortestPathsRequest(BaseModel):
    source_id: str = Field(min_length=1, max_length=512)
    target_id: str = Field(min_length=1, max_length=512)
    max_paths: int = Field(default=5, ge=1, le=20)
    max_length: int = Field(default=10, ge=2, le=20)


class SimilarityRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    algorithm: str = Field(default="jaccard", pattern="^(jaccard|adamic_adar|common_neighbors)$")
    limit: int = Field(default=10, ge=1, le=50)


class WhatIfRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    action: str = Field(default="remove", pattern="^(remove|isolate)$")


class AnomalyRequest(BaseModel):
    algorithms: list[str] = Field(default=["degree_zscore"])
    threshold: float = Field(default=2.0, ge=1.0, le=5.0)


class NLQueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1024)


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
        if label is not None and label not in VERTEX_LABELS:
            raise HTTPException(status_code=422, detail="Unknown vertex label")
        plan = QueryPlan(
            intent="SEARCH",
            anchors=[query],
            max_depth=1,
            result_limit=limit,
            evidence_mode="NONE",
            filters={"label": label} if label else None,
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

    @app.post("/api/v1/impact", response_model=TraversalGraphResult)
    def impact(payload: ImpactRequest) -> TraversalGraphResult:
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

    @app.post("/api/v1/query/nl")
    def query_nl(payload: NLQueryRequest):
        interpretation = interpret(payload.question, store=store)
        if interpretation.plan is None:
            return {"interpretation": interpretation.model_dump(), "result": None}
        try:
            result = executor.execute(interpretation.plan)
        except PolicyViolation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return {
            "interpretation": interpretation.model_dump(),
            "result": result,
        }

    metrics_engine = GraphMetricsEngine(store)

    @app.post("/api/v1/graph/blast-radius")
    def blast_radius(payload: BlastRadiusRequest):
        result = metrics_engine.blast_radius(payload.canonical_id, payload.max_depth)
        if result.total_affected == 0 and not store.get_vertex_by_canonical_id(payload.canonical_id):
            raise HTTPException(404, "Entity not found")
        return result.to_dict()

    @app.post("/api/v1/graph/reverse-impact")
    def reverse_impact(payload: BlastRadiusRequest):
        result = metrics_engine.reverse_impact(payload.canonical_id, payload.max_depth)
        if result.total_affected == 0 and not store.get_vertex_by_canonical_id(payload.canonical_id):
            raise HTTPException(404, "Entity not found")
        return result.to_dict()

    @app.post("/api/v1/graph/metrics")
    def graph_metrics(payload: MetricsRequest):
        results = metrics_engine.centrality(payload.canonical_ids)
        return {cid: m.to_dict() for cid, m in results.items()}

    @app.get("/api/v1/graph/schema")
    def graph_schema():
        return metrics_engine.graph_schema()

    @app.get("/api/v1/graph/statistics")
    def graph_statistics():
        return metrics_engine.graph_statistics()

    @app.post("/api/v1/graph/centrality/full")
    def full_centrality(payload: FullCentralityRequest):
        results = metrics_engine.full_centrality(payload.canonical_ids, payload.algorithms)
        return {cid: m.to_dict() for cid, m in results.items()}

    @app.post("/api/v1/graph/cluster")
    def graph_cluster(payload: ClusterRequest):
        from eoip.graph.community import CommunityDetectionEngine
        community_engine = CommunityDetectionEngine(store)
        if payload.algorithm == "louvain":
            result = community_engine.louvain(resolution=payload.resolution)
        elif payload.algorithm == "leiden":
            result = community_engine.leiden(resolution=payload.resolution)
        else:
            result = community_engine.label_propagation()
        return result.to_dict()

    @app.post("/api/v1/graph/shortest-paths")
    def shortest_paths(payload: ShortestPathsRequest):
        from eoip.graph.paths import GraphPathFinder
        finder = GraphPathFinder(store)
        paths = finder.all_shortest_paths(
            payload.source_id, payload.target_id, max_paths=payload.max_paths
        )
        return {"paths": paths, "count": len(paths)}

    @app.post("/api/v1/graph/similarity")
    def graph_similarity(payload: SimilarityRequest):
        from eoip.graph.similarity import SimilarityEngine
        engine = SimilarityEngine(store)
        if payload.algorithm == "adamic_adar":
            results = engine.adamic_adar(payload.canonical_id, limit=payload.limit)
        elif payload.algorithm == "common_neighbors":
            results = engine.common_neighbors(payload.canonical_id, limit=payload.limit)
        else:
            results = engine.jaccard(payload.canonical_id, limit=payload.limit)
        return [r.to_dict() for r in results]

    @app.post("/api/v1/graph/what-if")
    def what_if(payload: WhatIfRequest):
        root = store.get_vertex_by_canonical_id(payload.canonical_id)
        if root is None:
            raise HTTPException(404, "Entity not found")
        out_edges = store.edges_from(root["vid"])
        in_edges = store.edges_to(root["vid"])
        neighbors = set()
        for edge in out_edges:
            v = store.get_vertex(edge["in_v"])
            if v:
                neighbors.add(v["properties"]["canonical_id"])
        for edge in in_edges:
            v = store.get_vertex(edge["out_v"])
            if v:
                neighbors.add(v["properties"]["canonical_id"])
        orphaned = 0
        for cid in neighbors:
            v = store.get_vertex_by_canonical_id(cid)
            if v:
                other_out = [e for e in store.edges_from(v["vid"]) if e["in_v"] != root["vid"]]
                other_in = [e for e in store.edges_to(v["vid"]) if e["out_v"] != root["vid"]]
                if not other_out and not other_in:
                    orphaned += 1
        return {
            "canonical_id": payload.canonical_id,
            "action": payload.action,
            "broken_edges": len(out_edges) + len(in_edges),
            "affected_neighbors": len(neighbors),
            "orphaned_entities": orphaned,
        }

    @app.post("/api/v1/graph/anomalies")
    def graph_anomalies(payload: AnomalyRequest):
        from eoip.graph.anomaly import AnomalyDetector
        detector = AnomalyDetector(store)
        results = []
        if "degree_zscore" in payload.algorithms:
            results.extend(detector.degree_zscore_outliers(threshold=payload.threshold))
        return [r.to_dict() for r in results]

    return app
