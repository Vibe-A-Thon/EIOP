# WP-CONNECTORS Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-CONNECTORS

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-CONN-001 | Connector SDK | P1-MVP | A new connector can be added without editing ingestion core. |
| FR-CONN-002 | Jira JSON connector | P1-MVP | Repeat import is idempotent and creates expected graph. |
| FR-CONN-003 | Git repository connector | P1-MVP | Repository, branch and commit nodes plus modifications exist. |
| FR-CONN-004 | GitLab metadata adapter | P1-MVP | MR and pipeline records link to commits and work items. |
| FR-CONN-005 | Connector resiliency | P1-MVP | Restart resumes without duplicate canonical nodes. |
| FR-CONN-006 | Dry run and replay | P1-MVP | Same input/version produces same canonical mutations. |
| FR-CONN-007 | Source deletion semantics | P1-MVP | Deleted source is queryable historically and excluded from current views. |
| FR-CONF-001 | Confluence connector | P2 | Incremental sync and provenance pass. |
| FR-SNOW-001 | ServiceNow connector | P2 | Incremental sync and mappings pass. |

## Implementation sequence

### WP-CONNECTORS-01 — Connector SDK
**Objective:** Provide a versioned connector interface for discover, extract, checkpoint, health and replay.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** ConnectorConfig, SourceEvent, Checkpoint  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Connector isolation; retryable failures checkpoint; poison records to DLQ.  
**Tests:** Contract tests against a fake source.  
**Acceptance:** A new connector can be added without editing ingestion core.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CONN-001`.
### WP-CONNECTORS-02 — Jira JSON connector
**Objective:** Import configurable Jira JSON plus the synthetic MVP fixture.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** JSON file, mapping YAML, SourceEvent  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Malformed records rejected individually with evidence; run continues.  
**Tests:** Fixture, malformed, duplicate, resume tests.  
**Acceptance:** Repeat import is idempotent and creates expected graph.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CONN-002`.
### WP-CONNECTORS-03 — Git repository connector
**Objective:** Inspect local Git repositories without network access.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Local repository path, git metadata  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Invalid repo/path traversal rejected; repository errors do not corrupt prior data.  
**Tests:** Temporary repository integration tests.  
**Acceptance:** Repository, branch and commit nodes plus modifications exist.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CONN-003`.
### WP-CONNECTORS-04 — GitLab metadata adapter
**Objective:** Support GitLab-style MR/pipeline metadata from configurable API or local JSON fixture.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** MR/pipeline JSON, endpoint config  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Rate limits/retries/checkpoints; no hard-coded credential.  
**Tests:** Mock API and fixture contract tests.  
**Acceptance:** MR and pipeline records link to commits and work items.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CONN-004`.
### WP-CONNECTORS-05 — Connector resiliency
**Objective:** Implement pagination, retry/backoff, rate-limit handling, checkpointing and resume.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Checkpoint JSON, job state  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Bounded retries then DLQ/failure state.  
**Tests:** Fault-injection restart tests.  
**Acceptance:** Restart resumes without duplicate canonical nodes.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CONN-005`.
### WP-CONNECTORS-06 — Dry run and replay
**Objective:** Allow validation-only dry run and deterministic replay of captured source events.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** SourceEvent archive  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Invalid replay schema/version is quarantined.  
**Tests:** Golden-event replay tests.  
**Acceptance:** Same input/version produces same canonical mutations.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CONN-006`.
### WP-CONNECTORS-07 — Source deletion semantics
**Objective:** Represent source disappearance/deletion without silent hard delete.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Source version/tombstone  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Conflicting source state becomes validation finding.  
**Tests:** Deletion/reappearance tests.  
**Acceptance:** Deleted source is queryable historically and excluded from current views.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CONN-007`.
### WP-CONNECTORS-08 — Confluence connector
**Objective:** Add on-prem Confluence connector through Connector SDK.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Confluence API records  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Same connector failure model.  
**Tests:** Contract tests in P2.  
**Acceptance:** Incremental sync and provenance pass.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CONF-001`.
### WP-CONNECTORS-09 — ServiceNow connector
**Objective:** Add on-prem ServiceNow incident/problem/change/KB connector.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** ServiceNow table API  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Rate limits and schema drift isolated.  
**Tests:** Contract tests in P2.  
**Acceptance:** Incremental sync and mappings pass.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-SNOW-001`.
