from __future__ import annotations

import pytest
from pathlib import Path
from eoip.jobs import JobQueue

pytestmark = [pytest.mark.req("GAP-JOB-001", "SR-TEN-001", "CP-10")]


def test_job_queue_tenant_isolation(tmp_path: Path):
    queue = JobQueue(tmp_path)

    # Tenant-alpha submits a job
    job_alpha = queue.submit(
        "JIRA_JSON",
        {"issues": [1, 2]},
        tenant_id="tenant-alpha",
        created_by="alice",
    )
    job_alpha_id = job_alpha["job_id"]
    assert job_alpha["tenant_id"] == "tenant-alpha"
    assert job_alpha["created_by"] == "alice"
    assert job_alpha["status"] == "PENDING"

    # Tenant-beta submits a job
    job_beta = queue.submit(
        "GITLAB_JSON",
        {"mr": 42},
        tenant_id="tenant-beta",
        created_by="bob",
    )
    job_beta_id = job_beta["job_id"]

    # 1. Tenant-alpha can get own job
    fetched_alpha = queue.get(job_alpha_id, tenant_id="tenant-alpha")
    assert fetched_alpha["job_id"] == job_alpha_id
    assert fetched_alpha["payload"] == {"issues": [1, 2]}

    # 2. Tenant-beta trying to get Tenant-alpha's job raises PermissionError
    with pytest.raises(PermissionError) as exc:
        queue.get(job_alpha_id, tenant_id="tenant-beta")
    assert "Cross-tenant job access forbidden" in str(exc.value)

    # 3. Listing with tenant-alpha only returns tenant-alpha jobs
    list_alpha = queue.list(tenant_id="tenant-alpha")
    assert len(list_alpha) == 1
    assert list_alpha[0]["job_id"] == job_alpha_id

    # 4. Listing with tenant-beta only returns tenant-beta jobs
    list_beta = queue.list(tenant_id="tenant-beta")
    assert len(list_beta) == 1
    assert list_beta[0]["job_id"] == job_beta_id

    # 5. Global/admin listing (no tenant filter) returns both
    list_all = queue.list()
    assert len(list_all) == 2

    # 6. Tenant-beta cannot cancel Tenant-alpha's job
    with pytest.raises(PermissionError):
        queue.cancel(job_alpha_id, tenant_id="tenant-beta")

    # 7. Tenant-alpha can cancel own job
    cancelled = queue.cancel(job_alpha_id, tenant_id="tenant-alpha")
    assert cancelled["status"] == "CANCELLED"
    assert queue.get(job_alpha_id, tenant_id="tenant-alpha")["status"] == "CANCELLED"
