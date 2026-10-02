# Code Graph

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define AST/symbol/source-control graph

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

The code graph is AST/symbol based. It records repositories, revisions, files, symbols, source ranges, imports, statically resolvable calls/dependencies and commit-to-file/symbol relationships. Dynamic behavior that cannot be established deterministically is marked unresolved or deferred rather than hallucinated.

Provenance is part of every mutation, not a separate report. Cross-domain links have evidence references to raw events, commits/diffs, parser output or mapping rules, plus ingestion/parser/ontology versions. API, UI, RAG and MCP return the same evidence identifiers so an answer can be audited independent of the LLM.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-CODE-001 | Deterministic code parser | P1-MVP | Supported files yield stable symbol graph and exact source ranges. |
| FR-CODE-002 | Python and TypeScript MVP parsing | P1-MVP | Demo repo symbols and imports/calls are queryable. |
| FR-CODE-003 | Commit-to-symbol linking | P1-MVP | Demo commit connects to relevant function(s). |
| FR-CODE-004 | Call/import/dependency edges | P1-MVP | Blast radius traverses only validated edge classes. |
| FR-CODE-005 | Source navigation | P1-MVP | Extension opens demo symbol at correct range. |

## Engineering rules

- Configuration is versioned; secrets are references, never committed values.
- Every persistent fact carries canonical identity and provenance where applicable.
- Every failure path returns a stable error category, logs a correlation ID, and avoids partial silent success.
- MVP behavior must remain functional without an external network and, for graph features, without a local LLM.
- New implementation work must add/adjust automated tests and traceability entries.

## Validation / definition of done

- Normative interfaces are implemented and documented.
- Automated tests mapped to the listed requirement IDs pass.
- Error, security, logging and configuration paths are exercised.
- Acceptance evidence is reproducible from a clean documented environment.
- Deferred capabilities remain behind stable interfaces and are not represented as already implemented.
