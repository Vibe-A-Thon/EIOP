"""Acquisition and sync semantics: full rebuild, backfill, selective rescan."""

import pytest
from eoip.connectors.acquisition import (
    AcquisitionPolicy,
    AcquisitionScheduler,
    BackfillSpec,
    SelectiveRescanFilter,
)
from eoip.connectors.registry import SourceRegistry
from eoip.contracts.source_registry import SourceRegistryEntry
from eoip.jobs import JobQueue


def _source(source_id: str = "confluence-prod") -> SourceRegistryEntry:
    return SourceRegistryEntry(
        source_id=source_id,
        source_type="confluence",
        name="Production Confluence",
        base_url="https://confluence.example.test",
        capabilities={"polling": True, "reconciliation": True, "replay": True},
        secret_refs={"token": "env://EOIP_CONFLUENCE_PROD_TOKEN"},
    )


@pytest.mark.req("G2-SYNC-010")
def test_full_rebuild_requires_explicit_maintenance_authorization(tmp_path):
    registry = SourceRegistry(tmp_path / "state" / "source-registry.json")
    registry.create(_source())
    queue = JobQueue(tmp_path)
    scheduler = AcquisitionScheduler(tmp_path, registry, queue)

    # Full rebuild without maintenance authorization is rejected
    with pytest.raises(ValueError, match="Full rebuild is exceptional"):
        scheduler.submit("confluence-prod", "FULL_REBUILD")

    # Full rebuild with explicit maintenance authorization is admitted
    result = scheduler.submit("confluence-prod", "FULL_REBUILD", maintenance=True)
    job = queue.get(result["job_id"])
    assert job["payload"]["operation"] == "FULL_REBUILD"
    assert job["payload"]["maintenance"] is True


@pytest.mark.req("G2-SYNC-013")
def test_bounded_historical_backfill_submits_bounded_specification(tmp_path):
    registry = SourceRegistry(tmp_path / "state" / "source-registry.json")
    registry.create(_source())
    queue = JobQueue(tmp_path)
    scheduler = AcquisitionScheduler(tmp_path, registry, queue)

    spec = BackfillSpec(
        entity_type="Document",
        mapping_version="v2.1",
        start_cursor="cursor-100",
        end_cursor="cursor-200",
        max_records=500,
    )

    with pytest.raises(ValueError, match="backfill_spec is required"):
        scheduler.submit("confluence-prod", "BACKFILL")

    result = scheduler.submit("confluence-prod", "BACKFILL", backfill_spec=spec)
    job = queue.get(result["job_id"])
    assert job["payload"]["operation"] == "BACKFILL"
    assert job["payload"]["backfill_spec"]["entity_type"] == "Document"
    assert job["payload"]["backfill_spec"]["start_cursor"] == "cursor-100"
    assert job["payload"]["backfill_spec"]["end_cursor"] == "cursor-200"
    assert job["payload"]["backfill_spec"]["max_records"] == 500


@pytest.mark.req("G2-SYNC-014")
def test_selective_rescan_submits_filters_by_criteria(tmp_path):
    registry = SourceRegistry(tmp_path / "state" / "source-registry.json")
    registry.create(_source())
    queue = JobQueue(tmp_path)
    scheduler = AcquisitionScheduler(tmp_path, registry, queue)

    filter_criteria = SelectiveRescanFilter(
        entity_type="Document",
        path="docs/architecture/*",
        repository="org/repo-main",
        project="PROJ",
        time_range_start="2026-09-01T00:00:00Z",
        time_range_end="2026-10-01T00:00:00Z",
        source_id="confluence-prod",
    )

    with pytest.raises(ValueError, match="rescan_filter is required"):
        scheduler.submit("confluence-prod", "RESCAN")

    result = scheduler.submit("confluence-prod", "RESCAN", rescan_filter=filter_criteria)
    job = queue.get(result["job_id"])
    assert job["payload"]["operation"] == "RESCAN"
    rescan = job["payload"]["rescan_filter"]
    assert rescan["entity_type"] == "Document"
    assert rescan["path"] == "docs/architecture/*"
    assert rescan["repository"] == "org/repo-main"
    assert rescan["project"] == "PROJ"
    assert rescan["time_range_start"] == "2026-09-01T00:00:00Z"
    assert rescan["source_id"] == "confluence-prod"
