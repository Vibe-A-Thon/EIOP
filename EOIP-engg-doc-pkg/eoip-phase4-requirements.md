# EOIP/KnowGridFlow Phase 4 — Engineering Requirements & Feature Roadmap

> **Generated**: 2026-10-12 | **Author**: CTO/Architect Feasibility Study
> **Platform**: Enterprise Cognitive Intelligence Platform | **TAM**: $14.4B
> **Baseline**: 21 discipline engines, 64 RAG modes, 35 agent types, 71 query dialects, 14 control loops, 23 autonomous execution loops

---

## How to Use This Document

- **AI Coding Agents**: Each requirement has a unique ID, clear acceptance criteria, file paths, and dependencies. Implement requirements in phase order, respecting dependency chains.
- **Human Tracking**: Use the companion `eoip-phase4-tracker.html` for interactive progress tracking with filters, search, and status updates.
- **Priority Legend**: P0 = Critical/Must-Have | P1 = High/Should-Have | P2 = Medium/Nice-to-Have | P3 = Low/Future

---

## PHASE 1 — HIGH-IMPACT CORE ENGINES

### CORE-001: Token Format Serialization Engines
- **Priority**: P0
- **Category**: Token Economics
- **Description**: Build dedicated serialization engines for all 7 token-efficient formats already referenced across 27 files but lacking implementation: TOON (Token-Oriented Object Notation), TRON (Token Reduced Object Notation), LEAN (LLM-Efficient Adaptive Notation), ASON (Aliased Serialization Object Notation), ZON (Zero Overhead Notation), ZOON (Zero Overhead Object Notation), TSON (Tokenized Structural Object Notation).
- **Rationale**: Token economics is the #1 enterprise AI cost concern. These formats can reduce LLM token consumption by 30-70% on graph payloads, RAG contexts, and agent messages. No competitor has dedicated token-efficient serialization.
- **Implementation**:
  - Create `packages/eoip/token_formats/engine.py`
  - Create `packages/eoip/token_formats/__init__.py`
  - Each format as a pluggable `FormatStrategy` with `serialize()`, `deserialize()`, `estimate_tokens()`, `compression_ratio()`
  - `TokenFormatEngine` with auto-format selection based on payload size, context budget, and content type
  - Round-trip fidelity guarantees with validation
  - Integration points: RAG context serialization, agent message encoding, graph payload compression, API response formatting
  - Benchmarking: token count comparison across all 7 formats vs raw JSON
- **Acceptance Criteria**:
  - [ ] All 7 format strategies implemented with serialize/deserialize
  - [ ] Auto-format selection based on payload characteristics
  - [ ] Round-trip fidelity: `deserialize(serialize(obj)) == obj` for all supported types
  - [ ] Token reduction benchmarks showing 30%+ savings vs JSON
  - [ ] Thread-safe singleton `get_token_format_engine()`
  - [ ] Wired into `brain_os.py` telemetry and `platform_router.py` endpoints
  - [ ] Unit tests covering all 7 formats with edge cases
- **Dependencies**: None
- **Estimated Complexity**: High (7 format implementations + auto-selection + benchmarks)

### CORE-002: Verification & Guardrail Engineering
- **Priority**: P0
- **Category**: Enterprise Trust & Safety
- **Description**: Standalone verification discipline with deterministic non-LLM validators that grade every agent output before loop progression. Distinct from the existing security engine (which handles prompt injection/PII) — this handles semantic correctness, schema conformance, policy compliance, and cognitive drift detection.
- **Rationale**: Enterprise customers in regulated industries demand auditable verification chains. Unverified code execution and cognitive drift are top production failure modes.
- **Implementation**:
  - Create `packages/eoip/verification/engine.py`
  - Create `packages/eoip/verification/__init__.py`
  - `VerificationRule` base class with `check(output) -> VerificationResult`
  - Built-in rule types: `SchemaConformanceRule`, `PolicyComplianceRule`, `ConfidenceThresholdRule`, `HallucinationDetectionRule`, `CognitiveDriftRule`, `FactConsistencyRule`, `OutputFormatRule`
  - `VerifierRegistry` for composable rule chains with short-circuit on failure
  - `VerificationGate` that integrates at loop boundaries (before each loop iteration proceeds)
  - `DynamicGuardrailInjector` for real-time semantic interception of agent intents against safety/compliance/policy boundaries before tool/API execution
  - Verification audit trail with tamper-evident logging
- **Acceptance Criteria**:
  - [ ] VerifierRegistry with register/unregister/compose operations
  - [ ] 7+ built-in verification rules
  - [ ] DynamicGuardrailInjector with real-time intent checking
  - [ ] Integration hooks at loop boundaries
  - [ ] Verification audit trail
  - [ ] Thread-safe singleton `get_verification_engine()`
  - [ ] Wired into brain_os.py and platform_router.py
  - [ ] Unit tests for each rule type and composition
- **Dependencies**: None
- **Estimated Complexity**: High

### CORE-003: Intent Router Engineering
- **Priority**: P0
- **Category**: Deterministic Routing & Cost Optimization
- **Description**: Fast intent classifier front-door that routes queries to the cheapest capable path: deterministic DAG (graph lookup, cached answer, template fill) vs. full agentic pipeline. Routes 60-70% of queries down cheap deterministic paths.
- **Rationale**: Cuts compute costs by 40-60% for enterprise deployments. Most queries don't need full agentic reasoning — a graph lookup or cached answer suffices.
- **Implementation**:
  - Create `packages/eoip/routing/engine.py`
  - Create `packages/eoip/routing/__init__.py`
  - `IntentClassifier` with fast text classification (TF-IDF + lightweight model, no LLM)
  - Intent categories: `GRAPH_LOOKUP`, `CACHED_ANSWER`, `TEMPLATE_FILL`, `SIMPLE_RAG`, `MULTI_STEP_RAG`, `AGENTIC_REASONING`, `GRAPH_MUTATION`, `ADMIN_OPERATION`
  - `RoutingDecision` with confidence, selected path, estimated cost, estimated latency
  - `RouterEngine` orchestrating classification, path selection, cost estimation
  - Feedback loop: track actual vs predicted cost/latency for classifier improvement
  - Integration with `cost_optimization/engine.py` for budget-aware routing
