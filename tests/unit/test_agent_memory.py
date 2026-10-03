"""FR-MEM-001 / NFR-PRIV-001: bounded, scoped, minimized task memory."""

import json
import multiprocessing
from datetime import UTC, datetime, timedelta

import pytest
from eoip.agents.memory import (
    MAX_TTL_SECONDS,
    FileMemoryStore,
    MemoryCapacityError,
    MemoryPolicy,
    MemoryPolicyError,
    MemoryStorageError,
)
from eoip.contracts.memory import MemoryRecord


def record(**changes):
    values = {
        "memory_id": "run-1",
        "kind": "TASK",
        "scope": "agent:TraceImpact",
        "owner": "local-user",
        "source": "TraceImpact",
        "created_at": "2026-10-01T00:00:00Z",
        "ttl_seconds": 60,
        "provenance_refs": ["urn:eoip:agent:run:run-1"],
        "confidence": None,
        "classification": "INTERNAL",
        "deletion_policy": "DELETE_AT_EXPIRY",
        "content": {"status": "SUCCEEDED", "evidence_count": 2},
    }
    return MemoryRecord(**(values | changes))


def test_memory_timestamp_is_created_per_instance():
    import eoip.contracts.memory as contracts

    assert contracts.MemoryRecord.model_fields["created_at"].default_factory is not None


def test_exact_expiry_purges_persistent_record_and_survives_restart(tmp_path):
    now = datetime(2026, 10, 1, tzinfo=UTC)
    store = FileMemoryStore(tmp_path, clock=lambda: now)
    store.put(record())
    assert FileMemoryStore(tmp_path, clock=lambda: now).get(
        "run-1", scope="agent:TraceImpact", owner="local-user"
    ) == record()
    now += timedelta(seconds=60)
    assert store.get("run-1", scope="agent:TraceImpact", owner="local-user") is None
    assert json.loads(store.path.read_text(encoding="utf-8"))["records"] == []


def test_scope_and_owner_are_exact_and_export_keeps_classification(tmp_path):
    store = FileMemoryStore(
        tmp_path, clock=lambda: datetime(2026, 10, 1, tzinfo=UTC)
    )
    store.put(record())
    assert store.get("run-1", scope="agent:Other", owner="local-user") is None
    assert store.get("run-1", scope="agent:TraceImpact", owner="another-user") is None
    exported = store.get("run-1", scope="agent:TraceImpact", owner="local-user")
    assert exported.model_dump()["classification"] == "INTERNAL"
    with pytest.raises(MemoryPolicyError):
        store.put(record(owner="another-user"))


@pytest.mark.parametrize("changes", [
    {"ttl_seconds": None}, {"ttl_seconds": 0}, {"ttl_seconds": -1},
    {"ttl_seconds": 30 * 86400 + 1},
    {"classification": "RESTRICTED"}, {"classification": "UNKNOWN"},
    {"kind": "CONVERSATION"}, {"deletion_policy": None},
    {"content": {"prompt": "secret prompt"}},
    {"content": {"status": "SUCCEEDED", "evidence_count": -1}},
    {"provenance_refs": []}, {"owner": ""},
    {"created_at": "2026-10-02T00:00:00Z"},
    {"created_at": "not-a-date"}, {"created_at": "2026-10-01T00:00:00"},
])
def test_invalid_or_forbidden_records_refuse_without_writing(tmp_path, changes):
    store = FileMemoryStore(
        tmp_path, clock=lambda: datetime(2026, 10, 1, tzinfo=UTC)
    )
    with pytest.raises(MemoryPolicyError):
        store.put(record(**changes))
    assert not store.path.exists()


def test_count_capacity_refuses_without_evicting_unexpired_evidence(tmp_path):
    now = datetime(2026, 10, 1, tzinfo=UTC)
    store = FileMemoryStore(tmp_path, policy=MemoryPolicy(max_records=1), clock=lambda: now)
    store.put(record())
    original = store.path.read_bytes()
    with pytest.raises(MemoryCapacityError):
        store.put(record(memory_id="run-2"))
    assert store.path.read_bytes() == original
    now += timedelta(seconds=60)
    store.put(record(memory_id="run-2", created_at=now.isoformat()))
    assert len(json.loads(store.path.read_text(encoding="utf-8"))["records"]) == 1


def test_byte_capacity_counts_utf8_and_preserves_previous_file(tmp_path):
    store = FileMemoryStore(
        tmp_path, policy=MemoryPolicy(max_bytes=600),
        clock=lambda: datetime(2026, 10, 1, tzinfo=UTC),
    )
    store.put(record())
    original = store.path.read_bytes()
    with pytest.raises(MemoryCapacityError):
        store.put(record(memory_id="run-2", owner="\u00e9" * 256))
    assert store.path.read_bytes() == original


