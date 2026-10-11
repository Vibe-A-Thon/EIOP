---
document_id: KGF-MASTER-BACKLOG-2026-10-11
version: 1.0
date: 2026-10-11
workspace: F:\code\EIP\EIOP
merges:
  - Audit-GAPS-G-dev.md   # EOIP-AUDIT-GAPS-G-DEV-2026-10-11 (826 requirements audited, 434 gaps)
  - Audit-GAPS-CG-dev.md  # AUDIT-GAPS-CG-DEV-2026-10-11 (CG-GAP-001..009, code-graph findings, closure plan)
  - index.html            # KnowGridFlow Conquest Plan v1.0 (47 deliverables, 8 KPIs, engineering principles)
audience: autonomous code-developer AI agent
tracker: kgf-completion-board.html (imports this file to show progress)
---

# KnowGridFlow / EOIP: Master Completion Backlog

This one file replaces the three source files as the working backlog. Every ID from all three is here exactly once. When every box in this file is ticked and the Phase 8 receipts exist, nothing listed in the three sources remains open.

## 1. Read this first

1. Work phase by phase, work package by work package, in the order of section 6. A package lists its dependencies; do not start it before they are ticked.
2. **Verify before you build.** Many rows marked "Not dev" with no code or test hint are features that already exist but were never tagged (see conflict C8). For every task: search the repo, then tag, complete or build, in that order.
3. Close each task against the Definition of Done in section 4. A task is done only when its evidence exists, not when code has been written.
4. Tick the box in this file (`[x]`) in the same commit that closes the task. Use `[~]` for in progress and `[!]` for blocked (add the reason after the row). The tracker HTML imports these marks.
5. Do not rewrite historical audit files. Do not invent requirement text: the authoritative text for FR, G2, GAP, MS, MVP and NFR IDs lives in `EOIP-engg-doc-pkg/*requirements*.md` and `diamond-moonshots-advanced.md`. Read the text for an ID before implementing it. Several G2 and MS titles below are only labels inferred from the ID prefix.
6. If a task cannot be completed without a human decision or live credentials, mark it `[!]`, note why, and move on. Section 5 lists the open decisions.
7. New work discovered during triage (CG-GAP-004) is appended to the matching package as a new row and to the registry. Never close the programme with unregistered gaps.

## 2. Mission and what "100% and production-ready" means here

Done means all of the following are true on one final working tree:

- All 516 tasks in this file are ticked (434 audited requirement rows, plus Plan, CG, roadmap, baseline and release tasks).
- The requirement registry (BASE-01) shows 826 of 826 audited requirements closed with code, a requirement-tagged test and, where applicable, an API route, a UI surface and an evidence receipt.
- Every exit gate in section 7 is met.
- Phase 8 receipts exist for live connectors, Hubble runtime, browser E2E, VS Code extension host, HA/backup/DR, security and performance.

Limits you must state in the final report rather than hide: the audits are static analyses of documentation and code; triage of the 1,199 unmapped documentation records (CG-GAP-004) may add tasks; MS-6/MS-7 have no definition in the audits; frontier items (MS-15, 18, 22, 29, 30) are open-ended and need agreed acceptance criteria (DEC-09).

## 3. Baseline snapshot (2026-10-11)

| Evidence | Result |
|---|---|
| Markdown corpus read mechanically | 192 files / 38,121 lines |
| Conservative documentation audit | 194 documents / 46,685 lines; 1,639 candidate records (440 Partial, 1,199 Missing) |
| Zero-tolerance requirement audit (G-dev) | 826 requirements: 392 fully developed (47.5%), 103 partial (12.5%), 331 roadmap (40.1%) |
| GAP coverage gate | 296/296 done; P0 gate passed |
| G2 coverage gate | 364/364 done; P0 gate passed |
| Deployment app route scan | 502 routes (memory backend) |
| Product capability scanner | 0.9857; first-choice gate failed only on PIC-002 (not advanced-ready) |
| Python test suite | 2,843 passed, 34 skipped, 2 warnings, 0 failures (709.87 s) |
| Web build | Vite build passed; 167 modules; 8.35 s |
| Not re-run in either audit | Live Hubble, real external connectors, production HA, browser E2E, VS Code extension host |

Per-family status from the G-dev audit:

| Family | Source spec | Total | Developed | Partial | Roadmap | Open rows in this file |
|---|---|---:|---:|---:|---:|---:|
| FR | `03-functional-requirements.md` | 67 | 14 | 27 | 26 | 53 |
| G2 | `gaps2-requirements.md` | 364 | 66 | 34 | 264 | 298 |
| GAP | `gaps-requirements.md` | 296 | 250 | 30 | 16 | 46 |
| KGR-G | `KGR-g-requirements.md` | 27 | 27 | 0 | 0 | 0 |
| MS | `diamond-moonshots-advanced.md` | 30 | 16 | 0 | 14 | 14 |
| MVP | `MVP-requirements.md` | 28 | 18 | 2 | 8 | 10 |
| NFR | `04-non-functional-requirements.md` | 14 | 1 | 10 | 3 | 13 |

### Already built: do not rebuild, only verify, tag and wire

