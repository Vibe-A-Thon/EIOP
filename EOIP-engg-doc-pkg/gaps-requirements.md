# gaps-requirements.md
## Enterprise Ontology & Knowledge Intelligence Platform — Competitive Gap Requirements

**Document status:** Research-backed product requirements  
**Date:** 2026-10-01  
**Primary deployment:** On-premises / air-gapped capable  
**Primary graph database:** Apache HugeGraph  
**Packaging:** Docker / Docker Compose for MVP; production-ready container topology thereafter  
**Cloud dependency:** None required  
**MVP authorization constraint:** No RBAC in MVP; route/screen separation is UX only, not a security boundary  
**Product direction:** Enterprise Ontology + Knowledge Graph + Engineering Intelligence + GraphRAG + Agentic Intelligence + Governance

---

## 1. Purpose

This document identifies capability gaps between the proposed platform and major enterprise knowledge-graph / ontology / semantic-data platforms, then converts those gaps into implementable product requirements.

The objective is **not** to imitate competitors feature-for-feature. The objective is to combine the strongest patterns observed across semantic platforms, graph databases, data catalogs, ontology-management products, GraphRAG systems, governance products, and engineering-intelligence tools while deliberately avoiding common trade-offs such as:

- cloud lock-in,
- closed or opaque data models,
- ontology-only workflows disconnected from engineering systems,
- property-graph systems with weak semantic standards,
- semantic systems with weak code intelligence,
- expensive feature add-ons,
- heavy infrastructure footprints,
- limited traceability from requirement to code to runtime,
- weak provenance for AI-inferred relationships,
- insufficient agent/tool governance,
- limited offline/air-gapped operation,
- fragmented UX across business, engineering, ontology, operations and AI personas,
- lack of measurable graph quality,
- lack of reproducible ontology evolution,
- weak “why is this answer true?” evidence chains.

The resulting platform should be positioned as an **Enterprise Knowledge & Engineering Intelligence Platform** whose ontology/knowledge graph is the durable semantic foundation.

---

# 2. Existing Baseline Already Covered

The current system already includes or plans:

- Apache HugeGraph as the primary graph store.
- Jira, Confluence, GitLab, ServiceNow, files, code and documentation connectors.
- Jira Graph, Code Graph, Meta Graph, Relationships Graph and cross-graph links.
- RDF/OWL interoperability layer.
- Gremlin-first query architecture with high-level APIs.
- Ontology validation.
- GraphRAG / Hybrid RAG / Corrective RAG / Agentic RAG patterns.
- Agent framework with cognitive, memory, planning, tool, guardrail and collaboration layers.
- MCP tools.
- Human-control workflow patterns.
- Web User application.
- Admin/Engineering application.
- VS Code extension.
- No-cloud / local-first operation.
- Dockerized deployment.
- Provenance, temporal graph and graph quality concepts.
- Demonstrable vertical-slice MVP.

This document therefore focuses on **new or strengthened requirements**.

---

# 3. Research Method

The comparison was based primarily on official product documentation and standards, with selected research literature for knowledge-graph quality and GraphRAG.

Platforms and reference systems examined:

1. Stardog
2. Neo4j + Graph Data Science + neosemantics
3. Ontotext GraphDB
4. TopQuadrant TopBraid EDG / TQ Data Foundation
5. PoolParty Semantic Suite
6. Cambridge Semantics Anzo / Graph Studio
7. metaphacts metaphactory
8. data.world
9. Amazon Neptune
10. Oracle RDF Graph
11. Microsoft GraphRAG
12. Apache HugeGraph
13. W3C SHACL
14. W3C PROV-O
15. OpenLineage
16. OpenTelemetry

The study deliberately distinguishes:
- **documented product capability**, and
- **product trade-off / inference** derived from architecture, licensing, deployment or scope.

A “con” below is therefore a **trade-off relative to this product’s target**, not a claim that the competing product is poor.

---

# 4. Competitive Study

## 4.1 Stardog

### Documented strengths
- Enterprise knowledge-graph platform with SPARQL, reasoning, inference and semantic modeling.
- Virtual Graphs allow in-place mapping/querying of relational and selected NoSQL data without materializing everything.
- Knowledge Catalog manages metadata about virtual graphs and sources.
- On-premise/self-managed deployment is supported.
- Enterprise capabilities include HA, caching, backups, LDAP and connectors.
- Strong semantic standards orientation and inference.

### Trade-offs relative to our target
- Primarily semantic-data / knowledge-graph oriented rather than an engineering-intelligence product spanning Jira → code → build → deployment → incident → docs.
- Enterprise capabilities are licensed as a commercial platform.
- Product-specific virtualization/mapping concepts can increase vendor dependence.
- Agentic engineering workflows, VS Code-centered developer intelligence and code-graph lineage are not the core product identity.

### Requirements to turn these trade-offs into strengths
- **GAP-FED-001:** Build a first-class **Semantic Federation & Virtualization Layer** for external sources without forcing materialization.
- **GAP-FED-002:** Support policy-controlled choice between `VIRTUAL`, `CACHE`, `MATERIALIZE`, and `HYBRID` per source/entity type.
- **GAP-FED-003:** Maintain explainable query plans showing which results came from HugeGraph versus live sources.
- **GAP-FED-004:** Build federation adapters independently of HugeGraph so the product can query JDBC/REST/file sources while keeping HugeGraph as semantic control plane.
- **GAP-ENG-001:** Make requirement-to-code-to-runtime traceability a native differentiator rather than an external integration.

---

## 4.2 Neo4j

### Documented strengths
- Mature property-graph database and Cypher ecosystem.
- Strong graph traversal and graph-data-science algorithms.
- Enterprise clustering, online backup, LDAP/RBAC and production tooling.
- GraphRAG libraries and AI-focused tooling.
- neosemantics supports RDF import/export, OWL/RDFS/SKOS, SHACL validation and basic inferencing for self-hosted deployments.

### Trade-offs relative to our target
- RDF/ontology capabilities are an extension/plugin path rather than the native center of the property-graph architecture.
- Some production/analytics capabilities require Enterprise licensing.
- GDS relies on in-memory graph projections for analytics, adding memory planning and lifecycle complexity.
- Ontology governance, taxonomy stewardship and business-semantic workflows are not the primary product center.
- A graph database does not by itself solve source provenance, semantic governance, engineering traceability, agent governance or evidence-backed AI.

