# Non-Functional Requirements

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Complete normative non-functional requirement catalog

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

### NFR-SEC-001 — No outbound enterprise-data egress
**WHAT:** Disable external LLM/API egress by default and document firewall/Docker network controls.  
**WHY:** Enterprise data must remain local.  
**HOW:** MVP services need no internet at runtime after images/models are staged.  
**DATA / INTERFACES:** Network policy/config  
**FAILURE:** Blocked egress fails closed; audit safe error.  
**TEST:** Egress test with deny network.  
**COMPLETE WHEN:** Demo succeeds with external network disabled.  
**TARGET PHASE:** P1-MVP

### NFR-SEC-002 — Secret isolation
**WHAT:** Credentials are never hardcoded/logged and use mounted secret files/env references.  
**WHY:** Connector/model/admin secrets require protection.  
**HOW:** Secret loader resolves file references; redaction filter protects logs.  
**DATA / INTERFACES:** SecretRef  
**FAILURE:** Missing secret fails connector without exposing value.  
**TEST:** Secret scan/log redaction tests.  
**COMPLETE WHEN:** Repository and logs contain no test secret plaintext.  
**TARGET PHASE:** P1-MVP

### NFR-SEC-003 — Input/file safety
**WHAT:** Validate paths, sizes, MIME/extension expectations, archive behavior and URL endpoints.  
**WHY:** Ingestion handles untrusted enterprise artifacts.  
**HOW:** Restrict to configured roots; reject traversal/symlink escape; bound files and parsers.  
**DATA / INTERFACES:** Upload/connector config  
**FAILURE:** Unsafe input quarantined.  
**TEST:** Traversal/zip-bomb/oversize tests.  
**COMPLETE WHEN:** Security suite rejects malicious fixtures.  
**TARGET PHASE:** P1-MVP

### NFR-SEC-004 — Prompt/tool injection defenses
**WHAT:** Treat retrieved content as data, not instructions, and validate all tool plans.  
**WHY:** Malicious docs/code can manipulate agents.  
**HOW:** Context delimiters, instruction hierarchy, tool allowlists, QueryPlan schema/policy and output validation.  
**DATA / INTERFACES:** Agent/QueryPlan  
**FAILURE:** Injection attempt cannot add tool or exceed query policy.  
**TEST:** Adversarial evals.  
**COMPLETE WHEN:** Known injection cases remain read-only/bounded.  
**TARGET PHASE:** P1-MVP

### NFR-SEC-005 — Authentication without MVP RBAC
**WHAT:** Protect non-loopback deployments with single-user/local authentication while not implementing role matrices.  
**WHY:** No RBAC does not mean unauthenticated exposure.  
**HOW:** Loopback dev may use dev token; controlled demo uses configured local credential and CSRF-safe patterns.  
**DATA / INTERFACES:** Auth config  
**FAILURE:** Missing auth in non-dev profile blocks startup/exposure.  
**TEST:** Profile/auth tests.  
**COMPLETE WHEN:** /admin route presence is never claimed as authorization boundary.  
**TARGET PHASE:** P1-MVP

### NFR-SEC-006 — Container hardening
**WHAT:** Use non-root where practical, read-only FS where practical, dropped capabilities, healthchecks and private networks.  
**WHY:** Reduces local attack surface.  
**HOW:** Compose separates public app edge from internal graph/model networks.  
**DATA / INTERFACES:** Compose/security profile  
**FAILURE:** Hardening exception documented.  
**TEST:** Container inspection tests.  
**COMPLETE WHEN:** HugeGraph/model not exposed externally by default.  
**TARGET PHASE:** P1-MVP

### NFR-SEC-007 — Audit events
**WHAT:** Record auth, ingestion, query, agent/tool, admin mutation, backup/restore and policy-denial events.  
**WHY:** Operational accountability is required.  
**HOW:** Structured append-only local audit stream plus selected graph meta references; never private chain-of-thought.  
**DATA / INTERFACES:** AuditEvent v1  
**FAILURE:** Audit write failure blocks high-risk action and alerts; read query may degrade per policy.  
**TEST:** Audit coverage tests.  
**COMPLETE WHEN:** Sensitive operation has traceable audit ID.  
**TARGET PHASE:** P1-MVP

### NFR-REL-001 — Restart-safe processing
**WHAT:** Workers recover from crash using checkpoints and idempotent graph mutations.  
**WHY:** Local containers will restart.  
**HOW:** Run state persists to mounted state volume/meta graph.  
**DATA / INTERFACES:** Checkpoint/IngestionRun  
**FAILURE:** Unclean shutdown detected and resumed/reconciled.  
**TEST:** Kill/restart E2E.  
**COMPLETE WHEN:** No duplicates or silent skipped records after restart.  
**TARGET PHASE:** P1-MVP

