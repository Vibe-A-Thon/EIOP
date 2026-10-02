# WP-CODEGRAPH Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-CODEGRAPH

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-CODE-001 | Deterministic code parser | P1-MVP | Supported files yield stable symbol graph and exact source ranges. |
| FR-CODE-002 | Python and TypeScript MVP parsing | P1-MVP | Demo repo symbols and imports/calls are queryable. |
| FR-CODE-003 | Commit-to-symbol linking | P1-MVP | Demo commit connects to relevant function(s). |
| FR-CODE-004 | Call/import/dependency edges | P1-MVP | Blast radius traverses only validated edge classes. |
| FR-CODE-005 | Source navigation | P1-MVP | Extension opens demo symbol at correct range. |

## Implementation sequence

### WP-CODEGRAPH-01 — Deterministic code parser
**Objective:** Parse source using Tree-sitter/language-specific AST tooling, never LLM as primary parser.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Repository checkout, parser contracts  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Parse errors become file-level findings and do not abort repository.  
**Tests:** Golden parser fixtures.  
**Acceptance:** Supported files yield stable symbol graph and exact source ranges.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CODE-001`.
### WP-CODEGRAPH-02 — Python and TypeScript MVP parsing
**Objective:** Support Python and TypeScript/JavaScript in Phase 1.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Source files  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unsupported syntax is partial with confidence/status.  
**Tests:** Language-specific fixtures.  
**Acceptance:** Demo repo symbols and imports/calls are queryable.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CODE-002`.
### WP-CODEGRAPH-03 — Commit-to-symbol linking
**Objective:** Relate commits to files and affected symbols using changed ranges/versions where available.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Git diff metadata, symbols  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Ambiguous deleted/renamed symbols produce evidence-backed partial link.  
**Tests:** Rename/diff tests.  
**Acceptance:** Demo commit connects to relevant function(s).  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CODE-003`.
### WP-CODEGRAPH-04 — Call/import/dependency edges
**Objective:** Represent calls, imports and package/module dependencies with provenance.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** AST, manifests  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Dynamic calls are not fabricated.  
**Tests:** Static-call fixtures.  
**Acceptance:** Blast radius traverses only validated edge classes.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CODE-004`.
### WP-CODEGRAPH-05 — Source navigation
**Objective:** Preserve repo, revision, path and line/column ranges.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** CodeSymbol  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Missing local checkout returns context without unsafe file access.  
**Tests:** Navigation contract tests.  
**Acceptance:** Extension opens demo symbol at correct range.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-CODE-005`.
