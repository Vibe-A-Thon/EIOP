# EOIP Development and Demo-Readiness Audit

**Audit date:** 2026-10-03  
**Repository revision inspected:** `f5a2402` (`dev_local`)  
**Scope:** current working tree, the engineering handoff in `EOIP-engg-doc-pkg/`, application source and tests, available validation results, and prior deployment/test evidence.

> **Executive conclusion:** EOIP has a substantial P1/MVP implementation and the current Docker test profile now passes: the Python suite completed all 418 tests, smoke checks passed including repeat-ingestion replay, and both included Playwright scenarios passed. The API readiness check and web page also returned successfully against the running stack. This is meaningful current demo evidence, but it does **not** establish 100% completion or full roadmap completion. The clean-reset golden-path/restore gate, broader P1 safety and quality evidence, and real VS Code extension-host acceptance remain open.

## Remediation update — 2026-10-03

**Priority gate 1 (captured-event replay and a green Python baseline) is complete on the current working tree.** The code replay path consumes the content stored in the immutable `SourceEvent` and does not reopen the source checkout. This was verified after deleting the originally ingested source file.

| Check | Result |
|---|---|
| Captured code replay regression | `tests/unit/test_replay.py::test_captured_code_event_replays_without_source_tree` passed. |
| Earlier complete Python suite | **357 passed** in 34.44 seconds; superseded by the current Docker test-profile run recorded under gate 3. |
| Ruff | `ruff check apps packages scripts tests` passed. |
| Patch whitespace | `git diff --check` passed (line-ending conversion warnings only). |

This closes order 1 in §5 and restores `MVP-FR-027`'s local automated Python-suite evidence.

### Priority gate 2 — Docker demo stack

**The Docker startup, schema, health, and persistence gate is complete.** Docker Desktop 4.93.0 / Engine 29.8.1 was available in the user-local installation discovered by `scripts/docker.ps1`, although its CLI directory was not on the shell's initial `PATH`.

| Check | Result |
|---|---|
| Compose validation and build | `deploy/docker-compose.yml` validated; application and web images built successfully. |
| Existing demo stack | HugeGraph, API, worker, MCP, and web reached healthy status; schema initialization exited successfully. |
| Public health checks | API readiness, MCP liveness, and web liveness returned HTTP 200. |
| Repeatable schema bootstrap | Initial bootstrap returned `created: True`; the immediate rerun returned `created: False, initialized: True`. |
| Existing-volume persistence | 115 vertices and 374 edges remained unchanged after a HugeGraph restart. |
| Isolated clean-stack verification | A separate Compose project with fresh volumes reached health on alternate ports; 23 vertices and 5 edges remained unchanged after restart. |
| Cleanup | Only the isolated verification project's containers, networks, and volumes were removed; the primary `eoip` stack remains healthy and running. |

### Priority gate 3 — repeat ingestion, smoke, and browser acceptance

**The current Docker test profile completed successfully** against the running local stack after correcting HugeGraph edge updates to omit the immutable `edge_key` sort key and aligning smoke-test expectations with the server's 15-tool MCP inventory.

| Check | Result |
|---|---|
| Full Python suite | **418 tests completed; progress reached 100% with no reported failures.** |
| Docker smoke | Passed readiness/authentication/limits, the Jira-to-code path, impact/evidence/validation, replay with stable logical entity counts, web, and real MCP search/path tools. |
| Playwright UI acceptance | **2 passed**: login/search/trace graph evidence/administer persisted data; invalid credentials show an error without access. |
| Live endpoint spot-check | API readiness returned `ready`; `http://localhost:8080/app` returned HTTP 200. |

This closes the current-running-stack and repeat-ingestion checks in orders 1–3 of §5 and provides current evidence for the directly exercised acceptance slices. It is not a clean-reset golden-path plus restore run, and the two browser scenarios do not cover every UI/admin/error-state requirement.

## 1. Summary

| Measure | Result | Interpretation |
|---|---:|---|
| Engineering Markdown files | 117 files / 14,058 physical lines | The handoff directory; all counted Markdown is under `EOIP-engg-doc-pkg/`. |
| All repository Markdown | 134 files / 15,298 physical lines | Includes the engineering handoff and 17 other project Markdown files. |
| Production source | 149 files / 20,280 nonblank LOC | Code-only sizing; comments count as LOC, blank lines do not. |
| Test source | 68 files / 7,108 nonblank LOC | Included separately from production source. |
| Total code source and tests | 217 files / 27,388 nonblank LOC | Production plus test source. |
| Normative functional requirements | 67 unique `FR-*` IDs | Requirement IDs are deduplicated; repeated mentions elsewhere are not additional features. |
| Normative non-functional requirements | 14 unique `NFR-*` IDs | The handoff uses qualified IDs such as `NFR-SEC-001`, not a separate `NFR-001` numbering scheme. |
| MVP acceptance requirements | 28 `MVP-FR-*` entries | P1/MVP acceptance scope. |
| Implementation work-package tasks | **82 distinct `WP-*` IDs** | The earlier approximate figure of 94 is not supported by the task-ID inventory; see §4. |
| MVP requirement evidence score | **79.5% estimated implementation-evidence score** | Updated status-weighted estimate, not a claim that 79.5% of end-to-end acceptance is passing. |
| MVP acceptance evidence | **17/28 (60.7%) verified; 10 partial; 1 unverified** | Evidence reflects the current green test profile and exercised browser/runtime slices; remaining partial criteria and the VS Code extension remain open. |
| Current Python test suite | **418 tests completed, progress reached 100%, no reported failures** | Captured in the successful Docker test-profile run; the profile also passed smoke and browser acceptance. |
| Current frontend production build | Pass | `npm --prefix apps/web run build`. |
| Current Ruff lint | Pass | `ruff check apps packages scripts tests`. |
| Docker | Available and running | Current Docker test profile passed; API readiness and the served web application were spot-checked. Clean-reset golden-path/restore acceptance remains open. |
| Node.js | Available: `v26.8.2` | Two current Playwright acceptance scenarios passed; full UI/admin/error-state coverage remains open. |
| Worktree | 30 changed entries | 24 modified and 6 untracked; this report does not alter or discard them. |

