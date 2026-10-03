# EOIP/KnowGridFlow — Phase Completion Audit Checklist

**Date:** 2026-10-03
**Method:** every Markdown document in the repository was read and analyzed (EOIP-engg-doc-pkg root: 00–75 series, MVP requirements/plan, gaps/gaps2 requirements + implementation, KGR requirements + implementation plan, knowgridflow product architecture, all 17 diagrams, implementation work packages, examples, traceability catalog; plus repo docs/). Backend and frontend were audited file-by-file against those obligations; all P0 defects were fixed and re-verified.

## Latest bounded certification - 2026-10-04

**Temporal compatibility follow-up:** the newer
[full-host receipt](../test-results/temporal-compatibility-full.xml) now contains
**1,031 outcomes: 1,016 passed / 0 failed / 0 errors / 15 skipped**. Eight added
outcomes cover legacy restored physical identities, normalized ingestion,
replacement/deletion/reversion, deletion-only revision recreation and the
disposable temporal acceptance helper. The failed-first selection had seven
failures before the repair. The
[rebuilt HugeGraph receipt](../test-results/eoip-acceptance-d8225f6f8365484782688753b7ce2959.json)
passes legacy expiry, current-only replacement, deletion barriers and recreation
with exactly three physical history edges. Its separately verified demo snapshot
contains 115 vertices, 345 edges and 11 raw files. Primary readiness remains green;
the primary deployment was not modified. This follow-up did not rerun Chromium
or reread every Markdown file; the earlier UI/audit evidence remains historical.
See [the gap audit](gap-audit-2026-10-02.md) for boundaries and current receipts.

**The current automated demo gate is green; overall product certification remains
bounded, not complete.** The refreshed full-host
[receipt](../test-results/full-regression-2026-10-04.xml) contains **1,023
outcomes: 1,008 passed / 0 failed / 0 errors / 15 skipped**. The five temporal
and documentation-reference failures in `recovery-bundle-final-host.xml` were
repaired and are historical. Full Docker smoke passes, all five Chromium
journeys pass, the rebuilt primary stack is healthy, and the live catalog reports
8/8 Northstar scenarios ready.

The isolated real-HugeGraph acceptance gate is also **PASS**; see
[`eoip-acceptance-0e315bbbdca147d5b50c7d96e9da287a.json`](../test-results/eoip-acceptance-0e315bbbdca147d5b50c7d96e9da287a.json).
It proves replay equivalence, clean validation, canonical-ingestion contracts,
populated-target refusal and fail-closed schema preflight without touching the
primary volumes. Live primary validation has zero errors but retains warnings
from older development entities, so the isolated receipt is the clean sales
claim.

Completed within this batch's scope:

- Self-contained logical configuration/model-byte recovery: **62 focused tests
  pass**; combined recovery/evidence regression: **78 pass**, exit 0.
- Rebuilt isolated Docker recovery: **PASS**, exact graph/raw/operational/config/
  binary equality, checkpoint equality, held jobs, golden queries and refusal
  of populated destinations. The fixture has 112 vertices, 320 edges, 11 raw
  files, 9 asset files and one 1,310,720-byte synthetic Ollama-layout blob;
  [receipt](../test-results/eoip-recovery-acceptance-b604ed44ee93462c93ee783d5badfd61.json).
  Disposable project resources are absent; primary readiness is HTTP 200/`ready`.
  No primary reset/redeployment was performed.
- Fail-closed executable evidence mapping for all 28 MVP requirements:
  **16 checker cases pass** in the combined selection. The actual
  [report](../test-results/mvp-requirement-evidence.json) is `EVIDENCE_GAPS`,
  exits 1 and maps passing annotations for only 3/28 rows (10.71%).
  This is **annotation coverage, not development completion**. Absent
  annotations do not prove absent functionality, and current source hashes do
  not retrospectively revision-bind the full-host JUnit receipt.

