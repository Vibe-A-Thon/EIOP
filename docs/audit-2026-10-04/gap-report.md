# EOIP documentation and acceptance gap audit

## Current progress (supersedes historical totals below)

The [current snapshot](./current-gap-report.json) indexes **172 documents /
29,538 lines** and **1,428 candidate records: 0 Done, 224 Partial, 1,204 Missing**.
Certified semantic review: **0/172 documents, 0/1,428 candidates**; acceptance
verification: **0/1,428**. These are evidence-triage counts, not proof of missing behavior.
Latest local regression: **1,486 passed, 31 skipped, 0 failures/errors** out of
1,517 cases; content-bound PASS at `2026-10-04T20:33:58.615862+00:00`.
Phase 1 tooling is implemented; publication, remote CI, review and later phases
remain paused/pending. See the [checklist](./completion-checklist.md) and
[test report](./test-report.md). Original snapshot figures below are historical.

> Historical snapshot. See the [current gap report](./current-gap-report.md) and
> [phase specification and decisions](./phase-1-spec.md) for the newly authorized
> KGR-inclusive scope. Counts below are not current completion evidence. The
> [inventory](./documentation-inventory.json) has been refreshed as a mechanical
> read ledger; it does not certify this older review's semantic completeness.

**Audit date:** 2026-10-04
**Repository/branch:** `Vibe-A-Thon/EIOP`, `feature/audit-evidence-foundation`
**Role:** QA Lead; read-only documentation audit
**Scope:** First-party Markdown/text requirements and traceability evidence, bounded by the actual read ledger in [documentation-inventory.json](./documentation-inventory.json).
**Structured rows:** [gap-report.json](./gap-report.json)

## Executive result

This is a **partial documentation audit, not an implementation or completion audit**. I reviewed 22 of 153 safe-content-review-target Markdown/text files completely, partially read one more, and did not read 130. One additional tracked example-token file was withheld from content inspection. The two expressly excluded KGR documents were not read, hashed, or used. Ignored/runtime documentation was counted by metadata only.

The fully reviewed core catalogs yield **109 distinct canonical FR/NFR/MVP IDs**: FR 67, NFR 14, MVP-FR 28. All 109 remain `assessment_pending`; **zero were verified**, including all 28 P1 MVP rows. A separate mechanical scan found 518 explicit GAP/G2 tokens; their catalogs remain unread in full and all 518 await semantic reconciliation.

**Post-audit evidence update:** the parent validation report now records a later source-bound local PASS at HEAD `47bc8516d76031481c637780ddf8952ca865f2e1`: 1,207 outcomes, 1,192 passed, 15 skipped, zero failures/errors, with receipts `test-results\audit-source-bound-validation.json` and `test-results\audit-full-regression.xml`. The earlier ordinary full pytest result remains historical: 1,106 outcomes (1,091 passed, 15 skipped, zero failures/errors), receipt `test-results\audit-phase1-regression.xml`, not source-bound because source edits overlapped it. Remote CI and independent review remain unobserved. This bounded audit still did not independently verify those results, inspect source/test binding, or run tests; the later [mvp-gap-report.md](./mvp-gap-report.md) is the current implementation-evidence artifact for MVP/Core P1 closure.

A literal identifier scan across the core FR/NFR/MVP catalogs, the four GAP/G2 catalogs, and the requirements map found **627 distinct explicit tokens**: FR 67, NFR 14, MVP-FR 28, GAP 286, and G2 232. This is a mechanical count, not semantic review of the gap catalogs; range/wildcard shorthands were not expanded.

## MVP acceptance matrix

The criterion text below is condensed from the normative [MVP-requirements.md](../../EOIP-engg-doc-pkg/MVP-requirements.md); the parent-ID and T-task mapping follows [mvp-traceability.csv](../../EOIP-engg-doc-pkg/traceability/mvp-traceability.csv). Source line citations point to each numbered MVP criterion. All statuses remain `assessment_pending` because documentation alone cannot establish implementation or runtime behavior.

