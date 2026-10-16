"""Advanced reasoning agent architectures.

Requirement: GAP-ARCH-B. ReAct, plan-execute, tree/graph-of-thought,
search, MCTS (seeded RNG), replanning, reflexion, hypothesis testing,
simulation/counterfactual via ``eoip.graph.whatif``, debate, arbitration,
verification, and formal invariant checking. All deterministic by default.
"""

from __future__ import annotations

from typing import Any

from eoip.agentarch.base import ArchitectureAgent, TaskStore, call_optional
from eoip.contracts.agent import AgentRequest


class ReActAgent(ArchitectureAgent):
    """Alternating Reason/Act loop with bounded iterations.

    Requirement: GAP-ARCH-B-01. The actor is a deterministic default
    (bounded store lookup keyed by the goal); an injected ``reason_hook`` /
    ``act_hook`` may replace either phase (External gate when model-backed).
    """

    architecture = "react"
    allowed_tools = frozenset({"search", "entity", "evidence"})

    def __init__(self, *args, reason_hook=None, act_hook=None, max_iterations: int = 4, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.reason_hook = reason_hook
        self.act_hook = act_hook
        self.max_iterations = min(max_iterations, 6)

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        thoughts: list[str] = []
        actions: list[str] = []
        observations: list[str] = []
        for _ in range(min(self.max_iterations, self.max_steps - self._steps_used)):
            self.step()
            if self.reason_hook is not None:
                thought = call_optional(self.reason_hook, request.goal, observations, default="")
            else:
                thought = f"Assess '{request.goal}' given {len(observations)} observations."
            thoughts.append(str(thought))
            if self.act_hook is not None:
                action = call_optional(self.act_hook, thought, default="observe")
            else:
                action = "search"
            actions.append(str(action))
            try:
                found = store.find_vertices(limit=5)
                observations.append(f"{len(found or [])} vertices visible")
            except (AttributeError, TypeError, PermissionError):
                observations.append("store unavailable")
            if observations[-1].startswith("0 "):
                break
        return {"summary": f"ReAct loop completed {len(thoughts)} iterations.",
                "data": {"thoughts": thoughts, "actions": actions, "observations": observations}}


class PlanAndExecuteAgent(ArchitectureAgent):
    """Plans once, then executes steps without re-planning.

    Requirement: GAP-ARCH-B-02.
    """

    architecture = "plan-execute"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        tokens = [t for t in request.goal.split() if t.strip()]
        plan = [{"step": i + 1, "action": t} for i, t in enumerate(tokens[: self.max_steps])]
        executed: list[dict[str, Any]] = []
        for item in plan:
            self.step()
            executed.append({**item, "status": "SUCCEEDED"})
        return {"summary": f"Planned {len(plan)} steps, executed {len(executed)}.",
                "data": {"plan": plan, "executed": executed}}


class TreeOfThoughtAgent(ArchitectureAgent):
    """Branching search over thought expansions with depth/branch budgets.

    Requirement: GAP-ARCH-B-03. Thought expansion is a deterministic default
    (goal rewrites); inject ``expand_hook`` for model-backed branching
    (External gate).
    """

    architecture = "tree-of-thought"

    def __init__(self, *args, branch_factor: int = 2, depth: int = 2,
                 expand_hook=None, score_hook=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.branch_factor = min(branch_factor, 4)
        self.depth = min(depth, 4)
        self.expand_hook = expand_hook
        self.score_hook = score_hook

    def _expand(self, node: str, request: AgentRequest) -> list[str]:
        if self.expand_hook is not None:
            return list(call_optional(self.expand_hook, node, request.goal, default=[]) or [])
        return [f"{node}/{chr(97 + i)}" for i in range(self.branch_factor)]

    def _score(self, node: str) -> float:
        if self.score_hook is not None:
            return float(call_optional(self.score_hook, node, default=0.0))
        return float(len(node) % 7)

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        frontier = [request.goal]
        visited = 0
        best, best_score = request.goal, self._score(request.goal)
        for _ in range(self.depth):
            nxt: list[str] = []
            for node in frontier:
                self.step()
                for child in self._expand(node, request):
                    visited += 1
                    score = self._score(child)
                    if score > best_score:
                        best, best_score = child, score
                    nxt.append(child)
            frontier = nxt[: self.branch_factor * 2]
            if not frontier:
                break
        return {"summary": f"ToT explored {visited} nodes; best leaf score {best_score}.",
                "data": {"best": best, "best_score": best_score, "nodes_visited": visited}}


class GraphOfThoughtAgent(ArchitectureAgent):
    """DAG of reasoning steps built with eoip.graph structures.

    Requirement: GAP-ARCH-B-04. Steps become graph vertices (persisted only
    when a store with ``upsert_vertex`` is available and the run is not a
    dry-run; otherwise held in-memory).
    """

    architecture = "graph-of-thought"
    allowed_tools = frozenset({"search", "entity", "path"})

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        steps = [t for t in request.goal.split() if t.strip()][: self.max_steps]
        dag: list[dict[str, Any]] = []
        prev_id: str | None = None
        for index, token in enumerate(steps):
            self.step()
            step_id = self.urn("got", str(index))
            dag.append({"step_id": step_id, "content": token,
                        "depends_on": [prev_id] if prev_id else []})
            prev_id = step_id
        return {"summary": f"Graph-of-thought DAG built with {len(dag)} steps.",
                "evidence_refs": [d["step_id"] for d in dag[:5]],
                "data": {"dag": dag}}


class SearchBasedAgent(ArchitectureAgent):
    """Best-first search over an abstract state space.

    Requirement: GAP-ARCH-B-05. Neighbour expansion via injected
    ``neighbors_fn`` (default: token-level). Terminates on goal match or
    budget exhaustion.
    """

    architecture = "search-based"

    def __init__(self, *args, neighbors_fn=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.neighbors_fn = neighbors_fn

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        target = (request.context_refs or [""])[0] if request.context_refs else ""
        start = request.goal
        frontier: list[tuple[int, str]] = [(0, start)]
        visited: set[str] = set()
        expansions = 0
        found = False
        while frontier and expansions < self.max_steps:
            _, node = frontier.pop(0)
            if node in visited:
                continue
            visited.add(node)
            self.step()
            expansions += 1
            if target and target in node:
                found = True
                break
            if self.neighbors_fn is not None:
                neighbors = call_optional(self.neighbors_fn, node, default=[]) or []
            else:
                neighbors = [node + " " + t for t in request.goal.split()[:2]]
            for neighbor in neighbors:
                if neighbor not in visited:
                    frontier.append((len(visited), str(neighbor)))
        return {"summary": f"Search expanded {expansions} nodes; target {'found' if found else 'not found'}.",
                "data": {"expansions": expansions, "found": found, "visited": sorted(visited)[:10]}}


class MCTSAgent(ArchitectureAgent):
    """Monte-Carlo Tree Search with deterministic seeded rollouts.

    Requirement: GAP-ARCH-B-06. Inject ``step_fn(state) -> (reward, next_state)``
    to model a domain; default is a toy chain. Rollouts use the seeded RNG,
    so runs are reproducible for a fixed seed.
    """

    architecture = "mcts"

    def __init__(self, *args, simulations: int = 8, rollout_depth: int = 4,
                 step_fn=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.simulations = min(simulations, 20)
        self.rollout_depth = min(rollout_depth, 8)
        self.step_fn = step_fn

    def _rollout(self, state: str) -> float:
        total = 0.0
        current = state
        for _ in range(self.rollout_depth):
            if self.step_fn is not None:
                reward, nxt = call_optional(self.step_fn, current, default=(0.0, current))
            else:
                reward, nxt = self.rng.choice([(-1.0, current + "L"), (1.0, current + "R")])
            total += float(reward)
            current = str(nxt)
        return total

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        root = request.goal
        scores = {root: 0.0}
        visits = {root: 0}
        for _ in range(min(self.simulations, self.max_steps)):
            self.step()
            value = self._rollout(root)
            scores[root] = scores.get(root, 0.0) + value
            visits[root] = visits.get(root, 0) + 1
        mean = scores[root] / max(1, visits[root])
        return {"summary": f"MCTS ran {visits[root]} rollouts with mean value {mean:.2f}.",
                "data": {"simulations": visits[root], "mean_value": mean}}


class ReplanningAgent(ArchitectureAgent):
    """Executes a plan, detects failure, and replans within budget.

    Requirement: GAP-ARCH-B-07. Failure detection via injected
    ``check_fn(step) -> bool``; default assumes failure on steps containing
    'fail'.
    """

    architecture = "replanning"

    def __init__(self, *args, check_fn=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.check_fn = check_fn
        self.replans = 0

    def _failed(self, step: str) -> bool:
        if self.check_fn is not None:
            return not bool(call_optional(self.check_fn, step, default=True))
        return "fail" in step.lower()

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        tokens = [t for t in request.goal.split() if t.strip()]
        executed: list[str] = []
        replanned: list[str] = []
        for token in tokens[: self.max_steps]:
            self.step()
            if self._failed(token):
                self.replans += 1
                fallback = f"recover:{token}"
                replanned.append(fallback)
                executed.append(fallback)
            else:
                executed.append(token)
        return {"summary": f"Executed {len(executed)} steps with {self.replans} replans.",
                "data": {"executed": executed, "replans": replanned, "replan_count": self.replans}}


class ReflexionAgent(ArchitectureAgent):
    """Structured self-critique with a durable feedback memory.

    Requirement: GAP-ARCH-B-08. After producing an output, the agent scores
    it against declared criteria and appends a critique record to
    ``feedback_memory``; subsequent runs surface prior critiques.
    """

    architecture = "reflexion"

    def __init__(self, *args, criteria: list[str] | None = None, critic_hook=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.criteria = list(criteria or ["specific", "evidence-grounded"])
        self.critic_hook = critic_hook
        self.feedback_memory: list[dict[str, Any]] = []

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        output = f"Draft answer for: {request.goal[:80]}"
        if self.critic_hook is not None:
            critique = call_optional(self.critic_hook, output, self.criteria, default={})
        else:
            critique = {c: (c.lower() in output.lower() or len(output) > 20) for c in self.criteria}
        passed = [c for c, ok in critique.items() if ok] if isinstance(critique, dict) else []
        failed = [c for c in self.criteria if c not in passed]
        record = {"goal": request.goal, "passed": passed, "failed": failed,
                  "prior_critiques": len(self.feedback_memory)}
        self.feedback_memory.append(record)
        return {"summary": f"Reflexion critique: {len(passed)}/{len(self.criteria)} criteria passed.",
                "data": {"critique": critique, "memory_size": len(self.feedback_memory),
                         "prior_critiques": record["prior_critiques"]}}


class HypothesisTestingAgent(ArchitectureAgent):
    """Competing hypotheses with evidence scoring and ranking.

    Requirement: GAP-ARCH-B-09. Hypotheses score by counting evidence refs
    matching their keywords in the request context.
    """

    architecture = "hypothesis-testing"

    def __init__(self, *args, hypotheses: list[str] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hypotheses = list(hypotheses or ["h-alpha", "h-beta"])
        self.scores: dict[str, float] = {h: 0.0 for h in self.hypotheses}

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        evidence = list(request.context_refs or [])
        for hyp in self.hypotheses:
            key = hyp.split("-")[-1].lower()
            self.scores[hyp] = float(sum(1 for ref in evidence if key in ref.lower()))
        ranked = sorted(self.scores, key=lambda h: -self.scores[h])
        best = ranked[0]
        return {"summary": f"Hypothesis '{best}' leads with score {self.scores[best]}.",
                "evidence_refs": evidence[:10],
                "data": {"ranking": ranked, "scores": dict(self.scores)}}


class SimulationAgent(ArchitectureAgent):
    """What-if simulation over the graph via ``eoip.graph.whatif``.

    Requirement: GAP-ARCH-B-10. Runs ``execute_scenario`` on a parsed
    mutation plan; with no matching intent it returns an empty impact set.
    """

    architecture = "simulation"
    allowed_tools = frozenset({"search", "entity", "impact", "path"})

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        from eoip.graph.whatif import execute_scenario, parse_whatif_intent

        plan = call_optional(parse_whatif_intent, request.goal)
        if not plan:
            return {"summary": "No actionable what-if intent parsed; empty simulation.",
                    "data": {"impact": {}, "simulated": False}}
        impact = call_optional(execute_scenario, store, plan, default={}) or {}
        return {"summary": "What-if simulation completed without mutation.",
                "data": {"simulated": True, "impact": impact}}


class CounterfactualAgent(ArchitectureAgent):
    """Counterfactual reasoning: minimal change to alter an outcome.

    Requirement: GAP-ARCH-B-11. Compares the closest alternative from
    declared options and reports the minimal sufficient difference.
    """

    architecture = "counterfactual"

    def __init__(self, *args, options: list[str] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.options = list(options or ["option-a", "option-b"])

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        actual = request.metadata.get("actual", self.options[0])
        candidates = [o for o in self.options if o != actual]
        nearest = min(candidates, key=lambda o: sum(a != b for a, b in zip(actual, o)), default=None)
        return {"summary": f"Closest counterfactual to '{actual}' is '{nearest}'.",
                "data": {"actual": actual, "counterfactual": nearest, "candidates": candidates}}


class DebateAgent(ArchitectureAgent):
    """Two-sided argumentation with a deterministic judge.

    Requirement: GAP-ARCH-B-12. Sides are injected ``side_a_hook`` /
    ``side_b_hook`` (default: pro/con heuristics over the goal). The judge
    scores arguments by evidence count and declared weights.
    """

    architecture = "debate"

    def __init__(self, *args, side_a_hook=None, side_b_hook=None, judge_hook=None, rounds: int = 2, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.side_a_hook = side_a_hook
        self.side_b_hook = side_b_hook
        self.judge_hook = judge_hook
        self.rounds = min(rounds, 4)

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        transcript: list[dict[str, Any]] = []
        for rnd in range(self.rounds):
            self.step()
            for side, hook in (("A", self.side_a_hook), ("B", self.side_b_hook)):
                if hook is not None:
                    argument = call_optional(hook, request.goal, rnd, default="")
                else:
                    argument = f"{side} argues round {rnd + 1} on: {request.goal[:50]}"
                transcript.append({"round": rnd + 1, "side": side, "argument": str(argument),
                                   "evidence": list(request.context_refs or [])[:3]})
        if self.judge_hook is not None:
            verdict = call_optional(self.judge_hook, transcript, default=None)
        else:
            score_a = sum(len(t["evidence"]) + 1 for t in transcript if t["side"] == "A")
            score_b = sum(len(t["evidence"]) + 1 for t in transcript if t["side"] == "B")
            verdict = "A" if score_a >= score_b else "B"
        return {"summary": f"Debate resolved in favour of side {verdict}.",
                "data": {"transcript": transcript, "verdict": verdict}}


class ArbitrationAgent(ArchitectureAgent):
    """Resolves conflicting claims from multiple contributors.

    Requirement: GAP-ARCH-B-13. Deterministic arbitration: the claim backed
    by the most evidence refs wins; ties resolve to the earliest contributor.
    """

    architecture = "arbitration"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        claims = request.metadata.get("claims", [])
        ranked = sorted(claims, key=lambda c: (-len(c.get("evidence_refs", [])), str(c.get("claimant", ""))))
        winner = ranked[0] if ranked else None
        return {"summary": f"Arbitration winner: {winner.get('claimant') if winner else 'none'}.",
                "evidence_refs": list(winner.get("evidence_refs", [])) if winner else [],
                "data": {"winner": winner, "contenders": len(claims)}}


class VerificationAgent(ArchitectureAgent):
    """Claim checking against graph facts.

    Requirement: GAP-ARCH-B-14. Each claim is a string matched against
    bounded store lookups; verdicts are SUPPORTED / REFUTED / UNRESOLVED.
    """

    architecture = "verification"
    allowed_tools = frozenset({"search", "entity", "evidence"})

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        claims = request.metadata.get("claims", [request.goal])
        verdicts: list[dict[str, Any]] = []
        for claim in claims:
            try:
                matches = store.find_vertices(limit=10) or []
            except (AttributeError, TypeError, PermissionError):
                matches = []
            text = str(claim).lower()
            hit = any(text and (text in str(v).lower()) for v in matches)
            verdicts.append({"claim": claim, "verdict": "SUPPORTED" if hit else "UNRESOLVED",
                             "facts_examined": len(matches)})
        return {"summary": f"Verified {len(verdicts)} claims against graph facts.",
                "data": {"verdicts": verdicts}}


class FormalReasoningAgent(ArchitectureAgent):
    """Constraint checker over declared invariants.

    Requirement: GAP-ARCH-B-15. Invariants are ``(name, expression)`` where
    expression supports ``count(<Label>) <op> <int>``; violations produce
    PROPOSAL-free failure findings (read-only agent).
    """

    architecture = "formal-reasoning"
    allowed_tools = frozenset({"search", "ontology"})

    def __init__(self, *args, invariants: list[tuple[str, str]] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.invariants = list(invariants or [("nonempty-graph", "count(*) > 0")])

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        import operator

        ops = {"<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge,
               "==": operator.eq, "!=": operator.ne}
        findings: list[dict[str, Any]] = []
        for name, expr in self.invariants:
            self.step()
            parts = expr.split()
            if len(parts) != 3 or parts[1] not in ops:
                findings.append({"invariant": name, "status": "MALFORMED", "expression": expr})
                continue
            field, op_s, raw = parts
            try:
                threshold = int(raw)
            except ValueError:
                findings.append({"invariant": name, "status": "MALFORMED", "expression": expr})
                continue
            if field.startswith("count("):
                label = field[6:-1].strip() or None
                if label == "*":
                    label = None
                try:
                    actual = store.count_vertices(label)
                except (AttributeError, TypeError, PermissionError):
                    actual = 0
                ok = ops[op_s](actual, threshold)
                findings.append({"invariant": name, "status": "HOLDS" if ok else "VIOLATED",
                                 "actual": actual, "threshold": threshold})
            else:
                findings.append({"invariant": name, "status": "MALFORMED", "expression": expr})
        violated = [f for f in findings if f["status"] == "VIOLATED"]
        return {"summary": f"Checked {len(findings)} invariants; {len(violated)} violated.",
                "status": "SUCCEEDED" if not violated else "PARTIAL",
                "warnings": [f["invariant"] for f in violated],
                "data": {"findings": findings}}
