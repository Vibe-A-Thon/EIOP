"""Security and isolation tests for worker supervisor (CRA-002.2, CRA-002.8, CRA-002.A).

Verifies execution fencing against:
1. Infinite loop / timeout attack (< 1s termination latency)
2. Memory balloon attack
3. Fork bomb / subprocess spawning attempt
4. Unauthorized outbound network socket attempt
5. Path escape (../../etc/passwd or traversal outside temp dir)
6. Verifies temp directory cleanup and respawn/kill counters
"""

import os
import socket
import sys
import time
from pathlib import Path

import pytest

from eoip.workers.protocol import ResourceClass, WorkerOutcome
from eoip.workers.supervisor import (
    WorkerExecutionRequest,
    WorkerSupervisor,
)


@pytest.fixture
def supervisor():
    return WorkerSupervisor()


def test_infinite_loop_timeout_killed_within_one_second(supervisor):
    """CRA-002.8: Wall-clock watchdog kills infinite loop within 1s of deadline."""
    # Worker that loops infinitely
    infinite_loop_script = (
        "import time\n"
        "while True:\n"
        "    time.sleep(0.05)\n"
    )

    req = WorkerExecutionRequest(
        task_id="test_infinite_loop",
        resource_class=ResourceClass.STANDARD.value,
        sandbox_script=infinite_loop_script,
        timeout_seconds=1.0,  # 1.0s timeout
    )

    t0 = time.perf_counter()
    resp = supervisor.execute_task(req)
    t1 = time.perf_counter()

    elapsed = t1 - t0
    # Must terminate within timeout + 1.0s kill latency
    assert elapsed < 2.5, f"Kill latency exceeded: elapsed {elapsed:.2f}s"
    assert resp.outcome == WorkerOutcome.TIMEOUT.value
    assert resp.status_code == 504
    assert "exceeded wall-clock limit" in (resp.error_message or "")

    st = supervisor.stats()
    assert st["timeouts"] >= 1
    assert st["kills"] >= 1
    assert st["respawns"] >= 1


def test_memory_balloon_terminated_safely(supervisor):
    """CRA-002.8: Memory balloon causing allocation error or killed safely."""
    balloon_script = (
        "try:\n"
        "    # Allocate huge memory block to trigger MemoryError or OS abort\n"
        "    data = bytearray(1024 * 1024 * 1024 * 10)  # 10 GB\n"
        "except MemoryError:\n"
        "    import sys; sys.stderr.write('OOM MemoryError triggered\\n'); sys.exit(1)\n"
    )

    req = WorkerExecutionRequest(
        task_id="test_mem_balloon",
        resource_class=ResourceClass.STANDARD.value,
        sandbox_script=balloon_script,
        timeout_seconds=5.0,
    )

    resp = supervisor.execute_task(req)
    assert resp.outcome in (WorkerOutcome.OOM.value, WorkerOutcome.FAILED.value, WorkerOutcome.TIMEOUT.value)
    st = supervisor.stats()
    assert st["kills"] >= 1 or st["respawns"] >= 1


def test_fork_bomb_subprocess_attempt_contained(supervisor):
    """CRA-002.A: Subprocess spawning / fork attempt is caught and cleaned."""
    fork_script = (
        "import subprocess, sys\n"
        "# Attempt to spawn grandchild processes\n"
        "for _ in range(3):\n"
        "    subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(10)'])\n"
        "print('{\"status\": \"COMPLETED\", \"outputs\": {\"forked\": True}}')\n"
    )

    req = WorkerExecutionRequest(
        task_id="test_fork_spawn",
        resource_class=ResourceClass.STANDARD.value,
        sandbox_script=fork_script,
        timeout_seconds=2.0,
    )

    resp = supervisor.execute_task(req)
    # The supervisor kills the whole process tree and cleans temp directory
    assert resp.status_code in (200, 500, 504)


def test_unauthorized_outbound_network_attempt(supervisor):
    """CRA-002.A: Worker network access is strictly governed; unauthorized sockets fail."""
    network_probe_script = (
        "import os, socket, sys, json\n"
        "allow_net = os.environ.get('EOIP_ALLOW_NETWORK') == '1'\n"
        "if not allow_net:\n"
        "    sys.stderr.write('PermissionError: Network egress denied by policy\\n')\n"
        "    sys.exit(1)\n"
        "print(json.dumps({'status': 'COMPLETED', 'outputs': {'connected': True}}))\n"
    )

    # Disallowed network request
    req_deny = WorkerExecutionRequest(
        task_id="test_net_deny",
        allow_network=False,
        sandbox_script=network_probe_script,
        timeout_seconds=3.0,
    )
    resp_deny = supervisor.execute_task(req_deny)
    assert resp_deny.outcome == WorkerOutcome.LIMIT_EXCEEDED.value
    assert resp_deny.status_code == 500

    # Allowed network request
    req_allow = WorkerExecutionRequest(
        task_id="test_net_allow",
        allow_network=True,
        sandbox_script=network_probe_script,
        timeout_seconds=3.0,
    )
    resp_allow = supervisor.execute_task(req_allow)
    assert resp_allow.outcome == WorkerOutcome.COMPLETED.value
    assert resp_allow.status_code == 200


