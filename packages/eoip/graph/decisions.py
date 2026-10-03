"""Decision graph service (G2-T0610..0612, G2-GRAPH-DEC-001..003).

Extracts decisions from structured documents, manages the decision model,
and links decisions to architecture/code/releases.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from eoip.graph.store import GraphStore


def extract_decisions_from_document(store: GraphStore, document_cid: str) -> list[dict]:
    """Extract ADR-style decisions from a document's content.

    Looks for structured patterns: "Decision:", "Status:", "Context:",
    "Alternatives:", "Consequences:" headings typical of ADRs.
    """
    doc = store.get_vertex_by_canonical_id(document_cid)
    if not doc:
        return []

    content = doc["properties"].get("description", "") or ""
    payload = doc["properties"].get("payload_json", "")
    if payload:
        content = f"{content}\n{payload}"

    if not content.strip():
        return []

    decisions: list[dict] = []
    adr_pattern = re.compile(
        r"(?:^|\n)#+\s*(?:ADR|Decision)[\s:\-]*(\d*)\s*[:\-]?\s*(.+?)(?:\n|$)",
        re.IGNORECASE,
    )
    for match in adr_pattern.finditer(content):
        adr_num = match.group(1).strip() if match.group(1) else str(len(decisions) + 1)
        title = match.group(2).strip()

        status_match = re.search(
            r"(?:^|\n)\*?\*?Status\*?\*?\s*[:\-]\s*(.+?)(?:\n|$)",
            content[match.start():],
            re.IGNORECASE,
        )
        status = status_match.group(1).strip() if status_match else "Proposed"

        context_match = re.search(
            r"(?:^|\n)\*?\*?(?:Context|Background)\*?\*?\s*[:\-]\s*(.+?)(?:\n(?:##|$))",
            content[match.start():],
            re.IGNORECASE | re.DOTALL,
        )
        rationale = context_match.group(1).strip()[:500] if context_match else ""

        decisions.append({
            "adr_number": adr_num,
            "title": title,
            "status": status,
            "rationale": rationale,
            "source_document": document_cid,
        })

    return decisions


def ingest_decision(
    store: GraphStore,
    name: str,
    *,
    rationale: str = "",
    status: str = "Proposed",
    constraints: str = "",
    alternatives: list[dict] | None = None,
    linked_entities: list[str] | None = None,
    source_document: str | None = None,
    ingestion_run_id: str = "manual",
) -> dict:
    """Create or update a Decision vertex with its alternatives and links."""
    now = datetime.now(timezone.utc).isoformat()
    cid = f"urn:eoip:decision:{name.lower().replace(' ', '-')}"

    decision = store.upsert_vertex("Decision", {
        "canonical_id": cid,
        "name": name,
        "rationale": rationale,
        "decision_status": status,
        "constraints": constraints,
        "ingestion_run_id": ingestion_run_id,
        "created_at": now,
    })

    created_alternatives: list[dict] = []
    for alt in (alternatives or []):
        alt_cid = f"{cid}:alt:{alt['name'].lower().replace(' ', '-')}"
        alt_v = store.upsert_vertex("Alternative", {
            "canonical_id": alt_cid,
            "name": alt["name"],
            "description": alt.get("description", ""),
            "rationale": alt.get("rationale", ""),
            "outcome": alt.get("outcome", ""),
            "ingestion_run_id": ingestion_run_id,
        })
        store.upsert_edge("HAS_ALTERNATIVE", decision["vid"], alt_v["vid"], {
            "fact_key": f"alt:{cid}:{alt_cid}",
            "creation_status": "DETERMINISTIC",
        })
        created_alternatives.append(alt_v)

    linked: list[dict] = []
    for entity_cid in (linked_entities or []):
        target = store.get_vertex_by_canonical_id(entity_cid)
        if not target:
            continue
        spec = ("DECIDES", target)
        if target["label"] in (s for s in ["File", "CodeSymbol", "Service", "APIService", "APIEndpoint", "Deployment", "Repository"]):
            store.upsert_edge("DECIDES", decision["vid"], target["vid"], {
                "fact_key": f"decides:{cid}:{entity_cid}",
                "creation_status": "DETERMINISTIC",
            })
            linked.append({"canonical_id": entity_cid, "edge": "DECIDES"})
        else:
            store.upsert_edge("TRACES_TO", decision["vid"], target["vid"], {
                "fact_key": f"traces:{cid}:{entity_cid}",
                "creation_status": "DETERMINISTIC",
            })
            linked.append({"canonical_id": entity_cid, "edge": "TRACES_TO"})

    if source_document:
        doc = store.get_vertex_by_canonical_id(source_document)
        if doc:
            store.upsert_edge("EVIDENCED_BY", decision["vid"], doc["vid"], {
                "fact_key": f"evidence:{cid}:{source_document}",
                "creation_status": "DETERMINISTIC",
            }) if doc["label"] == "Evidence" else None

    return {
        "decision": decision,
        "alternatives": created_alternatives,
        "linked_entities": linked,
    }


def find_decisions_for_entity(store: GraphStore, entity_cid: str) -> list[dict]:
    """Find all decisions that affect a given entity (DECIDES or TRACES_TO edges)."""
    entity = store.get_vertex_by_canonical_id(entity_cid)
    if not entity:
        return []

    edges = store.find_edges(in_v=entity["vid"], limit=1000)
    decisions: list[dict] = []
    for edge in edges:
        if edge["label"] in ("DECIDES", "TRACES_TO"):
            src = store.get_vertex(edge["out_v"])
            if src and src["label"] == "Decision":
                alt_edges = store.find_edges(out_v=src["vid"], limit=100)
                alts = []
                for ae in alt_edges:
                    if ae["label"] == "HAS_ALTERNATIVE":
                        alt = store.get_vertex(ae["in_v"])
                        if alt:
                            alts.append({
                                "canonical_id": alt["canonical_id"],
                                "name": alt["properties"].get("name", ""),
                            })
                decisions.append({
                    "canonical_id": src["canonical_id"],
                    "name": src["properties"].get("name", ""),
                    "status": src["properties"].get("decision_status", ""),
                    "rationale": src["properties"].get("rationale", ""),
                    "alternatives": alts,
                    "edge_type": edge["label"],
                })
    return decisions