Still open: explicit mapped evidence for the remaining 25 MVP rows;
native/crash-consistent recovery; webhook receipt/path rebasing;
memory/audit/trace recovery; actual installed-model readability/inference;
live tenants and attachment bytes; live/visual/packaged extension acceptance;
and revision-linked release SBOM/license/no-egress/hardware benchmark evidence.
Later-phase code availability alone is not requirement-level certification.
See [the reconciled gap audit](gap-audit-2026-10-02.md) for exact failing checks
and recovery boundaries.

**Earlier verified release-operations baseline (2026-10-03):**
- Working tree based on `9a70e5a24c06722c60f0f97a57e5187db6a7fe27`, not a committed release.
- `scripts/docker.ps1 test` — exit 0: **477 Python tests**, live container smoke checks and **4 Chromium journeys** passed.
- `scripts/docker.ps1 acceptance` — exit 0: two fresh isolated HugeGraph servers, 53 vertices / 141 edges / 9 raw records, exact logical restore equality and populated-target rejection passed.
- Primary API readiness and web returned HTTP 200; disposable acceptance resources were removed without resetting primary data.
- Earlier local baseline: 467 Python tests and full Ruff passed.

**Registered v2 replay batch (2026-10-03):**
- The isolated API/worker/HugeGraph DLQ gate now passes six named journeys,
  including registered Confluence v2 PARTIAL rejection, persistent mapper
  recovery, stable logical replay equivalence, and registry admission refusals.
- Receipt: `test-results/eoip-dlq-acceptance-f7ad5bc7752d499b930138f885b52db1.json`
  with matching XML; exit 0, zero skipped runtime cases.
- Full host regression: 537 passed / 6 opt-in skips; final focused receipt
  tests: 9 passed / 6 skips. Changed-file Ruff passes.
- Disposable resources cleaned; primary readiness confirmed. No production
  logic changes or primary redeployment. Local captured replay does not certify
  live upstream acquisition, other registered adapters or the remaining roadmap.

**ServiceNow acquisition and replay-admission batch (2026-10-03):**
- Fixed registered DLQ replay bypassing the source scheduler. Paired endpoint
  tests verify disabled, paused, replay-capability, concurrency and rate refusals
  enqueue no jobs and perform no graph writes.
- Shared REST connectors now forward `X-Correlation-ID` upstream; actual HTTP
  fixture tests cover successful acquisition and upstream authentication failure.
- Nine exact-name Docker journeys pass, exit 0, with zero failures/errors/skips.
  ServiceNow baseline pagination across four tables, five persisted entities
  and evidence links, checkpointed incremental sync, idempotent capture replay,
  mapping rejection and persistent upstream authentication failure are certified.
- Receipt: `test-results/eoip-dlq-acceptance-9cce39ba324243179ff3e71922eae4e1.json`
  and matching XML. Earlier failing receipts remain FAIL. The first exposed
  missing correlation and an incorrect 422 audit expectation; the second
  exposed omitted polling capability in test registration.
- Full host suite: **557 passed, 9 opt-in skips**, exit 0. Focused endpoint,
  fixture, adapter and receipt regression: **45 passed**, exit 0. Changed-code
  Ruff, editor diagnostics and whitespace checks pass.
- Disposable DLQ containers/network/volume removed; primary readiness is
  `ready`. No primary redeployment/reset. ServiceNow is an authenticated
  internal HTTP protocol fixture, not a live tenant; other adapters, release
  non-functional gates and the remaining roadmap are still open.

**Confluence HTTP acquisition and provenance batch (2026-10-03):**
- Added authenticated Data Center REST protocol fixture and three multi-step
  API/worker/HugeGraph journeys: paginated baseline with hierarchy/evidence,
  incremental refresh and immutable replay; fetched mapping rejection; and
  persistent authentication/schema-drift/invalid-response failures.
- Fixed shared REST ingestion overwriting immutable Evidence capture timestamps
  and replay regressing observation freshness. Two deterministic source-specific
  regressions failed before repair and now pass; only the unchanged space's
  `last_seen` may change during incremental polling, not its semantic graph.
- Final exact-name Docker gate: **12 passed, zero failures/errors/skips**, exit 0.
  Receipt: `test-results/eoip-dlq-acceptance-ccb926603ecc45639d64f167236a7c4c.json`
  with matching XML. The first 11-pass/1-failure receipt remains FAIL.
