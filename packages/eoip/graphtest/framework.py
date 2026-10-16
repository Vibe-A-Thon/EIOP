"""Declarative graph-assertion test framework (GAP-GRAPHTEST-001..011).

A YAML/JSON-loadable test DSL that asserts structural and semantic
properties of the knowledge graph: path existence/forbiddance,
cardinality, required relationships, orphans, cycles, data types,
ownership, provenance, temporal validity, architecture boundaries,
and traceability coverage per project/release.

Suites are executed against a GraphStore and produce a machine-readable
report with per-assertion pass/fail status and the violating nodes/edges.
No LLM interaction — every assertion is a deterministic graph query.
"""

from __future__ import annotations

import json
from collections import deque
from datetime import date, datetime
from enum import Enum
from typing import Any

import yaml
from pydantic import BaseModel, Field

from eoip.graph.conformance import ArchRule, RuleKind, compile_rule
from eoip.graph.store import GraphStore


class AssertionType(str, Enum):
    PATH_EXISTS = "path_exists"
    PATH_FORBIDDEN = "path_forbidden"
    CARDINALITY = "cardinality"
    REQUIRED_RELATIONSHIP = "required_relationship"
    NO_ORPHAN = "no_orphan"
    NO_CYCLE = "no_cycle"
    DATA_TYPE = "data_type"
    OWNERSHIP = "ownership"
    PROVENANCE_PRESENT = "provenance_present"
    TEMPORAL_VALIDITY = "temporal_validity"
    ARCHITECTURE_BOUNDARY = "architecture_boundary"
    TRACEABILITY_COVERAGE = "traceability_coverage"


class GraphAssertion(BaseModel):
    """A single declarative graph assertion (GAP-GRAPHTEST-001)."""

    id: str
    type: AssertionType
    description: str = ""
    # vertex selection
    source_label: str | None = None
    target_label: str | None = None
    label: str | None = None
    # relationship / path
    relationship: str | None = None
    via: list[str] = Field(default_factory=list)
    max_depth: int = 4
    # cardinality bounds
    min_count: int | None = None
    max_count: int | None = None
    # data type / property checks
    property: str | None = None
    expected_type: str | None = None
    # scoping (project / release / filter)
    filters: dict[str, Any] = Field(default_factory=dict)
    # provenance / ownership
    provenance_edges: list[str] = Field(
        default_factory=lambda: ["EVIDENCED_BY", "INGESTED_IN", "PRODUCED_BY"]
    )
    ownership_edge: str = "OWNED_BY"
    owner_label: str | None = None
    # traceability coverage
    coverage_threshold: float | None = None
    as_of: str | None = None


class GraphTestSuite(BaseModel):
    """A named suite of graph assertions (GAP-GRAPHTEST-002)."""

    id: str
    name: str = ""
    description: str = ""
    project: str | None = None
    release: str | None = None
    assertions: list[GraphAssertion] = Field(default_factory=list)


class AssertionResult(BaseModel):
    id: str
    type: AssertionType
    passed: bool
    message: str = ""
    violating_nodes: list[str] = Field(default_factory=list)
    violating_edges: list[dict[str, Any]] = Field(default_factory=list)
    measured: dict[str, Any] = Field(default_factory=dict)


class GraphTestReport(BaseModel):
    suite_id: str
    suite_name: str = ""
    total: int = 0
    passed: int = 0
    failed: int = 0
    results: list[AssertionResult] = Field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "suite_id": self.suite_id,
            "suite_name": self.suite_name,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "conformant": self.failed == 0,
            "results": [r.model_dump() for r in self.results],
        }


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_suite_file(path: str) -> GraphTestSuite:
    """Load a graph-test suite from a YAML or JSON file (GAP-GRAPHTEST-003)."""
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    data = yaml.safe_load(text) if path.lower().endswith((".yaml", ".yml")) else json.loads(text)
    return load_suite(data)


