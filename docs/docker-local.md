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
| HugeGraph Hubble | http://localhost:8088 | Existing EOIP graph connection; see [Hubble setup](hubble-local.md) |

All published application ports bind to `127.0.0.1`. This is a local development
authentication model: one token grants access to both query and administration
operations. `/admin` is navigation, not a separate authorization boundary.

Change `EOIP_WEB_PORT`, `EOIP_API_PORT`, `EOIP_MCP_PORT`, or `EOIP_HUBBLE_PORT` in `deploy/.env` if a
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
| hubble | Hubble 1.7.0 with an English first-use default; local schema browser, graph visualization and direct Gremlin queries |
| hubble-init | Idempotent connection registration against the existing DEFAULT/hugegraph; never initializes or clears graph data |
| schema-init | One-time, idempotent property/vertex/edge/index bootstrap |
| eoip-api | Search, QueryPlan execution, entities, bounded path/impact/lineage, GraphRAG retrieval, agent contracts, admin jobs/validation/ingestion, metrics |
| eoip-worker | Single-worker durable filesystem queue; capture-first ingestion and demo loading |
| eoip-web | Built React SPA served by Nginx; same-origin API proxy |
| eoip-mcp | Authenticated, read-only MCP façade over the application API |

Docker named volumes hold graph storage and application raw events, DLQ,
job records, worker state, snapshots, Hubble connection/query metadata and uploads.
`docker.ps1 rebuild` performs a no-cache application/web/Hubble build and recreates services
without deleting these volumes. `docker.ps1 down` removes this project's
containers and networks while retaining volumes. Startup resumes interrupted
RUNNING jobs and retries transient I/O/HTTP failures three times. Keep one worker
replica: the filesystem queue does not implement multi-worker claiming.

