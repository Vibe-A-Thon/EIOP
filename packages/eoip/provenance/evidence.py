"""Evidence service (FR-PROV-001).

Creates and retrieves evidence vertices linked to canonical facts.
Every cross-domain edge should have an evidence reference.

Implements:
- GAP-PROV-001: every fact can reference provenance.
- GAP-PROV-002: evidence records preserve source, capture, mapper, and content hash data.
- GAP-PROV-003: graph facts can link to evidence vertices.
- GAP-PROV-004: evidence coverage is measurable.
- GAP-PROV-006: AI answers can emit evidence manifests.
- GAP-AI-001: answers are evidence-addressable to graph nodes, paths, and source records.
- GAP-KRAG-007: GraphRAG outputs include machine-readable evidence.
- GAP-GRAG-006: evidence chains are persisted with every answer.
- Section 50 explainability: evidence, provenance, query plan, confidence, and freshness.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from eoip.contracts.source_event import SourceEvent
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION
from eoip.provenance.trust import trust_disclosure


@dataclass(frozen=True)
class EvidenceManifest:
    """Machine-readable evidence bundle for query, retrieval, and agent answers."""

    answer_id: str
    evidence_refs: list[str]
    node_refs: list[str] = field(default_factory=list)
    edge_refs: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)
    graph_version: str = SCHEMA_VERSION
    ontology_version: str = ONTOLOGY_VERSION
    query_plan: dict | None = None
    tool_calls: list[dict] = field(default_factory=list)
    rules_fired: list[dict] = field(default_factory=list)
    confidence_inputs: list[dict] = field(default_factory=list)
    trust: dict = field(default_factory=dict)
    source_freshness: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "answer_id": self.answer_id,
            "evidence_refs": self.evidence_refs,
            "node_refs": self.node_refs,
            "edge_refs": self.edge_refs,
            "source_refs": self.source_refs,
            "graph_version": self.graph_version,
            "ontology_version": self.ontology_version,
            "query_plan": self.query_plan,
            "tool_calls": self.tool_calls,
            "rules_fired": self.rules_fired,
            "confidence_inputs": self.confidence_inputs,
            "trust": self.trust,
            "source_freshness": self.source_freshness,
        }


class EvidenceService:
    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def create_evidence(
        self,
        event: SourceEvent,
        *,
        method: str = "SOURCE_EVENT",
        ingestion_run_id: str | None = None,
    ) -> dict:
        evidence_cid = f"urn:eoip:evidence:source-event:{event.source_system}:{event.event_id}"
        return self._store.upsert_vertex(
            "Evidence",
            {
                "canonical_id": evidence_cid,
                "source_system": event.source_system,
                "source_ref": f"{event.source_system}://{event.source_record_id}",
                "source_id": event.source_record_id,
                "source_version": event.source_version,
                "method": method,
                "captured_at": event.captured_at,
                "evidence_key": event.event_id,
                "content_hash": event.payload_hash,
                "mapper_version": getattr(event, "mapper_version", None),
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
            },
        )

    def link_evidence(
        self,
        entity_vid: str,
        evidence_vid: str,
        *,
        fact_key: str,
        evidence_key: str,
        source_ref: str,
        source_system: str,
        ingestion_run_id: str | None = None,
    ) -> dict:
        return self._store.upsert_edge(
            "EVIDENCED_BY",
            entity_vid,
            evidence_vid,
            {
                "fact_key": fact_key,
                "evidence_key": evidence_key,
                "source_ref": source_ref,
                "source_system": source_system,
                "ingestion_run_id": ingestion_run_id,
                "creation_status": "DETERMINISTIC",
            },
        )

    def coverage(self) -> dict:
        vertices = self._store.find_vertices(limit=100_000)
        meta_labels = {
            "IngestionRun", "GraphDomain", "OntologyVersion",
            "ValidationRun", "ValidationFinding", "DataSource", "Evidence",
        }
        business = [v for v in vertices if v["label"] not in meta_labels]
        with_evidence = 0
        for vertex in business:
            edges = self._store.edges_from(vertex["vid"], labels=["EVIDENCED_BY"])
            if edges:
                with_evidence += 1
        return {
            "total_entities": len(business),
            "with_evidence": with_evidence,
            "coverage": round(with_evidence / len(business), 4) if business else 1.0,
        }

    def build_manifest(
        self,
        *,
        answer_id: str,
        node_ids: list[str] | None = None,
        edge_ids: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        query_plan: dict | None = None,
        tool_calls: list[dict] | None = None,
        rules_fired: list[dict] | None = None,
        confidence_inputs: list[dict] | None = None,
    ) -> EvidenceManifest:
        """Build an evidence manifest from graph nodes/edges and explicit refs."""

        nodes = [
            self._store.get_vertex_by_canonical_id(node_id) or self._store.get_vertex(node_id)
            for node_id in (node_ids or [])
        ]
        nodes = [node for node in nodes if node]
        edge_lookup = {edge["eid"]: edge for edge in self._store.find_edges(limit=100_000)}
        edges = [edge_lookup[edge_id] for edge_id in (edge_ids or []) if edge_id in edge_lookup]

        collected_evidence = set(evidence_refs or [])
        source_refs = set()
        freshness: dict[str, str] = {}
        trust_items: list[dict] = []

        for node in nodes:
            props = node["properties"]
            if props.get("source_ref"):
                source_refs.add(props["source_ref"])
            if props.get("captured_at"):
                freshness[node["canonical_id"]] = props["captured_at"]
            trust_items.append(props)
            for edge in self._store.edges_from(node["vid"], labels=["EVIDENCED_BY"], limit=100):
                collected_evidence.add(edge["in_cid"])
                if edge["properties"].get("source_ref"):
                    source_refs.add(edge["properties"]["source_ref"])
                trust_items.append(edge["properties"])

        for edge in edges:
            props = edge["properties"]
            for key in ("source_ref", "evidence_key"):
                if props.get(key):
                    collected_evidence.add(props[key])
            if props.get("source_ref"):
                source_refs.add(props["source_ref"])
            trust_items.append(props)

        return EvidenceManifest(
            answer_id=answer_id,
            evidence_refs=sorted(collected_evidence),
            node_refs=sorted({node["canonical_id"] for node in nodes}),
            edge_refs=sorted({edge["eid"] for edge in edges}),
            source_refs=sorted(source_refs),
            query_plan=query_plan,
            tool_calls=tool_calls or [],
            rules_fired=rules_fired or [],
            confidence_inputs=confidence_inputs or [],
            trust=trust_disclosure(trust_items),
            source_freshness=freshness,
        )

    @staticmethod
    def hash_payload(payload: object) -> str:
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(serialized).hexdigest()
