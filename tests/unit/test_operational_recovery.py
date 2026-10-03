import json
import os

import pytest
from eoip.connectors.acquisition import AcquisitionScheduler
from eoip.connectors.registry import SourceRegistry
from eoip.contracts.source_registry import SourceRegistryEntry
from eoip.graph.memory import MemoryGraphStore
from eoip.jobs import JobQueue, write_json
from eoip.snapshot import backup, digest, restore

from scripts.verify_restore import verify_restored_snapshot


def seed(root):
    registry = SourceRegistry(root / "state" / "source-registry.json")
    registry.create(SourceRegistryEntry(
        source_id="confluence-test", source_type="confluence", name="Confluence",
        base_url="https://example.invalid", secret_refs={"token": "env://CONF_TOKEN"},
    ))
    write_json(root / "state" / "connectors" / "confluence-test.json",
               {"cursor": "2026-10-03T00:00:00Z", "baseline_complete": True})
    write_json(root / "state" / "worker.json", {"status": "running"})
    journal = root / "journal" / "semantic-changes.ndjson"
    journal.parent.mkdir()
    journal.write_text('{"event_id":"change-1"}\n', encoding="utf-8")
    queue = JobQueue(root)
    jobs = [queue.submit("JIRA_JSON", {"document": {"issues": []}}) for _ in range(3)]
    for job, status in zip(jobs, ("PENDING", "RUNNING", "SUCCEEDED"), strict=True):
        record = queue.get(job["job_id"])
        write_json(queue.root / f"{job['job_id']}.json", {**record, "status": status})
    return jobs


@pytest.mark.req("NFR-REL-002", "G2-REL-007")
def test_operational_recovery_preserves_state_and_holds_active_jobs(tmp_path):
    source, target = tmp_path / "source", tmp_path / "target"
    jobs = seed(source)
    archive = tmp_path / "backup.json"
    backup(MemoryGraphStore(), source, archive)
    restore(MemoryGraphStore(), target, archive)
    queue = JobQueue(target)
    assert [queue.get(job["job_id"])["status"] for job in jobs] == ["HELD", "HELD", "SUCCEEDED"]
    for job, previous in zip(jobs[:2], ("PENDING", "RUNNING"), strict=True):
        record = queue.get(job["job_id"])
        assert record["recovery"]["original_status"] == previous
        assert record["recovery"]["snapshot_sha256"] == json.loads(archive.read_text())["sha256"]
        assert record["payload"] == {"document": {"issues": []}}
    assert not (target / "state" / "worker.json").exists()
    assert (target / "journal" / "semantic-changes.ndjson").read_bytes() == (
        source / "journal" / "semantic-changes.ndjson"
    ).read_bytes()
    assert (target / "state" / "connectors" / "confluence-test.json").read_bytes() == (
        source / "state" / "connectors" / "confluence-test.json"
    ).read_bytes()
    assert SourceRegistry(target / "state" / "source-registry.json").get(
        "confluence-test"
    ).secret_refs == {"token": "env://CONF_TOKEN"}
    verify_restored_snapshot(MemoryGraphStore(), target, archive)


@pytest.mark.parametrize("name", [
    "state/../../escape.json", "state/worker.json", "jobs/not-a-uuid.json",
    "state/CON.json", "state/path./checkpoint.json",
])
def test_operational_paths_refused_before_graph_or_file_mutation(tmp_path, name):
    source = MemoryGraphStore()
    source.upsert_vertex("WorkItem", {"canonical_id": "test:1", "issue_key": "TEST-1"})
    archive = tmp_path / "backup.json"
    backup(source, tmp_path / "source", archive)
    document = json.loads(archive.read_text())
    document["payload"]["operational_files"] = {name: "{}"}
    document["sha256"] = digest(document["payload"])
    write_json(archive, document)
    target = MemoryGraphStore()
    with pytest.raises((ValueError, TypeError), match="operational"):
        restore(target, tmp_path / "target", archive)
    assert target.count_vertices() == 0
    assert not (tmp_path / "target").exists()


def test_restore_refuses_existing_operational_state_before_mutation(tmp_path):
    archive = tmp_path / "backup.json"
    backup(MemoryGraphStore(), tmp_path / "source", archive)
    root = tmp_path / "target"
    write_json(root / "state" / "connectors" / "existing.json", {"cursor": "keep"})
    with pytest.raises(ValueError, match="empty application"):
        restore(MemoryGraphStore(), root, archive)
    assert json.loads((root / "state" / "connectors" / "existing.json").read_text()) == {"cursor": "keep"}


