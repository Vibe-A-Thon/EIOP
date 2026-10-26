"""Unit tests for packages/eoip/execution (§7 durable execution infra)."""

from __future__ import annotations

import pytest
from eoip.execution.eventstore import EventStore
from eoip.execution.router import build_router
from eoip.execution.scheduling import PriorityWorkQueue, SchedulerElection
from eoip.execution.workflows import (
    ExecutionEngine,
    RetryPolicy,
    StepDefinition,
    WorkflowDefinition,
    apply_event,
)
from eoip.ha import LeaderLease


def _definition(**kwargs):
    steps = [
        StepDefinition(name="extract", action="extract"),
        StepDefinition(name="transform", action="transform", depends_on=["extract"]),
        StepDefinition(name="load", action="load", depends_on=["transform"]),
    ]
    return WorkflowDefinition(workflow_id="urn:wf:etl", name="etl", steps=steps, **kwargs)


# ---------------------------------------------------------------------------
# Event store
# ---------------------------------------------------------------------------

def test_eventstore_append_and_sequence():
    store = EventStore()
    e1 = store.append("s1", "CREATED", {"a": 1})
    e2 = store.append("s1", "UPDATED")
    assert (e1.seq, e2.seq) == (1, 2)
    assert [e.event_type for e in store.read("s1")] == ["CREATED", "UPDATED"]
    assert [e.seq for e in store.read("s1", after_seq=1)] == [2]


def test_eventstore_optimistic_concurrency():
    store = EventStore()
    store.append("s1", "A")
    with pytest.raises(RuntimeError):
        store.append("s1", "B", expected_seq=5)
    ok = store.append("s1", "B", expected_seq=2)
    assert ok.seq == 2


def test_eventstore_persistence_and_load(tmp_path):
    store = EventStore(tmp_path)
    store.append("s1", "A", {"x": 1})
    fresh = EventStore(tmp_path)
    fresh.load("s1")
    assert len(fresh.read("s1")) == 1
    assert fresh.read("s1")[0].payload == {"x": 1}


def test_eventstore_snapshots(tmp_path):
    store = EventStore(tmp_path)
    store.append("s1", "A")
    snap = store.save_snapshot("s1", {"count": 1}, up_to_seq=1)
    loaded = store.load_snapshot("s1")
    assert loaded.state == snap.state == {"count": 1}
    assert loaded.up_to_seq == 1


def test_eventstore_reconcile_consistent_and_gaps():
    store = EventStore()
    for i in range(4):
        store.append("s1", f"E{i}")
    report = store.reconcile("s1")
    assert report.consistent
    assert report.expected_next_seq == 5
    assert report.gaps == [] and report.duplicates == []
    empty = store.reconcile("missing")
    assert empty.event_count == 0 and empty.expected_next_seq == 1


def test_eventstore_reconcile_detects_gaps_and_duplicates():
    from eoip.execution.eventstore import Event
    store = EventStore()
    store._memory["s1"] = [
        Event(stream_id="s1", seq=1, event_type="A", recorded_at="t"),
        Event(stream_id="s1", seq=3, event_type="B", recorded_at="t"),
        Event(stream_id="s1", seq=3, event_type="B", recorded_at="t2"),
    ]
    report = store.reconcile("s1")
    assert not report.consistent
    assert report.gaps == [2]
    assert report.duplicates == [3]


# ---------------------------------------------------------------------------
# Workflow engine
# ---------------------------------------------------------------------------

def test_workflow_runs_dag_to_completion():
    ran = []
    engine = ExecutionEngine(EventStore(), {
        "extract": lambda vars, ctx: ran.append("extract") or "raw",
        "transform": lambda vars, ctx: ran.append("transform") or "clean",
        "load": lambda vars, ctx: ran.append("load") or "done",
    })
    definition = _definition()
    state = engine.run(definition, payload={"src": "db"})
    assert state.status == "SUCCEEDED"
    assert ran == ["extract", "transform", "load"]
    assert state.variables["result.load"] == "done"
    assert state.finished_at