### How to read the estimates

The specifications mix implementation requirements, user-facing acceptance criteria, quality controls, and explicitly deferred roadmap scope. They also repeat related needs in several documents. Therefore:

* `verified` means there is direct code and test or runtime evidence for the stated slice. It does **not** imply the whole application or the clean-stack demo has passed.
* `partial` means some of the requirement is implemented, but acceptance evidence or stated sub-capabilities remain incomplete.
* `unverified` means code/configuration or historical evidence exists, but the current checkout could not be independently verified.
* `missing` means the required evidence/capability is not demonstrated and no sufficient implementation evidence was identified.
* `deferred` means the requirement belongs to a later phase, not a P1/MVP defect.
* The illustrative weighted implementation score uses `verified = 1`, `partial = 0.5`, `unverified = 0.25`, and `missing/deferred = 0`. For P1 rollups, deferred later-phase work is excluded. This makes uncertainty visible but is not a substitute for acceptance tests.
* Completion percentages are estimates at the stated scope. Where a normative `FR-*` ID is linked to an MVP criterion, its status is the closest matching acceptance slice; it is not an independent additional denominator.

## 2. Repository inventory and counting method

### 2.1 Included workspace file categories

The broad working-tree inventory contains **774 files** in these mutually exclusive categories:

| Category | Files | Definition |
|---|---:|---|
| Production source code | 149 | Application/library code, excluding test code. |
| Test code | 68 | Unit, integration, security, and end-to-end test source. |
| Markdown documentation | 134 | All repository `.md` files, including engineering handoff documents. |
| Configuration and manifests | 97 | Build, package, environment, deployment, and tool configuration files. |
| Scripts | 5 | Standalone project scripts not counted as application/test source. |
| Data | 6 | Checked-in structured fixture/data files. |
| Assets | 4 | Non-source static assets. |
| Logs, caches, and backups | 247 | Existing working-tree artifacts, retained in this inventory but not treated as source or product functionality. |
| Other | 64 | Files not matched by the categories above. |
| **Total** | **774** | Excludes `.git` and dependency/build/cache directories excluded by the inventory rules. |

These are *working-tree* counts, not a clean Git-tracked-file count. In particular, logs/caches/backups and untracked files are present; do not treat them as product code or as evidence of completed features.

### 2.2 Code LOC

| Code scope | Files | Nonblank LOC |
|---|---:|---:|
| Production code | 149 | 20,280 |
| Test code | 68 | 7,108 |
| **Total** | **217** | **27,388** |

LOC counts nonblank source lines, including comments. It excludes blank lines, `.git`, dependency/build/cache directories, and generated/minified files. It is a sizing metric, not a measure of completion or quality.

### 2.3 Markdown counts

| Markdown scope | Files | Physical lines |
|---|---:|---:|
| `EOIP-engg-doc-pkg/` total | 117 | 14,058 |
| ├─ package root | 87 | 12,854 |
| ├─ `diagrams/` | 17 | 250 |
| ├─ `examples/` | 1 | 2 |
| └─ `implementation/` | 12 | 952 |
| Other project Markdown | 17 | 1,240 |
| **Repository Markdown total** | **134** | **15,298** |

The engineering package contains approximately 2,143 Markdown headings. The source package and its phase/implementation plans are the normative source for scope; generated audit notes and historical validation reports are supporting evidence, not a replacement for requirements.

## 3. Current validation and readiness evidence

| Check | Current evidence | Status |
|---|---|---|
| Python full test suite | Docker test-profile output reached 100%; 418 test progress markers, no reported failures. | **PASS** |
| Ruff | `ruff check apps packages scripts tests` completed successfully. | **PASS** |
| Frontend production build | `npm --prefix apps/web run build` completed successfully. | **PASS** |
| Patch whitespace check | `git diff --check` exit code 0. | **PASS** |
| Docker local stack | Current test profile passed smoke, repeat-demo replay, and browser tests; API readiness and web HTTP 200 were checked on the running stack. | **PASS — CURRENT PROFILE** |
| Browser acceptance | Two Playwright scenarios passed, covering login/search/trace graph/administered persisted data and rejection of invalid credentials. | **PASS — 2 SCENARIOS; BROADER COVERAGE OPEN** |
| VS Code extension host behavior | Packaged VSIX and historical packaging evidence exist; current extension commands were not demonstrated in a real VS Code host during this audit. | **UNVERIFIED** |
| Historical Docker verification | `docs/deployment-verification.md` records earlier startup/persistence and other checks. Older docs cite differing test totals. | **HISTORICAL ONLY** |

The test profile resolves the previously failing captured-event replay case and exercises persistent repeat ingestion. The Python progress output is recorded as 418 completed tests; the run output did not print a separate pytest count summary. Do not use older 123-, 137-, 355-, or 357-test totals as the current result.

## 4. Requirement and feature completion

### 4.1 P1/MVP acceptance criteria: all 28

The implementation/status estimates below are based on source/test evidence reviewed for this audit. “Verified” indicates direct implementation/test evidence for the requirement slice; it is deliberately narrower than “full-stack demo verified.”

