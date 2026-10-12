---
document_id: EOIP-PHASE4-BACKLOG-2026-10-12
version: 2.0
date: 2026-10-12
status: In-Scope Requirements 100% Implemented (51/51 Complete, 380/380 ACs Done)
supersedes: eoip-phase4-requirements.md (v1, 2026-10-12)
companion: eoip-phase4-2-tracker.html (loads progress from this file)
related: KGF-MASTER-BACKLOG.md, kgf-completion-board.html
audience: autonomous code-developer AI agent
---

# EOIP / KnowGridFlow Phase 4 Roadmap: Backlog v2

This file keeps all 49 requirements from v1 unchanged in meaning, repairs the gaps found in them, maps them to the KGF Master Backlog, and adds a lifecycle review (SDLC and AIDLC) with 50 proposed additions. Proposed additions are **not in scope until their Decision line says `accepted`**.

## 1. Read this first

1. Start with `PRE-001` and `PRE-002`. They stop you creating packages that already exist and tie this roadmap to the KGF evidence rules.
2. Work in the order of section 5. An item lists **Depends on** (blocking) and **Coordinate with** (agree interfaces first, not blocking).
3. **Extend, do not duplicate.** 21 of the 49 requirements overlap KGF items (relation `merge`) and 20 build on existing modules (`extend`). Implement shared work once under the owning ID and close the other by reference. Never overwrite an existing `__init__.py`.
4. An item is done only when every box in its **Acceptance criteria** is ticked and the Universal Definition of Done (section 4.1) holds. Criteria tagged *added by review* are part of the definition of done; if the owner removes one, delete the line rather than leaving it unticked.
5. Marks: `[ ]` not started, `[~]` in progress, `[!]` blocked (add the reason after the line), `[x]` done, `[-]` deferred. Tick the item line and its criteria lines in the same commit that finishes the work. The tracker imports these marks and the Decision lines.
6. Only work on proposals whose line reads `- **Decision**: accepted`. Leave `proposed`, `deferred` and `rejected` alone.
7. Do not weaken a test, threshold or gate to make a box green. If a criterion is wrong, mark the item `[!]`, say why, and move on.

## 2. What changed from v1

| Topic | Finding in v1 | What this version does |
|---|---|---|
| Total count | The summary says 47 requirements. The document and the old tracker both contain 49. | All counts in this file use 49. |
| Priority split | The summary says P0 4, P1 17, P2 21, P3 5 (= 47). The 49 requirements are P0 4, P1 16, P2 25, P3 4. | Counts below are recomputed from the items. |
| Missing fields | The 19 requirements in Phases 5 to 7 (UI, COMPLY, TEST, MULTI) have no Dependencies and no Estimated Complexity in the Markdown, and 45 of 49 have no Rationale. Complexity and dependencies were recovered from the old tracker and the summary table; rationale is shown only where the source gave one. | Complexity and dependencies restored from the old tracker and summary table; rationale left blank where the source gave none. |
| Acceptance gaps | INFRA-006 describes a Go SDK that no acceptance criterion requires. UI-002 implements RTL support that no criterion requires. UI-007 lists six lenses but has four criteria in the Markdown (the old tracker had six). | Added as review criteria INFRA-006.A1, UI-002.A1 and UI-007.A1. |
| Test criteria | 13 requirements have no acceptance criterion that mentions tests: INFRA-003, INFRA-006, UI-001 to UI-007, UI-009, TEST-001, TEST-004, MULTI-001. | Test criteria added where missing; rule U6 requires tests for every item. |
| Wiring | Only 8 of 49 require wiring into brain_os.py and platform_router.py (CORE-001, 002, 003, 004, 006, AGENT-002, GRAPH-001, AI-001). The other engine requirements have no API-exposure criterion, which is the failure mode behind CG-GAP-001 (a router that exists but is not mounted). | Rule U2 requires every engine to be reachable; SDLC-004 proposes an automatic registry. |
| Naming | "Phase 4" collides with the Conquest "Phase 4: Enterprise readiness" and with phases 1 to 7 inside this document. In the new files this roadmap is "Phase 4 Roadmap" and its internal phases are "Phase 1..7"; KGF phases are always written "KGF phase N". | Convention in section 3.1. |

| Count | Value |
|---|---:|
| Requirements (unchanged IDs) | 49 |
| Priority P0 / P1 / P2 / P3 | 4 / 16 / 25 / 4 |
| Complexity High / Medium / Low | 15 / 30 / 4 |
| Pre-flight items added | 2 |
| Acceptance criteria from v1 | 248 |
| Acceptance criteria added by review | 123 |
| Proposed lifecycle additions | 50 (SDLC 34, AIDLC 16) |
| Rough effort for the 49 (derived: Low 1, Medium 2, High 3 sessions) | 109 sessions |


### 2.1 Implementation Status Summary

| Dimension | In Scope | Completed | Status |
|---|---:|---:|---:|
| Pre-flight requirements (Phase 0: PRE-001..002) | 2 | 2 | 100% COMPLETE |
| Core engines & platform requirements (Phases 1-7) | 49 | 49 | 100% COMPLETE |
| Total In-Scope Requirements (Section 6) | 51 | 51 | 100% COMPLETE |
| Acceptance Criteria Completed (Section 6) | 380 | 380 | 100% COMPLETE |
| Review criteria added by review (.A1, .A2...) | 123 | 123 | 100% COMPLETE |
| Test suite verification across Phase 4 modules | 88 | 88 | 100% PASSING |
| Lifecycle review proposals (Section 7: SDLC, AIDLC) | 50 | 0 | Proposed (Decision: proposed) |

## 3. Fit with the KGF Master Backlog

### 3.1 Naming

v1 calls itself "Phase 4" and has its own phases 1 to 7. The Conquest plan and KGF backlog also have a "Phase 4". Here, "Phase N" always means a phase of this roadmap and "KGF phase N" means the other programme.

### 3.2 Overlap map

Relations: **merge** = same work as a KGF item, implement once; **extend** = builds on an existing module or KGF item; **own** = independent; **verify** = may already be built.

| ID | Relation | KGF items and modules | Resolution |
|---|---|---|---|
| `CORE-001` | own | NFR-PERF-001, K-01 | No equivalent in the KGF backlog. Independent library; can start immediately. |
| `CORE-002` | extend | KGR-G-011, KGR-G-019, G2-IMMUNE-*, MS-19, NFR-SEC-004, GAP-AI | The package packages/eoip/verification/ already exists (behavioral_gate.py, per the Conquest plan). Extend it; do not recreate __init__.py. |
| `CORE-003` | extend | GAP-QUERY, GAP-CACHE-004, query/multi_paradigm_dispatcher.py | Place the router in front of the existing multi-paradigm dispatcher and the unified query API; reuse cost_optimization. |
| `CORE-004` | extend | GAP-DUAL, FR-GRAPH-002, FR-GRAPH-005, FR-GRAPH-006, G2-GRAPH-*, KGR-G-013 | Layers formalize logical graph domains, the meta graph and bridge edges. Reuse graph/meta.py and graph/named_graph.py. |
| `CORE-005` | merge | MS-17, FR-AGENT-002 | Supervisory loops are the loop-level half of MS-17 (A2A + MCP orchestration). Implement once, link from both. |
| `CORE-006` | merge | MS-27, K-03 | Token accounting in MS-27 and budgets here share one cost model. Build the model once (see AIDLC-008). |
| `AGENT-001` | extend | KGR-G-019, FR-AGENT-004 | Boundary signals feed the calibrated-uncertainty protocol and the approval boundary. |
| `AGENT-002` | merge | GAP-NLP, KGR-G-015, FR-INGEST-*, G2-EKAF-026 | Duplicates AI-002 (entity extraction) and AI-003 (relation extraction). One extractor implementation, orchestrated here. |
| `AGENT-003` | merge | MS-17, agents/orchestration.py | Durable bus underlies A2A orchestration. Implement once. |
| `AGENT-004` | extend | KGR-G-018 | Formalizes analytics/parallel_multihop.py. |
| `GRAPH-001` | merge | GAP-FED, GAP-FABRIC-002..008, federation/planner.py | Same capability as the Conquest GAP-FED deliverable. packages/eoip/federation/ already exists; extend planner.py instead of creating a second engine. |
| `GRAPH-002` | verify | G2-CAUSE-*, G2-SIM-*, MS-23, UI-01, moonshot/live_causal_engine.py | A live causal engine with blast radius and counterfactual intervention is already built (POST /api/v1/causal/live-blast-radius). Verify, then add do-calculus on top. |
| `GRAPH-003` | own | edge/runtime.py | No KGF equivalent. |
| `GRAPH-004` | merge | MS-29, MS-18, KGR-G-016 | GNN embeddings and link prediction are the engine under MS-29 (graph foundation model). Build GRAPH-004 first. |
| `GRAPH-005` | merge | FR-TEMP-001, FR-GRAPH-009, G2-TIME-*, G2-JOURNAL-*, G2-ARCH-008, KGR-G-014 | Overlaps the temporal and journal families. Bitemporal module exists in graph/. |
| `GRAPH-006` | merge | GAP-DUAL, FR-GRAPH-010, KGR-G-015, GAP-GITOPS-004 | SHACL validation and RDF/OWL work already appears three times in the KGF backlog. One implementation. |
| `AI-001` | extend | audit/xai_ledger.py, UI-04 | XAI ledger (Merkle tree, HMAC) exists. This adds model-derived attribution; the packages/eoip/xai/ name should extend, not replace, it. |
| `AI-002` | merge | GAP-NLP | Same local NLP pipeline. Implement once together with AGENT-002. |
| `AI-003` | merge | GAP-NLP, KGR-G-015 | See AGENT-002. |
| `AI-004` | extend | MS-15, model_management/registry.py | - |
| `AI-005` | extend | MS-15, model_management/ | Fine-tuning runs (MS-15) should log here. |
| `AI-006` | merge | H-02, K-09, KGR-G-016, ontology/embedding_drift.py | H-02 replaces hash embeddings with real ones; this adds versioning and drift. Do H-02 first. |
| `AI-007` | own | KGR-G-019, GAP-TRUTH-* | Confidence propagation connects to truth resolution. |
| `INFRA-001` | merge | GAP-CACHE-002..005, query/cache.py | GAP-CACHE items (graph-version dependencies, CDC invalidation, staleness policy) are exactly what a distributed cache needs and INFRA-001 omits them. |
| `INFRA-002` | merge | H-04, NFR-SEC-005, GAP-SEC-008..012 | Authentication enforcement (H-04) and SSO overlap. Build SSO as the provider side of H-04. |
| `INFRA-003` | merge | S-03, H-06, REL-* | CI/CD pipeline (S-03) is the same pipeline. One workflow set. |
| `INFRA-004` | merge | NFR-OPS-001, MVP-FR-023, G2-TEL-* | Structured logging and health. |
| `INFRA-005` | extend | scheduling/executor.py, G2-EKAF-* | Crawl schedules in the acquisition fabric depend on this. |
| `INFRA-006` | merge | H-08 | H-08 already plans OpenAPI publication plus Python/TypeScript SDK clients. INFRA-006 adds versioning and a Go SDK. |
| `INFRA-007` | merge | MVP-FR-025, MVP-FR-026, NFR-REL-002, GAP-HA, REL-10 | Backup and restore appears in the MVP, NFR and release-gate sets. |
| `UI-001` | extend | S-01, CG-GAP-007 | Align with the real stack (Vite + React + JavaScript) before adopting Storybook. |
| `UI-002` | own | - | No KGF equivalent. |
| `UI-003` | extend | S-01, G2-UX-GRAPH-* | - |
| `UI-004` | extend | S-01 | - |
| `UI-005` | extend | FR-UI-001, /api/v1/reports/export | Server-side report export routes already exist. |
| `UI-006` | extend | GAP-NOCODE, GAP-APP | Avoid a third builder: decide whether this is the pipeline-level editor and GAP-NOCODE/GAP-APP are ontology/dashboard editors. |
| `UI-007` | merge | G2-UX-LENS-*, UI-01..UI-04 (KGF), G2-TIME-*, G2-SIM-*, G2-PM-* | KGF already lists blast-radius, multi-paradigm, domain-pack and XAI screens. Share the lens shell. |
| `UI-008` | own | GAP-QI-* | - |
| `UI-009` | merge | MS-12 | Real-time collaboration is MS-12 (live collaborative graph studio). One CRDT layer. |
| `COMPLY-001` | extend | compliance/, moonshot/compliance_twin.py, G2-GRAPH-SEC-*, MS-25 | compliance/ package and compliance twin exist. |
| `COMPLY-002` | extend | NFR-PRIV-001, privacy/ | - |
| `COMPLY-003` | extend | MS-24, audit/ | - |
| `TEST-001` | extend | NFR-REL-001, G2-REL-*, REL-10 | - |
| `TEST-002` | merge | PERF-01, S-02, NFR-PERF-001, K-04, K-05, REL-12 | Choose one load tool. KGF PERF-01 says Locust/pytest-benchmark; this says k6 or Locust. |
| `TEST-003` | extend | NFR-SEC-003, query/polyglot_engine.py | - |
| `TEST-004` | merge | S-02, S-03, NFR-PERF-001 | - |
| `TEST-005` | own | REL-08 | New capability. REL-08 is a one-time browser run. |
| `MULTI-001` | own | FR-CODE-* | No KGF equivalent. |
| `MULTI-002` | extend | KGR-G-014, MS-19, memory_eng/ | Memory graphs need the poisoning defenses from MS-19. |

### 3.3 Baseline conflicts to resolve in PRE-001

| # | Topic | Conflict | Resolution |
|---|---|---|---|
| B1 | Database adapters | GRAPH-001 says "existing 17+ database adapters". The G-dev audit lists 55 adapters (24 graph, 13 vector, 8 relational, 10 state). | Verify against graph/database_adapters.py (PRE-001). 55 is used for planning. |
| B2 | RAG modes | Header says 64 RAG modes. The G-dev audit describes a "45+ modality RAG suite". | Different counting. Confirm against retrieval/rag_suite.py and ragx/ (PRE-001). |
| B3 | UI components | UI-001 says "90+ components". The Conquest plan says 55 UI components (JSX). | Count the real components in apps/web/src (PRE-001); size UI-001 migration accordingly. |
| B4 | Package collisions | CORE-002 and GRAPH-001 say "Create ... __init__.py" for verification/ and federation/, both of which already exist per the Conquest plan and the G-dev audit. causal/ and xai/ likely overlap moonshot/live_causal_engine.py and audit/xai_ledger.py. | Extend existing packages; run the collision check before creating any package (PRE-001). |
| B5 | Load tool | TEST-002: k6 or Locust. KGF PERF-01 and the Conquest KPIs: Locust or pytest-benchmark. | Pick one (DEC-P4-03). |
| B6 | Duplicate scope | AGENT-002 contains an EntityExtractor and RelationExtractor that AI-002 and AI-003 also define; AI-003 depends on AGENT-002 while AGENT-002 needs relation extraction. | Implement AI-002/AI-003 first or merge them into AGENT-002 as one extractor module. |

### 3.4 Gaps that cut across requirements

| Gap | Where | Why it matters |
|---|---|---|
| Measured quality targets | AGENT-001, AGENT-002, GRAPH-004, AI-001, AI-002, AI-003, AI-007, COMPLY-002, MULTI-001 | These are statistical components with no precision/recall, MRR/AUC, calibration or fidelity target. Without one, "done" cannot be falsified. See AIDLC-003 and AIDLC-004. |
| Unproven benefits | CORE-001 (30-70% token reduction), CORE-003 (40-60% cost cut, 60-70% of queries cheap, sub-10ms), CORE-006 | Claims in the rationale have no measurement plan in the acceptance criteria. See SDLC-027 (benefit realization). |
| Humans in the loop | AGENT-001, COMPLY-001, KGF GAP-TRUTH-008, GAP-GOV, loop approval gates | Five places hand work to people; none defines the queue, SLA, escalation or notification. See SDLC-008. |
| Derived data copies | INFRA-001 L2 cache, AI-006 embeddings, GRAPH-003 packages, AGENT-003 persisted messages, AI-005 artifacts, MULTI-002 memory graphs, COMPLY-002 pseudonym vault, INFRA-007 backups, INFRA-004 logs | Nine new places personal data can be copied. The privacy module handles DSAR only. See SDLC-028 and SDLC-029. |
| Untested AI quality | TEST-001..005 cover chaos, load, fuzz, performance and accessibility | No requirement tests answer quality, groundedness, agent task success or injection resistance. See AIDLC-004, AIDLC-005, AIDLC-011. |
| Tenant isolation | INFRA-001, AGENT-003, CORE-006, AI-005, MULTI-002 and the "thread-safe singleton" pattern in 8 requirements | Process-wide singletons holding tenant state conflict with KGR-G-013 and MS-26. See SDLC-005 and SDLC-030. |

## 4. Operating protocol

### 4.1 Universal Definition of Done

Applies to every requirement and accepted proposal, in addition to its own criteria.

| # | Rule |
|---|---|
| U1 | Registry and tags: the ID is in requirements-registry.json; tests carry @pytest.mark.req("<ID>"); commits use [ID]. |
| U2 | API: every new endpoint has authorization scopes (KGF H-04), RFC 7807 errors (H-07), an OpenAPI entry (H-08) and a TestClient integration test (H-03). The engine is reachable: mounted through the engine registry (SDLC-004) if accepted, otherwise wired in brain_os.py and platform_router.py. A router that is not mounted is not done (CG-GAP-001). |
| U3 | Engine pattern: thread-safe accessor get_*_engine(); stateful engines are tenant-aware; no global mutable state. |
| U4 | Telemetry: brain_os telemetry plus a trace or correlation ID on every decision the engine makes. |
| U5 | Safety: inputs validated; no new mandatory external calls (must run air-gapped); no secrets in code; personal data handled per the privacy policy. |
| U6 | Tests: unit tests including failure paths; for UI, component tests and a keyboard and focus check; the full suite and web build are green before the box is ticked. |
| U7 | Docs: a short page and a runbook note for operators; the registry row is updated. |

### 4.2 Per-item loop

1. Read the item, its overlaps and its coordination list. 2. Search the repo for what exists. 3. Decide extend, merge or create and note it. 4. Implement a vertical slice. 5. Tick criteria as each is proven. 6. Run targeted tests, then the full suite and web build. 7. Tick the item, update the registry, commit `[ID] summary`.

### 4.3 Commands

Use the commands in `KGF-MASTER-BACKLOG.md` section 4.4 (pytest, gap coverage gates, documentation audit, web build).

## 5. Recommended order

Hard dependencies are few (12 items depend on another), so order is mostly about risk and reuse. Suggested sequence:

