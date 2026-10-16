# ServiceNow Connector Requirements

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define Phase 2 ServiceNow connector

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Connectors own source-system concerns only: authentication, pagination, throttling, extraction, source version and checkpoint position. They never write HugeGraph directly. The SDK output is a versioned SourceEvent stream consumed by the common ingestion pipeline.

The roadmap protects the vertical slice. P0 establishes contracts/schema/security foundations; P1 delivers the integrated MVP; P2 broadens connectors/ontology; P3 advances retrieval/RAG; P4 adds multi-agent patterns; P5 temporal/analytics; P6 human-control automation; P7 enterprise scale/hardening; P8+ controlled self-improvement only after governance exists.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-SNOW-001 | ServiceNow connector | P2 | Incremental sync and mappings pass. |

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