- Final UTF-8 host suite: **565 passed, 12 opt-in skips**, exit 0; focused
  regression: **44 passed**, exit 0. Changed-code Ruff/editor diagnostics,
  PowerShell parser and whitespace pass. Disposable resources removed;
  primary readiness `ready`; no primary reset/redeployment by this batch.
- FR-CONF-001 and G2-T0401..0404 are certified only for the documented acquisition/
  hierarchy/attachment-metadata scope, not completely discharged. Real tenant,
  historical versions, authors/labels, attachment bytes, body-structure extraction,
  semantic linking and stale-document detection remain unverified/open.

**Confluence structured body extraction batch (2026-10-03):**
- G2-SRC-CONF-003 practical storage extraction is implemented: headings, explicit
  anchors, safe URL links and unresolved resource references, literal code
  snippets and structured tables. Versioned output uses Document `payload_json`;
  Document/Evidence carry `confluence-storage/1.0`. Raw body/capture and temporal
  revision history remain intact.
- Empty/missing body clears current content; old replay cannot reinstate it.
  Malformed/bounded-input violations are captured and DLQ'd before business writes.
- Full host regression: **578 passed / 12 opt-in skips**, exit 0; focused
  regression **43 passed**; final parser/history assertions **13 passed**.
  Changed-code Ruff/editor diagnostics and whitespace checks pass.
- Rebuilt isolated Docker API/worker/HugeGraph gate: **12 passed**, exit 0,
  no failures/errors/skips. Receipt:
  `test-results/eoip-dlq-acceptance-2b3b094995e84c87851c8a2b8b79ef81.json`
  with matching XML. Both disposable projects removed; primary readiness
  `ready`; primary was not redeployed/reset.
- Extraction is not semantic document/entity linking or arbitrary rendered macro
  expansion. Real tenants, authors/labels, source history fetching, attachment
  bytes, stale detection and remaining release/roadmap gates remain open.
  Earlier batch boundary statements above describe their original scope.

**Confluence history/reference freshness and temporal recovery batch:**
- G2-SRC-CONF-002/004/005 now have bounded implementation and fixture
  certification: complete public version-metadata acquisition and immutable
  replay; exact evidence-backed document links; shared referenced-fact
  freshness through validation, stale API and the governed agent.
- Ontology 0.4.0/schema 1.2 add 21 document-reference lookup indexes.
  Initial Docker failure (10 passed / 2 failed) is retained as FAIL:
  `test-results/eoip-dlq-acceptance-00342b77ba7f468d975b74ddd07be9b2.json`.
  Required Service identity and missing indexes were corrected, not bypassed.
- Fixed temporal deletion/reversion ordering and historical interval loss.
  Logical recovery now preserves tombstones/expired edges and rejects even
  tombstone-only destinations; unit round-trips preserve as-of barriers.
- Final full host regression: **625 passed / 12 opt-in skips**, exit 0.
  Changed-Python Ruff and whitespace checks pass. Existing dependency
  deprecation warning remains unchanged.
- Final isolated API/worker/HugeGraph gate: **12 passed / zero failures/
  errors/skips**, exit 0. Stale API returns HTTP 200 with two changed-target
  findings that survive offline capture replay. Receipt:
  `test-results/eoip-dlq-acceptance-0c5d4828d59f44d295db5a66169bdcef.json`.
- Final canonical/exact logical recovery: **PASS**, exit 0; 111 vertices /
  345 edges / 11 raw records, zero validation errors, replay equivalence,
  populated-target refusal and four nonmutating schema incompatibility
  refusals. Receipt:
  `test-results/eoip-acceptance-3199c002c5b44eae9ee9808d232492d7.json`.
- Both disposable projects are completely removed; primary readiness `ready`.
  Primary deployment/data remain unchanged. This supersedes earlier open-history/
  explicit-link/freshness statements only within this batch's bounded scope,
  not full G2-P4 sign-off or 100% application completion.
- Live tenants, inferred semantic matching, attachment bytes, configuration/
  checkpoint/job/native recovery, other adapters, release non-functional
  gates and remaining G2-P6..P10 functionality are not certified by this batch.