| ID | Acceptance criterion (condensed) | Parent IDs / task | Source | Status | Risk | Next concrete validation |
|---|---|---|---:|---|---|---|
| MVP-FR-001 | Compose HugeGraph startup; restart persistence; graph internal-only by default | FR-GRAPH-001 / T01 | [MVP-requirements.md:68](../../EOIP-engg-doc-pkg/MVP-requirements.md#L68) | assessment_pending | P0 | Inspect Compose/network bindings; run clean start, graph write/read, restart persistence, and host-port exposure checks. |
| MVP-FR-002 | Fresh schema bootstrap; repeat startup is idempotent | FR-GRAPH-003 / T02 | [MVP-requirements.md:74](../../EOIP-engg-doc-pkg/MVP-requirements.md#L74) | assessment_pending | P0 | Test clean initialization, second-run no-op, and incompatible schema failure without data loss. |
| MVP-FR-003 | Configurable synthetic Jira JSON mapping; per-record validation and evidence | FR-CONN-002 / T03 | [MVP-requirements.md:80](../../EOIP-engg-doc-pkg/MVP-requirements.md#L80) | assessment_pending | P0 | Import fixture; assert expected entities, provenance, malformed-row isolation, and repeat idempotency. |
| MVP-FR-004 | Local repository plus GitLab-style MR/pipeline fixture yields linked facts | FR-CONN-003, FR-CONN-004 / T04 | [MVP-requirements.md:86](../../EOIP-engg-doc-pkg/MVP-requirements.md#L86) | assessment_pending | P0 | Ingest a temporary repository and fixture; verify commit/MR/pipeline/work-item links and offline operation. |
| MVP-FR-005 | Python and TypeScript parsing yields symbols/ranges/imports/calls without LLM parsing | FR-CODE-001, FR-CODE-002 / T05 | [MVP-requirements.md:92](../../EOIP-engg-doc-pkg/MVP-requirements.md#L92) | assessment_pending | P0 | Run parser golden tests and compare exact symbols, source ranges, and static dependency edges. |
| MVP-FR-006 | Stable canonical IDs; identical re-ingestion creates no logical duplicate | FR-INGEST-002, FR-GRAPH-004 / T06 | [MVP-requirements.md:98](../../EOIP-engg-doc-pkg/MVP-requirements.md#L98) | assessment_pending | P0 | Compare IDs and logical graph counts over repeated imports; test collision and ambiguous identity cases. |
| MVP-FR-007 | Queryable Jira project/work-item subgraph with provenance | FR-ONTO-001, FR-GRAPH-002 / T07 | [MVP-requirements.md:104](../../EOIP-engg-doc-pkg/MVP-requirements.md#L104) | assessment_pending | P1 | Query fixture records and trace a returned fact to source event and ingestion run. |
| MVP-FR-008 | Queryable repository→file→symbol and dependency graph with exact source locations | FR-CODE-001, FR-CODE-004 / T08 | [MVP-requirements.md:110](../../EOIP-engg-doc-pkg/MVP-requirements.md#L110) | assessment_pending | P0 | Verify persisted symbol/dependency paths including revision, path, and exact range. |
| MVP-FR-009 | Queryable meta graph for sources/runs/domains/versions/validation/quality | FR-GRAPH-005 / T09 | [MVP-requirements.md:116](../../EOIP-engg-doc-pkg/MVP-requirements.md#L116) | assessment_pending | P1 | Reconcile persisted run, source/domain/version records, statistics, and validation snapshot. |
| MVP-FR-010 | Complete demo path is traversable forward and reverse with evidence | FR-GRAPH-006 / T10 | [MVP-requirements.md:122](../../EOIP-engg-doc-pkg/MVP-requirements.md#L122) | assessment_pending | P0 | Assert the ordered Jira→MR→commit→file→function→dependency→pipeline→documentation path and reverse traversal. |
| MVP-FR-011 | Cross-domain edges have evidence/status; lineage reaches capture/run | FR-PROV-001, FR-PROV-002 / T11 | [MVP-requirements.md:128](../../EOIP-engg-doc-pkg/MVP-requirements.md#L128) | assessment_pending | P0 | Measure evidence coverage across all demo bridge edges and trace deterministic/inferred facts to capture/run. |
| MVP-FR-012 | Seeded invalid data creates findings; hard-invalid edges are blocked/quarantined | FR-VALID-001, FR-VALID-002 / T12 | [MVP-requirements.md:134](../../EOIP-engg-doc-pkg/MVP-requirements.md#L134) | assessment_pending | P0 | Seed invalid endpoint/domain/provenance cases and reconcile rejection/findings with the admin view. |
| MVP-FR-013 | Versioned REST returns real data and enforces query policy | FR-QUERY-001, FR-QUERY-006 / T13 | [MVP-requirements.md:140](../../EOIP-engg-doc-pkg/MVP-requirements.md#L140) | assessment_pending | P0 | Exercise fixture-backed API requests and depth/result/timeout/relationship-policy boundaries. |
| MVP-FR-014 | Golden impact set and evidence paths within configured limits | FR-QUERY-003 / T14 | [MVP-requirements.md:146](../../EOIP-engg-doc-pkg/MVP-requirements.md#L146) | assessment_pending | P0 | Compare exact golden results and paths; exercise cycle and depth/result/time bounds. |
| MVP-FR-015 | Jira issue→function path matches golden ordered vertices/edges | FR-QUERY-002 / T15 | [MVP-requirements.md:152](../../EOIP-engg-doc-pkg/MVP-requirements.md#L152) | assessment_pending | P0 | Run known, unknown, and over-depth path cases against the ordered golden sequence. |
| MVP-FR-016 | Search/query UI uses APIs; API outage shows error, not canned fallback | FR-UI-001 / T16 | [MVP-requirements.md:158](../../EOIP-engg-doc-pkg/MVP-requirements.md#L158) | assessment_pending | P1 | Trace UI results to API responses; stop API and verify explicit failure with no demo data. |
| MVP-FR-017 | Visualizer shows bounded real graph, typed edges, paths, and provenance | FR-UI-002 / T17 | [MVP-requirements.md:164](../../EOIP-engg-doc-pkg/MVP-requirements.md#L164) | assessment_pending | P1 | Render persisted demo path, verify evidence access, and test expansion caps. |
| MVP-FR-018 | Admin UI reflects real run counts/status, graph stats, findings, quality | FR-ADMIN-001, FR-ADMIN-002 / T18 | [MVP-requirements.md:170](../../EOIP-engg-doc-pkg/MVP-requirements.md#L170) | assessment_pending | P1 | Reconcile displayed values against API/meta graph; confirm route separation is not auth. |
| MVP-FR-019 | VS Code symbol view returns Jira/commit/dependency/docs/evidence and exact range | FR-VSCODE-001, FR-VSCODE-002 / T19 | [MVP-requirements.md:176](../../EOIP-engg-doc-pkg/MVP-requirements.md#L176) | assessment_pending | P1 | Extension-host test on canonical demo symbol; assert context, offline state, and exact navigation. |
| MVP-FR-020 | GraphRAG returns graph/document evidence and citations; model-down structured fallback | FR-RAG-001, FR-RAG-002, FR-RAG-003 / T20 | [MVP-requirements.md:182](../../EOIP-engg-doc-pkg/MVP-requirements.md#L182) | assessment_pending | P0 | Prove actual local inference and citation grounding, then stop model and verify structured fallback. |
| MVP-FR-021 | TraceImpactAgent answers demo request with allowlisted read tools and budgets | FR-AGENT-003 / T21 | [MVP-requirements.md:188](../../EOIP-engg-doc-pkg/MVP-requirements.md#L188) | assessment_pending | P0 | Run workflow; capture evidence, audit/tool allowlist, budget-exhaustion and denied-write checks. |
| MVP-FR-022 | MCP semantics match REST for entity/path/impact/evidence; no write tool | FR-MCP-001, FR-MCP-002 / T22 | [MVP-requirements.md:194](../../EOIP-engg-doc-pkg/MVP-requirements.md#L194) | assessment_pending | P0 | Compare MCP and REST fixture results; inspect capabilities for absence of mutation tools. |
| MVP-FR-023 | Structured correlated workflow/failure logs, no secrets | NFR-OPS-001 / T23 | [MVP-requirements.md:200](../../EOIP-engg-doc-pkg/MVP-requirements.md#L200) | assessment_pending | P1 | Capture representative success/failure logs, correlate IDs, and test redaction. |
| MVP-FR-024 | Local machine-readable ingestion/query/model/agent/failure metrics | NFR-OPS-002 / T24 | [MVP-requirements.md:206](../../EOIP-engg-doc-pkg/MVP-requirements.md#L206) | assessment_pending | P1 | Scrape metrics after representative workflows; verify series and optional-profile behavior. |
| MVP-FR-025 | Checksummed graph/application backup artifact from demo data | NFR-REL-002 / T25 | [MVP-requirements.md:212](../../EOIP-engg-doc-pkg/MVP-requirements.md#L212) | assessment_pending | P0 | Create populated backup; verify manifest/checksum/coverage and failure is not reported as success. |
| MVP-FR-026 | Clean-target restore reproduces expected counts and golden queries | NFR-REL-002 / T26 | [MVP-requirements.md:218](../../EOIP-engg-doc-pkg/MVP-requirements.md#L218) | assessment_pending | P0 | Restore into empty target; compare counts and rerun golden path/impact queries. |
| MVP-FR-027 | Local unit/contract/integration/security/E2E suites produce a report | NFR-MAINT-001 / T27 | [MVP-requirements.md:224](../../EOIP-engg-doc-pkg/MVP-requirements.md#L224) | assessment_pending | P0 | Full source-bound validation is BLOCKED for this focused-check publication; reassess with a stable source snapshot, inspect suite binding, retain provenance-linked reports, and verify remote CI. |
| MVP-FR-028 | Clean-reset end-to-end flow includes persisted data and backup/restore | FR-GRAPH-006, FR-AGENT-003 / T28 | [MVP-requirements.md:230](../../EOIP-engg-doc-pkg/MVP-requirements.md#L230) | assessment_pending | P0 | Run the whole documented sequence and repeat golden checks from restored state. |

The mapping to T01–T28 is a traceability reference, not confirmation that those implementation tasks have been completed. The separate [MVP-implementation-plan.md](../../EOIP-engg-doc-pkg/MVP-implementation-plan.md) and [67-implementation-plan.md](../../EOIP-engg-doc-pkg/67-implementation-plan.md) were not read in this bounded pass.

## Broader requirements and release gates

The fully read core catalogs define 67 FR IDs and 14 NFR IDs in addition to the 28 MVP IDs. Their current implementation state is **assessment_pending**: this audit did not inspect implementation evidence. The principal catalog links are [03-functional-requirements.md](../../EOIP-engg-doc-pkg/03-functional-requirements.md), [04-non-functional-requirements.md](../../EOIP-engg-doc-pkg/04-non-functional-requirements.md), and [70-acceptance-criteria.md](../../EOIP-engg-doc-pkg/70-acceptance-criteria.md). The crosswalk is [72-requirement-traceability.md](../../EOIP-engg-doc-pkg/72-requirement-traceability.md); the 28-row MVP-to-task matrix is [mvp-traceability.csv](../../EOIP-engg-doc-pkg/traceability/mvp-traceability.csv).

| Gate | Boundary / required evidence |
|---|---|
| Fixtures versus live integrations | P1 requires synthetic Jira JSON, local Git, and GitLab-style fixture behavior. Live integrations or real-source schema claims require their own explicit evidence. |
| Local AI | A local provider configuration does not establish true inference. Verify a real local-model response grounded in graph/document evidence, plus model-down fallback. |
| Temporal behavior | P1 temporal/version fields and current-state views are not snapshots or point-in-time truth. Snapshots/diffs are P5. |
| Backup versus DR | P1 checksummed backup/restore is distinct from native disaster-recovery guarantees, HA, and measured RPO/RTO targets. |
| VS Code | Required P1 surface; needs extension-host evidence and exact symbol range/context, not README or code-presence evidence. |
| Offline/SBOM | Restricted/offline run and SBOM/dependency/license outputs must be demonstrated after dependencies/models are staged; no such run occurred. |
| Performance | Dataset and latency/readiness values are targets only; no throughput, percentile, resource, or readiness benchmark was measured. |
| Security boundaries | No MVP RBAC does not remove authentication, network isolation, secret hygiene, audit, and read/write separation requirements. |

## Ambiguities and resolved interpretation

1. **No RBAC is not no authentication.** P1 uses the documented local/single-user authentication profile; `/app`, `/admin`, and API URL separation are not authorization controls.
2. **Read-only AI/MCP versus admin operations.** User-facing graph operations and agent/MCP tools remain read-only. Explicit administrative ingestion/schema/backup/restore operations do not imply unrestricted Gremlin or agent writes.
3. **Temporal fields versus historical truth.** Persisting temporal fields in P1 does not mean the graph answers point-in-time questions. Snapshot/diff/temporal intelligence remains P5.
4. **Synthetic demo tenancy.** Do not infer tenant isolation or product RBAC from synthetic multi-tenant examples.
5. **Demo path casing.** Current canonical paths are `demo\demodata\manual`, `demo\demodata\pipelines`, `demo\script\walkthrough.md`, `demo\script\presentation.pptx`, and `demo\autodemo`.
6. **Performance thresholds.** Treat figures as acceptance targets until reproducible results identify dataset, hardware, and version.
7. **Jira source provenance.** No actual Jira schema was supplied/reviewed for this audit; do not claim that real Jira data has been analyzed.
8. **GAP/G2 legacy material.** The explicit-ID scan does not establish which proposals remain active, are superseded, or belong to later phases. Read and reconcile the four gap catalogs before importing their requirements into the active backlog.

## Phase sequencing recommendation

- **P0 — evidence foundation:** Verify source binding and baseline evidence for the restored validation harness; finish requirement/plan reconciliation before asserting completion.
- **P1 — real integrated MVP:** Gate on all 28 rows, including persisted HugeGraph data, no-egress/security, exact golden path/impact behavior, local-model-on and model-down modes, extension-host behavior, MCP read-only parity, backup/restore, and end-to-end demo.
- **P2 — connector/ontology expansion:** Confluence, ServiceNow, and explicit RDF/OWL/JSON-LD adapter behavior.
- **P3 — retrieval expansion:** Evaluate optional local embeddings/vector retrieval and advanced RAG against measured baseline.
- **P4 — multi-agent workflows:** Only justified patterns, under P1 tool and execution bounds.
- **P5 — temporal intelligence:** Snapshots, diffs, point-in-time and deeper analytics; snapshots must not be represented as current live truth.
- **P6 — governed action:** Human approval and explicitly separated write/action registry.
- **P7 — enterprise hardening:** Evaluate RBAC/SSO, HA, quotas, tenancy/isolation, and DR/SLO operation.
- **P8+ — self-modification:** Proposal/sandbox/evaluation/approval/rollback only; never unreviewed production mutation.

The normative phase source read in this audit is [66-phase-roadmap.md](../../EOIP-engg-doc-pkg/66-phase-roadmap.md). This sequencing is a recommendation, not a claim that any phase is complete.

**Mandatory stop:** complete and review the first-phase PR/review gate, then stop. This audit did not perform that review and does not authorize progression beyond it.

## Reading coverage and exclusions

- The inventory contains 153 tracked nonignored `.md`/`.txt` paths and one untracked ticket. Of the 153 safe-content-review-target documents, 22 were fully read, one was partially read, and 130 remain unread.
- `secrets.example\api-token.txt` was counted by path only; its contents and hash were withheld.
- `EOIP-engg-doc-pkg\KGR-requirements.md` and `EOIP-engg-doc-pkg\KGR-implementation-plan.md` were expressly excluded, including from hashing, analysis, and evidence.
- Ignored runtime/vendor documentation totals 639 files / 3,631,431 bytes from metadata and was not content-reviewed.
- The 2,374-line `source-master-prompt.txt` was only partially and inconclusively read because large views were truncated; the inventory marks it `partial`, not complete.
- The four `gaps*` catalogs were mechanically scanned for ID tokens but were not read in full. The 627 total is exact-token inventory only; shorthand ID ranges are not expanded.
- No source files or tests were audited for acceptance, no behavior was verified, and this audit ran no test/build/deployment. Parent-reported checks now include the 45 focused regression outcomes, scoped Ruff, and a later source-bound full regression PASS with 1,207 outcomes / 1,192 passed / 15 skipped / zero failures/errors. Workflow YAML structure was checked but remote CI was not observed; see `validation-evidence-phase1.md` for parent-recorded commands and boundaries.
- The worktree already contained unrelated/parent-owned changes. The original bounded audit wrote only the three files under `docs\audit-2026-10-04\`; later documentation synchronization updated the audit notes and coordination Markdown without modifying KGR files, wrapper code or production code.

## Exact next actions to complete the audit

1. Complete and review the first-phase PR/review gate; stop at that gate and do not proceed to later phases.
2. Treat the local source-bound PASS as author-executed implementation evidence, not independent release certification. Obtain an observed remote CI result and independent review before revising release acceptance verdicts.
3. Finish full, bounded reads for the 130 unread safe documents; recover every truncated range and update the inventory only when the full file is actually read.
4. Read `gaps-requirements.md`, `gaps-implementation.md`, `gaps2-requirements.md`, `gaps2-implementation.md`, `67-implementation-plan.md`, and `MVP-implementation-plan.md`; reconcile all 518 scanned GAP/G2 tokens with active canonical IDs and phases, without wholesale ID renaming.
5. When authorized, validate clean-state fixture ingestion, repeat/restart, real local inference/model-down fallback, extension host, MCP/REST parity, no-egress/offline package, backup/restore, and measurable performance.
6. Keep unsupported verdicts `assessment_pending`; assign Partial/Missing only after current evidence establishes that status.
