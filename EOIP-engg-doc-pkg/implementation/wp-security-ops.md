# WP-SECURITY-OPS Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-SECURITY-OPS

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| NFR-SEC-001 | No outbound enterprise-data egress | P1-MVP | Demo succeeds with external network disabled. |
| NFR-SEC-002 | Secret isolation | P1-MVP | Repository and logs contain no test secret plaintext. |
| NFR-SEC-003 | Input/file safety | P1-MVP | Security suite rejects malicious fixtures. |
| NFR-SEC-004 | Prompt/tool injection defenses | P1-MVP | Known injection cases remain read-only/bounded. |
| NFR-SEC-005 | Authentication without MVP RBAC | P1-MVP | /admin route presence is never claimed as authorization boundary. |
| NFR-SEC-006 | Container hardening | P1-MVP | HugeGraph/model not exposed externally by default. |
| NFR-SEC-007 | Audit events | P1-MVP | Sensitive operation has traceable audit ID. |
| NFR-REL-001 | Restart-safe processing | P1-MVP | No duplicates or silent skipped records after restart. |
| NFR-REL-002 | Backup and restore | P1-MVP | Restored demo reproduces expected counts/path queries. |
| NFR-OPS-001 | Structured logging and health | P1-MVP | Failure can be followed by correlation ID. |
| NFR-OPS-002 | Local metrics | P1-MVP | Key MVP metrics are machine-readable. |
| NFR-PERF-001 | Benchmark-defined objectives | P1-MVP | Published numbers identify dataset/hardware/version. |
| NFR-MAINT-001 | Modular monolith boundary | P1-MVP | Core can later split without changing external contracts. |
| NFR-PRIV-001 | Data minimization and classification | P1-MVP | Audit/log exports contain no prohibited content. |

## Implementation sequence

### WP-SECURITY-OPS-01 — No outbound enterprise-data egress
**Objective:** Disable external LLM/API egress by default and document firewall/Docker network controls.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Network policy/config  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Blocked egress fails closed; audit safe error.  
**Tests:** Egress test with deny network.  
**Acceptance:** Demo succeeds with external network disabled.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-SEC-001`.
### WP-SECURITY-OPS-02 — Secret isolation
**Objective:** Credentials are never hardcoded/logged and use mounted secret files/env references.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** SecretRef  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Missing secret fails connector without exposing value.  
**Tests:** Secret scan/log redaction tests.  
**Acceptance:** Repository and logs contain no test secret plaintext.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-SEC-002`.
### WP-SECURITY-OPS-03 — Input/file safety
**Objective:** Validate paths, sizes, MIME/extension expectations, archive behavior and URL endpoints.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Upload/connector config  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unsafe input quarantined.  
**Tests:** Traversal/zip-bomb/oversize tests.  
**Acceptance:** Security suite rejects malicious fixtures.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-SEC-003`.
### WP-SECURITY-OPS-04 — Prompt/tool injection defenses
**Objective:** Treat retrieved content as data, not instructions, and validate all tool plans.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Agent/QueryPlan  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Injection attempt cannot add tool or exceed query policy.  
**Tests:** Adversarial evals.  
**Acceptance:** Known injection cases remain read-only/bounded.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-SEC-004`.
### WP-SECURITY-OPS-05 — Authentication without MVP RBAC
**Objective:** Protect non-loopback deployments with single-user/local authentication while not implementing role matrices.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Auth config  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Missing auth in non-dev profile blocks startup/exposure.  
**Tests:** Profile/auth tests.  
**Acceptance:** /admin route presence is never claimed as authorization boundary.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-SEC-005`.
### WP-SECURITY-OPS-06 — Container hardening
**Objective:** Use non-root where practical, read-only FS where practical, dropped capabilities, healthchecks and private networks.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Compose/security profile  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Hardening exception documented.  
**Tests:** Container inspection tests.  
**Acceptance:** HugeGraph/model not exposed externally by default.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-SEC-006`.
### WP-SECURITY-OPS-07 — Audit events
**Objective:** Record auth, ingestion, query, agent/tool, admin mutation, backup/restore and policy-denial events.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** AuditEvent v1  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Audit write failure blocks high-risk action and alerts; read query may degrade per policy.  
**Tests:** Audit coverage tests.  
**Acceptance:** Sensitive operation has traceable audit ID.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-SEC-007`.
### WP-SECURITY-OPS-08 — Restart-safe processing
**Objective:** Workers recover from crash using checkpoints and idempotent graph mutations.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Checkpoint/IngestionRun  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unclean shutdown detected and resumed/reconciled.  
**Tests:** Kill/restart E2E.  
**Acceptance:** No duplicates or silent skipped records after restart.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-REL-001`.
### WP-SECURITY-OPS-09 — Backup and restore
**Objective:** Provide repeatable graph schema+data backup and restore plus config/raw-state backup guidance.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Backup manifest  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Failed backup never marked successful; restore uses clean target/test mode.  
**Tests:** Backup/restore E2E.  
**Acceptance:** Restored demo reproduces expected counts/path queries.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-REL-002`.
### WP-SECURITY-OPS-10 — Structured logging and health
**Objective:** Expose structured logs, liveness/readiness and correlation IDs locally.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** LogEvent  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Dependency failure makes readiness false.  
**Tests:** Health/log tests.  
**Acceptance:** Failure can be followed by correlation ID.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-OPS-001`.
### WP-SECURITY-OPS-11 — Local metrics
**Objective:** Expose Prometheus-format metrics for ingestion, graph queries, RAG/model, agents, tools and errors.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Metric series  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Metrics failure does not break core request path.  
**Tests:** Metric scrape tests.  
**Acceptance:** Key MVP metrics are machine-readable.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-OPS-002`.
### WP-SECURITY-OPS-12 — Benchmark-defined objectives
**Objective:** Define and run a representative local benchmark before claiming throughput/latency.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Benchmark manifest/results  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Missed targets create tuning issue, not hidden result.  
**Tests:** Automated benchmark smoke + manual full run.  
**Acceptance:** Published numbers identify dataset/hardware/version.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-PERF-001`.
### WP-SECURITY-OPS-13 — Modular monolith boundary
**Objective:** Use modular monolith services in Phase 1; split only on evidence.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Python package boundaries  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Cross-module direct DB access rejected by architecture tests/convention.  
**Tests:** Dependency/lint tests.  
**Acceptance:** Core can later split without changing external contracts.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-MAINT-001`.
### WP-SECURITY-OPS-14 — Data minimization and classification
**Objective:** Capture only required source fields and classify sensitive content.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** Source mapping/classification  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unknown sensitive field defaults to protected handling.  
**Tests:** Redaction fixtures.  
**Acceptance:** Audit/log exports contain no prohibited content.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `NFR-PRIV-001`.
