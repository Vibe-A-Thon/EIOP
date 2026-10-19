# Neural Schema Implementation Plan & Verification Protocol

> **Document ID**: NS-PLAN-v1  
> **Date**: 2026-10-19  
> **Status**: Approved for Implementation  
> **Companion**: `neural-schema-agg-requirements.md` (normative requirements specification)  
> **Target Package**: `packages/eoip/neural/schemas/`, `packages/eoip/brain/schemas/`, `reva/schemas/`  
> **Audience**: AI Coding Agents, Systems Architects, and Verification Engineers  

---

## 0. Non-Negotiable Operational Rules

### 0.1 The Evidence Ledger Rule
A file path, class declaration, test count, or green checkmark is **never** accepted as proof that a task is complete. A task is marked complete **only** when:
1. The implementation code executes deterministically on the target environment (Windows/Linux, Python 3.11).
2. The verification command named in the task's Done-When specification has been executed with captured output.
3. Every numeric performance or accuracy metric meets or exceeds the stated threshold.
4. REVA has evaluated all Proof-of-Done obligations for the task and emitted a cryptographically signed closure record (`cls1_...`).

### 0.2 Epistemic Labeling Verification
Before any phase gate can close, an automated AST and runtime scan (`scripts/reva/verify_epistemic_labels.py`) must pass with **0 violations**, proving that:
- Zero schema-inferred fields are stored or exposed with `epistemic_state = "observed"`.
- Every schema inference carries a valid REVA Warrant reference (`wr1_...`).

### 0.3 Zero-Placeholder Enforcement
Every production file under `packages/eoip/neural/schemas/` and related directories must pass `python scripts/reva/forbid_placeholders.py` with **0 violations**. No `pass`-only stubs, no `NotImplementedError`, and no mock fallbacks in production paths.

---

## 1. Implementation Sequencing & Phase Overview

