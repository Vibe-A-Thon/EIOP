"""QueryPlan v1 — typed, policy-validated query intent.

Normative: EOIP-engg-doc-pkg/schemas/query_plan.schema.json
Natural language NEVER produces executable Gremlin; it produces a QueryPlan
validated against schema + policy, then executed via a named bounded Gremlin
template (FR-QUERY-001, FR-QUERY-005, FR-QUERY-008).
"""

from typing import Literal

from pydantic import BaseModel, Field

QueryIntent = Literal["SEARCH", "PATH", "IMPACT", "NEIGHBORHOOD", "LINEAGE", "TRACEABILITY"]
EvidenceMode = Literal["NONE", "SUMMARY", "FULL"]


class QueryPlan(BaseModel):
    intent: QueryIntent
    anchors: list[str]
    relationship_allowlist: list[str] | None = None
    max_depth: int = Field(ge=1, le=8)
    result_limit: int = Field(ge=1, le=500)
    timeout_ms: int = Field(default=5000, ge=50, le=30000)
    evidence_mode: EvidenceMode
    filters: dict | None = None
