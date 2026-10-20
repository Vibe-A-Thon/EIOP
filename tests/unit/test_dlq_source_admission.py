"""Registered DLQ replay must obey the same admission policy as source replay."""

from _principals import provision_api_token
import json

import pytest
from eoip.connectors.acquisition import AcquisitionPolicy, AcquisitionScheduler
from eoip.connectors.registry import SourceRegistry
from eoip.contracts.source_event import SourceEventV2
from eoip.contracts.source_registry import SourceRegistryEntry
from eoip.graph.memory import MemoryGraphStore
from eoip.jobs import JobQueue, write_json
from fastapi.testclient import TestClient


@pytest.mark.parametrize("control", ["disabled", "paused", "capability", "concurrency", "rate"])
@pytest.mark.parametrize("route", ["dlq", "source"])
def test_registered_replay_admission_parity(monkeypatch, tmp_path, control, route):
    from apps.api import main as api_main

    store = MemoryGraphStore()
    monkeypatch.setattr(api_main, "create_store", lambda: store)
    provision_api_token(monkeypatch, "x" * 32)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    registry = SourceRegistry(tmp_path / "state" / "source-registry.json")
    registry.create(SourceRegistryEntry(
        source_id="sn-prod", source_type="servicenow", name="ServiceNow",
        base_url="https://example.invalid",
    ))
    event = SourceEventV2(
        event_id="b" * 64, source_system="servicenow", source_instance_id="instance",
        source_record_id="incident:broken", event_time="2026-10-03T00:00:00Z",
        content_hash="c" * 64, payload={"sys_id": "broken"},
    )
    write_json(tmp_path / "raw" / "servicenow" / f"{event.event_id}.json",
               event.model_dump(mode="json"))
    write_json(tmp_path / "dlq" / f"{event.event_id}.json", {
        "source_system": "servicenow", "payload_hash": event.payload_hash,
        "registry_source_id": "sn-prod", "event_id": event.event_id,
    })
    queue = JobQueue(tmp_path)
    scheduler = AcquisitionScheduler(tmp_path, registry, queue)
    if control == "disabled":
        registry.update("sn-prod", {"enabled": False})
    elif control == "paused":
        scheduler.pause("sn-prod")
    elif control == "capability":
        registry.update("sn-prod", {"capabilities": {"replay": False}})
    else:
        scheduler.set_policy("sn-prod", AcquisitionPolicy(rate_limit_per_minute=1))
        admitted = scheduler.submit("sn-prod", "REPLAY", event_ids=[event.event_id])
        if control == "rate":
            path = tmp_path / "jobs" / f"{admitted['job_id']}.json"
            job = json.loads(path.read_text(encoding="utf-8"))
            write_json(path, {**job, "status": "SUCCEEDED"})
    jobs_before = {path.name for path in (tmp_path / "jobs").glob("*.json")}
    graph_before = store.count_vertices()
    client = TestClient(api_main.create_app())
    try:
        endpoint = (f"/api/v1/admin/dlq/{event.event_id}/replay" if route == "dlq"
                    else "/api/v1/sources/sn-prod/replay")
        response = client.post(endpoint, json={"event_ids": [event.event_id]},
                               headers={"Authorization": "Bearer " + "x" * 32})
        assert response.status_code == (422 if control == "capability" else 409), response.text
        assert {path.name for path in (tmp_path / "jobs").glob("*.json")} == jobs_before
        assert store.count_vertices() == graph_before
    finally:
        client.close()
