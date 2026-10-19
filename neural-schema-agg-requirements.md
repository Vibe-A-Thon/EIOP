# Neural Schema Architecture & Aggregate Requirements for EOIP / KnowGridFlow

> **Document ID**: NS-REQ-v1  
> **Date**: 2026-10-19  
> **Status**: Approved for Implementation  
> **Product**: Enterprise Operational Intelligence Platform (EOIP) / KnowGridFlow (KGF)  
> **Companion**: `neural-schema-implementation-plan.md` (sequencing, work packages, evidence protocol, verification gates)  
> **Audience**: AI Coding Agents, Systems Architects, and Verification Engineers  
> **Scope**: Neuro-symbolic schema induction, cognitive brain schemas, clone-structured graph schemas, LLM-era memory schemas, and attention schemas across Autonomous Agents, Knowledge Graphs (GL0–GL3), Wisdom Graphs (GW), and REVA Proof-of-Done verification.

---

## 0. Non-Negotiable Foundational Invariants

### 0.1 A File or Test is Not Proof of Completion
The existence of source code, test files, classes, or mock functions is **never** accepted as evidence of completion. Every requirement in this document is complete **only** when it passes all required verification levels defined in the companion implementation plan and produces a cryptographically sealed REVA Warrant and Proof-of-Done Ledger record (`ldg1_[0-9a-f]{64}`).

### 0.2 The Epistemic Separation Rule: Inferred vs. Observed
**Schema-filled defaults and neural predictions are NEVER facts.**
1. Any triple, slot, attribute, or relation populated via neural schema inference, slot-filling, or clone-state projection **MUST** carry `epistemic_state = "inferred"` (or `Authority.CONTROLLED_EXECUTION` with confidence band $< 10000\text{ bp}$).
2. Only data ingested directly from immutable source systems or verified human attestations may carry `epistemic_state = "observed"` or `Authority.SOURCE_SYSTEM_RECORD`.
3. Writing an `OBSERVED` record from a neural schema prediction is a **P0 Critical Defect** that triggers automatic pipeline quarantine and raises `REVA_INTEGRITY_VIOLATION`.

### 0.3 The Baseline Gating Rule
**Every neural schema capability MUST beat an empirical no-schema baseline.**
No neural schema mechanism (rapid assimilation, clone rebinding, attention gating, or LLM memory consolidation) shall be promoted to active production use unless it demonstrates a statistically significant improvement ($p < 0.01$, paired Wilcoxon signed-rank test across $\ge 100$ evaluation instances) over a deterministic, no-schema baseline (e.g., standard vector search, naive prompt retrieval, or unconstrained relation extraction). If a schema fails to beat the baseline, the system automatically falls back to baseline execution.

### 0.4 No Assumptions — Resolve, Don't Guess
All entities, properties, schemas, thresholds, and endpoints in this document are specified with exact types, bounds, and algorithms. If any ambiguity or contradiction arises, the agent must halt and log a blocking question rather than inventing undocumented behaviors.

---

## 1. Executive Summary & Scientific Foundations

The EOIP Neural Schema layer bridges cognitive neuroscience, modern graph machine learning, generative LLM memory architectures, and attention schema theory to provide autonomous AI agents and enterprise knowledge graphs with human-like rapid learning, contextual disambiguation, and metacognitive self-governance.

```
+----------------------------------------------------------------------------------------------------+
|                                    EOIP NEURAL SCHEMA FABRIC                                       |
+----------------------------------------------------------------------------------------------------+
|  1. BRAIN SCHEMAS (Tse, Morris, Hwu)         |  2. ML GRAPH SCHEMAS & CSCG (DeepMind, George)      |
|  - Fast 1-trial assimilation into mPFC       |  - Clone-Structured Cognitive Graphs (CSCG)         |
|  - Schema-consistent: < 50ms slot-filling    |  - Disambiguate polysemous entities via clone nodes |
|  - Schema-violating: ACh/NE novelty surge    |  - Zero-shot relational schema rebinding            |
+----------------------------------------------+-----------------------------------------------------+
|  3. LLM-ERA MEMORY & AUTOSCHEMAKG            |  4. ATTENTION SCHEMAS (Graziano AST)                |
|  - Dynamic episodic-to-semantic induction    |  - Agent internal causal model of attention state   |
|  - Slot-filling with SHACL constraint bounds |  - Metacognitive drift detection & self-steering    |
|  - Schema-directed retrieval scratchpads     |  - A2A Theory of Mind for multi-agent swarms        |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|                        NEURO-SYMBOLIC VERIFICATION & REVA ASSURANCE                                |
|  - Formal SHACL Core/Advanced constraint validation before graph commit                            |
|  - Baseline gating: p < 0.01 vs. raw retrieval                                                      |
|  - Epistemic labeling: schema predictions tagged strictly as 'inferred'                            |
|  - RFC 8785 Canonical JSON hashing + Ed25519 signing -> REVA Ledger ('ldg1_...')                   |
+----------------------------------------------------------------------------------------------------+
```