| ID | Requirement | Status | Evidence and remaining proof |
|---|---|---|---|
| MVP-FR-001 | Apache HugeGraph local Docker | **Verified — 100% evidence score** | Current Compose stack ran the Docker smoke/profile successfully; prior isolated clean-stack and persistence checks are recorded above. |
| MVP-FR-002 | Automatic graph schema initialization | **Verified — 100%** | Current stack/schema checks and repeatable bootstrap evidence are recorded above; broader clean-reset golden-path acceptance remains open. |
| MVP-FR-003 | Jira JSON ingestion | **Verified — 100%** | Jira ingestion implementation and unit/demo flow tests. |
| MVP-FR-004 | Git repository/GitLab ingestion | **Partial — 50%** | Git/GitLab adapters and tests exist; multi-commit/deletion synchronization remains documented work. |
| MVP-FR-005 | Deterministic Python/TypeScript code parsing | **Verified — 100%** | Parser/ingestion implementations and tests assert symbols and source structure. |
| MVP-FR-006 | Canonical entity generation and idempotency | **Partial — 50%** | Stable IDs and repeat-ingestion/replay assertions pass in the current profile; broader identity migration and cross-source idempotency cases remain. |
| MVP-FR-007 | Queryable Jira graph with provenance | **Verified — 100%** | Jira and demo-flow tests exercise the work-item graph. |
| MVP-FR-008 | Queryable code graph and source locations | **Verified — 100%** | Code ingestion/parser and demo-flow assertions. |
| MVP-FR-009 | Queryable meta graph | **Partial — 50%** | Meta/run/admin APIs exist; quality evidence notes orphan `AgentRun` findings. |
| MVP-FR-010 | Forward/reverse cross-graph linking with evidence | **Verified — 100%** | Current Docker smoke and demo-flow assertions exercise the Jira→MR→commit→file→symbol path with evidence. |
| MVP-FR-011 | Provenance lineage | **Verified — 100%** | Provenance package, API/demo tests, and lineage assertions exist. |
| MVP-FR-012 | Graph validation and invalid-data handling | **Partial — 50%** | Validation engine/gate exist; seeded-invalid-graph coverage is recorded as remaining work. |
| MVP-FR-013 | Safe, real-data query API | **Verified — 100%** | API/query modules, API tests, and bounds/security tests. |
| MVP-FR-014 | Bounded impact analysis | **Verified — 100%** | Executor and demo-flow impact assertions. |
| MVP-FR-015 | Bounded path query | **Verified — 100%** | Traversal and demo/unit tests assert path results. |
| MVP-FR-016 | Real-API search/query UI and error state | **Partial — 50%** | Current browser acceptance exercised login and search; broader query/error-state and API-unavailable behavior coverage remains open. |
| MVP-FR-017 | Graph visualizer | **Partial — 50%** | Trace graph evidence is covered by the current browser test; the full graph/path interaction acceptance matrix remains open. |
| MVP-FR-018 | Admin ingestion and validation UI | **Partial — 50%** | Current browser acceptance administers persisted data; validation/ontology/DLQ workflows still need broader end-to-end coverage. |
| MVP-FR-019 | VS Code context extension | **Unverified — 25%** | VSIX/package artifact exists; current real-host symbol/context journey was not rerun. |
| MVP-FR-020 | Local graph-grounded RAG | **Verified — 100%** | Retrieval and evaluation test suites exist; historical model-unavailable fallback evidence is not a current end-to-end run. |
| MVP-FR-021 | Bounded read-only agent workflow | **Verified — 100%** | Agent runtime/deep-agent and demo-flow tests. |
| MVP-FR-022 | Read-only MCP graph access | **Verified — 100%** | MCP server/tool implementations and transport/tool tests. |
| MVP-FR-023 | Structured, correlation-aware logging | **Partial — 50%** | Logging/audit code and tests exist; broader audit coverage/fail-closed behavior remains open. |
| MVP-FR-024 | Local machine-readable metrics | **Verified — 100%** | Observability/deployment API tests; earlier Prometheus scrape is historical evidence. |
| MVP-FR-025 | Checksummed backup artifact | **Partial — 50%** | Logical backup implementation/evidence exists; native HugeGraph backup and configuration archival remain open. |
| MVP-FR-026 | Isolated restore with golden-query verification | **Verified — 100%** | Restore/demo tests and historical isolated restore evidence; current Docker restore was not rerun. |
| MVP-FR-027 | Local automated test/report suites | **Verified — 100%** | The current Docker test profile completed the Python suite and both Playwright scenarios successfully; Ruff and frontend build also pass. |
| MVP-FR-028 | Clean-reset end-to-end demo | **Partial — 50%** | Current Docker smoke verifies the golden path and repeat replay on the running stack; a clean-reset plus restore demonstration remains unverified. |

**Score:** 17 verified, 10 partial, 1 unverified. Applying the explicitly illustrative weights above yields **79.5% implementation-evidence score**. Directly verified criteria are **17/28 = 60.7%**. These estimates do not imply that every P1 acceptance criterion or the clean-reset demo is complete.

### 4.2 Normative functional requirements: all 67 unique `FR-*`

The FR register below records each distinct requirement ID and its P1 evidence estimate. The five later-phase requirements are intentionally deferred and are excluded from the P1 score. The status follows the closest MVP acceptance slice and is not an independent duplicate score.

