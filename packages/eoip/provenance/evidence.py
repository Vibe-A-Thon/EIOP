"""Evidence service (FR-PROV-001).

Creates and retrieves evidence vertices linked to canonical facts.
Every cross-domain edge should have an evidence reference.
"""

from __future__ import annotations

import hashlib
import json

from eoip.contracts.source_event import SourceEvent, utc_now_iso
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION


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

    @staticmethod
    def hash_payload(payload: object) -> str:
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(serialized).hexdigest()