### Requirements
- **GAP-DUAL-001:** Implement a **Dual Semantic Model**: native HugeGraph property graph + canonical RDF/OWL/SHACL semantic representation.
- **GAP-DUAL-002:** Guarantee round-trip mappings for supported ontology constructs.
- **GAP-GDS-001:** Create a local graph-analytics service with pluggable algorithms without requiring the authoritative graph to be copied permanently into another database.
- **GAP-GDS-002:** Provide algorithms for PageRank, centrality, connected components, community detection, similarity, shortest path and dependency risk.
- **GAP-SEM-001:** Treat ontology/schema/governance as first-class, not a plugin.
- **GAP-AI-001:** Make every GraphRAG/agent answer evidence-addressable to graph nodes, paths and source records.

---

## 4.3 Ontotext GraphDB

### Documented strengths
- RDF-native database with SPARQL 1.1.
- Forward-chaining reasoning and standard/custom rulesets.
- Lucene/OpenSearch/Elasticsearch-style connector ecosystem for search.
- Enterprise edition includes HA and advanced security integrations.
- Local vector-search integration can be supported through connector architecture.
- Workbench and semantic tooling.

### Trade-offs relative to our target
- RDF-centric model can be less natural for code-level engineering traversal than a property-graph-first representation.
- Some advanced functionality is edition/add-on dependent.
- Engineering workflow integration and IDE-native traceability are not the central product proposition.
- AI agent orchestration and enterprise action governance are beyond the core graph database function.

### Requirements
- **GAP-SEARCH-001:** Add synchronized **full-text + vector + graph hybrid search** with freshness guarantees.
- **GAP-SEARCH-002:** Search results must preserve graph identity and provenance.
- **GAP-RULE-001:** Build a deterministic rules engine supporting versioned inference policies.
- **GAP-RULE-002:** Distinguish asserted, inferred, model-generated and human-confirmed facts.
- **GAP-RULE-003:** Support retraction/recomputation when source assertions change.
- **GAP-IDE-001:** Expose ontology and lineage directly within VS Code.

---

## 4.4 TopBraid EDG / TQ Data Foundation

### Documented strengths
- Strong ontology, vocabulary, taxonomy, reference-data and governance workflows.
- SHACL-centered schema and validation.
- RDFS/OWL interoperability.
- GraphQL generation from SHACL and data validation.
- Rich business/technical stewardship UX.
- Highly configurable model-driven asset collections.

### Trade-offs relative to our target
- Governance/semantic stewardship orientation can be heavyweight for developer workflows.
- Application deployment uses a traditional Java/Tomcat operational model.
- Its strongest differentiator is semantic governance rather than deep code/runtime engineering intelligence.
- The product’s workflows may require specialized semantic-modeling expertise.

### Requirements
- **GAP-NOCODE-001:** Build a visual **Ontology Studio** for ontology classes, properties, edges, SHACL-like constraints and mappings.
- **GAP-NOCODE-002:** Provide novice, analyst and expert editing modes.
- **GAP-NOCODE-003:** Generate forms, GraphQL/OpenAPI schemas and validation rules from ontology definitions where feasible.
- **GAP-GOV-001:** Add semantic stewardship workflow: draft → review → approve → publish → deprecate.
- **GAP-GOV-002:** Support ontology branches, diffs, merge conflict detection and semantic merge.
- **GAP-GOV-003:** Add business glossary, taxonomy, reference-data and ontology crosswalks.
- **GAP-UX-001:** Hide RDF/SHACL complexity from non-semantic users while preserving standards internally.

---

## 4.5 PoolParty Semantic Suite

### Documented strengths
- Mature taxonomy/thesaurus/ontology tooling.
- SKOS/RDF semantic standards.
- NLP/text extraction and auto-classification.
- Knowledge graph, semantic search and recommendation capabilities.
- Modular commercial packaging.
- Knowledge-engineer-oriented tooling and workflows.

### Trade-offs relative to our target
- Broad functionality is packaged in modules/editions, which can increase commercial complexity.
- Primarily semantic knowledge/content management rather than software-engineering traceability.
- Deep code graph and runtime lineage are not the center of the platform.
- AI/application capabilities may require additional modules/services.

### Requirements
- **GAP-TAX-001:** Add enterprise taxonomy/thesaurus management using SKOS-compatible concepts.
- **GAP-NLP-001:** Add local entity extraction, tagging, classification and concept recommendation.
- **GAP-REC-001:** Add graph-aware recommendation engine for documents, experts, components and related concepts.
- **GAP-PACK-001:** Keep major core capabilities integrated in one platform while allowing optional modules rather than artificial fragmentation.
- **GAP-TCO-001:** Provide transparent resource consumption, sizing calculator and offline license/deployment model.

---

## 4.6 Cambridge Semantics Anzo / Graph Studio

### Documented strengths
- Semantic models, data onboarding, blending and Graphmarts.
- Dataset catalog with technical, operational and business metadata.
- Tracks transformations and metadata throughout onboarding.
- Graph layers support transformation and enrichment.
- Enterprise deployment guidance, multiple environment patterns and large-scale analytics.

### Trade-offs relative to our target
- Some deployment profiles can be resource intensive; documented Graph Lakehouse recommendations can be substantial for production.
- Platform architecture can be operationally complex.
- Developer IDE/code-graph intelligence is not the core product.
- Our target requires a lighter Docker-first entry point with progressive scale-out.

### Requirements
- **GAP-LAYER-001:** Introduce **Graph Views / Knowledge Products** comparable conceptually to curated graph subsets:
  - domain views,
  - project views,
  - risk views,
  - audit views,
  - developer views,
  - executive views.
- **GAP-LAYER-002:** Views must be declarative, versioned and reproducible.
- **GAP-LITE-001:** Support laptop/dev, single-server production and distributed production profiles.
- **GAP-LITE-002:** Implement automated sizing and capacity planning.
- **GAP-DATAOPS-001:** Capture every transformation as lineage metadata.

---

## 4.7 metaphactory

### Documented strengths
- Enterprise knowledge-graph platform for semantic modeling, data management and model/data-driven application development.
- Visual semantic modeling and app-building environment.
- Federation, search, visualization and knowledge-discovery capabilities.
- Modular app-based approach.

