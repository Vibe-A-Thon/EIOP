# Git/GitLab Connector Requirements

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define local Git and on-prem GitLab metadata ingestion

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Connectors own source-system concerns only: authentication, pagination, throttling, extraction, source version and checkpoint position. They never write HugeGraph directly. The SDK output is a versioned SourceEvent stream consumed by the common ingestion pipeline.

The code graph is AST/symbol based. It records repositories, revisions, files, symbols, source ranges, imports, statically resolvable calls/dependencies and commit-to-file/symbol relationships. Dynamic behavior that cannot be established deterministically is marked unresolved or deferred rather than hallucinated.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-CONN-003 | Git repository connector | P1-MVP | Repository, branch and commit nodes plus modifications exist. |
| FR-CONN-004 | GitLab metadata adapter | P1-MVP | MR and pipeline records link to commits and work items. |
| FR-CODE-003 | Commit-to-symbol linking | P1-MVP | Demo commit connects to relevant function(s). |

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
