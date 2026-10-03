"""Causal hypothesis engine (G2-T0920..0924, G2-CAUSE-001..006).

Generates evidence-grounded causal hypotheses from temporal graph data.
Never emits HUMAN_CONFIRMED_CAUSE automatically — all hypotheses require
explicit human reviewer confirmation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from eoip.graph.store import GraphStore

TEMPORAL_FIELDS = ("created_at", "modified_at", "event_timestamp", "started_at", "observed_at")
CAUSAL_EDGE_LABELS = ("TRIGGERED_BY", "RESOLVES", "CORRELATES_WITH", "IMPLEMENTS", "MODIFIES")
VALID_HYPOTHESIS_STATUSES = ("CORRELATION", "HYPOTHESIS", "NEEDS_REVIEW", "REJECTED")


@dataclass
class CausalHypothesis:
    hypothesis_id: str
    cause_cid: str
    effect_cid: str
    cause_label: str = ""
    effect_label: str = ""
    status: str = "CORRELATION"
    confidence: float = 0.0
    temporal_distance_seconds: float = 0.0
    evidence: list[dict[str, Any]] = field(default_factory=list)
    alternatives: list[dict[str, Any]] = field(default_factory=list)
    reviewer_notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "cause": {"canonical_id": self.cause_cid, "label": self.cause_label},
            "effect": {"canonical_id": self.effect_cid, "label": self.effect_label},
            "status": self.status,
            "confidence": self.confidence,
            "temporal_distance_seconds": self.temporal_distance_seconds,
            "evidence": self.evidence,
            "alternatives": self.alternatives,
            "reviewer_notes": self.reviewer_notes,
        }


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.fromisoformat(value)
        except (ValueError, AttributeError):
            continue
    return None


def _get_timestamp(vertex: dict) -> datetime | None:
    props = vertex.get("properties", {})
    for f in TEMPORAL_FIELDS:
        ts = _parse_timestamp(props.get(f))
        if ts:
            return ts
    return None


def find_temporal_correlations(
    store: GraphStore,
    entity_cid: str,
    time_window_hours: float = 24.0,
) -> list[dict[str, Any]]:
    """Find entities temporally correlated with the given entity (G2-T0920)."""
    entity = store.get_vertex_by_canonical_id(entity_cid)
    if not entity:
        return []
    entity_ts = _get_timestamp(entity)
    if not entity_ts:
        return []

    window_secs = time_window_hours * 3600
    correlations: list[dict[str, Any]] = []

    in_edges = store.find_edges(in_v=entity["vid"], limit=500)
    out_edges = store.find_edges(out_v=entity["vid"], limit=500)
    neighbor_vids: set[str] = set()
    for e in in_edges:
        neighbor_vids.add(e["out_v"])
    for e in out_edges:
        neighbor_vids.add(e["in_v"])

    for vid in neighbor_vids:
        neighbor = store.get_vertex(vid)
        if not neighbor:
            continue
        n_ts = _get_timestamp(neighbor)
        if not n_ts:
            continue
        delta = abs((n_ts - entity_ts).total_seconds())
        if delta <= window_secs:
            correlations.append({
                "canonical_id": neighbor["canonical_id"],
                "label": neighbor["label"],
                "timestamp": n_ts.isoformat(),
                "temporal_distance_seconds": delta,
                "direction": "before" if n_ts < entity_ts else "after" if n_ts > entity_ts else "simultaneous",
            })

    correlations.sort(key=lambda c: c["temporal_distance_seconds"])
    return correlations


def check_causal_prerequisites(
    store: GraphStore,
    cause_cid: str,
    effect_cid: str,
) -> dict[str, Any]:
    """Check whether cause precedes effect and supporting evidence exists (G2-T0921)."""
    cause = store.get_vertex_by_canonical_id(cause_cid)
    effect = store.get_vertex_by_canonical_id(effect_cid)
    if not cause or not effect:
        missing = []
        if not cause:
            missing.append(cause_cid)
        if not effect:
            missing.append(effect_cid)
        return {"valid": False, "reason": "entity_not_found", "missing": missing}

    cause_ts = _get_timestamp(cause)
    effect_ts = _get_timestamp(effect)
    time_order_ok = True
    temporal_distance: float | None = None
    if cause_ts and effect_ts:
        time_order_ok = cause_ts <= effect_ts
        temporal_distance = (effect_ts - cause_ts).total_seconds()

    direct_edges = store.find_edges(out_v=cause["vid"], in_v=effect["vid"], limit=100)
    reverse_edges = store.find_edges(out_v=effect["vid"], in_v=cause["vid"], limit=100)
    causal_edges = [e for e in direct_edges if e["label"] in CAUSAL_EDGE_LABELS]
    reverse_causal = [e for e in reverse_edges if e["label"] in CAUSAL_EDGE_LABELS]

    evidence_chain: list[dict[str, str]] = []
    for e in causal_edges:
        evidence_chain.append({"edge": e["label"], "direction": "cause->effect"})
    for e in reverse_causal:
        evidence_chain.append({"edge": e["label"], "direction": "effect->cause"})

    has_evidence = len(evidence_chain) > 0
    confidence = 0.0
    if time_order_ok and has_evidence:
        confidence = 0.7
    elif time_order_ok:
        confidence = 0.3
    elif has_evidence:
        confidence = 0.2

    return {
        "valid": time_order_ok,
        "time_order_ok": time_order_ok,
        "temporal_distance_seconds": temporal_distance,
        "has_evidence": has_evidence,
        "evidence_chain": evidence_chain,
        "confidence": confidence,
    }


def generate_hypotheses(
    store: GraphStore,
    incident_cid: str,
    time_window_hours: float = 24.0,
    max_hypotheses: int = 10,
) -> dict[str, Any]:
    """Generate causal hypotheses for an incident from temporal correlations (G2-T0920..0924).

    All hypotheses start as CORRELATION or HYPOTHESIS — never HUMAN_CONFIRMED_CAUSE.
    """
    incident = store.get_vertex_by_canonical_id(incident_cid)
    if not incident:
        return {"incident": incident_cid, "hypotheses": [], "error": "Incident not found"}

    correlations = find_temporal_correlations(store, incident_cid, time_window_hours)
    before_events = [c for c in correlations if c["direction"] == "before"]

    hypotheses: list[CausalHypothesis] = []
    for i, corr in enumerate(before_events[:max_hypotheses]):
        prereq = check_causal_prerequisites(store, corr["canonical_id"], incident_cid)
        status = "HYPOTHESIS" if prereq["confidence"] >= 0.5 else "CORRELATION"

        alternatives = []
        for other in before_events:
            if other["canonical_id"] != corr["canonical_id"]:
                alternatives.append({
                    "canonical_id": other["canonical_id"],
                    "label": other["label"],
                    "temporal_distance_seconds": other["temporal_distance_seconds"],
                })

        h = CausalHypothesis(
            hypothesis_id=f"hyp-{i:03d}",
            cause_cid=corr["canonical_id"],
            effect_cid=incident_cid,
            cause_label=corr["label"],
            effect_label=incident["label"],
            status=status,
            confidence=prereq["confidence"],
            temporal_distance_seconds=corr["temporal_distance_seconds"],
            evidence=prereq.get("evidence_chain", []),
            alternatives=alternatives[:5],
        )
        hypotheses.append(h)

    hypotheses.sort(key=lambda h: h.confidence, reverse=True)

    return {
        "incident": incident_cid,
        "incident_label": incident["label"],
        "total_correlations": len(correlations),
        "hypotheses": [h.to_dict() for h in hypotheses],
        "total_hypotheses": len(hypotheses),
        "status_note": "All hypotheses require human review — HUMAN_CONFIRMED_CAUSE is never emitted automatically.",
    }


def review_hypothesis(hypothesis: CausalHypothesis, decision: str, notes: str = "") -> CausalHypothesis:
    """Apply a reviewer's decision to a hypothesis (G2-T0923..0924).

    Allowed decisions: HYPOTHESIS, NEEDS_REVIEW, REJECTED.
    HUMAN_CONFIRMED_CAUSE is only set through this explicit review path.
    """
    allowed = {"HYPOTHESIS", "NEEDS_REVIEW", "REJECTED", "HUMAN_CONFIRMED_CAUSE"}
    if decision not in allowed:
        raise ValueError(f"Invalid decision: {decision}. Allowed: {allowed}")
    hypothesis.status = decision
    hypothesis.reviewer_notes = notes
    return hypothesis
