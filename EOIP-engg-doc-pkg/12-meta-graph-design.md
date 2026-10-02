# Meta Graph Design

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define the graph-about-the-graph

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

The meta graph makes the graph self-describing: data sources, domains, ontology/schema versions, ingestion runs, validation runs, quality snapshots and dataset lineage are graph objects. The query router can use these records to understand which domains contain relevant evidence rather than scanning the full graph blindly.

Provenance is part of every mutation, not a separate report. Cross-domain links have evidence references to raw events, commits/diffs, parser output or mapping rules, plus ingestion/parser/ontology versions. API, UI, RAG and MCP return the same evidence identifiers so an answer can be audited independent of the LLM.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-GRAPH-005 | Meta graph | P1-MVP | Admin statistics are derived from graph/meta records. |
| FR-INGEST-004 | Ingestion job lifecycle | P1-MVP | Admin UI reflects actual backend run state. |
| FR-VALID-003 | Graph quality metrics | P1-MVP | Dashboard values reconcile with fixture counts. |

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
