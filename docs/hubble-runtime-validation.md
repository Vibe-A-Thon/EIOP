# Hubble Runtime Validation Report

**Initial validation**: 2026-10-05T13:01:58+05:30
**Latest scope**: enriched enterprise data and named live Hubble exploration
**Target**: local EOIP Docker deployment, HugeGraph/Hubble 1.7.0, standalone RocksDB
**Publication**: changes remain uncommitted at the user's request; no PR, push,
merge or remote CI result is claimed.

## Summary

| Validation | Status | Exit code | Evidence |
|---|---|---|---|
| No-cache clean rebuild | PASS | 0 | Original 310 vertex IDs, 374 edge IDs and 14 raw/job file hashes retained |
| Derived English-default image startup | PASS | 0 | Official Hubble 1.7.0 base; healthy local Hubble |
| Earlier focused integration/setup/security tests | PASS | 0 | 43 tests passed before enrichment |
| Enrichment-focused Python tests | PASS | 0 | 17 tests passed, including TEXT schema compatibility and immutable capture retries |
| Latest browser tests | PASS | 0 | 5 tests, including all 11 live named scenarios and explicit query error handling |
| Latest complete-corpus loading | PASS | 0 | 85 files, 85 current Documents, 1,131 current chunks, 11 enterprise scenarios; PAY/FRD Jira |
| Earlier persisted artifact verification | PASS | 0 | 510 exported files checked against manifest hashes; 1,116 vector records before enrichment |
| Earlier live API/Hubble tests | PASS | 0 | 4 tests: manual ingestion, pipeline ingestion, persistence, entire corpus read-back |
| Latest live enrichment/corpus tests | PASS | 0 | 2 enterprise tests and 1 full-corpus read-back test |
| Latest real complete-corpus rerun | PASS | 0 | Loaded 0, retained 85; exact 1,893 vertex and 6,055 edge identity sets unchanged |
| Enrichment retains previous corpus graph | PASS | 0 | All pre-enrichment 1,805 vertex IDs and 4,349 edge IDs remain present |
| Automatic guided walkthrough | PASS | N/A | Browser reached scenario 11, returned to idle, and restart/Stop controls worked |
| Actual separate Hubble launcher | PASS | 0 | Rebuilt/startup completed, retained all 85 assets, checked guide and opened automatic tour |
| Post-launcher readiness and retention | PASS | 0 | Web/guide HTTP 200; exact 1,893 vertex / 6,055 edge identity sets retained |
| Original graph read-back after loading | PASS | 0 | All original 310 vertices and 374 edges present |
| Scoped Ruff, Compose validation, whitespace | PASS | 0 | Final scoped checks passed |
| Canonical full Python regression | FAIL | 1 | 1,668 passed, 12 failed, 20 skipped, 0 errors |

**Overall: FAIL for the full regression gate.** The requested Hubble deployment,
language, corpus, ingestion and data-retention acceptance checks passed. The
broader regression gate is not green and has no waiver. Do not describe this
phase as CI-passing or all application requirements as complete.

## Environment and verdict

```text
environment:
  docker: AVAILABLE - docker info succeeded during setup; six runtime services healthy
  node: AVAILABLE - Node v26.8.2
  playwright: AVAILABLE - existing toolchain with cached Chromium 1194
  infra-tier: PRIMARY(Docker-based) - real persisted HugeGraph/RocksDB
  browser-tier: PRIMARY(Playwright) - no HTTP-only substitute
startup: PASS - exit_code: 0; Docker startup and readiness checks succeeded
integration: PASS - exit_code: 0; latest 17 focused tests; earlier 43-test receipt retained
e2e: PASS - exit_code: 0; latest 3 live enrichment/corpus tests and 5 browser tests
regression: FAIL - exit_code: 1; passed: 1668, failed: 12, skipped: 20, errors: 0
overall: FAIL - broader regression failures remain; no full-suite waiver or remote CI evidence
```

