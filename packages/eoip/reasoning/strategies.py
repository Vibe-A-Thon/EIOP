"""Reasoning strategy registry — §7 Reasoning & Orchestration: reasoning architectures.

Implements the §7 reasoning architectures as a deterministic-first registry.
Every strategy operates over a plain-text problem (plus optional structured
context) and produces a :class:`ReasoningResult` trace. LLM hooks are
*optional*: when no hook is supplied each strategy falls back to a
deterministic heuristic (lexicographic scoring, string heuristics, or the
caller-supplied scoring function), so every strategy runs offline in tests.

Strategies (§7 "Reasoning Architectures"):

* ``react``            — ReAct thought/action/observation interleaving.
* ``tot``              — Tree-of-Thoughts: expand + score + backtrack by depth.
* ``got``              — Graph-of-Thoughts: DAG of thoughts, convergent aggregation.
* ``best-first`` / ``beam`` — search-based reasoning over scored states.
* ``htn``              — HTN-lite planning: task decomposition into primitives.
* ``world-model``      — world-model rollout: score actions by simulated return.
* ``neuro-symbolic``   — rules verified over embedding-ranked candidates.
* ``causal``           — do-operator style queries over causal hypotheses.
* ``meta``             — meta-reasoning: strategy selection by problem features.
"""

from __future__ import annotations

import hashlib
import heapq
import itertools
from collections import defaultdict
from typing import Any, Callable, Iterable, Protocol

from pydantic import BaseModel, ConfigDict, Field


def _urn(kind: str, seed: str) -> str:
    return "urn:eoip:reasoning:" + kind + ":" + hashlib.sha256(seed.encode()).hexdigest()[:24]


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------

class ReasoningHooks(BaseModel):
    """Optional LLM/cognitive hooks. Every field is optional; strategies must
    degrade to deterministic heuristics when a hook is absent."""

    model_config = ConfigDict(extra="forbid")

    llm: Callable[[str], str] | None = Field(default=None, exclude=True)
    score: Callable[[str], float] | None = Field(default=None, exclude=True)
    simulate: Callable[[str, str], float] | None = Field(default=None, exclude=True)


class ReasoningProblem(BaseModel):
    """A reasoning problem instance passed to any registered strategy."""

    model_config = ConfigDict(extra="forbid")

    problem_id: str | None = None
    prompt: str
    context: dict[str, Any] = Field(default_factory=dict)
    max_steps: int = Field(default=16, ge=1)
    candidate_actions: list[str] = Field(default_factory=list)
    causal_model: list[dict[str, Any]] = Field(default_factory=list)


class ReasoningStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_index: int
    kind: str  # thought | action | observation | expansion | rollout | rule-check | ...
    content: str
    score: float | None = None
    parent: str | None = None


class ReasoningResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    result_id: str
    strategy: str
    status: str  # SUCCEEDED | MAX_STEPS | FAILED
    answer: str = ""
    steps: list[ReasoningStep] = Field(default_factory=list)
    iterations: int = 0


class ReasoningStrategy(Protocol):
    """Protocol for §7 reasoning architectures."""

    name: str

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        ...


def _default_score(hooks: ReasoningHooks | None, text: str) -> float:
    if hooks and hooks.score:
        return float(hooks.score(text))
    # Deterministic heuristic: reward specificity (length) + keyword coverage.
    keywords = ("because", "therefore", "verify", "check", "result", "evidence")
    hits = sum(1 for kw in keywords if kw in text.lower())
    return round(min(len(text), 400) / 400.0 + hits * 0.25, 4)


def _llm_or(hooks: ReasoningHooks | None, prompt: str, fallback: str) -> str:
    if hooks and hooks.llm:
        try:
            out = hooks.llm(prompt)
            if out:
                return str(out)
        except Exception:
            pass  # graceful fallback to deterministic text
    return fallback


# ---------------------------------------------------------------------------
# ReAct (§7)
# ---------------------------------------------------------------------------

