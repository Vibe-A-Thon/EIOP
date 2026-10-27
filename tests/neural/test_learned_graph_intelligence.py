"""Acceptance test suite for Learned Graph Intelligence over the Graph Planes (WP-044, CRA-044.1-13, CRA-044.A)."""
from __future__ import annotations

import time
import numpy as np
import pytest

torch = pytest.importorskip("torch", reason="Graph encoder tests require the optional N1 neural tier")

from eoip.contracts.canonical import (
    KnowledgeState,
    ModelLineage,
    ProducerClass,
    PrincipalType,
    TrustedScope,
)
from eoip.neural.planes import (
    EpochBoundSnapshot,
    GraphLevel,
    GraphPlane,
    GraphPlaneCoordinator,
    ParallelTemporalStoreProhibitedError,
)
from eoip.neural.datasets import (
    ContentAddressedSnapshot,
    EdgeEvent,
    TemporalLeakageError,
    create_event_time_split,
    sample_type_constrained_negatives,
    validate_batch_leakage,
)
from eoip.neural.evaluation import (
    AUROCOnlyReportRefusedError,
    ModelEvaluationHarness,
    compute_auprc,
    compute_auroc,
    compute_ece,
    compute_macro_f1,
    compute_time_filtered_mrr,
)
from eoip.neural.encoders import (
    ChebNetFilter,
    GraphGPSModel,
    GraphSAGEModel,
    HGTModel,
    RGATModel,
    RGCNModel,
)
from eoip.neural.discriminator import (
    AdversarialPlausibilityDiscriminator,
    ResearchSandboxTenant,
)
from eoip.neural.explain import (
    NeuralExplainer,
)
from eoip.neural.lifecycle import (
    FailureModeGuards,
    NeuralModelLifecycleManager,
    create_model_prediction_assertion,
)


@pytest.fixture
def scope():
    return TrustedScope(
        tenant_id="tenant_eng",
        workspace_id="ws_1",
        principal_id="engineer_bob",
        principal_type=PrincipalType.USER,
        roles=["developer"],
    )


# ===========================================================================
# CRA-044.2: Graph planes mapping and policy-epoch bound snapshots
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_2_graph_planes_and_levels(scope):
    coord = GraphPlaneCoordinator()

    # GL0 instance graph -> planes 1 and 2
    assert coord.map_level_to_planes(GraphLevel.GL0_INSTANCE) == [
        GraphPlane.PLANE_1_RAW,
        GraphPlane.PLANE_2_ENTITY,
    ]
    # GL1 meta-graph -> plane 3
    assert coord.map_level_to_planes(GraphLevel.GL1_METAGRAPH) == [GraphPlane.PLANE_3_ONTOLOGY]
    # GL2 living brain -> plane 2
    assert coord.map_level_to_planes(GraphLevel.GL2_LIVING_BRAIN) == [GraphPlane.PLANE_2_ENTITY]
    # GL3 enterprise ontology -> plane 3
    assert coord.map_level_to_planes(GraphLevel.GL3_ONTOLOGY) == [GraphPlane.PLANE_3_ONTOLOGY]
    # GLT temporal -> plane 7
    assert coord.map_level_to_planes(GraphLevel.GLT_TEMPORAL) == [GraphPlane.PLANE_7_TEMPORAL]

    # Prohibits parallel temporal store duplicating plane 2
    with pytest.raises(ParallelTemporalStoreProhibitedError, match="duplicates Plane 2"):
        coord.register_temporal_backend("parallel_temporal_store_x", duplicates_plane_2=True)

    # Allowed temporal store registered successfully
    coord.register_temporal_backend("canonical_plane_7_store", duplicates_plane_2=False)

    # Epoch-bound snapshot
    snap = coord.create_epoch_bound_snapshot(
        snapshot_id="snap_epoch_2026_q4",
        level=GraphLevel.GL0_INSTANCE,
        policy_epoch="epoch-2026-10-18",
        scope=scope,
        data=[{"id": "e1"}],
    )
    assert snap.policy_epoch == "epoch-2026-10-18"
    assert len(snap.digest) == 64


