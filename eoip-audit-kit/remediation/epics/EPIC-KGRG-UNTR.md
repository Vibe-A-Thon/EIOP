# EPIC-KGRG-UNTR: EOIP-engg-doc-pkg/KGR-g-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 13 tasks, ~86.5 h, priorities {'P0': 13}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-KGR-G-005 [P0] KGR-G-005: Universal Zero-ETL Virtual Relational Graph Adapter

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:250-258` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-005: Universal Zero-ETL Virtual Relational Graph Adapter
- **Classification:** Functional Requirement | **Priority:** P0 (Core)
- **Description:** The system SHALL extend the Universal Transpiler to provide live virtual views over relational databases (PostgreSQL, SQLite, MySQL) using declarative mapping configurations, translating openCypher `MATCH (u:User)-[:OWNS]->(a:Account)` into single-pass SQL `JOIN` queries.
- **Verification Criteria:**
  - Virtual queries execute without pre-ingesting relational rows into graph storage.
  - Query latency overhead compared to raw SQL is < 15ms at P95.
  - Returns graph-shaped node/edge dictionaries conforming to `GraphStore` contracts.
- **Target Implementation:** `packages/eoip/query/virtual_graph.py` & `moonshot/universal_transpiler.py`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-005

**Acceptance criteria**
- [ ] The system SHALL extend the Universal Transpiler to provide live virtual views over relational databases (PostgreSQL, SQLite, MySQL) using declarative mapping configurations, translating openCypher MATCH (u:User)-[:OWNS]->(a:Account) into single-pass SQL JOIN queries.
- [ ] Virtual queries execute without pre-ingesting relational rows into graph storage
- [ ] Query latency overhead compared to raw SQL is < 15ms at P95
- [ ] Returns graph-shaped node/edge dictionaries conforming to GraphStore contracts
- [ ] Target Implementation: packages/eoip/query/virtualgraph.py & moonshot/universaltranspiler.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-006 [P0] KGR-G-006: 2D Bitemporal CRDT Branch Engine & Merkle Audit Trail

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:259-267` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-006: 2D Bitemporal CRDT Branch Engine & Merkle Audit Trail
- **Classification:** Functional Requirement | **Priority:** P0 (Core)
- **Description:** The system SHALL maintain complete bitemporal indexing (`valid_time` denoting real-world validity and `transaction_time` denoting system recording time) with Git-like branching (`main`, `feature/*`, `release/*`), 3-way CRDT merge resolution, and cryptographic Merkle root verification.
- **Verification Criteria:**
  - Point-in-time time-travel queries retrieve the exact graph state at any `(VT, TT)` coordinates.
  - CRDT merge reconciles non-conflicting concurrent branch edits without data loss.
  - Merkle root hash recalculates on every mutation, enabling tamper detection.
- **Target Implementation:** `packages/eoip/moonshot/bitemporal_state_machine.py`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-006

**Acceptance criteria**
- [ ] The system SHALL maintain complete bitemporal indexing (valid_time denoting real-world validity and transaction_time denoting system recording time) with Git-like branching (main, feature/, release/), 3-way CRDT merge resolution, and cryptographic Merkle root verification.
- [ ] Point-in-time time-travel queries retrieve the exact graph state at any (VT, TT) coordinates
- [ ] CRDT merge reconciles non-conflicting concurrent branch edits without data loss
- [ ] Merkle root hash recalculates on every mutation, enabling tamper detection
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-007 [P0] KGR-G-007: Autonomous Self-Healing Active Fabric & Governance Approvals

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:268-276` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 7.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-007: Autonomous Self-Healing Active Fabric & Governance Approvals
- **Classification:** Functional / Governance | **Priority:** P0 (Core)
- **Description:** The system SHALL monitor architecture drift between declared ontology contracts and live runtime telemetry/code, automatically synthesizing Git PR diffs and Terraform HCL remediation blocks, guarded by configurable risk levels (R0=Auto, R1=Peer, R2=Lead, R3=CAB, R4=Executive).
- **Verification Criteria:**
  - Detected drift generates syntactically valid unified diffs and Terraform blocks.
  - Any mutation with Risk Level ≥ R2 is strictly blocked until an authorized signature token is supplied.
  - Full audit records are emitted with actor identity, timestamp, and before/after diffs.
- **Target Implementation:** `packages/eoip/moonshot/self_healing.py`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-007

**Acceptance criteria**
- [ ] The system SHALL monitor architecture drift between declared ontology contracts and live runtime telemetry/code, automatically synthesizing Git PR diffs and Terraform HCL remediation blocks, guarded by configurable risk levels (R0=Auto, R1=Peer, R2=Lead, R3=CAB, R4=Executive).
- [ ] Detected drift generates syntactically valid unified diffs and Terraform blocks
- [ ] Any mutation with Risk Level ≥ R2 is strictly blocked until an authorized signature token is supplied
- [ ] Full audit records are emitted with actor identity, timestamp, and before/after diffs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-KGR-G-008 [P0] KGR-G-008: Zero-Trust Confidential Graph & Egress DLP Gateway

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:277-285` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 7.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-008: Zero-Trust Confidential Graph & Egress DLP Gateway
- **Classification:** Security / Privacy | **Priority:** P0 (Core)
- **Description:** The system SHALL support additive homomorphic encryption for numeric entity properties, HMAC-SHA256 blind indexing tokens for encrypted property searching, Zero-Knowledge evidence verification, and an inline egress gateway enforcing token, byte, and dollar cost budgets.
- **Verification Criteria:**
  - Homomorphic addition operates directly on ciphertext without revealing plaintexts.
  - Blind index lookup finds matching nodes with zero false negatives while protecting plaintext strings.
  - Egress gateway blocks outbound payloads exceeding tenant quota or triggering DLP regex rules (e.g. credit card numbers, private API keys).