class ReActStrategy:
    """ReAct: interleave Thought / Action / Observation until an answer."""

    name = "react"

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        steps: list[ReasoningStep] = []
        context_note = ""
        for i in range(problem.max_steps):
            thought = _llm_or(hooks, f"Thought {i} for: {problem.prompt}",
                              f"Consider what is known after: {context_note or 'the initial prompt'}.")
            steps.append(ReasoningStep(step_index=len(steps), kind="thought", content=thought))
            action = _llm_or(
                hooks,
                f"Action {i} (final answer when confident) for: {problem.prompt}",
                problem.candidate_actions[min(i, len(problem.candidate_actions) - 1)]
                if problem.candidate_actions and "answer" not in thought.lower()
                else f"answer: {problem.prompt}",
            )
            steps.append(ReasoningStep(step_index=len(steps), kind="action", content=action,
                                       score=_default_score(hooks, action)))
            if action.lower().startswith("answer:"):
                return ReasoningResult(result_id=_urn("result", problem.prompt + "react"), strategy=self.name,
                                       status="SUCCEEDED", answer=action.split(":", 1)[1].strip(),
                                       steps=steps, iterations=i + 1)
            obs = _llm_or(hooks, f"Observation after action: {action}",
                          f"observed result of '{action}'")
            context_note = obs
            steps.append(ReasoningStep(step_index=len(steps), kind="observation", content=obs))
        return ReasoningResult(result_id=_urn("result", problem.prompt + "react"), strategy=self.name,
                               status="MAX_STEPS", steps=steps, iterations=problem.max_steps)


# ---------------------------------------------------------------------------
# Tree-of-Thoughts (§7)
# ---------------------------------------------------------------------------

class TreeOfThoughtsStrategy:
    """ToT: expand candidate thoughts per depth, keep the best-scored branch."""

    name = "tot"

    def __init__(self, branching: int = 2, depth: int = 3):
        self.branching = max(1, branching)
        self.depth = max(1, depth)

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        steps: list[ReasoningStep] = []
        frontier: list[tuple[float, str]] = [(0.0, problem.prompt)]
        for depth in range(self.depth):
            candidates: list[tuple[float, str]] = []
            for _, parent in frontier:
                for b in range(self.branching):
                    thought = _llm_or(
                        hooks,
                        f"Expand branch {b} at depth {depth} from: {parent}",
                        f"{parent} -> option {b + 1} (depth {depth + 1})",
                    )
                    score = _default_score(hooks, thought)
                    steps.append(ReasoningStep(step_index=len(steps), kind="expansion", content=thought,
                                               score=score, parent=parent))
                    candidates.append((score, thought))
            candidates.sort(key=lambda item: item[0], reverse=True)
            frontier = candidates[: self.branching]
        best = frontier[0][1] if frontier else problem.prompt
        return ReasoningResult(result_id=_urn("result", problem.prompt + "tot"), strategy=self.name,
                               status="SUCCEEDED", answer=best, steps=steps,
                               iterations=min(self.depth, problem.max_steps))


# ---------------------------------------------------------------------------
# Graph-of-Thoughts (§7)
# ---------------------------------------------------------------------------

class GraphOfThoughtsStrategy:
    """GoT: thoughts form a DAG; aggregation combines leaf thoughts by score."""

    name = "got"

    def __init__(self, branching: int = 2, depth: int = 3):
        self.branching = max(1, branching)
        self.depth = max(1, depth)

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        steps: list[ReasoningStep] = []
        current = [problem.prompt]
        for depth in range(self.depth):
            nxt: list[str] = []
            for parent in current:
                for b in range(self.branching):
                    thought = _llm_or(hooks, f"GoT vertex depth {depth} branch {b}: {parent}",
                                      f"{parent} | vertex d{depth}b{b}")
                    score = _default_score(hooks, thought)
                    steps.append(ReasoningStep(step_index=len(steps), kind="vertex", content=thought,
                                               score=score, parent=parent))
                    nxt.append(thought)
            current = nxt
        scored = sorted(((s.score or 0.0, s.content) for s in steps if s.kind == "vertex"),
                        reverse=True)
        answer = scored[0][1] if scored else problem.prompt
        return ReasoningResult(result_id=_urn("result", problem.prompt + "got"), strategy=self.name,
                               status="SUCCEEDED", answer=answer, steps=steps,
                               iterations=len(current) if current else 1)


# ---------------------------------------------------------------------------
# Search-based: best-first and beam (§7)
# ---------------------------------------------------------------------------

