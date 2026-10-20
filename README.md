# EOIP

EOIP (Enterprise Ontology & Intelligence Platform), also called KnowGridFlow (KGF) in parts of this repository, is a local-first knowledge graph application. It provides authenticated graph/query APIs, ingestion connectors and jobs, provenance and validation services, a React web app, an MCP server, a worker, a VS Code extension, and local container deployment assets.

This repository contains both active application code and research, demo, planning, and audit material. A module, test, backlog checkbox, or demo result is not proof that a feature is production-qualified. The ASPEII, Community/IP, IP/Warrant, and Graph Neurons plans define acceptance gates that are still being implemented and verified. Do not interpret historical completion counts or old test totals in archived reports as the state of the current checkout.

## Repository Map

For a task-oriented reading path, start with the [Documentation Index](docs/README.md). Every major runtime/source area now has a component README; the [repository inventory](docs/generated/README.md) records static file coverage and its exclusions.

| Path | Purpose |
|---|---|
| `apps/api/` | FastAPI application factory, authentication, middleware, and HTTP routes |
| `apps/worker/` | Single filesystem-backed job worker and ingestion handlers |
| `apps/mcp/` | Read-only MCP server facade over the authenticated API |
| `apps/web/` | React/Vite explorer and administration UI |
| `apps/vscode-extension/` | Read-only VS Code context and MCP client extension |
| `frontend/` | Separate TypeScript preview frontend; not the UI built by default Compose |
| `backend/` | Preview/supervisor shim that delegates to the API factory with development defaults |
| `packages/eoip/` | Graph, ontology, connector, query, retrieval, agent, policy, and domain modules |
| [`reva/`](reva/README.md) | Evidence/assurance workstream; optional API mount, separate packaging and integration caveats |
| `config/` | Graph backend, ontology, connector, agent, and policy configuration |
| `schemas/` | JSON Schemas and schema catalog |
| `deploy/` | Docker/OCI images, Compose profiles, Hubble configuration, and observability config |
| `scripts/` | Container helpers, setup, migration, demo, backup, and verification utilities |
| `tests/` | Unit, integration, contract, security, semantic, neural, and browser tests |
| `docs/` | Operator, developer, API, installation, and decision documentation |
| `EOIP-engg-doc-pkg/` | Engineering specifications, architecture material, audits, and historical research |
| `demo/` | Synthetic demo inputs and browser-driven demonstration tooling |

## Fastest Local Run

The container helper detects Docker, Podman, nerdctl, Finch, or supported Compose commands. On first `up`, it creates a local `deploy/.env` with generated credentials; that file is ignored by Git. Docker or another compatible OCI runtime with Compose must be installed and running.

PowerShell:

```powershell
.\scripts\container.ps1 detect
.\scripts\container.ps1 up
```

Bash:

```bash
./scripts/container.sh detect
./scripts/container.sh up
```

The default Compose profile starts HugeGraph, schema/Hubble initialization, the API, worker, MCP server, web UI, and Hubble. Open:

- Web app: <http://localhost:8080/app>
- Administration UI: <http://localhost:8080/admin>
- API OpenAPI UI: <http://localhost:8000/docs>
- MCP Streamable HTTP: <http://localhost:8001/mcp>
- Hubble: <http://localhost:8088>

Use the generated `EOIP_API_TOKEN` in `deploy/.env` to authenticate. Do not print or commit the token. `scripts/container.ps1 status`, `logs`, `backup`, `restore-test`, and `down` are available. `down` preserves named volumes; avoid `down --volumes` unless you intentionally want to delete local graph and application data.

For exact runtime actions and optional Compose profiles, see [Getting Started](docs/getting-started.md) and [Docker/Container Operations](EOIP-engg-doc-pkg/reference/docker-local.md).

## Host Development

