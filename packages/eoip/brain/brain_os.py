"""Enterprise Brain OS — Unified Cognitive Kernel for Living Enterprise Knowledge.

Coordinates:
- 14 Control Loops (HCTL, HITL-FE, HBTL, HATL, HITD, EITL, HITL, HOTL, HOOTL, HITA, HITC, HITI, MITL, HITP)
- 35 Agent Archetypes & Swarm Systems
- 17 Unified RAG Retrieval Patterns
- 13 Query Languages & Transpilation (RDF, OWL, Gremlin, Cypher, GQL, openCypher, SHACL, SPARQL, SKOS, EOQL, EQL, OSQL, NL2Query)
- 17 Multi-Model, Native Graph & Vector Databases
- Deterministic & Non-Deterministic Hybrid Answering Engine
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import time

from eoip.agents.loops import EnterpriseLoopManager, LoopType, RiskTier, LoopDecision
from eoip.agents.archetypes import AgentFactory, BaseAgent, AgentResponse
from eoip.retrieval.rag_suite import EnterpriseRAGSuite, RAGMode, RAGResult
from eoip.query.polyglot_engine import PolyglotQueryEngine, QueryDialect, PolyglotQuery, QueryExecutionResult
from eoip.graph.database_adapters import DatabaseAdapterRegistry, DatabaseType, DatabaseHealth
from eoip.brain.living_brain_algorithms import LivingBrainAlgorithms, BrainStateSnapshot
from eoip.models.self_llm import get_self_llm_engine, CognitiveTier, GenerationConfig, SelfLLMEngine
from eoip.brain.learning_engine import CognitiveLearningEngine, LearningParadigm
from eoip.brain.report_generator import DetailedReportGenerator, QueryApproach, BrainReport
from eoip.brain.cognitive_narrator import CognitiveNarrator, CognitiveNarration




@dataclass
class BrainAnswer:
    query: str
    answer: str
    mode: str  # DETERMINISTIC, NON_DETERMINISTIC_AUGMENTED, HYBRID
    confidence: float
    evidence_refs: list[str] = field(default_factory=list)
    governance_decision: LoopDecision | None = None
    agent_trace: list[str] = field(default_factory=list)
    rag_result: RAGResult | None = None
    query_result: QueryExecutionResult | None = None
    cognitive_tier: str | None = None
    xai_explanation: dict[str, Any] | None = None
    latency_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "answer": self.answer,
            "mode": self.mode,
            "confidence": round(self.confidence, 3),
            "evidence_count": len(self.evidence_refs),
            "cognitive_tier": self.cognitive_tier,
            "latency_ms": round(self.latency_ms, 2),
            "governance": {
                "loop_type": self.governance_decision.loop_type.value if self.governance_decision else None,
                "allowed": self.governance_decision.allowed if self.governance_decision else True,
            },
            "agent_trace": self.agent_trace,
            "xai": self.xai_explanation,
            "metadata": self.metadata,
        }


class BrainOSKernel:
    """The central Enterprise Brain Operating System kernel."""

    def __init__(self, graph_store: Any = None) -> None:
        self.graph_store = graph_store
        self.loop_manager = EnterpriseLoopManager()
        self.rag_suite = EnterpriseRAGSuite(graph_store=graph_store)
        self.polyglot_engine = PolyglotQueryEngine()
        self.db_registry = DatabaseAdapterRegistry()
        self.living_brain = LivingBrainAlgorithms()
        self.self_llm: SelfLLMEngine = get_self_llm_engine()
        self.learning_engine: CognitiveLearningEngine = CognitiveLearningEngine()
        self.report_generator: DetailedReportGenerator = DetailedReportGenerator(learning_engine=self.learning_engine)
        self.cognitive_narrator: CognitiveNarrator = CognitiveNarrator()

        self.working_memory: list[dict[str, Any]] = []

        self.episodic_memory: list[dict[str, Any]] = []
        self.semantic_memory: dict[str, Any] = {}
        self.procedural_memory: dict[str, Any] = {}

    def ask(
        self,
        query: str,
        loop: LoopType = LoopType.HITL_FE,
        risk: RiskTier = RiskTier.R1,
        rag_mode: RAGMode = RAGMode.HYBRID_RAG,
        target_db: DatabaseType = DatabaseType.NEO4J,
        force_deterministic: bool = False,
        context: dict[str, Any] | None = None,
        tier: CognitiveTier = CognitiveTier.OPUS_FRONTIER,
    ) -> BrainAnswer:
        """Universal query and answering interface.

        Supports both deterministic structured query execution and non-deterministic
        LLM-augmented reasoning with strict SHACL/graph guardrails.
        """
        start = time.time()
        ctx = context or {}

        # 1. Governance Loop Verification
        decision = self.loop_manager.evaluate_action(
            action_name="user_query_answering",
            risk_tier=risk,
            loop_override=loop,
            context=ctx,
        )
        if not decision.allowed:
            return BrainAnswer(
                query=query,
                answer=f"Execution blocked by governance loop {decision.loop_type.value}: {decision.reason}",
                mode="BLOCKED",
                confidence=0.0,
                governance_decision=decision,
                latency_ms=(time.time() - start) * 1000.0,
            )

        # 2. Query Dialect Analysis
        detected_dialect = self.polyglot_engine.detect_dialect(query)

        # 3. Deterministic Execution Route
        is_structured_query = detected_dialect != QueryDialect.NL2QUERY or force_deterministic

        if is_structured_query and detected_dialect != QueryDialect.NL2QUERY:
            poly_query = PolyglotQuery(query_text=query, dialect=detected_dialect)
            q_res = self.polyglot_engine.execute_query(poly_query, store=self.graph_store)
            adapter = self.db_registry.get_adapter(target_db)
            db_res = adapter.execute_query(q_res.plan.executable_code)

            answer_text = (
                f"Deterministic query executed via {detected_dialect.value} on {target_db.value}. "
                f"Returned {len(q_res.records)} records."
            )
            return BrainAnswer(
                query=query,
                answer=answer_text,
                mode="DETERMINISTIC",
                confidence=1.0,
                evidence_refs=[r.get("id", "rec") for r in q_res.records],
                governance_decision=decision,
                query_result=q_res,
                cognitive_tier=tier.value,
                agent_trace=[f"Detected dialect: {detected_dialect.value}", f"Executed on {target_db.value}"],
                latency_ms=(time.time() - start) * 1000.0,
                metadata={"db_response": db_res},
            )

        # 4. Hybrid / Non-Deterministic LLM-Augmented Route
        rag_res = self.rag_suite.execute(query=query, mode=rag_mode, context=ctx)

        # Route through appropriate agent archetype
        router = AgentFactory.create("RouterAgent")
        route_decision = router.run(query).output
        selected_route = route_decision.get("selected_route", "RAG_AGENT")

        agent_worker = AgentFactory.create("LAYAAgent" if selected_route == "ENTERPRISE_AGENT" else "RAGAgent")
        agent_res = agent_worker.run(query, context={"evidence": [e.content for e in rag_res.evidence]})

        # Self-LLM Frontier Neural Generation & Reasoning
        llm_gen = self.self_llm.generate(
            prompt=query,
            config=GenerationConfig(
                tier=tier,
                system_prompt="You are the Enterprise Living Brain OS Kernel with frontier reasoning capabilities.",
                enable_xai=True,
            ),
            context="\n".join(e.content for e in rag_res.evidence),
        )

        final_answer = llm_gen.content if llm_gen.content else f"{agent_res.output.get('answer', rag_res.answer)}"

        xai_payload = None
        if llm_gen.xai:
            xai_payload = {
                "token_attributions": [
                    {"token": t.token, "salience": t.salience_score, "entity": t.grounded_entity}
                    for t in llm_gen.xai.token_attributions
                ],
                "neuro_symbolic_citations": llm_gen.xai.neuro_symbolic_citations,
                "counterfactuals": [
                    {"premise": c.premise, "impact_delta": c.impact_delta, "explanation": c.explanation}
                    for c in llm_gen.xai.counterfactuals
                ],
                "uncertainty": {
                    "epistemic": llm_gen.xai.epistemic_uncertainty,
                    "aleatoric": llm_gen.xai.aleatoric_uncertainty,
                    "coverage_pct": llm_gen.xai.conformal_coverage_pct,
                },
            }

        # Consolidate into Living Brain memory
        self.episodic_memory.append({"query": query, "answer": final_answer, "timestamp": time.time()})
        if len(self.episodic_memory) >= 5:
            self.living_brain.consolidate_neuro_symbolic_memory(self.episodic_memory)
            self.episodic_memory.clear()

        narration = self.cognitive_narrator.narrate(query=query, tier=tier, context=ctx)

        return BrainAnswer(
            query=query,
            answer=final_answer,
            mode="HYBRID",
            confidence=max(rag_res.confidence, 0.85),
            evidence_refs=[e.chunk_id for e in rag_res.evidence],
            governance_decision=decision,
            agent_trace=[f"Router -> {selected_route}", f"Worker -> {agent_worker.name}"] + rag_res.reasoning_steps + llm_gen.reasoning_trace,
            rag_result=rag_res,
            cognitive_tier=tier.value,
            xai_explanation=xai_payload,
            latency_ms=(time.time() - start) * 1000.0,
            metadata={
                "agent_response": agent_res.output,
                "model_name": llm_gen.model_name,
                "enhanced_formulation": narration.enhanced_query.enhanced_formulation,
                "narration": narration.to_dict(),
            },
        )

    def narrate_query(
        self,
        query: str,
        tier: CognitiveTier = CognitiveTier.OPUS_FRONTIER,
        context: dict[str, Any] | None = None,
    ) -> CognitiveNarration:
        """Deeply comprehends the query, enhances it, generates 6 approach questions,
        and constructs a flowing publication-grade LLM narration.
        """
        return self.cognitive_narrator.narrate(query=query, tier=tier, context=context)

    def query_and_report(
        self,
        query: str,
        approach: QueryApproach = QueryApproach.HYBRID,
        tier: CognitiveTier = CognitiveTier.OPUS_FRONTIER,
        context: dict[str, Any] | None = None,
    ) -> BrainReport:
        """Executes one of 6 analytical approaches and generates an exhaustive, publication-grade deep report."""
        return self.report_generator.generate_report(
            query=query,
            approach=approach,
            tier=tier,
            graph_store=self.graph_store,
            context=context,
        )

    def get_system_telemetry(self) -> dict[str, Any]:
        """Returns comprehensive telemetry across all Brain OS subsystems."""
        snapshot = self.living_brain.compute_brain_snapshot()
        db_health = self.db_registry.health_check_all()

        return {
            "status": "OPERATIONAL",
            "supported_loops": [loop.value for loop in LoopType],
            "supported_agents": AgentFactory.list_archetypes(),
            "supported_rag_modes": [mode.value for mode in RAGMode],
            "supported_query_dialects": [dialect.value for dialect in QueryDialect],
            "supported_databases": self.db_registry.list_supported_databases(),
            "supported_approaches": [approach.value for approach in QueryApproach],
            "self_llm": {
                "status": "OPERATIONAL",
                "default_tier": CognitiveTier.OPUS_FRONTIER.value,
                "supported_tiers": [tier.value for tier in CognitiveTier],
                "xai_support": True,
            },
            "cognitive_narrator": {
                "status": "OPERATIONAL",
                "approaches_supported": 6,
                "capabilities": [
                    "QUESTION_UNDERSTANDING",
                    "QUESTION_ENHANCEMENT",
                    "COMPLEMENTARY_QUESTION_GENERATION",
                    "MULTI_PARADIGM_ANSWERING",
                    "PUBLICATION_GRADE_LLM_NARRATION",
                ],
            },
            "learning_engine": self.learning_engine.get_learning_telemetry(),
            "brain_snapshot": {
                "snapshot_id": snapshot.snapshot_id,
                "coherence_score": snapshot.coherence_score,
                "concept_count": snapshot.concept_count,
                "merkle_root": snapshot.merkle_root,
            },
            "database_health": {k: v.connected for k, v in db_health.items()},
        }