### Trade-offs relative to our target
- General-purpose semantic application platform rather than engineering lifecycle intelligence.
- A powerful low-code platform can introduce its own application/runtime model that users must learn.
- Code provenance, CI/CD lineage and agent governance are not the product’s center.

### Requirements
- **GAP-APP-001:** Build a **Knowledge App Builder** that can compose query, table, graph, timeline, KPI and evidence panels from saved semantic queries.
- **GAP-APP-002:** App definitions must be configuration-as-code and exportable.
- **GAP-TEMPLATE-001:** Provide packaged templates for engineering, audit, risk, incident, architecture and compliance use cases.
- **GAP-EXT-001:** Support extension SDKs rather than requiring modification of the core platform.

---

## 4.8 data.world

### Documented strengths
- Graph-powered metadata/data catalog.
- Business glossary, technical/business/custom metadata.
- Curation/enrichment workflows.
- Lineage and impact analysis.
- Stewardship, certification states and auditability.
- SSO/SAML/RBAC and enterprise governance.

### Trade-offs relative to our target
- Data-catalog / metadata-governance center of gravity rather than full engineering code/runtime graph.
- Cloud-oriented enterprise catalog patterns may not satisfy strict offline/air-gapped requirements without appropriate deployment offerings.
- Ontology reasoning, deep code graph, local AI agents and IDE workflow are different problem spaces.

### Requirements
- **GAP-CATALOG-001:** Add an enterprise **Knowledge Catalog** over all graph assets.
- **GAP-CATALOG-002:** Support asset certification states: Draft, Candidate, Trusted, Certified, Deprecated, Quarantined.
- **GAP-CATALOG-003:** Create stewardship assignments and data/knowledge ownership.
- **GAP-CATALOG-004:** Add domain collections / knowledge products.
- **GAP-CATALOG-005:** Provide lineage-impact navigation from catalog to underlying graph path.

---

## 4.9 Amazon Neptune

### Documented strengths
- Managed graph database.
- Supports Gremlin, openCypher and SPARQL, with distinct property-graph and RDF models.
- High availability, replicas, backup and cloud-managed operations.
- Suitable for large connected datasets.

### Trade-offs relative to our target
- Cloud-only managed service conflicts directly with the on-prem/air-gapped requirement.
- RDF and property-graph query models remain distinct rather than one unified semantic abstraction.
- Managed infrastructure creates cloud/provider dependence.
- Database service alone does not provide the full ontology/product/agent/developer experience.

### Requirements
- **GAP-OFFLINE-001:** Zero mandatory Internet/cloud dependency.
- **GAP-PORT-001:** Export/import through open formats to reduce lock-in.
- **GAP-QUERY-001:** Provide one **Unified Semantic Query API** capable of routing internally to Gremlin, semantic/RDF adapter, search, vector or federated source.
- **GAP-HA-001:** Provide self-managed HA patterns for HugeGraph distributed mode.

---

## 4.10 Oracle RDF Graph

### Documented strengths
- RDF, RDFS and OWL semantic capabilities integrated with Oracle Database.
- Enterprise database ecosystem and operational tooling.

### Trade-offs relative to our target
- Dependency on Oracle’s broader database/license ecosystem.
- Semantic functionality is tied to a general-purpose database platform rather than a dedicated engineering-knowledge product.
- Product portability and lightweight adoption are lower priorities than in our target.

### Requirements
- **GAP-DBAGNOSTIC-001:** Keep ontology/domain contracts independent of any single graph database implementation.
- **GAP-EXPORT-001:** Support RDF, JSON-LD, GraphML/CSV and canonical JSON exports.
- **GAP-MIGRATION-001:** Provide migration utilities and stable external IDs.

---

## 4.11 Microsoft GraphRAG

### Documented strengths
- Extracts entities, relationships and claims from unstructured text.
- Community detection and hierarchical community reports.
- Configurable workflows and embeddings.
- Designed to improve answering over private datasets.

### Documented cautions
- The project describes itself as research-oriented/maintenance-mode rather than a supported enterprise product.
- The documentation warns indexing can be expensive.
- Prompt tuning is recommended.

### Requirements
- **GAP-GRAG-001:** Do not make LLM extraction the only path to graph construction.
- **GAP-GRAG-002:** Use deterministic source-system relations first; model-generated relations second.
- **GAP-GRAG-003:** Add community detection and hierarchical semantic summaries, but regenerate summaries incrementally rather than rebuilding the whole corpus.
- **GAP-GRAG-004:** Maintain cost/compute budgets even for local models.
- **GAP-GRAG-005:** Benchmark GraphRAG against direct graph query, vector RAG, hybrid RAG and no-RAG baselines.
- **GAP-GRAG-006:** Persist evidence chains for every answer.

---

# 5. Highest-Value Gaps to Add

The following requirements are the most important additions if the aim is to create a genuinely differentiated enterprise platform.

---

# 6. Semantic Digital Thread

## Objective

Create a continuously maintained graph that links business intent to software implementation and runtime outcomes.

## Requirements

- **GAP-SDT-001:** Every requirement must be linkable to design, story, commit, code symbol, test, build, deployment, service and incident.
- **GAP-SDT-002:** Support forward and reverse navigation.
- **GAP-SDT-003:** Each link must have provenance, confidence and evidence.
- **GAP-SDT-004:** Provide missing-link detection.
- **GAP-SDT-005:** Generate traceability coverage percentage per project/release.
- **GAP-SDT-006:** Provide release-level “traceability completeness” gates.
- **GAP-SDT-007:** Maintain temporal state so historical releases can be reconstructed.
- **GAP-SDT-008:** Support semantic digital-thread comparison between releases.

### Acceptance
A user must be able to select a production incident and navigate backward to deployment → build → commit → function → Jira requirement → design/documentation with source evidence.

---

# 7. Enterprise Semantic Control Plane

## Requirements

- **GAP-CP-001:** Ontology is the semantic control plane, not merely another graph.
- **GAP-CP-002:** Maintain a canonical entity registry.
- **GAP-CP-003:** Maintain canonical relationship registry.
- **GAP-CP-004:** Maintain policy, validation, provenance and mapping metadata.
- **GAP-CP-005:** Every connector maps into canonical contracts.
- **GAP-CP-006:** Source-specific fields remain accessible without polluting the canonical ontology.
- **GAP-CP-007:** Every schema/ontology change is versioned and diffable.
- **GAP-CP-008:** Breaking schema changes require migration plans.
- **GAP-CP-009:** Semantic contracts are machine-readable and testable.