- **Target Implementation:** `packages/eoip/moonshot/confidential_graph.py` & `egress/gateway.py`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-008

**Acceptance criteria**
- [ ] The system SHALL support additive homomorphic encryption for numeric entity properties, HMAC-SHA256 blind indexing tokens for encrypted property searching, Zero-Knowledge evidence verification, and an inline egress gateway enforcing token, byte, and dollar cost budgets.
- [ ] Homomorphic addition operates directly on ciphertext without revealing plaintexts
- [ ] Blind index lookup finds matching nodes with zero false negatives while protecting plaintext strings
- [ ] Egress gateway blocks outbound payloads exceeding tenant quota or triggering DLP regex rules (e.g. credit card numbers, private API keys)
- [ ] Target Implementation: packages/eoip/moonshot/confidentialgraph.py & egress/gateway.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-KGR-G-009 [P0] KGR-G-009: Neuro-Symbolic Agent Memory (AGAM) & IDE MCP Server

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:286-294` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-009: Neuro-Symbolic Agent Memory (AGAM) & IDE MCP Server
- **Classification:** AI / Agentic | **Priority:** P0 (Core)
- **Description:** The system SHALL provide an Adaptive Graph Attention Memory (AGAM) module for autonomous coding agents, featuring exponential salience decay, dynamic importance re-ranking, and symbolic SHACL constraint validation, accessible to AI IDEs (Claude Code, Cursor, VS Code) via high-performance MCP protocol.
- **Verification Criteria:**
  - Salience scores decay smoothly over query cycles (`score = base * (0.95 ^ delta)`).
  - Agent memory insertions violating ontology shapes are rejected with structured SHACL diagnostic errors.
  - MCP endpoints respond in < 25ms for entity lookup, blast radius queries, and symbol resolution.
- **Target Implementation:** `packages/eoip/moonshot/neuro_symbolic_memory.py` & `agents/mcp_server.py`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-009

**Acceptance criteria**
- [ ] The system SHALL provide an Adaptive Graph Attention Memory (AGAM) module for autonomous coding agents, featuring exponential salience decay, dynamic importance re-ranking, and symbolic SHACL constraint validation, accessible to AI IDEs (Claude Code, Cursor, VS Code) via high-performance MCP protocol.
- [ ] Salience scores decay smoothly over query cycles (score = base (0.95 ^ delta))
- [ ] Agent memory insertions violating ontology shapes are rejected with structured SHACL diagnostic errors
- [ ] MCP endpoints respond in < 25ms for entity lookup, blast radius queries, and symbol resolution
- [ ] Target Implementation: packages/eoip/moonshot/neurosymbolicmemory.py & agents/mcpserver.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-010 [P0] KGR-G-010: Continuous Compliance Twin & AI-BOM Synthesizer

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:295-305` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-010: Continuous Compliance Twin & AI-BOM Synthesizer
- **Classification:** Governance & Compliance | **Priority:** P0 (Core)
- **Description:** The system SHALL synthesize real-time Software/AI Bill of Materials (AI-BOM / SBOM) in CycloneDX and SPDX formats, continuously mapping datasets, models, code artifacts, and pipelines against regulatory frameworks (EU AI Act, SOC 2 Type II, ISO 42001) with cryptographic verification seals.
- **Verification Criteria:**
  - Generates compliant CycloneDX JSON and SPDX 3.0 documents on demand.
  - Automatically flags uncertified models, untracked training datasets, or non-compliant licenses.
  - Cryptographic seal verifies data immutability using SHA-256 hash chains.
- **Target Implementation:** `packages/eoip/moonshot/compliance_twin.py`

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-010

