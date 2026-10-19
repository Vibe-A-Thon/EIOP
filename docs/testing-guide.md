# Testing and Evidence Guide

Tests establish only the behavior and environment they actually exercise. Use requirement IDs for traceability, but never treat filenames, markers, counts or code coverage as proof of full product completion.

## Python

Install the repository in a Python 3.11+ virtual environment with `python -m pip install -e ".[dev]"`. The authoritative pytest configuration is [pyproject.toml](../pyproject.toml). `tests/conftest.py` adds root/package paths for subprocesses and loads `eoip.verification.pytest_evidence`.

```powershell
python -m pytest tests/unit/test_provenance.py -q
python -m pytest tests/integration/test_external_mcp_bridge.py -q
python -m pytest tests/neural/test_numerics.py tests/neural/test_runtime_tiers.py -q
```

Neural/report/parser tests may require their optional extras. Inspect the test and its fixtures before running infrastructure-dependent cases. Markers include `req`, `smoke`, `slow`, `integration`, `security`, `performance`, `enterprise` and `eoip_requirement`. The `slow` marker's description is not an automatic exclusion: current default `addopts` does not contain `-m 'not slow'`.

For a bounded evidence-producing run:

```powershell
python -m pytest tests/unit/test_repository_inventory.py -q --junitxml=test-results/repository-inventory.xml --run-evidence=test-results/repository-inventory-receipt.json
```

Keep the process exit code, command, UTC time, source/build identity, profile and output artifacts together. Do not overwrite earlier failing receipts and present only the final successful summary. A dirty checkout needs source hashes or a corresponding committed build identity, not just the word `HEAD`.

## Web and IDE

The default web package has `typecheck`, `test:unit`, `build`, `test:e2e` and `test:a11y` scripts. The latter two select specific specs, not every browser test. See [frontend development](frontend-development.md) for host/container URL setup and the alternate frontend's distinct script set.

VS Code `npm test` runs Node tests and an extension host. It may download a VS Code host unless configured otherwise. It uses isolated profiles and contract fixtures; distinguish those results from a live API/graph run and packaged-VSIX acceptance. See the [extension README](../apps/vscode-extension/README.md).

## Integrated Profiles

Container helper actions include `test`, `acceptance`, `recovery-acceptance`, `dlq-acceptance` and `restore-test`. These can build images, write demo state and create/delete disposable resources. Inspect the [deployment README](../deploy/README.md) and run them only against the intended test profile.

The main [CI workflow](../.github/workflows/ci.yml) declares Python checks, security/transport checks, web type/unit/build checks and selected browser specs. [Validation evidence](../.github/workflows/validation-evidence.yml) has additional platform-specific automation. Workflow existence is not evidence that the current branch passed remote CI. Not every local module, frontend, connector or deployment profile is covered by the main workflow.

## Risk-Based Selection

| Change | Minimum relevant checks |
|---|---|
| Pure documentation/tooling | Link/path checks, tool tests, documented CLI syntax and no secrets in output |
| Contract/query | Schema validation, bounds, malformed inputs, backward compatibility, authorized and denied reads |
| Storage or jobs | Restart, interrupted writes, replay, duplicate delivery, concurrency and restore |
| Authentication/tenancy | Invalid/expired/revoked credentials, cross-tenant objects, direct API access, cached/exported/event data |
| Connector | Real protocol with isolated fixture first, then authorized vendor sandbox qualification; retry and cursor recovery |
| UI | Unit/type/build, keyboard/a11y/layout, real-backend journey and protected exports |
| Agent/model | Original programme's effect/evidence/anti-stub/calibration gates; unavailable profile refusal |
| Distribution | Fresh install, upgrade, notices, dependency profile, offline/egress and rollback |

## Evidence and Status

Use the owning programme's exact status vocabulary. `CODE-COMPLETE` is not `VERIFIED`. Missing infrastructure, absent credentials, skipped tests, a green mock server or a screenshot of a component must not close a live integration gate. A required negative control should demonstrate that missing/tampered evidence prevents completion.

Store durable release evidence outside ignored scratch directories with controlled retention. Track small fixtures, schemas, commands and evidence manifests in Git. The tracked `.audit-scratch/baseline/` files are currently referenced by acceptance tests; migrate those references deliberately before untracking the entire folder.

The release-gate helper has limitations described in [Release Checklist](release-checklist.md). Its checklist-presence check is not a release certification. Investigate misleading gate behavior as implementation work; do not compensate by changing documentation to say it passed.
