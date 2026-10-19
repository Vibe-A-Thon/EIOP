# Getting Started

This guide covers the repository's integrated local container run and a separate host-only development run. For ownership and service boundaries, see the [Developer and Maintainer Guide](developer-maintainer-guide.md).

## Requirements

- Python 3.11 or later for host development and Python tests.
- Node.js 22 for the `apps/web` build and local Vite development server.
- Docker with Compose, Podman with Compose, nerdctl with Compose, or Finch for the integrated container deployment.
- Git for source checkout and code-ingestion demonstrations.

Some optional demos/tests need Chrome, an installed VS Code host, browser dependencies, or extra Python packages. They are not prerequisites for a basic API or container start.

## Integrated Container Run (Recommended)

From the repository root, run:

```powershell
.\scripts\container.ps1 detect
.\scripts\container.ps1 up
```

On Linux/macOS:

```bash
./scripts/container.sh detect
./scripts/container.sh up
```

The helper detects an available OCI runtime and Compose command. On the first `up`, it creates `deploy/.env` containing locally generated `EOIP_API_TOKEN` and `HUGEGRAPH_PASSWORD` values. Keep this ignored file private. The default Compose profile launches HugeGraph, schema/Hubble initialization, the API, worker, MCP server, web UI, and Hubble; it waits for service health.

Local endpoints:

| Surface | URL |
|---|---|
| Web explorer | <http://localhost:8080/app> |
| Administration UI | <http://localhost:8080/admin> |
| API OpenAPI UI | <http://localhost:8000/docs> |
| MCP Streamable HTTP | <http://localhost:8001/mcp> |
| Hubble | <http://localhost:8088> |

The browser UI uses the token generated in `deploy/.env`. Do not paste that value into logs or commit it. The container scripts also support `status`, `logs`, `down`, `backup`, `backup-bundle`, `restore-test`, `acceptance`, `recovery-acceptance`, `dlq-acceptance`, `extension`, `demo-data`, and `rebuild`; some actions require optional Compose profiles and platform tools. See the [container runbook](../EOIP-engg-doc-pkg/reference/docker-local.md).

The default graph backend is HugeGraph. Container graph/application state is stored in named volumes; `down` does not remove them. Do not run volume deletion/reset commands against data you need.

## Host-Only Development

This profile runs the API against a process-local `MemoryGraphStore`. Graph data disappears when the API process exits. It does not start the worker, MCP server, HugeGraph, Hubble, or a durable job store.

The API can still create file-backed application/job records under `EOIP_DATA_DIR`; those files do not make the memory graph persistent. Starting a separate memory-backed worker will not populate this API's graph. Use a shared persistent backend for integrated ingestion.

Create the Python environment and install the development extra:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Start the API with an explicit in-memory backend and a local-only token:

```powershell
$env:EOIP_API_TOKEN = 'local-development-token-at-least-24-chars'
$env:EOIP_GRAPH_BACKEND = 'memory'
$env:EOIP_DATA_DIR = (Join-Path $PWD '.eoip-data')
python -m uvicorn apps.api.main:create_app --factory --host 127.0.0.1 --port 8000 --reload
```

The API uses a factory callable; `apps.api.main:app` is not the supported entrypoint. `apps.api.app:create_app(store, ...)` is a lower-level query application that requires an injected graph store.

In another shell, install web dependencies and run Vite:

```powershell
npm --prefix apps/web ci
$env:EOIP_DEV_API_URL = 'http://127.0.0.1:8000'
npm --prefix apps/web run dev
```

`EOIP_DEV_API_URL` enables Vite proxies for `/api`, `/health`, and `/metrics`. Without it, the development server does not proxy those routes to the API.

There is also a separate `frontend/` TypeScript app and `backend/server.py` preview shim. They have different environment and hosting assumptions; see [Frontend Development](frontend-development.md) instead of mixing their commands with this profile.

For Bash host development, activate `.venv/bin/activate`, use `export EOIP_API_TOKEN=...`, `export EOIP_GRAPH_BACKEND=memory`, and `export EOIP_DATA_DIR="$PWD/.eoip-data"`, then run the same Uvicorn command. Set `EOIP_DEV_API_URL` in the web-server shell. Use a disposable token of at least 24 characters and keep real values out of shell history/logs.

## First Checks

With the API running:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health/ready
```

Run the related checks from the repository root:

```powershell
python -m pytest tests/unit/test_provenance.py -q
python -m pytest tests/unit/test_document_references.py -q
python -m pytest tests/integration/test_external_mcp_bridge.py -q
npm --prefix apps/web run typecheck
npm --prefix apps/web run test:unit
npm --prefix apps/web run build
```

For the full local test container profile, use `scripts/container.ps1 test` or `scripts/container.sh test`. Results may vary by optional packages and host platform; skipped tests and unavailable integration profiles are not passes.

## Optional Features

The core installation does not include NumPy, SciPy, scikit-learn, or Torch. The optional N0 numeric extra can be installed with `python -m pip install -e ".[numerics]"`; refer to [Optional Neural Tiers](install-neural.md) for its measured profile and unresolved release gates. Do not install or describe N1/N2/N3 as available until their extras and qualification evidence exist.

Third-party packages and system images are subject to the [license review](../THIRD_PARTY_NOTICES.md). A successful install does not imply a commercial distribution approval.

## Next Steps

Read [configuration](configuration-reference.md) before connecting a real source, [operations](operations-runbook.md) before changing persistent state, and [testing](testing-guide.md) before interpreting a test/demo result. For non-demo deployments, explicitly set `EOIP_LOAD_DEMO=false`; the worker's current default is true. The [documentation index](README.md) links component-specific maintenance and migration instructions.
