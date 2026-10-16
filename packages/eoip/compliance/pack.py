"""Compliance Pack format and evidence evaluation (SR-GOV-001).

A Compliance Pack is a declarative control catalog for a regulatory or
voluntary framework (§14.4): a list of controls, each mapped to platform
capabilities, with automated evidence query specs over the graph and audit
sink, report template references, and a gap-analysis output. Packs are data
(see ``eoip.compliance.packs``); this module defines the format and the
evidence-status evaluator that reports per-control evidence present/missing
against the real platform modules (audit sink, graph store, authz core,
agent proposal store, validation engine, ops bundles).

Deferred: PDF/DOCX/PPTX report rendering is an External gate (binary
renderers are intentionally not bundled; HTML/Markdown renderers live in
``eoip.reports``). Vendor certifications themselves are out of scope — the
platform supports *customer* compliance (§14.4 note).
"""

from __future__ import annotations

import uuid
from typing import Any, Callable, Literal

from pydantic import BaseModel, ConfigDict, Field

EvidenceKind = Literal[
    "audit_event",       # events of a given action/type in the audit sink
    "graph_vertices",    # vertices of a given label in the graph store
    "graph_edges",       # edges of a given label in the graph store
    "authz_roles",       # roles registered in the authz RoleRegistry
    "authz_decisions",   # auditable allow/deny decisions recorded
    "proposals",         # governed change proposals present
    "validation_findings",  # validation engine findings recorded
    "evidence_vertices", # provenance Evidence vertices present
    "backup_manifest",   # ops bundle / backup manifest present
    "policy_exceptions", # active policy exceptions visible
    "ai_governance",     # model cards / evaluation records registered
]


def new_id(area: str, type_: str) -> str:
    return f"urn:eoip:{area}:{type_}:{uuid.uuid4().hex[:12]}"


class EvidenceQuerySpec(BaseModel):
    """Automated evidence query for a control (SR-GOV-001).

    ``kind`` selects which real module is probed; ``params`` are passed to
    the probe. A control is satisfied when every spec in ``evidence`` is
    present (``min_count`` items found).
    """

    model_config = ConfigDict(extra="forbid")

    kind: EvidenceKind
    params: dict[str, Any] = Field(default_factory=dict)
    min_count: int = 1
    description: str = ""


class Control(BaseModel):
    """A single control in a pack's catalog."""

    model_config = ConfigDict(extra="forbid")

    control_id: str
    framework: str
    title: str
    description: str = ""
    platform_capabilities: list[str] = Field(default_factory=list)
    evidence: list[EvidenceQuerySpec] = Field(default_factory=list)
    report_template: str | None = None


class CompliancePack(BaseModel):
    """Control catalog + capability mapping + report templates (SR-GOV-001)."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str
    framework: str
    version: str
    description: str = ""
    controls: list[Control] = Field(default_factory=list)
    report_templates: list[str] = Field(default_factory=list)


class EvidenceStatus(BaseModel):
    """Per-control evidence evaluation result."""

    model_config = ConfigDict(extra="forbid")

    control_id: str
    present: bool
    details: list[dict[str, Any]] = Field(default_factory=list)


class GapAnalysisResult(BaseModel):
    """Gap analysis output: controls with missing evidence (SR-GOV-001)."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str
    evaluated_at: str
    total_controls: int
    satisfied: int
    gaps: list[str] = Field(default_factory=list)
    control_status: list[EvidenceStatus] = Field(default_factory=list)


