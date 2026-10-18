"""Integration tests for Durable Jobs, Leases, Fencing, Outbox, and Governed DLQ (CRA-031.1 - CRA-031.7, CRA-031.A).

Exercises:
1. Multi-instance claims and two-worker race conditions (CRA-031.5, CRA-031.6).
2. Worker lease expiration, checkpoint reclamation, and fencing of expired workers (CRA-031.5, CRA-031.6).
3. Transactional publication outbox intent persistence on commit (CRA-031.2).
4. Poison payload and non-idempotent mutation handling in governed DLQ with redacted secrets (CRA-031.4, CRA-031.7).
5. Mid-job cancellation and revocation fencing (CRA-031.5, CRA-031.A).
6. DLQ replay with audit authority and re-execution (CRA-031.7, CRA-031.A).
7. Tenant-scoped isolation across claims and DLQ operations.
"""

from __future__ import annotations

import time
from pathlib import Path
import pytest

from eoip.jobs import (
    DurableJobStore,
    FencedWorkerError,
    redact_diagnostics,
)


def test_durable_store_two_worker_claim_race(tmp_path: Path):
    """CRA-031.5, CRA-031.6: Two workers racing to claim jobs; only one gets each job."""
    db_file = tmp_path / "jobs.sqlite"
    store = DurableJobStore(db_file)

    # Submit 2 jobs
    j1 = store.submit("SYNC_JIRA", {"project": "ALPHA"}, tenant_id="t1")
    j2 = store.submit("SYNC_CONFLUENCE", {"space": "DOCS"}, tenant_id="t1")

    # Worker 1 and Worker 2 claim
    claim1 = store.claim_job(worker_id="worker-1", lease_ttl_s=30.0)
    claim2 = store.claim_job(worker_id="worker-2", lease_ttl_s=30.0)
    claim3 = store.claim_job(worker_id="worker-1", lease_ttl_s=30.0)

    assert claim1 is not None
    assert claim2 is not None
    assert claim3 is None  # No more pending jobs

    # Ensure workers claimed distinct jobs
    assert claim1["job_id"] != claim2["job_id"]
    assert claim1["lease_holder"] == "worker-1"
    assert claim2["lease_holder"] == "worker-2"
    assert claim1["fencing_token"] == 1
    assert claim2["fencing_token"] == 1


def test_worker_lease_expiration_and_fencing(tmp_path: Path):
    """CRA-031.5, CRA-031.6: Worker 1 lease expires, Worker 2 reclaims, Worker 1 is fenced."""
    db_file = tmp_path / "jobs.sqlite"
    store = DurableJobStore(db_file)

    store.submit("IMPORT_SCHEMA", {"target": "neo4j"}, tenant_id="t1")

    # Worker 1 claims with very short lease TTL (0.1s)
    w1_job = store.claim_job(worker_id="worker-1", lease_ttl_s=0.1)
    assert w1_job is not None
    job_id = w1_job["job_id"]
    w1_fence = w1_job["fencing_token"]
    assert w1_fence == 1

    # Worker 1 saves checkpoint
    store.checkpoint(job_id, worker_id="worker-1", fencing_token=w1_fence, state_data={"processed_rows": 50})

    # Wait for lease to expire
    time.sleep(0.2)

    # Worker 2 claims the expired job
    w2_job = store.claim_job(worker_id="worker-2", lease_ttl_s=30.0)
    assert w2_job is not None
    assert w2_job["job_id"] == job_id
    assert w2_job["lease_holder"] == "worker-2"
    assert w2_job["fencing_token"] == 2  # Incremented fencing token!
    assert w2_job["checkpoint"] == {"processed_rows": 50}  # Reclaimed from checkpoint

    # Expired Worker 1 attempts to heartbeat -> must be fenced
    with pytest.raises(FencedWorkerError):
        store.heartbeat(job_id, worker_id="worker-1", fencing_token=w1_fence)

    # Expired Worker 1 attempts to commit -> must be fenced
    with pytest.raises(FencedWorkerError):
        store.commit_job(job_id, worker_id="worker-1", fencing_token=w1_fence)

    # Worker 2 successfully completes and commits
    store.commit_job(job_id, worker_id="worker-2", fencing_token=2)
    completed = store.get_job(job_id)
    assert completed["status"] == "COMPLETED"
    assert completed["finished_at"] is not None


def test_transactional_outbox_on_commit(tmp_path: Path):
    """CRA-031.2: Commit persists publication outbox intent in the same transaction."""
    db_file = tmp_path / "jobs.sqlite"
    store = DurableJobStore(db_file)

    store.submit("GENERATE_EMBEDDINGS", {"nodes": 100}, tenant_id="tenant-acme")
    job = store.claim_job(worker_id="worker-fast", lease_ttl_s=30.0)
    assert job is not None

    outbox_events = [
        {"event_type": "GRAPH_MUTATED", "payload": {"node_count": 100}},
        {"event_type": "EMBEDDINGS_REFRESHED", "payload": {"model": "onnx-bge"}},
    ]

    store.commit_job(
        job["job_id"],
        worker_id="worker-fast",
        fencing_token=job["fencing_token"],
        outbox_events=outbox_events,
    )

    outbox_rows = store.list_outbox()
    assert len(outbox_rows) == 2
    types = [r["event_type"] for r in outbox_rows]
    assert "GRAPH_MUTATED" in types
    assert "EMBEDDINGS_REFRESHED" in types
    assert all(r["tenant_id"] == "tenant-acme" for r in outbox_rows)


