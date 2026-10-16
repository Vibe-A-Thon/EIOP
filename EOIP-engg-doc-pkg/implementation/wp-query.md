# WP-QUERY Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-QUERY

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-QUERY-001 | Structured QueryPlan | P1-MVP | All NL and structured requests compile to validated QueryPlan. |
| FR-QUERY-002 | Path query | P1-MVP | Demo Jira-to-function path returns expected ordered edges. |
| FR-QUERY-003 | Impact analysis | P1-MVP | Demo function change returns expected dependents with paths. |
| FR-QUERY-004 | Entity search | P1-MVP | Demo Jira issue, commit and symbol are discoverable. |
| FR-QUERY-005 | Natural-language query interpretation | P1-MVP | Prompt injection cannot bypass QueryPlan policy. |
| FR-QUERY-006 | Query safety policy | P1-MVP | All exposed query endpoints pass policy conformance suite. |
| FR-QUERY-007 | Query evidence envelope | P1-MVP | GraphRAG/UI/MCP consume same evidence format. |
| FR-QUERY-008 | Raw Gremlin admin boundary | P1-MVP | No public OpenAPI/MCP tool accepts free-form Gremlin in MVP. |
| FR-GRAPH-007 | Gremlin repository | P1-MVP | No UI/agent endpoint can execute arbitrary mutation Gremlin. |

## Implementation sequence

### WP-QUERY-01 — Structured QueryPlan
**Objective:** Represent user/agent query intent as a typed plan before Gremlin.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** QueryPlan v1  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Invalid/oversized plans rejected before graph call.  
**Tests:** Schema/property-based tests.  
**Acceptance:** All NL and structured requests compile to validated QueryPlan.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-QUERY-001`.
### WP-QUERY-02 — Path query
**Objective:** Find bounded paths between known entities.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Entity IDs, QueryPlan  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** No path returns empty evidence-backed result; timeout is explicit.  
**Tests:** Known/unknown/over-depth tests.  
**Acceptance:** Demo Jira-to-function path returns expected ordered edges.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-QUERY-002`.
### WP-QUERY-03 — Impact analysis
**Objective:** Compute directional bounded blast radius using configured impact edge semantics.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Anchor entity, impact policy  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Cycles bounded; partial results marked on timeout.  
**Tests:** Cyclic graph and golden blast-radius tests.  
**Acceptance:** Demo function change returns expected dependents with paths.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-QUERY-003`.
### WP-QUERY-04 — Entity search
**Objective:** Search by canonical/source IDs, issue key, commit SHA, symbol/path and names.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** SearchRequest  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Broad queries require minimum term and result cap.  
**Tests:** Search relevance/limit tests.  
**Acceptance:** Demo Jira issue, commit and symbol are discoverable.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-QUERY-004`.
### WP-QUERY-05 — Natural-language query interpretation
**Objective:** Interpret supported NL intents locally and safely.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** NL text, schema snapshot  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Model failure falls back to deterministic intents or requests structured refinement.  
**Tests:** Adversarial prompt/query tests.  
**Acceptance:** Prompt injection cannot bypass QueryPlan policy.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-QUERY-005`.
### WP-QUERY-06 — Query safety policy
**Objective:** Enforce traversal depth, result count, timeout, relationship/property allowlists and read-only mode.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** QueryPolicy  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Violation returns stable error code and audit event.  
**Tests:** Boundary/fuzz tests.  
**Acceptance:** All exposed query endpoints pass policy conformance suite.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-QUERY-006`.
### WP-QUERY-07 — Query evidence envelope
**Objective:** Every derived result can include paths, fact IDs and evidence references.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** GraphResult v1  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Missing evidence is visible in result quality.  
**Tests:** Evidence completeness tests.  
**Acceptance:** GraphRAG/UI/MCP consume same evidence format.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-QUERY-007`.
### WP-QUERY-08 — Raw Gremlin admin boundary
**Objective:** Do not expose unrestricted Gremlin to user app, agent or MCP.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Admin configuration  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Disabled path returns 404/403-like policy response.  
**Tests:** Endpoint exposure tests.  
**Acceptance:** No public OpenAPI/MCP tool accepts free-form Gremlin in MVP.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-QUERY-008`.
### WP-QUERY-09 — Gremlin repository
**Objective:** Centralize parameterized/bounded Gremlin templates.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** QueryPlan v1  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unknown template or over-limit request rejected.  
**Tests:** Policy and traversal-bound tests.  
**Acceptance:** No UI/agent endpoint can execute arbitrary mutation Gremlin.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-GRAPH-007`.
