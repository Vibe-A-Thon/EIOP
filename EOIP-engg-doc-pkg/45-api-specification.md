# API Specification

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define versioned REST/SSE contracts

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

All external contracts are versioned under `/api/v1`. Domain services return canonical IDs and evidence objects rather than HugeGraph internal structures. OpenAPI is generated from Pydantic models and checked in CI for compatibility review.

The application exposes domain query services rather than database access. Exact identifier search anchors graph operations. Natural-language interpretation produces a typed QueryPlan, validated against ontology/schema and policy, then executes a named bounded Gremlin template. Depth, edge classes, result size and timeout are explicit inputs with hard maximums.

The ingestion worker is restart-safe and replayable. Capture precedes mutation; checkpoints advance only after committed graph batches. Mapping/parser failures are isolated to records and recorded in a local DLQ. A dry run executes parsing/mapping/validation without writing graph facts.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-QUERY-001 | Structured QueryPlan | P1-MVP | All NL and structured requests compile to validated QueryPlan. |
| FR-QUERY-007 | Query evidence envelope | P1-MVP | GraphRAG/UI/MCP consume same evidence format. |
| FR-INGEST-004 | Ingestion job lifecycle | P1-MVP | Admin UI reflects actual backend run state. |
| FR-AGENT-003 | TraceImpact agent | P1-MVP | Same demo question works via UI/API/MCP context. |

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
