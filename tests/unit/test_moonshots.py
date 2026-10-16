"""Unit and integration tests for Moonshots 1, 2, 3, 4, 5, 8, 9, 10."""

from __future__ import annotations

import time
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from eoip.moonshot.bitemporal_state_machine import (
    BitemporalDelta,
    BitemporalStateMachine,
)
from eoip.moonshot.causal_simulator import (
    CausalGraphSimulator,
)
from eoip.moonshot.compliance_twin import (
    AutonomousComplianceTwin,
)
from eoip.moonshot.confidential_graph import (
    EnclaveDLPInterceptor,
    HomomorphicPropertyEncryptor,
    ZeroKnowledgeEvidenceVerifier,
)
from eoip.moonshot.generative_studio import (
    DynamicDomainPackSynthesizer,
    SchemaInductionEngine,
)
from eoip.moonshot.neuro_symbolic_memory import (
    AdaptiveGraphAttentionMemory,
    NeuroSymbolicGuardrail,
)
from eoip.moonshot.self_healing import (
    AutonomousRemediationEngine,
    GraphDriftDetector,
)
from eoip.moonshot.universal_transpiler import (
    PhantomVirtualGraphView,
    UniversalAST,
    UniversalTranspiler,
)
from eoip.moonshot.router import build_moonshot_router


# ==============================================================================
# Moonshot 1: Bitemporal State Machine & Time-Warp Replay
# ==============================================================================

def test_moonshot1_bitemporal_state_machine_and_time_warp():
    sm = BitemporalStateMachine(tenant_id="tenant-alpha")
    assert sm.list_branches() == ["main"]

    t0 = 1000.0
    t1 = 2000.0
    t2 = 3000.0

    # Commit at t0
    sm.commit("main", "srv-billing", {"status": "ACTIVE", "tier": "gold"}, valid_from=t0, tx_time=t0)
    # Commit update at t1
    sm.commit("main", "srv-billing", {"status": "MAINTENANCE"}, valid_from=t1, tx_time=t1)

    # Time-warp replay at t0
    state_t0 = sm.time_warp_replay("main", valid_at=t0, tx_at=t0)
    assert state_t0["srv-billing"]["status"] == "ACTIVE"
    assert state_t0["srv-billing"]["tier"] == "gold"

    # Time-warp replay at t1
    state_t1 = sm.time_warp_replay("main", valid_at=t1, tx_at=t1)
    assert state_t1["srv-billing"]["status"] == "MAINTENANCE"
    assert state_t1["srv-billing"]["tier"] == "gold"

    # Virtual branching
    sm.branch("sim/experiment", from_branch="main")
    assert "sim/experiment" in sm.list_branches()

    # Commit on experiment branch
    sm.commit("sim/experiment", "srv-billing", {"status": "RETIRED"}, valid_from=t2, tx_time=t2)
    state_exp = sm.time_warp_replay("sim/experiment", valid_at=t2, tx_at=t2)
    assert state_exp["srv-billing"]["status"] == "RETIRED"

    # Verify main is untouched
    state_main = sm.time_warp_replay("main", valid_at=t2, tx_at=t2)
    assert state_main["srv-billing"]["status"] == "MAINTENANCE"

    # Diff branches
    diff = sm.diff_branches("main", "sim/experiment")
    assert "srv-billing" in diff["modified"]

    # CRDT Merge
    merge_commit = sm.merge_crdt(target_branch="main", source_branch="sim/experiment")
    assert merge_commit is not None
    assert sm.verify_chain_integrity("main") is True


# ==============================================================================
# Moonshot 2: Confidential Graph & ZK Evidence Proofs
# ==============================================================================

