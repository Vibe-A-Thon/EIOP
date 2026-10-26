"""Agent architectures: classical/cognitive types, advanced reasoning,
enterprise operational classes, multi-agent org patterns, and an A2A-style
communication layer (Requirement: GAP-ARCH).

Built on top of ``eoip.agents.runtime`` — every architecture class
implements the governed ``Agent`` protocol (budgets, firewall, circuit
breaker, XAI traces). Deterministic-first; optional hooks with graceful
fallback; external systems exposed as ``ExternalGate`` manifests.
"""

from eoip.agentarch.base import ArchitectureAgent, ExternalGate
from eoip.agentarch.org import (
    Blackboard, ContractNet, Coordinator, Ensemble, EventDriven,
    FederatedArchitecture, HandoffBased, HierarchicalTeams, LeaderFollower,
    ManagerSpecialist, MarketBased, Mesh, MixtureOfAgents, NegotiationBased,
    Pipeline, RuntimeRunner, SupervisorWorker, VotingBased,
)
from eoip.agentarch.a2a import (
    A2ABus, A2AMessage, CapabilityCard, TaskHandle, child_traceparent,
    new_traceparent, parse_traceparent,
)

__all__ = [
    "ArchitectureAgent", "ExternalGate",
    "Coordinator", "RuntimeRunner",
    "SupervisorWorker", "ManagerSpecialist", "LeaderFollower", "Blackboard",
    "HierarchicalTeams", "FederatedArchitecture", "MarketBased",
    "ContractNet", "NegotiationBased", "VotingBased", "Ensemble", "Mesh",
    "EventDriven", "Pipeline", "HandoffBased", "MixtureOfAgents",
    "A2ABus", "A2AMessage", "CapabilityCard", "TaskHandle",
    "child_traceparent", "new_traceparent", "parse_traceparent",
]
