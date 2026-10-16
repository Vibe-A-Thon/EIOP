# Acceptance Criteria

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** System-wide requirement completion catalog

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirement acceptance criteria

| Requirement | Acceptance criterion | Phase |
|---|---|---|
| FR-CONN-001 | A new connector can be added without editing ingestion core. | P1-MVP |
| FR-CONN-002 | Repeat import is idempotent and creates expected graph. | P1-MVP |
| FR-CONN-003 | Repository, branch and commit nodes plus modifications exist. | P1-MVP |
| FR-CONN-004 | MR and pipeline records link to commits and work items. | P1-MVP |
| FR-CONN-005 | Restart resumes without duplicate canonical nodes. | P1-MVP |
| FR-CONN-006 | Same input/version produces same canonical mutations. | P1-MVP |
| FR-CONN-007 | Deleted source is queryable historically and excluded from current views. | P1-MVP |
| FR-CONF-001 | Incremental sync and provenance pass. | P2 |
| FR-SNOW-001 | Incremental sync and mappings pass. | P2 |
| FR-INGEST-001 | Every graph mutation references a captured event. | P1-MVP |
| FR-INGEST-002 | Same source record maps deterministically for same mapper version. | P1-MVP |
| FR-INGEST-003 | Second identical run does not increase logical entity/edge counts. | P1-MVP |
| FR-INGEST-004 | Admin UI reflects actual backend run state. | P1-MVP |
| FR-INGEST-005 | Rejected records are inspectable and replayable. | P1-MVP |
| FR-GRAPH-001 | All demo graph paths survive service restart. | P1-MVP |
| FR-GRAPH-002 | Every business vertex/edge belongs to a valid domain. | P1-MVP |
| FR-GRAPH-003 | Fresh stack auto-initializes and second run is no-op. | P1-MVP |
| FR-GRAPH-004 | Every canonical entity has unique stable canonical_id. | P1-MVP |
| FR-GRAPH-005 | Admin statistics are derived from graph/meta records. | P1-MVP |
| FR-GRAPH-006 | Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable. | P1-MVP |
| FR-GRAPH-007 | No UI/agent endpoint can execute arbitrary mutation Gremlin. | P1-MVP |
| FR-GRAPH-008 | Benchmark-critical lookup paths use planned indexes. | P1-MVP |
| FR-GRAPH-009 | Each changed fact can be attributed to a run/version. | P1-MVP |
| FR-GRAPH-010 | No documentation claims native SPARQL support. | P2 |
| FR-ONTO-001 | MVP entities/edges reference ontology version and valid terms. | P1-MVP |
| FR-ONTO-002 | No MVP business relationship relies on untyped generic edge. | P1-MVP |
| FR-PROV-001 | MVP evidence coverage is 100% for cross-domain bridge edges. | P1-MVP |
| FR-PROV-002 | User can trace demo answer to source fixture/commit metadata. | P1-MVP |
| FR-ID-001 | Exact aliases merge predictably and retain source aliases. | P1-MVP |
| FR-ID-002 | No fuzzy-only match produces same canonical_id automatically. | P1-MVP |
| FR-TEMP-001 | MVP schema is ready for P5 without ID rewrite. | P1-MVP |
| FR-CODE-001 | Supported files yield stable symbol graph and exact source ranges. | P1-MVP |
| FR-CODE-002 | Demo repo symbols and imports/calls are queryable. | P1-MVP |
| FR-CODE-003 | Demo commit connects to relevant function(s). | P1-MVP |
| FR-CODE-004 | Blast radius traverses only validated edge classes. | P1-MVP |
| FR-CODE-005 | Extension opens demo symbol at correct range. | P1-MVP |
| FR-QUERY-001 | All NL and structured requests compile to validated QueryPlan. | P1-MVP |
| FR-QUERY-002 | Demo Jira-to-function path returns expected ordered edges. | P1-MVP |
| FR-QUERY-003 | Demo function change returns expected dependents with paths. | P1-MVP |
| FR-QUERY-004 | Demo Jira issue, commit and symbol are discoverable. | P1-MVP |
| FR-QUERY-005 | Prompt injection cannot bypass QueryPlan policy. | P1-MVP |
| FR-QUERY-006 | All exposed query endpoints pass policy conformance suite. | P1-MVP |
| FR-QUERY-007 | GraphRAG/UI/MCP consume same evidence format. | P1-MVP |
| FR-QUERY-008 | No public OpenAPI/MCP tool accepts free-form Gremlin in MVP. | P1-MVP |
| FR-VALID-001 | Admin UI shows real findings from demo data. | P1-MVP |
| FR-VALID-002 | Invalid endpoint edge cannot silently enter graph. | P1-MVP |
| FR-VALID-003 | Dashboard values reconcile with fixture counts. | P1-MVP |
| FR-RAG-001 | Known MVP questions route without external service. | P1-MVP |
| FR-RAG-002 | Demo GraphRAG answer cites graph/source references. | P1-MVP |
| FR-RAG-003 | Core search/path/impact remains usable with model service stopped. | P1-MVP |
| FR-RAG-004 | MVP starts and demos without vector database. | P1-MVP |
| FR-RAG-005 | Baseline report is reproducible locally. | P1-MVP |
| FR-RAG-006 | P3 can add strategy plugin without changing callers. | P3 |
| FR-AGENT-001 | Every enabled agent has a validated contract. | P1-MVP |
| FR-AGENT-002 | Agent cannot exceed configured execution envelope. | P1-MVP |
| FR-AGENT-003 | Same demo question works via UI/API/MCP context. | P1-MVP |
| FR-AGENT-004 | No MVP agent can mutate source systems or code. | P1-MVP |
| FR-AGENT-005 | No production self-modification path exists before P8+. | P8+ |
| FR-MEM-001 | No uncontrolled accumulation in MVP. | P1-MVP |
| FR-MCP-001 | MCP returns same graph evidence as REST for demo case. | P1-MVP |
| FR-MCP-002 | MVP MCP surface is read-only. | P1-MVP |
| FR-UI-001 | Demo flow works from persisted data. | P1-MVP |
| FR-UI-002 | Demo path is highlighted with evidence access. | P1-MVP |
| FR-ADMIN-001 | Run state reconciles with backend/meta graph. | P1-MVP |
| FR-ADMIN-002 | No dashboard KPI is hardcoded. | P1-MVP |
| FR-VSCODE-001 | Opening demo function retrieves correct graph context. | P1-MVP |
| FR-VSCODE-002 | Demo command returns Jira→code path and impact. | P1-MVP |
| NFR-SEC-001 | Demo succeeds with external network disabled. | P1-MVP |
| NFR-SEC-002 | Repository and logs contain no test secret plaintext. | P1-MVP |
| NFR-SEC-003 | Security suite rejects malicious fixtures. | P1-MVP |
| NFR-SEC-004 | Known injection cases remain read-only/bounded. | P1-MVP |
| NFR-SEC-005 | /admin route presence is never claimed as authorization boundary. | P1-MVP |
| NFR-SEC-006 | HugeGraph/model not exposed externally by default. | P1-MVP |
| NFR-SEC-007 | Sensitive operation has traceable audit ID. | P1-MVP |
| NFR-REL-001 | No duplicates or silent skipped records after restart. | P1-MVP |
| NFR-REL-002 | Restored demo reproduces expected counts/path queries. | P1-MVP |
| NFR-OPS-001 | Failure can be followed by correlation ID. | P1-MVP |
| NFR-OPS-002 | Key MVP metrics are machine-readable. | P1-MVP |
| NFR-PERF-001 | Published numbers identify dataset/hardware/version. | P1-MVP |
| NFR-MAINT-001 | Core can later split without changing external contracts. | P1-MVP |
| NFR-PRIV-001 | Audit/log exports contain no prohibited content. | P1-MVP |

