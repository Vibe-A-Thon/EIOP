"""AgentRequest v1 / AgentResult v1.

Normative: EOIP-engg-doc-pkg/schemas/agent_request.schema.json,
EOIP-engg-doc-pkg/schemas/agent_result.schema.json
Agents return decision summaries and evidence — never hidden chain-of-thought.
"""

from typing import Literal

from pydantic import BaseModel

AgentStatus = Literal["SUCCEEDED", "PARTIAL", "FAILED", "DENIED"]


class AgentRequest(BaseModel):
    request_id: str
    agent_id: str
    goal: str
    context_refs: list[str] | None = None
    budgets: dict | None = None


class AgentResult(BaseModel):
    request_id: str
    status: AgentStatus
    summary: str
    evidence_refs: list[str]
    tool_calls: list | None = None
    warnings: list[str] | None = None
