"""Expertise inference and documentation freshness (GAP-REC-001, GAP-FRESH-001..005).

Expertise is inferred only from explicit graph evidence (commit authorship,
work-item assignment) — weighted and recency-aware, never from sensitive
attributes. Freshness compares a document's capture time with the most recent
modification of the entities it references, flagging potentially stale
documentation for human review (never silently rewritten).
"""

from __future__ import annotations

from datetime import datetime
from time import time
from typing import Any

_RECENCY_HALFLIFE_DAYS = 180


def _iso_age_days(value: str | None, now_days: float) -> float | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    return max(0.0, now_days - parsed.timestamp() / 86400.0)


def _component_neighbors(store, component_cid: str) -> set[str]:
    """The component itself plus every canonical id directly connected to it."""
    vertex = store.get_vertex_by_canonical_id(component_cid)
    neighbors = {component_cid}
    if vertex is None:
        return neighbors
    for edge in store.edges_from(vertex["vid"], limit=500):
        neighbors.add(edge["in_cid"])
    for edge in store.edges_to(vertex["vid"], limit=500):
        neighbors.add(edge["out_cid"])
    return neighbors


def find_experts(store, component_cid: str, *, limit: int = 10) -> dict[str, Any]:
    """Rank candidate experts for a component from explicit authorship/assignment evidence."""
    if store.get_vertex_by_canonical_id(component_cid) is None:
        raise ValueError(f"entity not found: {component_cid}")
    now = time() / 86400.0
    neighbors = _component_neighbors(store, component_cid)
    scores: dict[str, dict[str, Any]] = {}

    for edge in store.find_edges(limit=20_000, include_historical=False):
        if edge["label"] not in {"AUTHORED_BY", "ASSIGNED_TO"}:
            continue
        if edge["out_cid"] not in neighbors:
            continue
        person = store.get_vertex_by_canonical_id(edge["in_cid"])
        if person is None or person["label"] != "Person":
            continue
        subject = store.get_vertex_by_canonical_id(edge["out_cid"])
        when = None
        if subject is not None:
            when = (
                subject["properties"].get("created_at")
                if edge["label"] == "AUTHORED_BY"
                else subject["properties"].get("modified_at")
            )
        age = _iso_age_days(when, now)
        recency = 0.5 ** ((age if age is not None else 365.0) / _RECENCY_HALFLIFE_DAYS)
        weight = 1.0 if edge["label"] == "AUTHORED_BY" else 0.7
        entry = scores.setdefault(
            edge["in_cid"],
            {
                "person_cid": edge["in_cid"],
                "display_name": person["properties"].get("display_name", edge["in_cid"]),
                "score": 0.0,
                "evidence": [],
            },
        )
        entry["score"] += weight * recency
        entry["evidence"].append(
            {"basis": edge["label"], "via": edge["out_cid"], "recency": round(recency, 3)}
        )

    ranked = sorted(scores.values(), key=lambda item: item["score"], reverse=True)[:limit]
    for entry in ranked:
        entry["score"] = round(entry["score"], 3)
    return {"component_cid": component_cid, "experts": ranked}


def freshness_report(store, *, stale_days: int = 90) -> dict[str, Any]:
    """Flag documents whose referenced entities changed long after capture."""
    now = time() / 86400.0
    rows = []
    for document in store.find_vertices(label="Document", limit=5_000):
        props = document["properties"]
        doc_age = _iso_age_days(props.get("last_seen") or props.get("modified_at"), now)
        latest_reference_change = None
        for edge in store.edges_from(document["vid"], limit=200):
            if edge["label"] not in {"REFERENCES", "DOCUMENTS"}:
                continue
            target = store.get_vertex_by_canonical_id(edge["in_cid"])
            if target is None:
                continue
            age = _iso_age_days(
                target["properties"].get("modified_at") or target["properties"].get("last_seen"),
                now,
            )
            if age is not None and (latest_reference_change is None or age < latest_reference_change):
                latest_reference_change = age
        stale = (
            doc_age is not None
            and latest_reference_change is not None
            and (doc_age - latest_reference_change) > stale_days
        )
        rows.append(
            {
                "canonical_id": document["canonical_id"],
                "name": props.get("name"),
                "stale": stale,
                "document_age_days": None if doc_age is None else round(doc_age, 1),
                "reference_changed_days_ago": (
                    None if latest_reference_change is None else round(latest_reference_change, 1)
                ),
                "recommendation": (
                    "human review recommended — referenced facts changed after capture"
                    if stale
                    else "fresh"
                ),
            }
        )
    return {
        "documents": rows,
        "stale_count": len([row for row in rows if row["stale"]]),
        "policy_stale_days": stale_days,
    }
