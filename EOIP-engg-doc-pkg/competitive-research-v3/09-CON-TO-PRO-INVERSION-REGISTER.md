# 09 — Con-to-Pro Inversion Register

| Field | Value |
|---|---|
| Document | 09-CON-TO-PRO-INVERSION-REGISTER.md |
| Scope | 10 Competitor Inversions + 5 Self-Inversions (KnowGridFlow Weaknesses Turned into Strengths) |
| Methodology | Root Cause Analysis -> 3-Option Formulation -> Selected Architectural Inversion -> Falsifiable Benchmark |
| Verification Cutoff | 2026-10-18 UTC |

---

## Con-to-Pro Inversion Register

| INV-ID | Target System | Competitor Con / Drawback | Architectural Root Cause | KnowGridFlow Inverted Design (Pro) | Decision |
|---|---|---|---|---|---|
| `INV-01` | **GraphDB / Stardog / Palantir** | Permission Leakage via Inference and Retrieval | Derived facts and vector embeddings are treated as globally visible, surfacing restricted data | **Derivation-Aware ACL Composition: Cryptographically compose premise ACLs onto derived facts; policy epoch invalidation on revocation** | `ADOPT (P0)` |
| `INV-02` | **Protégé / WebProtégé** | In-Memory JVM Heap Limits & Single-User Lockout | Desktop client crashes on large graphs; lacks GitOps collaboration and branching | **Web-native collaborative Schema Studio over out-of-core memory-mapped store with GitOps ontology-as-code** | `ADOPT (P0)` |
| `INV-03` | **TopBraid EDG** | Heavyweight Enterprise Footprint & Slow Time-to-Value | Monolithic server appliance requiring months of configuration and specialized training | **GitOps-native ontology-as-code (Turtle/LinkML/YAML) with instant CLI linting, diff, and automated rollback** | `ADOPT (P0)` |
| `INV-04` | **Ontop / Timbr.ai** | Virtual Graphs are Read-Only and Blind to Unstructured Data | OBDA strictly translates SQL; completely blind to PDFs, docs, diagrams, and logs | **Universal Connection Factory + Multimodal Grounding Pipeline: virtualize SQL, extract unstructured dark data** | `ADOPT (P0)` |
| `INV-05` | **Microsoft GraphRAG** | Exorbitant LLM Token Costs & Prohibitive Indexing Latency | Batch extraction and Leiden community summarization costs hundreds of dollars per run | **LightRAG/HippoRAG dual-level routing, deterministic NER pre-extraction, and incremental on-demand community summarization** | `ADOPT (P0)` |
| `INV-06` | **Palantir / Glean / Rovo** | Proprietary Cloud-Only Lock-in & No Air-Gap Operation | Customer enterprise data sent to proprietary SaaS cloud runtimes; cannot run on-prem | **100% Self-Hosted, Local-First, Air-Gap-Capable Architecture with zero external data egress** | `ADOPT (P0)` |
| `INV-07` | **Senzing / Commercial ER** | Expensive Proprietary Licensing for Entity Resolution | Per-record pricing creates severe cost barriers for large enterprise data lakes | **Integrate open-source Splink (Fellegi-Sunter model) with DuckDB acceleration; 100% free of per-record fees** | `ADOPT (P0)` |
| `INV-08` | **TerminusDB** | WOQL Query Complexity & Proprietary Runtime Overhead | Custom Prolog/Rust query language creates steep learning curves and vendor lock-in | **Standard Cypher/GQL query interface over bitemporal revision vertices (EntityRevision, RelationshipRevision)** | `ADOPT (P1)` |
| `INV-09` | **Gephi / Cytoscape** | Client-Side DOM Freezes on Large Graph Visualization | Canvas/SVG rendering stalls and crashes on graphs larger than 5,000 nodes | **WebGL hardware-accelerated Sigma.js canvas (100k+ nodes @ 60 FPS) + server-side progressive disclosure** | `ADOPT (P0)` |
| `INV-10` | **Stardog (Join Variance) vs GraphDB (Write Amp)** | Combinatorial Forward Materialization vs. Slow Backward Query Joins | GraphDB slows ingestion 10x; Stardog causes query timeouts on deep recursion | **Hybrid Tiered Reasoning (HTRE): forward-materialize static taxonomy; rewrite complex axioms at query time** | `ADOPT (P0)` |
| `INV-SELF-01` | **KnowGridFlow Baseline (BL-18)** | Missing Source-ACL Enforcement in Search & Answers | Existing retrieval service evaluates graph edges without checking caller's ACL tokens | **Build derivation ACL filter into retrieval pipeline; discard unauthorized paths before LLM context generation** | `ADOPT (P0)` |
| `INV-SELF-02` | **KnowGridFlow Baseline (BL-20)** | Tenant Isolation Exists as Contract Only ('External Gate') | Graph backend adapters contain zero tenant scoping parameters, risking multi-tenant cross-talk | **Enforce tenant prefixing and logical partition isolation in GraphStore protocol across all backends** | `ADOPT (P0)` |
| `INV-SELF-03` | **KnowGridFlow Baseline (BL-09)** | Regex-Based Query Transpiler Breaks on Complex Dialects | Regex string substitution cannot parse nested subqueries, aggregations, or GQL path expressions | **Build typed AST query compiler (QueryPlan -> Backend AST) with formal dialect conformance tests** | `ADOPT (P0)` |
| `INV-SELF-04` | **KnowGridFlow Baseline (BL-10)** | Application-Level Query DSLs (EQL, OSQL) Create Vendor Lock-in | Custom query languages force users to learn proprietary syntax | **Standardize user-facing query interfaces on openCypher / ISO GQL and natural language with query suggestions** | `ADOPT (P1)` |
| `INV-SELF-05` | **KnowGridFlow Baseline (BL-29)** | pySHACL Adapter Uninstalled in Locked Environment | Differential SHACL test fails due to missing dependency | **Pin pyshacl in requirements-neural.lock and provide pure-Python SHACL-Core fallback** | `ADOPT (P0)` |