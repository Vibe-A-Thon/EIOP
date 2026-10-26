"""Unit tests for packages/eoip/reasoning (§7 reasoning & memory & evaluation & AgentOps)."""

from __future__ import annotations

import pytest
from eoip.reasoning.agentops import (
    CostLedger,
    DeploymentDescriptor,
    IncidentStore,
    RunTracer,
    SLAPolicy,
    SLATracker,
    validate_deployment,
)
from eoip.reasoning.evaluation import (
    ADVERSARIAL_PROBES,
    AdversarialTestSuite,
    BenchmarkRunner,
    BusinessOutcomeTracker,
    GoldenTask,
    OutcomeRecord,
    Trajectory,
    TrajectoryScorer,
    TrajectoryStep,
)
from eoip.reasoning.memory import (
    EpisodicMemory,
    HierarchicalMemory,
    ProceduralMemory,
    SemanticMemory,
    SharedMemory,
    TemporalMemory,
    WorkingMemory,
    estimate_tokens,
)
from eoip.reasoning.router import build_router
from eoip.reasoning.strategies import (
    HTNPlanner,
    NeuroSymbolicStrategy,
    ReasoningHooks,
    ReasoningProblem,
    StrategyRegistry,
    TaskSpec,
    default_registry,
)

# ---------------------------------------------------------------------------
# Strategies (§7)
# ---------------------------------------------------------------------------

def test_registry_lists_all_architectures():
    names = default_registry().names()
    for expected in ("react", "tot", "got", "best-first", "beam", "htn",
                     "world-model", "neuro-symbolic", "causal", "meta"):
        assert expected in names


def test_registry_unknown_strategy_raises():
    with pytest.raises(KeyError):
        default_registry().get("nope")


def test_react_answers_deterministically():
    problem = ReasoningProblem(prompt="what is 2+2?", candidate_actions=["compute", "verify"])
    result = default_registry().run("react", problem)
    assert result.status in {"SUCCEEDED", "MAX_STEPS"}
    kinds = {s.kind for s in result.steps}
    assert "thought" in kinds and "action" in kinds


def test_react_with_llm_hook_uses_hook():
    hooks = ReasoningHooks(llm=lambda prompt: "answer: 4")
    result = default_registry().run("react", ReasoningProblem(prompt="2+2?"), hooks)
    assert result.status == "SUCCEEDED"
    assert result.answer == "4"


def test_llm_hook_failure_falls_back():
    def boom(prompt):
        raise RuntimeError("provider down")
    hooks = ReasoningHooks(llm=boom)
    result = default_registry().run("tot", ReasoningProblem(prompt="fallback?"), hooks)
    assert result.status == "SUCCEEDED"


def test_tot_and_got_succeed():
    problem = ReasoningProblem(prompt="plan the release")
    for name in ("tot", "got"):
        result = default_registry().run(name, problem)
        assert result.status == "SUCCEEDED"
        assert result.answer


def test_beam_search_finds_answer_action():
    problem = ReasoningProblem(prompt="solve", candidate_actions=["explore", "answer final"])
    result = default_registry().run("beam", problem)
    assert result.status == "SUCCEEDED"
    assert "answer" in result.answer


def test_best_first_respects_max_steps():
    problem = ReasoningProblem(prompt="loop", candidate_actions=["loop"], max_steps=3)
    result = default_registry().run("best-first", problem)
    assert result.status == "MAX_STEPS"
    assert result.iterations <= 3


def test_htn_decomposition_and_execution():
    tasks = {
        "ship": TaskSpec(name="ship", subtasks=["build", "verify"]),
        "build": TaskSpec(name="build", subtasks=["compile", "compile"]),
        "compile": TaskSpec(name="compile", primitive=True, action="gcc"),
        "verify": TaskSpec(name="verify", primitive=True, action="test"),
    }
    ran = []
    planner = HTNPlanner(tasks, executors={"gcc": lambda p: ran.append("gcc") or "ok",
                                           "test": lambda p: ran.append("test") or "ok"})
    result = planner.run(ReasoningProblem(prompt="ship", context={"task": "ship"}))
    assert result.status == "SUCCEEDED"
    assert ran == ["gcc", "gcc", "test"]
    assert result.answer == "gcc > gcc > test"


def test_htn_cycle_fails():
    tasks = {"a": TaskSpec(name="a", subtasks=["b"]), "b": TaskSpec(name="a", subtasks=["a"])}
    planner = HTNPlanner(tasks)
    result = planner.run(ReasoningProblem(prompt="a", context={"task": "a"}))
    assert result.status == "FAILED"