- **Acceptance Criteria**:
  - [ ] IntentClassifier with 8+ intent categories
  - [ ] Sub-10ms classification latency
  - [ ] RoutingDecision with cost/latency estimates
  - [ ] Feedback loop for classifier accuracy tracking
  - [ ] Integration with cost_optimization engine
  - [ ] Thread-safe singleton `get_router_engine()`
  - [ ] Wired into brain_os.py and platform_router.py
  - [ ] Unit tests with diverse query types
- **Dependencies**: CORE-001 (token formats for payload sizing)
- **Estimated Complexity**: High

### CORE-004: Graph-over-Graph Engineering
- **Priority**: P0
- **Category**: Graph Intelligence
- **Description**: Third graph execution mode alongside Graph-over-Loop and Loop-over-Graph. Meta-graph operations that layer graphs: ontology graph over instance graph, temporal graph over current graph, compliance graph over data graph, knowledge graph over schema graph.
- **Rationale**: Enterprise customers need cross-layer graph queries. Example: "which data entities violate constraints defined in the compliance ontology?" requires querying across graph layers.
- **Implementation**:
  - Create `packages/eoip/graph_graph/engine.py`
  - Create `packages/eoip/graph_graph/__init__.py`
  - `GraphLayer` abstraction (name, graph_type, priority, schema)
  - `LayerRelation` defining cross-layer edges (maps_to, constrains, extends, overrides)
  - `GraphOverGraphEngine` with `project(query, layers)`, `cross_layer_query(source_layer, target_layer, pattern)`, `merge_layers()`, `diff_layers()`
  - Built-in layer types: `ONTOLOGY`, `INSTANCE`, `TEMPORAL`, `COMPLIANCE`, `SCHEMA`, `PROVENANCE`, `SECURITY`
  - Cross-layer constraint propagation
  - Layer-aware query planning (which layers to activate for a given query)
- **Acceptance Criteria**:
  - [ ] GraphLayer abstraction with 7+ built-in types
  - [ ] Cross-layer query execution
  - [ ] Layer projection and merging
  - [ ] Layer diff for change detection
  - [ ] Constraint propagation across layers
  - [ ] Thread-safe singleton `get_graph_graph_engine()`
  - [ ] Wired into brain_os.py and platform_router.py
  - [ ] Unit tests for cross-layer operations
- **Dependencies**: None
- **Estimated Complexity**: High

### CORE-005: Loop-over-Loop Engineering
- **Priority**: P1
- **Category**: Meta-Orchestration
- **Description**: Supervisory loops that orchestrate inner loops. An outer OODA loop can supervise inner ReAct loops, a meta-evaluation loop can monitor reasoning quality across multiple inner reasoning loops, and an adaptation loop can switch strategies when inner loops underperform.
- **Implementation**:
  - Extend `packages/eoip/intelligence_eng/engine.py` with `SupervisoryLoop` class
  - `LoopMonitor` tracking inner loop metrics (iterations, convergence, cost, quality)
  - `LoopSwitcher` for dynamic strategy switching when inner loop underperforms
  - `LoopComposition` for declarative outer-inner loop binding
  - Timeout and circuit-breaker integration at the supervisory level
- **Acceptance Criteria**:
  - [ ] SupervisoryLoop wrapping and monitoring inner loops
  - [ ] LoopMonitor with real-time metrics
  - [ ] Dynamic strategy switching
  - [ ] Circuit-breaker integration
  - [ ] Unit tests for composition patterns
- **Dependencies**: CORE-002 (verification gates at loop boundaries)
- **Estimated Complexity**: Medium

### CORE-006: Token Budget Engineering
- **Priority**: P1
- **Category**: Token Economics
- **Description**: Dynamic token allocation across cognitive pipeline stages. A total token budget is distributed across plan steps — more tokens for reasoning, fewer for lookups — with real-time reallocation based on actual consumption.
- **Implementation**:
  - Create `packages/eoip/token_budget/engine.py`
  - Create `packages/eoip/token_budget/__init__.py`
  - `TokenBudget` with total allocation and per-stage allocations
  - `BudgetPolicy` strategies: EQUAL_SPLIT, PROPORTIONAL, PRIORITY_WEIGHTED, ADAPTIVE
  - `BudgetTracker` with real-time consumption tracking and reallocation
  - Integration with `intelligence_eng` cognitive plans and `cost_optimization` engine
  - Alerts when stages exceed budget, with automatic context compression triggers
- **Acceptance Criteria**:
  - [ ] TokenBudget with 4 allocation strategies
  - [ ] Real-time consumption tracking per pipeline stage
  - [ ] Dynamic reallocation when stages under/over-consume
  - [ ] Context compression triggers on budget exceed
  - [ ] Integration with intelligence_eng and cost_optimization
  - [ ] Thread-safe singleton
  - [ ] Wired into brain_os.py and platform_router.py
  - [ ] Unit tests
- **Dependencies**: CORE-001 (token format engines for accurate counting)
- **Estimated Complexity**: Medium

---

## PHASE 2 — AGENTIC AI & GRAPH INTELLIGENCE

### AGENT-001: Cognitive Boundary Telemetry
- **Priority**: P1
- **Category**: Agentic AI Engineering
- **Description**: Detect when agents hit cognitive boundaries (confidence drops, hallucination signals, context overflow, repeated tool failures, reasoning loops) and gracefully hand off to higher-autonomy loops or humans.
- **Implementation**:
  - Extend `packages/eoip/telemetry/adapter.py` with `CognitiveBoundaryDetector`
  - Boundary signals: confidence_drop, hallucination_probability, context_overflow, tool_failure_streak, reasoning_loop_detected, latency_spike, cost_overrun
  - `HandoffDecision` with target (human, higher-autonomy loop, fallback agent)
  - Integration with the 14 control loops for autonomy escalation
- **Acceptance Criteria**:
  - [ ] 7+ boundary signal detectors
  - [ ] HandoffDecision with target selection
  - [ ] Integration with control loop autonomy levels
  - [ ] Telemetry event emission on boundary detection
  - [ ] Unit tests for each signal type
- **Dependencies**: None
- **Estimated Complexity**: Medium

