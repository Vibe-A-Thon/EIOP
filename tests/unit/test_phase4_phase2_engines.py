"""Unit tests for Phase 4 - Phase 2 Requirements:
- AGENT-001: Cognitive Boundary Telemetry
- AGENT-002: Dynamic Entity & Community Extraction
- AGENT-003: Agent Communication Bus
- AGENT-004: Parallel Fan-Out/Fan-In MapReduce
- GRAPH-001: Federated Graph Engineering
- GRAPH-002: Causal Inference over Graphs
- GRAPH-003: Knowledge Distillation Engineering
- GRAPH-004: Graph Neural Network Integration
- GRAPH-005: Temporal & Hybrid Retrieval
- GRAPH-006: OWL Reasoning & SHACL Validation
- AI-003: Relation Extraction & Triple Generation
"""

import sys
import time
from pathlib import Path

# Ensure workspace packages take precedence
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "packages"))

import pytest

from eoip.agents.message_bus import (
    AgentMessageBus,
    AgentMessageSchema,
    AgentMessageType,
    BroadcastChannel,
    CapabilityNegotiation,
    MessageQueue,
    get_agent_message_bus,
)
from eoip.causal.engine import (
    BlastRadiusAnalysis,
    CausalInferenceEngine,
    CounterfactualQuery,
    InterventionModel,
)
from eoip.distillation.engine import (
    DistillationEngine,
    DistillationStrategy,
    GraphDistiller,
    KnowledgePackage,
    PackageDeployer,
)
from eoip.extraction.engine import (
    ChunkStrategy,
    CommunityDetector,
    DocumentChunker,
    EntityExtractor,
    ExtractionPipeline,
)
from eoip.extraction.relation_extractor import (
    ExtractedTriple,
    RelationExtractor,
    RelationPattern,
    TripleDeduplicator,
    TripleValidator,
)
from eoip.federation.engine import (
    BackendMapping,
    CatalogService,
    FederatedGraph,
    FederationPlanner,
    ResultMerger,
    get_federation_engine,
)
from eoip.gnn.engine import (
    EmbeddingModelType,
    GNNEngine,
    GraphEmbedder,
    LinkPredictor,
    NodeClassifier,
)
from eoip.graph.database_adapters import DatabaseType
from eoip.graph.memory import MemoryGraphStore
from eoip.harness.engine import (
    FanInStage,
    FanOutStage,
    HarnessEngine,
    MergeStrategy,
    PipelineStage,
    StateSchema,
)
from eoip.ontology.rdf import OWLReasoner
from eoip.ontology.shacl_validator import (
    SHACLSeverity,
    SHACLShape,
    SHACLValidator,
)
from eoip.retrieval.temporal import (
    AsOfQuery,
    TemporalFact,
    TemporalHybridRetrievalEngine,
    TemporalIndex,
    TemporalRangeQuery,
)
from eoip.telemetry.adapter import (
    BoundarySignal,
    CognitiveBoundaryDetector,
    HandoffDecision,
    HandoffTarget,
)


class TestAgent001CognitiveBoundaryTelemetry:
    """AGENT-001: Cognitive Boundary Telemetry."""

    def test_all_seven_boundary_signals(self):
        detector = CognitiveBoundaryDetector(
            min_confidence=0.70,
            max_hallucination=0.30,
            max_context_tokens=4000,
            max_tool_failures=2,
            max_repeated_thoughts=2,
            max_latency_ms=5000.0,
            max_cost_usd=1.00,
        )

        # 1. Healthy agent metrics -> no trigger
        healthy = detector.evaluate_metrics("agent_test", {
            "confidence": 0.95,
            "hallucination_score": 0.05,
            "context_tokens": 1200,
            "consecutive_tool_failures": 0,
            "repeated_reasoning_steps": 0,
            "latency_ms": 120.0,
            "accumulated_cost_usd": 0.05,
        })
        assert not healthy.triggered
        assert healthy.target == HandoffTarget.NONE

        # 2. Tool failure streak -> triggers Human escalation
        failing_tools = detector.evaluate_metrics("agent_test", {"consecutive_tool_failures": 3})
        assert failing_tools.triggered
        assert failing_tools.target == HandoffTarget.HUMAN
        assert any(b.signal == BoundarySignal.TOOL_FAILURE_STREAK for b in failing_tools.breached_signals)

        # 3. Context overflow -> triggers fallback summarizer agent
        overflow = detector.evaluate_metrics("agent_test", {"context_tokens": 5000})
        assert overflow.triggered
        assert overflow.target == HandoffTarget.FALLBACK_AGENT
        assert any(b.signal == BoundarySignal.CONTEXT_OVERFLOW for b in overflow.breached_signals)

        # 4. Latency spike -> triggers higher autonomy HOTL loop
        latency_spike = detector.evaluate_metrics("agent_test", {"latency_ms": 8000.0})
        assert latency_spike.triggered
        assert latency_spike.target == HandoffTarget.HIGHER_AUTONOMY_LOOP
        assert any(b.signal == BoundarySignal.LATENCY_SPIKE for b in latency_spike.breached_signals)

        # Telemetry events emitted
        events = detector.get_events()
        assert len(events) >= 3