Run `.\scripts\docker.ps1 demo-data` to add the entire checked-in demo corpus to
an existing graph without resetting it. This includes the typed core/enterprise
seed and PAY/FRD Jira records, plus source-preserving documents and RAG chunks for
the remaining exports, Office files and scenario catalogs. See
[the complete corpus scope and repeatable loading behavior](hubble-local.md#load-all-available-demonstration-data).

Do not run `docker compose down --volumes`, remove the named volumes, or prune
volumes to clean-build the application. Deleting Docker images alone does not
delete stored data. A fresh data deployment requires a separate, explicit
data-deletion decision; normal startup, shutdown and rebuild never request it.

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

After the recovery and schema checks, the disposable source also exercises a
synthetic pre-upgrade temporal relationship with its original fact-based physical
edge identity. Replacement must expire that exact edge, deletion must leave no
current edge, recreation must not materialize a deletion-only revision as an edge,
and late replay must remain rejected. The `temporal_edge_upgrade` receipt records
these assertions separately: its three physical history edges are created after
the snapshot comparison and are not included in the demo snapshot counts.
Host regressions additionally cover restoring legacy snapshots and canonical
ingestion envelopes. This is bounded upgrade compatibility, not an atomic
multi-writer migration or native disaster-recovery certificate.

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
project, and runs fifteen opt-in
multi-step pytest journeys plus a Linux independent-process memory-writer test:

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
- Confluence page storage XHTML is extracted deterministically into Document
  `payload_json`: headings, explicit anchors, safe HTTP(S) links, unresolved
  page/attachment references, code snippets and structured tables. Document and
  Evidence record `parser_version=confluence-storage/1.1`. Original body text
  remains in `description` and immutable capture; revisions preserve both forms.
- Page payloads also retain source labels, author/editor references and UTC
  creation/modification timestamps. Expanded labels with continuation are
  reacquired through the trusted content-label endpoint; the fixture verifies
  complete pagination, correlation propagation and exact persisted metadata.
- Public historical-content requests acquire all previous version metadata
  before hashing/capture. Replay preserves complete source history offline.
- Exact canonical URNs and unambiguous indexed source URLs create evidence-backed
  temporal `DOCUMENTS` links. Changed/deleted referenced technical facts appear
  in validation, the stale API and DocumentationFreshnessAgent. Replaying the
  same capture cannot silently acknowledge newer target facts.
- A fetched Confluence page without a title is captured and rejected as a
  mapping error. The baseline and unchanged-input DLQ replay remain `PARTIAL`
  without advancing a checkpoint or creating the rejected Document.
- Confluence authentication, missing content ID and invalid response-shape
  (including the secondary label endpoint)
  failures persist categorized `FAILED` jobs/manifests with matching API/worker
  and upstream correlations, and no capture, business graph or checkpoint writes.
- TraceImpact task-memory journeys verify authenticated classified HTTP retrieval,
  shared-volume persistence across independent API/test processes, short-TTL
  expiry without deleting durable run evidence, exact owner/scope deletion,
  invalid TTL refusal, minimized content and explicit corruption failure.
  Three independently spawned writers additionally verify that OS locking
  prevents lost JSON records on Linux; the host unit suite exercises Windows.

Durable job results and matching API/worker audit correlation IDs are checked.
DLQ entries are historical evidence: successful replay does **not** delete or
mark them resolved; an immutable invalid payload is not repaired by replay.

The gate publishes no ports, uses no primary volumes and has an internal-only
network. Its containers/network/application volume are removed in `finally`.
JSON verdict and JUnit evidence persist as
`test-results/eoip-dlq-acceptance-<run-id>.json` and `.xml`. Failed collection,
missing evidence, unexpected/duplicate journey names, any skipped journey or
nonzero pytest exit fails the gate. Normal host pytest runs skip these fifteen
HTTP journeys; the command above runs all fifteen against the actual services
and the independent-writer test in Linux. No browser
run is part of this API-only gate. The earlier Confluence mapper-recovery journeys
still use service-seeded immutable captures and an unreachable upstream URL;
the new acquisition journeys use a separate authenticated internal HTTP fixture.
Both source fixtures use deterministic fixture-only credentials via environment
secret references, not real Confluence/ServiceNow tenants. Attachment metadata
is covered, not downloading/parsing attachment bytes. Historical version metadata,
explicit document links and referenced-fact staleness are covered; historical
body retrieval, rendered/rich macro expansion and inferred semantic matching are
not covered. Other registered adapters, live
source systems, worker crash recovery and config/native recovery remain
separate acceptance obligations.

## Bounded scoped agent task memory

The API composition root loads `config/memory-policy.yaml` and stores approved
task records in `EOIP_DATA_DIR/agent-memory/records.json`. The versioned defaults
are **30 days maximum**, **1,000 records** and **8 MiB serialized JSON**.
Operators may shorten retention; per-run `memory_ttl_seconds` is a strict
positive integer no greater than the configured maximum. No policy may exceed
30 days. Invalid configuration fails startup rather than silently relaxing policy.

Only the catalog's TraceImpact contract currently enables `APPROVED` persistent
memory. Other catalog agents remain `RUN_ONLY`; generic conversation, semantic
and procedural retention are not enabled. A record retains only outcome status
and evidence count, together with run identity, exact agent scope, owner,
source, provenance, confidence, classification, creation time and deletion policy.
Task goals, prompts, document bodies and tool payloads are not copied into this
memory store. This does not certify all pre-existing graph/log/audit content.

`GET /api/v1/agents/runs/{run_id}/memory` uses existing bearer authentication and
operation auditing. Responses preserve `INTERNAL` classification. Missing,
expired, disallowed or unavailable run-scoped records return 404; corrupt or
unavailable memory storage returns a safe 503. The existing local bearer token
is not a new multi-tenant identity or RBAC boundary. In-agent
`recall_task(run_id)` uses the current actor and agent scope, enforces APPROVED
policy, and consumes the existing tool-call/time budget.

Records are immutable until exact-scope/owner deletion or expiry. Writes use an
OS lock, a flushed temporary file and atomic replacement; readers validate the
entire bounded envelope. Capacity exhaustion refuses the new record rather than
evicting unexpired persistent evidence. Memory is admitted only after its graph
run and trace have persisted. Persistence failure is explicit in warnings and
explanations; otherwise successful runs become PARTIAL.

Expiry is enforced at startup and on every storage operation, including at the
exact TTL boundary. There is no idle background sweeper: physical deletion occurs
on the next operation/startup. A corrupt file is not silently repaired or
overwritten. Tightening policy below existing records' TTL/count/byte bounds may
refuse startup; restore the previous valid policy, perform explicit governed
cleanup/migration, then apply the stricter policy. Do not edit a live file while
writers are active.

The transient AgentResult cache is separately bounded by retention, record count
and serialized bytes; it evicts oldest entries and excludes oversized results.
These are serialized-byte bounds, not exact Python heap-size guarantees.
Run detail may return `result: null` after eviction/restart while the durable trace
remains; explanation retrieval falls back to trace evidence.

Durable traces, audits, proposals and graph history have separate lifecycles.
Their global retention/privacy certification remains open. Operational snapshots
currently cover graph/raw/DLQ/state/journal/jobs, **not this memory directory**;
this batch does not extend disaster-recovery guarantees to task memory.

### Confluence storage extraction boundaries

Storage fragments must be well-formed XHTML/XML; known HTML entities are
normalized outside CDATA, while code macro CDATA stays literal. Malformed
markup, declarations, unknown entities, invalid table spans and exceeded limits
raise mapping errors after capture, before Document/Evidence writes, using the
existing DLQ path. Limits are 2,000,000 characters, 50,000 elements (including
the wrapper), 128 nesting levels and table spans of 1..1000.

Extraction does not fetch link targets or expand arbitrary macros. Explicit
canonical EOIP URNs are retained for the separate reference reconciler described
below. Script/style/noscript subtrees and other non-HTTP(S)
URL links are excluded from derived output; raw content is retained as evidence,
not sanitized HTML for rendering. An empty/missing body clears current raw and
derived content while retaining earlier revisions; older replay cannot restore
stale content. Existing `payload_json` and `parser_version` graph property keys
are reused; parser changes do not add physical property keys.

### Confluence source metadata boundaries

The `confluence-dc/1.2` mapper retains `source_metadata` (schema `1.0`) alongside
the existing storage-extraction output in Document `payload_json`. Labels are
sorted and deduplicated by `(prefix, name)`; missing prefixes remain empty,
not inferred. Author (`history.createdBy`) and editor (`version.by`) contain
only source `type`, user key, username and display name. Email is not copied
into derived metadata. These references do not create canonical Person entities
or cross-source identity merges.

Creation (`history.createdDate`) and modification (`version.when`) timestamps
are normalized to UTC, retaining available fractional precision. The shared
timestamp parser accepts ISO-8601 input and treats timezone-less input as UTC.
Missing fields produce explicit empty labels/null actor or timestamp values,
clearing current metadata on an update while preserving earlier revisions.
Source timestamps do not replace capture/event time or change late-event rules.
Immutable raw capture retains the acquired page payload, including source actor
fields and complete labels. Label enrichment happens before event hashing and
capture; the truncated expansion is replaced with the label endpoint results.

When expanded labels advertise continuation, acquisition restarts at offset
zero using the configured trusted base URL and a quoted content ID. It never
follows response-provided URLs with credentials. Short pages with explicit
continuation continue; repeated pages, empty continuation pages, invalid
response shapes and collections exceeding 10,000 acquired labels fail
explicitly before ingestion. Malformed individual metadata fields or unresolved
label continuation in a submitted capture fail mapping through the existing
capture-before-write DLQ path. Replay uses captured complete labels without
upstream requests.

### Confluence history, document links and freshness boundaries

`source_history` (schema `1.0`) contains ordered version numbers, UTC timestamps,
editor references, messages, minor-edit flags and trusted constructed source
references. Acquisition uses the configured base and quoted content ID with
`status=historical&version=N&expand=version`, never response-provided URLs.
The current search result supplies current-version metadata; earlier versions
are fetched before capture. A complete history must agree with that current
metadata and contain every version from 1 through the current version.
The maximum is 1,000 versions. Invalid/noninteger versions, missing/inaccessible
history, mismatched IDs/versions or exceeded bounds fail explicitly, without
silent truncation. Historical bodies are not fetched. Older captures without
acquired history remain ingestible with `complete=false`; replay stays offline.

Managed `DOCUMENTS` links support Service, APIService, APIEndpoint, Project,
WorkItem, File and CodeSymbol. Eligible existing entities resolve by exact EOIP
URN or exact `url`, `path` or `source_uri`; each property has a single-property
HugeGraph secondary index. Ambiguous URLs are logged and not linked. Titles
and names are not identity evidence; targets are not fetched or inferred.
Managed links carry `document-reference/1.0`, source evidence, the document
capture hash and a baseline fingerprint of target business properties.
Observation timestamps/provenance do not trigger staleness. File/CodeSymbol
content hashes do; non-code envelope hashes do not.

Validation and `/api/v1/graph/stale` report `target_changed`, `target_deleted`
or `target_missing` per reference. The stale API includes a `partial` flag;
DocumentationFreshnessAgent reports PARTIAL for stale references or capped
scans. Scan caps are 50,000 vertices/reference edges; reconciliation refuses
more than 10,000 source links or existing document edges rather than truncating.
Source-link reconciliation limits are enforced after mapping, so they are not
an acquisition-before-write guarantee.

Identical capture replay retains the baseline even after target changes. A new
document version can acknowledge current target facts; removed references or
document deletion expire managed links. Late replay cannot resurrect deleted
entities/relationships. Deletion markers remain current revision barriers but
are excluded from as-of facts. Returning to identical earlier content creates
a distinct revision interval without rewriting the previous interval; unchanged
polling/replay remains idempotent.

These controlled endpoint/index additions use ontology `0.4.0`, schema `1.2`.
Fresh bootstrap and compatible additive schema initialization install them.
Snapshots still require exact schema equality: older `1.1` archives need an
explicit migration, not automatic acceptance. Attachment bytes, inferred semantic
matching and live-tenant certification remain open.

## Backup and restore

Avoid submitting admin writes during backup. This command stops the worker,
exports a checksummed logical graph and raw/DLQ evidence, and restarts the worker.
The archive also preserves operational JSON under `state/` and `jobs/`, and
NDJSON under `journal/`. Worker heartbeat `state/worker.json` is excluded.

```powershell
.\scripts\docker.ps1 backup
.\scripts\docker.ps1 restore-test
```

The output path is inside `/data/backups/`. Copy a snapshot to the host using
`docker compose -f deploy/docker-compose.yml --env-file deploy/.env cp
eoip-api:/data/backups/FILE.json ./FILE.json` as a single command.

`restore-test` restores the newest snapshot into a disposable, separate HugeGraph
container, checks all vertex/edge properties, raw/DLQ JSON equality, operational
state and the Jira-to-symbol evidence path (plus asset inventory/byte equality
when the newest archive is a ZIP recovery bundle), then
removes that test graph container. The main deployment and its volumes remain
available. Run backup before this command.
The Python verifier also accepts `--source <snapshot-path>` to select an explicit
archive; without it, the lexically newest snapshot filename is used. A missing
backup produces an actionable error rather than an empty-selection exception.
Recovery preserves terminal job history. Pending/running jobs become `HELD`
with their original status, snapshot checksum and recovery timestamp. Already
held jobs retain their existing recovery metadata. The worker skips held jobs;
starting it must not automatically resume interrupted work.

For restore, create a separate Compose project with separate ports and
`EOIP_LOAD_DEMO=false`. Start HugeGraph and schema-init, leave the worker stopped,
and mount/copy the snapshot into an application container. Run:

```text
python -m scripts.restore /data/backups/FILE.json
```

Restore checks the checksum, schema version, endpoint types, and evidence paths
before mutation, and requires a physically empty graph, including tombstoned
vertices and expired relationships, and empty raw/DLQ/state/journal/job data
(a worker heartbeat alone is permitted). It never clears existing data.
Operational paths reject traversal, worker-heartbeat entries, noncanonical job
IDs and Windows reserved names. Export refuses symlinked operational files;
restore refuses paths resolving outside its data root. Operational exports are bounded to
100,000 files and 64,000,000 UTF-8 bytes; oversized archives fail explicitly.
Logical exports preserve tombstones and historical edges in both store paths;
the non-paginated path refuses more than 1,000,000 vertices or edges. Temporal
revision/deletion barriers remain effective after recovery.
The local logical export is intended for small, quiescent development datasets;
it is not a transaction-consistent production RocksDB backup. Quiesce all writers
for both export and restore; graph/file restoration is not an atomic transaction.
After restoration, review held jobs in **Administration -> Sources & jobs**.
**Readmit** requires confirmation and invokes authenticated, audit-preflighted
`POST /api/v1/admin/jobs/{job_id}/readmit`. Registered source operations recheck
enabled state, pause, capability, concurrency and rate limits. Successful
readmission retains the job ID, records the operator correlation ID and new
admission time, resets execution/retry state, and returns HTTP 202. A repeated
readmission refuses with HTTP 409. Held jobs can also be cancelled.
The archive ends at the quiescent backup boundary. Events arriving afterward
are not present: recover them from retained immutable captures outside this
archive, or run the source's supported incremental/reconciliation operation
from its restored committed checkpoint after checking current credentials and
admission policy. Do not advance checkpoints manually or assume that readmitting
a held job recovers every post-backup event. Verify source continuity and run
validation before treating the restored instance as authoritative.
Re-execution can repeat pre-backup side effects; confirmation is not a guarantee
of exactly-once delivery. In-process locking serializes operator transitions;
this remains a single-API/single-worker filesystem queue, not a distributed queue.

Snapshots created before operational export remain readable under the same
schema version but cannot recover operational state that was never captured.
The legacy JSON snapshot does not include repository `config/`, model manifests/binaries,
webhook receipts, audit history or agent traces. Held webhook jobs refuse
readmission explicitly because receipt recovery/path rebasing is not implemented.
Reprovision source secrets separately, including any referenced external files.
Archives may contain sensitive raw/job/configuration values; handle them as
confidential. Exact logical equality is not native disaster-recovery certification.
Use supported native HugeGraph backup tooling for production-sized graphs.

### Self-contained configuration and model-weight bundles

The opt-in ZIP bundle adds actual configuration and Ollama model-weight bytes
to the existing logical snapshot. Legacy JSON commands remain supported.

```powershell
.\scripts\docker.ps1 backup-bundle
.\scripts\docker.ps1 restore-test
.\scripts\docker.ps1 recovery-acceptance
```

Build the current application image before using `backup-bundle`. It stops only
the currently running API, MCP, worker and local-model services, then uses a
one-off audited backup container with read-only access to the existing model
volume. Those services are restarted in `finally`, including after a failure.
Stop any other graph/configuration/model writers and close admin clients yourself;
this command cannot quiesce external processes. The API is unavailable during
this backup. Model files/directories must be readable by the image's UID 10001;
permission errors are reported, not bypassed. A disabled model with no downloaded
weights is valid and records zero model blobs.

The bundle contains `bundle.json`, `snapshot.json`, `config/` YAML/JSON and
`models/blobs/sha256-*` plus `models/manifests/`. Each asset has its exact size and
SHA-256 in the manifest. Ollama manifest digest/size references must match actual
included blobs. Weight copies/hashing are streamed, not base64-encoded into JSON.
Backup publishes the ZIP by same-directory atomic replacement after validation;
failure leaves a previous destination archive intact. Source edits detected
during copying refuse publication; this is not a substitute for quiescence.

Current limits: **64 GiB total uncompressed asset bytes**, **100,000 assets
including the logical snapshot**, **256 MiB snapshot**, and **1 MiB per
configuration/model manifest and for `bundle.json`**. `--max-bytes` can lower
the total bound, not increase it. The existing logical graph/operational limits
still apply. Ensure temporary storage and the destination have sufficient free
space: restore stages a full validated copy before copying assets to targets.
Do not infer production scale or native backup guarantees from these limits.

`.env`, arbitrary deployment files and private-key files are not supported
configuration assets. Plaintext values under recognized password/token/API-key/
authorization/private-key fields are refused, including common camel-case and
hyphenated variants. `env://` and `vault://` references can be preserved, but
their external credentials/resolvers must be reprovisioned separately. This
key-based check is not a general secret scanner. Raw graph/evidence, configuration
and model assets may be sensitive or licensed: the manifest labels the archive
`RESTRICTED`; use access-controlled storage and honor model redistribution terms.
The archive is neither encrypted nor signed; checksums detect corruption, not
replacement by an attacker who can rewrite the archive and its manifest.

For direct local commands, supply the **models** directory, not its `.ollama`
parent. Bundle restore requires explicit, separate, empty configuration/model
targets and the existing empty graph/data conditions:

```powershell
python -m scripts.backup --bundle --config-dir .\config --model-dir C:\local-model\.ollama\models --output C:\recovery\eoip.zip
$env:EOIP_DATA_DIR = 'C:\recovery-target\data'
python -m scripts.restore C:\recovery\eoip.zip --config-dir C:\recovery-target\config --model-dir C:\recovery-target\models
```

The ZIP manifest/member allowlist, sizes, checksums, model references,
configuration and inner logical graph are checked before any target writes.
Traversal, duplicate/case-colliding names, unsupported schema, symlinks,
recursive configuration aliases and populated targets refuse recovery.
Do not concurrently write to restore destinations. Graph restoration followed
by asset copies is **not transactional or crash-atomic**; disk/process failures
after mutation can leave partial targets. Preserve the archive and use a new
isolated empty deployment for retry rather than overwriting the failed target.

Activation is deliberate: in a separate Docker deployment mount the restored
configuration directory read-only at `/opt/eoip/config` (the same path used by
bundled mappings/ontology and policy loaders), and mount the restored **models**
directory at `/root/.ollama/models` in the local-model container. Set
`EOIP_CONFIG_DIR=/opt/eoip/config`, the desired `EOIP_OLLAMA_MODEL` tag and the
local model URL as appropriate. On the host, set `EOIP_CONFIG_DIR` to the restored
configuration root and explicitly select restored mapping/ontology paths for
commands with their own path arguments. Restore does not silently switch a
running deployment to new policies or restart model serving. Verify policies,
model availability and held jobs before starting writers.

`recovery-acceptance` builds and uses two fresh disposable HugeGraphs, checks
exact logical recovery, actual binary/configuration byte equality and inventory,
configuration-loader equivalence, held jobs, golden queries and populated-graph
refusal; it writes a unique JSON receipt under `test-results/` and removes its
containers/network in `finally`. Its Ollama-layout binary fixture is synthetic:
it certifies recovery bytes, not downloaded model quality or inference. The
primary graph/data/model volumes are neither reset nor restored by this gate.
Webhook receipt rebasing, audit/trace/memory history, native RocksDB recovery and
multi-store transactional recovery remain outside this bundle.

## Executable MVP requirement evidence

Use an existing pytest JUnit receipt to check explicit requirement annotations
against every row in the 28-requirement MVP traceability matrix:

```powershell
.\.venv\Scripts\python.exe -X utf8 -m scripts.verify_requirement_evidence . `
  EOIP-engg-doc-pkg\traceability\mvp-traceability.csv `
  test-results\recovery-bundle-final-host.xml `
  --output test-results\mvp-requirement-evidence.json
```

The checker reads literal `pytest.mark.req("REQUIREMENT-ID")` annotations,
including module/class inheritance, without importing test modules. It matches
exact JUnit test identities and all parameterized outcomes. A direct MVP
annotation or passing evidence for every declared parent can support a row;
failed/skipped/partial/missing outcomes remain explicit. It also refuses a
globally green verdict if any test in the supplied receipt failed or errored.
Malformed matrices/receipts and source paths escaping the test directory fail
explicitly. All 28 declared MVP rows are required; the denominator is not reduced
to only annotated tests.

The output directory is created when needed. `EVIDENCE_GAPS` persists a report
and returns **exit 1**; complete mapped passing evidence returns exit 0 with
`MAPPED_TEST_EVIDENCE`, not an application-completion certificate. An unannotated
requirement may already have implementation and tests: inspect it and add
accurate requirement-specific acceptance evidence rather than inflating coverage
with unrelated markers.

The refreshed `test-results/full-regression-2026-10-04.xml` receipt contains
**1,023 outcomes: 1,008 passed / 0 failed / 0 errors / 15 skipped**. The bound
`test-results/mvp-requirement-evidence-2026-10-04.json` receipt still reports
`EVIDENCE_GAPS`: passing annotations map only **3/28 requirements (10.71%
annotated evidence coverage)**. This is not 10.71% development completion;
`application_completion_percent` remains null. `source_revision_bound` also
remains false because file hashes and a JUnit artifact do not cryptographically
bind a Git revision. The earlier five-failure receipt is historical and must not
be used as the current regression verdict.

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
