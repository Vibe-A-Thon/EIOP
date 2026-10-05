# Hubble Runtime Validation Report

**Generated**: 2026-10-05T13:01:58+05:30
**Target**: local EOIP Docker deployment, HugeGraph/Hubble 1.7.0, standalone RocksDB
**Publication**: changes remain uncommitted at the user's request; no PR, push,
merge or remote CI result is claimed.

## Summary

| Validation | Status | Exit code | Evidence |
|---|---|---|---|
| No-cache clean rebuild | PASS | 0 | Original 310 vertex IDs, 374 edge IDs and 14 raw/job file hashes retained |
| Derived English-default image startup | PASS | 0 | Official Hubble 1.7.0 base; healthy local Hubble |
| Focused Python integration/setup/security tests | PASS | 0 | 43 tests passed |
| Browser tests | PASS | 0 | 3 tests: English bootstrap, real Gremlin/schema journey, saved-language preservation |
| Complete-corpus loading | PASS | 0 | 85 files, 85 Documents, 1,116 chunks, 8 enterprise scenarios; PAY/FRD Jira |
| Persisted artifact verification | PASS | 0 | 510 exported files checked against manifest hashes; 1,116 vector records |
| Live API/Hubble tests | PASS | 0 | 4 tests: manual ingestion, pipeline ingestion, persistence, entire corpus read-back |
| Real complete-corpus rerun | PASS | 0 | Loaded 0, retained 85; vertex/edge totals unchanged |
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
integration: PASS - exit_code: 0; passed: 43, failed: 0, skipped: 0; focused scope
e2e: PASS - exit_code: 0; 4 live API/Hubble tests and 3 browser tests
regression: FAIL - exit_code: 1; passed: 1668, failed: 12, skipped: 20, errors: 0
overall: FAIL - broader regression failures remain; no full-suite waiver or remote CI evidence
```

No dependency or browser installation was needed. Tests used the configured
Python 3.11.9 virtual environment and an existing cached browser. The Hubble
browser tests ran before the complete-corpus import; the subsequent live corpus
test verified every imported document/chunk in the populated graph. After
loading, the open English Hubble browser also successfully executed
`g.V().hasLabel('Document').limit(5)`; its query history reported success in
1.088 seconds.

## Acceptance checklist

| Requirement | Outcome | Evidence |
|---|---|---|
| View the same standalone RocksDB graph through Hubble | Verified | [Compose](../deploy/docker-compose.yml), real Gremlin/schema browser journey |
| Use the requested local admin/admin graph connection | Verified | [Authenticated account/connection setup](../scripts/setup_hubble.py), successful real graph queries |
| English on first use without overriding saved choices | Verified | [Language bootstrap](../deploy/hubble/default-language.js), three [browser tests](../apps/web/tests/hubble.spec.js) |
| Manual ingestion persists and is queryable | Verified | [Live manual journey](../tests/runtime_hubble/test_01_manual.py) |
| Batch pipeline ingestion persists and is queryable | Verified | [Live pipeline journey](../tests/runtime_hubble/test_02_pipeline.py) |
| Clean builds retain existing graph and application data | Verified | No-cache rebuild comparison: 310 vertices, 374 edges, 14 unchanged raw/job hashes |
| Load every selected checked-in demo asset | Verified | [Additive loader](../scripts/load_demo_corpus.py), 85-file successful receipt |
| Read every corpus document and RAG chunk through Hubble | Verified | [Full-corpus live test](../tests/runtime_hubble/test_04_corpus.py), exact ID-set comparisons |
| Retain unchanged assets without duplicate graph records | Verified | Real rerun: loaded 0, retained 85, counts unchanged |
| Full regression and remote CI green | Not verified / blocked | Full local suite failed; remote CI not run |

Synthetic acceptance records are intentionally retained. No graph reset,
schema clear, volume deletion or destructive cleanup was used.

## Corpus and persistence evidence

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

1. Open **http://localhost:8088**, then **Visit** on the **EOIP** connection.
2. Under **Data Analysis**, execute `g.V().hasLabel('WorkItem').limit(25)`,
   `g.V().hasLabel('Document').limit(25)` or
   `g.V().hasLabel('DocumentSection').limit(25)`.
3. Inspect **Chart** and **Json**; open **Metadata Configuration** for schema.
4. Use **http://localhost:8080/admin** for manual ingestion with the existing
   EOIP API token. The web/API token is distinct from graph `admin/admin`.
5. Run `.\scripts\docker.ps1 rebuild` for a data-safe clean build.

Image deletion alone does not delete data. A fresh deployment requires a
separately approved volume deletion. Keep the Compose project name `eoip`.