def test_moonshot2_confidential_graph_and_zk_proofs():
    # 1. Homomorphic Property Encryptor
    enc = HomomorphicPropertyEncryptor()
    c1 = enc.encrypt_numeric(50)
    c2 = enc.encrypt_numeric(75)
    c3 = c1 + c2
    assert enc.decrypt_numeric(c3) == 125

    # Searchable encryption
    tok1 = enc.searchable_token("secret_customer_ssn")
    tok2 = enc.searchable_token("secret_customer_ssn")
    tok3 = enc.searchable_token("other_term")
    assert tok1 == tok2
    assert tok1 != tok3

    # Encrypt node properties
    props = {"revenue": 1000, "email": "alice@corp.com", "public_flag": True}
    enc_props = enc.encrypt_node_properties(props)
    assert "enc_num_revenue" in enc_props
    assert "token_email" in enc_props

    # 2. Zero-Knowledge Evidence Proof
    path = ["User:Alice", "Role:Admin", "Service:Vault", "Secret:ProdKey"]
    proof = ZeroKnowledgeEvidenceVerifier.generate_path_proof(path)
    assert proof.hop_count == 3
    assert ZeroKnowledgeEvidenceVerifier.verify_path_proof(proof, "User:Alice", "Secret:ProdKey") is True
    assert ZeroKnowledgeEvidenceVerifier.verify_path_proof(proof, "User:Bob", "Secret:ProdKey") is False

    # 3. Enclave DLP Interceptor
    enclave = EnclaveDLPInterceptor()
    raw_query = "MATCH (n:Account) WHERE n.secret_key = 'KEY-9999' RETURN n"
    masked = enclave.mask_query(raw_query, sensitive_terms=["KEY-9999"])
    assert "KEY-9999" not in masked
    assert "enclave_" in masked

    unmasked = enclave.unmask_result({"result": masked})
    assert "KEY-9999" in unmasked["result"]


# ==============================================================================
# Moonshot 3: Causal GNN Simulator & Counterfactual Probing
# ==============================================================================

def test_moonshot3_causal_gnn_simulator():
    sim = CausalGraphSimulator()
    sim.add_node("auth-svc", "Service", resilience=0.3, criticality=2.0)
    sim.add_node("api-gateway", "Service", resilience=0.6, criticality=1.5)
    sim.add_node("payment-svc", "Service", resilience=0.5, criticality=3.0)
    sim.add_node("db-cluster", "Database", resilience=0.9, criticality=5.0)

    sim.add_edge("api-gateway", "auth-svc", coupling_strength=0.9)
    sim.add_edge("api-gateway", "payment-svc", coupling_strength=0.85)
    sim.add_edge("payment-svc", "db-cluster", coupling_strength=0.7)

    # Initial shock at api-gateway
    result = sim.simulate_cascade({"api-gateway": 1.0}, max_steps=5)
    assert result.total_steps >= 2
    assert "api-gateway" in result.collapsed_nodes
    assert result.systemic_loss_score > 0.0

    # Counterfactual probe: Harden auth-svc and payment-svc
    probe = sim.counterfactual_probe(
        baseline_shock={"api-gateway": 1.0},
        interventions={"auth-svc": 0.95, "payment-svc": 0.95},
    )
    assert probe["loss_reduction"] >= 0.0
    assert probe["effective_roi"] >= 0.0


# ==============================================================================
# Moonshot 4: Self-Healing Active Graph Fabric
# ==============================================================================

def test_moonshot4_self_healing_fabric():
    detector = GraphDriftDetector()
    engine = AutonomousRemediationEngine()

    entities = [
        {"id": "svc-orphan", "type": "Service"},
        {"id": "sa-legacy", "type": "ServiceAccount", "created_at": time.time() - (120 * 86400)},
        {"id": "ui-portal", "type": "Frontend"},
        {"id": "db-sql", "type": "Database"},
    ]
    edges = [
        {"from": "ui-portal", "to": "db-sql", "from_type": "Frontend", "to_type": "Database", "type": "DIRECT_CALL"},
    ]

    violations = detector.scan_graph(entities, edges)
    assert len(violations) >= 3

    # Generate remediation for each
    actions = [engine.generate_remediation(v) for v in violations]
    action_types = {a.action_type for a in actions}
    assert "JIRA_TICKET" in action_types
    assert "TERRAFORM_FIX" in action_types
    assert "GIT_PR" in action_types

    # Test approval workflow
    high_risk_act = [a for a in actions if a.risk_level in ("R3", "R4")][0]
    with pytest.raises(PermissionError):
        engine.approve_action(high_risk_act.action_id, approver="junior-dev", approver_role="engineer")

    engine.approve_action(high_risk_act.action_id, approver="security-lead", approver_role="Lead Admin")
    dispatch_res = engine.dispatch_action(high_risk_act.action_id)
    assert dispatch_res["dispatched"] is True


