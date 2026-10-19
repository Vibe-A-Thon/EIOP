# 14 — Implementation Roadmap (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 14-IMPLEMENTATION-ROADMAP.md |
| Work Packages | 12 Dependency-Aware Work Packages (WP-KG3-01 to WP-KG3-12) |
| Prioritization Formula | Master Prompt Section 13 Priority Score (Normalized 0–5) |
| Horizon | P0 (Correctness & Security) -> P1 (Core Enhancements) -> P2 (Advanced Intelligence) -> P3 (Scale) |
| Verification Cutoff | 2026-10-18 UTC |

---

## 1. Phased Dependency-Aware Execution Plan

```
Phase 0: P0 Hard Gates & Security Foundations (Weeks 1-4)
  WP-KG3-01: Derivation-Aware Source-ACL Filtering (GAP-01 / INV-01)
  WP-KG3-02: Tenant Isolation Hardening Across Backends (GAP-07 / INV-SELF-02)
  WP-KG3-03: Multi-Dialect QueryPlan Compiler (GAP-04 / INV-SELF-03)
         │
         ▼
Phase 1: High-Value Enterprise Capabilities (Weeks 5-8)
  WP-KG3-04: Splink Probabilistic Entity Resolution (GAP-03 / STR-07)
  WP-KG3-05: W3C SHACL Core Conformance Gate (GAP-02 / INV-05)
  WP-KG3-06: GitOps Ontology-as-Code Studio (STR-05 / INV-02)
  WP-KG3-07: LightRAG & HippoRAG Associative Retrieval (GAP-05 / STR-11)
         │
         ▼
Phase 2: Operational Actions & Governance (Weeks 9-12)
  WP-KG3-08: Two-Phase Transactional Action Write-Back (STR-08)
  WP-KG3-09: Universal Relational Virtualization (Ontop OBDA) (GAP-09 / STR-06)
  WP-KG3-10: Sigma.js Canvas Consolidation & Cytoscape Deprecation (GAP-10 / STR-15)
         │
         ▼
Phase 3: Advanced Intelligence & Neuro-Symbolic Inference (Weeks 13-16)
  WP-KG3-11: CPU-Only GNN Prediction Plane (GAP-08 / STR-02)
  WP-KG3-12: Distributed Partition Routing & Scale-Out (CAP-05)
```

---

## 2. Work Package Inventory

### `WP-KG3-01`: Derivation-Aware Source-ACL Filtering (GAP-01 / INV-01)
- **Scope:** Implement cryptographic derivation ACL composition and policy epoch tracking in `retrieval/service.py` and `query/executor.py`.
- **Dependencies:** None (P0 Foundation).
- **Effort:** 3 Engineer-Weeks.
- **Acceptance Gate:** Journey J5: Two users with differing ACLs receive different answers to the same query; zero permission leakage.

### `WP-KG3-02`: Tenant Isolation Hardening (GAP-07 / INV-SELF-02)
- **Scope:** Enforce automatic tenant key prefixing in `GraphStore` protocol across HugeGraph, Neo4j, and Neptune.
- **Dependencies:** None (P0 Foundation).
- **Effort:** 2 Engineer-Weeks.
- **Acceptance Gate:** Journey J13: Zero cross-tenant data, index, cache, or log leakage under concurrent multi-tenant loads.

### `WP-KG3-03`: Multi-Dialect QueryPlan AST Compiler (GAP-04 / INV-SELF-03)
- **Scope:** Replace regex universal transpiler with a typed AST compiler targeting Gremlin, Cypher 25, and SPARQL 1.1.
- **Dependencies:** `WP-KG3-01`.
- **Effort:** 4 Engineer-Weeks.
- **Acceptance Gate:** Journey J14: Identical QueryPlan executes on HugeGraph, Neo4j, and Neptune returning equivalent subgraphs.

### `WP-KG3-04`: Splink Probabilistic Entity Resolution (GAP-03 / STR-07)
- **Scope:** Integrate Splink Fellegi-Sunter model with DuckDB execution in `identity/resolver.py`.
- **Dependencies:** `WP-KG3-01`.
- **Effort:** 3 Engineer-Weeks.
- **Acceptance Gate:** 95%+ precision/recall on standard benchmark deduplication with automated candidate queue routing.

### `WP-KG3-05`: W3C SHACL Core Conformance (GAP-02 / INV-05)
- **Scope:** Embed pySHACL into validation gate and run full W3C SHACL Core test suite.
- **Dependencies:** None.
- **Effort:** 2 Engineer-Weeks.
- **Acceptance Gate:** 100% pass on W3C SHACL Core test suite; zero silent passes.

### `WP-KG3-06`: GitOps Ontology-as-Code Studio (STR-05 / INV-02)
- **Scope:** Build web-native collaborative Schema Studio supporting LinkML YAML and Turtle export with CI linting.
- **Dependencies:** `WP-KG3-05`.
- **Effort:** 4 Engineer-Weeks.
- **Acceptance Gate:** Journey J4: Non-destructive ontology evolution with diff, dry-run validation, and rollback.

### `WP-KG3-07`: Dual-Level GraphRAG & HippoRAG Diffusion (GAP-05 / STR-11)
- **Scope:** Combine LightRAG dual-level routing with HippoRAG Personalized PageRank graph diffusion.
- **Dependencies:** `WP-KG3-01`, `WP-KG3-03`.
- **Effort:** 4 Engineer-Weeks.
- **Acceptance Gate:** Multi-hop question answering exceeds vector-only baseline by >= 25% on HotpotQA with 80% lower token cost.

### `WP-KG3-08`: Two-Phase Transactional Action Write-Back (STR-08)
- **Scope:** SHACL-constrained operational actions with dry-run simulation and approval gates.
- **Dependencies:** `WP-KG3-05`.
- **Effort:** 3 Engineer-Weeks.
- **Acceptance Gate:** End-to-end writeback to Jira/ServiceNow with verified rollback.