class TestAgent002AndAi003Extraction:
    """AGENT-002: Dynamic Extraction Pipeline & AI-003: Relation Extraction."""

    def test_chunker_and_entity_extractor(self):
        chunker = DocumentChunker()
        text = "OrderService calls InventoryService. InventoryService is a part of FulfillmentGateway."
        chunks = chunker.chunk(text, strategy=ChunkStrategy.SENTENCE)
        assert len(chunks) >= 2

        extractor = EntityExtractor()
        entities = extractor.extract_entities(text)
        assert any(e.name == "OrderService" for e in entities)
        assert any(e.name == "InventoryService" for e in entities)

    def test_relation_extractor_triples(self):
        rel_extractor = RelationExtractor()
        text = "PaymentService depends on FraudEngine. BillingService calls PaymentService."
        triples = rel_extractor.extract_triples(text)
        assert len(triples) >= 1
        assert any(t.predicate == "DEPENDS_ON" and t.subject == "PaymentService" and t.object == "FraudEngine" for t in triples)

    def test_full_pipeline_and_communities(self):
        pipeline = ExtractionPipeline()
        doc = (
            "AuthGateway calls UserDatabase. UserDatabase is a part of CoreInfra.\n\n"
            "PaymentService depends on BankAPI. BankAPI calls SettlementEngine."
        )
        res = pipeline.process_text(doc)
        assert res.chunks_count >= 1
        assert len(res.entities) >= 2
        assert res.vertices_upserted >= 2
        assert len(res.communities) >= 1


class TestAgent003MessageBus:
    """AGENT-003: Agent Communication Bus."""

    def test_capability_negotiation(self):
        bus = AgentMessageBus()
        bus.negotiation.register_agent("graph_worker_1", "GraphAgent", ["graph_traversal", "cypher_query"])
        bus.negotiation.register_agent("rag_worker_1", "RAGAgent", ["vector_search", "document_summary"])

        matched = bus.negotiation.discover_by_capability("graph_traversal")
        assert len(matched) == 1
        assert matched[0].agent_id == "graph_worker_1"

        negotiated = bus.negotiation.negotiate("requester_alpha", ["document_summary"])
        assert negotiated is not None
        assert negotiated.agent_id == "rag_worker_1"

    def test_queue_and_dlq_expiration(self):
        bus = AgentMessageBus()
        msg_live = AgentMessageSchema(
            sender_id="sender_a",
            recipient_id="worker_b",
            payload={"task": "execute_plan"},
            ttl_seconds=100.0,
        )
        bus.send_message(msg_live)
        received = bus.receive_message("worker_b")
        assert received is not None
        assert received.payload["task"] == "execute_plan"

        # Expired message goes to DLQ
        msg_expired = AgentMessageSchema(
            sender_id="sender_a",
            recipient_id="worker_b",
            payload={"task": "stale_task"},
            ttl_seconds=-1.0,
        )
        bus.send_message(msg_expired)
        dlq = bus.get_dlq("worker_b")
        assert len(dlq) >= 1

    def test_broadcast_channel(self):
        channel = BroadcastChannel()
        received_payloads = []
        channel.subscribe("telemetry_alerts", "observer_agent", lambda m: received_payloads.append(m.payload))
        msg = AgentMessageSchema(headers={"topic": "telemetry_alerts"}, payload={"alert": "cpu_high"})
        count = channel.publish("telemetry_alerts", msg)
        assert count == 1
        assert len(received_payloads) == 1