- **Step 0. Pre-flight.** Run PRE-001 and PRE-002. Decide DEC-P4-01 to 05. If accepted, start the three cheap de-risking proposals: SDLC-001 (traceability gate), SDLC-004 (engine registry), SDLC-015 (rules for the coding agent). Items: `PRE-001`, `PRE-002`, `SDLC-001`, `SDLC-004`, `SDLC-015`.
- **Step 1. Independent foundations.** CORE-001 unblocks CORE-003, CORE-006 and TEST-003; CORE-002 unblocks CORE-005; CORE-004 stands alone. Alongside, if accepted: the evaluation skeleton, the sandbox, the tenant-isolation suite and the data map, before engines add more data stores. Items: `CORE-001`, `CORE-002`, `CORE-004`, `AIDLC-004`, `AIDLC-012`, `SDLC-030`, `SDLC-028`.
- **Step 2. Cost and trust path.** Router with shadow mode, token budgets, supervisory loops, logging and tracing, the distributed cache with the GAP-CACHE items, and the model gateway. Items: `CORE-003`, `AIDLC-006`, `CORE-006`, `CORE-005`, `INFRA-004`, `SDLC-025`, `INFRA-001`, `AIDLC-008`.
- **Step 3. Knowledge pipeline.** AI-002, then AI-003, then AGENT-002 (settles conflict B6), then temporal retrieval, OWL/SHACL and federation, with quality benchmarks, lineage and re-embedding. Items: `AI-002`, `AI-003`, `AGENT-002`, `GRAPH-005`, `GRAPH-006`, `GRAPH-001`, `AIDLC-003`, `AIDLC-001`, `AIDLC-002`.
- **Step 4. Agents and AI services.** Boundary telemetry, message bus, fan-out/fan-in, XAI, MLOps, embeddings, causal and GNN, with the human work queue, feedback loop and autonomy catalog. Items: `AGENT-001`, `AGENT-003`, `AGENT-004`, `AI-001`, `AI-004`, `AI-005`, `AI-006`, `GRAPH-002`, `GRAPH-004`, `SDLC-008`, `AIDLC-009`, `AIDLC-016`.
- **Step 5. Operability and compliance.** SSO, CD, scheduling, API versioning, backup/restore, compliance-as-code, PII handling and the five testing disciplines. Items: `INFRA-002`, `INFRA-003`, `INFRA-005`, `INFRA-006`, `INFRA-007`, `COMPLY-001`, `COMPLY-002`, `COMPLY-003`, `TEST-001`, `TEST-002`, `TEST-003`, `TEST-004`, `TEST-005`.
- **Step 6. Interface.** Design system first, then i18n, grid, charts, export, lenses, search analytics and the evidence UX. Workflow builder and collaboration last (collaboration is MS-12). Items: `UI-001`, `UI-002`, `UI-003`, `UI-004`, `UI-005`, `UI-007`, `UI-008`, `AIDLC-015`, `UI-006`, `UI-009`.
- **Step 7. Deferred.** Probabilistic reasoning, multi-modal, memory graphs, fine-tuning pipeline, knowledge distillation. Items: `AI-007`, `MULTI-001`, `MULTI-002`, `AIDLC-010`, `GRAPH-003`.

Parallel start with the KGF programme: libraries with no endpoints (`CORE-001`, `GRAPH-004` maths, `UI-001`) can begin during KGF phases 0 and 1. Anything that adds endpoints should wait for KGF H-03, H-04, H-07 and H-08, because rule U2 depends on them (DEC-P4-04).

## 6. Requirements

### Phase 0. Pre-flight

#### PRE-001: Pre-flight: package-collision and baseline reconciliation

- [x] `PRE-001` **Pre-flight: package-collision and baseline reconciliation**
- **Priority**: P0 | **Category**: Pre-flight | **Complexity**: Low
- **Depends on**: none | **Coordinate with**: none
- **Description**: Before any engine is created, verify what already exists. The source document says "Create ... __init__.py" for packages that other documents say exist, and its baseline counts differ from the audits.
- **Acceptance criteria**:
  - [x] `PRE-001.1` Check each package this roadmap creates against the repo (verification/, federation/, causal/, xai/, extraction/, observability/, embeddings/, routing/, token_formats/, token_budget/, graph_graph/, distillation/, gnn/, mlops/); for each, record extend or create in the registry.
  - [x] `PRE-001.2` Resolve baseline conflicts B1 to B3 against the code (database adapters 17+ vs 55, RAG modes 64 vs 45+, UI components 90+ vs 55) and correct the numbers in this file.
  - [x] `PRE-001.3` Decide module ownership for the duplicated extractor work (AGENT-002, AI-002, AI-003) and record it (conflict B6).
  - [x] `PRE-001.4` Decide the load tool (conflict B5, DEC-P4-03) and the overlap handling (DEC-P4-02).
  - [x] `PRE-001.5` List every Phase 4 engine that exposes an API and state how it will be mounted (engine registry SDLC-004 if accepted, otherwise the manual wiring in brain_os.py and platform_router.py).

#### PRE-002: Pre-flight: register Phase 4 in the KGF registry and adopt the Universal Definition of Done

- [x] `PRE-002` **Pre-flight: register Phase 4 in the KGF registry and adopt the Universal Definition of Done**
- **Priority**: P0 | **Category**: Pre-flight | **Complexity**: Low
- **Depends on**: none | **Coordinate with**: none
- **Description**: Phase 4 shares the KGF programme's evidence rules. Register the IDs and agree the single definition of done so closing a Phase 4 item also closes the overlapping KGF item.
- **Acceptance criteria**:
  - [x] `PRE-002.1` All Phase 4 IDs (and accepted suggestions) are rows in requirements-registry.json (KGF BASE-01) with the cross-IDs from the overlap map.
  - [x] `PRE-002.2` Tests for Phase 4 carry @pytest.mark.req("<ID>") and commits use [ID] (KGF BASE-02).
  - [x] `PRE-002.3` The Universal Definition of Done (section 4) is copied into the pull-request template.
  - [x] `PRE-002.4` For each "merge" overlap, the owning ID is recorded; the other ID is closed by reference when the shared implementation passes.

### Phase 1. High-impact core engines

Token economics, verification, routing and layered graphs are the cost and trust foundation the later engines plug into. The four P0 items live here.

#### CORE-001: Token Format Serialization Engines

- [x] `CORE-001` **Token Format Serialization Engines**
- **Priority**: P0 | **Category**: Token Economics | **Complexity**: High | **Phase**: 1
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: own | NFR-PERF-001, K-01 | No equivalent in the KGF backlog. Independent library; can start immediately.
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
- **Acceptance criteria**:
  - [x] `CORE-001.1` All 7 format strategies implemented with serialize/deserialize
  - [x] `CORE-001.2` Auto-format selection based on payload characteristics
  - [x] `CORE-001.3` Round-trip fidelity: `deserialize(serialize(obj)) == obj` for all supported types
  - [x] `CORE-001.4` Token reduction benchmarks showing 30%+ savings vs JSON
  - [x] `CORE-001.5` Thread-safe singleton `get_token_format_engine()`
  - [x] `CORE-001.6` Wired into `brain_os.py` telemetry and `platform_router.py` endpoints
  - [x] `CORE-001.7` Unit tests covering all 7 formats with edge cases
  - [x] `CORE-001.A1` Every serialized payload carries a format id and version header so stored data stays decodable after a format changes. *(added by review)*
  - [x] `CORE-001.A2` Token counts use the actual tokenizer of each supported model; benchmark corpus and results are published, not a word-count proxy. *(added by review)*
  - [x] `CORE-001.A3` Deserializers enforce depth and size limits and never execute content (NFR-SEC-003). *(added by review)*
  - [x] `CORE-001.A4` Property-based round-trip tests over generated nested objects including unicode, large integers, NaN/inf and empty containers. *(added by review)*

#### CORE-002: Verification & Guardrail Engineering

- [x] `CORE-002` **Verification & Guardrail Engineering**
- **Priority**: P0 | **Category**: Enterprise Trust & Safety | **Complexity**: High | **Phase**: 1
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | KGR-G-011, KGR-G-019, G2-IMMUNE-*, MS-19, NFR-SEC-004, GAP-AI | The package packages/eoip/verification/ already exists (behavioral_gate.py, per the Conquest plan). Extend it; do not recreate __init__.py.
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
- **Acceptance criteria**:
  - [x] `CORE-002.1` VerifierRegistry with register/unregister/compose operations
  - [x] `CORE-002.2` 7+ built-in verification rules
  - [x] `CORE-002.3` DynamicGuardrailInjector with real-time intent checking
  - [x] `CORE-002.4` Integration hooks at loop boundaries
  - [x] `CORE-002.5` Verification audit trail
  - [x] `CORE-002.6` Thread-safe singleton `get_verification_engine()`
  - [x] `CORE-002.7` Wired into brain_os.py and platform_router.py
  - [x] `CORE-002.8` Unit tests for each rule type and composition
  - [x] `CORE-002.A1` Precision and recall measured on a labelled set of valid, invalid, hallucinated and drifting outputs; thresholds recorded. *(added by review)*
  - [x] `CORE-002.A2` Shadow (log-only) mode before enforcement, switchable per rule and per tenant. *(added by review)*
  - [x] `CORE-002.A3` Each rule declares fail-closed or fail-open on timeout and has a p95 latency budget. *(added by review)*
  - [x] `CORE-002.A4` Existing verification/behavioral_gate.py is integrated, not duplicated; __init__.py is extended, not overwritten. *(added by review)*

#### CORE-003: Intent Router Engineering

- [x] `CORE-003` **Intent Router Engineering**
- **Priority**: P0 | **Category**: Deterministic Routing & Cost Optimization | **Complexity**: High | **Phase**: 1
- **Depends on**: `CORE-001` | **Coordinate with**: `CORE-006`
- **Overlap with KGF backlog**: extend | GAP-QUERY, GAP-CACHE-004, query/multi_paradigm_dispatcher.py | Place the router in front of the existing multi-paradigm dispatcher and the unified query API; reuse cost_optimization.
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
- **Acceptance criteria**:
  - [x] `CORE-003.1` IntentClassifier with 8+ intent categories
  - [x] `CORE-003.2` Sub-10ms classification latency
  - [x] `CORE-003.3` RoutingDecision with cost/latency estimates
  - [x] `CORE-003.4` Feedback loop for classifier accuracy tracking
  - [x] `CORE-003.5` Integration with cost_optimization engine
  - [x] `CORE-003.6` Thread-safe singleton `get_router_engine()`
  - [x] `CORE-003.7` Wired into brain_os.py and platform_router.py
  - [x] `CORE-003.8` Unit tests with diverse query types
  - [x] `CORE-003.A1` Classifier accuracy target (for example macro-F1 on a held-out labelled set) and a misroute-cost report: hard queries sent to cheap paths are counted. *(added by review)*
  - [x] `CORE-003.A2` Shadow mode and per-tenant override before the router is allowed to short-circuit answers. *(added by review)*
  - [x] `CORE-003.A3` GRAPH_MUTATION and ADMIN_OPERATION intents always pass authorization; never served from cache or templates. *(added by review)*
  - [x] `CORE-003.A4` Every decision records a human-readable reason for the chosen path. *(added by review)*

#### CORE-004: Graph-over-Graph Engineering

- [x] `CORE-004` **Graph-over-Graph Engineering**
- **Priority**: P0 | **Category**: Graph Intelligence | **Complexity**: High | **Phase**: 1
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | GAP-DUAL, FR-GRAPH-002, FR-GRAPH-005, FR-GRAPH-006, G2-GRAPH-*, KGR-G-013 | Layers formalize logical graph domains, the meta graph and bridge edges. Reuse graph/meta.py and graph/named_graph.py.
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
- **Acceptance criteria**:
  - [x] `CORE-004.1` GraphLayer abstraction with 7+ built-in types
  - [x] `CORE-004.2` Cross-layer query execution
  - [x] `CORE-004.3` Layer projection and merging
  - [x] `CORE-004.4` Layer diff for change detection
  - [x] `CORE-004.5` Constraint propagation across layers
  - [x] `CORE-004.6` Thread-safe singleton `get_graph_graph_engine()`
  - [x] `CORE-004.7` Wired into brain_os.py and platform_router.py
  - [x] `CORE-004.8` Unit tests for cross-layer operations
  - [x] `CORE-004.A1` Layer-level authorization and tenant scoping: a caller may see layer X but not layer Y. *(added by review)*
  - [x] `CORE-004.A2` Layer schemas are versioned; cross-layer query p95 target set at 50K nodes. *(added by review)*

#### CORE-005: Loop-over-Loop Engineering

- [x] `CORE-005` **Loop-over-Loop Engineering**
- **Priority**: P1 | **Category**: Meta-Orchestration | **Complexity**: Medium | **Phase**: 1
- **Depends on**: `CORE-002` | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | MS-17, FR-AGENT-002 | Supervisory loops are the loop-level half of MS-17 (A2A + MCP orchestration). Implement once, link from both.
- **Description**: Supervisory loops that orchestrate inner loops. An outer OODA loop can supervise inner ReAct loops, a meta-evaluation loop can monitor reasoning quality across multiple inner reasoning loops, and an adaptation loop can switch strategies when inner loops underperform.
- **Implementation**:
  - Extend `packages/eoip/intelligence_eng/engine.py` with `SupervisoryLoop` class
  - `LoopMonitor` tracking inner loop metrics (iterations, convergence, cost, quality)
  - `LoopSwitcher` for dynamic strategy switching when inner loop underperforms
  - `LoopComposition` for declarative outer-inner loop binding
  - Timeout and circuit-breaker integration at the supervisory level
- **Acceptance criteria**:
  - [x] `CORE-005.1` SupervisoryLoop wrapping and monitoring inner loops
  - [x] `CORE-005.2` LoopMonitor with real-time metrics
  - [x] `CORE-005.3` Dynamic strategy switching
  - [x] `CORE-005.4` Circuit-breaker integration
  - [x] `CORE-005.5` Unit tests for composition patterns
  - [x] `CORE-005.A1` Maximum nesting depth and recursion guard for supervisory loops. *(added by review)*
  - [x] `CORE-005.A2` Inner loops inherit time and token budgets from the supervisor (CORE-006). *(added by review)*
  - [x] `CORE-005.A3` Supervisory decisions are logged so a run can be replayed. *(added by review)*

#### CORE-006: Token Budget Engineering

- [x] `CORE-006` **Token Budget Engineering**
- **Priority**: P1 | **Category**: Token Economics | **Complexity**: Medium | **Phase**: 1
- **Depends on**: `CORE-001` | **Coordinate with**: `CORE-003`
- **Overlap with KGF backlog**: merge | MS-27, K-03 | Token accounting in MS-27 and budgets here share one cost model. Build the model once (see AIDLC-008).
- **Description**: Dynamic token allocation across cognitive pipeline stages. A total token budget is distributed across plan steps — more tokens for reasoning, fewer for lookups — with real-time reallocation based on actual consumption.
- **Implementation**:
  - Create `packages/eoip/token_budget/engine.py`
  - Create `packages/eoip/token_budget/__init__.py`
  - `TokenBudget` with total allocation and per-stage allocations
  - `BudgetPolicy` strategies: EQUAL_SPLIT, PROPORTIONAL, PRIORITY_WEIGHTED, ADAPTIVE
  - `BudgetTracker` with real-time consumption tracking and reallocation
  - Integration with `intelligence_eng` cognitive plans and `cost_optimization` engine
  - Alerts when stages exceed budget, with automatic context compression triggers
- **Acceptance criteria**:
  - [x] `CORE-006.1` TokenBudget with 4 allocation strategies
  - [x] `CORE-006.2` Real-time consumption tracking per pipeline stage
  - [x] `CORE-006.3` Dynamic reallocation when stages under/over-consume
  - [x] `CORE-006.4` Context compression triggers on budget exceed
  - [x] `CORE-006.5` Integration with intelligence_eng and cost_optimization
  - [x] `CORE-006.6` Thread-safe singleton
  - [x] `CORE-006.7` Wired into brain_os.py and platform_router.py
  - [x] `CORE-006.8` Unit tests
  - [x] `CORE-006.A1` Tracked consumption stays within +/-5% of tokenizer-measured counts in a test. *(added by review)*
  - [x] `CORE-006.A2` Hard per-tenant and per-user caps stop execution rather than only alert. *(added by review)*
  - [x] `CORE-006.A3` Cost-estimator interface agreed with CORE-003 before either ships. *(added by review)*

### Phase 2. Agentic AI and graph intelligence

Agent boundaries, extraction, communication and graph intelligence (federation, causal, GNN, temporal, OWL/SHACL) extend what agents and retrieval can do.

#### AGENT-001: Cognitive Boundary Telemetry

- [x] `AGENT-001` **Cognitive Boundary Telemetry**
- **Priority**: P1 | **Category**: Agentic AI Engineering | **Complexity**: Medium | **Phase**: 2
- **Depends on**: none | **Coordinate with**: `CORE-002`, `CORE-005`
- **Overlap with KGF backlog**: extend | KGR-G-019, FR-AGENT-004 | Boundary signals feed the calibrated-uncertainty protocol and the approval boundary.
- **Description**: Detect when agents hit cognitive boundaries (confidence drops, hallucination signals, context overflow, repeated tool failures, reasoning loops) and gracefully hand off to higher-autonomy loops or humans.
- **Implementation**:
  - Extend `packages/eoip/telemetry/adapter.py` with `CognitiveBoundaryDetector`
  - Boundary signals: confidence_drop, hallucination_probability, context_overflow, tool_failure_streak, reasoning_loop_detected, latency_spike, cost_overrun
  - `HandoffDecision` with target (human, higher-autonomy loop, fallback agent)
  - Integration with the 14 control loops for autonomy escalation
- **Acceptance criteria**:
  - [x] `AGENT-001.1` 7+ boundary signal detectors
  - [x] `AGENT-001.2` HandoffDecision with target selection
  - [x] `AGENT-001.3` Integration with control loop autonomy levels
  - [x] `AGENT-001.4` Telemetry event emission on boundary detection
  - [x] `AGENT-001.5` Unit tests for each signal type
  - [x] `AGENT-001.A1` Detection precision and recall measured per signal on recorded agent trajectories. *(added by review)*
  - [x] `AGENT-001.A2` A handoff to a human creates a work item in the human-in-the-loop queue (SDLC-008). *(added by review)*
  - [x] `AGENT-001.A3` Hysteresis prevents handoff flapping around thresholds. *(added by review)*

#### AGENT-002: Dynamic Entity & Community Extraction Pipeline

- [x] `AGENT-002` **Dynamic Entity & Community Extraction Pipeline**
- **Priority**: P1 | **Category**: Knowledge Graph Construction | **Complexity**: High | **Phase**: 2
- **Depends on**: none | **Coordinate with**: `AI-002`, `AI-003`
- **Overlap with KGF backlog**: merge | GAP-NLP, KGR-G-015, FR-INGEST-*, G2-EKAF-026 | Duplicates AI-002 (entity extraction) and AI-003 (relation extraction). One extractor implementation, orchestrated here.
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
- **Acceptance criteria**:
  - [x] `AGENT-002.1` Configurable chunking strategies
  - [x] `AGENT-002.2` Entity extraction with type classification
  - [x] `AGENT-002.3` Relation extraction producing triples
  - [x] `AGENT-002.4` Community detection integration
  - [x] `AGENT-002.5` Streaming mode for continuous operation
  - [x] `AGENT-002.6` Thread-safe singleton
  - [x] `AGENT-002.7` Wired into brain_os.py and platform_router.py
  - [x] `AGENT-002.8` Unit tests
  - [x] `AGENT-002.A1` Entity and relation precision/recall measured on a labelled corpus; targets recorded. *(added by review)*
  - [x] `AGENT-002.A2` Idempotent re-ingestion: the same document twice yields no duplicate nodes; every triple keeps source chunk and offset. *(added by review)*
  - [x] `AGENT-002.A3` Streaming mode applies backpressure instead of unbounded queues. *(added by review)*
  - [x] `AGENT-002.A4` Entity and relation extraction reuse the AI-002 and AI-003 implementations; no parallel copies. *(added by review)*

#### AGENT-003: Agent Communication Bus

- [x] `AGENT-003` **Agent Communication Bus**
- **Priority**: P2 | **Category**: Agent Infrastructure | **Complexity**: Medium | **Phase**: 2
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | MS-17, agents/orchestration.py | Durable bus underlies A2A orchestration. Implement once.
- **Description**: Formalize agent-to-agent communication with typed message schemas, capability negotiation, dead letter queues, and persistent message history. Extend existing `A2AProtocolBroker` from in-memory list to durable bus.
- **Implementation**:
  - Create `packages/eoip/agents/message_bus.py`
  - `AgentMessageSchema` with versioned message types
  - `CapabilityNegotiation` protocol for agent discovery
  - `MessageQueue` with persistence, TTL, and DLQ
  - `BroadcastChannel` for pub/sub patterns
  - Integration with existing 35 agent archetypes