---

# 8. Ontology GitOps / Semantic DevOps

This is a major opportunity for differentiation.

## Requirements

- **GAP-GITOPS-001:** Store ontology/schema source definitions in Git-compatible text formats.
- **GAP-GITOPS-002:** Provide ontology branch, pull-request/review and merge workflows.
- **GAP-GITOPS-003:** Generate semantic diffs:
  - class added/removed,
  - property added/removed,
  - cardinality changed,
  - relationship direction changed,
  - constraint tightened/relaxed,
  - term deprecated,
  - mapping changed.
- **GAP-GITOPS-004:** CI validates ontology before publishing.
- **GAP-GITOPS-005:** Run impact analysis for ontology changes.
- **GAP-GITOPS-006:** Generate migration scripts.
- **GAP-GITOPS-007:** Allow rollback to previous semantic version.
- **GAP-GITOPS-008:** Package ontology releases using SemVer-like policy.

---

# 9. Semantic Contract Testing

## Requirements

- **GAP-CONTRACT-001:** Define contracts between source systems and ontology mappings.
- **GAP-CONTRACT-002:** Detect connector schema drift.
- **GAP-CONTRACT-003:** Fail or quarantine ingestion when required semantic invariants are violated.
- **GAP-CONTRACT-004:** Generate compatibility reports before deploying ontology changes.
- **GAP-CONTRACT-005:** Maintain producer/consumer mapping contracts.
- **GAP-CONTRACT-006:** Expose contract tests to CI/CD.

---

# 10. Provenance & Evidence Ledger

Use W3C PROV-O concepts where interoperable.

## Requirements

- **GAP-PROV-001:** Represent Entity, Activity and Agent provenance concepts.
- **GAP-PROV-002:** Every inferred edge must reference the evidence used.
- **GAP-PROV-003:** Preserve extraction algorithm/model/parser version.
- **GAP-PROV-004:** Preserve source checksum/version.
- **GAP-PROV-005:** Support graph-path evidence bundles.
- **GAP-PROV-006:** Every AI answer returns an Evidence Manifest.
- **GAP-PROV-007:** Evidence manifests must be exportable and immutable after issuance.
- **GAP-PROV-008:** Provide “why does this edge exist?” UI.
- **GAP-PROV-009:** Provide “what would disappear if source X were removed?” analysis.

---

# 11. Confidence, Contradiction & Truth Management

## Requirements

- **GAP-TRUTH-001:** Do not overwrite conflicting claims.
- **GAP-TRUTH-002:** Represent claims separately from resolved canonical facts.
- **GAP-TRUTH-003:** Store source authority score.
- **GAP-TRUTH-004:** Store extraction confidence.
- **GAP-TRUTH-005:** Store validation confidence.
- **GAP-TRUTH-006:** Detect contradictory claims.
- **GAP-TRUTH-007:** Support configurable truth-resolution policy.
- **GAP-TRUTH-008:** Permit human adjudication.
- **GAP-TRUTH-009:** Retain rejected/obsolete claims for history.
- **GAP-TRUTH-010:** Explain why a canonical fact was selected.

---

# 12. Knowledge Quality SLOs

Research literature consistently treats KG quality as multidimensional, including accuracy, completeness, consistency, timeliness, trustworthiness and availability.

## Requirements

- **GAP-KQ-001:** Define per-domain quality SLOs.
- **GAP-KQ-002:** Compute:
  - accuracy proxy,
  - completeness,
  - consistency,
  - timeliness,
  - provenance coverage,
  - trust score,
  - orphan ratio,
  - duplication rate,
  - invalid-edge rate,
  - unresolved-identity rate,
  - stale-asset rate.
- **GAP-KQ-003:** Quality SLO violations generate actionable findings.
- **GAP-KQ-004:** Quality score is not one opaque number; show component dimensions.
- **GAP-KQ-005:** Quality must be measurable by source, project, graph, domain and release.
- **GAP-KQ-006:** Support trend charts and regression gates.

---

# 13. Semantic Drift Detection

## Requirements

- **GAP-DRIFT-001:** Detect source schema drift.
- **GAP-DRIFT-002:** Detect ontology drift.
- **GAP-DRIFT-003:** Detect vocabulary usage drift.
- **GAP-DRIFT-004:** Detect relationship distribution shifts.
- **GAP-DRIFT-005:** Detect embedding-space drift if vector retrieval is used.
- **GAP-DRIFT-006:** Detect code architecture drift from intended ontology/architecture.
- **GAP-DRIFT-007:** Generate drift explanations and affected assets.

---

# 14. Architecture Conformance Engine

This should become a major engineering differentiator.

## Requirements

- **GAP-ARCH-001:** Allow architecture rules such as:
  - service A may not depend on service B,
  - UI layer cannot access database directly,
  - domain X may consume only public APIs of domain Y,
  - critical components require tests,
  - regulated data cannot cross boundary Z.
- **GAP-ARCH-002:** Evaluate actual code/deployment graph against intended architecture.
- **GAP-ARCH-003:** Show violations in Web UI and VS Code.
- **GAP-ARCH-004:** Support CI gate mode.
- **GAP-ARCH-005:** Link violation to exact code symbols/commits.
- **GAP-ARCH-006:** Provide trend and technical-debt history.

---

# 15. Change Intelligence & Semantic Blast Radius

## Requirements

- **GAP-CHANGE-001:** Analyze a proposed code change before merge.
- **GAP-CHANGE-002:** Analyze a Jira/change request before implementation.
- **GAP-CHANGE-003:** Traverse code, service, test, deployment, ownership and incident relationships.
- **GAP-CHANGE-004:** Categorize impact:
  - direct,
  - transitive,
  - runtime,
  - data,
  - API,
  - documentation,
  - compliance,
  - ownership.
- **GAP-CHANGE-005:** Provide confidence and supporting paths.
- **GAP-CHANGE-006:** Compare predicted impact with actual post-deployment incidents to calibrate the model.

---

# 16. Temporal / Bitemporal Knowledge

## Requirements

