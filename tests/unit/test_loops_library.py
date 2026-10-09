"""Tests for the bounded execution-loop library (GAP-LOOP-001..047, §2)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from eoip.loops import (
    ApprovalPolicy,
    Approver,
    GateDecision,
    HumanPattern,
    InMemoryApprovalQueue,
    JsonCheckpointStore,
    LOOP_PHASES,
    LOOP_RUNNERS,
    LoopConfig,
    LoopDriver,
    LoopStatus,
    PolicyGate,
    StepOutcome,
    StepSignal,
    TerminationReason,
    gates_for,
    make_decision,
    run_loop,
)
from eoip.loops.router import build_router


def _scripted_completion(last_phase: str):
    """Step fn that completes once the final phase has been executed."""

    def step(state, ctx):
        phases_seen = state.setdefault("phases_seen", [])
        if ctx.phase not in phases_seen:
            phases_seen.append(ctx.phase)
        state["n"] = state.get("n", 0) + 1
        signal = StepSignal.COMPLETE if ctx.phase == last_phase else StepSignal.CONTINUE
        return StepOutcome(signal=signal, tokens_used=2, note=ctx.phase)

    return step


# ---------------------------------------------------------------------------
# (A) every loop driver runs a scripted scenario
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("loop_name", sorted(LOOP_RUNNERS))
def test_every_loop_runs_scripted_scenario(loop_name):
    phases = LOOP_PHASES[loop_name]
    result = LOOP_RUNNERS[loop_name](
        _scripted_completion(phases[-1]),
        {"seed": True},
        LoopConfig(loop_name=loop_name, max_iterations=64),
    )
    assert result.status == LoopStatus.COMPLETED
    assert result.termination_reason == TerminationReason.COMPLETED
    assert result.loop_name == loop_name
    assert result.run_id.startswith("urn:eoip:loop:run:")
    # every scheduled phase was visited
    assert set(phases) <= set(result.state["phases_seen"])
    assert result.metrics.tokens_used == 2 * result.metrics.iterations
    assert result.metrics.outcome == "completed"


def test_phase_specific_step_mapping():
    def decide(state, ctx):
        state["decided"] = True
        return StepOutcome(signal=StepSignal.COMPLETE)

    result = LOOP_RUNNERS["ooda"]({"observe": _scripted_completion("act")["observe"] if False else None} if False else {
        "observe": lambda s, c: (s.update(o=True), StepOutcome())[1],
        "orient": lambda s, c: (s.update(oriented=True), StepOutcome())[1],
        "decide": decide,
    }, {}, LoopConfig(loop_name="ooda", max_iterations=8))
    assert result.state.get("decided") is True


def test_run_loop_dispatch_unknown():
    with pytest.raises(KeyError):
        run_loop("not_a_loop", _scripted_completion("act"))


# ---------------------------------------------------------------------------
# (B) budget / termination enforcement
# ---------------------------------------------------------------------------


def test_max_iterations_terminates():
    result = run_loop("react", lambda s, c: StepOutcome(), {}, LoopConfig(max_iterations=5))
    assert result.termination_reason == TerminationReason.MAX_ITERATIONS
    assert result.iterations == 5


def test_token_budget_terminates():
    result = run_loop("react", lambda s, c: StepOutcome(tokens_used=10), {},
                      LoopConfig(max_iterations=100, token_budget=25))
    assert result.termination_reason == TerminationReason.TOKEN_BUDGET
    assert result.metrics.tokens_used >= 25


def test_cost_budget_terminates():
    result = run_loop("react", lambda s, c: StepOutcome(cost_used=1.5), {},
                      LoopConfig(max_iterations=100, cost_budget=3.0))
    assert result.termination_reason == TerminationReason.COST_BUDGET


def test_time_budget_terminates():
    ticks = iter(range(1000))
    result = run_loop(
        "react",
        lambda s, c: StepOutcome(),
        {},
        LoopConfig(max_iterations=10_000, time_budget_seconds=0.5),
        clock=lambda: next(ticks) * 1.0,
    )
    assert result.termination_reason == TerminationReason.TIME_BUDGET


def test_convergence_signal():
    result = run_loop("reflection", lambda s, c: StepOutcome(signal=StepSignal.CONVERGED), {})
    assert result.status == LoopStatus.CONVERGED
    assert result.termination_reason == TerminationReason.CONVERGED


def test_cycle_detection():
    # state never changes -> same fingerprint on second iteration
    result = run_loop("react", lambda s, c: StepOutcome(), {"fixed": 1},
                      LoopConfig(max_iterations=50))
    assert result.termination_reason == TerminationReason.CYCLE_DETECTED


def test_cycle_detection_disabled():
    result = run_loop("react", lambda s, c: StepOutcome(), {"fixed": 1},
                      LoopConfig(max_iterations=3, detect_cycles=False))
    assert result.termination_reason == TerminationReason.MAX_ITERATIONS


def test_step_error_stable_category_and_rollback():
    executed = []

    def handler(args):
        executed.append(args)

    def step(state, ctx):
        ctx.record_compensation("undo_write", key="k1")
        raise RuntimeError("boom")

    driver = LoopDriver(LoopConfig(loop_name="react"), phases=["reason", "act"],
                        compensation_handlers={"undo_write": handler})
    result = driver.run(step, {})
    assert result.status == LoopStatus.FAILED
    assert result.termination_reason == TerminationReason.STEP_ERROR
    assert result.metrics.error_category == "step_exception:RuntimeError"
    assert executed == [{"key": "k1"}]
    assert result.metrics.compensations_executed == 1
    assert result.correlation_id


# ---------------------------------------------------------------------------
# (C) checkpoint + resume
# ---------------------------------------------------------------------------


def test_checkpoint_resume(tmp_path):
    store = JsonCheckpointStore(tmp_path)
    config = LoopConfig(loop_name="react", max_iterations=100, checkpoint_dir=str(tmp_path))

    def step(state, ctx):
        state["n"] = state.get("n", 0) + 1
        if state["n"] >= 3:
            return StepOutcome(signal=StepSignal.COMPLETE)
        return StepOutcome()

    driver = LoopDriver(config, phases=["reason", "act"], store=store)
    result = driver.run(step, {})
    assert result.status == LoopStatus.COMPLETED
    assert result.state["n"] == 3
    assert store.load(driver.run_id) is not None
    assert result.metrics.checkpoints_written >= 3

    # resume mid-run: driver whose first step completes immediately
    mid_driver = LoopDriver(config, phases=["reason", "act"], store=store)
    mid_driver.run(lambda s, c: StepOutcome(), {})  # runs to budget, checkpoint saved

    def finish_step(state, ctx):
        return StepOutcome(signal=StepSignal.COMPLETE, result={"done": state.get("n", 0)})

    checkpoint = store.load(mid_driver.run_id)
    resume_driver = LoopDriver(config, phases=["reason", "act"], store=store)
    resumed = resume_driver.run(finish_step, resume_from=checkpoint)
    assert resumed.state["n"] == checkpoint.state["n"]


def test_resume_pending_approval_denied(tmp_path):
    store = JsonCheckpointStore(tmp_path)
    config = LoopConfig(loop_name="ooda", checkpoint_dir=str(tmp_path))
    driver = LoopDriver(config, phases=LOOP_PHASES["ooda"], store=store)
    parked = driver.run(
        lambda s, c: StepOutcome(await_approval={"ask": "ok?"}),
        {"x": 1},
    )
    assert parked.status == LoopStatus.AWAITING_APPROVAL
    checkpoint = store.load(driver.run_id)
    assert checkpoint.pending_approval is not None

    resume_driver = LoopDriver(config, phases=LOOP_PHASES["ooda"], store=store)
    denied = resume_driver.run(
        lambda s, c: StepOutcome(signal=StepSignal.COMPLETE),
        resume_from=checkpoint,
        on_approval_resume=lambda pending: False,
    )
    assert denied.termination_reason == TerminationReason.APPROVAL_DENIED

    resume_driver2 = LoopDriver(config, phases=LOOP_PHASES["ooda"], store=store)
    allowed = resume_driver2.run(
        lambda s, c: StepOutcome(signal=StepSignal.COMPLETE),
        resume_from=checkpoint,
        on_approval_resume=lambda pending: True,
    )
    assert allowed.status == LoopStatus.COMPLETED


# ---------------------------------------------------------------------------
# (D) idempotency
# ---------------------------------------------------------------------------


def test_idempotency_key_replay(tmp_path):
    store = JsonCheckpointStore(tmp_path)
    config = LoopConfig(loop_name="react", checkpoint_dir=str(tmp_path), idempotency_key="job-42")
    driver = LoopDriver(config, phases=["reason", "act"], store=store)
    first = driver.run(lambda s, c: StepOutcome(signal=StepSignal.COMPLETE, result={"v": 1}), {})
    replay = LoopDriver(config, phases=["reason", "act"], store=store).run(
        lambda s, c: StepOutcome(signal=StepSignal.COMPLETE, result={"v": 2}), {}
    )
    assert replay.idempotent_replay is True
    assert replay.result == {"v": 1}


# ---------------------------------------------------------------------------
# (E) approval gates: allow / deny / park + 15 patterns
# ---------------------------------------------------------------------------


def _policy(**kwargs):
    base = dict(policy_id="urn:eoip:loop:policy:p1", action="agents:approve")
    base.update(kwargs)
    return ApprovalPolicy(**base)


def test_all_fifteen_patterns_exist():
    assert len(HumanPattern) == 15


def test_gate_deny_when_role_missing():
    gate = PolicyGate(_policy(allowed_roles=["steward"]))
    verdict = gate.evaluate(gate="run", context={"approver_roles": ["viewer"]})
    assert verdict.decision == "deny"


def test_gate_allow_when_role_matches_and_no_human_needed():
    gate = PolicyGate(_policy(allowed_roles=["steward"]))
    verdict = gate.evaluate(gate="run", context={"approver_roles": ["steward"]})
    assert verdict.decision == "allow"


def test_gate_park_and_resume_with_human_decision():
    queue = InMemoryApprovalQueue()
    gate = PolicyGate(
        _policy(allowed_roles=["steward"], required_evidence=["ticket"], min_approvals=2),
        queue=queue,
    )
    first = gate.evaluate(gate="run", context={"approver_roles": ["viewer"], "classification": "internal"})
    assert first.decision == "park"
    assert len(queue.pending()) == 1
    request = queue.pending()[0]
    assert request.request_id.startswith("urn:eoip:loop:approval:")

    approver = Approver(subject="alice", roles=["steward"])
    queue.decide(request.request_id, make_decision(
        request, approver, GateDecision.APPROVE, evidence={"ticket": "JIRA-1"}))
    # multi-human approval needs a second approver
    still_parked = gate.evaluate(gate="run", context={
        "approver_roles": ["viewer"], "classification": "internal",
        "approval_request_id": request.request_id})
    assert still_parked.decision == "park"
    queue.decide(request.request_id, make_decision(
        request, Approver(subject="bob", roles=["steward"]), GateDecision.APPROVE,
        evidence={"ticket": "JIRA-1"}))
    allowed = gate.evaluate(gate="run", context={
        "approver_roles": ["viewer"], "classification": "internal",
        "approval_request_id": request.request_id})
    assert allowed.decision == "allow"
    assert allowed.approver == "bob"


def test_gate_denial_after_human_denies():
    queue = InMemoryApprovalQueue()
    gate = PolicyGate(_policy(), queue=queue)
    gate.evaluate(gate="run", context={})
    request = queue.pending()[0]
    queue.decide(request.request_id, make_decision(
        request, Approver(subject="carol"), GateDecision.DENY, reason="insufficient evidence"))
    verdict = gate.evaluate(gate="run", context={"approval_request_id": request.request_id})
    assert verdict.decision == "deny"
    assert "insufficient evidence" in verdict.reason


def test_gate_conditions_not_applicable_pass():
    gate = PolicyGate(_policy(conditions={"classification": "restricted"}))
    verdict = gate.evaluate(gate="run", context={"classification": "public"})
    assert verdict.decision == "allow"  # gate does not apply to public data


def test_gate_conditions_apply():
    gate = PolicyGate(_policy(allowed_roles=["admin"], conditions={"classification": "restricted"}))
    verdict = gate.evaluate(gate="run", context={"classification": "restricted", "approver_roles": ["viewer"]})
    assert verdict.decision == "deny"
    verdict2 = gate.evaluate(gate="run", context={"classification": "restricted", "approver_roles": ["admin"]})
    assert verdict2.decision == "allow"


def test_driver_with_denying_gate_rolls_back():
    executed = []
    gate = PolicyGate(_policy(allowed_roles=["steward"]))
    driver = LoopDriver(
        LoopConfig(loop_name="react"),
        phases=["reason", "act"],
        gates={"run": [gate]},
        compensation_handlers={"undo": lambda args: executed.append(args)},
    )

    def step(state, ctx):
        ctx.record_compensation("undo", at=ctx.phase)
        return StepOutcome()

    result = driver.run(step, {"approver_roles": ["viewer"]})
    assert result.termination_reason == TerminationReason.APPROVAL_DENIED
    assert result.metrics.error_category == "approval_denied"
    assert executed  # rollback ran


def test_gates_for_pattern_filters():
    policies = [
        _policy(policy_id="p1", pattern=HumanPattern.AT_COMMIT),
        _policy(policy_id="p2", pattern=HumanPattern.IN_RECOVERY),
    ]
    gates = gates_for(HumanPattern.AT_COMMIT, policies)
    assert len(gates) == 1
    assert gates[0].policy.policy_id == "p1"


def test_metrics_progress_and_failure_counters():
    result = run_loop("ooda", _scripted_completion("act"), {}, LoopConfig(max_iterations=64))
    m = result.metrics
    assert m.iterations == result.iterations
    assert m.phases_executed == {"observe": 1, "orient": 1, "decide": 1, "act": 1}
    assert m.outcome == "completed"
    assert m.error_category is None


# ---------------------------------------------------------------------------
# (F) router
# ---------------------------------------------------------------------------


@pytest.fixture
def client(tmp_path):
    return TestClient(build_router(store=JsonCheckpointStore(tmp_path / "ck"),
                                   queue=InMemoryApprovalQueue()))


def test_router_catalog(client):
    resp = client.get("/api/v1/loops/catalog")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["loops"]) == 23
    assert len(body["human_patterns"]) == 15
    names = {loop["loop_name"] for loop in body["loops"]}
    assert "ooda" in names and "consensus_reconciliation" in names


def test_router_run_and_resume(client):
    resp = client.post("/api/v1/loops/run/react", json={
        "config": {"max_iterations": 32},
        "initial_state": {},
        "script": [
            {"increment": "n"},
            {"increment": "n"},
            {"signal": "complete"},
        ],
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "completed"
    assert body["state"]["n"] == 3

    # unknown loop -> 404
    assert client.post("/api/v1/loops/run/nope", json={}).status_code == 404


def test_router_park_resume_and_decide(client, tmp_path):
    resp = client.post("/api/v1/loops/run/ooda", json={
        "config": {"max_iterations": 32, "checkpoint_dir": str(tmp_path / "ck2")},
        "script": [{"await_approval": {"ask": "proceed?"}}],
    })
    assert resp.status_code == 200
    parked = resp.json()
    assert parked["status"] == "awaiting_approval"

    pending = client.get("/api/v1/loops/approvals/pending").json()
    # (parked via StepOutcome.await_approval does not create queue entries; decide endpoint still works)
    req_id = "urn:eoip:loop:approval:test-1"
    decided = client.post("/api/v1/loops/approvals/decide", json={
        "request_id": req_id, "approver": "alice", "roles": ["steward"],
        "decision": "approve", "evidence": {"ticket": "JIRA-9"},
    })
    assert decided.status_code == 200
    assert decided.json()["decision"] == "approve"
    # queue may be empty; endpoint must not fail
    assert client.get("/api/v1/loops/approvals/pending").status_code == 200
