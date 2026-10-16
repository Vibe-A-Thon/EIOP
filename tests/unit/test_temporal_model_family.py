import json
import pytest
from eoip.graph.bitemporal import (
    BitemporalCoordinate,
    BitemporalQueryEngine,
)
from eoip.graph.memory import MemoryGraphStore

T0 = "2026-10-01T00:00:00Z"
T1 = "2026-10-02T00:00:00Z"
T2 = "2026-10-03T00:00:00Z"
T3 = "2026-10-04T00:00:00Z"


@pytest.fixture
def bitemporal_store():
    store = MemoryGraphStore()

    # EntityRevision for Service A: V1 at T1, V2 at T2
    payload_a1 = {"label": "Service", "properties": {"status": "Staging", "version": "1.0"}, "canonical_id": "svc:auth"}
    store.upsert_vertex("EntityRevision", {
        "canonical_id": "urn:eoip:revision:entity:r-a-1",
        "revision_id": "r-a-1",
        "subject_id": "svc:auth",
        "entity_type": "Service",
        "observed_at": T1,
        "valid_from": T1,
        "valid_to": T2,
        "is_current": False,
        "payload_json": json.dumps(payload_a1),
        "source_event_id": "evt-1",
        "graph_version": "gv-v1.0",
    })

    payload_a2 = {"label": "Service", "properties": {"status": "Production", "version": "1.1"}, "canonical_id": "svc:auth"}
    store.upsert_vertex("EntityRevision", {
        "canonical_id": "urn:eoip:revision:entity:r-a-2",
        "revision_id": "r-a-2",
        "subject_id": "svc:auth",
        "entity_type": "Service",
        "observed_at": T2,
        "valid_from": T2,
        "valid_to": "",
        "is_current": True,
        "payload_json": json.dumps(payload_a2),
        "source_event_id": "evt-2",
        "graph_version": "gv-v1.1",
    })

    # EntityRevision for Service B: created at T1, deleted at T3
    payload_b1 = {"label": "Service", "properties": {"status": "Production"}, "canonical_id": "svc:billing"}
    store.upsert_vertex("EntityRevision", {
        "canonical_id": "urn:eoip:revision:entity:r-b-1",
        "revision_id": "r-b-1",
        "subject_id": "svc:billing",
        "entity_type": "Service",
        "observed_at": T1,
        "valid_from": T1,
        "valid_to": T3,
        "is_current": False,
        "payload_json": json.dumps(payload_b1),
        "source_event_id": "evt-b1",
        "graph_version": "gv-v1.0",
    })

    # RelationshipRevision: svc:auth -> svc:billing
    payload_r1 = {
        "relationship_type": "CALLS",
        "from_id": "svc:auth",
        "to_id": "svc:billing",
        "properties": {},
        "relationship_id": "rel-auth-billing",
    }
    store.upsert_vertex("RelationshipRevision", {
        "canonical_id": "urn:eoip:revision:relationship:r-rel-1",
        "revision_id": "r-rel-1",
        "relationship_id": "rel-auth-billing",
        "relationship_type": "CALLS",
        "from_id": "svc:auth",
        "to_id": "svc:billing",
        "observed_at": T1,
        "valid_from": T1,
        "valid_to": T3,
        "is_current": False,
        "payload_json": json.dumps(payload_r1),
        "source_event_id": "evt-r1",
        "graph_version": "gv-v1.0",
    })

    return store


@pytest.mark.req("G2-TIME-002")
def test_time_machine_state_as_of_t(bitemporal_store):
    engine = BitemporalQueryEngine(bitemporal_store)

    # State as of T1: svc:auth has version 1.0, status Staging
    slice_t1 = engine.valid_at("2026-10-02T12:00:00Z")
    auth_t1 = next(e for e in slice_t1.entities if e.subject_id == "svc:auth")
    assert auth_t1.payload["properties"]["status"] == "Staging"
    assert auth_t1.payload["properties"]["version"] == "1.0"

    # State as of T2: svc:auth has version 1.1, status Production
    slice_t2 = engine.valid_at("2026-10-03T12:00:00Z")
    auth_t2 = next(e for e in slice_t2.entities if e.subject_id == "svc:auth")
    assert auth_t2.payload["properties"]["status"] == "Production"
    assert auth_t2.payload["properties"]["version"] == "1.1"


@pytest.mark.req("G2-TIME-003")
def test_time_machine_compare_t1_vs_t2(bitemporal_store):
    engine = BitemporalQueryEngine(bitemporal_store)
    c1 = BitemporalCoordinate(valid_at="2026-10-02T12:00:00Z", known_at=T2)
    c2 = BitemporalCoordinate(valid_at="2026-10-03T12:00:00Z", known_at=T2)

    diff = engine.diff(c1, c2)
    assert diff.from_coordinate.valid_at == "2026-10-02T12:00:00Z"
    assert diff.to_coordinate.valid_at == "2026-10-03T12:00:00Z"


@pytest.mark.req("G2-TIME-004")
def test_time_machine_highlights_semantic_changes(bitemporal_store):
    engine = BitemporalQueryEngine(bitemporal_store)
    c_early = BitemporalCoordinate(valid_at=T1, known_at=T1)
    c_late = BitemporalCoordinate(valid_at=T3, known_at=T3)

    diff = engine.diff(c_early, c_late)
    # Service B was deleted at T3
    assert "svc:billing" in diff.entities.removed
    # Relationship between auth and billing was expired/removed
    assert "rel-auth-billing" in diff.relationships.removed


@pytest.mark.req("G2-TIME-005")
def test_release_based_snapshots(bitemporal_store):
    engine = BitemporalQueryEngine(bitemporal_store)
    # Graph version gv-v1.0 corresponds to Release 1.0
    slice_v1 = engine.known_at(T1)
    for ent in slice_v1.entities:
        assert ent.graph_version == "gv-v1.0"


@pytest.mark.req("G2-TIME-006")
def test_time_travel_schema_version_context(bitemporal_store):
    engine = BitemporalQueryEngine(bitemporal_store)
    slice_early = engine.slice(valid_at=T1, known_at=T1)
    slice_late = engine.slice(valid_at=T2, known_at=T2)

    auth_early = next(e for e in slice_early.entities if e.subject_id == "svc:auth")
    auth_late = next(e for e in slice_late.entities if e.subject_id == "svc:auth")

    assert auth_early.graph_version == "gv-v1.0"
    assert auth_late.graph_version == "gv-v1.1"


@pytest.mark.req("G2-TIME-007")
def test_historical_mode_evidence_reflects_valid_time(bitemporal_store):
    engine = BitemporalQueryEngine(bitemporal_store)
    topo_t1 = engine.topology(valid_at=T1, known_at=T1)
    assert set(topo_t1.entity_ids) == {"svc:auth", "svc:billing"}
    assert len(topo_t1.edges) == 1

    # At T3, svc:billing was deleted, so historical evidence query at T3 excludes it
    topo_t3 = engine.topology(valid_at=T3, known_at=T3)
    assert "svc:billing" not in topo_t3.entity_ids
    assert len(topo_t3.edges) == 0
