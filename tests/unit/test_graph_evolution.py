from __future__ import annotations

import hashlib
import json

import pytest
from eoip.contracts.source_event import SourceEventV2
from eoip.graph.evolution import ChangeJournal, GraphEvolutionEngine, SemanticEventBus
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient


def _event(event_id: str, at: str, payload: dict, operation: str = "UPSERT") -> SourceEventV2:
    body = json.dumps(payload, sort_keys=True)
    return SourceEventV2(
        event_id=event_id,
        source_system="test",
        source_instance_id="test-source",
        source_record_id=payload.get("id", event_id),
        operation=operation,
        event_time=at,
        captured_at=at,
        content_hash=hashlib.sha256(body.encode()).hexdigest(),
        payload=payload if operation != "DELETE" else None,
    )


@pytest.mark.req("G2-T0210", "G2-T0211", "G2-T0213", "G2-T0222", "G2-T0225")
def test_entity_evolution_is_idempotent_temporal_and_late_event_safe(tmp_path) -> None:
    store = MemoryGraphStore()
    journal = ChangeJournal(tmp_path / "journal.ndjson")
    published = []
    bus = SemanticEventBus()
    bus.subscribe(published.append)
    engine = GraphEvolutionEngine(store, journal, bus)
    first_event = _event("event-1", "2026-10-01T00:00:00Z", {"id": "EOIP-1", "status": "Open"})
    second_event = _event("event-2", "2026-10-02T00:00:00Z", {"id": "EOIP-1", "status": "Done"})

    created = engine.evolve_entity(
        "WorkItem", "urn:eoip:work:item:jira:EOIP-1", {"issue_key": "EOIP-1", "summary": "Temporal", "status": "Open"}, first_event
    )
    duplicate = engine.evolve_entity(
        "WorkItem", "urn:eoip:work:item:jira:EOIP-1", {"issue_key": "EOIP-1", "summary": "Temporal", "status": "Open"}, first_event
    )
    updated = engine.evolve_entity(
        "WorkItem", "urn:eoip:work:item:jira:EOIP-1", {"issue_key": "EOIP-1", "summary": "Temporal", "status": "Done"}, second_event
    )
    late = engine.evolve_entity(
        "WorkItem",
        "urn:eoip:work:item:jira:EOIP-1",
        {"issue_key": "EOIP-1", "summary": "Temporal", "status": "Stale"},
        _event("event-late", "2026-10-01T12:00:00Z", {"id": "EOIP-1", "status": "Stale"}),
    )

    assert created["status"] == "CREATE"
    assert duplicate["status"] == "UNCHANGED"
    assert updated["status"] == "UPDATE"
    assert late["status"] == "LATE_IGNORED"
    assert store.get_vertex_by_canonical_id("urn:eoip:work:item:jira:EOIP-1")["properties"]["status"] == "Done"
    assert engine.as_of("2026-10-01T12:00:00Z")["entities"][0]["properties"]["status"] == "Open"
    assert engine.as_of("2026-10-03T00:00:00Z")["entities"][0]["properties"]["status"] == "Done"
    diff = engine.diff("2026-10-01T12:00:00Z", "2026-10-03T00:00:00Z")
    assert len(diff["entities"]["changed"]) == 1
    assert len(journal.read()) == len(published) == 3


@pytest.mark.req("G2-T0220", "G2-T0221", "G2-T0223", "G2-T0224")
def test_relationship_replacement_expires_old_edge_and_preserves_history(tmp_path) -> None:
    store = MemoryGraphStore()
    for cid, name in (("a", "A"), ("b", "B"), ("c", "C")):
        store.upsert_vertex("File", {"canonical_id": cid, "repo_id": "repo", "path": name})
    engine = GraphEvolutionEngine(store, ChangeJournal(tmp_path / "journal.ndjson"))

    engine.evolve_relationship(
        "dependency-1", "DEPENDS_ON", "a", "b", {"confidence": 1.0},
        _event("rel-1", "2026-10-01T00:00:00Z", {"id": "dependency-1", "to": "b"}),
    )
    engine.evolve_relationship(
        "dependency-1", "DEPENDS_ON", "a", "c", {"confidence": 1.0},
        _event("rel-2", "2026-10-02T00:00:00Z", {"id": "dependency-1", "to": "c"}),
    )

    assert [edge["in_cid"] for edge in store.edges_from("v:1")] == ["c"]
    assert {edge["in_cid"] for edge in store.edges_from("v:1", include_historical=True)} == {"b", "c"}
    assert engine.as_of("2026-10-01T12:00:00Z")["relationships"][0]["to_id"] == "b"
    assert engine.as_of("2026-10-03T00:00:00Z")["relationships"][0]["to_id"] == "c"


@pytest.mark.req("G2-T0230", "G2-T0232", "G2-REL-005")
def test_change_journal_has_cursor_and_hash_chain_integrity(tmp_path) -> None:
    path = tmp_path / "journal.ndjson"
    journal = ChangeJournal(path)
    base = {
        "graph_version": "v1",
        "change_kind": "CREATE",
        "target_kind": "ENTITY",
        "target_id": "x",
        "source_event_id": "event-x",
        "observed_at": "2026-10-01T00:00:00Z",
        "details": {},
    }
    first = journal.append(base)
    second = journal.append({**base, "graph_version": "v2", "target_id": "y"})
    assert [item.cursor for item in journal.read(after=1)] == [second.cursor]
    assert second.previous_hash == first.entry_hash

    path.write_text(path.read_text().replace('"target_id":"x"', '"target_id":"z"'), encoding="utf-8")
    with pytest.raises(ValueError, match="integrity"):
        journal.read()


@pytest.mark.req("G2-T0223", "G2-T0224", "G2-T0231")
def test_temporal_api_exposes_versions_as_of_diff_and_journal(monkeypatch, tmp_path) -> None:
    from apps.api import main as api_main

    store = MemoryGraphStore()
    engine = GraphEvolutionEngine(store, ChangeJournal(tmp_path / "journal" / "semantic-changes.ndjson"))
    event = _event("event-api", "2026-10-01T00:00:00Z", {"id": "API-1"})
    engine.evolve_entity(
        "WorkItem", "urn:api:1", {"issue_key": "API-1", "summary": "API history"}, event
    )
    monkeypatch.setattr(api_main, "api_token", lambda: "x" * 32)
    monkeypatch.setattr(api_main, "create_store", lambda: store)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    client = TestClient(api_main.create_app())
    headers = {"Authorization": "Bearer " + "x" * 32}

    assert client.get("/api/v1/graph/versions", headers=headers).json()
    assert client.get(
        "/api/v1/graph/as-of?at=2026-10-02T00:00:00Z", headers=headers
    ).json()["entities"]
    assert client.get(
        "/api/v1/graph/diff?from=2026-09-01T00:00:00Z&to=2026-10-02T00:00:00Z",
        headers=headers,
    ).json()["entities"]["added"]
    assert client.get("/api/v1/change-journal?after=0", headers=headers).json()
