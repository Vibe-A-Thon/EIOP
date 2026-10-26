# EPIC-NEURALSCHEMAAG-UNTR: neural-schema-agg-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 13 tasks, ~96.5 h, priorities {'P1': 13}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-NS-AGENT-001 [P1] NS-AGENT-001: Schema-Structured Agent Working Memory

- **Source:** `neural-schema-agg-requirements.md:187-200` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-NS-AGENT-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-AGENT-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-AGENT-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-AGENT-001

**Acceptance criteria**
- [ ] Autonomous agents MUST represent their transient operational context as instantiated schema slots rather than unstructured text buffers.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-AGENT-002 [P1] NS-AGENT-002: Attention Schema Theory (AST) Engine for Agents

- **Source:** `neural-schema-agg-requirements.md:201-227` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-NS-AGENT-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-AGENT-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-AGENT-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-AGENT-002

**Acceptance criteria**
- [ ] Every autonomous agent in the system MUST maintain an explicit, real-time descriptive Attention Schema representing its own attentional focus.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-AGENT-003 [P1] NS-AGENT-003: Agent-to-Agent (A2A) Attention & Theory of Mind Sharing

- **Source:** `neural-schema-agg-requirements.md:228-239` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-NS-AGENT-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-AGENT-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-AGENT-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-AGENT-003

**Acceptance criteria**
- [ ] Swarms of agents communicating over A2AProtocolBroker MUST exchange attention summaries to coordinate task execution.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-CORE-001 [P1] NS-CORE-001: Unified Neural Schema Representation Specification

- **Source:** `neural-schema-agg-requirements.md:103-137` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-NS-CORE-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-CORE-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-CORE-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-CORE-001

**Acceptance criteria**
- [ ] The platform MUST define and enforce a strict, typed schema data model representing both graph templates and cognitive memory frames.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-CORE-002 [P1] NS-CORE-002: Dual-Pathway Assimilation Engine (Tse-Morris Pathway)

- **Source:** `neural-schema-agg-requirements.md:138-158` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-NS-CORE-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-CORE-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-CORE-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-CORE-002

**Acceptance criteria**
- [ ] The system MUST implement a dual-pathway intake for all new observations, evaluating schema consistency before choosing between fast-path slot filling and slow-path accommodation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-CORE-003 [P1] NS-CORE-003: Clone-Structured Cognitive Graph (CSCG) Engine

- **Source:** `neural-schema-agg-requirements.md:159-169` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-NS-CORE-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-CORE-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-CORE-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-CORE-003

**Acceptance criteria**
- [ ] The graph runtime MUST implement CSCG decomposition to resolve polysemy and context-dependent behavior across enterprise entities.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-CORE-004 [P1] NS-CORE-004: Baseline Gating & Verification Oracle

- **Source:** `neural-schema-agg-requirements.md:170-184` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-NS-CORE-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-CORE-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-CORE-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-CORE-004

**Acceptance criteria**
- [ ] The runtime MUST execute automated baseline comparison for every proposed schema before promotion to active.
- [ ] Description: The runtime MUST execute automated baseline comparison for every proposed schema before promotion to active
- [ ] Maintain a standard test set of $\ge 100$ gold-standard queries for the target domain
- [ ] Condition A: Deterministic baseline (unassisted multi-hop graph search / raw BM25 + dense retrieval)
- [ ] Condition B: Schema-assisted routing (Path A assimilation + clone traversal)
- [ ] Measure Target Metric: F1-Score on downstream task, Token Consumption, and Execution Latency
- [ ] Promotion Rule: Condition B must achieve statistically significant superiority ($p < 0.01$, Wilcoxon test) and $\ge 15\%$ token reduction. Otherwise status remains candidate or shadow
- [ ] NS-CORE-004.D01: Automated benchmark harness outputs empirical delta and p-value
- [ ] NS-CORE-004.D02: Schemas failing the threshold are blocked from active status and logged in docs/reva/gaps.json
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-KG-001 [P1] NS-KG-001: AutoSchemaKG Induction Engine

- **Source:** `neural-schema-agg-requirements.md:242-253` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-NS-KG-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-KG-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-KG-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-KG-001

**Acceptance criteria**
- [ ] The background knowledge ingestion pipeline MUST support automated induction of emergent schema candidates from heterogeneous unstructured and semi-structured streams.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-KG-002 [P1] NS-KG-002: Epistemic Schema Slot Projection in GL0

- **Source:** `neural-schema-agg-requirements.md:254-274` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-NS-KG-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-KG-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-KG-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-KG-002

**Acceptance criteria**
- [ ] When an instance vertex is populated via schema defaults, the property must be stored with provenance metadata indicating its inferred status.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-KG-003 [P1] NS-KG-003: Codebase Schema Induction from Ingested Repositories & Zero-Leak Fencing

- **Source:** `neural-schema-agg-requirements.md:275-288` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-NS-KG-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-KG-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-KG-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-KG-003

**Acceptance criteria**
- [ ] When a code repository (GitHub, GitLab, Bitbucket, Git URL) is ingested via REVA, the Neural Schema induction engine MUST extract structural and architectural schemas directly from code ASTs using pure-Python analysis, strictly enforcing zero data leakage to external LLMs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-REVA-001 [P1] NS-REVA-001: Cryptographic Schema Registry & Translog Notarization

- **Source:** `neural-schema-agg-requirements.md:307-318` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-NS-REVA-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-REVA-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-REVA-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-REVA-001

**Acceptance criteria**
- [ ] All active neural schemas MUST be immutably notarized in REVA's Merkle transparency log.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-REVA-002 [P1] NS-REVA-002: Schema-Aware Proof-of-Done Evaluator

- **Source:** `neural-schema-agg-requirements.md:319-332` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-NS-REVA-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-REVA-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-REVA-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-REVA-002

**Acceptance criteria**
- [ ] REVA's closure engine (reva.pd.closure) MUST include dedicated checks verifying that code and data artifacts comply with declared neural schemas.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NS-WG-001 [P1] NS-WG-001: Wisdom Graph Decision Schema & Situation Archetypes

- **Source:** `neural-schema-agg-requirements.md:289-304` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-NS-WG-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NS-WG-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NS-WG-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-NS-WG-001

**Acceptance criteria**
- [ ] The Wisdom Graph MUST structure decision traces and precedents into standardized DecisionSchema frames.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

