"""Bounded hierarchical orchestration over governed child agents."""

from __future__ import annotations

from eoip.agents.runtime import AgentRuntime
from eoip.contracts.agent import AgentRequest, AgentResult
from pydantic import BaseModel, Field


class WorkflowPlan(BaseModel):
    workflow_id: str
    agent_ids: list[str] = Field(min_length=1, max_length=12)
    goal: str = Field(min_length=1)
    context_refs: list[str] = Field(default_factory=list, max_length=100)
    max_steps: int = Field(default=6, ge=1, le=12)
    max_seconds_per_agent: float = Field(default=15, gt=0, le=60)
    stop_on_failure: bool = True


class WorkflowResult(BaseModel):
    workflow_id: str
    status: str
    summary: str
    child_results: list[AgentResult]
    evidence_refs: list[str]


class AgentOrchestrator:
    """Sequential supervisor with explicit fan-out and recursion bounds."""

    def __init__(self, runtime: AgentRuntime) -> None:
        self._runtime = runtime

    def run(self, plan: WorkflowPlan, *, actor_id: str, correlation_id: str) -> WorkflowResult:
        if len(plan.agent_ids) > plan.max_steps:
            raise ValueError("Workflow exceeds its child-step budget")
        results: list[AgentResult] = []
        evidence: set[str] = set()
        for index, agent_id in enumerate(plan.agent_ids):
            result = self._runtime.run(AgentRequest(
                request_id=f"{plan.workflow_id}:{index}",
                agent_id=agent_id,
                goal=plan.goal,
                context_refs=plan.context_refs,
                actor_id=actor_id,
                correlation_id=correlation_id,
                parent_run_id=plan.workflow_id,
                recursion_depth=1,
                budgets={"max_seconds": plan.max_seconds_per_agent},
            ))
            results.append(result)
            evidence.update(result.evidence_refs)
            if plan.stop_on_failure and result.status in {"FAILED", "DENIED", "CANCELLED"}:
                break
        statuses = {result.status for result in results}
        status = "FAILED" if statuses & {"FAILED", "DENIED", "CANCELLED"} else (
            "PARTIAL" if "PARTIAL" in statuses else "SUCCEEDED"
        )
        return WorkflowResult(
            workflow_id=plan.workflow_id,
            status=status,
            summary=f"Executed {len(results)} of {len(plan.agent_ids)} governed child agents.",
            child_results=results,
            evidence_refs=sorted(evidence),
        )
