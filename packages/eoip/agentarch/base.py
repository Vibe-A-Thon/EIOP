"""Shared base machinery for agent-architecture capability classes (GAP-ARCH-BASE).

Every architecture class in this package is a state-machine / capability
class implementing the ``eoip.agents.runtime.Agent`` protocol, so instances
can be registered in an ``AgentRegistry`` and executed through the governed
``AgentRuntime`` (budgets, knowledge firewall, circuit breaker, XAI traces).

Deterministic-first: no class requires an LLM. Optional hooks (policy
updaters, strategy selectors, environment adapters) are plain callables with
graceful fallback when absent. Capabilities that would require real network
protocols or vendor SDKs are exposed as :class:`ExternalGate` manifests and
never faked.
"""

from __future__ import annotations

import random
from typing import Any, Callable, Protocol

from eoip.contracts.agent import AgentRequest, AgentResult

URN_PREFIX = "urn:eoip:agentarch"


class TaskStore(Protocol):
    """Minimal read surface architecture classes rely on (subset of GraphStore)."""

    def find_vertices(self, label: str | None = None, *, limit: int = 100, **kwargs): ...
    def count_vertices(self, label: str | None = None) -> int: ...
    def get_vertex_by_canonical_id(self, canonical_id: str): ...


class ExternalGate:
    """Manifest for a capability that requires an external system.

    Requirement: GAP-ARCH-EXT. Marked 'External gate' deliberately: the
    platform declares the protocol boundary but never simulates the external
    behaviour.
    """

    def __init__(self, name: str, protocol: str, required_endpoints: list[str]) -> None:
        self.name = name
        self.protocol = protocol
        self.required_endpoints = list(required_endpoints)

    def to_dict(self) -> dict[str, Any]:
        return {
            "external_gate": True,
            "name": self.name,
            "protocol": self.protocol,
            "required_endpoints": list(self.required_endpoints),
        }


class ArchitectureAgent:
    """Base class implementing the governed ``Agent`` protocol.

    Subclasses set ``architecture`` and implement :meth:`act`, which returns
    a dict with keys ``summary`` (str), optional ``status``
    (SUCCEEDED/PARTIAL/FAILED), ``data``, ``evidence_refs``, ``warnings``.
    The base wraps it in an ``AgentResult`` and enforces a cooperative step
    budget via :meth:`step`.
    """

    architecture: str = "base"
    allowed_tools: frozenset[str] = frozenset({"search"})
    max_steps: int = 8
    max_seconds: float = 10.0

    def __init__(
        self,
        agent_id: str | None = None,
        *,
        seed: int = 0,
        max_steps: int | None = None,
        max_seconds: float | None = None,
    ) -> None:
        self.agent_id = agent_id or f"{URN_PREFIX}:{self.architecture}"
        if max_steps is not None:
            self.max_steps = max_steps
        if max_seconds is not None:
            self.max_seconds = max_seconds
        self.rng = random.Random(seed)
        self._steps_used = 0

    # -- governed Agent protocol -------------------------------------------

    def execute(self, request: AgentRequest, store: TaskStore) -> AgentResult:
        self._steps_used = 0
        try:
            outcome = self.act(request, store)
        except (PermissionError, RuntimeError, ValueError, TypeError) as exc:
            return AgentResult(
                request_id=request.request_id,
                status="FAILED",
                summary=f"{self.architecture} execution failed: {type(exc).__name__}",
                evidence_refs=[],
                warnings=[str(exc)],
            )
        status = outcome.get("status", "SUCCEEDED")
        return AgentResult(
            request_id=request.request_id,
            status=status,
            summary=outcome["summary"],
            evidence_refs=list(outcome.get("evidence_refs", [])),
            warnings=list(outcome.get("warnings", [])),
            data=outcome.get("data"),
        )

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        raise NotImplementedError

    # -- helpers ------------------------------------------------------------

    def step(self, budget: int | None = None) -> int:
        """Consume one unit of the step budget; returns the step index."""
        limit = budget if budget is not None else self.max_steps
        if self._steps_used >= limit:
            raise RuntimeError(f"Step budget exhausted for {self.agent_id}")
        self._steps_used += 1
        return self._steps_used

    def record_feedback(self, reward: float, context: dict[str, Any] | None = None) -> None:
        """Optional feedback hook (Requirement: GAP-ARCH-A-01)."""

    def urn(self, *parts: str) -> str:
        return ":".join([URN_PREFIX, self.architecture, *parts])


def call_optional(hook: Callable | None, *args, default: Any = None, **kwargs) -> Any:
    """Invoke an optional callable hook with graceful fallback."""
    if hook is None:
        return default
    try:
        return hook(*args, **kwargs)
    except Exception:
        return default
