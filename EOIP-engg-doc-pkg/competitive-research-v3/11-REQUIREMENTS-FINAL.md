# 11 — Final Implementation-Ready Requirements (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 11-REQUIREMENTS-FINAL.md |
| Total Requirements | 32 Exhaustive Requirements across 8 Modules |
| Traceability | Every REQ traces to verified GAP-ID, STR-ID, or INV-ID |
| Verification Cutoff | 2026-10-18 UTC |
| Status | Canonical Engineering Specification |

---

## Module 1: Storage Substrate & Backend Abstraction (`REQ-STG`)

### `REQ-STG-01`: Multi-Backend Capability-Negotiating GraphStore Protocol
- **Source:** GAP-04, STR-01, BL-01.
- **Problem:** Existing `GraphStore` protocol only exposes basic CRUD and neighborhood fetching, forcing multi-hop traversals to execute in Python client loops.
- **Behavior:** The `GraphStore` protocol shall support native query pushdown via `compile_and_execute(QueryPlan)` for HugeGraph (Gremlin), Neo4j (Cypher), and Neptune (openCypher). If a backend lacks a native feature (e.g., shortest path on SPARQL), the adapter shall fall back to deterministic client traversal while reporting `emulated: true`.
- **NFRs:** Traversal execution latency <= 15ms p95 for 2-hop neighborhoods.
- **Tests:** `tests/contract/test_graph_store_pushdown.py`.
- **Priority:** P0.

### `REQ-STG-02`: Degree-Bounded Traversal & Supernode Paging
- **Source:** CAP-07, GAP-01.
- **Problem:** Traversing supernodes (>100k edges) causes memory exhaustion and query timeouts.
- **Behavior:** The query executor shall enforce a configurable degree ceiling (`max_degree_per_hop = 1000`). If a node degree exceeds the ceiling, the engine shall sample the top edges by recency or weight and set `partial: true` with an explanatory warning.
- **Tests:** `tests/query/test_supernode_paging.py`.
- **Priority:** P0.

---

## Module 2: Schema & Ontology Governance (`REQ-ONT`)

### `REQ-ONT-01`: GitOps Ontology-as-Code Lifecycle
- **Source:** GAP-02, INV-02, INV-03, STR-05.
- **Problem:** Traditional ontology tools (Protégé, TopBraid) are desktop-bound or heavy monolithic appliances.
- **Behavior:** Ontologies shall be declared as versioned code artifacts (LinkML YAML or W3C Turtle) in git. Changes shall be submitted via pull requests, validated against automated CI SHACL tests, and deployed via two-phase migration with rollback scripts.
- **Tests:** `tests/ontology/test_gitops_lifecycle.py`.
- **Priority:** P0.

### `REQ-ONT-02`: W3C SHACL Core Conformance Gate
- **Source:** GAP-02, INV-SELF-05, BL-29.
- **Problem:** Existing SHACL validator is a partial in-memory subset that does not conform to the full W3C SHACL Core specification.
- **Behavior:** Integrate pySHACL into the validation gate. Every prospective graph mutation must validate against all registered `sh:NodeShape` and `sh:PropertyShape` definitions. Violations shall return structured `ValidationResult` objects with exact `sh:resultPath` and `sh:focusNode`.
- **Tests:** `tests/semantic/test_shacl_w3c_conformance.py`.
- **Priority:** P0.

---

## Module 3: Universal Ingestion & Entity Resolution (`REQ-ING`)

### `REQ-ING-01`: Universal Connection Factory & Rate-Limited Ingestion
- **Source:** CAP-26, BL-23, STR-08.
- **Problem:** Direct writes from external connectors risk corrupting graph consistency.
- **Behavior:** All connectors (Jira, Git, ServiceNow, Slack, S3, SQL) shall emit standardized `SourceEvent v2` envelopes. Connectors shall never write to the graph directly. An ingestion queue shall throttle, deduplicate, and route events through the validation gate.
- **Tests:** `tests/connectors/test_source_event_queue.py`.
- **Priority:** P0.

### `REQ-ING-02`: Splink Probabilistic Entity Resolution Integration
- **Source:** GAP-03, STR-07, INV-07, BL-36.
- **Problem:** Existing identity resolver is strictly deterministic and fails on misspelled or cross-system duplicate entities.
- **Behavior:** Integrate Splink with DuckDB execution. Ingested entity candidates shall be evaluated using the Fellegi-Sunter mathematical model with m-probabilities and u-probabilities. Matches with confidence >= 0.85 shall be merged with an immutable merge record; matches between 0.70 and 0.84 shall be routed to the candidate review queue.
- **Tests:** `tests/identity/test_splink_probabilistic_er.py`.
- **Priority:** P0.

---

## Module 4: Query, Federation & Virtualization (`REQ-QRY`)

### `REQ-QRY-01`: Typed QueryPlan AST & Multi-Dialect Compilers
- **Source:** GAP-04, INV-SELF-03, CAP-20.
- **Problem:** Regex-based query translation breaks on complex queries.
- **Behavior:** Build a formal QueryPlan Abstract Syntax Tree (AST). Compilers shall translate the AST into Gremlin bytecode, Cypher 25 text, and SPARQL 1.1 syntax with zero regex string manipulation.
- **Tests:** `tests/query/test_query_ast_compilers.py`.
- **Priority:** P0.