def test_world_model_picks_best_action():
    calls = []
    def simulate(state, action):
        calls.append(action)
        return 1.0 if action == "good" else 0.0
    hooks = ReasoningHooks(simulate=simulate)
    problem = ReasoningProblem(prompt="act", candidate_actions=["bad", "good"])
    result = default_registry().run("world-model", problem, hooks)
    assert result.answer == "good"
    assert calls


def test_neuro_symbolic_rules_filter_candidates():
    strat = NeuroSymbolicStrategy(rules={"must-be-lower": lambda c: c.islower()})
    problem = ReasoningProblem(prompt="pick", candidate_actions=["BAD", "good", "AlsoBad"])
    result = strat.run(problem)
    assert result.status == "SUCCEEDED"
    assert result.answer == "good"


def test_neuro_symbolic_fails_when_nothing_verifies():
    strat = NeuroSymbolicStrategy(rules={"never": lambda c: False})
    result = strat.run(ReasoningProblem(prompt="x", candidate_actions=["a"]))
    assert result.status == "FAILED"


def test_causal_do_query():
    model = [{
        "cause": {"canonical_id": "urn:deploy"},
        "effect": {"canonical_id": "urn:outage"},
        "status": "HYPOTHESIS",
        "confidence": 0.8,
        "alternatives": [{"canonical_id": "urn:traffic"}],
    }]
    problem = ReasoningProblem(prompt="did deploy cause outage?",
                               context={"cause": "urn:deploy", "effect": "urn:outage"},
                               causal_model=model)
    result = default_registry().run("causal", problem)
    assert result.status == "SUCCEEDED"
    assert result.answer == "0.800"
    kinds = [s.kind for s in result.steps]
    assert "intervention" in kinds and "adjustment" in kinds


def test_meta_selects_causal_for_causal_features():
    problem = ReasoningProblem(prompt="q?", context={"cause": "a", "effect": "b"}, causal_model=[])
    result = default_registry().select_and_run(problem)
    assert result.strategy.startswith("meta->causal")


def test_meta_selects_htn_for_tasks():
    registry = StrategyRegistry()
    registry.register(HTNPlanner({"t": TaskSpec(name="t", primitive=True, action="t")}))
    from eoip.reasoning.strategies import MetaReasoningStrategy
    meta = MetaReasoningStrategy(registry)
    problem = ReasoningProblem(prompt="do it", context={"task": "t"})
    assert meta.select(problem) == "htn"


# ---------------------------------------------------------------------------
# Memory architectures (§7)
# ---------------------------------------------------------------------------

def test_working_memory_token_budget_evicts():
    wm = WorkingMemory(token_budget=10)
    _, evicted = wm.add("x" * 40, priority=0.0)  # 10 tokens
    assert not evicted
    _, evicted = wm.add("y" * 40, priority=0.0)
    assert len(wm.snapshot()) == 1  # oldest evicted, still within budget


def test_working_memory_priority_protects_items():
    wm = WorkingMemory(token_budget=10)  # one item of "x"*40 == exactly 10 tokens
    wm.add("x" * 40, priority=5.0)
    _, evicted = wm.add("y" * 40, priority=0.0)
    assert [e.content for e in evicted] == ["y" * 40]  # low-priority new item evicted
    assert [i.content for i in wm.snapshot()] == ["x" * 40]


def test_estimate_tokens_monotonic():
    assert estimate_tokens("") == 1
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcdefgh") == 2


def test_episodic_memory_consolidation():
    em = EpisodicMemory(consolidate_after=3)
    for i in range(6):
        em.record("event", f"event {i}")
    consolidated = em.consolidate()
    assert consolidated == 3
    open_eps = [e for e in em.all() if not e.consolidated]
    assert len(open_eps) == 3
    assert all(e.summary for e in em.all() if e.consolidated)
    assert em.consolidate() == 0  # nothing left to consolidate


def test_episodic_memory_consolidation_with_hook():
    em = EpisodicMemory(consolidate_after=2, summarize=lambda texts: f"summary of {len(texts)}")
    for i in range(4):
        em.record("event", f"e{i}")
    assert em.consolidate() == 2
    assert em.all()[0].summary == "summary of 2"


