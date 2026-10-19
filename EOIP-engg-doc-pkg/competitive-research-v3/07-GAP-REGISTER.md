# 07 — Gap Register

| Field | Value |
|---|---|
| Document | 07-GAP-REGISTER.md |
| Total Gaps Identified | 10 Strategic Gaps (Prioritized P0 to P2) |
| Verification Source | Derived from Baseline Analysis (`01-SYSTEM-BASELINE.md`) and Master Matrix (`06-MASTER-CAPABILITY-MATRIX.md`) |
| Quality Gate | All P0 gaps mapped to immediate architectural inversions and roadmap packages |

---

## Strategic Gap Register

| GAP-ID | Affected Capabilities | Summary of Gap | Gap Class | Severity | Root Cause Analysis | Target Resolution & ADR |
|---|---|---|---|---|---|---|
| `GAP-01` | `CAP-46 / BL-18` | **Source-ACL Enforcement Missing in Graph Retrieval & Summaries** | `Security` | **P0** | Triplestores, vector stores, and KnowGridFlow's existing retrieval service treat graph facts as globally readable once indexed. Evaluating traversals over mixed-permission data leaks private facts to unauthorized users. | Derivation-Aware ACL Composition & Policy Epoch Invalidation (INV-01 / ADR-KG3-03). |
| `GAP-02` | `CAP-10 / BL-29` | **In-House SHACL Subset Lacks W3C Core Conformance Testing** | `Standards` | **P0** | Existing SHACL validator is a custom subset over in-memory MemoryGraphStore; pySHACL adapter is present but pySHACL is omitted from locked dependencies. | Install pySHACL in locked environment; run W3C SHACL Core conformance test suite (INV-05 / REQ-ONT-02). |
| `CAP-31` | `CAP-31 / BL-36` | **Absence of Probabilistic Entity Resolution Engine** | `Quality` | **P0** | Existing identity resolver is purely deterministic on person keys; cannot resolve fuzzy duplicates across Jira, ServiceNow, and HRIS systems. | Integrate Splink Fellegi-Sunter probabilistic matching with DuckDB acceleration (INV-07 / REQ-ING-04). |
| `GAP-04` | `CAP-20 / BL-09` | **Query Translation is Regex-Based Rather Than Full AST Compiler** | `Interoperability` | **P0** | Moonshot universal transpiler uses regex substitution, which breaks on nested sub-queries and variable-length path predicates. | Build typed QueryPlan AST compiler targeting Gremlin, Cypher 25, and SPARQL 1.1 (ADR-KG3-01 / REQ-QRY-01). |
| `GAP-05` | `CAP-56 / BL-16` | **Absence of Hierarchical Community Summarization for Global Queries** | `Research` | **P1** | Existing GraphRAG handles 1-2 hop neighborhood retrieval but cannot answer corpus-wide thematic questions ('What are the major systemic risks across all services?'). | Adopt LightRAG dual-level routing and HippoRAG Personalized PageRank diffusion (INV-05 / REQ-RAG-01). |
| `GAP-06` | `CAP-32 / C05` | **Multimodal Document Parsing Relies on External Unlocked Tika** | `Quality` | **P1** | Document extraction lacks byte-exact locator tracking across audio/video and complex PDF diagram bounding boxes. | Integrate Docling / Apache Tika sandboxed workers with byte-exact offset spans (REQ-ING-05). |
| `GAP-07` | `CAP-47 / BL-20` | **Tenant Isolation is Handled at App Layer Without Graph-Level Enforcement** | `Security` | **P0** | Graph backend adapters contain 0 references to tenant scoping; physical isolation is labeled 'External gate'. | Implement automatic tenant prefixing and cryptographic tenant context propagation in GraphStore protocol (ADR-KG3-04 / REQ-SEC-01). |
| `GAP-08` | `CAP-64 / BL-44` | **GNN and Neural Stack Blocked by Missing Numerical Dependencies** | `Research` | **P2** | Neural modules under packages/eoip/neural/ import numpy and torch which were not in base requirements.lock. | Establish locked numerical profile (requirements-neural.lock) with CPU-only PyTorch execution discipline (ADR-KG3-11 / REQ-ML-01). |
| `GAP-09` | `CAP-21 / BL-51` | **Virtual Graph Federation (OBDA) Lacks Standardized R2RML Compliant Rewriting** | `Quality` | **P1** | Existing federation planner handles simple SQL queries but lacks self-join elimination and W3C R2RML compliance. | Integrate Ontop virtual knowledge graph engine for relational database federation (REQ-FED-01). |
| `GAP-10` | `CAP-70 / BL-54` | **Legacy Dual-Engine Graph Visualization Canvas (Cytoscape + Sigma)** | `UX` | **P1** | apps/web contains legacy Cytoscape components alongside modern Sigma.js WebGL canvas, creating redundant bundle weight and inconsistent UX. | Consolidate strictly on Sigma.js + Graphology as the sole primary WebGL graph renderer (Rule R13 / ADR-KG3-10). |