def test_corrupt_storage_is_not_silently_overwritten(tmp_path):
    store = FileMemoryStore(
        tmp_path, clock=lambda: datetime(2026, 10, 1, tzinfo=UTC)
    )
    store.path.write_text("{bad", encoding="utf-8")
    with pytest.raises(MemoryStorageError):
        store.put(record())
    assert store.path.read_text(encoding="utf-8") == "{bad"


def test_delete_requires_owner_and_scope(tmp_path):
    store = FileMemoryStore(
        tmp_path, clock=lambda: datetime(2026, 10, 1, tzinfo=UTC)
    )
    store.put(record())
    assert not store.delete("run-1", scope="agent:Other", owner="local-user")
    assert store.delete("run-1", scope="agent:TraceImpact", owner="local-user")
    assert store.get("run-1", scope="agent:TraceImpact", owner="local-user") is None


def test_store_cleans_expired_records_on_startup(tmp_path):
    store = FileMemoryStore(
        tmp_path, clock=lambda: datetime(2026, 10, 1, tzinfo=UTC)
    )
    store.put(record())
    FileMemoryStore(tmp_path, clock=lambda: datetime(2026, 10, 2, tzinfo=UTC))
    assert json.loads(store.path.read_text(encoding="utf-8"))["records"] == []


def test_runtime_persists_only_approved_minimized_task_memory(tmp_path):
    from eoip.agents.catalog import build_agent_registry
    from eoip.agents.runtime import AgentRuntime
    from eoip.agents.trace import AgentTraceStore
    from eoip.contracts.agent import AgentRequest
    from eoip.graph.memory import MemoryGraphStore

    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {"canonical_id": "urn:test:item:1"})
    runtime = AgentRuntime(
        store, build_agent_registry(), memory_store=FileMemoryStore(tmp_path),
        trace_store=AgentTraceStore(tmp_path),
    )
    result = runtime.run(AgentRequest(
        request_id="minimized", agent_id="TraceImpact", actor_id="tester",
        goal="document body api_key=do-not-copy",
        context_refs=["urn:test:item:1"],
        metadata={"memory_ttl_seconds": 60},
    ))
    memory = runtime.get_memory("minimized")
    assert memory.content == {"status": result.status, "evidence_count": len(result.evidence_refs)}
    assert memory.owner == "tester"
    assert memory.ttl_seconds == 60
    assert memory.provenance_refs == ["urn:eoip:agent:run:minimized"]
    assert "do-not-copy" not in runtime.memory_store.path.read_text(encoding="utf-8")
    assert "document body" not in runtime.memory_store.path.read_text(encoding="utf-8")
    runtime.run(AgentRequest(request_id="run-only", agent_id="DataQuality", goal="Check"))
    assert runtime.get_memory("run-only") is None


def test_runtime_memory_failure_is_explicit_and_preserves_trace(tmp_path):
    from eoip.agents.catalog import build_agent_registry
    from eoip.agents.runtime import AgentRuntime
    from eoip.agents.trace import AgentTraceStore
    from eoip.contracts.agent import AgentRequest
    from eoip.graph.memory import MemoryGraphStore

    memory = FileMemoryStore(tmp_path, policy=MemoryPolicy(max_records=1))
    runtime = AgentRuntime(
        MemoryGraphStore(), build_agent_registry(), memory_store=memory,
        trace_store=AgentTraceStore(tmp_path),
    )
    memory.put(record(created_at=datetime.now(UTC).isoformat()))
    result = runtime.run(AgentRequest(
        request_id="full", agent_id="TraceImpact", goal="Check",
    ))
    assert any("Task memory could not be persisted" in warning for warning in result.warnings)
    assert any("Task memory could not be persisted" in warning for warning in result.explanation.uncertainty)
    assert runtime.trace_store.get("full") is not None
    assert runtime.get_result("full") == result