| Area | Evidence |
|---|---|
| API runtime | `apps/api/app.py`, `main.py`, `extended.py`; 502 routes |
| Graph core | `packages/eoip/graph/*`: memory store, HugeGraph, Neptune, Neo4j, algorithms, metrics, bitemporal, evolution, snapshots, simulation, causal, what-if, twin, process mining |
| Query | `packages/eoip/query/*`: executor, NL/NLQ, policy, cache, languages, intelligence, polyglot engine (71 dialects), `multi_paradigm_dispatcher.py` |
| Retrieval / RAG | `packages/eoip/retrieval/*`, `ragx/*`, `rag_suite.py` (Graph, RAPTOR, LightRAG, HippoRAG, PathRAG, LazyGraphRAG, DRIFT) |
| Connectors / ingestion | `connectors/*`, `ingestion/*`, `fileparse/*`, `systems/*`: Jira, GitHub, GitLab, Confluence, ServiceNow, files, crawler, CI/CD, observability, API portal, SBOM |
| Agents, loops, memory | `agents/*`, `loops/*`, `reasoning/*`, `brain/*`; `mesh_supervisor.py`, `cognitive_narrator.py`, `learning_engine.py`, `living_brain_algorithms.py`, `models/self_llm.py` |
| Moonshot engines | `moonshot/live_causal_engine.py` (POST /api/v1/causal/live-blast-radius, /counterfactual-intervention); `ontology/domain_pack_manager.py` (GET/POST /api/v1/domain-packs/*, 8 domains); `audit/xai_ledger.py` (POST /api/v1/xai/certify-decision, /verify-certificate) |
| Database adapters | `graph/database_adapters.py`: 55 adapters (24 graph, 13 vector, 8 relational, 10 state) |
| Security / governance | `authn`, `authz`, `audit`, `egress`, `privacy`, `compliance`, `licensing`, `tenancy`, `config`, `model_management`, `marketplace`, `plugins`, `qa` |
| Web app | `apps/web`: Vite + React + JavaScript/CSS, Cytoscape graph explorer, admin, KGR panels, export/report UI |
| VS Code extension | `apps/vscode-extension`: extension host code, MCP client, demo driver, tests |
| MCP app | `apps/mcp/main.py` |
| Deployment / ops | `deploy/*`, Helm chart, container scripts, Hubble assets, backup/restore scripts, smoke/recovery scripts, Prometheus config |
| Code graph | `ingestion/code.py`, `code_graph_json.py`, `repository.py`, `local_code.py`, `packages/eoip/codegraph/*` with unit coverage |

## 4. Operating protocol

### 4.1 Per-task loop

1. Read the requirement text for the ID (spec file named in section 3), and any related rows.
2. Search the repo: the ID, its keywords, the module and route hints in the row. Record what exists.
3. Classify: **tag only** (code and test exist), **complete** (partial), **build** (absent), **needs live infrastructure** (provide an offline fixture and an acceptance test now; the live run is in Phase 8), or **needs decision** (mark `[!]`).
4. Implement as a vertical slice: model, service, API endpoint, brain_os telemetry, tests (principles below).
5. Add or tag the test with `@pytest.mark.req("<ID>")`.
6. Run the targeted tests, then the full suite and web build before ticking.
7. Update the registry row, tick the box, commit with the message `[<ID>] <summary>`.

### 4.2 Definition of Done (all tasks)

Implementation, unit tests, integration wiring, full test-suite pass, OpenAPI verification (Conquest "verify before moving on"). Plus, by family:

| Family | Extra evidence required |
|---|---|
| FR | Backend contract verified; dedicated apps/web screen (or an external-credential mock fixture) wired; explicit test fixture tagged @pytest.mark.req("<ID>"). |
| G2 | Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. |
| GAP | REST endpoint in apps/api/extended.py, automated verification test tagged with the ID, and a web dashboard visualization. |
| MS | Standalone service or UI canvas module, unit tests in tests/unit/, API surface, and brain_os telemetry. |
| MVP | Existing test annotated with @pytest.mark.req("<ID>"), acceptance criteria verified, and a new test added if none exists. |
| NFR | Measured threshold recorded: tests/benchmark/ (Locust or pytest-benchmark) for PERF/OPS/REL, tests/security/ for SEC/PRIV. Note: the audit text prescribes a load benchmark for every NFR; for security NFRs the correct evidence is a security test. |
| Plan / CG / roadmap | The description of the task is satisfied and verified by a test, a command output or a document diff cited in the commit. |
| Release (REL) | A receipt file: command, environment, date, commit SHA, result. |

### 4.3 Engineering principles (from the Conquest plan)

- **Real logic only.** Every module computes real values. No hardcoded scores, no placeholder returns, no mocked intelligence.
- **Vertical integration.** Every feature works end to end: model, service, API endpoint, brain_os telemetry, tests.
- **Test-verified.** Nothing ships without unit tests. Integration tests for API flows. Every edge case exercised.
- **Thread-safe singletons.** All stateful services use double-checked locking. No global mutable state. Safe for concurrent access.
- **OpenAPI first.** Every endpoint generates a clean OpenAPI 3.1 schema. Pydantic models at module level, always.
- **Local-first, no cloud lock-in.** Every capability works offline. Zero mandatory external calls. Air-gap deployable.

### 4.4 Commands

```powershell
$env:PYTHONPATH='packages;.'
python -m scripts.documentation_audit --project-root .
python -m scripts.gap_coverage --project-root . --output .tmp/gap-verify-current.json --fail-on-gate --gate-priority P0
python -m scripts.gap_coverage --project-root . --doc-set g2 --output .tmp/g2-verify-current.json --fail-on-gate --gate-priority P0
python -m pytest
cd apps/web; npm run build
```

### 4.5 Rules that prevent regressions

- No hardcoded scores, placeholder returns or mocked intelligence in non-test code.
- No new mandatory external calls; everything must work offline and air-gapped (NFR-SEC-001).
- Never commit secrets. Live-connector credentials come from environment or a secret store.
- Historical audit documents stay as written. Generated audit artifacts are derived evidence, never source requirements.
- Do not change a gate threshold to make it pass.

### 4.6 Working rhythm (from the Conquest plan)

- Session by session: pick one to three tasks from the current work package.
- Verify before moving on: implementation, unit tests, integration wiring, full suite, OpenAPI check.
- No skipping phases: phases are ordered by dependency. If a later task is unblocked and an earlier one is blocked, say so in the row and continue only with unblocked work.
- Adjust as you learn: if the owner says "reprioritize", reorder packages but keep the dependency lists true.

## 5. Reconciliation register and open decisions

The three sources disagree in places. This is how each disagreement is resolved in this backlog.

| # | Conflict | Resolution used |
|---|---|---|
| C1 | CG-dev says GAP 296/296 and G2 364/364 are "done"; G-dev says GAP 250/296 (84.5%) and G2 66/364 (18.1%) are fully developed. | Different yardsticks. The coverage gates check that a literal implementation lead exists; the zero-tolerance audit also requires code, a requirement-tagged test and a surface. This backlog closes against the stricter yardstick (see the Definition of Done) and keeps the gates as regression checks. |
| C2 | G-dev conclusion says "412 identified roadmap items"; its own tables give 103 partial + 331 roadmap = 434. | 434 is used. 14 MS + 298 G2 + 53 FR + 46 GAP + 10 MVP + 13 NFR = 434. |
| C3 | Conquest page headline says "forty deliverables"; it lists 47 (8 + 10 + 8 + 7 + 9 + 5). | All 47 are tracked. |
| C4 | Conquest stats are stale (481 modules, 2,607 tests, 143 endpoints, 62%) against the CG audit (2,843 tests, 502 routes). | CG audit numbers are the baseline. The "200+ endpoints" KPI is tightened to every deployed route (K-02). |
| C5 | G-dev Phase B text labels GitOps as MS-12 and the collaborative canvas as MS-13; its own table and the Conquest page say MS-12 = collaborative studio, MS-13 = graph-as-code. | Table titles win. The implementation notes were attached to the right item by title. |
| C6 | Conquest lists MS-17, MS-21, MS-23, MS-25 as planned; G-dev lists none of them as gaps (counts them developed). G-dev Phase D adds MS-30, which is also not in its gap table. | Tracked as verify-then-close tasks, not rebuilds. |
| C7 | G-dev gap and remediation text is identical for every row of a family (e.g. all 298 G2 rows say "requires live enterprise crawler connector or distributed Kubernetes"; all NFR rows say "requires 10,000 qps load benchmark"). | Treated as family-level templates, not item-specific diagnoses. Per-item work comes from the requirement text in the spec documents; the Definition of Done per family is in this backlog. |
| C8 | Rows marked NOT_YET_DEVELOPED with Code: None / Test: None include features that exist (e.g. MVP-FR-019 VS Code extension, FR-UI-001 web app, MVP-FR-022 MCP graph access). | Every task starts with a repo verification (BASE-04). Tag or complete what exists; never rebuild it. |
| C9 | Conquest says extension.js is 690 lines and needs graph webview and MCP integration; CG says the extension already has an MCP client, demo driver and tests; G-dev says FR-VSCODE / MVP-FR-019 are not developed. | Resolved by verification during GAP-IDE / WP 5.4, then host acceptance in REL-09. |
| C10 | Latency targets differ: Conquest p95 < 200 ms at 50K nodes vs G-dev sub-50 ms at 10,000 concurrent requests. | Both are measured (REL-12); DEC-08 settles which is the release criterion. |
| C11 | G-dev prescribes a Locust/pytest-benchmark script for every NFR, including security NFRs. | Security and privacy NFRs close with tests in tests/security/; performance, reliability and operations NFRs close with benchmarks. |
| C12 | CG-dev records live acceptance as unproven; G-dev and Conquest never plan it. | Added Phase 8 so "production ready" is evidenced, not asserted. |

Decisions needed from the owner. Where a recommendation is given, proceed with it unless told otherwise, except where the task is marked blocked.

| ID | Question | Recommendation | Affects |
|---|---|---|---|
| DEC-01 | Implement apps/console, or mark it not shipped? | Mark it not shipped and fold the operator functions into the admin web UI plus documented scripts, unless a requirement mandates a standalone console. | CG-GAP-006, FR-ADMIN-*, G2-ADMIN-* |
| DEC-02 | Keep Vite + React + JavaScript, or plan a TypeScript/Next.js migration? | Keep the current stack, correct the docs now, and list any migration as a separate future item. | CG-GAP-007 |
| DEC-03 | Loops route: mount eoip.loops.router at /api/v1/loops, or change the scanner to /api/v1/brain/loops? | Mount the router and keep the Brain OS route; this satisfies the scanner and the existing clients. | CG-GAP-001, PIC-002 |
| DEC-04 | Reports: add GET /api/v1/reports, or change the scanner? | Add the root summary route; it is small and makes the API discoverable. | CG-GAP-002, PIC-010 |
| DEC-05 | Generated audit artifacts: commit as derived evidence, or gitignore? | Commit under audits/generated with a header marking them derived; never treat them as requirements. | CG-GAP-009 |
| DEC-06 | Who provisions live infrastructure for Phase 8 (Jira, GitLab, GitHub, Confluence, ServiceNow tenants; Hubble; an HA environment)? | Name an owner and a date before Phase 2 ends. REL-06, REL-07 and REL-10 cannot be closed without it. | REL-06, REL-07, REL-10, CG-GAP-008 |
| DEC-07 | What are MS-6 and MS-7? | The audit only has placeholder titles. Read diamond-moonshots-advanced.md and copy the real definitions into the registry before building. | MS-6, MS-7 |
| DEC-08 | Which latency target is authoritative? | Keep both measurements (200 ms p95 at 50K nodes; 50 ms at 10,000 concurrent) until 04-non-functional-requirements.md settles it. | PERF-01, S-02, REL-12 |
| DEC-09 | Depth of the frontier items (MS-15, 18, 22, 29, 30) for "100%"? | Define per-item acceptance criteria and deliver a tested local reference runtime. State this explicitly, because full research-grade versions are open-ended. | MS-15, MS-18, MS-22, MS-29, MS-30 |
| DEC-10 | MS-26/27 commercial scope: billing ledger only, or an external billing provider? | Ledger plus usage export first; external billing integration only if a customer requires it. | MS-26, MS-27 |

## 6. Execution plan

Priority: P0 blocks the programme; P1 core; P2 scale; P3 frontier. Priorities come from the source where one was given (CG-GAP, Conquest phase labels, G-dev phase lists) and are derived otherwise.

| Phase | Name | Tasks | Priority | Origin |
|---:|---|---:|---|---|
| 0 | Baseline and traceability | 13 | P0 | Added by merge, from G-dev Phase A.1 and CG-GAP-003/004/005/009 |
| 1 | Harden and integrate | 65 | P0 | Conquest Phase 1, CG-GAP-001/002/006, G-dev Phase A |
| 2 | Acquisition fabric and live connectors | 130 | P0 | G-dev Phase A.2 (live connectors) and the G2-EKAF / G2-SYNC / G2-SRC families |
| 3 | Competitive differentiation and cognition | 52 | P0 | Conquest Phase 2 (KGR-G-011..020) plus temporal, causal and agent families |
| 4 | Intelligence amplification | 73 | P1 | Conquest Phase 3 plus GAP-FABRIC / CACHE / FRESH / TRUTH / QI and G2 domain families |
| 5 | Enterprise readiness and experience | 81 | P1 | Conquest Phase 4 plus FR-UI / ADMIN / VSCODE, G2-UX / ADMIN / VSC, GAP-GITOPS / MKT / SEC and G-dev Phase A.3 |
| 6 | Moonshots and trust | 45 | P1 | Conquest Phase 5 plus G-dev Phases B, C and D |
| 7 | Scale, reliability and polish | 40 | P2 | Conquest Phase 6 plus G-dev Phase C (NFR benchmark suite) and the G2 PERF / REL / SLO / TEL families |
| 8 | Production release gate | 17 | P0 | CG-GAP-008, CG closure plan steps 3 and 8, Conquest KPIs |

Checkbox format used below (the tracker parses it): table rows start `| [ ] | \`ID\` |`, list items start `- [ ] \`ID\``.

### Phase 0. Baseline and traceability

**Why now.** Both audits disagree on what "done" means (local gates say 364/364 for G2, the zero-tolerance audit says 66/364). Settle one definition, one registry and one test-tagging scheme first, so every later task is closed against the same evidence.

**Exit criteria.** Every task below ticked; full pytest and web build green; registry updated.

#### WP 0.1. Requirement registry and test tagging (5 tasks)

**Goal.** One machine-readable registry (ID, spec source, code, tests, API route, UI surface, evidence, status) and a pytest marker so every requirement is closed against test evidence.

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- MVP: Existing test annotated with @pytest.mark.req("<ID>"), acceptance criteria verified, and a new test added if none exists. Audit note: "Implemented via core services; lacks standalone explicit MVP requirement tag in test suite."

- [x] `BASE-01` **Create the requirement registry** (P0, src ADD+CG+G)
  - Create requirements-registry.json: one row per ID in this backlog (826 audited requirements plus Plan/CG/REL tasks) with spec source, code paths, tests, API route, UI surface, evidence receipt and status. This is the machine form of CG-GAP-004 ("convert candidates into atomic requirements, map semantically to code/tests").
- [x] `BASE-02` **Add the @pytest.mark.req marker and a requirement-to-test map** (P0, src G)
  - Register a req marker in pytest config, add a conftest plugin that collects the IDs per test and emits requirements-test-map.json. From G-dev Phase A step 1 and the MVP remediation text.
  - Related: `MVP-FR-027`
- [x] `BASE-03` **Retro-tag existing tests with requirement IDs** (P0, src G)
  - Tag all untagged tests in tests/ with the exact FR-*, G2-*, GAP-*, MVP-FR-* IDs they already cover (G-dev Phase A step 1). Most NOT_YET_DEVELOPED rows with "Test: None" are expected to flip to tagged-and-passing here without new code.
  - Related: `MVP-FR-027`
- [x] `BASE-04` **Verification sweep of all 434 audit-gap IDs** (P0, src ADD)
  - For every gap ID: search the repo (ID, keywords, route, module), then classify as already implemented (tag only), needs code, needs live infrastructure, or roadmap. Record in the registry. This prevents rebuilding features the audits mislabelled (see conflict C8) and lets the later phases focus on real work.

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [x] | `MVP-FR-027` | Automated tests | Partial | - | tests/unit/test_validation_source_binding.py |

#### WP 0.2. Documentation truth and drift reconciliation (8 tasks)

**Goal.** Make this backlog and available-status.md the active status, triage the 1,199 unmapped documentation-audit records, fix stale paths/stack claims and code-graph docs. Historical audit files stay historical.

- [x] `CG-CODE-01` **Align code-graph docs to the real modules** (P1, src CG)
  - EOIP-engg-doc-pkg/17-code-graph.md, reference/code-graph.md and the implementation work packages must point at packages/eoip/ingestion/code.py, code_graph_json.py, repository.py, local_code.py and packages/eoip/codegraph/*.
  - Related: `G2-SRC-CODE-002`
- [x] `CG-CODE-02` **Publish the exact polyglot parser language matrix** (P1, src CG)
  - Docs claim broad language coverage. Derive the matrix (language, parse depth, edge types, test file) from the current parser and code-ingestion tests, and use it as the single source of truth for each language claim.
  - Related: `FR-CODE-002`
- [x] `CG-DOC-01` **Point the live docs at this backlog** (P0, src CG)
  - Update README.md, available-status.md, todo-status.md, EOIP-engg-doc-pkg/available-status.md, EOIP-engg-doc-pkg/todo-status.md, EOIP-engg-doc-pkg/DOCUMENTATION-INDEX.md and EOIP-engg-doc-pkg/README.md to reference the master backlog and the generated evidence files (current-gap-report.json/.md, documentation-inventory.json). Historical audit files stay historical and must not be silently rewritten.
- [x] `CG-GAP-003` **Reconcile documentation drift** (P0, src CG)
  - Status: Documentation drift. Gap: Current docs still contain stale or incorrect implementation paths and historical pass counts. Evidence: Older status docs referenced apps/console, packages/eoip/ontology/schema.py, packages/eoip/rag/engine.py and old pytest totals. Closure: Treat this backlog and available-status.md as active current status; reconcile older docs section by section instead of rewriting historical audit records.
  - Related: `CG-DOC-01`
- [x] `CG-GAP-004` **Triage the 1,199 unmapped documentation-audit records** (P0, src CG)
  - Status: Traceability gap. Gap: Conservative documentation audit indexed 1,199 candidate records without literal implementation/test leads (1,639 records: 440 Partial, 1,199 Missing). Evidence: python -m scripts.documentation_audit --project-root . Closure: Convert candidates into atomic requirements, map semantically to code/tests, retire false positives. Classify each as: true gap, duplicate historical claim, false positive, or roadmap item. Every true gap becomes a new task in the registry (loop-back rule).
  - Related: `BASE-01`, `REL-05`
- [x] `CG-GAP-005` **Markdown link-check pass (non-historical docs first)** (P1, src CG)
  - Status: Documentation link drift. Gap: Root README guide links were corrected, but historical/engineering package links still need a dedicated pass. Evidence: Earlier link audit found stale local Markdown links. Closure: Run a link checker after the audit and patch non-historical docs first. Re-run in Phase 8 (REL-13).
  - Related: `REL-13`
- [x] `CG-GAP-007` **Update web UX docs to the real stack** (P1, src CG)
  - Status: Web stack documentation drift. Gap: Older docs claim Next.js, TypeScript, Tailwind and 2D/3D Force-Graph; the current app is Vite + React + JavaScript/CSS with a Cytoscape-based graph UI. Evidence: apps/web/package.json, build output, and source tree. Closure: Update web UX docs to the current stack and describe any planned future stack separately. See DEC-02.
- [x] `CG-GAP-009` **Generated audit artifacts policy** (P2, src CG)
  - Status: Generated artifacts are derived evidence. Gap: EOIP-engg-doc-pkg/audits/generated/* is generated by the audit script and useful, but is derived evidence. Evidence: Generated in the CG audit pass. Closure: Keep as audit evidence or add to a generated-artifact policy. Never treat generated output as source requirements. See DEC-05.


### Phase 1. Harden and integrate

**Why now.** Real infrastructure under the intelligence features: HugeGraph wiring, real embeddings, integration tests on every route, auth on every handler. Close the two scanner/route gaps that currently fail the product first-choice gate.

**Exit criteria.** Every task below ticked; full pytest and web build green; registry updated; OpenAPI schema resolves.

#### WP 1.1. Platform hardening (Conquest Phase 1) (8 tasks)

**Goal.** Real HugeGraph queries, real embeddings, integration tests for all routes, auth/RBAC on every handler, validated config, compose smoke test, RFC 7807 errors, published OpenAPI and SDKs.

**Depends on.** WP 0.1

- [x] `H-01` **HugeGraph adapter wiring** (P0, about 3 sessions, src CQ)
  - Connect graph/* modules to real Gremlin queries via hugegraph.py adapter
  - Related: `FR-GRAPH-007`
- [x] `H-02` **Real embedding integration** (P0, about 2 sessions, src CQ)
  - Replace _hash_embed() with sentence-transformers or Ollama embeddings in semantic.py + hybrid_engine.py
- [x] `H-03` **Integration test suite** (P0, about 3 sessions, src CQ)
  - TestClient-based tests for all 143 API endpoints across platform_router + enterprise_router
- [x] `H-04` **Auth/RBAC enforcement** (P0, about 2 sessions, src CQ)
  - Wire authn/ JWT flows + authz/ RBAC policies onto all route handlers
  - Related: `NFR-SEC-005`
- [x] `H-05` **Configuration validation** (P0, about 1 session, src CQ)
  - Pydantic settings for all env vars, .env loading, config-as-code verification
- [x] `H-06` **Docker Compose smoke test** (P0, about 1 session, src CQ)
  - Verify deploy/docker-compose.yml boots HugeGraph + API + web, health checks pass
- [x] `H-07` **Error handling audit** (P0, about 1 session, src CQ)
  - Consistent error responses (RFC 7807), proper HTTP status codes, no stack traces in prod
- [x] `H-08` **OpenAPI schema publication** (P0, about 1 session, src CQ)
  - Published Swagger UI, generate Python/TypeScript SDK clients from spec

#### WP 1.2. Route, scanner and operator-console closure (3 tasks)

**Goal.** Make the product capability scanner pass the first-choice gate (PIC-002 loops catalog, PIC-010 reports root) and settle the apps/console question.

- [x] `CG-GAP-001` **Mount the loops catalog route (PIC-002)** (P0, src CG)
  - Status: Partially developed. Gap: Product scanner expects /api/v1/loops/catalog; the deployment route table exposes /api/v1/brain/loops and the standalone eoip.loops.router is not mounted. Evidence: Route scan found /api/v1/brain/loops, not /api/v1/loops/catalog; packages/eoip/loops/router.py exists. Closure: Mount build_router() from eoip.loops.router, or update the scanner/docs to the supported Brain OS loops route. Add a route test.
  - Related: `REL-04`
- [x] `CG-GAP-002` **Add the reports root route (PIC-010)** (P1, src CG)
  - Status: Partially developed / scanner mismatch. Gap: Scanner expects exact /api/v1/reports; the app exposes /api/v1/reports/templates, /render, /export/{report_id} and schedule routes but no root index. Evidence: Route scan found report subroutes but not /api/v1/reports. Closure: Add GET /api/v1/reports summary route, or change the scanner expectation to a concrete subroute.
  - Related: `REL-04`
- [x] `CG-GAP-006` **Decide and close the apps/console question** (P1, src CG)
  - Status: Operator console drift. Gap: Older docs mention apps/console; no apps/console directory exists. Evidence: Test-Path apps\console returned false. Closure: Either implement the console, move console capability into documented scripts/API (and the admin web UI), or mark the console as not shipped. See DEC-01.

#### WP 1.3. Core graph, ontology, provenance and validation contracts (33 tasks)

**Goal.** Canonical identifiers, bridge edges, Gremlin repository, graph version journal, RDF/OWL interop, bitemporal fields, evidence/provenance model, validation gates, and the G2 architecture principles and rule catalog.

**Depends on.** WP 1.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- FR: Backend contract verified; dedicated apps/web screen (or an external-credential mock fixture) wired; explicit test fixture tagged @pytest.mark.req("<ID>"). Audit note: "Backend logic present but missing dedicated frontend screen or external credential mock."
- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [x] | `FR-GRAPH-002` | Logical graph domains | Partial | packages/eoip/graph/meta.py | - |
| [x] | `FR-GRAPH-003` | Schema bootstrap | Partial | - | tests/unit/test_phase2_hugegraph_schema.py |
| [x] | `FR-GRAPH-004` | Canonical identifiers | Not dev | - | - |
| [x] | `FR-GRAPH-005` | Meta graph | Partial | packages/eoip/graph/meta.py | - |
| [x] | `FR-GRAPH-006` | Cross-domain bridge edges | Not dev | - | - |
| [x] | `FR-GRAPH-007` | Gremlin repository | Not dev | - | - |
| [x] | `FR-GRAPH-008` | Index strategy | Partial | packages/eoip/ontology/manifest.py | - |
| [x] | `FR-GRAPH-009` | Graph version journal | Not dev | - | - |
| [x] | `FR-GRAPH-010` | RDF/OWL interoperability | Not dev | - | - |
| [x] | `FR-ONTO-001` | Enterprise ontology vocabulary | Partial | packages/eoip/ontology/manifest.py | - |
| [x] | `FR-ONTO-002` | Relationship semantics | Partial | packages/eoip/ontology/manifest.py | - |
| [x] | `FR-PROV-001` | Evidence model | Partial | packages/eoip/provenance/evidence.py | - |
| [x] | `FR-PROV-002` | Provenance traversal | Partial | packages/eoip/provenance/lineage.py | - |
| [x] | `FR-TEMP-001` | Bitemporal-ready fields | Not dev | - | - |
| [x] | `FR-VALID-001` | Graph validation rules | Partial | packages/eoip/validation/engine.py | - |
| [x] | `FR-VALID-002` | Validation gates | Partial | packages/eoip/ontology/manifest.py, packages/eoip/validation/engine.py | - |
| [x] | `G2-ARCH-002` | API/event first | Partial | packages/eoip/gaps/g2_architecture.py | - |
| [x] | `G2-ARCH-003` | Deterministic first | Partial | packages/eoip/gaps/g2_architecture.py | - |
| [x] | `G2-ARCH-004` | Preserve source fidelity | Partial | packages/eoip/gaps/g2_architecture.py | - |
| [x] | `G2-ARCH-005` | HugeGraph is semantic operational truth | Partial | packages/eoip/gaps/g2_architecture.py | - |
| [x] | `G2-ARCH-008` | Current and historical views | Partial | packages/eoip/gaps/g2_architecture.py | - |
| [x] | `G2-ARCH-009` | One semantic identity system | Partial | packages/eoip/gaps/g2_architecture.py | - |
| [x] | `G2-ARCH-012` | Incremental by default after baseline | Partial | packages/eoip/gaps/g2_architecture.py | - |
| [x] | `G2-ARCH-013` | Replayability | Partial | packages/eoip/gaps/g2_architecture.py | - |
| [x] | `G2-ARCH-014` | Source permissions respected | Partial | packages/eoip/gaps/g2_architecture.py | - |
| [x] | `G2-ARCHC-002` | Architecture rule catalog | Partial | packages/eoip/graph/rule_catalog.py | - |
| [x] | `G2-ARCHC-003` | Architecture rule catalog | Not dev | - | - |
| [x] | `G2-ARCHC-004` | Architecture rule catalog | Not dev | - | - |
| [x] | `G2-ARCHC-005` | Architecture rule catalog | Not dev | - | - |
| [x] | `G2-ARCHC-006` | Architecture rule catalog | Not dev | - | - |
| [x] | `G2-ARCHC-007` | Architecture rule catalog | Not dev | - | - |
| [x] | `G2-ARCHC-008` | Architecture rule catalog | Not dev | - | - |
| [x] | `G2-ARCHC-009` | Architecture rule catalog | Not dev | - | - |

#### WP 1.4. Query, RAG and MCP core (13 tasks)

**Goal.** Entity search, structured QueryPlan, retrieval router, local GraphRAG, MCP graph access with action separation.

**Depends on.** WP 1.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- FR: Backend contract verified; dedicated apps/web screen (or an external-credential mock fixture) wired; explicit test fixture tagged @pytest.mark.req("<ID>"). Audit note: "Backend logic present but missing dedicated frontend screen or external credential mock."
- MVP: Existing test annotated with @pytest.mark.req("<ID>"), acceptance criteria verified, and a new test added if none exists. Audit note: "Implemented via core services; lacks standalone explicit MVP requirement tag in test suite."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [x] | `FR-MCP-001` | MCP read server | Partial | apps/mcp/main.py | - |
| [x] | `FR-MCP-002` | MCP action separation | Partial | apps/mcp/main.py | - |
| [x] | `FR-QUERY-001` | Structured QueryPlan | Partial | packages/eoip/contracts/query_plan.py | - |
| [x] | `FR-QUERY-002` | Path query | Partial | packages/eoip/contracts/graph_result.py | - |
| [x] | `FR-QUERY-003` | Impact analysis | Partial | packages/eoip/contracts/graph_result.py | - |
| [x] | `FR-QUERY-004` | Entity search | Not dev | - | - |
| [x] | `FR-QUERY-007` | Query evidence envelope | Partial | packages/eoip/contracts/graph_result.py | - |
| [x] | `FR-RAG-001` | Retrieval router | Partial | packages/eoip/retrieval/service.py | - |
| [x] | `FR-RAG-002` | GraphRAG evidence retrieval | Partial | packages/eoip/models/provider.py, packages/eoip/retrieval/service.py | - |
| [x] | `FR-RAG-003` | Local model abstraction | Partial | packages/eoip/retrieval/service.py | - |
| [x] | `FR-RAG-004` | No mandatory vector DB in MVP | Not dev | - | - |
| [x] | `MVP-FR-020` | Local GraphRAG | Not dev | - | - |
| [x] | `MVP-FR-022` | MCP core graph access | Not dev | - | - |

#### WP 1.5. Security and privacy baseline (8 tasks)

**Goal.** Authentication, input/file safety, injection defenses, secret isolation, no-egress, container hardening, audit events and data minimization.

**Depends on.** WP 1.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- NFR: Measured threshold recorded: tests/benchmark/ (Locust or pytest-benchmark) for PERF/OPS/REL, tests/security/ for SEC/PRIV. Note: the audit text prescribes a load benchmark for every NFR; for security NFRs the correct evidence is a security test. Audit note: "Non-functional constraint active; requires formal 10,000 qps load benchmark harness."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [x] | `NFR-PRIV-001` | Data minimization and classification | Partial | - | tests/unit/test_agent_memory.py |
| [x] | `NFR-SEC-001` | No outbound enterprise-data egress | Partial | - | tests/security/test_no_egress.py, tests/security/test_verification_suite.py |
| [x] | `NFR-SEC-002` | Secret isolation | Partial | - | tests/security/test_verification_suite.py |
| [x] | `NFR-SEC-003` | Input/file safety | Not dev | - | - |
| [x] | `NFR-SEC-004` | Prompt/tool injection defenses | Partial | - | tests/security/test_verification_suite.py |
| [x] | `NFR-SEC-005` | Authentication without MVP RBAC | Not dev | - | - |
| [x] | `NFR-SEC-006` | Container hardening | Partial | - | tests/security/test_container_hardening.py |
| [x] | `NFR-SEC-007` | Audit events | Partial | packages/eoip/audit/sink.py | - |


### Phase 2. Acquisition fabric and live connectors

**Why now.** Everything downstream depends on trustworthy ingestion: connector SDK, incremental sync, event semantics, source connectors with offline fixtures, and crawler security.

**Exit criteria.** Every task below ticked; full pytest and web build green; registry updated; OpenAPI schema resolves.

#### WP 2.1. Connector SDK and acquisition framework (35 tasks)

**Goal.** Connector SDK, SourceEvent envelope, baseline and incremental crawl, webhook/poll, idempotency, checkpointing, replay, dead-letter, dry run, fixtures, onboarding wizard, and the FR connector/ingest contracts.

**Depends on.** WP 1.3

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- FR: Backend contract verified; dedicated apps/web screen (or an external-credential mock fixture) wired; explicit test fixture tagged @pytest.mark.req("<ID>"). Audit note: "Backend logic present but missing dedicated frontend screen or external credential mock."
- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [x] | `FR-CONN-001` | Connector SDK | Partial | packages/eoip/connectors/base.py | - |
| [x] | `FR-CONN-002` | Jira JSON connector | Not dev | packages/eoip/connectors/jira_json.py, packages/eoip/ingestion/jira.py | tests/unit/test_jira_ingestion.py |
| [x] | `FR-CONN-003` | Git repository connector | Not dev | - | - |
| [x] | `FR-CONN-004` | GitLab metadata adapter | Not dev | - | - |
| [x] | `FR-CONN-005` | Connector resiliency | Not dev | - | - |
| [x] | `FR-CONN-007` | Source deletion semantics | Not dev | packages/eoip/connectors/jira_json.py, packages/eoip/ingestion/jira.py | tests/unit/test_jira_ingestion.py |
| [x] | `FR-INGEST-001` | Raw capture | Partial | packages/eoip/contracts/source_event.py, packages/eoip/ingestion/jira.py | tests/unit/test_jira_ingestion.py |
| [x] | `FR-INGEST-002` | Canonicalization | Partial | packages/eoip/identity/resolver.py | - |
| [x] | `FR-INGEST-004` | Ingestion job lifecycle | Not dev | - | - |
| [x] | `G2-EKAF-002` | Connector SDK | Not dev | - | - |
| [x] | `G2-EKAF-003` | SourceEvent envelope | Complete | packages/eoip/contracts/source_event.py | tests/contract/test_g2_contracts.py |
| [x] | `G2-EKAF-004` | Baseline crawl | Not dev | - | - |
| [x] | `G2-EKAF-005` | Incremental sync | Not dev | - | - |
| [x] | `G2-EKAF-006` | Webhook/event ingestion | Not dev | - | - |
| [x] | `G2-EKAF-007` | Poll fallback | Not dev | - | - |
| [x] | `G2-EKAF-008` | Reconciliation crawl | Not dev | - | - |
| [x] | `G2-EKAF-009` | Idempotency | Not dev | - | - |
| [x] | `G2-EKAF-010` | Ordering tolerance | Complete | packages/eoip/graph/evolution.py | tests/unit/test_graph_evolution.py |
| [x] | `G2-EKAF-011` | Rate limiting | Not dev | - | - |
| [x] | `G2-EKAF-012` | Checkpointing | Not dev | - | - |
| [x] | `G2-EKAF-013` | Replay | Not dev | - | - |
| [x] | `G2-EKAF-014` | Dead-letter handling | Complete | packages/eoip/ingestion/dlq.py | tests/unit/test_phase2_ingestion.py |
| [x] | `G2-EKAF-015` | Dry run | Not dev | - | - |
| [x] | `G2-EKAF-016` | Source deletion semantics | Complete | packages/eoip/graph/evolution.py | tests/unit/test_graph_evolution.py |
| [x] | `G2-EKAF-019` | Crawl boundaries | Partial | - | tests/unit/test_acquisition_fabric.py |
| [x] | `G2-EKAF-020` | Authentication isolation | Not dev | - | - |
| [x] | `G2-EKAF-021` | Connector health | Partial | - | tests/unit/test_source_registry.py |
| [x] | `G2-EKAF-023` | Permission-aware metadata | Complete | packages/eoip/contracts/source_event.py | tests/contract/test_g2_contracts.py |
| [x] | `G2-EKAF-024` | Content fingerprinting | Complete | packages/eoip/graph/evolution.py | tests/unit/test_graph_evolution.py |
| [x] | `G2-EKAF-025` | Attachment handling | Complete | packages/eoip/connectors/files.py, packages/eoip/ingestion/files.py | tests/unit/test_file_ingestion.py |
| [x] | `G2-EKAF-026` | Incremental graph enrichment | Complete | packages/eoip/identity/resolver.py | tests/unit/test_identity_resolver.py |
| [x] | `G2-EKAF-027` | Source capability introspection | Not dev | - | - |
| [x] | `G2-EKAF-028` | Connector compatibility matrix | Partial | - | tests/unit/test_source_registry.py |
| [x] | `G2-EKAF-029` | Offline source fixture mode | Not dev | - | - |
| [x] | `G2-EKAF-030` | Source onboarding wizard | Not dev | - | - |

#### WP 2.2. Sync and event semantics (19 tasks)

**Goal.** Baseline snapshot, delta processing, delete/retire, missed/duplicate/late events, dependency-aware update, consistency watermark, rebuild equivalence, backfill, selective rescan, plus the event family.

**Depends on.** WP 2.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [x] | `G2-EVENT-002` | Event model and streaming | Complete | packages/eoip/graph/evolution.py | tests/unit/test_semantic_consumers_reconciliation.py |
| [x] | `G2-EVENT-003` | Event model and streaming | Complete | packages/eoip/graph/consumers.py | tests/unit/test_semantic_consumers_reconciliation.py |
| [x] | `G2-EVENT-004` | Event model and streaming | Complete | packages/eoip/graph/evolution.py, packages/eoip/graph/consumers.py | tests/unit/test_semantic_consumers_reconciliation.py |
| [x] | `G2-EVENT-005` | Event model and streaming | Complete | packages/eoip/graph/consumers.py | tests/unit/test_semantic_consumers_reconciliation.py |
| [x] | `G2-EVENT-006` | Event model and streaming | Complete | packages/eoip/graph/consumers.py | tests/unit/test_semantic_consumers_reconciliation.py |
| [x] | `G2-EVENT-007` | Event model and streaming | Complete | packages/eoip/graph/evolution.py, packages/eoip/graph/consumers.py | tests/unit/test_semantic_consumers_reconciliation.py |
| [x] | `G2-SYNC-002` | Baseline snapshot | Complete | packages/eoip/connectors/acquisition.py | tests/unit/test_acquisition_fabric.py |
| [x] | `G2-SYNC-003` | Delta processing | Complete | packages/eoip/connectors/reconciliation.py | tests/unit/test_semantic_consumers_reconciliation.py |
| [x] | `G2-SYNC-004` | Delete/retire | Complete | packages/eoip/graph/evolution.py | tests/unit/test_graph_evolution.py |
| [x] | `G2-SYNC-005` | Missed-event recovery | Complete | packages/eoip/connectors/reconciliation.py | tests/unit/test_semantic_consumers_reconciliation.py |
| [x] | `G2-SYNC-006` | Duplicate-event handling | Complete | packages/eoip/graph/evolution.py | tests/unit/test_graph_evolution.py |
| [x] | `G2-SYNC-007` | Late event handling | Complete | packages/eoip/graph/evolution.py | tests/unit/test_graph_evolution.py |
| [x] | `G2-SYNC-008` | Dependency-aware update | Complete | packages/eoip/graph/consumers.py | tests/unit/test_semantic_consumers_reconciliation.py |
| [x] | `G2-SYNC-009` | Consistency watermark | Complete | packages/eoip/connectors/confluence.py, packages/eoip/connectors/servicenow.py, packages/eoip/ingestion/source_sync.py | tests/unit/test_phase2_api.py |
| [x] | `G2-SYNC-010` | Full rebuild is exceptional | Complete | packages/eoip/connectors/acquisition.py | tests/unit/test_acquisition_sync_semantics.py |
| [x] | `G2-SYNC-011` | Rebuild equivalence test | Complete | packages/eoip/ingestion/replay.py | tests/unit/test_file_ingestion.py |
| [x] | `G2-SYNC-012` | Connector pause/resume | Complete | packages/eoip/connectors/acquisition.py | tests/unit/test_acquisition_fabric.py |
| [x] | `G2-SYNC-013` | Backfill | Complete | packages/eoip/connectors/acquisition.py | tests/unit/test_acquisition_sync_semantics.py |
| [x] | `G2-SYNC-014` | Selective rescan | Complete | packages/eoip/connectors/acquisition.py | tests/unit/test_acquisition_sync_semantics.py |

#### WP 2.3. Enterprise source connectors (57 tasks)

**Goal.** Live-capable connectors with offline fixtures for Jira, Confluence, ServiceNow, GitHub, GitLab, CI/CD, API portal, observability, SBOM, web crawl and related sources, including the Jira changelog stream.

**Depends on.** WP 2.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- FR: Backend contract verified; dedicated apps/web screen (or an external-credential mock fixture) wired; explicit test fixture tagged @pytest.mark.req("<ID>"). Audit note: "Backend logic present but missing dedicated frontend screen or external credential mock."
- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."

- [x] `CONN-01` **Confluence offline fixtures and live-connector test** (P0, src G)
  - G-dev Phase A step 2: extend packages/eoip/connectors/ with real mock fixtures for Confluence. Related: FR-CONF-001, G2-SRC-CONF-*.
  - Related: `FR-CONF-001`
- [x] `CONN-02` **ServiceNow offline fixtures and live-connector test** (P0, src G)
  - G-dev Phase A step 2: real mock fixtures for ServiceNow. Related: FR-SNOW-001, G2-SRC-SNOW-*.
  - Related: `FR-SNOW-001`
- [x] `CONN-03` **Jira changelog streaming connector and fixtures** (P0, src G)
  - G-dev Phase A step 2: Jira changelog streaming with mock fixtures. Related: FR-CONN-002, G2-SRC-JIRA-*.
  - Related: `FR-CONN-002`

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [x] | `FR-CONF-001` | Confluence connector | Complete | packages/eoip/connectors/confluence.py | tests/unit/test_phase2_connectors.py |
| [x] | `FR-SNOW-001` | ServiceNow connector | Complete | packages/eoip/connectors/servicenow.py | tests/unit/test_servicenow_connector.py |
| [x] | `G2-SRC-API-002` | Source: API portal | Complete | packages/eoip/connectors/api_portal.py | tests/unit/test_api_portal_connector.py |
| [x] | `G2-SRC-API-003` | Source: API portal | Complete | packages/eoip/connectors/api_portal.py | tests/unit/test_api_portal_connector.py |
| [x] | `G2-SRC-API-004` | Source: API portal | Complete | packages/eoip/connectors/api_portal.py | tests/unit/test_api_portal_connector.py |
| [x] | `G2-SRC-API-005` | Source: API portal | Complete | packages/eoip/connectors/api_portal.py | tests/unit/test_api_portal_connector.py |
| [x] | `G2-SRC-API-006` | Source: API portal | Complete | packages/eoip/connectors/api_portal.py | tests/unit/test_api_portal_connector.py |
| [x] | `G2-SRC-CICD-002` | Source: CI/CD | Complete | packages/eoip/connectors/cicd.py | tests/unit/test_cicd_connector.py |
| [x] | `G2-SRC-CICD-003` | Source: CI/CD | Complete | packages/eoip/connectors/cicd.py | tests/unit/test_cicd_connector.py |
| [x] | `G2-SRC-CICD-004` | Source: CI/CD | Complete | packages/eoip/connectors/cicd.py | tests/unit/test_cicd_connector.py |
| [x] | `G2-SRC-CONF-002` | Source: Confluence | Complete | packages/eoip/connectors/confluence.py | tests/unit/test_confluence_history.py |
| [x] | `G2-SRC-CONF-003` | Source: Confluence | Complete | packages/eoip/connectors/confluence_body.py | tests/unit/test_confluence_body.py |
| [x] | `G2-SRC-CONF-004` | Source: Confluence | Complete | packages/eoip/connectors/confluence.py | tests/unit/test_document_references.py |
| [x] | `G2-SRC-CONF-005` | Source: Confluence | Complete | packages/eoip/connectors/confluence.py | tests/unit/test_document_references.py |
| [x] | `G2-SRC-DD-002` | Source: DD connector | Not dev | - | - |
| [x] | `G2-SRC-DD-003` | Source: DD connector | Not dev | - | - |
| [x] | `G2-SRC-DD-004` | Source: DD connector | Not dev | - | - |
| [x] | `G2-SRC-GH-002` | Source: GitHub | Partial | - | tests/unit/test_acquisition_fabric.py |
| [x] | `G2-SRC-GH-003` | Source: GitHub | Not dev | - | - |
| [x] | `G2-SRC-GH-004` | Source: GitHub | Not dev | - | - |
| [x] | `G2-SRC-GL-002` | Source: GitLab | Partial | - | tests/unit/test_acquisition_fabric.py |
| [x] | `G2-SRC-GL-003` | Source: GitLab | Not dev | - | - |
| [x] | `G2-SRC-GL-004` | Source: GitLab | Not dev | - | - |
| [x] | `G2-SRC-GRAF-002` | Source: Grafana | Not dev | - | - |
| [x] | `G2-SRC-GRAF-003` | Source: Grafana | Not dev | - | - |
| [x] | `G2-SRC-JIRA-002` | Source: Jira | Complete | packages/eoip/connectors/jira.py | tests/unit/test_jira_connector.py |
| [x] | `G2-SRC-JIRA-003` | Source: Jira | Complete | packages/eoip/connectors/jira.py | tests/unit/test_jira_connector.py |
| [x] | `G2-SRC-JIRA-004` | Source: Jira | Complete | packages/eoip/connectors/jira.py | tests/unit/test_jira_connector.py |
| [x] | `G2-SRC-JIRA-005` | Source: Jira | Complete | packages/eoip/connectors/jira.py | tests/unit/test_jira_connector.py |
| [x] | `G2-SRC-JIRA-006` | Source: Jira | Complete | packages/eoip/connectors/jira.py | tests/unit/test_jira_connector.py |
| [x] | `G2-SRC-KIB-002` | Source: Kibana | Not dev | - | - |
| [x] | `G2-SRC-KIB-003` | Source: Kibana | Not dev | - | - |
| [x] | `G2-SRC-KIB-004` | Source: Kibana | Not dev | - | - |
| [x] | `G2-SRC-KIB-005` | Source: Kibana | Not dev | - | - |
| [x] | `G2-SRC-OTEL-002` | Source: OpenTelemetry | Complete | packages/eoip/connectors/otel.py | tests/unit/test_otel_connector.py |
| [x] | `G2-SRC-OTEL-003` | Source: OpenTelemetry | Complete | packages/eoip/connectors/otel.py | tests/unit/test_otel_connector.py |
| [x] | `G2-SRC-OTEL-004` | Source: OpenTelemetry | Complete | packages/eoip/connectors/otel.py | tests/unit/test_otel_connector.py |
| [x] | `G2-SRC-OTEL-005` | Source: OpenTelemetry | Complete | packages/eoip/connectors/otel.py | tests/unit/test_otel_connector.py |
| [x] | `G2-SRC-RUNTIME-002` | Source: runtime | Complete | packages/eoip/connectors/runtime_infra.py | tests/unit/test_runtime_connector.py |
| [x] | `G2-SRC-RUNTIME-003` | Source: runtime | Complete | packages/eoip/connectors/runtime_infra.py | tests/unit/test_runtime_connector.py |
| [x] | `G2-SRC-SBOM-002` | Source: SBOM | Complete | packages/eoip/connectors/sbom.py | tests/unit/test_sbom_connector.py |
| [x] | `G2-SRC-SBOM-003` | Source: SBOM | Complete | packages/eoip/connectors/sbom.py | tests/unit/test_sbom_connector.py |
| [x] | `G2-SRC-SBOM-004` | Source: SBOM | Complete | packages/eoip/connectors/sbom.py | tests/unit/test_sbom_connector.py |
| [x] | `G2-SRC-SNKB-002` | Source: ServiceNow knowledge base | Complete | packages/eoip/connectors/servicenow.py | tests/unit/test_servicenow_connector.py |
| [x] | `G2-SRC-SNKB-003` | Source: ServiceNow knowledge base | Complete | packages/eoip/connectors/servicenow.py | tests/unit/test_servicenow_connector.py |
| [x] | `G2-SRC-SNOW-002` | Source: ServiceNow | Complete | packages/eoip/connectors/servicenow.py | tests/unit/test_servicenow_connector.py |
| [x] | `G2-SRC-SNOW-003` | Source: ServiceNow | Complete | packages/eoip/connectors/servicenow.py | tests/unit/test_servicenow_connector.py |
| [x] | `G2-SRC-SNOW-004` | Source: ServiceNow | Complete | packages/eoip/connectors/servicenow.py | tests/unit/test_servicenow_connector.py |
| [x] | `G2-SRC-SNOW-005` | Source: ServiceNow | Complete | packages/eoip/connectors/servicenow.py | tests/unit/test_servicenow_connector.py |
| [x] | `G2-SRC-SNOW-006` | Source: ServiceNow | Complete | packages/eoip/connectors/servicenow.py | tests/unit/test_servicenow_connector.py |
| [x] | `G2-SRC-WEB-002` | Source: web crawl | Complete | packages/eoip/connectors/crawler.py | tests/unit/test_web_crawler_connector.py |
| [x] | `G2-SRC-WEB-003` | Source: web crawl | Complete | packages/eoip/connectors/crawler.py | tests/unit/test_web_crawler_connector.py |
| [x] | `G2-SRC-WEB-004` | Source: web crawl | Complete | packages/eoip/connectors/crawler.py | tests/unit/test_web_crawler_connector.py |
| [x] | `G2-SRC-WEB-005` | Source: web crawl | Complete | packages/eoip/connectors/crawler.py | tests/unit/test_web_crawler_connector.py |

#### WP 2.4. Code graph and repository sources (8 tasks)

**Goal.** Deterministic parsing (Python/TypeScript MVP and the exact language matrix), call/import/dependency edges, source navigation, repository sources, and code-graph docs aligned to modules.

**Depends on.** WP 2.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- FR: Backend contract verified; dedicated apps/web screen (or an external-credential mock fixture) wired; explicit test fixture tagged @pytest.mark.req("<ID>"). Audit note: "Backend logic present but missing dedicated frontend screen or external credential mock."
- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [x] | `FR-CODE-001` | Deterministic code parser | Partial | - | tests/unit/test_requirement_evidence.py |
| [x] | `FR-CODE-002` | Python and TypeScript MVP parsing | Not dev | - | - |
| [x] | `FR-CODE-004` | Call/import/dependency edges | Not dev | - | - |
| [x] | `FR-CODE-005` | Source navigation | Not dev | - | - |
| [x] | `G2-SRC-CODE-002` | Source: code repositories | Not dev | - | - |
| [x] | `G2-SRC-CODE-003` | Source: code repositories | Not dev | - | - |
| [x] | `G2-SRC-CODE-004` | Source: code repositories | Not dev | - | - |
| [x] | `G2-SRC-CODE-005` | Source: code repositories | Not dev | - | - |

#### WP 2.5. Crawler security (11 tasks)

**Goal.** Authentication isolation, crawl boundaries, permission-aware metadata and the crawler security family.

**Depends on.** WP 2.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [x] | `G2-SEC-CRAWL-002` | Crawler security | Complete | packages/eoip/connectors/crawler.py | tests/security/test_crawler_security.py |
| [x] | `G2-SEC-CRAWL-003` | Crawler security | Complete | packages/eoip/connectors/crawler.py | tests/security/test_crawler_security.py |
| [x] | `G2-SEC-CRAWL-004` | Crawler security | Complete | packages/eoip/connectors/crawler.py | tests/security/test_crawler_security.py |
| [x] | `G2-SEC-CRAWL-005` | Crawler security | Complete | packages/eoip/connectors/crawler.py | tests/security/test_crawler_security.py |
| [x] | `G2-SEC-CRAWL-006` | Crawler security | Complete | packages/eoip/connectors/crawler.py | tests/security/test_crawler_security.py |
| [x] | `G2-SEC-CRAWL-007` | Crawler security | Complete | packages/eoip/connectors/crawler.py | tests/security/test_crawler_security.py |
| [x] | `G2-SEC-CRAWL-008` | Crawler security | Complete | packages/eoip/fileparse/archives.py | tests/security/test_crawler_security.py |
| [x] | `G2-SEC-CRAWL-009` | Crawler security | Complete | packages/eoip/graph/memory_store.py | tests/security/test_crawler_security.py |
| [x] | `G2-SEC-CRAWL-010` | Crawler security | Complete | packages/eoip/connectors/crawler.py | tests/security/test_crawler_security.py |
| [x] | `G2-SEC-CRAWL-011` | Crawler security | Complete | packages/eoip/connectors/registry.py | tests/security/test_crawler_security.py |
| [x] | `G2-SEC-CRAWL-012` | Crawler security | Complete | packages/eoip/audit/sink.py | tests/security/test_crawler_security.py |


### Phase 3. Competitive differentiation and cognition

**Why now.** Wire and prove the ten capabilities no competitor combines, then complete the temporal/causal/evolution families and the governed agent contracts they rely on.

**Exit criteria.** Every task below ticked; full pytest and web build green; registry updated; OpenAPI schema resolves.

#### WP 3.1. KGR-G-011..020 wiring (Conquest Phase 2) (10 tasks)

**Goal.** Wire the ten competitive differentiators that exist as modules into CI, tenancy, agents, MCP and streaming, with tests and benchmarks.

**Depends on.** WP 1.1

- [x] `KGR-G-011` **Behavioral verification gate** (P0, about 2 sessions, src CQ)
  - Formal verification at merge gate — verification/behavioral_gate.py exists, wire to CI pipeline
- [x] `KGR-G-012` **Incremental AST re-indexer** (P0, about 2 sessions, src CQ)
  - Git-hook differential AST re-index — ingestion/incremental_indexer.py exists, add git hook + tests
- [x] `KGR-G-013` **Per-tenant named-graph isolation** (P0, about 1 session, src CQ)
  - graph/named_graph.py exists — wire to tenancy/ and add isolation boundary tests
- [ ] `KGR-G-014` **Streaming temporal agent memory** (P0, about 2 sessions, src CQ)
  - moonshot/streaming_agent_memory.py exists — integrate with agents/memory.py + dual-timeline tests
- [ ] `KGR-G-015` **LLM ontology induction + SHACL** (P0, about 2 sessions, src CQ)
  - moonshot/ontology_induction.py exists — add SHACL constraint generation + anti-drift validation
- [ ] `KGR-G-016` **HNSW vector-graph adapter** (P0, about 2 sessions, src CQ)
  - graph/vector_graph.py exists — add real HNSW index, co-located with graph store
- [ ] `KGR-G-017` **PR-level cross-repo impact triage** (P0, about 2 sessions, src CQ)
  - agents/mcp_pr_tools.py exists — add cross-repo graph traversal + MCP tool registration
- [ ] `KGR-G-018` **Parallel deep multi-hop analytics** (P0, about 1 session, src CQ)
  - analytics/parallel_multihop.py exists — test 5+ hop traversals, benchmark at scale
- [ ] `KGR-G-019` **Calibrated uncertainty protocol** (P0, about 1 session, src CQ)
  - agents/uncertainty_protocol.py exists — wire honest-abstain into MCP tool responses
- [ ] `KGR-G-020` **Real-time graph mutation streaming** (P0, about 2 sessions, src CQ)
  - streaming/mutation_stream.py exists — add WebSocket endpoint + webhook delivery

#### WP 3.2. Temporal, causal and evolution families (36 tasks)

**Goal.** Causal reasoning, graph and ontology evolution, temporal model and the graph change journal.

**Depends on.** WP 1.3

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `G2-CAUSE-002` | Causal reasoning | Not dev | - | - |
| [ ] | `G2-CAUSE-003` | Causal reasoning | Not dev | - | - |
| [ ] | `G2-CAUSE-004` | Causal reasoning | Not dev | - | - |
| [ ] | `G2-CAUSE-005` | Causal reasoning | Not dev | - | - |
| [ ] | `G2-CAUSE-006` | Causal reasoning | Not dev | - | - |
| [ ] | `G2-EVOL-002` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-003` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-004` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-005` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-006` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-007` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-008` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-009` | Graph / knowledge evolution | Partial | packages/eoip/contracts/revision.py | - |
| [ ] | `G2-EVOL-010` | Graph / knowledge evolution | Partial | - | tests/unit/test_bulk_load.py |
| [ ] | `G2-EVOL-011` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-012` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-013` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-014` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-015` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-EVOL-016` | Graph / knowledge evolution | Not dev | - | - |
| [ ] | `G2-JOURNAL-002` | Graph change journal | Not dev | - | - |
| [ ] | `G2-JOURNAL-003` | Graph change journal | Not dev | - | - |
| [ ] | `G2-JOURNAL-004` | Graph change journal | Not dev | - | - |
| [ ] | `G2-JOURNAL-005` | Graph change journal | Not dev | - | - |
| [ ] | `G2-JOURNAL-006` | Graph change journal | Not dev | - | - |
| [ ] | `G2-OEVO-002` | Ontology evolution | Not dev | - | - |
| [ ] | `G2-OEVO-003` | Ontology evolution | Not dev | - | - |
| [ ] | `G2-OEVO-004` | Ontology evolution | Not dev | - | - |
| [ ] | `G2-OEVO-005` | Ontology evolution | Not dev | - | - |
| [ ] | `G2-OEVO-006` | Ontology evolution | Not dev | - | - |
| [ ] | `G2-TIME-002` | Temporal model | Not dev | - | - |
| [ ] | `G2-TIME-003` | Temporal model | Not dev | - | - |
| [ ] | `G2-TIME-004` | Temporal model | Not dev | - | - |
| [ ] | `G2-TIME-005` | Temporal model | Not dev | - | - |
| [ ] | `G2-TIME-006` | Temporal model | Not dev | - | - |
| [ ] | `G2-TIME-007` | Temporal model | Not dev | - | - |

#### WP 3.3. Governed agents (6 tasks)

**Goal.** Agent contract, bounded runtime, TraceImpact agent, write/action approval boundary, controlled self-modification, and the useful read-only agent workflow.

**Depends on.** WP 1.4

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- FR: Backend contract verified; dedicated apps/web screen (or an external-credential mock fixture) wired; explicit test fixture tagged @pytest.mark.req("<ID>"). Audit note: "Backend logic present but missing dedicated frontend screen or external credential mock."
- MVP: Existing test annotated with @pytest.mark.req("<ID>"), acceptance criteria verified, and a new test added if none exists. Audit note: "Implemented via core services; lacks standalone explicit MVP requirement tag in test suite."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `FR-AGENT-001` | Agent contract | Not dev | - | - |
| [ ] | `FR-AGENT-002` | Bounded agent runtime | Partial | packages/eoip/loops/core.py | - |
| [ ] | `FR-AGENT-003` | TraceImpact agent | Partial | packages/eoip/agents/anomaly.py, packages/eoip/agents/blast_radius.py | - |
| [ ] | `FR-AGENT-004` | Write/action approval boundary | Not dev | - | - |
| [ ] | `FR-AGENT-005` | Controlled self-modification | Not dev | - | - |
| [ ] | `MVP-FR-021` | Useful read-only agent workflow | Not dev | - | - |


### Phase 4. Intelligence amplification

**Why now.** Federation, dual semantic model, evidence-addressable RAG, deterministic rules, truth resolution and the question-operator family make the knowledge computable and every answer auditable.

**Exit criteria.** Every task below ticked; full pytest and web build green; registry updated; OpenAPI schema resolves.

#### WP 4.1. Intelligence amplification (Conquest Phase 3) (8 tasks)

**Goal.** Federation, dual semantic model, local analytics service, evidence-addressable RAG, deterministic rules, local NLP, recommendations, unified query API.

**Depends on.** WP 3.1

- [ ] `GAP-AI` **Evidence-addressable RAG** (P1, about 2 sessions, src CQ)
  - ragx/ + retrieval/ exist — wire every answer to graph nodes, paths, and source records with citation chains
  - Related: `FR-RAG-002`, `FR-QUERY-007`
- [ ] `GAP-DUAL` **Dual semantic model (RDF/OWL ↔ property graph)** (P1, about 2 sessions, src CQ)
  - ontology/rdf.py exists — add round-trip mapping, SHACL validation, RDF export/import
  - Related: `FR-GRAPH-010`
- [ ] `GAP-FED` **Semantic federation layer** (P1, about 3 sessions, src CQ)
  - federation/planner.py exists — add JDBC/REST/file adapters, virtual vs. materialized modes, explainable query plans
  - Related: `GAP-FABRIC-002`, `GAP-FABRIC-003`, `GAP-FABRIC-004`, `GAP-FABRIC-005`, `GAP-FABRIC-006`, `GAP-FABRIC-007`, `GAP-FABRIC-008`
- [ ] `GAP-GDS` **Local graph analytics service** (P1, about 2 sessions, src CQ)
  - graph/algorithms.py + analytics/ exist — package as pluggable analytics API with all standard algorithms
- [ ] `GAP-NLP` **Local NLP pipeline** (P1, about 2 sessions, src CQ)
  - Add entity extraction, tagging, classification, concept recommendation — all local, no cloud
- [ ] `GAP-QUERY` **Unified semantic query API** (P1, about 2 sessions, src CQ)
  - query/ has 6 languages — build single routing API across Gremlin, RDF, search, vector, federated
  - Related: `GAP-QI-005`, `GAP-QI-006`, `GAP-QI-008`
- [ ] `GAP-REC` **Graph-aware recommendation engine** (P1, about 1 session, src CQ)
  - graph/similarity.py exists — extend to expert, document, component, concept recommendations
- [ ] `GAP-RULE` **Deterministic rules engine** (P1, about 2 sessions, src CQ)
  - reasoning/ exists — add versioned inference policies, fact classification (asserted/inferred/model/human), retraction/recomputation

#### WP 4.2. Federation, cache and freshness (15 tasks)

**Goal.** Source capability registry, cost-aware routing, offline degradation, graph-version-aware cache with CDC invalidation, and doc/code/ownership freshness detection.

**Depends on.** WP 4.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- GAP: REST endpoint in apps/api/extended.py, automated verification test tagged with the ID, and a web dashboard visualization. Audit note: "Core feature active in CLI/API; needs dedicated web dashboard visualization."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `GAP-CACHE-002` | Cache dependencies reference graph versions/source freshness | Partial | packages/eoip/future_scope.py | - |
| [ ] | `GAP-CACHE-003` | Invalidate using graph CDC | Partial | packages/eoip/future_scope.py | - |
| [ ] | `GAP-CACHE-004` | Separate deterministic query cache from AI response cache | Partial | packages/eoip/query/cache.py | - |
| [ ] | `GAP-CACHE-005` | Do not serve stale results beyond policy | Partial | packages/eoip/future_scope.py | - |
| [ ] | `GAP-FABRIC-002` | Source capability registry | Partial | packages/eoip/federation/planner.py, apps/api/extended.py | - |
| [ ] | `GAP-FABRIC-003` | Cost-aware query routing | Partial | packages/eoip/federation/planner.py | - |
| [ ] | `GAP-FABRIC-004` | Push filters/projections to source where possible | Partial | packages/eoip/federation/planner.py | - |
| [ ] | `GAP-FABRIC-005` | Local result cache with provenance/freshness | Partial | packages/eoip/federation/planner.py | - |
| [ ] | `GAP-FABRIC-006` | Offline degradation strategy | Partial | packages/eoip/federation/planner.py | - |
| [ ] | `GAP-FABRIC-007` | Explain query routing | Partial | packages/eoip/federation/planner.py | - |
| [ ] | `GAP-FABRIC-008` | Enforce source-level data policies | Not dev | - | - |
| [ ] | `GAP-FRESH-002` | Detect docs contradicted by code/config/runtime | Not dev | - | - |
| [ ] | `GAP-FRESH-003` | Detect ownership changes | Not dev | - | - |
| [ ] | `GAP-FRESH-004` | Detect deprecated APIs still referenced in docs | Not dev | - | - |
| [ ] | `GAP-FRESH-005` | Recommend review—not silently rewrite authoritative docs | Not dev | - | - |

#### WP 4.3. Truth resolution, query intelligence and question operators (20 tasks)

**Goal.** Claims vs canonical facts, confidence scoring, contradiction handling, human adjudication, query intelligence, and the WHY NOT / WHAT IF / WHAT CHANGED / WHEN / WHO / WHERE / HOW operators.

**Depends on.** WP 4.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."
- GAP: REST endpoint in apps/api/extended.py, automated verification test tagged with the ID, and a web dashboard visualization. Audit note: "Core feature active in CLI/API; needs dedicated web dashboard visualization."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `G2-QOP-002` | WHY NOT | Not dev | - | - |
| [ ] | `G2-QOP-003` | WHAT IF | Partial | - | tests/unit/test_gap_coverage.py |
| [ ] | `G2-QOP-004` | WHAT CHANGED | Not dev | - | - |
| [ ] | `G2-QOP-005` | WHEN | Not dev | - | - |
| [ ] | `G2-QOP-006` | WHO | Not dev | - | - |
| [ ] | `G2-QOP-007` | WHERE | Not dev | - | - |
| [ ] | `G2-QOP-008` | HOW | Not dev | - | - |
| [ ] | `G2-QOP-009` | Question operator | Not dev | - | - |
| [ ] | `GAP-QI-005` | Suggested indexes | Partial | packages/eoip/query/intelligence.py | - |
| [ ] | `GAP-QI-006` | Traversal-risk detector | Partial | packages/eoip/query/intelligence.py | - |
| [ ] | `GAP-QI-008` | Natural-language query produces editable structured plan before execution when risk is high | Partial | packages/eoip/query/intelligence.py | - |
| [ ] | `GAP-TRUTH-002` | Represent claims separately from resolved canonical facts | Not dev | - | - |
| [ ] | `GAP-TRUTH-003` | Store source authority score | Partial | apps/api/extended.py | - |
| [ ] | `GAP-TRUTH-004` | Store extraction confidence | Not dev | - | - |
| [ ] | `GAP-TRUTH-005` | Store validation confidence | Partial | apps/api/extended.py | - |
| [ ] | `GAP-TRUTH-006` | Detect contradictory claims | Partial | apps/api/extended.py | - |
| [ ] | `GAP-TRUTH-007` | Support configurable truth-resolution policy | Partial | apps/api/extended.py | - |
| [ ] | `GAP-TRUTH-008` | Permit human adjudication | Not dev | - | - |
| [ ] | `GAP-TRUTH-009` | Retain rejected/obsolete claims for history | Not dev | - | - |
| [ ] | `GAP-TRUTH-010` | Explain why a canonical fact was selected | Partial | apps/api/extended.py | - |

#### WP 4.4. G2 domain-graph and capability families (30 tasks)

**Goal.** Domain graphs (API, business, decisions, observability, process, runtime, security, test) and the CAP, KD and I2R capability families. Titles are not in the audit: read gaps2-requirements.md before implementing.

**Depends on.** WP 4.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `G2-CAP-002` | Capability family CAP | Not dev | - | - |
| [ ] | `G2-CAP-003` | Capability family CAP | Not dev | - | - |
| [ ] | `G2-CAP-004` | Capability family CAP | Not dev | - | - |
| [ ] | `G2-CAP-005` | Capability family CAP | Not dev | - | - |
| [ ] | `G2-CAP-006` | Capability family CAP | Not dev | - | - |
| [ ] | `G2-GRAPH-API-002` | Domain graph: API | Not dev | - | - |
| [ ] | `G2-GRAPH-API-003` | Domain graph: API | Not dev | - | - |
| [ ] | `G2-GRAPH-BIZ-002` | Domain graph: business | Not dev | - | - |
| [ ] | `G2-GRAPH-BIZ-003` | Domain graph: business | Not dev | - | - |
| [ ] | `G2-GRAPH-DEC-002` | Domain graph: decisions | Not dev | - | - |
| [ ] | `G2-GRAPH-DEC-003` | Domain graph: decisions | Not dev | - | - |
| [ ] | `G2-GRAPH-OBS-002` | Domain graph: observability | Not dev | - | - |
| [ ] | `G2-GRAPH-OBS-003` | Domain graph: observability | Not dev | - | - |
| [ ] | `G2-GRAPH-PROC-002` | Domain graph: process | Not dev | - | - |
| [ ] | `G2-GRAPH-PROC-003` | Domain graph: process | Not dev | - | - |
| [ ] | `G2-GRAPH-RUNTIME-002` | Domain graph: runtime | Not dev | - | - |
| [ ] | `G2-GRAPH-RUNTIME-003` | Domain graph: runtime | Not dev | - | - |
| [ ] | `G2-GRAPH-SEC-002` | Domain graph: security | Not dev | - | - |
| [ ] | `G2-GRAPH-SEC-003` | Domain graph: security | Not dev | - | - |
| [ ] | `G2-GRAPH-TEST-002` | Domain graph: test | Not dev | - | - |
| [ ] | `G2-GRAPH-TEST-003` | Domain graph: test | Not dev | - | - |
| [ ] | `G2-I2R-002` | Capability family I2R | Not dev | - | - |
| [ ] | `G2-I2R-003` | Capability family I2R | Not dev | - | - |
| [ ] | `G2-I2R-004` | Capability family I2R | Not dev | - | - |
| [ ] | `G2-I2R-005` | Capability family I2R | Not dev | - | - |
| [ ] | `G2-KD-002` | Capability family KD | Not dev | - | - |
| [ ] | `G2-KD-003` | Capability family KD | Not dev | - | - |
| [ ] | `G2-KD-004` | Capability family KD | Not dev | - | - |
| [ ] | `G2-KD-005` | Capability family KD | Not dev | - | - |
| [ ] | `G2-KD-006` | Capability family KD | Not dev | - | - |


### Phase 5. Enterprise readiness and experience

**Why now.** Governance, catalog, HA, no-code studio, web screens for the new engines, VS Code completion, ontology GitOps, marketplace and enterprise security.

**Exit criteria.** Every task below ticked; full pytest and web build green; registry updated; OpenAPI schema resolves.

#### WP 5.1. Enterprise readiness (Conquest Phase 4) (7 tasks)

**Goal.** Stewardship workflow, knowledge catalog, HA, visual ontology studio, VS Code completion, knowledge app builder, industry templates.

**Depends on.** WP 4.1

- [ ] `GAP-APP` **Knowledge app builder** (P1, about 2 sessions, src CQ)
  - dashboards/builder.py exists — compose query, table, graph, timeline, KPI panels from saved queries
- [ ] `GAP-CATALOG` **Knowledge catalog** (P1, about 2 sessions, src CQ)
  - catalog/products.py exists — add certification states, stewardship, domain collections, lineage navigation
- [ ] `GAP-GOV` **Semantic stewardship workflow** (P1, about 3 sessions, src CQ)
  - Draft → review → approve → publish → deprecate. Ontology branching, diffs, semantic merge.
  - Related: `GAP-GITOPS-002`, `GAP-GITOPS-007`
- [ ] `GAP-HA` **High availability patterns** (P1, about 2 sessions, src CQ)
  - ha.py + recovery/wal.py exist — add HugeGraph distributed mode HA, automatic failover
- [ ] `GAP-IDE` **VS Code extension completion** (P1, about 2 sessions, src CQ)
  - extension.js (690 lines) exists — add graph webview, MCP integration, inline ontology/lineage
  - Related: `FR-VSCODE-001`, `FR-VSCODE-002`, `MVP-FR-019`
- [ ] `GAP-NOCODE` **Visual ontology studio** (P1, about 3 sessions, src CQ)
  - Drag-and-drop ontology builder for non-technical users. Novice/analyst/expert modes.
- [ ] `GAP-TEMPLATE` **Industry templates** (P1, about 1 session, src CQ)
  - Packaged templates for engineering, audit, risk, incident, architecture, compliance use cases
  - Related: `GAP-MKT-003`, `GAP-MKT-006`

#### WP 5.2. Ontology GitOps and marketplace (14 tasks)

**Goal.** Ontology branch/PR/merge, semantic diffs, impact analysis, migration scripts, rollback, SemVer releases; marketplace packaging, dependencies and signing.

**Depends on.** WP 4.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- GAP: REST endpoint in apps/api/extended.py, automated verification test tagged with the ID, and a web dashboard visualization. Audit note: "Core feature active in CLI/API; needs dedicated web dashboard visualization."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `GAP-GITOPS-002` | Provide ontology branch, pull-request/review and merge workflows | Not dev | - | - |
| [ ] | `GAP-GITOPS-003` | Generate semantic diffs: | Partial | apps/api/main.py | - |
| [ ] | `GAP-GITOPS-004` | CI validates ontology before publishing | Partial | packages/eoip/ontology/gitops.py | - |
| [ ] | `GAP-GITOPS-005` | Run impact analysis for ontology changes | Not dev | - | - |
| [ ] | `GAP-GITOPS-006` | Generate migration scripts | Not dev | - | - |
| [ ] | `GAP-GITOPS-007` | Allow rollback to previous semantic version | Not dev | - | - |
| [ ] | `GAP-GITOPS-008` | Package ontology releases using SemVer-like policy | Not dev | - | - |
| [ ] | `GAP-MKT-002` | Package connector mappings | Partial | packages/eoip/marketplace/manifest.py | - |
| [ ] | `GAP-MKT-003` | Package query templates | Partial | packages/eoip/marketplace/packager.py, packages/eoip/marketplace/sample.py | - |
| [ ] | `GAP-MKT-004` | Package validation rules | Partial | packages/eoip/marketplace/installer.py, packages/eoip/marketplace/manifest.py | - |
| [ ] | `GAP-MKT-005` | Package agent workflows | Partial | packages/eoip/marketplace/installer.py, packages/eoip/marketplace/packager.py | - |
| [ ] | `GAP-MKT-006` | Package dashboards | Partial | packages/eoip/marketplace/installer.py, packages/eoip/marketplace/registry.py | - |
| [ ] | `GAP-MKT-007` | Dependency/version management | Partial | packages/eoip/marketplace/installer.py, packages/eoip/marketplace/signing.py | - |
| [ ] | `GAP-MKT-008` | Signed packages in later phases | Partial | packages/eoip/marketplace/registry.py | - |

#### WP 5.3. Web UX, admin and new-engine screens (45 tasks)

**Goal.** User web application and graph explorer, admin UIs, graph/lens/playground UX, and dashboards for blast radius, multi-paradigm query, domain packs and XAI verification.

**Depends on.** WP 1.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- FR: Backend contract verified; dedicated apps/web screen (or an external-credential mock fixture) wired; explicit test fixture tagged @pytest.mark.req("<ID>"). Audit note: "Backend logic present but missing dedicated frontend screen or external credential mock."
- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."

- [ ] `UI-01` **Dashboard: causal blast radius** (P0, src G)
  - G-dev Phase A step 3: dedicated screen in apps/web for the live causal engine (POST /api/v1/causal/live-blast-radius, /api/v1/causal/counterfactual-intervention).
- [ ] `UI-02` **Dashboard: multi-paradigm querying** (P0, src G)
  - G-dev Phase A step 3: screen for POST /api/v1/query/multi-paradigm showing the five kernels and the harmonized result.
- [ ] `UI-03` **Dashboard: domain pack activation** (P0, src G)
  - G-dev Phase A step 3: screen for GET/POST /api/v1/domain-packs/* (8 domains: bfsi, cybersecurity, healthcare, compliance, data-governance, itsm, manufacturing, software-engineering).
- [ ] `UI-04` **Dashboard: XAI factor verification** (P0, src G)
  - G-dev Phase A step 3: screen for POST /api/v1/xai/certify-decision and /api/v1/xai/verify-certificate.

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `FR-ADMIN-001` | Admin ingestion UI | Not dev | - | - |
| [ ] | `FR-ADMIN-002` | Admin graph quality UI | Not dev | - | - |
| [ ] | `FR-UI-001` | User web application | Not dev | - | - |
| [ ] | `FR-UI-002` | Graph explorer | Not dev | - | - |
| [ ] | `G2-ADMIN-002` | Admin console / admin UI capability | Partial | apps/web/src/admin/index.jsx | - |
| [ ] | `G2-ADMIN-003` | Admin console / admin UI capability | Partial | apps/web/src/admin/index.jsx | - |
| [ ] | `G2-ADMIN-004` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-005` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-006` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-007` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-008` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-009` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-010` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-011` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-012` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-013` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-014` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-015` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-016` | Admin console / admin UI capability | Not dev | - | - |
| [ ] | `G2-ADMIN-017` | Admin console / admin UI capability | Partial | - | tests/unit/test_g2_readiness.py |
| [ ] | `G2-UX-GRAPH-002` | Graph UX | Partial | apps/web/src/kgr/enhancements/enhancements.css | - |
| [ ] | `G2-UX-GRAPH-003` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-004` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-005` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-006` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-007` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-008` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-009` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-010` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-011` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-012` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-013` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-014` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-015` | Graph UX | Not dev | - | - |
| [ ] | `G2-UX-GRAPH-016` | Graph UX | Partial | - | tests/unit/test_gap_coverage.py |
| [ ] | `G2-UX-LENS-002` | Lens UX | Not dev | - | - |
| [ ] | `G2-UX-LENS-003` | Lens UX | Not dev | - | - |
| [ ] | `G2-UX-PLAY-002` | Playground UX | Not dev | - | - |
| [ ] | `G2-UX-PLAY-003` | Playground UX | Not dev | - | - |
| [ ] | `G2-UX-PLAY-004` | Playground UX | Not dev | - | - |
| [ ] | `G2-UX-PLAY-005` | Playground UX | Not dev | - | - |

#### WP 5.4. VS Code extension (10 tasks)

**Goal.** Context extension, trace/impact commands, graph webview, MCP integration, host acceptance.

**Depends on.** WP 1.4

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- FR: Backend contract verified; dedicated apps/web screen (or an external-credential mock fixture) wired; explicit test fixture tagged @pytest.mark.req("<ID>"). Audit note: "Backend logic present but missing dedicated frontend screen or external credential mock."
- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."
- MVP: Existing test annotated with @pytest.mark.req("<ID>"), acceptance criteria verified, and a new test added if none exists. Audit note: "Implemented via core services; lacks standalone explicit MVP requirement tag in test suite."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `FR-VSCODE-001` | VS Code context extension | Not dev | - | - |
| [ ] | `FR-VSCODE-002` | VS Code trace/impact commands | Not dev | - | - |
| [ ] | `G2-VSC-002` | VS Code integration | Not dev | - | - |
| [ ] | `G2-VSC-003` | VS Code integration | Not dev | - | - |
| [ ] | `G2-VSC-004` | VS Code integration | Not dev | - | - |
| [ ] | `G2-VSC-005` | VS Code integration | Not dev | - | - |
| [ ] | `G2-VSC-006` | VS Code integration | Not dev | - | - |
| [ ] | `G2-VSC-007` | VS Code integration | Not dev | - | - |
| [ ] | `G2-VSC-008` | VS Code integration | Not dev | - | - |
| [ ] | `MVP-FR-019` | VS Code extension | Not dev | - | - |

#### WP 5.5. Enterprise security (5 tasks)

**Goal.** Close GAP-SEC-008..012 (token scopes and the reserved enterprise-security set).

**Depends on.** WP 1.5

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- GAP: REST endpoint in apps/api/extended.py, automated verification test tagged with the ID, and a web dashboard visualization. Audit note: "Core feature active in CLI/API; needs dedicated web dashboard visualization."

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `GAP-SEC-008` | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | Partial | packages/eoip/authz/tokens.py | - |
| [ ] | `GAP-SEC-009` | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | Partial | packages/eoip/authz/tokens.py | - |
| [ ] | `GAP-SEC-010` | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | Not dev | - | - |
| [ ] | `GAP-SEC-011` | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | Not dev | - | - |
| [ ] | `GAP-SEC-012` | GAP-SEC-001 through GAP-SEC-012 reserved for enterprise security implementation | Partial | - | tests/unit/test_gap_coverage.py |


### Phase 6. Moonshots and trust

**Why now.** Category-defining features: collaboration, plugin ecosystem, process intelligence, memory immune system, health sentinel, white-label and metering, then frontier research items.

**Exit criteria.** Every task below ticked; full pytest and web build green; registry updated; OpenAPI schema resolves.

#### WP 6.1. Platform and ecosystem moonshots (14 tasks)

**Goal.** Marketplace, collaborative studio, graph-as-code, process intelligence, A2A orchestration, domain packs, white-label and metering.

**Depends on.** WP 5.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."
- MS: Standalone service or UI canvas module, unit tests in tests/unit/, API surface, and brain_os telemetry. Audit note: "Moonshot feature not fully productized in frontend/cloud distribution."

- [ ] `MS-6` **Diamond moonshot baseline #6** (P1, src G, audit Not dev)
  - Only a placeholder title exists in the audit. Read diamond-moonshots-advanced.md for the real definition (see DEC-07).
- [ ] `MS-7` **Diamond moonshot baseline #7** (P1, src G, audit Not dev)
  - Only a placeholder title exists in the audit. Read diamond-moonshots-advanced.md for the real definition (see DEC-07).
- [ ] `MS-11` **Plugin marketplace** (P1, about 2 sessions, src G+CQ, audit Not dev)
  - Conquest: marketplace/ exists (8 modules); add discovery UI, install/update flow, sandboxed execution. G-dev Phase B: WASM / Python sandbox plugin loader with capability manifest audits.
- [ ] `MS-12` **Live collaborative graph studio** (P1, about 3 sessions, src G+CQ, audit Not dev)
  - Conquest: real-time multi-user graph editing via CRDT/OT ("Figma for knowledge graphs"). G-dev Phase B: multi-user CRDT synchronization for concurrent graph editing (G-dev Phase B labels this item MS-13; the table title and the Conquest plan say MS-12, which is used here).
- [ ] `MS-13` **Graph-as-code and GitOps for ontology, data and policy** (P1, about 2 sessions, src G+CQ, audit Not dev)
  - Conquest: ontology/gitops.py exists; add CLI, git hooks, PR-based ontology evolution. G-dev Phase B: automated PR diff generation for ontology and bitemporal schema mutations (labelled MS-12 in G-dev Phase B text; table title wins).
- [ ] `MS-16` **Agentic process intelligence and digital process twin** (P1, src G, audit Not dev)
  - G-dev Phase B: event-log ingestion (XES / OCEL) and Petri net / BPMN graph induction ("Enterprise Process Mining Loop").
- [ ] `MS-17` **Multi-agent A2A + MCP orchestration** (P2, about 3 sessions, src CQ)
  - Conquest: agents/mesh_supervisor.py + orchestration.py exist — add cross-agent coordination with graph grounding. The G-dev audit does not list this MS item as a gap (it counts it as developed), so first VERIFY what exists, then close whatever the Conquest text still requires.
- [ ] `MS-25` **Industry domain packs** (P2, about 2 sessions, src CQ)
  - Conquest: ontology/packs.py exists — build Financial Services, Healthcare, Software Eng verticals. The G-dev audit does not list this MS item as a gap (it counts it as developed), so first VERIFY what exists, then close whatever the Conquest text still requires.
- [ ] `MS-26` **White-label partner ecosystem and OEM framework** (P2, src G, audit Not dev)
  - G-dev Phase C: tenant-scoped CSS themes, custom logos, isolated graph namespaces ("Multi-Tenant White-Label Engine").
- [ ] `MS-27` **Usage intelligence and embedded billing metering engine** (P2, src G, audit Not dev)
  - G-dev Phase C: query token accounting, API rate limits, billing ledger integration.

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `G2-PM-002` | Process mining | Not dev | - | - |
| [ ] | `G2-PM-003` | Process mining | Not dev | - | - |
| [ ] | `G2-PM-004` | Process mining | Not dev | - | - |
| [ ] | `G2-PM-005` | Process mining | Not dev | - | - |

#### WP 6.2. Trust, health and frontier moonshots (31 tasks)

**Goal.** Memory immune system, KG integrity sentinel, health dashboard, living twin, simulation, and frontier items (LOM fine-tuning, federated learning, quantum-inspired optimization, graph foundation model, predictive radar).

**Depends on.** WP 5.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."
- MS: Standalone service or UI canvas module, unit tests in tests/unit/, API surface, and brain_os telemetry. Audit note: "Moonshot feature not fully productized in frontend/cloud distribution."

- [ ] `MS-15` **Enterprise Large Ontology Model (LOM) fine-tuning runtime** (P1, src G, audit Not dev)
  - No implementation detail in the sources. Read diamond-moonshots-advanced.md for the contract. Local-first: must run without cloud.
- [ ] `MS-18` **Federated cross-organizational privacy-preserving graph learning** (P1, src G, audit Not dev)
  - No implementation detail in the sources. Read diamond-moonshots-advanced.md. Must respect the no-egress NFR (NFR-SEC-001).
- [ ] `MS-19` **Agent memory immune system (AMIS)** (P1, about 2 sessions, src G+CQ, audit Not dev)
  - Conquest: OWASP ASI06 defense against memory poisoning: input sanitization, anomaly detection, quarantine. Related family: G2-IMMUNE.
- [ ] `MS-21` **KG integrity sentinel** (P2, about 2 sessions, src CQ)
  - Conquest: Oracle poisoning defense — mutation validation, provenance verification, rollback. The G-dev audit does not list this MS item as a gap (it counts it as developed), so first VERIFY what exists, then close whatever the Conquest text still requires.
- [ ] `MS-22` **Quantum-inspired graph optimization engine** (P2, src G, audit Not dev)
  - No implementation detail in the sources. Classical quantum-inspired heuristics (e.g. simulated annealing / QUBO-style) on local hardware; define acceptance criteria first (see DEC-09).
- [ ] `MS-23` **Living operational digital twin** (P2, about 2 sessions, src CQ)
  - Conquest: graph/twin.py + moonshot/compliance_twin.py exist — add real-time operational mirror. The G-dev audit does not list this MS item as a gap (it counts it as developed), so first VERIFY what exists, then close whatever the Conquest text still requires.
- [ ] `MS-24` **Continuous graph health intelligence dashboard** (P2, about 2 sessions, src G+CQ, audit Not dev)
  - Conquest: quality/engine.py + health/ exist; add continuous monitoring UI with alerts. G-dev Phase C: "Autonomous Graph Health Sentinel" with automatic index rebalancing, orphan vertex garbage collection, storage compaction.
- [ ] `MS-29` **Graph-native foundation model runtime** (P3, src G, audit Not dev)
  - G-dev Phase D: train GNN node/edge embeddings for zero-shot link prediction across cross-domain graphs.
- [ ] `MS-30` **Strategic intelligence and predictive radar** (P3, src G)
  - G-dev Phase D: expand predictive analytics with industry macro-economic indicators and geopolitical risk graphs. Not in the G-dev gap table (counted developed there), so VERIFY first, then expand.

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `G2-IMMUNE-002` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-003` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-004` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-005` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-006` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-007` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-008` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-009` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-010` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-011` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-012` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-IMMUNE-013` | Graph / agent immune system | Not dev | - | - |
| [ ] | `G2-SIM-002` | Simulation | Not dev | - | - |
| [ ] | `G2-SIM-003` | Simulation | Not dev | - | - |
| [ ] | `G2-SIM-004` | Simulation | Not dev | - | - |
| [ ] | `G2-SIM-005` | Simulation | Not dev | - | - |
| [ ] | `G2-SIM-006` | Simulation | Not dev | - | - |
| [ ] | `G2-SIM-007` | Simulation | Not dev | - | - |
| [ ] | `G2-TWIN-002` | Digital twin | Not dev | - | - |
| [ ] | `G2-TWIN-003` | Digital twin | Not dev | - | - |
| [ ] | `G2-TWIN-004` | Digital twin | Not dev | - | - |
| [ ] | `G2-TWIN-005` | Digital twin | Not dev | - | - |


### Phase 7. Scale, reliability and polish

**Why now.** Make it fast, observable, recoverable and documented: WebGL rendering, benchmarks at scale, CI/CD, developer docs, security hardening, and the NFR/MVP operational requirements.

**Exit criteria.** Every task below ticked; full pytest and web build green; registry updated; OpenAPI schema resolves.

#### WP 7.1. Scale and polish (Conquest Phase 6) (5 tasks)

**Goal.** WebGL graph rendering, benchmarks at 50K+ nodes, CI/CD, developer documentation, security hardening.

**Depends on.** WP 5.3

- [ ] `S-01` **Frontend KGR completion** (P3, about 4 sessions, src CQ)
  - 55 JSX components exist — add WebGL large-graph rendering, Web Worker layouts, visual query builder
  - Related: `G2-UX-GRAPH-002`
- [ ] `S-02` **Performance benchmarks** (P3, about 2 sessions, src CQ)
  - graph/benchmark.py exists — add load testing at 50K+ nodes, query latency baselines, memory profiling
  - Related: `NFR-PERF-001`, `PERF-01`
- [ ] `S-03` **CI/CD pipeline** (P3, about 1 session, src CQ)
  - ci/pipeline.py exists — add GitHub Actions/GitLab CI, automated test + lint + build + deploy
- [ ] `S-04` **Developer documentation** (P3, about 2 sessions, src CQ)
  - API docs via Swagger UI, architecture guides, getting-started tutorial, contribution guide
- [ ] `S-05` **Security hardening** (P3, about 1 session, src CQ)
  - 4 security test files exist — add OWASP top 10 audit, dependency scanning, secrets detection
  - Related: `NFR-SEC-001`, `NFR-SEC-002`, `NFR-SEC-003`, `NFR-SEC-004`, `NFR-SEC-006`

#### WP 7.2. Performance, reliability, SLO, telemetry and operations (35 tasks)

**Goal.** NFR benchmark suite, SLOs, telemetry, logging, metrics, backup/restore, restart safety.

**Depends on.** WP 1.1

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- G2: Dedicated live-connector endpoint or offline fixture mode for CI, plus an end-to-end integration test matching the G2 contract and tagged with the ID. Live-credential run is recorded in Phase 8. Audit note: "Requires live enterprise crawler connector or distributed Kubernetes cluster deployment."
- MVP: Existing test annotated with @pytest.mark.req("<ID>"), acceptance criteria verified, and a new test added if none exists. Audit note: "Implemented via core services; lacks standalone explicit MVP requirement tag in test suite."
- NFR: Measured threshold recorded: tests/benchmark/ (Locust or pytest-benchmark) for PERF/OPS/REL, tests/security/ for SEC/PRIV. Note: the audit text prescribes a load benchmark for every NFR; for security NFRs the correct evidence is a security test. Audit note: "Non-functional constraint active; requires formal 10,000 qps load benchmark harness."

- [ ] `PERF-01` **Formal NFR benchmark suite (Locust / pytest-benchmark)** (P2, src G)
  - G-dev Phase C step 1: sub-50 ms query latency under 10,000 concurrent requests in tests/benchmark/. Conflicts with the Conquest KPI (p95 < 200 ms at 50K nodes): keep both measurements, confirm the target against 04-non-functional-requirements.md (DEC-08).
  - Related: `NFR-PERF-001`, `S-02`

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `G2-PERF-002` | Performance | Not dev | - | - |
| [ ] | `G2-PERF-003` | Performance | Not dev | - | - |
| [ ] | `G2-PERF-004` | Performance | Not dev | - | - |
| [ ] | `G2-PERF-005` | Performance | Not dev | - | - |
| [ ] | `G2-PERF-006` | Performance | Not dev | - | - |
| [ ] | `G2-PERF-007` | Performance | Not dev | - | - |
| [ ] | `G2-PERF-008` | Performance | Not dev | - | - |
| [ ] | `G2-REL-002` | Reliability | Not dev | - | - |
| [ ] | `G2-REL-003` | Reliability | Not dev | - | - |
| [ ] | `G2-REL-004` | Reliability | Not dev | - | - |
| [ ] | `G2-REL-005` | Reliability | Partial | - | tests/unit/test_graph_evolution.py |
| [ ] | `G2-REL-006` | Reliability | Not dev | - | - |
| [ ] | `G2-REL-007` | Reliability | Partial | - | tests/unit/test_operational_recovery.py, tests/unit/test_recovery_bundle.py |
| [ ] | `G2-REL-008` | Reliability | Not dev | - | - |
| [ ] | `G2-SLO-002` | Service-level objectives | Not dev | - | - |
| [ ] | `G2-SLO-003` | Service-level objectives | Not dev | - | - |
| [ ] | `G2-SLO-004` | Service-level objectives | Not dev | - | - |
| [ ] | `G2-SLO-005` | Service-level objectives | Not dev | - | - |
| [ ] | `G2-TEL-002` | Telemetry | Not dev | - | - |
| [ ] | `G2-TEL-003` | Telemetry | Not dev | - | - |
| [ ] | `G2-TEL-004` | Telemetry | Not dev | - | - |
| [ ] | `G2-TEL-005` | Telemetry | Not dev | - | - |
| [ ] | `G2-TEL-006` | Telemetry | Not dev | - | - |
| [ ] | `G2-TEL-007` | Telemetry | Not dev | - | - |
| [ ] | `G2-TEL-008` | Telemetry | Not dev | - | - |
| [ ] | `MVP-FR-023` | Logging | Not dev | - | - |
| [ ] | `MVP-FR-024` | Metrics | Not dev | - | - |
| [ ] | `MVP-FR-025` | Backup | Not dev | - | - |
| [ ] | `MVP-FR-026` | Restore | Not dev | - | - |
| [ ] | `NFR-OPS-001` | Structured logging and health | Partial | packages/eoip/audit/redaction.py, packages/eoip/audit/sink.py | - |
| [ ] | `NFR-OPS-002` | Local metrics | Not dev | - | - |
| [ ] | `NFR-PERF-001` | Benchmark-defined objectives | Partial | - | tests/performance/test_benchmarks.py, tests/performance/test_benchmark_publication.py |
| [ ] | `NFR-REL-001` | Restart-safe processing | Partial | - | tests/e2e/test_restart_safe.py |
| [ ] | `NFR-REL-002` | Backup and restore | Partial | - | tests/unit/test_graph_evolution.py, tests/unit/test_operational_recovery.py |


### Phase 8. Production release gate

**Why now.** No production claim without fresh receipts: live connectors, Hubble runtime, browser E2E, VS Code host, HA/DR, security and performance evidence on the exact final working tree.

**Exit criteria.** Every task below ticked; full pytest and web build green; registry updated; OpenAPI schema resolves.

#### WP 8.1. Production release gate (17 tasks)

**Goal.** Release checklist and fresh receipts from live infrastructure on the exact final working tree.

**Depends on.** WP 0.1, 1.1, 2.3, 5.3, 7.1, 7.2

**Family evidence and audit note** (the audit note is family-level template text, see C7):

- MVP: Existing test annotated with @pytest.mark.req("<ID>"), acceptance criteria verified, and a new test added if none exists. Audit note: "Implemented via core services; lacks standalone explicit MVP requirement tag in test suite."

- [ ] `CG-GAP-008` **Live and external acceptance receipts (delivered in Phase 8)** (P1, src CG)
  - Status: External/live acceptance not proven. Gap: Full Python suite and web build pass, but live Hubble, real external connectors, production HA, browser E2E and VS Code extension-host acceptance were not rerun. Evidence: The audit ran local regression/build/gates only. Closure: Add a release checklist that requires live infra/profile receipts before production-release claims. Implemented as REL-01 (checklist) and REL-06..REL-12 (receipts).
  - Related: `REL-01`, `REL-06`, `REL-07`, `REL-08`, `REL-09`, `REL-10`, `REL-11`, `REL-12`
- [ ] `REL-01` **Author the release checklist that requires live receipts** (P0, src CG+CQ+ADD)
  - CG-GAP-008: no production-release claim without live infra/profile receipts. Create docs/release-checklist.md listing each receipt (command, environment, date, commit SHA, result location).
- [ ] `REL-02` **Full regression green on the final tree** (P0, src CG+CQ+ADD)
  - python -m pytest with 0 failures (baseline: 2,843 passed, 34 skipped, 2 warnings) and npm run build passes (baseline: 167 modules, 8.35s). Conquest KPI: 3,500+ tests passing.
- [ ] `REL-03` **GAP and G2 P0 coverage gates pass** (P0, src CG+CQ+ADD)
  - python -m scripts.gap_coverage ... --fail-on-gate --gate-priority P0 for the default set (296/296) and --doc-set g2 (364/364).
- [x] `REL-04` **Product capability scanner first-choice gate passes** (P0, src CG+CQ+ADD)
  - Baseline score 0.9857 with the gate failing only on PIC-002. After CG-GAP-001/002 the gate must pass and PIC-002 and PIC-010 must be advanced-ready. (CG closure plan step 3.)
  - Related: `CG-GAP-001`, `CG-GAP-002`
- [ ] `REL-05` **Documentation audit re-run and regenerated** (P0, src CG+CQ+ADD)
  - Re-run python -m scripts.documentation_audit --project-root .; every candidate record triaged (none left unreviewed); regenerate EOIP-engg-doc-pkg/audits/generated/*. Update the master status doc with the passing gates.
  - Related: `CG-GAP-004`
- [ ] `REL-06` **Live connector acceptance with real credentials** (P0, src CG+CQ+ADD)
  - Jira, GitLab, GitHub, Confluence and ServiceNow against real tenants; record receipts (CG-GAP-008, closure plan step 8). Needs DEC-06.
  - Related: `CONN-01`, `CONN-02`, `CONN-03`
- [ ] `REL-07` **Live Hubble/runtime validation, including source-bound code graph** (P0, src CG+CQ+ADD)
  - Run the Hubble/runtime profile on this exact working tree; include source-bound code-graph acceptance (the CG audit marks it "needs release evidence").
- [ ] `REL-08` **Browser-level web E2E after the Vite build** (P0, src CG+CQ+ADD)
  - End-to-end tests (e.g. Playwright) over the production bundle covering graph explorer, admin, KGR panels, report export and the new engine dashboards (UI-01..04).
  - Related: `UI-01`, `UI-02`, `UI-03`, `UI-04`
- [ ] `REL-09` **VS Code extension-host verification against the current backend** (P0, src CG+CQ+ADD)
  - Run the extension in a real extension host (apps/vscode-extension) against the final API/MCP; capture the demo-driver run.
  - Related: `GAP-IDE`, `MVP-FR-019`
- [ ] `REL-10` **Production HA, backup/restore and disaster-recovery receipts** (P0, src CG+CQ+ADD)
  - In a real deployed environment: HugeGraph distributed-mode HA failover, backup and restore drill, restart-safe processing, DR runbook execution. Covers GAP-HA, NFR-REL-001/002, MVP-FR-025/026. Needs DEC-06.
  - Related: `GAP-HA`, `MVP-FR-025`, `MVP-FR-026`, `NFR-REL-001`, `NFR-REL-002`
- [ ] `REL-11` **Security certification receipts** (P0, src CG+CQ+ADD)
  - OWASP Top 10 audit, dependency scanning (0 critical CVEs), secrets detection, container hardening, no-egress proof, prompt/tool-injection tests. Covers S-05 and NFR-SEC-*.
  - Related: `S-05`
- [ ] `REL-12` **Performance benchmark receipts** (P0, src CG+CQ+ADD)
  - p95 query latency < 200 ms at 50K nodes (Conquest KPI) and the NFR concurrency benchmark from PERF-01; memory profile; publish via the existing benchmark-publication test.
  - Related: `NFR-PERF-001`, `PERF-01`, `S-02`
- [ ] `REL-13` **Link-check pass on all non-historical docs** (P0, src CG+CQ+ADD)
  - Zero broken local links (CG-GAP-005 re-run on the final docs).
  - Related: `CG-GAP-005`
- [ ] `REL-14` **End-to-end demo on the final build** (P0, src CG+CQ+ADD)
  - MVP-FR-028: run the demo flow (tests/e2e/test_demo_flow.py plus the VS Code demo driver) on the release candidate.
  - Related: `MVP-FR-028`
- [ ] `REL-15` **Close-out re-audit, registry reconciliation and release tag** (P0, src CG+CQ+ADD)
  - Registry shows 826/826 audited requirements closed with evidence; no open Plan/CG tasks; regenerate current-gap-report and update available-status.md / todo-status.md; tag the release candidate.

| Done | ID | Requirement | Audit | Code found | Test found |
|:---:|---|---|---|---|---|
| [ ] | `MVP-FR-028` | End-to-end demo | Partial | - | tests/e2e/test_demo_flow.py |


## 7. Exit gates

| Gate | Now | Target | Source |
|---|---|---|---|
| K-01 Python tests passing | 2,843 passed, 34 skipped, 0 failures | 3,500+ passing, 0 failures | CG baseline; Conquest KPI |
| K-02 Deployed API routes with auth and integration tests | 502 routes exist; auth+integration coverage not measured | 100% of deployed routes covered | Conquest KPI (200+) tightened to all routes, see C4 |
| K-03 Hardcoded or mocked confidence values | not measured | 0 | Conquest KPI |
| K-04 p95 query latency at 50K nodes | not measured | < 200 ms | Conquest KPI |
| K-05 Query latency under 10,000 concurrent requests | not measured | < 50 ms (confirm via DEC-08) | G-dev Phase C |
| K-06 KGR-G requirements implemented | 27/27 per G-dev (Conquest tracks 011..020 wiring) | All KGR-G wired, tested, CI-gated (Conquest KPI: 20/20) | Conquest KPI; G-dev |
| K-07 OpenAPI schema resolves cleanly | not measured | 100% | Conquest KPI |
| K-08 Critical CVEs in dependencies | not measured | 0 | Conquest KPI |
| K-09 Search modalities with real embeddings | hash pseudo-embeddings in places | 7/7 | Conquest KPI |
| K-10 GAP P0 coverage gate | 296/296, passed | stays passed | CG baseline |
| K-11 G2 P0 coverage gate | 364/364, passed | stays passed | CG baseline |
| K-12 Product capability scanner | 0.9857; first-choice gate failed on PIC-002 | Gate passes; PIC-002 and PIC-010 advanced-ready | CG baseline |
| K-13 Web build | Vite build passes (167 modules, 8.35 s) | passes | CG baseline |
| K-14 Documentation-audit records triaged | 0 of 1,639 triaged (440 Partial, 1,199 Missing) | All triaged; true gaps converted to tasks | CG baseline |
| K-15 Broken links in non-historical docs | known stale links | 0 | CG-GAP-005 |

## 8. Traceability: where every source item landed

### 8.1 Counts

| Source | Items | Where |
|---|---:|---|
| G-dev gap rows | 434 | MS 14, G2 298, FR 53, GAP 46, MVP 10, NFR 13, spread over WP 0.1 to 8.1 |
| G-dev roadmap section 4 | 13 steps | BASE-02/03, CONN-01..03, UI-01..04, MS-11/12/13/16, MS-24/26/27, PERF-01, MS-29, MS-30 |
| G-dev verified capabilities (sections 2.1 to 2.3) | 14 clusters | Section 3 "Already built" |
| CG-dev gaps CG-GAP-001..009 | 9 | WP 0.2, 1.2, 8.1 |
| CG-dev code-graph findings | 5 | CG-CODE-01, CG-CODE-02, WP 2.4, REL-07 |
| CG-dev "not yet closed" list | 10 | see 8.2 |
| CG-dev closure plan | 8 steps | see 8.2 |
| CG-dev documentation policy | 7 live docs | CG-DOC-01 |
| Conquest deliverables | 47 | 42 as their own tasks; MS-11, MS-12, MS-13, MS-19, MS-24 merged into the matching G-dev MS rows |
| Conquest KPIs | 8 | K-01..K-09 |
| Conquest principles and workflow | 6 + 4 | Section 4 |
| Tasks in this file | 516 | 434 audited requirement rows, 42 Plan, 12 CG, 9 roadmap, 4 baseline, 15 release |

### 8.2 CG closure plan and open list

| CG item | Task |
|---|---|
| Closure 1: mount or document the loops catalog route | CG-GAP-001 |
| Closure 2: reports root route or scanner change | CG-GAP-002 |
| Closure 3: re-run scanner, first-choice gate passes | REL-04 |
| Closure 4: link checker on non-historical docs | CG-GAP-005, REL-13 |
| Closure 5: triage 1,199 Missing records | CG-GAP-004 |
| Closure 6: web docs to Vite/React | CG-GAP-007 |
| Closure 7: implement or retire apps/console | CG-GAP-006, DEC-01 |
| Closure 8: live connector, Hubble, browser E2E, VS Code receipts | REL-06, REL-07, REL-08, REL-09 |
| Open: PIC-002 governed autonomous agent runtime | CG-GAP-001 |
| Open: PIC-010 role-based experience and executive reporting | CG-GAP-002 |
| Open: 1,199 unmapped records | CG-GAP-004 |
| Open: historical claims needing semantic review | CG-GAP-003, CG-GAP-004 |
| Open: live connector acceptance | REL-06 |
| Open: live Hubble/runtime receipts for this tree | REL-07 |
| Open: browser-level web E2E | REL-08 |
| Open: VS Code extension host verification | REL-09 |
| Open: production HA, backup/restore, DR, security certification | REL-10, REL-11 |
| Open: link-check cleanup | CG-GAP-005, REL-13 |

### 8.3 Self-check the agent should run after any edit to this file

```python
import re, sys
text = open("KGF-MASTER-BACKLOG.md", encoding="utf-8").read()
ids = re.findall(r"^(?:- |\| )\[[ x~!]\] (?:\| )?`([A-Za-z0-9.\-]+)`", text, re.M)
assert len(ids) == len(set(ids)), "duplicate task rows"
assert len(ids) == 516, "expected 516 tasks, found %d" % len(ids)
print("ok", len(ids), "tasks;", sum(1 for _ in re.finditer(r"\[x\]", text)), "ticked")
```

---
End of backlog. Generated 2026-10-11 from the three source files; update this file, not the sources.