| Requirement ID | Scope | Target | Status |
|---|---|---|---|
| FR-CONN-001 | Connector SDK / source event contract | P1 | Partial |
| FR-CONN-002 | Jira JSON connector | P1 | Verified |
| FR-CONN-003 | Local Git repository connector | P1 | Partial |
| FR-CONN-004 | GitLab metadata adapter | P1 | Partial |
| FR-CONN-005 | Connector retries, pagination, checkpoint/resume | P1 | Partial |
| FR-CONN-006 | Dry-run and deterministic replay | P1 | Partial |
| FR-CONN-007 | Tombstones/source deletion semantics | P1 | Partial |
| FR-CONF-001 | Confluence pages/spaces/attachment metadata | P2 | Deferred |
| FR-SNOW-001 | ServiceNow records/table API | P2 | Deferred |
| FR-INGEST-001 | Immutable raw SourceEvent capture | P1 | Verified |
| FR-INGEST-002 | Deterministic canonicalization | P1 | Partial |
| FR-INGEST-003 | Idempotent graph mutation | P1 | Partial |
| FR-INGEST-004 | Ingestion job lifecycle/status | P1 | Partial |
| FR-INGEST-005 | Dead-letter storage and replay controls | P1 | Partial |
| FR-GRAPH-001 | HugeGraph authoritative operational store | P1 | Verified |
| FR-GRAPH-002 | Logical graph domains | P1 | Partial |
| FR-GRAPH-003 | Idempotent schema bootstrap | P1 | Verified |
| FR-GRAPH-004 | Stable canonical identifiers | P1 | Partial |
| FR-GRAPH-005 | Graph-backed meta graph | P1 | Partial |
| FR-GRAPH-006 | Cross-domain bridge path | P1 | Verified |
| FR-GRAPH-007 | Reviewed/versioned Gremlin repository | P1 | Verified |
| FR-GRAPH-008 | Measured graph index strategy | P1 | Partial |
| FR-GRAPH-009 | Graph version journal/temporal metadata | P1 | Partial |
| FR-GRAPH-010 | Bounded RDF/OWL/JSON-LD interoperability | P2 | Deferred |
| FR-ONTO-001 | Versioned enterprise ontology vocabulary | P1 | Partial |
| FR-ONTO-002 | Typed relationship/domain/range semantics | P1 | Partial |
| FR-PROV-001 | Evidence metadata model | P1 | Verified |
| FR-PROV-002 | Reverse provenance traversal | P1 | Verified |
| FR-ID-001 | Deterministic identity resolution | P1 | Partial |
| FR-ID-002 | Ambiguous identity candidates/review | P1 | Partial |
| FR-TEMP-001 | Bitemporal-ready source/entity fields | P1 | Partial |
| FR-CODE-001 | Deterministic AST code parser | P1 | Verified |
| FR-CODE-002 | Python and TypeScript/JavaScript parsing | P1 | Verified |
| FR-CODE-003 | Commit-to-symbol/diff-range linking | P1 | Partial |
| FR-CODE-004 | Typed call/import/dependency edges | P1 | Verified |
| FR-CODE-005 | Source navigation with exact locations | P1 | Verified |
| FR-QUERY-001 | Validated structured QueryPlan | P1 | Verified |
| FR-QUERY-002 | Bounded path query | P1 | Verified |
| FR-QUERY-003 | Bounded impact analysis | P1 | Verified |
| FR-QUERY-004 | Controlled canonical entity search | P1 | Verified |
| FR-QUERY-005 | Natural-language query interpretation | P1 | Partial |
| FR-QUERY-006 | Query safety bounds/allowlists/read-only controls | P1 | Verified |
| FR-QUERY-007 | Query result evidence envelope | P1 | Verified |
| FR-QUERY-008 | Restricted reviewed/admin raw Gremlin boundary | P1 | Verified |
| FR-VALID-001 | Ontology/schema/evidence/identity validation rules | P1 | Partial |
| FR-VALID-002 | Mutation validation gates/quarantine | P1 | Partial |
| FR-VALID-003 | Graph quality findings/metrics | P1 | Partial |
| FR-RAG-001 | Retrieval strategy router | P1 | Verified |
| FR-RAG-002 | Graph-grounded evidence retrieval | P1 | Verified |
| FR-RAG-003 | Optional local model abstraction | P1 | Partial |
| FR-RAG-004 | No mandatory vector DB for MVP | P1 | Verified |
| FR-RAG-005 | Retrieval/answer evaluation harness | P1 | Verified |
| FR-RAG-006 | Adaptive/CRAG/Self-RAG strategy plugins | P3 | Deferred |
| FR-AGENT-001 | Versioned agent/tool contract | P1 | Verified |
| FR-AGENT-002 | Bounded agent runtime and tool allowlist | P1 | Verified |
| FR-AGENT-003 | Read-only TraceImpact agent | P1 | Verified |
| FR-AGENT-004 | Separate governed write/action boundary | P1 | Verified |
| FR-AGENT-005 | Controlled sandboxed self-modification | P8+ | Deferred |
| FR-MEM-001 | Scoped, bounded, auditable agent memory | P1 | Partial |
| FR-MCP-001 | Read-only MCP entity/path/impact/evidence tools | P1 | Verified |
| FR-MCP-002 | Separate/absent MVP write actions | P1 | Verified |
| FR-UI-001 | Real-API user web application | P1 | Partial |
| FR-UI-002 | Bounded graph explorer/path/provenance UI | P1 | Partial |
| FR-ADMIN-001 | Ingestion-run administration UI | P1 | Partial |
| FR-ADMIN-002 | Graph-quality/validation administration UI | P1 | Partial |
| FR-VSCODE-001 | Context for current VS Code symbol | P1 | Unverified |
| FR-VSCODE-002 | In-editor trace/impact commands | P1 | Unverified |

**P1 functional rollup:** 62 requirements: 29 verified, 29 partial, 4 unverified. Weighted estimate: `(29 + 29×0.5 + 4×0.25) / 62 = 71.8%`. Five later-phase requirements are deferred. The crosswalk sources are the MVP matrix (§4.1), implementation work packages (§4.4), and evidence files linked in §8.

### 4.3 Non-functional requirements: all 14

The documentation IDs are qualified; the requested shorthand `NFR-001..014` below is merely a row number, not the canonical identifier.

