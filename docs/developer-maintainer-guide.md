# Developer and Maintainer Guide

This guide describes the repository as it exists today. Normative workstream requirements remain in their own specifications; a guide, module, or passing unit test is not evidence that a workstream is complete.

## Runtime Map

| Component | Entry point | Responsibility and boundary |
|---|---|---|
| API | `apps/api/main.py:create_app` | Builds the authenticated FastAPI application, configures the graph store, auth, audit, validation, jobs, agent runtime, and routes. Run with Uvicorn's `--factory` option. |
| Query/API sub-application | `apps/api/app.py:create_app(store, ...)` | Creates the graph/query application against an injected `GraphStore`; the main factory mounts and extends this route surface. It is not a second standalone default app unless a caller supplies a store. |
| Worker | `apps/worker/main.py:main` | Polls the filesystem-backed `JobQueue` under `EOIP_DATA_DIR` and invokes ingestion and graph-consumer handlers. The current worker is a single process; do not describe its queue as a distributed broker. |
| MCP server | `apps/mcp/main.py:create_app` | Exposes read-oriented MCP tools and forwards requests to the authenticated API using the configured API token. It does not own graph storage. |
| Web application | `apps/web/` | React 19/Vite app for graph exploration and administration. The production image builds static assets and serves them through unprivileged Nginx; the development server proxies API paths only when `EOIP_DEV_API_URL` is set. |
| Alternate frontend | `frontend/src/App.tsx` | Separate TypeScript router/shell/client, not the default Compose build. Reconcile its unique behavior before any retirement. |
| Preview backend | `backend/server.py:app` | Supervisor shim over the API factory, with local development defaults and demo seeding. Not a production credential profile. |
| VS Code extension | `apps/vscode-extension/` | Read-only IDE integration. It stores the API token in VS Code SecretStorage and constrains source navigation to the configured workspace root. |
| Graph abstraction | `packages/eoip/graph/` | `GraphStore` contracts, backend selection, in-memory store, and vendor adapters. |
| Shared policy/domain | `packages/eoip/contracts/`, `authn/`, `authz/`, `tenancy/`, `policies/` | Request/record schemas and identity, authorization, and tenant policy boundaries. |
| Configuration | `config/` | Graph-store, ontology, agent, policy, mapping, and capability configuration. |

The container deployment in `deploy/docker-compose.yml` includes HugeGraph, schema initialization, Hubble, API, worker, MCP, and web services. Test, local-model, tools, restore-test, and observability services are profile-gated. The default graph backend in `config/graph-store.yaml` is HugeGraph. Host development should explicitly select `EOIP_GRAPH_BACKEND=memory` unless a reachable graph backend is configured; memory state is not durable across API restarts.

## Data and Persistence Boundaries

- The graph store owns graph records. The default container profile uses a named HugeGraph data volume; `memory` is suitable for isolated tests and disposable local development only.
- Application files under `EOIP_DATA_DIR` hold job queue state, worker heartbeat, audit data, connector state, receipts, and other file-backed records. Compose mounts this directory at `/data` through the application data volume.
- Separate memory-backed processes do not share graph state even if their data directory is shared. Optional filesystem leader-lease code does not qualify multi-host execution.
- The worker queue is file-backed and designed for this deployment profile. Do not infer multi-host coordination, transactional outbox behavior, or PostgreSQL authority storage from the existence of a queue or store interface.
- Demo and research data under `demo/` and `research/` are synthetic/local inputs. Explicit ingestion is required; their presence does not make them production connector registrations or live-vendor evidence.
- Connector credentials belong in deployment secret/environment configuration. Store opaque references and non-secret options in source/job records. Do not put tokens in request examples, logs, fixtures, or evidence bundles.

## Local Development

