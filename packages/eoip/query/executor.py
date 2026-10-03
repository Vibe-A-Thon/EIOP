"""QueryPlan executor: validates against policy, selects template, runs traversal.

Natural language NEVER produces executable Gremlin; it produces a QueryPlan
validated against schema + policy, then executed via a named bounded template.
"""

from __future__ import annotations

import concurrent.futures
import re
from uuid import uuid4

from eoip.contracts.graph_result import GraphEdge, GraphNode, GraphPath, GraphResult, TraversalGraphResult
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
        timeout_s = plan.timeout_ms / 1000.0
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(handler, self._store, plan)
            try:
                return future.result(timeout=timeout_s)
            except concurrent.futures.TimeoutError:
                raise QueryTimeout(plan.timeout_ms)


class PolicyViolation(Exception):
    def __init__(self, violations: list[str]) -> None:
        self.violations = violations
        super().__init__("; ".join(violations))


class QueryTimeout(Exception):
    def __init__(self, timeout_ms: int) -> None:
        self.timeout_ms = timeout_ms
        super().__init__(f"Query exceeded {timeout_ms}ms timeout")


_SEARCHABLE_PROPS = {
    "canonical_id",
    "name",
    "display_name",
    "summary",
    "issue_key",
    "path",
    "qualified_name",
    "commit_sha",
}

_ISSUE_KEY_EXACT = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")
_SHA_EXACT = re.compile(r"^[0-9a-f]{40}$")
# Index-backed exact lookups tried before the general substring scan
# (mirror the SECONDARY indexes declared in the ontology manifest).
_EXACT_PROPERTY_LOOKUPS = (
    ("WorkItem", "issue_key"),
    ("Commit", "commit_sha"),
    ("CodeSymbol", "qualified_name"),
)


def _search(store: GraphStore, plan: QueryPlan) -> GraphResult:
    raw_query = plan.anchors[0].strip()
    filters = dict(plan.filters or {})
    label = filters.pop("label", None)
    if (
        len(raw_query) < 2
        and not _ISSUE_KEY_EXACT.fullmatch(raw_query)
        and not _SHA_EXACT.fullmatch(raw_query)
    ):
        raise PolicyViolation(
            [
                (
                    "Search query must be at least 2 characters "
                    "(exact issue keys and commit SHAs remain allowed)"
                )
            ]
        )
    exact = _exact_matches(store, raw_query, label)
    seen = {v["canonical_id"] for v in exact}
    query = raw_query.casefold()
    candidates = store.find_vertices(label=label, filters=filters or None, limit=5000)
    matches = [
        v
        for v in candidates
        if v["canonical_id"] not in seen
        and any(
            query in str(val).casefold()
            for key, val in v["properties"].items()
            if key in _SEARCHABLE_PROPS
        )
    ]
    matches.sort(
        key=lambda v: (
            query != str(v["canonical_id"]).casefold(),
            str(v["properties"].get("name", "")).casefold(),
        )
    )
    combined = exact + matches
    nodes = [_to_node(v) for v in combined[: plan.result_limit]]
    return GraphResult(
        query_id=str(uuid4()),
        nodes=nodes,
        edges=[],
        partial=len(combined) > plan.result_limit or len(candidates) == 5000,
        evidence=[],
    )


def _exact_matches(store: GraphStore, raw_query: str, label: str | None) -> list[dict]:
    found: list[dict] = []
    seen: set[str] = set()
    for item_label, key in _EXACT_PROPERTY_LOOKUPS:
        if label is not None and label != item_label:
            continue
        for vertex in store.find_vertex_by_property(item_label, key, raw_query):
            if vertex["canonical_id"] not in seen and not vertex["properties"].get("deleted_at"):
                seen.add(vertex["canonical_id"])
                found.append(vertex)
    if "/" in raw_query and label in (None, "File"):
        for vertex in store.find_vertices(label="File", filters={"path": raw_query}, limit=10):
            if vertex["canonical_id"] not in seen and not vertex["properties"].get("deleted_at"):
                seen.add(vertex["canonical_id"])
                found.append(vertex)
    return found


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
    kwargs: dict = {"max_depth": 1, "max_results": plan.result_limit}
    if plan.relationship_allowlist:
        kwargs["allowed_edges"] = frozenset(plan.relationship_allowlist)
    traversal = GraphTraversal(store, **kwargs)
    result = traversal.impact(plan.anchors[0], max_depth=1)
    if result["source"] is None:
        return GraphResult(query_id=str(uuid4()), partial=False)
    return _traversal_result(result)


def _traceability(store: GraphStore, plan: QueryPlan) -> GraphResult:
    traversal = GraphTraversal(
        store,
        allowed_edges=frozenset({"IMPLEMENTS", "REFERENCES", "DOCUMENTS"}),
        max_depth=plan.max_depth,
        max_results=plan.result_limit,
    )
    result = traversal.impact(plan.anchors[0], max_depth=plan.max_depth)
    if result["source"] is None:
        return GraphResult(query_id=str(uuid4()), partial=False)
    return _traversal_result(result)


_TEMPLATES = {
    "SEARCH": _search,
    "PATH": _path,
    "IMPACT": _impact,
    "LINEAGE": _lineage,
    "NEIGHBORHOOD": _neighborhood,
    "TRACEABILITY": _traceability,
}


def _traversal_result(result: dict) -> TraversalGraphResult:
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
    rationale = {
        item["vertex"]["canonical_id"]: item["rationale"]
        for item in result["impacted"]
        if item.get("rationale")
    }
    return TraversalGraphResult(
        query_id=str(uuid4()),
        nodes=[_to_node(v) for v in vertices.values()],
        edges=[_to_edge(e) for e in edges.values()],
        paths=paths,
        evidence=_edge_evidence(list(edges.values())),
        partial=result["truncated"],
        meta={"impact_rationale": rationale},
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
