# File and Intranet Connector Requirements

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define local file/document and controlled intranet ingestion

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Connectors own source-system concerns only: authentication, pagination, throttling, extraction, source version and checkpoint position. They never write HugeGraph directly. The SDK output is a versioned SourceEvent stream consumed by the common ingestion pipeline.

Security is designed for a local trusted-network MVP without pretending that trusted means safe. The system minimizes exposed ports, runs components least-privileged, protects secrets, validates inputs, prevents prompt/tool injection from bypassing policies, denies outbound enterprise-data egress and records auditable actions.

Local deployment reduces transmission risk but does not eliminate privacy duties. Connector mappings explicitly select fields; log/audit schemas avoid document bodies and secrets; retention and deletion are documented; exports inherit data classification. Future external providers remain disabled until a redaction/approval gateway exists.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-CONN-001 | Connector SDK | P1-MVP | A new connector can be added without editing ingestion core. |
| NFR-SEC-003 | Input/file safety | P1-MVP | Security suite rejects malicious fixtures. |
| NFR-PRIV-001 | Data minimization and classification | P1-MVP | Audit/log exports contain no prohibited content. |

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
