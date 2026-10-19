# Cohort 01 — Labeled Property Graph (LPG) & Multi-Model Engines

| Field | Value |
|---|---|
| Document | 01-LPG-ENGINES-COHORT.md |
| Workload Focus | Evaluation of transaction processing, traversal latency, distributed scaling, and query language dialect support across the leading property graph engines. |
| Technologies Evaluated | **Apache HugeGraph (BL-02)**, **Neo4j (BL-03)**, **Amazon Neptune (BL-04)**, **Memgraph**, **TigerGraph**, **JanusGraph (BL-05)**, **FalkorDB**, **KnowGridFlow Target** |
| Verification Cutoff | 2026-10-18 UTC |
| Status | Comprehensive Workload Cohort Comparison |

---

## 1. Executive Summary & Workload Scope
Evaluation of transaction processing, traversal latency, distributed scaling, and query language dialect support across the leading property graph engines.

## 2. Deep Comparative Matrix
| Dimension | Apache HugeGraph (BL-02) | Neo4j (BL-03) | Amazon Neptune (BL-04) | Memgraph | TigerGraph | JanusGraph (BL-05) | KnowGridFlow Target |
|---| --- | --- | --- | --- | --- | --- | --- |
| **Storage Model** | `RocksDB/HBase/Cassandra KV` | Native Paged Double-linked lists | `Cloud Log-Structured Storage` | `In-Memory RocksDB delta` | `C++ Native Parallel Block` | Pluggable KV (Cassandra/HBase) | **Multi-Backend Abstraction Layer** |
| **Query Dialect** | `Gremlin / Cypher subset` | `Cypher 25 / GQL subset` | `openCypher / Gremlin / SPARQL` | `Cypher / MAGE` | `GSQL` | `Gremlin` | **Universal Typed QueryPlan -> Multi-Dialect** |
| **Air-Gap Viability** | `Yes (Self-hosted)` | `Yes (Community/Enterprise)` | `No (Cloud managed only)` | `Yes` | `Yes` | `Yes` | **100% Native Local-First Air-Gap** |
| **Multi-Tenancy** | `Database-level / None` | `Multi-database (Enterprise)` | `AWS Instance isolation` | `Multi-database` | `Graph-level domain` | `None (Schema keys)` | **Cryptographic Derivation ACLs + SILO/BRIDGE/POOL** |
| **Licensing** | `Apache-2.0` | `GPLv3 / Commercial` | `Proprietary Cloud` | `Apache-2.0 / BSL` | `Commercial` | `Apache-2.0` | **Apache-2.0 Cleanroom Core** |

## 3. Verified Strategic Trade-Offs
- **Performance vs. Complexity:** Commercial single-paradigm engines achieve high raw speed at the cost of proprietary lock-in and operational rigidity.
- **Standards vs. Ergonomics:** Academic W3C tooling enforces strict mathematical semantics but fails on enterprise operational usability and multimodal ingestion.
- **Cloud vs. Local-First:** SaaS offerings (Palantir, Glean, Neptune) compromise customer data sovereignty and cannot run air-gapped.

## 4. Architectural Verdict for KnowGridFlow
> [!IMPORTANT]
> **Strategic Direction:** KnowGridFlow must NOT lock into a single backend engine. HugeGraph remains our reference operational backend for large-scale on-premises deployments; Neo4j and Neptune are preserved as first-class adapters via our capability-negotiating GraphStore protocol.
