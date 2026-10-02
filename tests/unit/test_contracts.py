from eoip.contracts import AuditEvent, SourceEvent


def test_source_event_contract_imports_and_sets_capture_time() -> None:
    event = SourceEvent(
        event_id="event-1",
        source_system="jira",
        source_record_id="EOIP-1",
        payload_hash="abc123",
        payload={"key": "EOIP-1"},
    )

    assert event.captured_at.endswith("Z")


def test_audit_event_timestamp_uses_a_per_instance_factory() -> None:
    assert AuditEvent.model_fields["timestamp"].default_factory is not None
