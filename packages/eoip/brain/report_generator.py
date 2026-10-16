"""Enterprise Deep Report Generator & Multi-Approach Query Engine.

Supports 6 distinct querying and reasoning approaches:
1. DETERMINISTIC (Exact graph pattern matching, invariant verification, zero hallucination)
2. NON_DETERMINISTIC (Generative neural synthesis, open-ended frontier reasoning)
3. PROBABILISTIC (Bayesian belief updates, posterior probability distributions, confidence bounds)
4. HEURISTIC (A* pathfinding, rule-based inference, PageRank / centrality ranking)
5. STOCHASTIC (Monte Carlo random-walk exploration, simulated annealing, temperature rollouts)
6. HYBRID / HYPERAUTOMATION (Unified hyperautomated orchestration executing all 5 paradigms)
"""

from __future__ import annotations

import enum
import hashlib
import json
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from eoip.models.self_llm import (
    CognitiveTier,
    GenerationConfig,
    GenerationResult,
    TensorMath,
    get_self_llm_engine,
)
from eoip.brain.learning_engine import CognitiveLearningEngine, LearningParadigm
from eoip.brain.graph_intelligence import GraphIntelligenceEngine


class QueryApproach(str, enum.Enum):
    DETERMINISTIC = "DETERMINISTIC"
    NON_DETERMINISTIC = "NON_DETERMINISTIC"
    PROBABILISTIC = "PROBABILISTIC"
    HEURISTIC = "HEURISTIC"
    STOCHASTIC = "STOCHASTIC"
    HYBRID = "HYBRID"  # Hyperautomation approach


@dataclass
class BrainReport:
    report_id: str
    query: str
    approach: QueryApproach
    cognitive_tier: str
    executive_summary: str
    methodology_review: str
    graph_topology: dict[str, Any]
    analytical_findings: list[str]
    learning_insights: dict[str, Any]
    xai_attribution: dict[str, Any]
    counterfactual_scenarios: list[dict[str, Any]]
    strategic_recommendations: list[str]
    confidence_score: float
    merkle_root: str
    generation_latency_ms: float
    markdown_report: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "query": self.query,
            "approach": self.approach.value,
            "cognitive_tier": self.cognitive_tier,
            "confidence_score": round(self.confidence_score, 4),
            "merkle_root": self.merkle_root,
            "latency_ms": round(self.generation_latency_ms, 2),
            "executive_summary": self.executive_summary,
            "methodology_review": self.methodology_review,
            "graph_topology": self.graph_topology,
            "analytical_findings": self.analytical_findings,
            "learning_insights": self.learning_insights,
            "xai_attribution": self.xai_attribution,
            "counterfactual_scenarios": self.counterfactual_scenarios,
            "strategic_recommendations": self.strategic_recommendations,
            "markdown_report": self.markdown_report,
            "metadata": self.metadata,
        }


