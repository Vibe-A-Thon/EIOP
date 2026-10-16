"""Egress policy engine (SR-LLM-011, super-requirements.md §10.2).

The policy matrix maps ``(data class / orthogonal tags) x (task type) x
(endpoint) x (user role) x (region)`` to a maximum sharing level plus an
approval requirement. Decisions are **most-restrictive-wins**: the minimum
``max_level`` across all matching rules applies, and the default level is
**S0** (nothing leaves the boundary) for every tenant until an
administrator enables an endpoint with a recorded consent/contract record
(SR-LLM-017).

Sharing levels (§10.2 Dimension B):

* S0 None (default) · S1 Schema-only · S2 Aggregates · S3 Synthetic ·
  S4 Tokenized/pseudonymized · S5 Redacted excerpts · S6 Minimized full
  context with per-request human approval (exact preview) · S7 Full.

Data classes (Dimension A): D0 public, D1 metadata/schema/ontology labels,
D2 internal business facts, D3 confidential, D4 restricted — plus
orthogonal tags (PII, PHI, PCI, SECRET, SOURCE_CODE, ...).
"""

from __future__ import annotations

from enum import Enum, IntEnum

from pydantic import BaseModel, ConfigDict, Field


class DataClass(str, Enum):
    """Data class dimension (§10.2 Dimension A)."""

    D0 = "D0"
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"
    D4 = "D4"


KNOWN_TAGS: frozenset[str] = frozenset({
    "PII", "PHI", "PCI", "SECRET", "SOURCE_CODE", "IP", "LEGAL_PRIVILEGED",
    "EXPORT_CONTROLLED", "EMPLOYEE", "CUSTOMER", "FINANCIAL", "GEO",
})

# Classes that may never leave the boundary (restriction rules win over any
# permissive rule that matches them).
RESTRICTED_CLASSES: frozenset[str] = frozenset({DataClass.D4})

# Tags that force schema-only unless a rule explicitly allows more.
SENSITIVE_TAGS: frozenset[str] = frozenset({
    "PII", "PHI", "PCI", "SECRET", "SOURCE_CODE",
})


class SharingLevel(IntEnum):
    """Sharing level S0..S7, ordered — lower is more restrictive."""

    S0 = 0
    S1 = 1
    S2 = 2
    S3 = 3
    S4 = 4
    S5 = 5
    S6 = 6
    S7 = 7


class EgressTask(str, Enum):
    """Task types an egress call can serve (summarize, classify, ...)."""

    CHAT = "chat"
    SUMMARIZE = "summarize"
    CLASSIFY = "classify"
    EMBED = "embed"
    OCR = "ocr"
    SPEECH = "speech"
    RERANK = "rerank"
    TELEMETRY = "telemetry"
    REPORT_NARRATION = "report_narration"


class ApprovalRequirement(str, Enum):
    """Approval mode attached to a policy decision."""

    NONE = "none"
    PER_REQUEST = "per_request"  # S6: human approves each request


class PolicyRule(BaseModel):
    """One matrix row: match dimensions → max level + approval (SR-LLM-011)."""

    model_config = ConfigDict(extra="forbid")

    rule_id: str
    classes: list[str] = Field(default_factory=list, description="Data classes matched (empty = all)")
    tags: list[str] = Field(default_factory=list, description="Orthogonal tags matched (any)")
    tasks: list[str] = Field(default_factory=list, description="Task types matched (empty = all)")
    endpoints: list[str] = Field(default_factory=list, description="Endpoint ids matched (empty = all)")
    roles: list[str] = Field(default_factory=list, description="User roles matched (empty = all)")
    regions: list[str] = Field(default_factory=list, description="Jurisdiction pins (empty = all)")
    max_level: SharingLevel
    approval: ApprovalRequirement = ApprovalRequirement.NONE
    reason: str = ""


class PolicyDecision(BaseModel):
    """Auditable policy decision for one egress request."""

    model_config = ConfigDict(extra="forbid")

    allowed_level: SharingLevel
    approval_required: bool
    matched_rule_ids: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)

    @property
    def allowed(self) -> bool:
        return self.allowed_level > SharingLevel.S0


class PolicyEngine:
    """Most-restrictive-wins matrix evaluator (SR-LLM-011).

    Every request is evaluated against all rules; the effective level is
    the minimum ``max_level`` among matching rules, floored at the
    default level (S0). Restricted classes (D4) and sensitive tags
    (PII/PHI/PCI/SECRET/SOURCE_CODE) apply an implicit ceiling unless an
    explicit rule for the same dimension lifts it — i.e. the implicit
    ceiling always wins (fail closed).
    """

    def __init__(self, rules: list[PolicyRule] | None = None,
                 default_level: SharingLevel = SharingLevel.S0) -> None:
        self.rules: list[PolicyRule] = list(rules or [])
        self.default_level = default_level

    def add_rule(self, rule: PolicyRule) -> None:
        self.rules.append(rule)

    def evaluate(self, *, classes: list[str], tags: list[str] | None = None,
                 task: str, endpoint: str, role: str,
                 region: str | None = None) -> PolicyDecision:
        tags = tags or []
        matched: list[str] = []
        reasons: list[str] = []
        matched_levels: list[SharingLevel] = []
        approval = False

        for rule in self.rules:
            if rule.classes and not set(classes) & set(rule.classes):
                continue
            if rule.tags and not set(tags) & set(rule.tags):
                continue
            if rule.tasks and task not in rule.tasks:
                continue
            if rule.endpoints and endpoint not in rule.endpoints:
                continue
            if rule.roles and role not in rule.roles:
                continue
            if rule.regions and region not in rule.regions:
                continue
            matched.append(rule.rule_id)
            matched_levels.append(rule.max_level)
            if rule.approval == ApprovalRequirement.PER_REQUEST:
                approval = True

        # Most-restrictive-wins across all matching rules; default deny (S0)
        # when nothing matches (SR-LLM-011).
        if matched_levels:
            level = min(matched_levels)
            reasons.append(f"min level across rules {matched} = {level.name}")
        else:
            level = self.default_level
            reasons.append(f"no rule matched; default level {self.default_level.name}")

        # Fail-closed implicit ceilings (SR-LLM-011 default deny posture).
        implicit: SharingLevel | None = None
        if set(classes) & RESTRICTED_CLASSES:
            implicit = SharingLevel.S0
        elif set(tags) & SENSITIVE_TAGS:
            implicit = SharingLevel.S1
        if implicit is not None and implicit < level:
            level = implicit
            reasons.append(
                "implicit ceiling: restricted class/tag limits egress"
            )

        return PolicyDecision(
            allowed_level=level,
            approval_required=approval or level == SharingLevel.S6,
            matched_rule_ids=matched,
            reasons=reasons,
        )
