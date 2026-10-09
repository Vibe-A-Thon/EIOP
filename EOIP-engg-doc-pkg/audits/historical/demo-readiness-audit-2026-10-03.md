# EOIP enterprise demo-readiness audit

**Audit date:** 2026-10-03  
**Scope:** all Markdown specifications and guidance plus the executable API, worker, graph, ingestion, connector, web, VS Code, MCP, deployment, schema, test, and example surfaces in this repository.  
**Purpose:** establish a defensible sales-demo boundary and supply a connected corpus that exercises the implemented application rather than relying on disconnected mock screens.

## Audit inventory and method

### Current enterprise remediation progress

The current canonical Northstar pack is **1.2.0: 13 scenarios, 80 entities,
134 relationships**, plus eight shared multi-step capability journeys.
The persistent corpus contains **85 current Documents and 1,144 chunks**.
These synthetic source/corpus counts are distinct from total retained graph
counts and from verified product-requirement completion.

The pre-what-if-fix complete regression passed **1,880 tests, 0 failed, 22 skipped
(exit 0)** in 1,316.21 seconds, replacing both the earlier twelve-failure
baseline and the later 1,874/1/22 checkpoint. The marketplace test's invalid
capability and stale nested-manifest assertions were corrected; the combined
query/schema/API/metrics suite passed **62 tests (exit 0)**. Audit reporting
changed during the full run and separately passed 14 focused tests (exit 0).

SEARCH now uses bounded Gremlin property projection and full selected-node
hydration, retaining the original five-second budget. Real persisted-graph
measurements were 3.450 seconds cold and 1.722/1.716 seconds warm. Administration
validation avoids repeated endpoint reads, and EOIP metrics no longer disappear
behind the HTTP metrics route. The actual administration rehearsal completed
42 steps (exit 0); coverage is still PARTIAL, not certification of every API.
Ingestion demonstrations reject nested failure receipts and incomplete batches.

The fresh live source-extension rehearsal passed all **17 steps (exit 0)**:
six NLQ intents and eleven MCP tools against the persisted graph. The earlier
post-rebuild SEARCH timeout is retained as a failure receipt; a passing rerun
does not establish a cold-start SLO. All six services are healthy and the
enterprise explorer returns HTTP 200. The actual application rehearsal
passed 166 steps, then failed its what-if request at the unchanged 120-second
timeout (exit 1). Removal now partitions the remaining neighbor components
once instead of repeating pairwise traversal; exact split-count, repeated-read,
freshness and no-mutation regression tests are included. The what-if/metrics
suite passed 22 tests (exit 0), with scoped Ruff clean. The deployed PAY-142
simulation returned HTTP 200 in 15.903 seconds. The post-fix application
rehearsal completed all 183 steps without failure (exit 0); operation coverage
remains PARTIAL. Post-fix full regression passed 1,883 tests with 22 skips and
zero failures (exit 0, 1,258.37 seconds). Audit receipt reporting changed during
that run and independently passed 14 tests (exit 0). Pipeline rehearsal then
failed after 187 passing steps: code-graph ingestion returned 53 structured
endpoint errors (exit 1). The failure receipt is preserved. Code exports now
have typed, repository-scoped facts and explicitly declared runtime dependencies;
inline forward references are deferred until all entities exist. Original source
edges and evidence are retained with their normalized ontology relationships.
The manual export's formerly silent omission is covered by a regression test.
Focused importer/API/audit tests passed 59 tests (exit 0), with scoped Ruff clean.
Application services were rebuilt/recreated successfully (exit 0); all six
services are healthy and API/web/enterprise explorer return HTTP 200.
Live manual/pipeline code acceptance passed two tests (exit 0), including
authentication refusal, exact ingestion counts, typed Hubble read-back and
source-edge replay identity. Initial test-query errors remain recorded; the
passing checks use bounded adjacency and physical HugeGraph edge labels.
The demo now refuses incomplete code facts/relationships; 19 Node tests passed
(exit 0). No graph volume was reset or deleted.
Post-importer full regression passed 1,897 tests with 24 skips, no failures
(exit 0, 1,467.13 seconds). The two added opt-in live cases have their separate
passing receipt; only their query implementation changed during that full run,
not production Python source.
Fresh deployed pipeline rehearsal passed **213 steps, zero failures, exit 0**,
including complete typed code-export and batch-ingestion acceptance. Coverage
remains **PARTIAL: 66 of 271 operations demonstrated, 205 not demonstrated**.
The corpus refresh loaded two changed assets and retained 83; its unchanged
rerun loaded zero and retained all 85. Both commands exited 0. The complete
2,474-vertex/6,897-edge physical identity sets remained exactly unchanged
on that rerun. All current corpus Documents/chunks were then verified through
Hubble (one live test passed, exit 0).
Passing local regression is not
remote CI evidence or proof that every documentation requirement is completed.
See [the runtime evidence](hubble-runtime-validation.md) for current and
historical measurements. The inventory and 2026-10-04 receipts below are
historical snapshots, not current execution counts.