- **GAP-TEMP-001:** Support event time and system/ingestion time.
- **GAP-TEMP-002:** Query “what was known at time T?”
- **GAP-TEMP-003:** Query “what was actually valid at time T?”
- **GAP-TEMP-004:** Support historical topology reconstruction.
- **GAP-TEMP-005:** Retain semantic changes without overwriting history.
- **GAP-TEMP-006:** Graph diffs must be first-class objects.

---

# 17. Knowledge Catalog & Knowledge Products

## Requirements

- **GAP-KP-001:** Catalog every graph, ontology, data source, connector, model, query, agent and knowledge product.
- **GAP-KP-002:** A Knowledge Product defines:
  - owner,
  - domain,
  - source graphs,
  - ontology version,
  - quality SLO,
  - freshness SLO,
  - access policy,
  - APIs,
  - dashboards,
  - consumers.
- **GAP-KP-003:** Product states: Draft, Experimental, Trusted, Certified, Deprecated.
- **GAP-KP-004:** Product lineage must be navigable.
- **GAP-KP-005:** Export/import product definitions.

---

# 18. Ontology Studio & Collaborative Knowledge Engineering

## Requirements

- **GAP-STUDIO-001:** Visual class/property/relationship editor.
- **GAP-STUDIO-002:** Text source view for experts.
- **GAP-STUDIO-003:** SHACL-style validation rules.
- **GAP-STUDIO-004:** RDFS/OWL export.
- **GAP-STUDIO-005:** SKOS taxonomy support.
- **GAP-STUDIO-006:** Diff/merge.
- **GAP-STUDIO-007:** Comments and review workflow.
- **GAP-STUDIO-008:** Reusable ontology modules.
- **GAP-STUDIO-009:** Crosswalk/mapping designer.
- **GAP-STUDIO-010:** Impact preview before publish.
- **GAP-STUDIO-011:** Generate forms and API schemas from ontology where practical.

---

# 19. Enterprise Entity Resolution Workbench

## Requirements

- **GAP-ER-001:** Deterministic match rules.
- **GAP-ER-002:** Probabilistic/fuzzy match.
- **GAP-ER-003:** Configurable match features.
- **GAP-ER-004:** Explain match score.
- **GAP-ER-005:** Candidate queue for human review.
- **GAP-ER-006:** Merge/unmerge.
- **GAP-ER-007:** Golden entity record.
- **GAP-ER-008:** Source aliases.
- **GAP-ER-009:** Historical identity evolution.
- **GAP-ER-010:** No irreversible automatic merge below confidence threshold.

---

# 20. Federated Knowledge Fabric

## Requirements

- **GAP-FABRIC-001:** Query materialized HugeGraph data and selected external sources in one plan.
- **GAP-FABRIC-002:** Source capability registry.
- **GAP-FABRIC-003:** Cost-aware query routing.
- **GAP-FABRIC-004:** Push filters/projections to source where possible.
- **GAP-FABRIC-005:** Local result cache with provenance/freshness.
- **GAP-FABRIC-006:** Offline degradation strategy.
- **GAP-FABRIC-007:** Explain query routing.
- **GAP-FABRIC-008:** Enforce source-level data policies.

---

# 21. Unified Retrieval Fabric

## Requirements

One request may require graph, keyword, vector, source API or code-symbol retrieval.

- **GAP-RET-001:** Implement retrieval router.
- **GAP-RET-002:** Candidate retrievers:
  - graph traversal,
  - keyword/full-text,
  - vector,
  - hybrid,
  - code-symbol,
  - provenance,
  - temporal,
  - source federation.
- **GAP-RET-003:** Rank using evidence quality, recency, authority and relevance.
- **GAP-RET-004:** Query planner chooses minimal sufficient retrieval path.
- **GAP-RET-005:** Evaluate retrievers independently.
- **GAP-RET-006:** Provide retrieval trace for debugging.

---

# 22. Knowledge-Aware GraphRAG

## Requirements

- **GAP-KRAG-001:** Retrieval must be ontology-aware.
- **GAP-KRAG-002:** Favor authoritative graph facts over generated summaries.
- **GAP-KRAG-003:** Community summaries must link to underlying nodes/edges.
- **GAP-KRAG-004:** Incremental community update.
- **GAP-KRAG-005:** Temporal filtering.
- **GAP-KRAG-006:** Contradiction-aware context assembly.
- **GAP-KRAG-007:** Answer abstention when evidence is insufficient.
- **GAP-KRAG-008:** Confidence calibrated from evidence—not model self-confidence.
- **GAP-KRAG-009:** Every response includes evidence manifest.
- **GAP-KRAG-010:** Local model routing by task complexity.

---

# 23. Agentic Knowledge Operations

## Requirements

Agents should not just “chat”; they should safely operate on knowledge workflows.

- **GAP-AKO-001:** Knowledge Curator Agent.
- **GAP-AKO-002:** Ontology Reviewer Agent.
- **GAP-AKO-003:** Data Quality Agent.
- **GAP-AKO-004:** Connector Diagnosis Agent.
- **GAP-AKO-005:** Change Impact Agent.
- **GAP-AKO-006:** Architecture Conformance Agent.
- **GAP-AKO-007:** Incident Investigation Agent.
- **GAP-AKO-008:** Documentation Freshness Agent.
- **GAP-AKO-009:** Evidence Verification Agent.
- **GAP-AKO-010:** Query Optimization Agent.

All must operate through bounded tools, budgets, audit and human policy.

---

# 24. Agent & MCP Governance

## Requirements

- **GAP-AGOV-001:** Tool registry with versioned schemas.
- **GAP-AGOV-002:** Read/write/destructive risk classification.
- **GAP-AGOV-003:** Capability tokens or equivalent scoped tool authorization in future enterprise phases.
- **GAP-AGOV-004:** Human approval policy by risk.
- **GAP-AGOV-005:** Per-agent time/step/tool/model budgets.
- **GAP-AGOV-006:** Prompt-injection detection.
- **GAP-AGOV-007:** Tool-output sanitization.
- **GAP-AGOV-008:** MCP server allowlist.
- **GAP-AGOV-009:** Complete action provenance.
- **GAP-AGOV-010:** Replayable agent execution traces excluding private chain-of-thought.
- **GAP-AGOV-011:** Deterministic dry-run mode.
- **GAP-AGOV-012:** Agent evaluation gates before promotion.

---

# 25. Knowledge Firewall

A differentiating security capability.

## Requirements

