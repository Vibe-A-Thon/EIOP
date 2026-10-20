# EOIP QA automation portfolio

This directory is the control plane for repeatable QA, not a claim that every feature is complete. `qa/manifest.json` lists automated, infrastructure-dependent, quarantined and human-review suites. `qa/test-catalog.json` inventories maintained tests under `tests/` and `apps/web/tests/`; the quarantined `qa_bench/` is deliberately excluded until promoted. `qa/QA-COVERAGE-MATRIX.md` maps QA disciplines to evidence and remaining release conditions. A static test definition or a passing file is **not** proof of integrated product behavior.

## Fast start

Run from the repository root with Python 3.11+ and the project dev dependencies installed:

```powershell
python -m qa.portfolio list
python -m qa.portfolio catalog
python -m qa.portfolio run --profile quick
python -m qa.completeness report
```

The quick profile runs harness tests, a 751-operation OpenAPI method/path drift gate, a dedicated-probe inventory, an API schema-quality regression gate, and a disposable source-registry CRUD workflow. Each child process receives a disposable `EOIP_DATA_DIR`, memory graph backend and local token. The runner does not use shell execution, does not save raw command output and writes a machine-readable summary under ignored `test-results/qa-bench/`. Exit codes: 0 pass, 1 failure, 2 blocked. Run `python -m qa.portfolio run --profile extended` to attempt existing contract, security, compliance, frontend, integration, acceptance, AI, connector, fuzz and end-to-end suites; expensive suites remain blocked until `--allow-expensive` is supplied. A blocked or skipped suite never counts as passed.

The catalog indexes files and test function definitions, not collected parametrized cases or measured application coverage. After adding/removing tests, run `python -m qa.portfolio catalog --write`, review the diff and commit the pin. CI runs the catalog check.

`python -m qa.completeness report` writes a per-item gap inventory to ignored `test-results/qa-bench/completeness.json`. It scans the live OpenAPI surface, MCP registrations, production Python modules (runtime, REVA, scripts, tools, demo, QA harness and audit kit), and web/extension source modules. It distinguishes a dedicated API probe from executed functional proof, and marks modules unmeasured unless a branch-enabled pytest-cov JSON is supplied with `--coverage-json`. Even 100% line/branch execution would not by itself prove behavior. `python -m qa.completeness gate` intentionally returns exit code 2 while release-level executed evidence, requirement mappings and sign-offs are absent; do not use the reporting command as a release approval.

## Postman and API checks

`qa/postman/EOIP-readonly-QA.postman_collection.json` contains 17 bounded probes spanning health, OpenAPI, metrics, authentication denials, admin status, graph, query templates, report templates, product capabilities and missing-route behavior. It only issues GETs. `qa/postman/EOIP-disposable-source-workflow.postman_collection.json` exercises source create, read, duplicate rejection, update, list, delete and post-delete 404. It is **mutating** and refuses to run unless the target is loopback and `qaDisposableTarget=true`. Do not set that flag against an existing server. The supported Newman entry point launches its own in-memory API and supplies the flag only for that process:

`qa/postman/EOIP-API-operation-catalog.postman_collection.json` is a **non-executable design catalog** for all 751 OpenAPI operations. It has a collection-level `pm.execution.skipRequest()` hard stop, no response assertions and no request fixtures. Its presence never counts as a test. To implement one operation, copy its blueprint into a separate reviewed collection, add synthetic fixtures, authorization/tenant assertions, response-schema and semantic assertions, failure cases and cleanup, then run it against a disposable target. Regenerate and review the full catalog with `python -m qa.postman.build_api_catalog`; CI checks drift via `qa.bench offline`.

```powershell
python -m qa.bench workflow
```

Newman must be available on `PATH` or installed locally in `qa/postman/node_modules/.bin`. An audit of the current Newman 6.2.3 dependency tree found 19 advisories, including one critical, so this repository deliberately does **not** ship or install a Newman dependency in CI. Use an approved, isolated Postman/Newman tool environment and review its dependency audit before opting in. The workflow command generates a random token and temporary data directory, starts a loopback API, runs both collections, stops the API and deletes the directory. The token is passed through a short-lived Postman environment file, never as a CLI argument. No raw Newman response or environment export is kept. CI instead runs `python -m qa.source_workflow`, an equivalent seven-step workflow using the in-process API and no Newman dependency. Regenerate collection artifacts only through `python -m qa.postman.build_collection` and `python -m qa.postman.build_workflow`, then review the JSON diff.

To probe an **existing isolated QA API** without mutation, set `QA_TOKEN` privately and run:

```powershell
python -m qa.bench live --base-url http://127.0.0.1:8000
python -m qa.bench schema --base-url http://127.0.0.1:8000
python -m qa.bench postman --base-url http://127.0.0.1:8000
```