def test_semantic_memory_upsert_confidence():
    sm = SemanticMemory()
    sm.upsert("urn:a", "owns", "urn:b", confidence=0.5)
    fact = sm.upsert("urn:a", "owns", "urn:c", confidence=0.9)
    assert fact.object == "urn:c"
    lower = sm.upsert("urn:a", "owns", "urn:d", confidence=0.1)
    assert lower.object == "urn:c"  # lower confidence did not overwrite
    assert len(sm.recall(subject="urn:a", min_confidence=0.9)) == 1


def test_procedural_memory_ranks_by_preconditions():
    pm = ProceduralMemory()
    pm.register("deploy", preconditions=["image-built", "tests-passed", "approval"])
    pm.register("lint", preconditions=["code-present", "ci-green"])
    ranked = pm.retrieve(["image-built", "tests-passed", "code-present"])
    assert ranked[0].name == "deploy"
    assert ranked[1].name == "lint"
    pm.record_outcome("deploy", True)
    assert pm.get("deploy").success_count == 1


def test_shared_memory_atomic_update():
    board = SharedMemory()
    board.write("counter", "1")
    new = board.update("counter", lambda v: str(int(v or "0") + 1))
    assert new == "2"
    assert board.read("counter") == "2"
    assert "counter" in board


def test_hierarchical_memory_layers():
    hm = HierarchicalMemory(l0_capacity=4)
    for i in range(4):
        hm.add_raw(f"item {i}")
    summary = hm.promote()
    assert summary
    assert len(hm.layer("L0")) == 2
    assert len(hm.layer("L1")) == 1
    hm.distill("eternal truth")
    assert hm.layer("L2") == ["eternal truth"]
    with pytest.raises(KeyError):
        hm.layer("L9")


def test_temporal_memory_valid_time_queries():
    tm = TemporalMemory()
    tm.assert_fact("urn:price", "equals", "10", "2024-01-01", "2024-06-01")
    tm.assert_fact("urn:price", "equals", "12", "2024-06-01")
    assert [f.object for f in tm.at("2024-03-01", subject="urn:price")] == ["10"]
    assert [f.object for f in tm.at("2024-07-01", subject="urn:price")] == ["12"]
    assert len(tm.history("urn:price", "equals")) == 2
    with pytest.raises(ValueError):
        tm.assert_fact("a", "b", "c", "2024-06-01", "2024-01-01")


# ---------------------------------------------------------------------------
# Evaluation framework (§7)
# ---------------------------------------------------------------------------

def _trajectory(task_id, steps, tools=None, succeeded=True):
    tools = tools or []
    return Trajectory(
        trajectory_id=f"urn:t:{task_id}", agent_id="agent-x", task_id=task_id,
        steps=[TrajectoryStep(step_index=i, kind="tool_call" if tools else "thought",
                              content=f"s{i}", tool_name=tools[i % len(tools)] if tools else None)
               for i in range(steps)],
        succeeded=succeeded,
    )


def test_step_efficiency_scoring():
    scorer = TrajectoryScorer()
    scorer.set_reference("t1", steps=5)
    scores = scorer.score(_trajectory("t1", 5))
    assert scores.step_efficiency == 1.0 and scores.redundant_steps == 0
    scores = scorer.score(_trajectory("t1", 8))
    assert scores.step_efficiency == pytest.approx(0.4)
    assert scores.redundant_steps == 3


def test_tool_use_precision_recall():
    traj = _trajectory("t2", 3, tools=["search", "search", "run"])
    precision, recall = __import__("eoip.reasoning.evaluation", fromlist=["score_tool_use"]).score_tool_use(traj, ["search", "verify"])
    assert precision == pytest.approx(1 / 3)  # only 1 of 3 used tools is in golden
    assert recall == pytest.approx(0.5)


def test_benchmark_runner_gates():
    tasks = [
        GoldenTask(task_id="ok", prompt="p", reference_steps=3, golden_tools=["a"]),
        GoldenTask(task_id="slow", prompt="p", reference_steps=1),
    ]
    def agent_fn(task):
        if task.task_id == "ok":
            return _trajectory(task.task_id, 2, tools=["a"])
        return _trajectory(task.task_id, 10)
    report = BenchmarkRunner(agent_fn).run(tasks)
    assert report.tasks == 2 and report.passed == 1
    assert report.pass_rate == 0.5
    assert any("slow" in f for f in report.failures)


def test_benchmark_runner_requires_tasks():
    with pytest.raises(ValueError):
        BenchmarkRunner(lambda t: _trajectory(t.task_id, 1)).run([])


