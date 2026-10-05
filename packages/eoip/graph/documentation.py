"""Evidence-backed documentation links and referenced-fact freshness."""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Callable

from eoip.contracts.source_event import SourceEventV2
from eoip.graph.evolution import GraphEvolutionEngine
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import DOCUMENT_TARGET_LABELS

log = logging.getLogger(__name__)
_OBSERVATION_KEYS = {
    "canonical_id", "source_system", "source_id", "registry_source_id", "source_version",
    "mapper_version", "parser_version", "ontology_version", "schema_version",
    "ingestion_run_id", "first_seen", "last_seen", "created_at", "modified_at",
    "valid_from", "valid_to", "deleted_at", "graph_version", "graph_domain", "entity_type",
    "creation_status", "confidence",
}


def technical_fingerprint(vertex: dict) -> str:
    ignored = _OBSERVATION_KEYS
    if vertex["label"] not in {"File", "CodeSymbol"}:
        ignored = ignored | {"content_hash"}
    state = {
        "label": vertex["label"],
        "properties": {key: value for key, value in vertex["properties"].items() if key not in ignored},
    }
    return hashlib.sha256(json.dumps(state, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _resolve_reference(store: GraphStore, reference: str) -> dict | None:
    if reference.startswith("urn:eoip:"):
        target = store.get_vertex_by_canonical_id(reference)
        return target if (
            target and target["label"] in DOCUMENT_TARGET_LABELS
        ) else None
    candidates = {}
    for label in DOCUMENT_TARGET_LABELS:
        for key in ("url", "path", "source_uri"):
            for vertex in store.find_vertex_by_property(label, key, reference, limit=2):
                candidates[vertex["canonical_id"]] = vertex
    if len(candidates) > 1:
        log.warning("ambiguous documentation reference", extra={"candidate_count": len(candidates)})
    return next(iter(candidates.values())) if len(candidates) == 1 else None


def reconcile_document_references(
    store: GraphStore, evolution: GraphEvolutionEngine, document: dict,
    event: SourceEventV2, evidence_properties: dict,
) -> None:
    structure = json.loads(document["properties"]["payload_json"])
    existing = store.find_edges(label="DOCUMENTS", out_v=document["vid"], limit=10_001)
    if len(existing) > 10_000:
        raise ValueError("document reference reconciliation exceeds 10000 relationships")
    existing = {edge["in_cid"]: edge for edge in existing
                if edge["properties"].get("parser_version") == "document-reference/1.0"}
    resolved = {}
    if len(structure["links"]) > 10_000:
        raise ValueError("document reference reconciliation exceeds 10000 source links")
    for link in ([] if event.operation == "DELETE" else structure["links"]):
        if link["kind"] not in {"entity", "internal", "external"}:
            continue
        reference = link["target"]
        target = _resolve_reference(store, reference)
        if target:
            resolved.setdefault(target["canonical_id"], (target, reference))
    for target_id, (target, reference) in resolved.items():
        previous = existing.get(target_id)
        if previous:
            baseline = json.loads(previous["properties"]["payload_json"])
            if event.operation != "DELETE" and baseline["document_content_hash"] == event.content_hash:
                # Replaying the same document cannot certify newly changed target facts.
                continue
        fact_key = f"document-reference:{document['canonical_id']}:{target_id}"
        evolution.evolve_relationship(
            fact_key, "DOCUMENTS", document["canonical_id"], target_id,
            {
                **evidence_properties, "parser_version": "document-reference/1.0",
                "payload_json": json.dumps({
                    "schema_version": "1.0", "matched_reference": reference,
                    "document_content_hash": event.content_hash,
                    "target_fingerprint": technical_fingerprint(target),
                }, sort_keys=True),
            },
            event,
        )
    for target_id, edge in existing.items():
        if target_id not in resolved:
            baseline = json.loads(edge["properties"]["payload_json"])
            if event.operation != "DELETE" and baseline["document_content_hash"] == event.content_hash:
                continue
            evolution.evolve_relationship(
                edge["properties"]["fact_key"], "DOCUMENTS", document["canonical_id"], target_id,
                edge["properties"], event.model_copy(update={"operation": "DELETE"}),
            )


def document_reference_findings(
    store: GraphStore, edges: list[dict], *, get_vertex: Callable[[str], dict | None] | None = None,
) -> list[dict]:
    get_vertex = get_vertex or store.get_vertex
    findings = []
    for edge in edges:
        properties = edge["properties"]
        if (
            edge["label"] != "DOCUMENTS" or properties.get("is_current") is False
            or properties.get("parser_version") != "document-reference/1.0"
        ):
            continue
        baseline = json.loads(properties["payload_json"])
        target = get_vertex(edge["in_v"])
        document = get_vertex(edge["out_v"])
        if document is None or document["properties"].get("deleted_at"):
            continue
        if target is None:
            reason = "target_missing"
        elif target["properties"].get("deleted_at"):
            reason = "target_deleted"
        elif technical_fingerprint(target) != baseline["target_fingerprint"]:
            reason = "target_changed"
        else:
            continue
        findings.append({
            "canonical_id": document["canonical_id"], "edge_id": edge["eid"],
            "target_id": edge["in_cid"], "rule": "stale_document_reference",
            "reason": reason, "severity": "WARNING",
            "evidence_key": properties["evidence_key"],
            "detail": f"Referenced technical fact requires documentation review: {edge['in_cid']} ({reason})",
            "remediation": "Review the referenced fact and ingest a new source document version.",
        })
    return findings
