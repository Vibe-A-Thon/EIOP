# Local Docker deployment

This deployment runs the implemented EOIP slice against Apache HugeGraph/RocksDB.
Runtime services use persisted graph data; the in-memory store is used by unit
tests only. The wider engineering package includes future phases and capabilities
that are not all implemented by this deployment.

## Start and connect

Use Docker Desktop with Linux containers. The first build downloads images and
dependencies; subsequent builds use Docker's cache. Allow several minutes for
the first schema bootstrap and demo ingestion.

From the repository root in PowerShell:

```powershell
.\scripts\docker.ps1 up
.\scripts\docker.ps1 status
```

If PowerShell blocks scripts under your execution policy, invoke the same file
with `powershell -ExecutionPolicy Bypass -File .\scripts\docker.ps1 up`.

The script resolves Docker Desktop's per-user or system installation and adds
its CLI/credential helper directory to the process PATH. It creates
`deploy/.env` with random API and graph credentials. Keep that file local.
The graph admin password is initialized with the graph; changing the environment
value later is not a graph password-rotation procedure.

| Interface | Address | Access |
|---|---|---|
| Knowledge explorer | http://localhost:8080/app | Paste EOIP_API_TOKEN into the login form |
| Administration | http://localhost:8080/admin | Same local token |
| Swagger API | http://localhost:8000/docs | Click Authorize and paste EOIP_API_TOKEN |
| Read-only MCP | http://localhost:8001/mcp | Authorization: Bearer EOIP_API_TOKEN |
| API readiness | http://localhost:8000/health/ready | No token |

All published application ports bind to `127.0.0.1`. This is a local development
authentication model: one token grants access to both query and administration
operations. `/admin` is navigation, not a separate authorization boundary.

Change `EOIP_WEB_PORT`, `EOIP_API_PORT`, or `EOIP_MCP_PORT` in `deploy/.env` if a
port is occupied, then rerun startup. The API docs link in the web interface
uses the default API port; visit the configured port directly if changed.

For direct Compose use, ensure Docker and its credential helper are on PATH:

```powershell
cd deploy
docker compose --env-file .env up --build -d --wait --wait-timeout 420
```

## Services and storage

| Service | Responsibility |
|---|---|
| hugegraph-server | HugeGraph 1.7.0 with RocksDB; no host port |
| schema-init | One-time, idempotent property/vertex/edge/index bootstrap |
| eoip-api | Search, entities, bounded path/impact, graph retrieval, admin jobs/validation, metrics |
| eoip-worker | Single-worker durable filesystem queue; capture-first ingestion and demo loading |
| eoip-web | Built React SPA served by Nginx; same-origin API proxy |
| eoip-mcp | Authenticated, read-only MCP façade over the application API |

Docker named volumes hold graph storage and application raw events, DLQ,
job records, worker state, and snapshots. `docker.ps1 down` removes this project's
containers and networks while retaining volumes. Startup resumes interrupted
RUNNING jobs and retries transient I/O/HTTP failures three times. Keep one worker
replica: the filesystem queue does not implement multi-worker claiming.

The backend network is internal. Graph, worker, schema bootstrap, and local
model services have no external gateway. Published web/API/MCP services also join
a frontend network because Docker Desktop does not publish localhost ports for
services attached only to an internal network. Strict host-wide egress blocking
requires an additional firewall policy; this Compose file does not claim it.

## Exercise the demo

1. Wait until the DEMO job shows SUCCEEDED in Administration. Refresh counts.
2. Search for `EOIP-1`, `compute_impact`, a file name, or the demo commit SHA.
3. Select a symbol. Its canonical ID fills the target field. Use the default
   source `urn:eoip:work:item:jira:EOIP-1` and choose **Find path**.
4. Inspect `IMPLEMENTS → MODIFIES → DECLARES` and each source reference.
5. Use **Explore impact** and **Run TraceImpact** for bounded connected evidence.
6. In Administration, run validation, import a Jira JSON export, or replay the
   demo. Replay preserves logical business entity identities; ingestion-run
   history and run relationships deliberately accumulate.

`EOIP_LOAD_DEMO=false` starts an empty system. The admin **Load / replay demo**
operation remains available. Raw events are captured before graph mutation;
invalid Jira records are retained in the DLQ. A job result with rejected records
is PARTIAL. File imports are limited to 3 MB in the web UI and 4 MB at the API.

## Automated checks

```powershell
.\scripts\docker.ps1 test
```

Run startup first. The test command builds test images, runs Python tests inside
Linux, runs the real-stack smoke test, and then runs Chromium UI tests inside a
Playwright container. The browser image is a substantial first-time download.

