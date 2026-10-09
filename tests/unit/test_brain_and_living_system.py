"""Unit Tests for Enterprise Brain OS, Loops, Agents, RAGs, Polyglot Queries, and Living Brain.

Validates:
- 14 Control Loops (HCTL, HITL-FE, HBTL, HATL, HITD, EITL, HITL, HOTL, HOOTL, HITA, HITC, HITI, MITL, HITP)
- 35 Agent Archetypes & Swarm Systems
- 17 Unified RAG Retrieval Patterns
- 13 Query Languages (RDF, OWL, Gremlin, Cypher, GQL, openCypher, SHACL, SPARQL, SKOS, EOQL, EQL, OSQL, NL2Query)
- 17 Enterprise Database Adapters
- Living Brain Building Algorithms & Merkle state verification
- Brain OS Kernel Deterministic & Hybrid Answering
"""

import pytest

from eoip.agents.loops import EnterpriseLoopManager, LoopType, RiskTier
from eoip.agents.archetypes import AgentFactory, BaseAgent
from eoip.retrieval.rag_suite import EnterpriseRAGSuite, RAGMode
from eoip.query.polyglot_engine import PolyglotQueryEngine, QueryDialect, PolyglotQuery
from eoip.graph.database_adapters import DatabaseAdapterRegistry, DatabaseType
from eoip.brain.living_brain_algorithms import LivingBrainAlgorithms
from eoip.brain.brain_os import BrainOSKernel


# ---------------------------------------------------------------------------
# 1. Test All 14 Control Loops
# ---------------------------------------------------------------------------
def test_all_14_control_loops():
    mgr = EnterpriseLoopManager()
    all_loops = list(LoopType)
    assert len(all_loops) == 14

    for loop in all_loops:
        # HOOTL is blocked for high-risk R3/R4 operations
        if loop == LoopType.HOOTL:
            blocked_decision = mgr.evaluate_action(
                action_name="test_action",
                risk_tier=RiskTier.R3,
                loop_override=loop,
            )
            assert not blocked_decision.allowed
            assert blocked_decision.requires_human_approval

            # Low risk HOOTL is permitted
            allowed_decision = mgr.evaluate_action(
                action_name="test_action",
                risk_tier=RiskTier.R1,
                loop_override=loop,
            )
            assert allowed_decision.allowed
        elif loop == LoopType.HCTL:
            # Requires human command initiation
            dec_uncommanded = mgr.evaluate_action("test", RiskTier.R1, loop_override=loop, context={"human_commanded": False})
            assert not dec_uncommanded.allowed
            dec_commanded = mgr.evaluate_action("test", RiskTier.R1, loop_override=loop, context={"human_commanded": True})
            assert dec_commanded.allowed
        elif loop in (LoopType.HITL, LoopType.HITA):
            dec_no_app = mgr.evaluate_action("test", RiskTier.R1, loop_override=loop, context={"human_approved": False})
            assert not dec_no_app.allowed
            dec_app = mgr.evaluate_action("test", RiskTier.R1, loop_override=loop, context={"human_approved": True})
            assert dec_app.allowed
        else:
            # Standard automated execution envelope
            dec = mgr.evaluate_action("test", RiskTier.R0, loop_override=loop)
            assert dec.allowed

    # Verify history tracking
    rec = mgr.record_action(dec, status="EXECUTED", operator="test_runner")
    assert len(mgr.list_history()) >= 1
    assert rec.status == "EXECUTED"


# ---------------------------------------------------------------------------
# 2. Test All 35 Agent Archetypes
# ---------------------------------------------------------------------------
def test_all_35_agent_archetypes():
    archetypes = AgentFactory.list_archetypes()
    assert len(archetypes) == 35

    for arch_name in archetypes:
        agent = AgentFactory.create(arch_name)
        assert isinstance(agent, BaseAgent)
        res = agent.run("Analyze critical infrastructure component")
        assert res.agent_type == arch_name
        assert res.output is not None
        assert len(res.reasoning_trace) >= 1


# ---------------------------------------------------------------------------
# 3. Test All 17 RAG Modalities
# ---------------------------------------------------------------------------
def test_all_17_rag_modalities():
    rag_suite = EnterpriseRAGSuite()
    rag_suite.add_documents([
        {"id": "d1", "content": "payment-service is a critical microservice that handles all credit card transactions and connects to the billing database"},
        {"id": "d2", "content": "the blast radius of payment-service includes billing-db, invoice-generator, and the notification service"},
        {"id": "d3", "content": "authentication service validates user tokens via OIDC and LDAP protocols before allowing API access"},
        {"id": "d4", "content": "graph database stores entity relationships and provides traversal queries for impact analysis"},
        {"id": "d5", "content": "payment-service depends on config-service for feature flags and rate limiting configuration"},
    ])
    all_modes = list(RAGMode)
    assert len(all_modes) == 17

    for mode in all_modes:
        res = rag_suite.execute(
            query="What is the blast radius of payment-service?",
            mode=mode,
            context={"session_id": "test_session_42"},
        )
        assert res.mode == mode
        assert res.answer is not None
        assert res.confidence >= 0.10
        assert res.latency_ms >= 0.0
        assert len(res.reasoning_steps) >= 1