@pytest.mark.parametrize("failure", ["graph", "trace"])
def test_memory_requires_durable_run_provenance(tmp_path, monkeypatch, failure):
    from eoip.agents.catalog import build_agent_registry
    from eoip.agents.runtime import AgentRuntime
    from eoip.agents.trace import AgentTraceStore
    from eoip.contracts.agent import AgentRequest
    from eoip.graph.memory import MemoryGraphStore

    graph = MemoryGraphStore()
    trace = AgentTraceStore(tmp_path)

    def unavailable(*args, **kwargs):
        raise OSError("Run provenance unavailable")

    if failure == "graph":
        monkeypatch.setattr(graph, "upsert_vertex", unavailable)
    else:
        monkeypatch.setattr(trace, "save", unavailable)
    memory = FileMemoryStore(tmp_path)
    runtime = AgentRuntime(
        graph, build_agent_registry(), memory_store=memory, trace_store=trace,
    )
    result = runtime.run(AgentRequest(
        request_id="failed-provenance", agent_id="TraceImpact", goal="Check",
    ))
    assert "Agent run could not be persisted" in result.warnings
    assert memory.get(
        result.run_id, scope="agent:TraceImpact", owner="anonymous",
    ) is None


def test_result_cache_is_bounded_and_expires_without_deleting_traces():
    from eoip.agents.memory import AgentResultCache
    from eoip.contracts.agent import AgentResult

    now = datetime(2026, 10, 1, tzinfo=UTC)
    cache = AgentResultCache(policy=MemoryPolicy(max_records=1, ttl_seconds=60), clock=lambda: now)
    first = AgentResult(request_id="one", status="SUCCEEDED", summary="Done", evidence_refs=[])
    second = first.model_copy(update={"request_id": "two"})
    cache.put("one", first)
    cache.put("two", second)
    assert cache.get("one") is None
    assert cache.get("two") == second
    now += timedelta(seconds=60)
    assert cache.get("two") is None


def test_result_cache_oversized_result_is_not_retained():
    from eoip.agents.memory import AgentResultCache
    from eoip.contracts.agent import AgentResult

    cache = AgentResultCache(policy=MemoryPolicy(max_bytes=512))
    cache.put("large", AgentResult(
        request_id="large", status="SUCCEEDED", summary="x" * 600, evidence_refs=[]
    ))
    assert cache.get("large") is None


def test_memory_api_requires_auth_and_returns_classified_record(tmp_path, monkeypatch):
    from eoip.graph.memory import MemoryGraphStore
    from fastapi.testclient import TestClient

    from apps.api import main

    graph = MemoryGraphStore()
    monkeypatch.setattr(graph, "close", lambda: None, raising=False)
    graph.upsert_vertex("WorkItem", {"canonical_id": "urn:test:item:1"})
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("EOIP_API_TOKEN", "test-token-with-at-least-24-characters")
    monkeypatch.setattr(main, "create_store", lambda: graph)
    with TestClient(main.create_app()) as api:
        headers = {"Authorization": "Bearer test-token-with-at-least-24-characters"}
        response = api.post("/api/v1/agents/TraceImpact/runs", headers=headers, json={
            "goal": "Trace this", "context_refs": ["urn:test:item:1"], "memory_ttl_seconds": 60,
        })
        assert response.status_code == 200
        run_id = response.json()["run_id"]
        path = f"/api/v1/agents/runs/{run_id}/memory"
        assert api.get(path).status_code == 401
        recovered = api.get(path, headers=headers)
        assert recovered.status_code == 200
        assert recovered.json()["classification"] == "INTERNAL"
        assert recovered.json()["ttl_seconds"] == 60
        assert api.get("/api/v1/agents/runs/not-found/memory", headers=headers).status_code == 404
    with TestClient(main.create_app()) as restarted:
        assert restarted.get(path, headers=headers).json() == recovered.json()


def _concurrent_writer(root, memory_id):
    store = FileMemoryStore(root, clock=lambda: datetime(2026, 10, 1, tzinfo=UTC))
    store.put(record(memory_id=memory_id))


def test_independent_processes_do_not_lose_memory_records(tmp_path):
    context = multiprocessing.get_context("spawn")
    children = [
        context.Process(target=_concurrent_writer, args=(tmp_path, f"concurrent-{index}"))
        for index in range(3)
    ]
    try:
        for child in children:
            child.start()
        for child in children:
            child.join(timeout=30)
            assert child.exitcode == 0
    finally:
        for child in children:
            if child.is_alive():
                child.terminate()
                child.join(timeout=10)
    stored = FileMemoryStore(tmp_path, clock=lambda: datetime(2026, 10, 1, tzinfo=UTC))
    assert {item["memory_id"] for item in json.loads(stored.path.read_bytes())["records"]} == {
        "concurrent-0", "concurrent-1", "concurrent-2",
    }