def test_held_jobs_require_explicit_readmission_or_cancellation(tmp_path):
    jobs = seed(tmp_path / "source")
    archive = tmp_path / "backup.json"
    backup(MemoryGraphStore(), tmp_path / "source", archive)
    root = tmp_path / "target"
    restore(MemoryGraphStore(), root, archive)
    queue = JobQueue(root)
    admitted = queue.readmit(jobs[0]["job_id"], correlation_id="operator-readmission")
    assert admitted["status"] == "PENDING"
    assert admitted["correlation_id"] == "operator-readmission"
    assert admitted["recovery"]["original_status"] == "PENDING"
    assert admitted["recovery"]["readmitted_at"]
    assert "payload" not in admitted
    with pytest.raises(RuntimeError, match="held"):
        queue.readmit(jobs[0]["job_id"])
    assert queue.cancel(jobs[1]["job_id"])["status"] == "CANCELLED"


def test_nullable_demo_payload_survives_recovery(tmp_path):
    source, target = tmp_path / "source", tmp_path / "target"
    job = JobQueue(source).submit("DEMO")
    archive = tmp_path / "backup.json"
    backup(MemoryGraphStore(), source, archive)
    restore(MemoryGraphStore(), target, archive)
    queue = JobQueue(target)
    assert queue.get(job["job_id"])["payload"] is None
    assert queue.get(job["job_id"])["status"] == "HELD"
    verify_restored_snapshot(MemoryGraphStore(), target, archive)
    assert queue.readmit(job["job_id"])["status"] == "PENDING"


def test_held_source_job_readmission_rechecks_scheduler_admission(tmp_path):
    jobs = seed(tmp_path / "source")
    source_queue = JobQueue(tmp_path / "source")
    job = source_queue.get(jobs[0]["job_id"])
    job.update(kind="SOURCE_OPERATION", payload={
        "source_id": "confluence-test", "operation": "REPLAY", "checkpoint": None,
        "event_ids": ["event-1"], "dry_run": False,
    })
    write_json(source_queue.root / f"{job['job_id']}.json", job)
    archive = tmp_path / "backup.json"
    backup(MemoryGraphStore(), tmp_path / "source", archive)
    root = tmp_path / "target"
    restore(MemoryGraphStore(), root, archive)
    queue = JobQueue(root)
    registry = SourceRegistry(root / "state" / "source-registry.json")
    scheduler = AcquisitionScheduler(root, registry, queue)
    scheduler.pause("confluence-test")
    with pytest.raises(RuntimeError, match="paused"):
        scheduler.readmit(job["job_id"], correlation_id="operator")
    assert queue.get(job["job_id"])["status"] == "HELD"
    scheduler.resume("confluence-test")
    assert scheduler.readmit(job["job_id"], correlation_id="operator")["status"] == "PENDING"


@pytest.mark.parametrize("records", [None, [], {"state/test.json": 123}])
def test_malformed_operational_archive_is_refused_before_mutation(tmp_path, records):
    archive = tmp_path / "backup.json"
    backup(MemoryGraphStore(), tmp_path / "source", archive)
    document = json.loads(archive.read_text())
    document["payload"]["operational_files"] = records
    document["sha256"] = digest(document["payload"])
    write_json(archive, document)
    target = MemoryGraphStore()
    with pytest.raises((ValueError, TypeError), match="operational"):
        restore(target, tmp_path / "target", archive)
    assert target.count_vertices() == 0
    assert not (tmp_path / "target").exists()


def test_verifier_handles_preexisting_hold_and_detects_operational_loss(tmp_path):
    source, target = tmp_path / "source", tmp_path / "target"
    jobs = seed(source)
    queue = JobQueue(source)
    job = queue.get(jobs[0]["job_id"])
    job.update(status="HELD", recovery={
        "original_status": "PENDING", "snapshot_sha256": "previous",
        "restored_at": "2026-01-01T00:00:00Z",
    })
    write_json(queue.root / f"{job['job_id']}.json", job)
    archive = tmp_path / "backup.json"
    backup(MemoryGraphStore(), source, archive)
    restore(MemoryGraphStore(), target, archive)
    verify_restored_snapshot(MemoryGraphStore(), target, archive)
    (target / "state" / "connectors" / "confluence-test.json").unlink()
    with pytest.raises(AssertionError, match="operational"):
        verify_restored_snapshot(MemoryGraphStore(), target, archive)