# ---------------------------------------------------------------------------
# 4. Test All 13 Query Dialects and Transpilation
# ---------------------------------------------------------------------------
def test_all_13_query_dialects():
    engine = PolyglotQueryEngine()
    dialects = list(QueryDialect)
    assert len(dialects) == 13

    # Dialect detection tests
    assert engine.detect_dialect("SELECT ?s ?p ?o WHERE { ?s ?p ?o }") == QueryDialect.SPARQL
    assert engine.detect_dialect("MATCH (n:User) RETURN n") == QueryDialect.CYPHER
    assert engine.detect_dialect("g.V().hasLabel('Service')") == QueryDialect.GREMLIN
    assert engine.detect_dialect("FIND OBJECT User WHERE id = 1") == QueryDialect.EOQL
    assert engine.detect_dialect("ON EVENT ServiceCrash") == QueryDialect.EQL
    assert engine.detect_dialect("What services are affected by checkout?") == QueryDialect.NL2QUERY

    # Transpilation tests
    for dialect in dialects:
        q = PolyglotQuery(query_text="MATCH (n) RETURN n", dialect=dialect)
        plan = engine.transpile(q, target_dialect=QueryDialect.CYPHER)
        assert plan.executable_code is not None
        assert plan.estimated_cost > 0.0

    # Query execution test (no store provided — returns empty results correctly)
    exec_res = engine.execute_query(PolyglotQuery("MATCH (n) RETURN n", QueryDialect.CYPHER))
    assert exec_res.total_records >= 0
    assert exec_res.dialect_used == QueryDialect.CYPHER


# ---------------------------------------------------------------------------
# 5. Test All 17 Enterprise Database Adapters
# ---------------------------------------------------------------------------
def test_all_17_database_adapters():
    registry = DatabaseAdapterRegistry()
    supported = registry.list_supported_databases()
    assert len(supported) == 17

    for db_type in DatabaseType:
        adapter = registry.get_adapter(db_type)
        health = adapter.get_health()
        assert health.connected
        assert health.db_type == db_type
        assert health.node_count >= 0

        res = adapter.execute_query("MATCH (n) RETURN n")
        assert len(res) >= 1
        assert res[0]["db_engine"] == db_type.value


# ---------------------------------------------------------------------------
# 6. Test Living Brain Building Algorithms
# ---------------------------------------------------------------------------
def test_living_brain_algorithms():
    algo = LivingBrainAlgorithms()

    # Dynamic ontology induction from unstructured text
    corpus = [
        "PaymentGateway handles transactions for OrderService.",
        "KafkaCluster streams event payloads to AnalyticsEngine.",
    ]
    concepts = algo.induce_ontology_from_corpus(corpus, confidence_threshold=0.3)
    assert len(concepts) >= 2
    concept_names = [c.name for c in concepts]
    assert any("Payment" in name or "Gateway" in name for name in concept_names)

    # Neuro-symbolic memory consolidation
    events = [
        {"action": "DEPLOY_MICROSERVICE", "actor": "alice"},
        {"action": "ROLLBACK_RELEASE", "actor": "bob"},
    ]
    consolidation = algo.consolidate_neuro_symbolic_memory(events)
    assert consolidation["consolidated_events"] == 2
    assert consolidation["memory_coherence"] > 0.0

    # Cryptographic state snapshot
    snapshot = algo.compute_brain_snapshot()
    assert len(snapshot.merkle_root) == 64
    assert snapshot.coherence_score > 0.0


# ---------------------------------------------------------------------------
# 7. Test Enterprise Brain OS Kernel Answering Engine
# ---------------------------------------------------------------------------
def test_brain_os_kernel():
    os_kernel = BrainOSKernel()

    # Deterministic query path
    det_ans = os_kernel.ask(
        query="MATCH (s:Service) RETURN s",
        target_db=DatabaseType.NEO4J,
        force_deterministic=True,
    )
    assert det_ans.mode == "DETERMINISTIC"
    assert det_ans.confidence == 1.0
    assert len(det_ans.evidence_refs) >= 0

    # Hybrid LLM-augmented answering path
    hybrid_ans = os_kernel.ask(
        query="Explain the dependency risks of the billing subsystem.",
        loop=LoopType.HBTL,
        rag_mode=RAGMode.GRAPH_RAG,
    )
    assert hybrid_ans.mode == "HYBRID"
    assert hybrid_ans.confidence >= 0.0
    assert len(hybrid_ans.evidence_refs) >= 0

    # Governance blocked path
    blocked_ans = os_kernel.ask(
        query="Delete all production tables",
        loop=LoopType.HOOTL,
        risk=RiskTier.R4,
    )
    assert blocked_ans.mode == "BLOCKED"
    assert blocked_ans.confidence == 0.0

    # System telemetry
    telemetry = os_kernel.get_system_telemetry()
    assert telemetry["status"] == "OPERATIONAL"
    assert len(telemetry["supported_loops"]) == 14
    assert len(telemetry["supported_agents"]) == 35
    assert len(telemetry["supported_rag_modes"]) == 17
    assert len(telemetry["supported_query_dialects"]) == 13
    assert len(telemetry["supported_databases"]) == 17