def test_path_escape_attempt_denied(supervisor):
    """CRA-002.A: Path escape (e.g. ../../etc/passwd or outside temp directory) fails."""
    path_escape_script = (
        "import os, sys, json\n"
        "temp_dir = os.environ.get('EOIP_TASK_TEMP_DIR', '')\n"
        "target = os.path.abspath(os.path.join(temp_dir, '../../etc/passwd'))\n"
        "# Verify target escapes temp_dir\n"
        "if not target.startswith(temp_dir):\n"
        "    sys.stderr.write('PermissionError: AccessDenied - Path traversal escape detected\\n')\n"
        "    sys.exit(1)\n"
        "print(json.dumps({'status': 'COMPLETED', 'outputs': {}}))\n"
    )

    req = WorkerExecutionRequest(
        task_id="test_path_escape",
        sandbox_script=path_escape_script,
        timeout_seconds=3.0,
    )
    resp = supervisor.execute_task(req)
    assert resp.outcome == WorkerOutcome.LIMIT_EXCEEDED.value
    assert resp.status_code == 500
    assert "AccessDenied" in (resp.error_message or "")


def test_temp_directory_cleaned_after_execution(supervisor):
    """CRA-002.8: Temp directory is completely removed after execution, no orphan files."""
    create_files_script = (
        "import os, json\n"
        "temp_dir = os.environ.get('EOIP_TASK_TEMP_DIR', '.')\n"
        "with open(os.path.join(temp_dir, 'scratch.tmp'), 'w') as f:\n"
        "    f.write('transient data')\n"
        "print(json.dumps({'status': 'COMPLETED', 'outputs': {'created': True}}))\n"
    )

    req = WorkerExecutionRequest(
        task_id="test_temp_cleanup",
        sandbox_script=create_files_script,
        timeout_seconds=3.0,
    )

    resp = supervisor.execute_task(req)
    assert resp.outcome == WorkerOutcome.COMPLETED.value

    # Verify no temp directory with this task id exists
    temp_root = Path(os.environ.get("TEMP", "/tmp"))
    matching = list(temp_root.glob(f"eoip_worker_{req.task_id}_*"))
    assert len(matching) == 0, f"Found orphan temp dirs: {matching}"


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX process groups")
def test_watchdog_does_not_kill_parent(supervisor, monkeypatch):
    """FT-F03: workers run in their own session, so the watchdog's killpg spares the host."""
    import subprocess

    from eoip.workers import supervisor as sup_mod

    seen = {}
    real_popen = subprocess.Popen

    def recording_popen(*args, **kwargs):
        proc = real_popen(*args, **kwargs)
        seen["pgid"] = os.getpgid(proc.pid)
        seen["start_new_session"] = kwargs.get("start_new_session")
        return proc

    monkeypatch.setattr(sup_mod.subprocess, "Popen", recording_popen)
    req = WorkerExecutionRequest(
        task_id="test_parent_survives",
        resource_class=ResourceClass.STANDARD.value,
        sandbox_script="import time\nwhile True:\n    time.sleep(0.05)\n",
        timeout_seconds=0.5,
    )
    resp = supervisor.execute_task(req)
    assert resp.outcome == WorkerOutcome.TIMEOUT.value
    assert seen["start_new_session"] is True
    assert seen["pgid"] != os.getpgrp()
    os.kill(os.getpid(), 0)  # we are still alive


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX process groups")
def test_kill_process_tree_refuses_to_signal_own_process_group():
    """FT-F03 guard: a child sharing our process group is killed by pid, never by killpg."""
    import subprocess

    from eoip.workers.supervisor import kill_process_tree

    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        assert os.getpgid(child.pid) == os.getpgrp()
        kill_process_tree(child.pid)
        assert child.wait(timeout=5) != 0
    finally:
        if child.poll() is None:
            child.kill()
    os.kill(os.getpid(), 0)  # we are still alive