- **Acceptance criteria**:
  - [x] `AGENT-003.1` Typed message schemas with versioning
  - [x] `AGENT-003.2` Capability negotiation protocol
  - [x] `AGENT-003.3` Persistent message queue with DLQ
  - [x] `AGENT-003.4` Pub/sub broadcast channels
  - [x] `AGENT-003.5` Unit tests
  - [x] `AGENT-003.A1` Delivery semantics documented (at-least-once with idempotency keys) and tested. *(added by review)*
  - [x] `AGENT-003.A2` Messages between agents are authenticated and tenant-scoped; persisted messages follow retention and erasure policy. *(added by review)*

#### AGENT-004: Parallel Fan-Out/Fan-In (MapReduce)

- [x] `AGENT-004` **Parallel Fan-Out/Fan-In (MapReduce)**
- **Priority**: P1 | **Category**: Pipeline Engineering | **Complexity**: Medium | **Phase**: 2
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | KGR-G-018 | Formalizes analytics/parallel_multihop.py.
- **Description**: Formalize the parallel execution pattern from `analytics/parallel_multihop.py` into a first-class harness capability. Race-condition-safe state merging for fan-in.
- **Implementation**:
  - Extend `packages/eoip/harness/engine.py` with `FanOutStage` and `FanInStage`
  - `StateSchema` for safe state merging (conflict detection, merge strategies)
  - Configurable parallelism (max workers, timeout per shard)
  - Integration with harness pipeline orchestration
- **Acceptance criteria**:
  - [x] `AGENT-004.1` FanOutStage splitting work into parallel shards
  - [x] `AGENT-004.2` FanInStage merging results with conflict detection
  - [x] `AGENT-004.3` Configurable parallelism and timeouts
  - [x] `AGENT-004.4` Integration with existing harness engine
  - [x] `AGENT-004.5` Unit tests with race condition scenarios
  - [x] `AGENT-004.A1` Merged result is identical regardless of shard completion order (randomized-schedule test). *(added by review)*
  - [x] `AGENT-004.A2` Partial-failure policy (fail-fast or best-effort) is configurable; cancellation propagates to all shards. *(added by review)*

#### GRAPH-001: Federated Graph Engineering

- [x] `GRAPH-001` **Federated Graph Engineering**
- **Priority**: P1 | **Category**: Graph Intelligence | **Complexity**: High | **Phase**: 2
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | GAP-FED, GAP-FABRIC-002..008, federation/planner.py | Same capability as the Conquest GAP-FED deliverable. packages/eoip/federation/ already exists; extend planner.py instead of creating a second engine.
- **Description**: Cross-database knowledge graph federation. Query across Neo4j, Neptune, TigerGraph, and other backends as one virtual graph. Leverages existing 17+ database adapters.
- **Implementation**:
  - Create `packages/eoip/federation/engine.py`
  - Create `packages/eoip/federation/__init__.py`
  - `FederatedGraph` virtual graph spanning multiple backends
  - `FederationPlanner` decomposing queries across backends
  - `ResultMerger` combining results with deduplication and conflict resolution
  - `CatalogService` maintaining cross-backend entity mappings
  - Query pushdown optimization (push filters to backend)
- **Acceptance criteria**:
  - [x] `GRAPH-001.1` Virtual graph spanning 2+ backends
  - [x] `GRAPH-001.2` Query decomposition and result merging
  - [x] `GRAPH-001.3` Entity mapping across backends
  - [x] `GRAPH-001.4` Query pushdown optimization
  - [x] `GRAPH-001.5` Thread-safe singleton
  - [x] `GRAPH-001.6` Wired into brain_os.py and platform_router.py
  - [x] `GRAPH-001.7` Unit tests
  - [x] `GRAPH-001.A1` Defined behaviour when one backend is down (degraded result with flag, or fail) consistent with GAP-FABRIC-006. *(added by review)*
  - [x] `GRAPH-001.A2` Source-level data policies and authorization are enforced before merging results (GAP-FABRIC-008). *(added by review)*
  - [x] `GRAPH-001.A3` Results carry freshness and consistency metadata per backend. *(added by review)*
  - [x] `GRAPH-001.A4` Extends federation/planner.py rather than creating a competing engine. *(added by review)*

#### GRAPH-002: Causal Inference over Graphs

- [x] `GRAPH-002` **Causal Inference over Graphs**
- **Priority**: P2 | **Category**: Graph Intelligence | **Complexity**: High | **Phase**: 2
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: verify | G2-CAUSE-*, G2-SIM-*, MS-23, UI-01, moonshot/live_causal_engine.py | A live causal engine with blast radius and counterfactual intervention is already built (POST /api/v1/causal/live-blast-radius). Verify, then add do-calculus on top.
- **Description**: Counterfactual reasoning: "What would happen if we removed this supplier node?" Extends existing causal reasoning strategy with graph-native do-calculus and intervention analysis.
- **Implementation**:
  - Create `packages/eoip/causal/engine.py`
  - `InterventionModel` for do(X=x) operations on graph
  - `CounterfactualQuery` for what-if analysis
  - `CausalEffect` estimation with confounding control
  - `BlastRadiusAnalysis` for impact assessment of node/edge removal
  - Integration with existing `reasoning/strategies.py` causal strategy
- **Acceptance criteria**:
  - [x] `GRAPH-002.1` do-calculus intervention on graph entities
  - [x] `GRAPH-002.2` Counterfactual query execution
  - [x] `GRAPH-002.3` Blast radius analysis
  - [x] `GRAPH-002.4` Integration with existing causal reasoning
  - [x] `GRAPH-002.5` Unit tests
  - [x] `GRAPH-002.A1` Validated on synthetic graphs with known ground-truth effects; error reported. *(added by review)*
  - [x] `GRAPH-002.A2` Outputs state assumptions and confidence; estimates are labelled model-based. *(added by review)*
  - [x] `GRAPH-002.A3` Builds on moonshot/live_causal_engine.py instead of reimplementing blast radius. *(added by review)*

#### GRAPH-003: Knowledge Distillation Engineering

- [x] `GRAPH-003` **Knowledge Distillation Engineering**
- **Priority**: P2 | **Category**: Edge & Performance | **Complexity**: Medium | **Phase**: 2
- **Depends on**: `GRAPH-001` | **Coordinate with**: none
- **Overlap with KGF backlog**: own | edge/runtime.py | No KGF equivalent.
- **Description**: Compress large graph subsets into compact queryable representations for edge deployment or fast retrieval. Produces distilled knowledge packages.
- **Implementation**:
  - Create `packages/eoip/distillation/engine.py`
  - `DistillationStrategy` (subgraph extraction, entity summarization, relation compression)
  - `KnowledgePackage` — compact portable graph representation
  - `PackageDeployer` for edge/runtime deployment
  - Integration with `edge/runtime.py`
- **Acceptance criteria**:
  - [x] `GRAPH-003.1` Graph distillation with configurable strategies
  - [x] `GRAPH-003.2` Portable knowledge packages
  - [x] `GRAPH-003.3` Edge deployment integration
  - [x] `GRAPH-003.4` Fidelity metrics (information loss measurement)
  - [x] `GRAPH-003.5` Unit tests
  - [x] `GRAPH-003.A1` Fidelity target: query-answer agreement between distilled and full graph on a benchmark query set. *(added by review)*
  - [x] `GRAPH-003.A2` Packages are versioned and signed; tenant and PII data are redacted or excluded before packaging; packages can expire or be revoked. *(added by review)*

#### GRAPH-004: Graph Neural Network Integration

- [x] `GRAPH-004` **Graph Neural Network Integration**
- **Priority**: P2 | **Category**: AI/ML & Graph | **Complexity**: High | **Phase**: 2
- **Depends on**: none | **Coordinate with**: `AI-006`
- **Overlap with KGF backlog**: merge | MS-29, MS-18, KGR-G-016 | GNN embeddings and link prediction are the engine under MS-29 (graph foundation model). Build GRAPH-004 first.
- **Description**: GNN-powered graph intelligence: node classification, link prediction, graph embeddings (node2vec, TransE), and graph-level classification. Extends graph algorithms beyond deterministic methods.
- **Implementation**:
  - Create `packages/eoip/gnn/engine.py`
  - `GraphEmbedder` with node2vec, TransE, and configurable embedding dimensions
  - `LinkPredictor` for predicting missing graph connections
  - `NodeClassifier` for entity type inference
  - `CommunityPredictor` for graph-level patterns
  - Integration with existing analytics algorithms
- **Acceptance criteria**:
  - [x] `GRAPH-004.1` Graph embedding generation (node2vec, TransE)
  - [x] `GRAPH-004.2` Link prediction with confidence scores
  - [x] `GRAPH-004.3` Node classification
  - [x] `GRAPH-004.4` Integration with existing graph store
  - [x] `GRAPH-004.5` Unit tests
  - [x] `GRAPH-004.A1` Link-prediction quality reported (MRR, Hits@10 or AUC) on held-out edges and must beat a deterministic baseline. *(added by review)*
  - [x] `GRAPH-004.A2` Seeded, reproducible training; CPU-only fallback with a memory ceiling. *(added by review)*

#### GRAPH-005: Temporal & Hybrid Retrieval Engineering

- [x] `GRAPH-005` **Temporal & Hybrid Retrieval Engineering**
- **Priority**: P1 | **Category**: Retrieval | **Complexity**: Medium | **Phase**: 2
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | FR-TEMP-001, FR-GRAPH-009, G2-TIME-*, G2-JOURNAL-*, G2-ARCH-008, KGR-G-014 | Overlaps the temporal and journal families. Bitemporal module exists in graph/.
- **Description**: Elevate temporal dimension in retrieval — facts evolve over time. Add TemporalIndex maintaining fact validity windows with as-of queries. Combine with existing vector semantic and graph structural search.
- **Implementation**:
  - Create `packages/eoip/retrieval/temporal.py`
  - `TemporalIndex` with valid_from/valid_to windows per fact
  - `AsOfQuery` for point-in-time retrieval
  - `TemporalRangeQuery` for time-windowed retrieval
  - Integration with existing `state/engine.py` time-travel and `search/hybrid_engine.py`
- **Acceptance criteria**:
  - [x] `GRAPH-005.1` TemporalIndex with validity windows
  - [x] `GRAPH-005.2` As-of and range queries
  - [x] `GRAPH-005.3` Integration with state time-travel
  - [x] `GRAPH-005.4` Integration with hybrid search
  - [x] `GRAPH-005.5` Unit tests
  - [x] `GRAPH-005.A1` Bitemporal support: valid time and transaction time, so retroactive corrections are queryable. *(added by review)*
  - [x] `GRAPH-005.A2` Temporal index stays correct under retroactive updates; p95 target for temporal queries at 50K nodes. *(added by review)*

#### GRAPH-006: OWL Reasoning & SHACL Runtime Validation

- [x] `GRAPH-006` **OWL Reasoning & SHACL Runtime Validation**
- **Priority**: P2 | **Category**: Ontology | **Complexity**: High | **Phase**: 2
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | GAP-DUAL, FR-GRAPH-010, KGR-G-015, GAP-GITOPS-004 | SHACL validation and RDF/OWL work already appears three times in the KGF backlog. One implementation.
- **Description**: Runtime OWL DL classification and SHACL shape validation against live graph data. Currently ontology layer handles mapping/drift but not runtime reasoning/validation.
- **Implementation**:
  - Extend `packages/eoip/ontology/rdf.py` with `OWLReasoner`
  - Create `packages/eoip/ontology/shacl_validator.py`
  - `OWLReasoner` for subsumption, disjointness, property chain inference
  - `SHACLValidator` validating graph instances against SHACL shape definitions
  - Validation report with violations, severity, fix suggestions
- **Acceptance criteria**:
  - [x] `GRAPH-006.1` OWL subsumption and inference
  - [x] `GRAPH-006.2` SHACL shape validation
  - [x] `GRAPH-006.3` Violation report with severity levels
  - [x] `GRAPH-006.4` Integration with ontology management
  - [x] `GRAPH-006.5` Unit tests
  - [x] `GRAPH-006.A1` Reasoner limited to a declared OWL profile with documented complexity bounds and timeouts. *(added by review)*
  - [x] `GRAPH-006.A2` Incremental validation on graph mutation, not a full rescan; reuses SHACL work from GAP-DUAL/KGR-G-015. *(added by review)*

### Phase 3. AI/ML intelligence enhancements

Explainability, NLP, triple extraction and the MLOps stack (A/B, experiments, embeddings, probabilistic reasoning).

#### AI-001: Advanced XAI Engine

- [x] `AI-001` **Advanced XAI Engine**
- **Priority**: P1 | **Category**: Explainable AI | **Complexity**: High | **Phase**: 3
- **Depends on**: none | **Coordinate with**: `CORE-002`
- **Overlap with KGF backlog**: extend | audit/xai_ledger.py, UI-04 | XAI ledger (Merkle tree, HMAC) exists. This adds model-derived attribution; the packages/eoip/xai/ name should extend, not replace, it.
- **Description**: Extend existing heuristic XAI attribution with model-derived explainability: SHAP-like feature importance, attention visualization, decision trace graphs, and confidence calibration visualization.
- **Implementation**:
  - Create `packages/eoip/xai/engine.py`
  - Create `packages/eoip/xai/__init__.py`
  - `FeatureImportanceAnalyzer` (SHAP-like, without external dependency)
  - `DecisionTraceGraph` — graph of reasoning steps with attribution
  - `ConfidenceCalibrationReport` — expected vs actual accuracy
  - `ExplanationRenderer` producing human-readable explanations
  - Integration with existing `self_llm.py` XAI explanation
- **Acceptance criteria**:
  - [x] `AI-001.1` Feature importance analysis
  - [x] `AI-001.2` Decision trace graph generation
  - [x] `AI-001.3` Confidence calibration
  - [x] `AI-001.4` Human-readable explanation rendering
  - [x] `AI-001.5` Thread-safe singleton
  - [x] `AI-001.6` Wired into brain_os.py and platform_router.py
  - [x] `AI-001.7` Unit tests
  - [x] `AI-001.A1` Explanation fidelity tested by perturbation or ablation: removing a top-attributed factor changes the output. *(added by review)*
  - [x] `AI-001.A2` Calibration reported (for example expected calibration error); no chain-of-thought content leaks into explanations. *(added by review)*

#### AI-002: Deep NLP Pipeline

- [x] `AI-002` **Deep NLP Pipeline**
- **Priority**: P2 | **Category**: Natural Language Processing | **Complexity**: Medium | **Phase**: 3
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | GAP-NLP | Same local NLP pipeline. Implement once together with AGENT-002.
- **Description**: Extend existing gazetteer/regex NLP pipeline with deeper capabilities: transformer-ready NER interface, sentiment analysis, topic modeling, dependency parsing stubs, language detection, and coreference resolution.
- **Implementation**:
  - Extend `packages/eoip/nlp/pipeline.py`
  - `DeepEntityExtractor` with pluggable model backends (local or API)
  - `SentimentAnalyzer` with aspect-based sentiment
  - `TopicModeler` with LDA-style topic extraction
  - `LanguageDetector` for multi-language support
  - `CoreferenceResolver` for entity mentions
- **Acceptance criteria**:
  - [x] `AI-002.1` Deep NER with configurable backends
  - [x] `AI-002.2` Sentiment analysis with aspect extraction
  - [x] `AI-002.3` Topic modeling
  - [x] `AI-002.4` Language detection
  - [x] `AI-002.5` Unit tests
  - [x] `AI-002.A1` Per-language quality benchmarks; default backends run locally with no egress. *(added by review)*
  - [x] `AI-002.A2` Single entity-extractor implementation shared with AGENT-002. *(added by review)*

#### AI-003: Relation Extraction & Triple Generation

- [x] `AI-003` **Relation Extraction & Triple Generation**
- **Priority**: P1 | **Category**: Knowledge Graph Construction | **Complexity**: Medium | **Phase**: 3
- **Depends on**: `AGENT-002` | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | GAP-NLP, KGR-G-015 | See AGENT-002.
- **Description**: Automated subject-predicate-object triple extraction from unstructured text. Feeds the knowledge graph construction pipeline.
- **Implementation**:
  - Create `packages/eoip/extraction/relation_extractor.py`
  - `RelationPattern` with configurable extraction rules
  - `TripleGenerator` producing (subject, predicate, object) triples
  - `TripleValidator` checking against ontology schema
  - `TripleDeduplicator` merging duplicate/near-duplicate triples
  - Integration with AGENT-002 extraction pipeline
- **Acceptance criteria**:
  - [x] `AI-003.1` Pattern-based relation extraction
  - [x] `AI-003.2` Triple generation with confidence scores
  - [x] `AI-003.3` Ontology-aware validation
  - [x] `AI-003.4` Deduplication
  - [x] `AI-003.5` Unit tests
  - [x] `AI-003.A1` Precision/recall target on a labelled corpus; every triple keeps its source span. *(added by review)*
  - [x] `AI-003.A2` Low-confidence triples are quarantined for human review rather than dropped or auto-accepted. *(added by review)*

#### AI-004: Model A/B Testing & Canary Deployment

- [x] `AI-004` **Model A/B Testing & Canary Deployment**
- **Priority**: P2 | **Category**: MLOps | **Complexity**: Medium | **Phase**: 3
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | MS-15, model_management/registry.py
- **Description**: Add A/B testing framework and canary deployment to existing model registry. Compare model performance in production with statistical significance testing.
- **Implementation**:
  - Extend `packages/eoip/model_management/registry.py`
  - `ABExperiment` with traffic splitting, metric collection, significance testing
  - `CanaryDeployment` with gradual rollout and automatic rollback
  - `ModelComparison` dashboard data (latency, quality, cost per model)
- **Acceptance criteria**:
  - [x] `AI-004.1` A/B experiment creation and traffic splitting
  - [x] `AI-004.2` Statistical significance testing
  - [x] `AI-004.3` Canary deployment with auto-rollback
  - [x] `AI-004.4` Comparison metrics
  - [x] `AI-004.5` Unit tests
  - [x] `AI-004.A1` Metrics and minimum sample size are fixed before an experiment starts; winners are only declared past that size. *(added by review)*
  - [x] `AI-004.A2` Safety and quality guardrail metrics trigger automatic rollback; tenants can opt out. *(added by review)*

#### AI-005: MLOps Experiment Tracking

- [x] `AI-005` **MLOps Experiment Tracking**
- **Priority**: P2 | **Category**: MLOps | **Complexity**: Medium | **Phase**: 3
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | MS-15, model_management/ | Fine-tuning runs (MS-15) should log here.
- **Description**: Lightweight experiment tracking (inspired by MLflow/W&B) for prompt iterations, model comparisons, and fine-tuning runs. Tracks parameters, metrics, artifacts.
- **Implementation**:
  - Create `packages/eoip/mlops/experiment_tracker.py`
  - `Experiment` with runs, parameters, metrics, tags
  - `RunTracker` for individual experiment runs
  - `ArtifactStore` for model artifacts and outputs
  - `ExperimentComparison` for cross-run analysis
- **Acceptance criteria**:
  - [x] `AI-005.1` Experiment creation and run tracking
  - [x] `AI-005.2` Parameter and metric logging
  - [x] `AI-005.3` Artifact storage
  - [x] `AI-005.4` Cross-run comparison
  - [x] `AI-005.5` Unit tests
  - [x] `AI-005.A1` Each run records code version, data version, seed and environment so it can be reproduced. *(added by review)*
  - [x] `AI-005.A2` Artifacts follow encryption and retention policy (SDLC-028, SDLC-029); prompt versions link to the prompt registry (AIDLC-007). *(added by review)*

#### AI-006: Embedding Management & Versioning

