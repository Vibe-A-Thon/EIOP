"""QueryPlan executor: validates against policy, selects template, runs traversal.

Natural language NEVER produces executable Gremlin; it produces a QueryPlan
validated against schema + policy, then executed via a named bounded template.
"""

from __future__ import annotations

from uuid import uuid4

from eoip.contracts.graph_result import GraphEdge, GraphNode, GraphPath, GraphResult
from eoip.contracts.query_plan import QueryPlan
from eoip.graph.store import GraphStore
from eoip.graph.traversal import GraphTraversal
from eoip.query.policy import DEFAULT_POLICY, QueryPolicy


class QueryExecutor:
    def __init__(self, store: GraphStore, policy: QueryPolicy | None = None) -> None:
        self._store = store
        self._policy = policy or DEFAULT_POLICY

    @property
    def policy(self) -> QueryPolicy:
        return self._policy

    def execute(self, plan: QueryPlan) -> GraphResult:
        violations = self._policy.validate(plan)
        if violations:
            raise PolicyViolation(violations)
        plan = self._policy.clamp(plan)
        handler = _TEMPLATES.get(plan.intent)
        if handler is None:
            raise PolicyViolation([f"No template registered for intent '{plan.intent}'"])
        return handler(self._store, plan)


class PolicyViolation(Exception):
    def __init__(self, violations: list[str]) -> None:
        self.violations = violations
        super().__init__("; ".join(violations))


def _search(store: GraphStore, plan: QueryPlan) -> GraphResult:
    query = plan.anchors[0].strip().casefold()
    candidates = store.find_vertices(limit=5000)
    matches = [
        v
        for v in candidates
        if any(
            query in str(val).casefold()
            for key, val in v["properties"].items()
            if key
            in {
                "canonical_id",
                "name",
                "display_name",
                "summary",
                "issue_key",
                "path",
                "qualified_name",
                "commit_sha",
            }
        )
    ]
    matches.sort(
        key=lambda v: (
            query != str(v["canonical_id"]).casefold(),
            str(v["properties"].get("name", "")).casefold(),
        )
    )
    nodes = [_to_node(v) for v in matches[: plan.result_limit]]
    return GraphResult(
        query_id=str(uuid4()),
        nodes=nodes,
        edges=[],
        partial=len(matches) > plan.result_limit or len(candidates) == 5000,
        evidence=[],
    )


def _path(store: GraphStore, plan: QueryPlan) -> GraphResult:
    if len(plan.anchors) < 2:
        raise PolicyViolation(["PATH intent requires exactly 2 anchors (source, target)"])
    kwargs: dict = {"max_depth": plan.max_depth, "max_results": plan.result_limit}
    if plan.relationship_allowlist:
        kwargs["allowed_edges"] = frozenset(plan.relationship_allowlist)
    traversal = GraphTraversal(store, **kwargs)
    result = traversal.find_path(plan.anchors[0], plan.anchors[1], max_depth=plan.max_depth)
    if result is None:
        return GraphResult(query_id=str(uuid4()), partial=False)
    path_id = str(uuid4())
    return GraphResult(
        query_id=str(uuid4()),
        nodes=[_to_node(v) for v in result["vertices"]],
        edges=[_to_edge(e) for e in result["edges"]],
        paths=[
            GraphPath(
                path_id=path_id,
                node_ids=[v["canonical_id"] for v in result["vertices"]],
                edge_ids=[e["eid"] for e in result["edges"]],
            )
        ],
        evidence=_edge_evidence(result["edges"]),
        partial=False,
    )


def _impact(store: GraphStore, plan: QueryPlan) -> GraphResult:
    kwargs: dict = {"max_depth": plan.max_depth, "max_results": plan.result_limit}
    if plan.relationship_allowlist:
        kwargs["allowed_edges"] = frozenset(plan.relationship_allowlist)
    traversal = GraphTraversal(store, **kwargs)
    result = traversal.impact(plan.anchors[0], max_depth=plan.max_depth)
    if result["source"] is None:
        return GraphResult(query_id=str(uuid4()), partial=False)
    return _traversal_result(result)


def _lineage(store: GraphStore, plan: QueryPlan) -> GraphResult:
    traversal = GraphTraversal(
        store,
        allowed_edges=frozenset({"EVIDENCED_BY", "INGESTED_IN"}),
        max_depth=plan.max_depth,
        max_results=plan.result_limit,
    )
    result = traversal.impact(plan.anchors[0], max_depth=plan.max_depth, direction="outgoing")
    if result["source"] is None:
        return GraphResult(query_id=str(uuid4()), partial=False)
    return _traversal_result(result)


def _neighborhood(store: GraphStore, plan: QueryPlan) -> GraphResult:
    return _impact(store, plan)


def _traceability(store: GraphStore, plan: QueryPlan) -> GraphResult:
    return _impact(store, plan)


_TEMPLATES = {
    "SEARCH": _search,
    "PATH": _path,
    "IMPACT": _impact,
    "LINEAGE": _lineage,
    "NEIGHBORHOOD": _neighborhood,
    "TRACEABILITY": _traceability,
}


def _traversal_result(result: dict) -> GraphResult:
    vertices = {result["source"]["canonical_id"]: result["source"]}
    edges = {}
    paths = []
    for item in result["impacted"]:
        path = item["path"]
        vertices.update({v["canonical_id"]: v for v in path["vertices"]})
        edges.update({e["eid"]: e for e in path["edges"]})
        paths.append(
            GraphPath(
                path_id=str(uuid4()),
                node_ids=[v["canonical_id"] for v in path["vertices"]],
                edge_ids=[e["eid"] for e in path["edges"]],
            )
        )
    return GraphResult(
        query_id=str(uuid4()),
        nodes=[_to_node(v) for v in vertices.values()],
        edges=[_to_edge(e) for e in edges.values()],
        paths=paths,
        evidence=_edge_evidence(list(edges.values())),
        partial=result["truncated"],
    )


def _to_node(vertex: dict) -> GraphNode:
    props = vertex["properties"]
    return GraphNode(
        id=vertex["canonical_id"],
        label=vertex["label"],
        domain=props.get("graph_domain"),
        properties=props,
    )


def _to_edge(edge: dict) -> GraphEdge:
    props = edge["properties"]
    return GraphEdge(
        id=edge["eid"],
        type=edge["label"],
        from_id=edge["out_cid"],
        to_id=edge["in_cid"],
        creation_status=props.get("creation_status"),
        properties=props,
    )


def _edge_evidence(edges: list[dict]) -> list[dict]:
    evidence = []
    for edge in edges:
        props = edge["properties"]
        if props.get("evidence_key") or props.get("source_ref"):
            evidence.append(
                {
                    "edge_id": edge["eid"],
                    "evidence_key": props.get("evidence_key"),
                    "source_ref": props.get("source_ref"),
                    "source_system": props.get("source_system"),
                    "ingestion_run_id": props.get("ingestion_run_id"),
                }
            )
    return evidence
