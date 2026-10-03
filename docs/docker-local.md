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
| eoip-api | Search, QueryPlan execution, entities, bounded path/impact/lineage, GraphRAG retrieval, agent contracts, admin jobs/validation/ingestion, metrics |
| eoip-worker | Single-worker durable filesystem queue; capture-first ingestion and demo loading |
| eoip-web | Built React SPA served by Nginx; same-origin API proxy |
| eoip-mcp | Authenticated, read-only MCP façade over the application API |

Docker named volumes hold graph storage and application raw events, DLQ,
job records, worker state, and snapshots. `docker.ps1 down` removes this project's
containers and networks while retaining volumes. Startup resumes interrupted
RUNNING jobs and retries transient I/O/HTTP failures three times. Keep one worker
replica: the filesystem queue does not implement multi-worker claiming.

### Schema compatibility and startup refusal

Schema bootstrap reads all four schema collections before making any changes.
It refuses incompatible property types/cardinality, vertex ID strategies/primary
keys, edge endpoints/frequency/sort keys, label-index settings, property
nullability, and same-name index definitions. Missing compatibility metadata
also causes refusal. The error identifies the schema object and conflicting field.
Compose keeps API/worker startup gated on successful schema initialization.

Compatible bootstrap remains idempotent; missing labels, keys, indexes and
nullable label properties can still be added. Required properties cannot be
retroactively appended to existing labels. Bootstrap no longer silently deletes
and rebuilds incompatible same-name indexes. The known obsolete
`idx_edge_key_lookup_*` cleanup runs only after the full compatibility check passes.
On refusal, preserve the existing volumes, back up the graph, and use an explicitly
reviewed migration or a separate empty graph; do not clear the live graph to force
startup. These are structural checks against the current manifest, not a
general-purpose schema-version migration framework. Quiesce other schema writers
during bootstrap: the read/check/write sequence is not a cross-process transaction.

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

## Confluence and ServiceNow ingestion

The single worker can run incremental Confluence Data Center and ServiceNow
Table API jobs. Supply source credentials to the worker through environment
secrets (do not put them in API requests or job payloads):

| Source | Required URL | Authentication |
|---|---|---|
| Confluence | `EOIP_CONFLUENCE_URL` | `EOIP_CONFLUENCE_TOKEN`, or both `EOIP_CONFLUENCE_USERNAME` and `EOIP_CONFLUENCE_PASSWORD` |
| ServiceNow | `EOIP_SERVICENOW_URL` | `EOIP_SERVICENOW_TOKEN`, or both `EOIP_SERVICENOW_USERNAME` and `EOIP_SERVICENOW_PASSWORD` |

The API uses the same local `EOIP_API_TOKEN` boundary as other admin operations.
Submit `POST /api/v1/admin/ingestion/confluence` or
`POST /api/v1/admin/ingestion/servicenow` with JSON such as
`{"checkpoint":"2026-10-01T00:00:00Z","watermark":"2026-10-02T12:00:00Z","dry_run":false}`.
Omit `checkpoint` to resume from `/data/state/connectors/{source}.json`;
successful non-dry runs store their next checkpoint there. A partial ingestion
does not advance the checkpoint, so rejected records can be retried after
correction. `dry_run:true` maps and reports records without graph/raw/DLQ writes
or checkpoint advancement. Confluence attachment handling imports metadata, not
binary content. Confluence page and ServiceNow knowledge article text is stored
in the document description. The connectors capture source events before graph
mutation and link the resulting canonical records to evidence and ingestion runs.

## Automated checks

```powershell
.\scripts\docker.ps1 test
```

Run startup first. The test command builds the test and smoke application images, runs Python tests inside
Linux, runs the real-stack smoke test, and then runs Chromium UI tests inside a
Playwright container. The browser image is a substantial first-time download.

The smoke test checks API authorization/limits, worker completion and replay,
Jira-to-code paths, impact, evidence, schema validation, model-unavailable
retrieval, the web service, and actual MCP initialization/list/call operations.
UI tests check valid/invalid login, symbol search, path visualization, agent
evidence, administration validation/ontology, DLQ rendering, and recovery after
simulated API unavailability or network interruption. DLQ rendering and outage
responses are browser-controlled test fixtures, not proof of live DLQ replay or
a real server crash. Screenshots are saved under the
Git-ignored `test-results/browser/`, separate from acceptance receipts so browser
runs cannot erase recovery evidence.

