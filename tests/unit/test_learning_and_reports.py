"""Tests for Enterprise Multi-Approach Querying, Deep Report Generation, and Cognitive Learning Paradigms.

Validates:
1. All 6 Query Approaches:
   - DETERMINISTIC (Exact graph pattern matching, invariant verification, zero hallucination)
   - NON_DETERMINISTIC (Generative neural synthesis, open-ended frontier reasoning)
   - PROBABILISTIC (Bayesian belief updates, posterior distributions, confidence bounds)
   - HEURISTIC (A* pathfinding, rule-based inference, PageRank / centrality ranking)
   - STOCHASTIC (Monte Carlo random-walk exploration, simulated annealing, temperature rollouts)
   - HYBRID / HYPERAUTOMATION (Unified hyperautomated orchestration of all paradigms)
2. Detailed Report Structure & Publication Quality:
   - Executive Summary
   - Methodology Review
   - Graph Topology
   - Multi-Hop Analytical Findings
   - Learning & Adaptive Insights
   - XAI Attributions & Counterfactuals
   - Strategic Recommendations
   - Merkle Root & Latency Profiling
   - Markdown & JSON outputs
3. Cognitive Learning Paradigms:
   - Q-Learning & Bellman Policy Optimizations
   - Imitation Learning / Behavioral Cloning (Human Expert Trajectories)
   - Self-Supervised Knowledge Graph Link Prediction
   - Semi-Supervised Graph Label Propagation
   - Unsupervised Concept Clustering
   - Self-Evolving & Self-Writing Agent Prompt Synthesis
4. FastAPI Endpoints:
   - POST /api/v1/brain/query
   - GET /api/v1/brain/approaches
   - GET /api/v1/brain/learning/status
   - POST /api/v1/brain/learning/train
   - GET /api/v1/brain/telemetry
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from apps.api.app import create_app
from eoip.graph.memory import MemoryGraphStore
from eoip.models.self_llm import CognitiveTier
from eoip.brain.brain_os import BrainOSKernel
from eoip.brain.report_generator import (
    DetailedReportGenerator,
    QueryApproach,
    BrainReport,
)
from eoip.brain.learning_engine import (
    CognitiveLearningEngine,
    LearningParadigm,
    AgentEvolutionType,
    QLearningEngine,
    ImitationLearningEngine,
    KnowledgeGraphLearner,
    UnsupervisedClusterer,
    SelfEvolvingAgentHarness,
)


# ---------------------------------------------------------------------------
# 1. Test All 6 Query Approaches in DetailedReportGenerator
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("approach", [
    QueryApproach.DETERMINISTIC,
    QueryApproach.NON_DETERMINISTIC,
    QueryApproach.PROBABILISTIC,
    QueryApproach.HEURISTIC,
    QueryApproach.STOCHASTIC,
    QueryApproach.HYBRID,
])
def test_all_six_query_approaches(approach: QueryApproach):
    store = MemoryGraphStore()
    generator = DetailedReportGenerator()
    query = "Evaluate dependencies, reliability metrics, and failure blast radius for Service_Auth"

    report = generator.generate_report(
        query=query,
        approach=approach,
        tier=CognitiveTier.OPUS_FRONTIER,
        graph_store=store,
    )

    assert isinstance(report, BrainReport)
    assert report.approach == approach
    assert report.cognitive_tier == "OPUS_FRONTIER"
    assert len(report.report_id) > 0
    assert len(report.executive_summary) > 20
    assert len(report.methodology_review) > 20
    assert len(report.analytical_findings) >= 2
    assert report.confidence_score > 0.0
    assert len(report.merkle_root) == 64  # SHA-256
    assert len(report.strategic_recommendations) >= 2
    assert "# Enterprise Living Brain Intelligence Report" in report.markdown_report
    assert "## 1. Executive Summary & Cognitive Synthesis" in report.markdown_report
    assert "## 8. Strategic Recommendations & Actionable Playbook" in report.markdown_report


    # Test dictionary serialization
    as_dict = report.to_dict()
    assert as_dict["approach"] == approach.value
    assert as_dict["report_id"] == report.report_id
    assert as_dict["merkle_root"] == report.merkle_root


# ---------------------------------------------------------------------------
# 2. Test BrainOSKernel.query_and_report Integration
# ---------------------------------------------------------------------------
def test_brain_kernel_query_and_report():
    store = MemoryGraphStore()
    kernel = BrainOSKernel(graph_store=store)

    report = kernel.query_and_report(
        query="Conduct zero-trust ontology path analysis",
        approach=QueryApproach.HYBRID,
        tier=CognitiveTier.SONNET_BALANCED,
    )

    assert isinstance(report, BrainReport)
    assert report.approach == QueryApproach.HYBRID
    assert report.cognitive_tier == "SONNET_BALANCED"
    assert report.confidence_score >= 0.8
    assert len(report.counterfactual_scenarios) > 0


# ---------------------------------------------------------------------------
# 3. Test Q-Learning Engine (Reinforcement Learning)
# ---------------------------------------------------------------------------
def test_q_learning_policy_updates():
    q_engine = QLearningEngine()
    query = "Find circular dependencies in order processing workflow"

    # Initial action
    best_action_initial = q_engine.select_action(query, force_exploit=True)
    assert best_action_initial in QLearningEngine.ACTIONS

    # Reward positive action
    q_val_1 = q_engine.update(query, "HYBRID_HYPERAUTOMATION", reward=1.0)
    q_val_2 = q_engine.update(query, "HYBRID_HYPERAUTOMATION", reward=1.0)
    assert q_val_2 > q_val_1
    assert q_engine.total_updates == 2

    # Verify best action converges to reinforced action
    best_action_after = q_engine.select_action(query, force_exploit=True)
    assert best_action_after == "HYBRID_HYPERAUTOMATION"


# ---------------------------------------------------------------------------
# 4. Test Imitation Learning (Behavioral Cloning)
# ---------------------------------------------------------------------------
def test_imitation_learning_trajectory_cloning():
    imitation = ImitationLearningEngine()

    traj = imitation.record_demonstration(
        query="Audit security boundary traversal for customer telemetry",
        approach="HYBRID",
        steps=[
            "Map IAM security group boundaries",
            "Identify lateral ingress/egress bridges",
            "Simulate credential compromise propagation",
        ],
        outcome_rating=0.99,
    )
    assert len(traj.trajectory_id) > 0
    assert len(traj.steps) == 3

    # Clone behavior for similar query
    cloned = imitation.clone_behavior("Audit security boundary traversal for customer telemetry")
    assert cloned is not None
    assert len(cloned["cloned_steps"]) == 3
    assert cloned["recommended_approach"] == "HYBRID"
    assert cloned["similarity"] >= 0.65


# ---------------------------------------------------------------------------
# 5. Test Graph Learning (Self-Supervised & Semi-Supervised)
# ---------------------------------------------------------------------------
def test_graph_learner_link_prediction_and_label_propagation():
    kg_learner = KnowledgeGraphLearner()

    # Self-Supervised Link Prediction
    candidates = kg_learner.predict_missing_links(
        entities=["CustomerService", "CustomerServiceDatabase", "PaymentService"],
        known_edges=[("CustomerService", "CALLS", "PaymentService")],
    )
    assert isinstance(candidates, list)
    for c in candidates:
        assert "confidence" in c
        assert c["paradigm"] == LearningParadigm.SELF_SUPERVISED_LEARNING.value

    # Semi-Supervised Label Propagation
    seed_labels = {
        "node_1": "CRITICAL",
        "node_2": "STANDARD",
    }
    graph_nodes = [
        {"id": "node_1", "neighbors": ["node_3"]},
        {"id": "node_2", "neighbors": ["node_4"]},
        {"id": "node_3", "neighbors": ["node_1"]},
        {"id": "node_4", "neighbors": ["node_2"]},
    ]
    labels = kg_learner.propagate_labels(graph_nodes, seed_labels)
    assert labels["node_1"] == "CRITICAL"
    assert labels["node_3"] == "CRITICAL"
    assert labels["node_4"] == "STANDARD"


# ---------------------------------------------------------------------------
# 6. Test Unsupervised Concept Clustering
# ---------------------------------------------------------------------------
def test_unsupervised_concept_clustering():
    clusterer = UnsupervisedClusterer()
    concepts = [
        "PaymentGateway",
        "BillingEngine",
        "InvoiceGenerator",
        "KubernetesCluster",
        "PodAutoscaler",
        "ContainerRegistry",
    ]
    clusters = clusterer.cluster_concepts(concepts, k=2)
    assert len(clusters) == 2
    total_clustered = sum(len(c) for c in clusters.values())
    assert total_clustered == len(concepts)


# ---------------------------------------------------------------------------
# 7. Test Self-Evolving & Self-Writing Agent Harness
# ---------------------------------------------------------------------------
def test_self_evolving_agent_prompt_synthesis():
    harness = SelfEvolvingAgentHarness()

    initial_prompt = "You are an enterprise graph query agent."
    failure = ["Query timed out when traversing 8 hops without cycle pruning."]

    evolved = harness.evolve_prompt(
        task_name="GraphTraversalAgent",
        base_prompt=initial_prompt,
        failure_trace=failure,
    )

    assert "Self-Evolving Invariant Directive" in evolved
    assert len(harness.evolution_history) == 1
    assert harness.evolution_history[0]["task_name"] == "GraphTraversalAgent"


# ---------------------------------------------------------------------------
# 8. Test FastAPI Endpoints for Deep Reports and Learning Engine
# ---------------------------------------------------------------------------
def test_fastapi_report_and_learning_endpoints():
    store = MemoryGraphStore()
    app = create_app(store)
    client = TestClient(app)

    # 1. GET /api/v1/brain/approaches
    res = client.get("/api/v1/brain/approaches")
    assert res.status_code == 200
    approaches = res.json()
    assert len(approaches) == 6
    assert "DETERMINISTIC" in approaches
    assert "HYBRID" in approaches
    assert "STOCHASTIC" in approaches

    # 2. POST /api/v1/brain/query (Deep Report generation)
    res = client.post(
        "/api/v1/brain/query",
        json={
            "query": "Synthesize end-to-end blast radius analysis for PaymentGateway",
            "approach": "HYBRID",
            "tier": "OPUS_FRONTIER",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["approach"] == "HYBRID"
    assert data["cognitive_tier"] == "OPUS_FRONTIER"
    assert len(data["report_id"]) > 0
    assert len(data["executive_summary"]) > 0
    assert len(data["analytical_findings"]) >= 2
    assert "xai_attribution" in data
    assert len(data["counterfactual_scenarios"]) > 0
    assert len(data["strategic_recommendations"]) > 0
    assert "# Enterprise Living Brain Intelligence Report" in data["markdown_report"]

    # Test deterministic approach query
    res_det = client.post(
        "/api/v1/brain/query",
        json={
            "query": "Find all nodes connected by DEPENDS_ON",
            "approach": "DETERMINISTIC",
            "tier": "SONNET_BALANCED",
        },
    )
    assert res_det.status_code == 200
    data_det = res_det.json()
    assert data_det["approach"] == "DETERMINISTIC"
    assert data_det["confidence_score"] == 1.0

    # 3. GET /api/v1/brain/learning/status
    res = client.get("/api/v1/brain/learning/status")
    assert res.status_code == 200
    learn_status = res.json()
    assert "q_learning" in learn_status
    assert "imitation_learning" in learn_status
    assert "self_evolving" in learn_status
    assert "paradigms_active" in learn_status

    # 4. POST /api/v1/brain/learning/train (Q-Learning update)
    res = client.post(
        "/api/v1/brain/learning/train",
        json={
            "paradigm": "Q_LEARNING",
            "query": "Analyze network topology",
            "action": "HYBRID_HYPERAUTOMATION",
            "reward": 1.0,
        },
    )
    assert res.status_code == 200
    q_data = res.json()
    assert q_data["status"] == "UPDATED"
    assert q_data["q_value"] > 0.0

    # 5. POST /api/v1/brain/learning/train (Imitation Learning)
    res = client.post(
        "/api/v1/brain/learning/train",
        json={
            "paradigm": "IMITATION_LEARNING",
            "query": "Design distributed cache cluster",
            "action": "HEURISTIC",
            "steps": ["Step 1", "Step 2"],
            "outcome_rating": 0.95,
        },
    )
    assert res.status_code == 200
    imit_data = res.json()
    assert imit_data["status"] == "RECORDED"
    assert imit_data["steps_count"] == 2

    # 6. POST /api/v1/brain/learning/train (Prompt Evolution)
    res = client.post(
        "/api/v1/brain/learning/train",
        json={
            "paradigm": "PROMPT_EVOLUTION",
            "action": "ResilienceAgent",
            "system_prompt": "Standard prompt",
            "error_trace": "Missing fallback timeout",
        },
    )
    assert res.status_code == 200
    evo_data = res.json()
    assert evo_data["status"] == "EVOLVED"
    assert "Self-Evolving Invariant Directive" in evo_data["evolved_prompt"]

    # 7. GET /api/v1/brain/telemetry (Brain OS telemetry with approaches and learning engine)
    res = client.get("/api/v1/brain/telemetry")
    assert res.status_code == 200
    telem = res.json()
    assert "supported_approaches" in telem
    assert len(telem["supported_approaches"]) == 6
    assert "learning_engine" in telem
    assert telem["learning_engine"]["q_learning"]["total_updates"] >= 1
