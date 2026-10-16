"""The 23 autonomous loop primitives (GAP-LOOP-010..032, §2).

Each loop is a deterministic phase schedule over ``LoopDriver``: the
caller supplies a step function keyed by phase name (or a single
function reused across phases), the driver enforces the §2.3 control
properties. Loops never require an LLM; an optional ``llm_hook`` may be
passed by the caller inside its own step function (graceful fallback:
loops run fully deterministically when no hook is provided).

Public loop runners (docstrings tag the loop names from §2):

    run_ooda_loop, run_react_loop, run_plan_execute_observe_loop,
    run_plan_execute_verify_loop, run_replanning_loop, run_reflection_loop,
    run_self_correction_loop, run_evaluator_optimizer_loop,
    run_generate_test_repair_loop, run_hypothesis_experiment_evaluate_loop,
    run_search_expand_prune_loop, run_retrieval_verification_loop,
    run_graph_traversal_loop, run_graph_enrichment_loop,
    run_memory_consolidation_loop, run_context_refresh_loop,
    run_confidence_calibration_loop, run_safety_validation_loop,
    run_retry_backoff_recovery_loop, run_monitor_detect_respond_loop,
    run_simulation_evaluation_loop, run_continuous_improvement_loop,
    run_consensus_reconciliation_loop

Each ``run_*`` accepts ``(step, state=None, config=None, **driver_kwargs)``
where ``step`` is either a ``StepFn`` reused for every phase or a mapping
``{phase_name: StepFn}``.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping

from eoip.loops.core import (
    GateVerdict,
    LoopConfig,
    LoopDriver,
    LoopResult,
    StepFn,
)

# phase schedules, keyed by public snake name (§2 loop inventory)
LOOP_PHASES: dict[str, list[str]] = {
    "ooda": ["observe", "orient", "decide", "act"],
    "react": ["reason", "act"],
    "plan_execute_observe": ["plan", "execute", "observe"],
    "plan_execute_verify": ["plan", "execute", "verify"],
    "replanning": ["plan", "execute", "observe", "replan"],
    "reflection": ["generate", "reflect"],
    "self_correction": ["generate", "critique", "correct"],
    "evaluator_optimizer": ["generate", "evaluate", "optimize"],
    "generate_test_repair": ["generate", "test", "repair"],
    "hypothesis_experiment_evaluate": ["hypothesize", "experiment", "evaluate"],
    "search_expand_prune": ["search", "expand", "prune"],
    "retrieval_verification": ["retrieve", "verify"],
    "graph_traversal": ["select", "traverse", "evaluate"],
    "graph_enrichment": ["identify_gap", "enrich", "validate"],
    "memory_consolidation": ["collect", "consolidate", "commit"],
    "context_refresh": ["assess", "evict", "reload"],
    "confidence_calibration": ["predict", "score", "calibrate"],
    "safety_validation": ["propose", "validate", "gate"],
    "retry_backoff_recovery": ["attempt", "backoff", "recover"],
    "monitor_detect_respond": ["monitor", "detect", "respond"],
    "simulation_evaluation": ["simulate", "evaluate"],
    "continuous_improvement": ["measure", "diagnose", "improve"],
    "consensus_reconciliation": ["propose", "collect_votes", "reconcile"],
}


def _resolve_step(step: StepFn | Mapping[str, StepFn], phase: str) -> StepFn:
    if callable(step):
        return step
    if phase in step:
        return step[phase]
    return step["*"]


def _run(loop_key: str, step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None,
         config: LoopConfig | None, **driver_kwargs: Any) -> LoopResult:
    config = config or LoopConfig(loop_name=loop_key)
    if config.loop_name == "loop":
        config = config.model_copy(update={"loop_name": loop_key})
    phases = LOOP_PHASES[loop_key]
    driver = LoopDriver(config, phases=phases, **driver_kwargs)

    def dispatch(run_state: dict[str, Any], ctx: Any) -> Any:
        return _resolve_step(step, ctx.phase or phases[0])(run_state, ctx)

    return driver.run(dispatch, state)


def run_ooda_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                  config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """OODA loop — Observe, Orient, Decide, Act (GAP-LOOP-010, §2)."""
    return _run("ooda", step, state, config, **kwargs)


def run_react_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                   config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """ReAct loop — Reason, Act (GAP-LOOP-011, §2)."""
    return _run("react", step, state, config, **kwargs)


def run_plan_execute_observe_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                  config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Plan-Execute-Observe loop (GAP-LOOP-012, §2)."""
    return _run("plan_execute_observe", step, state, config, **kwargs)


def run_plan_execute_verify_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                 config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Plan-Execute-Verify loop (GAP-LOOP-013, §2)."""
    return _run("plan_execute_verify", step, state, config, **kwargs)


def run_replanning_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                        config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Replanning loop — Plan, Execute, Observe, Replan (GAP-LOOP-014, §2)."""
    return _run("replanning", step, state, config, **kwargs)


def run_reflection_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                        config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Reflection loop — Generate, Reflect (GAP-LOOP-015, §2)."""
    return _run("reflection", step, state, config, **kwargs)


def run_self_correction_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                             config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Self-Correction loop — Generate, Critique, Correct (GAP-LOOP-016, §2)."""
    return _run("self_correction", step, state, config, **kwargs)