Local Python development remains available with `python -m pytest` from the repository root.
On Windows with a non-UTF-8 locale, use `python -X utf8 -m pytest`; UI source files
contain UTF-8 characters and some existing tests rely on Python's default encoding.
`requirements.lock` pins the runtime versions verified in the Linux image;
`pyproject.toml` describes portable development dependencies.

### Fresh demo and recovery acceptance

```powershell
.\scripts\docker.ps1 acceptance
```

This builds the current runtime and creates a uniquely named, disposable Compose
project with two fresh HugeGraph servers on an internal network. It publishes no
ports and mounts none of the running demo's graph/application volumes. It loads
the demo from empty storage, verifies the Jira-to-code path and its captured raw
evidence, impact and lineage, repeats ingestion, validates the graph, then
exports and restores a checksummed snapshot. Recovery must retain **every**
vertex/edge property, every raw/DLQ JSON record, and identical golden-query
results. A second restore must reject the populated target without changing it.
It also repeats schema bootstrap on the populated source and proposes four
incompatible manifest changes (property type, vertex ID strategy, edge frequency,
index type), each alongside a pending safe addition. All proposals must fail with
only schema GET requests and retain identical raw vertex/edge records and schema
definitions. The proposed manifest is substituted by the verifier; server reads
and preservation checks use the real HugeGraph instance.

Both initial ingestion and replay also validate emitted GraphMutation and
NormalizedEntity/NormalizedRelationship envelopes against the checked-in JSON
schemas. The receipt records vertex/edge mutation counts and distinct run counts;
referenced evidence must already have a captured raw record before consumption.
Administrative bootstrap and snapshot bulk loading are outside this source
contract boundary. Invalid contract proposals fail explicitly before their
affected write, but the run is not transactional: earlier writes can remain.
Raw captures are retained; automatic canonical-validation DLQ routing is not
part of this gate.

Re-ingestion compares business identities and properties, excluding ingestion
run history and observation timestamps (`captured_at`, `first_seen`, `last_seen`,
`valid_from`, `modified_at`), which change when fixtures are captured again.
Snapshot/restore comparisons do not omit those properties. This gate does not
certify temporal first-observation semantics or native HugeGraph disaster recovery.

The command exits nonzero on failure, saves a JSON receipt under
`test-results/eoip-acceptance-<run-id>.json`, and removes only that run's disposable
containers/network/volumes in a `finally` block. It does not reset the live demo.
Do not point the acceptance script at an existing graph: both targets must be empty.

The legacy `python -m scripts.demo_reset --confirm` command is for backends that
allow deletion. It preserves audit history, audits intent before mutation, closes
the store on every outcome, and fails rather than treating an unsupported clear
as a successful reset. Runtime HugeGraph deletion remains deliberately disabled;
use the isolated acceptance command instead. Reset is destructive and is not
transactional across graph and files; quiesce writers and back up first.

## Isolated live DLQ/API/worker acceptance

```powershell
.\scripts\docker.ps1 dlq-acceptance
```

This builds the current runtime and test images, starts a fresh HugeGraph,
schema initializer, HTTP API, independent worker and authenticated ServiceNow
Table API and Confluence Data Center REST fixtures in a uniquely named Compose
project, and runs twelve opt-in
multi-step pytest journeys:

- A real API-submitted Jira record is rejected by the worker, captured and listed
  in the DLQ. Replaying unchanged invalid input remains `PARTIAL`, creates no
  WorkItem, and preserves the raw capture and original DLQ entry.
- An obsolete mapper genuinely rejects valid Jira input via the ingestion
  service. The current worker mapper then replays that immutable capture
  successfully, persists the WorkItem and evidence link, and repeats replay
  without logical drift or duplicate business vertices. The initial rejection
  in this scenario is service-seeded, not API-submitted.
