"""Trust-zone utilities for graph facts and AI evidence disclosure.

Implements:
- GAP-TRUST-001: new, inferred, or untrusted knowledge can enter quarantine.
- GAP-TRUST-002: promotion requires rules, confidence, or approval evidence.
- GAP-TRUST-003: supported trust states are Raw, Parsed, Inferred, Reviewed, Trusted, Certified, Rejected.
- GAP-TRUST-004: queries can specify a minimum trust level.
- GAP-TRUST-005: AI answers disclose use of non-certified knowledge.
- GAP-RULE-002: distinguish asserted, inferred, model-generated, and human-confirmed facts.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from eoip.contracts.source_event import utc_now_iso


class TrustState(str, Enum):
    RAW = "RAW"
    PARSED = "PARSED"
    INFERRED = "INFERRED"
    REVIEWED = "REVIEWED"
    TRUSTED = "TRUSTED"
    CERTIFIED = "CERTIFIED"
    REJECTED = "REJECTED"


_TRUST_RANK = {
    TrustState.REJECTED: -1,
    TrustState.RAW: 0,
    TrustState.PARSED: 1,
    TrustState.INFERRED: 2,
    TrustState.REVIEWED: 3,
    TrustState.TRUSTED: 4,
    TrustState.CERTIFIED: 5,
}

_CREATION_TO_TRUST = {
    "DETERMINISTIC": TrustState.PARSED,
    "ASSERTED": TrustState.PARSED,
    "INFERRED": TrustState.INFERRED,
    "MODEL_GENERATED": TrustState.INFERRED,
    "HUMAN_CONFIRMED": TrustState.REVIEWED,
    "TRUSTED": TrustState.TRUSTED,
    "CERTIFIED": TrustState.CERTIFIED,
    "REJECTED": TrustState.REJECTED,
}


def normalize_trust_state(value: str | None, *, creation_status: str | None = None) -> TrustState:
    """Return a canonical trust state from user input or edge creation status."""

    if isinstance(value, TrustState):
        return value
    if value:
        normalized = value.upper()
        if normalized in TrustState.__members__:
            return TrustState[normalized]
    if creation_status:
        return _CREATION_TO_TRUST.get(creation_status.upper(), TrustState.RAW)
    return TrustState.RAW


def meets_trust_threshold(
    actual: str | None,
    threshold: str | None,
    *,
    creation_status: str | None = None,
) -> bool:
    """Check whether a fact is at least as trusted as the requested threshold."""

    if not threshold:
        return True
    state = normalize_trust_state(actual, creation_status=creation_status)
    minimum = normalize_trust_state(threshold)
    if state == TrustState.REJECTED:
        return False
    return _TRUST_RANK[state] >= _TRUST_RANK[minimum]


def quarantine_fact(properties: dict[str, Any], *, reason: str, source_ref: str | None = None) -> dict[str, Any]:
    """Return fact properties tagged for quarantine review."""

    updated = dict(properties)
    updated["trust_state"] = TrustState.RAW.value
    updated["quarantine"] = True
    updated["quarantine_reason"] = reason
    updated["trust_updated_at"] = utc_now_iso()
    if source_ref:
        updated["source_ref"] = source_ref
    return updated


def promote_fact(
    properties: dict[str, Any],
    target_state: TrustState | str,
    *,
    rule_id: str | None = None,
    approver: str | None = None,
    confidence: float | None = None,
) -> dict[str, Any]:
    """Promote a fact only when a rule, approval, or confidence signal exists."""

    target = normalize_trust_state(target_state)
    if target in {TrustState.TRUSTED, TrustState.CERTIFIED, TrustState.REVIEWED}:
        if not (rule_id or approver or (confidence is not None and confidence >= 0.8)):
            raise ValueError("trust promotion requires rule_id, approver, or confidence >= 0.8")
    updated = dict(properties)
    updated["trust_state"] = target.value
    updated["quarantine"] = False
    updated["trust_rule_id"] = rule_id
    updated["trust_approver"] = approver
    updated["trust_confidence"] = confidence
    updated["trust_updated_at"] = utc_now_iso()
    return updated


def trust_disclosure(evidence_items: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize trust levels used by an answer without exposing chain-of-thought."""

    states = [
        normalize_trust_state(
            item.get("trust_state"),
            creation_status=item.get("creation_status"),
        )
        for item in evidence_items
    ]
    non_certified = [state.value for state in states if state != TrustState.CERTIFIED]
    rejected = [state.value for state in states if state == TrustState.REJECTED]
    return {
        "states": sorted({state.value for state in states}),
        "uses_non_certified_knowledge": bool(non_certified),
        "uses_rejected_knowledge": bool(rejected),
        "minimum_state": min(states, key=lambda state: _TRUST_RANK[state]).value if states else None,
    }