### 1.1 Foundation 1: Cognitive Brain Schemas (Tse, Morris 2007/2011; Hwu & Krichmar)
In biological cognition, memory consolidation classically requires weeks for hippocampal replay to train the neocortex. However, Tse et al. (Science 2007, 2011) proved that when an organism possesses an established **cognitive schema** (a mental framework representing relational regularities), new information that is **schema-consistent** is assimilated into the medial prefrontal cortex (mPFC) in a **single trial** (< 24 hours), completely bypassing prolonged hippocampal consolidation.
- **Dual Pathway**:
  - *Schema-Consistent Event*: Mapped directly to an existing schema slot. Zero gradient retraining required. Latency $\le 50\text{ ms}$.
  - *Schema-Violating Event*: Triggers simulated neuromodulatory surge (high Acetylcholine / Norepinephrine), flags high unexpected uncertainty, creates a Knowledge Gap (`gap1_...`) in REVA, and routes to the slow hippocampal accommodation loop.

### 1.2 Foundation 2: ML Graph Schemas & Clone-Structured Cognitive Graphs (CSCG)
In enterprise graphs, entities appear in multiple distinct operational contexts (e.g., an "APIService" acting as a public gateway vs. an internal auth proxy). Naive graph representations collapse these into a single node, causing severe structural hallucinations and false transitive inferences.
- **Clone-Structured Cognitive Graphs (CSCG)** (George et al., Nature Communications 2021): Splits an observed entity into latent "clone states" conditioned on temporal/causal context.
- **DeepMind Relational Schemas**: Reusable graph network templates where nodes and edges act as typed slots that can be instantaneously rebound to novel enterprise configurations without retraining.

### 1.3 Foundation 3: LLM-Era Schemas & AutoSchemaKG
Combines the generative semantic flexibility of LLMs with formal symbolic structure:
- **Automatic Schema Induction**: Extracting recurrent structural frames from multi-modal enterprise logs, API specs, and text.
- **SHACL Guardrails**: Every induced schema must compile into W3C SHACL Core shapes. If an induced candidate violates SHACL metamodels, it is quarantined.
- **Schema-Based Memory**: Agent working memory is maintained as an instantiated schema frame rather than a raw conversational context window, dramatically cutting token budgets while increasing retrieval precision.

### 1.4 Foundation 4: Attention Schema Theory (AST - Michael Graziano)
To achieve true autonomy without runaway loops, an agent requires a model of its own attention:
- **Attention Schema**: An internal, lower-dimensional descriptive representation of the agent's current attentional allocation (which entities, tools, and graph subregions are currently consuming focus, why they were chosen, and where focus is predicted to transition next).
- **Metacognitive Steering**: If the attention schema detects attentional thrashing (repeated cycles over the same node set without progress), it forces an exploratory attention shift.
- **Theory of Mind (A2A)**: Agents in a swarm query each other's attention schemas to coordinate division of labor without central bottlenecks.

---

## 2. Graph & System Hierarchy Alignment

The Neural Schema layer operates across the five canonical graph planes of EOIP/KGF:

| Level | Code | Name | Neural Schema Role | Epistemic Invariant |
|---|---|---|---|---|
| **GL0** | Instance Graph | Ground entities, edges, and bitemporal states | Target of schema-consistent slot-filling | Predictions strictly `inferred` |
| **GL1** | Meta-Graph | Abstract entity types, relation topologies, metapaths | Repository of instantiated Graph Schemas & CSCG clone templates | Formal schemas versioned with `sch1_...` |
| **GL2** | Living Brain | Unified cross-tenant, cross-domain cognitive network | Multi-agent shared memory consolidation & schema clustering | Consolidated via Merkle snapshot hashes |
| **GL3** | Enterprise Ontology | OWL/RDFS formal classes, axioms, SHACL shapes | Strict validation boundary; rejects non-conforming schemas | Zero-triple commit on SHACL violation |
| **GW** | Wisdom Graph | Decision traces, precedents, outcomes, lessons, counsel | Stores decision schemas, situation archetypes, and attention traces | Lessons bound to empirical Brier scores |

---

## 3. Core Neural Schema Requirements (Area: NS-CORE)

### `NS-CORE-001`: Unified Neural Schema Representation Specification
- **Description**: The platform **MUST** define and enforce a strict, typed schema data model representing both graph templates and cognitive memory frames.
- **Specification**: Every neural schema is identified by a prefixed ID `sch1_[0-9a-f]{64}` derived via RFC 8785 canonical JSON hashing of its structural definition.
- **Data Model**:
  ```python
  class SlotConstraint(BaseModel):
      model_config = ConfigDict(extra="forbid", strict=True)
      slot_name: str
      target_type: str  # Vertex label or XSD datatype
      cardinality_min: int = 1
      cardinality_max: Optional[int] = None
      shacl_property_shape: Optional[Dict[str, Any]] = None
      default_inference_rule: Optional[str] = None

  class NeuralSchema(BaseModel):
      model_config = ConfigDict(extra="forbid", strict=True)
      schema_id: str
      tenant_id: str
      name: str
      version: int = 1
      domain: str  # e.g., "CICD", "SECURITY", "KNOWLEDGE"
      description: str
      parent_schema_id: Optional[str] = None
      slots: List[SlotConstraint]
      metapaths: List[List[str]]
      embedding_signature: Optional[List[float]] = None
      created_at: str
      updated_at: str
      status: Literal["candidate", "shadow", "active", "deprecated"] = "candidate"
      empirical_baseline_delta: Optional[float] = None
  ```
- **Done-When**:
  - `NS-CORE-001.D01`: `NeuralSchema` model validates all slot constraints, rejects non-string keys, and computes deterministic `sch1_...` IDs.
  - `NS-CORE-001.D02`: Schemas serialize to and deserialize from RFC 8785 canonical JSON without data loss.

### `NS-CORE-002`: Dual-Pathway Assimilation Engine (Tse-Morris Pathway)
- **Description**: The system **MUST** implement a dual-pathway intake for all new observations, evaluating schema consistency before choosing between fast-path slot filling and slow-path accommodation.
- **Algorithm (Algorithm NS-1: Dual-Pathway Routing)**:
  1. Receive candidate instance observation $O = (V_o, E_o)$.
  2. Compute structural similarity against active schemas:
     $$S(O, \mathcal{S}_k) = \alpha \cdot \text{CosineSim}(e_O, e_{\mathcal{S}_k}) + (1 - \alpha) \cdot \text{GraphOverlap}(O, \mathcal{S}_k)$$
  3. If $\max_k S(O, \mathcal{S}_k) \ge \tau_{\text{consistent}}$ (default $0.85$):
     - **Path A (Fast Assimilation)**:
       - Instantaneously bind observation to $\mathcal{S}_k$.
       - Fill missing attributes via schema default rules with `epistemic_state = "inferred"`.
       - Latency **MUST** be $\le 50\text{ ms}$.
       - Emit warrant `reva.pred.schema_fast_assimilation`.
  4. Else:
     - **Path B (Novelty / Accommodation)**:
       - Trigger simulated neuromodulatory surge: $\Delta \text{Novelty} = 1.0 - \max_k S(O, \mathcal{S}_k)$.
       - Record Knowledge Gap (`gap1_...`) with scope $O$.
       - Queue observation for batch hippocampal accommodation and clustering.
- **Done-When**:
  - `NS-CORE-002.D01`: Consistent inputs assimilate in $< 50\text{ ms}$ on standard CPU without neural weight updates.
  - `NS-CORE-002.D02`: Inconsistent inputs create a valid `gap1_...` record in REVA store with status `open`.

