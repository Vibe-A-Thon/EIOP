"""Query intelligence: plan explain, cost estimation, history, slow-query
analysis, and saved parameterized query templates.

GAP-QI-001: query plan explain (steps, estimated fanout/visited vertices, indexes used)
GAP-QI-002: heuristic cost estimation from plan shape + graph size stats
GAP-QI-003: query history ring-buffer with latency/plan/result size, persisted via audit sink
GAP-QI-004 / GAP-QI-005: slow-query analyzer with top-N report and suggested indexes
GAP-QI-006: traversal-risk warnings (supernodes, full scans, deep traversal)
GAP-QI-007: saved parameterized query templates (CRUD + binding + safety validation)
GAP-QI-008: policy-aware templates (bound plans re-validated against QueryPolicy)

All estimates are deterministic heuristics over graph size statistics — no LLM calls.
"""

from __future__ import annotations

import time
from collections import deque
from uuid import uuid4

from pydantic import BaseModel, Field, ValidationError

from eoip.audit.sink import AuditSink
from eoip.contracts.audit import AuditEvent
from eoip.contracts.query_plan import QueryPlan
from eoip.graph.store import GraphStore
from eoip.query.executor import QueryExecutor
from eoip.query.policy import DEFAULT_POLICY, QueryPolicy

EXACT_INDEX_LOOKUPS = (
    ("WorkItem", "issue_key"),
    ("Commit", "commit_sha"),
    ("CodeSymbol", "qualified_name"),
)


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------


class PlanStep(BaseModel):
    order: int
    operation: str
    description: str
    estimated_visited_vertices: int
    fanout: float
    indexes_used: list[str] = Field(default_factory=list)


class ExplainedQueryPlan(BaseModel):
    explain_id: str
    plan: QueryPlan
    policy_violations: list[str] = Field(default_factory=list)
    steps: list[PlanStep] = Field(default_factory=list)
    total_estimated_vertices: int
    estimated_fanout: float
    indexes_used: list[str] = Field(default_factory=list)
    estimated_cost: float
    traversal_risks: list[str] = Field(default_factory=list)