- Missing/invalid authentication, unknown records, missing capture and
  mismatched DLQ/capture hash are refused without queuing jobs or graph writes.
- Registered Confluence v2 invalid captures route through `SOURCE_OPERATION`
  to the independent worker, remain `PARTIAL`, and preserve raw/DLQ bytes.
- An obsolete Confluence mapper service-seeds a genuine rejection. The current
  worker recovers the Document and evidence link; repeat replay through the
  source endpoint preserves the entire stable logical graph.
- Missing registry entries and wrong adapter types return 409 without jobs or
  graph mutations, with correlated refusal audits. Registry IDs deliberately
  differ from adapter instance hashes to verify DLQ routing.
- ServiceNow baseline acquisition paginates four tables over actual HTTP,
  persists five mapped entities and evidence links, advances a checkpoint, and
  then runs an empty incremental sync. Replay preserves the logical graph,
  raw bytes and checkpoint without fetching upstream again.
- A fetched ServiceNow mapping rejection remains `PARTIAL` through DLQ replay.
  Authentication and source-policy refusals enqueue nothing. Registered DLQ
  replay shares source scheduler admission for enabled, paused, capability,
  concurrency and rate controls; concurrency has paired endpoint unit coverage.
- Invalid upstream credentials persist a categorized `FAILED` job and baseline
  manifest without capture, business graph or checkpoint writes. Outbound
  REST requests carry the job's `X-Correlation-ID`, including failed requests.
- Confluence baseline paginates space, page and attachment metadata over real
  HTTP. Four entities, provenance and space/page/attachment hierarchy persist
  in HugeGraph. Incremental sync refreshes the unchanged space's `last_seen`
  without changing content, revisions, hierarchy or original capture provenance.
  Replay preserves the latest observation time, immutable raw bytes and checkpoint,
  and performs no upstream acquisition.
- A fetched Confluence page without a title is captured and rejected as a
  mapping error. The baseline and unchanged-input DLQ replay remain `PARTIAL`
  without advancing a checkpoint or creating the rejected Document.
- Confluence authentication, missing content ID and invalid response-shape
  failures persist categorized `FAILED` jobs/manifests with matching API/worker
  and upstream correlations, and no capture, business graph or checkpoint writes.

Durable job results and matching API/worker audit correlation IDs are checked.
DLQ entries are historical evidence: successful replay does **not** delete or
mark them resolved; an immutable invalid payload is not repaired by replay.

The gate publishes no ports, uses no primary volumes and has an internal-only
network. Its containers/network/application volume are removed in `finally`.
JSON verdict and JUnit evidence persist as
`test-results/eoip-dlq-acceptance-<run-id>.json` and `.xml`. Failed collection,
missing evidence, unexpected/duplicate journey names, any skipped journey or
nonzero pytest exit fails the gate. Normal host pytest runs skip these twelve
tests; the command above runs all twelve against the actual services. No browser
run is part of this API-only gate. The earlier Confluence mapper-recovery journeys
still use service-seeded immutable captures and an unreachable upstream URL;
the new acquisition journeys use a separate authenticated internal HTTP fixture.
Both source fixtures use deterministic fixture-only credentials via environment
secret references, not real Confluence/ServiceNow tenants. Attachment metadata
is covered, not downloading/parsing attachment bytes; historical versions,
authors, labels, body-structure extraction, semantic document links and stale
documentation detection remain separate G2-P4 obligations. Other registered adapters, live
source systems, worker crash recovery and config/native recovery remain
separate acceptance obligations.

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
container, checks all vertex/edge properties, raw/DLQ JSON equality, counts and
the Jira-to-symbol evidence path, then
removes that test graph container. The main deployment and its volumes remain
available. Run backup before this command.
The Python verifier also accepts `--source <snapshot-path>` to select an explicit
archive; without it, the lexically newest snapshot filename is used. A missing
backup produces an actionable error rather than an empty-selection exception.
Because snapshots omit worker job history, the smoke test validates the restored
graph directly before submitting an idempotent demo replay to verify worker
processing.

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
The API's `/metrics` endpoint includes request/operation counts and latency,
as well as durable ingestion-job status transitions and processing runtimes.

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