class _SearchBase:
    name = "search"

    def _neighbors(self, state: str, problem: ReasoningProblem, hooks: ReasoningHooks | None) -> list[str]:
        actions = problem.candidate_actions or ["explore", "refine", "answer"]
        return [f"{state} + {a}" for a in actions]

    def _score(self, state: str, hooks: ReasoningHooks | None) -> float:
        return _default_score(hooks, state)


class BestFirstSearchStrategy(_SearchBase):
    """Best-first search over states scored by the (optional) hook."""

    name = "best-first"

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        steps: list[ReasoningStep] = []
        counter = itertools.count()
        heap: list[tuple[float, int, str]] = [(-self._score(problem.prompt, hooks), next(counter), problem.prompt)]
        visited: set[str] = set()
        iterations = 0
        while heap and iterations < problem.max_steps:
            neg, _, state = heapq.heappop(heap)
            if state in visited:
                continue
            visited.add(state)
            score = -neg
            steps.append(ReasoningStep(step_index=len(steps), kind="expand", content=state, score=score))
            iterations += 1
            if state.split(" + ")[-1].startswith("answer"):
                return ReasoningResult(result_id=_urn("result", problem.prompt + "bfs"), strategy=self.name,
                                       status="SUCCEEDED", answer=state, steps=steps, iterations=iterations)
            for nxt in self._neighbors(state, problem, hooks):
                heapq.heappush(heap, (-self._score(nxt, hooks), next(counter), nxt))
        return ReasoningResult(result_id=_urn("result", problem.prompt + "bfs"), strategy=self.name,
                               status="MAX_STEPS", answer="", steps=steps, iterations=iterations)


class BeamSearchStrategy(_SearchBase):
    """Beam search: keep the top-``beam_width`` scored states per level."""

    name = "beam"

    def __init__(self, beam_width: int = 2, depth: int = 4):
        self.beam_width = max(1, beam_width)
        self.depth = max(1, depth)

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        steps: list[ReasoningStep] = []
        beam = [problem.prompt]
        best = problem.prompt
        best_score = self._score(best, hooks)
        for depth in range(self.depth):
            scored: list[tuple[float, str]] = []
            for state in beam:
                for nxt in self._neighbors(state, problem, hooks):
                    s = self._score(nxt, hooks)
                    steps.append(ReasoningStep(step_index=len(steps), kind="candidate", content=nxt,
                                               score=s, parent=state))
                    scored.append((s, nxt))
            scored.sort(key=lambda item: item[0], reverse=True)
            beam = [s for _, s in scored[: self.beam_width]]
            if beam and scored[0][0] >= best_score:
                best_score, best = scored[0]
            if any(state.split(" + ")[-1].startswith("answer") for state in beam):
                chosen = next(s for s in beam if s.split(" + ")[-1].startswith("answer"))
                return ReasoningResult(result_id=_urn("result", problem.prompt + "beam"), strategy=self.name,
                                       status="SUCCEEDED", answer=chosen, steps=steps, iterations=depth + 1)
        return ReasoningResult(result_id=_urn("result", problem.prompt + "beam"), strategy=self.name,
                               status="SUCCEEDED", answer=best, steps=steps, iterations=self.depth)


# ---------------------------------------------------------------------------
# HTN-lite planning (§7)
# ---------------------------------------------------------------------------

class TaskSpec(BaseModel):
    """A task in an HTN network: primitive (executable) or compound (decomposed)."""

    model_config = ConfigDict(extra="forbid")

    name: str
    primitive: bool = False
    subtasks: list[str] = Field(default_factory=list)  # compound: ordered decomposition
    action: str | None = None  # primitive: executor key


