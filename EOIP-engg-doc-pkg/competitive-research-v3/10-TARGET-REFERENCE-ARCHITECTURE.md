# 10 — Target Reference Architecture (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 10-TARGET-REFERENCE-ARCHITECTURE.md |
| System Under Design | KnowGridFlow / EOIP (Enterprise Living Brain) |
| Core Paradigm | Neuro-Symbolic Multi-Backend Enterprise Knowledge Platform |
| Deployment Norms | 100% Local-First, Air-Gap Capable, Zero Mandatory Cloud, Multi-Tenant |
| Verification Cutoff | 2026-10-18 UTC |

---

## 1. Architectural Philosophy & Guiding Invariants
KnowGridFlow replaces fragmented commercial triplestores, proprietary operational platforms, and siloed vector databases with a **Unified Neuro-Symbolic Enterprise Living Brain**.

### The 6 Architectural Invariants:
1. **Multi-Backend Neutrality:** The core platform never locks into a single database vendor. Native adapters for Apache HugeGraph, Neo4j, and Amazon Neptune are abstracted behind a capability-negotiating `GraphStore` protocol and a portable typed `QueryPlan` IR.
2. **Derivation-Aware Zero-Trust Security:** Inferred facts, vector embeddings, and search snippets cryptographically inherit the Access Control Lists (ACLs) of all supporting premises. Revoking a source permission invalidates dependent derived facts in $O(1)$ via policy epochs.
3. **Epistemic Plane Separation:** Verified ground truth, provisional AI predictions, and architectural wisdom are stored in distinct, decoupled planes:
   - **Plane GL0:** Raw Unstructured Blobs & Source Events
   - **Plane GL1:** Explicit Domain Knowledge Graph (LPG Entities & Relations)
   - **Plane GL2:** Neural Schemas, SHACL Shapes & Cognitive Graphs
   - **Plane GW:** Wisdom Graph (Decisions, Rationale, Risk Hotspots, Trade-offs)
   - **Plane GP:** Isolated Prediction Plane (Quarantined until human approval)
4. **Local-First Air-Gapped Viability:** All core services (ingestion, graph traversal, hybrid search, AST code extraction, and SLM inference) operate 100% on-premises without internet access or mandatory external cloud APIs.
5. **Zero-Data-Leak LLM Egress Fencing:** Proprietary source code, database URIs, API tokens, and PII are redacted before any model call; prompt fencing markers (`<<<UNTRUSTED_CONTENT...>>>`) and tripwire canaries prevent prompt injection and exfiltration.
6. **Deterministic First, AI Second:** Every user query executes a deterministic structured traversal first; probabilistic generative AI is reserved for contextual summarization and guided query formulation.

---

## 2. End-to-End System Block Diagram