**Operational state and held-job recovery batch (2026-10-03):**
- G2-REL-006/007/008 and G2-T1046 gain bounded logical preservation of registry,
  acquisition policies, connector checkpoints, state reports, semantic journal
  and durable jobs. Stale worker heartbeat is excluded.
- User-approved policy: interrupted PENDING/RUNNING jobs become HELD; worker
  startup does not execute them. Authenticated, audit-preflighted readmission
  retains the ID and rechecks current source admission. Confirmation-gated admin
  controls provide readmission and cancellation, with visible refusal errors.
- Fixed a compatibility defect found during final review: normal DEMO jobs use
  null payloads. Export/restore now preserve those jobs rather than rejecting
  legitimate history; malformed registered-source payloads still refuse.
- Final full host regression: **646 passed / 12 opt-in skips**; focused recovery
  contracts: **37 passed**. Changed-code Ruff, editor diagnostics and whitespace
  checks pass. Frontend production build passes (existing chunk-size warning).
- Edge fixture-backed admin flow: **1 passed**, zero page errors.
  `test-results/operational-recovery-browser.xml`.
- Final isolated API/independent-worker/HugeGraph gate: **12 passed**, no
  failures/errors/skips; actual HELD dormancy, same-ID HTTP 202 readmission,
  successful execution and duplicate HTTP 409 refusal are asserted.
  `test-results/eoip-dlq-acceptance-b556b50c177a4581973df82ce5d4b509.json`.
- Final exact logical recovery: **PASS**, 111 vertices / 345 edges / 11 raw
  records, checkpoint equality, active-job hold and heartbeat omission.
  `test-results/eoip-acceptance-dc9fb89bd0734a50b46fd808af24159e.json`.
- Final disposable containers/networks/volumes are removed; temporary frontend
  stopped; primary deployment/data untouched and readiness remains `ready`.
- Logical export requires quiescence and is not atomic/native recovery.
  Configuration/model artifacts, webhook receipts/path rebasing, audit/trace
  history, live tenant certification, distributed admission and remaining
  roadmap/release/hardware gates are not closed by this batch.

**Schema-compatibility batch (2026-10-03, `6f6149b` + working-tree changes):**
- Gap 22 adds a fail-before-mutation structural compatibility preflight; compatible additive bootstrap remains supported.
- Full local `python -X utf8 -m pytest`: **505 passed**, exit 0; focused schema/recovery/repository suite: **35 passed**, exit 0; changed-file Ruff and editor error diagnostics pass.
- The initial plain Windows full run failed seven existing UI-file decoding tests; UTF-8-mode rerun resolves the locale mismatch without unrelated source changes.
- Gap 18 already has bounded history and diff-hunk implementation/tests; gap 19's then-unwired helper is addressed in the following batch.
- Isolated HugeGraph acceptance: exit 0, 54 vertices / 142 edges / 10 raw records; replay/restore pass. Four incompatible manifest proposals cause no schema mutations and preserve exact raw graph/schema state. Receipt: `test-results/eoip-acceptance-8fa23747ff814739ab7439aacb9dde33.json`; primary volumes untouched.
- See [the reconciled original backlog](gap-audit-2026-10-02.md) for scope and next priorities. This batch does not replace the earlier live UI/extension evidence with new certification.

**Canonical-boundary batch (2026-10-03, same baseline + working-tree changes):**
- Gap 19 now routes all eight ingestion services, including temporal/domain writes and existing-entity tombstones, through validated NormalizedEntity/NormalizedRelationship/GraphMutation envelopes.
- Invalid identity/domain/confidence/status proposals fail before their write; real run IDs are required and context-isolated. Repository raw capture precedes its first graph mutation.
- Existing persisted projections, revision subject types, fact-based edge deduplication and missing-entity deletion no-ops are preserved. Administrative bulk/schema/reset and demo meta bootstrap remain outside the source-ingestion boundary.
- Final full UTF-8-mode Python suite: **528 passed**; focused canonical/recovery suite: **32 passed**. Changed-code Ruff and pipeline editor diagnostics pass; repository diff handling retains two baseline lint findings.
- Contract failures propagate and preserve captured input; automatic canonical-validation DLQ handling, transactional run rollback and full-scale endpoint-lookup performance certification are not claimed.
- New isolated HugeGraph acceptance: **PASS**, 54 vertices / 142 edges / 10 raw records, zero validation errors, replay and exact logical restore equality. Initial/replay consumed 53/53 vertex and 108/83 edge envelopes with two run IDs each. The schema refusal gate also passes. Receipt: `test-results/eoip-acceptance-94d8065314e34dc3a0f6ebdc3db5521c.json`; disposable resources removed, primary services healthy and not redeployed/reset.

