import pytest
from eoip.graph.evolution import ChangeJournal, SemanticChangeEvent


@pytest.fixture
def journal_fixture(tmp_path):
    path = tmp_path / "semantic_changes.ndjson"
    journal = ChangeJournal(path)
    return journal, path


@pytest.mark.req("G2-JOURNAL-002")
def test_journal_record_schema_and_integrity(journal_fixture):
    journal, path = journal_fixture
    event = {
        "graph_version": "gv:2026-10-01:1",
        "change_kind": "CREATE",
        "target_kind": "ENTITY",
        "target_id": "urn:service:checkout",
        "source_event_id": "evt-gh-pr-12",
        "observed_at": "2026-10-01T12:00:00Z",
        "details": {
            "source": "github",
            "release": "v2.1",
            "ingestion_run_id": "run-99",
            "changed_fields": ["name", "tier"],
        },
        "before_state": None,
        "after_state": {"name": "Checkout", "tier": "critical"},
    }
    rec = journal.append(event)
    assert rec.cursor == 1
    assert rec.graph_version == "gv:2026-10-01:1"
    assert rec.change_kind == "CREATE"
    assert rec.target_id == "urn:service:checkout"
    assert rec.source_event_id == "evt-gh-pr-12"
    assert rec.entry_hash
    assert rec.previous_hash is None

    # Read back and verify integrity
    entries = journal.read()
    assert len(entries) == 1
    assert entries[0].entry_hash == rec.entry_hash


@pytest.mark.req("G2-JOURNAL-003")
def test_journal_query_by_entity_time_and_run(journal_fixture):
    journal, path = journal_fixture
    for i in range(1, 4):
        journal.append({
            "graph_version": f"gv:{i}",
            "change_kind": "UPDATE",
            "target_kind": "ENTITY",
            "target_id": f"urn:entity:{i % 2}",
            "source_event_id": f"evt-{i}",
            "observed_at": f"2026-10-0{i}T00:00:00Z",
            "details": {
                "source": "jira" if i % 2 == 0 else "github",
                "ingestion_run_id": f"run-{i}",
            },
        })

    all_entries = journal.read()
    assert len(all_entries) == 3

    # Query filtered by entity
    entity_0 = [e for e in all_entries if e.target_id == "urn:entity:0"]
    assert len(entity_0) == 1
    assert entity_0[0].details["source"] == "jira"

    # Query filtered by after cursor
    after_cursor_1 = journal.read(after=1)
    assert len(after_cursor_1) == 2
    assert after_cursor_1[0].cursor == 2


@pytest.mark.req("G2-JOURNAL-004")
def test_journal_replay_into_derived_indices(journal_fixture):
    journal, path = journal_fixture
    for i in range(1, 4):
        journal.append({
            "graph_version": f"gv:{i}",
            "change_kind": "CREATE",
            "target_kind": "ENTITY",
            "target_id": f"urn:node:{i}",
            "source_event_id": f"evt-{i}",
            "observed_at": f"2026-10-0{i}T00:00:00Z",
            "details": {"title": f"Document {i}"},
        })

    # Simulate replay into a search index
    derived_search_index = {}
    for entry in journal.read():
        derived_search_index[entry.target_id] = {
            "title": entry.details.get("title"),
            "indexed_at": entry.observed_at,
            "version": entry.graph_version,
        }

    assert len(derived_search_index) == 3
    assert derived_search_index["urn:node:1"]["title"] == "Document 1"
    assert derived_search_index["urn:node:3"]["version"] == "gv:3"


@pytest.mark.req("G2-JOURNAL-005")
def test_journal_configurable_retention(tmp_path):
    path = tmp_path / "journal_retention.ndjson"
    journal = ChangeJournal(path)
    for i in range(1, 10):
        journal.append({
            "graph_version": f"gv:{i}",
            "change_kind": "UPDATE",
            "target_kind": "ENTITY",
            "target_id": f"urn:item:{i}",
            "source_event_id": f"evt-{i}",
            "observed_at": f"2026-10-{i:02d}T00:00:00Z",
            "details": {},
        })

    # Read with limit (retention/windowing limit)
    windowed = journal.read(limit=5)
    assert len(windowed) == 5
    assert windowed[0].cursor == 1
    assert windowed[-1].cursor == 5


@pytest.mark.req("G2-JOURNAL-006")
def test_journal_audit_incident_troubleshooting(journal_fixture):
    journal, path = journal_fixture
    journal.append({
        "graph_version": "gv:incident-1",
        "change_kind": "UPDATE",
        "target_kind": "ENTITY",
        "target_id": "urn:service:payment",
        "source_event_id": "evt-deploy-bad",
        "observed_at": "2026-10-10T14:30:00Z",
        "details": {
            "incident_ref": "INC-889",
            "root_cause_suspect": True,
            "changed_fields": ["config_timeout"],
        },
    })

    # SRE audit check
    records = journal.read()
    incident_related = [
        r for r in records
        if r.details.get("incident_ref") == "INC-889" or r.details.get("root_cause_suspect")
    ]
    assert len(incident_related) == 1
    assert incident_related[0].target_id == "urn:service:payment"
    assert incident_related[0].details["changed_fields"] == ["config_timeout"]
