# Testing Strategy

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Requirement-linked quality strategy and suites

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.
Tests are traceability assets. Unit/parser/connector/schema/integrity/ontology/identity/relationship/provenance/idempotency/recovery/query-limit/RAG/agent/MCP/UI/VS Code/security/Docker/backup/E2E/performance suites map to requirement IDs. A feature is done only when its requirement, implementation task, tests and acceptance evidence are linked.


## Test layers

| Suite | Primary focus | Required examples |
|---|---|---|
| Unit | pure mappers, ID algorithms, policies, parsers | canonical ID stability; QueryPlan bounds; rule functions |
| Contract | connector, parser, model, MCP, REST contracts | pagination/retry; SourceEvent schema; MCP tool schemas |
| Graph schema/integrity | labels, indexes, endpoint/domain constraints | bootstrap idempotency; invalid edge rejection |
| Integration | HugeGraph + worker/API | Jira/Git ingest; provenance; path/impact queries |
| Recovery | restart/checkpoint/backup/restore | kill worker; duplicate replay; clean restore |
| Security | no-egress, secret redaction, path/query/prompt attacks | traversal; arbitrary Gremlin; prompt injection; container exposure |
| RAG/agent evaluation | retrieval/evidence/groundedness/budgets | golden QA; model-down; loop termination |
| UI/VS Code | product workflows against real API | graph path; admin state; current symbol context |
| E2E | clean-stack business story | Jira→code→pipeline→doc; MCP parity; restore replay |
| Performance | benchmark workload | ingest throughput; lookup/path/impact p50/p95/p99 |

## Requirement-to-test obligations

