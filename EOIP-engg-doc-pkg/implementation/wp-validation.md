# WP-VALIDATION Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-VALIDATION

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-VALID-001 | Graph validation rules | P1-MVP | Admin UI shows real findings from demo data. |
| FR-VALID-002 | Validation gates | P1-MVP | Invalid endpoint edge cannot silently enter graph. |
| FR-VALID-003 | Graph quality metrics | P1-MVP | Dashboard values reconcile with fixture counts. |

## Implementation sequence

### WP-VALIDATION-01 — Graph validation rules
**Objective:** Execute rule packs for orphan, endpoint/domain-range, duplicate, provenance, mandatory edge, type and dangling reference checks.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** ValidationRun/Finding  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Rule failure isolated and reported.  
**Tests:** Seeded-invalid-graph tests.  
**Acceptance:** Admin UI shows real findings from demo data.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-VALID-001`.
### WP-VALIDATION-02 — Validation gates
**Objective:** Block or quarantine mutations that violate hard invariants; soft rules run post-ingestion.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Rule policy  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Partial batches are rolled back or safely marked by mutation strategy.  
**Tests:** Hard/soft rule tests.  
**Acceptance:** Invalid endpoint edge cannot silently enter graph.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-VALID-002`.
### WP-VALIDATION-03 — Graph quality metrics
**Objective:** Compute completeness, freshness, orphan rate, duplicate rate, provenance/evidence coverage and schema compliance.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** QualitySnapshot  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unknown denominator reported as N/A, not false zero/100%.  
**Tests:** Metric fixture tests.  
**Acceptance:** Dashboard values reconcile with fixture counts.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-VALID-003`.