**Live DLQ acceptance batch (2026-10-03):**
- Added `scripts/docker.ps1 dlq-acceptance`: fresh internal-only HugeGraph/API/worker, separate application volume, no host ports/primary mounts and targeted finally cleanup.
- Three real HTTP/worker journeys pass: genuine worker rejection and still-invalid replay remain PARTIAL; service-seeded obsolete-mapper rejection recovers with preserved raw input/evidence and idempotent replay; auth/missing capture/hash mismatch refusals enqueue nothing.
- Durable jobs, API/worker audit correlations and retained DLQ history are checked. Successful replay does not imply deletion/resolution of the historical DLQ record.
- Latest full UTF-8-mode host regression: **534 passed, 3 opt-in runtime tests skipped**, exit 0. The three runtime tests separately **passed in Docker**, exit 0. New-code Ruff and PowerShell syntax checks pass; editor workspace import-resolution warnings remain.
- Receipt: `test-results/eoip-dlq-acceptance-e97e862f386e406b9e71e94da9fff68c.json` plus matching JUnit XML. Primary services remained healthy and were not recreated/reset.
- This certifies Jira v1 replay only; registered v2/live sources, browser UI and crash/native/config/job-state recovery are not covered by this gate.

**Real VS Code host batch (2026-10-03):**
- Four multi-step journeys in installed VS Code 1.140.0 pass, exit 0, with all eight contributed commands executed.
- Fixed nonexistent document-symbol API usage and name-only range matching; real nested and flat providers resolve a cursor inside the function body.
- Search/entity read-back, path/impact/lineage/retrieval, exact source navigation, authentication/path refusal and offline preservation pass; source text remains unchanged.
- Unique user-data/extensions profiles are cleaned with bounded Windows lock retries before PASS. Missing/incomplete receipt, host failure or cleanup failure fails the gate.
- Receipt: `test-results/extension-host-a55403be-9158-4035-bcd2-7771cae2fc01.json`. JS syntax/editor checks pass; primary readiness remains ready.
- HTTP contract fixture and automated prompts are explicit test doubles. Live graph integration, manual UI, visual TreeView/webview and packaged-VSIX certification remain separate.
- Python/container/browser suites were not re-run for this JS-only batch; the preceding counts are historical.

**Scoped task-memory batch:**
- FR-MEM-001 / WP-AGENT-MEMORY-06 now enforce versioned file-backed task memory,
  30-day maximum retention, shorter per-record TTLs, count/byte limits, exact
  owner/scope isolation and classified minimized content. Only TraceImpact is
  approved; all other catalog agents remain RUN_ONLY.
- Corruption/capacity failures are explicit. Durable graph-run and trace
  persistence precede memory admission; warnings refresh result explanation
  uncertainty. Failed recalls consume the tool-call budget.
- Final full UTF-8 host suite: **840 passed / 15 opt-in skips**, zero failures/
  errors, exit 0: `test-results/scoped-memory-final-host.xml`.
  Focused selection: **66 passed**; conformance/receipt regression: **24 passed**.
  Changed-code Ruff/editor diagnostics pass.
- Rebuilt isolated API/worker/HugeGraph gate: **16 passed**, zero failures/
  errors/skips, exit 0. Includes three memory HTTP journeys and Linux
  independent-process writer certification; Windows is covered by host tests.
  Receipt: `test-results/eoip-dlq-acceptance-5382af51be56413f94e3a0ba07de70b8.json`
  and matching XML. Earlier 15-pass Docker evidence predates final refinements.
  Earlier 804-pass/1-failure host evidence remains FAIL.
