# Hubble Basics + standalone RocksDB

This stack pins HugeGraph Server and Hubble to 1.7.0. Hubble connects to the
same `DEFAULT/hugegraph` graph used by the API, worker, manual imports and
pipeline imports. There is no second database and no graph migration.

## Start, credentials and URL

```powershell
.\scripts\docker.ps1 up
```

Open **http://localhost:8088**. The `hubble-init` service registers the existing
graph as **EOIP**, using the current local graph credentials. In Hubble 1.7,
credentials belong to a graph connection, not to a separate UI login page.
The derived image keeps the official 1.7.0 release and defaults new browser
sessions to English before the UI starts. An explicit saved language preference
is preserved; select **English** in the language selector to change that browser.

To explicitly enable the requested local demonstration account:

```powershell
.\scripts\docker.ps1 hubble-local-admin
```

This rotates the existing HugeGraph administrator to **admin / admin** through
the authenticated user API, updates the ignored deployment environment file,
recreates the application clients, and refreshes Hubble's connection. It does
not remove schema, vertices, edges, application state or Docker volumes.
Do not simply edit the password environment value on an initialized database:
that alone does not rotate the stored account.

If interrupted after the account update but before configuration synchronization,
set `HUGEGRAPH_PASSWORD=admin` in your local `deploy/.env` and run startup again.
Keep the API token unchanged. The rotation command is intentionally opt-in;
new deployments still generate random credentials by default.

All Hubble host access is bound to `127.0.0.1`; HugeGraph itself remains private
on the backend network. Never expose this weak demo account or Hubble to a LAN
or the Internet. Hubble 1.7 has a local connection manager rather than per-user
UI authorization: any local user able to access the UI can use its saved graph
credentials to modify data. It is an administration tool, not the read-only
application/MCP interface.

If manually creating a Hubble connection, supply:

| Field | Value |
|---|---|
| Graph ID / connection display name | EOIP |
| Graph Name | hugegraph |
| Hostname | hugegraph-server |
| Port | 8080 |
| Username | admin |
| Password | admin after the opt-in rotation; otherwise your local graph password |

The hostname is resolved inside Docker, not by the browser. Hubble's connection
allowlist only permits `hugegraph-server:8080`.

## View and query actual ingested data

For readable names, directed labeled edges and domain colors, open
**http://localhost:8088/enterprise.html** or the **EOIP Named Enterprise Graph**
link in native Hubble. Choose one of 11 business questions or a named seed
entity instead of entering physical IDs. The page queries the same persisted
graph through Hubble, never a fixture substitute. Inspect node/edge facts,
source evidence, the accessible relationship table and generated read-only
Gremlin; toggle provenance nodes, drag nodes, zoom/fit or export returned JSON.
Queries include edges and are bounded to 120 relationships.

For a broader graph-database workbench, open
**http://localhost:8088/graph-idl.html** or the **Graph IDL** link in native
Hubble. Graph Integrated Development Studio keeps live Hubble Gremlin reads for
the current HugeGraph connection while presenting backend profiles, query
language templates and property graph/table/RDF/JSON representations for
HugeGraph, Neptune, Neo4j/OpenCypher, RDF stores and multi-model graph targets.

Double-click `demo\autodemo\run-demo-hubble.bat` to prepare the additive corpus
and automatically walk through all 11 graph scenarios. Stop the walkthrough
to investigate any scenario. Existing administration, ingestion and VS Code
launchers remain separate; this view is not a claim that every application
capability or production acceptance criterion has been demonstrated.

Click **Visit** on **EOIP**. Under **Data Analysis**, use the Gremlin editor and
**Execute Query**, then choose **Chart** or **Json**. To inspect schema, select
**Metadata Configuration** and **Vertex Type**. These read-only example queries
execute directly on HugeGraph:

```groovy
g.V().count()
g.E().count()
g.V().limit(25)
g.V().hasLabel('WorkItem').limit(25)
g.V().hasLabel('Document').limit(25)
g.V().hasLabel('DocumentSection').limit(25)
g.V('PHYSICAL_VERTEX_ID_FROM_JSON_RESULT').bothE().limit(25)
```

Switch between graph, table and JSON results. Physical edge labels include
endpoint-label suffixes; the EOIP API exposes their logical relationship names.
Use the physical vertex `id` shown in JSON results for direct lookups. EOIP uses
`eoip-` followed by the SHA-256 hex digest of the canonical ID. An unrestricted
`has('canonical_id', ...)` query is not supported without a corresponding
secondary index; do not mistake that query error for missing data.
Hubble can also run mutating Gremlin: do not use `drop()` or clear graph/schema
actions unless you explicitly intend to delete data.

Manual ingestion is available at **http://localhost:8080/admin**. Paste the
existing API token, import JSON or upload a supported file, then verify its
canonical ID in Hubble. The manual and pipeline demonstration launchers use
the same graph. A successful request alone is not proof of ingestion: check
reported errors/rejections, the completed job where applicable, and read the
entity back through both EOIP search and Hubble.

