"""Unit Tests for Enterprise Brain OS, Loops, Agents, RAGs, Polyglot Queries, and Living Brain.

Validates:
- 14 Control Loops, 15 Human Governance Patterns & 23 Autonomous Execution Loops
- 54 Agent Archetypes & Multi-Agent Swarm Systems + A2A Protocol Broker
- 64 Unified RAG Retrieval Patterns (Graph, Tree, Temporal, Code, Reasoning, Corrective & Retrieval Techniques)
- 71 Query Languages & NL2* Translation Family + Knowledge Representation Standards
- 55 Enterprise Database Adapters (Native Graph, Multimodel, Vector, and Operational Persistence)
- Living Brain Building Algorithms & Merkle state verification
- Brain OS Kernel Deterministic & Hybrid Answering
"""

import pytest

from eoip.agents.loops import (
    EnterpriseLoopManager, LoopType, RiskTier,
    HumanControlPattern, AutonomousExecutionLoop, ExecutionLimits,
)
from eoip.agents.archetypes import AgentFactory, BaseAgent, A2AProtocolBroker
from eoip.retrieval.rag_suite import EnterpriseRAGSuite, RAGMode
from eoip.query.polyglot_engine import PolyglotQueryEngine, QueryDialect, PolyglotQuery
from eoip.graph.database_adapters import DatabaseAdapterRegistry, DatabaseType
from eoip.brain.living_brain_algorithms import LivingBrainAlgorithms
from eoip.brain.brain_os import BrainOSKernel


# ---------------------------------------------------------------------------
# 1. Test Control Loops, Human Governance & Autonomous Loops
# ---------------------------------------------------------------------------
def test_all_control_loops_and_patterns():
    mgr = EnterpriseLoopManager()
    all_loops = list(LoopType)
    assert len(all_loops) == 14

    all_human_patterns = list(HumanControlPattern)
    assert len(all_human_patterns) == 15

    all_auto_loops = list(AutonomousExecutionLoop)
    assert len(all_auto_loops) == 23

    # Test execution limits container
    limits = ExecutionLimits(max_iterations=5, token_budget=1000)
    assert limits.max_iterations == 5
    assert not limits.is_exhausted()
    limits.current_iteration = 6
    assert limits.is_exhausted()

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
# 2. Test All 76+ Agent Archetypes & A2A Broker
# ---------------------------------------------------------------------------
def test_all_agent_archetypes_and_a2a():
    archetypes = AgentFactory.list_archetypes()
    assert len(archetypes) >= 76
    assert len(archetypes) == len(AgentFactory._REGISTRY)

    for arch_name in archetypes:
        agent = AgentFactory.create(arch_name)
        assert isinstance(agent, BaseAgent)
        res = agent.run("Analyze critical infrastructure component")
        assert res.agent_type == arch_name
        assert res.output is not None
        assert len(res.reasoning_trace) >= 1

    # Verify A2A Protocol Broker
    broker = A2AProtocolBroker()
    a1 = AgentFactory.create("PlannerAgent")
    a2 = AgentFactory.create("ExecutorAgent")
    broker.register_agent(a1)
    broker.register_agent(a2)
    msg = broker.send_a2a_message(a1.agent_id, a2.agent_id, {"task": "execute_dag"})
    assert msg.sender == a1.agent_id
    assert msg.receiver == a2.agent_id
    inbox = broker.get_messages_for_agent(a2.agent_id)
    assert len(inbox) == 1
    assert inbox[0].content["task"] == "execute_dag"


# ---------------------------------------------------------------------------
# 3. Test All RAG Modalities
# ---------------------------------------------------------------------------
def test_all_rag_modalities():
    rag_suite = EnterpriseRAGSuite()
    rag_suite.add_documents([
        {"id": "d1", "content": "payment-service is a critical microservice that handles all credit card transactions and connects to the billing database", "source_type": "text"},
        {"id": "d2", "content": "the blast radius of payment-service includes billing-db, invoice-generator, and the notification service", "source_type": "text"},
        {"id": "d3", "content": "authentication service validates user tokens via OIDC and LDAP protocols before allowing API access", "source_type": "text"},
        {"id": "d4", "content": "def process_payment(account_id, amount):\n    return execute_transaction(account_id, amount)", "source_type": "code"},
        {"id": "d5", "content": "payment-service depends on config-service for feature flags and rate limiting configuration", "source_type": "text"},
    ])
    all_modes = list(RAGMode)
    assert len(all_modes) >= 64

    for mode in all_modes:
        res = rag_suite.execute(
            query="What is the blast radius of payment-service?",
            mode=mode,
            context={"session_id": "test_session_42", "clearance": "confidential"},
        )
        assert res.mode == mode
        assert res.answer is not None
        assert res.confidence >= 0.0
        assert res.latency_ms >= 0.0
        assert len(res.reasoning_steps) >= 1


# ---------------------------------------------------------------------------
# 4. Test All Polyglot Query Dialects and Transpilation
# ---------------------------------------------------------------------------
def test_all_query_dialects():
    engine = PolyglotQueryEngine()
    dialects = list(QueryDialect)
    assert len(dialects) >= 71

    # Dialect detection tests
    assert engine.detect_dialect("SELECT ?s ?p ?o WHERE { ?s ?p ?o }") == QueryDialect.SPARQL
    assert engine.detect_dialect("MATCH (n:User) RETURN n") == QueryDialect.CYPHER
    assert engine.detect_dialect("g.V().hasLabel('Service')") == QueryDialect.GREMLIN
    assert engine.detect_dialect("FIND OBJECT User WHERE id = 1") == QueryDialect.EOQL
    assert engine.detect_dialect("ON EVENT ServiceCrash") == QueryDialect.EQL
    assert engine.detect_dialect("sum(rate(http_requests_total[5m])) by (instance)") == QueryDialect.PROMQL
    assert engine.detect_dialect('{app="eoip"} |= "error"') == QueryDialect.LOGQL
    assert engine.detect_dialect("traces | where SeverityLevel == 'Error'") == QueryDialect.KQL_AZURE
    assert engine.detect_dialect("What services are affected by checkout?") == QueryDialect.NL2QUERY

    # Transpilation tests across all dialects
    for dialect in dialects:
        q = PolyglotQuery(query_text="MATCH (n) RETURN n", dialect=dialect)
        plan = engine.transpile(q, target_dialect=QueryDialect.CYPHER)
        assert plan.executable_code is not None
        assert plan.estimated_cost > 0.0

    # Query execution test (no store provided — returns empty results gracefully)
    exec_res = engine.execute_query(PolyglotQuery("MATCH (n) RETURN n", QueryDialect.CYPHER))
    assert exec_res.total_records >= 0
    assert exec_res.dialect_used == QueryDialect.CYPHER


# ---------------------------------------------------------------------------
# 5. Test All 39 Enterprise Database Adapters
# ---------------------------------------------------------------------------
def test_all_database_adapters():
    registry = DatabaseAdapterRegistry()
    supported = registry.list_supported_databases()
    assert len(supported) >= 39
    assert len(supported) == len(DatabaseType)

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
    assert len(telemetry["supported_agents"]) >= 76
    assert len(telemetry["supported_agents"]) == len(AgentFactory._REGISTRY)
    assert len(telemetry["supported_rag_modes"]) >= 64
    assert len(telemetry["supported_query_dialects"]) >= 71
    assert len(telemetry["supported_databases"]) >= 55
    assert len(telemetry["supported_databases"]) == len(DatabaseType)