| # | Canonical ID | Requirement | Status | Evidence / gap |
|---:|---|---|---|---|
| 1 | NFR-SEC-001 | No outbound enterprise-data egress | **Unverified — 25%** | Compose network controls exist; deny-egress test remains documented and was not exercised by the current profile. |
| 2 | NFR-SEC-002 | Secret isolation | **Partial — 50%** | Security tests and historical generated-secret checks exist; current full secret/egress evidence incomplete. |
| 3 | NFR-SEC-003 | Input/file safety | **Verified — 100%** | Path traversal, oversized input, and malformed-input security tests. |
| 4 | NFR-SEC-004 | Prompt/tool-injection defenses | **Verified — 100%** | Prompt-injection-as-data and read-only-tool tests. |
| 5 | NFR-SEC-005 | Authentication (without mandatory MVP RBAC) | **Verified — 100%** | API/MCP auth tests and token configuration. |
| 6 | NFR-SEC-006 | Container hardening/internal-only service exposure | **Unverified — 25%** | Compose controls exist; current container runtime inspection unavailable. |
| 7 | NFR-SEC-007 | Security/audit event coverage | **Partial — 50%** | Audit implementation/tests exist; coverage and fail-closed behavior remain open. |
| 8 | NFR-REL-001 | Restart-safe processing | **Verified — 100%** | Worker/state code and current repeat-ingestion replay smoke pass; clean-reset/restore verification remains open. |
| 9 | NFR-REL-002 | Backup/restore with verification | **Partial — 50%** | Backup/restore tests and historical run exist; native graph backup/config archival remains open. |
| 10 | NFR-OPS-001 | Structured logs, health, correlation IDs | **Verified — 100%** | Health/observability and deployment API tests; historical services reported healthy. |
| 11 | NFR-OPS-002 | Local machine-readable metrics | **Verified — 100%** | Metrics and deployment API tests; historical Prometheus scrape. |
| 12 | NFR-PERF-001 | Measured, benchmark-defined objectives | **Partial** | Versioned manifest, deterministic smoke/full datasets, automated tests, hardware/resource metadata, and published memory p50/p95/p99 evidence now exist. Full HugeGraph + HTTP measurement remains open. |
| 13 | NFR-MAINT-001 | Modular-monolith boundaries/stable contracts | **Partial — 50%** | Package/service boundaries, lint, and current test-profile evidence exist; contract and architecture fitness evidence remains incomplete. |
| 14 | NFR-PRIV-001 | Data minimization/classification | **Partial — 50%** | Redaction/safe-summary tests exist; complete field classification/prohibited-content coverage is unverified. |

**NFR rollup:** 6 verified, 5 partial, 2 unverified, 1 missing. Weighted estimate: **64.3%**; directly verified: **6/14 = 42.9%**.

### 4.4 Implementation task register: 82 distinct `WP-*`

The handoff’s 12 implementation work-package files contain **82 unique task IDs**, not 94. The earlier “~94” likely counted 12 work-package headings in addition to task IDs or included repeated references. The task counts below are the direct sum of each task file. Statuses are estimates from the closest functional/NFR evidence; a task marked verified still does not establish clean-stack demo readiness.

Status shorthand: **V** verified; **P** partial; **U** unverified; **M** missing; **D** deferred to later phase.

