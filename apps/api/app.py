from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from eoip.config import load_query_policy
from eoip.contracts.graph_result import GraphResult, TraversalGraphResult
from eoip.contracts.query_plan import QueryPlan
from eoip.demo_scenarios import read_demo_scenario_pack
from eoip.graph.metrics import GraphMetricsEngine
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import VERTEX_LABELS
from eoip.query.executor import PolicyViolation, QueryExecutor, QueryTimeout
from eoip.query.nlq import NLQProcessor
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


class KCoreRequest(BaseModel):
    min_k: int = Field(default=1, ge=0, le=100)


class ComponentsRequest(BaseModel):
    limit: int = Field(default=50, ge=1, le=1000)


class WhatIfRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    action: str = Field(default="remove", pattern="^(remove|isolate)$")


class AnomalyRequest(BaseModel):
    algorithms: list[str] = Field(default=["degree_zscore"])
    threshold: float = Field(default=2.0, ge=1.0, le=5.0)


class LinkPredictionRequest(BaseModel):
    canonical_id: str = Field(min_length=1, max_length=512)
    algorithm: str = Field(default="common_neighbors", pattern="^(common_neighbors|jaccard|adamic_adar)$")
    limit: int = Field(default=10, ge=1, le=50)


class SurpriseRequest(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)


class DiffRequest(BaseModel):
    snapshot_a: str = Field(min_length=1, max_length=64)
    snapshot_b: str = Field(min_length=1, max_length=64)


class NLQueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1024)


class GraphMergePayload(BaseModel):
    strategy: str = Field(default="union", pattern="^(union|intersection|diff)$")
    vertices: list[dict] = Field(default_factory=list)
    edges: list[dict] = Field(default_factory=list)


class RAGQueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    pattern: str | None = None
    context: dict = Field(default_factory=dict)


class AgentQueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    agent_type: str | None = None
    context: dict = Field(default_factory=dict)


class EngineeringRequest(BaseModel):
    discipline: str = Field(min_length=1, max_length=100)
    query: str = Field(min_length=1, max_length=2000)
    context: dict = Field(default_factory=dict)


class JsonIngestionRequest(BaseModel):
    data: dict | list = Field(...)
    source_label: str = Field(default="json_upload", max_length=128)
    pipeline_id: str = Field(default="manual", max_length=128)


class FormatConvertRequest(BaseModel):
    format_id: str = Field(
        min_length=1, max_length=32,
        pattern="^(rdf|rdf_xml|rdfs|owl|gremlin|cypher|gql|sparql)$",
    )
    limit: int = Field(default=10000, ge=1, le=50000)


class BatchIngestionRequest(BaseModel):
    files: list[dict] = Field(min_length=1, max_length=50)
    pipeline_id: str = Field(default="batch", max_length=128)


class FirewallInspectRequest(BaseModel):
    content: str = Field(min_length=1, max_length=50_000)
    boundary: str = Field(default="agent_context", max_length=128)
    source_ref: str | None = Field(default=None, max_length=512)
    block_on_restricted: bool = False