def run_evaluator_optimizer_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                 config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Evaluator-Optimizer loop — Generate, Evaluate, Optimize (GAP-LOOP-017, §2)."""
    return _run("evaluator_optimizer", step, state, config, **kwargs)


def run_generate_test_repair_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                  config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Generate-Test-Repair loop (GAP-LOOP-018, §2)."""
    return _run("generate_test_repair", step, state, config, **kwargs)


def run_hypothesis_experiment_evaluate_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                            config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Hypothesis-Experiment-Evaluate loop (GAP-LOOP-019, §2)."""
    return _run("hypothesis_experiment_evaluate", step, state, config, **kwargs)


def run_search_expand_prune_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                 config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Search-Expand-Prune loop (GAP-LOOP-020, §2)."""
    return _run("search_expand_prune", step, state, config, **kwargs)


def run_retrieval_verification_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                    config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Retrieval-Verification loop (GAP-LOOP-021, §2)."""
    return _run("retrieval_verification", step, state, config, **kwargs)


def run_graph_traversal_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                             config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Graph-Traversal loop (loop-over-graph, §38, GAP-LOOP-022)."""
    return _run("graph_traversal", step, state, config, **kwargs)


def run_graph_enrichment_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                              config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Graph-Enrichment loop — Identify-Gap, Enrich, Validate (GAP-LOOP-023, §2)."""
    return _run("graph_enrichment", step, state, config, **kwargs)


def run_memory_consolidation_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                  config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Memory-Consolidation loop — Collect, Consolidate, Commit (§32, GAP-LOOP-024)."""
    return _run("memory_consolidation", step, state, config, **kwargs)


def run_context_refresh_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                             config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Context-Refresh loop — Assess, Evict, Reload (§33, GAP-LOOP-025)."""
    return _run("context_refresh", step, state, config, **kwargs)


def run_confidence_calibration_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                    config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Confidence-Calibration loop — Predict, Score, Calibrate (GAP-LOOP-026, §2)."""
    return _run("confidence_calibration", step, state, config, **kwargs)


def run_safety_validation_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                               config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Safety-Validation loop — Propose, Validate, Gate (GAP-LOOP-027, §2)."""
    return _run("safety_validation", step, state, config, **kwargs)


def run_retry_backoff_recovery_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                    config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Retry-Backoff-Recovery loop (GAP-LOOP-028, §2)."""
    return _run("retry_backoff_recovery", step, state, config, **kwargs)


def run_monitor_detect_respond_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                    config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Monitor-Detect-Respond loop (GAP-LOOP-029, §2)."""
    return _run("monitor_detect_respond", step, state, config, **kwargs)


def run_simulation_evaluation_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                   config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Simulation-Evaluation loop (GAP-LOOP-030, §2)."""
    return _run("simulation_evaluation", step, state, config, **kwargs)


def run_continuous_improvement_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                    config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Continuous-Improvement loop — Measure, Diagnose, Improve (GAP-LOOP-031, §2)."""
    return _run("continuous_improvement", step, state, config, **kwargs)


def run_consensus_reconciliation_loop(step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
                                      config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Consensus-Reconciliation loop — Propose, Collect-Votes, Reconcile (GAP-LOOP-032, §2)."""
    return _run("consensus_reconciliation", step, state, config, **kwargs)


LOOP_RUNNERS: dict[str, Callable[..., LoopResult]] = {
    "ooda": run_ooda_loop,
    "react": run_react_loop,
    "plan_execute_observe": run_plan_execute_observe_loop,
    "plan_execute_verify": run_plan_execute_verify_loop,
    "replanning": run_replanning_loop,
    "reflection": run_reflection_loop,
    "self_correction": run_self_correction_loop,
    "evaluator_optimizer": run_evaluator_optimizer_loop,
    "generate_test_repair": run_generate_test_repair_loop,
    "hypothesis_experiment_evaluate": run_hypothesis_experiment_evaluate_loop,
    "search_expand_prune": run_search_expand_prune_loop,
    "retrieval_verification": run_retrieval_verification_loop,
    "graph_traversal": run_graph_traversal_loop,
    "graph_enrichment": run_graph_enrichment_loop,
    "memory_consolidation": run_memory_consolidation_loop,
    "context_refresh": run_context_refresh_loop,
    "confidence_calibration": run_confidence_calibration_loop,
    "safety_validation": run_safety_validation_loop,
    "retry_backoff_recovery": run_retry_backoff_recovery_loop,
    "monitor_detect_respond": run_monitor_detect_respond_loop,
    "simulation_evaluation": run_simulation_evaluation_loop,
    "continuous_improvement": run_continuous_improvement_loop,
    "consensus_reconciliation": run_consensus_reconciliation_loop,
}


def run_loop(loop_name: str, step: StepFn | Mapping[str, StepFn], state: dict[str, Any] | None = None,
             config: LoopConfig | None = None, **kwargs: Any) -> LoopResult:
    """Dispatch any of the 23 loops by snake-case name (§2)."""
    if loop_name not in LOOP_RUNNERS:
        raise KeyError(f"unknown loop: {loop_name!r}; known: {sorted(LOOP_RUNNERS)}")
    return LOOP_RUNNERS[loop_name](step, state, config, **kwargs)