| Work package | Task ID | Scope | Status |
|---|---|---|:---:|
| Foundation | WP-FOUNDATION-01 | HugeGraph authoritative store | V |
| Foundation | WP-FOUNDATION-02 | Logical graph domains | P |
| Foundation | WP-FOUNDATION-03 | Schema bootstrap | V |
| Foundation | WP-FOUNDATION-04 | Canonical identifiers | P |
| Foundation | WP-FOUNDATION-05 | Modular-monolith boundary | P |
| Connectors | WP-CONNECTORS-01 | Connector SDK | P |
| Connectors | WP-CONNECTORS-02 | Jira JSON connector | V |
| Connectors | WP-CONNECTORS-03 | Git repository connector | P |
| Connectors | WP-CONNECTORS-04 | GitLab metadata adapter | P |
| Connectors | WP-CONNECTORS-05 | Connector resiliency | P |
| Connectors | WP-CONNECTORS-06 | Dry run and replay | P |
| Connectors | WP-CONNECTORS-07 | Source deletion semantics | P |
| Connectors | WP-CONNECTORS-08 | Confluence connector | D |
| Connectors | WP-CONNECTORS-09 | ServiceNow connector | D |
| Ingestion | WP-INGESTION-01 | Immutable raw capture | V |
| Ingestion | WP-INGESTION-02 | Canonicalization | P |
| Ingestion | WP-INGESTION-03 | Idempotent mutation | P |
| Ingestion | WP-INGESTION-04 | Ingestion job lifecycle | P |
| Ingestion | WP-INGESTION-05 | Dead-letter processing | P |
| Ontology/graph | WP-ONTOLOGY-GRAPH-01 | Meta graph | P |
| Ontology/graph | WP-ONTOLOGY-GRAPH-02 | Cross-domain bridge edges | V |
| Ontology/graph | WP-ONTOLOGY-GRAPH-03 | Index strategy | P |
| Ontology/graph | WP-ONTOLOGY-GRAPH-04 | Graph version journal | P |
| Ontology/graph | WP-ONTOLOGY-GRAPH-05 | RDF/OWL interoperability | D |
| Ontology/graph | WP-ONTOLOGY-GRAPH-06 | Enterprise ontology vocabulary | P |
| Ontology/graph | WP-ONTOLOGY-GRAPH-07 | Relationship semantics | P |
| Ontology/graph | WP-ONTOLOGY-GRAPH-08 | Evidence model | V |
| Ontology/graph | WP-ONTOLOGY-GRAPH-09 | Provenance traversal | V |
| Ontology/graph | WP-ONTOLOGY-GRAPH-10 | Deterministic identity resolution | P |
| Ontology/graph | WP-ONTOLOGY-GRAPH-11 | Ambiguous identity candidates | P |
| Ontology/graph | WP-ONTOLOGY-GRAPH-12 | Bitemporal-ready fields | P |
| Code graph | WP-CODEGRAPH-01 | Deterministic code parser | V |
| Code graph | WP-CODEGRAPH-02 | Python and TypeScript MVP parsing | V |
| Code graph | WP-CODEGRAPH-03 | Commit-to-symbol linking | P |
| Code graph | WP-CODEGRAPH-04 | Call/import/dependency edges | V |
| Code graph | WP-CODEGRAPH-05 | Source navigation | V |
| Query | WP-QUERY-01 | Structured QueryPlan | V |
| Query | WP-QUERY-02 | Bounded path query | V |
| Query | WP-QUERY-03 | Impact analysis | V |
| Query | WP-QUERY-04 | Entity search | V |
| Query | WP-QUERY-05 | Natural-language interpretation | P |
| Query | WP-QUERY-06 | Query safety policy | V |
| Query | WP-QUERY-07 | Query evidence envelope | V |
| Query | WP-QUERY-08 | Raw Gremlin admin boundary | V |
| Query | WP-QUERY-09 | Reviewed Gremlin repository | V |
| Validation | WP-VALIDATION-01 | Graph validation rules | P |
| Validation | WP-VALIDATION-02 | Validation gates | P |
| Validation | WP-VALIDATION-03 | Graph quality metrics | P |
| RAG | WP-RAG-01 | Retrieval router | V |
| RAG | WP-RAG-02 | GraphRAG evidence retrieval | V |
| RAG | WP-RAG-03 | Local model abstraction | P |
| RAG | WP-RAG-04 | No mandatory vector DB in MVP | V |
| RAG | WP-RAG-05 | RAG evaluation harness | V |
| RAG | WP-RAG-06 | Adaptive RAG strategy framework | D |
| Agent/memory | WP-AGENT-MEMORY-01 | Agent contract | V |
| Agent/memory | WP-AGENT-MEMORY-02 | Bounded agent runtime | V |
| Agent/memory | WP-AGENT-MEMORY-03 | TraceImpact agent | V |
| Agent/memory | WP-AGENT-MEMORY-04 | Write/action approval boundary | V |
| Agent/memory | WP-AGENT-MEMORY-05 | Controlled self-modification | D |
| Agent/memory | WP-AGENT-MEMORY-06 | Scoped memory records | U |
| MCP | WP-MCP-01 | MCP read server | V |
| MCP | WP-MCP-02 | MCP action separation | V |
| Experience | WP-EXPERIENCE-01 | User web application | P |
| Experience | WP-EXPERIENCE-02 | Graph explorer | P |
| Experience | WP-EXPERIENCE-03 | Admin ingestion UI | P |
| Experience | WP-EXPERIENCE-04 | Admin graph-quality UI | P |
| Experience | WP-EXPERIENCE-05 | VS Code context extension | U |
| Experience | WP-EXPERIENCE-06 | VS Code trace/impact commands | U |
| Security/ops | WP-SECURITY-OPS-01 | No outbound enterprise-data egress | U |
| Security/ops | WP-SECURITY-OPS-02 | Secret isolation | P |
| Security/ops | WP-SECURITY-OPS-03 | Input/file safety | V |
| Security/ops | WP-SECURITY-OPS-04 | Prompt/tool injection defenses | V |
| Security/ops | WP-SECURITY-OPS-05 | Authentication without MVP RBAC | V |
| Security/ops | WP-SECURITY-OPS-06 | Container hardening | U |
| Security/ops | WP-SECURITY-OPS-07 | Audit events | P |
| Security/ops | WP-SECURITY-OPS-08 | Restart-safe processing | V |
| Security/ops | WP-SECURITY-OPS-09 | Backup and restore | P |
| Security/ops | WP-SECURITY-OPS-10 | Structured logging and health | V |
| Security/ops | WP-SECURITY-OPS-11 | Local metrics | V |
| Security/ops | WP-SECURITY-OPS-12 | Benchmark-defined objectives | M |
| Security/ops | WP-SECURITY-OPS-13 | Modular-monolith boundary | P |
| Security/ops | WP-SECURITY-OPS-14 | Data minimization/classification | P |

**WP rollup:** 82 tasks = 77 P1 tasks + 5 explicitly later-phase tasks. Of the 77 P1 tasks, the evidence-based estimate is 35 V, 36 P, 5 U, and 1 M. Applying the stated weights gives **70.5% estimated P1 task implementation-evidence score**; directly verified is **35/77 = 45.5%**. The 5 later-phase tasks are deferred, not MVP failures.

## 5. Prioritized completion sequence

Order work so the product remains demonstrable at each checkpoint. Do not spend MVP time implementing later-phase capabilities before the vertical slice, startup, and acceptance gates are reliable.