The smoke test checks API authorization/limits, worker completion and replay,
Jira-to-code paths, impact, evidence, schema validation, model-unavailable
retrieval, the web service, and actual MCP initialization/list/call operations.
UI tests check valid/invalid login, symbol search, path visualization, agent
evidence, and administration validation. Screenshots are saved under the
Git-ignored `test-results/`.

Local Python development remains available with `python -m pytest` from the repository root.
`requirements.lock` pins the runtime versions verified in the Linux image;
`pyproject.toml` describes portable development dependencies.

## Backup and restore

Avoid submitting admin writes during backup. This command stops the worker,
exports a checksummed logical graph and raw/DLQ evidence, and restarts the worker:

```powershell
.\scripts\docker.ps1 backup
.\scripts\docker.ps1 restore-test
```

The output path is inside `/data/backups/`. Copy a snapshot to the host using
`docker compose -f deploy/docker-compose.yml --env-file deploy/.env cp
eoip-api:/data/backups/FILE.json ./FILE.json` as a single command.

`restore-test` restores the newest snapshot into a disposable, separate HugeGraph
container, checks vertex/edge counts and the Jira-to-symbol evidence path, then
removes that test graph container. The main deployment and its volumes remain
available. Run backup before this command.

For restore, create a separate Compose project with separate ports and
`EOIP_LOAD_DEMO=false`. Start HugeGraph and schema-init, leave the worker stopped,
and mount/copy the snapshot into an application container. Run:

```text
python -m scripts.restore /data/backups/FILE.json
```

Restore checks the checksum, schema version, endpoint types, and evidence paths
before mutation, and requires an empty graph. It never clears an existing graph.
The local logical export is intended for small, quiescent development datasets;
it is not a transaction-consistent production RocksDB backup. Job history is not
restored, so pending imports cannot resume automatically from the snapshot.
Use supported native HugeGraph backup tooling for production-sized graphs.

## VS Code extension

```powershell
.\scripts\docker.ps1 extension
```

Docker packages `apps/vscode-extension/dist/eoip-context-0.1.0.vsix`.
Install it using **Extensions: Install from VSIX**, then run **EOIP: Set Access
Token**. The token is stored in VS Code SecretStorage. Search, context, path,
impact, and source-opening commands are read-only. Set `eoip.repositoryRoot` to
the local ingested repository for navigation. The extension runs on the host
inside VS Code, not as a web container.

## Optional local generation and metrics

The `ai` profile runs Ollama; the `observability` profile runs Prometheus on
localhost:9090. Neither is needed for graph search or traversal.

```powershell
cd deploy
docker compose --profile observability up -d prometheus
docker compose --profile ai up -d local-model
```

The local model has no outbound network access. Stage an approved model into the
`eoip_model-data` volume using an isolated temporary Ollama container on a network
with download access, or import a pre-staged volume. Set `EOIP_OLLAMA_MODEL` in
`.env` and recreate `eoip-api`. POST `/api/v1/rag` with `canonical_id`, `question`,
and `synthesize: true` to request optional local synthesis. Evidence is returned
independently if the model is absent or unavailable. No cloud model endpoint is
used. Model downloads and generated-answer quality require separate evaluation.

## Implementation boundaries

HugeGraph physical edge names encode logical relation plus endpoint label pair,
because each HugeGraph edge label has one source/target type. The REST/MCP query
interfaces return the original ontology relationship names. Canonical IDs map to
deterministic string vertex IDs. The adapter enforces required vertex properties
and endpoint constraints; timestamp properties retain ISO-8601 text.

Search scans at most 5,000 candidate vertices; traversal bounds depth, returned
results, visits, and elapsed time, with per-request graph timeouts. Validation
checks at most 10,001 records per collection and reports partial coverage. These
are local-development limits, not large-dataset performance claims.

The deployment does not complete every engineering-package acceptance criterion.
Remaining work includes incremental multi-commit Git synchronization/deletion,
checkpoint reconciliation, DLQ inspection/replay UI, richer temporal reconstruction,
full audit retention/redaction policy, advanced identity resolution, all requested
MCP domain tools, model-quality evaluation, production backup tooling, distributed
queue/HA, fine-grained authorization, and later-phase enterprise connectors.

Schema/REST implementation references: [Apache HugeGraph quick start](https://hugegraph.apache.org/docs/quickstart/hugegraph/hugegraph-server/),
[vertex REST API](https://hugegraph.apache.org/docs/clients/restful-api/vertex/),
[edge REST API](https://hugegraph.apache.org/docs/clients/restful-api/edge/).