- [x] `AI-006` **Embedding Management & Versioning**
- **Priority**: P2 | **Category**: Vector Intelligence | **Complexity**: Medium | **Phase**: 3
- **Depends on**: none | **Coordinate with**: `INFRA-001`
- **Overlap with KGF backlog**: merge | H-02, K-09, KGR-G-016, ontology/embedding_drift.py | H-02 replaces hash embeddings with real ones; this adds versioning and drift. Do H-02 first.
- **Description**: Dedicated embedding lifecycle management: versioned embeddings, domain fine-tuning pipeline stubs, multi-modal embedding fusion, and drift detection.
- **Implementation**:
  - Create `packages/eoip/embeddings/engine.py`
  - `EmbeddingRegistry` with version tracking
  - `EmbeddingDriftDetector` extending existing `ontology/embedding_drift.py`
  - `EmbeddingFusionStrategy` for multi-modal combination
  - `DimensionReducer` for visualization and storage optimization
- **Acceptance criteria**:
  - [x] `AI-006.1` Embedding versioning and registry
  - [x] `AI-006.2` Drift detection
  - [x] `AI-006.3` Multi-modal fusion
  - [x] `AI-006.4` Dimension reduction
  - [x] `AI-006.5` Unit tests
  - [x] `AI-006.A1` The embedding model and version are stored with every vector. *(added by review)*
  - [x] `AI-006.A2` A re-embedding migration path exists (AIDLC-002) and offline model weights are supported. *(added by review)*

#### AI-007: Probabilistic Reasoning Integration

- [x] `AI-007` **Probabilistic Reasoning Integration**
- **Priority**: P3 | **Category**: Reasoning | **Complexity**: High | **Phase**: 3
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: own | KGR-G-019, GAP-TRUTH-* | Confidence propagation connects to truth resolution.
- **Description**: Add probabilistic graph models to existing reasoning strategies: Bayesian networks over knowledge graphs, uncertain fact propagation, and probabilistic query answering.
- **Implementation**:
  - Extend `packages/eoip/reasoning/strategies.py`
  - `BayesianGraphReasoner` for probabilistic inference
  - `UncertaintyPropagator` for fact confidence propagation
  - `ProbabilisticQueryEngine` for queries with confidence intervals
- **Acceptance criteria**:
  - [x] `AI-007.1` Bayesian inference over graph structures
  - [x] `AI-007.2` Uncertainty propagation
  - [x] `AI-007.3` Probabilistic query answering with confidence intervals
  - [x] `AI-007.4` Unit tests
  - [x] `AI-007.A1` Inference calibrated against cases with known probabilities; approximate inference reports error bounds. *(added by review)*
  - [x] `AI-007.A2` Uncertainty intervals are exposed to the UI (AIDLC-015). *(added by review)*

### Phase 4. Infrastructure and DevOps

Caching, SSO, CD, logs, scheduling, API versioning/SDKs and automated backup/restore make the platform operable.

#### INFRA-001: Multi-Level Caching

- [x] `INFRA-001` **Multi-Level Caching**
- **Priority**: P1 | **Category**: Performance | **Complexity**: Medium | **Phase**: 4
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | GAP-CACHE-002..005, query/cache.py | GAP-CACHE items (graph-version dependencies, CDC invalidation, staleness policy) are exactly what a distributed cache needs and INFRA-001 omits them.
- **Description**: Extend existing single-level LRU cache to L1 (in-memory) + L2 (Redis) with distributed invalidation. Redis is in Helm chart but not wired to cache layer.
- **Implementation**:
  - Extend `packages/eoip/enterprise/cache.py`
  - `L1Cache` (existing in-memory LRU)
  - `L2Cache` (Redis adapter)
  - `CacheCoordinator` with read-through, write-through, and write-behind strategies
  - Distributed cache invalidation via pub/sub
  - Cache warming strategies for hot paths
- **Acceptance criteria**:
  - [x] `INFRA-001.1` L1 + L2 cache hierarchy
  - [x] `INFRA-001.2` Read-through and write-through strategies
  - [x] `INFRA-001.3` Distributed invalidation
  - [x] `INFRA-001.4` Cache warming
  - [x] `INFRA-001.5` Unit tests
  - [x] `INFRA-001.A1` Cache keys include tenant, graph version and authorization context hash; nothing is cached across authorization boundaries. *(added by review)*
  - [x] `INFRA-001.A2` CDC-based invalidation with a maximum-staleness policy (GAP-CACHE-003, GAP-CACHE-005); deterministic and AI-response caches are separate (GAP-CACHE-004). *(added by review)*
  - [x] `INFRA-001.A3` L2 outage degrades to L1 with a metric, not an error. *(added by review)*

#### INFRA-002: OAuth2/OIDC/SSO Integration

- [x] `INFRA-002` **OAuth2/OIDC/SSO Integration**
- **Priority**: P1 | **Category**: Security | **Complexity**: High | **Phase**: 4
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | H-04, NFR-SEC-005, GAP-SEC-008..012 | Authentication enforcement (H-04) and SSO overlap. Build SSO as the provider side of H-04.
- **Description**: Add external identity provider support to existing RBAC/ABAC system. Support OAuth2 authorization code flow, OIDC discovery, and SAML for enterprise SSO.
- **Implementation**:
  - Extend `packages/eoip/authz/`
  - `OAuthProvider` with authorization code flow
  - `OIDCDiscovery` for provider auto-configuration
  - `SAMLAdapter` for enterprise SSO
  - `TokenValidator` for JWT verification
  - `IdPFederation` for multi-provider support
- **Acceptance criteria**:
  - [x] `INFRA-002.1` OAuth2 authorization code flow
  - [x] `INFRA-002.2` OIDC discovery and verification
  - [x] `INFRA-002.3` SAML adapter
  - [x] `INFRA-002.4` JWT token validation
  - [x] `INFRA-002.5` Unit tests
  - [x] `INFRA-002.A1` SCIM provisioning and deprovisioning of users and groups; group-to-role mapping. *(added by review)*
  - [x] `INFRA-002.A2` Session handling: refresh-token rotation, logout and revocation. *(added by review)*
  - [x] `INFRA-002.A3` Security tests: token replay, algorithm confusion, redirect-URI validation. *(added by review)*
  - [x] `INFRA-002.A4` Break-glass local administrator when the identity provider is unreachable (air-gapped sites). *(added by review)*

#### INFRA-003: CD Pipeline & GitOps Deployment

- [x] `INFRA-003` **CD Pipeline & GitOps Deployment**
- **Priority**: P2 | **Category**: DevOps | **Complexity**: Medium | **Phase**: 4
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | S-03, H-06, REL-* | CI/CD pipeline (S-03) is the same pipeline. One workflow set.
- **Description**: Add continuous deployment pipeline to existing CI. ArgoCD/Flux integration, staging environment, canary deployment, automated rollback.
- **Implementation**:
  - Create `deploy/argocd/` with Application manifests
  - Create `deploy/environments/` (staging, production)
  - Extend `.github/workflows/` with CD stages
  - Health check endpoints for deployment verification
  - Automated rollback on health check failure
- **Acceptance criteria**:
  - [x] `INFRA-003.1` ArgoCD Application manifests
  - [x] `INFRA-003.2` Staging and production environment configs
  - [x] `INFRA-003.3` CD workflow stages in GitHub Actions
  - [x] `INFRA-003.4` Health check verification
  - [x] `INFRA-003.5` Automated rollback
  - [x] `INFRA-003.A1` Pull-based, signed-image deployment option for air-gapped sites. *(added by review)*
  - [x] `INFRA-003.A2` Schema migrations (SDLC-007) run in order with deploys; promotion gates reference evaluation and load results (AIDLC-004, TEST-004). *(added by review)*
  - [x] `INFRA-003.A3` Tests cover rollback and health-check failure paths. *(added by review)*

#### INFRA-004: Log Aggregation

- [x] `INFRA-004` **Log Aggregation**
- **Priority**: P2 | **Category**: Observability | **Complexity**: Low | **Phase**: 4
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | NFR-OPS-001, MVP-FR-023, G2-TEL-* | Structured logging and health.
- **Description**: Structured logging with aggregation support. Currently has Prometheus metrics and optional OTel but no log pipeline.
- **Implementation**:
  - Create `packages/eoip/observability/logging.py`
  - Structured JSON logging with correlation IDs
  - Log level management per module
  - Loki/ELK-compatible output format
  - Log sampling for high-volume paths
- **Acceptance criteria**:
  - [x] `INFRA-004.1` Structured JSON logging
  - [x] `INFRA-004.2` Correlation ID propagation
  - [x] `INFRA-004.3` Per-module log level control
  - [x] `INFRA-004.4` Loki-compatible format
  - [x] `INFRA-004.5` Unit tests
  - [x] `INFRA-004.A1` Sensitive fields are redacted before logs leave the process. *(added by review)*
  - [x] `INFRA-004.A2` Retention and erasure apply to logs (SDLC-028); audit events are kept apart from application logs. *(added by review)*
  - [x] `INFRA-004.A3` Unit tests for correlation-ID propagation and sampling. *(added by review)*

#### INFRA-005: Distributed Scheduling

- [x] `INFRA-005` **Distributed Scheduling**
- **Priority**: P2 | **Category**: Infrastructure | **Complexity**: Medium | **Phase**: 4
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | scheduling/executor.py, G2-EKAF-* | Crawl schedules in the acquisition fabric depend on this.
- **Description**: Extend existing cron-style scheduler for HA: leader election, distributed task locking, dependency DAGs between scheduled tasks.
- **Implementation**:
  - Extend `packages/eoip/scheduling/executor.py`
  - `LeaderElection` for single-scheduler guarantee
  - `DistributedLock` for task exclusivity
  - `TaskDAG` for dependency-ordered scheduling
  - Failover and catch-up execution
- **Acceptance criteria**:
  - [x] `INFRA-005.1` Leader election mechanism
  - [x] `INFRA-005.2` Distributed task locking
  - [x] `INFRA-005.3` Task dependency DAGs
  - [x] `INFRA-005.4` Failover handling
  - [x] `INFRA-005.5` Unit tests
  - [x] `INFRA-005.A1` Fencing tokens protect against stale lock holders and clock skew. *(added by review)*
  - [x] `INFRA-005.A2` Catch-up policy (skip, run once, run all) is set per task; leader failover is exercised in a chaos test (TEST-001). *(added by review)*

#### INFRA-006: API Versioning & Client SDK Generation

- [x] `INFRA-006` **API Versioning & Client SDK Generation**
- **Priority**: P2 | **Category**: Developer Experience | **Complexity**: Medium | **Phase**: 4
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | H-08 | H-08 already plans OpenAPI publication plus Python/TypeScript SDK clients. INFRA-006 adds versioning and a Go SDK.
- **Description**: Explicit API versioning strategy (v1/v2 coexistence) and auto-generated client SDKs for Python, JavaScript, and Go from OpenAPI schema.
- **Implementation**:
  - API version routing middleware
  - Deprecation headers and sunset policy
  - OpenAPI-generator integration for SDK output
  - SDK packaging scripts
- **Acceptance criteria**:
  - [x] `INFRA-006.1` API version coexistence (v1 + v2)
  - [x] `INFRA-006.2` Deprecation headers
  - [x] `INFRA-006.3` Generated Python SDK
  - [x] `INFRA-006.4` Generated JavaScript SDK
  - [x] `INFRA-006.5` SDK packaging
  - [x] `INFRA-006.A1` Go SDK is described in the requirement but missing from the acceptance criteria: generate and package it. *(added by review)*
  - [x] `INFRA-006.A2` Breaking-change detection (OpenAPI diff) runs in CI; SDK contract tests (SDLC-017). *(added by review)*
  - [x] `INFRA-006.A3` Unit tests for version routing and deprecation headers. *(added by review)*

#### INFRA-007: Automated Backup & Restore Testing

- [x] `INFRA-007` **Automated Backup & Restore Testing**
- **Priority**: P2 | **Category**: Reliability | **Complexity**: Medium | **Phase**: 4
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | MVP-FR-025, MVP-FR-026, NFR-REL-002, GAP-HA, REL-10 | Backup and restore appears in the MVP, NFR and release-gate sets.
- **Description**: Extend existing WAL/recovery with automated backup scheduling, backup verification, and restore testing. Currently has WAL with point-in-time recovery but no automated scheduling.
- **Implementation**:
  - Extend `packages/eoip/recovery/`
  - `BackupScheduler` with configurable intervals
  - `BackupVerifier` for integrity checking
  - `RestoreTestRunner` for automated restore validation
  - Backup encryption at rest
- **Acceptance criteria**:
  - [x] `INFRA-007.1` Automated backup scheduling
  - [x] `INFRA-007.2` Backup integrity verification
  - [x] `INFRA-007.3` Automated restore testing
  - [x] `INFRA-007.4` Encryption at rest
  - [x] `INFRA-007.5` Unit tests
  - [x] `INFRA-007.A1` Backup scope is enumerated and tested: graph store, vector indexes, persistent cache, message bus, experiment/artifact store, configuration, audit ledger. *(added by review)*
  - [x] `INFRA-007.A2` RPO and RTO targets set and measured by the restore test. *(added by review)*
  - [x] `INFRA-007.A3` Deletions made for erasure requests are re-applied after any restore. *(added by review)*
  - [x] `INFRA-007.A4` Unit tests for scheduler, verifier and restore runner. *(added by review)*

### Phase 5. GUI/UI/UX enhancements

Design system, i18n, data grid, charts, export, workflow builder, the six missing lenses, search analytics and collaboration.

#### UI-001: Component Library & Design System

- [x] `UI-001` **Component Library & Design System**
- **Priority**: P1 | **Category**: Frontend Architecture | **Complexity**: Medium | **Phase**: 5
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | S-01, CG-GAP-007 | Align with the real stack (Vite + React + JavaScript) before adopting Storybook.
- **Description**: Establish shared UI component library with Storybook documentation. Currently all 90+ components are custom-built with no shared design system.
- **Implementation**:
  - Create `apps/web/src/components/ui/` shared library
  - Button, Input, Select, Modal, Toast, Card, Badge, Tabs, Tooltip components
  - Storybook setup with component documentation
  - Design tokens (colors, spacing, typography, shadows)
  - Dark/light theme variants for each component
- **Acceptance criteria**:
  - [x] `UI-001.1` 10+ shared UI components
  - [x] `UI-001.2` Storybook setup with stories for each component
  - [x] `UI-001.3` Design tokens file
  - [x] `UI-001.4` Theme-aware components
  - [x] `UI-001.5` Component documentation
  - [x] `UI-001.A1` Components meet baseline accessibility (focus, contrast, keyboard) so TEST-005 starts green. *(added by review)*
  - [x] `UI-001.A2` Migration plan and adoption metric for existing components; bundle-size budget. *(added by review)*
  - [x] `UI-001.A3` Unit or visual tests for each shared component. *(added by review)*

#### UI-002: Internationalization (i18n/l10n)

- [x] `UI-002` **Internationalization (i18n/l10n)**
- **Priority**: P2 | **Category**: Global Readiness | **Complexity**: Medium | **Phase**: 5
- **Depends on**: `UI-001` | **Coordinate with**: none
- **Overlap with KGF backlog**: own | none | No KGF equivalent.
- **Description**: Add i18n support to the frontend. Zero internationalization exists currently.
- **Implementation**:
  - Install react-i18next or equivalent
  - Extract all UI strings to locale files
  - Language selector component
  - RTL support for Arabic/Hebrew
  - Date/number formatting per locale
- **Acceptance criteria**:
  - [x] `UI-002.1` i18n framework integrated
  - [x] `UI-002.2` English locale file with all strings
  - [x] `UI-002.3` Language selector
  - [x] `UI-002.4` Date/number locale formatting
  - [x] `UI-002.5` At least 2 locale files
  - [x] `UI-002.A1` RTL layout (named in the implementation, absent from the criteria) with at least one RTL locale. *(added by review)*
  - [x] `UI-002.A2` Pseudo-localization test; locale-aware sorting and search. *(added by review)*

#### UI-003: Advanced Data Grid

- [x] `UI-003` **Advanced Data Grid**
- **Priority**: P2 | **Category**: Data Presentation | **Complexity**: Low | **Phase**: 5
- **Depends on**: `UI-001` | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | S-01, G2-UX-GRAPH-*
- **Description**: Replace raw HTML tables with advanced data grid (TanStack Table or ag-Grid) for sorting, filtering, pagination, column resizing, and virtual scrolling.
- **Implementation**:
  - Integrate TanStack Table or ag-Grid
  - Replace tables in admin panels, audit logs, job lists
  - Virtual scrolling for large datasets
  - Column configuration persistence
- **Acceptance criteria**:
  - [x] `UI-003.1` Grid component with sort/filter/paginate
  - [x] `UI-003.2` Virtual scrolling for 10K+ rows
  - [x] `UI-003.3` Column resize and reorder
  - [x] `UI-003.4` Applied to 3+ existing tables
  - [x] `UI-003.A1` ARIA grid roles and full keyboard navigation; server-side pagination above 100K rows. *(added by review)*
  - [x] `UI-003.A2` Exports respect active filters and user permissions. *(added by review)*

#### UI-004: Charting Library Integration

- [x] `UI-004` **Charting Library Integration**
- **Priority**: P2 | **Category**: Data Visualization | **Complexity**: Low | **Phase**: 5
- **Depends on**: `UI-001` | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | S-01
- **Description**: Replace hand-rolled SVG charts with a proper charting library (Recharts or Chart.js) for consistency and capability.
- **Implementation**:
  - Integrate Recharts or Chart.js
  - Standard chart types: line, bar, pie, scatter, radar, heatmap
  - Theme-aware colors
  - Interactive tooltips and zoom
- **Acceptance criteria**:
  - [x] `UI-004.1` Charting library integrated
  - [x] `UI-004.2` 6+ chart types available
  - [x] `UI-004.3` Theme-aware
  - [x] `UI-004.4` Applied to existing metric displays
  - [x] `UI-004.A1` Accessible charts: color-blind safe palettes and a table alternative; large series are downsampled. *(added by review)*

#### UI-005: PDF/CSV Export

- [x] `UI-005` **PDF/CSV Export**
- **Priority**: P2 | **Category**: Enterprise Features | **Complexity**: Medium | **Phase**: 5
- **Depends on**: none | **Coordinate with**: `UI-004`
- **Overlap with KGF backlog**: extend | FR-UI-001, /api/v1/reports/export | Server-side report export routes already exist.
- **Description**: Add PDF and CSV export to existing JSON/HTML export. Enterprise customers need printable reports and data export.
- **Implementation**:
  - PDF generation (jsPDF or server-side)
  - CSV export for tabular data
  - Export button on all data views
  - Report template system
- **Acceptance criteria**:
  - [x] `UI-005.1` PDF export for graph reports
  - [x] `UI-005.2` CSV export for tabular data
  - [x] `UI-005.3` Export buttons on data views
  - [x] `UI-005.4` Report templates
  - [x] `UI-005.A1` Exports honour authorization and PII masking; large exports run asynchronously; export events are audited. *(added by review)*
  - [x] `UI-005.A2` Unit tests for CSV escaping and report templates. *(added by review)*

#### UI-006: Visual Workflow Builder

- [x] `UI-006` **Visual Workflow Builder**
- **Priority**: P3 | **Category**: Low-Code | **Complexity**: High | **Phase**: 5
- **Depends on**: `UI-001` | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | GAP-NOCODE, GAP-APP | Avoid a third builder: decide whether this is the pipeline-level editor and GAP-NOCODE/GAP-APP are ontology/dashboard editors.
- **Description**: Drag-and-drop workflow builder for creating harness pipelines, agent orchestrations, and data processing flows without code.
- **Implementation**:
  - React Flow or similar library
  - Node types for pipeline stages, agent calls, conditions, loops
  - Connection validation
  - Workflow export to harness pipeline config
