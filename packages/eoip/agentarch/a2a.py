"""A2A-style agent communication layer.

Requirement: GAP-ARCH-E. Complements MCP: an envelope for inter-agent
messages, capability discovery, delegation with bounded recursion, task
cancellation, and trace propagation (traceparent-style). All transports are
in-process by default; wire transports are External gates.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.contracts.source_event import utc_now_iso


class A2AMessage(BaseModel):
    """Inter-agent message envelope.

    Requirement: GAP-ARCH-E-01. Carries a W3C-tracecontext-style
    ``traceparent`` (``00-<trace-id>-<parent-id>-01``) so causal chains span
    agent hops.
    """

    model_config = ConfigDict(extra="forbid")

    message_id: str = Field(default_factory=lambda: f"urn:eoip:a2a:msg:{uuid4()}")
    sender_id: str
    recipient_id: str
    message_type: str = "TASK"  # TASK | RESPONSE | CANCEL | CAPABILITY_QUERY | HEARTBEAT
    content: dict[str, Any] = Field(default_factory=dict)
    traceparent: str
    causation_id: str | None = None
    created_at: str = Field(default_factory=utc_now_iso)


class CapabilityCard(BaseModel):
    """Advertised capability descriptor for discovery.

    Requirement: GAP-ARCH-E-02.
    """

    model_config = ConfigDict(extra="forbid")

    agent_id: str
    capabilities: list[str] = Field(default_factory=list)
    input_contract: dict[str, str] = Field(default_factory=dict)
    output_contract: dict[str, str] = Field(default_factory=dict)
    budgets: dict[str, Any] = Field(default_factory=dict)


def new_traceparent() -> str:
    return f"00-{uuid4().hex[:32]}-{uuid4().hex[:16]}-01"


def child_traceparent(parent: str) -> str:
    """Propagate the trace id, replacing the parent id."""
    parts = parent.split("-")
    if len(parts) != 4 or parts[0] != "00":
        return new_traceparent()
    return f"00-{parts[1]}-{uuid4().hex[:16]}-01"


def parse_traceparent(traceparent: str) -> dict[str, str]:
    parts = traceparent.split("-")
    if len(parts) != 4:
        raise ValueError("Invalid traceparent")
    return {"version": parts[0], "trace_id": parts[1], "parent_id": parts[2], "flags": parts[3]}


class TaskHandle(BaseModel):
    """Handle for a delegated task, enabling cancellation."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    agent_id: str
    traceparent: str
    status: str = "RUNNING"  # RUNNING | SUCCEEDED | FAILED | CANCELLED


class A2ABus:
    """In-process A2A bus: registry, delegation, cancellation, discovery.

    Requirement: GAP-ARCH-E-03. Transports (HTTP/gRPC) are External gates;
    the bus itself is a deterministic in-process fabric over the governed
    ``AgentRuntime`` or an injected runner.
    """

    def __init__(self, runner, *, max_recursion: int = 2) -> None:
        self._runner = runner
        self._cards: dict[str, CapabilityCard] = {}
        self._tasks: dict[str, TaskHandle] = {}
        self._results: dict[str, AgentResult] = {}
        self._cancelled: set[str] = set()
        self._max_recursion = max_recursion

    # -- capability discovery ----------------------------------------------

    def register(self, card: CapabilityCard) -> None:
        self._cards[card.agent_id] = card

    def capabilities(self, agent_id: str) -> CapabilityCard | None:
        return self._cards.get(agent_id)

    def find_agents(self, capability: str) -> list[str]:
        return sorted(aid for aid, card in self._cards.items() if capability in card.capabilities)

    # -- messaging ------------------------------------------------------------

    def send(self, message: A2AMessage) -> A2AMessage:
        """Deliver a message; returns the recipient's response envelope."""
        if message.recipient_id not in self._cards:
            raise ValueError(f"Unknown recipient: {message.recipient_id}")
        if message.message_type == "CANCEL":
            self._cancelled.add(str(message.content.get("task_id", "")))
            return self._reply(message, {"cancelled": True})
        if message.message_type == "CAPABILITY_QUERY":
            card = self._cards[message.recipient_id]
            return self._reply(message, {"card": card.model_dump()})
        if message.message_type == "TASK":
            handle = self.delegate(message.recipient_id, message.content.get("goal", ""),
                                   traceparent=message.traceparent,
                                   recursion_depth=int(message.content.get("recursion_depth", 0)))
            return self._reply(message, {"task_id": handle.task_id, "status": handle.status})
        return self._reply(message, {})

    def _reply(self, message: A2AMessage, content: dict[str, Any]) -> A2AMessage:
        return A2AMessage(
            sender_id=message.recipient_id, recipient_id=message.sender_id,
            message_type="RESPONSE", content=content,
            traceparent=child_traceparent(message.traceparent),
            causation_id=message.message_id,
        )

    # -- delegation & cancellation --------------------------------------------

    def delegate(self, agent_id: str, goal: str, *, traceparent: str,
                 recursion_depth: int = 0, metadata: dict | None = None) -> TaskHandle:
        if agent_id not in self._cards:
            raise ValueError(f"Unknown agent: {agent_id}")
        if recursion_depth > self._max_recursion:
            raise ValueError("Delegation recursion budget exceeded")
        task_id = f"urn:eoip:a2a:task:{uuid4()}"
        handle = TaskHandle(task_id=task_id, agent_id=agent_id,
                            traceparent=child_traceparent(traceparent))
        self._tasks[task_id] = handle
        if task_id in self._cancelled:
            handle.status = "CANCELLED"
            return handle
        result = self._runner.run(agent_id, goal, metadata=metadata or {})
        if task_id in self._cancelled:
            handle.status = "CANCELLED"
        else:
            handle.status = result.status if result.status in {"SUCCEEDED", "FAILED"} else "SUCCEEDED"
        self._results[task_id] = result
        return handle

    def cancel(self, task_id: str) -> bool:
        handle = self._tasks.get(task_id)
        if handle is None:
            return False
        self._cancelled.add(task_id)
        handle.status = "CANCELLED"
        return True

    def result(self, task_id: str) -> AgentResult | None:
        return self._results.get(task_id)
