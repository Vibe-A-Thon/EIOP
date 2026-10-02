# Observability

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define logs, metrics, health and optional tracing

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Logs, metrics and health are mandatory; full distributed tracing is optional where it adds diagnostic value. Correlation IDs bind user query→QueryPlan→Gremlin→RAG/agent calls and ingestion event→mutation→validation. Prometheus/Grafana are optional Compose profiles, so their absence does not block the core stack.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| NFR-OPS-001 | Structured logging and health | P1-MVP | Failure can be followed by correlation ID. |
| NFR-OPS-002 | Local metrics | P1-MVP | Key MVP metrics are machine-readable. |
| NFR-SEC-007 | Audit events | P1-MVP | Sensitive operation has traceable audit ID. |

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
