"""Validated ingestion pipeline: canonical contracts at process boundaries (P1-19).

Every graph mutation routes through NormalizedEntity/NormalizedRelationship
validation before reaching the store, ensuring schema conformance at the
map→store boundary.
"""

from __future__ import annotations

from uuid import uuid4

from eoip.contracts.graph_mutation import GraphMutation
from eoip.contracts.normalized import NormalizedEntity, NormalizedRelationship
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import VERTEX_LABELS


def validate_and_write_entity(
    store: GraphStore,
    label: str,
    canonical_id: str,
    properties: dict,
    source_refs: list[str] | None = None,
    ingestion_run_id: str | None = None,
    creation_status: str = "DETERMINISTIC",
) -> dict:
    """Validate an entity through NormalizedEntity before writing to the store."""
    spec = VERTEX_LABELS.get(label)
    domain = spec[0] if spec else "META"
    entity = NormalizedEntity(
        canonical_id=canonical_id,
        entity_type=label,
        graph_domain=domain,
        source_refs=source_refs or [],
        creation_status=creation_status,
        properties=properties,
    )
    GraphMutation(
        mutation_id=str(uuid4()),
        operation="UPSERT",
        target_kind="VERTEX",
        payload=entity.model_dump(),
        ingestion_run_id=ingestion_run_id or "",
    )
    return store.upsert_vertex(label, {"canonical_id": canonical_id, **properties})


def validate_and_write_relationship(
    store: GraphStore,
    label: str,
    from_id: str,
    to_id: str,
    properties: dict,
    evidence_refs: list[str] | None = None,
    ingestion_run_id: str | None = None,
    creation_status: str = "DETERMINISTIC",
) -> dict:
    """Validate a relationship through NormalizedRelationship before writing."""
    rel = NormalizedRelationship(
        relationship_id=f"{label}:{from_id}:{to_id}",
        relationship_type=label,
        from_id=from_id,
        to_id=to_id,
        evidence_refs=evidence_refs or [],
        creation_status=creation_status,
        properties=properties,
    )
    GraphMutation(
        mutation_id=str(uuid4()),
        operation="UPSERT",
        target_kind="EDGE",
        payload=rel.model_dump(),
        ingestion_run_id=ingestion_run_id or "",
    )
    return store.upsert_edge(label, from_id, to_id, properties)
