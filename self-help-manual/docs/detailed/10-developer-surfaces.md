# Chapter 10 — Developer Surfaces

This chapter covers everything EOIP offers developers beyond the web UI: the VS Code
extension, the MCP (Model Context Protocol) gateway, the operator script toolbox, the
Python SDK, the secondary application surfaces (`eopisuite/`, `backend/`, `frontend/`,
`reva/`), and the extension points for building your own connectors, plugins,
marketplace packages, and domain packs.

Everything below is grounded in the source at the paths cited. Where a behavior was
verified only by reading code (not by running it against a live deployment), it is
marked **(source-verified only)**.

**Index**

- [VS Code Extension](#vs-code-extension)
  - [Install and run](#install-and-run-the-extension)
  - [Configuration settings](#configuration-settings)
  - [Command reference (19 commands)](#command-reference)
  - [How the extension talks to the API](#how-the-extension-talks-to-the-api)
  - [Extension error handling](#extension-error-handling)
- [MCP Server Tools Reference](#mcp-server-tools-reference)
  - [Running the MCP gateway](#running-the-mcp-gateway)
  - [Tool reference (18 tools)](#tool-reference)
  - [Configuring an MCP client](#configuring-an-mcp-client)
- [CLI / Script Toolbox](#cli--script-toolbox)
- [Python SDK Surface](#python-sdk-surface)
- [Other App Surfaces](#other-app-surfaces)
- [Extending the Platform](#extending-the-platform)

---

## VS Code Extension

Source: `apps/vscode-extension/` (`extension.js`, `package.json`, `mcp-client.js`).

**What it does.** The "EOIP Context" extension (`package.json` name `eoip-context`,
display name `EOIP Context`, version `0.1.0`, publisher `eoip-local`) is a **read-only**
IDE surface over your local EOIP deployment. It searches the knowledge graph, shows
context for the active source file, traces requirement-to-code paths, and explores
impact/lineage — it never edits files and refuses write/admin MCP tools.

> Note: the task brief mentions "10 commands", but `apps/vscode-extension/package.json`
> actually contributes **19 commands** (its README confirms "the command catalog has
> grown beyond the original ten-command fixture suite"). All 19 are documented below.

### Install and run the extension

**Step by step**

1. Build the VSIX package from the `deploy/` directory (container-oriented build):
   ```
   docker compose --profile tools run --build --rm extension-build
   ```
   or via the wrapper: `scripts/container.ps1 extension` (Windows PowerShell).
2. In VS Code run **Extensions: Install from VSIX…** and select
   `dist/eoip-context-0.1.0.vsix`.
3. Run **EOIP: Set Access Token** and paste the `EOIP_API_TOKEN` value from
   `deploy/.env`. The token is stored in VS Code **SecretStorage** (key `eoip-token`),
   never in settings.
4. Set `eoip.repositoryRoot` to the local checkout matching the ingested repository
   (for example `eoip/demo/demodata/core/demo-repo`).

For development (run from source): open `apps/vscode-extension/` in VS Code and press
F5, or run the acceptance suite with `npm test` (uses `@vscode/test-electron`; set
`VSCODE_EXECUTABLE` to an installed Code binary to skip the download).

**Errors and recovery.** `npm test` failures write a JSON receipt under the repo's
ignored `test-results/` directory; a nonzero host exit or missing receipt fails the
gate. The `npm run package` script outputs to `/output/...`, which only exists inside
the build container — do not run it bare on Windows.

### Configuration settings

From `package.json → contributes.configuration` (title `EOIP`):

| Setting | Default | Purpose |
|---|---|---|
| `eoip.mcpUrl` | `http://localhost:8001/mcp` | Local stateless JSON Streamable HTTP MCP endpoint |
| `eoip.apiUrl` | `http://localhost:8000` | URL of your local EOIP API |
| `eoip.repositoryRoot` | `""` | Local root matching the ingested repository |

### Command reference

All titles are exact strings from `package.json`. Every command is registered in
`extension.js` via a `command(name, action)` wrapper that catches errors, shows them
with `vscode.window.showErrorMessage`, and returns `{ok:false, code, message}`.

**EOIP: Set Access Token** (`eoip.setToken`) — prompts (password-masked) for
`EOIP_API_TOKEN` and stores it in SecretStorage. Run this first; every other command
fails with `EOIP_AUTH_REQUIRED` ("Run EOIP: Set Access Token first.") otherwise.

**EOIP: Natural Language Query** (`eoip.nlq`) — prompts for a question (default value
`What is the impact of PAY-202?`) and POSTs `{question}` to `/api/v1/query/nl`. Shows
the full JSON result (interpretation, answer, warnings, results) in a read-only editor.
Throws `EOIP_INVALID_QUESTION` for empty input, `EOIP_INVALID_RESPONSE` when the
server returns no `interpretation`.

**EOIP: Read-only MCP Tool** (`eoip.mcp`) — quick-picks one of `search`,
`jira_issue`, `code_symbol`, prompts for a query (default `PAY-202`), then calls the
tool via `mcp-client.js` against `eoip.mcpUrl`. Only tools in the client allowlist
(see [How the extension talks to the API](#how-the-extension-talks-to-the-api)) are
permitted; anything else raises "Only approved read-only MCP tools can be called."

**EOIP: Search Knowledge Graph** (`eoip.search`) — prompts for an issue key, symbol,
or source path; GETs `/api/v1/search?q=…`; you pick an entity from a quick-pick; the
extension then GETs `/api/v1/entities/{id}` and shows it as JSON.

**EOIP: Context for Active File** (`eoip.context`) — reveals the **EOIP Context**
Explorer view (`eoip.contextView`) and resolves the symbol under the caret (preferring
the language server's document symbols, falling back to the word at the cursor). It
searches `/api/v1/search?q=…&label=CodeSymbol&limit=50`, matches by
`properties.path`/`name`/`qualified_name`, then fetches `/api/v1/impact`
(`max_depth: 4, result_limit: 100`) and `/api/v1/lineage` (`max_depth: 3,
result_limit: 50`) in parallel. The tree shows "Current symbol: …", "Graph context
(n)" grouped by node label with `via EDGE → EDGE` route descriptions, and
"Provenance and evidence (n)". Truncated traversals add a "Results are truncated by
the configured traversal budget." row; server warnings appear as `Warning: …` rows.
The view also auto-refreshes (350 ms debounce) when you move the caret to a different
symbol.

**EOIP: Explore Impact** (`eoip.impact`) — POSTs `/api/v1/impact` with
`{canonical_id, max_depth: 4}` for the selected/current entity and shows the JSON.
Requires a selection: error `EOIP_ENTITY_REQUIRED`.

**EOIP: Trace Requirement to Code** (`eoip.path`) — prompts for a Jira issue key or
source canonical ID (placeholder "For example, EOIP-1"), lets you pick the source
entity, then POSTs both `/api/v1/path` (`{source_id, target_id, max_depth: 8}`) and
`/api/v1/impact` for the target, and shows `{source, target, path, impact}`.

**EOIP: Trace Provenance / Lineage** (`eoip.lineage`) — prompts for a canonical ID
(default: current selection) and POSTs `/api/v1/lineage` with `max_depth: 4`.

**EOIP: GraphRAG Retrieval** (`eoip.retrieval`) — prompts for a canonical ID and a
question (default `Explain the implementation and its evidence`), then POSTs
`/api/v1/rag` with `{canonical_id, question, synthesize: false}`.

**EOIP: Open Symbol Source** (`eoip.openSource`) — opens the workspace file for an
indexed symbol at its `start_line`/`end_line`/`start_column`/`end_column` range.
Strictly path-safe: absolute indexed paths, `..` traversal, and symlinks escaping
`eoip.repositoryRoot` are refused with `EOIP_UNSAFE_SOURCE_PATH`.

**EOIP: Why Does This Code Exist?** (`eoip.why`) — runs lineage (`max_depth: 3`) and
filters nodes to labels `WorkItem`, `Requirement`, `ArchitectureDecisionRecord`,
`ADR`, `Commit`; shows `{action: "WHY", target, rationale, paths, evidence}`.

**EOIP: What Changed?** (`eoip.whatChanged`) — runs impact (`max_depth: 3`) filtered
to `Commit`, `PullRequest`, `SemanticChangeJournal`, `Release`; shows
`{action: "WHAT_CHANGED", changes, evidence}`.

**EOIP: Where Used?** (`eoip.whereUsed`) — runs impact (`max_depth: 4`) filtered to
`CodeSymbol`, `Service`, `APIService`, `Endpoint`, `TestCase` (excluding the node
itself); shows `{action: "WHERE_USED", usages, paths}`.

**EOIP: Connected Runtime Services & Deployments** (`eoip.services`) — impact
(`max_depth: 4`) filtered to `Service`, `Deployment`, `APIService`, `Microservice`;
shows `{command: "RUNTIME_SERVICES", connected_services}`.

**EOIP: Architecture Conformance Findings** (`eoip.conformance`) — impact
(`max_depth: 3`) filtered to `ArchitectureRule`, `ConformanceViolation`,
`ArchitectureViolation`, `Rule`; shows `conformance_status: "CONFORMANT"` when no
findings, else `"VIOLATIONS_FOUND"` with the finding nodes. Note this is a
graph-neighborhood heuristic, not a full conformance engine run.

**EOIP: Impacted Tests** (`eoip.impactedTests`) — impact (`max_depth: 4`) filtered to
`TestCase`, `TestSuite`, `TestRun`; shows `impacted_test_count` and the test nodes.

**EOIP: Relevant Incidents & Errors** (`eoip.incidents`) — impact (`max_depth: 4`)
filtered to `Incident`, `ErrorSignature`, `Alert`, `Vulnerability`; shows
`incident_count` and nodes.

**EOIP: Decision / ADR Rationale** (`eoip.adrRationale`) — impact (`max_depth: 3`)
filtered to `ArchitectureDecisionRecord`, `ADR`, `Decision`, `DocumentSection`.

**EOIP: Bounded Semantic Telemetry Summary** (`eoip.telemetrySummary`) — impact
(`max_depth: 2`) filtered to `SemanticTelemetry`, `ServiceMetricSummary`,
`MetricWindow`. Passing `{rawStream: true}` or `{unrestricted: true}` is refused with
`EOIP_RAW_TELEMETRY_REFUSED` ("Unrestricted raw telemetry streams are disallowed in
the editor."). If the graph has no telemetry nodes the command returns a **synthetic
placeholder** metric (`latency_p95_ms = 42.5, sample_count: 1000, status: "NORMAL"`)
— treat that exact payload as illustrative, not real telemetry.

### How the extension talks to the API

All API traffic goes through the internal `call(endpoint, body)` helper in
`extension.js`:

- Reads the token from SecretStorage (`eoip-token`) — missing → `EOIP_AUTH_REQUIRED`.
- Builds the URL from `eoip.apiUrl`; non-HTTP/HTTPS URLs → `EOIP_INVALID_API_URL`.
- GET when no body, POST with `Content-Type: application/json` otherwise; always sends
  `Authorization: Bearer <token>`; 60-second request timeout.
- Responses over 4 MB are rejected (`EOIP_RESPONSE_TOO_LARGE`); non-JSON →
  `EOIP_INVALID_RESPONSE`; HTTP ≥ 400 → `EOIP_HTTP_<status>` with the server's
  `detail` message; network failure → `EOIP_OFFLINE`; timeout → `EOIP_TIMEOUT`.
- A status-bar item shows `$(graph) EOIP` when `/health/ready` succeeds at activation
  and `$(debug-disconnect) EOIP offline` (warning background) otherwise; connectivity
  is re-evaluated after every call. Commands stay read-only and never block editing.
- The MCP command uses `mcp-client.js`, which performs a real JSON-RPC exchange:
  `initialize` (protocol `2024-11-05`) → `notifications/initialized` → `tools/list`
  → `tools/call`, all POSTs to `eoip.mcpUrl` with the same Bearer token. Its
  client-side allowlist is exactly:
  `search, entity, path, impact, lineage, neighbors, document, code_symbol,
  jira_issue, evidence, query`.

### Extension error handling

Coded errors you may see and what to do:

- `EOIP_AUTH_REQUIRED` — run **EOIP: Set Access Token**.
- `EOIP_OFFLINE` / `EOIP_TIMEOUT` — API unreachable; check the deployment and
  `eoip.apiUrl`. The context view retains the last successful context.
- `EOIP_SYMBOL_NOT_FOUND` — no indexed `CodeSymbol` matched; ingest the repository
  first, or check `eoip.repositoryRoot` points at the same tree that was ingested.
- `EOIP_SOURCE_OUTSIDE_REPOSITORY` — the active file is outside
  `eoip.repositoryRoot`; fix the setting.
- `EOIP_ENTITY_REQUIRED` / `EOIP_SOURCE_REQUIRED` — open a source symbol or select an
  entity via **EOIP: Search Knowledge Graph** first.
- `EOIP_UNSAFE_SOURCE_PATH` — indexed path escapes the repository root; refused by
  design.
- `EOIP_INVALID_MCP_ARGUMENTS` — pass `{tool: string, arguments: object}`.

---

## MCP Server Tools Reference

Source: `apps/mcp/main.py` (FastMCP app factory `create_app`), `apps/mcp/README.md`.

**What it does.** The MCP gateway is a read-oriented facade: each tool delegates to
the EOIP REST API with the deployment token rather than owning graph storage. Every
tool response is passed through `eoip.agents.uncertainty_protocol.annotate_mcp_payload`
(KGR-G-019), so payloads carry a calibrated uncertainty envelope. The server enforces a
constant-time Bearer-token check (`hmac.compare_digest`) on every route except
`/health/live`.

### Running the MCP gateway

The default Compose profile serves `/mcp` on host port **8001**. For host development
with an already-running API:

```powershell
$env:EOIP_API_URL = 'http://127.0.0.1:8000'
python -m uvicorn apps.mcp.main:create_app --factory --host 127.0.0.1 --port 8001
```

Environment: `EOIP_API_URL` (default `http://eoip-api:8000`), and the token from
`eoip.runtime.api_token()`. Transport security allowlists hosts `localhost:*`,
`127.0.0.1:*`, `eoip-mcp:*` and origins `http://localhost:*`, `http://127.0.0.1:*` —
review before any non-local deployment. Upstream API errors surface as MCP errors with
the HTTP status code ("EOIP API error 404: …"); connectivity failures surface as code
503 "EOIP API unavailable".

### Tool reference

All 18 tools registered in `apps/mcp/main.py`, with the REST call each one makes:

| Tool | Parameters (defaults) | Calls |
|---|---|---|
| `search` | `q: str, limit=25` | `GET /api/v1/search` |
| `entity` | `canonical_id: str` | `GET /api/v1/entities/{id}` |
| `path` | `source_id, target_id, max_depth=8` | `POST /api/v1/path` |
| `impact` | `canonical_id, max_depth=4` | `POST /api/v1/impact` |
| `lineage` | `canonical_id, max_depth=4, result_limit=100` | `POST /api/v1/lineage` |
| `trace_impact` | `canonical_id, max_depth=4` | `POST /api/v1/agents/trace-impact` |
| `list_agents` | — | `GET /api/v1/agents` |
| `run_agent` | `agent_id, goal, context_refs=None, dry_run=false, synthesize=false` | `POST /api/v1/agents/{id}/runs` |
| `agent_explanation` | `run_id` | `GET /api/v1/agents/runs/{id}/explanation` |
| `blast_radius` | `canonical_id, max_depth=4` | `POST /api/v1/graph/blast-radius` |
| `graph_surprises` | `limit=20` | `POST /api/v1/graph/surprises` |
| `validate_ontology` | — | `POST /api/v1/admin/validation` (empty body) |
| `neighbors` | `canonical_id, max_depth=1, result_limit=50` | `POST /api/v1/neighborhood` |
| `document` | `canonical_id` | `GET /api/v1/entities/{id}` |
| `code_symbol` | `qualified_name` | `GET /api/v1/search` (limit 5) |
| `jira_issue` | `issue_key` | `GET /api/v1/search` (limit 5) |
| `evidence` | `canonical_id` | `POST /api/v1/lineage` (depth 2, limit 50) |
| `query` | `plan: dict` | `POST /api/v1/query` |

**Returns.** Each tool returns the upstream API JSON (nodes/edges/paths/evidence for
graph tools; agent run descriptors for agent tools) annotated with the uncertainty
envelope. `run_agent` is explicitly constrained: "mutations can only be returned as
inert proposals" — the gateway is not a write path.

**Example JSON-RPC call** (`tools/call` against `http://localhost:8001/mcp`, after the
initialize/initialized handshake):

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "jira_issue",
    "arguments": { "issue_key": "EOIP-123" }
  }
}
```

Headers: `Authorization: Bearer <EOIP_API_TOKEN>`,
`Accept: application/json, text/event-stream`, and `MCP-Protocol-Version` echoing the
version returned by `initialize`. A 401 response body is
`{"detail": "A valid Bearer token is required"}`.

### Configuring an MCP client

Point any Streamable-HTTP MCP client at `http://localhost:8001/mcp` with the Bearer
token. Discover the live catalog with `tools/list` rather than hardcoding — the README
warns that "tool discovery is not a guarantee that every backend/profile can execute a
capability." Focused transport tests:
`python -m pytest tests/integration/test_mcp_transport.py tests/integration/test_external_mcp_bridge.py -q`.

> Do not confuse this server with EOIP's **external MCP client**
> (`packages/eoip/tools_contract/mcp_bridge.py`, configured via the "External MCP
> Configuration" section of `docs/api-reference.md`) — that is the opposite direction
> (EOIP calling out to third-party MCP servers). Also note the gateway uses one
> deployment credential downstream; per `apps/mcp/README.md` it "is not currently a
> general per-user OAuth delegation service."

---

## CLI / Script Toolbox

All scripts run as modules from the repository root (`python -m scripts.<name>`).
The container wrapper `scripts/container.ps1` (Windows) / `scripts/container.sh`
auto-detects Docker, Podman, nerdctl, Finch, or lima-nerdctl (override with
`$env:EOIP_CONTAINER_RUNTIME` / `$env:EOIP_COMPOSE_COMMAND`).

### container.ps1 commands

Validated actions (`scripts/container.ps1 <action>`):

- `up` — build + start, `compose up --build -d --wait` (must run first; every other
  action throws "Run scripts/container.ps1 up once to initialize the local
  configuration." if local config is missing)
- `rebuild` — no-cache rebuild
- `status`, `logs`, `down` — health, logs, stop
- `backup` — runs `python -m scripts.backup` inside `eoip-api`
- `backup-bundle` — `--profile tools run --rm --no-deps bundle-backup`
- `extension` — builds the VS Code extension VSIX
- `demo-data`, `test`, `hubble-local-admin`
- `restore-test`, `acceptance`, `recovery-acceptance`, `dlq-acceptance` — acceptance
  suites using dedicated compose files (e.g. `deploy/docker-compose.acceptance.yml`)
- `detect`, `info` — print detected runtime info

### Backup and restore

```
python -m scripts.backup [--output PATH] [--bundle --model-dir DIR]
                         [--config-dir config] [--max-bytes N]
python -m scripts.restore SOURCE.zip [--config-dir DIR --model-dir DIR] [--max-bytes N]
```

- Plain backup writes a quiescent graph + raw-evidence JSON (default
  `<data_root>/backups/eoip-<UTC timestamp>.json`); `--bundle` produces a `.zip`
  recovery bundle including config and local model bytes, and **requires
  `--model-dir`** ("an absent directory represents no installed models").
- Bundle restore requires explicit empty `--config-dir` and `--model-dir` targets and
  refuses otherwise: "Restore into an empty, isolated EOIP deployment."
- Both emit audit events (`backup_intent` / `restore_intent`, actor `local-operator`)
  through `eoip.audit.sink.AuditSink`.

### Benchmark

```
python -m scripts.benchmark --run smoke --store memory
python -m scripts.benchmark --run full --store configured --prepare-configured
```

Runs the versioned graph benchmark from manifest `config/benchmarks/mvp-v1.json` and
emits an evidence report (nearest-rank latency percentiles). `--prepare-configured` is
deliberately guarded: the configured graph must be empty; use only with an isolated
HugeGraph deployment. Related: `scripts/benchmark_data.py`, `scripts/llm_benchmark.py`.

### KGCI / gap coverage

There is **no script literally named "kgci"** in `scripts/`. The KG-CI capability
(requirements GAP-KGCI-001/002/003, per the module docstring) is delivered by
`scripts/gap_coverage.py`:

```
python -m scripts.gap_coverage --project-root . --output gap-coverage.json \
    [--doc-set gap|g2] [--fail-on-planned-p0] [--fail-on-gate ...]
```

It builds a machine-readable GAP requirement coverage report from
`eoip.gaps.coverage.build_gap_coverage_report`; `--fail-on-planned-p0` exits 1 when any
P0 GAP requirement has no code/test evidence (that is the CI fail-on-regression gate).

### Demo reset

```
python -m scripts.demo_reset --confirm [--data-dir /data]
```

Clears the graph, raw evidence, DLQ and state, re-bootstraps schema and meta-graph,
then reloads demo fixtures. `--confirm` is mandatory. Only for backends that permit
deletion — HugeGraph requires a disposable deployment.

### Smoke test

`scripts/smoke_test.py` (run inside the Compose network) checks persisted data, worker
replay, policies, web, and MCP against `EOIP_API_URL` (default
`http://eoip-api:8000`). Auth: if `EOIP_ADMIN_USERNAME`/`EOIP_ADMIN_PASSWORD` are set
it logs in via `POST /api/v1/auth/login` and uses the returned token; otherwise it
falls back to the raw `EOIP_API_TOKEN`. Container variant: `scripts/ci/container_smoke.sh`.

---

## Python SDK Surface

The installable package is `eoip` (source under `packages/eoip/`, installed editable in
this repo). Two distinct things live under `packages/eoip/sdk/`:

- `eoip.sdk` (`__init__.py`) — an internal "API excellence layer" exporting
  `APIGateway`, `GatewayQuery`, `GatewayResult`, `RateLimiter`, `RateLimitPolicy`,
  `SchemaType`, `SchemaField`, `FieldNode`, `get_api_gateway` (a GraphQL-style flexible
  query gateway with rate limiting and schema introspection).
- `eoip.sdk.python_client.EOIPClient` — the typed HTTP client SDK (docstring: proposed
  package `eoip-python`, CRA-039.6) with `AuthenticationError`, `NotFoundError`,
  `GovernanceViolationError`. Constructor:
  `EOIPClient(base_url="http://localhost:8000", api_token=None, timeout=30.0)`.

For in-process programmatic use, import the same building blocks the apps use:

```python
# Graph store (memory backend by default; EOIP_GRAPH_BACKEND selects)
from eoip.runtime import create_store, data_root, api_token
store = create_store()

# Query execution with validated query plans
from eoip.contracts.query_plan import QueryPlan
from eoip.query.executor import QueryExecutor
plan = QueryPlan(...)            # validated contract
results = QueryExecutor(store).execute(plan)

# Agents (deterministic, governed)
# MCP tools call POST /api/v1/agents/trace-impact; in-process equivalents live under
from eoip.agents.uncertainty_protocol import annotate_mcp_payload

# Ingestion / demo corpus
from eoip.demo import load_demo
load_demo(store, data_root(), project_root=".")
```

Relevant packages to explore: `eoip.store`-equivalent via `eoip.runtime.create_store`,
`eoip.query`, `eoip.agents`, `eoip.ingestion` / `eoip.ingest`, `eoip.connectors`,
`eoip.contracts`. *(Import snippets source-verified only; run them inside the repo
venv, e.g. `.venv/Scripts/python`, with `packages/` on the path.)*

---

## Other App Surfaces

Honest notes on what these are versus the main `apps/web` + `apps/api` application:

- **`backend/server.py`** — a *supervisor entrypoint shim*, not a second product. It
  puts the repo root on `sys.path`, provisions the first admin from
  `EOIP_ADMIN_USERNAME`/`EOIP_ADMIN_PASSWORD(_FILE)` (no committed default token or
  account; the app "refuses to start" with no principal), defaults
  `EOIP_DATA_DIR` to `.eoip-data`, `EOIP_GRAPH_BACKEND=memory`, and
  `EOIP_LOAD_DEMO=true` only when `EOIP_ENV=dev`, then re-exports
  `apps.api.main.create_app()` as `app` and best-effort seeds the demo graph. The
  supervisor runs `uvicorn server:app` from `/app/backend` on port 8001.
- **`frontend/`** — a substantial *alternate* React/TypeScript prototype
  (`knowgridflow-web`, React 19.1.1, Vite 6, TanStack Query, sigma/graphology,
  Tailwind 4) with its own screens (overview, Ask, graph/entity, query, ingestion,
  ontology, quality, agents, reports, governance, tenancy, health, temporal). The
  deployed/CI-tested UI is `apps/web`; "changes here do not automatically update that
  deployed UI." Dev: `$env:REACT_APP_BACKEND_URL='http://127.0.0.1:8000'; npm --prefix
  frontend run dev`. Known adoption blocker (from its README): `lib/auth.tsx`
  fabricates a bootstrap-admin principal when identity lookup fails — do not treat it
  as authenticated.
- **`eopisuite/multi/`** — documentation only (15 handbook files), the multi-repo
  extraction plan ("EOIP suite" under the `AvyukthiAI` GitHub org). It contains no
  runnable code.
- **`reva/` + `packages/reva/`** — REVA (Reverse-engineering, Evidence, Verification &
  Assurance) is an optional component. `packages/reva/__init__.py` is just a proxy
  re-exporting the root `reva` package. The API factory mounts `reva_router` at
  `/api/reva/v1` **only when `REVA_ENABLED=true`** (default false). Per
  `reva/README.md`: the host factory mounts the router but does not call
  `set_api_kernel(...)` or `register_reva_error_handlers(...)`, so without extra
  initialization the warrants API returns HTTP 503; `/api/reva/v1/health` is a static
  unauthenticated response that "does not establish database, key, kernel,
  authorization or worker readiness." Do not treat a mounted router as an integrated
  service. Scripts live in `scripts/reva/` (e.g. `run_lane.py`, `build_reva_ledger.py`,
  `airgap_preflight.py`).

---

## Extending the Platform

### Connector protocol

Implement `eoip.connectors.base.SourceConnector` (`packages/eoip/connectors/base.py`),
a `runtime_checkable` Protocol — "the only interface source adapters expose to the
common pipeline" (FR-CONN-001). Methods to implement:

```python
class MyConnector:
    source_id: str
    def capabilities(self) -> SourceCapabilities: ...
    def discover(self, scope: DiscoveryScope) -> DiscoveryResult: ...
    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]: ...
    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]: ...
    def handle_event(self, event: dict) -> Iterator[SourceEventV2]: ...
    def fetch_record(self, ref: str) -> SourceEventV2: ...
    def health(self) -> ConnectorHealth: ...        # HEALTHY | DEGRADED | UNAVAILABLE | MISCONFIGURED
    def replay(self, events) -> Iterator[SourceEventV2]: ...
```

Contract models (`extra="forbid"`): `DiscoveryScope` (include/exclude lists, max 1000),
`DiscoveredResource`, `DiscoveryResult`. ~35 existing connectors in the same package
(`jira.py`, `github.py`, `confluence.py`, `kubernetes.py`, `servicenow.py`, …) are the
reference implementations; register via `eoip.connectors.registry` / `factory.py`.

### Plugins

`packages/eoip/plugins/` provides the runtime. A plugin is a directory containing
`plugin.json` (discovered recursively by `PluginDiscovery` in `loader.py`). The signed
manifest (`plugins/manifest.py`, CRA-002.3/4) requires `manifest_version`,
`plugin_id`, `publisher_identity`, plus dependencies, permissions
(`PluginPermission(resource, scope, description)` — e.g. resources `graph_read`,
`graph_write`, `network`, `filesystem`, `models`), a config schema, migrations, and an
uninstall policy (`retain`/`delete`/`archive`). Enforcement: SHA-256 digest
verification of all plugin contents, Ed25519 signature verification, and declarative
config validation that rejects `eval`/`exec`/`__import__`/`os.system`/`subprocess`,
shell metacharacters, and `module:function` references. Build against
`eoip.plugins.sdk` (`PluginManifest`, `PluginCapability`, `PluginPermission`).

### Marketplace packaging flow

`packages/eoip/marketplace/` (GAP-MKT-001/002): a package is a `.eoipkg` zip archive
containing `manifest.json` (a `PackageManifest`), payload files under `payload/`, and
`checksums.json` (SHA-256 of every member), optionally signed via
`eoip.marketplace.signing`.

```python
from eoip.marketplace.manifest import PackageManifest, CapabilityKind
from eoip.marketplace.packager import build_package

manifest = PackageManifest(
    id="urn:eoip:marketplace:package:checkout-analytics",
    name="checkout-analytics",          # ^[a-z0-9][a-z0-9_-]*$
    version="1.0.0",                    # strict SemVer
    platforms=["any"],
    provides={CapabilityKind.QUERY_TEMPLATES: ["checkout-impact"]},
    dependencies=[],                    # PackageDependency(name, range=">=1.0.0,<2.0.0")
)
archive_bytes = build_package(manifest, {"templates/checkout-impact.json": b"..."})
```

Capability kinds: `ontologies`, `mappings`, `query_templates`, `validators`,
`agent_workflows`, `dashboards`. `build_package` raises `PackageBuildError` on empty
payloads, path collisions, or reserved names. Install side: `installer.py`,
`registry.py`, `semver.py` range checking.

### Domain pack authoring

Domain packs live in `config/domain-packs/<name>/` with two files:

- `pack.yaml` — `name`, `version`, `extends: core`, and a description.
- `ontology.yaml` — `ontology_version`, `schema_version`, `domains:` list, and
  `classes:` entries. A class has `description`, optional `extends_core: true`,
  `properties:` (`name: TYPE` with types like `TEXT`, `INT`), and `relationships:`
  with `out:`/`in:` target-class lists.

Eight shipped examples: `bfsi`, `compliance`, `cybersecurity`, `data-governance`,
`healthcare`, `itsm`, `manufacturing`, `software-engineering`. Minimal example
(adapted from `software-engineering`):

```yaml
# pack.yaml
name: checkout-domain
version: "1.0.0"
extends: core
description: Checkout service pack for the t-001 demo tenant.
```

```yaml
# ontology.yaml
ontology_version: "0.4.0"
schema_version: "1.2"
domains: [WORK, CODE]
classes:
  CheckoutRun:
    description: A checkout pipeline execution.
    properties:
      run_id: TEXT
      canonical_id: TEXT
    relationships:
      TRIGGERED_BY:
        out: [CheckoutRun]
        in: [WorkItem]
```

Load/validate behavior is exercised through `POST /api/v1/admin/validation` (also the
MCP `validate_ontology` tool). *(Exact hot-load mechanism for new packs was not
runtime-verified for this chapter.)*