The live suite issues only GETs and records status, latency, response size and correlation-header presence. The schema suite validates four documented 200 JSON responses against their published OpenAPI schemas; it cannot validate endpoints whose schema is empty. The Postman environment template has a blank secret variable; never commit a populated copy. Existing-target commands require `QA_TOKEN` or `EOIP_API_TOKEN` and reject remote targets unless `--allow-remote` is explicit. Even with that switch, mutating workflow commands cannot target a remote server. Never run load, security scans or mutation probes against production.

## Contract quality and known gaps

`qa/contracts/api-surface.json` pins every OpenAPI method/path pair. An intentional route change requires `python -m qa.bench baseline --write`, API-owner review and a committed diff. `qa/contracts/probe-coverage.json` shows that 14 of 751 operations currently have dedicated QA bench requests; the other 737 are **not** thereby proven untested elsewhere, but are unprobed by this dedicated bench. Refresh after a reviewed collection change with `python -m qa.probe_coverage --write`. `qa/contracts/schema-quality.json` pins successful-response documentation findings. On the initial scan, 237 responses had an empty schema and two had no response content. New undocumented success responses fail the gate; existing findings remain open, not silently accepted. For an intentional documentation change, run `python -m qa.schema_quality --write` and review the full diff. None of these pins proves request/response correctness.

On an initial disposable live run, early 401 responses lacked `X-Correlation-ID`, whereas successful responses included it. This is an observability finding. Live evidence records it but does not mislabel the auth denial itself as a failure.

## Other automated suites

| Area | Command or existing location | Boundary |
|---|---|---|
| Python contracts, security, privacy, compliance | `python -m qa.portfolio run --suite python-contract --suite security --suite privacy --suite compliance` | In-process checks; review fixtures and results |
| Integration, acceptance, E2E, AI, connectors, fuzz | `python -m qa.portfolio run --profile extended --allow-expensive` | Potentially slow; disposable data, no external credentials |
| Frontend unit and build | `python -m qa.portfolio run --suite web-unit --suite web-build` | Existing React scripts |
| Browser accessibility/layout | `python -m qa.portfolio run --suite browser-quality --allow-infrastructure` | Local Vite and Playwright browser; serious/critical axe, mobile/desktop overflow, JS errors |
| Bounded load | `python -m qa.portfolio run --suite bounded-load --allow-infrastructure` | k6, two VUs for 30 seconds, isolated target only; smoke threshold, not production SLO |
| Graph benchmark | `python scripts/benchmark.py --help` | Dedicated graph store; see `EOIP-engg-doc-pkg/reference/benchmarking.md` |
| MCP, VS Code, worker, REVA | `mcp`, `vscode-unit`, `domain-engines`; extension-host test and `.github/workflows/reva-*.yml` | Read fixtures and infrastructure requirements before running |

The `mcp` suite now calls every one of the 18 registered tools through streamable HTTP and checks upstream method/path/arguments/token plus representative upstream errors. Its upstream API is mocked for the per-tool matrix; the existing transport test sends `search` to the real in-process API. These tests prove delegation and protocol behavior, not full business semantics of every API endpoint.

`tests/security/test_full_api_auth_surface.py` also sends both missing and invalid bearer credentials through every protected OpenAPI method/path in a disposable in-memory app. It excludes the explicitly public health, metrics and ontology documentation routes and the specially handled source webhook intake. This is an authorization-boundary sweep, not a positive functional test for each endpoint. CI executes it with the other security checks.

The newer `qa_bench/` contains API, Selenium, performance and E2E tests, but is **quarantined from the umbrella runner**: its current configuration embeds role tokens and defaults to the repository's tracked `.eoip-data`. It must be changed to use disposable storage and externally supplied or generated credentials, then verified, before being promoted into automated profiles. Its presence is not a passing functional test result.

Isolation caveat: the umbrella runner redirects `EOIP_DATA_DIR` and the graph backend, but some application endpoints still accept relative output paths (for example, brain learning state defaults to `data/learning`). Do not treat an arbitrary extended or external-target suite as side-effect-free until its file/network writes are audited. Review and clean up only artifacts whose provenance is known; do not delete existing local worktree data as part of QA setup.

## Release evidence and remaining work

For each executed suite retain the commit, environment/dependency versions, dataset or fixture hash, command, dated result, failure triage and owner approval. The runner intentionally retains only status, timing and an output hash to avoid leaking API bodies, tokens or customer data. For diagnosis, rerun a failing command in the approved isolated environment and keep sensitive logs in the team's protected evidence store, not Git.

The manifest also records still-open categories: real external connector certification, disruptive restore/failover, authenticated DAST and penetration review, fresh advisory/signature scanning, representative soak/scale, cross-browser/device compatibility and human assistive-technology review. Those require a scoped environment, target criteria and approval. A green quick profile cannot close them.