No dependency or browser installation was needed. Tests used the configured
Python 3.11.9 virtual environment and an existing cached browser. The Hubble
initial browser tests ran before the complete-corpus import; the subsequent live corpus
test verified every imported document/chunk in the populated graph. After
loading, the open English Hubble browser also successfully executed
`g.V().hasLabel('Document').limit(5)`; its query history reported success in
1.088 seconds.

The latest five-test browser run occurred after enrichment. It queried the
same saved Hubble connection and real persisted graph. A PROCESS-only scenario
legitimately has one domain; the test verifies that each legend exactly matches
its returned nodes rather than incorrectly requiring multiple domains everywhere.

## Acceptance checklist

| Requirement | Outcome | Evidence |
|---|---|---|
| View the same standalone RocksDB graph through Hubble | Verified | [Compose](../deploy/docker-compose.yml), real Gremlin/schema browser journey |
| Use the requested local admin/admin graph connection | Verified | [Authenticated account/connection setup](../scripts/setup_hubble.py), successful real graph queries |
| English on first use without overriding saved choices | Verified | [Language bootstrap](../deploy/hubble/default-language.js), latest [browser tests](../apps/web/tests/hubble.spec.js) |
| Business names, colors and directed relationships | Verified | [Live guided explorer](../deploy/hubble/enterprise.js), all-scenario browser journey |
| Understandable business questions over the same graph | Verified | 11 selectable scenarios, live queries, property inspection and query copying |
| Enrich business value, decision history and incident-response steps | Verified | [Canonical seed](../demo/demodata/enterprise/scenario-pack.json): 70 entities, 114 relationships; [live enterprise tests](../tests/runtime_hubble/test_05_enterprise.py) |
| Preserve existing identities and immutable captures | Verified | Exact graph ID retention, 92 legacy fact identities and corrected same-version capture regression |
| Manual ingestion persists and is queryable | Verified | [Live manual journey](../tests/runtime_hubble/test_01_manual.py) |
| Batch pipeline ingestion persists and is queryable | Verified | [Live pipeline journey](../tests/runtime_hubble/test_02_pipeline.py) |
| Clean builds retain existing graph and application data | Verified | No-cache rebuild comparison: 310 vertices, 374 edges, 14 unchanged raw/job hashes |
| Load every selected checked-in demo asset | Verified | [Additive loader](../scripts/load_demo_corpus.py), 85-file successful receipt |
| Read every corpus document and RAG chunk through Hubble | Verified | [Full-corpus live test](../tests/runtime_hubble/test_04_corpus.py), exact ID-set comparisons |
| Retain unchanged assets without duplicate graph records | Verified | Real rerun: loaded 0, retained 85, counts unchanged |
| Full regression and remote CI green | Not verified / blocked | Full local suite failed; remote CI not run |

Synthetic acceptance records are intentionally retained. No graph reset,
schema clear, volume deletion or destructive cleanup was used.

## Latest enterprise enrichment evidence

The canonical Northstar seed is now **1.1.0: 11 scenarios, 70 entities and
114 relationships**. It includes business objectives/capabilities, alternative
decisions and revision/outcome evidence, ordered incident-response steps and an
approval-delay deviation. This is connected synthetic demonstration data, not
measured production KPIs or a claim of automated process mining.

The first successful enriched load returned:

```json
{
  "run_status": "SUCCEEDED",
  "files": 85,
  "loaded": 2,
  "retained": 83,
  "documents": 85,
  "chunks": 1131,
  "enterprise_scenarios": 11,
  "jira_datasets": ["manual", "pipelines"]
}
```

A subsequent real rerun returned **loaded=0, retained=85**. The graph contains
**1,893 vertices and 6,055 edges**. Every pre-enrichment physical ID
(1,805 vertices / 4,349 edges) remains present, and the exact enriched vertex
and edge sets were unchanged on rerun. Current corpus Document/chunk counts
are not total graph counts: earlier source revisions, verification records and
provenance remain stored intentionally.

Two ingestion issues were resolved without changing schema or resetting data:

- Existing `kpi_target` and `kpi_actual` properties are TEXT. Seed values now
  include readable units (`98.5%`, `96.2%`, `450 ms`, `812 ms`), with an
  ontology-type regression test. Numeric duration/capability properties retain
  their proper numeric types.