# ==============================================================================
# Moonshot 5: Universal Multi-Dialect Transpiler & Virtual Views
# ==============================================================================

def test_moonshot5_universal_transpiler_and_virtual_views():
    transpiler = UniversalTranspiler()
    cypher_input = "MATCH (s:Service) WHERE s.tier = 'critical' RETURN s LIMIT 25"

    ast = transpiler.parse_cypher_or_gql(cypher_input)
    assert ast.anchor_label == "Service"
    assert ast.filters[0]["field"] == "tier"
    assert ast.filters[0]["value"] == "critical"
    assert ast.limit == 25

    gremlin = transpiler.to_gremlin(ast)
    assert "g.V().hasLabel('Service').has('tier', 'critical').limit(25)" == gremlin

    cypher_out = transpiler.to_cypher(ast)
    assert "MATCH (s:Service) WHERE s.tier = 'critical' RETURN s LIMIT 25" == cypher_out

    gql_out = transpiler.to_gql(ast)
    assert gql_out == cypher_out

    sparql = transpiler.to_sparql(ast)
    assert "SELECT ?s WHERE { ?s a :Service . ?s :tier 'critical' . } LIMIT 25" == sparql

    sql_pgq = transpiler.to_sql_pgq(ast)
    assert "GRAPH_TABLE" in sql_pgq

    # Zero-ETL Virtual Graph View
    raw_records = [
        {"id": "s1", "tier": "critical", "name": "PaymentGW"},
        {"id": "s2", "tier": "low", "name": "Logger"},
        {"id": "s3", "tier": "critical", "name": "AuthService"},
    ]
    virtual_view = PhantomVirtualGraphView("services_table", raw_records, id_col="id", label="Service")
    matches = virtual_view.query(ast)
    assert len(matches) == 2
    assert {m["id"] for m in matches} == {"s1", "s3"}


# ==============================================================================
# Moonshot 8: Adaptive Graph Attention Memory & Neuro-Symbolic Brain
# ==============================================================================

def test_moonshot8_neuro_symbolic_memory():
    agam = AdaptiveGraphAttentionMemory()
    mem1 = agam.record_interaction("Incident INC-123 was caused by Redis connection exhaustion", connected_entities=["Incident", "Redis"])
    mem2 = agam.record_interaction("Deployment of auth service requires rolling update", connected_entities=["AuthService"])

    # Attention retrieval
    results = agam.retrieve_relevant("Redis incident connection")
    assert len(results) >= 1
    assert results[0].memory_id == mem1.memory_id

    # Neuro-Symbolic Guardrail
    guardrail = NeuroSymbolicGuardrail(
        allowed_vertex_types={"Service", "Incident", "Person", "Repository"},
        allowed_edge_types={"DEPENDS_ON", "OWNED_BY", "CAUSED_BY"},
    )
    ok, err = guardrail.validate_action("create_vertex", {"label": "Service"})
    assert ok is True

    ok, err = guardrail.validate_action("create_vertex", {"label": "ForbiddenAlienType"})
    assert ok is False
    assert "Symbolic Guardrail Rejection" in str(err)

    ok, err = guardrail.validate_action("delete_graph", {})
    assert ok is False


# ==============================================================================
# Moonshot 9: Enterprise Governance & Autonomous Compliance Twin
# ==============================================================================

