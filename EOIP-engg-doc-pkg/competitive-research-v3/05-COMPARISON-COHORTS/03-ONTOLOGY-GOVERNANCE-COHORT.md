# Cohort 03 — Ontology Modeling, Taxonomies & Semantic Governance

| Field | Value |
|---|---|
| Document | 03-ONTOLOGY-GOVERNANCE-COHORT.md |
| Workload Focus | Analysis of ontology authoring ergonomics, multi-user collaboration, GitOps integration, and semantic lifecycle stewardship. |
| Technologies Evaluated | **Protégé / WebProtégé**, **TopBraid EDG**, **PoolParty**, **metaphactory**, **LinkML**, **VocBench 3**, **KnowGridFlow Target** |
| Verification Cutoff | 2026-10-18 UTC |
| Status | Comprehensive Workload Cohort Comparison |

---

## 1. Executive Summary & Workload Scope
Analysis of ontology authoring ergonomics, multi-user collaboration, GitOps integration, and semantic lifecycle stewardship.

## 2. Deep Comparative Matrix
| Dimension | Protégé / WebProtégé | TopBraid EDG | PoolParty | metaphactory | LinkML | VocBench 3 | KnowGridFlow Target |
|---| --- | --- | --- | --- | --- | --- | --- |
| **Deployment Model** | `Desktop Java Swing / Web` | `Monolithic Enterprise Server` | `Server Appliance` | `Docker / Cloud` | `CLI / Code / YAML` | `Web / Java Backend` | **Web-Native + CLI + GitOps CI/CD** |
| **Collaboration Model** | Single-User Desktop / Locking Web | `Asset Collection Approvals` | `Workflow-based` | `Low-code app templates` | `Git PR / Branch / Merge` | `Role-based workflows` | **Real-Time Multi-User + GitOps PR/Diff/Rollback** |
| **Metamodel Basis** | `W3C OWL 2 DL` | `W3C SHACL Core + Dash` | `W3C SKOS / SKOS-XL` | `W3C RDF / SPARQL` | `Python / YAML Schemas` | `W3C SKOS / OWL` | **Unified SHACL + OWL 2 + LPG Manifest** |
| **Scale Handling** | In-Memory JVM Heap (<10M axioms) | Out-of-core Jena / Named Graphs | `Server memory-backed` | `Delegated to SPARQL store` | `Static file generation` | `Delegated to RDF4J` | **Out-of-core memory-mapped store with lazy graph rendering** |

## 3. Verified Strategic Trade-Offs
- **Performance vs. Complexity:** Commercial single-paradigm engines achieve high raw speed at the cost of proprietary lock-in and operational rigidity.
- **Standards vs. Ergonomics:** Academic W3C tooling enforces strict mathematical semantics but fails on enterprise operational usability and multimodal ingestion.
- **Cloud vs. Local-First:** SaaS offerings (Palantir, Glean, Neptune) compromise customer data sovereignty and cannot run air-gapped.

## 4. Architectural Verdict for KnowGridFlow
> [!IMPORTANT]
> **Strategic Direction:** Replace desktop in-memory bottlenecks (Protégé) and heavy enterprise appliances (TopBraid) with GitOps-native ontology-as-code (LinkML/Turtle) integrated into a calm, browser-based collaborative Schema Studio.