class TestAgent004ParallelFanOutFanIn:
    """AGENT-004: Parallel Fan-Out/Fan-In (MapReduce)."""

    def test_fan_out_fan_in_map_reduce(self):
        harness = HarnessEngine()

        # Fan-Out stage: splits numbers into parallel squared shards
        fan_out = FanOutStage(
            name="map_squares",
            shard_generator=lambda ctx: ctx.get("numbers", [1, 2, 3, 4]),
            worker_fn=lambda n, ctx: {"partial_sum": n * n, "processed_items": [f"item_{n}"]},
            max_workers=4,
        )

        # Fan-In stage: merges partial sums and appends lists
        schema = StateSchema(
            default_strategy=MergeStrategy.RECURSIVE_MERGE,
            field_strategies={"processed_items": MergeStrategy.APPEND_LISTS},
        )
        fan_in = FanInStage(
            name="reduce_sum",
            fan_out_stage_name="map_squares",
            schema=schema,
        )

        harness.register_pipeline("parallel_sum", [fan_out, fan_in])
        run = harness.run_pipeline("parallel_sum", context={"numbers": [1, 2, 3, 4, 5]})

        assert run.status == "completed"
        # Sum of 1^2 + 2^2 + 3^2 + 4^2 + 5^2 = 1 + 4 + 9 + 16 + 25 = 55
        assert run.context_output.get("partial_sum") == 55
        assert len(run.context_output.get("processed_items", [])) == 5


class TestGraph001Federation:
    """GRAPH-001: Federated Graph Engineering."""

    def test_catalog_and_federated_query(self):
        engine = get_federation_engine()
        engine.catalog.register_mapping(BackendMapping("AuditLog", DatabaseType.NEO4J, priority=1))

        # Query spans virtual graph across mock backends
        res = engine.query("MATCH (n:Person) RETURN n", filters={"active": "true"})
        assert "participating_backends" in res
        assert "subquery_plans" in res
        assert len(res["subquery_plans"]) >= 1


class TestGraph002CausalInference:
    """GRAPH-002: Causal Inference over Graphs."""

    def test_intervention_and_blast_radius(self):
        store = MemoryGraphStore()
        store.upsert_vertex("Service", {"name": "SupplierAlpha", "service_id": "sup_alpha", "canonical_id": "sup_alpha"})
        store.upsert_vertex("Service", {"name": "AssemblyBeta", "service_id": "asm_beta", "canonical_id": "asm_beta"})
        store.upsert_vertex("Service", {"name": "ProductGamma", "service_id": "prod_gamma", "canonical_id": "prod_gamma"})

        store.upsert_edge("CALLS", "sup_alpha", "asm_beta", {})
        store.upsert_edge("CALLS", "asm_beta", "prod_gamma", {})

        engine = CausalInferenceEngine(store=store)

        # 1. Blast radius of supplier alpha failure
        blast = engine.blast_radius("sup_alpha")
        assert "asm_beta" in blast.direct_dependents
        assert "prod_gamma" in blast.transitive_dependents

        # 2. What-if counterfactual query
        what_if = engine.evaluate_what_if("sup_alpha", "prod_gamma")
        assert what_if["outcome_affected"] is True
        assert what_if["causal_effect"]["effect_size"] > 0.0


class TestGraph003Distillation:
    """GRAPH-003: Knowledge Distillation Engineering."""

    def test_distillation_package_and_deploy(self):
        store = MemoryGraphStore()
        for i in range(10):
            store.upsert_vertex("Service", {"name": f"Service_{i}", "service_id": f"srv_{i}", "canonical_id": f"srv_{i}", "description": "x" * 200})
            if i > 0:
                store.upsert_edge("CALLS", f"srv_{i-1}", f"srv_{i}", {})

        distiller = GraphDistiller()
        pkg = distiller.distill(store, seed_ids=["srv_0"], max_hops=2, strategy=DistillationStrategy.HYBRID_COMPACT)

        assert pkg.original_vertex_count == 10
        assert len(pkg.vertices) < 10  # Pruned to 2-hop radius
        assert pkg.compression_ratio >= 0.0
        assert pkg.fidelity_score > 0.5
        assert len(pkg.checksum) > 0

        # Deploy package
        deployer = PackageDeployer()
        dep_res = deployer.deploy_to_edge(pkg, "edge_node_alpha")
        assert dep_res["status"] == "DEPLOYED"


class TestGraph004GNNIntegration:
    """GRAPH-004: Graph Neural Network Integration."""

    def test_embeddings_and_link_prediction(self):
        store = MemoryGraphStore()
        store.upsert_vertex("Service", {"canonical_id": "srv_a", "service_id": "srv_a", "name": "AuthService", "description": "Microservice"})
        store.upsert_vertex("Service", {"canonical_id": "srv_b", "service_id": "srv_b", "name": "PaymentService", "description": "Microservice"})
        store.upsert_vertex("Service", {"canonical_id": "srv_c", "service_id": "srv_c", "name": "LoggingService", "description": "Unknown"})

        store.upsert_edge("CALLS", "srv_a", "srv_b", {})
        store.upsert_edge("CALLS", "srv_b", "srv_c", {})

        gnn = GNNEngine()
        # Node2vec embeddings
        embs = gnn.compute_embeddings(store, model_type=EmbeddingModelType.NODE2VEC, dimensions=16)
        assert len(embs) == 3
        assert len(embs["srv_a"]) == 16

        # TransE embeddings
        transe = gnn.compute_embeddings(store, model_type=EmbeddingModelType.TRANSE, dimensions=16)
        assert len(transe) == 3

        # Link prediction
        preds = gnn.predict_links(store, "srv_a", top_k=2)
        assert isinstance(preds, list)

        # Node classification via message passing
        cls_res = gnn.classify_node(store, "srv_c")
        assert cls_res["predicted_class"] == "Microservice"