## Load all available demonstration data

```powershell
.\scripts\docker.ps1 demo-data
```

This additive command rebuilds changed images as needed, waits for the stack,
and loads the checked-in `demo/demodata` corpus into the existing RocksDB graph:

- The existing typed core Jira/repository graph and eleven enterprise scenarios,
  including business alignment, decision alternatives and process deviations.
- Native Jira WorkItems, projects and people from the manual PAY and pipeline
  FRD exports.
- All source exports, Office documents, CSV/text, code, crawler, agent, query,
  LAYA, pipeline and RAG scenario files as source-preserving Document entities
  with DocumentSection chunks, source-event evidence and JSON/RAG/vector bundles.
- Markdown, Python and TypeScript are parsed as text with their original
  `fixture://demo/demodata/...` source URI. Git internals, Python caches and
  package `__init__.py` markers are excluded, not demonstration data.

Raw vendor exports are searchable source documents, **not** a claim that every
vendor record has been normalized into a typed business entity. Configuration
and evaluation catalogs become knowledge artifacts; loading them does not
execute scenario actions or connect to the synthetic external hosts.
The existing manual/pipeline demo launchers remain separate workflows.

Per-file checkpoints and receipts are stored in
`/data/state/demo-corpus.json` and `/data/state/demo-corpus-result.json`.
Reruns retain unchanged bundles only after checking graph read-back; missing
bundles or graph entities are re-ingested. Parsing/rejection errors stop the
command rather than reporting false success. Completed files survive retries.
No graph reset, schema clear, volume deletion or automatic data cleanup occurs.
The ordinary `EOIP_LOAD_DEMO` startup flag still loads the smaller core/enterprise
seed; run `demo-data` explicitly to load the complete corpus on an existing graph.

### Verified local corpus receipt

The 2026-10-05 deployment loaded **85 files, 85 Documents and 1,116 RAG chunks**,
including eight typed enterprise scenarios and native PAY/FRD Jira datasets.
All corpus identities were read back through Hubble, and the hashes of all
510 exported artifact files were verified. A second real load retained all
85 assets, loaded zero files, and left graph totals unchanged.

The graph then contained **1,805 vertices and 4,349 edges**, including 56
WorkItems, 87 Documents and 1,117 DocumentSections. These totals include
pre-existing and retained verification data; they are not corpus-only counts.
All original 310 vertices and 374 edges remained present.

See [the runtime validation report](hubble-runtime-validation.md) for commands,
acceptance evidence and the full-suite failures outside the Hubble changes.

## Data-safe clean builds

```powershell
.\scripts\docker.ps1 rebuild
.\scripts\docker.ps1 down
.\scripts\docker.ps1 up
```

`rebuild` bypasses the application/web/Hubble image build cache and force-recreates
services. It never deletes volumes or changes the stored credentials.
`down` retains data; `up` reconnects and performs compatible idempotent schema
bootstrap. Set `EOIP_LOAD_DEMO=false` to avoid automatic demo loading; this does
not clear an existing graph.

| Stable volume | Contents |
|---|---|
| eoip_graph-data | Authoritative RocksDB database, schema and graph accounts |
| eoip_application-data | Raw events, parsed artifacts, RAG chunks, queue, jobs, DLQ, state and backups |
| eoip_hubble-data | H2 connection metadata, query history and UI configuration |
| eoip_hubble-uploads | Hubble import uploads |
| eoip_model-data | Local models when enabled |
| eoip_metrics-data | Metrics when enabled |

Keep the Compose project name `eoip`. Changing the project name attaches different
volumes and can look like lost data even when the old data still exists.
The server image additionally creates an anonymous installation volume; graph
durability relies on the explicitly mounted `eoip_graph-data` RocksDB directory,
not that installation volume.

Image deletion is **not** data deletion. Docker Desktop's deletion of volumes,
factory reset, or disk loss can remove data. A fully fresh deployment therefore
requires explicit volume deletion as a separately approved destructive operation;
there is deliberately no automatic reset command here. Back up first:

```powershell
.\scripts\docker.ps1 backup-bundle
```

## Validation

Focused deployment/setup tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\unit\test_hubble_setup.py tests\security\test_container_hardening.py tests\security\test_no_egress.py
```

Live tests opt in with `EOIP_RUNTIME_HUBBLE=1`, require the running Docker stack,
and exercise manual and batch-pipeline ingestion, API authentication rejection,
and Hubble read-back. They retain clearly identified synthetic verification
records rather than deleting anything from the user's graph.

```powershell
$env:EOIP_RUNTIME_HUBBLE='1'
.\.venv\Scripts\python.exe -m pytest tests\runtime_hubble -v
```

Official release-specific configuration is used rather than copying current
`master` instructions: Hubble 1.7 uses graph connections and a file-backed H2
metadata store. Newer Hubble standalone/PD configuration options are not silently
applied to this pinned release.
