"""Comprehensive Unit Tests for EOIP Phase 4 — Compliance, Chaos, Multi-Modal & Memory.

Validates:
- COMPLY-001: Compliance-as-Code Graph Constraints (GDPR, SOX, HIPAA, SOC2 rules, ContinuousMonitor)
- COMPLY-002: Automated PII Detection & Anonymization (Scanner, Masking, k-anonymity, Pseudonymizer)
- TEST-001: Chaos Engineering Framework (Latency spike, outage, connection reset, recovery)
- MULTI-001: Scoped Multi-Modal Diagram-to-Graph & Rendering (Mermaid parsing, SVG rendering)
- MULTI-002: Knowledge & Memory Graph Engineering (Episodic graph, consolidation to semantic rules)
"""

import time
import pytest

from eoip.compliance.constraints import (
    ComplianceFramework,
    ComplianceSeverity,
    ContinuousMonitor,
    GDPRRightToErasureRule,
    HIPAAMinimumNecessaryRule,
    SOC2AccessControlRule,
    SOXSegregationOfDutiesRule,
)
from eoip.privacy.scanner import (
    Anonymizer,
    PIIScanner,
    PIIType,
    Pseudonymizer,
)
from tests.chaos.fault_injector import (
    ChaosFaultError,
    ChaosFaultType,
    FaultConfig,
    FaultInjector,
)
from eoip.fileparse.diagram_parser import (
    DiagramToGraphParser,
    GraphToDiagramRenderer,
)
from eoip.memory_eng.engine import (
    EpisodicMemoryGraph,
    MemoryConsolidationGraph,
    MemoryGraph,
)
from eoip.graph.memory import MemoryGraphStore


@pytest.mark.req("COMPLY-001")
class TestComply001ComplianceAsCode:
    """COMPLY-001: Compliance-as-Code Graph Constraints."""

    def test_compliance_rules_and_monitor(self):
        store = MemoryGraphStore()
        # 1. Valid services
        store.upsert_vertex("Service", {"name": "AuthService", "service_id": "srv_auth", "canonical_id": "srv_auth", "criticality": "CRITICAL", "resilience": "MULTI_AZ"})
        store.upsert_vertex("Service", {"name": "PaymentService", "service_id": "srv_pay", "canonical_id": "srv_pay", "criticality": "LOW"})

        # 2. SOC2 Violation: Critical service missing resilience
        store.upsert_vertex("Service", {"name": "RiskService", "service_id": "srv_risk", "canonical_id": "srv_risk", "criticality": "CRITICAL"})

        # 3. HIPAA Violation: Database with PHI unencrypted
        store.upsert_vertex("Database", {"name": "PatientHealthDB", "canonical_id": "db_health", "description": "PHI unencrypted"})

        # 4. SOX Violation: Self-deployed Deployment
        store.upsert_vertex("Deployment", {"name": "DeployProd", "canonical_id": "dep_prod", "author_name": "usr_dev", "actor": "usr_dev"})

        # Run continuous monitor
        monitor = ContinuousMonitor()
        report = monitor.evaluate_compliance(store)

        assert not report.conforms
        assert report.total_violations >= 3

        rule_ids = {v.rule_id for v in report.violations}
        assert "SOC2-001" in rule_ids
        assert "HIPAA-001" in rule_ids
        assert "SOX-001" in rule_ids


@pytest.mark.req("COMPLY-002")
class TestComply002PIIDetectionAndAnonymization:
    """COMPLY-002: Automated PII Detection & Anonymization."""

    def test_pii_scanner(self):
        scanner = PIIScanner()
        props = {
            "contact_email": "jane.doe@enterprise.com",
            "support_phone": "212-555-1234",
            "ssn_record": "987-65-4321",
            "server_ip": "192.168.1.100",
            "plain_text": "Normal description without sensitive data",
        }
        findings = scanner.scan_properties("user_101", props)
        assert len(findings) == 4

        types = {f.pii_type for f in findings}
        assert PIIType.EMAIL in types
        assert PIIType.PHONE in types
        assert PIIType.SSN in types
        assert PIIType.IP_ADDRESS in types

    def test_anonymizer_and_pseudonymizer(self):
        # 1. Masking
        assert Anonymizer.mask("john.smith@gmail.com", PIIType.EMAIL) == "j***@gmail.com"
        assert Anonymizer.mask("123-45-6789", PIIType.SSN) == "***-**-6789"
        assert Anonymizer.mask("192.168.1.42", PIIType.IP_ADDRESS) == "192.168.*.*"

        # 2. k-Anonymity Generalization
        records = [
            {"name": "Alice", "age": 24, "city": "NY"},
            {"name": "Bob", "age": 28, "city": "NY"},
            {"name": "Charlie", "age": 35, "city": "SF"},
        ]
        anon_records = Anonymizer.k_anonymize(records, quasi_identifiers=["age"], k=2)
        assert anon_records[0]["age"] == "[20-29]"
        assert anon_records[1]["age"] == "[20-29]"
        assert anon_records[2]["age"] == "[30-39]"

        # 3. Pseudonymizer (Reversible)
        vault = Pseudonymizer()
        token = vault.pseudonymize("customer_ssn_12345")
        assert token.startswith("PSEUDO_")
        assert vault.de_pseudonymize(token) == "customer_ssn_12345"