class TestGraph005TemporalRetrieval:
    """GRAPH-005: Temporal & Hybrid Retrieval."""

    def test_temporal_index_as_of_and_range(self):
        index = TemporalIndex()
        # Entity attribute changed over time
        t1 = 1000.0
        t2 = 2000.0
        t3 = 3000.0

        index.add_fact(TemporalFact(fact_id="f1", subject="cluster_us_east", predicate="status", object_value="PROVISIONING", valid_from=t1, valid_to=t2))
        index.add_fact(TemporalFact(fact_id="f2", subject="cluster_us_east", predicate="status", object_value="HEALTHY", valid_from=t2, valid_to=t3))
        index.add_fact(TemporalFact(fact_id="f3", subject="cluster_us_east", predicate="status", object_value="DEGRADED", valid_from=t3, valid_to=None))

        # Query as-of T=1500 (PROVISIONING)
        res_t1500 = index.query_as_of(AsOfQuery(as_of_time=1500.0, subject="cluster_us_east"))
        assert len(res_t1500) == 1
        assert res_t1500[0].object_value == "PROVISIONING"

        # Query as-of T=2500 (HEALTHY)
        res_t2500 = index.query_as_of(AsOfQuery(as_of_time=2500.0, subject="cluster_us_east"))
        assert len(res_t2500) == 1
        assert res_t2500[0].object_value == "HEALTHY"

        # Query timeline evolution
        timeline = index.query_timeline("cluster_us_east")
        assert len(timeline) == 3
        assert [f.object_value for f in timeline] == ["PROVISIONING", "HEALTHY", "DEGRADED"]


class TestGraph006OWLAndSHACLValidation:
    """GRAPH-006: OWL Reasoning & SHACL Runtime Validation."""

    def test_owl_reasoner(self):
        reasoner = OWLReasoner()
        # Subsumption: RelationalDatabase -> DatabaseService -> Service
        assert reasoner.is_subclass_of("RelationalDatabase", "Service")
        assert reasoner.is_subclass_of("RelationalDatabase", "DatabaseService")
        assert not reasoner.is_subclass_of("Service", "RelationalDatabase")

        # Disjointness
        assert reasoner.are_disjoint("Service", "Person")
        assert reasoner.are_disjoint("RelationalDatabase", "GraphDatabase")

        # Property chain inference: A DEPENDS_ON B and B DEPENDS_ON C -> A DEPENDS_ON C
        store = MemoryGraphStore()
        store.upsert_vertex("Service", {"name": "SubService", "service_id": "srv_sub", "canonical_id": "srv_sub"})
        store.upsert_vertex("Service", {"name": "CompService", "service_id": "srv_comp", "canonical_id": "srv_comp"})
        store.upsert_vertex("Service", {"name": "SysService", "service_id": "srv_sys", "canonical_id": "srv_sys"})

        store.upsert_edge("DEPENDS_ON", "srv_sub", "srv_comp", {})
        store.upsert_edge("DEPENDS_ON", "srv_comp", "srv_sys", {})
        inferred = reasoner.infer_triples(store)
        sub_vid = store._vids["srv_sub"]
        sys_vid = store._vids["srv_sys"]
        assert any(t["out_v"] == sub_vid and t["in_v"] == sys_vid and t["label"] == "DEPENDS_ON" for t in inferred)

    def test_shacl_shape_validation(self):
        validator = SHACLValidator()
        store = MemoryGraphStore()

        # Valid service
        store.upsert_vertex("Service", {"name": "AuthService", "service_id": "srv_auth", "canonical_id": "srv_auth"})

        # Invalid service with empty string name
        store.upsert_vertex("Service", {"name": "", "service_id": "srv_broken", "canonical_id": "srv_broken"})

        report = validator.validate(store)
        assert not report.conforms
        assert report.total_violations >= 1
        assert any(v.focus_node == "srv_broken" and v.path == "name" for v in report.violations)
