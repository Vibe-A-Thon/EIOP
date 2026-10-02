# WP-MCP Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-MCP

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-MCP-001 | MCP read server | P1-MVP | MCP returns same graph evidence as REST for demo case. |
| FR-MCP-002 | MCP action separation | P1-MVP | MVP MCP surface is read-only. |

## Implementation sequence

### WP-MCP-01 — MCP read server
**Objective:** Expose search_entity/get_entity/neighbors/path/query/impact/code/jira/document/lineage/evidence as local MCP tools/resources.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** MCP tool schemas  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Backend/policy errors map to structured MCP errors.  
**Tests:** MCP contract/E2E tests.  
**Acceptance:** MCP returns same graph evidence as REST for demo case.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-MCP-001`.
### WP-MCP-02 — MCP action separation
**Objective:** Keep write/action tools in separate registry and disabled in MVP.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** ToolRegistry  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Disabled writes are not advertised.  
**Tests:** Capability-list tests.  
**Acceptance:** MVP MCP surface is read-only.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-MCP-002`.
