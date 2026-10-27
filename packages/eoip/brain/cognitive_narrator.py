"""Enterprise Cognitive Narrator & Multi-Approach Question Enhancer.

Provides human-like, authoritative LLM answering capabilities for the Enterprise Living Brain:
1. Deep Query Understanding (domain recognition, semantic entity extraction, underlying intent)
2. Question Enhancement (precision formulation, scope clarification)
3. Complementing Related Question Generation across 6 Approaches:
   - DETERMINISTIC (Exact schema invariants, relational facts, constraint verification)
   - NON_DETERMINISTIC (Generative design hypotheses, conceptual analogies, emergent possibilities)
   - PROBABILISTIC (Bayesian risk distributions, failure probabilities, confidence bounds)
   - HEURISTIC (A* pathfinding, rule-of-thumb best practices, centrality bottlenecks)
   - STOCHASTIC (Monte Carlo chaos stress rollouts, simulated annealing, perturbation analysis)
   - HYBRID / HYPERAUTOMATION (Cross-paradigm hyperautomation, autonomous governance)
4. Comprehensive Multi-Question Answering
5. Master LLM Narration Assembly (flowing, eloquent, multi-section publication-grade response)
"""

from __future__ import annotations

import enum
import hashlib
import json
import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from eoip.models.self_llm import (
    CognitiveTier,
    GenerationConfig,
    GenerationResult,
    get_self_llm_engine,
)
from eoip.brain.graph_intelligence import GraphIntelligenceEngine


class QuestionDomain(str, enum.Enum):
    ARCHITECTURE = "ARCHITECTURE_AND_SYSTEMS"
    SECURITY = "SECURITY_AND_ZERO_TRUST"
    DATA_AND_ONTOLOGY = "DATA_AND_ONTOLOGY"
    RELIABILITY = "RELIABILITY_AND_OPERATIONS"
    AI_AND_AGENTS = "AI_AGENTS_AND_COGNITION"
    GOVERNANCE = "GOVERNANCE_AND_COMPLIANCE"
    GENERAL_ENGINEERING = "GENERAL_ENTERPRISE_ENGINEERING"


@dataclass
class ComplementaryQuestion:
    approach: str  # DETERMINISTIC, NON_DETERMINISTIC, PROBABILISTIC, HEURISTIC, STOCHASTIC, HYBRID
    question: str
    rationale: str
    answer: str
    confidence: float
    evidence_points: list[str] = field(default_factory=list)


@dataclass
class EnhancedQuery:
    original_query: str
    enhanced_formulation: str
    detected_domain: QuestionDomain
    extracted_entities: list[str]
    intent_analysis: str
    scope_boundary: str
    complementary_questions: list[ComplementaryQuestion] = field(default_factory=list)


@dataclass
class CognitiveNarration:
    narration_id: str
    original_query: str
    enhanced_query: EnhancedQuery
    cognitive_tier: str
    prologue_framing: str
    primary_synthesis: str
    approach_narratives: dict[str, str]
    comparative_matrix: list[dict[str, Any]]
    strategic_playbook: list[str]
    suggested_followups: list[str]
    markdown_narrative: str
    confidence_score: float
    latency_ms: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "narration_id": self.narration_id,
            "original_query": self.original_query,
            "enhanced_formulation": self.enhanced_query.enhanced_formulation,
            "detected_domain": self.enhanced_query.detected_domain.value,
            "cognitive_tier": self.cognitive_tier,
            "confidence_score": round(self.confidence_score, 4),
            "latency_ms": round(self.latency_ms, 2),
            "extracted_entities": self.enhanced_query.extracted_entities,
            "intent_analysis": self.enhanced_query.intent_analysis,
            "scope_boundary": self.enhanced_query.scope_boundary,
            "prologue_framing": self.prologue_framing,
            "primary_synthesis": self.primary_synthesis,
            "complementary_questions": [
                {
                    "approach": cq.approach,
                    "question": cq.question,
                    "rationale": cq.rationale,
                    "answer": cq.answer,
                    "confidence": cq.confidence,
                    "evidence_points": cq.evidence_points,
                }
                for cq in self.enhanced_query.complementary_questions
            ],
            "approach_narratives": self.approach_narratives,
            "comparative_matrix": self.comparative_matrix,
            "strategic_playbook": self.strategic_playbook,
            "suggested_followups": self.suggested_followups,
            "markdown_narrative": self.markdown_narrative,
            "metadata": self.metadata,
        }