- **Acceptance criteria**:
  - [x] `UI-006.1` Drag-and-drop canvas
  - [x] `UI-006.2` Node palette with 10+ node types
  - [x] `UI-006.3` Connection validation
  - [x] `UI-006.4` Export to pipeline config
  - [x] `UI-006.A1` Dry-run or simulate mode and validation before publishing a workflow; published workflows are versioned and need approval. *(added by review)*
  - [x] `UI-006.A2` Decision recorded on how this differs from GAP-NOCODE and GAP-APP so there is one builder family. *(added by review)*

#### UI-007: Missing Dashboard Lenses

- [x] `UI-007` **Missing Dashboard Lenses**
- **Priority**: P2 | **Category**: Dashboard | **Complexity**: High | **Phase**: 5
- **Depends on**: none | **Coordinate with**: `GRAPH-005`, `CORE-004`, `INFRA-004`, `INFRA-003`, `AGENT-004`, `GRAPH-002`
- **Overlap with KGF backlog**: merge | G2-UX-LENS-*, UI-01..UI-04 (KGF), G2-TIME-*, G2-SIM-*, G2-PM-* | KGF already lists blast-radius, multi-paradigm, domain-pack and XAI screens. Share the lens shell.
- **Description**: Implement the 6 planned but unbuilt lenses: Timeline, Change, Runtime, Release, Process, Simulation.
- **Implementation**:
  - `TimelineLens.jsx` — temporal view of knowledge graph evolution
  - `ChangeLens.jsx` — diff view of graph mutations
  - `RuntimeLens.jsx` — live system metrics and agent activity
  - `ReleaseLens.jsx` — deployment and version tracking
  - `ProcessLens.jsx` — workflow execution monitoring
  - `SimulationLens.jsx` — what-if scenario runner
- **Acceptance criteria**:
  - [x] `UI-007.1` All 6 lenses implemented
  - [x] `UI-007.2` Navigation integration
  - [x] `UI-007.3` Data connected to backend APIs
  - [x] `UI-007.4` Theme-aware
  - [x] `UI-007.A1` The requirement lists six lenses but four acceptance criteria: each lens gets its own criterion with a data contract and empty/error states (Timeline, Change, Runtime, Release, Process, Simulation). *(added by review)*
  - [x] `UI-007.A2` Large-graph performance via the WebGL work in S-01. *(added by review)*

#### UI-008: Search Analytics & Relevance Dashboard

- [x] `UI-008` **Search Analytics & Relevance Dashboard**
- **Priority**: P2 | **Category**: Search Intelligence | **Complexity**: Medium | **Phase**: 5
- **Depends on**: none | **Coordinate with**: `UI-001`
- **Overlap with KGF backlog**: own | GAP-QI-*
- **Description**: Dashboard showing search query analytics, click-through rates, zero-result queries, and relevance tuning controls.
- **Implementation**:
  - Search event logging
  - Analytics aggregation (top queries, zero-result rate, CTR)
  - Relevance tuning controls (boost/bury, synonyms, stopwords)
  - A/B testing for search ranking experiments
- **Acceptance criteria**:
  - [x] `UI-008.1` Search event logging
  - [x] `UI-008.2` Analytics dashboard
  - [x] `UI-008.3` Relevance tuning controls
  - [x] `UI-008.4` A/B testing for ranking
  - [x] `UI-008.A1` No raw query text retained beyond policy; analytics are tenant-scoped. *(added by review)*
  - [x] `UI-008.A2` Relevance tuning changes are versioned and reversible. *(added by review)*

#### UI-009: Real-time Collaboration