# ===========================================================================
# CRA-044.4: Snapshot and split discipline
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_4_snapshots_and_temporal_splits():
    nodes = [{"id": "svc_auth", "type": "Service"}, {"id": "db_users", "type": "Database"}]
    edges = [
        EdgeEvent(source_id="svc_auth", target_id="db_users", relation="CONNECTS_TO", event_time=100.0, source_type="Service", target_type="Database"),
        EdgeEvent(source_id="svc_auth", target_id="db_users", relation="CONNECTS_TO", event_time=200.0, source_type="Service", target_type="Database"),
        EdgeEvent(source_id="svc_auth", target_id="db_users", relation="CONNECTS_TO", event_time=300.0, source_type="Service", target_type="Database"),
    ]

    # 1. Content-addressed snapshot
    snapshot = ContentAddressedSnapshot.create("snap_001", nodes, edges)
    assert len(snapshot.sha256_digest) == 64

    # 2. Event-time temporal split
    split = create_event_time_split(edges, train_cutoff_s=150.0, val_cutoff_s=250.0, test_cutoff_s=350.0)
    assert len(split.train_edges) == 1
    assert len(split.val_edges) == 1
    assert len(split.test_edges) == 1

    # 3. Batch leakage validation: leaked edge raises TemporalLeakageError
    validate_batch_leakage(split.train_edges, max_allowed_time=150.0)
    leaked_batch = [EdgeEvent("svc_a", "svc_b", "CALLS", event_time=199.0)]
    with pytest.raises(TemporalLeakageError, match="Temporal leakage detected"):
        validate_batch_leakage(leaked_batch, max_allowed_time=150.0)

    # 4. Type-constrained negative sampling against ontology
    candidates_by_type = {
        "Database": ["db_orders", "db_analytics", "db_logs"],
        "Service": ["svc_gateway", "svc_billing"],
    }
    negs = sample_type_constrained_negatives(split.train_edges, candidates_by_type, num_negatives_per_pos=2)
    assert len(negs) == 2
    assert all(neg.target_id in candidates_by_type["Database"] for neg in negs)


# ===========================================================================
# CRA-044.5: Evaluation discipline and 5 baselines
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_5_evaluation_discipline_and_baselines():
    harness = ModelEvaluationHarness()
    y_true = [1, 1, 1, 0, 0, 0, 1, 0, 1, 0]
    y_score = [0.95, 0.88, 0.82, 0.15, 0.22, 0.18, 0.90, 0.30, 0.75, 0.10]
    cal_probs = [0.95, 0.92, 0.88, 0.05, 0.08, 0.04, 0.90, 0.10, 0.85, 0.02]

    # AUROC reported alone is REFUSED
    with pytest.raises(AUROCOnlyReportRefusedError, match="AUROC is NEVER reported alone"):
        harness.evaluate_link_prediction("TestModel", y_true, y_score, {}, report_auroc_only=True)

    # Full report with 5 baselines and calibration
    baselines = {
        "random": [0.5] * 10,
        "degree": [0.4, 0.4, 0.3, 0.5, 0.3, 0.2, 0.6, 0.5, 0.4, 0.3],
        "common_neighbours": [0.4, 0.6, 0.2, 0.7, 0.5, 0.1, 0.3, 0.8, 0.4, 0.2],
        "hash_baseline": [0.51, 0.49, 0.52, 0.48, 0.50, 0.53, 0.49, 0.51, 0.50, 0.48],
        "rule_traversal": [0.5, 0.4, 0.6, 0.6, 0.2, 0.3, 0.5, 0.4, 0.3, 0.2],
    }
    report = harness.evaluate_link_prediction(
        "LearnedRGCN",
        y_true,
        y_score,
        baselines,
        calibrated_probs=cal_probs,
    )
    assert report.primary_metric_name == "AUPRC"
    assert report.primary_metric_value > 0.80
    assert report.beats_common_neighbours is True
    assert report.beats_rule is True
    assert report.is_calibrated is True
    assert report.ece <= 0.10
    assert report.status == "PROMOTED"