| Order | Gate / work | Exit evidence required | Why this comes next |
|---:|---|---|---|
| 0 | Preserve and baseline the current worktree | Record current diff; keep all 30 existing changed entries intact; establish a test/build baseline on this checkout. | Avoid overwriting the user’s in-progress code and make subsequent fixes attributable. |
| 1 | Fix replay and establish a green automated baseline | Captured-event replay regression, full Python test-profile run, and Docker replay smoke pass; current profile completed with exit code 0. | **Complete on the current working tree.** |
| 2 | Verify the current Docker demo stack | Current stack smoke/profile passed, including health/auth/schema-dependent use and replay; API readiness and web returned successfully. Clean-reset plus restore remains a separate open gate. | **Current-stack gate complete; clean-reset acceptance remains open under order 5/7.** |
| 3 | Confirm supported UI/API wiring | API readiness and web HTTP 200 spot-check passed; browser login succeeds. Still prove API shutdown produces an explicit error without fallback data. | Basic live wiring is evidenced; unavailable-API/error-state acceptance remains. |
| 4 | Expand primary browser journey coverage | Two current Playwright scenarios pass for login/search/trace graph/administered persisted data and invalid credentials. Extend coverage to query/path details, validation/ontology, DLQ, and service-unavailable behavior. | **Partially evidenced; broader acceptance matrix remains open.** |
| 5 | Lock the core graph vertical slice from a clean reset | From a clean reset, ingest Jira + local Git/GitLab fixtures + code; assert canonical idempotency, the golden cross-graph path, provenance, and impact analysis. | Docker smoke and replay pass on the current stack; clean-reset cross-source acceptance still needed. |
| 6 | Close P1 safety/quality gaps | Add seeded invalid graph cases, egress/secret checks, audit fail-closed/coverage tests, temporal/identity acceptance cases, and measure index behavior. | Convert partial controls into explicit acceptance, particularly security and integrity guarantees. |
| 7 | Finish demo operations | Generate checksum backup; restore to a clean graph; compare expected counts/golden queries; validate logs/metrics; add a single documented reset/demo command. | Makes the demo repeatable, recoverable, and observable. |
| 8 | Verify VS Code extension in a real host | Install the built extension into a test VS Code profile; exercise current-symbol context and trace/impact commands against the same demo graph; capture output/evidence. | The extension is a named MVP feature but presently has package evidence rather than current host acceptance. |
| 9 | Freeze demo release baseline | Full Python suite, Ruff, frontend build, broader Playwright, extension-host checks, clean-reset/restore Docker run, and runbook all pass on one recorded revision. | Only this gate supports “demo-ready” for this revision. |
| 10 | Continue roadmap after MVP sign-off | Prioritize P2 connectors/ontology export, then P3 adaptive RAG, later agent/temporal/automation/hardening phases according to the phase plan. | Prevents roadmap scope from obscuring MVP exit criteria. |

## 6. Phase-level assessment

| Scope | Assessment |
|---|---|
| P0 foundation | Implemented substantially; current Docker profile, schema-dependent runtime, and replay checks pass. Clean-reset plus backup/restore acceptance remains open. |
| P1 integrated MVP | Substantial breadth exists; current evidence estimates are about 70–80% by weighted requirement crosswalks, with 60.7% of explicit MVP criteria classified verified. Broader UI, safety/quality, restore, and extension-host gates prevent a full demo-ready sign-off. |
| P2 connectors/ontology depth | Confluence, ServiceNow, and RDF/OWL export are explicitly later-phase; do not count as P1 MVP defects. |
| P3 advanced retrieval | Adaptive RAG strategy framework deferred. |
| P4–P7 advanced agent/temporal/human-control/enterprise hardening | Roadmap scope; assess when those phase plans are activated. |
| P8+ controlled self-improvement | Explicitly later-phase; not required for the read-only MVP. |
| Whole roadmap | Not 100% complete. The phase catalog intentionally includes unfinished future work; no “whole application 100%” claim is supported. |

## 7. Scope, ambiguities, and audit limitations

1. The normative FR catalog and MVP acceptance catalog overlap by design. Their counts must not be summed as distinct delivered features.
2. Some documents describe broad “linked documentation” outcomes while Confluence is explicitly P2; the MVP demo must use an agreed fixture/source for documentation context or the acceptance wording should be clarified.
3. The work-package estimate is a scope-to-evidence crosswalk. The plan files do not store per-task numeric completion percentages; the scores are explicitly audit estimates, not project-management state.
4. Current successful profile evidence supersedes the earlier replay, smoke-inventory, browser, and Docker-unavailable observations; the prior failures remain relevant history but are not the current status.
5. Two browser scenarios now pass, but do not cover the complete acceptance matrix. In particular, API-unavailable behavior, validation/ontology workflows, and DLQ details still need explicit acceptance.
6. Docker is available and the current profile passes on the running stack. A fresh clean-reset demo plus restore/backup verification remains a separate release gate.
7. This is a point-in-time review of revision `f5a2402` plus its existing dirty worktree and the current validation run. Any subsequent code changes require a new test and readiness pass.

## 8. Evidence and source references

### Normative engineering package

* [`EOIP-engg-doc-pkg/03-functional-requirements.md`](../EOIP-engg-doc-pkg/03-functional-requirements.md) — 67 unique functional requirement definitions and target phases.
* [`EOIP-engg-doc-pkg/04-non-functional-requirements.md`](../EOIP-engg-doc-pkg/04-non-functional-requirements.md) — 14 qualified NFRs.
* [`EOIP-engg-doc-pkg/MVP-requirements.md`](../EOIP-engg-doc-pkg/MVP-requirements.md) — 28 MVP acceptance requirements.
* [`EOIP-engg-doc-pkg/67-implementation-plan.md`](../EOIP-engg-doc-pkg/67-implementation-plan.md) — phase sequencing and work-package index.
* [`EOIP-engg-doc-pkg/implementation/`](../EOIP-engg-doc-pkg/implementation/) — 12 implementation work-package files containing 82 distinct task IDs.
* Other cross-cutting inputs reviewed include phase roadmap, architecture/system design, traceability, validation strategy, deployment/demo and security documents within the 117-file package.

### Current implementation and validation references