- **GAP-KFW-001:** Inspect all context leaving a knowledge boundary.
- **GAP-KFW-002:** Detect secrets, PII, credentials, regulated data and restricted classifications.
- **GAP-KFW-003:** Block or redact based on policy.
- **GAP-KFW-004:** Prevent source text from becoming executable agent instructions.
- **GAP-KFW-005:** Tag untrusted/externally sourced graph content.
- **GAP-KFW-006:** Defend against graph poisoning and semantic prompt injection.
- **GAP-KFW-007:** Maintain security provenance.
- **GAP-KFW-008:** Provide “why blocked/redacted?” explanation.

---

# 26. Knowledge Quarantine & Trust Zones

## Requirements

- **GAP-TRUST-001:** New/inferred/untrusted knowledge enters a quarantine zone.
- **GAP-TRUST-002:** Promotion requires rules, confidence or approval.
- **GAP-TRUST-003:** Trust states:
  - Raw,
  - Parsed,
  - Inferred,
  - Reviewed,
  - Trusted,
  - Certified,
  - Rejected.
- **GAP-TRUST-004:** Queries may specify minimum trust level.
- **GAP-TRUST-005:** AI answers must disclose use of non-certified knowledge.

---

# 27. Fine-Grained Security Roadmap

Although MVP intentionally excludes RBAC, commercial enterprise phases should add:

- SSO/OIDC/SAML.
- LDAP/Active Directory.
- RBAC.
- ABAC.
- Graph-level access.
- Node/edge/property-level policy where required.
- Source-derived security inheritance.
- Row/record-level filtering.
- Query audit.
- Service accounts.
- API keys/token rotation.
- policy-as-code.

Requirements:
- **GAP-SEC-001** through **GAP-SEC-012** reserved for enterprise security implementation.

---

# 28. Data & Knowledge Lineage Interoperability

## Requirements

- **GAP-LIN-001:** Map internal lineage to OpenLineage concepts where applicable.
- **GAP-LIN-002:** Map semantic provenance to PROV-O where applicable.
- **GAP-LIN-003:** Keep internal richer model without losing standards compatibility.
- **GAP-LIN-004:** Ingest lineage events from CI/CD and data pipelines.
- **GAP-LIN-005:** Emit lineage events for platform transformations.

---

# 29. Graph Change Data Capture

## Requirements

- **GAP-CDC-001:** Every graph mutation emits an internal event.
- **GAP-CDC-002:** Event includes before/after semantic identity.
- **GAP-CDC-003:** Consumers can subscribe to entity/edge/domain changes.
- **GAP-CDC-004:** Support incremental search/vector/index synchronization.
- **GAP-CDC-005:** Support incremental GraphRAG summary update.
- **GAP-CDC-006:** Replay from checkpoint.

---

# 30. Knowledge Graph CI/CD

## Requirements

Pipeline:

`lint → schema validation → contract test → sample ingest → SHACL-like validation → graph invariant tests → quality gates → compatibility checks → security checks → migration simulation → publish`

- **GAP-KGCI-001:** CLI runnable in CI.
- **GAP-KGCI-002:** Machine-readable report.
- **GAP-KGCI-003:** Fail build on configured semantic regression.
- **GAP-KGCI-004:** Generate versioned ontology artifact.

---

# 31. Graph Testing Framework

## Requirements

Provide test DSL/framework for:
- expected path,
- forbidden path,
- cardinality,
- required relationship,
- no orphan,
- no cycle,
- data type,
- ownership,
- provenance,
- temporal validity,
- architecture boundary,
- traceability coverage.

Tests must run locally and in CI.

---

# 32. Graph Observability

Use OpenTelemetry-compatible telemetry where practical.

## Requirements

- **GAP-OBS-001:** Trace a request from UI → API → planner → HugeGraph → retriever → model → response.
- **GAP-OBS-002:** Trace ingestion from source record → entity → edge → index.
- **GAP-OBS-003:** Metrics per connector/query/agent/retriever.
- **GAP-OBS-004:** Correlate logs, metrics and traces.
- **GAP-OBS-005:** Graph-specific metrics:
  - traversal fanout,
  - visited vertices,
  - visited edges,
  - cache hit rate,
  - index utilization,
  - semantic validation time.

---

# 33. Query Intelligence

## Requirements

- **GAP-QI-001:** Query plan explain.
- **GAP-QI-002:** Cost estimation.
- **GAP-QI-003:** Query history.
- **GAP-QI-004:** Slow-query analyzer.
- **GAP-QI-005:** Suggested indexes.
- **GAP-QI-006:** Traversal-risk detector.
- **GAP-QI-007:** Saved parameterized query templates.
- **GAP-QI-008:** Natural-language query produces editable structured plan before execution when risk is high.

---

# 34. Semantic Cache

## Requirements

- **GAP-CACHE-001:** Cache by normalized semantic intent/query plan rather than raw prompt only.
- **GAP-CACHE-002:** Cache dependencies reference graph versions/source freshness.
- **GAP-CACHE-003:** Invalidate using graph CDC.
- **GAP-CACHE-004:** Separate deterministic query cache from AI response cache.
- **GAP-CACHE-005:** Do not serve stale results beyond policy.

---

# 35. Knowledge Compaction & Lifecycle

## Requirements

- **GAP-LIFE-001:** Tier hot/warm/archive graph information.
- **GAP-LIFE-002:** Archive historical facts without losing lineage.
- **GAP-LIFE-003:** Expire transient agent memory separately from enterprise facts.
- **GAP-LIFE-004:** Retention policies per domain/classification.
- **GAP-LIFE-005:** Purge with provenance record where legally allowed.
- **GAP-LIFE-006:** Rebuild derived data from authoritative inputs.

---

# 36. Schema & Mapping Marketplace

Internal enterprise marketplace, not public SaaS.

## Requirements

- **GAP-MKT-001:** Package reusable ontology modules.
- **GAP-MKT-002:** Package connector mappings.
- **GAP-MKT-003:** Package query templates.
- **GAP-MKT-004:** Package validation rules.
- **GAP-MKT-005:** Package agent workflows.
- **GAP-MKT-006:** Package dashboards.
- **GAP-MKT-007:** Dependency/version management.
- **GAP-MKT-008:** Signed packages in later phases.

---

# 37. Domain Packs

Provide optional prebuilt ontology/relationship packs for:

- software engineering,
- ITSM,
- BFSI,
- telecom,
- healthcare,
- manufacturing,
- cybersecurity,
- data governance,
- compliance,
- supply chain.

Each pack must extend, not fork, the core ontology.

---

# 38. Enterprise Search Experience

## Requirements

Single search should find:
- Jira,
- code symbols,
- commits,
- documents,
- services,
- incidents,
- people,
- teams,
- ontology terms,
- APIs,
- deployments,
- knowledge products.

Results should support:
- semantic facets,
- graph-neighborhood preview,
- evidence,
- authority,
- freshness,
- ownership,
- trust state,
- “why this result”.

---

# 39. Expert Finder / Organizational Knowledge

## Requirements

Infer expertise carefully from evidence:
- contributions,
- ownership,
- reviewed MRs,
- Jira history,
- documents,
- incidents.

Never infer sensitive personal attributes.

Provide:
- expertise evidence,
- recency,
- project/domain filters,
- team-level alternatives.

---

# 40. Knowledge Freshness Engine

## Requirements

- **GAP-FRESH-001:** Detect stale documents.
- **GAP-FRESH-002:** Detect docs contradicted by code/config/runtime.
- **GAP-FRESH-003:** Detect ownership changes.
- **GAP-FRESH-004:** Detect deprecated APIs still referenced in docs.
- **GAP-FRESH-005:** Recommend review—not silently rewrite authoritative docs.

---

# 41. Semantic Diff & Release Intelligence

## Requirements

Every release should generate:
- graph delta,
- ontology delta,
- code delta,
- service/deployment delta,
- risk delta,
- ownership delta,
- docs delta,
- traceability delta.

Provide “What changed semantically?” rather than only file diffs.

---

# 42. Graph Simulation / What-If Engine

## Requirements

- Fork a graph snapshot.
- Apply hypothetical changes.
- Run blast-radius and policy validation without changing production graph.
- Compare predicted topology.
- Allow simulation for:
  - API removal,
  - library upgrade,
  - team ownership transfer,
  - service split,
  - dependency replacement,
  - ontology change.

---

# 43. Knowledge Graph Benchmark Harness

## Requirements

Create reproducible benchmark suites for:
- ingestion,
- update,
- point lookup,
- 1–N hop traversal,
- shortest path,
- impact analysis,
- temporal query,
- hybrid retrieval,
- GraphRAG,
- concurrent query,
- graph validation.

Publish hardware + data size + configuration with every benchmark.

Never advertise unsupported performance claims.

---

# 44. HugeGraph-Specific Hardening

Apache HugeGraph documentation describes standalone RocksDB and distributed HStore modes, TinkerPop/Gremlin compliance, schema/index management and large graph scale.

## Requirements

- **GAP-HG-001:** Abstract HugeGraph client behind repository interface.
- **GAP-HG-002:** Automated schema migration.
- **GAP-HG-003:** Index advisor.
- **GAP-HG-004:** Bulk-loader path.
- **GAP-HG-005:** Online ingestion path.
- **GAP-HG-006:** standalone → distributed migration playbook.
- **GAP-HG-007:** backup/restore verification.
- **GAP-HG-008:** capacity benchmark before production.
- **GAP-HG-009:** Gremlin query safety.
- **GAP-HG-010:** avoid pretending SPARQL/RDF is native; use explicit semantic adapter.

---

# 45. Product Extensibility

## Requirements

SDKs:
- Connector SDK
- Parser SDK
- Entity Resolver SDK
- Relationship Extractor SDK
- Ontology Module SDK
- Query Function SDK
- Retriever SDK
- Agent SDK
- MCP Tool SDK
- UI Widget SDK
- Validation Rule SDK

Extensions must have manifests, versions, capabilities and compatibility metadata.

---

# 46. Enterprise Packaging

Add installable profiles:

### Developer
Single machine, Docker Compose, synthetic/sample data.

### Team
Single server, backups, multiple connectors.

### Enterprise
Distributed HugeGraph, SSO/RBAC later, HA, observability, policy engine.

### Air-Gapped
Offline images, offline model packages, offline dependency bundle, SBOM, signed manifests.

---

# 47. Operational Excellence

Requirements:
- one-command preflight check,
- configuration validator,
- upgrade planner,
- migration dry run,
- rollback,
- health bundle,
- support bundle,
- diagnostic snapshots,
- offline upgrade package,
- reproducible environment manifest.

---

# 48. Security Beyond MVP

Future enterprise release must include:
- SSO,
- LDAP/AD,
- OIDC/SAML,
- RBAC,
- ABAC,
- graph-level security,
- data-classification inheritance,
- source permission synchronization,
- encryption at rest,
- TLS,
- secret rotation,
- audit retention,
- signed extensions,
- supply-chain verification.

---

# 49. Responsible AI & Model Governance

## Requirements

- model registry,
- model version,
- local model health,
- approved model list,
- prompt/template registry,
- evaluation dataset,
- regression test,
- groundedness threshold,
- unsafe action threshold,
- abstention policy,
- AI feature kill switch,
- model-output classification,
- hallucination incident logging.

---

# 50. Explainability Without Chain-of-Thought

Requirements:
- Evidence path
- Data provenance
- Query plan
- Tool calls
- Rules fired
- Confidence inputs
- Human approvals
- Source freshness

Do not require exposing hidden model chain-of-thought.

---

# 51. “Why / Why Not / What If” Native Queries

The query engine must support:

- Why is A linked to B?
- Why was this result returned?
- Why was this result excluded?
- Why is this fact considered trusted?
- Why does this change affect service X?
- What evidence supports this answer?
- What if dependency X is removed?
- What changed since version Y?

These should be first-class product operations, not prompt tricks.

---

# 52. Requirement Priority

## P0 — Core differentiation
1. Semantic Digital Thread
2. Provenance/Evidence Ledger
3. Ontology GitOps
4. Graph quality SLOs
5. Architecture Conformance
6. Change Intelligence / Blast Radius
7. Unified Retrieval Fabric
8. Evidence-grounded GraphRAG
9. HugeGraph hardening
10. Enterprise connector reliability
11. Ontology Studio
12. Knowledge Catalog
13. Graph testing/CI
14. Air-gapped deployment
15. Agent/MCP governance

## P1 — Enterprise maturity
- Federation/virtualization
- temporal/bitemporal graph
- entity-resolution workbench
- trust zones
- semantic drift
- Graph CDC
- knowledge-product framework
- SSO/RBAC/ABAC
- HA
- advanced search/vector
- observability
- simulation

