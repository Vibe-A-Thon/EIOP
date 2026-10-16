"""Canonical map-to-store boundary for ingestion (P1-19).

Services use IngestionGraphStore, including their domain and temporal writes.
Administrative schema/reset/snapshot operations retain the underlying store's
semantics; normalized envelopes do not add properties to persisted projections.
"""

from __future__ import annotations

from contextvars import ContextVar
from uuid import uuid4

from eoip.contracts.graph_mutation import GraphMutation
from eoip.contracts.normalized import NormalizedEntity, NormalizedRelationship
from eoip.graph.memory import edge_key
from eoip.graph.store import GraphStore, Vertex
from eoip.ontology.manifest import VERTEX_LABELS
from eoip.validation.gate import MutationBlocked, check_edge, check_vertex


def _endpoint(store: GraphStore, identity: str) -> Vertex:
    vertex = store.get_vertex_by_canonical_id(identity)
    if vertex is None:
        vertex = store.get_vertex(identity)
    if vertex is None:
        raise MutationBlocked(f"missing relationship endpoint: {identity}")
    return vertex


def _entity_projection(entity: NormalizedEntity) -> dict:
    if (
        "canonical_id" in entity.properties
        and entity.properties["canonical_id"] != entity.canonical_id
    ):
        raise MutationBlocked("canonical_id conflicts with normalized identity", label=entity.entity_type)
    properties = {**entity.properties, "canonical_id": entity.canonical_id}
    check_vertex(entity.entity_type, properties)
    if entity.graph_domain != VERTEX_LABELS[entity.entity_type][0]:
        raise MutationBlocked("graph_domain conflicts with ontology", label=entity.entity_type)
    # EntityRevision properties intentionally retain the subject's entity_type.
    for key in ("graph_domain", "creation_status", "confidence"):
        if key in properties and properties[key] != getattr(entity, key):
            raise MutationBlocked(f"{key} conflicts with normalized envelope", label=entity.entity_type)
    return properties


def apply_graph_mutation(store: GraphStore, mutation: GraphMutation) -> dict | bool:
    """Consume a validated envelope; reject invalid proposals before store writes."""
    # Revalidate at the consumer, including callers passing a mutated model instance.
    mutation = GraphMutation.model_validate(mutation.model_dump())
    if mutation.target_kind == "VERTEX":
        entity = NormalizedEntity.model_validate(mutation.payload)
        properties = _entity_projection(entity)
        if mutation.operation == "TOMBSTONE":
            return store.tombstone_vertex(entity.canonical_id)
        return store.upsert_vertex(entity.entity_type, properties)

    if mutation.operation != "UPSERT":
        raise MutationBlocked("edge TOMBSTONE is unsupported; expire a temporal relationship instead")
    relationship = NormalizedRelationship.model_validate(mutation.payload)
    source = _endpoint(store, relationship.from_id)
    target = _endpoint(store, relationship.to_id)
    if source["canonical_id"] != relationship.from_id or target["canonical_id"] != relationship.to_id:
        raise MutationBlocked("normalized relationship endpoints must be canonical IDs")
    properties = relationship.properties or {}
    check_edge(relationship.relationship_type, source["label"], target["label"], properties)
    expected_key = properties.get("edge_key") or edge_key(
        relationship.relationship_type, relationship.from_id, relationship.to_id,
        properties.get("fact_key", ""),
    )
    if relationship.relationship_id != expected_key:
        raise MutationBlocked("relationship_id conflicts with fact identity")
    for key in ("creation_status", "confidence"):
        if key in properties and properties[key] != getattr(relationship, key):
            raise MutationBlocked(f"{key} conflicts with normalized envelope")
    return store.upsert_edge(
        relationship.relationship_type, source["vid"], target["vid"], properties
    )


