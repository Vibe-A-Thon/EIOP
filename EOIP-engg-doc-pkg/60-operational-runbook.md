# Operational Runbook

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define day-0/day-1/day-2 operations

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

The runbook assumes a restricted local environment: stage images/models, provision secrets, start Compose, verify readiness/schema, load demo or enterprise mappings, monitor job and graph quality, run smoke queries, back up before destructive maintenance, and capture diagnostics with correlation IDs. Recovery instructions favor replay/idempotency over manual graph surgery.

Graph backup/restore uses supported HugeGraph tooling and is complemented by application config, raw-capture/checkpoint and model/config manifests. Every backup has checksum, timestamp, schema/ontology versions and verification status. Restore is tested into a clean target and verified with known count/path queries.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| NFR-REL-001 | Restart-safe processing | P1-MVP | No duplicates or silent skipped records after restart. |
| NFR-REL-002 | Backup and restore | P1-MVP | Restored demo reproduces expected counts/path queries. |
| NFR-OPS-001 | Structured logging and health | P1-MVP | Failure can be followed by correlation ID. |
| NFR-OPS-002 | Local metrics | P1-MVP | Key MVP metrics are machine-readable. |

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
