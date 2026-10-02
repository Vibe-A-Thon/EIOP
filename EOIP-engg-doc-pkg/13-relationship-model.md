# Relationship Model

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define semantic edges and edge evidence policy

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

EOIP forbids an undifferentiated `RELATED_TO` model for core facts. Relationships express semantics such as CONTAINS, IMPLEMENTS, MODIFIES, CALLS, IMPORTS, DEPENDS_ON, REFERENCES, DOCUMENTS and EVIDENCED_BY. Every inferred edge records confidence and evidence and is visually/semantically distinct from deterministic and human-confirmed facts.

Provenance is part of every mutation, not a separate report. Cross-domain links have evidence references to raw events, commits/diffs, parser output or mapping rules, plus ingestion/parser/ontology versions. API, UI, RAG and MCP return the same evidence identifiers so an answer can be audited independent of the LLM.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-ONTO-002 | Relationship semantics | P1-MVP | No MVP business relationship relies on untyped generic edge. |
| FR-GRAPH-006 | Cross-domain bridge edges | P1-MVP | Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable. |
| FR-PROV-001 | Evidence model | P1-MVP | MVP evidence coverage is 100% for cross-domain bridge edges. |

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
