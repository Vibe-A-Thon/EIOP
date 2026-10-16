# Security Architecture

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define local security controls

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Security is designed for a local trusted-network MVP without pretending that trusted means safe. The system minimizes exposed ports, runs components least-privileged, protects secrets, validates inputs, prevents prompt/tool injection from bypassing policies, denies outbound enterprise-data egress and records auditable actions.

Local deployment reduces transmission risk but does not eliminate privacy duties. Connector mappings explicitly select fields; log/audit schemas avoid document bodies and secrets; retention and deletion are documented; exports inherit data classification. Future external providers remain disabled until a redaction/approval gateway exists.


## Phase 1 security baseline

- Runtime egress is denied by default; model/images/dependencies are staged before restricted deployment.
- HugeGraph and local-model ports stay on an internal Docker network; only the web/API edge is exposed as configured.
- Non-loopback profiles require local authentication; the current codebase now includes local RBAC/ABAC primitives, policy evaluation, role/user export, signed token checks and `/api/v1/authz/*` management/evaluation routes. Production multi-user authorization still requires release hardening and Phase 8 security receipts.
- Secrets are file-mounted/referenced and redacted from logs; example files contain placeholders only.
- Source paths are allowlisted roots; path traversal/symlink escape/oversized input is rejected.
- Model/retrieved text is untrusted data. It cannot create new tool permissions, arbitrary Gremlin or shell commands.
- QueryPlan bounds and read-only Gremlin templates are enforced for UI, agent and MCP equally.
- Audit events record ingestion, queries, agent/tool calls, admin operations, backup/restore and policy denials; hidden chain-of-thought is never stored.
- Write/destructive MCP/agent tools are not registered in the MVP.

## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| NFR-SEC-001 | No outbound enterprise-data egress | P1-MVP | Demo succeeds with external network disabled. |
| NFR-SEC-002 | Secret isolation | P1-MVP | Repository and logs contain no test secret plaintext. |
| NFR-SEC-003 | Input/file safety | P1-MVP | Security suite rejects malicious fixtures. |
| NFR-SEC-004 | Prompt/tool injection defenses | P1-MVP | Known injection cases remain read-only/bounded. |
| NFR-SEC-005 | Authentication without MVP RBAC | P1-MVP | /admin route presence is never claimed as authorization boundary. |
| NFR-SEC-006 | Container hardening | P1-MVP | HugeGraph/model not exposed externally by default. |
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
