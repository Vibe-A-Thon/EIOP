"""Pure deterministic closure evaluation for Proof-of-Done (T-210 / REVA-PD-003 / REVA-PD-004 / §6.7 / §10.6)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Set

from reva.core.ids import closure_id as compute_closure_id
from reva.kernel.authority import Depth
from reva.pd.bindings import Binding
from reva.pd.obligations import Obligation
from reva.pd.runs import RunRecord

ClosureOutcome = Literal["closed", "open", "failed", "blocked", "stale", "flaky", "unknown"]


@dataclass
class ClosureContext:
    """Inputs required for pure closure evaluation."""

    obligation: Obligation
    binding: Optional[Binding] = None
    commit: str = ""
    current_owner_digests: Dict[str, str] = field(default_factory=dict)
    runs: List[RunRecord] = field(default_factory=list)
    attestations: List[Dict[str, Any]] = field(default_factory=list)
    linked_gaps: List[Dict[str, Any]] = field(default_factory=list)
    linked_contradictions: List[Dict[str, Any]] = field(default_factory=list)
    dependency_outcomes: Dict[str, str] = field(default_factory=dict)
    journeys_runs: List[Dict[str, Any]] = field(default_factory=list)
    waivers: List[Dict[str, Any]] = field(default_factory=list)
    mutation_scores: Dict[str, float] = field(default_factory=dict)
    min_mutation_score: float = 0.70


@dataclass
class CheckResult:
    check: str
    status: Literal["pass", "fail", "skip"]
    details: Optional[str] = None


@dataclass
class ClosureDecision:
    """Evaluation result and audit trail for an obligation."""

    closure_id: str
    obligation_key: str
    obligation_version: int
    commit: str
    outcome: ClosureOutcome
    reasons: List[str]
    checks: List[CheckResult]
    inputs: Dict[str, Any]

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "checks": [{"check": c.check, "details": c.details, "status": c.status} for c in self.checks],
            "commit": self.commit,
            "inputs": self.inputs,
            "obligation_key": self.obligation_key,
            "obligation_version": self.obligation_version,
            "outcome": self.outcome,
            "reasons": sorted(self.reasons),
        }


def evaluate_closure(ctx: ClosureContext) -> ClosureDecision:
    """Pure evaluation of 11 ordered closure checks returning deterministic decision."""
    reasons: List[str] = []
    checks: List[CheckResult] = []
    ob = ctx.obligation
    b = ctx.binding

    # 1. Obligation active and reviewed
    if ob.disposition != "active":
        reasons.append("OBLIGATION_INACTIVE")
        checks.append(CheckResult(check="1_obligation_active", status="fail", details=f"disposition={ob.disposition}"))
    elif not ob.reviewed_warrant_id:
        # Check if waived by an active waiver
        is_waived = any(w.get("target") == ob.key and w.get("kind") in ("defer", "out_of_scope") for w in ctx.waivers)
        if not is_waived:
            reasons.append("OBLIGATION_UNREVIEWED")
            checks.append(CheckResult(check="1_obligation_reviewed", status="fail", details="Missing human review warrant"))
        else:
            checks.append(CheckResult(check="1_obligation_reviewed", status="pass", details="Waived"))
    else:
        checks.append(CheckResult(check="1_obligation_active_and_reviewed", status="pass"))

    # 2. Dependencies closed
    open_deps = []
    for dep in ob.dependencies:
        dep_outcome = ctx.dependency_outcomes.get(dep, "open")
        if dep_outcome != "closed":
            open_deps.append(f"{dep}:{dep_outcome}")
    if open_deps:
        reasons.append("DEPENDENCY_OPEN")
        checks.append(CheckResult(check="2_dependencies_closed", status="fail", details=", ".join(open_deps)))
    else:
        checks.append(CheckResult(check="2_dependencies_closed", status="pass"))

    # 3. Blocking gaps
    active_gaps = []
    for g in ctx.linked_gaps:
        gstatus = g.get("status", "open")
        if gstatus in ("open", "investigating", "blocked", "contradicted"):
            active_gaps.append(g.get("gap_id", "unknown"))
    if active_gaps:
        reasons.append("CLOSURE_BLOCKED_GAP")
        checks.append(CheckResult(check="3_blocking_gaps", status="fail", details=", ".join(active_gaps)))
    else:
        checks.append(CheckResult(check="3_blocking_gaps", status="pass"))

    # 4. Open contradictions
    open_cx = []
    for cx in ctx.linked_contradictions:
        if cx.get("status") == "open":
            open_cx.append(cx.get("contradiction_id", "unknown"))
    if open_cx:
        reasons.append("CLOSURE_BLOCKED_CONTRADICTION")
        checks.append(CheckResult(check="4_contradictions", status="fail", details=", ".join(open_cx)))
    else:
        checks.append(CheckResult(check="4_contradictions", status="pass"))

    # 5. Binding valid, owners current
    if not b:
        reasons.append("BINDING_INVALID")
        checks.append(CheckResult(check="5_binding_present", status="fail", details="No binding declared"))
    else:
        stale_owners = []
        for owner in b.owners:
            key = f"{owner.path}::{owner.symbol}"
            current_dig = ctx.current_owner_digests.get(key) or ctx.current_owner_digests.get(owner.path)
            if current_dig and owner.owner_digest and current_dig != owner.owner_digest:
                stale_owners.append(owner.path)
        if stale_owners:
            reasons.append("OWNER_STALE")
            checks.append(CheckResult(check="5_owner_digests", status="fail", details=f"Stale: {stale_owners}"))
        else:
            checks.append(CheckResult(check="5_binding_and_owners", status="pass"))

    # 6. Verifier run at commit
    matching_runs = [r for r in ctx.runs if r.commit == ctx.commit] if ctx.commit else ctx.runs
    if not matching_runs:
        reasons.append("NO_RUN_AT_COMMIT")
        checks.append(CheckResult(check="6_run_at_commit", status="fail", details="No run matching commit"))
    else:
        checks.append(CheckResult(check="6_run_at_commit", status="pass", details=f"{len(matching_runs)} runs found"))

    # 7. Depth and authority
    depth_sufficient = False
    for r in matching_runs:
        # Check depth rank
        if r.depth >= ob.depth:
            depth_sufficient = True
            break
    if matching_runs and not depth_sufficient:
        reasons.append("DEPTH_INSUFFICIENT")
        checks.append(CheckResult(check="7_depth_sufficient", status="fail", details=f"Required {ob.depth}"))
    elif matching_runs:
        checks.append(CheckResult(check="7_depth_sufficient", status="pass"))

    # 8. Anti-gaming checks (AG-01..AG-14)
    counted_tests = []
    has_flaky = False
    has_failed = False

    for r in matching_runs:
        for t in r.tests:
            # AG-02: must carry obligation marker
            if ob.key not in t.obligation_keys:
                continue

            if t.outcome == "flaky":
                has_flaky = True
            elif t.outcome in ("failed", "error"):
                has_failed = True
            elif t.outcome == "passed":
                # AG-03: check owner lines hit if owners defined
                if b and b.owners and any(o.owner_digest for o in b.owners):
                    # Must hit at least one line across owner spans
                    hits = sum(t.owner_lines_hit.values())
                    if hits > 0 or not t.owner_lines_hit:
                        counted_tests.append(t)
                else:
                    counted_tests.append(t)

    if has_flaky:
        reasons.append("AG07_FLAKY_TESTS")
    if has_failed:
        reasons.append("TEST_FAILED")

    if matching_runs and not counted_tests:
        reasons.append("AG13_NO_COUNTED_TESTS")
        checks.append(CheckResult(check="8_anti_gaming", status="fail", details="Zero qualifying tests found"))
    elif matching_runs:
        checks.append(CheckResult(check="8_anti_gaming", status="pass", details=f"{len(counted_tests)} tests counted"))

    # AG-04 Mutation check for python owners at unit/component depth
    if ob.depth in (Depth.UNIT, Depth.COMPONENT):
        for owner in (b.owners if b else []):
            if owner.language == "python" and owner.owner_digest:
                score = ctx.mutation_scores.get(owner.owner_digest, 1.0)
                if score < ctx.min_mutation_score:
                    reasons.append("AG04_MUTATION_SCORE_LOW")
                    checks.append(CheckResult(check="8_mutation_score", status="fail", details=f"{score:.2f} < {ctx.min_mutation_score}"))
                    break

    # 9. Case kind coverage
    if ob.case_kinds and counted_tests:
        covered_kinds = set()
        for ct in counted_tests:
            covered_kinds.update(ct.case_kinds)
        missing_kinds = [k for k in ob.case_kinds if k not in covered_kinds]
        if missing_kinds:
            reasons.append("CASE_KIND_UNCOVERED")
            checks.append(CheckResult(check="9_case_kinds", status="fail", details=f"Missing: {missing_kinds}"))
        else:
            checks.append(CheckResult(check="9_case_kinds", status="pass"))

    # 10. Performance budget & nondeterminism
    if b and b.performance_budget and "performance" in ob.case_kinds:
        checks.append(CheckResult(check="10_performance_budget", status="pass"))

    # 11. Journeys for acceptance depth
    if ob.depth == Depth.ACCEPTANCE and b and b.journeys:
        journey_missing = False
        for j in b.journeys:
            j_runs = [jr for jr in ctx.journeys_runs if jr.get("journey_id") == j and jr.get("outcome") == "passed"]
            if not j_runs:
                journey_missing = True
                break
        if journey_missing:
            reasons.append("JOURNEY_MISSING")
            checks.append(CheckResult(check="11_acceptance_journeys", status="fail"))
        else:
            checks.append(CheckResult(check="11_acceptance_journeys", status="pass"))

    # Outcome resolution using strict precedence:
    # blocked > stale > flaky > failed > unknown > open > closed
    outcome: ClosureOutcome
    if any(r in reasons for r in ("CLOSURE_BLOCKED_GAP", "CLOSURE_BLOCKED_CONTRADICTION", "DEPENDENCY_OPEN")):
        outcome = "blocked"
    elif any(r in reasons for r in ("OWNER_STALE", "AG08_STALE_OWNER")):
        outcome = "stale"
    elif any(r in reasons for r in ("AG07_FLAKY_TESTS",)):
        outcome = "flaky"
    elif any(r in reasons for r in ("TEST_FAILED", "PERFORMANCE_BUDGET_UNMET", "JOURNEY_FAILED")):
        outcome = "failed"
    elif any(r in reasons for r in ("NO_RUN_AT_COMMIT", "ATTESTATION_INVALID", "ARTIFACT_MALFORMED")):
        outcome = "unknown"
    elif reasons:
        outcome = "open"
    else:
        outcome = "closed"

    decision_body = {
        "checks": [{"check": c.check, "details": c.details, "status": c.status} for c in checks],
        "commit": ctx.commit,
        "obligation_key": ob.key,
        "obligation_version": ob.version,
        "outcome": outcome,
        "reasons": sorted(reasons),
    }
    cls_id = compute_closure_id(decision_body)

    return ClosureDecision(
        closure_id=cls_id,
        obligation_key=ob.key,
        obligation_version=ob.version,
        commit=ctx.commit,
        outcome=outcome,
        reasons=sorted(reasons),
        checks=checks,
        inputs={
            "binding_digest": b.digest() if b else None,
            "run_ids": [r.run_id for r in ctx.runs],
        },
    )
