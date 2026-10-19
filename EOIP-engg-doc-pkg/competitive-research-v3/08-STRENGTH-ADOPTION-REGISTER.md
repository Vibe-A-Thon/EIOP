# 08 — Strength-Adoption Register

| Field | Value |
|---|---|
| Document | 08-STRENGTH-ADOPTION-REGISTER.md |
| Total Strengths Cataloged | 15 Verified Core Competitor Strengths |
| Strategy | Match, exceed, or lawfully integrate verified strengths without copying protected assets |
| Verification Cutoff | 2026-10-18 UTC |

---

## Verified Competitor Strength Adoption Register

| STR-ID | Competitor / Technology | Verified Competitor Strength | Customer / Business Value | KnowGridFlow Adoption Strategy |
|---|---|---|---|---|
| `STR-01` | **Neo4j** | **Native Index-Free Adjacency & Traversal Optimization** | High-speed graph traversal with sub-millisecond p95 latency on deep hops | MATCH in HugeGraph/Neo4j pushdown; emulate in memory-mapped GraphStore |
| `STR-02` | **TigerGraph** | **Massive Parallel Processing (MPP) & GSQL Accumulators** | Real-time graph analytics and parallel algorithm execution directly in query language | ADOPT accumulator concepts in KnowGridFlow QueryPlan IR |
| `STR-03` | **Stardog** | **On-the-Fly Backward-Chaining Reasoning over Complex Axioms** | Answers SPARQL queries incorporating full OWL 2 DL class hierarchies without write amplification | ADOPT hybrid tiering: backward-chain complex axioms; pre-materialize taxonomy |
| `STR-04` | **Ontotext GraphDB** | **TRREE Forward Chaining Rule Engine for Zero-Latency Subsumption** | Instant O(1) read latency for class hierarchy and domain/range checks | ADOPT forward materialization for static RDFS taxonomies at ingest |
| `STR-05` | **TopBraid EDG** | **Native SHACL-Driven UI Generation & Semantic Governance** | Dynamic web form generation and validation directly from W3C SHACL shapes | REUSE SHACL shape definitions to drive KnowGridFlow Admin UI forms |
| `STR-06` | **Ontop** | **High-Performance SPARQL-to-SQL Rewriting with Self-Join Elimination** | Zero-ETL real-time querying of existing enterprise SQL databases without data duplication | INTEGRATE Ontop SQL rewriting engine for relational data sources |
| `STR-07` | **Splink** | **DuckDB-Accelerated Fellegi-Sunter Probabilistic Record Linkage** | Resolves millions of duplicate entities in seconds on standard commodity hardware | REUSE Splink as core probabilistic entity resolution provider |
| `STR-08` | **Palantir Foundry** | **Two-Phase Operational Actions and Write-Backs to Source Systems** | Transforms passive knowledge graphs into active operational operating systems | ADOPT two-phase transactional outbox write-back with dry-run simulation |
| `STR-09` | **Atlassian Rovo** | **Deep Digital Thread Across Jira, Confluence, Bitbucket, and Slack** | Unifies issue tracking, requirements, source code, and collaboration into a cohesive work graph | MATCH end-to-end digital thread in KnowGridFlow Journey J1 |
| `STR-10` | **Microsoft GraphRAG** | **Hierarchical Leiden Community Detection for Global Sensemaking** | Answers abstract dataset-wide thematic questions that vector search completely misses | ADOPT hierarchical community summarization for macro reporting |
| `STR-11` | **LightRAG** | **Dual-Level Retrieval Routing (Low-Level Entities + High-Level Themes)** | Achieves GraphRAG benefits with 90% lower LLM token cost and fast incremental indexing | REUSE dual-level retrieval architecture in KnowGridFlow NLQ |
| `STR-12` | **HippoRAG** | **Single-Pass Personalized PageRank Associative Diffusion** | 10x to 30x faster multi-hop associative retrieval than iterative multi-agent loops | INTEGRATE Personalized PageRank traversal over knowledge graphs |
| `STR-13` | **Qdrant** | **Hardware-Accelerated Single-Stage Payload Filtering During HNSW Traversal** | Filters by tenant and ACL attributes directly during vector search without post-filtering latency | INTEGRATE Qdrant as optional high-speed vector backend |
| `STR-14` | **TerminusDB** | **Git-Like Branching, Diff, Merge, and Succinct Immutable Layer Files** | Enables safe collaborative schema and data editing with non-destructive rollbacks | ADOPT Git-like branching and diffing in KnowGridFlow Schema Studio |
| `STR-15` | **Sigma.js** | **WebGL Hardware-Accelerated Large Graph Visualization** | Smooth 60 FPS exploration of 100,000+ nodes and edges in standard browser canvas | STANDARDIZE on Sigma.js as sole primary WebGL graph renderer (Rule R13) |