### AGENT-002: Dynamic Entity & Community Extraction Pipeline
- **Priority**: P1
- **Category**: Knowledge Graph Construction
- **Description**: Real-time pipeline: document ingestion -> chunking -> entity extraction -> relation extraction -> triple generation -> community detection -> knowledge graph update. Automates KG construction from unstructured data.
- **Implementation**:
  - Create `packages/eoip/extraction/engine.py`
  - Create `packages/eoip/extraction/__init__.py`
  - `DocumentChunker` with configurable strategies (sentence, paragraph, semantic)
  - `EntityExtractor` (extend existing `nlp/pipeline.py` with transformer-ready interface)
  - `RelationExtractor` for subject-predicate-object triple generation
  - `CommunityDetector` wrapping existing Leiden/Louvain algorithms
  - `ExtractionPipeline` orchestrating the full flow
  - Streaming mode for continuous ingestion
- **Acceptance Criteria**:
  - [ ] Configurable chunking strategies
  - [ ] Entity extraction with type classification
  - [ ] Relation extraction producing triples
  - [ ] Community detection integration
  - [ ] Streaming mode for continuous operation
  - [ ] Thread-safe singleton
  - [ ] Wired into brain_os.py and platform_router.py
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: High

### AGENT-003: Agent Communication Bus
- **Priority**: P2
- **Category**: Agent Infrastructure
- **Description**: Formalize agent-to-agent communication with typed message schemas, capability negotiation, dead letter queues, and persistent message history. Extend existing `A2AProtocolBroker` from in-memory list to durable bus.
- **Implementation**:
  - Create `packages/eoip/agents/message_bus.py`
  - `AgentMessageSchema` with versioned message types
  - `CapabilityNegotiation` protocol for agent discovery
  - `MessageQueue` with persistence, TTL, and DLQ
  - `BroadcastChannel` for pub/sub patterns
  - Integration with existing 35 agent archetypes
- **Acceptance Criteria**:
  - [ ] Typed message schemas with versioning
  - [ ] Capability negotiation protocol
  - [ ] Persistent message queue with DLQ
  - [ ] Pub/sub broadcast channels
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: Medium

### AGENT-004: Parallel Fan-Out/Fan-In (MapReduce)
- **Priority**: P1
- **Category**: Pipeline Engineering
- **Description**: Formalize the parallel execution pattern from `analytics/parallel_multihop.py` into a first-class harness capability. Race-condition-safe state merging for fan-in.
- **Implementation**:
  - Extend `packages/eoip/harness/engine.py` with `FanOutStage` and `FanInStage`
  - `StateSchema` for safe state merging (conflict detection, merge strategies)
  - Configurable parallelism (max workers, timeout per shard)
  - Integration with harness pipeline orchestration
- **Acceptance Criteria**:
  - [ ] FanOutStage splitting work into parallel shards
  - [ ] FanInStage merging results with conflict detection
  - [ ] Configurable parallelism and timeouts
  - [ ] Integration with existing harness engine
  - [ ] Unit tests with race condition scenarios
- **Dependencies**: None
- **Estimated Complexity**: Medium

### GRAPH-001: Federated Graph Engineering
- **Priority**: P1
- **Category**: Graph Intelligence
- **Description**: Cross-database knowledge graph federation. Query across Neo4j, Neptune, TigerGraph, and other backends as one virtual graph. Leverages existing 17+ database adapters.
- **Implementation**:
  - Create `packages/eoip/federation/engine.py`
  - Create `packages/eoip/federation/__init__.py`
  - `FederatedGraph` virtual graph spanning multiple backends
  - `FederationPlanner` decomposing queries across backends
  - `ResultMerger` combining results with deduplication and conflict resolution
  - `CatalogService` maintaining cross-backend entity mappings
  - Query pushdown optimization (push filters to backend)
- **Acceptance Criteria**:
  - [ ] Virtual graph spanning 2+ backends
  - [ ] Query decomposition and result merging
  - [ ] Entity mapping across backends
  - [ ] Query pushdown optimization
  - [ ] Thread-safe singleton
  - [ ] Wired into brain_os.py and platform_router.py
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: High

### GRAPH-002: Causal Inference over Graphs
- **Priority**: P2
- **Category**: Graph Intelligence
- **Description**: Counterfactual reasoning: "What would happen if we removed this supplier node?" Extends existing causal reasoning strategy with graph-native do-calculus and intervention analysis.
- **Implementation**:
  - Create `packages/eoip/causal/engine.py`
  - `InterventionModel` for do(X=x) operations on graph
  - `CounterfactualQuery` for what-if analysis
  - `CausalEffect` estimation with confounding control
  - `BlastRadiusAnalysis` for impact assessment of node/edge removal
  - Integration with existing `reasoning/strategies.py` causal strategy
- **Acceptance Criteria**:
  - [ ] do-calculus intervention on graph entities
  - [ ] Counterfactual query execution
  - [ ] Blast radius analysis
  - [ ] Integration with existing causal reasoning
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: High

### GRAPH-003: Knowledge Distillation Engineering
- **Priority**: P2
- **Category**: Edge & Performance
- **Description**: Compress large graph subsets into compact queryable representations for edge deployment or fast retrieval. Produces distilled knowledge packages.
- **Implementation**:
  - Create `packages/eoip/distillation/engine.py`
  - `DistillationStrategy` (subgraph extraction, entity summarization, relation compression)
  - `KnowledgePackage` — compact portable graph representation
  - `PackageDeployer` for edge/runtime deployment
  - Integration with `edge/runtime.py`
- **Acceptance Criteria**:
  - [ ] Graph distillation with configurable strategies
  - [ ] Portable knowledge packages
  - [ ] Edge deployment integration
  - [ ] Fidelity metrics (information loss measurement)
  - [ ] Unit tests
- **Dependencies**: GRAPH-001 (federation for source graphs)
- **Estimated Complexity**: Medium

### GRAPH-004: Graph Neural Network Integration
- **Priority**: P2
- **Category**: AI/ML & Graph
- **Description**: GNN-powered graph intelligence: node classification, link prediction, graph embeddings (node2vec, TransE), and graph-level classification. Extends graph algorithms beyond deterministic methods.
- **Implementation**:
  - Create `packages/eoip/gnn/engine.py`
  - `GraphEmbedder` with node2vec, TransE, and configurable embedding dimensions
  - `LinkPredictor` for predicting missing graph connections
  - `NodeClassifier` for entity type inference
  - `CommunityPredictor` for graph-level patterns
  - Integration with existing analytics algorithms