def test_atomic_replace_failure_is_explicit_and_cleans_temporary_file(tmp_path, monkeypatch):
    from unittest.mock import Mock

    from eoip.agents import memory

    store = FileMemoryStore(tmp_path, clock=lambda: datetime(2026, 10, 1, tzinfo=UTC))
    store.put(record())
    before = store.path.read_bytes()

    def refuse_replace(*args):
        raise OSError("disk full")

    monkeypatch.setattr(memory.os, "replace", refuse_replace)
    logged_error = Mock(wraps=memory.log.error)
    monkeypatch.setattr(memory.log, "error", logged_error)
    with pytest.raises(MemoryStorageError):
        store.put(record(memory_id="run-2"))
    assert store.path.read_bytes() == before
    assert not list(store.path.parent.glob("*.tmp"))
    assert logged_error.call_args.args == ("memory.storage_failed",)
    assert logged_error.call_args.kwargs["extra"]["error_type"] == "OSError"


def test_context_memory_recall_is_scoped_and_consumes_budget(tmp_path, monkeypatch):
    from time import monotonic

    from eoip.agents.runtime import AgentExecutionContext
    from eoip.agents.tools import build_graph_tool_registry
    from eoip.contracts.agent import AgentBudgets, AgentContract, AgentRequest
    from eoip.graph.memory import MemoryGraphStore

    memory = FileMemoryStore(tmp_path, clock=lambda: datetime(2026, 10, 1, tzinfo=UTC))
    memory.put(record())
    contract = AgentContract(agent_id="TraceImpact", purpose="Recall", memory_policy="APPROVED")
    context = AgentExecutionContext(
        run_id="run-2",
        request=AgentRequest(request_id="run-2", agent_id="TraceImpact", goal="Recall", actor_id="local-user"),
        contract=contract, budgets=AgentBudgets(max_tool_calls=2),
        tools=build_graph_tool_registry(MemoryGraphStore()), deadline=monotonic() + 10,
        emit=lambda *args: None, memory_store=memory,
    )
    assert context.recall_task("run-1") == record()
    context.request = context.request.model_copy(update={"actor_id": "another-user"})
    assert context.recall_task("run-1") is None
    with pytest.raises(RuntimeError, match="Tool-call budget"):
        context.recall_task("run-1")
    context.contract = contract.model_copy(update={"memory_policy": "NONE"})
    with pytest.raises(PermissionError):
        context.recall_task("run-1")
    context.contract = contract
    context.tool_calls.clear()

    def unavailable(*args, **kwargs):
        raise MemoryStorageError("Memory unavailable")

    monkeypatch.setattr(memory, "get", unavailable)
    for _ in range(2):
        with pytest.raises(MemoryStorageError):
            context.recall_task("run-1")
    assert len(context.tool_calls) == 2
    assert all(call["status"] == "FAILED" for call in context.tool_calls)
    with pytest.raises(RuntimeError, match="Tool-call budget"):
        context.recall_task("run-1")


def test_invalid_config_refuses_startup_and_shorter_policy_is_loaded(tmp_path, monkeypatch):
    from eoip.config import load_memory_policy

    monkeypatch.setenv("EOIP_CONFIG_DIR", str(tmp_path))
    path = tmp_path / "memory-policy.yaml"
    path.write_text("ttl_seconds: 86400\nmax_records: 3\n", encoding="utf-8")
    assert load_memory_policy().ttl_seconds == 86400
    assert load_memory_policy().max_records == 3
    path.write_text("ttl_seconds: 2592001\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_memory_policy()


def test_memory_api_refuses_invalid_ttl_and_corruption(tmp_path, monkeypatch):
    from eoip.graph.memory import MemoryGraphStore
    from fastapi.testclient import TestClient

    from apps.api import main

    graph = MemoryGraphStore()
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("EOIP_API_TOKEN", "test-token-with-at-least-24-characters")
    monkeypatch.setattr(main, "create_store", lambda: graph)
    api = TestClient(main.create_app())
    headers = {"Authorization": "Bearer test-token-with-at-least-24-characters"}
    for invalid in (0, MAX_TTL_SECONDS + 1, True, "60"):
        assert api.post("/api/v1/agents/TraceImpact/runs", headers=headers, json={
            "goal": "Check", "memory_ttl_seconds": invalid,
        }).status_code == 422
    run_id = api.post("/api/v1/agents/TraceImpact/runs", headers=headers, json={
        "goal": "Check",
    }).json()["run_id"]
    (tmp_path / "agent-memory" / "records.json").write_text("{bad", encoding="utf-8")
    refused = api.get(f"/api/v1/agents/runs/{run_id}/memory", headers=headers)
    assert refused.status_code == 503
    assert refused.json()["detail"] == "Task memory storage is unavailable"
