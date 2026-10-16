# Connector Framework

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define connector SDK and source isolation

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Connectors own source-system concerns only: authentication, pagination, throttling, extraction, source version and checkpoint position. They never write HugeGraph directly. The SDK output is a versioned SourceEvent stream consumed by the common ingestion pipeline.

The ingestion worker is restart-safe and replayable. Capture precedes mutation; checkpoints advance only after committed graph batches. Mapping/parser failures are isolated to records and recorded in a local DLQ. A dry run executes parsing/mapping/validation without writing graph facts.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-CONN-001 | Connector SDK | P1-MVP | A new connector can be added without editing ingestion core. |
| FR-CONN-005 | Connector resiliency | P1-MVP | Restart resumes without duplicate canonical nodes. |
| FR-CONN-006 | Dry run and replay | P1-MVP | Same input/version produces same canonical mutations. |
| FR-CONN-007 | Source deletion semantics | P1-MVP | Deleted source is queryable historically and excluded from current views. |

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