- **Acceptance Criteria**:
  - [ ] Graph embedding generation (node2vec, TransE)
  - [ ] Link prediction with confidence scores
  - [ ] Node classification
  - [ ] Integration with existing graph store
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: High

### GRAPH-005: Temporal & Hybrid Retrieval Engineering
- **Priority**: P1
- **Category**: Retrieval
- **Description**: Elevate temporal dimension in retrieval — facts evolve over time. Add TemporalIndex maintaining fact validity windows with as-of queries. Combine with existing vector semantic and graph structural search.
- **Implementation**:
  - Create `packages/eoip/retrieval/temporal.py`
  - `TemporalIndex` with valid_from/valid_to windows per fact
  - `AsOfQuery` for point-in-time retrieval
  - `TemporalRangeQuery` for time-windowed retrieval
  - Integration with existing `state/engine.py` time-travel and `search/hybrid_engine.py`
- **Acceptance Criteria**:
  - [ ] TemporalIndex with validity windows
  - [ ] As-of and range queries
  - [ ] Integration with state time-travel
  - [ ] Integration with hybrid search
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: Medium

### GRAPH-006: OWL Reasoning & SHACL Runtime Validation
- **Priority**: P2
- **Category**: Ontology
- **Description**: Runtime OWL DL classification and SHACL shape validation against live graph data. Currently ontology layer handles mapping/drift but not runtime reasoning/validation.
- **Implementation**:
  - Extend `packages/eoip/ontology/rdf.py` with `OWLReasoner`
  - Create `packages/eoip/ontology/shacl_validator.py`
  - `OWLReasoner` for subsumption, disjointness, property chain inference
  - `SHACLValidator` validating graph instances against SHACL shape definitions
  - Validation report with violations, severity, fix suggestions
- **Acceptance Criteria**:
  - [ ] OWL subsumption and inference
  - [ ] SHACL shape validation
  - [ ] Violation report with severity levels
  - [ ] Integration with ontology management
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: High

---

## PHASE 3 — AI/ML INTELLIGENCE ENHANCEMENTS

### AI-001: Advanced XAI Engine
- **Priority**: P1
- **Category**: Explainable AI
- **Description**: Extend existing heuristic XAI attribution with model-derived explainability: SHAP-like feature importance, attention visualization, decision trace graphs, and confidence calibration visualization.
- **Implementation**:
  - Create `packages/eoip/xai/engine.py`
  - Create `packages/eoip/xai/__init__.py`
  - `FeatureImportanceAnalyzer` (SHAP-like, without external dependency)
  - `DecisionTraceGraph` — graph of reasoning steps with attribution
  - `ConfidenceCalibrationReport` — expected vs actual accuracy
  - `ExplanationRenderer` producing human-readable explanations
  - Integration with existing `self_llm.py` XAI explanation
- **Acceptance Criteria**:
  - [ ] Feature importance analysis
  - [ ] Decision trace graph generation
  - [ ] Confidence calibration
  - [ ] Human-readable explanation rendering
  - [ ] Thread-safe singleton
  - [ ] Wired into brain_os.py and platform_router.py
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: High

### AI-002: Deep NLP Pipeline
- **Priority**: P2
- **Category**: Natural Language Processing
- **Description**: Extend existing gazetteer/regex NLP pipeline with deeper capabilities: transformer-ready NER interface, sentiment analysis, topic modeling, dependency parsing stubs, language detection, and coreference resolution.
- **Implementation**:
  - Extend `packages/eoip/nlp/pipeline.py`
  - `DeepEntityExtractor` with pluggable model backends (local or API)
  - `SentimentAnalyzer` with aspect-based sentiment
  - `TopicModeler` with LDA-style topic extraction
  - `LanguageDetector` for multi-language support
  - `CoreferenceResolver` for entity mentions
- **Acceptance Criteria**:
  - [ ] Deep NER with configurable backends
  - [ ] Sentiment analysis with aspect extraction
  - [ ] Topic modeling
  - [ ] Language detection
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: Medium

### AI-003: Relation Extraction & Triple Generation
- **Priority**: P1
- **Category**: Knowledge Graph Construction
- **Description**: Automated subject-predicate-object triple extraction from unstructured text. Feeds the knowledge graph construction pipeline.
- **Implementation**:
  - Create `packages/eoip/extraction/relation_extractor.py`
  - `RelationPattern` with configurable extraction rules
  - `TripleGenerator` producing (subject, predicate, object) triples
  - `TripleValidator` checking against ontology schema
  - `TripleDeduplicator` merging duplicate/near-duplicate triples
  - Integration with AGENT-002 extraction pipeline
- **Acceptance Criteria**:
  - [ ] Pattern-based relation extraction
  - [ ] Triple generation with confidence scores
  - [ ] Ontology-aware validation
  - [ ] Deduplication
  - [ ] Unit tests
- **Dependencies**: AGENT-002
- **Estimated Complexity**: Medium

### AI-004: Model A/B Testing & Canary Deployment
- **Priority**: P2
- **Category**: MLOps
- **Description**: Add A/B testing framework and canary deployment to existing model registry. Compare model performance in production with statistical significance testing.
- **Implementation**:
  - Extend `packages/eoip/model_management/registry.py`
  - `ABExperiment` with traffic splitting, metric collection, significance testing
  - `CanaryDeployment` with gradual rollout and automatic rollback
  - `ModelComparison` dashboard data (latency, quality, cost per model)
- **Acceptance Criteria**:
  - [ ] A/B experiment creation and traffic splitting
  - [ ] Statistical significance testing
  - [ ] Canary deployment with auto-rollback
  - [ ] Comparison metrics
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: Medium

### AI-005: MLOps Experiment Tracking
- **Priority**: P2
- **Category**: MLOps
- **Description**: Lightweight experiment tracking (inspired by MLflow/W&B) for prompt iterations, model comparisons, and fine-tuning runs. Tracks parameters, metrics, artifacts.
- **Implementation**:
  - Create `packages/eoip/mlops/experiment_tracker.py`
  - `Experiment` with runs, parameters, metrics, tags
  - `RunTracker` for individual experiment runs
  - `ArtifactStore` for model artifacts and outputs
  - `ExperimentComparison` for cross-run analysis
