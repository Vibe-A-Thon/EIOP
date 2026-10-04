from __future__ import annotations

import json

import pytest
from eoip.graph.bitemporal import (
    BitemporalCoordinate,
    BitemporalQueryEngine,
    build_router,
)
from eoip.graph.memory import MemoryGraphStore
from apps.api.app import create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient

T0 = "2026-10-01T00:00:00Z"
T1 = "2026-10-02T00:00:00Z"
T2 = "2026-10-03T00:00:00Z"
T3 = "2026-10-04T00:00:00Z"


def _entity_revision(
    store: MemoryGraphStore,
    rid: str,
    subject: str,
    observed_at: str,
    *,
    valid_from: str = T0,
    valid_to: str = "",
    is_current: bool = True,
    status: str = "Open",
    entity_type: str = "WorkItem",
    operation: str | None = None,
) -> None:
    payload = {"label": entity_type, "properties": {"status": status}, "canonical_id": subject}
    if operation:
        payload["operation"] = operation
    store.upsert_vertex(
        "EntityRevision",
        {
            "canonical_id": f"urn:eoip:revision:entity:{rid}",
            "revision_id": rid,
            "subject_id": subject,
            "entity_type": entity_type,
            "observed_at": observed_at,
            "valid_from": valid_from,
            "valid_to": valid_to,
            "is_current": is_current,
            "payload_json": json.dumps(payload, sort_keys=True),
            "source_event_id": f"evt-{rid}",
            "graph_version": f"gv-{rid}",
        },
    )


def _relationship_revision(
    store: MemoryGraphStore,
    rid: str,
    rel_id: str,
    observed_at: str,
    *,
    valid_from: str = T0,
    valid_to: str = "",
    is_current: bool = True,
    from_id: str = "urn:e:a",
    to_id: str = "urn:e:b",
    operation: str | None = None,
) -> None:
    payload = {
        "relationship_type": "DEPENDS_ON",
        "from_id": from_id,
        "to_id": to_id,
        "properties": {},
        "relationship_id": rel_id,
    }
    if operation:
        payload["operation"] = operation
    store.upsert_vertex(
        "RelationshipRevision",
        {
            "canonical_id": f"urn:eoip:revision:relationship:{rid}",
            "revision_id": rid,
            "relationship_id": rel_id,
            "relationship_type": "DEPENDS_ON",
            "from_id": from_id,
            "to_id": to_id,
            "observed_at": observed_at,
            "valid_from": valid_from,
            "valid_to": valid_to,
            "is_current": is_current,
            "payload_json": json.dumps(payload, sort_keys=True),
            "source_event_id": f"evt-{rid}",
            "graph_version": f"gv-{rid}",
        },
    )


@pytest.fixture
def store() -> MemoryGraphStore:
    """Fabricated revision journal for urn:e:a across a bitemporal timeline.

    Entity A: created T0 (status Open), updated T2 (status Done).
    Entity B: created T1, deleted T3.
    Relationship R1 (A->B): created T1, superseded T2.
    """
    store = MemoryGraphStore()
    _entity_revision(store, "r-a-1", "urn:e:a", T0, valid_from=T0, valid_to=T2, is_current=False, status="Open")
    _entity_revision(store, "r-a-2", "urn:e:a", T2, valid_from=T2, valid_to="", is_current=True, status="Done")
    _entity_revision(store, "r-b-1", "urn:e:b", T1, valid_from=T1, valid_to=T3, is_current=False)
    _entity_revision(store, "r-b-2", "urn:e:b", T3, valid_from=T3, valid_to="", is_current=True, operation="DELETE")
    _relationship_revision(store, "r-r1-1", "urn:r:1", T1, valid_from=T1, valid_to=T2, is_current=False)
    _relationship_revision(store, "r-r1-2", "urn:r:1", T2, valid_from=T2, valid_to="", is_current=True)
    return store


@pytest.mark.req("GAP-TEMP-001")
def test_known_at_returns_latest_revision_observed_before_system_time(store: MemoryGraphStore) -> None:
    engine = BitemporalQueryEngine(store)

    early = engine.known_at(T1)
    assert [e.subject_id for e in early.entities] == ["urn:e:a", "urn:e:b"]
    assert early.entities[0].payload["properties"]["status"] == "Open"
    assert [r.subject_id for r in early.relationships] == ["urn:r:1"]
    assert early.relationships[0].revision_id == "r-r1-1"

    later = engine.known_at(T2)
    statuses = {e.subject_id: e.payload["properties"]["status"] for e in later.entities}
    assert statuses == {"urn:e:a": "Done", "urn:e:b": "Open"}
    assert later.relationships[0].revision_id == "r-r1-2"

    empty = engine.known_at("2026-09-30T00:00:00Z")
    assert empty.entities == [] and empty.relationships == []