@pytest.mark.req("TEST-001")
class TestChaos001FaultInjection:
    """TEST-001: Chaos Engineering Framework."""

    def test_chaos_fault_injection_and_recovery(self):
        injector = FaultInjector()

        # 1. Store Outage Fault
        injector.inject_fault(
            FaultConfig(
                fault_type=ChaosFaultType.STORE_OUTAGE,
                target_component="neptune_cluster",
            )
        )

        with pytest.raises(ChaosFaultError, match="Chaos injected outage"):
            injector.intercept("neptune_cluster", lambda: "normal_data")

        # 2. Connection Reset Fault
        injector.inject_fault(
            FaultConfig(
                fault_type=ChaosFaultType.CONNECTION_RESET,
                target_component="kafka_broker",
            )
        )
        with pytest.raises(ConnectionResetError):
            injector.intercept("kafka_broker", lambda: "ok")

        # 3. Clear faults & Verify Recovery
        recovered = injector.verify_recovery("neptune_cluster", lambda: True)
        assert recovered is True
        assert injector.intercept("neptune_cluster", lambda: "healthy_data") == "healthy_data"


@pytest.mark.req("MULTI-001")
class TestMulti001DiagramParsingAndRendering:
    """MULTI-001: Scoped Multi-Modal Diagram-to-Graph & Rendering."""

    def test_mermaid_parsing_and_loading(self):
        parser = DiagramToGraphParser()
        mermaid_src = """
        flowchart LR
            AuthService["Authentication Service"] -->|CALLS| TokenService["Token Service"]
            TokenService["Token Service"] -->|CALLS| RedisCluster["Redis Cluster"]
        """
        graph = parser.parse_mermaid(mermaid_src)
        assert len(graph.vertices) == 3
        assert len(graph.edges) == 2

        store = MemoryGraphStore()
        graph.load_into_store(store)
        assert store.count_vertices() == 3
        assert store.count_edges() == 2

    def test_graph_to_diagram_renderer(self):
        renderer = GraphToDiagramRenderer()
        vertices = [
            {"canonical_id": "srv_a", "properties": {"name": "ServiceA"}},
            {"canonical_id": "srv_b", "properties": {"name": "ServiceB"}},
        ]
        edges = [{"out_cid": "srv_a", "in_cid": "srv_b", "label": "CALLS"}]

        mermaid_out = renderer.render_mermaid(vertices, edges)
        assert "flowchart LR" in mermaid_out
        assert 'srv_a["ServiceA"]' in mermaid_out
        assert "srv_a -->|CALLS| srv_b" in mermaid_out

        svg_out = renderer.render_svg(vertices, edges)
        assert "<svg" in svg_out
        assert "ServiceA" in svg_out
        assert "</svg>" in svg_out


@pytest.mark.req("MULTI-002")
class TestMulti002MemoryGraph:
    """MULTI-002: Knowledge & Memory Graph Engineering."""

    def test_episodic_graph_and_consolidation(self):
        episodic = EpisodicMemoryGraph()
        # Record sequence of steps
        episodic.record_episode_step("User asks for DB latency report", {"query": "SELECT ..."})
        episodic.record_episode_step("Agent retrieves Prometheus metrics", {"metric": "query_duration"})
        episodic.record_episode_step("User asks for DB latency report", {"query": "SELECT ..."})

        assert len(episodic.nodes) == 3
        assert len(episodic.edges) == 2

        # Subgraph query
        sub = episodic.query_subgraph(memory_type="EPISODIC", min_importance=0.5)
        assert len(sub["nodes"]) == 3

        # Consolidate recurring steps into Semantic Memory
        consolidator = MemoryConsolidationGraph(episodic_graph=episodic)
        promoted_count = consolidator.consolidate(frequency_threshold=2)

        assert promoted_count == 1
        long_term_nodes = consolidator.long_term_graph.nodes
        assert len(long_term_nodes) == 1
        consolidated_rule = list(long_term_nodes.values())[0]
        assert "Consolidated Rule: User asks for DB latency report" in consolidated_rule.content
        assert consolidated_rule.memory_type == "SEMANTIC"