- **Acceptance Criteria**:
  - [ ] Experiment creation and run tracking
  - [ ] Parameter and metric logging
  - [ ] Artifact storage
  - [ ] Cross-run comparison
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: Medium

### AI-006: Embedding Management & Versioning
- **Priority**: P2
- **Category**: Vector Intelligence
- **Description**: Dedicated embedding lifecycle management: versioned embeddings, domain fine-tuning pipeline stubs, multi-modal embedding fusion, and drift detection.
- **Implementation**:
  - Create `packages/eoip/embeddings/engine.py`
  - `EmbeddingRegistry` with version tracking
  - `EmbeddingDriftDetector` extending existing `ontology/embedding_drift.py`
  - `EmbeddingFusionStrategy` for multi-modal combination
  - `DimensionReducer` for visualization and storage optimization
- **Acceptance Criteria**:
  - [ ] Embedding versioning and registry
  - [ ] Drift detection
  - [ ] Multi-modal fusion
  - [ ] Dimension reduction
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: Medium

### AI-007: Probabilistic Reasoning Integration
- **Priority**: P3
- **Category**: Reasoning
- **Description**: Add probabilistic graph models to existing reasoning strategies: Bayesian networks over knowledge graphs, uncertain fact propagation, and probabilistic query answering.
- **Implementation**:
  - Extend `packages/eoip/reasoning/strategies.py`
  - `BayesianGraphReasoner` for probabilistic inference
  - `UncertaintyPropagator` for fact confidence propagation
  - `ProbabilisticQueryEngine` for queries with confidence intervals
- **Acceptance Criteria**:
  - [ ] Bayesian inference over graph structures
  - [ ] Uncertainty propagation
  - [ ] Probabilistic query answering with confidence intervals
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: High

---

## PHASE 4 — INFRASTRUCTURE & DEVOPS

### INFRA-001: Multi-Level Caching
- **Priority**: P1
- **Category**: Performance
- **Description**: Extend existing single-level LRU cache to L1 (in-memory) + L2 (Redis) with distributed invalidation. Redis is in Helm chart but not wired to cache layer.
- **Implementation**:
  - Extend `packages/eoip/enterprise/cache.py`
  - `L1Cache` (existing in-memory LRU)
  - `L2Cache` (Redis adapter)
  - `CacheCoordinator` with read-through, write-through, and write-behind strategies
  - Distributed cache invalidation via pub/sub
  - Cache warming strategies for hot paths
- **Acceptance Criteria**:
  - [ ] L1 + L2 cache hierarchy
  - [ ] Read-through and write-through strategies
  - [ ] Distributed invalidation
  - [ ] Cache warming
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: Medium

### INFRA-002: OAuth2/OIDC/SSO Integration
- **Priority**: P1
- **Category**: Security
- **Description**: Add external identity provider support to existing RBAC/ABAC system. Support OAuth2 authorization code flow, OIDC discovery, and SAML for enterprise SSO.
- **Implementation**:
  - Extend `packages/eoip/authz/`
  - `OAuthProvider` with authorization code flow
  - `OIDCDiscovery` for provider auto-configuration
  - `SAMLAdapter` for enterprise SSO
  - `TokenValidator` for JWT verification
  - `IdPFederation` for multi-provider support
- **Acceptance Criteria**:
  - [ ] OAuth2 authorization code flow
  - [ ] OIDC discovery and verification
  - [ ] SAML adapter
  - [ ] JWT token validation
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: High

### INFRA-003: CD Pipeline & GitOps Deployment
- **Priority**: P2
- **Category**: DevOps
- **Description**: Add continuous deployment pipeline to existing CI. ArgoCD/Flux integration, staging environment, canary deployment, automated rollback.
- **Implementation**:
  - Create `deploy/argocd/` with Application manifests
  - Create `deploy/environments/` (staging, production)
  - Extend `.github/workflows/` with CD stages
  - Health check endpoints for deployment verification
  - Automated rollback on health check failure
- **Acceptance Criteria**:
  - [ ] ArgoCD Application manifests
  - [ ] Staging and production environment configs
  - [ ] CD workflow stages in GitHub Actions
  - [ ] Health check verification
  - [ ] Automated rollback
- **Dependencies**: None
- **Estimated Complexity**: Medium

### INFRA-004: Log Aggregation
- **Priority**: P2
- **Category**: Observability
- **Description**: Structured logging with aggregation support. Currently has Prometheus metrics and optional OTel but no log pipeline.
- **Implementation**:
  - Create `packages/eoip/observability/logging.py`
  - Structured JSON logging with correlation IDs
  - Log level management per module
  - Loki/ELK-compatible output format
  - Log sampling for high-volume paths
- **Acceptance Criteria**:
  - [ ] Structured JSON logging
  - [ ] Correlation ID propagation
  - [ ] Per-module log level control
  - [ ] Loki-compatible format
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: Low

### INFRA-005: Distributed Scheduling
- **Priority**: P2
- **Category**: Infrastructure
- **Description**: Extend existing cron-style scheduler for HA: leader election, distributed task locking, dependency DAGs between scheduled tasks.
- **Implementation**:
  - Extend `packages/eoip/scheduling/executor.py`
  - `LeaderElection` for single-scheduler guarantee
  - `DistributedLock` for task exclusivity
  - `TaskDAG` for dependency-ordered scheduling
  - Failover and catch-up execution
- **Acceptance Criteria**:
  - [ ] Leader election mechanism
  - [ ] Distributed task locking
  - [ ] Task dependency DAGs
  - [ ] Failover handling
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: Medium

### INFRA-006: API Versioning & Client SDK Generation
- **Priority**: P2
- **Category**: Developer Experience
- **Description**: Explicit API versioning strategy (v1/v2 coexistence) and auto-generated client SDKs for Python, JavaScript, and Go from OpenAPI schema.
- **Implementation**:
  - API version routing middleware
  - Deprecation headers and sunset policy
  - OpenAPI-generator integration for SDK output
  - SDK packaging scripts
