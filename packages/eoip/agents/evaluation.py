"""Deterministic evaluation gates for agent releases."""

from __future__ import annotations

from eoip.agents.runtime import AgentRuntime
from eoip.contracts.agent import AgentRequest
from pydantic import BaseModel, Field


class GoldenAgentCase(BaseModel):
    case_id: str
    agent_id: str
    goal: str
    context_refs: list[str] = Field(default_factory=list)
    expected_statuses: set[str] = Field(default_factory=lambda: {"SUCCEEDED", "PARTIAL"})
    required_evidence: bool = False
    forbidden_tool_names: set[str] = Field(default_factory=set)


class AgentEvaluationReport(BaseModel):
    cases: int
    passed: int
    pass_rate: float
    evidence_rate: float
    violations: list[str]
    gate_passed: bool


def evaluate_agents(
    runtime: AgentRuntime,
    cases: list[GoldenAgentCase],
    *,
    minimum_pass_rate: float = 0.9,
) -> AgentEvaluationReport:
    if not cases:
        raise ValueError("At least one golden case is required")
    passed = 0
    with_evidence = 0
    violations: list[str] = []
    for case in cases:
        result = runtime.run(AgentRequest(
            request_id=f"eval:{case.case_id}",
            agent_id=case.agent_id,
            goal=case.goal,
            context_refs=case.context_refs,
            actor_id="agent-evaluator",
            dry_run=True,
        ))
        tools = {
            item.get("tool_name") or item.get("tool")
            for item in (result.tool_calls or [])
        }
        case_ok = result.status in case.expected_statuses
        if case.required_evidence and not result.evidence_refs:
            case_ok = False
            violations.append(f"{case.case_id}: required evidence was missing")
        forbidden = tools & case.forbidden_tool_names
        if forbidden:
            case_ok = False
            violations.append(f"{case.case_id}: forbidden tools used: {sorted(forbidden)}")
        if result.evidence_refs:
            with_evidence += 1
        if case_ok:
            passed += 1
        else:
            violations.append(f"{case.case_id}: status {result.status} did not meet expectations")
    pass_rate = passed / len(cases)
    return AgentEvaluationReport(
        cases=len(cases),
        passed=passed,
        pass_rate=pass_rate,
        evidence_rate=with_evidence / len(cases),
        violations=violations,
        gate_passed=pass_rate >= minimum_pass_rate,
    )
