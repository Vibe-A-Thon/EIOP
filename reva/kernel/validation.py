"""Cross-field warrant validation enforcing rules V-01..V-16 (T-105 / REVA-WK-004 / §6.3.3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set

from reva.core.errors import ValidationError
from reva.core.time import parse_ts
from reva.kernel.authority import Authority, ConfidenceBand, CoverageStatus, Epistemic
from reva.kernel.warrant import WarrantBody


@dataclass
class Violation:
    rule_id: str
    pointer: str
    message: str


@dataclass
class ValidationContext:
    known_artifacts: Dict[str, str] = field(default_factory=dict)  # artifact_id -> sha256
    known_warrants: Set[str] = field(default_factory=set)          # warrant_ids in tenant
    active_keys: Set[str] = field(default_factory=set)             # active key_ids
    predicate_validators: Dict[str, Callable[[Dict[str, Any]], bool]] = field(default_factory=dict)
    skip_external_lookups: bool = False


def rule_v01(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.authority == Authority.MODEL_INFERRED and b.epistemic_state != Epistemic.INFERRED:
        return Violation("V-01", "/epistemic_state", f"Authority model_inferred requires epistemic_state inferred, got {b.epistemic_state.value}")
    return None


def rule_v02(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.authority == Authority.RULE_DERIVED and b.epistemic_state not in {Epistemic.DERIVED, Epistemic.INFERRED}:
        return Violation("V-02", "/epistemic_state", f"Authority rule_derived requires epistemic_state derived or inferred, got {b.epistemic_state.value}")
    return None


def rule_v03(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    allowed = {
        Authority.SOURCE_SYSTEM_RECORD,
        Authority.SOURCE_CODE_STATIC,
        Authority.SHIPPED_ARTIFACT,
        Authority.RUNTIME_OBSERVED,
        Authority.CONTROLLED_EXECUTION,
        Authority.HUMAN_ATTESTED,
        Authority.EXTERNAL_SERVICE,
    }
    if b.epistemic_state == Epistemic.OBSERVED and b.authority not in allowed:
        return Violation("V-03", "/authority", f"Epistemic state observed requires empirical authority, got {b.authority.value}")
    return None


def rule_v04(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.confidence.band == ConfidenceBand.EXACT:
        if b.epistemic_state != Epistemic.OBSERVED or b.confidence.score_bp != 10000:
            return Violation("V-04", "/confidence", "Exact confidence requires epistemic_state=observed and score_bp=10000")
    return None


def rule_v05(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.epistemic_state in {Epistemic.UNKNOWN, Epistemic.UNAVAILABLE}:
        if (
            b.confidence.band != ConfidenceBand.UNKNOWN
            or b.confidence.score_bp != 0
            or len(b.limitations) == 0
            or not b.statement.get("reason")
        ):
            return Violation(
                "V-05",
                "/epistemic_state",
                "Unknown/unavailable states require band=unknown, score_bp=0, >=1 limitation and statement.reason non-empty",
            )
    return None


def rule_v06(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.epistemic_state in {Epistemic.INFERRED, Epistemic.DERIVED}:
        has_rel = any(l.rel in {"derived_from", "context"} for l in b.links)
        if len(b.limitations) == 0 or not has_rel:
            return Violation(
                "V-06",
                "/links",
                f"Epistemic state {b.epistemic_state.value} requires >=1 limitation and >=1 derived_from or context link",
            )
    return None


def rule_v07(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.predicate == "reva.pred.observed_as":
        has_static = any(l.rel == "reconciles_static" for l in b.links)
        has_runtime = any(l.rel == "reconciles_runtime" for l in b.links)
        if b.epistemic_state != Epistemic.INFERRED or not has_static or not has_runtime:
            return Violation(
                "V-07",
                "/links",
                "Predicate reva.pred.observed_as requires inferred epistemic state, >=1 reconciles_static and >=1 reconciles_runtime link",
            )
    return None


def rule_v08(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.coverage:
        if b.coverage.status == CoverageStatus.PARTIAL:
            if not b.coverage.limits and not b.coverage.reasons:
                return Violation("V-08", "/coverage/reasons", "Partial coverage requires limits or reasons")
        if b.coverage.truncated:
            if b.coverage.status != CoverageStatus.PARTIAL:
                return Violation("V-08", "/coverage/status", "Truncated coverage must have status partial")
    return None


def rule_v09(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.coverage and b.coverage.status == CoverageStatus.COMPLETE:
        if b.coverage.truncated or b.coverage.omitted_count != 0:
            return Violation("V-09", "/coverage", "Complete coverage requires truncated=false and omitted_count=0")
    return None


def rule_v10(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.authority in {Authority.SOURCE_CODE_STATIC, Authority.SHIPPED_ARTIFACT}:
        if any(getattr(loc, "kind", None) == "runtime" for loc in b.locations):
            return Violation("V-10", "/locations", "Static/shipped authority cannot declare runtime location kinds")
    return None


def rule_v11(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.authority == Authority.RUNTIME_OBSERVED:
        has_runtime_loc = any(getattr(loc, "kind", None) in {"runtime", "log", "url"} for loc in b.locations)
        if not has_runtime_loc:
            return Violation("V-11", "/locations", "Runtime observed authority requires runtime, log, or url location")
    return None


def rule_v12(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if ctx.skip_external_lookups:
        return None
    if getattr(b.subject, "kind", None) == "artifact":
        art_id = getattr(b.subject, "artifact_id", None)
        sha = getattr(b.subject, "sha256", None)
        if art_id in ctx.known_artifacts:
            expected = ctx.known_artifacts[art_id]
            if sha and sha.lower() != expected.lower():
                return Violation("V-12", "/subject/sha256", f"Artifact digest mismatch: declared {sha}, stored {expected}")
    return None


def rule_v13(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    from_dt = parse_ts(b.valid_time.from_ts)
    if b.valid_time.to_ts:
        to_dt = parse_ts(b.valid_time.to_ts)
        if to_dt < from_dt:
            return Violation("V-13", "/valid_time/to", f"valid_time.to ({b.valid_time.to_ts}) must be >= valid_time.from ({b.valid_time.from_ts})")
    return None


def rule_v14(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if ctx.skip_external_lookups or not ctx.known_warrants:
        return None
    for idx, link in enumerate(b.links):
        if link.warrant_id not in ctx.known_warrants:
            return Violation("V-14", f"/links/{idx}/warrant_id", f"Referenced link warrant does not exist: {link.warrant_id}")
    return None


def rule_v15(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if ctx.skip_external_lookups or not ctx.active_keys:
        return None
    if b.producer.key_id not in ctx.active_keys:
        return Violation("V-15", "/producer/key_id", f"Producer key is not active: {b.producer.key_id}")
    return None


def rule_v16(b: WarrantBody, ctx: ValidationContext) -> Optional[Violation]:
    if b.predicate in ctx.predicate_validators:
        validator = ctx.predicate_validators[b.predicate]
        if not validator(b.statement):
            return Violation("V-16", "/statement", f"Statement failed predicate model validation for {b.predicate}")
    return None


RULES: List[Callable[[WarrantBody, ValidationContext], Optional[Violation]]] = [
    rule_v01,
    rule_v02,
    rule_v03,
    rule_v04,
    rule_v05,
    rule_v06,
    rule_v07,
    rule_v08,
    rule_v09,
    rule_v10,
    rule_v11,
    rule_v12,
    rule_v13,
    rule_v14,
    rule_v15,
    rule_v16,
]


def validate_warrant_body(body: WarrantBody, *, ctx: Optional[ValidationContext] = None) -> List[Violation]:
    """Validate a warrant body against all cross-field rules V-01..V-16."""
    c = ctx or ValidationContext(skip_external_lookups=True)
    violations: List[Violation] = []
    for rule in RULES:
        res = rule(body, c)
        if res is not None:
            violations.append(res)
    return violations


def assert_valid(body: WarrantBody, ctx: Optional[ValidationContext] = None) -> None:
    """Assert body is valid, or raise ValidationError listing all violations."""
    violations = validate_warrant_body(body, ctx=ctx)
    if violations:
        issues = [{"pointer": v.pointer, "reason": f"[{v.rule_id}] {v.message}"} for v in violations]
        raise ValidationError(
            f"Warrant body failed {len(violations)} validation rules: {', '.join(v.rule_id for v in violations)}",
            details={"issues": issues},
        )
