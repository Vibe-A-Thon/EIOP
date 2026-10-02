"""Query policy enforcement (FR-QUERY-006, FR-QUERY-008).

Every QueryPlan is validated against the active policy before execution.
The policy enforces depth, result, timeout, and relationship bounds.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from eoip.contracts.query_plan import QueryPlan
from eoip.ontology.manifest import EDGE_LABELS


@dataclass(frozen=True)
class QueryPolicy:
    max_depth: int = 8
    max_results: int = 500
    max_timeout_ms: int = 30000
    allowed_intents: frozenset[str] = frozenset(
        {"SEARCH", "PATH", "IMPACT", "NEIGHBORHOOD", "LINEAGE", "TRACEABILITY"}
    )
    blocked_edges: frozenset[str] = frozenset()
    read_only: bool = True

    def validate(self, plan: QueryPlan) -> list[str]:
        violations: list[str] = []
        if plan.intent not in self.allowed_intents:
            violations.append(f"Intent '{plan.intent}' is not permitted by query policy")
        if plan.max_depth > self.max_depth:
            violations.append(
                f"Requested depth {plan.max_depth} exceeds policy maximum {self.max_depth}"
            )
        if plan.result_limit > self.max_results:
            violations.append(
                f"Requested result limit {plan.result_limit} exceeds policy maximum {self.max_results}"
            )
        if plan.timeout_ms > self.max_timeout_ms:
            violations.append(
                f"Requested timeout {plan.timeout_ms}ms exceeds policy maximum {self.max_timeout_ms}ms"
            )
        if plan.relationship_allowlist:
            unknown = set(plan.relationship_allowlist) - set(EDGE_LABELS)
            if unknown:
                violations.append(f"Unknown relationship types: {sorted(unknown)}")
            blocked = set(plan.relationship_allowlist) & self.blocked_edges
            if blocked:
                violations.append(f"Blocked relationship types: {sorted(blocked)}")
        if not plan.anchors:
            violations.append("At least one anchor canonical_id is required")
        return violations

    def clamp(self, plan: QueryPlan) -> QueryPlan:
        return plan.model_copy(
            update={
                "max_depth": min(plan.max_depth, self.max_depth),
                "result_limit": min(plan.result_limit, self.max_results),
                "timeout_ms": min(plan.timeout_ms, self.max_timeout_ms),
            }
        )


DEFAULT_POLICY = QueryPolicy()