- Disposable resources removed; primary not redeployed/reset. Idle disk expiry
  waits for startup/access; durable audit/trace/history retention, privacy of
  all exports, multi-tenant authorization, other memory kinds, memory snapshot
  recovery and crash-atomic multi-store persistence are not certified.
  Passing shared-working-tree tests do not establish a committed release.

**Interpretation:** IMPLEMENTED below describes code availability, not completed
end-to-end certification. Broader registered/live-source replay, live-backend/visual extension acceptance, broader
safety/quality/release evidence and later-phase partial obligations remain open.
See [the updated development audit](eoip-development-audit-2026-10-03.md) for the
tested scope, failures corrected, exclusions and remaining gates.

## Phase 1 / MVP (T01–T28) — IMPLEMENTED

| Task | Area | Evidence |
|---|---|---|
| T01–T02 | HugeGraph + schema bootstrap | `deploy/docker-compose.yml`, `packages/eoip/graph/hugegraph.py`, `scripts/bootstrap_schema.py`, manifest integrity test |
| T03–T05 | Jira/Git/GitLab/code parsing | `connectors/jira_json.py`, `ingestion/repository.py`, `codegraph/parser.py` (Python AST + tree-sitter TS) |
| T06–T09 | Canonical model, graphs, meta | deterministic URNs, idempotent upserts (edge dedup by `edge_key` UNIQUE index), meta graph, `BELONGS_TO_DOMAIN` on all ingestion paths |
| T10–T12 | Linking, provenance, validation | issue-key linking, `Evidence`/`EVIDENCED_BY`, lineage endpoint, **hard mutation-path gate** (`validation/gate.py`) + soft rule engine + N/A-correct quality metrics |
| T13–T15 | Query API, impact, path | typed `QueryPlan`, policy bounds, **NL→QueryPlan** (`query/nl.py`, `POST /api/v1/query/nl`), index-backed search, impact rationale + ranking |
| T16–T18 | Web UI, graph visualizer, admin | React app, Cytoscape + bundled Sigma.js/WebGL (no CDN), search/graph/impact/evidence/architecture/agent/KGR lenses, admin jobs/quality/audit/DLQ |
| T19 | VS Code extension | sidebar TreeView, body/nested/flat document-symbol resolution + word fallback, status-bar connectivity, traversal-guarded source opening; four real-host journeys cover all commands with an HTTP contract fixture |
| T20–T22 | GraphRAG, agent, MCP | strategy router + model-down fallback, **RAG eval harness** (`retrieval/eval.py`, `scripts/rag_eval.py`), governed agent runtime + catalog, 15 read-only MCP tools incl. `neighbors`/`document` with structured errors |
| T23–T24 | Logging, metrics | correlation IDs, JSON audit sink (API + worker), Prometheus counters/histograms, health endpoints |
| T25–T26 | Backup/restore | checksummed snapshot + restore verification (`snapshot.py`, `scripts/backup.py`, `restore.py`, `verify_restore.py`, restore-test compose profile) |
| T27–T28 | Tests, E2E demo | Latest 534 local Python passes / 3 opt-in skips plus 3 isolated live DLQ journeys; isolated canonical-ingestion/HugeGraph/logical-recovery acceptance; earlier 477 container tests, live smoke and 4 Chromium journeys; full release certification remains open |

## Gap-closure items from the 2026-10-02 audit — status

