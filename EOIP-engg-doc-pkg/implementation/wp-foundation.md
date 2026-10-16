# WP-FOUNDATION Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-FOUNDATION

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-GRAPH-001 | HugeGraph authoritative store | P1-MVP | All demo graph paths survive service restart. |
| FR-GRAPH-002 | Logical graph domains | P1-MVP | Every business vertex/edge belongs to a valid domain. |
| FR-GRAPH-003 | Schema bootstrap | P1-MVP | Fresh stack auto-initializes and second run is no-op. |
| FR-GRAPH-004 | Canonical identifiers | P1-MVP | Every canonical entity has unique stable canonical_id. |
| NFR-MAINT-001 | Modular monolith boundary | P1-MVP | Core can later split without changing external contracts. |

## Implementation sequence

### WP-FOUNDATION-01 — HugeGraph authoritative store
**Objective:** Use Apache HugeGraph as the authoritative property graph and ontology operational store.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** HugeGraph schema/Gremlin  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Graph unavailable returns degraded/readiness failure; no shadow DB fallback.  
**Tests:** Startup and persistence tests.  
**Acceptance:** All demo graph paths survive service restart.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-001`.
### WP-FOUNDATION-02 — Logical graph domains
**Objective:** Represent Jira, Code, Docs, CI, Provenance, Meta and other domains explicitly within the graph.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** graph_domain, GraphDomain node  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unknown domain is rejected by schema policy.  
**Tests:** Domain integrity tests.  
**Acceptance:** Every business vertex/edge belongs to a valid domain.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-002`.
### WP-FOUNDATION-03 — Schema bootstrap
**Objective:** Initialize property keys, vertex labels, edge labels and indexes idempotently.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Schema manifest  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Incompatible migration fails startup of app mutation path but preserves DB.  
**Tests:** Fresh/repeat/incompatible schema tests.  
**Acceptance:** Fresh stack auto-initializes and second run is no-op.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-003`.
### WP-FOUNDATION-04 — Canonical identifiers
**Objective:** Define deterministic IDs independent of HugeGraph internal IDs where possible.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** canonical_id/source_id/source_system  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Collision is a blocking validation error.  
**Tests:** Collision/idempotency tests.  
**Acceptance:** Every canonical entity has unique stable canonical_id.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-004`.
### WP-FOUNDATION-05 — Modular monolith boundary
**Objective:** Use modular monolith services in Phase 1; split only on evidence.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Python package boundaries  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Cross-module direct DB access rejected by architecture tests/convention.  
**Tests:** Dependency/lint tests.  
**Acceptance:** Core can later split without changing external contracts.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-MAINT-001`.