def test_workflow_state_is_replayable_from_events():
    store = EventStore()
    engine = ExecutionEngine(store, {"a": lambda v, c: 1, "b": lambda v, c: 2})
    definition = WorkflowDefinition(
        workflow_id="urn:wf:r", name="r",
        steps=[StepDefinition(name="a", action="a"), StepDefinition(name="b", action="b", depends_on=["a"])],
    )
    engine.run(definition)
    replayed = engine.state(definition)
    assert replayed.status == "SUCCEEDED"
    assert replayed.steps["b"].status == "SUCCEEDED"
    assert replayed.variables["result.a"] == 1


def test_workflow_retry_then_fail():
    attempts = {"n": 0}

    def flaky(vars, ctx):
        attempts["n"] += 1
        raise RuntimeError("boom")

    engine = ExecutionEngine(EventStore(), {"flaky": flaky})
    definition = WorkflowDefinition(
        workflow_id="urn:wf:flaky", name="flaky",
        steps=[StepDefinition(name="f", action="flaky", retry=RetryPolicy(max_attempts=3))],
    )
    state = engine.run(definition)
    assert state.status == "FAILED"
    assert state.steps["f"].attempts == 3
    assert state.steps["f"].error == "boom"


def test_workflow_retry_eventually_succeeds():
    attempts = {"n": 0}

    def flaky(vars, ctx):
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise RuntimeError("not yet")
        return "ok"

    engine = ExecutionEngine(EventStore(), {"flaky": flaky})
    definition = WorkflowDefinition(
        workflow_id="urn:wf:flaky-ok", name="flaky-ok",
        steps=[StepDefinition(name="f", action="flaky", retry=RetryPolicy(max_attempts=3))],
    )
    state = engine.run(definition)
    assert state.status == "SUCCEEDED"
    assert state.steps["f"].attempts == 3


def test_workflow_human_approval_gate():
    engine = ExecutionEngine(EventStore(), {"danger": lambda v, c: "done"})
    definition = WorkflowDefinition(
        workflow_id="urn:wf:approval", name="approval",
        steps=[StepDefinition(name="danger", action="danger", requires_approval=True)],
    )
    state = engine.run(definition)
    assert state.status == "RUNNING"
    assert state.steps["danger"].status == "WAITING_APPROVAL"
    state = engine.approve(definition, "danger", approved=False)
    assert state.status == "REJECTED"
    assert state.steps["danger"].status == "SKIPPED"
    with pytest.raises(RuntimeError):
        engine.approve(definition, "danger", approved=True)  # no longer awaiting


def test_workflow_approval_then_resume():
    engine = ExecutionEngine(EventStore(), {"step": lambda v, c: "ran"})
    definition = WorkflowDefinition(
        workflow_id="urn:wf:resume", name="resume",
        steps=[StepDefinition(name="s1", action="step", requires_approval=True)],
    )
    engine.run(definition)
    engine.approve(definition, "s1", approved=True)
    state = engine.run(definition)  # resume: pending step executes
    assert state.status == "SUCCEEDED"


def test_workflow_cancellation():
    engine = ExecutionEngine(EventStore(), {"a": lambda v, c: 1, "b": lambda v, c: 2})
    definition = WorkflowDefinition(
        workflow_id="urn:wf:cancel", name="cancel",
        steps=[StepDefinition(name="a", action="a"),
               StepDefinition(name="b", action="b", requires_approval=True)],
    )
    state = engine.run(definition)  # runs until the approval gate, stays RUNNING
    assert state.status == "RUNNING"
    state = engine.cancel(definition)
    assert state.status == "CANCELLED"
    assert state.steps["b"].status == "SKIPPED"
    with pytest.raises(RuntimeError):
        engine.cancel(definition)  # already terminal


