"""Tests for Enterprise Cognitive Narrator & Multi-Approach Question Enhancer.

Validates:
1. Deep Query Understanding & Domain Classification (Architecture, Security, Reliability, Data, Governance)
2. Question Enhancement into high-precision technical formulations
3. Generation of 6 Complementing Related Questions across:
   - DETERMINISTIC (Exact schema invariants & dependency constraints)
   - NON_DETERMINISTIC (Generative design hypotheses & conceptual analogies)
   - PROBABILISTIC (Bayesian posterior distributions & risk probabilities)
   - HEURISTIC (A* pathfinding, rule-of-thumb best practices & bottleneck ranking)
   - STOCHASTIC (Monte Carlo chaos stress rollouts & simulated annealing)
   - HYBRID / HYPERAUTOMATION (Cross-paradigm hyperautomation & HITL governance)
4. Comprehensive Multi-Question Answering with verified evidence
5. Master LLM Narration Assembly:
   - Executive Prologue
   - Master Narrative & Primary Synthesis
   - 6 Approach Answers in flowing prose
   - Comparative Synthesis Matrix
   - Strategic Recommendations Playbook
   - Suggested Next-Generation Follow-Up Inquiries
6. BrainOSKernel Integration (`narrate_query`, `ask` with narration metadata)
7. FastAPI Endpoint `POST /api/v1/brain/narrate`
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from apps.api.app import create_app
from eoip.graph.memory import MemoryGraphStore
from eoip.models.self_llm import CognitiveTier
from eoip.brain.brain_os import BrainOSKernel
from eoip.brain.cognitive_narrator import (
    CognitiveNarrator,
    CognitiveNarration,
    EnhancedQuery,
    ComplementaryQuestion,
    QuestionDomain,
)


# ---------------------------------------------------------------------------
# 1. Test Query Understanding & Domain Classification
# ---------------------------------------------------------------------------
def test_query_understanding_and_domains():
    narrator = CognitiveNarrator()

    # Security query
    sec_enh = narrator.analyze_and_enhance("How do we audit token leakage and zero-trust IAM boundaries?")
    assert sec_enh.detected_domain == QuestionDomain.SECURITY
    assert len(sec_enh.extracted_entities) > 0

    # Reliability query
    rel_enh = narrator.analyze_and_enhance("Evaluate blast radius and latency spikes during database cluster failover")
    assert rel_enh.detected_domain == QuestionDomain.RELIABILITY

    # Data & Ontology query
    onto_enh = narrator.analyze_and_enhance("Validate RDF schema invariants and SHACL constraints for payment ontology")
    assert onto_enh.detected_domain == QuestionDomain.DATA_AND_ONTOLOGY

    # Architecture query
    arch_enh = narrator.analyze_and_enhance("Design a high-throughput microservice mesh with event-driven pipelines")
    assert arch_enh.detected_domain == QuestionDomain.ARCHITECTURE


# ---------------------------------------------------------------------------
# 2. Test Question Enhancement & 6 Complementary Questions Generation
# ---------------------------------------------------------------------------
def test_question_enhancement_and_six_approach_questions():
    narrator = CognitiveNarrator()
    raw_query = "What happens if the PaymentGateway service experiences a sudden outage?"

    enhanced = narrator.analyze_and_enhance(raw_query)

    assert isinstance(enhanced, EnhancedQuery)
    assert enhanced.original_query == raw_query
    assert len(enhanced.enhanced_formulation) > len(raw_query)
    assert "Comprehensive Multi-Paradigm Inquiry" in enhanced.enhanced_formulation
    assert len(enhanced.intent_analysis) > 30
    assert len(enhanced.scope_boundary) > 30

    # Exactly 6 complementing approach questions generated
    assert len(enhanced.complementary_questions) == 6
    approaches = [cq.approach for cq in enhanced.complementary_questions]
    assert approaches == [
        "DETERMINISTIC",
        "NON_DETERMINISTIC",
        "PROBABILISTIC",
        "HEURISTIC",
        "STOCHASTIC",
        "HYBRID",
    ]

    for cq in enhanced.complementary_questions:
        assert isinstance(cq, ComplementaryQuestion)
        assert len(cq.question) > 15
        assert len(cq.rationale) > 15
        assert len(cq.answer) > 30
        assert 0.0 < cq.confidence <= 1.0
        assert len(cq.evidence_points) > 0


# ---------------------------------------------------------------------------
# 3. Test Master LLM Narration Assembly & Flowing Output
# ---------------------------------------------------------------------------
def test_master_llm_narration_assembly():
    narrator = CognitiveNarrator()
    query = "Analyze circular dependencies between OrderService and InventoryVault"

    narration = narrator.narrate(query, tier=CognitiveTier.OPUS_FRONTIER)

    assert isinstance(narration, CognitiveNarration)
    assert len(narration.narration_id) > 0
    assert narration.cognitive_tier == "OPUS_FRONTIER"
    assert len(narration.prologue_framing) > 50
    assert len(narration.primary_synthesis) > 50
    assert len(narration.approach_narratives) == 6
    assert len(narration.comparative_matrix) == 6
    assert len(narration.strategic_playbook) >= 3
    assert len(narration.suggested_followups) >= 3
    assert narration.confidence_score > 0.0

    # Check Markdown Narration structure
    md = narration.markdown_narrative
    assert "# Enterprise Living Brain Cognitive Narration" in md
    assert "## 1. Executive Prologue & Question Understanding" in md
    assert "### Enhanced Question Formulation" in md
    assert "## 2. Master Narrative & Primary Synthesis" in md
    assert "## 3. Multidimensional Deep Dive: Answering Complementary Approach Questions" in md
    assert "#### 1. Deterministic Approach" in md
    assert "#### 6. Hybrid Approach" in md
    assert "## 4. Cross-Approach Comparative Synthesis Matrix" in md
    assert "## 5. Deliberative Reasoning Trace & Evidence Grounding" in md
    assert "## 6. Strategic Recommendations & Action Playbook" in md
    assert "## 7. Recommended Next-Generation Follow-Up Inquiries" in md

    # Check dictionary serialization
    as_dict = narration.to_dict()
    assert as_dict["narration_id"] == narration.narration_id
    assert as_dict["original_query"] == query
    assert len(as_dict["complementary_questions"]) == 6
    assert len(as_dict["markdown_narrative"]) > 500


# ---------------------------------------------------------------------------
# 4. Test BrainOSKernel Integration
# ---------------------------------------------------------------------------
def test_brain_kernel_cognitive_narrator_integration():
    store = MemoryGraphStore()
    kernel = BrainOSKernel(graph_store=store)

    # 1. Direct narrate_query() call
    narration = kernel.narrate_query(
        query="Explain resilience strategies for multi-region Kafka clusters",
        tier=CognitiveTier.SONNET_BALANCED,
    )
    assert isinstance(narration, CognitiveNarration)
    assert narration.cognitive_tier == "SONNET_BALANCED"
    assert len(narration.approach_narratives) == 6

    # 2. ask() method enriching metadata with narration & enhanced question
    ans = kernel.ask(
        query="Evaluate security boundaries for customer database access",
        tier=CognitiveTier.OPUS_FRONTIER,
    )
    assert ans.mode == "HYBRID"
    assert "narration" in ans.metadata
    assert "enhanced_formulation" in ans.metadata
    assert "Comprehensive Multi-Paradigm Inquiry" in ans.metadata["enhanced_formulation"]
    assert len(ans.metadata["narration"]["complementary_questions"]) == 6

    # 3. Telemetry reporting cognitive narrator capabilities
    telemetry = kernel.get_system_telemetry()
    assert "cognitive_narrator" in telemetry
    assert telemetry["cognitive_narrator"]["status"] == "OPERATIONAL"
    assert telemetry["cognitive_narrator"]["approaches_supported"] == 6


# ---------------------------------------------------------------------------
# 5. Test FastAPI POST /api/v1/brain/narrate Endpoint
# ---------------------------------------------------------------------------
def test_fastapi_narrate_endpoint():
    store = MemoryGraphStore()
    app = create_app(store)
    client = TestClient(app)

    res = client.post(
        "/api/v1/brain/narrate",
        json={
            "query": "How do we prevent cascading connection pool exhaustion in our API gateway?",
            "tier": "OPUS_FRONTIER",
        },
    )

    assert res.status_code == 200
    data = res.json()

    assert len(data["narration_id"]) > 0
    assert "enhanced_formulation" in data
    assert "Comprehensive Multi-Paradigm Inquiry" in data["enhanced_formulation"]
    assert data["cognitive_tier"] == "OPUS_FRONTIER"
    assert len(data["complementary_questions"]) == 6
    assert len(data["approach_narratives"]) == 6
    assert len(data["comparative_matrix"]) == 6
    assert len(data["strategic_playbook"]) >= 3
    assert len(data["suggested_followups"]) >= 3
    assert "# Enterprise Living Brain Cognitive Narration" in data["markdown_narrative"]