def load_suite(data: dict[str, Any]) -> GraphTestSuite:
    """Build a GraphTestSuite from a plain dict (already-parsed YAML/JSON)."""
    return GraphTestSuite.model_validate(data)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

_DISPATCH: dict[AssertionType, Any] = {}


def _check(fn):
    _DISPATCH[fn.__name__.removeprefix("_check_")] = fn
    return fn


class GraphTestRunner:
    """Executes a GraphTestSuite against a GraphStore (GAP-GRAPHTEST-004)."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def run(self, suite: GraphTestSuite) -> GraphTestReport:
        report = GraphTestReport(suite_id=suite.id, suite_name=suite.name or suite.id)
        for assertion in suite.assertions:
            result = self.run_assertion(assertion)
            report.results.append(result)
        report.total = len(report.results)
        report.passed = sum(1 for r in report.results if r.passed)
        report.failed = report.total - report.passed
        return report

    def run_assertion(self, assertion: GraphAssertion) -> AssertionResult:
        method = getattr(self, f"_check_{assertion.type.value}", None)
        if method is not None:
            return method(assertion)
        fn = _DISPATCH.get(assertion.type.value)
        if fn is None:
            return AssertionResult(
                id=assertion.id, type=assertion.type, passed=False,
                message=f"Unsupported assertion type: {assertion.type}",
            )
        return fn(self, assertion)

    # -- helpers -------------------------------------------------------------

    def _vertices(self, assertion: GraphAssertion, role: str = "source") -> list[dict]:
        label = (
            assertion.source_label if role == "source" else assertion.target_label
        ) or assertion.label
        if label is None:
            return []
        vertices = self._store.find_vertices(label=label, limit=10_000)
        filters = assertion.filters or {}
        if filters:
            vertices = [
                v for v in vertices
                if all(v["properties"].get(k) == val for k, val in filters.items())
            ]
        return vertices

    def _active_vertices(self, assertion: GraphAssertion, role: str = "source") -> list[dict]:
        today = date.today()
        active = []
        for vertex in self._vertices(assertion, role):
            props = vertex.get("properties") or {}
            valid_from = self._parse_date(props.get("valid_from"))
            valid_until = self._parse_date(props.get("valid_until"))
            if valid_from and valid_from > today:
                continue
            if valid_until and valid_until < today:
                continue
            active.append(vertex)
        return active

    def _peer(self, edge: dict, vid: str) -> dict | None:
        other = edge["in_v"] if edge["out_v"] == vid else edge["out_v"]
        return self._store.get_vertex(other)

    def _all_edges(self, vid: str) -> list[dict]:
        return self._store.edges_from(vid, limit=1000) + self._store.edges_to(vid, limit=1000)

    @staticmethod
    def _is_governance_edge(edge: dict) -> bool:
        return edge["label"] in {
            "ASSIGNED_TO",
            "OWNED_BY",
            "EVIDENCED_BY",
            "INGESTED_IN",
            "PRODUCED_BY",
        }

    def _reachable(self, start_vid: str, target_vids: set[str], max_depth: int,
                   allowed_labels: list[str] | None = None) -> list[dict] | None:
        """BFS; returns the path of (canonical_id, edge_label) hops to a target."""
        if start_vid in target_vids:
            return []
        visited = {start_vid}
        queue: deque[list[dict]] = deque([[]])
        frontier = [start_vid]
        for _ in range(max(1, max_depth)):
            nxt: list[str] = []
            for vid in frontier:
                path = queue.popleft() if queue else []
                for e in self._store.edges_from(vid, limit=500):
                    if allowed_labels and e["label"] not in allowed_labels:
                        continue
                    if e["in_v"] in visited:
                        continue
                    hop = {"edge": e["label"], "to": e["in_v"]}
                    new_path = path + [hop]
                    if e["in_v"] in target_vids:
                        return new_path
                    visited.add(e["in_v"])
                    nxt.append(e["in_v"])
                    queue.append(new_path)
            frontier = nxt
            if not frontier:
                break
        return None

    # -- assertion implementations -------------------------------------------

    def _check_path_exists(self, a: GraphAssertion) -> AssertionResult:
        sources = self._active_vertices(a, "source")
        targets = {t["vid"] for t in self._active_vertices(a, "target")}
        if not sources or not targets:
            return AssertionResult(id=a.id, type=a.type, passed=False,
                                   message="Source or target vertices not found")
        reachable = []
        for src in sources:
            if self._reachable(src["vid"], targets, a.max_depth, a.via or None) is not None:
                reachable.append(src["canonical_id"])
        return AssertionResult(
            id=a.id, type=a.type, passed=bool(reachable),
            message=(f"{len(reachable)} source(s) reach target within depth {a.max_depth}"
                     if reachable else "No source reaches target"),
            violating_nodes=[] if reachable else [src["canonical_id"] for src in sources],
            measured={"sources": len(sources), "reachable": len(reachable)},
        )

    def _check_path_forbidden(self, a: GraphAssertion) -> AssertionResult:
        sources = self._vertices(a, "source")
        targets = {t["vid"] for t in self._vertices(a, "target")}
        violations = []
        for src in sources:
            path = self._reachable(src["vid"], targets, a.max_depth, a.via or None)
            if path is not None:
                violations.append(src["canonical_id"])
        return AssertionResult(
            id=a.id, type=a.type, passed=not violations,
            message=(f"{len(violations)} source(s) illegally reach target"
                     if violations else "No forbidden path found"),
            violating_nodes=violations,
        )

    def _check_cardinality(self, a: GraphAssertion) -> AssertionResult:
        sources = self._active_vertices(a, "source")
        target_label = a.target_label
        violating = []
        counts: list[int] = []
        for src in sources:
            edges = self._store.edges_from(src["vid"], limit=1000) if a.relationship else self._all_edges(src["vid"])
            if a.relationship:
                edges = [e for e in edges if e["label"] == a.relationship]
            else:
                edges = [e for e in edges if not self._is_governance_edge(e)]
            if target_label:
                matched = []
                for e in edges:
                    peer = self._peer(e, src["vid"])
                    if peer and peer["label"] == target_label:
                        matched.append(e)
                edges = matched
            count = len(edges)
            counts.append(count)
            if (a.min_count is not None and count < a.min_count) or \
               (a.max_count is not None and count > a.max_count):
                violating.append(src["canonical_id"])
        return AssertionResult(
            id=a.id, type=a.type, passed=not violating,
            message=(f"{len(violating)} node(s) violate cardinality bounds"
                     if violating else "All nodes within cardinality bounds"),
            violating_nodes=violating,
            measured={"min": min(counts, default=0), "max": max(counts, default=0)},
        )

    def _check_required_relationship(self, a: GraphAssertion) -> AssertionResult:
        sources = self._active_vertices(a, "source")
        missing = []
        for src in sources:
            found = False
            for e in self._all_edges(src["vid"]):
                if a.relationship and e["label"] != a.relationship:
                    continue
                if a.target_label:
                    peer = self._peer(e, src["vid"])
                    if not peer or peer["label"] != a.target_label:
                        continue
                found = True
                break
            if not found:
                missing.append(src["canonical_id"])
        return AssertionResult(
            id=a.id, type=a.type, passed=not missing,
            message=(f"{len(missing)} node(s) missing required relationship {a.relationship or ''}"
                     if missing else "All nodes have required relationship"),
            violating_nodes=missing,
        )

    def _check_no_orphan(self, a: GraphAssertion) -> AssertionResult:
        vertices = self._vertices(a)
        orphans = []
        allowed = a.via or None
        for v in vertices:
            edges = self._all_edges(v["vid"])
            if allowed:
                edges = [e for e in edges if e["label"] in allowed]
            if not edges:
                orphans.append(v["canonical_id"])
        return AssertionResult(
            id=a.id, type=a.type, passed=not orphans,
            message=(f"{len(orphans)} orphan node(s) of type {a.label}"
                     if orphans else "No orphans found"),
            violating_nodes=orphans,
            measured={"checked": len(vertices), "orphans": len(orphans)},
        )

    def _check_no_cycle(self, a: GraphAssertion) -> AssertionResult:
        vertices = self._vertices(a)
        allowed = set(a.via) if a.via else None
        adjacency: dict[str, list[str]] = {}
        for v in vertices:
            outs = []
            for e in self._store.edges_from(v["vid"], limit=500):
                if allowed is not None and e["label"] not in allowed:
                    continue
                if any(u["vid"] == e["in_v"] for u in vertices):
                    outs.append(e["in_v"])
            adjacency[v["vid"]] = outs

        WHITE, GRAY, BLACK = 0, 1, 2
        color = {vid: WHITE for vid in adjacency}
        cycle_nodes: list[str] = []

        def visit(vid: str) -> bool:
            color[vid] = GRAY
            for nxt in adjacency[vid]:
                if color[nxt] == GRAY:
                    return True
                if color[nxt] == WHITE and visit(nxt):
                    return True
            color[vid] = BLACK
            return False

        for v in vertices:
            if color[v["vid"]] == WHITE and visit(v["vid"]):
                cycle_nodes.append(v["canonical_id"])
                break
        return AssertionResult(
            id=a.id, type=a.type, passed=not cycle_nodes,
            message="Cycle detected in subgraph" if cycle_nodes else "Subgraph is acyclic",
            violating_nodes=cycle_nodes,
        )

    _TYPE_MAP = {
        "string": str, "integer": int, "number": (int, float),
        "boolean": bool, "array": list, "object": dict,
    }

    def _check_data_type(self, a: GraphAssertion) -> AssertionResult:
        vertices = self._vertices(a)
        expected = self._TYPE_MAP.get((a.expected_type or "").lower())
        violating = []
        for v in vertices:
            if a.property not in v["properties"]:
                continue  # absence is checked by required_relationship
            value = v["properties"][a.property]
            if expected and value is not None and not isinstance(value, expected):
                violating.append(v["canonical_id"])
            elif expected is None:
                violating.append(v["canonical_id"])
        return AssertionResult(
            id=a.id, type=a.type, passed=not violating,
            message=(f"{len(violating)} node(s) have wrong type for {a.property}"
                     if violating else "All property values match expected type"),
            violating_nodes=violating,
        )

    def _check_ownership(self, a: GraphAssertion) -> AssertionResult:
        vertices = self._active_vertices(a)
        owner_label = a.owner_label or a.target_label
        unowned = []
        multi = []
        for v in vertices:
            owners = []
            for e in self._store.edges_from(v["vid"], limit=500):
                if e["label"] != a.ownership_edge:
                    continue
                peer = self._store.get_vertex(e["in_v"])
                if peer and (owner_label is None or peer["label"] == owner_label):
                    owners.append(peer["canonical_id"])
            if len(owners) == 0:
                unowned.append(v["canonical_id"])
            elif len(owners) > 1:
                multi.append(v["canonical_id"])
        violating = unowned + multi
        return AssertionResult(
            id=a.id, type=a.type, passed=not violating,
            message=(f"{len(unowned)} unowned, {len(multi)} multiply-owned"
                     if violating else "Every node has exactly one owner"),
            violating_nodes=violating,
            measured={"unowned": len(unowned), "multi_owned": len(multi)},
        )

    def _check_provenance_present(self, a: GraphAssertion) -> AssertionResult:
        vertices = self._vertices(a)
        provenance_props = ("source_system", "source", "provenance", "origin")
        missing = []
        for v in vertices:
            has_edge = any(
                e["label"] in a.provenance_edges for e in self._all_edges(v["vid"])
            )
            has_prop = any(
                v["properties"].get(p) is not None for p in provenance_props
            )
            if not has_edge and not has_prop:
                missing.append(v["canonical_id"])
        return AssertionResult(
            id=a.id, type=a.type, passed=not missing,
            message=(f"{len(missing)} node(s) lack provenance"
                     if missing else "All nodes carry provenance"),
            violating_nodes=missing,
        )

    def _check_temporal_validity(self, a: GraphAssertion) -> AssertionResult:
        as_of = self._parse_date(a.as_of) if a.as_of else date.today()
        violating = []
        for v in self._vertices(a):
            props = v["properties"]
            valid_from = self._parse_date(props.get("valid_from"))
            valid_until = self._parse_date(props.get("valid_until"))
            if valid_from and valid_until and valid_until < valid_from:
                violating.append(v["canonical_id"])
                continue
            if valid_from and valid_from > as_of:
                violating.append(v["canonical_id"])
            elif valid_until and valid_until < as_of:
                violating.append(v["canonical_id"])
        return AssertionResult(
            id=a.id, type=a.type, passed=not violating,
            message=(f"{len(violating)} node(s) outside temporal validity as of {as_of}"
                     if violating else "All nodes temporally valid"),
            violating_nodes=violating,
        )

    @staticmethod
    def _parse_date(value: Any) -> date | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        return datetime.fromisoformat(str(value)).date()

    def _check_architecture_boundary(self, a: GraphAssertion) -> AssertionResult:
        """Reuse the conformance engine's rule compilation (GAP-ARCHC-*) directly."""
        if not (a.source_label and a.target_label):
            return AssertionResult(id=a.id, type=a.type, passed=False,
                                   message="source_label and target_label are required")
        rule = ArchRule(
            id=a.id,
            kind=RuleKind.MUST_NOT_DEPEND,
            source=a.source_label,
            target=a.target_label,
            description=a.description,
            max_depth=a.max_depth,
        )
        findings = compile_rule(rule, self._store)
        return AssertionResult(
            id=a.id, type=a.type, passed=not findings,
            message=(f"{len(findings)} boundary violation(s)" if findings else "Boundary respected"),
            violating_nodes=[f.source_symbol or f.rule_id for f in findings],
            violating_edges=[{"path": f.violating_path} for f in findings if f.violating_path],
        )

    def _check_traceability_coverage(self, a: GraphAssertion) -> AssertionResult:
        sources = self._vertices(a, "source")
        target_label = a.target_label
        linked = 0
        for src in sources:
            for e in self._all_edges(src["vid"]):
                if a.via and e["label"] not in a.via:
                    continue
                if target_label:
                    peer = self._peer(e, src["vid"])
                    if not peer or peer["label"] != target_label:
                        continue
                linked += 1
                break
        total = len(sources)
        coverage = (linked / total * 100.0) if total else 100.0
        threshold = a.coverage_threshold if a.coverage_threshold is not None else 100.0
        unlinked = [v["canonical_id"] for v in sources][:20]
        return AssertionResult(
            id=a.id, type=a.type, passed=coverage >= threshold,
            message=(f"Traceability coverage {coverage:.1f}% ({linked}/{total}) "
                     f"vs threshold {threshold:.1f}%"),
            violating_nodes=[] if coverage >= threshold else unlinked,
            measured={"coverage_pct": round(coverage, 2), "linked": linked, "total": total},
        )


def run_suite(store: GraphStore, suite: GraphTestSuite) -> GraphTestReport:
    """Convenience: execute a suite and return the machine-readable report."""
    return GraphTestRunner(store).run(suite)


def run_suite_file(store: GraphStore, path: str) -> GraphTestReport:
    """Load a YAML/JSON suite file and execute it against the store."""
    return run_suite(store, load_suite_file(path))