### `NS-CORE-003`: Clone-Structured Cognitive Graph (CSCG) Engine
- **Description**: The graph runtime **MUST** implement CSCG decomposition to resolve polysemy and context-dependent behavior across enterprise entities.
- **Specification**:
  1. For any entity $u$ observed across multiple temporal sequences or call trees, allocate latent clone states $\{u^{(1)}, u^{(2)}, \dots, u^{(K)}\}$.
  2. Transition probabilities between clone states are trained via Expectation-Maximization (EM) over observation sequences:
     $$P(v^{(j)} \mid u^{(i)}) \propto T(u^{(i)}, v^{(j)}) \cdot E(v \mid v^{(j)})$$
  3. When an agent queries entity $u$ in context $C$, the system returns the specific clone $u^{(c)}$ that maximizes sequence likelihood, preventing false multi-hop paths.
- **Done-When**:
  - `NS-CORE-003.D01`: Entities with $\ge 2$ distinct operational contexts are partitioned into orthogonal clone nodes in GL1.
  - `NS-CORE-003.D02`: Random walks over CSCG demonstrate $\ge 40\%$ reduction in spurious cross-context path generation compared to collapsed graphs.

### `NS-CORE-004`: Baseline Gating & Verification Oracle
- **Description**: The runtime **MUST** execute automated baseline comparison for every proposed schema before promotion to `active`.
- **Specification**:
  1. Maintain a standard test set of $\ge 100$ gold-standard queries for the target domain.
  2. Run queries under:
     - Condition A: Deterministic baseline (unassisted multi-hop graph search / raw BM25 + dense retrieval).
     - Condition B: Schema-assisted routing (Path A assimilation + clone traversal).
  3. Measure Target Metric: F1-Score on downstream task, Token Consumption, and Execution Latency.
  4. Promotion Rule: Condition B must achieve statistically significant superiority ($p < 0.01$, Wilcoxon test) and $\ge 15\%$ token reduction. Otherwise status remains `candidate` or `shadow`.
- **Done-When**:
  - `NS-CORE-004.D01`: Automated benchmark harness outputs empirical delta and p-value.
  - `NS-CORE-004.D02`: Schemas failing the threshold are blocked from active status and logged in `docs/reva/gaps.json`.

---

## 4. Agent Schema & Memory Integration (Area: NS-AGENT)

### `NS-AGENT-001`: Schema-Structured Agent Working Memory
- **Description**: Autonomous agents **MUST** represent their transient operational context as instantiated schema slots rather than unstructured text buffers.
- **Specification**:
  - Agents initialize a `WorkingMemoryFrame` conforming to a registered `NeuralSchema`.
  - When an agent observes an environment event or tool response, it maps the response into typed slots:
    * `goal_slot`: Current task objective and constraints.
    * `entity_focus_slots`: Pointers to GL0 vertex IDs currently undergoing manipulation.
    * `hypothesis_slot`: Inferred operational premise.
    * `evidence_slots`: List of REVA warrant IDs validating current state.
  - Slot updates that violate cardinality or data types are rejected by local SHACL shape checks.
- **Done-When**:
  - `NS-AGENT-001.D01`: Agent context serialization uses structured JSON frames matching `WorkingMemoryFrame`.
  - `NS-AGENT-001.D02`: Working memory token footprint is reduced by $\ge 50\%$ compared to raw message transcript buffers.

### `NS-AGENT-002`: Attention Schema Theory (AST) Engine for Agents
- **Description**: Every autonomous agent in the system **MUST** maintain an explicit, real-time descriptive Attention Schema representing its own attentional focus.
- **Specification (The Graziano Model)**:
  ```python
  class AttentionAllocation(BaseModel):
      target_id: str  # Entity ID, tool name, or prompt section
      target_type: Literal["vertex", "edge", "tool", "memory_slot", "code_symbol"]
      intensity: float  # Normalized 0.0 - 1.0
      focus_duration_ms: float
      assigned_reason: str
      predicted_transition_target: Optional[str] = None

  class AgentAttentionSchema(BaseModel):
      agent_id: str
      timestamp: str
      primary_focus: AttentionAllocation
      peripheral_focus: List[AttentionAllocation]
      attentional_bandwidth_utilization: float  # 0.0 - 1.0
      entropy: float  # Shannon entropy of attention distribution
      thrashing_detected: bool = False
  ```