Requirements: Python 3.11 or later, Node.js 22 for the web app, and Git. A virtual environment is recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
npm --prefix apps/web ci
```

Start a local in-memory API in one PowerShell session. These settings are development-only; never reuse the example token in a deployed environment.

```powershell
$env:EOIP_API_TOKEN = 'local-development-token-at-least-32-characters'
$env:EOIP_GRAPH_BACKEND = 'memory'
$env:EOIP_DATA_DIR = (Join-Path $PWD '.eoip-data')
python -m uvicorn apps.api.main:create_app --factory --host 127.0.0.1 --port 8000 --reload
```

In another session, start the UI:

```powershell
$env:EOIP_DEV_API_URL = 'http://127.0.0.1:8000'
npm --prefix apps/web run dev
```

The host API factory is `apps.api.main:create_app`; `apps.api.app:create_app(store, ...)` is a lower-level query application that requires a graph store. For durable local data or a full multi-service run, use the container setup. The `memory` graph backend is process-local and does not survive a restart.

## Tests and Checks

Run focused tests while changing a subsystem, then broaden as needed:

```powershell
python -m pytest tests/unit/test_provenance.py -q
python -m pytest tests/integration/test_external_mcp_bridge.py -q
python -m pytest tests/neural/test_numerics.py tests/neural/test_runtime_tiers.py -q
npm --prefix apps/web run typecheck
npm --prefix apps/web run test:unit
npm --prefix apps/web run build
```

The Python suite is run with `python -m pytest`; test markers include `req`, `integration`, `security`, `performance`, and `enterprise`. Some integration, browser, container, external-provider, and neural tests require extra dependencies or services. A skipped or unavailable profile is not a pass. `scripts/container.ps1 test` runs the Compose test, smoke, and UI-test services where the required container runtime is available.

## Optional Python Extras

`pip install -e .` installs the core application dependencies. Features that need larger or platform-sensitive packages are optional extras in `pyproject.toml`; do not add numerical or GPU packages to core dependencies.

The N0 numerical foundation is installed with:

```powershell
python -m pip install -e ".[numerics]"
```

It installs NumPy, SciPy, and scikit-learn, but not Torch or CUDA. See [Optional Neural Tiers](docs/install-neural.md) for the current install and qualification boundary. N1/N2/N3 model execution is not qualified merely because experimental modules exist. The current Windows N0 cosine benchmark has not met the specified 20 ms target; consult the install guide before relying on that path.

Other extras include `reports`, `fileparse`, `codeparse`, `otel`, `k8s`, `redis`, and `enterprise`. Review the exact resolved dependencies and [third-party licensing status](THIRD_PARTY_NOTICES.md) before building or distributing an image; the repository's release checklist is not currently a commercial clearance.

## Architecture and Data Boundaries

The container deployment uses HugeGraph as its default graph service, a FastAPI API process, a filesystem-backed worker/job queue, an MCP HTTP facade, and a static web image. Other graph adapters are selected through `config/graph-store.yaml` and environment overrides. The API, worker, MCP process, graph backend, and browser have distinct responsibilities; see [Architecture](docs/architecture-guide.md).

Demo datasets are synthetic. They exercise explicit ingestion and query paths; they are not customer data, live vendor qualification, production federation registrations, or proof of production performance. Connector credentials are configured as secrets/environment values and must not be placed in request payloads or documentation. Graph sources and worker storage have different persistence properties; do not describe the file-backed queue as a distributed database or the in-memory graph as durable storage.

The two frontend trees have different routing, authentication and development-server configuration. Read the [Frontend Guide](docs/frontend-development.md) before modifying or consolidating them. A worker and API configured with separate memory stores cannot share graph state through the data directory. The worker defaults to demo loading; explicitly disable `EOIP_LOAD_DEMO` for non-demo deployments.

The [Application Suite Plan](docs/EOIP-suite-architecture-plan.md) proposes independently built portals on the shared platform. It is a migration roadmap, not the current deployment. Existing routes and clients must retain compatible behavior during that work.

## Documentation

| Guide | Use it for |
|---|---|
| [Documentation Index](docs/README.md) | Reading paths, component guides and all active programme links |
| [Getting Started](docs/getting-started.md) | Container and host development setup |
| [Developer and Maintainer Guide](docs/developer-maintainer-guide.md) | Repository layout, service boundaries, change workflow, tests, operations, and documentation policy |
| [Architecture Guide](docs/architecture-guide.md) | Runtime topology, data flow, persistence boundaries, and security boundaries |
| [API Reference](docs/api-reference.md) | API entrypoints, route families, authentication, and MCP configuration |
| [Configuration Reference](docs/configuration-reference.md) | Environment precedence, file loaders, secret handling and safe changes |
| [Operations Runbook](docs/operations-runbook.md) | Diagnosis, persistent state, backup, restore and incident handover |
| [Testing Guide](docs/testing-guide.md) | Test profiles, CI scope, evidence and known verification limits |
| [Migration and Refactoring](docs/migration-refactoring-guide.md) | Contract/storage changes, new development and team handover |
| [Documentation Policy](docs/documentation-policy.md) | Ownership, regeneration and preventing stale completion claims |
| [Optional Neural Tiers](docs/install-neural.md) | Optional N0 setup and qualified/unqualified neural profiles |
| [Release Checklist](docs/release-checklist.md) | Local release preparation checklist and known qualification gaps |
| [Engineering Documentation Package](EOIP-engg-doc-pkg/README.md) | Normative architecture, design, and historical engineering material |
| [ASPEII requirements and plan](aspeii-reqirements.md) | ASPEII scope and evidence gates |
| [Community/IP requirements and plan](community-ip-requirements.md) | CTAR and AMRB scope and evidence gates |
| [IP/Warrant requirements and plan](ip-requirements.md) | Warrant, neural-fabric, and IP work package requirements |
| [Graph Neurons requirements and plan](Graph-Neurons-requirements.md) | Numerical foundation, neural tiering, and model verification gates |
| [Wisdom Graph requirements](wisdom-graph-requirements.md) | Decisions, precedents, outcomes, lessons, counsel and qualification |
| [Third-party notices](THIRD_PARTY_NOTICES.md) | Dependency attribution locations and unresolved licensing review |

## Current Completion Status

This README does not claim the platform or its programme requirements are complete. The implementation plans require behavior at real API, storage, worker, MCP, UI, and deployment boundaries, plus independent verification. Local unit-test success is component evidence only. Review the individual programme ledgers and release evidence for current status; where a required ledger or evidence bundle is absent, treat that work as open or blocked.

See the [documentation review](docs/documentation-review-2026-10-18.md) for this refresh's scope and unresolved implementation risks. First-party distribution follows [LICENSING.md](LICENSING.md); dependencies retain their own terms. No documentation refresh or install command grants commercial clearance.
