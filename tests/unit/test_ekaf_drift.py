from __future__ import annotations

import json

import pytest
from eoip.connectors.drift import (
    MappingDriftLedger,
    classify_payload_drift,
    infer_payload_schema,
)


@pytest.mark.req("G2-EKAF-017")
def test_schema_drift_classifies_compatible_and_additive_payloads() -> None:
    previous = {"id": "PAY-1", "fields": {"summary": "Pay", "points": 3}}
    same = {"id": "PAY-2", "fields": {"summary": "Refund", "points": 5}}
    additive = {
        "id": "PAY-2",
        "fields": {"summary": "Refund", "points": 5, "labels": ["risk"]},
    }

    assert classify_payload_drift(previous, same).classification == "compatible"
    report = classify_payload_drift(previous, additive)

    assert report.classification == "additive"
    assert report.added_paths == ["$.fields.labels", "$.fields.labels[]"]


@pytest.mark.req("G2-EKAF-017")
def test_schema_drift_classifies_scalar_changes_as_potentially_breaking() -> None:
    report = classify_payload_drift(
        {"id": "PAY-1", "fields": {"points": 3}},
        {"id": "PAY-1", "fields": {"points": "3"}},
    )

    assert report.classification == "potentially_breaking"
    assert report.changed_type_paths == {
        "$.fields.points": {"previous": "integer", "current": "string"}
    }


@pytest.mark.req("G2-EKAF-017")
def test_schema_drift_classifies_removed_or_container_changes_as_breaking() -> None:
    removed = classify_payload_drift(
        {"id": "PAY-1", "fields": {"summary": "Pay"}},
        {"id": "PAY-1", "fields": {}},
    )
    container = classify_payload_drift(
        {"id": "PAY-1", "fields": {"assignee": {"name": "Raj"}}},
        {"id": "PAY-1", "fields": {"assignee": ["Raj"]}},
    )

    assert removed.classification == "breaking"
    assert removed.removed_paths == ["$.fields.summary"]
    assert container.classification == "breaking"
    assert container.changed_type_paths["$.fields.assignee"] == {
        "previous": "object",
        "current": "array",
    }


@pytest.mark.req("G2-EKAF-017")
def test_payload_schema_is_stable_and_escapes_path_separators() -> None:
    schema = infer_payload_schema({"a.b": {"tilde~key": True}, "items": [{"id": 1}]})

    assert list(schema) == sorted(schema)
    assert schema["$.a~1b.tilde~0key"] == "boolean"
    assert schema["$.items[]"] == "object"
    assert schema["$.items[].id"] == "integer"


@pytest.mark.req("G2-EKAF-018")
def test_mapping_drift_ledger_records_version_changes_and_builds_replay_plan(tmp_path) -> None:
    ledger = MappingDriftLedger(tmp_path / "state" / "mapping-drift.json")

    unchanged = ledger.record(
        source_id="jira-prod",
        previous_mapping_version="jira/1.0",
        new_mapping_version="jira/1.0",
    )
    first = ledger.record(
        source_id="jira-prod",
        previous_mapping_version="jira/1.0",
        new_mapping_version="jira/2.0",
        replay_from_checkpoint="cursor-10",
        event_ids=["event-b", "event-a"],
        correlation_id="corr-1",
        note="summary mapping changed",
    )
    ledger.record(
        source_id="jira-prod",
        previous_mapping_version="jira/2.0",
        new_mapping_version="jira/3.0",
        event_ids=["event-b", "event-c"],
    )
    ledger.record(
        source_id="gitlab-prod",
        previous_mapping_version="gitlab/1.0",
        new_mapping_version="gitlab/2.0",
        replay_from_checkpoint="cursor-gl",
    )

    document = json.loads((tmp_path / "state" / "mapping-drift.json").read_text())
    plan = MappingDriftLedger(tmp_path / "state" / "mapping-drift.json").replay_plan("jira-prod")

    assert unchanged is None
    assert first is not None
    assert document["schema_version"] == "1.0"
    assert [record.new_mapping_version for record in plan.records] == ["jira/2.0", "jira/3.0"]
    assert plan.replay_from_checkpoint == "cursor-10"
    assert plan.event_ids == ["event-a", "event-b", "event-c"]