class CostEstimate(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    grade: str  # LOW / MODERATE / HIGH / SEVERE
    breakdown: dict[str, float]
    estimated_vertices: int


class QueryHistoryEntry(BaseModel):
    history_id: str
    query_id: str | None
    intent: str
    anchors: list[str]
    latency_ms: float
    result_nodes: int
    result_edges: int
    partial: bool
    cost_score: float
    explain_id: str


class SlowQueryReport(BaseModel):
    threshold_ms: float
    total_executed: int
    slow_count: int
    top: list[QueryHistoryEntry]
    suggestions: list[str]


class QueryTemplate(BaseModel):
    template_id: str
    name: str
    description: str = ""
    intent: str
    anchor_params: list[str]
    filters_template: dict | None = None
    relationship_allowlist: list[str] | None = None
    max_depth: int = Field(default=3, ge=1, le=8)
    result_limit: int = Field(default=50, ge=1, le=500)
    timeout_ms: int = Field(default=5000, ge=50, le=30000)
    evidence_mode: str = "SUMMARY"
    created_by: str = "system"


class TemplateBindingError(ValueError):
    pass


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class QueryIntelligence:
    """Explain, cost, record, and analyze queries executed via QueryExecutor."""

    def __init__(
        self,
        store: GraphStore,
        policy: QueryPolicy | None = None,
        audit_sink: AuditSink | None = None,
        history_capacity: int = 1000,
    ) -> None:
        self._store = store
        self._policy = policy or DEFAULT_POLICY
        self._audit = audit_sink
        self._executor = QueryExecutor(store, self._policy)
        self._history: deque[QueryHistoryEntry] = deque(maxlen=history_capacity)
        self._templates: dict[str, QueryTemplate] = {}

    # -- GAP-QI-001: plan explain -------------------------------------------

    def explain(self, plan: QueryPlan) -> ExplainedQueryPlan:
        violations = self._policy.validate(plan)
        stats = self._graph_stats()
        steps = self._build_steps(plan, stats)
        total = sum(s.estimated_visited_vertices for s in steps)
        fanout = max((s.fanout for s in steps), default=0.0)
        indexes = sorted({idx for s in steps for idx in s.indexes_used})
        cost = self._cost_score(plan, total, stats)
        return ExplainedQueryPlan(
            explain_id=f"urn:eoip:query:explain:{uuid4()}",
            plan=plan,
            policy_violations=violations,
            steps=steps,
            total_estimated_vertices=total,
            estimated_fanout=round(fanout, 3),
            indexes_used=indexes,
            estimated_cost=cost.score,
            traversal_risks=self._traversal_risks(plan, total, stats),
        )

    def _graph_stats(self) -> dict:
        vertices = max(0, int(self._store.count_vertices()))
        edges = max(0, int(self._store.count_edges()))
        return {
            "vertices": vertices,
            "edges": edges,
            "avg_degree": (edges / vertices) if vertices else 0.0,
        }

    def _build_steps(self, plan: QueryPlan, stats: dict) -> list[PlanStep]:
        v, avg_degree = stats["vertices"], stats["avg_degree"]
        if plan.intent == "SEARCH":
            return self._search_steps(plan, stats)
        depth = plan.max_depth
        steps: list[PlanStep] = []
        visited = 1
        frontier = 1.0
        for level in range(1, depth + 1):
            frontier = frontier * max(avg_degree, 1.0)
            level_visited = int(min(frontier, max(plan.result_limit, 1)))
            visited += level_visited
            steps.append(
                PlanStep(
                    order=level,
                    operation="bfs_expand",
                    description=f"Expand frontier at depth {level} (bounded by result_limit)",
                    estimated_visited_vertices=level_visited,
                    fanout=round(max(avg_degree, 1.0), 3),
                    indexes_used=["primary.vertex_id"] if level == 1 else [],
                )
            )
        if plan.intent == "PATH":
            steps.insert(
                0,
                PlanStep(
                    order=0,
                    operation="anchor_lookup",
                    description="Resolve source and target anchors by canonical_id",
                    estimated_visited_vertices=2,
                    fanout=1.0,
                    indexes_used=["primary.canonical_id"],
                ),
            )
        else:
            steps.insert(
                0,
                PlanStep(
                    order=0,
                    operation="anchor_lookup",
                    description="Resolve anchor vertex by canonical_id",
                    estimated_visited_vertices=1,
                    fanout=1.0,
                    indexes_used=["primary.canonical_id"],
                ),
            )
        return steps

    def _search_steps(self, plan: QueryPlan, stats: dict) -> list[PlanStep]:
        query = plan.anchors[0] if plan.anchors else ""
        filters = dict(plan.filters or {})
        label = filters.get("label")
        steps: list[PlanStep] = []
        indexes: list[str] = []
        for item_label, key in EXACT_INDEX_LOOKUPS:
            if label is not None and label != item_label:
                continue
            indexes.append(f"secondary.{item_label}.{key}")
        steps.append(
            PlanStep(
                order=0,
                operation="exact_index_lookup",
                description="Exact-match probe of secondary indexes before scan",
                estimated_visited_vertices=1,
                fanout=1.0,
                indexes_used=indexes,
            )
        )
        steps.append(
            PlanStep(
                order=1,
                operation="label_scan",
                description="Scan candidate vertices and substring-match searchable properties",
                estimated_visited_vertices=min(stats["vertices"], 5000),
                fanout=round(max(stats["avg_degree"], 1.0), 3),
                indexes_used=[],
            )
        )
        return steps

    # -- GAP-QI-002: cost estimation ----------------------------------------

    def cost(self, plan: QueryPlan) -> CostEstimate:
        stats = self._graph_stats()
        total = sum(s.estimated_visited_vertices for s in self._build_steps(plan, stats))
        return self._cost_score(plan, total, stats)

    def _cost_score(self, plan: QueryPlan, estimated_vertices: int, stats: dict) -> CostEstimate:
        v = max(stats["vertices"], 1)
        depth_ratio = min(plan.max_depth / max(self._policy.max_depth, 1), 1.0)
        volume_ratio = min(estimated_vertices / v, 1.0)
        scan_ratio = 1.0 if plan.intent == "SEARCH" else 0.5
        timeout_ratio = plan.timeout_ms / max(self._policy.max_timeout_ms, 1)
        score = round(
            0.35 * depth_ratio
            + 0.35 * volume_ratio
            + 0.15 * scan_ratio
            + 0.15 * timeout_ratio,
            4,
        )
        grade = (
            "SEVERE" if score >= 0.8 else "HIGH" if score >= 0.6 else "MODERATE" if score >= 0.35 else "LOW"
        )
        return CostEstimate(
            score=score,
            grade=grade,
            breakdown={
                "depth": round(0.35 * depth_ratio, 4),
                "volume": round(0.35 * volume_ratio, 4),
                "scan": round(0.15 * scan_ratio, 4),
                "timeout": round(0.15 * timeout_ratio, 4),
            },
            estimated_vertices=estimated_vertices,
        )

    # -- GAP-QI-006: traversal-risk warnings --------------------------------

    def _traversal_risks(self, plan: QueryPlan, estimated: int, stats: dict) -> list[str]:
        risks: list[str] = []
        if stats["avg_degree"] > 20:
            risks.append(
                f"Supernode risk: average degree {stats['avg_degree']:.1f} may expand "
                "the frontier faster than result_limit can bound"
            )
        if plan.intent == "SEARCH" and stats["vertices"] > 5000:
            risks.append("Full candidate scan over >5000 vertices; no covering index for the free-text term")
        if plan.max_depth >= self._policy.max_depth:
            risks.append(f"Traversal depth {plan.max_depth} is at the policy maximum")
        if not plan.relationship_allowlist and plan.intent in {"IMPACT", "PATH", "TRACEABILITY", "LINEAGE"}:
            risks.append("No relationship allowlist: traversal crosses all edge labels")
        if estimated > stats["vertices"] * 0.5 and stats["vertices"] > 0:
            risks.append("Estimated visited vertices exceed half the graph")
        return risks

    # -- GAP-QI-003: query history (execution + persistence) -----------------

    @property
    def history(self) -> list[QueryHistoryEntry]:
        return list(self._history)

    def execute(self, plan: QueryPlan):
        """Execute via QueryExecutor, record latency/plan/result size in history."""
        explain = self.explain(plan)
        start = time.perf_counter()
        result = self._executor.execute(plan)
        latency_ms = (time.perf_counter() - start) * 1000.0
        entry = QueryHistoryEntry(
            history_id=f"urn:eoip:query:history:{uuid4()}",
            query_id=result.query_id,
            intent=plan.intent,
            anchors=list(plan.anchors),
            latency_ms=round(latency_ms, 3),
            result_nodes=len(result.nodes),
            result_edges=len(result.edges),
            partial=result.partial,
            cost_score=explain.estimated_cost,
            explain_id=explain.explain_id,
        )
        self._history.append(entry)
        self._persist(entry, explain, plan)
        return result

    def _persist(self, entry: QueryHistoryEntry, explain: ExplainedQueryPlan, plan: QueryPlan) -> None:
        if self._audit is None:
            return
        self._audit.emit(
            AuditEvent(
                audit_id=f"urn:eoip:audit:query:{uuid4()}",
                event_type="query.executed",
                actor="query-intelligence",
                correlation_id=entry.history_id,
                resource_refs=list(plan.anchors),
                outcome="success",
                reason_code="slow_query" if entry.latency_ms >= 1000 else None,
                safe_summary=(
                    f"intent={plan.intent} latency_ms={entry.latency_ms} "
                    f"nodes={entry.result_nodes} cost={entry.cost_score}"
                ),
            ),
            plan={
                "intent": plan.intent,
                "max_depth": plan.max_depth,
                "result_limit": plan.result_limit,
                "estimated_cost": explain.estimated_cost,
                "indexes_used": explain.indexes_used,
                "traversal_risks": explain.traversal_risks,
            },
        )

    # -- GAP-QI-004 / QI-005: slow-query analyzer ----------------------------

    def slow_queries(self, threshold_ms: float = 1000.0, top_n: int = 10) -> SlowQueryReport:
        slow = [e for e in self._history if e.latency_ms >= threshold_ms]
        slow.sort(key=lambda e: e.latency_ms, reverse=True)
        top = slow[:top_n]
        suggestions: list[str] = []
        for entry in top:
            if entry.intent == "SEARCH":
                suggestions.append(
                    f"Query {entry.history_id} (SEARCH, {entry.latency_ms}ms): add a secondary "
                    "index on the filtered property or narrow the label filter to skip the candidate scan"
                )
            else:
                suggestions.append(
                    f"Query {entry.history_id} ({entry.intent}, {entry.latency_ms}ms): add a "
                    "relationship allowlist, lower max_depth, or add a secondary index on the "
                    "traversed edge label"
                )
        if not top:
            suggestions.append("No slow queries above threshold")
        return SlowQueryReport(
            threshold_ms=threshold_ms,
            total_executed=len(self._history),
            slow_count=len(slow),
            top=top,
            suggestions=suggestions,
        )

    # -- GAP-QI-007 / QI-008: saved parameterized templates ------------------

    def save_template(
        self,
        name: str,
        intent: str,
        anchor_params: list[str],
        *,
        description: str = "",
        filters_template: dict | None = None,
        relationship_allowlist: list[str] | None = None,
        max_depth: int = 3,
        result_limit: int = 50,
        timeout_ms: int = 5000,
        evidence_mode: str = "SUMMARY",
        created_by: str = "system",
    ) -> QueryTemplate:
        template = QueryTemplate(
            template_id=f"urn:eoip:query:template:{uuid4()}",
            name=name,
            description=description,
            intent=intent,
            anchor_params=list(anchor_params),
            filters_template=filters_template,
            relationship_allowlist=relationship_allowlist,
            max_depth=max_depth,
            result_limit=result_limit,
            timeout_ms=timeout_ms,
            evidence_mode=evidence_mode,
            created_by=created_by,
        )
        # Safety: the default-bound plan must pass policy validation.
        probe = self.bind_template(template, {p: "probe-anchor" for p in template.anchor_params})
        violations = self._policy.validate(probe)
        if violations:
            raise TemplateBindingError(f"Template fails policy validation: {violations}")
        self._templates[template.template_id] = template
        return template

    def list_templates(self) -> list[QueryTemplate]:
        return list(self._templates.values())

    def get_template(self, template_id: str) -> QueryTemplate:
        try:
            return self._templates[template_id]
        except KeyError:
            raise TemplateBindingError(f"Unknown template: {template_id}") from None

    def delete_template(self, template_id: str) -> bool:
        return self._templates.pop(template_id, None) is not None

    def bind_template(self, template: QueryTemplate, params: dict[str, str]) -> QueryPlan:
        """Bind named string parameters into a QueryPlan (GAP-QI-007).

        Safety validation: parameters must all be strings, every declared
        anchor param must be supplied, no extras are allowed, and values may
        not contain template-injection characters.
        """
        if set(params) != set(template.anchor_params):
            missing = set(template.anchor_params) - set(params)
            extra = set(params) - set(template.anchor_params)
            raise TemplateBindingError(
                f"Parameter mismatch: missing={sorted(missing)} extra={sorted(extra)}"
            )
        try:
            return self._build_plan(template, params)
        except ValidationError as exc:
            raise TemplateBindingError(f"Template binding failed validation: {exc}") from None

    def _build_plan(self, template: QueryTemplate, params: dict[str, str]) -> QueryPlan:
        anchors: list[str] = []
        for param in template.anchor_params:
            value = params[param]
            if not isinstance(value, str):
                raise TemplateBindingError(f"Parameter '{param}' must be a string")
            if any(ch in value for ch in "{}$\\"):
                raise TemplateBindingError(
                    f"Parameter '{param}' contains forbidden characters"
                )
            if not value.strip():
                raise TemplateBindingError(f"Parameter '{param}' must not be empty")
            anchors.append(value)
        return QueryPlan(
            intent=template.intent,
            anchors=anchors,
            relationship_allowlist=template.relationship_allowlist,
            max_depth=template.max_depth,
            result_limit=template.result_limit,
            timeout_ms=template.timeout_ms,
            evidence_mode=template.evidence_mode,
            filters=template.filters_template,
        )
