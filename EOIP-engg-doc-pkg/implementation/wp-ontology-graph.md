# WP-ONTOLOGY-GRAPH Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-ONTOLOGY-GRAPH

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-GRAPH-005 | Meta graph | P1-MVP | Admin statistics are derived from graph/meta records. |
| FR-GRAPH-006 | Cross-domain bridge edges | P1-MVP | Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable. |
| FR-GRAPH-008 | Index strategy | P1-MVP | Benchmark-critical lookup paths use planned indexes. |
| FR-GRAPH-009 | Graph version journal | P1-MVP | Each changed fact can be attributed to a run/version. |
| FR-GRAPH-010 | RDF/OWL interoperability | P2 | No documentation claims native SPARQL support. |
| FR-ONTO-001 | Enterprise ontology vocabulary | P1-MVP | MVP entities/edges reference ontology version and valid terms. |
| FR-ONTO-002 | Relationship semantics | P1-MVP | No MVP business relationship relies on untyped generic edge. |
| FR-PROV-001 | Evidence model | P1-MVP | MVP evidence coverage is 100% for cross-domain bridge edges. |
| FR-PROV-002 | Provenance traversal | P1-MVP | User can trace demo answer to source fixture/commit metadata. |
| FR-ID-001 | Deterministic identity resolution | P1-MVP | Exact aliases merge predictably and retain source aliases. |
| FR-ID-002 | Ambiguous identity candidates | P1-MVP | No fuzzy-only match produces same canonical_id automatically. |
| FR-TEMP-001 | Bitemporal-ready fields | P1-MVP | MVP schema is ready for P5 without ID rewrite. |

## Implementation sequence

### WP-ONTOLOGY-GRAPH-01 — Meta graph
**Objective:** Model datasets, sources, graph domains, schema/ontology versions, ingestion runs, quality and lineage metadata.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Meta entities/edges  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Stale meta state is validation finding.  
**Tests:** Meta traversal tests.  
**Acceptance:** Admin statistics are derived from graph/meta records.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-005`.
### WP-ONTOLOGY-GRAPH-02 — Cross-domain bridge edges
**Objective:** Create explicit, evidence-backed edges between work, code, CI and documents.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** IMPLEMENTS, MODIFIES, REFERENCES, DOCUMENTS, PRODUCED_BY  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Low-confidence inference never becomes deterministic truth.  
**Tests:** Synthetic E2E path assertions.  
**Acceptance:** Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-006`.
### WP-ONTOLOGY-GRAPH-03 — Index strategy
**Objective:** Create indexes only for measured access patterns.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** HugeGraph IndexLabels  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Index bootstrap mismatch blocks incompatible mutation.  
**Tests:** Query-plan benchmark tests.  
**Acceptance:** Benchmark-critical lookup paths use planned indexes.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-008`.
### WP-ONTOLOGY-GRAPH-04 — Graph version journal
**Objective:** Record mutation run, schema/ontology version, first/last seen and validity metadata.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** revision fields, IngestionRun  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Missing version metadata is validation error.  
**Tests:** Replay/version tests.  
**Acceptance:** Each changed fact can be attributed to a run/version.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-009`.
### WP-ONTOLOGY-GRAPH-05 — RDF/OWL interoperability
**Objective:** Export platform ontology/data through explicit adapters rather than claiming native RDF/SPARQL.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** RDF/OWL mapping  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unsupported construct reports mapping loss.  
**Tests:** Round-trip fixtures where possible.  
**Acceptance:** No documentation claims native SPARQL support.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-010`.
### WP-ONTOLOGY-GRAPH-06 — Enterprise ontology vocabulary
**Objective:** Version organization, work, code, CI/CD, operations, knowledge and AI/agent concepts.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Ontology manifest  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unknown/deprecated term creates validation error/warning.  
**Tests:** Ontology conformance tests.  
**Acceptance:** MVP entities/edges reference ontology version and valid terms.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-ONTO-001`.
### WP-ONTOLOGY-GRAPH-07 — Relationship semantics
**Objective:** Distinguish containment, identity, dependency, implementation, authorship, provenance, temporal and cross-domain semantics.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Edge manifest  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Invalid endpoints rejected or quarantined.  
**Tests:** Edge domain/range tests.  
**Acceptance:** No MVP business relationship relies on untyped generic edge.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-ONTO-002`.
### WP-ONTOLOGY-GRAPH-08 — Evidence model
**Objective:** Attach source reference, event hash, extraction time, mapper/parser version, confidence and creation status.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Evidence v1  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Missing evidence makes inferred fact invalid.  
**Tests:** Provenance coverage tests.  
**Acceptance:** MVP evidence coverage is 100% for cross-domain bridge edges.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-PROV-001`.
### WP-ONTOLOGY-GRAPH-09 — Provenance traversal
**Objective:** Support reverse traversal from graph fact to source event and ingestion run.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Evidence, SourceEvent, IngestionRun  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Missing source artifact is reported, not hidden.  
**Tests:** Lineage API E2E.  
**Acceptance:** User can trace demo answer to source fixture/commit metadata.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-PROV-002`.
### WP-ONTOLOGY-GRAPH-10 — Deterministic identity resolution
**Objective:** Resolve exact emails, canonical source IDs and configured aliases before fuzzy methods.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** IdentityCandidate  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Conflict preserved as separate nodes.  
**Tests:** Alias/conflict tests.  
**Acceptance:** Exact aliases merge predictably and retain source aliases.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-ID-001`.
### WP-ONTOLOGY-GRAPH-11 — Ambiguous identity candidates
**Objective:** Never silently merge low-confidence fuzzy matches.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** IdentityCandidate  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Ambiguous candidates remain separate.  
**Tests:** Fuzzy boundary tests.  
**Acceptance:** No fuzzy-only match produces same canonical_id automatically.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-ID-002`.
### WP-ONTOLOGY-GRAPH-12 — Bitemporal-ready fields
**Objective:** Store created/modified/deleted, first/last seen, valid_from/valid_to and source_version where available.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** temporal properties  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Invalid intervals generate validation findings.  
**Tests:** Temporal validation tests.  
**Acceptance:** MVP schema is ready for P5 without ID rewrite.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-TEMP-001`.
