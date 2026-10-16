"""SemanticIndexAgent: orchestrates post-ingestion semantic processing.

Runs the semantic pipeline (Step 2) as a bounded agent workflow.
Triggered manually via admin API or automatically via graph evolution events.
"""

from __future__ import annotations

from eoip.contracts.agent import AgentRequest, AgentResult, ExplanationEnvelope
from eoip.graph.store import GraphStore
from eoip.ingestion.semantic_pipeline import PipelineStage, SemanticPipeline


class SemanticIndexAgent:
    agent_id = "SemanticIndex"
    allowed_tools = frozenset({"search", "entity", "validation", "analytics"})
    max_steps = 20
    max_seconds = 120.0

    def __init__(self, config: dict | None = None) -> None:
        if config:
            budgets = config.get("budgets", {})
            self.max_steps = budgets.get("max_steps", self.max_steps)
            self.max_seconds = budgets.get("max_seconds", self.max_seconds)

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        pipeline = SemanticPipeline(store)

        stages = None
        if request.context_refs:
            stage_names = [s.strip() for s in request.context_refs if s.strip()]
            stages = []
            for name in stage_names:
                try:
                    stages.append(PipelineStage(name))
                except ValueError:
                    pass
            if not stages:
                stages = None

        scope = {}
        if request.goal:
            parts = request.goal.split(":")
            if len(parts) == 2:
                scope[parts[0].strip()] = parts[1].strip()

        result = pipeline.run(
            pipeline_id=f"agent-{request.request_id}",
            stages=stages,
            scope=scope,
        )

        stage_summaries = []
        evidence_refs = []
        for sr in result.stages:
            stage_summaries.append(f"{sr.stage.value}: {sr.status.value} ({sr.items_processed} items, {sr.duration_ms:.0f}ms)")
            if sr.errors:
                evidence_refs.extend(sr.errors)

        envelope = ExplanationEnvelope(
            decision_summary=f"Semantic pipeline completed: {len(result.stages)} stages, {result.total_duration_ms:.0f}ms total",
            observed_facts=[f"Pipeline {result.pipeline_id} executed {len(result.stages)} stages"],
            inferred_findings=stage_summaries,
            evidence_refs=[f"pipeline:{result.pipeline_id}"],
            confidence=1.0 if result.overall_status == "completed" else 0.5,
            uncertainty=["Pipeline stages may have partial results"] if result.overall_status != "completed" else [],
        )

        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED" if result.overall_status == "completed" else "PARTIAL",
            summary=f"Semantic pipeline completed: {len(result.stages)} stages, {result.total_duration_ms:.0f}ms total",
            evidence_refs=[f"pipeline:{result.pipeline_id}"],
            explanation=envelope,
            data=result.to_dict(),
        )
