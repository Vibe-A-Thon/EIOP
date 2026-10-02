"""Agent registry and runtime (FR-AGENT-003).

Read-only agents use allowlisted tools within execution budgets.
"""

from eoip.agents.runtime import AgentRegistry, AgentRuntime
from eoip.agents.trace_impact import TraceImpactAgent

__all__ = ["AgentRegistry", "AgentRuntime", "TraceImpactAgent"]
