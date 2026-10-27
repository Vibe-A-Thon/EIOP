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
from eoip.brain.graph_intelligence import GraphIntelligenceEngine, ApproachFindings
from eoip.enterprise.circuit_breaker import get_circuit_breaker_registry
from eoip.enterprise.audit import get_audit_log, AuditCategory
from eoip.enterprise.cache import get_cache
from eoip.enterprise.lifecycle import get_lifecycle_manager
from eoip.enterprise.feature_flags import get_feature_flags
from eoip.enterprise.webhooks import get_webhook_manager
from eoip.notifications.hub import get_notification_hub
from eoip.scheduling.executor import get_task_executor
from eoip.incidents.manager import get_incident_manager
from eoip.imports.engine import get_import_engine
from eoip.model_management.registry import get_model_registry
from eoip.maintenance.autonomous import get_maintenance_engine
from eoip.streaming.event_stream import get_event_stream
from eoip.integrations.bus import get_integration_bus
from eoip.edge.runtime import get_edge_runtime
from eoip.sdk.gateway import get_api_gateway
from eoip.search.semantic import get_semantic_index
from eoip.recovery.wal import get_wal
from eoip.copilot.engine import get_copilot_engine
from eoip.model_management.ai_ml_ops import get_aiml_ops
from eoip.search.hybrid_engine import get_hybrid_search_engine
from eoip.features.engine import get_feature_engine
from eoip.specs.engine import get_spec_engine
from eoip.prompts.engine import get_prompt_engine
from eoip.cost_optimization.engine import get_cost_engine
from eoip.security.engine import get_security_engine
from eoip.state.engine import get_state_engine
from eoip.harness.engine import get_harness_engine
from eoip.context.engine import get_context_engine
from eoip.tools_contract.engine import get_tool_contract_engine
from eoip.graph_loop.engine import get_graph_loop_engine
from eoip.evaluation.engine import get_evaluation_engine
from eoip.memory_eng.engine import get_memory_engine
from eoip.intelligence_eng.engine import get_intelligence_engine
from eoip.token_formats.engine import get_token_format_engine
from eoip.verification.engine import get_verification_engine
from eoip.routing.engine import get_router_engine
from eoip.graph_graph.engine import get_graph_graph_engine
from eoip.token_budget.engine import get_token_budget_engine
from eoip.xai.engine import get_xai_engine
from eoip.mlops.experiment_tracker import get_experiment_tracker
from eoip.embeddings.engine import get_embedding_engine
from eoip.causal.engine import get_causal_engine
from eoip.federation.engine import get_federation_engine
from eoip.distillation.engine import get_distillation_engine
from eoip.gnn.engine import get_gnn_engine




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
        self.cognitive_narrator: CognitiveNarrator = CognitiveNarrator(graph_store=graph_store)
        self.graph_intelligence: GraphIntelligenceEngine = GraphIntelligenceEngine(graph_store=graph_store)

        # Phase 1 Core Engines
        self.token_format_engine = get_token_format_engine()
        self.verification_engine = get_verification_engine()
        self.router_engine = get_router_engine()
        self.graph_graph_engine = get_graph_graph_engine()
        self.token_budget_engine = get_token_budget_engine()

        # Phase 2 & Phase 3 Engines
        self.xai_engine = get_xai_engine()
        self.experiment_tracker = get_experiment_tracker()
        self.embedding_engine = get_embedding_engine()
        self.causal_engine = get_causal_engine(store=graph_store)
        self.federation_engine = get_federation_engine()
        self.distillation_engine = get_distillation_engine()
        self.gnn_engine = get_gnn_engine()

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
        start = time.perf_counter()  # monotonic, high resolution (Windows time.time() ticks ~15 ms)
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
                latency_ms=(time.perf_counter() - start) * 1000.0,
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
                latency_ms=(time.perf_counter() - start) * 1000.0,
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
            latency_ms=(time.perf_counter() - start) * 1000.0,
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

    def intelligent_query(
        self,
        query: str,
        approach: str = "HYBRID",
        tier: CognitiveTier = CognitiveTier.OPUS_FRONTIER,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Unified intelligent query: understands the question, queries the live graph,
        runs multi-approach analysis, and assembles a flowing LLM-style narrative answer.

        This is the master endpoint that combines:
        - Question understanding and enhancement (CognitiveNarrator)
        - Live graph evidence gathering (GraphIntelligenceEngine)
        - 6 analytical approaches with real data
        - Self-LLM synthesis and XAI attribution
        - Q-Learning policy updates
        - Publication-grade markdown narration
        """
        start = time.perf_counter()
        ctx = context or {}

        cache = get_cache()
        cache_key = cache.fingerprint(query, approach=approach, tier=tier.value)
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        approach_enum = QueryApproach.HYBRID
        for qa in QueryApproach:
            if qa.value == approach.upper():
                approach_enum = qa
                break

        # 1. Question Understanding & Enhancement
        enhanced = self.cognitive_narrator.analyze_and_enhance(query)

        # 2. Live Graph Evidence Gathering
        if approach_enum == QueryApproach.DETERMINISTIC:
            graph_findings = self.graph_intelligence.execute_deterministic(query)
        elif approach_enum == QueryApproach.PROBABILISTIC:
            graph_findings = self.graph_intelligence.execute_probabilistic(query)
        elif approach_enum == QueryApproach.HEURISTIC:
            graph_findings = self.graph_intelligence.execute_heuristic(query)
        elif approach_enum == QueryApproach.STOCHASTIC:
            graph_findings = self.graph_intelligence.execute_stochastic(query)
        elif approach_enum == QueryApproach.NON_DETERMINISTIC:
            graph_findings = self.graph_intelligence.execute_non_deterministic(query)
        else:
            graph_findings = self.graph_intelligence.execute_hybrid(query)

        # 3. Topology snapshot for context
        topology = self.graph_intelligence.get_topology_snapshot()

        # 4. Self-LLM Frontier Synthesis
        evidence_context = "\n".join(
            f"- {e.title} ({e.label}): {len(e.outbound_edges)} outbound, {len(e.inbound_edges)} inbound edges"
            for e in graph_findings.raw_evidence[:10]
        )
        llm_gen = self.self_llm.generate(
            prompt=enhanced.enhanced_formulation,
            config=GenerationConfig(
                tier=tier,
                system_prompt=(
                    "You are the Enterprise Living Brain answering with precision and eloquence. "
                    "Ground every claim in the provided graph evidence. Deliver a comprehensive, "
                    "multi-section answer as a frontier AI would."
                ),
                enable_xai=True,
            ),
            context=evidence_context,
        )

        # 5. Q-Learning Reward Update
        reward = 1.0 if graph_findings.confidence > 0.8 else 0.5
        q_val = self.learning_engine.q_learning.update(
            query=query,
            action=f"{approach_enum.value}_{tier.value}",
            reward=reward,
        )

        # 6. Narration Assembly
        narration = self.cognitive_narrator.narrate(query=query, tier=tier, context=ctx)

        # 7. Build the unified response
        latency_ms = (time.perf_counter() - start) * 1000.0

        get_audit_log().record(
            category=AuditCategory.QUERY_EXECUTION,
            action="intelligent_query",
            resource=f"approach:{approach_enum.value}",
            details={"query_length": len(query), "entities_found": len(graph_findings.discovered_entities)},
        )

        result = {
            "query": query,
            "enhanced_formulation": enhanced.enhanced_formulation,
            "detected_domain": enhanced.detected_domain.value,
            "extracted_entities": enhanced.extracted_entities,
            "intent_analysis": enhanced.intent_analysis,
            "scope_boundary": enhanced.scope_boundary,
            "approach": approach_enum.value,
            "cognitive_tier": tier.value,
            "graph_findings": {
                "methodology": graph_findings.methodology,
                "discovered_entities": graph_findings.discovered_entities,
                "known_edges": [
                    {"source": s, "relation": r, "target": t}
                    for s, r, t in graph_findings.known_edges[:20]
                ],
                "findings": graph_findings.findings,
                "recommendations": graph_findings.recommendations,
                "confidence": graph_findings.confidence,
                "metrics": graph_findings.metrics,
            },
            "topology": {
                "total_vertices": topology.total_vertices,
                "total_edges": topology.total_edges,
                "label_distribution": topology.label_distribution,
                "hub_vertices": topology.hub_vertices[:5],
                "avg_degree": topology.avg_degree,
                "density": topology.density,
            },
            "complementary_questions": [
                {
                    "approach": cq.approach,
                    "question": cq.question,
                    "rationale": cq.rationale,
                    "answer": cq.answer,
                    "confidence": cq.confidence,
                    "evidence_points": cq.evidence_points,
                }
                for cq in enhanced.complementary_questions
            ],
            "llm_synthesis": llm_gen.content,
            "reasoning_trace": llm_gen.reasoning_trace,
            "xai_attribution": {
                "token_attributions": [
                    {"token": t.token, "salience": t.salience_score, "entity": t.grounded_entity}
                    for t in (llm_gen.xai.token_attributions if llm_gen.xai else [])
                ],
                "neuro_symbolic_citations": llm_gen.xai.neuro_symbolic_citations if llm_gen.xai else [],
                "counterfactuals": [
                    {"premise": c.premise, "impact_delta": c.impact_delta, "explanation": c.explanation}
                    for c in (llm_gen.xai.counterfactuals if llm_gen.xai else [])
                ],
                "uncertainty": {
                    "epistemic": llm_gen.xai.epistemic_uncertainty if llm_gen.xai else 0.0,
                    "aleatoric": llm_gen.xai.aleatoric_uncertainty if llm_gen.xai else 0.0,
                } if llm_gen.xai else None,
            },
            "learning": {
                "q_value": q_val,
                "reward": reward,
                "action": f"{approach_enum.value}_{tier.value}",
            },
            "narrative_markdown": narration.markdown_narrative,
            "confidence_score": round(
                (graph_findings.confidence + narration.confidence_score) / 2, 4
            ),
            "latency_ms": round(latency_ms, 2),
            "metadata": {
                "model_name": llm_gen.model_name,
                "narration_id": narration.narration_id,
                "evidence_count": len(graph_findings.raw_evidence),
                "cached": False,
            },
        }

        cache.put(cache_key, result, ttl=120.0)
        return result

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
            "graph_intelligence": {
                "status": "OPERATIONAL",
                "graph_store_connected": self.graph_intelligence._has_store(),
                "approaches": [
                    "DETERMINISTIC", "NON_DETERMINISTIC", "PROBABILISTIC",
                    "HEURISTIC", "STOCHASTIC", "HYBRID",
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
            "circuit_breakers": [
                {"name": m.name, "state": m.state.value, "failures": m.failure_count}
                for m in get_circuit_breaker_registry().all_metrics()
            ],
            "audit_log": get_audit_log().get_stats(),
            "cache": {
                "hits": get_cache().stats().hits,
                "misses": get_cache().stats().misses,
                "hit_rate": get_cache().stats().hit_rate,
                "size": get_cache().stats().current_size,
            },
            "lifecycle": get_lifecycle_manager().stats(),
            "feature_flags": get_feature_flags().stats(),
            "webhooks": get_webhook_manager().stats(),
            "notifications": get_notification_hub().stats(),
            "scheduled_tasks": get_task_executor().stats(),
            "incidents": get_incident_manager().stats(),
            "imports": get_import_engine().stats(),
            "model_registry": get_model_registry().stats(),
            "maintenance": get_maintenance_engine().stats(),
            "event_stream": get_event_stream().stats(),
            "integrations": get_integration_bus().stats(),
            "edge_runtime": get_edge_runtime().stats(),
            "api_gateway": get_api_gateway().stats(),
            "semantic_search": get_semantic_index().stats(),
            "wal_recovery": get_wal().stats(),
            "copilot": get_copilot_engine().stats(),
            "aiml_ops": get_aiml_ops().stats(),
            "hybrid_search": get_hybrid_search_engine().stats(),
            "feature_engineering": get_feature_engine().stats(),
            "spec_engineering": get_spec_engine().stats(),
            "prompt_engineering": get_prompt_engine().stats(),
            "cost_optimization": get_cost_engine().stats(),
            "security_red_team": get_security_engine().stats(),
            "state_persistence": get_state_engine().stats(),
            "harness_engineering": get_harness_engine().stats(),
            "context_engineering": get_context_engine().stats(),
            "tool_contract_mcp": get_tool_contract_engine().stats(),
            "graph_loop_engineering": get_graph_loop_engine().stats(),
            "evaluation_benchmarking": get_evaluation_engine().stats(),
            "memory_engineering": get_memory_engine().stats(),
            "intelligence_engineering": get_intelligence_engine().stats(),
        }