- An earlier failed attempt had already captured its payload immutably.
  Enterprise event IDs now include the full canonical-content SHA256 digest.
  Corrected content under the same version creates a separate immutable
  capture; identical content reuses its capture. The test preserves original
  capture bytes and stable business/fact identities.

The guided page at **http://localhost:8088/enterprise.html** is served by
Hubble and renders real returned vertices/edges, not catalog-generated graph
data. Browser inspection confirmed business captions, directional arrows,
domain colors, property inspection and successful scenario transitions.
The automatic walkthrough reached the final scenario and returned to idle;
restarting it and stopping early also succeeded.

Executing [run-demo-hubble.ps1](../demo/autodemo/run-demo-hubble.ps1) completed
with exit 0. Its existing `demo-data` preparation workflow rebuilt/recreated
the deployment, retained all 85 assets (`loaded=0`), checked the guided page,
and opened the tour URL. After completion both the web page and guided page
returned HTTP 200, and a fresh Hubble query verified the exact saved enriched
vertex and edge identity sets were still unchanged.

The explorer is a bounded one-hop view (120 relationships per query).
Provenance is hidden by default but can be shown. Seed entity search is not
an exhaustive search of every corpus document. Native Hubble remains available
for unrestricted query authoring; physical IDs are preserved and inspectable.
Semantic embedding quality, production-scale behavior, packaged VSIX/NLQ
acceptance and all application capabilities are not certified by these checks.

## Historical corpus and persistence evidence

First load:

```json
{
  "run_status": "SUCCEEDED",
  "files": 85,
  "loaded": 85,
  "retained": 0,
  "documents": 85,
  "chunks": 1116,
  "enterprise_scenarios": 8,
  "jira_datasets": ["manual", "pipelines"]
}
```

Second real load: `loaded=0`, `retained=85`. Graph counts were **1,805 vertices
and 4,349 edges both before and after** this rerun. Hubble label counts included
56 WorkItems, 87 Documents and 1,117 DocumentSections. The extra two Documents
and one DocumentSection predate this corpus import; totals also include
provenance and verification records.

All 510 exported files matched their manifest hashes. All manifests reported
`SUCCEEDED` with no parsing errors, and vector bundles contained 1,116 records.
These vectors use deterministic local lexical hashing, not trained semantic
embeddings. Other vendor exports are source-preserving documents, not a claim
of complete typed normalization for every vendor.

Durable receipts live in `/data/state/demo-corpus.json` and
`/data/state/demo-corpus-result.json` on the application volume. The verification
rerun called the loader directly and did not overwrite the original CLI receipt.
Changing data or parser versions triggers re-ingestion; unchanged files are
retained only after bundle and graph checks.

The earlier no-cache rebuild comparison verified every original graph ID and
all 14 selected raw/job hashes before intentional demo ingestion. After loading,
every original vertex and edge was checked again. Edge queries used batches
of 25 because Hubble rejects Gremlin statements longer than 10,000 characters;
an oversized diagnostic query was corrected without changing data.

## Test commands and scope

Focused Python command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\e2e\test_demo_corpus.py tests\e2e\test_demo_flow.py tests\e2e\test_enterprise_demo_scenarios.py tests\unit\test_hubble_setup.py tests\security\test_container_hardening.py tests\security\test_no_egress.py -q
```

Latest enrichment-focused command: **17 passed, exit 0**:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\e2e\test_enterprise_demo_scenarios.py tests\e2e\test_demo_corpus.py -q
```

Latest live checks used `EOIP_RUNTIME_HUBBLE=1` and ran
[test_05_enterprise.py](../tests/runtime_hubble/test_05_enterprise.py)
(2 passed) and [test_04_corpus.py](../tests/runtime_hubble/test_04_corpus.py)
(1 passed), both with exit 0. The browser command below now reports **5 passed**.

The initial lint pass in the combined focused run reported import ordering in
the new live corpus test. That ordering was corrected, and a separate final
scoped Ruff command passed. The focused pytest exit code was 0.

Live API/Hubble command:

```powershell
$env:EOIP_RUNTIME_HUBBLE='1'
$env:EOIP_RUNTIME_RUN_ID='hubble-acceptance-20261005'
.\.venv\Scripts\python.exe -m pytest tests\runtime_hubble -v
```

Browser command, from the repository root:

```powershell
$env:EOIP_RUNTIME_HUBBLE='1'
$env:PLAYWRIGHT_BASE_URL='http://localhost:8080'
$env:PLAYWRIGHT_EXECUTABLE_PATH="$env:LOCALAPPDATA\ms-playwright\chromium-1194\chrome-win\chrome.exe"
Set-Location apps\web
npx --no-install playwright test hubble
```

Canonical regression command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The project suppresses the usual final count line at this verbosity. The
recorded 1,668/12/20 counts were derived from the complete pytest progress
output, with all twelve failures named below. Exit code was 1.

### Browser changes

| Test file | Change | Verification |
|---|---|---|
| [hubble.spec.js](../apps/web/tests/hubble.spec.js) | New bootstrap semantics test using the real script | English default and explicit preference preserved |
| Same file | Existing real graph journey no longer manually selects English | Gremlin result, JSON canonical IDs and WorkItem metadata |
| Same file | Added saved `zh-CN` browser preference journey | Explicit preference remains after startup |

## Full regression failures

These areas have no source or test changes in the Hubble worktree diff. Their
failures are outside the focused implementation; no unrelated fixes were made.
No clean-checkout baseline reproduction or waiver is claimed.

| Area | Failing test | Observed failure |
|---|---|---|
| Authentication | `TestLocalIdentityProvider.test_authenticate_success` | Principal ID prefix differs from expected contract |
| Authentication | `TestOidcJwtValidator.test_rejects_non_rs256` | Expected exception not raised |
| Authentication | `TestOidcJwtValidator.test_cryptography_verifier_not_available_path` | Unavailable-cryptography/reload path fails |
| Domain packs | `test_all_packs_load_and_validate_cleanly` | Cybersecurity TARGETS references unknown ConfigurationItem label |
| Domain packs | `test_loaded_packs_are_pydantic_models_with_classes_and_validators` | Same domain-pack validation error |
| Embeddings | `test_ollama_provider_success_and_dim` | Embedding request raises RemoteDisconnected/ModelUnavailable |
| Embeddings | `test_ollama_provider_embed_one` | Same embedding request failure |
| Embeddings | `test_vector_index_with_real_embeddings_ranking` | Same embedding request failure |
| Embeddings | `test_dimension_mismatch_between_add_and_query_falls_back` | Same embedding request failure |
| Embeddings | `test_build_search_index_with_embedder_uses_provider` | Same embedding request failure |
| Marketplace | `TestBuild.test_build_rejects_empty_payload_and_bad_paths` | Expected rejection not raised |
| Marketplace | `TestRegistry.test_list_and_search` | Expected package absent from search results |

An earlier broader smoke run also failed on an expected MCP-tool inventory
that omitted registered `graph_surprises`. That smoke command was not rerun
for this corpus phase, and no full smoke success is claimed.

## Manual use

1. Open **http://localhost:8088/enterprise.html** for named, colored, directed
   exploration. Choose a business question or start the 11-scenario walkthrough.
   The separate [Hubble launcher](../demo/autodemo/run-demo-hubble.bat) prepares
   the real demo corpus and opens the automatic tour.
2. For native Hubble, open **http://localhost:8088**, then **Visit** on the
   **EOIP** connection.
3. Under **Data Analysis**, execute `g.V().hasLabel('WorkItem').limit(25)`,
   `g.V().hasLabel('Document').limit(25)` or
   `g.V().hasLabel('DocumentSection').limit(25)`.
4. Inspect **Chart** and **Json**; open **Metadata Configuration** for schema.
5. Use **http://localhost:8080/admin** for manual ingestion with the existing
   EOIP API token. The web/API token is distinct from graph `admin/admin`.
6. Run `.\scripts\docker.ps1 rebuild` for a data-safe clean build.

Image deletion alone does not delete data. A fresh deployment requires a
separately approved volume deletion. Keep the Compose project name `eoip`.
