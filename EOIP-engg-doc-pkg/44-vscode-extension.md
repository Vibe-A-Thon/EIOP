# VS Code Extension

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define developer context extension

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

The extension is context-aware but read-only in Phase 1. It maps workspace/repository/path/current symbol to canonical graph entities, then displays Jira origin, commits, callers/callees/dependencies, related docs, provenance and impact. Failure to reach EOIP never blocks normal editing.

The code graph is AST/symbol based. It records repositories, revisions, files, symbols, source ranges, imports, statically resolvable calls/dependencies and commit-to-file/symbol relationships. Dynamic behavior that cannot be established deterministically is marked unresolved or deferred rather than hallucinated.

The application exposes domain query services rather than database access. Exact identifier search anchors graph operations. Natural-language interpretation produces a typed QueryPlan, validated against ontology/schema and policy, then executes a named bounded Gremlin template. Depth, edge classes, result size and timeout are explicit inputs with hard maximums.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-VSCODE-001 | VS Code context extension | P1-MVP | Opening demo function retrieves correct graph context. |
| FR-VSCODE-002 | VS Code trace/impact commands | P1-MVP | Demo command returns Jira→code path and impact. |
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