The repository contains 138 Markdown files and 21,702 physical lines after adding the Northstar wiki and package guidance. The inventory comprises 117 engineering-package files, 14 operational/audit files under `docs/`, one application README, four example READMEs, and two root/other guides. The review covered every file heading and body, extracted requirement/status language, and reconciled claims against code, routes, tests, schemas, fixtures, deployment definitions, and runtime loaders.

The documentation corpus references 28 unique `MVP-FR-*` identifiers, 83 unique `FR-*` identifiers, 19 `NFR-*` identifiers, 364 `G2-*` identifiers, 16 `FR-KGR-*` identifiers, and 82 implementation work packages. Counts overlap where specialized identifiers are also matched by a broader family; they describe documentation scope, not completion percentages.

The refreshed executable inventory contains 137 FastAPI route declarations, 860 Python test functions, five Playwright scenarios, 29 connector modules, 62 ontology vertex labels, and 56 relationship labels. Parameterization explains why the current JUnit receipt contains more outcomes than Python test-function definitions. Code existence was not treated as proof of a live external integration or non-functional certification.

## Executive finding

The implementation has a strong Phase 1/MVP and KGR analytics surface, but the previous automatic demo corpus exercised only Jira, Git/code, one merge request, one pipeline, and repository documentation. That undersold the implemented ontology and made several UI/graph lenses appear sparse even though backend capability existed.

This audit closes the data/readiness gap with an auto-loaded Northstar Commerce digital thread:

- 13 audience-specific scenarios;
- 80 curated cross-domain entities and 134 curated relationships;
- representative Jira, GitLab, Confluence, ServiceNow, Grafana/Datadog/Kibana, qTest, Figma, and API portal JSON;
- runnable project code and tests, an OpenAPI contract, architecture wiki page, and incident runbook;
- immutable raw capture, normalized mutation ingestion, domain membership, ingestion lineage, and deterministic edge identity;
- a live `/api/v1/demo/scenarios` readiness endpoint that verifies every advertised scenario entity exists.

Combined with the original fixture, the in-memory acceptance graph contains approximately 149 vertices and 456 relationships. Validation reports zero errors and zero warnings; evidence coverage and provenance coverage are both 1.0.

## Capability reconciliation

| Area | Executable evidence | Demo disposition |
|---|---|---|
| Enterprise graph foundation | HugeGraph store, ontology manifest, schema bootstrap, canonical mutation boundary | Live and populated across all logical business domains used by the current ontology. |
| Work/portfolio | Jira project/work items plus Rally-style epic, feature and story entities | PAY-142 traces from business intent to delivery and runtime. |
| Code and API graph | Repository/code parser, symbols, dependencies, API services/endpoints/connections | Checkout-to-risk/payment blast-radius story is populated. |
| CI/CD and release | Commits, MR, tag, pipeline, jobs, artifact, release and deployment | Release 2026.10.1 has a complete governed path. |
| Test intelligence | qTest connector vocabulary, suites, cases, cycle and run | Requirement, symbol and endpoint coverage paths are populated. |
| Design graph | Figma connector vocabulary and design file/page/component | Design-to-feature/story paths are populated. |
| Operations/observability | ServiceNow, Grafana, Datadog and Kibana connector vocabulary | Incident, alert, log, dashboard, deployment and change correlation is populated. |
| Knowledge/RAG | Documents, sections, KB article, product page, GraphRAG retrieval | Architecture and runbook answers have graph lineage and evidence. |
| KGR analytics | Blast radius, centrality, communities, paths, similarity, link prediction, k-core, components, what-if, anomalies and diff endpoints | The denser cross-domain subgraph gives each implemented analytic a meaningful demo target. |
| Agents/MCP/VS Code | Governed agent runtime, read-only MCP tools, eight VS Code commands | The Northstar PAY-142 source-extension journey passed all six NLQ intents and eleven MCP tools against the live graph. Packaged VSIX acceptance remains separate. |
| Security/operations | bearer boundary, audit, DLQ/replay, metrics, backup/restore scripts | Demonstrable locally; do not equate fixture success with production accreditation. |