**Acceptance criteria**
- [ ] The system SHALL synthesize real-time Software/AI Bill of Materials (AI-BOM / SBOM) in CycloneDX and SPDX formats, continuously mapping datasets, models, code artifacts, and pipelines against regulatory frameworks (EU AI Act, SOC 2 Type II, ISO 42001) with cryptographic verification seals.
- [ ] Generates compliant CycloneDX JSON and SPDX 3.0 documents on demand
- [ ] Automatically flags uncertified models, untracked training datasets, or non-compliant licenses
- [ ] Cryptographic seal verifies data immutability using SHA-256 hash chains
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-021 [P0] KGR-G-021: Enterprise Control Loops Governance Engine

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:868-872` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-021; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### KGR-G-021: Enterprise Control Loops Governance Engine
- **Classification:** Governance / Safety | **Priority:** P0 (Core)
- **Description:** Enforces 14 standard loops, 15 human governance patterns, and 23 autonomous execution loops with strict risk gating and execution limits.
- **Verification:** Passing in `tests/unit/test_brain_and_living_system.py`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-021' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-021') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-021

**Acceptance criteria**
- [ ] Enforces 14 standard loops, 15 human governance patterns, and 23 autonomous execution loops with strict risk gating and execution limits.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-022 [P0] KGR-G-022: Multi-Archetype Agent Factory & A2A Protocol (76+ Archetypes & Swarms)

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:873-877` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-022; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### KGR-G-022: Multi-Archetype Agent Factory & A2A Protocol (76+ Archetypes & Swarms)
- **Classification:** AI / Agentic | **Priority:** P0 (Core)
- **Description:** Instantiates all 76+ specialized agent archetypes and multi-agent swarm orchestrators, with A2A protocol messaging and capability negotiation.
- **Verification:** Passing in `tests/unit/test_brain_and_living_system.py`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-022' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-022') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-022

**Acceptance criteria**
- [ ] Instantiates all 76+ specialized agent archetypes and multi-agent swarm orchestrators, with A2A protocol messaging and capability negotiation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-023 [P0] KGR-G-023: 45+ Modality Unified Enterprise RAG Suite

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:878-882` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-023; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### KGR-G-023: 45+ Modality Unified Enterprise RAG Suite
- **Classification:** Retrieval / AI | **Priority:** P0 (Core)
- **Description:** Supports Graph, Tree, Temporal, Code, Lineage, and Corrective RAG modalities with deterministic fallbacks.
- **Verification:** Passing in `tests/unit/test_brain_and_living_system.py`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-023' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-023') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-023

**Acceptance criteria**
- [ ] Supports Graph, Tree, Temporal, Code, Lineage, and Corrective RAG modalities with deterministic fallbacks.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-024 [P0] KGR-G-024: Polyglot Query Transpiler & NL2 Router

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:883-887` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-024; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### KGR-G-024: Polyglot Query Transpiler & NL2* Router
- **Classification:** Query Engine | **Priority:** P0 (Core)
- **Description:** Transpiles across 40+ dialects including SPARQL, Cypher, GQL, PromQL, LogQL, and the dedicated NL2* family.
- **Verification:** Passing in `tests/unit/test_brain_and_living_system.py`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-024' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-024') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-024

**Acceptance criteria**
- [ ] Transpiles across 40+ dialects including SPARQL, Cypher, GQL, PromQL, LogQL, and the dedicated NL2* family.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-025 [P0] KGR-G-025: Universal 55-Database Registry & Adapter SPI

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:888-892` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-025; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### KGR-G-025: Universal 55-Database Registry & Adapter SPI
- **Classification:** Storage / Database | **Priority:** P0 (Core)
- **Description:** Provides connection management, health checks, and dialect transpilation across 55 enterprise databases.
- **Verification:** Passing in `tests/unit/test_brain_and_living_system.py`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-025' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-025') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-025

**Acceptance criteria**
- [ ] Provides connection management, health checks, and dialect transpilation across 55 enterprise databases.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-026 [P0] KGR-G-026: Dynamic Living Brain Ontology Induction & Consolidation

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:893-897` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-026; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### KGR-G-026: Dynamic Living Brain Ontology Induction & Consolidation
- **Classification:** Cognitive / Brain | **Priority:** P0 (Core)
- **Description:** Continuous unsupervised ontology induction and Merkle root state snapshot computation.
- **Verification:** Passing in `tests/unit/test_brain_and_living_system.py`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-026' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-026') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-026

**Acceptance criteria**
- [ ] Continuous unsupervised ontology induction and Merkle root state snapshot computation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-027 [P0] KGR-G-027: Brain OS Kernel Dual-Route Answering Engine

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:898-904` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-027; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### KGR-G-027: Brain OS Kernel Dual-Route Answering Engine
- **Classification:** Operating System / Core | **Priority:** P0 (Core)
- **Description:** High-performance kernel routing deterministic structured queries and hybrid LLM-augmented questions through governance loops.
- **Verification:** Passing in `tests/unit/test_brain_and_living_system.py`.

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'KGR-G-027' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('KGR-G-027') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-KGR-G-027

**Acceptance criteria**
- [ ] High-performance kernel routing deterministic structured queries and hybrid LLM-augmented questions through governance loops.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