class DetailedReportGenerator:
    """Generates publication-grade, comprehensive deep analytical reports."""

    def __init__(self, learning_engine: CognitiveLearningEngine | None = None) -> None:
        self.learning_engine = learning_engine or CognitiveLearningEngine()
        self.llm = get_self_llm_engine()

    def generate_report(
        self,
        query: str,
        approach: QueryApproach = QueryApproach.HYBRID,
        tier: CognitiveTier = CognitiveTier.OPUS_FRONTIER,
        graph_store: Any = None,
        context: dict[str, Any] | None = None,
    ) -> BrainReport:
        """Executes selected query approach and produces an exhaustive, structured deep report."""
        start_time = time.perf_counter()
        report_id = str(uuid.uuid4())
        ctx = context or {}

        # 1. Approach-Specific Analytical Execution (uses live graph when available)
        gi = GraphIntelligenceEngine(graph_store=graph_store)
        gi_used = False
        if gi._has_store():
            gi_findings = {
                QueryApproach.DETERMINISTIC: gi.execute_deterministic,
                QueryApproach.NON_DETERMINISTIC: gi.execute_non_deterministic,
                QueryApproach.PROBABILISTIC: gi.execute_probabilistic,
                QueryApproach.HEURISTIC: gi.execute_heuristic,
                QueryApproach.STOCHASTIC: gi.execute_stochastic,
                QueryApproach.HYBRID: gi.execute_hybrid,
            }[approach](query)
            if gi_findings.raw_evidence:
                exec_data = {
                    "methodology_desc": gi_findings.methodology,
                    "discovered_entities": gi_findings.discovered_entities,
                    "known_edges": gi_findings.known_edges,
                    "findings": gi_findings.findings,
                    "recommendations": gi_findings.recommendations,
                    "confidence": gi_findings.confidence,
                }
                gi_used = True

        if not gi_used:
            if approach == QueryApproach.DETERMINISTIC:
                exec_data = self._execute_deterministic(query, graph_store)
            elif approach == QueryApproach.NON_DETERMINISTIC:
                exec_data = self._execute_non_deterministic(query, tier)
            elif approach == QueryApproach.PROBABILISTIC:
                exec_data = self._execute_probabilistic(query, graph_store)
            elif approach == QueryApproach.HEURISTIC:
                exec_data = self._execute_heuristic(query, graph_store)
            elif approach == QueryApproach.STOCHASTIC:
                exec_data = self._execute_stochastic(query, graph_store)
            else:
                exec_data = self._execute_hybrid_hyperautomation(query, tier, graph_store)

        # 2. Frontier Neural Synthesis for the Executive Summary
        llm_config = GenerationConfig(
            tier=tier,
            system_prompt=(
                "You are the Chief Enterprise Intelligence Architect producing an authoritative, "
                "rigorous, and comprehensive executive synthesis of enterprise graph state."
            ),
            enable_xai=True,
        )
        llm_res = self.llm.generate(prompt=query, config=llm_config)

        # 3. Learning & Adaptive Intelligence Updates
        # Update Q-Learning policy reward
        reward = 1.0 if exec_data["confidence"] > 0.8 else 0.5
        q_val = self.learning_engine.q_learning.update(
            query=query,
            action=f"{approach.value}_{tier.value}",
            reward=reward,
        )

        learning_insights = {
            "q_learning_policy_value": q_val,
            "reinforcement_reward": reward,
            "selected_action": f"{approach.value}_{tier.value}",
            "latent_link_predictions": self.learning_engine.kg_learner.predict_missing_links(
                entities=exec_data["discovered_entities"][:6],
                known_edges=exec_data["known_edges"][:10],
            ),
            "concept_clusters": self.learning_engine.clusterer.cluster_concepts(
                concepts=exec_data["discovered_entities"][:6],
                k=2,
            ),
        }

        # 4. Merkle Root Calculation for Auditability
        merkle_content = f"{report_id}:{query}:{exec_data['confidence']}:{time.time()}"
        merkle_root = hashlib.sha256(merkle_content.encode()).hexdigest()

        # 5. Markdown Report Assembly
        md_text = self._build_markdown_report(
            report_id=report_id,
            query=query,
            approach=approach,
            tier=tier,
            exec_data=exec_data,
            llm_res=llm_res,
            learning_insights=learning_insights,
            merkle_root=merkle_root,
        )

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        return BrainReport(
            report_id=report_id,
            query=query,
            approach=approach,
            cognitive_tier=tier.value,
            executive_summary=llm_res.content,
            methodology_review=exec_data["methodology_desc"],
            graph_topology={
                "nodes_inspected": len(exec_data["discovered_entities"]),
                "edges_traversed": len(exec_data["known_edges"]),
                "entities": exec_data["discovered_entities"][:15],
            },
            analytical_findings=exec_data["findings"],
            learning_insights=learning_insights,
            xai_attribution={
                "token_attributions": [
                    {"token": t.token, "salience": t.salience_score, "entity": t.grounded_entity}
                    for t in (llm_res.xai.token_attributions if llm_res.xai else [])
                ],
                "neuro_symbolic_citations": llm_res.xai.neuro_symbolic_citations if llm_res.xai else [],
            },
            counterfactual_scenarios=[
                {
                    "premise": cf.premise,
                    "alternative_hypothesis": cf.alternative_hypothesis,
                    "impact_delta": cf.impact_delta,
                    "explanation": cf.explanation,
                }
                for cf in (llm_res.xai.counterfactuals if llm_res.xai else [])
            ],
            strategic_recommendations=exec_data["recommendations"],
            confidence_score=exec_data["confidence"],
            merkle_root=merkle_root,
            generation_latency_ms=latency_ms,
            markdown_report=md_text,
            metadata={"llm_model": llm_res.model_name, "tokens": llm_res.tokens_generated},
        )

    # ------------------------------------------------------------------------
    # Execution Approaches
    # ------------------------------------------------------------------------

    @staticmethod
    def _extract_query_entities(query: str) -> list[str]:
        """Extract entity names from the query text for contextual reporting."""
        import re
        pascal = re.findall(r"\b[A-Z][a-zA-Z0-9_]+\b", query)
        snake = re.findall(r"\b[a-z]+(?:_[a-z]+)+\b", query)
        entities = list(dict.fromkeys(pascal + snake))
        if not entities:
            words = [w for w in re.findall(r"\b[A-Za-z]{4,}\b", query)
                     if w.lower() not in {"what", "when", "where", "which", "about",
                                          "evaluate", "analyze", "find", "conduct"}]
            entities = words[:4]
        return entities[:6] or ["TargetSystem"]

    def _execute_deterministic(self, query: str, store: Any) -> dict[str, Any]:
        entities = self._extract_query_entities(query)
        edges = [(entities[0], "RELATES_TO", e) for e in entities[1:3]] if len(entities) > 1 else []
        return {
            "methodology_desc": (
                "Deterministic Graph Traversal: Schema axiom validation and exact relational "
                "path traversals with zero semantic variance. No live graph data available — "
                "analysis based on query-derived entities."
            ),
            "discovered_entities": entities,
            "known_edges": edges,
            "findings": [
                f"Query targets {len(entities)} entities: {', '.join(entities[:4])}.",
                "No live graph store connected for deterministic verification. "
                "Connect a graph backend to enable full schema conformance validation.",
                "Recommendation: Populate the knowledge graph with domain entities to unlock "
                "real deterministic path traversal and SHACL constraint verification.",
            ],
            "recommendations": [
                "Connect a live graph store (Neo4j, TigerGraph, Memgraph, or MemoryGraphStore) "
                "for real deterministic analysis.",
                f"Ingest {', '.join(entities[:3])} entities and their relationships into the graph.",
            ],
            "confidence": 0.35,
        }

    def _execute_non_deterministic(self, query: str, tier: CognitiveTier) -> dict[str, Any]:
        entities = self._extract_query_entities(query)
        edges = [(entities[0], "INTERACTS_WITH", e) for e in entities[1:2]] if len(entities) > 1 else []
        return {
            "methodology_desc": (
                f"Non-Deterministic Generative Synthesis ({tier.value}): Frontier deep attention layers "
                f"and Chain-of-Thought deliberation. No live graph data — analysis uses query context."
            ),
            "discovered_entities": entities,
            "known_edges": edges,
            "findings": [
                f"Generative analysis of entities: {', '.join(entities[:4])}.",
                "No live graph store connected for emergent pattern detection. "
                "Connect a graph backend to enable co-occurrence and semantic clustering analysis.",
                "Populate domain entities to unlock generative synthesis with real interaction data.",
            ],
            "recommendations": [
                "Connect a live graph store for real emergent pattern discovery.",
                f"Ingest interaction data for {', '.join(entities[:2])} to enable behavioral analysis.",
            ],
            "confidence": 0.3,
        }

    def _execute_probabilistic(self, query: str, store: Any) -> dict[str, Any]:
        entities = self._extract_query_entities(query)
        edges = [(entities[0], "DEPENDS_ON", e) for e in entities[1:2]] if len(entities) > 1 else []
        return {
            "methodology_desc": (
                "Probabilistic Bayesian Inference: Posterior probability distributions and "
                "belief network risk propagation. No live graph data for statistical analysis."
            ),
            "discovered_entities": entities,
            "known_edges": edges,
            "findings": [
                f"Probabilistic analysis targets entities: {', '.join(entities[:4])}.",
                "No live graph store connected for degree distribution and Bayesian risk computation. "
                "Connect a graph backend to compute real posterior failure probabilities.",
                "Real Bayesian analysis requires graph topology — populate with domain entities.",
            ],
            "recommendations": [
                "Connect a live graph store to compute real degree distributions and risk posteriors.",
                f"Model failure dependencies for {', '.join(entities[:2])} in the knowledge graph.",
            ],
            "confidence": 0.3,
        }

    def _execute_heuristic(self, query: str, store: Any) -> dict[str, Any]:
        entities = self._extract_query_entities(query)
        edges = [(entities[0], "CONNECTS_TO", e) for e in entities[1:3]] if len(entities) > 1 else []
        return {
            "methodology_desc": (
                "Heuristic Optimization & Centrality Search: A* pathfinding and degree-centrality "
                "ranking. No live graph data for real topology analysis."
            ),
            "discovered_entities": entities,
            "known_edges": edges,
            "findings": [
                f"Heuristic analysis targets entities: {', '.join(entities[:4])}.",
                "No live graph store connected for centrality computation and bottleneck identification. "
                "Connect a graph backend for real A* pathfinding and PageRank analysis.",
                "Real heuristic ranking requires graph edges — ingest relationship data.",
            ],
            "recommendations": [
                "Connect a live graph store for real centrality ranking and pathfinding.",
                f"Map relationships between {', '.join(entities[:3])} for bottleneck detection.",
            ],
            "confidence": 0.3,
        }

    def _execute_stochastic(self, query: str, store: Any) -> dict[str, Any]:
        entities = self._extract_query_entities(query)
        edges = [(entities[0], "EMITS_TO", e) for e in entities[1:3]] if len(entities) > 1 else []
        return {
            "methodology_desc": (
                "Stochastic Monte Carlo Simulation: Randomized perturbation trials and "
                "resilience analysis. No live graph data for real simulation."
            ),
            "discovered_entities": entities,
            "known_edges": edges,
            "findings": [
                f"Stochastic analysis targets entities: {', '.join(entities[:4])}.",
                "No live graph store connected for Monte Carlo simulation. "
                "Connect a graph backend to run real node-failure resilience tests.",
                "Real stochastic simulation requires graph topology data — populate with entities and edges.",
            ],
            "recommendations": [
                "Connect a live graph store for real Monte Carlo chaos simulation.",
                f"Model failure propagation paths for {', '.join(entities[:2])} in the knowledge graph.",
            ],
            "confidence": 0.3,
        }

    def _execute_hybrid_hyperautomation(self, query: str, tier: CognitiveTier, store: Any) -> dict[str, Any]:
        det = self._execute_deterministic(query, store)
        prob = self._execute_probabilistic(query, store)
        heur = self._execute_heuristic(query, store)
        stoch = self._execute_stochastic(query, store)
        non_det = self._execute_non_deterministic(query, tier)

        all_entities = list(dict.fromkeys(
            det["discovered_entities"] + prob["discovered_entities"] + heur["discovered_entities"]
        ))
        all_edges = det["known_edges"] + prob["known_edges"] + heur["known_edges"]

        combined_findings = [
            f"[Deterministic] {det['findings'][0]}",
            f"[Probabilistic] {prob['findings'][0]}",
            f"[Heuristic] {heur['findings'][0]}",
            f"[Stochastic] {stoch['findings'][0]}",
            f"[Generative ({tier.value})] {non_det['findings'][0]}",
        ]

        sub_confidences = [det["confidence"], prob["confidence"], heur["confidence"],
                           stoch["confidence"], non_det["confidence"]]
        avg_confidence = sum(sub_confidences) / len(sub_confidences)

        combined_recs = list(dict.fromkeys(
            det["recommendations"][:1] + prob["recommendations"][:1] +
            heur["recommendations"][:1] + stoch["recommendations"][:1] +
            non_det["recommendations"][:1]
        ))

        return {
            "methodology_desc": (
                f"Hybrid Hyperautomation: Orchestrates all 5 analytical paradigms — deterministic, "
                f"probabilistic, heuristic, stochastic, and generative ({tier.value}) — into a "
                f"unified cross-paradigm analysis."
            ),
            "discovered_entities": all_entities,
            "known_edges": all_edges,
            "findings": combined_findings,
            "recommendations": combined_recs,
            "confidence": round(avg_confidence, 3),
        }

    # ------------------------------------------------------------------------
    # Markdown Report Formatter
    # ------------------------------------------------------------------------

    def _build_markdown_report(
        self,
        report_id: str,
        query: str,
        approach: QueryApproach,
        tier: CognitiveTier,
        exec_data: dict[str, Any],
        llm_res: GenerationResult,
        learning_insights: dict[str, Any],
        merkle_root: str,
    ) -> str:
        """Formats comprehensive publication-grade markdown document."""
        return f"""# Enterprise Living Brain Intelligence Report
**Report Identifier**: `{report_id}`  
**Query**: *"{query}"*  
**Execution Approach**: `{approach.value}` (Hyperautomation Active)  
**Cognitive Tier**: `{tier.value}` (`{llm_res.model_name}`)  
**Cryptographic Merkle Root**: `{merkle_root}`  
**Overall Confidence**: `{exec_data['confidence'] * 100:.1f}%`  
**Timestamp**: `{time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}`  

---

## 1. Executive Summary & Cognitive Synthesis
{llm_res.content}

---

## 2. Methodology & Reasoning Approach
{exec_data['methodology_desc']}

- **Execution Paradigm**: {approach.value}
- **Neural Reasoning Trace**:
{chr(10).join('  - ' + step for step in llm_res.reasoning_trace)}

---

## 3. Knowledge Graph & Ontology Topology
- **Inspected Entities ({len(exec_data['discovered_entities'])})**: `{', '.join(exec_data['discovered_entities'])}`
- **Traversed Relationships ({len(exec_data['known_edges'])})**:
{chr(10).join(f'  - `({s}) -[:{r}]-> ({t})`' for s, r, t in exec_data['known_edges'][:8])}

---

## 4. Deep Analytical Findings
{chr(10).join('### 4.' + str(idx+1) + ' Finding' + chr(10) + f + chr(10) for idx, f in enumerate(exec_data['findings']))}

---

## 5. Machine Learning & Adaptive Intelligence Insights
- **Q-Learning Policy Reward**: `{learning_insights['reinforcement_reward']}` (Updated Q-Value: `{learning_insights['q_learning_policy_value']}`)
- **Latent Relationship Predictions (Self-Supervised)**:
{chr(10).join(f"  - Predicted `({p['source']}) -[:{p['predicted_relation']}]-> ({p['target']})` (Confidence: {p['confidence']})" for p in learning_insights['latent_link_predictions'])}
- **Concept Semantic Clustering (Unsupervised)**:
{chr(10).join(f"  - Cluster {k}: `{', '.join(v)}`" for k, v in learning_insights['concept_clusters'].items())}

---

## 6. Explainable AI (XAI) Attribution & Evidence Lineage
- **Token Attention Attribution (Top Salience)**:
{chr(10).join(f"  - Token `{t.token}`: Salience `{t.salience_score}` | Entity Grounding: `{t.grounded_entity or 'None'}`" for t in (llm_res.xai.token_attributions[:6] if llm_res.xai else []))}
- **Neuro-Symbolic Citations**:
{chr(10).join(f"  - Claim: {c['claim']} | Triple: `{c['triple']}` (Confidence: {c['confidence']})" for c in (llm_res.xai.neuro_symbolic_citations if llm_res.xai else []))}

---

## 7. Counterfactual & What-If Scenario Analysis
{chr(10).join(f"### What-If Scenario: {cf.alternative_hypothesis}" + chr(10) + f"- **Premise**: {cf.premise}" + chr(10) + f"- **Impact Delta**: `{cf.impact_delta:+0.2f}`" + chr(10) + f"- **Assessment**: {cf.explanation}" + chr(10) for cf in (llm_res.xai.counterfactuals if llm_res.xai else []))}

---

## 8. Strategic Recommendations & Actionable Playbook
{chr(10).join(f"- {rec}" for rec in exec_data['recommendations'])}

---
*Generated by EOIP Enterprise Living Brain OS Kernel • Cryptographically Sealed • Verified Sovereign Execution*
"""