- **Acceptance Criteria**:
  - [ ] API version coexistence (v1 + v2)
  - [ ] Deprecation headers
  - [ ] Generated Python SDK
  - [ ] Generated JavaScript SDK
  - [ ] SDK packaging
- **Dependencies**: None
- **Estimated Complexity**: Medium

### INFRA-007: Automated Backup & Restore Testing
- **Priority**: P2
- **Category**: Reliability
- **Description**: Extend existing WAL/recovery with automated backup scheduling, backup verification, and restore testing. Currently has WAL with point-in-time recovery but no automated scheduling.
- **Implementation**:
  - Extend `packages/eoip/recovery/`
  - `BackupScheduler` with configurable intervals
  - `BackupVerifier` for integrity checking
  - `RestoreTestRunner` for automated restore validation
  - Backup encryption at rest
- **Acceptance Criteria**:
  - [ ] Automated backup scheduling
  - [ ] Backup integrity verification
  - [ ] Automated restore testing
  - [ ] Encryption at rest
  - [ ] Unit tests
- **Dependencies**: None
- **Estimated Complexity**: Medium

---

## PHASE 5 — GUI/UI/UX ENHANCEMENTS

### UI-001: Component Library & Design System
- **Priority**: P1
- **Category**: Frontend Architecture
- **Description**: Establish shared UI component library with Storybook documentation. Currently all 90+ components are custom-built with no shared design system.
- **Implementation**:
  - Create `apps/web/src/components/ui/` shared library
  - Button, Input, Select, Modal, Toast, Card, Badge, Tabs, Tooltip components
  - Storybook setup with component documentation
  - Design tokens (colors, spacing, typography, shadows)
  - Dark/light theme variants for each component
- **Acceptance Criteria**:
  - [ ] 10+ shared UI components
  - [ ] Storybook setup with stories for each component
  - [ ] Design tokens file
  - [ ] Theme-aware components
  - [ ] Component documentation

### UI-002: Internationalization (i18n/l10n)
- **Priority**: P2
- **Category**: Global Readiness
- **Description**: Add i18n support to the frontend. Zero internationalization exists currently.
- **Implementation**:
  - Install react-i18next or equivalent
  - Extract all UI strings to locale files
  - Language selector component
  - RTL support for Arabic/Hebrew
  - Date/number formatting per locale
- **Acceptance Criteria**:
  - [ ] i18n framework integrated
  - [ ] English locale file with all strings
  - [ ] Language selector
  - [ ] Date/number locale formatting
  - [ ] At least 2 locale files

### UI-003: Advanced Data Grid
- **Priority**: P2
- **Category**: Data Presentation
- **Description**: Replace raw HTML tables with advanced data grid (TanStack Table or ag-Grid) for sorting, filtering, pagination, column resizing, and virtual scrolling.
- **Implementation**:
  - Integrate TanStack Table or ag-Grid
  - Replace tables in admin panels, audit logs, job lists
  - Virtual scrolling for large datasets
  - Column configuration persistence
- **Acceptance Criteria**:
  - [ ] Grid component with sort/filter/paginate
  - [ ] Virtual scrolling for 10K+ rows
  - [ ] Column resize and reorder
  - [ ] Applied to 3+ existing tables

### UI-004: Charting Library Integration
- **Priority**: P2
- **Category**: Data Visualization
- **Description**: Replace hand-rolled SVG charts with a proper charting library (Recharts or Chart.js) for consistency and capability.
- **Implementation**:
  - Integrate Recharts or Chart.js
  - Standard chart types: line, bar, pie, scatter, radar, heatmap
  - Theme-aware colors
  - Interactive tooltips and zoom
- **Acceptance Criteria**:
  - [ ] Charting library integrated
  - [ ] 6+ chart types available
  - [ ] Theme-aware
  - [ ] Applied to existing metric displays

### UI-005: PDF/CSV Export
- **Priority**: P2
- **Category**: Enterprise Features
- **Description**: Add PDF and CSV export to existing JSON/HTML export. Enterprise customers need printable reports and data export.
- **Implementation**:
  - PDF generation (jsPDF or server-side)
  - CSV export for tabular data
  - Export button on all data views
  - Report template system
- **Acceptance Criteria**:
  - [ ] PDF export for graph reports
  - [ ] CSV export for tabular data
  - [ ] Export buttons on data views
  - [ ] Report templates

### UI-006: Visual Workflow Builder
- **Priority**: P3
- **Category**: Low-Code
- **Description**: Drag-and-drop workflow builder for creating harness pipelines, agent orchestrations, and data processing flows without code.
- **Implementation**:
  - React Flow or similar library
  - Node types for pipeline stages, agent calls, conditions, loops
  - Connection validation
  - Workflow export to harness pipeline config
- **Acceptance Criteria**:
  - [ ] Drag-and-drop canvas
  - [ ] Node palette with 10+ node types
  - [ ] Connection validation
  - [ ] Export to pipeline config

### UI-007: Missing Dashboard Lenses
- **Priority**: P2
- **Category**: Dashboard
- **Description**: Implement the 6 planned but unbuilt lenses: Timeline, Change, Runtime, Release, Process, Simulation.
- **Implementation**:
  - `TimelineLens.jsx` — temporal view of knowledge graph evolution
  - `ChangeLens.jsx` — diff view of graph mutations
  - `RuntimeLens.jsx` — live system metrics and agent activity
  - `ReleaseLens.jsx` — deployment and version tracking
  - `ProcessLens.jsx` — workflow execution monitoring
  - `SimulationLens.jsx` — what-if scenario runner
- **Acceptance Criteria**:
  - [ ] All 6 lenses implemented
  - [ ] Navigation integration
  - [ ] Data connected to backend APIs
  - [ ] Theme-aware

### UI-008: Search Analytics & Relevance Dashboard
- **Priority**: P2
- **Category**: Search Intelligence
- **Description**: Dashboard showing search query analytics, click-through rates, zero-result queries, and relevance tuning controls.
- **Implementation**:
  - Search event logging
  - Analytics aggregation (top queries, zero-result rate, CTR)
  - Relevance tuning controls (boost/bury, synonyms, stopwords)
  - A/B testing for search ranking experiments