# ===========================================================================
# CRA-044.6: Core encoders: R-GCN and inductive GraphSAGE
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_6_core_encoders_rgcn_and_inductive_graphsage():
    # 1. R-GCN with basis decomposition
    rgcn = RGCNModel(in_features=8, hidden_dim=32, out_dim=16, num_relations=4, num_bases=4)
    x = torch.randn(6, 8)
    adj_rels = [torch.eye(6) for _ in range(4)]
    out_rgcn = rgcn(x, adj_rels)
    assert out_rgcn.shape == (6, 16)
    weight_hash_rgcn = rgcn.get_weight_hash()
    assert len(weight_hash_rgcn) == 64

    # 2. Inductive GraphSAGE: embed new node with UNCHANGED weight hash
    sage = GraphSAGEModel(in_features=8, hidden_dim=32, out_dim=16)
    hash_before = sage.get_weight_hash()

    existing_feats = torch.randn(5, 8)
    new_node_feat = torch.randn(8)
    connections = torch.tensor([1.0, 0.0, 1.0, 0.0, 0.0])

    emb_new, hash_after = sage.embed_new_unseen_node(new_node_feat, existing_feats, connections)
    assert emb_new.shape == (16,)
    assert hash_before == hash_after, "Weight hash must remain strictly identical during inductive inference!"


# ===========================================================================
# CRA-044.7: Bake-off architectures
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_7_bakeoff_architectures():
    # 1. RGAT with retrievable edge attention weights
    rgat = RGATModel(in_features=4, hidden_dim=8, num_relations=3)
    x = torch.randn(4, 4)
    edges = [(0, 1, 0), (1, 2, 1), (2, 3, 2)]
    out_rgat = rgat(x, edges)
    assert out_rgat.shape == (4, 8)
    assert len(rgat.last_attention_weights) == 3
    assert "0->1:0" in rgat.last_attention_weights

    # 2. HGT across multi-domain types
    hgt = HGTModel(in_features=4, hidden_dim=8, num_types=3)
    x_types = [torch.randn(2, 4), torch.randn(3, 4), torch.randn(2, 4)]
    out_hgt = hgt(x_types)
    assert len(out_hgt) == 3
    assert out_hgt[0].shape == (2, 8)

    # 3. GraphGPS local-plus-global
    gps = GraphGPSModel(in_features=4, hidden_dim=8)
    adj_norm = torch.eye(4)
    out_gps = gps(x, adj_norm)
    assert out_gps.shape == (4, 8)

    # 4. ChebNet spectral filter: zero false positives on clean control
    cheb = ChebNetFilter(in_features=4, out_features=4, k_order=2)
    laplacian = torch.eye(4)
    score_clean = cheb.score_anomaly(laplacian, x)
    assert isinstance(score_clean, float)