| # | Item | Status |
|---|---|---|
| 1 | HugeGraph edge dedup | **IMPLEMENTED** (`find_edge_by_key` + UNIQUE index + HugeGraph-backed unit test) |
| 2 | NL → QueryPlan | **IMPLEMENTED** (rule fast path + optional model drafting + clarification, adversarial fixtures) |
| 3 | Identity resolution wired in | **IMPLEMENTED** (shared email namespace, `source_aliases`, cross-source merge test) |
| 4 | Hard validation gates | **IMPLEMENTED** (`validation/gate.py` in both stores; unknown label/endpoint/key blocked pre-write) |
| 5 | Quality N/A + metrics | **IMPLEMENTED** (all coverage metrics return N/A on empty denominators; orphan/duplicate/freshness/completeness/schema-compliance) |
| 6 | RAG evaluation harness | **IMPLEMENTED** (golden fixture, precision/recall/coverage/groundedness, reproducible report) |
| 7 | Connector SDK | **IMPLEMENTED** (`connectors/base.py` Protocol + registry + fake-source coverage via REST/EKAF connectors) |
| 8 | Tombstone deletion | **IMPLEMENTED** (`POST /api/v1/admin/entities/{cid}/delete`, `?include_deleted=true`, ALREADY_DELETED idempotency) |
| 9 | Deterministic replay | **IMPLEMENTED** (`ingestion/replay.py` jira/gitlab/git + logical-diff golden comparison, `REPLAY` job, `scripts/replay.py`) |
| 10 | DLQ schema unification | **IMPLEMENTED** (`ingestion/dlq.py` envelope: stage/error_category/run_id/correlation_id/replay_ref; all 7 writers migrated) |
| 11 | Impact "why included" | **IMPLEMENTED** (per-item rationale, ranked by path length + evidence) |
| 12 | Search hardening | **IMPLEMENTED** (min-term + index-backed exact lookups) |
| 13 | Agent runtime/contract | **IMPLEMENTED** (AgentContract + catalog + budgets + explanation/XAI endpoints) |
| 14 | MCP completeness | **IMPLEMENTED** (15 tools, structured `McpError` mapping) |
| 15 | Audit coverage | **IMPLEMENTED** (worker audit through shared AuditSink, policy-denial typing, canary-secret redaction tests) |
| 16 | HugeGraph-native backup | **DEFERRED** — HugeGraph native backup tooling is not available in the pinned 1.7.0 image; the checksummed logical archive track is implemented, tested, and documented as the MVP-supported track |
| 17 | Domain links on all paths | **IMPLEMENTED** |
| 18 | Multi-commit git history | **IMPLEMENTED, LIMITED ACCEPTANCE** — bounded commit walk + parent/diff-hunk symbol links and repository tests exist; historical coordinates, deletion/rename/merge cases need broader certification |
| 19 | Canonical contracts at boundaries | **IMPLEMENTED** — all eight ingestion services consume normalized GraphMutation envelopes through the shared adapter, including temporal/domain/tombstone paths; guarded service/JSON-schema tests cover capture, run context and pre-write rejection |
| 20 | Security verification suite | **IMPLEMENTED** (prompt-injection/poisoned-fixture tests, canary redaction, read-only surface checks, policy-bound tests) |
| 21 | Benchmark dataset | **IMPLEMENTED** (deterministic scale s/m generator + bounded-traversal benchmark test; full-scale HugeGraph benchmarking deferred to capacity work) |
| 22 | Schema version discipline | **IMPLEMENTED STRUCTURAL GATE** — all schema kinds are preflighted before any mutation; incompatibilities fail explicitly, compatible additive changes remain supported. General version migration and cross-process schema locking are not provided. |
| 23 | Version stamping completeness | **IMPLEMENTED** (ontology/schema versions on all edges; missing-version soft rule) |

**Confluence page metadata batch (2026-10-03):**
- G2-SRC-CONF-001 labels, author/editor references and creation/modification
  timestamps now persist in page `payload_json` with source mapper version
  `confluence-dc/1.1`. UTC normalization retains fractional precision;
  source-only actor references do not create canonical Person identities.
- Complete-label pagination uses the trusted content endpoint, forwards
  correlation and refuses malformed/repeated/empty-next/over-limit collections.
  Mapping failures capture before DLQ; current clearing, prior revisions and
  late replay are tested. Capture/event time semantics are unchanged.
- Focused regression: **51 passed**; full host regression: **598 passed /
  12 opt-in skips**, exit 0. Changed-code Ruff/editor/Pylance and whitespace pass.
- Final rebuilt Docker API/worker/HugeGraph gate: **12 passed**, exit 0,
  no failures/errors/skips. Receipt:
  `test-results/eoip-dlq-acceptance-8f341c4e08814b9d914c39ac4ae0373c.json`
  with matching XML. Initial 11-pass/1-failure receipt remains FAIL; only the
  rejection request-count assertion was stale after added label pagination.
