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


def detect_contradictions(store, *, document_cid: str | None = None) -> list[dict[str, Any]]:
    """Detect documents whose claimed properties contradict code/config/runtime (GAP-FRESH-002)."""
    import json

    docs = (
        [store.get_vertex_by_canonical_id(document_cid)]
        if document_cid
        else store.find_vertices(label="Document", limit=5_000)
    )
    contradictions = []

    for doc in docs:
        if not doc:
            continue
        props = doc["properties"]
        doc_cid = doc["canonical_id"]

        # Parse claims from payload_json or description
        claims: dict[str, Any] = {}
        payload_raw = props.get("payload_json")
        if payload_raw:
            try:
                payload = json.loads(payload_raw) if isinstance(payload_raw, str) else payload_raw
                if isinstance(payload, dict):
                    claims = payload.get("claims", payload)
            except Exception:
                pass

        # Inspect target components connected via DOCUMENTS or REFERENCES
        for edge in store.edges_from(doc["vid"], limit=200):
            if edge["label"] not in {"DOCUMENTS", "REFERENCES", "DOCUMENTS_API"}:
                continue
            target = store.get_vertex_by_canonical_id(edge["in_cid"])
            if not target:
                continue

            target_props = target["properties"]
            target_cid = target["canonical_id"]

            # 1. Status claim contradictions (e.g. doc claims status='active', target is 'deprecated' or 'inactive')
            claimed_status = claims.get("status") or claims.get(f"{target_cid}.status")
            actual_status = target_props.get("status")
            if claimed_status and actual_status and str(claimed_status).upper() != str(actual_status).upper():
                contradictions.append({
                    "document_cid": doc_cid,
                    "target_cid": target_cid,
                    "target_label": target["label"],
                    "field": "status",
                    "doc_claimed": claimed_status,
                    "actual_state": actual_status,
                    "contradiction_type": "status_contradiction",
                    "evidence": f"Document claims status='{claimed_status}' for {target_cid}, but actual is '{actual_status}'",
                })

            # 2. Criticality / Tier contradiction
            claimed_crit = claims.get("criticality") or claims.get(f"{target_cid}.criticality")
            actual_crit = target_props.get("criticality")
            if claimed_crit and actual_crit and str(claimed_crit).upper() != str(actual_crit).upper():
                contradictions.append({
                    "document_cid": doc_cid,
                    "target_cid": target_cid,
                    "target_label": target["label"],
                    "field": "criticality",
                    "doc_claimed": claimed_crit,
                    "actual_state": actual_crit,
                    "contradiction_type": "config_contradiction",
                    "evidence": f"Document claims criticality='{claimed_crit}' for {target_cid}, but runtime is '{actual_crit}'",
                })

    return contradictions


def detect_ownership_drift(store, *, document_cid: str | None = None) -> list[dict[str, Any]]:
    """Detect ownership changes where document states an owner that no longer owns component (GAP-FRESH-003)."""
    import json

    docs = (
        [store.get_vertex_by_canonical_id(document_cid)]
        if document_cid
        else store.find_vertices(label="Document", limit=5_000)
    )
    drifts = []

    for doc in docs:
        if not doc:
            continue
        props = doc["properties"]
        doc_cid = doc["canonical_id"]

        doc_owner = props.get("owner") or props.get("author_name")
        if not doc_owner and props.get("payload_json"):
            try:
                p = json.loads(props["payload_json"]) if isinstance(props["payload_json"], str) else props["payload_json"]
                if isinstance(p, dict):
                    doc_owner = p.get("owner") or p.get("author")
            except Exception:
                pass

        if not doc_owner:
            continue

        for edge in store.edges_from(doc["vid"], limit=200):
            if edge["label"] not in {"DOCUMENTS", "REFERENCES"}:
                continue
            target = store.get_vertex_by_canonical_id(edge["in_cid"])
            if not target:
                continue

            target_cid = target["canonical_id"]
            # Current owner from target properties or ASSIGNED_TO
            current_owner = target["properties"].get("owner")
            if not current_owner:
                for t_edge in store.edges_from(target["vid"], limit=50):
                    if t_edge["label"] == "ASSIGNED_TO":
                        person = store.get_vertex_by_canonical_id(t_edge["in_cid"])
                        if person:
                            current_owner = person["properties"].get("display_name") or person["canonical_id"]
                            break

            if current_owner and current_owner != doc_owner:
                drifts.append({
                    "document_cid": doc_cid,
                    "component_cid": target_cid,
                    "component_label": target["label"],
                    "document_stated_owner": doc_owner,
                    "current_owner": current_owner,
                    "drift_detected": True,
                    "evidence": f"Document states owner '{doc_owner}', but current owner of {target_cid} is '{current_owner}'",
                })

    return drifts