def test_moonshot9_compliance_twin():
    twin = AutonomousComplianceTwin(tenant_id="enterprise-1")

    # Generate AI-BOM
    active_models = [
        {"id": "m1", "name": "llama3.2-local", "version": "3.2.1", "license": "Llama-3.2-Community"},
        {"id": "m2", "name": "bge-embeddings", "version": "1.5", "license": "MIT"},
    ]
    aibom = twin.generate_ai_bom(active_models)
    assert len(aibom.components) == 2
    assert len(aibom.cryptographic_seal) == 64

    # Compliance Evaluation
    report = twin.evaluate_compliance(
        framework="EU_AI_ACT",
        system_stats={
            "audit_logging_enabled": True,
            "model_transparency_docs": True,
            "hitl_approval_required": True,
            "no_egress_default": True,
        },
    )
    assert report["compliance_score_percent"] == 100.0
    assert report["controls_passed"] == 4
    assert len(report["evidence_package_seal"]) == 64


# ==============================================================================
# Moonshot 10: Generative Knowledge Studio & Dynamic Domain Pack Synthesizer
# ==============================================================================

def test_moonshot10_generative_studio():
    engine = SchemaInductionEngine()
    synthesizer = DynamicDomainPackSynthesizer()

    sample_orders = [
        {"id": 1001, "customer_id": 42, "total_price": 99.99, "is_fulfilled": True, "created_at": "2026-10-09"},
        {"id": 1002, "customer_id": 43, "total_price": 149.50, "is_fulfilled": False, "created_at": "2026-10-09"},
    ]

    entity, relations = engine.induce_schema("orders", sample_orders)
    assert entity.entity_label == "Order"
    assert entity.key_field == "id"
    assert len(relations) == 1
    assert relations[0].edge_label == "REL_CUSTOMER"

    pack = synthesizer.synthesize_pack("Commerce", domain="Retail", entities=[entity], relations=relations)
    assert pack["pack_id"] == "pack-commerce"
    assert "type Order {" in pack["graphql_sdl"]
    assert len(pack["signature"]) == 64


# ==============================================================================
# FastAPI Router TestClient Integration
# ==============================================================================

def test_moonshot_router_endpoints():
    app = FastAPI()
    app.include_router(build_moonshot_router())
    client = TestClient(app)

    # 1. Bitemporal
    resp = client.post("/api/v1/moonshot/bitemporal/branch", json={"new_branch": "test-branch"})
    assert resp.status_code == 200

    resp = client.post("/api/v1/moonshot/bitemporal/time-warp", json={"branch": "main", "valid_at": 1000})
    assert resp.status_code == 200

    # 2. ZK Proof
    resp = client.post("/api/v1/moonshot/confidential/zk-proof", json={"path_nodes": ["A", "B", "C"]})
    assert resp.status_code == 200
    assert resp.json()["verified"] is True

    # 3. Causal Simulation
    resp = client.post("/api/v1/moonshot/causal/simulate", json={
        "nodes": [{"id": "s1", "resilience": 0.5}],
        "edges": [],
        "shocks": {"s1": 1.0},
    })
    assert resp.status_code == 200

    # 4. Self-healing drift scan
    resp = client.post("/api/v1/moonshot/self-healing/scan", json={
        "entities": [{"id": "srv1", "type": "Service"}],
        "edges": [],
    })
    assert resp.status_code == 200

    # 5. Transpilation
    resp = client.post("/api/v1/moonshot/transpile", json={
        "query": "MATCH (n:Service) WHERE n.tier = 'gold' RETURN n",
        "target_dialect": "GREMLIN",
    })
    assert resp.status_code == 200
    assert "g.V()" in resp.json()["transpiled_query"]

    # 8. Memory consolidation
    resp = client.post("/api/v1/moonshot/memory/consolidate", json={
        "content": "User discussed payment SLA issue",
        "connected_entities": ["PaymentService"],
    })
    assert resp.status_code == 200

    # 9. Compliance audit
    resp = client.post("/api/v1/moonshot/compliance/audit", json={
        "framework": "EU_AI_ACT",
        "system_stats": {"audit_logging_enabled": True},
    })
    assert resp.status_code == 200

    # 10. Studio Induction
    resp = client.post("/api/v1/moonshot/studio/induce", json={
        "dataset_name": "tickets",
        "records": [{"id": 1, "title": "Crash", "user_id": 5}],
    })
    assert resp.status_code == 200
    assert resp.json()["pack_id"] == "pack-tickets"