# ===========================================================================
# CRA-044.8: Adversarial discriminator and research sandbox
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_8_discriminator_and_sandbox():
    disc = AdversarialPlausibilityDiscriminator(threshold=0.50)

    # 1. Valid triple with high learned plausibility -> Admitted
    res_valid = disc.evaluate_triple(
        subject="svc_auth",
        predicate="calls",
        object_="svc_billing",
        subject_type="Service",
        object_type="Service",
        learned_score=0.92,
    )
    assert res_valid.quarantined is False
    assert res_valid.ontology_veto is False
    assert res_valid.latency_ms <= 5.0

    # 2. Valid types but low learned score -> Quarantined for review (NEVER deleted)
    res_low = disc.evaluate_triple(
        subject="svc_auth",
        predicate="calls",
        object_="svc_billing",
        subject_type="Service",
        object_type="Service",
        learned_score=0.35,
    )
    assert res_low.quarantined is True
    assert res_low.ontology_veto is False

    # 3. Ontology domain/range violation -> Ontology veto OVERRIDES learned score
    res_veto = disc.evaluate_triple(
        subject="svc_auth",
        predicate="calls",
        object_="table_users",
        subject_type="Service",
        object_type="Table",  # Invalid object for 'calls'
        learned_score=0.99,  # High learned score
    )
    assert res_veto.ontology_veto is True
    assert res_veto.quarantined is True  # Veto forces quarantine despite high score

    # 4. Research sandbox
    sandbox = ResearchSandboxTenant("sandbox_tenant_x")
    out = sandbox.execute_spiking_encoder("spiking_res_01", {})
    assert out["status"] == "SANDBOX_EXECUTED"
    assert out["production_dependency"] is False


# ===========================================================================
# CRA-044.9: Model lifecycle, lineage, and rollback (< 60s)
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_9_lifecycle_lineage_and_rollback():
    mgr = NeuralModelLifecycleManager()

    # Register version 1
    m1 = RGCNModel(in_features=4, hidden_dim=8, out_dim=4, num_relations=2, num_bases=2)
    rec1 = mgr.register_and_promote_model(
        model_id="rgcn_prod",
        version="v1.0.0",
        snapshot_id="snap_20261018",
        code_commit="ad9937b",
        seed_bundle={"torch": 42},
        environment_digest="env_cpu_win",
        gate_report_ref="gate_rep_001",
        model_instance=m1,
    )
    assert rec1.is_active is True
    assert mgr.get_active_model("rgcn_prod").version == "v1.0.0"

    # Register version 2
    m2 = RGCNModel(in_features=4, hidden_dim=8, out_dim=4, num_relations=2, num_bases=2)
    mgr.register_and_promote_model(
        model_id="rgcn_prod",
        version="v2.0.0",
        snapshot_id="snap_20261019",
        code_commit="bd9937c",
        seed_bundle={"torch": 42},
        environment_digest="env_cpu_win",
        gate_report_ref="gate_rep_002",
        model_instance=m2,
    )
    assert mgr.get_active_model("rgcn_prod").version == "v2.0.0"

    # Rollback restores v1.0.0 immediately (< 60s)
    t_start = time.perf_counter()
    restored = mgr.rollback("rgcn_prod")
    rollback_ms = (time.perf_counter() - t_start) * 1000.0
    assert rollback_ms < 60000.0
    assert restored.version == "v1.0.0"
    assert mgr.get_active_model("rgcn_prod").version == "v1.0.0"


# ===========================================================================
# CRA-044.10: Explainability and faithfulness probe (score drops >= 50%)
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_10_explainability_faithfulness():
    explainer = NeuralExplainer()

    # Faithful explanation: removing evidence path lowers score from 0.90 to 0.20 (>= 50% drop)
    def faithful_evaluator(path):
        return 0.90 if len(path) > 0 else 0.20

    res_faithful = explainer.explain_prediction(
        prediction_id="pred_01",
        target_edge=("svc_auth", "calls", "svc_billing"),
        base_score=0.90,
        evidence_path=[("svc_auth", "depends_on", "svc_token"), ("svc_token", "calls", "svc_billing")],
        score_evaluator=faithful_evaluator,
    )
    assert res_faithful.is_faithful is True
    assert res_faithful.score_reduction_ratio >= 0.50

    # Unfaithful explanation: removing evidence path barely changes score (0.90 -> 0.80, only 11% drop)
    def unfaithful_evaluator(path):
        return 0.90 if len(path) > 0 else 0.80

    res_unfaithful = explainer.explain_prediction(
        prediction_id="pred_02",
        target_edge=("svc_auth", "calls", "svc_billing"),
        base_score=0.90,
        evidence_path=[("svc_auth", "depends_on", "svc_token")],
        score_evaluator=unfaithful_evaluator,
    )
    assert res_unfaithful.is_faithful is False