def test_workflow_saga_compensation():
    compensated = []
    engine = ExecutionEngine(EventStore(), {
        "charge": lambda v, c: "charged",
        "refund": lambda v, c: compensated.append(c["step"]) or "refunded",
    })
    definition = WorkflowDefinition(
        workflow_id="urn:wf:saga", name="saga",
        steps=[StepDefinition(name="charge", action="charge", compensation="refund")],
    )
    engine.run(definition)
    state = engine.compensate(definition)
    assert state.status == "COMPENSATED"
    assert state.steps["charge"].status == "COMPENSATED"
    assert compensated == ["charge"]


def test_workflow_long_running_timer():
    engine = ExecutionEngine(EventStore(), {"later": lambda v, c: "done"})
    definition = WorkflowDefinition(
        workflow_id="urn:wf:timer", name="timer",
        steps=[StepDefinition(name="t", action="later", timer_seconds=3600)],
    )
    state = engine.run(definition)
    assert state.steps["t"].status == "WAITING_TIMER"
    assert state.steps["t"].timer_fire_at
    assert engine.due_timers(definition) == []  # not due yet
    state = engine.run(definition, now="2999-01-01T00:00:00.000Z")  # timer elapsed -> resumes
    assert state.status == "SUCCEEDED"


def test_workflow_validation():
    with pytest.raises(ValueError):
        WorkflowDefinition(workflow_id="w", name="dup",
                           steps=[StepDefinition(name="a", action="x"),
                                  StepDefinition(name="a", action="y")]).validate_dag()
    with pytest.raises(ValueError):
        WorkflowDefinition(workflow_id="w", name="unknown",
                           steps=[StepDefinition(name="a", action="x", depends_on=["ghost"])]).validate_dag()
    with pytest.raises(ValueError):
        WorkflowDefinition(workflow_id="w", name="cycle",
                           steps=[StepDefinition(name="a", action="x", depends_on=["b"]),
                                  StepDefinition(name="b", action="y", depends_on=["a"])]).validate_dag()


def test_apply_event_variable_set():
    from eoip.execution.eventstore import Event
    from eoip.execution.workflows import _initial_state
    definition = _definition()
    state = _initial_state(definition)
    apply_event(state, Event(stream_id="s", seq=1, event_type="VARIABLE_SET",
                             payload={"key": "k", "value": 42}, recorded_at="t"))
    assert state.variables["k"] == 42


# ---------------------------------------------------------------------------
# Distributed scheduling
# ---------------------------------------------------------------------------

def test_priority_queue_claims_highest_priority_first():
    queue = PriorityWorkQueue()
    queue.enqueue("low", {"n": 1}, priority=1)
    queue.enqueue("high", {"n": 2}, priority=9)
    item = queue.claim("worker-1")
    assert item.kind == "high"
    assert item.status == "LEASED" and item.lease_owner == "worker-1"


def test_claim_returns_none_when_empty_or_leased():
    queue = PriorityWorkQueue()
    assert queue.claim("w") is None
    queue.enqueue("a")
    assert queue.claim("w1") is not None
    assert queue.claim("w2") is None  # live lease blocks


def test_complete_and_release_ownership():
    queue = PriorityWorkQueue()
    item = queue.enqueue("a")
    queue.claim("owner-1")
    with pytest.raises(RuntimeError):
        queue.complete(item.item_id, owner="owner-2")
    queue.complete(item.item_id, owner="owner-1")
    assert queue.claim("owner-1") is None
    # release path
    item2 = queue.enqueue("b")
    queue.claim("owner-1")
    queue.release(item2.item_id, owner="owner-1")
    reclaimed = queue.claim("owner-2")
    assert reclaimed.item_id == item2.item_id


def test_expired_lease_is_reclaimed():
    queue = PriorityWorkQueue(lease_ttl_seconds=0.1)
    queue.enqueue("a")
    item = queue.claim("w1")
    assert item.attempts == 0
    import time
    time.sleep(0.3)  # > TTL with margin for coarse Windows timer granularity
    reclaimed = queue.claim("w2")
    assert reclaimed.item_id == item.item_id
    assert reclaimed.attempts == 1  # reclaimed after expiry


