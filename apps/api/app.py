from __future__ import annotations

from uuid import uuid4

from eoip.contracts.graph_result import GraphEdge, GraphNode, GraphPath, GraphResult
from eoip.graph.store import GraphStore
from eoip.graph.traversal import GraphTraversal
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


def create_app(store: GraphStore, *, max_depth: int = 8, dependencies=None) -> FastAPI:
    app = FastAPI(title="EOIP API", version="1.0.0", dependencies=dependencies or [])
    traversal = GraphTraversal(store, max_depth=max_depth)
    app.state.graph_store = store

    @app.middleware("http")
    async def add_correlation_id(request: Request, call_next):
        supplied = request.headers.get("X-Correlation-ID", "")
        correlation_id = supplied if 0 < len(supplied) <= 128 else str(uuid4())
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response

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
        query = q.strip().casefold()
        if not query:
            raise HTTPException(status_code=422, detail="Search query must not be blank")
        try:
            candidates = store.find_vertices(label=label, limit=5000)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        matches = [
            vertex
            for vertex in candidates
            if any(
                query in str(value).casefold()
                for key, value in vertex["properties"].items()
                if key in {"canonical_id", "name", "display_name", "summary", "issue_key", "path", "qualified_name", "commit_sha"}
            )
        ]
        matches.sort(
            key=lambda vertex: (
                query != str(vertex["canonical_id"]).casefold(),
                str(vertex["properties"].get("name", "")).casefold(),
            )
        )
        nodes = [_to_node(vertex) for vertex in matches[:limit]]
        return GraphResult(query_id=str(uuid4()), nodes=nodes, edges=[], partial=len(matches) > limit or len(candidates) == 5000, evidence=[])

    @app.post("/api/v1/path", response_model=GraphResult)
    def find_path(payload: PathRequest) -> GraphResult:
        try:
            result = traversal.find_path(payload.source_id, payload.target_id, max_depth=payload.max_depth)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        if result is None:
            return GraphResult(query_id=str(uuid4()), partial=False)
        path_id = str(uuid4())
        return GraphResult(
            query_id=str(uuid4()),
            nodes=[_to_node(vertex) for vertex in result["vertices"]],
            edges=[_to_edge(edge) for edge in result["edges"]],
            paths=[
                GraphPath(
                    path_id=path_id,
                    node_ids=[vertex["canonical_id"] for vertex in result["vertices"]],
                    edge_ids=[edge["eid"] for edge in result["edges"]],
                )
            ],
            evidence=_edge_evidence(result["edges"]),
            partial=False,
        )

    @app.post("/api/v1/impact", response_model=GraphResult)
    def impact(payload: ImpactRequest) -> GraphResult:
        limited_traversal = GraphTraversal(
            store,
            max_depth=max_depth,
            max_results=payload.result_limit,
        )
        try:
            result = limited_traversal.impact(payload.canonical_id, max_depth=payload.max_depth)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        if result["source"] is None:
            raise HTTPException(status_code=404, detail="Entity not found")
        vertices = {result["source"]["canonical_id"]: result["source"]}
        edges = {}
        paths = []
        for item in result["impacted"]:
            path = item["path"]
            vertices.update({vertex["canonical_id"]: vertex for vertex in path["vertices"]})
            edges.update({edge["eid"]: edge for edge in path["edges"]})
            paths.append(
                GraphPath(
                    path_id=str(uuid4()),
                    node_ids=[vertex["canonical_id"] for vertex in path["vertices"]],
                    edge_ids=[edge["eid"] for edge in path["edges"]],
                )
            )
        return GraphResult(
            query_id=str(uuid4()),
            nodes=[_to_node(vertex) for vertex in vertices.values()],
            edges=[_to_edge(edge) for edge in edges.values()],
            paths=paths,
            evidence=_edge_evidence(list(edges.values())),
            partial=result["truncated"],
        )

    return app


def _to_node(vertex: dict) -> GraphNode:
    properties = vertex["properties"]
    return GraphNode(
        id=vertex["canonical_id"],
        label=vertex["label"],
        domain=properties.get("graph_domain"),
        properties=properties,
    )


def _to_edge(edge: dict) -> GraphEdge:
    properties = edge["properties"]
    return GraphEdge(
        id=edge["eid"],
        type=edge["label"],
        from_id=edge["out_cid"],
        to_id=edge["in_cid"],
        creation_status=properties.get("creation_status"),
        properties=properties,
    )


def _edge_evidence(edges: list[dict]) -> list[dict]:
    evidence = []
    for edge in edges:
        properties = edge["properties"]
        if properties.get("evidence_key") or properties.get("source_ref"):
            evidence.append(
                {
                    "edge_id": edge["eid"],
                    "evidence_key": properties.get("evidence_key"),
                    "source_ref": properties.get("source_ref"),
                    "source_system": properties.get("source_system"),
                    "ingestion_run_id": properties.get("ingestion_run_id"),
                }
            )
    return evidence