- **FR-CONN-001** — Contract tests against a fake source. Completion signal: A new connector can be added without editing ingestion core.
- **FR-CONN-002** — Fixture, malformed, duplicate, resume tests. Completion signal: Repeat import is idempotent and creates expected graph.
- **FR-CONN-003** — Temporary repository integration tests. Completion signal: Repository, branch and commit nodes plus modifications exist.
- **FR-CONN-004** — Mock API and fixture contract tests. Completion signal: MR and pipeline records link to commits and work items.
- **FR-CONN-005** — Fault-injection restart tests. Completion signal: Restart resumes without duplicate canonical nodes.
- **FR-CONN-006** — Golden-event replay tests. Completion signal: Same input/version produces same canonical mutations.
- **FR-CONN-007** — Deletion/reappearance tests. Completion signal: Deleted source is queryable historically and excluded from current views.
- **FR-CONF-001** — Contract tests in P2. Completion signal: Incremental sync and provenance pass.
- **FR-SNOW-001** — Contract tests in P2. Completion signal: Incremental sync and mappings pass.
- **FR-INGEST-001** — Hash/replay/restart tests. Completion signal: Every graph mutation references a captured event.
- **FR-INGEST-002** — Golden mapping tests. Completion signal: Same source record maps deterministically for same mapper version.
- **FR-INGEST-003** — Double-ingest E2E. Completion signal: Second identical run does not increase logical entity/edge counts.
- **FR-INGEST-004** — State-transition tests. Completion signal: Admin UI reflects actual backend run state.
- **FR-INGEST-005** — Malformed fixtures. Completion signal: Rejected records are inspectable and replayable.
- **FR-GRAPH-001** — Startup and persistence tests. Completion signal: All demo graph paths survive service restart.
- **FR-GRAPH-002** — Domain integrity tests. Completion signal: Every business vertex/edge belongs to a valid domain.
- **FR-GRAPH-003** — Fresh/repeat/incompatible schema tests. Completion signal: Fresh stack auto-initializes and second run is no-op.
- **FR-GRAPH-004** — Collision/idempotency tests. Completion signal: Every canonical entity has unique stable canonical_id.
- **FR-GRAPH-005** — Meta traversal tests. Completion signal: Admin statistics are derived from graph/meta records.
- **FR-GRAPH-006** — Synthetic E2E path assertions. Completion signal: Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable.
- **FR-GRAPH-007** — Policy and traversal-bound tests. Completion signal: No UI/agent endpoint can execute arbitrary mutation Gremlin.
- **FR-GRAPH-008** — Query-plan benchmark tests. Completion signal: Benchmark-critical lookup paths use planned indexes.
- **FR-GRAPH-009** — Replay/version tests. Completion signal: Each changed fact can be attributed to a run/version.
- **FR-GRAPH-010** — Round-trip fixtures where possible. Completion signal: No documentation claims native SPARQL support.
- **FR-ONTO-001** — Ontology conformance tests. Completion signal: MVP entities/edges reference ontology version and valid terms.
- **FR-ONTO-002** — Edge domain/range tests. Completion signal: No MVP business relationship relies on untyped generic edge.
- **FR-PROV-001** — Provenance coverage tests. Completion signal: MVP evidence coverage is 100% for cross-domain bridge edges.
- **FR-PROV-002** — Lineage API E2E. Completion signal: User can trace demo answer to source fixture/commit metadata.
- **FR-ID-001** — Alias/conflict tests. Completion signal: Exact aliases merge predictably and retain source aliases.
- **FR-ID-002** — Fuzzy boundary tests. Completion signal: No fuzzy-only match produces same canonical_id automatically.
- **FR-TEMP-001** — Temporal validation tests. Completion signal: MVP schema is ready for P5 without ID rewrite.
- **FR-CODE-001** — Golden parser fixtures. Completion signal: Supported files yield stable symbol graph and exact source ranges.
- **FR-CODE-002** — Language-specific fixtures. Completion signal: Demo repo symbols and imports/calls are queryable.
- **FR-CODE-003** — Rename/diff tests. Completion signal: Demo commit connects to relevant function(s).
- **FR-CODE-004** — Static-call fixtures. Completion signal: Blast radius traverses only validated edge classes.
- **FR-CODE-005** — Navigation contract tests. Completion signal: Extension opens demo symbol at correct range.
- **FR-QUERY-001** — Schema/property-based tests. Completion signal: All NL and structured requests compile to validated QueryPlan.
- **FR-QUERY-002** — Known/unknown/over-depth tests. Completion signal: Demo Jira-to-function path returns expected ordered edges.
- **FR-QUERY-003** — Cyclic graph and golden blast-radius tests. Completion signal: Demo function change returns expected dependents with paths.
- **FR-QUERY-004** — Search relevance/limit tests. Completion signal: Demo Jira issue, commit and symbol are discoverable.
- **FR-QUERY-005** — Adversarial prompt/query tests. Completion signal: Prompt injection cannot bypass QueryPlan policy.
- **FR-QUERY-006** — Boundary/fuzz tests. Completion signal: All exposed query endpoints pass policy conformance suite.
- **FR-QUERY-007** — Evidence completeness tests. Completion signal: GraphRAG/UI/MCP consume same evidence format.
- **FR-QUERY-008** — Endpoint exposure tests. Completion signal: No public OpenAPI/MCP tool accepts free-form Gremlin in MVP.
- **FR-VALID-001** — Seeded-invalid-graph tests. Completion signal: Admin UI shows real findings from demo data.
- **FR-VALID-002** — Hard/soft rule tests. Completion signal: Invalid endpoint edge cannot silently enter graph.
- **FR-VALID-003** — Metric fixture tests. Completion signal: Dashboard values reconcile with fixture counts.
- **FR-RAG-001** — Router table tests. Completion signal: Known MVP questions route without external service.
- **FR-RAG-002** — Golden question/evidence tests. Completion signal: Demo GraphRAG answer cites graph/source references.
- **FR-RAG-003** — No-egress/model-down tests. Completion signal: Core search/path/impact remains usable with model service stopped.
- **FR-RAG-004** — Model-off tests. Completion signal: MVP starts and demos without vector database.
- **FR-RAG-005** — Automated evaluation tests. Completion signal: Baseline report is reproducible locally.
- **FR-RAG-006** — Strategy contract tests. Completion signal: P3 can add strategy plugin without changing callers.
- **FR-AGENT-001** — Schema tests. Completion signal: Every enabled agent has a validated contract.
- **FR-AGENT-002** — Loop/budget tests. Completion signal: Agent cannot exceed configured execution envelope.
- **FR-AGENT-003** — Golden E2E agent tests. Completion signal: Same demo question works via UI/API/MCP context.
- **FR-AGENT-004** — Negative policy tests. Completion signal: No MVP agent can mutate source systems or code.
- **FR-AGENT-005** — Policy tests. Completion signal: No production self-modification path exists before P8+.
- **FR-MEM-001** — TTL/scope tests. Completion signal: No uncontrolled accumulation in MVP.
- **FR-MCP-001** — MCP contract/E2E tests. Completion signal: MCP returns same graph evidence as REST for demo case.
- **FR-MCP-002** — Capability-list tests. Completion signal: MVP MCP surface is read-only.
- **FR-UI-001** — Component + Playwright E2E. Completion signal: Demo flow works from persisted data.
- **FR-UI-002** — Visual E2E + API bounds. Completion signal: Demo path is highlighted with evidence access.
- **FR-ADMIN-001** — Admin E2E. Completion signal: Run state reconciles with backend/meta graph.
- **FR-ADMIN-002** — Fixture reconciliation tests. Completion signal: No dashboard KPI is hardcoded.
- **FR-VSCODE-001** — Extension host tests. Completion signal: Opening demo function retrieves correct graph context.
- **FR-VSCODE-002** — Command E2E. Completion signal: Demo command returns Jira→code path and impact.
- **NFR-SEC-001** — Egress test with deny network. Completion signal: Demo succeeds with external network disabled.
- **NFR-SEC-002** — Secret scan/log redaction tests. Completion signal: Repository and logs contain no test secret plaintext.
- **NFR-SEC-003** — Traversal/zip-bomb/oversize tests. Completion signal: Security suite rejects malicious fixtures.
- **NFR-SEC-004** — Adversarial evals. Completion signal: Known injection cases remain read-only/bounded.
- **NFR-SEC-005** — Profile/auth tests. Completion signal: /admin route presence is never claimed as authorization boundary.
- **NFR-SEC-006** — Container inspection tests. Completion signal: HugeGraph/model not exposed externally by default.
- **NFR-SEC-007** — Audit coverage tests. Completion signal: Sensitive operation has traceable audit ID.
- **NFR-REL-001** — Kill/restart E2E. Completion signal: No duplicates or silent skipped records after restart.
- **NFR-REL-002** — Backup/restore E2E. Completion signal: Restored demo reproduces expected counts/path queries.
- **NFR-OPS-001** — Health/log tests. Completion signal: Failure can be followed by correlation ID.
- **NFR-OPS-002** — Metric scrape tests. Completion signal: Key MVP metrics are machine-readable.
- **NFR-PERF-001** — Automated benchmark smoke + manual full run. Completion signal: Published numbers identify dataset/hardware/version.
- **NFR-MAINT-001** — Dependency/lint tests. Completion signal: Core can later split without changing external contracts.
- **NFR-PRIV-001** — Redaction fixtures. Completion signal: Audit/log exports contain no prohibited content.