## P2 — Advanced differentiation
- semantic app builder
- internal marketplace
- domain packs
- recommendation
- expert finder
- agentic knowledge operations
- self-optimization under governance
- advanced community summarization

---

# 53. Commercial Differentiators to Target

Do not claim these until implemented and benchmarked. They are product targets.

1. **One graph from business intent to production runtime**
2. **Property-graph performance + standards-based semantic interoperability**
3. **Local-first / air-gapped AI**
4. **Every AI answer evidence-backed**
5. **Ontology GitOps**
6. **Architecture conformance directly against code**
7. **Semantic blast radius before change**
8. **Trust-aware knowledge**
9. **Knowledge-quality SLOs**
10. **One experience for business, architect, developer, ops and AI**
11. **MCP-native enterprise knowledge control plane**
12. **No mandatory cloud dependency**
13. **Progressive deployment from laptop to distributed production**
14. **Open export formats to reduce lock-in**
15. **Deterministic-first, AI-when-useful architecture**

---

# 54. Requirements Traceability Template

Every GAP requirement must map to:

| Requirement | Component | API/Event | Data Model | Phase | Test | Acceptance |
|---|---|---|---|---|---|---|
| GAP-SDT-001 | Digital Thread Engine | `/api/v1/trace` | TraceEdge | P1 | E2E-SDT-001 | Requirement-to-runtime path shown |
| GAP-PROV-006 | Evidence Service | `/api/v1/evidence` | EvidenceManifest | P1 | INT-EVID-006 | Every AI answer has evidence |
| GAP-GITOPS-003 | Ontology GitOps | CLI/API | SemanticDiff | P2 | UNIT-DIFF-* | Semantic changes correctly classified |

---

# 55. Non-Functional Targets

Numbers should be finalized only after benchmark datasets are agreed.

Mandatory categories:
- availability,
- durability,
- query p50/p95/p99,
- ingestion throughput,
- recovery time,
- recovery point,
- connector freshness,
- graph-quality SLO,
- evidence coverage,
- agent success rate,
- retrieval accuracy,
- GraphRAG groundedness,
- upgrade rollback time,
- maximum tolerated stale cache,
- maximum query traversal depth by class.

---

# 56. Important Product Principle

“Best of the best” must not mean “largest feature list.”

The product should win by **integrating capabilities that competitors often solve in separate layers**:

`Sources → Canonicalization → Ontology → Knowledge Graph → Provenance → Quality → Query → Search → GraphRAG → Agents → Human Governance → IDE/Web/MCP`

with one evidence and policy model across the entire path.

---

# 57. Research References

**R1 — Apache HugeGraph official GitHub/README (Apache Software Foundation, accessed 2026-10-01).**  
Documents TinkerPop/Gremlin compatibility, schema/index management, RocksDB standalone and HStore distributed deployment.

**R2 — Stardog documentation: Virtual Graphs, Knowledge Catalog, platform/pricing pages (accessed 2026-10-01).**  
Documents virtualized mappings, query rewriting, catalog metadata, on-premise deployment and enterprise features.

**R3 — Neo4j Operations Manual, Graph Data Science documentation and neosemantics documentation (accessed 2026-10-01).**  
Documents clustering/backup, GDS in-memory graph catalog/analytics, licensing boundaries and RDF/OWL/SKOS/SHACL support through neosemantics.

**R4 — Ontotext GraphDB 11.x documentation (accessed 2026-10-01).**  
Documents SPARQL, forward-chaining reasoning, rules, FTS connectors, OpenSearch/vector integration and enterprise security/HA features.

**R5 — TopQuadrant TopBraid EDG/TQ Data Foundation documentation (accessed 2026-10-01).**  
Documents SHACL-centered ontology management, RDFS/OWL conversion, GraphQL generation, asset governance and HA deployment model.

**R6 — PoolParty Semantic Suite documentation/product matrix (accessed 2026-10-01).**  
Documents taxonomy/ontology management, NLP/extraction, semantic search, modular packaging and enterprise features.

**R7 — Cambridge Semantics Anzo / Graph Studio documentation (accessed 2026-10-01).**  
Documents semantic models, data blending/Graphmarts, dataset catalog/lineage and deployment sizing.

**R8 — metaphacts metaphactory public documentation/product materials (accessed 2026-10-01).**  
Documents semantic modeling, data management, app development, federation, search and visualization.

**R9 — data.world product documentation (accessed 2026-10-01).**  
Documents graph-powered catalog, curation, lineage, glossary and governance.

**R10 — Amazon Neptune documentation (accessed 2026-10-01).**  
Documents Gremlin/openCypher/SPARQL support and managed HA/backup model; property graph and RDF query models are distinct.

**R11 — Oracle RDF Graph documentation (accessed 2026-10-01).**  
Documents RDF/RDFS/OWL integration within Oracle Database.

**R12 — Microsoft GraphRAG GitHub/documentation (accessed 2026-10-01).**  
Documents entity/relationship/claim extraction, community detection, hierarchical summaries and indexing caveats.

**R13 — W3C SHACL Recommendation.**  
Defines validation of RDF graphs using shapes and constraints.

**R14 — W3C PROV-O Recommendation.**  
Defines interoperable representation of entities, activities, agents and provenance.

**R15 — OpenLineage specification.**  
Defines job/run/dataset lineage events and extension facets.

**R16 — OpenTelemetry specification.**  
Defines vendor-neutral traces, metrics and logs.

**R17 — Wang et al., “Knowledge graph quality control: A survey,” 2021.**  
Discusses multidimensional KG quality including accuracy, completeness, consistency, timeliness, trustworthiness and availability.

**R18 — Issa et al., “Knowledge Graph Completeness: A Systematic Literature Review,” IEEE Access, 2021.**  
Reviews completeness and broader KG quality dimensions.

---

# 58. Final Requirement

No competitor feature should be added merely to make a comparison matrix look complete.

A capability is accepted into the platform only when it:
1. advances a target enterprise use case,
2. fits the local-first architecture,
3. has an owner,
4. has measurable acceptance criteria,
5. has a test strategy,
6. has a lifecycle/upgrade model,
7. has documented security implications,
8. integrates with provenance and observability,
9. does not break the MVP’s evolutionary architecture.

