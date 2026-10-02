from __future__ import annotations

from collections.abc import Iterable, Iterator

import pytest
from eoip.connectors.base import ConnectorHealth, DiscoveryResult, DiscoveryScope, SourceConnector
from eoip.contracts.revision import GraphRevision, RevisionMetadata
from eoip.contracts.source_event import SourceEvent, SourceEventV2, upgrade_source_event
from eoip.contracts.source_registry import SourceCapabilities
from pydantic import ValidationError


@pytest.mark.req("G2-T0002")
def test_v1_source_event_upgrade_preserves_identity_and_hash() -> None:
    legacy = SourceEvent(
        event_id="event-1",
        source_system="jira",
        source_record_id="EOIP-1",
        source_version="7",
        captured_at="2026-10-03T00:00:00Z",
        payload_hash="abc123",
        payload={"key": "EOIP-1"},
        metadata={"source_instance_id": "jira-prod"},
    )

    upgraded = upgrade_source_event(
        legacy,
        operation="UPDATE",
        cursor="cursor-7",
        permissions={"visibility": "RESTRICTED", "principal_refs": ["group:engineering"]},
    )

    assert upgraded.schema_version == "2.0"
    assert upgraded.event_id == legacy.event_id
    assert upgraded.payload_hash == legacy.payload_hash
    assert upgraded.source_instance_id == "jira-prod"
    assert upgraded.operation == "UPDATE"
    assert upgraded.cursor == "cursor-7"


@pytest.mark.req("G2-T0002")
def test_v2_event_requires_payload_reference_except_for_delete() -> None:
    common = {
        "event_id": "event-2",
        "source_system": "github",
        "source_instance_id": "github-enterprise",
        "source_record_id": "repo/1",
        "event_time": "2026-10-03T00:00:00Z",
        "content_hash": "deleted-record",
    }
    with pytest.raises(ValidationError):
        SourceEventV2(**common)

    deleted = SourceEventV2(**common, operation="DELETE")
    assert deleted.payload is None


@pytest.mark.req("G2-T0003")
def test_revision_contract_enforces_open_current_and_closed_historical_ranges() -> None:
    current = RevisionMetadata(
        revision_id="revision-2",
        valid_from="2026-10-03T00:00:00Z",
        observed_at="2026-10-03T00:01:00Z",
        previous_revision="revision-1",
        source_version="2",
    )
    revision = GraphRevision(
        canonical_id="urn:eoip:work:item:jira:EOIP-1",
        entity_type="WorkItem",
        revision=current,
        properties={"status": "Done"},
        source_event_id="event-2",
    )
    assert revision.revision.is_current is True

    with pytest.raises(ValidationError):
        RevisionMetadata(
            revision_id="revision-1",
            valid_from="2026-10-01T00:00:00Z",
            observed_at="2026-10-01T00:01:00Z",
            is_current=False,
        )


class FakeConnector:
    source_id = "fake-1"

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(polling=True)

    def discover(self, scope: DiscoveryScope) -> DiscoveryResult:
        return DiscoveryResult(source_id=self.source_id)

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        return iter(())

    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]:
        return iter(())

    def handle_event(self, event: dict) -> Iterator[SourceEventV2]:
        return iter(())

    def fetch_record(self, ref: str) -> SourceEventV2:
        raise LookupError(ref)

    def health(self) -> ConnectorHealth:
        return ConnectorHealth(status="HEALTHY", checked_at="2026-10-03T00:00:00Z")

    def replay(self, events: Iterable[SourceEventV2]) -> Iterator[SourceEventV2]:
        return iter(events)


@pytest.mark.req("G2-T0005")
def test_fake_connector_satisfies_runtime_connector_protocol() -> None:
    connector = FakeConnector()
    assert isinstance(connector, SourceConnector)
    assert connector.capabilities().polling is True
    assert connector.discover(DiscoveryScope()).source_id == "fake-1"