* [`pyproject.toml`](../pyproject.toml) — pytest/Ruff configuration.
* [`README.md`](../README.md) and [`deploy/docker-compose.yml`](../deploy/docker-compose.yml) — local startup/deployment instructions and service topology.
* [`apps/web/package.json`](../apps/web/package.json) — frontend build command; no package-level test script is defined.
* [`apps/web/src/App.jsx`](../apps/web/src/App.jsx) — user/admin UI, graph schema and DLQ views.
* [`apps/web/tests/application.spec.js`](../apps/web/tests/application.spec.js) — browser acceptance scenarios.
* [`packages/eoip/graph/hugegraph.py`](../packages/eoip/graph/hugegraph.py), [`tests/unit/test_edge_dedup.py`](../tests/unit/test_edge_dedup.py), and [`scripts/smoke_test.py`](../scripts/smoke_test.py) — immutable HugeGraph edge sort-key regression and current smoke MCP inventory.
* [`tests/unit/test_replay.py`](../tests/unit/test_replay.py) and [`packages/eoip/ingestion/replay.py`](../packages/eoip/ingestion/replay.py) — captured-event replay regression and implementation.
* [`docs/gap-audit-2026-10-02.md`](gap-audit-2026-10-02.md) — explicitly recorded open gaps.
* [`docs/application-audit-2026-10-02.md`](application-audit-2026-10-02.md) — earlier application audit; historical context only.
* [`docs/deployment-verification.md`](deployment-verification.md) — supplemental Docker/deployment evidence; the current test-profile result is recorded in this audit’s remediation update.
* [`docs/docker-local.md`](docker-local.md) — Docker-local limitations and connector synchronization notes.

### Current commands/results referenced

* Docker test profile — exit code 0; Python test progress reached 100% (418 progress dots); smoke and both Playwright scenarios passed.
* `ruff check apps packages scripts tests` — pass.
* `npm --prefix apps/web run build` — pass.
* `git diff --check` — pass.
* Docker runtime spot-check — API `/health/ready` reported `ready`; web `/app` returned HTTP 200.
* `node --version` — `v26.8.2`.
* Git — revision `f5a2402`, branch `dev_local`, worktree `30` changed entries.

## 9. Sign-off

**Current sign-off: NOT DEMO-READY / NOT 100% COMPLETE.**  
The previous replay, Docker-availability, and basic browser blockers are resolved for the current working tree. The shortest remaining path is to run and record a clean-reset cross-source golden path plus verified backup/restore; close the remaining P1 safety/quality evidence; exercise the complete browser acceptance matrix and VS Code extension in a real host; then rerun the release suite on one recorded revision. Deferred P2+ capabilities should remain clearly marked as later roadmap work rather than being mixed into the P1 exit gate.

## 10. Continuation remediation evidence (revision `354b8a9` plus working changes)

The following later evidence supersedes the corresponding open observations
above while preserving the original point-in-time audit history.

### Clean deployment and recovery gates

* A clean isolated Compose project created the schema on first bootstrap and
  returned `created=False` on the repeat bootstrap.
* The clean stack reported ready, retained graph counts across restart, and was
  removed without touching the normal development volumes.
* The current Docker test profile passed the Linux Python suite, live API/MCP/
  worker smoke journey, and both Playwright scenarios (login/search/trace/admin
  and invalid credentials).
* A checksum backup captured 179 vertices, 527 edges, and 9 raw files with
  SHA-256 `ebd5bd7be173f58d61bcd0cb549428a44e96e8f1ccbe2a635555a61a094b98ca`.
  Restore into an isolated empty HugeGraph instance reproduced all counts and
  preserved the golden path and source evidence.

These results close the clean-bootstrap and backup/restore portions of orders
5 and 7. Broader cross-source acceptance and the single-command release/demo
workflow remain separate work.

### `NFR-PERF-001` benchmark package

* Added versioned manifest `config/benchmarks/mvp-v1.json` and reproducible
  runner `scripts/benchmark.py`.
* The CI smoke profile and normative full profile now report true nearest-rank
  p50/p95/p99, throughput, hardware/configuration, Git state, CPU, peak RSS,
  and storage use. Benchmark failures are retained in the JSON report and
  return a non-zero exit.
* The full memory run generated 47,140 vertices and 223,940 edges from the
  documented 2,000-work-item / 15,000-commit / 25,000-file-symbol /
  5,000-document-section data shape. All measured in-process workloads passed
  their provisional thresholds; see `docs/benchmarks/2026-10-03-memory-full.json`.
* Live HugeGraph inspection exposed an O(E) edge-dedup lookup and a HugeGraph
  1.7 incompatibility: `UNIQUE` edge indexes are created but rejected for
  property-filter queries. The schema now uses a queryable `SECONDARY` edge-key
  index while retaining `edge_key` as the physical edge sort key. Schema
  migration waits for each asynchronous delete/rebuild task. A clean,
  isolated HugeGraph test verified indexed lookup and duplicate upsert collapse
  to one edge.
* The first isolated HugeGraph benchmark correctly failed bounded impact at
  3,814.025 ms p95 versus the 2,000 ms target. A bounded cache of immutable
  vertex identities removed redundant endpoint REST reads; the identical clean
  rerun passed at 917.343 ms p95. The failed and passing reports are both
  retained under `docs/benchmarks/`.
* The development graph migrated all 549 physical edge-key indexes from the
  non-queryable `UNIQUE` form to `SECONDARY`. Migration waits for HugeGraph
  delete/rebuild tasks, removed two known temporary index artifacts from an
  interrupted attempt, preserved the graph at 179 vertices / 527 edges, and
  completed with every normal service healthy.
* The post-migration Docker profile passed 461 Python tests and the live
  readiness/auth/query-limit, Jira-to-code/evidence/validation, durable replay,
  web, and MCP smoke checks. The browser journey exposed a stale-result race:
  graph entity buttons remained interactive during search. Those buttons now
  honor the global busy state; the login/search/path/agent/admin journey and
  invalid-credential scenario both pass on rerun.

The remaining performance gate is a full isolated HugeGraph + authenticated
HTTP run with server/container resource telemetry. Until that result is
published, the memory figures are algorithmic evidence only and not a product
performance claim.
