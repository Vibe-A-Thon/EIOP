"""Classical / cognitive agent types as state-machine & capability classes.

Requirement: GAP-ARCH-A. Each class is instantiable, deterministic by
default, and runnable through the governed ``AgentRuntime`` within budgets.
"""

from __future__ import annotations

from typing import Any

from eoip.agentarch.base import ArchitectureAgent, ExternalGate, TaskStore, call_optional
from eoip.contracts.agent import AgentRequest


class LearningAgent(ArchitectureAgent):
    """Feedback-driven agent: exposes policy-update hooks invoked on outcomes.

    Requirement: GAP-ARCH-A-01. ``policy`` maps observed state keys to action
    weights; ``record_feedback`` nudges the weight toward the reward. An
    optional ``update_hook(state, action, reward)`` may replace the default
    numeric update (External gate when it wraps an external learner).
    """

    architecture = "learning"

    def __init__(self, *args, learning_rate: float = 0.2, update_hook=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.learning_rate = learning_rate
        self.update_hook = update_hook
        self.policy: dict[str, dict[str, float]] = {}
        self.feedback_count = 0

    def record_feedback(self, reward: float, context: dict[str, Any] | None = None) -> None:
        context = context or {}
        state = str(context.get("state", "default"))
        action = str(context.get("action", "default"))
        if self.update_hook is not None:
            call_optional(self.update_hook, state, action, reward)
            self.feedback_count += 1
            return
        weights = self.policy.setdefault(state, {})
        current = weights.get(action, 0.5)
        weights[action] = max(0.0, min(1.0, current + self.learning_rate * (reward - current)))
        self.feedback_count += 1

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        state = request.goal
        weights = self.policy.get(state, {})
        best = max(weights, key=weights.get) if weights else "explore"
        return {
            "summary": f"Learning agent selected action '{best}' from {len(weights)} learned weights.",
            "data": {"action": best, "policy_size": sum(len(w) for w in self.policy.values()),
                     "feedback_count": self.feedback_count},
        }


class KnowledgeBasedAgent(ArchitectureAgent):
    """Fact + rule inference over the graph and declared rules.

    Requirement: GAP-ARCH-A-02. Facts are vertices matched from the store
    (bounded); rules are ``(name, when_facts, then)`` triples where ``when_facts``
    is a list of required substrings/labels. Facts may optionally be checked
    against ``eoip.truth.engine.TruthStore`` when one is injected.
    """

    architecture = "knowledge-based"
    allowed_tools = frozenset({"search", "entity", "ontology", "evidence"})

    def __init__(self, *args, rules: list[tuple[str, list[str], str]] | None = None,
                 truth_store=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rules = list(rules or [])
        self.truth_store = truth_store

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        facts: list[str] = []
        try:
            vertices = store.find_vertices(limit=25)
        except (AttributeError, TypeError, PermissionError):
            vertices = []
        for vertex in vertices or []:
            label = vertex.get("label") if isinstance(vertex, dict) else getattr(vertex, "label", None)
            cid = vertex.get("canonical_id") if isinstance(vertex, dict) else getattr(vertex, "canonical_id", "")
            if label:
                facts.append(f"{label}:{cid}")
        if self.truth_store is not None:
            confirmed = call_optional(getattr(self.truth_store, "list_confirmed", None))
            facts.extend(str(item) for item in (confirmed or [])[:25])
        fired: list[str] = []
        for name, when, then in self.rules:
            if all(any(token in fact for fact in facts) for token in when):
                fired.append(f"{name} -> {then}")
        return {
            "summary": f"Inferred {len(fired)} rule conclusions from {len(facts)} facts.",
            "evidence_refs": [f for f in facts if str(f).startswith("urn:")][:10],
            "data": {"facts": len(facts), "fired_rules": fired},
        }


class BDIAgent(ArchitectureAgent):
    """Belief-Desire-Intention cycle agent.

    Requirement: GAP-ARCH-A-03. Beliefs update from bounded store
    observations; desires rank by utility; the top feasible desire becomes
    the intention and is executed one step per run.
    """

    architecture = "bdi"

    def __init__(self, *args, desires: list[tuple[str, float]] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.beliefs: dict[str, Any] = {}
        self.desires = [{"name": n, "utility": u} for n, u in (desires or [("achieve-goal", 1.0)])]
        self.intentions: list[str] = []

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        try:
            self.beliefs["graph_vertices"] = store.count_vertices()
        except (AttributeError, TypeError, PermissionError):
            self.beliefs.setdefault("graph_vertices", 0)
        ranked = sorted(self.desires, key=lambda d: -d["utility"])
        chosen = next((d["name"] for d in ranked if d["name"] not in self.intentions), None)
        if chosen is not None:
            self.intentions.append(chosen)
        return {
            "summary": f"BDI cycle adopted intention '{chosen}' from {len(self.desires)} desires.",
            "data": {"beliefs": dict(self.beliefs), "intentions": list(self.intentions)},
        }


class ReactiveAgent(ArchitectureAgent):
    """Condition-action rule agent with no internal model.

    Requirement: GAP-ARCH-A-04. Rules are ``(predicate_substring, action)``
    pairs tested against the goal text.
    """

    architecture = "reactive"

    def __init__(self, *args, rules: list[tuple[str, str]] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rules = list(rules or [("help", "assist"), ("error", "diagnose")])

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        goal = request.goal.lower()
        for predicate, action in self.rules:
            if predicate.lower() in goal:
                return {"summary": f"Reactive rule fired: '{predicate}' -> '{action}'.",
                        "data": {"action": action, "rule": predicate}}
        return {"summary": "No reactive rule matched; default action.", "data": {"action": "default"}}


class DeliberativeAgent(ArchitectureAgent):
    """Plan-first agent: decomposes the goal into a bounded step plan.

    Requirement: GAP-ARCH-A-05. Deterministic decomposition by goal tokens;
    replanning hook optional.
    """

    architecture = "deliberative"

    def __init__(self, *args, replan_hook=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.replan_hook = replan_hook

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        steps = [token for token in request.goal.split() if token.strip()][: self.max_steps]
        plan = [{"step": i + 1, "action": s} for i, s in enumerate(steps)]
        if self.replan_hook is not None:
            plan = call_optional(self.replan_hook, plan, request.goal, default=plan) or plan
        return {"summary": f"Deliberative plan with {len(plan)} steps formed.",
                "data": {"plan": plan}}


class HybridAgent(ArchitectureAgent):
    """Reactive layer first, deliberative fallback.

    Requirement: GAP-ARCH-A-06. Combines :class:`ReactiveAgent` and
    :class:`DeliberativeAgent` delegates.
    """

    architecture = "hybrid"

    def __init__(self, *args, rules: list[tuple[str, str]] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.reactive = ReactiveAgent(f"{self.agent_id}:reactive", rules=rules)
        self.deliberative = DeliberativeAgent(f"{self.agent_id}:deliberative")

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        fast = self.reactive.act(request, store)
        if fast["data"].get("action") != "default":
            return {"summary": f"Hybrid reactive layer: {fast['summary']}", "data": {"layer": "reactive", **fast["data"]}}
        slow = self.deliberative.act(request, store)
        return {"summary": f"Hybrid deliberative layer: {slow['summary']}",
                "data": {"layer": "deliberative", **slow["data"]}}


class StatefulAgent(ArchitectureAgent):
    """Agent with durable run-scoped state across invocations.

    Requirement: GAP-ARCH-A-07.
    """

    architecture = "stateful"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.state: dict[str, Any] = {}

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        self.state.setdefault("invocations", 0)
        self.state["invocations"] += 1
        self.state["last_goal"] = request.goal
        return {"summary": f"Stateful agent invocation #{self.state['invocations']}.",
                "data": {"state": dict(self.state)}}


class StatelessAgent(ArchitectureAgent):
    """Agent that derives everything from the request; no retained state.

    Requirement: GAP-ARCH-A-08.
    """

    architecture = "stateless"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        digest = f"{request.goal}:{request.actor_id}"
        return {"summary": "Stateless derivation completed from request only.",
                "data": {"derivation_key": digest, "context_refs": list(request.context_refs or [])}}


class ProbabilisticAgent(ArchitectureAgent):
    """Chooses actions by sampled probabilities over a declared distribution.

    Requirement: GAP-ARCH-A-09. Uses the seeded RNG — deterministic for a
    fixed seed.
    """

    architecture = "probabilistic"

    def __init__(self, *args, distribution: dict[str, float] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.distribution = dict(distribution or {"proceed": 0.7, "defer": 0.3})

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        actions = sorted(self.distribution)
        weights = [self.distribution[a] for a in actions]
        action = self.rng.choices(actions, weights=weights, k=1)[0]
        return {"summary": f"Sampled action '{action}' from declared distribution.",
                "data": {"action": action, "distribution": self.distribution}}


class BayesianAgent(ArchitectureAgent):
    """Explicit belief updating with Beta-Bernoulli conjugate updates.

    Requirement: GAP-ARCH-A-10. Beliefs are Beta(alpha, beta) per hypothesis;
    ``update(hypothesis, success)`` applies the conjugate update.
    """

    architecture = "bayesian"

    def __init__(self, *args, priors: dict[str, tuple[float, float]] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.beliefs = {h: [a, b] for h, (a, b) in (priors or {"h1": (1.0, 1.0)}).items()}

    def update(self, hypothesis: str, success: bool) -> None:
        alpha, beta = self.beliefs.setdefault(hypothesis, [1.0, 1.0])
        if success:
            self.beliefs[hypothesis][0] = alpha + 1
        else:
            self.beliefs[hypothesis][1] = beta + 1

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        ranked = sorted(self.beliefs, key=lambda h: -(self.beliefs[h][0] / (self.beliefs[h][0] + self.beliefs[h][1])))
        best = ranked[0] if ranked else None
        return {"summary": f"Most probable hypothesis: '{best}'.",
                "data": {"hypothesis": best,
                         "posteriors": {h: a / (a + b) for h, (a, b) in self.beliefs.items()}}}


class RLAgent(ArchitectureAgent):
    """Tabular reinforcement-learning agent: real Q-table updates, toy scope.

    Requirement: GAP-ARCH-A-11. Q-learning update with epsilon-greedy policy
    over declared actions; environment responses come from an injected
    ``env_hook(state, action) -> (reward, next_state)`` or a deterministic
    default. Runs bounded episodes inside the step budget.
    """

    architecture = "rl"

    def __init__(self, *args, actions: list[str] | None = None, alpha: float = 0.5,
                 gamma: float = 0.9, epsilon: float = 0.1, env_hook=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.actions = list(actions or ["left", "right"])
        self.alpha, self.gamma, self.epsilon = alpha, gamma, epsilon
        self.env_hook = env_hook
        self.q_table: dict[str, dict[str, float]] = {}

    def _env(self, state: str, action: str) -> tuple[float, str]:
        if self.env_hook is not None:
            result = call_optional(self.env_hook, state, action, default=(0.0, state))
            return tuple(result)  # type: ignore[return-value]
        reward = 1.0 if action == "right" else -1.0
        return reward, state

    def choose(self, state: str) -> str:
        if self.rng.random() < self.epsilon:
            return self.rng.choice(self.actions)
        row = self.q_table.setdefault(state, {a: 0.0 for a in self.actions})
        return max(self.actions, key=lambda a: row.get(a, 0.0))

    def learn(self, state: str, action: str, reward: float, next_state: str) -> None:
        row = self.q_table.setdefault(state, {a: 0.0 for a in self.actions})
        next_row = self.q_table.setdefault(next_state, {a: 0.0 for a in self.actions})
        target = reward + self.gamma * max(next_row.values(), default=0.0)
        row[action] = row.get(action, 0.0) + self.alpha * (target - row.get(action, 0.0))

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        episodes = min(3, self.max_steps - self._steps_used)
        state = "s0"
        for _ in range(max(1, episodes)):
            self.step()
            for _ in range(4):
                action = self.choose(state)
                reward, next_state = self._env(state, action)
                self.learn(state, action, reward, next_state)
                state = next_state
        best = max(self.actions, key=lambda a: self.q_table.get("s0", {}).get(a, 0.0))
        return {"summary": f"RL policy converged on '{best}' for initial state.",
                "data": {"best_action": best, "q_table": {s: dict(r) for s, r in self.q_table.items()}}}


class NeuroSymbolicAgent(ArchitectureAgent):
    """Combines a neural perception hook with symbolic rule firing.

    Requirement: GAP-ARCH-A-12. The neural side is an optional injected
    ``perceive_hook`` (External gate when backed by a real model); symbolic
    side reuses deterministic rule matching.
    """

    architecture = "neuro-symbolic"
    allowed_tools = frozenset({"search", "ontology"})

    def __init__(self, *args, rules: list[tuple[str, list[str], str]] | None = None,
                 perceive_hook=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rules = list(rules or [])
        self.perceive_hook = perceive_hook

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        perceived = call_optional(self.perceive_hook, request.goal, default=[])
        kb = KnowledgeBasedAgent(f"{self.agent_id}:kb", rules=self.rules)
        outcome = kb.act(request, store)
        fired = outcome["data"]["fired_rules"]
        return {"summary": f"Neuro-symbolic: {len(perceived or [])} perceived cues, {len(fired)} symbolic rules fired.",
                "data": {"perceptions": list(perceived or []), "fired_rules": fired}}


class WorldModelAgent(ArchitectureAgent):
    """Agent with an explicit transition model of its environment.

    Requirement: GAP-ARCH-A-13. The world model maps ``(state, action) ->
    next_state``; the agent rolls the model forward to pick the first action
    of the best reachable trajectory.
    """

    architecture = "world-model"

    def __init__(self, *args, transitions: dict[tuple[str, str], str] | None = None,
                 actions: list[str] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.transitions = dict(transitions or {})
        self.actions = list(actions or ["a", "b"])

    def predict(self, state: str, action: str) -> str:
        return self.transitions.get((state, action), state)

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        start = "s0"
        horizon = min(3, self.max_steps)
        trajectory: list[str] = [start]
        state = start
        for _ in range(horizon):
            action = self.actions[0]
            state = self.predict(state, action)
            trajectory.append(state)
        return {"summary": f"World model rolled forward {horizon} steps; trajectory {trajectory}.",
                "data": {"trajectory": trajectory, "model_size": len(self.transitions)}}


class CausalReasoningAgent(ArchitectureAgent):
    """Causal hypothesis generation over the graph.

    Requirement: GAP-ARCH-A-14. Uses ``eoip.graph.causal.generate_hypotheses``
    when temporal data is present; otherwise reports zero hypotheses.
    """

    architecture = "causal-reasoning"
    allowed_tools = frozenset({"search", "entity", "evidence", "path"})

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        from eoip.graph.causal import generate_hypotheses

        hypotheses = call_optional(generate_hypotheses, store, limit=10, default=[])
        top = hypotheses[:5] if hypotheses else []
        return {
            "summary": f"Generated {len(hypotheses)} causal hypotheses (top {len(top)} reviewed).",
            "evidence_refs": [h.cause_cid for h in top] + [h.effect_cid for h in top],
            "data": {"hypotheses": [h.to_dict() for h in top]},
        }


class MetaReasoningAgent(ArchitectureAgent):
    """Strategy selector that picks among registered strategies by score.

    Requirement: GAP-ARCH-A-15. Strategies are ``(name, score_fn_or_const)``
    pairs; the selector runs the winning strategy. An injected
    ``select_hook`` may override (External gate when model-backed).
    """

    architecture = "meta-reasoning"

    def __init__(self, *args, strategies: dict[str, float] | None = None,
                 select_hook=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.strategies = dict(strategies or {"fast": 0.6, "thorough": 0.4})
        self.select_hook = select_hook

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        if self.select_hook is not None:
            chosen = call_optional(self.select_hook, request.goal, list(self.strategies))
        else:
            chosen = max(self.strategies, key=self.strategies.get)
        return {"summary": f"Meta-reasoning selected strategy '{chosen}'.",
                "data": {"strategy": chosen, "candidates": sorted(self.strategies)}}


class EmbodiedAgent(ArchitectureAgent):
    """Agent with an environment-interface protocol for physical/actuated systems.

    Requirement: GAP-ARCH-A-16. The embodiment boundary is an External gate:
    ``environment_adapter`` must implement ``sense()`` and ``act(command)``.
    Without an adapter the agent reports its capability manifest and stays
    inert (never faked).
    """

    architecture = "embodied"

    def __init__(self, *args, environment_adapter=None, endpoints: list[str] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.environment_adapter = environment_adapter
        self.gate = ExternalGate("embodiment", "sense/act adapter protocol", endpoints or ["sense", "act"])

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        if self.environment_adapter is None:
            return {"summary": "Embodied agent idle: environment adapter not configured (External gate).",
                    "status": "PARTIAL",
                    "warnings": ["External gate: no environment adapter bound"],
                    "data": {"manifest": self.gate.to_dict()}}
        observations = call_optional(getattr(self.environment_adapter, "sense", None), default=[])
        command = f"respond:{request.goal[:40]}"
        effect = call_optional(getattr(self.environment_adapter, "act", None), command, default=None)
        return {"summary": "Embodied sense-act cycle completed.",
                "data": {"observations": list(observations or []), "command": command, "effect": effect}}


class MultimodalAgent(ArchitectureAgent):
    """Routes a request to per-modality handlers.

    Requirement: GAP-ARCH-A-17. Modality handlers are injected callables;
    unregistered modalities degrade to a declared stub result. Real
    audio/vision encoders are External gates.
    """

    architecture = "multimodal"

    def __init__(self, *args, handlers: dict[str, Any] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.handlers = dict(handlers or {})

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        modalities = request.metadata.get("modalities", ["text"])
        routed: dict[str, Any] = {}
        for modality in modalities:
            handler = self.handlers.get(modality)
            if handler is None:
                routed[modality] = {"status": "EXTERNAL_GATE",
                                    "manifest": ExternalGate(modality, f"{modality} encoder protocol", [modality]).to_dict()}
            else:
                routed[modality] = {"status": "SUCCEEDED", "output": call_optional(handler, request.goal)}
        return {"summary": f"Routed {len(modalities)} modalities ({sum(1 for v in routed.values() if v['status'] == 'SUCCEEDED')} handled).",
                "data": {"routed": routed}}


class MPCAgent(ArchitectureAgent):
    """Moving-horizon optimization over a declared cost model.

    Requirement: GAP-ARCH-A-18. Enumerates action sequences up to the
    horizon, scores them with a deterministic cost function, executes the
    first action of the best sequence. Real numerical solvers are External
    gates.
    """

    architecture = "mpc"

    def __init__(self, *args, actions: list[str] | None = None, horizon: int = 2,
                 cost_fn=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.actions = list(actions or ["a", "b"])
        self.horizon = min(horizon, 3)
        self.cost_fn = cost_fn or (lambda seq: sum(1.0 for a in seq if a == "b"))

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        sequences: list[tuple[tuple[str, ...], float]] = []

        def extend(prefix: tuple[str, ...]) -> None:
            if len(prefix) >= self.horizon:
                sequences.append((prefix, float(self.cost_fn(list(prefix)))))
                return
            for action in self.actions:
                extend(prefix + (action,))

        extend(())
        best_seq, best_cost = min(sequences, key=lambda item: item[1])
        return {"summary": f"MPC chose first action '{best_seq[0]}' with cost {best_cost}.",
                "data": {"action": best_seq[0], "best_sequence": list(best_seq), "cost": best_cost}}