## MVP acceptance criteria

- **MVP-FR-001 — Apache HugeGraph local Docker:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-GRAPH-001.
- **MVP-FR-002 — Automatic graph schema initialization:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-GRAPH-003.
- **MVP-FR-003 — Jira JSON ingestion:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-CONN-002.
- **MVP-FR-004 — Git repository/GitLab ingestion:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-CONN-003,FR-CONN-004.
- **MVP-FR-005 — Code parsing:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-CODE-001,FR-CODE-002.
- **MVP-FR-006 — Canonical entity generation:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-INGEST-002,FR-GRAPH-004.
- **MVP-FR-007 — Jira graph:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-ONTO-001,FR-GRAPH-002.
- **MVP-FR-008 — Code graph:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-CODE-001,FR-CODE-004.
- **MVP-FR-009 — Meta graph:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-GRAPH-005.
- **MVP-FR-010 — Cross-graph linking:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-GRAPH-006.
- **MVP-FR-011 — Provenance:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-PROV-001,FR-PROV-002.
- **MVP-FR-012 — Graph validation:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-VALID-001,FR-VALID-002.
- **MVP-FR-013 — Query API:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-QUERY-001,FR-QUERY-006.
- **MVP-FR-014 — Impact analysis query:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-QUERY-003.
- **MVP-FR-015 — Path query:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-QUERY-002.
- **MVP-FR-016 — Search/query UI:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-UI-001.
- **MVP-FR-017 — Graph visualizer:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-UI-002.
- **MVP-FR-018 — Admin ingestion/validation UI:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-ADMIN-001,FR-ADMIN-002.
- **MVP-FR-019 — VS Code extension:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-VSCODE-001,FR-VSCODE-002.
- **MVP-FR-020 — Local GraphRAG:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-RAG-001,FR-RAG-002,FR-RAG-003.
- **MVP-FR-021 — Useful read-only agent workflow:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-AGENT-003.
- **MVP-FR-022 — MCP core graph access:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-MCP-001,FR-MCP-002.
- **MVP-FR-023 — Logging:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements NFR-OPS-001.
- **MVP-FR-024 — Metrics:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements NFR-OPS-002.
- **MVP-FR-025 — Backup:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements NFR-REL-002.
- **MVP-FR-026 — Restore:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements NFR-REL-002.
- **MVP-FR-027 — Automated tests:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements NFR-MAINT-001.
- **MVP-FR-028 — End-to-end demo:** must satisfy its detailed acceptance in `MVP-requirements.md` and parent requirements FR-GRAPH-006,FR-AGENT-003.


## Release acceptance gate

A release candidate must include immutable build/version metadata, dependency/SBOM/license output, automated test report, schema/ontology version, known-risk register, clean-deployment evidence, no-egress test, demo evidence and verified backup/restore evidence. Any waived criterion requires an ADR/risk acceptance entry; MVP non-negotiables cannot be waived by implementation convenience.
