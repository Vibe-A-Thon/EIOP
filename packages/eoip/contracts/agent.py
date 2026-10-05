"""Versioned contracts for governed Deep Agents and safe XAI.

Explanations expose evidence and decision factors, never private chain-of-thought.
Defaults retain wire compatibility with the original v1 request/result models.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

AgentStatus = Literal["SUCCEEDED", "PARTIAL", "FAILED", "DENIED", "CANCELLED"]
AgentPhase = Literal[
    "RECEIVE", "ROUTE", "CONTEXT", "PLAN", "VALIDATE", "EXECUTE",
    "OBSERVE", "EVALUATE", "EXPLAIN", "AUDIT", "FINISH",
]
AgentType = Literal[
    "REFLEX", "MODEL_BASED", "GOAL_BASED", "UTILITY_BASED", "TASK",
    "ROUTER", "TOOL", "RAG", "ENTERPRISE", "HIERARCHICAL",
    "ORCHESTRATOR", "CRITIC", "PLANNER", "EXECUTOR", "REVIEWER",
    "VALIDATOR", "XAI", "JIT", "LEARNING", "WRITING", "MULTI_AGENT",
]
RiskLevel = Literal["R0", "R1", "R2", "R3", "R4"]


class AgentBudgets(BaseModel):
    """Hard upper bounds used by every agent and orchestration run."""

    max_steps: int = Field(default=8, ge=1, le=100)
    max_tool_calls: int = Field(default=8, ge=0, le=100)
    max_retries: int = Field(default=1, ge=0, le=5)
    max_recursion: int = Field(default=2, ge=0, le=10)
    max_seconds: float = Field(default=15.0, gt=0, le=300)
    max_model_tokens: int = Field(default=4096, ge=0, le=100_000)
    max_context_items: int = Field(default=100, ge=1, le=10_000)


class AgentContract(BaseModel):
    """Validated registration contract for a production agent."""

    schema_version: str = "2.0"
    agent_id: str = Field(min_length=1)
    version: str = Field(default="1.0.0", min_length=1)
    agent_type: AgentType = "TASK"
    purpose: str = Field(min_length=1)
    capabilities: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    prohibited_tools: list[str] = Field(default_factory=list)
    model_policy: str = "deterministic"
    memory_policy: Literal["NONE", "RUN_ONLY", "APPROVED"] = "RUN_ONLY"
    human_control: Literal["READ_ONLY", "PROPOSE_ONLY", "APPROVAL_REQUIRED"] = "READ_ONLY"
    risk_level: RiskLevel = "R0"
    budgets: AgentBudgets = Field(default_factory=AgentBudgets)
    retry_policy: str = "bounded"
    failure_policy: str = "fail_closed"
    evidence_required: bool = True
    audit_required: bool = True
    enabled: bool = True

    @model_validator(mode="after")
    def validate_tool_boundaries(self) -> AgentContract:
        overlap = set(self.allowed_tools) & set(self.prohibited_tools)
        if overlap:
            raise ValueError(f"Tools cannot be both allowed and prohibited: {sorted(overlap)}")
        if self.risk_level in {"R2", "R3", "R4"} and self.human_control == "READ_ONLY":
            raise ValueError("Risk R2-R4 agents must use proposal or approval control")
        return self


class AgentRequest(BaseModel):
    schema_version: str = "2.0"
    request_id: str
    agent_id: str
    goal: str
    context_refs: list[str] | None = None
    budgets: dict[str, Any] | None = None
    actor_id: str = "anonymous"
    correlation_id: str | None = None
    parent_run_id: str | None = None
    recursion_depth: int = Field(default=0, ge=0)
    dry_run: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class RuleDecision(BaseModel):
    rule_id: str
    outcome: Literal["ALLOW", "DENY", "WARN", "REDACT", "ABSTAIN", "BLOCK"]
    summary: str


class ConfidenceInput(BaseModel):
    name: str
    value: float = Field(ge=0, le=1)
    weight: float = Field(default=1, ge=0, le=1)
    evidence_refs: list[str] = Field(default_factory=list)


class ToolCallRecord(BaseModel):
    tool_call_id: str
    tool_name: str
    status: str
    risk_level: RiskLevel = "R0"
    duration_ms: int = Field(default=0, ge=0)
    evidence_refs: list[str] = Field(default_factory=list)
    arguments_digest: str | None = None
    error_code: str | None = None


class ExplanationEnvelope(BaseModel):
    """User-facing XAI payload; deliberately excludes private reasoning."""

    decision_summary: str
    observed_facts: list[str] = Field(default_factory=list)
    inferred_findings: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    graph_paths: list[list[str]] = Field(default_factory=list)
    rule_decisions: list[RuleDecision] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0, le=1)
    confidence_inputs: list[ConfidenceInput] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)
    rejected_alternatives: list[str] = Field(default_factory=list)
    chain_of_thought_disclosed: Literal[False] = False


class AgentTraceEvent(BaseModel):
    sequence: int = Field(ge=0)
    phase: AgentPhase
    occurred_at: str
    status: str
    summary: str
    evidence_refs: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentExecutionTrace(BaseModel):
    schema_version: str = "2.0"
    run_id: str
    request_id: str
    agent_id: str
    actor_id: str
    correlation_id: str
    contract_version: str
    events: list[AgentTraceEvent] = Field(default_factory=list)
    final_status: AgentStatus | None = None


class ChangeProposal(BaseModel):
    """An inert requested mutation. It cannot execute without explicit approval."""

    proposal_id: str
    run_id: str
    proposed_by: str
    operation: str
    target_ref: str
    patch: dict[str, Any]
    rationale: str
    evidence_refs: list[str]
    risk_level: RiskLevel = "R2"
    status: Literal["PENDING", "APPROVED", "REJECTED", "EXPIRED"] = "PENDING"
    approved_by: str | None = None
    created_at: str
    decided_at: str | None = None


class AgentResult(BaseModel):
    schema_version: str = "2.0"
    request_id: str
    status: AgentStatus
    summary: str
    evidence_refs: list[str]
    run_id: str | None = None
    tool_calls: list[dict[str, Any]] | None = None
    warnings: list[str] | None = None
    explanation: ExplanationEnvelope | None = None
    proposals: list[ChangeProposal] = Field(default_factory=list)
    data: Any = None