- **Acceptance Criteria**:
  - [ ] Search event logging
  - [ ] Analytics dashboard
  - [ ] Relevance tuning controls
  - [ ] A/B testing for ranking

### UI-009: Real-time Collaboration
- **Priority**: P3
- **Category**: Collaboration
- **Description**: Multi-user real-time collaboration on graph exploration, annotations, and queries. Currently has workspaces but no real-time sync.
- **Implementation**:
  - CRDT-based state synchronization
  - Presence indicators (who's viewing what)
  - Shared cursors on graph canvas
  - Real-time annotation sync
- **Acceptance Criteria**:
  - [ ] Real-time state sync between users
  - [ ] Presence indicators
  - [ ] Shared graph exploration
  - [ ] Annotation sync

---

## PHASE 6 — COMPLIANCE, SECURITY & TESTING

### COMPLY-001: Compliance-as-Code Graph Constraints
- **Priority**: P1
- **Category**: Regulatory Compliance
- **Description**: Encode regulatory rules (GDPR, SOX, HIPAA) as graph constraint patterns checked continuously against the knowledge graph. Currently compliance packs are skeleton-only.
- **Implementation**:
  - Create `packages/eoip/compliance/constraints.py`
  - `ComplianceRule` encoded as graph patterns
  - `ContinuousMonitor` running rules against graph mutations
  - `ViolationReport` with severity, affected entities, remediation
  - Dashboard integration for compliance posture
- **Acceptance Criteria**:
  - [ ] Graph-pattern compliance rules
  - [ ] Continuous monitoring on graph mutations
  - [ ] Violation reporting with remediation
  - [ ] GDPR, SOX, HIPAA rule templates
  - [ ] Unit tests

### COMPLY-002: Automated PII Detection & Anonymization
- **Priority**: P1
- **Category**: Privacy
- **Description**: Automated PII scanning across graph entities with anonymization/pseudonymization. Currently privacy module has DSAR but no automated scanning.
- **Implementation**:
  - Extend `packages/eoip/privacy/`
  - `PIIScanner` detecting names, emails, phones, SSNs, addresses in graph properties
  - `Anonymizer` with k-anonymity and differential privacy strategies
  - `Pseudonymizer` with reversible token replacement
  - Scheduled scanning of new graph entities
- **Acceptance Criteria**:
  - [ ] PII detection across graph properties
  - [ ] k-anonymity implementation
  - [ ] Pseudonymization with token mapping
  - [ ] Scheduled scanning
  - [ ] Unit tests

### COMPLY-003: Continuous Compliance Monitoring Dashboard
- **Priority**: P2
- **Category**: Compliance
- **Description**: Real-time compliance posture dashboard with attestation tracking, evidence collection, and audit readiness scoring.
- **Implementation**:
  - Compliance score calculation per framework
  - Evidence collection automation
  - Attestation workflow
  - Audit trail export
- **Acceptance Criteria**:
  - [ ] Per-framework compliance scores
  - [ ] Evidence collection
  - [ ] Attestation tracking
  - [ ] Audit export

### TEST-001: Chaos Engineering Framework
- **Priority**: P2
- **Category**: Reliability Testing
- **Description**: Fault injection testing for graph store failures, network partitions, agent timeouts, and cascading failures.
- **Implementation**:
  - Create `tests/chaos/` framework
  - `FaultInjector` for controlled failure injection
  - Scenarios: graph store unavailable, RAG timeout, agent crash, memory exhaustion
  - Recovery verification after fault clearance
- **Acceptance Criteria**:
  - [ ] Fault injection framework
  - [ ] 5+ chaos scenarios
  - [ ] Recovery verification
  - [ ] CI integration (optional runs)

### TEST-002: Load Testing Framework
- **Priority**: P1
- **Category**: Performance Testing
- **Description**: Production-scale load testing with k6 or Locust. Currently performance tests use in-memory stores only.
- **Implementation**:
  - Create `tests/load/` with k6 scripts
  - Scenarios: concurrent queries, bulk ingestion, agent swarm, RAG under load
  - Latency percentile targets (p50, p90, p99)
  - Throughput baselines
- **Acceptance Criteria**:
  - [ ] Load test scripts
  - [ ] 4+ load scenarios
  - [ ] Latency and throughput targets
  - [ ] CI-runnable (optional)

### TEST-003: Property-Based & Fuzz Testing
- **Priority**: P2
- **Category**: Testing Quality
- **Description**: Add Hypothesis-based property testing and fuzz testing for serialization, query parsing, and graph operations.
- **Implementation**:
  - Hypothesis strategies for graph structures, queries, payloads
  - Fuzz testing for token format serialization round-trips
  - Property tests for query transpilation
- **Acceptance Criteria**:
  - [ ] Hypothesis test suite
  - [ ] Fuzz tests for serialization
  - [ ] Property tests for query engine
  - [ ] CI integration

### TEST-004: Performance Regression Detection in CI
- **Priority**: P1
- **Category**: Quality Gates
- **Description**: Automated performance regression detection in CI pipeline. Compare benchmark results against baselines, fail on regression beyond threshold.
- **Implementation**:
  - Benchmark runner in CI
  - Baseline storage and comparison
  - Regression threshold configuration
  - PR comment with performance diff
- **Acceptance Criteria**:
  - [ ] Benchmark runner in CI workflow
  - [ ] Baseline comparison
  - [ ] Configurable regression thresholds
  - [ ] PR performance report

### TEST-005: Accessibility Testing
- **Priority**: P2
- **Category**: Accessibility
- **Description**: Automated accessibility testing for frontend components. Currently has 146 ARIA attributes but no automated testing.
- **Implementation**:
  - axe-core integration in test suite
  - WCAG 2.1 AA compliance checking
  - Screen reader testing guidance
  - Accessibility CI gate
- **Acceptance Criteria**:
  - [ ] axe-core test integration
  - [ ] WCAG 2.1 AA compliance
  - [ ] CI gate for a11y violations

---

## PHASE 7 — MULTI-MODAL & ADVANCED (DEFERRED)

### MULTI-001: Scoped Multi-Modal Engineering
- **Priority**: P3
- **Category**: Multi-Modal
- **Description**: Scoped to: image-to-graph extraction (diagrams -> KG nodes) and graph-to-image rendering. NOT general multimodal perception.
- **Implementation**:
  - Add image extractors to `packages/eoip/fileparse/engine.py`
  - Diagram-to-graph parser (flowchart, ER diagram, architecture diagram)
  - Graph-to-image renderer for export
- **Acceptance Criteria**:
  - [ ] Diagram parsing to graph nodes
  - [ ] Graph-to-image rendering
  - [ ] Integration with fileparse engine

### MULTI-002: Knowledge & Memory Graph Engineering
- **Priority**: P2
- **Category**: Memory
- **Description**: Structural knowledge representations that evolve over time. Extends memory_eng with graph-native memory storage, episodic memory graphs, and memory consolidation via graph operations.
- **Implementation**:
  - Extend `packages/eoip/memory_eng/engine.py`
  - `MemoryGraph` storing memories as graph nodes with temporal edges
  - `EpisodicMemoryGraph` for session-based memory graphs
  - `MemoryConsolidationGraph` for promoting patterns to long-term graph structures
- **Acceptance Criteria**:
  - [ ] Graph-native memory storage
  - [ ] Episodic memory graphs
  - [ ] Graph-based consolidation
  - [ ] Unit tests

---

## SUMMARY TABLE

| ID | Feature | Phase | Priority | Category | Complexity |
|---|---|---|---|---|---|
| CORE-001 | Token Format Engines (7 formats) | 1 | P0 | Token Economics | High |
| CORE-002 | Verification & Guardrail Engineering | 1 | P0 | Enterprise Trust | High |
| CORE-003 | Intent Router Engineering | 1 | P0 | Cost Optimization | High |
| CORE-004 | Graph-over-Graph Engineering | 1 | P0 | Graph Intelligence | High |
| CORE-005 | Loop-over-Loop Engineering | 1 | P1 | Meta-Orchestration | Medium |
| CORE-006 | Token Budget Engineering | 1 | P1 | Token Economics | Medium |
| AGENT-001 | Cognitive Boundary Telemetry | 2 | P1 | Agentic AI | Medium |
| AGENT-002 | Dynamic Entity Extraction | 2 | P1 | KG Construction | High |
| AGENT-003 | Agent Communication Bus | 2 | P2 | Agent Infra | Medium |
| AGENT-004 | Parallel Fan-Out/Fan-In | 2 | P1 | Pipeline | Medium |
| GRAPH-001 | Federated Graph Engineering | 2 | P1 | Graph Intelligence | High |
| GRAPH-002 | Causal Inference over Graphs | 2 | P2 | Graph Intelligence | High |
| GRAPH-003 | Knowledge Distillation | 2 | P2 | Edge/Performance | Medium |
| GRAPH-004 | Graph Neural Network Integration | 2 | P2 | AI/ML & Graph | High |
| GRAPH-005 | Temporal & Hybrid Retrieval | 2 | P1 | Retrieval | Medium |
| GRAPH-006 | OWL Reasoning & SHACL Validation | 2 | P2 | Ontology | High |
| AI-001 | Advanced XAI Engine | 3 | P1 | Explainable AI | High |
| AI-002 | Deep NLP Pipeline | 3 | P2 | NLP | Medium |
| AI-003 | Relation Extraction & Triples | 3 | P1 | KG Construction | Medium |
| AI-004 | Model A/B Testing & Canary | 3 | P2 | MLOps | Medium |
| AI-005 | MLOps Experiment Tracking | 3 | P2 | MLOps | Medium |
| AI-006 | Embedding Management | 3 | P2 | Vector Intel | Medium |
| AI-007 | Probabilistic Reasoning | 3 | P3 | Reasoning | High |
| INFRA-001 | Multi-Level Caching | 4 | P1 | Performance | Medium |
| INFRA-002 | OAuth2/OIDC/SSO | 4 | P1 | Security | High |
| INFRA-003 | CD Pipeline & GitOps | 4 | P2 | DevOps | Medium |
| INFRA-004 | Log Aggregation | 4 | P2 | Observability | Low |
| INFRA-005 | Distributed Scheduling | 4 | P2 | Infrastructure | Medium |
| INFRA-006 | API Versioning & SDKs | 4 | P2 | Developer Exp | Medium |
| INFRA-007 | Automated Backup & Restore | 4 | P2 | Reliability | Medium |
| UI-001 | Component Library & Design System | 5 | P1 | Frontend | Medium |
| UI-002 | Internationalization | 5 | P2 | Global | Medium |
| UI-003 | Advanced Data Grid | 5 | P2 | Data Display | Low |
| UI-004 | Charting Library | 5 | P2 | Visualization | Low |
| UI-005 | PDF/CSV Export | 5 | P2 | Enterprise | Medium |
| UI-006 | Visual Workflow Builder | 5 | P3 | Low-Code | High |
| UI-007 | Missing Dashboard Lenses (6) | 5 | P2 | Dashboard | High |
| UI-008 | Search Analytics Dashboard | 5 | P2 | Search Intel | Medium |
| UI-009 | Real-time Collaboration | 5 | P3 | Collaboration | High |
| COMPLY-001 | Compliance-as-Code Constraints | 6 | P1 | Compliance | Medium |
| COMPLY-002 | PII Detection & Anonymization | 6 | P1 | Privacy | Medium |
| COMPLY-003 | Compliance Monitoring Dashboard | 6 | P2 | Compliance | Medium |
| TEST-001 | Chaos Engineering | 6 | P2 | Reliability | Medium |
| TEST-002 | Load Testing Framework | 6 | P1 | Performance | Medium |
| TEST-003 | Property-Based & Fuzz Testing | 6 | P2 | Testing | Medium |
| TEST-004 | Performance Regression in CI | 6 | P1 | Quality Gates | Medium |
| TEST-005 | Accessibility Testing | 6 | P2 | Accessibility | Low |
| MULTI-001 | Scoped Multi-Modal | 7 | P3 | Multi-Modal | Medium |
| MULTI-002 | Knowledge & Memory Graph Eng | 7 | P2 | Memory | Medium |

**Total**: 47 requirements across 7 phases
**P0 (Must Have)**: 4 | **P1 (Should Have)**: 17 | **P2 (Nice to Have)**: 21 | **P3 (Future)**: 5
