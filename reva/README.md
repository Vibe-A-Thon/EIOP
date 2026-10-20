# REVA Component

Source-inspected integration snapshot: 2026-10-19. REVA is the Reverse-engineering, Evidence, Verification & Assurance layer described by the [requirements](../reva-requirements.md) and [implementation plan](../reva-implementation-plan.md). Those specifications define intended behavior; this guide describes the visible integration boundaries, not requirement closure.

## Source and Ownership Map

| Location | Responsibility or starting point |
|---|---|
| `config.py` | `RevaSettings`, `REVA_` environment prefix and process-local settings cache |
| `core/` | Canonical data, identifiers, errors, redaction and time helpers |
| `kernel/` | Warrant records, persistence, signatures, blobs, transparency log and policy primitives |
| `pd/` | Proof-of-Done obligations, runs, closure evaluation and ledger export |
| `sandbox/` | Checkout, execution, collection and attestation components |
| `extract/`, `graph/`, `workflows/`, `views/` | Extraction, graph projection, analytical workflows and response budgeting |
| `api/` | FastAPI routers and domain error-handler registration helper |
| `cli/main.py` | Click CLI and its separate default local store |
| `worker.py` | Job enqueue/lease/worker classes; no module-level service launcher |
| `mcp/` | REVA MCP implementation; verify actual registration into the deployed MCP entry point |
| `../tests/reva/`, `../scripts/reva/` | Component tests and build/verification utilities |
| `../docs/reva/` | Baseline, decisions, obligations and generated status/ledger documents |

Directory names describe code organization, not assurance that every intended capability is complete or integrated.

## API Boundary and Startup

The inspected [API factory](../apps/api/main.py) imports REVA settings and mounts `reva_router` at `/api/reva/v1` only when `REVA_ENABLED` is true. The default is false. The import/mount block catches all ordinary exceptions without reporting them: a running EOIP API does not prove REVA loaded. Inspect the actual OpenAPI routes and startup behavior in an isolated environment.

The mounted `/api/reva/v1/health` is exempt from EOIP's generic bearer check and returns a static status/version. It does not establish database, key, kernel, authorization or worker readiness. Other REVA routes remain inside the enclosing API boundary, but handlers such as `api/routes_warrants.py` accept caller-provided tenant/principal headers. Review their binding to trusted identity before exposing them; outer authentication alone does not establish correct tenant authorization.

`api/routes_warrants.py` requires `set_api_kernel(...)`; without an initialized kernel, `get_kernel()` returns HTTP 503. The inspected host factory mounts the router but does not call that initializer or `register_reva_error_handlers(...)`. Resolve lifecycle initialization, error handling and trusted identity integration in a separately tested implementation change. Do not use a successful health response or standalone router test as proof of integrated service readiness.

## Configuration and Persistence

| Setting | Inspected default / boundary |
|---|---|
| `REVA_ENABLED` | `false`; controls the optional API mount |
| `REVA_STORE_URL` | `sqlite:///data/reva/reva.db`; a settings value is not proof every entry point uses it |
| `REVA_BLOB_ROOT` | `data/reva/blobs`, relative to the process working directory |
| `REVA_KEK` | Source default decodes to 32 zero bytes; never use it for production key protection |
| `REVA_DB_SAMPLE_ROWS` | `0`; row sampling is not enabled by default |
| `REVA_JIRA_WRITEBACK`, `REVA_AUTO_PROBES` | `false`; independently qualify any external effects before enabling |

Read [config.py](config.py) for the complete model and validation. The settings cache is process-local; changing an environment variable does not update an already-created settings instance. The current key validator checks decoded length, not deployment key security. Provision secret material through an approved private channel; never copy a real key into documentation or a command committed to Git.

The CLI's `get_default_store()` currently uses `~/.reva/<tenant>.db`, rather than `REVA_STORE_URL`. Do not assume CLI and API operate on the same data. Resolve data-root ownership, migrations, backup consistency, tenant isolation and restore behavior before sharing persistent environments.

## Packaging and Execution

Run source-tree commands from repository root with the intended environment activated. [pyproject.toml](../pyproject.toml) currently discovers `eoip*` under `packages/`; this does not package root-level `reva/` or establish a `reva` console script. The compatibility directory `packages/reva/` does not itself prove wheel inclusion. REVA imports additional libraries, including `pydantic_settings`, which are not declared as direct core dependencies in that manifest. A developer environment containing them is not a clean-install verification.

After resolving dependency availability, the implemented module CLI can be inspected with:

```powershell
python -m reva.cli.main --help
python -m pytest tests/reva -o addopts= -q -ra
```

These are entry points for follow-up verification, not commands executed by this documentation refresh. CLI operations such as `doctor` can create local persistence; use an isolated test account/home and disposable tenant identifiers. Verify dependencies and packaging in a clean environment before publishing installation instructions for customers.

[docker-compose.reva.yml](../docker-compose.reva.yml) currently declares volumes but comments out its only service example. It does not start a REVA service. Likewise, `python -m reva.worker` does not launch the `JobWorker` loop in the inspected source. Do not present either as a supported deployment procedure until executable lifecycle integration and shutdown/recovery tests exist.

## Evidence and Handover

[BUILD_STATE.md](../docs/reva/BUILD_STATE.md) contains completion claims from a separate workstream that have not been independently reproduced. The [ledger](../docs/reva/reva-ledger.md) is regenerated by `scripts/reva/run_reva_ledger.py --write-docs` from a real `pytest tests/reva` run (the reva-ledger CI lane runs the same on every push/PR); it currently closes nothing because no obligation has a human review (`docs/reva/obligations/reviews.yaml`) or a binding (`docs/reva/obligations/bindings.yaml`). The earlier all-closed ledger was produced by the retired, self-certifying `build_reva_ledger.py`.

Before promotion, verify a clean install, real host-factory startup, initialized persistence/key management, trusted tenant/principal binding, denied cross-tenant requests, worker lifecycle/recovery, MCP registration and any user-visible acceptance journeys. Retain source-bound execution artifacts required by the owning specification. Follow [testing](../docs/testing-guide.md), [migration](../docs/migration-refactoring-guide.md) and [release gates](../docs/release-checklist.md); source references and green unit tests alone cannot close integrated claims.