- Both disposable projects removed; primary readiness `ready`; no primary
  redeployment/reset. Protocol fixtures are not live tenants. Source revision
  retrieval, semantic linking, stale detection and attachment contents remain
  separate G2-P4 work; no phase/application 100% completion claim.

## G2 / KnowGridFlow phases

| Phase | Status | Evidence |
|---|---|---|
| G2-P0 contracts/revision | **IMPLEMENTED** | `SourceEventV2` (bitemporal fields), revision properties (`valid_from/to`, `is_current`), ADR-001, manifest integrity test |
| G2-P1 EKAF core | **IMPLEMENTED** | `connectors/registry.py` (Source Registry CRUD + endpoints), `base.py` SDK, `webhook.py`, `crawler.py`, `acquisition.py`, `reconciliation.py`, unified DLQ + replay console |
| G2-P2 sync/evolution | **IMPLEMENTED** | baseline/sync/reconcile/pause/resume endpoints, `graph/evolution.py`, `graph/as-of`, `graph/diff`, `graph/versions`, change journal endpoint, semantic events (`events/emitter.py`, `graph/consumers.py`) |
| G2-P3 sources wave 1 | **IMPLEMENTED** | `connectors/github.py`, `ingestion/github.py`, `jira_rest.py`, `gitlab_rest.py`, incremental code parsing |
| G2-P4 sources wave 2 | **IMPLEMENTED** | Confluence/ServiceNow (REST + temporal variants), `api_portal.py` (OpenAPI/GraphQL/AsyncAPI), Figma/qTest/Rally adapters |
| G2-P5 observability/runtime | **IMPLEMENTED** | `kibana.py`, `datadog.py`, `grafana.py` semantic-summary adapters (no raw telemetry in graph), SBOM/generic file adapters |
| G2-P6 twin domains | **PARTIAL** | test/decision/process/business-intent vocabulary partially in manifest; full intent-to-runtime chain demo pending pilot data |
| G2-P7 temporal/architecture | **PARTIAL** | Time Machine (`graph/as-of`, `graph/diff`) implemented; architecture-conformance DSL + process mining not yet built |
| G2-P8 knowledge health | **PARTIAL** | `graph/anomaly.py`, agents (proposals/firewall/evaluation) implemented; knowledge-debt catalog + SLO evaluator not yet built |
| G2-P9 simulation/causal | **PARTIAL** | `graph/whatif.py` entity-removal simulation; scenario-overlay engine + causal hypothesis engine not yet built |
| G2-P10 lenses/playback | **PARTIAL** | KGR explorer (8 graph types, 12 layouts, WebGL, events feed, diff, what-if, annotations); remaining planned lenses playback-only |

## KGR (Knowledge Graph Renderer & Explorer) — phases 1–8 IMPLEMENTED

Backend: metrics/centrality, paths (all-shortest + Yen), community (Leiden/Louvain/LabelPropagation), similarity + link prediction, anomaly, diff, what-if, k-core/components/degree-distribution, WebSocket + polling event feeds, schema/statistics/blast-radius/reverse-impact endpoints.
Frontend: KGRExplorer with 8 graph types, bundled Sigma.js renderer (CDN removed — NFR-KGR-005 satisfied), 10-dim filtering, bookmarks/history/annotations, export, timeline, diff/health panels, centrality radar, community hulls.
Remaining: Phase-2/4 cosmetic component extraction (FilterBar/NodeInspector inline), a11y audit, fisheye/edge-bundling polish.

## Honest completion boundary

The platform implements the MVP vertical slice plus substantial G2-P0..P5 and KGR code, with the earlier Docker evidence scoped above. Code presence is not end-to-end certification of every adapter or surface. G2-P6..P10 require further backend services and acceptance fixtures for architecture conformance, process mining, knowledge-health SLOs, counterfactual overlays, causal hypotheses and playback. Items 16/19 remain incomplete; item 18 has bounded implementation but broader historical acceptance remains open. Item 22 now enforces structural refusal before mutation, not a general schema migration framework.