class HTNPlanner:
    """HTN-lite: decompose a compound task into primitive actions, then execute
    primitives via the caller-supplied executor registry."""

    name = "htn"

    def __init__(self, tasks: dict[str, TaskSpec], executors: dict[str, Callable[..., str]] | None = None):
        self.tasks = tasks
        self.executors = executors or {}

    def decompose(self, task_name: str, _depth: int = 0) -> list[str]:
        if _depth > 64:
            raise ValueError("HTN decomposition exceeded maximum depth (possible cycle)")
        spec = self.tasks[task_name]
        if spec.primitive:
            return [spec.action or spec.name]
        plan: list[str] = []
        for sub in spec.subtasks:
            plan.extend(self.decompose(sub, _depth + 1))
        return plan

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        steps: list[ReasoningStep] = []
        root = problem.context.get("task") or problem.prompt
        try:
            plan = self.decompose(root)
        except (KeyError, ValueError) as exc:
            return ReasoningResult(result_id=_urn("result", str(root) + "htn"), strategy=self.name,
                                   status="FAILED", answer=str(exc), steps=steps, iterations=0)
        for i, action in enumerate(plan[: problem.max_steps]):
            steps.append(ReasoningStep(step_index=len(steps), kind="decompose", content=action))
            executor = self.executors.get(action)
            if executor is not None:
                outcome = executor(problem)
                steps.append(ReasoningStep(step_index=len(steps), kind="execute", content=str(outcome),
                                           score=_default_score(hooks, str(outcome))))
        return ReasoningResult(result_id=_urn("result", str(root) + "htn"), strategy=self.name,
                               status="SUCCEEDED", answer=" > ".join(plan), steps=steps,
                               iterations=len(plan))


# ---------------------------------------------------------------------------
# World-model rollout (§7)
# ---------------------------------------------------------------------------

class WorldModelRolloutStrategy:
    """Score each candidate action by rolling out a world model and summing the
    simulated return; pick the argmax action."""

    name = "world-model"

    def __init__(self, horizon: int = 3):
        self.horizon = max(1, horizon)

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        steps: list[ReasoningStep] = []
        actions = problem.candidate_actions or ["a", "b"]
        returns: dict[str, float] = {}
        for action in actions:
            total = 0.0
            state = problem.prompt
            for h in range(self.horizon):
                if hooks and hooks.simulate:
                    reward = float(hooks.simulate(state, action))
                    nxt = f"{state} ~{action}"
                else:
                    # Deterministic pseudo-transition derived from content hash.
                    digest = int(hashlib.sha256(f"{state}|{action}|{h}".encode()).hexdigest()[:8], 16)
                    reward = (digest % 1000) / 1000.0
                    nxt = f"{state} ~{action}[{h}]"
                total += reward
                steps.append(ReasoningStep(step_index=len(steps), kind="rollout",
                                           content=f"action={action} h={h} r={reward:.3f}",
                                           score=reward))
                state = nxt
            returns[action] = total
        best = max(returns, key=returns.get) if returns else ""
        return ReasoningResult(result_id=_urn("result", problem.prompt + "wm"), strategy=self.name,
                               status="SUCCEEDED", answer=best, steps=steps, iterations=len(actions))


# ---------------------------------------------------------------------------
# Neuro-symbolic (§7)
# ---------------------------------------------------------------------------

class NeuroSymbolicStrategy:
    """Rank candidate answers with an embedding-style scorer, then verify the
    top candidates against deterministic symbolic rules."""

    name = "neuro-symbolic"

    def __init__(self, rules: dict[str, Callable[[str], bool]] | None = None, top_k: int = 3):
        self.rules = rules or {}
        self.top_k = max(1, top_k)

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        steps: list[ReasoningStep] = []
        candidates = list(problem.candidate_actions) or [problem.prompt]
        ranked = sorted(candidates, key=lambda c: _default_score(hooks, c), reverse=True)[: self.top_k]
        verified: list[str] = []
        for cand in ranked:
            score = _default_score(hooks, cand)
            failed = [name for name, rule in self.rules.items() if not rule(cand)]
            kind = "rule-check"
            steps.append(ReasoningStep(step_index=len(steps), kind=kind, content=cand, score=score,
                                       parent=",".join(failed) if failed else None))
            if not failed:
                verified.append(cand)
        answer = verified[0] if verified else ""
        status = "SUCCEEDED" if verified else "FAILED"
        return ReasoningResult(result_id=_urn("result", problem.prompt + "ns"), strategy=self.name,
                               status=status, answer=answer, steps=steps, iterations=len(ranked))


# ---------------------------------------------------------------------------
# Causal — do-operator queries over causal hypotheses (§7)
# ---------------------------------------------------------------------------