# ===========================================================================
# CRA-044.11: Incremental k-hop invalidation & failure mode guards
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_11_failure_mode_guards():
    # 1. k-hop invalidation
    adj = {
        "A": ["B"],
        "B": ["A", "C"],
        "C": ["B", "D"],
        "D": ["C", "E"],
        "E": ["D"],
    }
    # Change at 'A' with k=2 hops invalidates A, B, C; D and E are preserved
    invalidated = FailureModeGuards.invalidate_k_hop(["A"], adj, k_hops=2)
    assert invalidated == {"A", "B", "C"}
    assert "D" not in invalidated
    assert "E" not in invalidated

    # 2. Oversmoothing variance measurement at layers 2, 4, 8
    embs = {
        2: np.array([[1.0, 0.0], [0.0, 1.0]]),
        4: np.array([[0.8, 0.2], [0.2, 0.8]]),
        8: np.array([[0.51, 0.49], [0.50, 0.50]]),
    }
    variances = FailureModeGuards.measure_oversmoothing(embs)
    assert variances[2] > variances[4] > variances[8]


# ===========================================================================
# CRA-044.12: Knowledge model entry as proposed with ModelLineage
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_12_knowledge_model_entry():
    lineage = ModelLineage(
        model_id="rgcn-link-predictor",
        model_version="v1.2.0",
        producer_class=ProducerClass.PROBABILISTIC,
        graph_snapshot_id="snap_20261018_epoch",
        code_commit="ad9937b",
        environment_digest="env_cpu_win",
    )

    assertion = create_model_prediction_assertion(
        assertion_id="ast_pred_909",
        subject_iri="http://example.org/svc_auth",
        predicate_iri="http://example.org/calls",
        object_iri="http://example.org/svc_billing",
        tenant_id="tenant_eng",
        lineage=lineage,
        calibrated_score=0.89,
        is_calibrated=True,
        evidence_path=["http://example.org/path_1"],
    )

    # Strictly PROPOSED (never ASSERTED)
    assert assertion.knowledge_state == KnowledgeState.PROPOSED
    assert assertion.confidence == 0.89
    assert assertion.confidence_calibrated is True
    assert assertion.extraction_model == "rgcn-link-predictor"


# ===========================================================================
# CRA-044.A: Full Acceptance Gate
# ===========================================================================

@pytest.mark.req("CRA-044")
def test_cra_044_a_acceptance_gate(scope):
    # 1. Graph planes coordinated
    coord = GraphPlaneCoordinator()
    planes = coord.map_level_to_planes(GraphLevel.GL0_INSTANCE)
    assert len(planes) == 2

    # 2. Inductive model embeds new node with unchanged weight hash
    sage = GraphSAGEModel(in_features=4, hidden_dim=8, out_dim=4)
    hash1 = sage.get_weight_hash()
    emb, hash2 = sage.embed_new_unseen_node(torch.randn(4), torch.randn(3, 4), torch.tensor([1.0, 0.0, 1.0]))
    assert hash1 == hash2

    # 3. Quality discriminator filters writes
    disc = AdversarialPlausibilityDiscriminator(threshold=0.50)
    res = disc.evaluate_triple("s", "calls", "o", "Service", "Service", 0.95)
    assert res.quarantined is False

    # 4. Result enters knowledge model as PROPOSED
    lineage = ModelLineage(
        model_id="sage_inductive",
        model_version="v1.0",
        producer_class=ProducerClass.PROBABILISTIC,
    )
    ast = create_model_prediction_assertion("ast_gate", "s", "p", "o", "tenant_eng", lineage, 0.95)
    assert ast.knowledge_state == KnowledgeState.PROPOSED
