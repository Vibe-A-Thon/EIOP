# WP-EXPERIENCE Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-EXPERIENCE

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-UI-001 | User web application | P1-MVP | Demo flow works from persisted data. |
| FR-UI-002 | Graph explorer | P1-MVP | Demo path is highlighted with evidence access. |
| FR-ADMIN-001 | Admin ingestion UI | P1-MVP | Run state reconciles with backend/meta graph. |
| FR-ADMIN-002 | Admin graph quality UI | P1-MVP | No dashboard KPI is hardcoded. |
| FR-VSCODE-001 | VS Code context extension | P1-MVP | Opening demo function retrieves correct graph context. |
| FR-VSCODE-002 | VS Code trace/impact commands | P1-MVP | Demo command returns Jira→code path and impact. |

## Implementation sequence

### WP-EXPERIENCE-01 — User web application
**Objective:** Provide search/NL query, graph visualization, details/evidence, path and impact views backed by real APIs.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** REST/SSE  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** API failure shows explicit degraded/error state.  
**Tests:** Component + Playwright E2E.  
**Acceptance:** Demo flow works from persisted data.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-UI-001`.
### WP-EXPERIENCE-02 — Graph explorer
**Objective:** Visualize typed nodes/edges with filters, expansion, path highlighting and provenance.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** GraphResult  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Large result prompts/refuses expansion beyond cap.  
**Tests:** Visual E2E + API bounds.  
**Acceptance:** Demo path is highlighted with evidence access.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-UI-002`.
### WP-EXPERIENCE-03 — Admin ingestion UI
**Objective:** Show connectors, runs, status, counts, errors, replay/dry-run controls.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** IngestionRun  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Actions validate local auth/confirmation.  
**Tests:** Admin E2E.  
**Acceptance:** Run state reconciles with backend/meta graph.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-ADMIN-001`.
### WP-EXPERIENCE-04 — Admin graph quality UI
**Objective:** Show graph stats, validation findings, quality metrics, schema/ontology versions and backup state.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** QualitySnapshot  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Missing metric displayed as unavailable.  
**Tests:** Fixture reconciliation tests.  
**Acceptance:** No dashboard KPI is hardcoded.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-ADMIN-002`.
### WP-EXPERIENCE-05 — VS Code context extension
**Objective:** Provide sidebar/webview showing current file/symbol, Jira, commits, dependencies, docs and provenance.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Extension API contract  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unavailable platform shows offline state; no source modification.  
**Tests:** Extension host tests.  
**Acceptance:** Opening demo function retrieves correct graph context.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-VSCODE-001`.
### WP-EXPERIENCE-06 — VS Code trace/impact commands
**Objective:** Commands answer why code exists and what change may affect.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Query API  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** No unrestricted Gremlin/tool execution.  
**Tests:** Command E2E.  
**Acceptance:** Demo command returns Jira→code path and impact.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-VSCODE-002`.