### NFR-REL-002 — Backup and restore
**WHAT:** Provide repeatable graph schema+data backup and restore plus config/raw-state backup guidance.  
**WHY:** MVP acceptance explicitly requires recovery.  
**HOW:** Use HugeGraph-supported tooling for graph export/restore and checksummed archive; run scripted verification query.  
**DATA / INTERFACES:** Backup manifest  
**FAILURE:** Failed backup never marked successful; restore uses clean target/test mode.  
**TEST:** Backup/restore E2E.  
**COMPLETE WHEN:** Restored demo reproduces expected counts/path queries.  
**TARGET PHASE:** P1-MVP

### NFR-OPS-001 — Structured logging and health
**WHAT:** Expose structured logs, liveness/readiness and correlation IDs locally.  
**WHY:** Troubleshooting must not depend on cloud observability.  
**HOW:** JSON logs to stdout/file, /health/live, /health/ready; correlation spans ingestion/query/agent.  
**DATA / INTERFACES:** LogEvent  
**FAILURE:** Dependency failure makes readiness false.  
**TEST:** Health/log tests.  
**COMPLETE WHEN:** Failure can be followed by correlation ID.  
**TARGET PHASE:** P1-MVP

### NFR-OPS-002 — Local metrics
**WHAT:** Expose Prometheus-format metrics for ingestion, graph queries, RAG/model, agents, tools and errors.  
**WHY:** Performance/quality claims require measurement.  
**HOW:** App /metrics; Prometheus/Grafana optional profile, not mandatory core.  
**DATA / INTERFACES:** Metric series  
**FAILURE:** Metrics failure does not break core request path.  
**TEST:** Metric scrape tests.  
**COMPLETE WHEN:** Key MVP metrics are machine-readable.  
**TARGET PHASE:** P1-MVP

### NFR-PERF-001 — Benchmark-defined objectives
**WHAT:** Define and run a representative local benchmark before claiming throughput/latency.  
**WHY:** Arbitrary performance claims are prohibited.  
**HOW:** Baseline dataset and hardware profile are versioned; report p50/p95/p99 and resource use.  
**DATA / INTERFACES:** Benchmark manifest/results  
**FAILURE:** Missed targets create tuning issue, not hidden result.  
**TEST:** Automated benchmark smoke + manual full run.  
**COMPLETE WHEN:** Published numbers identify dataset/hardware/version.  
**TARGET PHASE:** P1-MVP

### NFR-MAINT-001 — Modular monolith boundary
**WHAT:** Use modular monolith services in Phase 1; split only on evidence.  
**WHY:** Avoid premature distributed complexity.  
**HOW:** Domain packages expose typed ports; API/worker/MCP reuse application services.  
**DATA / INTERFACES:** Python package boundaries  
**FAILURE:** Cross-module direct DB access rejected by architecture tests/convention.  
**TEST:** Dependency/lint tests.  
**COMPLETE WHEN:** Core can later split without changing external contracts.  
**TARGET PHASE:** P1-MVP

### NFR-PRIV-001 — Data minimization and classification
**WHAT:** Capture only required source fields and classify sensitive content.  
**WHY:** Local operation still requires privacy discipline.  
**HOW:** Connector mappings define allow/deny/redaction; logs never copy document bodies by default.  
**DATA / INTERFACES:** Source mapping/classification  
**FAILURE:** Unknown sensitive field defaults to protected handling.  
**TEST:** Redaction fixtures.  
**COMPLETE WHEN:** Audit/log exports contain no prohibited content.  
**TARGET PHASE:** P1-MVP



## MVP benchmark definition (targets, not measured claims)

Representative baseline dataset: approximately 2,000 Jira work items, 10 Git repositories, 15,000 commits, 25,000 files/symbols, 5,000 document sections and 150,000–300,000 relationships. Reference developer workstation: 8 physical/logical CPU cores available to Docker, 32 GiB RAM and local NVMe/SSD. Record the exact hardware in every benchmark result.

Initial engineering targets are acceptance thresholds to validate after implementation: indexed entity lookup p95 ≤ 500 ms; bounded path/impact query p95 ≤ 2 s at configured depth/result limits; standard user API p95 ≤ 1 s excluding local-model generation; `docker compose up` readiness ≤ 120 s after images are locally available. These are not product performance claims until the benchmark suite measures them.



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