def test_queue_persistence(tmp_path):
    queue = PriorityWorkQueue(tmp_path)
    queue.enqueue("a", {"x": 1}, priority=3)
    import json
    files = list((tmp_path / "workqueue").glob("*.json"))
    assert files
    assert json.loads(files[0].read_text(encoding="utf-8"))["kind"] == "a"


def test_scheduler_election_requires_lease(tmp_path):
    lease_a = LeaderLease(tmp_path / "sched.lock", ttl_seconds=5)
    lease_b = LeaderLease(tmp_path / "sched.lock", ttl_seconds=5)
    queue = PriorityWorkQueue()
    queue.enqueue("job")
    sched_a = SchedulerElection(lease_a, queue)
    sched_b = SchedulerElection(lease_b, queue)
    # free lease: first dispatcher to acquire becomes the leader and dispatches
    item = sched_b.dispatch_once("w2")
    assert item is not None
    # a live foreign lease blocks the other dispatcher
    assert lease_a.acquire() is False
    assert sched_a.dispatch_once("w1") is None


def test_scheduler_election_failover_after_expiry(tmp_path):
    import time
    lease_a = LeaderLease(tmp_path / "sched.lock", ttl_seconds=0.1)
    lease_b = LeaderLease(tmp_path / "sched.lock", ttl_seconds=0.1)
    queue = PriorityWorkQueue()
    queue.enqueue("job")
    assert lease_a.acquire()
    time.sleep(0.3)  # > TTL with margin for coarse Windows timer granularity
    assert SchedulerElection(lease_b, queue).dispatch_once("w2") is not None


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

def test_execution_router_routes():
    router = build_router()
    routes = {(next(iter(r.methods)), r.path) for r in router.routes if hasattr(r, "methods")}
    expected = {
        ("POST", "/api/v1/execution/workflows"),
        ("GET", "/api/v1/execution/workflows/{workflow_id}/state"),
        ("POST", "/api/v1/execution/workflows/{workflow_id}/run"),
        ("POST", "/api/v1/execution/workflows/{workflow_id}/cancel"),
        ("POST", "/api/v1/execution/workflows/{workflow_id}/compensate"),
        ("POST", "/api/v1/execution/workflows/{workflow_id}/approve"),
        ("GET", "/api/v1/execution/workflows/{workflow_id}/timers"),
        ("POST", "/api/v1/execution/queue/items"),
        ("POST", "/api/v1/execution/queue/claim"),
        ("POST", "/api/v1/execution/queue/items/{item_id}/complete"),
        ("GET", "/api/v1/execution/streams/{stream_id}/reconcile"),
    }
    assert expected <= routes


def test_execution_router_end_to_end():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    app = FastAPI()
    app.include_router(build_router({"echo": lambda v, c: "ok"}))
    client = TestClient(app)
    resp = client.post("/api/v1/execution/workflows", json={
        "workflow_id": "urn:wf:http", "name": "http",
        "steps": [{"name": "s", "action": "echo"}],
    })
    assert resp.status_code == 200 and resp.json()["valid"] is True
    resp = client.post("/api/v1/execution/workflows/urn:wf:http/run", json={})
    assert resp.json()["status"] == "SUCCEEDED"
    resp = client.get("/api/v1/execution/workflows/urn:wf:http/state")
    assert resp.json()["steps"]["s"]["status"] == "SUCCEEDED"
    resp = client.get("/api/v1/execution/streams/urn:wf:http/reconcile")
    assert resp.json()["consistent"] is True
    # invalid definition rejected
    resp = client.post("/api/v1/execution/workflows", json={
        "workflow_id": "w2", "name": "bad",
        "steps": [{"name": "a", "action": "x", "depends_on": ["ghost"]}],
    })
    assert resp.status_code == 422