@pytest.mark.req("GAP-TEMP-002")
def test_valid_at_selects_revisions_whose_window_covers_valid_time(store: MemoryGraphStore) -> None:
    engine = BitemporalQueryEngine(store)

    mid = engine.valid_at("2026-10-03T12:00:00Z")
    subjects = {e.subject_id for e in mid.entities}
    # A's r-a-2 (valid_from T2, open) and B's r-b-1 (T1..T3) cover this point.
    assert subjects == {"urn:e:a", "urn:e:b"}
    assert all(r.revision_id == "r-r1-2" for r in mid.relationships)

    before_b = engine.valid_at("2026-10-01T12:00:00Z")
    assert {e.subject_id for e in before_b.entities} == {"urn:e:a"}
    assert before_b.relationships == []


@pytest.mark.req("GAP-TEMP-003")
def test_slice_combines_valid_and_transaction_time(store: MemoryGraphStore) -> None:
    engine = BitemporalQueryEngine(store)

    # Valid at T1 as known at T1: A r-a-1, B r-b-1, R1 r-r1-1.
    early = engine.slice(T1, T1)
    assert {e.revision_id for e in early.entities} == {"r-a-1", "r-b-1"}
    assert [r.revision_id for r in early.relationships] == ["r-r1-1"]

    # Valid at T1 as known at T3: later knowledge still preserves A's
    # historical valid interval instead of overwriting it.
    late = engine.slice(T1, T3)
    assert {e.revision_id for e in late.entities} == {"r-a-1", "r-b-1"}
    assert [r.revision_id for r in late.relationships] == ["r-r1-1"]

    # Late knowledge cannot leak earlier: known at T1 never sees r-a-2.
    assert all(e.revision_id != "r-a-2" for e in early.entities)


@pytest.mark.req("GAP-TEMP-004")
def test_topology_reconstructs_entity_and_edge_sets(store: MemoryGraphStore) -> None:
    engine = BitemporalQueryEngine(store)

    topo = engine.topology(T1, T1)
    assert topo.entity_ids == ["urn:e:a", "urn:e:b"]
    assert [(e.relationship_id, e.from_id, e.to_id) for e in topo.edges] == [
        ("urn:r:1", "urn:e:a", "urn:e:b")
    ]
    assert topo.entity_count == 2 and topo.edge_count == 1

    # After B's delete, topology excludes both B and the edge touching it.
    deleted = engine.topology(T3, T3)
    assert deleted.entity_ids == ["urn:e:a"]
    assert deleted.edges == []

    # Edge without endpoint is dropped even if its revision is selected.
    _relationship_revision(
        store, "r-r2-1", "urn:r:2", T1, from_id="urn:e:a", to_id="urn:e:missing"
    )
    filtered = engine.topology(T1, T1)
    assert [e.relationship_id for e in filtered.edges] == ["urn:r:1"]


@pytest.mark.req("GAP-TEMP-005")
def test_diff_between_coordinates_is_first_class(store: MemoryGraphStore) -> None:
    engine = BitemporalQueryEngine(store)
    before = BitemporalCoordinate(valid_at=T1, known_at=T1)
    after = BitemporalCoordinate(valid_at=T3, known_at=T3)

    result = engine.diff(before, after)
    assert result.diff_id.startswith("urn:eoip:bitemporal:diff:")
    assert result.entities.added == []
    assert result.entities.removed == ["urn:e:b"]
    assert result.relationships.removed == ["urn:r:1"]
    assert result.summary == {
        "entities_added": 0,
        "entities_removed": 1,
        "entities_changed": 0,
        "edges_added": 0,
        "edges_removed": 1,
        "edges_changed": 0,
    }
    # Diff is symmetric: reverse swap added/removed.
    reverse = engine.diff(after, before)
    assert reverse.entities.added == ["urn:e:b"]
    assert reverse.relationships.added == ["urn:r:1"]


def test_router_endpoints_round_trip(store: MemoryGraphStore) -> None:
    app = FastAPI()
    app.include_router(build_router(store))
    client = TestClient(app)

    response = client.post(
        "/api/v1/graph/bitemporal/slice",
        json={"valid_at": T1, "known_at": T1},
    )
    assert response.status_code == 200
    body = response.json()
    assert {e["revision_id"] for e in body["entities"]} == {"r-a-1", "r-b-1"}

    response = client.post(
        "/api/v1/graph/bitemporal/topology",
        json={"valid_at": T1, "known_at": T1},
    )
    assert response.status_code == 200
    assert response.json()["entity_ids"] == ["urn:e:a", "urn:e:b"]

    response = client.post(
        "/api/v1/graph/bitemporal/diff",
        json={
            "from_coordinate": {"valid_at": T1, "known_at": T1},
            "to_coordinate": {"valid_at": T3, "known_at": T3},
        },
    )
    assert response.status_code == 200
    assert response.json()["entities"]["removed"] == ["urn:e:b"]

    response = client.post(
        "/api/v1/graph/bitemporal/known-at", json={"known_at": T1}
    )
    assert response.status_code == 200


def test_main_api_mounts_bitemporal_router(store: MemoryGraphStore) -> None:
    client = TestClient(create_app(store))

    response = client.post(
        "/api/v1/graph/bitemporal/topology",
        json={"valid_at": T1, "known_at": T1},
    )

    assert response.status_code == 200
    assert response.json()["entity_ids"] == ["urn:e:a", "urn:e:b"]
