# Scalability

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define evidence-driven scale evolution

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Scale follows evidence. P1 is single-node RocksDB. Before adopting distributed HStore, measure graph size, write rate, p95/p99, recovery objectives and HA requirements. External API/contracts, canonical IDs and schema manifests are designed so storage topology can change without rewriting clients.

Performance numbers are benchmark outputs, not architecture slogans. EOIP versions a representative dataset, workload mix, hardware profile and query limits, then records throughput, p50/p95/p99, CPU, memory and storage. Index or service-split changes require before/after benchmark evidence.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| NFR-PERF-001 | Benchmark-defined objectives | P1-MVP | Published numbers identify dataset/hardware/version. |
| NFR-MAINT-001 | Modular monolith boundary | P1-MVP | Core can later split without changing external contracts. |
| FR-GRAPH-002 | Logical graph domains | P1-MVP | Every business vertex/edge belongs to a valid domain. |

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
