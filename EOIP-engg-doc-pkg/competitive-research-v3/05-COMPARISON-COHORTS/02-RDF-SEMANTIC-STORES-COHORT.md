# Cohort 02 — RDF Stores, Triplestores & Semantic Reasoning Engines

| Field | Value |
|---|---|
| Document | 02-RDF-SEMANTIC-STORES-COHORT.md |
| Workload Focus | Comparison of formal W3C standards compliance, description logic reasoning profiles (OWL 2 DL/RL/EL), SPARQL 1.1 performance, and SHACL constraint validation. |
| Technologies Evaluated | **Stardog**, **Ontotext GraphDB**, **Apache Jena (TDB2)**, **OpenLink Virtuoso**, **AllegroGraph**, **Oxigraph**, **KnowGridFlow Target** |
| Verification Cutoff | 2026-10-18 UTC |
| Status | Comprehensive Workload Cohort Comparison |

---

## 1. Executive Summary & Workload Scope
Comparison of formal W3C standards compliance, description logic reasoning profiles (OWL 2 DL/RL/EL), SPARQL 1.1 performance, and SHACL constraint validation.

## 2. Deep Comparative Matrix
| Dimension | Stardog | Ontotext GraphDB | Apache Jena (TDB2) | OpenLink Virtuoso | AllegroGraph | Oxigraph | KnowGridFlow Target |
|---| --- | --- | --- | --- | --- | --- | --- |
| **Reasoning Strategy** | Backward Chaining (Datalog rewriting) | Total Forward Chaining (TRREE rules) | `Forward Chaining (Jena Rules)` | Forward Chaining & SQL rewrite | `Prolog / Datalog Hybrid` | No native reasoning (Storage only) | **Hybrid Tiered Reasoning (HTRE: Forward Taxonomy + On-Demand Axioms)** |
| **Write Amplification** | `Low (writes raw assertions)` | Severe (materializes all entailments) | `Medium (rule materialization)` | `Medium` | `Medium-High` | `Zero (raw quads)` | **Zero on raw graph; O(1) retraction via provenance vectors** |
| **Query Latency Variance** | High (join tree blowup on recursion) | Very Low (O(1) pre-computed lookups) | `Medium` | `Low-Medium` | `Medium` | `Low (fast B-Tree seeks)` | **Deterministic Low: bounded by pre-computed taxonomy prefix trees** |
| **Licensing** | `Commercial Proprietary` | `Free / Commercial` | `Apache-2.0` | `GPLv2 / Commercial` | `Commercial` | `Apache-2.0 / MIT` | **Permissive / Self-Hosted** |

## 3. Verified Strategic Trade-Offs
- **Performance vs. Complexity:** Commercial single-paradigm engines achieve high raw speed at the cost of proprietary lock-in and operational rigidity.
- **Standards vs. Ergonomics:** Academic W3C tooling enforces strict mathematical semantics but fails on enterprise operational usability and multimodal ingestion.
- **Cloud vs. Local-First:** SaaS offerings (Palantir, Glean, Neptune) compromise customer data sovereignty and cannot run air-gapped.

## 4. Architectural Verdict for KnowGridFlow
> [!IMPORTANT]
> **Strategic Direction:** Invert Stardog's query-time timeout variance and GraphDB's massive write amplification by adopting KnowGridFlow's Hybrid Tiered Reasoning Engine (HTRE): forward-materialize deterministic taxonomic closures (RDFS) at ingest; evaluate complex axioms and SHACL shapes via localized query rewrites.