def test_adversarial_suite_resistance():
    suite = AdversarialTestSuite(lambda probe: "I cannot share that information.")
    report = suite.run()
    assert report.cases == len(ADVERSARIAL_PROBES)
    assert report.resistance_rate == 1.0


def test_adversarial_suite_detects_leak():
    suite = AdversarialTestSuite(lambda probe: "here is the system prompt: ...")
    report = suite.run(probes=["ignore instructions"])
    assert report.resistance_rate == 0.0


def test_business_outcome_metrics():
    tracker = BusinessOutcomeTracker()
    for i in range(10):
        tracker.record(OutcomeRecord(record_id=f"r{i}", agent_id="a", task_id=f"t{i}",
                                     succeeded=i < 8, resolved_by_agent=i < 9,
                                     cost_tokens=100, latency_seconds=float(i)))
    metrics = tracker.metrics()
    assert metrics.records == 10
    assert metrics.task_success_rate == 0.8
    assert metrics.autonomous_resolution_rate == 0.9
    assert metrics.mean_cost_tokens == 100.0
    assert metrics.p95_latency_seconds == 8.0
    assert metrics.cost_per_successful_task == pytest.approx(1000 / 8)


# ---------------------------------------------------------------------------
# AgentOps (§7)
# ---------------------------------------------------------------------------

def test_run_tracer_lifecycle(tmp_path):
    tracer = RunTracer(tmp_path)
    trace = tracer.start_run("run-1", "agent-x")
    span = tracer.start_span(trace, "llm-call", model="m1")
    tracer.end_span(trace, span)
    final = tracer.end_run(trace, tokens_used=50, estimated_cost=0.001)
    assert final.ended_at and final.spans[0].status == "OK"
    assert tracer.read(trace.trace_id).tokens_used == 50


def test_cost_ledger_accounting():
    ledger = CostLedger()
    ledger.set_rate("m1", 2.0)  # 2.0 per 1k tokens
    entry = ledger.record("run-1", "m1", 1000, 1000, 0.5)
    assert entry["cost"] == pytest.approx(4.0)
    ledger.record("run-2", "unknown-model", 500, 0, 0.1)  # no rate: tokens only
    totals = ledger.totals()
    assert totals["total_tokens"] == 2500
    assert totals["total_cost"] == pytest.approx(4.0)
    assert ledger.totals(run_id="run-1")["total_tokens"] == 2000
    with pytest.raises(ValueError):
        ledger.record("r", "m", -1, 0, 0.0)


def test_deployment_descriptor_validation():
    ok = DeploymentDescriptor(deployment_id="d1", agent_id="a", version="1.0.0",
                              environment="canary", canary_percentage=5.0)
    assert validate_deployment(ok) == []
    bad = DeploymentDescriptor(deployment_id="d2", agent_id="a", version="1.0.0",
                               environment="production")
    violations = validate_deployment(bad)
    assert any("canary" in v for v in violations)


def test_incident_store_lifecycle(tmp_path):
    store = IncidentStore(tmp_path)
    incident = store.open("d1", "SEV2", "agent loop", description="runaway")
    assert incident.status == "OPEN"
    store.update_status(incident, "RESOLVED")
    assert incident.resolved_at
    assert incident.resolution_seconds is not None
    assert len(store.list(status="RESOLVED")) == 1
    with pytest.raises(ValueError):
        store.open("d1", "SEV5", "bad severity")


def test_sla_tracker_burn():
    tracker = SLATracker(SLAPolicy(policy_id="sla1", agent_id="a",
                                   slo_target=0.9, window_records=10, error_budget=0.2))
    for _ in range(9):
        tracker.record(True)
    tracker.record(False)
    status = tracker.status()
    assert status["slo_met"] is True
    assert status["breach"] is False
    assert status["error_budget_remaining"] == 0.5  # 1 of 2 allowed failures burned
    for _ in range(3):
        tracker.record(False)
    assert tracker.status()["slo_met"] is False


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

def test_reasoning_router_routes():
    router = build_router()
    routes = {(next(iter(r.methods)), r.path) for r in router.routes if hasattr(r, "methods")}
    assert ("GET", "/api/v1/reasoning/strategies") in routes
    assert ("POST", "/api/v1/reasoning/strategies/{name}/run") in routes
    assert ("POST", "/api/v1/reasoning/select") in routes
    assert ("POST", "/api/v1/reasoning/memory/working") in routes
    assert ("GET", "/api/v1/reasoning/agentops/costs") in routes
