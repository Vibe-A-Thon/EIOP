# WP-AGENT-MEMORY Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-AGENT-MEMORY

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-AGENT-001 | Agent contract | P1-MVP | Every enabled agent has a validated contract. |
| FR-AGENT-002 | Bounded agent runtime | P1-MVP | Agent cannot exceed configured execution envelope. |
| FR-AGENT-003 | TraceImpact agent | P1-MVP | Same demo question works via UI/API/MCP context. |
| FR-AGENT-004 | Write/action approval boundary | P1-MVP | No MVP agent can mutate source systems or code. |
| FR-AGENT-005 | Controlled self-modification | P8+ | No production self-modification path exists before P8+. |
| FR-MEM-001 | Scoped memory records | P1-MVP | No uncontrolled accumulation in MVP. |

## Implementation sequence

### WP-AGENT-MEMORY-01 — Agent contract
**Objective:** Define ID/type/purpose/input/output/capabilities/tools/model/memory/policies/time/budget/retry/failure/evidence/audit fields.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** AgentContract  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Invalid contract cannot register.  
**Tests:** Schema tests.  
**Acceptance:** Every enabled agent has a validated contract.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-AGENT-001`.
### WP-AGENT-MEMORY-02 — Bounded agent runtime
**Objective:** Enforce maximum steps/retries/recursion/time/model/tool budgets and circuit breaker.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** AgentRun  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Budget exhaustion terminates with partial evidence.  
**Tests:** Loop/budget tests.  
**Acceptance:** Agent cannot exceed configured execution envelope.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-AGENT-002`.
### WP-AGENT-MEMORY-03 — TraceImpact agent
**Objective:** Provide one useful read-only MVP workflow that answers requirement/code trace and impact questions.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** AgentRequest/AgentResult  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Tool/model failures are surfaced with partial structured result.  
**Tests:** Golden E2E agent tests.  
**Acceptance:** Same demo question works via UI/API/MCP context.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-AGENT-003`.
### WP-AGENT-MEMORY-04 — Write/action approval boundary
**Objective:** Separate read tools from write/destructive tools and require explicit confirmation for future write actions.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** ToolContract  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unapproved write invocation denied/audited.  
**Tests:** Negative policy tests.  
**Acceptance:** No MVP agent can mutate source systems or code.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-AGENT-004`.
### WP-AGENT-MEMORY-05 — Controlled self-modification
**Objective:** Self-learning/evolving/writing capabilities remain disabled until governance, sandboxing, tests and approval exist.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** ChangeProposal  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Any runtime self-edit request denied in earlier phases.  
**Tests:** Policy tests.  
**Acceptance:** No production self-modification path exists before P8+.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-AGENT-005`.
### WP-AGENT-MEMORY-06 — Scoped memory records
**Objective:** Model working/task/conversation/semantic/episodic/procedural memory with scope/source/TTL/provenance/confidence/classification/deletion policy.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** MemoryRecord  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Expired/forbidden memory excluded.  
**Tests:** TTL/scope tests.  
**Acceptance:** No uncontrolled accumulation in MVP.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-MEM-001`.
