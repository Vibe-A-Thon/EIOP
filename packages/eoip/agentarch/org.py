"""Multi-agent organisational architectures.

Requirement: GAP-ARCH-D. Each pattern is a coordinator class that drives
2+ participant agents through a ``Runner`` (by default the governed
``AgentRuntime``; tests may inject stub runners). Coordinators reuse
``eoip.agents.runtime`` budgets semantics: every child invocation is a
bounded ``AgentRequest`` and the fan-out respects ``max_steps``.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, Protocol

from eoip.contracts.agent import AgentRequest, AgentResult


def _ok(result: AgentResult) -> bool:
    return result.status in {"SUCCEEDED", "PARTIAL"}


class Runner(Protocol):
    """How a coordinator invokes one child agent."""

    def run(self, agent_id: str, goal: str, *, metadata: dict | None = None) -> AgentResult: ...


class RuntimeRunner:
    """Default runner over the governed ``AgentRuntime``."""

    def __init__(self, runtime, *, actor_id: str = "coordinator", correlation_id: str = "coord",
                 budgets: dict | None = None) -> None:
        self._runtime = runtime
        self._actor_id = actor_id
        self._correlation_id = correlation_id
        self._budgets = budgets or {"max_seconds": 15}
        self._counter = 0

    def run(self, agent_id: str, goal: str, *, metadata: dict | None = None) -> AgentResult:
        self._counter += 1
        return self._runtime.run(AgentRequest(
            request_id=f"coord:{self._correlation_id}:{self._counter}",
            agent_id=agent_id, goal=goal, actor_id=self._actor_id,
            correlation_id=self._correlation_id, recursion_depth=1,
            budgets=dict(self._budgets), metadata=metadata or {},
        ))


class Coordinator:
    """Base coordinator: holds participants + runner and fans out bounded."""

    pattern: str = "base"

    def __init__(self, participants: list[str], runner: Runner, *, max_steps: int = 12) -> None:
        if not participants:
            raise ValueError("Coordinator requires at least one participant")
        self.participants = list(participants)
        self.runner = runner
        self.max_steps = max_steps

    def _invoke(self, agent_id: str, goal: str, metadata: dict | None = None) -> AgentResult:
        return self.runner.run(agent_id, goal, metadata=metadata)

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        raise NotImplementedError


class SupervisorWorker(Coordinator):
    """Supervisor decomposes the goal and dispatches subtasks to workers.

    Requirement: GAP-ARCH-D-01.
    """

    pattern = "supervisor-worker"

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        subtasks = [t for t in goal.split(";") if t.strip()] or [goal]
        results: list[AgentResult] = []
        for index, subtask in enumerate(subtasks[: self.max_steps]):
            worker = self.participants[index % len(self.participants)]
            result = self._invoke(worker, subtask.strip(), metadata=metadata)
            results.append(result)
            if not _ok(result):
                break
        return {"pattern": self.pattern, "status": "SUCCEEDED" if all(_ok(r) for r in results) else "PARTIAL",
                "assignments": [{"worker": self.participants[i % len(self.participants)],
                                 "subtask": (subtasks[i].strip() if i < len(subtasks) else goal)}
                                for i in range(len(results))],
                "child_results": results}


class ManagerSpecialist(Coordinator):
    """Manager routes each subtask to the specialist with the best declared fit.

    Requirement: GAP-ARCH-D-02. Fit scores come from injected
    ``specialist_profiles: {agent_id: [keywords]}``.
    """

    pattern = "manager-specialist"

    def __init__(self, participants, runner, *, specialist_profiles: dict[str, list[str]] | None = None, **kw) -> None:
        super().__init__(participants, runner, **kw)
        self.specialist_profiles = dict(specialist_profiles or {})

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        subtasks = [t.strip() for t in goal.split(";") if t.strip()] or [goal]
        results: list[AgentResult] = []
        for subtask in subtasks[: self.max_steps]:
            best, best_score = self.participants[0], -1
            for agent_id in self.participants:
                keywords = self.specialist_profiles.get(agent_id, [])
                score = sum(1 for k in keywords if k.lower() in subtask.lower())
                if score > best_score:
                    best, best_score = agent_id, score
            results.append(self._invoke(best, subtask, metadata=metadata))
        return {"pattern": self.pattern,
                "status": "SUCCEEDED" if all(_ok(r) for r in results) else "PARTIAL",
                "child_results": results}


class LeaderFollower(Coordinator):
    """Leader executes; followers replicate/check the leader's result.

    Requirement: GAP-ARCH-D-03.
    """

    pattern = "leader-follower"

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        leader = self.participants[0]
        followers = self.participants[1:]
        leader_result = self._invoke(leader, goal, metadata=metadata)
        follower_results = [self._invoke(f, f"verify: {goal}", metadata=metadata)
                            for f in followers[: self.max_steps - 1]]
        return {"pattern": self.pattern, "leader": leader,
                "leader_result": leader_result, "follower_results": follower_results,
                "status": "SUCCEEDED" if _ok(leader_result) else "FAILED"}


class Blackboard(Coordinator):
    """Shared-state store; agents read/update it in turns.

    Requirement: GAP-ARCH-D-04.
    """

    pattern = "blackboard"

    def __init__(self, participants, runner, **kw) -> None:
        super().__init__(participants, runner, **kw)
        self.state: dict[str, Any] = {}

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        results: list[AgentResult] = []
        for agent_id in self.participants[: self.max_steps]:
            merged = {**(metadata or {}), "blackboard": dict(self.state)}
            result = self._invoke(agent_id, goal, metadata=merged)
            results.append(result)
            self.state[agent_id] = result.summary
        return {"pattern": self.pattern, "blackboard": dict(self.state),
                "status": "SUCCEEDED" if all(_ok(r) for r in results) else "PARTIAL",
                "child_results": results}


class HierarchicalTeams(Coordinator):
    """Tree: a root coordinator delegates to team leads, each to members.

    Requirement: GAP-ARCH-D-05. ``teams: {lead: [members]}``.
    """

    pattern = "hierarchical-teams"

    def __init__(self, participants, runner, *, teams: dict[str, list[str]] | None = None, **kw) -> None:
        super().__init__(participants, runner, **kw)
        self.teams = dict(teams or {})

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        results: list[AgentResult] = []
        leads = [p for p in self.participants if p in self.teams] or self.participants[:1]
        budget = self.max_steps
        for lead in leads:
            if budget <= 0:
                break
            results.append(self._invoke(lead, goal, metadata=metadata))
            budget -= 1
            for member in self.teams.get(lead, [])[:budget]:
                results.append(self._invoke(member, f"{goal} (via {lead})", metadata=metadata))
                budget -= 1
        return {"pattern": self.pattern, "teams": {k: list(v) for k, v in self.teams.items()},
                "status": "SUCCEEDED" if all(_ok(r) for r in results) else "PARTIAL",
                "child_results": results}


class FederatedArchitecture(Coordinator):
    """Federated participants under a shared policy boundary.

    Requirement: GAP-ARCH-D-06. Each participant declares a policy tier;
    requests crossing a tier boundary are denied before invocation.
    """

    pattern = "federated"

    def __init__(self, participants, runner, *, policy_tiers: dict[str, int] | None = None, **kw) -> None:
        super().__init__(participants, runner, **kw)
        self.policy_tiers = dict(policy_tiers or {})

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        request_tier = int((metadata or {}).get("policy_tier", 0))
        allowed = [p for p in self.participants if self.policy_tiers.get(p, 0) <= request_tier]
        results = [self._invoke(p, goal, metadata=metadata) for p in allowed[: self.max_steps]]
        denied = sorted(set(self.participants) - set(allowed))
        return {"pattern": self.pattern, "invoked": allowed, "denied_by_policy": denied,
                "status": "SUCCEEDED" if len(results) == len(self.participants) else "PARTIAL",
                "child_results": results}


class MarketBased(Coordinator):
    """Bidding market: participants bid; lowest bidder wins the task.

    Requirement: GAP-ARCH-D-07. Bids come from injected ``bid_hook(agent_id)
    -> float`` or a deterministic per-agent constant.
    """

    pattern = "market-based"

    def __init__(self, participants, runner, *, bid_hook=None, **kw) -> None:
        super().__init__(participants, runner, **kw)
        self.bid_hook = bid_hook

    def _bid(self, agent_id: str, goal: str) -> float:
        if self.bid_hook is not None:
            try:
                return float(self.bid_hook(agent_id))
            except Exception:
                pass
        return float(abs(hash((agent_id, goal))) % 100) / 10.0

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        bids = {p: self._bid(p, goal) for p in self.participants}
        winner = min(bids, key=bids.get)
        result = self._invoke(winner, goal, metadata=metadata)
        return {"pattern": self.pattern, "bids": bids, "winner": winner, "award_result": result,
                "status": "SUCCEEDED" if _ok(result) else "FAILED"}


class ContractNet(Coordinator):
    """FIPA Contract-Net: announce, collect bids, award to best bid.

    Requirement: GAP-ARCH-D-08.
    """

    pattern = "contract-net"

    def __init__(self, participants, runner, *, bid_hook=None, **kw) -> None:
        super().__init__(participants, runner, **kw)
        self.bid_hook = bid_hook

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        announcements = [self._invoke(p, f"CFP: {goal}", metadata=metadata)
                         for p in self.participants[: self.max_steps - 1]]
        bids: dict[str, float] = {}
        for index, agent_id in enumerate(self.participants[: len(announcements)]):
            if self.bid_hook is not None:
                try:
                    bids[agent_id] = float(self.bid_hook(agent_id))
                    continue
                except Exception:
                    pass
            bids[agent_id] = float(len(announcements[index].summary) % 17)
        winner = min(bids, key=bids.get)
        award = self._invoke(winner, f"AWARD: {goal}", metadata=metadata)
        return {"pattern": self.pattern, "announcements": announcements, "bids": bids,
                "winner": winner, "award_result": award,
                "status": "SUCCEEDED" if _ok(award) else "FAILED"}


class NegotiationBased(Coordinator):
    """Iterative negotiation rounds until consensus or round budget.

    Requirement: GAP-ARCH-D-09.
    """

    pattern = "negotiation"

    def __init__(self, participants, runner, *, rounds: int = 3, **kw) -> None:
        super().__init__(participants, runner, **kw)
        self.rounds = min(rounds, 5)

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        offers: dict[str, str] = {}
        history: list[dict[str, str]] = []
        for rnd in range(self.rounds):
            round_offers: dict[str, str] = {}
            for agent_id in self.participants[: max(1, self.max_steps // self.rounds)]:
                result = self._invoke(agent_id, f"negotiate round {rnd + 1}: {goal}",
                                      metadata={**(metadata or {}), "current_offer": offers.get(agent_id)})
                round_offers[agent_id] = result.summary
            history.append(round_offers)
            if len(set(round_offers.values())) == 1 and round_offers:
                offers = round_offers
                break
            offers = round_offers
        consensus = len(set(offers.values())) <= 1
        return {"pattern": self.pattern, "rounds": len(history), "consensus": consensus,
                "final_offers": offers, "status": "SUCCEEDED" if consensus else "PARTIAL"}


class VotingBased(Coordinator):
    """Participants vote; majority (or plurality) wins.

    Requirement: GAP-ARCH-D-10. Votes are child-agent summaries; the most
    common wins. Tie breaks alphabetically (deterministic).
    """

    pattern = "voting"

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        votes: list[str] = []
        for agent_id in self.participants[: self.max_steps]:
            result = self._invoke(agent_id, goal, metadata=metadata)
            votes.append(result.summary)
        tally: dict[str, int] = defaultdict(int)
        for vote in votes:
            tally[vote] += 1
        winner = max(sorted(tally), key=tally.get) if tally else None
        return {"pattern": self.pattern, "tally": dict(tally), "winner": winner,
                "status": "SUCCEEDED" if winner is not None else "FAILED"}


class Ensemble(Coordinator):
    """Runs all participants and merges their outputs deterministically.

    Requirement: GAP-ARCH-D-11.
    """

    pattern = "ensemble"

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        results = [self._invoke(p, goal, metadata=metadata) for p in self.participants[: self.max_steps]]
        merged = sorted({ref for r in results for ref in r.evidence_refs})
        return {"pattern": self.pattern, "child_results": results, "merged_evidence": merged,
                "status": "SUCCEEDED" if all(_ok(r) for r in results) else "PARTIAL"}


class Mesh(Coordinator):
    """Peers exchange messages until the step budget is exhausted.

    Requirement: GAP-ARCH-D-12. Deterministic gossip: each peer forwards its
    accumulated knowledge to the next peer.
    """

    pattern = "mesh"

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        knowledge: dict[str, str] = {}
        exchanges: list[tuple[str, str]] = []
        budget = self.max_steps
        for agent_id in self.participants:
            if budget <= 0:
                break
            result = self._invoke(agent_id, goal, metadata={**(metadata or {}), "knowledge": dict(knowledge)})
            knowledge[agent_id] = result.summary
            budget -= 1
            if len(knowledge) > 1:
                prev = self.participants[self.participants.index(agent_id) - 1]
                exchanges.append((agent_id, prev))
        return {"pattern": self.pattern, "knowledge": knowledge, "exchanges": exchanges,
                "status": "SUCCEEDED"}


class EventDriven(Coordinator):
    """Agents react to queued events through an in-memory event bus.

    Requirement: GAP-ARCH-D-13.
    """

    pattern = "event-driven"

    def __init__(self, participants, runner, **kw) -> None:
        super().__init__(participants, runner, **kw)
        self.queue: deque[str] = deque()

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        self.queue.append(goal)
        handled: list[dict[str, Any]] = []
        steps = 0
        while self.queue and steps < self.max_steps:
            event = self.queue.popleft()
            agent_id = self.participants[steps % len(self.participants)]
            result = self._invoke(agent_id, event, metadata=metadata)
            handled.append({"event": event, "agent_id": agent_id, "status": result.status})
            followups = (metadata or {}).get("followups", [])
            for followup in followups:
                self.queue.append(str(followup))
            steps += 1
        return {"pattern": self.pattern, "handled": handled,
                "status": "SUCCEEDED" if not self.queue else "PARTIAL",
                "warnings": ["event queue not drained"] if self.queue else []}


class Pipeline(Coordinator):
    """Fixed sequence of stages; each agent's output feeds the next.

    Requirement: GAP-ARCH-D-14.
    """

    pattern = "pipeline"

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        stage_outputs: list[dict[str, Any]] = []
        current = goal
        for agent_id in self.participants[: self.max_steps]:
            result = self._invoke(agent_id, current, metadata=metadata)
            stage_outputs.append({"stage": agent_id, "status": result.status, "output": result.summary})
            current = result.summary
            if not _ok(result):
                return {"pattern": self.pattern, "stages": stage_outputs, "status": "FAILED"}
        return {"pattern": self.pattern, "stages": stage_outputs, "final_output": current,
                "status": "SUCCEEDED"}


class HandoffBased(Coordinator):
    """Token-passing: the current holder decides the next holder.

    Requirement: GAP-ARCH-D-15. Deterministic default: round-robin handoff.
    An injected ``next_fn(current, results)`` may decide (External gate when
    model-backed).
    """

    pattern = "handoff"

    def __init__(self, participants, runner, *, next_fn=None, **kw) -> None:
        super().__init__(participants, runner, **kw)
        self.next_fn = next_fn

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        order: list[str] = []
        results: list[AgentResult] = []
        current = self.participants[0]
        for _ in range(self.max_steps):
            result = self._invoke(current, goal if not order else f"continue: {goal}",
                                  metadata=metadata)
            order.append(current)
            results.append(result)
            if self.next_fn is not None:
                try:
                    nxt = self.next_fn(current, results)
                except Exception:
                    nxt = None
                if nxt in self.participants:
                    current = nxt
                    continue
            idx = (self.participants.index(current) + 1) % len(self.participants)
            if self.participants[idx] in order:
                break
            current = self.participants[idx]
        return {"pattern": self.pattern, "handoff_order": order,
                "status": "SUCCEEDED" if all(_ok(r) for r in results) else "PARTIAL",
                "child_results": results}


class MixtureOfAgents(Coordinator):
    """Layered mixture: proposers generate, aggregators synthesize, judge scores.

    Requirement: GAP-ARCH-D-16.
    """

    pattern = "mixture-of-agents"

    def coordinate(self, goal: str, *, metadata: dict | None = None) -> dict[str, Any]:
        proposers = self.participants[: max(1, len(self.participants) - 1)] or self.participants
        judge = self.participants[-1]
        proposals = [self._invoke(p, f"propose: {goal}", metadata=metadata)
                     for p in proposers[: self.max_steps - 1]]
        synthesized = "\n".join(sorted(p.summary for p in proposals))
        verdict = self._invoke(judge, f"judge: {synthesized}", metadata=metadata)
        return {"pattern": self.pattern, "proposals": proposals, "verdict": verdict,
                "status": "SUCCEEDED" if _ok(verdict) else "PARTIAL"}


PATTERNS: dict[str, type[Coordinator]] = {
    cls.pattern: cls
    for cls in (
        SupervisorWorker, ManagerSpecialist, LeaderFollower, Blackboard,
        HierarchicalTeams, FederatedArchitecture, MarketBased, ContractNet,
        NegotiationBased, VotingBased, Ensemble, Mesh, EventDriven, Pipeline,
        HandoffBased, MixtureOfAgents,
    )
}
