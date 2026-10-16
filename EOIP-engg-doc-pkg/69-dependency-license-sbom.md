# Dependency, License and SBOM

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define dependency governance and software bill of materials process

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Builds are reproducible and offline-deployable. Lock Python/npm dependencies, generate SBOMs, scan source/images/dependencies, pin container image versions/digests for releases, retain license inventory, run tests before packaging and produce an air-gap bundle manifest rather than downloading at runtime.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| NFR-SEC-006 | Container hardening | P1-MVP | HugeGraph/model not exposed externally by default. |
| NFR-MAINT-001 | Modular monolith boundary | P1-MVP | Core can later split without changing external contracts. |

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