def validate_and_write_entity(
    store: GraphStore,
    label: str,
    canonical_id: str,
    properties: dict,
    source_refs: list[str] | None = None,
    ingestion_run_id: str | None = None,
    creation_status: str = "DETERMINISTIC",
) -> dict:
    """Normalize and consume an entity mutation, preserving its graph projection."""
    if ingestion_run_id is None:
        raise ValueError("ingestion_run_id is required")
    check_vertex(label, {**properties, "canonical_id": canonical_id})
    entity = NormalizedEntity.model_validate(
        {
            "canonical_id": canonical_id,
            "entity_type": label,
            "graph_domain": VERTEX_LABELS[label][0],
            "source_refs": source_refs if source_refs is not None else [],
            "creation_status": properties.get("creation_status", creation_status),
            "confidence": properties.get("confidence"),
            "properties": properties,
        }
    )
    mutation = GraphMutation(
        mutation_id=str(uuid4()), operation="UPSERT", target_kind="VERTEX",
        payload=entity.model_dump(), ingestion_run_id=ingestion_run_id,
    )
    result = apply_graph_mutation(store, mutation)
    if isinstance(result, bool):
        raise TypeError("entity UPSERT unexpectedly returned a tombstone result")
    return result


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
    """Resolve physical IDs before building the canonical relationship envelope."""
    if ingestion_run_id is None:
        raise ValueError("ingestion_run_id is required")
    source, target = _endpoint(store, from_id), _endpoint(store, to_id)
    relationship = NormalizedRelationship.model_validate(
        {
            "relationship_id": properties.get("edge_key") or edge_key(
                label, source["canonical_id"], target["canonical_id"], properties.get("fact_key", "")
            ),
            "relationship_type": label,
            "from_id": source["canonical_id"],
            "to_id": target["canonical_id"],
            "evidence_refs": evidence_refs if evidence_refs is not None else [],
            "creation_status": properties.get("creation_status", creation_status),
            "confidence": properties.get("confidence"),
            "properties": properties,
        }
    )
    mutation = GraphMutation(
        mutation_id=str(uuid4()), operation="UPSERT", target_kind="EDGE",
        payload=relationship.model_dump(), ingestion_run_id=ingestion_run_id,
    )
    result = apply_graph_mutation(store, mutation)
    if isinstance(result, bool):
        raise TypeError("edge UPSERT unexpectedly returned a tombstone result")
    return result


class IngestionGraphStore:
    """Explicit store adapter; no shadow graph, fallback, or dynamic delegation."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        self._run_id: ContextVar[str | None] = ContextVar("ingestion_run_id", default=None)
        self.health = store.health
        self.ping = store.ping
        self.ensure_schema = store.ensure_schema
        self.schema_status = store.schema_status
        self.get_vertex = store.get_vertex
        self.get_vertex_by_canonical_id = store.get_vertex_by_canonical_id
        self.find_vertex_by_property = store.find_vertex_by_property
        self.find_vertices = store.find_vertices
        self.count_vertices = store.count_vertices
        self.get_edge = store.get_edge
        self.find_edge_by_key = store.find_edge_by_key
        self.find_edges = store.find_edges
        self.edges_from = store.edges_from
        self.edges_to = store.edges_to
        self.count_edges = store.count_edges
        self.bulk_load = store.bulk_load
        self.clear = store.clear

    def begin_run(self, run_id: str) -> None:
        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError("ingestion_run_id must be nonblank")
        self._run_id.set(run_id)

    def _run(self) -> str:
        run_id = self._run_id.get()
        if run_id is None:
            raise RuntimeError("begin_run is required before ingestion mutations")
        return run_id

    @staticmethod
    def _refs(properties: dict, keys: tuple[str, ...]) -> list[str]:
        return [properties[key] for key in keys if properties.get(key) is not None]

    def upsert_vertex(self, label: str, properties: dict) -> dict:
        return validate_and_write_entity(
            self._store, label, properties.get("canonical_id"), properties,
            source_refs=self._refs(properties, ("source_ref", "source_uri", "source_event_id")),
            ingestion_run_id=self._run(),
        )

    def upsert_edge(self, label: str, out_v: str, in_v: str, properties: dict) -> dict:
        return validate_and_write_relationship(
            self._store, label, out_v, in_v, properties,
            evidence_refs=self._refs(properties, ("source_ref", "evidence_key", "source_event_id")),
            ingestion_run_id=self._run(),
        )

    def tombstone_vertex(self, canonical_id: str) -> bool:
        run_id = self._run()
        if not canonical_id.strip():
            raise MutationBlocked("tombstone canonical_id must be nonblank")
        vertex = self.get_vertex_by_canonical_id(canonical_id)
        if vertex is None:
            return False
        entity = NormalizedEntity.model_validate(
            {
                "canonical_id": canonical_id, "entity_type": vertex["label"],
                "graph_domain": VERTEX_LABELS[vertex["label"]][0],
                "source_refs": self._refs(vertex["properties"], ("source_ref", "source_uri")),
                "creation_status": vertex["properties"].get("creation_status"),
                "confidence": vertex["properties"].get("confidence"),
                "properties": vertex["properties"],
            }
        )
        mutation = GraphMutation(
            mutation_id=str(uuid4()), operation="TOMBSTONE", target_kind="VERTEX",
            payload=entity.model_dump(), ingestion_run_id=run_id,
        )
        result = apply_graph_mutation(self._store, mutation)
        if not isinstance(result, bool):
            raise TypeError("TOMBSTONE unexpectedly returned an UPSERT result")
        return result