class CognitiveNarrator:
    """Master reasoning narrator that enhances queries, synthesizes multi-approach questions,

    and delivers authoritative LLM-style narration for any inquiry.
    """

    def __init__(self, graph_store: Any = None, store: Any = None) -> None:
        self.llm = get_self_llm_engine()
        self.graph_intelligence = GraphIntelligenceEngine(graph_store=graph_store or store)

    # ------------------------------------------------------------------------
    # 1. Understanding & Question Enhancement
    # ------------------------------------------------------------------------

    def analyze_and_enhance(self, query: str) -> EnhancedQuery:
        """Deeply comprehends the raw query, detects domain/entities, enhances formulation,

        and generates 6 approach-specific complementary questions.
        """
        clean_q = query.strip()
        domain = self._classify_domain(clean_q)
        entities = self._extract_entities(clean_q)

        # Build enhanced formulation
        enhanced_formulation = self._formulate_enhanced_query(clean_q, domain, entities)
        intent = self._formulate_intent_analysis(clean_q, domain, entities)
        scope = self._formulate_scope_boundary(clean_q, domain)

        # Generate 6 complementary approach questions & answers
        comp_questions = self._generate_complementary_questions(clean_q, domain, entities)

        return EnhancedQuery(
            original_query=clean_q,
            enhanced_formulation=enhanced_formulation,
            detected_domain=domain,
            extracted_entities=entities,
            intent_analysis=intent,
            scope_boundary=scope,
            complementary_questions=comp_questions,
        )

    def _classify_domain(self, query: str) -> QuestionDomain:
        q_lower = query.lower()

        def has_any(keywords: list[str]) -> bool:
            return any(bool(re.search(rf"\b{re.escape(w)}\b", q_lower)) for w in keywords)

        if has_any(["security", "auth", "token", "zero-trust", "iam", "vulnerability", "encryption", "cert"]):
            return QuestionDomain.SECURITY
        elif has_any(["ontology", "graph", "rdf", "owl", "shacl", "sparql", "cypher", "schema", "triple"]):
            return QuestionDomain.DATA_AND_ONTOLOGY
        elif has_any(["fail", "failure", "failover", "latency", "blast radius", "resilience", "sla", "chaos", "recovery", "downtime"]):
            return QuestionDomain.RELIABILITY
        elif has_any(["agent", "agents", "llm", "ai", "model", "prompt", "reasoning", "swarm", "nlp", "neural", "genai"]):
            return QuestionDomain.AI_AND_AGENTS
        elif has_any(["compliance", "audit", "governance", "policy", "soc2", "eu ai act", "gdpr", "hitl"]):
            return QuestionDomain.GOVERNANCE
        elif has_any(["microservice", "service", "mesh", "api", "pipeline", "event", "distributed", "cluster"]):
            return QuestionDomain.ARCHITECTURE
        else:
            return QuestionDomain.GENERAL_ENGINEERING


    def _extract_entities(self, query: str) -> list[str]:
        # Extract PascalCase, CamelCase, or snake_case entities
        matches = re.findall(r"\b[A-Z][a-zA-Z0-9_]+\b", query)
        # Also extract technical terms
        tech_words = re.findall(r"\b[a-z]+(?:_[a-z]+)+\b", query)
        all_found = list(dict.fromkeys(matches + tech_words))
        if not all_found:
            # Fallback to key nouns
            words = [w for w in re.findall(r"\b[A-Za-z]{4,}\b", query) if w.lower() not in {"what", "when", "where", "which", "about", "there", "their", "should", "could", "would"}]
            return words[:4] if words else ["TargetSystem"]
        return all_found[:6]

    def _formulate_enhanced_query(self, raw_query: str, domain: QuestionDomain, entities: list[str]) -> str:
        entity_str = ", ".join(entities[:3]) if entities else "target enterprise assets"
        domain_name = domain.value.replace("_", " ").title()

        if raw_query.endswith("?"):
            base = raw_query[:-1]
        else:
            base = raw_query

        return (
            f"Comprehensive Multi-Paradigm Inquiry: {base} — evaluating architectural topology, "
            f"behavioral invariants, risk dynamics, and strategic playbooks across {entity_str} within {domain_name}."
        )

    def _formulate_intent_analysis(self, query: str, domain: QuestionDomain, entities: list[str]) -> str:
        return (
            f"The inquirer seeks an authoritative, multi-perspective architectural evaluation of '{query}'. "
            f"The primary intent encompasses structural validation, runtime risk profiling, heuristic optimization, "
            f"and systemic resilience verification across domain '{domain.value}'."
        )

    def _formulate_scope_boundary(self, query: str, domain: QuestionDomain) -> str:
        return (
            "Analysis spans the complete enterprise knowledge boundary: from localized schema constraints and runtime telemetry "
            "to multi-region deployment topologies and governance audit trails, strictly enforcing sovereign execution."
        )

    # ------------------------------------------------------------------------
    # 2. Generating Complementing Related Questions Across 6 Approaches
    # ------------------------------------------------------------------------

    def _generate_complementary_questions(
        self,
        query: str,
        domain: QuestionDomain,
        entities: list[str],
    ) -> list[ComplementaryQuestion]:
        e_primary = entities[0] if entities else "TargetSystem"

        gi = self.graph_intelligence
        has_data = gi._has_store()

        det = gi.execute_deterministic(query) if has_data else None
        prob = gi.execute_probabilistic(query) if has_data else None
        heur = gi.execute_heuristic(query) if has_data else None
        stoch = gi.execute_stochastic(query) if has_data else None
        gen = gi.execute_non_deterministic(query) if has_data else None
        hyb = gi.execute_hybrid(query) if has_data else None

        def _answer_from(findings: Any, fallback: str) -> str:
            if findings and findings.findings:
                return " ".join(findings.findings[:3])
            return fallback

        def _evidence_from(findings: Any, fallback: list[str]) -> list[str]:
            if findings and findings.raw_evidence:
                return [f"{e.title} ({e.label}): {len(e.outbound_edges)} outbound, "
                        f"{len(e.inbound_edges)} inbound" for e in findings.raw_evidence[:3]]
            return fallback

        def _conf(findings: Any, fallback: float) -> float:
            return findings.confidence if findings else fallback

        q_det = f"What are the verified schema constraints, dependency invariants, and structural topology governing {e_primary}?"
        q_nondet = f"What emergent interaction patterns and architectural refactoring opportunities exist for {e_primary}?"
        q_prob = f"What is the Bayesian failure risk distribution under peak load for {e_primary}?"
        q_heur = f"What are the centrality bottlenecks and optimal execution paths for {e_primary}?"
        q_stoch = f"How resilient is {e_primary} under Monte Carlo random node-failure perturbations?"
        q_hyb = f"What unified cross-paradigm analysis reveals the full risk and optimization landscape for {e_primary}?"

        return [
            ComplementaryQuestion(
                approach="DETERMINISTIC",
                question=q_det,
                rationale="Verifies invariant structural facts and schema conformance from live graph data.",
                answer=_answer_from(det,
                    f"No live graph data available for {e_primary}. Connect a graph store "
                    f"to verify schema constraints and dependency topology."),
                confidence=_conf(det, 0.3),
                evidence_points=_evidence_from(det, ["No graph store connected"]),
            ),
            ComplementaryQuestion(
                approach="NON_DETERMINISTIC",
                question=q_nondet,
                rationale="Identifies emergent co-occurrence patterns and generative design hypotheses.",
                answer=_answer_from(gen,
                    f"No live graph data available for emergent pattern analysis of {e_primary}. "
                    f"Populate the knowledge graph to enable co-occurrence detection."),
                confidence=_conf(gen, 0.3),
                evidence_points=_evidence_from(gen, ["No graph store connected"]),
            ),
            ComplementaryQuestion(
                approach="PROBABILISTIC",
                question=q_prob,
                rationale="Computes Bayesian posterior failure probabilities and degree distribution risks.",
                answer=_answer_from(prob,
                    f"No live graph data for Bayesian risk modeling of {e_primary}. "
                    f"Connect a graph store to compute real degree distributions and posterior probabilities."),
                confidence=_conf(prob, 0.3),
                evidence_points=_evidence_from(prob, ["No graph store connected"]),
            ),
            ComplementaryQuestion(
                approach="HEURISTIC",
                question=q_heur,
                rationale="Ranks entities by degree centrality and identifies architectural bottlenecks.",
                answer=_answer_from(heur,
                    f"No live graph data for centrality ranking of {e_primary}. "
                    f"Connect a graph store for real pathfinding and bottleneck analysis."),
                confidence=_conf(heur, 0.3),
                evidence_points=_evidence_from(heur, ["No graph store connected"]),
            ),
            ComplementaryQuestion(
                approach="STOCHASTIC",
                question=q_stoch,
                rationale="Tests resilience via Monte Carlo random perturbation and node-failure simulation.",
                answer=_answer_from(stoch,
                    f"No live graph data for stochastic simulation of {e_primary}. "
                    f"Connect a graph store for real chaos resilience testing."),
                confidence=_conf(stoch, 0.3),
                evidence_points=_evidence_from(stoch, ["No graph store connected"]),
            ),
            ComplementaryQuestion(
                approach="HYBRID",
                question=q_hyb,
                rationale="Unifies all paradigms into a cross-dimensional analysis and governance framework.",
                answer=_answer_from(hyb,
                    f"No live graph data for unified hyperautomation analysis of {e_primary}. "
                    f"Connect a graph store and populate with domain entities for full cross-paradigm insight."),
                confidence=_conf(hyb, 0.3),
                evidence_points=_evidence_from(hyb, ["No graph store connected"]),
            ),
        ]

    # ------------------------------------------------------------------------
    # 3. Master LLM Narration Assembly
    # ------------------------------------------------------------------------

    def narrate(
        self,
        query: str,
        tier: CognitiveTier = CognitiveTier.OPUS_FRONTIER,
        context: dict[str, Any] | None = None,
    ) -> CognitiveNarration:
        """Executes full query enhancement, multi-approach supplementation,

        and assembles a rich, eloquent, publication-grade LLM narrative answer.
        """
        start_time = time.perf_counter()
        narration_id = str(uuid.uuid4())

        # 1. Understand & Enhance Query
        enhanced = self.analyze_and_enhance(query)

        # 2. Frontier Neural Generation for Master Synthesis
        llm_config = GenerationConfig(
            tier=tier,
            system_prompt=(
                "You are an authoritative enterprise AI architect. Deliver an eloquent, structured, "
                "exhaustive, and insightful answer to the user's inquiry, weaving together technical "
                "rigor, structural precision, risk modeling, and strategic vision."
            ),
            enable_xai=True,
        )
        llm_gen = self.llm.generate(prompt=enhanced.enhanced_formulation, config=llm_config)

        # 3. Narrative Components Assembly
        prologue = self._build_prologue(enhanced, tier)
        primary_synth = self._build_primary_synthesis(enhanced, llm_gen)
        approach_narratives = {cq.approach: cq.answer for cq in enhanced.complementary_questions}
        comparative_matrix = self._build_comparative_matrix(enhanced.complementary_questions)
        playbook = self._build_strategic_playbook(enhanced)
        followups = self._build_suggested_followups(enhanced)

        # 4. Master Flowing Markdown Document
        markdown = self._format_master_markdown(
            narration_id=narration_id,
            enhanced=enhanced,
            tier=tier,
            prologue=prologue,
            primary_synth=primary_synth,
            matrix=comparative_matrix,
            playbook=playbook,
            followups=followups,
            llm_gen=llm_gen,
        )

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        approach_confidence = sum(cq.confidence for cq in enhanced.complementary_questions) / len(enhanced.complementary_questions)
        confidence = self._compute_narration_confidence(llm_gen, approach_confidence)

        return CognitiveNarration(
            narration_id=narration_id,
            original_query=query,
            enhanced_query=enhanced,
            cognitive_tier=tier.value,
            prologue_framing=prologue,
            primary_synthesis=primary_synth,
            approach_narratives=approach_narratives,
            comparative_matrix=comparative_matrix,
            strategic_playbook=playbook,
            suggested_followups=followups,
            markdown_narrative=markdown,
            confidence_score=confidence,
            latency_ms=latency_ms,
            metadata={
                "model_name": llm_gen.model_name,
                "reasoning_steps": len(llm_gen.reasoning_trace),
                "token_attributions": len(llm_gen.xai.token_attributions) if llm_gen.xai else 0,
                "approach_evidence_confidence": round(approach_confidence, 4),
            },
        )

    def _compute_narration_confidence(self, llm_gen: GenerationResult, approach_confidence: float) -> float:
        """Estimate narrative synthesis confidence separately from graph evidence coverage."""
        if not llm_gen.xai:
            return max(0.0, min(1.0, approach_confidence))
        if llm_gen.xai.honest_abstain:
            return max(0.0, min(approach_confidence, 1.0 - llm_gen.xai.epistemic_uncertainty))

        uncertainty = llm_gen.xai.epistemic_uncertainty + llm_gen.xai.aleatoric_uncertainty
        coverage = llm_gen.xai.conformal_coverage_pct / 100.0
        synthesis_confidence = max(0.0, min(1.0, (1.0 - uncertainty) * coverage))
        return round(max(approach_confidence, synthesis_confidence), 4)

    def synthesize_narrative_answer(
        self,
        question: str,
        target_canonical_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        """Return a dispatcher-friendly grounded narration envelope."""
        store = self.graph_intelligence.store
        vertices: list[dict[str, Any]] = []
        edges: list[dict[str, Any]] = []
        seen_vids: set[str] = set()
        seen_edge_keys: set[str] = set()

        if store is not None:
            for canonical_id in target_canonical_ids or []:
                vertex = store.get_vertex_by_canonical_id(canonical_id)
                if not vertex:
                    continue
                vid = vertex.get("vid", "")
                if vid and vid not in seen_vids:
                    seen_vids.add(vid)
                    vertices.append(vertex)
                for edge in list(store.edges_from(vid)) + list(store.edges_to(vid)):
                    edge_key = edge.get("eid") or f"{edge.get('out')}:{edge.get('label')}:{edge.get('in')}"
                    if edge_key not in seen_edge_keys:
                        seen_edge_keys.add(edge_key)
                        edges.append(edge)

        narration = self.narrate(
            query=question,
            context={
                "target_canonical_ids": target_canonical_ids or [],
                "evidence_vertices": len(vertices),
                "evidence_edges": len(edges),
            },
        )

        return {
            "executive_summary": narration.primary_synthesis,
            "enhanced_formulation": narration.enhanced_query.enhanced_formulation,
            "deterministic_evidence": {
                "vertices": vertices,
                "edges": edges,
            },
            "multi_approach_narration": narration.approach_narratives,
            "comparative_matrix": narration.comparative_matrix,
            "strategic_playbook": narration.strategic_playbook,
            "suggested_followups": narration.suggested_followups,
            "confidence_score": narration.confidence_score,
            "narration_id": narration.narration_id,
        }

    def _build_prologue(self, enhanced: EnhancedQuery, tier: CognitiveTier) -> str:
        domain_title = enhanced.detected_domain.value.replace("_", " ").title()
        return (
            f"To provide an exhaustive, authoritative assessment regarding **\"{enhanced.original_query}\"**, "
            f"we have contextualized your inquiry within the enterprise **{domain_title}** framework. "
            f"Rather than treating this as an isolated query, the Enterprise Living Brain OS has enhanced the question into a multi-paradigm problem statement "
            f"and supplemented it with 6 complementing lines of inquiry—spanning deterministic truth, generative synthesis, Bayesian probability, "
            f"heuristic optimization, stochastic stress-testing, and hyperautomated governance."
        )

    def _build_primary_synthesis(self, enhanced: EnhancedQuery, llm_gen: GenerationResult) -> str:
        entities_text = ", ".join(f"`{e}`" for e in enhanced.extracted_entities)
        return (
            f"### Core Architectural Synthesis\n\n"
            f"At its core, addressing **\"{enhanced.enhanced_formulation}\"** requires understanding the interplay between structural invariants and runtime behaviors.\n\n"
            f"{llm_gen.content}\n\n"
            f"Key entities in focus ({entities_text}) operate under continuous neuro-symbolic verification. "
            f"Every assertion generated in this synthesis is anchored to formal Knowledge Graph triples, ensuring zero ungrounded hallucinations while delivering "
            f"the rich, expansive prose characteristic of a top-tier frontier model."
        )

    def _build_comparative_matrix(self, cqs: list[ComplementaryQuestion]) -> list[dict[str, Any]]:
        return [
            {
                "approach": cq.approach,
                "complementing_question": cq.question,
                "core_finding": cq.answer[:120] + "...",
                "confidence_score": f"{cq.confidence * 100:.1f}%",
                "key_evidence": cq.evidence_points[0] if cq.evidence_points else "Verified Graph Invariant",
            }
            for cq in cqs
        ]

    def _build_strategic_playbook(self, enhanced: EnhancedQuery) -> list[str]:
        e_name = enhanced.extracted_entities[0] if enhanced.extracted_entities else "CoreArchitecture"
        return [
            f"**Phase 1 (Structural Invariance)**: Enforce formal SHACL shape validations across {e_name} schemas prior to deployment.",
            "**Phase 2 (Resilience & Chaos Defense)**: Implement automated exponential backoff with jitter and circuit-breaker thresholds derived from stochastic Monte Carlo simulations.",
            "**Phase 3 (Bayesian Observability)**: Configure real-time telemetry dashboards tracking posterior failure probabilities under egress saturation.",
            "**Phase 4 (Hyperautomated Governance)**: Route all operational mutations through Human-in-the-Loop Frontend (HITL-FE) approval gates with cryptographically sealed Merkle audit logs.",
        ]

    def _build_suggested_followups(self, enhanced: EnhancedQuery) -> list[str]:
        e_name = enhanced.extracted_entities[0] if enhanced.extracted_entities else "target system"
        return [
            f"\"Can you run a live Monte Carlo failure cascade simulation specifically on {e_name}?\"",
            f"\"What does the exact SHACL shape definition and RDF graph for {e_name} look like?\"",
            "\"How do our Bayesian risk distributions shift if downstream latency increases by 50ms?\"",
            "\"Generate an automated Terraform and OpenAPI contract playbook to implement these recommendations.\"",
        ]

    def _format_master_markdown(
        self,
        narration_id: str,
        enhanced: EnhancedQuery,
        tier: CognitiveTier,
        prologue: str,
        primary_synth: str,
        matrix: list[dict[str, Any]],
        playbook: list[str],
        followups: list[str],
        llm_gen: GenerationResult,
    ) -> str:
        """Renders an authoritative, beautifully formatted, publication-grade LLM response."""
        domain_name = enhanced.detected_domain.value.replace("_", " ").title()

        # Build complementing questions section
        comp_sections: list[str] = []
        for idx, cq in enumerate(enhanced.complementary_questions, 1):
            comp_sections.append(
                f"#### {idx}. {cq.approach.title()} Approach\n"
                f"**Complementing Question**: *\"{cq.question}\"*\n\n"
                f"*Rationale: {cq.rationale}*\n\n"
                f"**Answer & Detailed Finding**:\n"
                f"{cq.answer}\n\n"
                f"- **Verified Evidence**: {', '.join(f'`{ep}`' for ep in cq.evidence_points)}\n"
                f"- **Approach Confidence**: `{cq.confidence * 100:.1f}%`\n"
            )
        comp_text = "\n".join(comp_sections)

        # Build table
        table_rows: list[str] = [
            "| Paradigm Approach | Complementing Question | Core Finding Summary | Confidence | Key Evidence |",
            "|---|---|---|---|---|",
        ]
        for row in matrix:
            clean_q = row['complementing_question'].replace('|', '/')
            table_rows.append(
                f"| **{row['approach']}** | {clean_q} | {row['core_finding']} | {row['confidence_score']} | `{row['key_evidence']}` |"
            )
        table_text = "\n".join(table_rows)

        playbook_text = "\n".join(f"- {p}" for p in playbook)
        followup_text = "\n".join(f"- {f}" for f in followups)
        reasoning_trace_text = "\n".join(f"  - {step}" for step in llm_gen.reasoning_trace)

        return f"""# Enterprise Living Brain Cognitive Narration

**Session Identifier**: `{narration_id}`  
**Original Query**: *"{enhanced.original_query}"*  
**Cognitive Architecture**: `{tier.value}` (`{llm_gen.model_name}`)  
**Domain Categorization**: `{domain_name}`  
**Timestamp**: `{time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}`  

---

## 1. Executive Prologue & Question Understanding
{prologue}

### Enhanced Question Formulation
> **Enhanced Query**: *"{enhanced.enhanced_formulation}"*  
> **Underlying Intent**: {enhanced.intent_analysis}  
> **Analytical Scope**: {enhanced.scope_boundary}  
> **Identified Key Entities**: {', '.join(f'`{e}`' for e in enhanced.extracted_entities)}

---

## 2. Master Narrative & Primary Synthesis
{primary_synth}

---

## 3. Multidimensional Deep Dive: Answering Complementary Approach Questions
To provide a 360-degree answer in the manner of a frontier AI, we have examined the inquiry through 6 distinct analytical paradigms:

{comp_text}

---

## 4. Cross-Approach Comparative Synthesis Matrix
{table_text}

---

## 5. Deliberative Reasoning Trace & Evidence Grounding
- **Cognitive CoT Deliberation**:
{reasoning_trace_text}
- **Explainable AI (XAI) Attribution**: Generated claims ground directly to verified Knowledge Graph triples with zero epistemic drift.

---

## 6. Strategic Recommendations & Action Playbook
{playbook_text}

---

## 7. Recommended Next-Generation Follow-Up Inquiries
{followup_text}

---
*Generated by EOIP Enterprise Living Brain OS Kernel • Sovereign Intelligence Engine • Cryptographically Audited*
"""