- **Attentional Thrashing Prevention**:
  If the attention entropy drops below $0.15$ while focus alternates between identical targets for $\ge 3$ consecutive cycles, `thrashing_detected` is set to `True`. The agent's control loop forces an immediate interrupt, drops current local focus, and shifts attention to peripheral hypothesis slots.
- **Done-When**:
  - `NS-AGENT-002.D01`: Attention schema updates concurrently with every agent execution step.
  - `NS-AGENT-002.D02`: Synthetic infinite loops in reasoning agents are detected and broken within 3 cycles.

### `NS-AGENT-003`: Agent-to-Agent (A2A) Attention & Theory of Mind Sharing
- **Description**: Swarms of agents communicating over `A2AProtocolBroker` **MUST** exchange attention summaries to coordinate task execution.
- **Specification**:
  1. Handoff packets between agents must include the sender's `AgentAttentionSchema`.
  2. The receiving agent parses the sender's attention schema to identify what the predecessor already scrutinized, avoiding redundant tool executions or overlapping subgraph traversals.
  3. Conflict Resolution: If two agents claim primary focus on the same mutable graph resource, the agent with higher confidence warrant authority retains focus; the other yields.
- **Done-When**:
  - `NS-AGENT-003.D01`: `AgentMessage` metadata carries serialized `AgentAttentionSchema`.
  - `NS-AGENT-003.D02`: Multi-agent collaborative benchmarks show $\ge 30\%$ reduction in duplicate tool calls.

---

## 5. Knowledge Graph & Wisdom Graph Integration (Area: NS-KG & NS-WG)

### `NS-KG-001`: AutoSchemaKG Induction Engine
- **Description**: The background knowledge ingestion pipeline **MUST** support automated induction of emergent schema candidates from heterogeneous unstructured and semi-structured streams.
- **Specification**:
  1. Ingest text, code, or HAR logs; perform noun-phrase and dependency extraction.
  2. Cluster recurrent relation triplets using sentence-transformer embeddings.
  3. Induce candidate `SlotConstraint` specifications with minimum frequency threshold $N \ge 10$.
  4. Automatically generate a candidate W3C SHACL Shape definition for each induced schema.
  5. Validate induced shape against existing GL3 ontology. If compliant, record in GL1 as `status = "candidate"`.
- **Done-When**:
  - `NS-KG-001.D01`: Ingestion of 50 enterprise API logs induces valid OpenAPI-aligned `NeuralSchema` objects without manual human authoring.
  - `NS-KG-001.D02`: Induced shapes compile into valid SHACL Turtle syntax verifiable by `eoip.ontology.shacl_validator`.

### `NS-KG-002`: Epistemic Schema Slot Projection in GL0
- **Description**: When an instance vertex is populated via schema defaults, the property must be stored with provenance metadata indicating its inferred status.
- **Specification**:
  - For property $P$ inferred on vertex $V$:
    ```json
    {
      "value": "inferred_default_val",
      "provenance": {
        "status": "inferred",
        "schema_id": "sch1_abc123...",
        "inference_rule": "default_parent_inheritance",
        "confidence_bp": 7500,
        "warrant_id": "wr1_def456..."
      }
    }
    ```
  - Query filters: `GET /graph/vertices?epistemic=observed` strictly omits all properties carrying `status = "inferred"`.
- **Done-When**:
  - `NS-KG-002.D01`: Queries filtering for observed facts return zero schema-inferred default values.
  - `NS-KG-002.D02`: Schema-inferred properties link to valid signed warrant records.