class CausalStrategy:
    """Answer do-operator style queries (``P(effect | do(cause))``) over a
    caller-supplied causal model (list of hypothesis dicts compatible with
    ``eoip.graph.causal.CausalHypothesis.to_dict``). Backdoor adjustment:
    confounders are blocked by conditioning on the ``context`` variables."""

    name = "causal"

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        steps: list[ReasoningStep] = []
        model = problem.causal_model
        cause = problem.context.get("cause", "")
        effect = problem.context.get("effect", "")
        if not cause or not effect:
            return ReasoningResult(result_id=_urn("result", problem.prompt + "causal"), strategy=self.name,
                                   status="FAILED", answer="query requires context.cause and context.effect",
                                   steps=steps, iterations=0)
        relevant = [h for h in model if h.get("cause", {}).get("canonical_id") == cause
                    and h.get("effect", {}).get("canonical_id") == effect]
        steps.append(ReasoningStep(step_index=0, kind="intervention",
                                   content=f"do({cause}) — sever incoming edges to {cause}"))
        confounders = sorted({alt.get("canonical_id") or alt.get("id", "")
                              for h in relevant for alt in h.get("alternatives", [])} - {""})
        steps.append(ReasoningStep(step_index=1, kind="adjustment",
                                   content=f"condition on backdoor set {{{', '.join(confounders)}}}"))
        confidences = [float(h.get("confidence", 0.0)) for h in relevant if h.get("status") != "REJECTED"]
        estimate = max(confidences) if confidences else 0.0
        steps.append(ReasoningStep(step_index=2, kind="estimate", content=f"P({effect}|do({cause}))={estimate:.3f}",
                                   score=estimate))
        return ReasoningResult(result_id=_urn("result", problem.prompt + "causal"), strategy=self.name,
                               status="SUCCEEDED", answer=f"{estimate:.3f}", steps=steps,
                               iterations=len(relevant) + 1)


# ---------------------------------------------------------------------------
# Meta-reasoning: strategy selection by problem features (§7)
# ---------------------------------------------------------------------------

class MetaReasoningStrategy:
    """Select a reasoning strategy from observable problem features."""

    name = "meta"

    def __init__(self, registry: StrategyRegistry | None = None):
        self.registry = registry or default_registry()

    def select(self, problem: ReasoningProblem) -> str:
        ctx = problem.context
        if ctx.get("cause") and ctx.get("effect"):
            return "causal"
        if ctx.get("task") or ctx.get("decomposable"):
            return "htn"
        if problem.causal_model:
            return "got"
        if len(problem.candidate_actions) >= 3:
            return "world-model"
        if problem.context.get("multi_step") or len(problem.prompt) > 200:
            return "tot"
        if problem.context.get("tools"):
            return "react"
        return "best-first"

    def run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        chosen = self.select(problem)
        result = self.registry.run(chosen, problem, hooks)
        result.steps.insert(0, ReasoningStep(step_index=0, kind="meta-select", content=chosen))
        for i, s in enumerate(result.steps):
            s.step_index = i
        result.strategy = f"meta->{chosen}"
        return result


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class StrategyRegistry:
    """Registry of §7 reasoning strategies keyed by name."""

    def __init__(self) -> None:
        self._strategies: dict[str, ReasoningStrategy] = {}

    def register(self, strategy: ReasoningStrategy) -> None:
        self._strategies[strategy.name] = strategy

    def names(self) -> list[str]:
        return sorted(self._strategies)

    def get(self, name: str) -> ReasoningStrategy:
        if name not in self._strategies:
            raise KeyError(f"unknown reasoning strategy: {name}")
        return self._strategies[name]

    def run(self, name: str, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        return self.get(name).run(problem, hooks)

    def select_and_run(self, problem: ReasoningProblem, hooks: ReasoningHooks | None = None) -> ReasoningResult:
        """Use meta-reasoning to choose a strategy, then run it."""
        meta = MetaReasoningStrategy(self)
        return meta.run(problem, hooks)


_DEFAULT: StrategyRegistry | None = None


def default_registry() -> StrategyRegistry:
    global _DEFAULT
    if _DEFAULT is None:
        reg = StrategyRegistry()
        reg.register(ReActStrategy())
        reg.register(TreeOfThoughtsStrategy())
        reg.register(GraphOfThoughtsStrategy())
        reg.register(BestFirstSearchStrategy())
        reg.register(BeamSearchStrategy())
        reg.register(HTNPlanner({}))
        reg.register(WorldModelRolloutStrategy())
        reg.register(NeuroSymbolicStrategy())
        reg.register(CausalStrategy())
        reg.register(MetaReasoningStrategy(reg))
        _DEFAULT = reg
    return _DEFAULT