def detect_deprecated_references(store, *, document_cid: str | None = None) -> list[dict[str, Any]]:
    """Detect deprecated APIs or symbols still referenced in documents (GAP-FRESH-004)."""
    docs = (
        [store.get_vertex_by_canonical_id(document_cid)]
        if document_cid
        else store.find_vertices(label="Document", limit=5_000)
    )
    deprecated = []

    for doc in docs:
        if not doc:
            continue
        doc_cid = doc["canonical_id"]

        for edge in store.edges_from(doc["vid"], limit=200):
            if edge["label"] not in {"DOCUMENTS", "REFERENCES", "DOCUMENTS_API"}:
                continue
            target = store.get_vertex_by_canonical_id(edge["in_cid"])
            if not target:
                continue

            target_props = target["properties"]
            status = str(target_props.get("status", "")).upper()
            is_dep = (
                status in {"DEPRECATED", "OBSOLETE", "RETIRED"}
                or target_props.get("is_deprecated") is True
                or "deprecated" in str(target_props.get("description", "")).lower()
            )

            if is_dep:
                deprecated.append({
                    "document_cid": doc_cid,
                    "api_cid": target["canonical_id"],
                    "api_label": target["label"],
                    "api_name": target_props.get("api_name") or target_props.get("name") or target["canonical_id"],
                    "status": target_props.get("status", "DEPRECATED"),
                    "evidence": f"Document references {target['label']} '{target['canonical_id']}' which is marked deprecated",
                })

    return deprecated


def recommend_document_reviews(
    store,
    *,
    document_cid: str | None = None,
    stale_days: int = 90,
) -> list[dict[str, Any]]:
    """Recommend review — not silently rewrite authoritative docs (GAP-FRESH-005).

    Generates structured review tickets with evidence, contradiction findings,
    and suggested reviewers without altering authoritative text.
    """
    f_rep = freshness_report(store, stale_days=stale_days)
    stale_by_doc = {r["canonical_id"]: r for r in f_rep["documents"] if r["stale"]}

    contradictions = detect_contradictions(store, document_cid=document_cid)
    contra_by_doc: dict[str, list] = {}
    for c in contradictions:
        contra_by_doc.setdefault(c["document_cid"], []).append(c)

    ownership_drifts = detect_ownership_drift(store, document_cid=document_cid)
    drift_by_doc: dict[str, list] = {}
    for d in ownership_drifts:
        drift_by_doc.setdefault(d["document_cid"], []).append(d)

    deprecated_refs = detect_deprecated_references(store, document_cid=document_cid)
    dep_by_doc: dict[str, list] = {}
    for dep in deprecated_refs:
        dep_by_doc.setdefault(dep["document_cid"], []).append(dep)

    all_flagged_cids = sorted(
        set(stale_by_doc.keys())
        | set(contra_by_doc.keys())
        | set(drift_by_doc.keys())
        | set(dep_by_doc.keys())
    )

    if document_cid:
        all_flagged_cids = [c for c in all_flagged_cids if c == document_cid]

    recommendations = []
    for cid in all_flagged_cids:
        doc = store.get_vertex_by_canonical_id(cid)
        doc_name = doc["properties"].get("name", cid) if doc else cid

        reasons = []
        if cid in stale_by_doc:
            reasons.append("stale_referenced_facts")
        if cid in contra_by_doc:
            reasons.append(f"contradictions_detected:{len(contra_by_doc[cid])}")
        if cid in drift_by_doc:
            reasons.append(f"ownership_drift_detected:{len(drift_by_doc[cid])}")
        if cid in dep_by_doc:
            reasons.append(f"deprecated_apis_referenced:{len(dep_by_doc[cid])}")

        # Suggest reviewers from candidate experts of documented components
        suggested_reviewers = []
        if doc:
            for edge in store.edges_from(doc["vid"], limit=50):
                if edge["label"] in {"DOCUMENTS", "REFERENCES"}:
                    try:
                        exp = find_experts(store, edge["in_cid"], limit=3)
                        suggested_reviewers.extend([e["display_name"] for e in exp["experts"]])
                    except Exception:
                        pass

        recommendations.append({
            "document_cid": cid,
            "name": doc_name,
            "action": "HUMAN_REVIEW_RECOMMENDED",
            "silent_rewrite_permitted": False,
            "reasons": reasons,
            "findings": {
                "stale_metadata": stale_by_doc.get(cid),
                "contradictions": contra_by_doc.get(cid, []),
                "ownership_drift": drift_by_doc.get(cid, []),
                "deprecated_references": dep_by_doc.get(cid, []),
            },
            "suggested_reviewers": sorted(set(suggested_reviewers))[:5],
            "governance_note": (
                "Authoritative documentation must NOT be silently rewritten by AI. "
                "Human review workflow initiated with verified graph evidence."
            ),
        })

    return recommendations