### `NS-KG-003`: Codebase Schema Induction from Ingested Repositories & Zero-Leak Fencing
- **Description**: When a code repository (GitHub, GitLab, Bitbucket, Git URL) is ingested via REVA, the Neural Schema induction engine **MUST** extract structural and architectural schemas directly from code ASTs using pure-Python analysis, strictly enforcing zero data leakage to external LLMs.
- **Specification**:
  1. Receives ingested repository ASTs from REVA's `GitRepositoryCloner` and `ts_js.py`/`python_web.py`/`java_spring.py`.
  2. Identifies recurrent architectural patterns (e.g., MVC controller-service-repository, CQRS event sourcing, middleware pipelines) using graph subtree isomorphism.
  3. Induces `NeuralSchema` definitions in GL1 with structural slots (inbound routes, service dependencies, storage resources).
  4. Enforces the **Zero-Data-Leak LLM Policy**:
     - All AST walking, clustering, and SHACL shape compilation is performed by deterministic Python scripts.
     - When semantic clustering requires vector embeddings, local offline sentence-transformers or local Ollama embeddings are used.
     - Zero proprietary source code files or confidential credentials are ever transmitted to external commercial LLMs.
- **Done-When**:
  - `NS-KG-003.D01`: Induces architectural schema templates from ingested repository ASTs without human authoring.
  - `NS-KG-003.D02`: 100% of schema induction is performed locally with zero raw code egress.

### `NS-WG-001`: Wisdom Graph Decision Schema & Situation Archetypes
- **Description**: The Wisdom Graph **MUST** structure decision traces and precedents into standardized `DecisionSchema` frames.
- **Specification**:
  - Each decision trace (`WG-TRACE-*`) is indexed by a `DecisionSchema` specifying:
    * `situation_slots`: Entity types and environmental metrics present at decision time.
    * `action_slot`: Chosen policy or tool.
    * `expected_outcome_slot`: Predicted delta.
    * `actual_outcome_slot`: Bitemporally recorded outcome.
    * `attribution_weights`: Relative causal contribution of each input entity.
  - When counsel is requested at a checkpoint, the Wisdom Graph matches the current situation against decision schemas using CSCG clone similarity, surfacing the top-3 closest precedents and applicable lessons.
- **Done-When**:
  - `NS-WG-001.D01`: Decision traces cluster into identifiable situation archetypes with silhouette score $\ge 0.45$.
  - `NS-WG-001.D02`: Checkpoint counsel latency is $\le 100\text{ ms}$ for graphs containing $\ge 100,000$ decisions.

---

## 6. REVA Verification & Assurance Integration (Area: NS-REVA)

### `NS-REVA-001`: Cryptographic Schema Registry & Translog Notarization
- **Description**: All active neural schemas **MUST** be immutably notarized in REVA's Merkle transparency log.
- **Specification**:
  1. On schema creation or promotion, canonicalize `NeuralSchema` via RFC 8785 (`reva.core.jcs`).
  2. Compute schema ID: `schema_id = "sch1_" + sha256_canonical(schema_body)`.
  3. Sign schema definition using tenant Ed25519 private key.
  4. Append signed leaf to REVA transparency log (`reva.kernel.translog`).
  5. Generate Signed Tree Head (STH).
- **Done-When**:
  - `NS-REVA-001.D01`: Schema leaf inclusion proof can be independently verified via `verify_inclusion(...)`.
  - `NS-REVA-001.D02`: Tampering with any schema slot definition invalidates the cryptographic signature.

### `NS-REVA-002`: Schema-Aware Proof-of-Done Evaluator
- **Description**: REVA's closure engine (`reva.pd.closure`) **MUST** include dedicated checks verifying that code and data artifacts comply with declared neural schemas.
- **Specification**:
  - New Closure Check: `12_schema_conformance`:
    * Evaluates whether all entities created during an verifier run adhere to active GL1 schemas.
    * Evaluates that no schema-inferred field is tagged as `observed`.
    * Validates that schema-assisted workflows beat the baseline threshold ($p < 0.01$).
  - A violation of check 12 results in outcome `failed` with reason code `CLOSURE_FAILED_SCHEMA_NONCONFORMANCE`.
- **Done-When**:
  - `NS-REVA-002.D01`: Verifier runs emitting uncalibrated schema predictions fail closure evaluation.
  - `NS-REVA-002.D02`: Valid schema runs pass check 12 and produce green closure decisions.

---

## 7. Interface Specifications (REST, MCP, CLI)

### 7.1 REST API Routes (`/api/reva/v1/schemas/`)