def test_secret_redaction_and_governed_dlq(tmp_path: Path):
    """CRA-031.4, CRA-031.7: Secret redaction in diagnostics and governed DLQ for non-idempotent/poison failures."""
    # Test secret redaction utility
    diagnostic_output = (
        "Error in API call: Authorization: Bearer secret_token_xyz123\n"
        "Connect string: postgresql://admin:password123@db:5432/db\n"
        "URL was https://service.internal/api?key=my_super_secret_api_key&safe=true\n"
        "Config dict: {'api_key': 'ak_live_abcdef'}"
    )
    redacted = redact_diagnostics(diagnostic_output)
    assert "secret_token_xyz123" not in redacted
    assert "password123" not in redacted
    assert "my_super_secret_api_key" not in redacted
    assert "ak_live_abcdef" not in redacted
    assert "[REDACTED]" in redacted

    db_file = tmp_path / "jobs.sqlite"
    store = DurableJobStore(db_file)

    # 1. Non-idempotent mutation job failure immediately routed to DLQ (CRA-031.4)
    store.submit("DELETE_RECORDS", {"filter": "test"}, tenant_id="t1", is_idempotent=False)
    j_mutation = store.claim_job(worker_id="w-mut")
    assert j_mutation is not None

    store.fail_job(
        j_mutation["job_id"],
        worker_id="w-mut",
        fencing_token=j_mutation["fencing_token"],
        error_message="Network partition with api_key=secret_xyz",
        stack_trace="Traceback: Bearer super_secret_token at line 42",
        is_poison=False,
    )

    j_post = store.get_job(j_mutation["job_id"])
    assert j_post["status"] == "DEAD_LETTER"

    dlq_items = store.list_dlq(tenant_id="t1")
    assert len(dlq_items) == 1
    dlq_item = dlq_items[0]
    assert dlq_item["reason"] == "NON_IDEMPOTENT_MUTATION_FAILURE"
    assert "secret_xyz" not in dlq_item["error_diagnostics"]
    assert "super_secret_token" not in dlq_item["error_diagnostics"]
    assert "[REDACTED]" in dlq_item["error_diagnostics"]


def test_mid_job_cancellation_fences_worker(tmp_path: Path):
    """CRA-031.5, CRA-031.A: Job cancelled mid-execution fences worker immediately."""
    db_file = tmp_path / "jobs.sqlite"
    store = DurableJobStore(db_file)

    store.submit("LONG_RUNNING_ETL", {"target": "warehouse"}, tenant_id="tenant-corp")
    job = store.claim_job(worker_id="w-long", lease_ttl_s=30.0)
    assert job is not None

    # Administrator cancels the job mid-execution
    store.cancel(job["job_id"], cancelled_by="admin_sec", tenant_id="tenant-corp")

    # Worker attempts heartbeat -> fenced!
    with pytest.raises(FencedWorkerError):
        store.heartbeat(job["job_id"], worker_id="w-long", fencing_token=job["fencing_token"])

    # Worker attempts commit -> fenced!
    with pytest.raises(FencedWorkerError):
        store.commit_job(job["job_id"], worker_id="w-long", fencing_token=job["fencing_token"])


def test_dlq_replay_with_audit_authority(tmp_path: Path):
    """CRA-031.7, CRA-031.A: DLQ replay requires authority and resets job to PENDING."""
    db_file = tmp_path / "jobs.sqlite"
    store = DurableJobStore(db_file)

    store.submit("POISON_JOB", {"data": "corrupt"}, tenant_id="t-dlq")
    job = store.claim_job(worker_id="w-dlq")
    assert job is not None

    store.fail_job(
        job["job_id"],
        worker_id="w-dlq",
        fencing_token=job["fencing_token"],
        error_message="Invalid format",
        stack_trace="Traceback ...",
        is_poison=True,
    )

    dlq_items = store.list_dlq(tenant_id="t-dlq")
    assert len(dlq_items) == 1
    dlq_id = dlq_items[0]["dlq_id"]

    # Replay without authority rejected
    with pytest.raises(PermissionError):
        store.replay_dlq(dlq_id, replay_authority="", tenant_id="t-dlq")

    # Cross-tenant replay rejected
    with pytest.raises(PermissionError):
        store.replay_dlq(dlq_id, replay_authority="admin", tenant_id="wrong-tenant")

    # Authorized replay succeeds
    res = store.replay_dlq(dlq_id, replay_authority="operator@acme.corp", tenant_id="t-dlq")
    assert res["status"] == "REQUEUED"

    # Job is back to PENDING and can be reclaimed
    reclaimed = store.claim_job(worker_id="w-new", lease_ttl_s=30.0)
    assert reclaimed is not None
    assert reclaimed["job_id"] == job["job_id"]
    assert reclaimed["attempts"] == 1
    assert reclaimed["lease_holder"] == "w-new"