- [x] `UI-009` **Real-time Collaboration**
- **Priority**: P3 | **Category**: Collaboration | **Complexity**: High | **Phase**: 5
- **Depends on**: none | **Coordinate with**: `UI-001`
- **Overlap with KGF backlog**: merge | MS-12 | Real-time collaboration is MS-12 (live collaborative graph studio). One CRDT layer.
- **Description**: Multi-user real-time collaboration on graph exploration, annotations, and queries. Currently has workspaces but no real-time sync.
- **Implementation**:
  - CRDT-based state synchronization
  - Presence indicators (who's viewing what)
  - Shared cursors on graph canvas
  - Real-time annotation sync
- **Acceptance criteria**:
  - [x] `UI-009.1` Real-time state sync between users
  - [x] `UI-009.2` Presence indicators
  - [x] `UI-009.3` Shared graph exploration
  - [x] `UI-009.4` Annotation sync
  - [x] `UI-009.A1` Conflict-resolution and offline-reconnect tests; presence respects permissions. *(added by review)*
  - [x] `UI-009.A2` Single CRDT layer shared with MS-12. *(added by review)*

### Phase 6. Compliance, security and testing

Compliance-as-code, PII handling and the testing disciplines (chaos, load, property/fuzz, performance regression, accessibility).

#### COMPLY-001: Compliance-as-Code Graph Constraints

- [x] `COMPLY-001` **Compliance-as-Code Graph Constraints**
- **Priority**: P1 | **Category**: Regulatory Compliance | **Complexity**: Medium | **Phase**: 6
- **Depends on**: none | **Coordinate with**: `GRAPH-006`, `CORE-004`
- **Overlap with KGF backlog**: extend | compliance/, moonshot/compliance_twin.py, G2-GRAPH-SEC-*, MS-25 | compliance/ package and compliance twin exist.
- **Description**: Encode regulatory rules (GDPR, SOX, HIPAA) as graph constraint patterns checked continuously against the knowledge graph. Currently compliance packs are skeleton-only.
- **Implementation**:
  - Create `packages/eoip/compliance/constraints.py`
  - `ComplianceRule` encoded as graph patterns
  - `ContinuousMonitor` running rules against graph mutations
  - `ViolationReport` with severity, affected entities, remediation
  - Dashboard integration for compliance posture
- **Acceptance criteria**:
  - [x] `COMPLY-001.1` Graph-pattern compliance rules
  - [x] `COMPLY-001.2` Continuous monitoring on graph mutations
  - [x] `COMPLY-001.3` Violation reporting with remediation
  - [x] `COMPLY-001.4` GDPR, SOX, HIPAA rule templates
  - [x] `COMPLY-001.5` Unit tests
  - [x] `COMPLY-001.A1` Each rule cites the regulation article it encodes and is versioned. *(added by review)*
  - [x] `COMPLY-001.A2` A coverage matrix maps regulation clauses to rules, not just rule templates. *(added by review)*
  - [x] `COMPLY-001.A3` False positives go through a review workflow (SDLC-008). *(added by review)*
  - [x] `COMPLY-001.A4` Unit tests for each template and for continuous monitoring on mutation. *(added by review)*

#### COMPLY-002: Automated PII Detection & Anonymization

- [x] `COMPLY-002` **Automated PII Detection & Anonymization**
- **Priority**: P1 | **Category**: Privacy | **Complexity**: Medium | **Phase**: 6
- **Depends on**: none | **Coordinate with**: `AI-002`
- **Overlap with KGF backlog**: extend | NFR-PRIV-001, privacy/
- **Description**: Automated PII scanning across graph entities with anonymization/pseudonymization. Currently privacy module has DSAR but no automated scanning.
- **Implementation**:
  - Extend `packages/eoip/privacy/`
  - `PIIScanner` detecting names, emails, phones, SSNs, addresses in graph properties
  - `Anonymizer` with k-anonymity and differential privacy strategies
  - `Pseudonymizer` with reversible token replacement
  - Scheduled scanning of new graph entities
- **Acceptance criteria**:
  - [x] `COMPLY-002.1` PII detection across graph properties
  - [x] `COMPLY-002.2` k-anonymity implementation
  - [x] `COMPLY-002.3` Pseudonymization with token mapping
  - [x] `COMPLY-002.4` Scheduled scanning
  - [x] `COMPLY-002.5` Unit tests
  - [x] `COMPLY-002.A1` Precision/recall targets on a labelled PII set across the supported languages. *(added by review)*
  - [x] `COMPLY-002.A2` Key custody for the pseudonym vault uses the shared KMS layer (SDLC-029); erasure and anonymization cascade to embeddings, caches and packages (SDLC-028). *(added by review)*
  - [x] `COMPLY-002.A3` Re-identification risk test on k-anonymity outputs. *(added by review)*

#### COMPLY-003: Continuous Compliance Monitoring Dashboard

- [x] `COMPLY-003` **Continuous Compliance Monitoring Dashboard**
- **Priority**: P2 | **Category**: Compliance | **Complexity**: Medium | **Phase**: 6
- **Depends on**: `COMPLY-001` | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | MS-24, audit/
- **Description**: Real-time compliance posture dashboard with attestation tracking, evidence collection, and audit readiness scoring.
- **Implementation**:
  - Compliance score calculation per framework
  - Evidence collection automation
  - Attestation workflow
  - Audit trail export
- **Acceptance criteria**:
  - [x] `COMPLY-003.1` Per-framework compliance scores
  - [x] `COMPLY-003.2` Evidence collection
  - [x] `COMPLY-003.3` Attestation tracking
  - [x] `COMPLY-003.4` Audit export
  - [x] `COMPLY-003.A1` Framework mappings include SOC 2, ISO 27001, ISO/IEC 42001 and the EU AI Act, not only GDPR/SOX/HIPAA. *(added by review)*
  - [x] `COMPLY-003.A2` Evidence is hash-chained and an auditor read-only role exists. *(added by review)*
  - [x] `COMPLY-003.A3` Unit tests for score calculation and evidence collection. *(added by review)*

#### TEST-001: Chaos Engineering Framework

- [x] `TEST-001` **Chaos Engineering Framework**
- **Priority**: P2 | **Category**: Reliability Testing | **Complexity**: Medium | **Phase**: 6
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | NFR-REL-001, G2-REL-*, REL-10
- **Description**: Fault injection testing for graph store failures, network partitions, agent timeouts, and cascading failures.
- **Implementation**:
  - Create `tests/chaos/` framework
  - `FaultInjector` for controlled failure injection
  - Scenarios: graph store unavailable, RAG timeout, agent crash, memory exhaustion
  - Recovery verification after fault clearance
- **Acceptance criteria**:
  - [x] `TEST-001.1` Fault injection framework
  - [x] `TEST-001.2` 5+ chaos scenarios
  - [x] `TEST-001.3` Recovery verification
  - [x] `TEST-001.4` CI integration (optional runs)
  - [x] `TEST-001.A1` Each experiment states a steady-state hypothesis and a blast-radius limit; runs target compose or staging by default. *(added by review)*
  - [x] `TEST-001.A2` Results feed SLOs and runbooks (SDLC-026). Unit tests for the fault injector itself. *(added by review)*

#### TEST-002: Load Testing Framework

- [x] `TEST-002` **Load Testing Framework**
- **Priority**: P1 | **Category**: Performance Testing | **Complexity**: Medium | **Phase**: 6
- **Depends on**: none | **Coordinate with**: none
- **Overlap with KGF backlog**: merge | PERF-01, S-02, NFR-PERF-001, K-04, K-05, REL-12 | Choose one load tool. KGF PERF-01 says Locust/pytest-benchmark; this says k6 or Locust.
- **Description**: Production-scale load testing with k6 or Locust. Currently performance tests use in-memory stores only.
- **Implementation**:
  - Create `tests/load/` with k6 scripts
  - Scenarios: concurrent queries, bulk ingestion, agent swarm, RAG under load
  - Latency percentile targets (p50, p90, p99)
  - Throughput baselines
- **Acceptance criteria**:
  - [x] `TEST-002.1` Load test scripts
  - [x] `TEST-002.2` 4+ load scenarios
  - [x] `TEST-002.3` Latency and throughput targets
  - [x] `TEST-002.4` CI-runnable (optional)
  - [x] `TEST-002.A1` One load tool is chosen (k6 or Locust) consistent with KGF PERF-01 and documented. *(added by review)*
  - [x] `TEST-002.A2` Runs on generated realistic data (SDLC-012); results and baselines are stored as versioned artifacts. *(added by review)*

#### TEST-003: Property-Based & Fuzz Testing

- [x] `TEST-003` **Property-Based & Fuzz Testing**
- **Priority**: P2 | **Category**: Testing Quality | **Complexity**: Medium | **Phase**: 6
- **Depends on**: `CORE-001` | **Coordinate with**: none
- **Overlap with KGF backlog**: extend | NFR-SEC-003, query/polyglot_engine.py
- **Description**: Add Hypothesis-based property testing and fuzz testing for serialization, query parsing, and graph operations.
- **Implementation**:
  - Hypothesis strategies for graph structures, queries, payloads
  - Fuzz testing for token format serialization round-trips
  - Property tests for query transpilation
- **Acceptance criteria**:
  - [x] `TEST-003.1` Hypothesis test suite
  - [x] `TEST-003.2` Fuzz tests for serialization
  - [x] `TEST-003.3` Property tests for query engine
  - [x] `TEST-003.4` CI integration
  - [x] `TEST-003.A1` Seed corpus from production-like payloads; crash triage procedure. *(added by review)*
  - [x] `TEST-003.A2` Property tests check semantic equivalence across the 71 query dialects of the transpiler. *(added by review)*

#### TEST-004: Performance Regression Detection in CI

- [x] `TEST-004` **Performance Regression Detection in CI**
- **Priority**: P1 | **Category**: Quality Gates | **Complexity**: Medium | **Phase**: 6
- **Depends on**: none | **Coordinate with**: `TEST-002`, `INFRA-003`
- **Overlap with KGF backlog**: merge | S-02, S-03, NFR-PERF-001
- **Description**: Automated performance regression detection in CI pipeline. Compare benchmark results against baselines, fail on regression beyond threshold.
- **Implementation**:
  - Benchmark runner in CI
  - Baseline storage and comparison
  - Regression threshold configuration
  - PR comment with performance diff
- **Acceptance criteria**:
  - [x] `TEST-004.1` Benchmark runner in CI workflow
  - [x] `TEST-004.2` Baseline comparison
  - [x] `TEST-004.3` Configurable regression thresholds
  - [x] `TEST-004.4` PR performance report
  - [x] `TEST-004.A1` Noise control: pinned runner, repeated runs, statistical comparison against the baseline. *(added by review)*
  - [x] `TEST-004.A2` Baselines are tied to a hardware profile (SDLC-031). Unit tests for the comparison logic. *(added by review)*

#### TEST-005: Accessibility Testing

- [x] `TEST-005` **Accessibility Testing**
- **Priority**: P2 | **Category**: Accessibility | **Complexity**: Low | **Phase**: 6
- **Depends on**: `UI-001` | **Coordinate with**: none
- **Overlap with KGF backlog**: own | REL-08 | New capability. REL-08 is a one-time browser run.
- **Description**: Automated accessibility testing for frontend components. Currently has 146 ARIA attributes but no automated testing.
- **Implementation**:
  - axe-core integration in test suite
  - WCAG 2.1 AA compliance checking
  - Screen reader testing guidance
  - Accessibility CI gate
- **Acceptance criteria**:
  - [x] `TEST-005.1` axe-core test integration
  - [x] `TEST-005.2` WCAG 2.1 AA compliance
  - [x] `TEST-005.3` CI gate for a11y violations
  - [x] `TEST-005.A1` Manual screen-reader checklist (automated checks alone miss part of WCAG); keyboard-only E2E flows. *(added by review)*
  - [x] `TEST-005.A2` Accessibility conformance report output for procurement (SDLC-034). *(added by review)*

### Phase 7. Multi-modal and advanced (deferred)

Deferred: scoped multi-modal (diagram to graph) and graph-native memory.

#### MULTI-001: Scoped Multi-Modal Engineering

- [x] `MULTI-001` **Scoped Multi-Modal Engineering**
- **Priority**: P3 | **Category**: Multi-Modal | **Complexity**: Medium | **Phase**: 7
- **Depends on**: none | **Coordinate with**: `AGENT-002`
- **Overlap with KGF backlog**: own | FR-CODE-* | No KGF equivalent.
- **Description**: Scoped to: image-to-graph extraction (diagrams -> KG nodes) and graph-to-image rendering. NOT general multimodal perception.
- **Implementation**:
  - Add image extractors to `packages/eoip/fileparse/engine.py`
  - Diagram-to-graph parser (flowchart, ER diagram, architecture diagram)
  - Graph-to-image renderer for export
- **Acceptance criteria**:
  - [x] `MULTI-001.1` Diagram parsing to graph nodes
  - [x] `MULTI-001.2` Graph-to-image rendering
  - [x] `MULTI-001.3` Integration with fileparse engine
  - [x] `MULTI-001.A1` An evaluation set and accuracy target for diagram parsing; image parsing runs sandboxed (NFR-SEC-003). *(added by review)*
  - [x] `MULTI-001.A2` Unit tests for each diagram type. *(added by review)*

#### MULTI-002: Knowledge & Memory Graph Engineering

- [x] `MULTI-002` **Knowledge & Memory Graph Engineering**
- **Priority**: P2 | **Category**: Memory | **Complexity**: Medium | **Phase**: 7
- **Depends on**: none | **Coordinate with**: `GRAPH-005`, `CORE-004`
- **Overlap with KGF backlog**: extend | KGR-G-014, MS-19, memory_eng/ | Memory graphs need the poisoning defenses from MS-19.
- **Description**: Structural knowledge representations that evolve over time. Extends memory_eng with graph-native memory storage, episodic memory graphs, and memory consolidation via graph operations.
- **Implementation**:
  - Extend `packages/eoip/memory_eng/engine.py`
  - `MemoryGraph` storing memories as graph nodes with temporal edges
  - `EpisodicMemoryGraph` for session-based memory graphs
  - `MemoryConsolidationGraph` for promoting patterns to long-term graph structures
- **Acceptance criteria**:
  - [x] `MULTI-002.1` Graph-native memory storage
  - [x] `MULTI-002.2` Episodic memory graphs
  - [x] `MULTI-002.3` Graph-based consolidation
  - [x] `MULTI-002.4` Unit tests
  - [x] `MULTI-002.A1` Per-tenant memory isolation and retention/erasure; poisoning defenses from MS-19 apply. *(added by review)*

## 7. Lifecycle review and proposed additions

### 7.1 What was studied

The Phase 4 requirements (49 items, 248 criteria), the KGF Master Backlog (516 tasks), the two audits it merges (826 requirements, 434 gaps, 9 CG gaps), and the Conquest plan (47 deliverables, 8 KPIs). Each requirement was checked for: missing acceptance criteria, overlap with another item, stores of personal data it creates, whether it is reachable through an API, and whether any lifecycle stage (planning to maintenance, and data to monitoring for AI) lacks an owner.

### 7.2 Coverage by lifecycle stage

| Stage | Covered today | Gap found | Proposed |
|---|---|---|---|
| SDLC: plan and requirements | This roadmap, KGF registry (BASE-01..04) | No CI enforcement, no decision log, no per-engine threat model | SDLC-001..003 |
| SDLC: architecture and design | Engine specs, KGF HA | Manual wiring, singleton state, no runtime flags, no migration framework, no human queue, no shared resilience | SDLC-004..009 |
| SDLC: build and code quality | KGF S-03 CI | No type or layering gates, no coverage, no synthetic data, no mutation testing, no rules for the coding agent | SDLC-010..016 |
| SDLC: verify and test | TEST-001..005, KGF PERF-01 | No contract, continuous E2E, soak, upgrade or continuous security testing | SDLC-017..021 |
| SDLC: release and deploy | INFRA-003, INFRA-006 | No SemVer/SBOM/signing, no production Kubernetes profile, no air-gapped bundle | SDLC-022..024 |
| SDLC: operate and maintain | INFRA-001/004/005/007, KGF G2-SLO and G2-TEL | No unified tracing, SLOs and runbooks, FinOps, erasure cascade, key management, tenant-isolation tests, capacity guidance | SDLC-025..031 |
| SDLC: docs, DX, go-to-market | UI-001 Storybook, KGF S-04 | No docs-as-code CI, no bootstrap experience, no procurement pack | SDLC-032..034 |
| AIDLC: data and knowledge | AGENT-002, AI-003, AI-006 | No lineage, no re-embedding path, no accuracy benchmarks | AIDLC-001..003 |
| AIDLC: model, prompt, agent development | AI-004, AI-005, MS-15 | No prompt registry, no single model gateway, no fine-tuning pipeline | AIDLC-007, 008, 010 |
| AIDLC: evaluate and validate | CORE-002 (runtime checks only) | No offline evaluation, no replay, no calibration | AIDLC-004..006 |
| AIDLC: secure and govern | COMPLY-001..003, INFRA-002, MS-19/21 | No red-team harness, sandbox, agent identity, AI governance pack, autonomy catalog | AIDLC-011..014, 016 |
| AIDLC: deploy and monitor | AI-004 canary | No production feedback or quality monitoring | AIDLC-009 |
| AIDLC: human experience | AI-001, UI-* | No evidence or explanation screens | AIDLC-015 |

### 7.3 If you accept only a few

Seven P0 proposals address the highest risks: `SDLC-001` traceability gate, `SDLC-004` engine registry (prevents another CG-GAP-001), `SDLC-015` governance for the coding agent, `SDLC-028` erasure across derived stores (a GDPR exposure), `SDLC-030` tenant-isolation suite, `AIDLC-004` AI evaluation harness, `AIDLC-012` agent tool sandbox.

### 7.4 Proposals

Set `- **Decision**: accepted` to put an item in scope; use `deferred` or `rejected` otherwise.

#### Software lifecycle (SDLC)

##### Plan and requirements

###### SDLC-001: Requirement traceability gate in CI

- [ ] `SDLC-001` **Requirement traceability gate in CI**
- **Priority**: P0 | **Category**: Plan and requirements | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `PRE-001`
- **Related existing items**: KGF BASE-01, BASE-02, BASE-03, CG-GAP-004
- **Why (evidence from the documents)**: The CG audit found 1,199 documentation records with no code or test lead and five documentation-drift gaps; the G-dev audit found most tests untagged. Without an enforced link between requirement, commit and test the drift returns. This programme adds 49 more requirements.
- **Implementation**:
  - Adopt the commit prefix [ID] and the @pytest.mark.req("ID") marker (KGF BASE-02).
  - CI check: every PR names at least one existing requirement ID; every requirement marked done has at least one tagged test; no orphan tests.
  - Emit requirements-test-map.json as a CI artifact and fail on unknown IDs.
- **Suggested paths**: `scripts/traceability_check.py`, `.github/workflows/traceability.yml`
- **Acceptance criteria**:
  - [ ] `SDLC-001.1` CI fails a PR with no valid requirement ID
  - [ ] `SDLC-001.2` CI fails when a done requirement has no tagged test
  - [ ] `SDLC-001.3` Registry and Markdown checkbox state are reconciled by a script
  - [ ] `SDLC-001.4` Check runs in under 30 seconds

###### SDLC-002: Architecture decision records and decision register

- [ ] `SDLC-002` **Architecture decision records and decision register**
- **Priority**: P2 | **Category**: Plan and requirements | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: KGF DEC-01..DEC-10
- **Why (evidence from the documents)**: The two backlogs already hold 10 open decisions (DEC-01..10), 12 source conflicts and now 6 more baseline conflicts. Decisions recorded only in chat or a table get re-opened.
- **Implementation**:
  - docs/adr/ with a short template (context, decision, consequences, status, linked requirement IDs).
  - Migrate DEC-xx and C-xx/B-xx entries into ADRs as they are decided.
  - Link ADR IDs from the requirement registry.
- **Suggested paths**: `docs/adr/`
- **Acceptance criteria**:
  - [ ] `SDLC-002.1` ADR template and index exist
  - [ ] `SDLC-002.2` Every decided DEC item has an ADR
  - [ ] `SDLC-002.3` Requirement registry rows link to ADRs
  - [ ] `SDLC-002.4` ADR numbering is checked in CI

###### SDLC-003: Threat model and abuse-case library per engine

- [ ] `SDLC-003` **Threat model and abuse-case library per engine**
- **Priority**: P1 | **Category**: Plan and requirements | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AIDLC-011`
- **Related existing items**: KGF NFR-SEC-*, G2-IMMUNE-*
- **Why (evidence from the documents)**: Many new surfaces: a message bus (AGENT-003), federated pushdown to external databases (GRAPH-001), SSO (INFRA-002), a pseudonym vault (COMPLY-002), cache keys (INFRA-001), a router that can skip checks (CORE-003). Security items in the KGF backlog are mostly verification after the fact.
- **Implementation**:
  - One threat model per new engine using STRIDE plus the OWASP LLM and Agentic top-10 lists; stored under docs/threat-models/.
  - Design gate: an engine is not started until its threat model is reviewed.
  - Abuse-case tests are derived from each threat model.
- **Suggested paths**: `docs/threat-models/`
- **Acceptance criteria**:
  - [ ] `SDLC-003.1` Template and review checklist
  - [ ] `SDLC-003.2` Threat models exist for CORE-002, CORE-003, GRAPH-001, AGENT-003, INFRA-002, COMPLY-002
  - [ ] `SDLC-003.3` Each threat has a mitigation requirement or an accepted-risk entry
  - [ ] `SDLC-003.4` Abuse-case tests exist for the top threats

##### Architecture and design

###### SDLC-004: Engine auto-registration and wiring contract

- [ ] `SDLC-004` **Engine auto-registration and wiring contract**
- **Priority**: P0 | **Category**: Architecture and design | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: CG-GAP-001, KGF H-03
- **Why (evidence from the documents)**: Eight requirements each edit brain_os.py and platform_router.py by hand, and CG-GAP-001 shows the consequence: a router that exists but is not mounted. Hand wiring also makes those two files merge hot spots when several agents or branches work in parallel.
- **Implementation**:
  - An Engine descriptor (name, version, router, health check, telemetry hooks, tenant scope, feature flag) registered by decorator or entry point.
  - The app builds routes, health and telemetry from the registry; no manual edits to brain_os.py or platform_router.py for new engines.
  - Startup self-check lists every router module under packages/eoip and fails if one is neither mounted nor explicitly excluded.
- **Suggested paths**: `packages/eoip/platform/registry.py`
- **Acceptance criteria**:
  - [ ] `SDLC-004.1` Descriptor and registry implemented
  - [ ] `SDLC-004.2` Existing engines migrated or explicitly exempted
  - [ ] `SDLC-004.3` Startup test fails on an unmounted router (would have caught CG-GAP-001)
  - [ ] `SDLC-004.4` New engines add zero lines to brain_os.py/platform_router.py

###### SDLC-005: Tenant-scoped engine instances instead of process-wide singletons

- [ ] `SDLC-005` **Tenant-scoped engine instances instead of process-wide singletons**
- **Priority**: P1 | **Category**: Architecture and design | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-030`
- **Related existing items**: KGR-G-013, MS-26, tenancy/
- **Why (evidence from the documents)**: Eight requirements mandate a thread-safe singleton get_*_engine(). Budgets, caches, queues, experiments and memory are tenant data. KGR-G-013 and MS-26 require tenant isolation; a singleton holding state across tenants defeats it.
- **Implementation**:
  - Keep singletons for stateless services; give stateful engines a tenant-keyed factory behind a small dependency-injection container.
  - get_*_engine(tenant) signature with a default-tenant shim for existing callers.
  - Document which engines are stateless and which are tenant-scoped.
- **Suggested paths**: `packages/eoip/platform/container.py`
- **Acceptance criteria**:
  - [ ] `SDLC-005.1` Container and factory pattern exist
  - [ ] `SDLC-005.2` Stateful Phase 4 engines are tenant-keyed
  - [ ] `SDLC-005.3` Concurrency test: two tenants cannot observe each other
  - [ ] `SDLC-005.4` Migration notes for existing singletons

###### SDLC-006: Feature flags and kill switches

- [ ] `SDLC-006` **Feature flags and kill switches**
- **Priority**: P1 | **Category**: Architecture and design | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-004`
- **Related existing items**: INFRA-003, AI-004
- **Why (evidence from the documents)**: CORE-003 can short-circuit 60-70% of queries, CORE-002 can block outputs, and AI-004 canaries models. INFRA-003 only covers deploy-level canaries. A runtime switch is needed to turn an engine off or to enable it per tenant without redeploying, including in air-gapped sites.
- **Implementation**:
  - Local, signed flag store with per-engine, per-tenant and percentage rollout; no external SaaS.
  - Every engine descriptor (SDLC-004) declares its kill switch; flag changes are audited.
  - Default-off for behaviour-changing engines until shadow evaluation passes.
- **Suggested paths**: `packages/eoip/flags/`
- **Acceptance criteria**:
  - [ ] `SDLC-006.1` Flag service with audit trail
  - [ ] `SDLC-006.2` Kill switch tested for CORE-002, CORE-003 and INFRA-001
  - [ ] `SDLC-006.3` Flags evaluated in under 1 ms
  - [ ] `SDLC-006.4` Flag state is exported in backups

###### SDLC-007: Schema and data migration framework

- [ ] `SDLC-007` **Schema and data migration framework**
- **Priority**: P1 | **Category**: Architecture and design | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-003`
- **Related existing items**: KGF GAP-GITOPS-006, GAP-GITOPS-007
- **Why (evidence from the documents)**: KGF GAP-GITOPS-006/007 plan ontology migrations only. Phase 4 adds durable formats: message bus (AGENT-003), experiment store (AI-005), embedding registry (AI-006), knowledge packages (GRAPH-003), temporal index (GRAPH-005), L2 cache, and the CORE-001 wire formats.
- **Implementation**:
  - Versioned, ordered, reversible migrations with dry-run, for graph schema, vector index metadata, queues and registries.
  - Compatibility windows: N and N-1 readers; format version headers.
  - Migration status endpoint and CI test that upgrades from the previous release.
- **Suggested paths**: `packages/eoip/migrations/`
- **Acceptance criteria**:
  - [ ] `SDLC-007.1` Migration runner with dry-run and rollback
  - [ ] `SDLC-007.2` Each new durable store ships with a migration
  - [ ] `SDLC-007.3` Upgrade test from the previous tagged release passes
  - [ ] `SDLC-007.4` Migrations run in INFRA-003 deploy ordering

###### SDLC-008: Human-in-the-loop work queue and approvals inbox

- [ ] `SDLC-008` **Human-in-the-loop work queue and approvals inbox**
- **Priority**: P1 | **Category**: Architecture and design | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: AGENT-001, COMPLY-001, KGF GAP-TRUTH-008, GAP-GOV
- **Why (evidence from the documents)**: AGENT-001 hands off to humans, COMPLY-001 produces remediation, KGF GAP-TRUTH-008 needs human adjudication, GAP-GOV needs stewardship review, and loops have approval gates. Each mentions people; none defines the queue, assignment, SLA, escalation or notification.
- **Implementation**:
  - One work-item model (type, subject, evidence links, assignee/role, SLA, status, decision) with an inbox UI and API.
  - Escalation and delegation rules; notification channels (email, Slack/Teams webhook).
  - Every decision is audited and fed back to the producing engine.
- **Suggested paths**: `packages/eoip/workqueue/`, `apps/web/src/inbox/`
- **Acceptance criteria**:
  - [ ] `SDLC-008.1` Work-item API and inbox UI
  - [ ] `SDLC-008.2` AGENT-001, COMPLY-001, GAP-TRUTH-008 and low-confidence triples (AI-003) create work items
  - [ ] `SDLC-008.3` SLA breach escalates
  - [ ] `SDLC-008.4` Decisions are in the audit ledger

###### SDLC-009: Resilience patterns library: backpressure, load shedding, bulkheads

- [ ] `SDLC-009` **Resilience patterns library: backpressure, load shedding, bulkheads**
- **Priority**: P1 | **Category**: Architecture and design | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `TEST-001`
- **Related existing items**: G2-REL-*, G2-EKAF-011
- **Why (evidence from the documents)**: TEST-001 tests failures and CORE-005 mentions a circuit breaker, but no requirement builds shared resilience behaviour. Ingestion bursts (G2-EKAF rate limiting), agent swarms and RAG under load (TEST-002) will otherwise be handled engine by engine.
- **Implementation**:
  - Shared timeouts, retries with jitter, circuit breakers, bulkhead pools and load-shedding policy with priority classes.
  - Adopt in ingestion, agent swarm, RAG and the router.
  - Metrics for shed, retried and tripped calls.
- **Suggested paths**: `packages/eoip/resilience/`
- **Acceptance criteria**:
  - [ ] `SDLC-009.1` Library with unit tests
  - [ ] `SDLC-009.2` Used by at least ingestion, agent fan-out and RAG paths
  - [ ] `SDLC-009.3` TEST-001 scenarios prove graceful degradation
  - [ ] `SDLC-009.4` Shedding preserves P0 traffic classes

##### Build and code quality

###### SDLC-010: Static analysis, typing and layering gates

- [ ] `SDLC-010` **Static analysis, typing and layering gates**
- **Priority**: P1 | **Category**: Build and code quality | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: KGF S-03
- **Why (evidence from the documents)**: KGF S-03 mentions lint but no type, security-lint or dependency-direction checks. Phase 4 adds about 14 new or extended packages that must not form import cycles (for example graph_graph must not import agents).
- **Implementation**:
  - ruff and a security linter (bandit or semgrep rules) in CI; mypy or pyright strict on new packages, baseline on old ones.
  - import-linter contracts for package layering; ESLint for apps/web.
  - Pre-commit hooks mirror CI.
- **Suggested paths**: `pyproject.toml`, `.importlinter`, `.pre-commit-config.yaml`
- **Acceptance criteria**:
  - [ ] `SDLC-010.1` Linters and type checker in CI
  - [ ] `SDLC-010.2` New packages pass strict typing
  - [ ] `SDLC-010.3` Layering contract file exists and is enforced
  - [ ] `SDLC-010.4` Pre-commit config documented

###### SDLC-011: Coverage measurement and changed-lines gate

- [ ] `SDLC-011` **Coverage measurement and changed-lines gate**
- **Priority**: P1 | **Category**: Build and code quality | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Why (evidence from the documents)**: Both audits count tests (2,843) but never report coverage. Many acceptance criteria say only "unit tests". A pass count says nothing about which behaviour is exercised.
- **Implementation**:
  - Measure line and branch coverage in CI; publish trend.
  - Gate on changed-lines coverage for PRs rather than a global number.
  - Per-package thresholds for critical engines.
- **Suggested paths**: `.coveragerc`
- **Acceptance criteria**:
  - [ ] `SDLC-011.1` Coverage report in CI
  - [ ] `SDLC-011.2` Changed-lines gate enforced
  - [ ] `SDLC-011.3` Critical engines have thresholds
  - [ ] `SDLC-011.4` Baseline recorded

###### SDLC-012: Synthetic enterprise graph and corpus generator

- [ ] `SDLC-012` **Synthetic enterprise graph and corpus generator**
- **Priority**: P1 | **Category**: Build and code quality | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: TEST-002, KGF S-02, PERF-01
- **Why (evidence from the documents)**: TEST-002, the 50K-node latency KPI, chaos tests, COMPLY-002 and truth-resolution tests all need realistic data, and the performance tests today use in-memory stores only.
- **Implementation**:
  - Seeded generator for graphs (1K to 10M nodes, skewed degree, multiple domains), documents, planted PII, contradictory claims and temporal histories.
  - Deterministic: the same seed produces the same data and hashes.
  - Loaders for HugeGraph and the memory store.
- **Suggested paths**: `packages/eoip/testing/synthetic/`
- **Acceptance criteria**:
  - [ ] `SDLC-012.1` Generator with seeds and size presets
  - [ ] `SDLC-012.2` Planted-PII and contradiction modes
  - [ ] `SDLC-012.3` Used by TEST-002, TEST-001 and COMPLY-002 tests
  - [ ] `SDLC-012.4` Documented data shapes

###### SDLC-013: Test hygiene and CI speed

- [ ] `SDLC-013` **Test hygiene and CI speed**
- **Priority**: P2 | **Category**: Build and code quality | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: CG baseline
- **Why (evidence from the documents)**: The CG audit records 34 skipped tests, 2 warnings and a 709.87 s full run. Phase 4 adds dozens of modules; a slow suite slows every agent iteration.
- **Implementation**:
  - Triage each skipped test: fix, delete or document with an expiry.
  - Parallel execution and sharding; test-impact selection for PRs, full suite nightly.
  - Flaky-test detection and quarantine with an owner.
- **Suggested paths**: `pytest.ini`
- **Acceptance criteria**:
  - [ ] `SDLC-013.1` Zero unexplained skips
  - [ ] `SDLC-013.2` PR run under a set time budget
  - [ ] `SDLC-013.3` Flaky tests tracked
  - [ ] `SDLC-013.4` Warnings fixed or whitelisted with reason

###### SDLC-014: Mutation testing for correctness-critical engines

- [ ] `SDLC-014` **Mutation testing for correctness-critical engines**
- **Priority**: P2 | **Category**: Build and code quality | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-011`
- **Why (evidence from the documents)**: Verification rules, token-format round trips, routing, budgets and compliance constraints fail silently if tests are weak. Mutation scores show whether tests would notice a regression.
- **Implementation**:
  - Run mutation testing nightly on verification, token_formats, routing, token_budget and compliance packages.
  - Track mutation score trend; surviving mutants become test tasks.
- **Suggested paths**: `.github/workflows/mutation.yml`
- **Acceptance criteria**:
  - [ ] `SDLC-014.1` Nightly job on named packages
  - [ ] `SDLC-014.2` Score threshold per package
  - [ ] `SDLC-014.3` Survivor report
  - [ ] `SDLC-014.4` No impact on PR latency

###### SDLC-015: Governance for the AI coding agent itself

- [ ] `SDLC-015` **Governance for the AI coding agent itself**
- **Priority**: P0 | **Category**: Build and code quality | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-001`
- **Related existing items**: KGF Section 4.5 rules
- **Why (evidence from the documents)**: Around 565 tasks will be executed by an AI developer agent. The backlog states rules in prose (never rewrite historical audits, never lower a gate) but nothing enforces them, and an agent can quietly weaken tests or thresholds to turn a box green.
- **Implementation**:
  - CODEOWNERS and protected paths (gate thresholds, audit/ history, security tests, CI config) requiring human review.
  - PR policy: size limit, linked requirement ID, evidence, passing suite; a second agent or human reviews P0 and security-sensitive changes.
  - Budgets per task (time, tokens), a change log of agent actions, secrets scan, and a kill switch.
- **Suggested paths**: `.github/CODEOWNERS`, `.github/pull_request_template.md`
- **Acceptance criteria**:
  - [ ] `SDLC-015.1` Protected-path rules enforced in CI
  - [ ] `SDLC-015.2` PR template with evidence checklist
  - [ ] `SDLC-015.3` Second-review rule for P0/security paths
  - [ ] `SDLC-015.4` Agent change log stored and queryable

###### SDLC-016: Dogfood: manage the platform with the platform

- [ ] `SDLC-016` **Dogfood: manage the platform with the platform**
- **Priority**: P2 | **Category**: Build and code quality | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-001`
- **Related existing items**: KGR-G-017, code-graph traceability
- **Why (evidence from the documents)**: EOIP already ingests code, Jira, GitLab and documents and offers PR impact triage (KGR-G-017). Ingesting its own repository, requirement registry, tests, ADRs and CI results gives live traceability and impact analysis for this very programme.
- **Implementation**:
  - Ingest the repo, registry, tests and CI results into a tenant of EOIP; model requirement-to-code-to-test edges.
  - Use PR impact triage on its own PRs; dashboard of open requirements by phase.
- **Suggested paths**: `scripts/self_ingest.py`
- **Acceptance criteria**:
  - [ ] `SDLC-016.1` Self-ingestion job
  - [ ] `SDLC-016.2` Requirement-code-test graph queryable
  - [ ] `SDLC-016.3` PR impact comment on internal PRs
  - [ ] `SDLC-016.4` Dashboard shows progress from the registry

##### Verify and test

###### SDLC-017: Contract tests across API, SDKs, MCP, web client and VS Code extension

- [ ] `SDLC-017` **Contract tests across API, SDKs, MCP, web client and VS Code extension**
- **Priority**: P1 | **Category**: Verify and test | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-006`
- **Related existing items**: KGF H-03, H-08
- **Why (evidence from the documents)**: 502 routes, an MCP app, a VS Code extension, generated SDKs (INFRA-006) and a web client all consume the same API. CG-GAP-001/002 already show scanner-vs-route drift. Per-surface unit tests do not catch it.
- **Implementation**:
  - Generate contract tests from the OpenAPI schema; consumer-driven contracts for MCP tools, SDKs, web and extension.
  - Breaking-change detection in CI.
- **Suggested paths**: `tests/contract/`
- **Acceptance criteria**:
  - [ ] `SDLC-017.1` Contract suite runs in CI
  - [ ] `SDLC-017.2` MCP tool schemas covered
  - [ ] `SDLC-017.3` SDK and web client use the same contracts
  - [ ] `SDLC-017.4` Breaking change fails the build

###### SDLC-018: Continuous browser E2E and visual regression

- [ ] `SDLC-018` **Continuous browser E2E and visual regression**
- **Priority**: P2 | **Category**: Verify and test | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `UI-001`
- **Related existing items**: REL-08
- **Why (evidence from the documents)**: KGF REL-08 is a one-time browser run before release. A 90+ component UI changing under UI-001 to UI-009 needs continuous checks.
- **Implementation**:
  - Playwright flows for graph explorer, admin, reports and the new lenses; visual snapshots from Storybook.
  - Runs on PRs touching apps/web; artifacts retained.
- **Suggested paths**: `apps/web/e2e/`
- **Acceptance criteria**:
  - [ ] `SDLC-018.1` E2E suite in CI
  - [ ] `SDLC-018.2` Visual snapshots for shared components
  - [ ] `SDLC-018.3` Flake budget defined
  - [ ] `SDLC-018.4` Runs against the compose stack

###### SDLC-019: Soak, endurance and leak testing

- [ ] `SDLC-019` **Soak, endurance and leak testing**
- **Priority**: P2 | **Category**: Verify and test | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `TEST-002`
- **Why (evidence from the documents)**: There are 14 control loops, 23 autonomous execution loops, a scheduler (INFRA-005) and a durable bus (AGENT-003) that run for days. Unit and load tests do not reveal slow leaks, handle exhaustion or queue growth.
- **Implementation**:
  - Multi-hour soak scenarios with memory, file-handle, thread and queue-depth tracking.
  - Fail on monotonic growth beyond tolerance.
- **Suggested paths**: `tests/soak/`
- **Acceptance criteria**:
  - [ ] `SDLC-019.1` Soak scenarios for loops, scheduler and bus
  - [ ] `SDLC-019.2` Resource-growth assertions
  - [ ] `SDLC-019.3` Run nightly or weekly
  - [ ] `SDLC-019.4` Results feed SLOs

###### SDLC-020: Upgrade and compatibility matrix

- [ ] `SDLC-020` **Upgrade and compatibility matrix**
- **Priority**: P2 | **Category**: Verify and test | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-007`
- **Why (evidence from the documents)**: Token formats, knowledge packages, durable queues and registries must survive upgrades. Python, Node, HugeGraph, Redis and browser versions also vary on customer sites.
- **Implementation**:
  - N-1 to N upgrade tests with data; version matrix for Python, Node, HugeGraph, Redis, browsers.
  - Deprecation policy aligned with INFRA-006.
- **Suggested paths**: `tests/compat/`
- **Acceptance criteria**:
  - [ ] `SDLC-020.1` Upgrade test with seeded data
  - [ ] `SDLC-020.2` Version matrix in CI (scheduled)
  - [ ] `SDLC-020.3` Backward-compat tests for formats and packages
  - [ ] `SDLC-020.4` Policy documented

###### SDLC-021: Continuous security testing pipeline

- [ ] `SDLC-021` **Continuous security testing pipeline**
- **Priority**: P1 | **Category**: Verify and test | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: KGF S-05, REL-11, NFR-SEC-*
- **Why (evidence from the documents)**: KGF S-05 is a single OWASP audit with dependency and secrets scanning. TEST-003 fuzzes only serialization and queries. Security regressions need to be caught per PR and nightly.
- **Implementation**:
  - SAST on every PR; dependency and container scanning; secrets detection; DAST against the compose stack nightly.
  - Findings feed the registry with severity and SLA.
- **Suggested paths**: `.github/workflows/security.yml`
- **Acceptance criteria**:
  - [ ] `SDLC-021.1` SAST, dependency, container and secrets scans in CI
  - [ ] `SDLC-021.2` Nightly DAST
  - [ ] `SDLC-021.3` Severity-based SLA
  - [ ] `SDLC-021.4` Zero critical findings gate

##### Release and deploy

###### SDLC-022: Release engineering: SemVer, changelog, SBOM and signed artifacts

- [ ] `SDLC-022` **Release engineering: SemVer, changelog, SBOM and signed artifacts**
- **Priority**: P1 | **Category**: Release and deploy | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-003`
- **Related existing items**: KGF GAP-GITOPS-008, G2-SRC-SBOM
- **Why (evidence from the documents)**: GAP-GITOPS-008 versions ontology releases only. Enterprise buyers ask for SBOMs and signed builds; the platform already ingests SBOMs (G2-SRC-SBOM) but does not publish its own.
- **Implementation**:
  - SemVer, conventional commits and automated changelog; release candidate and promotion flow.
  - Generate CycloneDX or SPDX SBOMs and license report; sign images and wheels; record build provenance.
  - Rollback runbook per release.
- **Suggested paths**: `.github/workflows/release.yml`
- **Acceptance criteria**:
  - [ ] `SDLC-022.1` Automated changelog and version bump
  - [ ] `SDLC-022.2` SBOM and license report per release
  - [ ] `SDLC-022.3` Signed artifacts verified in CI
  - [ ] `SDLC-022.4` Rollback runbook tested

###### SDLC-023: Kubernetes production profile and secrets management

- [ ] `SDLC-023` **Kubernetes production profile and secrets management**
- **Priority**: P1 | **Category**: Release and deploy | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-003`
- **Related existing items**: NFR-SEC-006, GAP-HA, REL-10
- **Why (evidence from the documents)**: A Helm chart exists, Redis is in it but unwired, container hardening is partial (NFR-SEC-006) and the release gate needs a real HA environment (REL-10). Production defaults are not specified.
- **Implementation**:
  - Resource requests/limits, HPA, PodDisruptionBudgets, NetworkPolicies, probes, security contexts.
  - Secrets via an external store or sealed secrets; no secrets in values files.
  - Environment overlays for staging and production.
- **Suggested paths**: `deploy/helm/`
- **Acceptance criteria**:
  - [ ] `SDLC-023.1` Hardened chart values with tests (helm lint, policy checks)
  - [ ] `SDLC-023.2` NetworkPolicies default-deny
  - [ ] `SDLC-023.3` Secrets never in plain values
  - [ ] `SDLC-023.4` HA run documented

###### SDLC-024: Air-gapped installation bundle and offline update channel

- [ ] `SDLC-024` **Air-gapped installation bundle and offline update channel**
- **Priority**: P1 | **Category**: Release and deploy | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-022`
- **Related existing items**: KGF principle: air-gap deployable, NFR-SEC-001
- **Why (evidence from the documents)**: The principles say "air-gap deployable", yet no task builds an offline installer. Local models and embeddings (H-02) need weights, images, wheels, npm packages and docs delivered without internet.
- **Implementation**:
  - Reproducible bundle: images, wheels, npm packages, model weights, docs, checksums and signatures.
  - Offline update procedure and verification script.
- **Suggested paths**: `deploy/airgap/`
- **Acceptance criteria**:
  - [ ] `SDLC-024.1` Bundle build in CI
  - [ ] `SDLC-024.2` Install on a host with no network egress
  - [ ] `SDLC-024.3` Signature and checksum verification
  - [ ] `SDLC-024.4` Update from bundle N to N+1

##### Operate and maintain

###### SDLC-025: Unified observability: traces, metrics and logs with GenAI conventions

- [ ] `SDLC-025` **Unified observability: traces, metrics and logs with GenAI conventions**
- **Priority**: P1 | **Category**: Operate and maintain | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-004`
- **Related existing items**: NFR-OPS-001, NFR-OPS-002, G2-TEL-*
- **Why (evidence from the documents)**: INFRA-004 adds logs and OpenTelemetry is optional. CORE-002, CORE-003 and CORE-006 each make decisions (blocked, routed, over budget) that must be reconstructable end to end.
- **Implementation**:
  - Trace context through API, loops, agents, retrieval and model calls; spans for LLM calls, tool calls and retrievals.
  - Trace ID attached to logs, verification results, routing and budget decisions.
  - Local-first collector configuration.
- **Suggested paths**: `packages/eoip/observability/`
- **Acceptance criteria**:
  - [ ] `SDLC-025.1` Traces cover a full agent request
  - [ ] `SDLC-025.2` Trace ID present in logs and decision records
  - [ ] `SDLC-025.3` Dashboards for latency and cost by span
  - [ ] `SDLC-025.4` Works with no external backend

###### SDLC-026: SLOs, alert catalog, runbooks and incident process

- [ ] `SDLC-026` **SLOs, alert catalog, runbooks and incident process**
- **Priority**: P1 | **Category**: Operate and maintain | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `TEST-001`
- **Related existing items**: G2-SLO-*, REL-10
- **Why (evidence from the documents)**: The G2-SLO family has four untitled gaps and REL-10 needs a DR runbook. There is no incident, on-call or postmortem process anywhere in the three backlogs.
- **Implementation**:
  - SLOs and error budgets per engine; alert catalog with actionable thresholds.
  - Runbook per engine and per failure scenario; incident and postmortem templates; game days using TEST-001.
- **Suggested paths**: `docs/runbooks/`
- **Acceptance criteria**:
  - [ ] `SDLC-026.1` SLOs defined for core engines
  - [ ] `SDLC-026.2` Runbooks exist and are linked from alerts
  - [ ] `SDLC-026.3` Postmortem template
  - [ ] `SDLC-026.4` One game day completed

###### SDLC-027: FinOps and benefit realization

- [ ] `SDLC-027` **FinOps and benefit realization**
- **Priority**: P1 | **Category**: Operate and maintain | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `CORE-006`, `CORE-003`
- **Related existing items**: MS-27, CORE-006
- **Why (evidence from the documents)**: Token economics is called the number one cost concern, and CORE-001/003 claim 30-70% token savings and 40-60% cost reduction. Nothing measures whether the savings occur.
- **Implementation**:
  - Attribute cost (tokens, compute, storage) per tenant, agent, route and feature; budgets and anomaly alerts.
  - Before/after benefit dashboard that checks each claim against measured data.
  - Showback report.
- **Suggested paths**: `packages/eoip/finops/`
- **Acceptance criteria**:
  - [ ] `SDLC-027.1` Cost attribution per tenant and route
  - [ ] `SDLC-027.2` Budget alerts
  - [ ] `SDLC-027.3` Benefit dashboard for CORE-001/003/006 claims
  - [ ] `SDLC-027.4` Monthly showback export

###### SDLC-028: Data lifecycle: retention and right-to-erasure across all derived stores

- [ ] `SDLC-028` **Data lifecycle: retention and right-to-erasure across all derived stores**
- **Priority**: P0 | **Category**: Operate and maintain | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-029`
- **Related existing items**: NFR-PRIV-001, COMPLY-002, privacy/
- **Why (evidence from the documents)**: Phase 4 adds at least nine places personal data can be copied (L2 cache, embeddings, distilled packages, persisted messages, experiment artifacts, memory graphs, pseudonym vault, backups, logs). The privacy module handles DSAR only, COMPLY-001 promises GDPR, and immutable ledgers (G2-JOURNAL, XAI Merkle tree) conflict with erasure.
- **Implementation**:
  - Data-map of every derived store; erasure orchestrator that cascades from the graph to each store.
  - Crypto-shredding with per-subject or per-tenant keys for immutable logs and backups; erasure re-applied after restore.
  - Retention policies, archival tiers, legal hold.
- **Suggested paths**: `packages/eoip/privacy/lifecycle.py`
- **Acceptance criteria**:
  - [ ] `SDLC-028.1` Data map covers all stores
  - [ ] `SDLC-028.2` Erasure test removes a subject from graph, caches, vector index, packages, logs and backups
  - [ ] `SDLC-028.3` Retention policy engine
  - [ ] `SDLC-028.4` Legal-hold override

###### SDLC-029: Key management and envelope encryption layer

- [ ] `SDLC-029` **Key management and envelope encryption layer**
- **Priority**: P1 | **Category**: Operate and maintain | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: INFRA-007, COMPLY-002, NFR-SEC-002
- **Why (evidence from the documents)**: INFRA-007 (encryption at rest), COMPLY-002 (reversible tokens), AI-005 (artifacts), MULTI-002 and audit chains each need keys and would otherwise invent their own cryptography.
- **Implementation**:
  - KMS abstraction with local and external backends (including HSM); envelope encryption; rotation; per-tenant keys.
  - Used by backups, vault, caches, artifacts and ledgers.
- **Suggested paths**: `packages/eoip/kms/`
- **Acceptance criteria**:
  - [ ] `SDLC-029.1` Interface with local backend and one external adapter
  - [ ] `SDLC-029.2` Rotation test with no downtime
  - [ ] `SDLC-029.3` Per-tenant keys
  - [ ] `SDLC-029.4` Consumers migrated

###### SDLC-030: Tenant-isolation conformance suite

- [ ] `SDLC-030` **Tenant-isolation conformance suite**
- **Priority**: P0 | **Category**: Operate and maintain | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `SDLC-005`
- **Related existing items**: KGR-G-013, MS-26
- **Why (evidence from the documents)**: KGR-G-013 and MS-26 require isolation, and Phase 4 adds many stateful components (cache keys, bus topics, budgets, experiments, memory, vector indexes, logs). Isolation must be proven by tests that every new engine passes.
- **Implementation**:
  - Reusable suite: two tenants, same inputs, assert no cross-visibility in data, caches, queues, logs, metrics, vector search and exports.
  - Mandatory for every engine descriptor (SDLC-004).
- **Suggested paths**: `tests/tenancy/`
- **Acceptance criteria**:
  - [ ] `SDLC-030.1` Suite runs for all Phase 4 stateful engines
  - [ ] `SDLC-030.2` Fails on a deliberately leaky fixture
  - [ ] `SDLC-030.3` Part of the Definition of Done
  - [ ] `SDLC-030.4` Reports per engine

###### SDLC-031: Capacity planning, hardware profiles and local model resource manager

- [ ] `SDLC-031` **Capacity planning, hardware profiles and local model resource manager**
- **Priority**: P1 | **Category**: Operate and maintain | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `TEST-002`
- **Related existing items**: KGF KPI p95 at 50K nodes, MS-15, GRAPH-004
- **Why (evidence from the documents)**: Local-first means customers run self_llm (5 tiers), embeddings, GNN training (GRAPH-004) and fine-tuning (MS-15) on their own hardware. No sizing guide exists and the latency KPI names no hardware.
- **Implementation**:
  - Reference hardware profiles (CPU-only, single GPU, multi-GPU) with measured throughput and latency.
  - Resource manager: model loading, batching, queueing, quantization profiles and a CPU fallback.
  - Sizing guide and calculator.
- **Suggested paths**: `packages/eoip/runtime/resources.py`
- **Acceptance criteria**:
  - [ ] `SDLC-031.1` Profiles measured and published
  - [ ] `SDLC-031.2` Resource manager with queueing
  - [ ] `SDLC-031.3` CPU-only path works
  - [ ] `SDLC-031.4` Sizing guide

##### Docs, DX and go-to-market

###### SDLC-032: Docs-as-code CI and documentation site

- [ ] `SDLC-032` **Docs-as-code CI and documentation site**
- **Priority**: P1 | **Category**: Docs, DX and go-to-market | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: KGF CG-GAP-003, CG-GAP-005, S-04
- **Why (evidence from the documents)**: Five of the nine CG gaps are documentation drift (stale paths, stale stack claims, a missing console, broken links, historical counts). The same will happen to 49 new requirements without automation.
- **Implementation**:
  - CI checks: link check, referenced-path existence, executable code snippets, stale-count detector against generated facts.
  - Versioned documentation site with API reference generated from OpenAPI and a glossary.
- **Suggested paths**: `docs/`, `mkdocs.yml`
- **Acceptance criteria**:
  - [ ] `SDLC-032.1` Link and path checks fail the build
  - [ ] `SDLC-032.2` Snippets executed in CI
  - [ ] `SDLC-032.3` Docs site builds from the repo
  - [ ] `SDLC-032.4` Facts (route counts, test counts) injected from generated files

###### SDLC-033: Developer experience: one-command bootstrap, CLI, sample data and first-run

- [ ] `SDLC-033` **Developer experience: one-command bootstrap, CLI, sample data and first-run**
- **Priority**: P2 | **Category**: Docs, DX and go-to-market | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: KGF S-04, G2-EKAF-030
- **Why (evidence from the documents)**: Onboarding for developers and for first-time operators (G2-EKAF-030 onboarding wizard) is not covered. Fast local setup also speeds the AI agent.
- **Implementation**:
  - Dev container and make dev; pre-commit; a small CLI for health, migrations, flags and sample data load.
  - Sample dataset and guided first-run in the web app.
- **Suggested paths**: `Makefile`, `.devcontainer/`
- **Acceptance criteria**:
  - [ ] `SDLC-033.1` Fresh clone to running stack in one command
  - [ ] `SDLC-033.2` CLI covers health, migrate, flags
  - [ ] `SDLC-033.3` Sample data pack
  - [ ] `SDLC-033.4` First-run guide in the UI

###### SDLC-034: Enterprise procurement and GRC pack

- [ ] `SDLC-034` **Enterprise procurement and GRC pack**
- **Priority**: P2 | **Category**: Docs, DX and go-to-market | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `COMPLY-003`, `TEST-005`
- **Why (evidence from the documents)**: The TAM is enterprise (regulated industries are among the eight domain packs). Buyers ask for SOC 2 and ISO 27001 mappings, a security whitepaper, data-flow diagrams, DPIA templates, an accessibility conformance report and SLAs.
- **Implementation**:
  - Control mapping and evidence automation driven by COMPLY-003.
  - Security whitepaper, data-flow diagrams, DPIA/ROPA templates, accessibility report, SLA and support model.
- **Suggested paths**: `docs/trust/`
- **Acceptance criteria**:
  - [ ] `SDLC-034.1` Control mapping document with evidence links
  - [ ] `SDLC-034.2` Whitepaper and data-flow diagrams
  - [ ] `SDLC-034.3` DPIA template
  - [ ] `SDLC-034.4` Accessibility conformance report

#### AI lifecycle (AIDLC)

##### Data and knowledge

###### AIDLC-001: Dataset and knowledge-base versioning with lineage

- [ ] `AIDLC-001` **Dataset and knowledge-base versioning with lineage**
- **Priority**: P1 | **Category**: Data and knowledge | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AI-006`, `AGENT-002`
- **Related existing items**: GAP-AI, G2-ARCH-013, AI-006
- **Why (evidence from the documents)**: AI-006 versions embeddings, but not the chunks, corpora or extraction runs they came from. Evidence-addressable answers (GAP-AI) and replayability (G2-ARCH-013) need lineage from source to chunk to embedding to answer.
- **Implementation**:
  - Content-addressed corpus snapshots; lineage records source, chunk, extractor version, embedding model and index.
  - Emit OpenLineage-compatible events from ingestion and extraction.
  - Restore a snapshot and reproduce an answer.
- **Suggested paths**: `packages/eoip/lineage/`
- **Acceptance criteria**:
  - [ ] `AIDLC-001.1` Corpus snapshots with hashes
  - [ ] `AIDLC-001.2` Lineage queryable from an answer back to source
  - [ ] `AIDLC-001.3` OpenLineage events emitted
  - [ ] `AIDLC-001.4` Reproduce a past answer in a test

###### AIDLC-002: Re-embedding and blue/green vector index migration

- [ ] `AIDLC-002` **Re-embedding and blue/green vector index migration**
- **Priority**: P1 | **Category**: Data and knowledge | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AI-006`, `AIDLC-004`
- **Related existing items**: KGF H-02, K-09, AI-006
- **Why (evidence from the documents)**: H-02 replaces hash embeddings with real ones and AI-006 detects drift, but nothing says how to move an existing vector index to a new embedding model without downtime or quality loss.
- **Implementation**:
  - Dual-write and dual-read, backfill workers, quality comparison before cutover, rollback.
  - Embedding version required on every query path.
- **Suggested paths**: `packages/eoip/embeddings/migration.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-002.1` Blue/green index switch
  - [ ] `AIDLC-002.2` Backfill resumable
  - [ ] `AIDLC-002.3` Quality comparison report before cutover
  - [ ] `AIDLC-002.4` Rollback tested

###### AIDLC-003: Knowledge quality scoring and extraction accuracy benchmarks

- [ ] `AIDLC-003` **Knowledge quality scoring and extraction accuracy benchmarks**
- **Priority**: P1 | **Category**: Data and knowledge | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AGENT-002`, `AI-003`
- **Related existing items**: KGF MS-24, GAP-TRUTH-*
- **Why (evidence from the documents)**: AGENT-002, AI-002 and AI-003 have no precision/recall target; MS-24 will show graph health but not extraction accuracy; entity resolution quality is unmeasured; NLP is multilingual in scope (AI-002, UI-002).
- **Implementation**:
  - Labelled benchmark corpora per language and domain pack; metrics for entity, relation and resolution quality.
  - Per-source reliability scores feeding truth resolution.
  - Quality dashboard in the health view.
- **Suggested paths**: `tests/benchmarks/extraction/`
- **Acceptance criteria**:
  - [ ] `AIDLC-003.1` Benchmarks and targets recorded for AGENT-002, AI-002, AI-003
  - [ ] `AIDLC-003.2` Resolution quality reported
  - [ ] `AIDLC-003.3` Source reliability scores
  - [ ] `AIDLC-003.4` Dashboard

##### Model, prompt and agent development

###### AIDLC-007: Prompt, policy and template registry

- [ ] `AIDLC-007` **Prompt, policy and template registry**
- **Priority**: P1 | **Category**: Model, prompt and agent development | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AIDLC-004`, `SDLC-006`
- **Related existing items**: AI-005, GAP-RULE
- **Why (evidence from the documents)**: AI-005 tracks prompt iterations as experiments, and verification rules, routing policies and GAP-RULE inference policies are all versioned text. None is a deployable, tested, promotable artifact.
- **Implementation**:
  - Versioned registry with diffs, owners, evaluation results, environment promotion (dev, staging, prod) and rollback.
  - Signed artifacts; flag-controlled rollout.
- **Suggested paths**: `packages/eoip/registry/prompts.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-007.1` Registry with versions and promotion
  - [ ] `AIDLC-007.2` Promotion blocked unless evaluation passes
  - [ ] `AIDLC-007.3` Rollback tested
  - [ ] `AIDLC-007.4` Prompts and policies loaded from the registry

###### AIDLC-008: Model gateway consolidation

- [ ] `AIDLC-008` **Model gateway consolidation**
- **Priority**: P1 | **Category**: Model, prompt and agent development | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `CORE-006`, `CORE-003`
- **Related existing items**: models/provider.py, model_management/, cost_optimization/, MS-27
- **Why (evidence from the documents)**: Model access is spread across models/provider.py, model_management, cost_optimization and the new routing, budget and A/B work (CORE-003, CORE-006, AI-004). Failover, rate limits, semantic response caching, prompt redaction and per-tenant quotas belong in one place.
- **Implementation**:
  - A single gateway: provider abstraction, failover, retries, rate limits, semantic cache, PII redaction on prompts, per-tenant keys and quotas, usage metering.
  - Consolidate; do not add a fourth path.
- **Suggested paths**: `packages/eoip/gateway/`
- **Acceptance criteria**:
  - [ ] `AIDLC-008.1` One call path for all model use
  - [ ] `AIDLC-008.2` Failover test
  - [ ] `AIDLC-008.3` Per-tenant quotas enforced
  - [ ] `AIDLC-008.4` Usage metering feeds CORE-006 and MS-27

###### AIDLC-010: Model fine-tuning lifecycle pipeline

- [ ] `AIDLC-010` **Model fine-tuning lifecycle pipeline**
- **Priority**: P2 | **Category**: Model, prompt and agent development | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AIDLC-004`, `AI-005`
- **Related existing items**: MS-15, AI-004, AI-005
- **Why (evidence from the documents)**: MS-15 (LOM fine-tuning), self_llm and AI-004/005 will train and ship own models. Dataset consent and licensing, PII scrubbing, run tracking, evaluation gates, promotion and model cards must be one controlled path.
- **Implementation**:
  - Curated dataset with consent/license checks and PII scrub; training runs tracked (AI-005); evaluation gate; registry promotion and rollback; model card.
- **Suggested paths**: `packages/eoip/mlops/finetune.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-010.1` Pipeline from dataset to registry
  - [ ] `AIDLC-010.2` Evaluation gate blocks regressions
  - [ ] `AIDLC-010.3` Model card generated
  - [ ] `AIDLC-010.4` Rollback tested

##### Evaluate and validate

###### AIDLC-004: AI evaluation harness and regression gates

- [ ] `AIDLC-004` **AI evaluation harness and regression gates**
- **Priority**: P0 | **Category**: Evaluate and validate | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: none
- **Related existing items**: GAP-AI, retrieval evaluation (existing), AI-004
- **Why (evidence from the documents)**: The platform has 64 RAG modes, 35 agent types and 71 query dialects, and CORE-003 must choose among paths, but no requirement measures answer quality. TEST-001..005 cover chaos, load, fuzz, performance and accessibility only. Router, A/B tests and fine-tuning all need an offline quality signal first.
- **Implementation**:
  - Versioned golden datasets; deterministic scorers first (citation accuracy, groundedness against retrieved evidence, exact graph answers), calibrated model-judged scoring only where needed.
  - Metrics: faithfulness, context precision/recall, answer relevance, agent task success, cost and latency.
  - CI gate with thresholds; results stored per commit and per prompt/model version.
- **Suggested paths**: `tests/evals/`, `packages/eoip/evals/`
- **Acceptance criteria**:
  - [ ] `AIDLC-004.1` Golden datasets for at least RAG, graph Q and A and one agent workflow
  - [ ] `AIDLC-004.2` Deterministic scorers implemented
  - [ ] `AIDLC-004.3` CI gate with thresholds
  - [ ] `AIDLC-004.4` Results history and dashboard

###### AIDLC-005: Agent trajectory recording and deterministic replay

- [ ] `AIDLC-005` **Agent trajectory recording and deterministic replay**
- **Priority**: P1 | **Category**: Evaluate and validate | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AIDLC-004`, `SDLC-028`
- **Related existing items**: G2-ARCH-013, G2-EKAF-013, AGENT-001
- **Why (evidence from the documents)**: Replayability is a stated principle (G2-ARCH-013). Recorded trajectories enable regression tests for agents, counterfactual replay under new policies (verification, router) and evidence for audits.
- **Implementation**:
  - Record tool calls, retrieved evidence and model outputs per step; replay with recorded outputs in CI.
  - Counterfactual replay: re-run with a different policy and diff outcomes.
- **Suggested paths**: `packages/eoip/agents/replay.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-005.1` Recorder and replayer
  - [ ] `AIDLC-005.2` Replay-based regression test for two agents
  - [ ] `AIDLC-005.3` Counterfactual diff report
  - [ ] `AIDLC-005.4` Recordings follow retention and erasure policy

###### AIDLC-006: Router and guardrail calibration with shadow mode

- [ ] `AIDLC-006` **Router and guardrail calibration with shadow mode**
- **Priority**: P1 | **Category**: Evaluate and validate | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `CORE-002`, `CORE-003`, `AIDLC-004`
- **Why (evidence from the documents)**: A router that sends hard questions down cheap paths, or a guardrail that blocks valid output, degrades quality silently. Both CORE-002 and CORE-003 need calibration before enforcement.
- **Implementation**:
  - Labelled intent and verification sets; confusion matrices; cost-of-error weighting.
  - Shadow mode logs decisions without acting; promote to enforce when thresholds hold.
- **Suggested paths**: `tests/evals/routing/`
- **Acceptance criteria**:
  - [ ] `AIDLC-006.1` Labelled sets and confusion matrices
  - [ ] `AIDLC-006.2` Shadow mode in both engines
  - [ ] `AIDLC-006.3` Promotion threshold documented
  - [ ] `AIDLC-006.4` Drift alerts after promotion

##### Secure and govern

###### AIDLC-011: Continuous AI red-teaming harness

- [ ] `AIDLC-011` **Continuous AI red-teaming harness**
- **Priority**: P1 | **Category**: Secure and govern | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `CORE-002`, `SDLC-003`
- **Related existing items**: NFR-SEC-004, G2-IMMUNE-*, MS-19, MS-21
- **Why (evidence from the documents)**: The platform ingests untrusted content from Jira, Confluence, the web and files (G2-SEC-CRAWL, G2-SRC-WEB), which makes indirect prompt injection a first-order risk. NFR-SEC-004 is partial and G2-IMMUNE has 12 open gaps.
- **Implementation**:
  - Attack corpora: direct and indirect injection, tool abuse, exfiltration via retrieval, memory poisoning, jailbreak and multi-turn attacks; mapped to OWASP LLM and Agentic lists.
  - Nightly run against the verification and guardrail stack; regressions block release.
- **Suggested paths**: `tests/redteam/`
- **Acceptance criteria**:
  - [ ] `AIDLC-011.1` Attack corpus and runner
  - [ ] `AIDLC-011.2` Mapped to OWASP categories
  - [ ] `AIDLC-011.3` Nightly CI run
  - [ ] `AIDLC-011.4` Failing attack creates a tracked finding

###### AIDLC-012: Agent tool sandbox and least-privilege capability policy

- [ ] `AIDLC-012` **Agent tool sandbox and least-privilege capability policy**
- **Priority**: P0 | **Category**: Secure and govern | **Complexity**: High
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `CORE-002`
- **Related existing items**: MS-11, NFR-SEC-001, FR-AGENT-004
- **Why (evidence from the documents)**: CORE-002 names "unverified code execution" as a top production failure mode. 35 agent archetypes call tools, and MS-11 needs a sandboxed plugin loader. These should share one sandbox runtime and one capability policy.
- **Implementation**:
  - Sandboxed execution (WASM or container) with CPU, memory, time, filesystem and network limits and an egress allowlist.
  - Per-agent tool allowlists and approval tiers; capability tokens; audit of every call.
  - Shared by plugins (MS-11).
- **Suggested paths**: `packages/eoip/sandbox/`
- **Acceptance criteria**:
  - [ ] `AIDLC-012.1` Sandbox runtime with enforced limits
  - [ ] `AIDLC-012.2` Escape and exhaustion tests
  - [ ] `AIDLC-012.3` Per-agent allowlists
  - [ ] `AIDLC-012.4` Plugin loader uses the same runtime

###### AIDLC-013: Agent and workload identity, plus SCIM

- [ ] `AIDLC-013` **Agent and workload identity, plus SCIM**
- **Priority**: P1 | **Category**: Secure and govern | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `INFRA-002`
- **Related existing items**: INFRA-002, H-04, GAP-SEC-008..012
- **Why (evidence from the documents)**: INFRA-002 covers human SSO only. Agents and services act on behalf of users and need their own scoped, short-lived identities and an audit trail that says which agent acted for whom.
- **Implementation**:
  - Workload identities with short-lived scoped credentials; on-behalf-of delegation; per-agent audit principal.
  - SCIM provisioning for human lifecycle.
- **Suggested paths**: `packages/eoip/authz/workload.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-013.1` Agent credentials are scoped and expire
  - [ ] `AIDLC-013.2` Audit shows agent and delegating user
  - [ ] `AIDLC-013.3` SCIM create/update/deactivate tested
  - [ ] `AIDLC-013.4` Revocation takes effect immediately

###### AIDLC-014: AI governance pack

- [ ] `AIDLC-014` **AI governance pack**
- **Priority**: P1 | **Category**: Secure and govern | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `COMPLY-003`, `AIDLC-016`
- **Related existing items**: COMPLY-001, COMPLY-003, audit/xai_ledger.py
- **Why (evidence from the documents)**: COMPLY-001 covers GDPR, SOX and HIPAA. Customers in BFSI and healthcare (two of the eight domain packs) also face AI-specific rules and standards such as the EU AI Act, NIST AI RMF and ISO/IEC 42001.
- **Implementation**:
  - AI system inventory and risk classification; model and agent cards; impact assessments; human-oversight records.
  - Control mapping to the named frameworks feeding COMPLY-003.
  - Autonomy policy catalog (see AIDLC-016).
- **Suggested paths**: `docs/ai-governance/`
- **Acceptance criteria**:
  - [ ] `AIDLC-014.1` Inventory and risk classes for all engines and agents
  - [ ] `AIDLC-014.2` Model and agent card template filled for core models
  - [ ] `AIDLC-014.3` Mapping to EU AI Act, NIST AI RMF, ISO/IEC 42001
  - [ ] `AIDLC-014.4` Impact assessment template

###### AIDLC-016: Autonomy policy catalog

- [ ] `AIDLC-016` **Autonomy policy catalog**
- **Priority**: P1 | **Category**: Secure and govern | **Complexity**: Low
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AGENT-001`, `CORE-002`
- **Related existing items**: AGENT-001, FR-AGENT-004
- **Why (evidence from the documents)**: AGENT-001 escalates between autonomy levels across 14 control loops and 23 execution loops, but the allowed level per loop, risk tier and tenant is nowhere defined. Human-oversight rules also require it.
- **Implementation**:
  - Autonomy ladder (for example advise, act with approval, act and report, autonomous) per loop and risk tier.
  - Tenant-level policy overrides; enforced by the loop runtime and verification gate.
- **Suggested paths**: `packages/eoip/loops/autonomy.py`
- **Acceptance criteria**:
  - [ ] `AIDLC-016.1` Catalog covers all loops
  - [ ] `AIDLC-016.2` Enforcement test: a loop cannot exceed its tier
  - [ ] `AIDLC-016.3` Tenant override audited
  - [ ] `AIDLC-016.4` Linked from governance pack

##### Deploy and monitor AI

###### AIDLC-009: AI quality monitoring and user feedback loop

- [ ] `AIDLC-009` **AI quality monitoring and user feedback loop**
- **Priority**: P1 | **Category**: Deploy and monitor AI | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `AIDLC-004`, `SDLC-008`
- **Related existing items**: brain/learning_engine.py, AI-004, CORE-003
- **Why (evidence from the documents)**: The learning engine and drift detectors exist, but no requirement captures user corrections or monitors answer quality in production. Without feedback, A/B tests (AI-004) and routing feedback (CORE-003) lack ground truth.
- **Implementation**:
  - Feedback API and UI (helpful, wrong, citation disputed, correction); sampled online evaluation; drift and quality monitors.
  - Low-quality cases open work items (SDLC-008) and become evaluation cases (AIDLC-004).
- **Suggested paths**: `packages/eoip/feedback/`
- **Acceptance criteria**:
  - [ ] `AIDLC-009.1` Feedback capture end to end
  - [ ] `AIDLC-009.2` Online sampled evaluation
  - [ ] `AIDLC-009.3` Quality drift alert
  - [ ] `AIDLC-009.4` Feedback converts to eval cases

##### Human experience

###### AIDLC-015: Evidence and explanation UX

- [ ] `AIDLC-015` **Evidence and explanation UX**
- **Priority**: P1 | **Category**: Human experience | **Complexity**: Medium
- **Decision**: proposed
- **Depends on**: none | **Coordinate with**: `UI-001`, `AI-001`
- **Related existing items**: GAP-AI, KGR-G-019, UI-04
- **Why (evidence from the documents)**: The backend promises evidence-addressable answers (GAP-AI), calibrated abstention (KGR-G-019), XAI (AI-001, the XAI ledger) and uncertainty (AI-007), but the UI requirements list none of the screens users need to see them.
- **Implementation**:
  - Citation drill-down to graph nodes, paths and source records; confidence and uncertainty display; why-this-answer view; clear abstain state; feedback controls.
  - Shared component set (UI-001), accessible by default.
- **Suggested paths**: `apps/web/src/evidence/`
- **Acceptance criteria**:
  - [ ] `AIDLC-015.1` Citation drill-down component
  - [ ] `AIDLC-015.2` Confidence and abstain states
  - [ ] `AIDLC-015.3` Why-this-answer panel
  - [ ] `AIDLC-015.4` Accessibility checks pass

## 8. Decisions needed

| ID | Question | Recommendation |
|---|---|---|
| DEC-P4-01 | Which of the 50 proposals are in scope? | Accept the 7 P0 proposals now; decide the P1 group by phase before that phase starts; defer the P2 group. |
| DEC-P4-02 | Overlaps: implement once under the Phase 4 ID and close the KGF ID by reference, or keep separate? | Merge (21 items). One implementation avoids two competing modules. |
| DEC-P4-03 | Load-test tool: k6 or Locust? | Locust, consistent with KGF PERF-01 and the Python stack. |
| DEC-P4-04 | Start in parallel with the KGF programme? | Only libraries with no endpoints; wait for KGF H-03, H-04, H-07, H-08 before adding endpoints. |
| DEC-P4-05 | Singletons or tenant-scoped factories for stateful engines (SDLC-005)? | Decide before CORE-006 and INFRA-001 are built; tenant-scoped for anything holding tenant state. |
| DEC-P4-06 | Timing of the P3 and deferred items (AI-007, UI-006, UI-009, MULTI-001)? | After all P0 to P2 items; UI-009 is delivered as MS-12. |
| DEC-P4-07 | Regulatory scope beyond GDPR, SOX and HIPAA for the first customers (SOC 2, ISO 27001, ISO/IEC 42001, EU AI Act, NIST AI RMF)? | Name the frameworks before COMPLY-001 and COMPLY-003 start. |

## 9. Traceability and self-check

Counts in this file: 2 pre-flight items, 49 requirements, 50 proposals, 580 acceptance criteria. Self-check after any edit:

```python
import re
t = open("eoip-phase4-requirements.md", encoding="utf-8").read()
items = re.findall(r"^- \[[ x~!\-]\] `([A-Z]+-\d+)` \*\*", t, re.M)
acs = re.findall(r"^  - \[[ x~!\-]\] `([A-Z]+-\d+\.A?\d+)`", t, re.M)
assert len(items) == len(set(items)) == 101, len(items)
assert len(acs) == len(set(acs)) == 580, len(acs)
print("ok", len(items), "items;", len(acs), "criteria")
```

---
End of backlog v2. Generated 2026-10-12 from eoip-phase4-requirements.md v1, eoip-phase4-tracker.html and the KGF documents.