| Method | Endpoint | Request Body | Response Body | Description |
|---|---|---|---|---|
| `POST` | `/api/reva/v1/schemas/candidate` | `CreateSchemaRequest` | `NeuralSchema` | Submit induced or authored schema candidate |
| `GET` | `/api/reva/v1/schemas/{schema_id}` | None | `NeuralSchema` | Retrieve verified schema by ID |
| `POST` | `/api/reva/v1/schemas/{schema_id}/evaluate` | `BenchmarkSpec` | `EvaluationReport` | Run baseline comparison benchmark |
| `POST` | `/api/reva/v1/schemas/{schema_id}/promote` | `PromotionRequest` | `SignedSchemaReceipt` | Promote shadow/candidate to active upon passing gates |
| `POST` | `/api/reva/v1/schemas/assimilate` | `ObservationPayload` | `AssimilationResult` | Execute Tse-Morris dual-pathway intake |

### 7.2 Model Context Protocol (MCP) Tools

1. `reva_schema_match(observation_json: str) -> str`: Matches observation against active schemas, returning best schema ID and similarity score.
2. `reva_schema_assimilate(observation_json: str, schema_id: str) -> str`: Fast-path slot filling returning enriched entity with `inferred` labels.
3. `reva_agent_attention_get(agent_id: str) -> str`: Fetches current `AgentAttentionSchema` for an agent.
4. `reva_agent_attention_steer(agent_id: str, new_target: str, reason: str) -> str`: Metacognitive top-down steering of agent focus.

### 7.3 CLI Commands

```bash
# Register and validate schema file
reva schema validate ./schemas/api_service.yaml

# Run empirical baseline benchmark
reva schema benchmark sch1_3a8f... --testset ./fixtures/queries.json --min-delta 0.15

# Promote schema with cryptographic warrant
reva schema promote sch1_3a8f... --attestation "Approved by ML Governance"

# Inspect active attention schemas across agent mesh
reva agent attention status --all
```

---

## 8. Telemetry, Observability & Safety Metrics

The implementation **MUST** emit Prometheus metrics matching the following exact names:

1. `reva_schema_assimilation_duration_seconds{domain, pathway}`: Histogram of dual-pathway processing times (Path A vs. Path B).
2. `reva_schema_inferred_triples_total{tenant_id, schema_id}`: Counter of triples written with `inferred` status.
3. `reva_schema_baseline_lift_ratio{schema_id}`: Gauge of empirical improvement over no-schema baseline.
4. `reva_agent_attention_entropy{agent_id}`: Gauge of agent attentional dispersion (0.0 to 1.0).
5. `reva_agent_attention_thrash_events_total{agent_id}`: Counter of triggered anti-thrashing interrupts.

---

## 9. Verification & Acceptance Criteria Matrix

| Req ID | Level | Verification Command | Acceptance Threshold |
|---|---|---|---|
| `NS-CORE-001` | L2 (Unit) | `pytest tests/reva/unit/schemas/test_schema_models.py` | 100% pass, strictly extra="forbid" |
| `NS-CORE-002` | L3 (Perf) | `pytest tests/reva/perf/test_dual_pathway_latency.py` | Path A latency $\le 50\text{ ms}$ on CPU |
| `NS-CORE-003` | L2 (Unit) | `pytest tests/reva/unit/schemas/test_cscg_engine.py` | Clone states split polysemous nodes |
| `NS-CORE-004` | L5 (Gate) | `python scripts/reva/eval_schema_baseline.py --all` | All active schemas beat baseline at $p < 0.01$ |
| `NS-AGENT-001` | L2 (Unit) | `pytest tests/reva/unit/schemas/test_agent_memory.py` | Memory slots strictly SHACL-validated |
| `NS-AGENT-002` | L4 (Anti-Game) | `pytest tests/reva/unit/schemas/test_attention_schema.py` | Thrashing detected in $\le 3$ cycles |
| `NS-KG-002` | L1 (Contract) | `python scripts/reva/verify_epistemic_labels.py` | 0 occurrences of inferred marked as observed |
| `NS-REVA-001` | L6 (Ledger) | `reva translog verify --schema-leaves` | Merkle inclusion proofs pass for all schemas |
