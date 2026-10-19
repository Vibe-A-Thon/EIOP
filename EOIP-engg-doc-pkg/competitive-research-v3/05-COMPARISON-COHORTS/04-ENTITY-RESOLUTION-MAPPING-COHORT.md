# Cohort 04 — Semantic ETL, Data Virtualization (OBDA) & Entity Resolution

| Field | Value |
|---|---|
| Document | 04-ENTITY-RESOLUTION-MAPPING-COHORT.md |
| Workload Focus | Comparison of record linkage, deduplication algorithms (Fellegi-Sunter, deep learning), and declarative relational mapping (R2RML, RML). |
| Technologies Evaluated | **Senzing**, **Splink**, **Zingg**, **Ontop**, **Morph-KGC**, **OpenRefine**, **KnowGridFlow Target** |
| Verification Cutoff | 2026-10-18 UTC |
| Status | Comprehensive Workload Cohort Comparison |

---

## 1. Executive Summary & Workload Scope
Comparison of record linkage, deduplication algorithms (Fellegi-Sunter, deep learning), and declarative relational mapping (R2RML, RML).

## 2. Deep Comparative Matrix
| Dimension | Senzing | Splink | Zingg | Ontop | Morph-KGC | OpenRefine | KnowGridFlow Target |
|---| --- | --- | --- | --- | --- | --- | --- |
| **Core Approach** | Real-Time Principle Entity Resolution | Probabilistic Fellegi-Sunter (DuckDB/Spark) | ML-Based Active Learning (Spark) | SPARQL-to-SQL Query Virtualization | RML / R2RML Compliant Batch ETL | `Interactive Tabular Cleaning` | **Deterministic Keys + Probabilistic Fellegi-Sunter + R2RML Virtualization** |
| **Throughput / Scale** | High (>1k entities/sec streaming) | Massive (Millions of records in DuckDB/Spark) | `Enterprise Distributed Spark` | Query-time virtual translation | High-throughput batch compiler | `Desktop memory bound` | **Streaming CDC + DuckDB-accelerated batch ER** |
| **Explainability** | `Proprietary 'Why' analysis` | Mathematical Match Weights & Bayes factors | `Classification confidence` | `Direct SQL query plan EXPLAIN` | `Deterministic mapping rules` | `Manual facet review` | **Byte-exact Evidence Spans + Mathematical Bayes Match Weights** |
| **Licensing** | `Commercial Proprietary SDK` | `MIT (Permissive)` | `Apache-2.0` | `Apache-2.0` | `Apache-2.0` | `BSD-3-Clause` | **Apache-2.0 / Redistribution-safe** |

## 3. Verified Strategic Trade-Offs
- **Performance vs. Complexity:** Commercial single-paradigm engines achieve high raw speed at the cost of proprietary lock-in and operational rigidity.
- **Standards vs. Ergonomics:** Academic W3C tooling enforces strict mathematical semantics but fails on enterprise operational usability and multimodal ingestion.
- **Cloud vs. Local-First:** SaaS offerings (Palantir, Glean, Neptune) compromise customer data sovereignty and cannot run air-gapped.

## 4. Architectural Verdict for KnowGridFlow
> [!IMPORTANT]
> **Strategic Direction:** Adopt Splink's mathematical Fellegi-Sunter engine for core probabilistic identity matching; integrate Ontop for relational virtualization; pair with KnowGridFlow's deterministic identity resolver and candidate review queue (BL-34, BL-35).