```
+---------------------------------------------------------------------------------------------------+
|                                  KNOWGRIDFLOW WORKBENCH & CLIENTS                                 |
|  [Sigma.js WebGL Canvas]   [Schema Studio]   [Digital Thread J1]   [MCP Server]   [VS Code Ext]   |
+---------------------------------------------------------------------------------------------------+
                                                  │ (HTTPS / JSON-RPC / WebSocket)
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                      SECURITY & POLICY GATEWAY                                    |
|   OAuth2 / OIDC SSO   │   ABAC Evaluator   │   Derivation ACL Filter   │   Tenant Context (S/B/P) |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                  QUERY & RETRIEVAL COORDINATOR                                    |
|   Natural Language Suggestions (suggest/parser)   │   QueryPlan v2 IR Compiler                   |
|   Hybrid Retrieval (BM25 + HNSW + RRF)            │   HippoRAG Personalized PageRank Diffusion    |
|   LightRAG Dual-Level Context Router              │   Parameterized Dialect Optimizer             |
+---------------------------------------------------------------------------------------------------+
                   │                                                  │
                   ▼ (Compiled Native Query)                          ▼ (GraphStore Protocol)
+--------------------------------------------------+   +--------------------------------------------+
|        MULTI-BACKEND GRAPH ADAPTER LAYER         |   |          HYBRID REASONING ENGINE (HTRE)    |
|  ├─ HugeGraphStore (Gremlin REST / WebSocket)    |   |  ├─ Ingest-Time Taxonomy Closure (RDFS)    |
|  ├─ Neo4jGraphStore (Transactional Cypher 25)    |   |  ├─ Query-Time Axiom Rewriter (OWL 2 QL)   |
|  ├─ NeptuneGraphStore (openCypher / SigV4)       |   |  ├─ pySHACL Validation Gate (W3C Core)     |
|  └─ MemoryGraphStore (High-Speed Local Test)     |   |  └─ Provenance Vector Retractor (O(1))     |
+--------------------------------------------------+   +--------------------------------------------+
                   │                                                  │
                   ▼                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                  PERSISTENCE & STORAGE SUBSTRATES                                 |
|  [Primary LPG Engine]   │   [RocksDB / Memory Mapped]   │   [Qdrant / HNSW]   │   [Event WAL / DLQ] |
|   HugeGraph / Neo4j     │   Prefix Taxonomy Trees       │   Vector Embeddings │   SourceEvent v2  |
+---------------------------------------------------------------------------------------------------+
                                                  ▲
                                                  │ (Idempotent Graph Mutations)
+---------------------------------------------------------------------------------------------------+
|                               UNIVERSAL INGESTION & PIPELINE ENGINE                               |
|  Universal Connection Factory (Jira, Confluence, Git, ServiceNow, Slack, Postgres, S3, Files)    |
|  Streaming Schema Profiler (Key Detection, Relationship Discovery) │ Splink Fellegi-Sunter ER     |
|  Apache Tika Multimodal Extractor │ CodeASTAnalyzer (Python, TS) │ Two-Phase Transactional Outbox |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. The 5 Core Architecture Planes

### 3.1 Control Plane
- **Tenant Registry & Placement:** Manages tenant isolation profiles (`SILO`, `BRIDGE`, `POOL`), quotas, and white-label branding assets without cross-tenant memory bleed.
- **Workflow & Task Orchestrator:** Manages long-running ingestion jobs, replay checkpoints, DLQ retries, and asynchronous batch jobs.

### 3.2 Data Plane
- **Universal Connection Factory:** Non-blocking asynchronous ingestion layer streaming events into an append-only WAL. Connectors are strictly read-only and never mutate the graph directly.
- **Validation Gate:** Enforces label declarations, required properties, and SHACL shape compliance on every prospective mutation before committing to the graph store.

### 3.3 Evidence Plane
- **Byte-Exact Locators:** Every vertex, edge, and inferred assertion points to a `SourceEvent` ID, file path, line range, or media timestamp.
- **W3C PROV-O Compliance:** Tracks `wasGeneratedBy`, `wasDerivedFrom`, and `wasAttributedTo` across all knowledge assets.
- **Merkle Warrants (`wr1_...`):** Every mutation receipt is cryptographically sealed with RFC 8785 canonical JSON hashes.

### 3.4 Security & Tenancy Plane
- **Derivation-Aware ACL Composition:** When an edge $E$ is inferred from premises $P_1$ and $P_2$, $ACL(E) = ACL(P_1) \cap ACL(P_2)$.
- **Policy Epoch Invalidation:** Security changes increment a tenant policy epoch; dependent derived nodes evaluate the current epoch at traversal time, achieving instant revocation without re-indexing.

### 3.5 AI & Living Brain Plane (Graffin & Neural Schemas)
- **Autonomy State Machine:** Governs living AI agent behavior from `L0` (Passive) to `L5` (Autonomous) with consequence budget $\kappa$ constraints.
- **Dual-Pathway Assimilation:** Fast sub-50ms slot filling for familiar schemas; slow accommodation and novelty gap routing for unfamiliar domain concepts.
- **Isolated Prediction Plane:** Link predictions and anomaly detections are strictly quarantined until human review and promotion.

---

## 4. Multi-Backend Abstraction Specification
The `GraphStore` protocol exposes:
- `get_vertex(id) -> Vertex`
- `get_neighborhood(id, direction, edge_labels, depth, limit) -> Subgraph`
- `commit_mutation_batch(mutations, warrant) -> BatchResult`
- `compile_and_execute_plan(query_plan, caller_context) -> QueryResult`

When running against **Apache HugeGraph**, the engine leverages native Gremlin bytecode and RocksDB storage.
When running against **Neo4j**, the engine pushes down Cypher 25 path expressions.
When running against **Amazon Neptune**, the engine translates plans to openCypher over HTTPS with AWS SigV4 request signing.