```
+---------------------------------------------------------------------------------------------------------+
|                                    NEURAL SCHEMA BUILD PHASES                                           |
+---------------------------------------------------------------------------------------------------------+
|  Phase NS-P0: Foundation & Numerical Scaffolding                                                        |
|  - Data contracts, slot models, canonical IDs, baseline testing harness                                 |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase NS-P1: Dual-Pathway Brain Schema Assimilation (Tse-Morris Pathway)                               |
|  - Fast slot-filling (< 50ms) + Slow hippocampal novelty gap routing                                    |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase NS-P2: Clone-Structured Cognitive Graphs (CSCG) & DeepMind Relational Schemas                    |
|  - Polysemy clone state splitting, EM transition matrix, zero-shot schema rebinding                     |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase NS-P3: LLM Memory Consolidation & AutoSchemaKG                                                   |
|  - Unstructured stream schema induction, SHACL shape synthesis, episodic-to-semantic consolidation      |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase NS-P4: Attention Schema Theory (AST) Engine & Metacognitive Steering                             |
|  - Real-time agent attention model, thrashing detection, A2A attention handoff                          |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase NS-P5: Graph Planes Integration (GL0, GL1, GL2, GL3, GW)                                         |
|  - Instance slot projection, Meta-Graph templates, Wisdom Graph decision archetypes                     |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|  Phase NS-P6: Empirical Baseline Gating & Final REVA Ledger Verification                                |
|  - 100-query benchmark (p < 0.01), REST/MCP interfaces, signed canonical ledger export (ldg1_...)        |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Work Packages & Task Breakdown

### Phase NS-P0: Foundation & Numerical Scaffolding

#### Task `T-NS-001`: Core Schema Contracts & Prefixed IDs (`sch1_...`)
- **File**: `packages/eoip/neural/schemas/models.py`
- **Reuses**: `reva.core.ids`, `reva.core.jcs`
- **Actions**:
  1. Implement `SlotConstraint`, `NeuralSchema`, `AssimilationResult`, and `EvaluationReport` Pydantic v2 models with `extra="forbid"`.
  2. Implement `schema_id(body: Dict[str, Any]) -> str` in `reva/core/ids.py` producing `sch1_[0-9a-f]{64}`.
- **Verification**: `pytest tests/reva/unit/schemas/test_schema_models.py`
- **Done-When**:
  - `T-NS-001.D01`: Valid schema compiles and produces deterministic `sch1_...` ID.
  - `T-NS-001.D02`: Non-string keys or float timestamps raise validation error.

#### Task `T-NS-002`: Epistemic Labeling Guardrails & AST Checker
- **File**: `scripts/reva/verify_epistemic_labels.py`
- **Actions**:
  1. Write AST static analyzer scanning all property writes across graph ingestion.
  2. Ensure any write originating from a schema module sets `epistemic_state = "inferred"`.
- **Verification**: `python scripts/reva/verify_epistemic_labels.py`
- **Done-When**:
  - `T-NS-002.D01`: Script reports `PASS (0 violations)`.

---

### Phase NS-P1: Dual-Pathway Brain Schema Assimilation (Tse-Morris Pathway)

#### Task `T-NS-003`: Fast-Path Assimilation & Slot-Filler
- **File**: `packages/eoip/neural/schemas/assimilation.py`
- **Requirements**: `NS-CORE-002`
- **Actions**:
  1. Implement `DualPathwayAssimilator` with configurable `consistency_threshold` (default $0.85$).
  2. Implement fast structural graph matcher using degree sequence + embedding cosine similarity.
  3. Implement Path A: Map input observation to schema slots, populate defaults, assign `epistemic_state = "inferred"`, link to warrant.
- **Verification**: `pytest tests/reva/unit/schemas/test_assimilation.py`
- **Done-When**:
  - `T-NS-003.D01`: Path A assimilation completes in $\le 50\text{ ms}$ on single CPU core.
  - `T-NS-003.D02`: Missing slot values are correctly populated with declared default inference rules.

#### Task `T-NS-004`: Slow-Path Novelty Detection & REVA Gap Routing
- **File**: `packages/eoip/neural/schemas/novelty.py`
- **Requirements**: `NS-CORE-002`
- **Actions**:
  1. Implement Path B: For inputs with similarity $< 0.85$, compute novelty magnitude $\Delta N = 1.0 - S$.
  2. Automatically instantiate a Knowledge Gap using REVA's `gap_id` formula.
  3. Persist gap record in `RevaStore` under `reva_gaps` with status `open` and domain `neural_schema`.
- **Verification**: `pytest tests/reva/unit/schemas/test_novelty_routing.py`
- **Done-When**:
  - `T-NS-004.D01`: Novelty input triggers `reva_gaps` row creation with exact `gap1_...` ID.
  - `T-NS-004.D02`: Emits event `reva.schema.novelty_detected` on internal outbox.

---

### Phase NS-P2: Clone-Structured Cognitive Graphs (CSCG) & DeepMind Relational Schemas

#### Task `T-NS-005`: CSCG Clone State Allocator & EM Learner
- **File**: `packages/eoip/neural/schemas/cscg.py`
- **Requirements**: `NS-CORE-003`
- **Actions**:
  1. Implement `CloneGraph` class managing entity clone states $\{u^{(1)}, \dots, u^{(K)}\}$.
  2. Implement Baum-Welch / EM transition estimation over observed trace sequences.
  3. Implement maximum-likelihood clone state resolution given historical sequence context.
- **Verification**: `pytest tests/reva/unit/schemas/test_cscg.py`
- **Done-When**:
  - `T-NS-005.D01`: Polysemous service entity observed in both gateway and worker roles is allocated 2 distinct clone nodes.
  - `T-NS-005.D02`: Contextual resolution achieves $\ge 95\%$ accuracy on synthetic multi-context traces.

#### Task `T-NS-006`: DeepMind Relational Schema Rebinding Engine
- **File**: `packages/eoip/neural/schemas/rebinding.py`
- **Requirements**: `NS-CORE-003`
- **Actions**:
  1. Implement relational template rebinding: given an abstract schema template $G_S = (V_S, E_S)$ and a target set of concrete entities $V_T$, compute optimal isomorphism mapping $\phi: V_S \to V_T$.
  2. Support zero-shot transfer: instant transfer of learned failure detection patterns to an unobserved microservice graph.
- **Verification**: `pytest tests/reva/unit/schemas/test_rebinding.py`
- **Done-When**:
  - `T-NS-006.D01`: Rebinding maps 10-node schema template to target enterprise topology in $< 15\text{ ms}$.
  - `T-NS-006.D02`: Transfer achieves identical downstream invariant verification without retraining.

---

### Phase NS-P3: LLM Memory Consolidation & AutoSchemaKG

#### Task `T-NS-007`: AutoSchemaKG Extraction & Clustering Pipeline
- **File**: `packages/eoip/neural/schemas/auto_schema.py`
- **Requirements**: `NS-KG-001`
- **Actions**:
  1. Implement sliding-window entity-relation co-occurrence mining across textual corpora and API logs.
  2. Cluster relation embeddings via HDBSCAN / Agglomerative Clustering to induce candidate relation schemas.
  3. Synthesize candidate `NeuralSchema` objects with slot cardinality bounds.
- **Verification**: `pytest tests/reva/unit/schemas/test_auto_schema.py`
- **Done-When**:
  - `T-NS-007.D01`: Automated extraction over 100 sample logs produces $\ge 5$ coherent candidate schemas.
  - `T-NS-007.D02`: Zero duplicate candidate schemas generated (deduplicated by JCS hash).

#### Task `T-NS-008`: SHACL Shape Compilation & Validation Gate
- **File**: `packages/eoip/neural/schemas/shacl_compiler.py`
- **Requirements**: `NS-KG-001`
- **Actions**:
  1. Implement compiler translating `NeuralSchema` slot constraints to W3C SHACL Core NodeShapes and PropertyShapes.
  2. Invoke `eoip.ontology.shacl_validator` against GL3 metamodel.
  3. If shape validation fails, quarantine candidate with error report.
- **Verification**: `pytest tests/reva/unit/schemas/test_shacl_compiler.py`
- **Done-When**:
  - `T-NS-008.D01`: Generated SHACL Turtle string validates cleanly with pySHACL / internal validator.
  - `T-NS-008.D02`: Malformed slot constraint triggers `SHACL_VALIDATION_ERROR` and blocks schema promotion.

#### Task `T-NS-009`: Agent Working Memory Frame Consolidation
- **File**: `packages/eoip/brain/schemas/memory_consolidation.py`
- **Requirements**: `NS-AGENT-001`
- **Actions**:
  1. Implement `WorkingMemoryConsolidator` converting episodic execution steps into consolidated semantic schemas.
  2. Compress raw conversational buffers into typed `WorkingMemoryFrame` representations.
- **Verification**: `pytest tests/reva/unit/schemas/test_memory_consolidation.py`
- **Done-When**:
  - `T-NS-009.D01`: Token size of agent state drops by $\ge 50\%$ upon consolidation.
  - `T-NS-009.D02`: Memory recall accuracy on goal-critical entities remains $100\%$.

#### Task `T-NS-009B`: Codebase Schema Induction & Safe Python Slot-Filling
- **File**: `packages/eoip/neural/schemas/code_induction.py`
- **Requirements**: `NS-KG-003`, `REVA-AB-014`, `REVA-SEC-013`
- **Actions**:
  1. Receive repository boundary graphs from REVA extraction pipeline.
  2. Implement graph pattern mining to extract recurrent architectural patterns (e.g., Spring controllers, FastAPI routers, microservice topologies).
  3. Compile detected topologies into typed `NeuralSchema` definitions and validate with SHACL compiler (`T-NS-008`).
  4. Ensure zero external LLM egress: All code AST traversal, pattern mining, and shape induction executed in pure Python; vector embeddings generated using local sentence-transformers.
- **Verification**: `pytest tests/reva/unit/schemas/test_code_induction.py`
- **Done-When**:
  - `T-NS-009B.D01`: Induces architectural schema definitions from ingested repository fixtures.
  - `T-NS-009B.D02`: Byte-scan verifies zero proprietary source code transmitted to external LLMs.

---

### Phase NS-P4: Attention Schema Theory (AST) Engine & Metacognitive Steering

#### Task `T-NS-010`: Real-Time Attention Schema Tracker
- **File**: `packages/eoip/neural/schemas/attention.py`
- **Requirements**: `NS-AGENT-002`
- **Actions**:
  1. Implement `AgentAttentionSchema` model and real-time state tracker.
  2. Record primary focus target, peripheral focus set, duration, and entropy over sliding window.
  3. Implement Shannon entropy calculation over attention weights.
- **Verification**: `pytest tests/reva/unit/schemas/test_attention.py`
- **Done-When**:
  - `T-NS-010.D01`: Attention state updates dynamically per tool execution step.
  - `T-NS-010.D02`: Entropy correctly scales from $0.0$ (hyper-focused) to $1.0$ (uniform dispersion).

#### Task `T-NS-011`: Attentional Thrashing Detection & Metacognitive Interrupt
- **File**: `packages/eoip/neural/schemas/thrashing.py`
- **Requirements**: `NS-AGENT-002`
- **Actions**:
  1. Implement cycle detection over attention target history: if the same entity or tool cycle repeats $\ge 3$ times with zero state progress, raise `ThrashingDetectedAlert`.
  2. Implement top-down steering interrupt: clears local focus buffer, injects alternative peripheral exploration candidates into agent context.
- **Verification**: `pytest tests/reva/unit/schemas/test_thrashing.py`
- **Done-When**:
  - `T-NS-011.D01`: Synthetic infinite loop agent is interrupted within $\le 3$ iterations.
  - `T-NS-011.D02`: Emits Prometheus metric `reva_agent_attention_thrash_events_total`.

#### Task `T-NS-012`: A2A Theory of Mind Attention Protocol
- **File**: `packages/eoip/neural/schemas/a2a_attention.py`
- **Requirements**: `NS-AGENT-003`
- **Actions**:
  1. Extend `A2AProtocolBroker` in `packages/eoip/agents/archetypes.py` to serialize and parse `AgentAttentionSchema`.
  2. Implement collaborative conflict detection: if Agent A and Agent B target the same entity for mutation, yield to higher-authority agent.
- **Verification**: `pytest tests/reva/unit/schemas/test_a2a_attention.py`
- **Done-When**:
  - `T-NS-012.D01`: Multi-agent collaborative benchmark shows zero concurrent mutation collision on shared vertices.

---

### Phase NS-P5: Graph Planes Integration (GL0, GL1, GL2, GL3, GW)

#### Task `T-NS-013`: GL0 Epistemic Slot Storage & Query Projection
- **File**: `packages/eoip/graph/schemas_projection.py`
- **Requirements**: `NS-KG-002`
- **Actions**:
  1. Extend vertex and edge property serializer in `packages/eoip/graph/` to store inferred slot provenance blocks.
  2. Implement query filtering in graph store: `epistemic="observed"` filters out inferred slots.
- **Verification**: `pytest tests/reva/unit/schemas/test_graph_projection.py`
- **Done-When**:
  - `T-NS-013.D01`: Query with `epistemic="observed"` strictly ignores schema-inferred fields.
  - `T-NS-013.D02`: Inferred fields retain cryptographic link to producing warrant ID.

#### Task `T-NS-014`: Wisdom Graph Decision Schema Indexer
- **File**: `packages/eoip/neural/schemas/wisdom_schemas.py`
- **Requirements**: `NS-WG-001`
- **Actions**:
  1. Implement `DecisionSchema` extractor indexing situation fingerprints, chosen choices, and bitemporal outcomes.
  2. Implement fast situation archetype clustering using CSCG clone state similarity.
- **Verification**: `pytest tests/reva/unit/schemas/test_wisdom_schemas.py`
- **Done-When**:
  - `T-NS-014.D01`: Decision trace is indexed into a valid decision schema in $\le 20\text{ ms}$.
  - `T-NS-014.D02`: Precedent retrieval surfaces top-3 archetypes with precision@3 $\ge 0.85$.

---

### Phase NS-P6: Empirical Baseline Gating & Final REVA Ledger Verification

#### Task `T-NS-015`: Automated 100-Query Empirical Baseline Benchmark
- **File**: `scripts/reva/eval_schema_baseline.py`
- **Requirements**: `NS-CORE-004`
- **Actions**:
  1. Implement automated test harness executing 100 reference enterprise queries across both Condition A (No-Schema) and Condition B (Neural Schema).
  2. Compute F1 accuracy, token consumption, and latency.
  3. Calculate paired Wilcoxon signed-rank test p-value.
  4. Block schema promotion if $p \ge 0.01$ or token improvement $< 15\%$.
- **Verification**: `python scripts/reva/eval_schema_baseline.py --all`
- **Done-When**:
  - `T-NS-015.D01`: Benchmark outputs structured JSON report with empirical delta and statistical significance.
  - `T-NS-015.D02`: All promoted schemas have $p < 0.01$ documented in report.

#### Task `T-NS-016`: REST API & MCP Tools Integration
- **File**: `reva/api/routes_schemas.py`, `reva/mcp/server.py`
- **Requirements**: §7.1, §7.2
- **Actions**:
  1. Implement FastAPI routes for schema submission, retrieval, benchmarking, promotion, and assimilation.
  2. Expose FastMCP tools: `reva_schema_match`, `reva_schema_assimilate`, `reva_agent_attention_get`, `reva_agent_attention_steer`.
- **Verification**: `pytest tests/reva/unit/schemas/test_schema_api.py`
- **Done-When**:
  - `T-NS-016.D01`: All REST endpoints return 200 OK with validated response schemas.
  - `T-NS-016.D02`: FastMCP server advertises all 4 tools and handles invocations cleanly.

#### Task `T-NS-017`: REVA Proof-of-Done Obligation Suite & Canonical Signed Ledger
- **File**: `docs/reva/obligations/neural_schemas.yaml`, `scripts/reva/build_schema_ledger.py`
- **Requirements**: `NS-REVA-001`, `NS-REVA-002`
- **Actions**:
  1. Define 17 formal obligations (`OBL-NS-001` through `OBL-NS-017`) covering all tasks.
  2. Implement Check 12 (`12_schema_conformance`) in `reva.pd.closure`.
  3. Execute full verifier run, evaluate closure decisions, build signed canonical ledger `docs/reva/neural-schema-ledger.json`.
- **Verification**: `python scripts/reva/build_schema_ledger.py`
- **Done-When**:
  - `T-NS-017.D01`: All 17 obligations evaluated to `outcome="closed"` with 0 failure reasons.
  - `T-NS-017.D02`: Emits signed canonical ledger `docs/reva/neural-schema-ledger.json` matching `^ldg1_[0-9a-f]{64}$`.

---

## 3. Seven-Level Verification Hierarchy

Every Neural Schema deliverable is subject to the standard Seven-Level Verification protocol:

```
+----------------------------------------------------------------------------------------------------+
|  Level 1: Syntactic & Type Correctness                                                             |
|  - Pydantic v2 strict validation, mypy zero-error pass, RFC 8785 canonical JSON compliance        |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 2: Unit Contract Execution                                                                  |
|  - Deterministic unit tests with @pytest.mark.reva_depth("unit"), 100% pass                         |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 3: Determinism & Performance Budgets                                                        |
|  - Path A assimilation <= 50ms, rebinding <= 15ms, zero float non-determinism                      |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 4: Anti-Gaming & Epistemic Verification                                                     |
|  - 0 occurrences of inferred marked as observed; AST scan clean; thrashing broken in <= 3 cycles  |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 5: Empirical Baseline Gating                                                                |
|  - Statistically significant lift over no-schema baseline (Wilcoxon p < 0.01) on 100 queries        |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 6: REVA Proof-of-Done & Closure                                                             |
|  - 11-step + Check 12 closure evaluation clean, signed DSSE attestation, signed ledger (ldg1_...) |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|  Level 7: System & Multi-Agent Swarm Integration                                                   |
|  - Clean integration with A2AProtocolBroker, GL0-GL3 graph stores, and Wisdom Graph counsel       |
+----------------------------------------------------------------------------------------------------+
```

---

## 4. Final Exit Gate Checklist

Before Phase NS-P6 can be signed off:
- [ ] `forbid_placeholders.py` passes with 0 violations across all schema modules.
- [ ] `check_depth_markers.py` passes across all `tests/reva/unit/schemas/`.
- [ ] `verify_epistemic_labels.py` passes with 0 violations.
- [ ] 100-query empirical benchmark confirms $p < 0.01$ lift over baseline.
- [ ] Canonical signed ledger `docs/reva/neural-schema-ledger.json` emitted with status `complete=True`.
