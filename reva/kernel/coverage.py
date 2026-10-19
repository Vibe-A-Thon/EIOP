"""Coverage model, composition, and absence assertions (T-104 / T-116 / REVA-CV-001 / §6.5)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

from reva.kernel.authority import CoverageStatus


class CoverageLimit(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    name: str
    value: int | float
    unit: str


class CoverageReason(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    code: str
    message: str


class SourceCoverage(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=False, frozen=True)
    source_id: str
    status: CoverageStatus
    watermark: Optional[str] = None


class Coverage(BaseModel):
    """Normative Coverage model representing completeness of an observation scope (§6.5)."""

    model_config = ConfigDict(extra="forbid", strict=False, frozen=True)


    status: CoverageStatus
    scope: str
    examined_count: Optional[int] = Field(default=None, ge=0)
    omitted_count: Optional[int] = Field(default=None, ge=0)
    truncated: bool = False
    limits: List[CoverageLimit] = Field(default_factory=list)
    reasons: List[CoverageReason] = Field(default_factory=list)
    directions: Optional[List[str]] = None
    per_source: Optional[List[SourceCoverage]] = None


def compose_coverage(*coverages: Coverage) -> Coverage:
    """Compose multiple Coverage instances into an aggregated result per §6.5 rules."""
    if not coverages:
        return Coverage(
            status=CoverageStatus.UNAVAILABLE,
            scope="empty",
            reasons=[CoverageReason(code="NO_COVERAGE", message="No coverage inputs supplied")],
        )

    # Status order: complete > partial > unknown > unavailable (min-status wins)
    min_status = min((c.status for c in coverages), key=lambda s: s.rank)

    # Scopes joined
    all_scopes = " ; ".join(dict.fromkeys(c.scope for c in coverages if c.scope))

    # Limits union (by name)
    seen_limits = set()
    limits = []
    for c in coverages:
        for lim in c.limits:
            key = (lim.name, lim.unit)
            if key not in seen_limits:
                seen_limits.add(key)
                limits.append(lim)

    # Reasons union (by code)
    seen_reasons = set()
    reasons = []
    for c in coverages:
        for r in c.reasons:
            if r.code not in seen_reasons:
                seen_reasons.add(r.code)
                reasons.append(r)

    # Examined counts sum
    examined = 0
    any_examined = False
    for c in coverages:
        if c.examined_count is not None:
            examined += c.examined_count
            any_examined = True

    # Omitted count: null-propagating
    omitted = 0
    omitted_known = True
    for c in coverages:
        if c.omitted_count is None:
            omitted_known = False
            break
        omitted += c.omitted_count

    truncated = any(c.truncated for c in coverages)

    return Coverage(
        status=min_status,
        scope=all_scopes,
        examined_count=examined if any_examined else None,
        omitted_count=omitted if omitted_known else None,
        truncated=truncated,
        limits=limits,
        reasons=reasons,
    )


def assert_absent(query: str, coverage: Coverage) -> Dict[str, Any]:
    """Return proven_absent only under complete coverage; otherwise not_found_unknown."""
    if coverage.status == CoverageStatus.COMPLETE and not coverage.truncated:
        return {
            "query": query,
            "verdict": "proven_absent",
            "coverage": coverage.model_dump(),
        }
    return {
        "query": query,
        "verdict": "not_found_unknown",
        "coverage": coverage.model_dump(),
        "reasons": [r.model_dump() for r in coverage.reasons],
    }
