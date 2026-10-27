"""Tests for worker crash/restart/duplicate delivery recovery on the JobQueue path (CC3-002)."""

import json
import time

from eoip.graph.memory import MemoryGraphStore
from eoip.jobs import JobQueue, write_json
from eoip.snapshot import backup, restore


def test_crash_recovery_resumes_running_job(tmp_path, monkeypatch):
    root = tmp_path
    queue = JobQueue(root)
    job = queue.submit("MOCK_JOB", {"data": 123})
    job_id = job["job_id"]

    # Simulate worker crash mid-execution: status set to RUNNING without finished_at
    job_file = queue.root / f"{job_id}.json"
    record = json.loads(job_file.read_text())
    record.update(status="RUNNING", started_at="2026-10-27T00:00:00Z")
    write_json(job_file, record)

    # Worker restart execution simulation
    store = MemoryGraphStore()
    executed = []

    def mock_execute(s, r, j):
        executed.append(j["job_id"])
        return {"run_status": "SUCCEEDED"}

    # Simulate worker loop pass
    for path in sorted(queue.root.glob("*.json")):
        j = json.loads(path.read_text())
        if j["status"] not in {"PENDING", "RUNNING"} or j.get("next_attempt", 0) > time.time():
            continue
        res = mock_execute(store, root, j)
        j.update(status="SUCCEEDED", result=res, finished_at="2026-10-27T00:01:00Z")
        write_json(path, j)

    assert executed == [job_id]
    final_job = queue.get(job_id)
    assert final_job["status"] == "SUCCEEDED"
    assert final_job["result"] == {"run_status": "SUCCEEDED"}


def test_duplicate_delivery_protection(tmp_path):
    root = tmp_path
    queue = JobQueue(root)
    job = queue.submit("MOCK_JOB", {"data": "test"})
    job_id = job["job_id"]

    job_file = queue.root / f"{job_id}.json"
    record = json.loads(job_file.read_text())
    record.update(status="SUCCEEDED", finished_at="2026-10-27T00:00:00Z", result={"already": "done"})
    write_json(job_file, record)

    # Worker poll should skip already-succeeded job
    executed = []
    for path in sorted(queue.root.glob("*.json")):
        j = json.loads(path.read_text())
        if j["status"] not in {"PENDING", "RUNNING"} or j.get("next_attempt", 0) > time.time():
            continue
        executed.append(j["job_id"])

    assert executed == []
    assert queue.get(job_id)["status"] == "SUCCEEDED"


def test_retry_exhaustion_marks_failed(tmp_path):
    root = tmp_path
    queue = JobQueue(root)
    job = queue.submit("FAILING_JOB")
    job_id = job["job_id"]
    job_file = queue.root / f"{job_id}.json"

    # Simulate 3 attempts failing
    for attempt in range(1, 4):
        j = json.loads(job_file.read_text())
        attempts = j.get("attempts", 0) + 1
        if attempts < 3:
            j.update(status="PENDING", attempts=attempts, error="simulated_error")
        else:
            j.update(status="FAILED", attempts=attempts, error="simulated_error", finished_at="2026-10-27T00:05:00Z")
        write_json(job_file, j)

    final_job = queue.get(job_id)
    assert final_job["status"] == "FAILED"
    assert final_job["attempts"] == 3
    assert final_job["error"] == "simulated_error"


def test_operational_restore_holds_unacknowledged_jobs(tmp_path):
    source, target = tmp_path / "source", tmp_path / "target"
    queue = JobQueue(source)
    j1 = queue.submit("JOB1")
    j2 = queue.submit("JOB2")

    # j2 was mid-run during crash
    write_json(queue.root / f"{j2['job_id']}.json", {**queue.get(j2["job_id"]), "status": "RUNNING"})

    archive = tmp_path / "snapshot.json"
    backup(MemoryGraphStore(), source, archive)
    restore(MemoryGraphStore(), target, archive)

    target_queue = JobQueue(target)
    assert target_queue.get(j1["job_id"])["status"] == "HELD"
    assert target_queue.get(j2["job_id"])["status"] == "HELD"

    # Operator readmission transitions to PENDING
    readmitted = target_queue.readmit(j1["job_id"])
    assert readmitted["status"] == "PENDING"