def test_authenticated_recovery_readmission_endpoint(monkeypatch, tmp_path):
    from tests.unit.test_deployment_api import client

    api = client(monkeypatch, tmp_path / "target")
    jobs = seed(tmp_path / "source")
    archive = tmp_path / "backup.json"
    backup(MemoryGraphStore(), tmp_path / "source", archive)
    restore(MemoryGraphStore(), tmp_path / "target", archive)
    queue = JobQueue(tmp_path / "target")
    url = f"/api/v1/admin/jobs/{jobs[0]['job_id']}/readmit"
    assert api.post(url).status_code == 401
    assert queue.get(jobs[0]["job_id"])["status"] == "HELD"
    api.headers.update({
        "Authorization": f"Bearer {os.environ['EOIP_API_TOKEN']}",
        "X-Correlation-ID": "recovery-operator",
    })
    result = api.post(url)
    assert result.status_code == 202
    assert result.headers["X-Audit-ID"]
    assert result.json()["status"] == "PENDING"
    assert result.json()["correlation_id"] == "recovery-operator"
    assert "payload" not in result.json()
    assert api.post(url).status_code == 409
    assert api.post("/api/v1/admin/jobs/not-a-uuid/readmit").status_code == 404
    webhook = queue.get(jobs[1]["job_id"])
    webhook["kind"] = "SOURCE_WEBHOOK"
    write_json(queue.root / f"{webhook['job_id']}.json", webhook)
    refused = api.post(f"/api/v1/admin/jobs/{webhook['job_id']}/readmit")
    assert refused.status_code == 409
    assert "receipt recovery" in refused.json()["detail"]
    assert queue.get(webhook["job_id"])["status"] == "HELD"


@pytest.mark.parametrize("control", ["disabled", "paused", "capability", "concurrency", "rate", "audit"])
def test_source_recovery_endpoint_refuses_without_mutation(monkeypatch, tmp_path, control):
    from eoip.connectors.acquisition import AcquisitionPolicy

    from tests.unit.test_deployment_api import client

    source, target = tmp_path / "source", tmp_path / "target"
    jobs = seed(source)
    queue = JobQueue(source)
    job = queue.get(jobs[0]["job_id"])
    job.update(kind="SOURCE_OPERATION", payload={
        "source_id": "confluence-test", "operation": "REPLAY", "event_ids": ["event-1"],
    })
    write_json(queue.root / f"{job['job_id']}.json", job)
    archive = tmp_path / "backup.json"
    backup(MemoryGraphStore(), source, archive)
    restore(MemoryGraphStore(), target, archive)
    registry = SourceRegistry(target / "state" / "source-registry.json")
    queue = JobQueue(target)
    scheduler = AcquisitionScheduler(target, registry, queue)
    if control == "disabled":
        registry.update("confluence-test", {"enabled": False})
    elif control == "paused":
        scheduler.pause("confluence-test")
    elif control == "capability":
        registry.update("confluence-test", {"capabilities": {"replay": False}})
    elif control in {"concurrency", "rate"}:
        scheduler.set_policy("confluence-test", AcquisitionPolicy(rate_limit_per_minute=1))
        admitted = scheduler.submit("confluence-test", "REPLAY", event_ids=["event-2"])
        if control == "rate":
            record = queue.get(admitted["job_id"])
            write_json(queue.root / f"{record['job_id']}.json", {**record, "status": "SUCCEEDED"})
    api = client(monkeypatch, target)
    if control == "audit":
        from apps.api import main

        def unavailable(*args, **kwargs):
            raise OSError("audit volume unavailable")

        monkeypatch.setattr(main.AuditSink, "emit", unavailable)
    before = (queue.root / f"{job['job_id']}.json").read_bytes()
    result = api.post(f"/api/v1/admin/jobs/{job['job_id']}/readmit",
                      headers={"Authorization": f"Bearer {os.environ['EOIP_API_TOKEN']}"})
    assert result.status_code == (503 if control == "audit" else 422 if control == "capability" else 409)
    assert (queue.root / f"{job['job_id']}.json").read_bytes() == before
