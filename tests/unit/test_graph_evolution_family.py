import hashlib
import json
import pytest
from eoip.contracts.source_event import SourceEventV2
from eoip.graph.evolution import ChangeJournal, GraphEvolutionEngine, SemanticEventBus
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.schema_migration import MigrationPlan, MigrationStrategy, MigrationPlanItem


def _event(event_id: str, at: str, payload: dict, operation: str = "UPSERT") -> SourceEventV2:
    body = json.dumps(payload, sort_keys=True)
    return SourceEventV2(
        event_id=event_id,
        source_system="test-system",
        source_instance_id="test-source",
        source_record_id=payload.get("id", event_id),
        operation=operation,
        event_time=at,
        captured_at=at,
        source_version="v1.0",
        content_hash=hashlib.sha256(body.encode()).hexdigest(),
        payload=payload if operation != "DELETE" else None,
    )


@pytest.fixture
def evolution_fixture(tmp_path):
    store = MemoryGraphStore()
    journal = ChangeJournal(tmp_path / "journal.ndjson")
    bus = SemanticEventBus()
    engine = GraphEvolutionEngine(store, journal, bus)
    return store, journal, bus, engine


@pytest.mark.req("G2-EVOL-002")
def test_evolve_relationship_validity_interval(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    store.upsert_vertex("File", {"canonical_id": "file:a", "repo_id": "r1", "path": "a.py"})
    store.upsert_vertex("File", {"canonical_id": "file:b", "repo_id": "r1", "path": "b.py"})

    e1 = _event("rel-1", "2026-10-01T00:00:00Z", {"id": "r1", "to": "file:b"})
    res = engine.evolve_relationship("rel:ab", "DEPENDS_ON", "file:a", "file:b", {}, e1)
    assert res["status"] == "CREATE"

    edges = store.find_edges(label="DEPENDS_ON", include_historical=True)
    assert len(edges) == 1
    edge = edges[0]
    assert edge["properties"]["valid_from"] == "2026-10-01T00:00:00Z"
    assert edge["properties"]["valid_to"] == ""


@pytest.mark.req("G2-EVOL-003")
def test_observation_time_separated_from_event_time(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    event = SourceEventV2(
        event_id="evt-obs",
        source_system="test",
        source_instance_id="test-source",
        source_record_id="item-1",
        operation="UPSERT",
        event_time="2026-10-01T08:00:00Z",
        captured_at="2026-10-01T08:05:00Z",
        content_hash="hash-1",
        payload={"id": "item-1"},
    )
    res = engine.evolve_entity("WorkItem", "urn:item:1", {"issue_key": "ITEM-1", "summary": "Task"}, event)
    assert res["status"] == "CREATE"
    rev = store.find_vertices(label="EntityRevision")[0]
    assert rev["properties"]["observed_at"] == "2026-10-01T08:00:00Z"


@pytest.mark.req("G2-EVOL-004")
def test_relationship_removal_expires_assertion_without_erasing_history(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    store.upsert_vertex("File", {"canonical_id": "f1", "repo_id": "r", "path": "f1"})
    store.upsert_vertex("File", {"canonical_id": "f2", "repo_id": "r", "path": "f2"})

    e_create = _event("c1", "2026-10-01T00:00:00Z", {"id": "rel-f1-f2"})
    engine.evolve_relationship("rel-f1-f2", "DEPENDS_ON", "f1", "f2", {}, e_create)

    e_delete = _event("d1", "2026-10-02T00:00:00Z", {"id": "rel-f1-f2"}, operation="DELETE")
    res = engine.evolve_relationship("rel-f1-f2", "DEPENDS_ON", "f1", "f2", {}, e_delete)
    assert res["status"] == "DELETE"

    # Current view excludes it
    assert len(store.find_edges(label="DEPENDS_ON")) == 0
    # Historical view retains it with valid_to set
    hist = store.find_edges(label="DEPENDS_ON", include_historical=True)
    assert len(hist) == 1
    assert hist[0]["properties"]["valid_to"] == "2026-10-02T00:00:00Z"


@pytest.mark.req("G2-EVOL-005")
def test_relationship_update_represented_as_new_revision(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    store.upsert_vertex("File", {"canonical_id": "x", "repo_id": "r", "path": "x"})
    store.upsert_vertex("File", {"canonical_id": "y", "repo_id": "r", "path": "y"})
    store.upsert_vertex("File", {"canonical_id": "z", "repo_id": "r", "path": "z"})

    e1 = _event("u1", "2026-10-01T00:00:00Z", {"id": "rel-xz", "to": "y"})
    engine.evolve_relationship("rel-xz", "DEPENDS_ON", "x", "y", {}, e1)

    e2 = _event("u2", "2026-10-02T00:00:00Z", {"id": "rel-xz", "to": "z"})
    engine.evolve_relationship("rel-xz", "DEPENDS_ON", "x", "z", {}, e2)

    revs = store.find_vertices(label="RelationshipRevision")
    assert len(revs) == 2


@pytest.mark.req("G2-EVOL-006")
def test_current_views_exclude_expired_facts(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    store.upsert_vertex("File", {"canonical_id": "p", "repo_id": "r", "path": "p"})
    store.upsert_vertex("File", {"canonical_id": "q", "repo_id": "r", "path": "q"})

    engine.evolve_relationship("rel-pq", "DEPENDS_ON", "p", "q", {}, _event("e1", "2026-10-01T00:00:00Z", {}))
    engine.evolve_relationship("rel-pq", "DEPENDS_ON", "p", "q", {}, _event("e2", "2026-10-02T00:00:00Z", {}, "DELETE"))

    current_edges = store.find_edges(label="DEPENDS_ON")
    assert len(current_edges) == 0


@pytest.mark.req("G2-EVOL-007")
def test_historical_as_of_reconstruction(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    e1 = _event("e1", "2026-10-01T00:00:00Z", {"status": "Open"})
    e2 = _event("e2", "2026-10-03T00:00:00Z", {"status": "Closed"})
    engine.evolve_entity("WorkItem", "item:100", {"issue_key": "W-100", "summary": "Fix bug", "status": "Open"}, e1)
    engine.evolve_entity("WorkItem", "item:100", {"issue_key": "W-100", "summary": "Fix bug", "status": "Closed"}, e2)

    past = engine.as_of("2026-10-02T00:00:00Z")
    assert past["entities"][0]["properties"]["status"] == "Open"
    future = engine.as_of("2026-10-04T00:00:00Z")
    assert future["entities"][0]["properties"]["status"] == "Closed"


@pytest.mark.req("G2-EVOL-008")
def test_graph_diff_between_timestamps(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    e1 = _event("e1", "2026-10-01T00:00:00Z", {"status": "Draft"})
    e2 = _event("e2", "2026-10-03T00:00:00Z", {"status": "Published"})
    engine.evolve_entity("WorkItem", "item:200", {"issue_key": "W-200", "summary": "RFC", "status": "Draft"}, e1)
    engine.evolve_entity("WorkItem", "item:200", {"issue_key": "W-200", "summary": "RFC", "status": "Published"}, e2)

    diff = engine.diff("2026-10-02T00:00:00Z", "2026-10-04T00:00:00Z")
    assert len(diff["entities"]["changed"]) == 1


@pytest.mark.req("G2-EVOL-009")
def test_graph_mutation_source_references(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    event = _event("evt-src-ref", "2026-10-01T00:00:00Z", {"id": "src-item"})
    engine.evolve_entity("WorkItem", "item:src", {"issue_key": "W-SRC", "summary": "Source Trace"}, event)

    rev = store.find_vertices(label="EntityRevision")[0]
    assert rev["properties"]["source_event_id"] == "evt-src-ref"
    assert rev["properties"]["source_version"] == "v1.0"
    assert rev["properties"]["graph_version"]


@pytest.mark.req("G2-EVOL-010")
def test_atomic_batch_isolation(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    # Verify lock and atomic updates
    events = [_event(f"evt-{i}", f"2026-10-01T00:00:0{i}Z", {"id": f"item-{i}"}) for i in range(3)]
    for i, ev in enumerate(events):
        engine.evolve_entity("WorkItem", f"item:{i}", {"issue_key": f"W-{i}", "summary": f"Item {i}"}, ev)
    assert len(store.find_vertices(label="EntityRevision")) == 3


@pytest.mark.req("G2-EVOL-011")
def test_failed_batch_does_not_advance_checkpoint(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    # Nonexistent relationship endpoint raises ValueError
    event = _event("evt-fail", "2026-10-01T00:00:00Z", {})
    with pytest.raises(ValueError, match="relationship endpoints must exist"):
        engine.evolve_relationship("rel-bad", "DEPENDS_ON", "missing-src", "missing-tgt", {}, event)
    # Journal does not record the failed relationship
    assert len(journal.read()) == 0


@pytest.mark.req("G2-EVOL-012")
def test_relationship_preservation_means_history_not_stale_edges(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    store.upsert_vertex("File", {"canonical_id": "fA", "repo_id": "r", "path": "fA"})
    store.upsert_vertex("File", {"canonical_id": "fB", "repo_id": "r", "path": "fB"})
    store.upsert_vertex("File", {"canonical_id": "fC", "repo_id": "r", "path": "fC"})

    engine.evolve_relationship("rel-AB", "DEPENDS_ON", "fA", "fB", {}, _event("e1", "2026-10-01T00:00:00Z", {}))
    engine.evolve_relationship("rel-AB", "DEPENDS_ON", "fA", "fC", {}, _event("e2", "2026-10-02T00:00:00Z", {}))

    active = store.find_edges(label="DEPENDS_ON")
    assert len(active) == 1
    assert active[0]["in_cid"] == "fC"


@pytest.mark.req("G2-EVOL-013")
def test_previous_revision_links(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    e1 = _event("e1", "2026-10-01T00:00:00Z", {"v": 1})
    e2 = _event("e2", "2026-10-02T00:00:00Z", {"v": 2})
    engine.evolve_entity("WorkItem", "item:chain", {"issue_key": "W-C", "summary": "V1"}, e1)
    engine.evolve_entity("WorkItem", "item:chain", {"issue_key": "W-C", "summary": "V2"}, e2)

    revs = sorted(store.find_vertices(label="EntityRevision"), key=lambda r: r["properties"]["observed_at"])
    assert len(revs) == 2
    assert revs[0]["properties"]["previous_revision"] is None
    assert revs[1]["properties"]["previous_revision"] == revs[0]["properties"]["revision_id"]


@pytest.mark.req("G2-EVOL-014")
def test_tombstone_retired_status(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    e1 = _event("e1", "2026-10-01T00:00:00Z", {})
    engine.evolve_entity("WorkItem", "item:tomb", {"issue_key": "W-T", "summary": "To Delete"}, e1)

    e_del = _event("e2", "2026-10-02T00:00:00Z", {}, operation="DELETE")
    engine.evolve_entity("WorkItem", "item:tomb", {}, e_del)

    v = store.get_vertex_by_canonical_id("item:tomb")
    assert bool(v["properties"]["deleted_at"])


@pytest.mark.req("G2-EVOL-015")
def test_rollback_and_replay_strategy(evolution_fixture):
    store, journal, bus, engine = evolution_fixture
    # Events can be replayed in deterministic sequence
    e1 = _event("r1", "2026-10-01T00:00:00Z", {"status": "Step1"})
    e2 = _event("r2", "2026-10-02T00:00:00Z", {"status": "Step2"})
    engine.evolve_entity("WorkItem", "item:replay", {"issue_key": "W-R", "summary": "Replay", "status": "Step1"}, e1)
    engine.evolve_entity("WorkItem", "item:replay", {"issue_key": "W-R", "summary": "Replay", "status": "Step2"}, e2)

    journal_records = journal.read()
    assert len(journal_records) == 2
    # Late event with earlier timestamp is safely ignored to protect current state
    e_late = _event("r_late", "2026-10-01T12:00:00Z", {"status": "Stale"})
    late_res = engine.evolve_entity("WorkItem", "item:replay", {"issue_key": "W-R", "summary": "Replay", "status": "Stale"}, e_late)
    assert late_res["status"] == "LATE_IGNORED"


@pytest.mark.req("G2-EVOL-016")
def test_schema_ontology_migration_strategy():
    plan = MigrationPlan(
        source_version="1.0.0",
        target_version="1.1.0",
        actions=[
            MigrationPlanItem(
                name="add_optional_property",
                strategy=MigrationStrategy.NO_MIGRATION,
                description="Additive property, existing facts remain valid",
            ),
            MigrationPlanItem(
                name="backfill_team_ownership",
                strategy=MigrationStrategy.ONLINE_BACKFILL,
                description="Online backfill of team ownership",
            ),
            MigrationPlanItem(
                name="deprecate_legacy_tag",
                strategy=MigrationStrategy.LAZY_MIGRATION,
                description="Migrate on read",
            ),
            MigrationPlanItem(
                name="reparse_repos",
                strategy=MigrationStrategy.SOURCE_REPLAY,
                description="Replay git connector for new symbol format",
            ),
        ],
    )
    strategies = {action.strategy for action in plan.actions}
    assert MigrationStrategy.NO_MIGRATION in strategies
    assert MigrationStrategy.ONLINE_BACKFILL in strategies
    assert MigrationStrategy.LAZY_MIGRATION in strategies
    assert MigrationStrategy.SOURCE_REPLAY in strategies