class EvidenceManifestRequest(BaseModel):
    answer_id: str = Field(min_length=1, max_length=256)
    node_ids: list[str] = Field(default_factory=list, max_length=100)
    edge_ids: list[str] = Field(default_factory=list, max_length=100)
    evidence_refs: list[str] = Field(default_factory=list, max_length=200)
    query_plan: dict | None = None
    tool_calls: list[dict] = Field(default_factory=list, max_length=100)
    rules_fired: list[dict] = Field(default_factory=list, max_length=100)
    confidence_inputs: list[dict] = Field(default_factory=list, max_length=100)


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

    @app.get("/api/v1/demo/scenarios")
    def demo_scenarios():
        """Return the sales-demo catalog with live graph-readiness state."""
        pack = read_demo_scenario_pack()
        scenarios = []
        for item in pack["scenarios"]:
            path_state = [
                {
                    "canonical_id": canonical_id,
                    "available": store.get_vertex_by_canonical_id(canonical_id) is not None,
                }
                for canonical_id in item["expected_path"]
            ]
            scenarios.append(
                {
                    **item,
                    "available": store.get_vertex_by_canonical_id(item["entrypoint"]) is not None,
                    "expected_path_state": path_state,
                    "ready": all(node["available"] for node in path_state),
                }
            )
        return {
            "dataset_id": pack["dataset_id"],
            "version": pack["version"],
            "title": pack["title"],
            "description": pack.get("description"),
            "ready": all(item["ready"] for item in scenarios),
            "scenarios": scenarios,
        }

    @app.get("/api/v1/search", response_model=GraphResult)
    def search(
        q: str = Query(min_length=1, max_length=256),
        label: str | None = Query(default=None, max_length=64),
        limit: int = Query(default=25, ge=1, le=100),
        include_deleted: bool = Query(default=False),
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
            filters={
                **({"label": label} if label else {}),
                "include_deleted": include_deleted,
            },
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
        nlq_response = NLQProcessor(store, executor).process(payload.question)
        interpretation = nlq_response.interpretation
        if interpretation.plan is None:
            return nlq_response.model_dump()
        if nlq_response.result is not None:
            return nlq_response.model_dump()
        try:
            result = executor.execute(interpretation.plan)
        except PolicyViolation as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return {
            "interpretation": interpretation.model_dump(),
            "result": result,
            "answer": nlq_response.answer,
            "confidence": nlq_response.confidence,
            "engine": nlq_response.engine,
            "highlights": nlq_response.highlights,
            "followups": nlq_response.followups,
            "warnings": nlq_response.warnings,
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

    @app.post("/api/v1/graph/k-core")
    def k_core(payload: KCoreRequest):
        result = metrics_engine.k_core_decomposition()
        if payload.min_k > 0:
            result = {k: v for k, v in result.items() if k >= payload.min_k}
        return {"cores": {str(k): v for k, v in result.items()}, "max_k": max(result.keys()) if result else 0}

    @app.post("/api/v1/graph/components")
    def components(payload: ComponentsRequest):
        result = metrics_engine.connected_components()
        return {
            "components": [{"id": i, "size": len(c), "members": c[:200]} for i, c in enumerate(result[:payload.limit])],
            "total_components": len(result),
        }

    @app.post("/api/v1/graph/degree-distribution")
    def degree_distribution():
        result = metrics_engine.degree_distribution()
        return {"distribution": result, "total_nodes": sum(result.values())}

    @app.post("/api/v1/graph/what-if")
    def what_if(payload: WhatIfRequest):
        from eoip.graph.whatif import WhatIfEngine
        engine = WhatIfEngine(store)
        if payload.action == "isolate":
            result = engine.simulate_isolation(payload.canonical_id)
        else:
            result = engine.simulate_removal(payload.canonical_id)
        return result.to_dict()

    @app.post("/api/v1/graph/anomalies")
    def graph_anomalies(payload: AnomalyRequest):
        from eoip.graph.anomaly import AnomalyDetector
        detector = AnomalyDetector(store)
        results = []
        if "degree_zscore" in payload.algorithms:
            results.extend(detector.degree_zscore_outliers(threshold=payload.threshold))
        if "dense_subgraph" in payload.algorithms:
            results.extend(detector.dense_subgraph_detection())
        if "missing_edges" in payload.algorithms:
            results.extend(detector.missing_expected_edges())
        return [r.to_dict() for r in results]

    @app.post("/api/v1/graph/link-prediction")
    def link_prediction(payload: LinkPredictionRequest):
        from eoip.graph.similarity import SimilarityEngine
        engine = SimilarityEngine(store)
        return engine.link_prediction(
            payload.canonical_id,
            algorithm=payload.algorithm,
            limit=payload.limit,
        )

    @app.post("/api/v1/graph/surprises")
    def graph_surprises(payload: SurpriseRequest):
        from eoip.graph.surprise import SurpriseDetector

        return SurpriseDetector(store).summary(limit=payload.limit)

    @app.get("/api/v1/graph/orphaned")
    def graph_orphaned(
        entity_types: str | None = Query(default=None, max_length=256),
    ):
        from eoip.graph.anomaly import AnomalyDetector
        detector = AnomalyDetector(store)
        types = [t.strip() for t in entity_types.split(",")] if entity_types else None
        results = detector.orphaned_entities(entity_types=types)
        return {"orphaned": [r.to_dict() for r in results], "count": len(results)}

    @app.get("/api/v1/graph/stale")
    def graph_stale(
        threshold_hours: int = Query(default=168, ge=1, le=8760),
    ):
        from eoip.graph.anomaly import AnomalyDetector
        detector = AnomalyDetector(store)
        results = detector.stale_entities(threshold_hours=threshold_hours)
        return {"stale": [r.to_dict() for r in results], "count": len(results), "partial": detector.partial}

    @app.get("/api/v1/graph/pr-impact")
    def graph_pr_impact():
        from eoip.graph.community import CommunityDetectionEngine
        community_engine = CommunityDetectionEngine(store)
        result = community_engine.detect_with_labels()
        community_map = {}
        for comm in result.communities:
            for member in comm["members"]:
                community_map[member] = comm.get("auto_label", f"Community {comm['id']}")

        vertices = store.find_vertices(limit=50_000)
        pr_groups: dict[str, list] = {}
        for v in vertices:
            props = v.get("properties", {})
            mr_id = props.get("merge_request_id") or props.get("pr_id")
            if mr_id:
                pr_groups.setdefault(str(mr_id), []).append(v)

        prs = []
        for mr_id, members in pr_groups.items():
            communities_touched = set()
            for m in members:
                cid = m.get("properties", {}).get("canonical_id", "")
                if cid in community_map:
                    communities_touched.add(community_map[cid])
            prs.append({
                "mr_id": mr_id,
                "title": members[0].get("properties", {}).get("pr_title", f"PR #{mr_id}"),
                "author": members[0].get("properties", {}).get("pr_author", ""),
                "communities_touched": sorted(communities_touched),
                "entities_modified": len(members),
            })

        conflicts = []
        pr_list = list(pr_groups.keys())
        for i, a in enumerate(pr_list):
            comms_a = {community_map.get(m.get("properties", {}).get("canonical_id", ""), "")
                       for m in pr_groups[a]} - {""}
            for b in pr_list[i + 1:]:
                comms_b = {community_map.get(m.get("properties", {}).get("canonical_id", ""), "")
                           for m in pr_groups[b]} - {""}
                overlap = comms_a & comms_b
                if overlap:
                    pct = len(overlap) / max(len(comms_a | comms_b), 1)
                    risk = "HIGH" if pct > 0.5 else "MEDIUM" if pct > 0.2 else "LOW"
                    conflicts.append({
                        "mr_a": a, "mr_b": b,
                        "overlap_communities": sorted(overlap),
                        "overlap_pct": round(pct, 3),
                        "risk": risk,
                    })

        return {"pull_requests": prs, "conflicts": conflicts}

    @app.get("/api/v1/files/{path:path}")
    def get_file(path: str):
        import os
        safe = os.path.normpath(path)
        if safe.startswith("..") or os.path.isabs(safe):
            raise HTTPException(400, "Invalid path")
        try:
            with open(safe, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(512_000)
        except FileNotFoundError:
            raise HTTPException(404, "File not found")
        except OSError:
            raise HTTPException(500, "Could not read file")
        return {"path": safe, "content": content, "lines": content.count("\n") + 1}

    @app.post("/api/v1/graph/diff")
    def graph_diff(payload: DiffRequest):
        vertices = store.find_vertices(limit=50_000)
        added, removed, modified = [], [], []
        for v in vertices:
            props = v.get("properties", {})
            ts = props.get("modified_at") or props.get("created_at", "")
            if ts >= payload.snapshot_b:
                added.append(props.get("canonical_id", v["vid"]))
            elif ts >= payload.snapshot_a:
                modified.append(props.get("canonical_id", v["vid"]))
        return {
            "added_nodes": added,
            "removed_nodes": removed,
            "modified_nodes": modified,
            "snapshot_a": payload.snapshot_a,
            "snapshot_b": payload.snapshot_b,
            "structural_changes": {
                "new_components": 0,
                "broken_paths": 0,
            },
        }

    # -- JSON Ingestion & Format Conversion Endpoints --

    @app.post("/api/v1/admin/ingestion/json")
    def ingest_json(payload: JsonIngestionRequest):
        from eoip.ingestion.json_processor import JsonProcessor
        processor = JsonProcessor(store)
        result = processor.process_json_data(
            payload.data,
            source_label=payload.source_label,
            pipeline_id=payload.pipeline_id,
        )
        return result.to_dict()

    @app.post("/api/v1/admin/ingestion/json/batch")
    def ingest_json_batch(payload: BatchIngestionRequest):
        from eoip.ingestion.json_processor import JsonProcessor
        processor = JsonProcessor(store)
        combined_entities = 0
        combined_relationships = 0
        combined_errors: list = []
        combined_log: list = []
        for i, file_data in enumerate(payload.files):
            data = file_data.get("data") or file_data.get("content")
            label = file_data.get("source_label") or file_data.get("name") or f"batch-{i}"
            if data is None:
                combined_errors.append({"index": i, "error": "Missing data field"})
                continue
            result = processor.process_json_data(
                data, source_label=label, pipeline_id=payload.pipeline_id,
            )
            combined_entities += result.entities_created
            combined_relationships += result.relationships_created
            combined_errors.extend(result.errors)
            combined_log.extend(result.log)
        return {
            "files_processed": len(payload.files),
            "entities_created": combined_entities,
            "relationships_created": combined_relationships,
            "error_count": len(combined_errors),
            "errors": combined_errors[:50],
            "log": combined_log[-100:],
        }

    @app.post("/api/v1/graph/convert")
    def convert_graph(payload: FormatConvertRequest):
        from eoip.graph.format_converter import FormatConverter
        converter = FormatConverter(store)
        content = converter.convert(payload.format_id, limit=payload.limit)
        formats = converter.available_formats()
        fmt = next((f for f in formats if f["id"] == payload.format_id), None)
        return {
            "format": payload.format_id,
            "extension": fmt["ext"] if fmt else ".txt",
            "label": fmt["label"] if fmt else payload.format_id,
            "content": content,
            "content_length": len(content),
        }

    @app.get("/api/v1/graph/formats")
    def available_formats():
        from eoip.graph.format_converter import FormatConverter
        return {"formats": FormatConverter.available_formats()}

    @app.post("/api/v1/admin/ingestion/process-and-convert")
    def process_and_convert(payload: JsonIngestionRequest):
        from eoip.graph.format_converter import FormatConverter
        from eoip.ingestion.json_processor import JsonProcessor
        processor = JsonProcessor(store)
        result = processor.process_json_data(
            payload.data,
            source_label=payload.source_label,
            pipeline_id=payload.pipeline_id,
        )
        converter = FormatConverter(store)
        generated = {}
        for fmt in converter.available_formats():
            try:
                generated[fmt["id"]] = {
                    "label": fmt["label"],
                    "ext": fmt["ext"],
                    "content": converter.convert(fmt["id"], limit=10000),
                }
            except Exception as exc:  # noqa: BLE001 - per-format failure must not abort the others
                generated[fmt["id"]] = {"label": fmt["label"], "error": str(exc)}
        result.formats_generated = list(generated.keys())
        return {
            "ingestion": result.to_dict(),
            "formats": generated,
        }

    # --- G2-P6: Twin Domain APIs ---

    @app.get("/api/v1/twin/test-intelligence/mappings")
    def test_code_mappings():
        from eoip.graph.test_intelligence import map_tests_to_code
        return {"mappings": map_tests_to_code(store)}

    @app.get("/api/v1/twin/test-intelligence/runs")
    def test_run_builds():
        from eoip.graph.test_intelligence import map_test_runs_to_builds
        return {"mappings": map_test_runs_to_builds(store)}

    @app.post("/api/v1/twin/test-intelligence/select")
    def select_tests(body: dict):
        from eoip.graph.test_intelligence import select_tests_for_changes
        changed = body.get("changed_files", [])
        if not changed:
            raise HTTPException(400, "changed_files required")
        return select_tests_for_changes(store, changed)

    @app.post("/api/v1/twin/decisions/ingest")
    def ingest_decision_endpoint(body: dict):
        from eoip.graph.decisions import ingest_decision
        name = body.get("name")
        if not name:
            raise HTTPException(400, "name required")
        return ingest_decision(
            store, name,
            rationale=body.get("rationale", ""),
            status=body.get("status", "Proposed"),
            constraints=body.get("constraints", ""),
            alternatives=body.get("alternatives"),
            linked_entities=body.get("linked_entities"),
        )

    @app.get("/api/v1/twin/decisions/{entity_cid:path}")
    def decisions_for_entity(entity_cid: str):
        from eoip.graph.decisions import find_decisions_for_entity
        return {"decisions": find_decisions_for_entity(store, entity_cid)}

    @app.post("/api/v1/twin/decisions/extract")
    def extract_decisions(body: dict):
        from eoip.graph.decisions import extract_decisions_from_document
        doc_cid = body.get("document_cid")
        if not doc_cid:
            raise HTTPException(400, "document_cid required")
        return {"decisions": extract_decisions_from_document(store, doc_cid)}

    @app.post("/api/v1/twin/business/objectives")
    def create_objective(body: dict):
        from eoip.graph.business_intent import ingest_objective
        name = body.get("name")
        if not name:
            raise HTTPException(400, "name required")
        result = ingest_objective(
            store, name,
            description=body.get("description", ""),
            objective_type=body.get("objective_type", "strategic"),
            priority=body.get("priority", "medium"),
            kpi_target=body.get("kpi_target", ""),
            owner_id=body.get("owner_id", ""),
        )
        return {"objective": result}

    @app.post("/api/v1/twin/business/capabilities")
    def create_capability(body: dict):
        from eoip.graph.business_intent import ingest_capability
        name = body.get("name")
        if not name:
            raise HTTPException(400, "name required")
        return {"capability": ingest_capability(
            store, name,
            description=body.get("description", ""),
            level=body.get("level", 1),
            business_domain=body.get("business_domain", ""),
            owner_id=body.get("owner_id", ""),
            parent_cid=body.get("parent_cid"),
            objective_cid=body.get("objective_cid"),
        )}

    @app.post("/api/v1/twin/business/link")
    def link_entity_to_capability(body: dict):
        from eoip.graph.business_intent import link_to_capability
        entity_cid = body.get("entity_cid")
        capability_cid = body.get("capability_cid")
        if not entity_cid or not capability_cid:
            raise HTTPException(400, "entity_cid and capability_cid required")
        result = link_to_capability(store, entity_cid, capability_cid)
        if not result:
            raise HTTPException(404, "Entity or capability not found")
        return result

    @app.get("/api/v1/twin/business/reverse-impact/{service_cid:path}")
    def business_reverse_impact(service_cid: str):
        from eoip.graph.business_intent import reverse_impact
        return reverse_impact(store, service_cid)

    @app.get("/api/v1/twin/business/chain/{objective_cid:path}")
    def intent_chain(objective_cid: str):
        from eoip.graph.business_intent import intent_to_runtime_chain
        return intent_to_runtime_chain(store, objective_cid)

    @app.get("/api/v1/twin/classify")
    def twin_classify():
        from eoip.graph.twin import classify_facts
        return classify_facts(store)

    @app.get("/api/v1/twin/coverage")
    def twin_coverage():
        from eoip.graph.twin import digital_thread_coverage
        return digital_thread_coverage(store)

    @app.get("/api/v1/twin/missing-links")
    def twin_missing_links():
        from eoip.graph.twin import detect_missing_links
        return detect_missing_links(store)

    # --- G2-P7: Architecture Conformance, Process Mining, Query Operators ---

    @app.post("/api/v1/conformance/check")
    def conformance_check(body: dict):
        from eoip.graph.conformance import check_conformance, parse_rules
        from eoip.graph.rule_catalog import get_rule_set
        dsl = body.get("rules_dsl", "")
        rules_list = body.get("rules", [])
        ruleset = body.get("ruleset", "")
        if ruleset:
            stored = get_rule_set(ruleset)
            if stored is None:
                raise HTTPException(404, f"Rule set not found: {ruleset}")
            dsl = dsl or stored
        if dsl:
            rules = parse_rules(dsl)
        elif rules_list:
            from eoip.graph.conformance import ArchRule, RuleKind
            rules = [ArchRule(
                id=r["id"], kind=RuleKind(r["kind"]),
                source=r["source"], target=r["target"],
                severity=r.get("severity", "ERROR"),
                max_depth=r.get("max_depth", 4),
            ) for r in rules_list]
        else:
            raise HTTPException(400, "rules_dsl, rules, or ruleset required")
        return check_conformance(store, rules)

    @app.get("/api/v1/conformance/rules")
    def conformance_rule_sets():
        from eoip.graph.rule_catalog import list_rule_sets

        return {"rule_sets": list_rule_sets()}

    @app.put("/api/v1/conformance/rules/{name}")
    def save_conformance_rule_set(name: str, body: dict):
        from eoip.graph.rule_catalog import save_rule_set

        try:
            path = save_rule_set(name, body.get("rules_dsl", ""))
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        return {"name": name, "path": str(path), "status": "SAVED"}

    @app.get("/api/v1/experts/{canonical_id:path}")
    def experts_for_component(canonical_id: str):
        """Evidence-ranked candidate experts for a component (GAP-REC-001)."""
        from eoip.graph.expertise import find_experts

        try:
            return find_experts(store, canonical_id)
        except ValueError as exc:
            raise HTTPException(404, str(exc)) from exc

    @app.get("/api/v1/knowledge/freshness")
    def knowledge_freshness(stale_days: int = Query(default=90, ge=1, le=3650)):
        """Stale-documentation detection for human review (GAP-FRESH-001..005)."""
        from eoip.graph.expertise import freshness_report

        return freshness_report(store, stale_days=stale_days)

    @app.get("/api/v1/query/cache/stats")
    def query_cache_stats():
        """Semantic query cache metrics (GAP-CACHE; active only when EOIP_QUERY_CACHE=1)."""
        from eoip.query.cache import SemanticQueryCache, cache_enabled

        if not hasattr(app.state, "query_cache"):
            app.state.query_cache = SemanticQueryCache()
        return {"enabled": cache_enabled(), **app.state.query_cache.stats()}

    @app.get("/api/v1/process/cases")
    def process_cases(source_label: str = "WorkItem"):
        from eoip.graph.process_mining import extract_cases_from_graph
        cases = extract_cases_from_graph(store, source_label=source_label)
        return {"cases": [c.to_dict() for c in cases[:100]], "total": len(cases)}

    @app.get("/api/v1/process/paths")
    def process_paths():
        from eoip.graph.process_mining import discover_process_paths, extract_cases_from_graph
        cases = extract_cases_from_graph(store)
        return discover_process_paths(cases)

    @app.post("/api/v1/process/deviations")
    def process_deviations(body: dict):
        from eoip.graph.process_mining import deviation_report
        designed = body.get("designed_steps")
        return deviation_report(store, designed_steps=designed)

    @app.get("/api/v1/knowledge/debt")
    def knowledge_debt():
        from eoip.graph.knowledge_debt import detect_knowledge_debt
        return detect_knowledge_debt(store)

    @app.post("/api/v1/knowledge/slo")
    def knowledge_slo(body: dict):
        from eoip.graph.knowledge_debt import evaluate_slos, parse_slo_rules
        rules_config = body.get("rules", [])
        if not rules_config:
            raise HTTPException(400, "rules required")
        rules = parse_slo_rules(rules_config)
        return evaluate_slos(store, rules)

    @app.get("/api/v1/query/why/{entity_cid:path}")
    def query_why_endpoint(entity_cid: str):
        from eoip.graph.query_operators import query_why
        return query_why(store, entity_cid)

    @app.post("/api/v1/query/why-not")
    def query_why_not_endpoint(body: dict):
        from eoip.graph.query_operators import query_why_not
        source = body.get("source_cid")
        target = body.get("target_cid")
        if not source or not target:
            raise HTTPException(400, "source_cid and target_cid required")
        return query_why_not(store, source, target)

    @app.get("/api/v1/query/what-changed/{entity_cid:path}")
    def query_what_changed_endpoint(entity_cid: str):
        from eoip.graph.query_operators import query_what_changed
        return query_what_changed(store, entity_cid)

    @app.get("/api/v1/query/context/{entity_cid:path}")
    def query_context_endpoint(entity_cid: str):
        from eoip.graph.query_operators import query_context
        return query_context(store, entity_cid)

    # --- G2-P9: Counterfactual Twin & Causal Intelligence ---

    _sim_workspace: dict = {}

    @app.post("/api/v1/simulation/create")
    def simulation_create(body: dict):
        from eoip.graph.simulation import SimulationWorkspace
        if "workspace" not in _sim_workspace:
            _sim_workspace["workspace"] = SimulationWorkspace(store)
        ws = _sim_workspace["workspace"]
        sim_id = ws.create(description=body.get("description", ""))
        return {"simulation_id": sim_id}

    @app.get("/api/v1/simulation/list")
    def simulation_list():
        if "workspace" not in _sim_workspace:
            return {"simulations": []}
        return {"simulations": _sim_workspace["workspace"].list_simulations()}

    @app.post("/api/v1/simulation/{sim_id}/mutate")
    def simulation_mutate(sim_id: str, body: dict):
        from eoip.graph.simulation import Mutation
        if "workspace" not in _sim_workspace:
            raise HTTPException(404, "No simulation workspace")
        ws = _sim_workspace["workspace"]
        mutations_data = body.get("mutations", [body] if "kind" in body else [])
        if not mutations_data:
            raise HTTPException(400, "mutations required")
        mutations = [Mutation(
            kind=m["kind"], label=m.get("label", ""),
            target_id=m.get("target_id", ""), properties=m.get("properties", {}),
            out_v=m.get("out_v", ""), in_v=m.get("in_v", ""),
        ) for m in mutations_data]
        results = ws.apply_mutations(sim_id, mutations)
        return {"results": results}

    @app.get("/api/v1/simulation/{sim_id}/analyze")
    def simulation_analyze(sim_id: str, analysis_type: str = "impact"):
        if "workspace" not in _sim_workspace:
            raise HTTPException(404, "No simulation workspace")
        return _sim_workspace["workspace"].run_analysis(sim_id, analysis_type)

    @app.get("/api/v1/simulation/{sim_id}/compare")
    def simulation_compare(sim_id: str):
        if "workspace" not in _sim_workspace:
            raise HTTPException(404, "No simulation workspace")
        return _sim_workspace["workspace"].compare(sim_id)

    @app.get("/api/v1/simulation/{sim_id}/manifest")
    def simulation_manifest(sim_id: str):
        if "workspace" not in _sim_workspace:
            raise HTTPException(404, "No simulation workspace")
        manifest = _sim_workspace["workspace"].get_manifest(sim_id)
        if not manifest:
            raise HTTPException(404, "Simulation not found")
        return manifest

    @app.post("/api/v1/whatif/plan")
    def whatif_plan(body: dict):
        from eoip.graph.whatif import confirm_scenario, parse_whatif_intent
        intent = body.get("intent", "")
        if not intent:
            raise HTTPException(400, "intent required")
        plan = parse_whatif_intent(intent)
        return confirm_scenario(plan)

    @app.post("/api/v1/whatif/execute")
    def whatif_execute(body: dict):
        from eoip.graph.whatif import execute_scenario, parse_whatif_intent
        intent = body.get("intent", "")
        if not intent:
            raise HTTPException(400, "intent required")
        plan = parse_whatif_intent(intent)
        plan.confirmed = True
        return execute_scenario(store, plan)

    @app.post("/api/v1/causal/correlations/{entity_cid:path}")
    def causal_correlations(entity_cid: str, body: dict | None = None):
        from eoip.graph.causal import find_temporal_correlations
        window = 24.0
        if body and "time_window_hours" in body:
            window = float(body["time_window_hours"])
        return {"entity": entity_cid, "correlations": find_temporal_correlations(store, entity_cid, window)}

    @app.post("/api/v1/causal/prerequisites")
    def causal_prerequisites(body: dict):
        from eoip.graph.causal import check_causal_prerequisites
        cause = body.get("cause_cid")
        effect = body.get("effect_cid")
        if not cause or not effect:
            raise HTTPException(400, "cause_cid and effect_cid required")
        return check_causal_prerequisites(store, cause, effect)

    @app.post("/api/v1/causal/hypotheses/{incident_cid:path}")
    def causal_hypotheses(incident_cid: str, body: dict | None = None):
        from eoip.graph.causal import generate_hypotheses
        window = 24.0
        if body and "time_window_hours" in body:
            window = float(body["time_window_hours"])
        return generate_hypotheses(store, incident_cid, window)

    # --- G2-P10: Lens Framework, Graph Playback, Production APIs ---

    @app.get("/api/v1/lens/catalog")
    def lens_catalog():
        from eoip.graph.lens import list_lenses
        return {"lenses": list_lenses()}

    @app.post("/api/v1/lens/{lens_id}")
    def lens_view(lens_id: str, body: dict | None = None):
        from eoip.graph.lens import KnowledgeContext, lens_data
        ctx = KnowledgeContext.from_dict(body or {})
        return lens_data(store, lens_id, ctx)

    @app.post("/api/v1/playback/stream")
    def playback_stream(body: dict):
        from eoip.graph.playback import build_event_stream
        root_cid = body.get("root_cid", "")
        if not root_cid:
            raise HTTPException(400, "root_cid required")
        return build_event_stream(store, root_cid, max_depth=body.get("max_depth", 3), max_events=body.get("max_events", 200))

    @app.post("/api/v1/playback/evidence")
    def playback_evidence(body: dict):
        from eoip.graph.playback import build_evidence_panel
        root_cid = body.get("root_cid", "")
        if not root_cid:
            raise HTTPException(400, "root_cid required")
        return build_evidence_panel(store, root_cid)

    @app.post("/api/v1/playback/export")
    def playback_export(body: dict):
        from eoip.graph.playback import export_timeline
        root_cid = body.get("root_cid", "")
        if not root_cid:
            raise HTTPException(400, "root_cid required")
        fmt = body.get("format", "json")
        return export_timeline(store, root_cid, format=fmt)

    @app.get("/api/v1/health/graph")
    def graph_health():
        v_count = store.count_vertices()
        e_count = store.count_edges()
        return {
            "status": "healthy",
            "vertices": v_count,
            "edges": e_count,
            "store_healthy": store.health(),
        }

    @app.get("/api/v1/admin/schema")
    def admin_schema():
        from eoip.ontology.manifest import DOMAINS, EDGE_LABELS, ONTOLOGY_VERSION, VERTEX_LABELS
        return {
            "ontology_version": ONTOLOGY_VERSION,
            "domains": DOMAINS,
            "vertex_types": len(VERTEX_LABELS),
            "edge_types": len(EDGE_LABELS),
            "vertex_labels": list(VERTEX_LABELS.keys()),
            "edge_labels": list(EDGE_LABELS.keys()),
        }

    @app.post("/api/v1/knowledge/firewall/inspect")
    def knowledge_firewall_inspect(payload: FirewallInspectRequest):
        from eoip.agents.firewall import KnowledgeFirewall

        result = KnowledgeFirewall().inspect(
            payload.content,
            boundary=payload.boundary,
            source_ref=payload.source_ref,
            block_on_restricted=payload.block_on_restricted,
        )
        return {
            "content": result.content,
            "blocked": result.blocked,
            "untrusted": result.untrusted,
            "classifications": list(result.classifications),
            "boundary": result.boundary,
            "decisions": [decision.model_dump() for decision in result.decisions],
            "provenance": result.provenance,
        }

    @app.get("/api/v1/knowledge/trust/states")
    def knowledge_trust_states():
        from eoip.provenance.trust import TrustState

        return {
            "states": [state.value for state in TrustState],
            "minimum_query_filter": "Use trust_state >= requested threshold; REJECTED never passes.",
        }

    @app.post("/api/v1/evidence/manifest")
    def evidence_manifest(payload: EvidenceManifestRequest):
        from eoip.provenance.evidence import EvidenceService

        manifest = EvidenceService(store).build_manifest(
            answer_id=payload.answer_id,
            node_ids=payload.node_ids,
            edge_ids=payload.edge_ids,
            evidence_refs=payload.evidence_refs,
            query_plan=payload.query_plan,
            tool_calls=payload.tool_calls,
            rules_fired=payload.rules_fired,
            confidence_inputs=payload.confidence_inputs,
        )
        return manifest.to_dict()

    @app.get("/api/v1/gaps/coverage")
    def gaps_coverage(
        status: str | None = Query(default=None, pattern="^(done|partial|planned)$"),
        priority: str | None = Query(default=None, pattern="^P[0-9]+$"),
        include_requirements: bool = Query(default=True),
    ):
        from eoip.gaps.coverage import build_gap_coverage_report

        repo_root = Path(__file__).resolve().parents[2]
        report = build_gap_coverage_report(repo_root).to_dict()
        requirements = report["requirements"]
        if status:
            requirements = [item for item in requirements if item["status"] == status]
        if priority:
            requirements = [item for item in requirements if item["priority"] == priority]
        report["filtered_total"] = len(requirements)
        report["requirements"] = requirements if include_requirements else []
        return report

    @app.get("/api/v1/gaps/requirements/{requirement_id}")
    def gap_requirement(requirement_id: str):
        from eoip.gaps.coverage import build_gap_coverage_report

        normalized = requirement_id.upper()
        repo_root = Path(__file__).resolve().parents[2]
        for item in build_gap_coverage_report(repo_root).to_dict()["requirements"]:
            if item["requirement_id"] == normalized:
                return item
        raise HTTPException(status_code=404, detail="GAP requirement not found")

    # --- EQL: EOIP Query Language ---

    @app.post("/api/v1/query/eql")
    def eql_query(body: dict):
        from eoip.query.eql import parse_and_execute
        q = body.get("query", "")
        if not q:
            raise HTTPException(400, "query required")
        return parse_and_execute(store, q)

    # --- Source & Pipeline Management (query-mode) ---

    @app.get("/api/v1/connectors/catalog")
    def connectors_catalog():
        return {"connectors": [
            {"id": "jira", "name": "Jira", "type": "api", "capabilities": ["baseline", "poll", "webhook"]},
            {"id": "gitlab", "name": "GitLab", "type": "api", "capabilities": ["baseline", "poll", "webhook"]},
            {"id": "github", "name": "GitHub", "type": "api", "capabilities": ["baseline", "poll", "webhook"]},
            {"id": "confluence", "name": "Confluence", "type": "api", "capabilities": ["baseline", "poll"]},
            {"id": "servicenow", "name": "ServiceNow", "type": "api", "capabilities": ["baseline", "poll"]},
            {"id": "rally", "name": "Rally", "type": "api", "capabilities": ["baseline", "poll"]},
            {"id": "grafana", "name": "Grafana", "type": "api", "capabilities": ["baseline", "poll"]},
            {"id": "datadog", "name": "Datadog", "type": "api", "capabilities": ["baseline", "poll"]},
            {"id": "kibana", "name": "Kibana", "type": "api", "capabilities": ["baseline", "poll"]},
            {"id": "qtest", "name": "qTest", "type": "api", "capabilities": ["baseline", "poll"]},
            {"id": "figma", "name": "Figma", "type": "api", "capabilities": ["baseline", "poll"]},
            {"id": "api_portal", "name": "API Portal", "type": "api", "capabilities": ["baseline"]},
            {"id": "web", "name": "Web Crawler", "type": "crawler", "capabilities": ["baseline", "poll", "reconcile"]},
            {"id": "local_code", "name": "Local Code", "type": "file", "capabilities": ["baseline"]},
            {"id": "generic", "name": "Generic JSON", "type": "json", "capabilities": ["baseline"]},
        ]}

    # --- Phase 12: Cross-project graph merge ---
    @app.post("/api/v1/graph/merge")
    def graph_merge(payload: GraphMergePayload):
        added_v = 0
        added_e = 0
        skipped = 0
        for v in payload.vertices:
            label = v.get("label", "Unknown")
            props = v.get("properties", {})
            cid = props.get("canonical_id")
            if not cid:
                skipped += 1
                continue
            if payload.strategy == "intersection":
                existing = store.find_vertices(limit=1, label=label)
                if not any(ev["properties"].get("canonical_id") == cid for ev in existing):
                    skipped += 1
                    continue
            store.upsert_vertex(label, props)
            added_v += 1
        for e in payload.edges:
            elabel = e.get("label", "RELATED_TO")
            src = e.get("from_id") or e.get("source_id")
            tgt = e.get("to_id") or e.get("target_id")
            if not src or not tgt:
                skipped += 1
                continue
            store.upsert_edge(elabel, src, tgt, e.get("properties", {}))
            added_e += 1
        return {"added_vertices": added_v, "added_edges": added_e, "skipped": skipped, "strategy": payload.strategy}

    # --- Phase 13: RAG query endpoint ---
    @app.post("/api/v1/rag/query")
    def rag_query(payload: RAGQueryRequest):
        from eoip.graph.rag_router import RAGRouter
        router = RAGRouter(store)
        return router.route(payload.query, pattern=payload.pattern, context=payload.context)

    @app.get("/api/v1/rag/patterns")
    def rag_patterns():
        from eoip.graph.rag_router import RAG_PATTERNS
        return {"patterns": [{"name": p.name, "description": p.description} for p in RAG_PATTERNS]}

    # --- Phase 13: Agent query endpoint ---
    @app.post("/api/v1/agents/query")
    def agents_query(payload: AgentQueryRequest):
        from eoip.graph.agent_router import AgentRouter
        router = AgentRouter(store)
        return router.route(payload.query, agent_type=payload.agent_type, context=payload.context)

    @app.get("/api/v1/agents/types")
    def agents_types():
        from eoip.graph.agent_router import AGENT_TYPES
        return {"types": [{"name": a.name, "category": a.category, "description": a.description} for a in AGENT_TYPES]}

    # --- Phase 13: Engineering discipline endpoints ---
    @app.post("/api/v1/engineering/{discipline}")
    def engineering_execute(discipline: str, payload: EngineeringRequest):
        from eoip.graph.engineering import EngineeringRouter
        router = EngineeringRouter(store)
        return router.execute(discipline, payload.query, context=payload.context)

    @app.get("/api/v1/pipeline/status")
    def pipeline_status():
        v_count = store.count_vertices()
        e_count = store.count_edges()
        from eoip.ontology.manifest import VERTEX_LABELS as VL
        label_counts = {}
        for lbl in VL:
            c = store.count_vertices(label=lbl)
            if c > 0:
                label_counts[lbl] = c
        return {
            "status": "operational",
            "graph": {"vertices": v_count, "edges": e_count},
            "entity_breakdown": label_counts,
            "domains_active": len({VL[lbl][0] for lbl in label_counts}),
        }

    return app