## Scenario acceptance matrix

| Scenario | Golden entrypoint | Required proof |
|---|---|---|
| Intent to runtime | `urn:eoip:work:item:jira:PAY-142` | Shortest governed trace contains `IMPLEMENTS`, `MODIFIES`, and `DECLARES`. |
| Incident root cause | `urn:eoip:ops:incident:INC0012042` | A path exists to production deployment and pipeline, with alert/log/dashboard correlations. |
| API blast radius | `urn:eoip:code:api-service:northstar:checkout` | Downstream services, endpoints, monitors and tests are reachable; blast radius returns a useful multi-node result. |
| Release governance | `urn:eoip:cicd:release:northstar:2026.10.1` | Release links to pipeline, jobs, artifact and deployment. |
| Test intelligence | `urn:eoip:test:suite:northstar:checkout-regression` | TC-884 reaches PAY-142, `authorize_order`, and `POST /orders`; run results are present. |
| Design to delivery | `urn:eoip:design:file:northstar:checkout` | File contains page/component and designs FTR-42/US-142. |
| Knowledge provenance | `urn:eoip:knowledge:kb:northstar:KB00192` | Runbook documents the Checkout API and is connected to operational context/evidence. |
| Graph analytics | Checkout API subgraph | Centrality, community, similarity, anomaly, link prediction and what-if endpoints have connected input. |

## Data and schema controls

`schemas/demo_scenario_pack.schema.json` defines the checked-in dataset contract. Runtime loading adds a second control layer: every vertex and relationship is checked against the current ontology, duplicate canonical IDs are refused, relationship endpoints must exist and satisfy domain/range constraints, and every scenario path must refer to fixture vertices. The fixture is captured before mutation and loaded through `IngestionGraphStore`, so it exercises the same normalized graph-mutation boundary as source ingestion.

The pack uses reserved `.invalid` hostnames and synthetic people, identifiers, metrics and incidents. It contains no credentials, customer records, real card information, or external network dependency.

## Remaining gaps and sales claims to avoid

- Connector fixture availability is not proof of authenticated connectivity to a customer's Jira, ServiceNow, Figma, observability or source-control instance. Run each connector's live acceptance gate in the target environment.
- KGR phases 9 and 10 remain explicitly TODO in the implementation plan even though some component files exist. Do not describe all advanced components as fully wired without browser acceptance.
- G2 P6-P10 architecture conformance, causal intelligence, immune-system automation, full process mining, knowledge capsules, and advanced temporal/simulation experiences remain partial, planned, or uncertified.
- Logical backup/restore is not native HugeGraph/RocksDB disaster recovery and does not yet prove complete configuration/job-state recovery.
- Published smoke benchmarks are not a production-scale hardware certification, capacity guarantee, or customer SLO.
- The live source-extension host rehearsal uses the real API/MCP and HugeGraph, not the HTTP contract fixture. It does not certify the installed VSIX or every rendered-UI behavior.
- Optional LLM synthesis depends on locally configured models. Every golden scenario must remain demonstrable with deterministic graph behavior.
- The governed `/api/v1/path` query uses a semantic relationship allowlist and does not return every cross-domain Northstar route. Use `/api/v1/graph/shortest-paths` for the incident, release, test and design scenarios until those query semantics are deliberately unified.

## Release gate

Before a sales session, require all of the following:

1. `python -X utf8 -m pytest -q tests/e2e/test_enterprise_demo_scenarios.py` passes.
2. The web production build passes.
3. The Docker stack reports healthy and the demo job succeeds.
4. `/api/v1/demo/scenarios` returns top-level `ready: true` and thirteen ready scenarios.
5. Graph validation returns zero errors; any warning is explained before presentation.
6. PAY-142 trace, INC0012042 correlation, Checkout API blast radius, and KB00192 retrieval are rehearsed against the exact deployed build.
7. The presenter states whether source systems are offline fixtures or live configured connectors.

This gate supports a credible demo of implemented capability while keeping roadmap and production-certification claims honest.

## Historical verification executed on 2026-10-04

- Runtime verification was refreshed on **2026-10-04** after rebuilding the primary Docker stack from the final working tree.
- Full Dockerized Python regression: **1,008 passed, 15 skipped** in 138.32 seconds. The two emitted warnings are the known Starlette/httpx deprecation and the deliberate duplicate-ZIP security fixture.
- Fresh host JUnit evidence: `test-results/full-regression-2026-10-04.xml` contains 1,023 outcomes: **1,008 passed, 0 failed, 0 errors, 15 skipped**. Its SHA-256 is recorded in the requirement-evidence receipt.
- MVP traceability evidence: `test-results/mvp-requirement-evidence-2026-10-04.json` is tamper-evident and correctly reports `EVIDENCE_GAPS`; only 3/28 MVP rows currently have complete passing requirement annotations (10.71%). This is an annotation-coverage result, not an application-completion percentage.
- Enterprise scenario and clean-recovery tests: passed, including idempotency, schema/ontology validation, live catalog readiness, cross-domain paths, graph analytics, replay, and exact logical recovery.
- Ruff over the entire repository: passed after closing the stale UTC alias, silent Git diff-hunk exception, and test-import findings.
- `git diff --check`: passed; Git emitted only the repository's existing Windows line-ending conversion notices.
- Web production build: passed with Vite; the existing greater-than-500-kB chunk warning remains a frontend performance optimization item.
- Executable in-process demo receipt: enterprise load `SUCCEEDED`; 8/8 scenarios ready; 150 vertices after persisting the validation run, 456 edges, 31 raw captures, zero validation errors/warnings, and 1.0 evidence/provenance coverage.
- Disposable real-HugeGraph acceptance: **PASS**. Receipt: `test-results/eoip-acceptance-0e315bbbdca147d5b50c7d96e9da287a.json`. It proves 111 vertices, 345 relationships, 11 restored raw files, exact replay equivalence, clean validation, populated-target refusal, canonical-ingestion contract validity, idempotent schema preflight, and rejection of four incompatible schema proposals without mutation.
- Docker smoke: **PASS** for readiness/authentication/query limits, Jira-to-commit-to-file-to-symbol evidence, validation, durable worker replay, frontend delivery, and real MCP search/path tools.
- Dockerized Playwright: **5 passed** in 33.7 seconds after recreating the web container from the current frontend. Coverage includes login/search/trace/admin, invalid credentials, API outage and retry, network interruption, and held-job readmission/cancellation.
- Live primary stack: API, worker, web, MCP, and HugeGraph containers are healthy. The live demo job `d2ec736e-e5c4-411f-933e-712b5485f765` succeeded and `/api/v1/demo/scenarios` reports `ready: true` with 8/8 scenarios ready.
- Live scenario probes: intent-to-runtime returned 2 shortest paths; incident-to-pipeline 2; release-to-deployment 3; test-suite-to-endpoint 3; design-to-feature 1; Checkout API blast radius affected 8 entities; KB00192 deterministic GraphRAG returned a grounded fact; centrality returned all 3 requested services; Checkout API removal what-if completed in 15.45 seconds.
- The persisted development graph currently validates with **0 errors**, 47 warnings, evidence coverage 1.0, and provenance coverage 0.6328 across 321 current entities and 1,033 relationships. The warnings and lower provenance score are attributable to older retained development entities, not the isolated Northstar pack; use the isolated acceptance receipt for a clean sales claim or reset into a disposable demo deployment before presentation.
- The desktop in-app browser runtime exposed no controllable browser instance during this audit. Visual verification was therefore completed through the repository's Dockerized Playwright/Chromium suite rather than an interactive browser session.