### `REQ-QRY-02`: Parameterized Query Gateway & Injection Defense
- **Source:** CAP-49, REVA Gate.
- **Problem:** Dynamic query generation risks Cypher/Gremlin injection attacks.
- **Behavior:** All user-supplied parameters shall be passed as bound query parameters (`$param`), never concatenated into raw query strings. Raw Cypher/Gremlin execution shall be restricted to authenticated platform administrators.
- **Tests:** `tests/security/test_query_injection_gateway.py`.
- **Priority:** P0.

---

## Module 5: GraphRAG, Memory & Natural Language (`REQ-RAG`)

### `REQ-RAG-01`: Dual-Level GraphRAG & HippoRAG Associative Diffusion
- **Source:** GAP-05, STR-10, STR-11, STR-12, INV-05.
- **Problem:** Plain vector RAG misses multi-hop relationships; Microsoft GraphRAG is too expensive for continuous updates.
- **Behavior:** Combine LightRAG dual-level routing (entity-level vs relationship-level) with HippoRAG Personalized PageRank (PPR) diffusion over the knowledge graph. Queries shall retrieve multi-hop subgraphs in a single associative pass without iterative LLM agent loops.
- **Tests:** `tests/retrieval/test_hipporag_diffusion.py`.
- **Priority:** P0.

### `REQ-RAG-02`: Deterministic First, NL Suggestions Second
- **Source:** CAP-58, BL-11, BL-12.
- **Problem:** Direct NL-to-query generates hallucinated queries that execute wrong traversals.
- **Behavior:** When a user types a natural language question, the system shall parse deterministic templates and present 3 ranked candidate queries with plain-language explanations. The query executes only after user confirmation.
- **Tests:** `tests/suggest/test_nl_candidate_ranking.py`.
- **Priority:** P0.

---

## Module 6: Security, Tenancy & Zero-Data-Leak (`REQ-SEC`)

### `REQ-SEC-01`: Derivation-Aware Source-ACL Enforcement
- **Source:** GAP-01, INV-01, INV-SELF-01, BL-18.
- **Problem:** Graph traversals and vector searches surface facts derived from sources the caller cannot access.
- **Behavior:** Every node and edge shall record a cryptographic `acl_hash` and `derivation_acls`. Query executors and GraphRAG retrievers shall evaluate caller token permissions against derivation ACLs, filtering unauthorized subgraphs before context injection.
- **Tests:** `tests/security/test_derivation_acl_filtering.py`.
- **Priority:** P0.

### `REQ-SEC-02`: Zero-Data-Leak LLM Egress Fencing & Canary Tripwires
- **Source:** CAP-51, REVA-SEC-013-STRICT.
- **Problem:** Calling cloud LLMs risks exfiltrating proprietary source code, credentials, and PII.
- **Behavior:** All LLM prompts must route through `EgressSecurityGate`. Redact passwords, bearer tokens, and private keys. Embed cryptographic canaries (`egress_canary_...`). Wrap prompts in untrusted boundaries (`<<<UNTRUSTED_CONTENT...>>>`).
- **Tests:** `tests/security/test_egress_gate_enforcement.py`.
- **Priority:** P0.

### `REQ-SEC-03`: Strict Multi-Tenant Isolation
- **Source:** GAP-07, INV-SELF-02, BL-20.
- **Problem:** Shared backend adapters lack physical tenant scoping.
- **Behavior:** All vertex and edge IDs shall be automatically namespaced with tenant IDs (`{tenant_id}:{entity_type}:{key}`). Query caches, vector indices, and temporary files must be partitioned by tenant.
- **Tests:** `tests/tenancy/test_multi_tenant_isolation.py`.
- **Priority:** P0.

---

## Module 7: UI Workbench & Visual Analytics (`REQ-UIX`)

### `REQ-UIX-01`: WebGL Large-Graph Canvas (Sigma.js + Graphology)
- **Source:** CAP-70, GAP-10, INV-09, Rule R13.
- **Problem:** Cytoscape Canvas freezes on large graphs.
- **Behavior:** Standardize exclusively on Sigma.js WebGL rendering powered by Graphology. Render 100,000+ nodes and edges at 60 FPS. If WebGL context is lost, gracefully fall back to synchronized accessible data tables (Rule R13, GUI-SCR-027).
- **Tests:** `apps/web/tests/gui-foundations.spec.js`.
- **Priority:** P0.

---

## Module 8: Wisdom Graph & Living AI (`REQ-WIS`)

### `REQ-WIS-01`: Wisdom Graph Miner & Decision Lineage (Plane GW)
- **Source:** CAP-80, BL-56.
- **Problem:** Organizations lose architectural rationale and repeat past mistakes.
- **Behavior:** Mine ADR markdown documents and git commit histories into Plane GW. Extract decisions, context, trade-offs, and cyclomatic risk hotspots (`RISK_IN_COMPONENT`), linking them directly to Plane GL1 code symbols.
- **Tests:** `tests/wisdom/test_wisdom_lifecycle.py`.
- **Priority:** P0.