class EvidenceSources(BaseModel):
    """Handles to the real platform modules probed by the evaluator.

    All fields optional so the evaluator degrades gracefully in unit tests
    and minimal deployments (missing source => its evidence kinds report
    missing rather than raising).
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    audit_sink: Any = None
    graph_store: Any = None
    role_registry: Any = None
    proposal_store: Any = None
    validation_engine: Any = None
    ops_bundle_dir: Any = None
    policy_exception_store: Any = None
    ai_governance_store: Any = None


def _count_audit_events(sink: Any, params: dict) -> int:
    events = sink.read(limit=int(params.get("limit", 500)))
    action = params.get("action")
    event_type = params.get("event_type")
    matched = 0
    for event in events:
        event_action = event.get("action") or event.get("outcome")
        if action and event_action != action:
            continue
        if event_type and event.get("event_type") != event_type:
            continue
        matched += 1
    return matched


def _probe(kind: EvidenceKind, params: dict, sources: EvidenceSources) -> int:
    """Return the number of matching evidence items found (0 if source absent)."""
    if kind == "audit_event":
        return _count_audit_events(sources.audit_sink, params) if sources.audit_sink else 0
    if kind == "graph_vertices":
        store = sources.graph_store
        if not store:
            return 0
        label = params.get("label")
        try:
            return store.count_vertices(label)
        except TypeError:
            return 0
    if kind == "graph_edges":
        store = sources.graph_store
        if not store:
            return 0
        try:
            return store.count_edges(params.get("label"))
        except TypeError:
            return 0
    if kind == "authz_roles":
        registry = sources.role_registry
        if not registry:
            return 0
        required = params.get("roles", [])
        try:
            existing = {role.name for role in registry.list()}
        except AttributeError:
            existing = set(getattr(registry, "roles", {}) or {})
        return sum(1 for role in required if role in existing)
    if kind == "authz_decisions":
        return _count_audit_events(sources.audit_sink, params) if sources.audit_sink else 0
    if kind == "proposals":
        store = sources.proposal_store
        if not store:
            return 0
        proposals = store.list()
        status = params.get("status")
        if status:
            proposals = [p for p in proposals if getattr(p, "status", None) == status]
        return len(proposals)
    if kind == "validation_findings":
        engine = sources.validation_engine
        if not engine:
            return 0
        findings = getattr(engine, "findings", None) or (
            engine.list() if hasattr(engine, "list") else []
        )
        return len(findings)
    if kind == "evidence_vertices":
        store = sources.graph_store
        if not store:
            return 0
        try:
            return store.count_vertices(params.get("label", "Evidence"))
        except TypeError:
            return 0
    if kind == "backup_manifest":
        import os

        directory = sources.ops_bundle_dir
        if not directory:
            return 0
        names = params.get("filenames", ["manifest.json"])
        return sum(
            1 for name in names if os.path.exists(os.path.join(str(directory), name))
        )
    if kind == "policy_exceptions":
        store = sources.policy_exception_store
        if not store:
            return 0
        return len(store.list(active_only=True))
    if kind == "ai_governance":
        store = sources.ai_governance_store
        if not store:
            return 0
        kind_param = params.get("record", "model_cards")
        items = {
            "model_cards": store.list_model_cards(),
            "evaluations": store.list_evaluations(),
        }.get(kind_param, [])
        return len(items)
    return 0


def evaluate_control(control: Control, sources: EvidenceSources) -> EvidenceStatus:
    """Report evidence present/missing for one control."""
    details = []
    all_present = True
    for spec in control.evidence:
        found = _probe(spec.kind, spec.params, sources)
        ok = found >= spec.min_count
        all_present = all_present and ok
        details.append({
            "kind": spec.kind,
            "params": spec.params,
            "found": found,
            "required": spec.min_count,
            "present": ok,
        })
    return EvidenceStatus(control_id=control.control_id, present=all_present, details=details)


def run_gap_analysis(
    pack: CompliancePack,
    sources: EvidenceSources,
    *,
    evaluated_at: str,
) -> GapAnalysisResult:
    """Evaluate every control in a pack and summarize gaps (SR-GOV-001)."""
    statuses = [evaluate_control(control, sources) for control in pack.controls]
    gaps = [s.control_id for s in statuses if not s.present]
    return GapAnalysisResult(
        pack_id=pack.pack_id,
        evaluated_at=evaluated_at,
        total_controls=len(pack.controls),
        satisfied=len(statuses) - len(gaps),
        gaps=gaps,
        control_status=statuses,
    )
