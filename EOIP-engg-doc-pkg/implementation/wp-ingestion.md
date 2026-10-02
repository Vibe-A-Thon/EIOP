# WP-INGESTION Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-INGESTION

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-INGEST-001 | Raw capture | P1-MVP | Every graph mutation references a captured event. |
| FR-INGEST-002 | Canonicalization | P1-MVP | Same source record maps deterministically for same mapper version. |
| FR-INGEST-003 | Idempotent mutation | P1-MVP | Second identical run does not increase logical entity/edge counts. |
| FR-INGEST-004 | Ingestion job lifecycle | P1-MVP | Admin UI reflects actual backend run state. |
| FR-INGEST-005 | Dead-letter processing | P1-MVP | Rejected records are inspectable and replayable. |

## Implementation sequence

### WP-INGESTION-01 — Raw capture
**Objective:** Persist immutable local SourceEvent envelopes before normalization.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** SourceEvent v1  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Disk-full fails job before graph mutation of uncaptured record.  
**Tests:** Hash/replay/restart tests.  
**Acceptance:** Every graph mutation references a captured event.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-INGEST-001`.
### WP-INGESTION-02 — Canonicalization
**Objective:** Normalize source events into typed canonical entities/relationships.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Canonical JSON contracts  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Mapper errors are per-record findings/DLQ.  
**Tests:** Golden mapping tests.  
**Acceptance:** Same source record maps deterministically for same mapper version.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-INGEST-002`.
### WP-INGESTION-03 — Idempotent mutation
**Objective:** Use deterministic canonical IDs and mutation upserts.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** GraphMutation v1  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Conflict surfaces validation finding; no blind merge.  
**Tests:** Double-ingest E2E.  
**Acceptance:** Second identical run does not increase logical entity/edge counts.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-INGEST-003`.
### WP-INGESTION-04 — Ingestion job lifecycle
**Objective:** Track queued/running/succeeded/partial/failed/cancelled states.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** IngestionRun  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Worker crash leaves resumable state.  
**Tests:** State-transition tests.  
**Acceptance:** Admin UI reflects actual backend run state.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-INGEST-004`.
### WP-INGESTION-05 — Dead-letter processing
**Objective:** Store rejected events locally with reason/evidence and replay controls.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** DLQ envelope  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Secrets/PII are not duplicated beyond allowed capture.  
**Tests:** Malformed fixtures.  
**Acceptance:** Rejected records are inspectable and replayable.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-INGEST-005`.
