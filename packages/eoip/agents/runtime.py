"""Agent runtime: registry, budget enforcement, bounded plan/execute/observe/evaluate.

Agents return decision summaries and evidence, never hidden chain-of-thought.
Write/destructive tools are not registered in the MVP.
"""

from __future__ import annotations

import logging
from time import monotonic
from typing import Protocol
from uuid import uuid4

from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.contracts.audit import AuditEvent
from eoip.contracts.source_event import utc_now_iso
from eoip.graph.store import GraphStore

log = logging.getLogger("eoip.agents")

READ_TOOLS = frozenset({"search", "entity", "path", "impact", "lineage"})


class Agent(Protocol):
    agent_id: str
    allowed_tools: frozenset[str]
    max_steps: int
    max_seconds: float

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult: ...


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        if not agent.allowed_tools.issubset(READ_TOOLS):
            forbidden = agent.allowed_tools - READ_TOOLS
            raise ValueError(f"Agent registers non-read tools: {sorted(forbidden)}")
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Agent | None:
        return self._agents.get(agent_id)

    def list_agents(self) -> list[str]:
        return sorted(self._agents)


class AgentRuntime:
    def __init__(self, store: GraphStore, registry: AgentRegistry) -> None:
        self._store = store
        self._registry = registry

    def run(self, request: AgentRequest) -> AgentResult:
        agent = self._registry.get(request.agent_id)
        if agent is None:
            return AgentResult(
                request_id=request.request_id,
                status="DENIED",
                summary=f"Unknown agent: {request.agent_id}",
                evidence_refs=[],
                warnings=[f"No agent registered with id '{request.agent_id}'"],
            )

        budgets = request.budgets or {}
        max_seconds = min(
            budgets.get("max_seconds", agent.max_seconds),
            agent.max_seconds,
        )

        start = monotonic()
        try:
            result = agent.execute(request, self._store)
        except Exception as exc:
            elapsed = monotonic() - start
            log.error(
                "agent.failed",
                extra={
                    "event": "agent.failed",
                    "agent_id": request.agent_id,
                    "request_id": request.request_id,
                    "elapsed_seconds": round(elapsed, 3),
                    "error_type": type(exc).__name__,
                },
            )
            return AgentResult(
                request_id=request.request_id,
                status="FAILED",
                summary=f"Agent execution failed: {type(exc).__name__}",
                evidence_refs=[],
                warnings=[str(exc)],
            )

        elapsed = monotonic() - start
        if elapsed > max_seconds:
            result = result.model_copy(
                update={
                    "status": "PARTIAL",
                    "warnings": (result.warnings or []) + ["Execution exceeded time budget"],
                }
            )

        self._persist_run(request, result, elapsed)
        return result

    def _persist_run(self, request: AgentRequest, result: AgentResult, elapsed: float) -> None:
        try:
            self._store.upsert_vertex(
                "AgentRun",
                {
                    "canonical_id": f"urn:eoip:agent:run:{request.request_id}",
                    "agent_id": request.agent_id,
                    "goal": request.goal,
                    "run_status": result.status,
                    "started_at": utc_now_iso(),
                    "finished_at": utc_now_iso(),
                    "budgets": str({"elapsed": round(elapsed, 3)}),
                },
            )
        except Exception:
            pass