Use Python 3.11+ and Node.js 22 for the current web package. Keep the core installation separate from optional extras.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
npm --prefix apps/web ci
```

For a disposable in-memory API, provide a token meeting the runtime's minimum length and select the memory graph backend:

```powershell
$env:EOIP_API_TOKEN = 'local-development-token-at-least-24-chars'
$env:EOIP_GRAPH_BACKEND = 'memory'
$env:EOIP_DATA_DIR = (Join-Path $PWD '.eoip-data')
python -m uvicorn apps.api.main:create_app --factory --host 127.0.0.1 --port 8000 --reload
```

In another shell:

```powershell
$env:EOIP_DEV_API_URL = 'http://127.0.0.1:8000'
npm --prefix apps/web run dev
```

The web package's Vite proxy is configured by `EOIP_DEV_API_URL`; without it, API calls are not automatically routed to the host API. For the integrated HugeGraph/worker/MCP deployment, use `scripts/container.ps1 up` or `scripts/container.sh up`, which creates a local ignored `deploy/.env` if needed. Never place production tokens in the example commands above.

## Tests and Quality Checks

Start with the narrowest relevant test, then run the applicable package and integration gates. Examples:

```powershell
python -m pytest tests/unit/test_provenance.py -q
python -m pytest tests/integration/test_external_mcp_bridge.py -q
python -m pytest tests/neural/test_numerics.py tests/neural/test_runtime_tiers.py -q
python -m pytest tests/unit/test_document_references.py -q
npm --prefix apps/web run typecheck
npm --prefix apps/web run test:unit
npm --prefix apps/web run build
```

`pyproject.toml` configures pytest's test roots, strict markers, and async mode. Relevant markers include `req`, `integration`, `security`, `performance`, and `enterprise`. Some tests require optional packages, external services, a browser host, or container runtime. A skip, missing dependency, or unrun profile is not a pass. Run `python -m pytest tests/compliance/test_no_cuda_packages.py -q` after changing Python dependency locks; the repository policy rejects CUDA/NVIDIA package names in distribution configuration.

The current `eoip` CLI is a small developer utility (`python -m eoip.cli --help` or the installed `eoip --help`), not a complete ASPEII workflow CLI. Do not document planned commands as available before they are registered and tested.

## Change Workflow

1. Read the owning specification, applicable plan, and repository-local instructions. Check `git status` and preserve unrelated work.
2. Choose one falsifiable behavior at the real owning boundary. State the smallest check that could disconfirm it before editing.
3. Follow the existing service/contract ownership. Prefer a Pydantic contract and injected service dependency over route-local business rules. Resolve identity and tenant from trusted request context, not caller-supplied identity fields.
4. Keep optional capabilities explicit. A missing model, graph service, vendor credential, or unqualified adapter must report unavailable/blocked rather than return synthetic success or a plausible placeholder result.
5. Add a positive case and the relevant negative/security case. For durable or consequential behavior, add persistence, replay/restart, authorization, and independent effect observation as applicable.
6. Run the focused test immediately after the edit. Then run targeted type/lint checks and the wider relevant suite. Record failures honestly; do not loosen thresholds or delete failing cases to make a gate green.
7. Update the owning docs and progress ledger only with behavior and evidence actually observed. Do not mark a requirement verified from source references or unit-test existence.

Use the graph abstraction instead of backend-specific logic outside its adapters. Preserve ontology labels and schema validation. Use the shared query-policy and evidence/provenance mechanisms instead of creating an alternate authorization path.

## MCP Boundary

The local MCP server is a read facade over the API. The external MCP client supports Streamable HTTP and explicitly configured stdio servers. HTTP hosts, server names, and tool names must come from trusted configuration; stdio process command/arguments/environment are not accepted from API requests. Discovery and schema are rechecked before invocation. MCP read-only annotations are not authority by themselves; the local allowlist is also required. This work does not qualify a real vendor write connector or an external-effect execution gateway.

Configuration keys and examples are in [API Reference](api-reference.md#external-mcp-configuration).

## Optional Neural Dependencies

The core dependency set must stay usable without the numerical or Torch stack. N0 is the optional `numerics` extra in `pyproject.toml`; its current resolved profile is documented in [Optional Neural Tiers](install-neural.md). N1–N3 are not declared/qualified in this checkout. Neural predictions must remain distinct from observed graph facts, and the current hash baseline exists only in tests. Do not promote an encoder to production without the prescribed behavioral/statistical, anti-stub, temporal, security, and operational evidence.

## Documentation Ownership

- Root `README.md`: project entrypoint, supported local run paths, current limitations, and links to maintained guides.
- `docs/getting-started.md`: commands and prerequisites for first run.
- `docs/architecture-guide.md`: runtime topology and data boundaries.
- `docs/api-reference.md`: API route families and request/configuration contracts.
- `docs/install-neural.md`: optional dependency tiers and measured qualification state.
- Workstream requirement/plan files: normative acceptance criteria and evidence gates.
- Demo/data `README.md` files: scope, contents, and execution expectations for those fixtures only.

When implementation, configuration, schema, or launch behavior changes, update its owner guide and test the linked commands where feasible. Generated audit reports are snapshots; regenerate them with their documented scanner instead of manually editing generated findings. Historical audit files remain historical.

## Known Workstream Status

ASPEII, CIP/CTAR, IP/Warrant, and Graph Neurons plans contain mandatory integration and independent-evidence gates. Local implementation slices and focused tests do not close those programmes. Durable authority storage, complete dispatch/receipt services, full CTAR workflows, production model qualification, external connector writes, browser release journeys, cross-platform packaging, restore, and independent release verification remain open or blocked unless a current programme ledger says otherwise.

## Team Handover and Further Reading

Use the [documentation index](README.md) as the handover entry point. The [package map](../packages/eoip/README.md) identifies domain starting points; [configuration](configuration-reference.md) explains loader boundaries; [operations](operations-runbook.md) explains diagnosis and recovery; [testing](testing-guide.md) explains evidence; [migration/refactoring](migration-refactoring-guide.md) defines change and compatibility procedures.

Wisdom Graph adds another cross-programme dependency chain; see its [requirements](../wisdom-graph-requirements.md). The [suite proposal](EOIP-suite-architecture-plan.md) is future organization, not a completed set of portals. Preserve original programme gates and exact record identities while reorganizing code.

The [documentation review](documentation-review-2026-10-18.md) records source-observed risks, including the alternate frontend's synthetic UI principal fallback and limitations of release-gate CLI verification. These remain implementation work, not problems solved by documentation.
