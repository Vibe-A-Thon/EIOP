# Chapter 3 — Ingestion and Graph Construction

This chapter covers everything between "I have data" and "I have a knowledge
graph": importing Jira and GitLab JSON exports, registering live sources,
running baseline/incremental/replay operations, following worker jobs through
their lifecycle, profiling unknown JSON datasets, and calling the deterministic
graph-build endpoints.

Every endpoint, field name, and status value below is taken from the running
code. Where behavior could not be verified against a live runtime it is marked
**[not runtime-verified]**.

## Index

1. [Concepts in five minutes](#concepts-in-five-minutes)
2. [Importing a Jira JSON export](#importing-a-jira-json-export)
3. [Importing a GitLab JSON export](#importing-a-gitlab-json-export)
4. [Registering a source](#registering-a-source)
5. [Running source operations: baseline, discovery, dry-run, sync, reconcile, replay](#running-source-operations-baseline-discovery-dry-run-sync-reconcile-replay)
6. [Incremental checkpoints and the dry-run flag](#incremental-checkpoints-and-the-dry-run-flag)
7. [How the worker processes jobs](#how-the-worker-processes-jobs)
8. [Cancelling and re-admitting jobs](#cancelling-and-re-admitting-jobs)
9. [The dead-letter queue (DLQ)](#the-dead-letter-queue-dlq)
10. [Profiling JSON datasets](#profiling-json-datasets)
11. [Graph-build endpoints](#graph-build-endpoints)
12. [Provenance and evidence](#provenance-and-evidence)

---

## Concepts in five minutes

- **Source connector** — an adapter implementing the `SourceConnector`
  protocol in `packages/eoip/connectors/base.py`: `capabilities()`,
  `discover(scope)`, `baseline(checkpoint)`, `poll_changes(checkpoint)`,
  `handle_event(event)`, `fetch_record(ref)`, `health()`, `replay(events)`.
  Shipped connectors include Jira, GitLab, GitHub, Confluence, ServiceNow,
  Rally, qTest, Grafana, Datadog, Kibana, Figma, an API-portal crawler,
  web/files crawlers, local code, Kubernetes, and OpenTelemetry
  (`packages/eoip/connectors/`). This chapter exercises Jira and GitLab end to
  end; the others follow the same protocol.
- **Source event** — the immutable captured record (`SourceEvent` /
  `SourceEventV2`) with `event_id` (a SHA-256), `source_system`,
  `source_record_id`, `payload_hash`, and `payload`. Raw events are written to
  `<data root>/raw/<source_system>/<event_id>.json` **before** any graph
  mutation ("capture-first").
- **Job** — every non-trivial ingestion is a durable JSON file in
  `<data root>/jobs/<job_id>.json` with a lifecycle of `PENDING`, `RUNNING`,
  `SUCCEEDED`, `PARTIAL`, `HELD`, `FAILED`, `CANCELLED` (the set is defined in
  `packages/eoip/snapshot.py`: `JOB_STATUSES`).
- **DLQ** — rejected records land in `<data root>/dlq/<event_id>.json` with a
  unified envelope (`packages/eoip/ingestion/dlq.py`).
- **Demo data** — a worker with `EOIP_LOAD_DEMO=true` (the default, see
  `apps/worker/main.py`) auto-submits a `DEMO` job on startup when the demo
  repository `urn:eoip:code:repo:demo` is absent.

---

## Importing a Jira JSON export

**What it does.** Turns a Jira JSON export (a list of issues, or an object with
an `issues` or `values` list) into graph vertices: `Project`, `WorkItem`,
`Person`, and `Evidence`, connected by `CONTAINS`, `ASSIGNED_TO`, `PARENT_OF`,
`EVIDENCED_BY`, and `INGESTED_IN` edges (see
`packages/eoip/ingestion/jira.py`).

**How to access.**

- API: `POST /api/v1/admin/ingestion/jira` (status 202) or the public alias
  `POST /api/v1/ingestion/jira-json` (status 202).
- UI: the Admin dashboard (`apps/web/src/admin/AdminDashboard.jsx`) shows the
  queued job under **JOB STATUS / Worker jobs**. The JSON paste/upload form is
  **[not runtime-verified]** as a dedicated screen; use the API.

**Step by step.**

1. Prepare the document. Field mapping is driven by
   `config/mappings/jira-mvp.yaml` loaded by
   `JiraJsonConnector.from_yaml(...)`; the built-in defaults
   (`packages/eoip/connectors/jira_json.py`, `DEFAULT_MAPPING`) expect
   `key`, `fields.summary`, `fields.issuetype.name`, `fields.status.name`,
   `fields.project.key`, `fields.assignee.displayName`, optional
   `fields.parent.key`, and optional `deleted` / `deleted_at` flags.
2. Submit the import:

```bash
curl -s -X POST http://localhost:8000/api/v1/admin/ingestion/jira \
  -H 'Content-Type: application/json' \
  -d '{
    "document": {
      "issues": [
        {
          "key": "EOIP-123",
          "fields": {
            "summary": "Checkout totals exclude gift-wrap fee",
            "description": "Seen on tenant t-001 production checkout.",
            "issuetype": {"name": "Bug"},
            "status": {"name": "In Progress"},
            "project": {"key": "EOIP", "name": "EOIP Platform"},
            "assignee": {"accountId": "5f-a1", "displayName": "A. Rivera",
                         "emailAddress": "arivera@example.com"}
          }
        }
      ]
    },
    "dry_run": false
  }'
```

3. The response is the queued job (payload stripped):

```json
{"job_id": "7c9e2f1e-...", "kind": "JIRA_JSON", "status": "PENDING",
 "created_at": "...", "correlation_id": "...", "tenant_id": "t-001",
 "created_by": "local-user"}
```

4. Poll `GET /api/v1/admin/jobs/{job_id}` until `status` is `SUCCEEDED` or
   `PARTIAL`.

**Response/result.** When the worker finishes, the job's `result` contains
(from `JiraIngestionService.ingest_events`):

- `run_id`, `run_status` (`SUCCEEDED`, `PARTIAL`, or `DRY_RUN`),
- `records_seen`, `records_accepted`, `records_rejected`,
- `rejected`: a list of `{event_id, source_record_id, error}`.

In the graph you get canonical IDs such as
`urn:eoip:work:project:jira:EOIP`, `urn:eoip:work:item:jira:EOIP-123`, and
`urn:eoip:evidence:source-event:jira:<event_id>`. Confirm via
`GET /api/v1/entities/{canonical_id}` (URL-encode the URN) or
`GET /api/v1/ingestion/runs` to see the `IngestionRun` summary with
`run_kind: "JIRA_JSON"` and `counts`.

**Errors and recovery.**

- `EOIP-123`-style records missing `key` are rejected with
  `"missing required Jira issue key"`; records missing a summary (and not
  flagged `deleted`) are rejected with `"EOIP-123: missing required summary"`.
  Rejected records go to the DLQ and the run becomes `PARTIAL` — the job still
  succeeds overall.
- Top-level JSON that is neither a list nor an object with `issues`/`values`
  fails the job (`FAILED` with the `TypeError` name in `error`).
- Nothing is written when `dry_run: true` — see
  [Incremental checkpoints and the dry-run flag](#incremental-checkpoints-and-the-dry-run-flag).

---

## Importing a GitLab JSON export

**What it does.** Turns a fixture-shaped GitLab export — an object with
`merge_requests` and `pipelines` lists — into merge-request and pipeline
vertices linked to Jira work items by extracted issue keys. Issue keys are
taken from an explicit `work_item_keys` list **and** scanned out of
`source_branch`, `title`, `description` (MRs) or `ref`, `name` (pipelines)
using the pattern `\b[A-Z][A-Z0-9]+-\d+\b`
(`packages/eoip/connectors/gitlab_json.py`).

**How to access.** `POST /api/v1/admin/ingestion/gitlab` (status 202).

**Step by step.**

1. Submit with an optional `repository_id` (default `"demo"`; must match
   `^[A-Za-z0-9][A-Za-z0-9._/-]*$`, max 128 chars):

```bash
curl -s -X POST http://localhost:8000/api/v1/admin/ingestion/gitlab \
  -H 'Content-Type: application/json' \
  -d '{
    "repository_id": "checkout",
    "document": {
      "merge_requests": [
        {"iid": 42, "title": "Fix EOIP-123 gift-wrap totals",
         "state": "merged", "source_branch": "bugfix/EOIP-123-totals",
         "target_branch": "main", "merge_commit_sha": "..."}
      ],
      "pipelines": [
        {"id": 9001, "name": "checkout-ci", "status": "success",
         "ref": "bugfix/EOIP-123-totals", "sha": "..."}
      ]
    },
    "dry_run": false
  }'
```

2. Poll `GET /api/v1/admin/jobs/{job_id}`.

**Response/result.** Same envelope as Jira (`run_id`, `run_status`,
`records_seen`, `records_accepted`, `records_rejected`, `rejected`). The
worker runs this as kind `GITLAB_JSON` via
`GitLabIngestionService` (`packages/eoip/ingestion/gitlab.py`) with mapper
version `gitlab-json/1.0`.

**Errors and recovery.**

- `"merge request requires iid and title"` — an MR record missing `iid` or a
  blank `title`; fix the record and re-submit, or replay the DLQ entry after
  fixing the source.
- `"pipeline requires id"` — pipeline record missing `id`.
- `"GitLab fixture must be a JSON object"` — you posted a list or scalar.
- Non-dict items inside the lists are replaced with `{"_invalid_record": ...}`
  and rejected at mapping; the run reports `PARTIAL`.

---

## Registering a source

**What it does.** Creates a durable, non-secret configuration entry in the
local source registry (`<data root>/state/source-registry.json`, written
atomically by `packages/eoip/connectors/registry.py`). Secrets are never
stored — only `secret_refs` such as `"env://JIRA_TOKEN"`.

**How to access.**

- API: `POST /api/v1/sources` (201), `GET /api/v1/sources`,
  `GET /api/v1/sources/{source_id}`, `PATCH /api/v1/sources/{source_id}`,
  `DELETE /api/v1/sources/{source_id}` (204).
- UI: the Studio **Connector Builder** (`apps/web/src/studio/ConnectorBuilder.jsx`)
  walks a 4-step wizard — step 0 **Source type** (Connector select + Manifest
  name), step 1 **Connection** parameters (`base_url` is required for `api`
  sources), step 2 **Authentication** (auth type select; secret fields are
  redacted as `<redacted>` in the manifest), step 3 **Scope** (entities).
  Validation messages shown include "Name is required.", "Connection parameter
  "base_url" is required for API sources.", and "Scope must list at least one
  entity type.". **[not runtime-verified]** whether the wizard POSTs directly
  to `/api/v1/sources` in your build — the API path below always works.

**Step by step (API).** The body is a `SourceRegistryEntry`
(`packages/eoip/contracts/source_registry.py`). Key fields:

| Field | Notes |
|---|---|
| `source_id` | pattern `^[A-Za-z0-9][A-Za-z0-9._-]*$`, ≤128 chars |
| `source_type` | free-form string, e.g. `jira`, `gitlab`, `github`, `confluence`, `servicenow`, `documents` |
| `name`, `base_url` | display name / endpoint |
| `acquisition_modes` | subset of `baseline`, `poll`, `webhook`, `reconcile`, `replay` |
| `capabilities` | `baseline`, `polling`, `webhooks`, `deletion_events`, `permission_events`, `discovery`, `reconciliation`, `replay` (booleans) |
| `polling_frequency_seconds`, `freshness_slo_seconds` | 1..31,536,000 |
| `secret_refs` | map of name → `"env://VAR_NAME"` |
| `config` | non-secret config; keys containing `password`, `secret`, `token`, `credential`, `api_key`, `private_key` are **rejected** with "config contains secret-like keys; use secret_refs" |
| `enabled`, `webhook_status`, `health` | lifecycle/status |

```bash
curl -s -X POST http://localhost:8000/api/v1/sources \
  -H 'Content-Type: application/json' \
  -d '{
    "source_id": "jira-eoip-prod",
    "source_type": "jira",
    "name": "Jira — EOIP project (prod)",
    "base_url": "https://jira.example.com",
    "acquisition_modes": ["baseline", "poll", "webhook"],
    "capabilities": {"baseline": true, "polling": true, "webhooks": true,
                     "discovery": true, "replay": true},
    "polling_frequency_seconds": 300,
    "secret_refs": {"api_token": "env://JIRA_TOKEN",
                    "webhook_hmac": "env://JIRA_WEBHOOK_SECRET"},
    "enabled": true
  }'
```

**Response/result.** `201` with the stored entry including `schema_version:
"1.0"`, `created_at`, `updated_at`.

**Errors and recovery.**

- `409 "Source already exists"` — pick a new `source_id` or `PATCH` the
  existing one. `schema_version`, `source_id`, and `created_at` are immutable
  (a `PATCH` touching them returns `422`).
- `422` from the secret-key validator — move the value into `secret_refs`.
- `PATCH` with an empty body returns `422 "At least one source field is required"`.

---

## Running source operations: baseline, discovery, dry-run, sync, reconcile, replay

**What they do.** Queue or run acquisition operations against a registered
source through the acquisition scheduler
(`packages/eoip/connectors/acquisition.py`), which enforces per-source
concurrency and rate limits and persists checkpoints.

**How to access** (all in `apps/api/main.py`; body model
`SourceOperationRequest = {checkpoint: str?, event_ids: string[], dry_run: bool}`):

| Endpoint | Operation queued |
|---|---|
| `POST /api/v1/sources/{id}/baseline` (202) | `BASELINE` |
| `POST /api/v1/sources/{id}/discover` | synchronous `connector.discover(scope)` |
| `POST /api/v1/sources/{id}/dry-run` (202) | `BASELINE`, or `POLL` if you pass a `checkpoint`; forces `dry_run: true` |
| `POST /api/v1/sources/{id}/sync` (202) | `POLL` |
| `POST /api/v1/sources/{id}/reconcile` (202) | `RECONCILE` |
| `GET  /api/v1/sources/{id}/reconciliations` | list past reconciliation reports |
| `GET  /api/v1/sources/{id}/checkpoint` | registry checkpoint + connector state file |
| `POST /api/v1/sources/{id}/replay` (202) | `REPLAY` of captured `event_ids` |
| `GET/PUT /api/v1/sources/{id}/schedule`, `POST .../pause`, `POST .../resume` | acquisition policy management |

**Step by step.**

1. Discover what the source offers (synchronous, no job):

```bash
curl -s -X POST http://localhost:8000/api/v1/sources/jira-eoip-prod/discover \
  -H 'Content-Type: application/json' \
  -d '{"include": ["project:EOIP"], "exclude": [], "options": {}}'
```

2. Run a dry-run baseline to validate credentials and mapping without writing:

```bash
curl -s -X POST http://localhost:8000/api/v1/sources/jira-eoip-prod/dry-run \
  -H 'Content-Type: application/json' -d '{}'
```

3. Run the real baseline: same call against `/baseline`.
4. Afterwards, keep current with `/sync` (a `POLL`); the stored checkpoint is
   used automatically, or pass `"checkpoint": "<value>"` explicitly.
5. Replay specific captured events after fixing a mapping:

```bash
curl -s -X POST http://localhost:8000/api/v1/sources/jira-eoip-prod/replay \
  -H 'Content-Type: application/json' \
  -d '{"event_ids": ["<64-char-sha256>"], "dry_run": false}'
```

**Response/result.** `202` with the queued job (`kind: "SOURCE_OPERATION"`).
Discovery returns `DiscoveryResult`: `source_id`, `resources[]`
(`resource_id`, `resource_type`, `name`, `estimated_records`, `metadata`),
and `warnings[]`. `GET .../checkpoint` returns
`{source_id, registry_checkpoint, baseline_complete, state}` where `state` is
the content of `<data root>/state/connectors/{source_id}.json`.

**Errors and recovery.**

- `404 "Source not found"` — bad `source_id`.
- `409 "Source discovery capability is not enabled"` — set
  `capabilities.discovery: true` and `enabled: true`.
- `409` with `"source concurrency limit reached"` or `"source rate limit
  reached"` — the acquisition policy throttled you; wait or adjust
  `PUT .../schedule`.
- `503 "Connector discovery unavailable: <category>"` — the remote system
  failed; `category` is one of the connector error categories such as
  `timeout`, `transport_error`, `rate_limited`, `remote_error`.

---

## Incremental checkpoints and the dry-run flag

**Checkpoints.** Each connector persists per-source state in
`<data root>/state/connectors/{source_id}.json`; the registry entry also
carries `checkpoint`, `last_successful_baseline`, and `last_incremental_run`.
Sync services return `next_checkpoint` in their result (see
`SourceSyncIngestionService.ingest` in `packages/eoip/ingestion/source_sync.py`),
so a `POLL` always resumes where the last successful run stopped. Inspect the
current position with `GET /api/v1/sources/{source_id}/checkpoint`;
`baseline_complete` is true when either the registry's
`last_successful_baseline` or the state file's `baseline_complete` flag is set.

**Dry-run-only.** Every ingestion path accepts `dry_run: true`:

- The result reports `run_status: "DRY_RUN"`.
- No raw capture files, no DLQ records, and **no graph mutations** are written
  (the `if not dry_run:` guards in `jira.py` / `source_sync.py` skip capture,
  `begin_run`, and all `upsert_*` calls).
- The dedicated `POST /api/v1/sources/{id}/dry-run` endpoint forces
  `dry_run: true` server-side even if you forget the flag.

Use dry-run first whenever you change a mapping file or point a source at a
new project.

---

## How the worker processes jobs

**What it does.** `apps/worker/main.py` is a single durable filesystem worker:
it scans `<data root>/jobs/*.json` every 2 seconds, executes jobs whose
`status` is `PENDING` (or stale `RUNNING`) and whose `next_attempt` time has
passed, and writes results back into the same file. "Interrupted jobs replay
idempotently" (module docstring).

**Job kinds** (from `execute_job`): `DEMO`, `JIRA_JSON`, `GITLAB_JSON`,
`REPLAY`, `CONFLUENCE`, `SERVICENOW`, `SOURCE_OPERATION` (dispatched by
`source_type` to file/github/gitlab/jira/registered handlers), and
`SOURCE_WEBHOOK`.

**Lifecycle.**

1. **Submit** — `POST` endpoint calls `queue.submit(kind, payload, ...)`;
   the job starts as `PENDING` (`packages/eoip/jobs.py`, `submit`).
2. **Lease (optional HA)** — if `EOIP_LEASE_PATH` is set, only the worker
   holding the `LeaderLease` (TTL `EOIP_LEASE_TTL_SECONDS`, default 30 s)
   processes jobs; contenders log `worker.lease_contended` and idle.
3. **RUNNING** — the worker stamps `started_at` and runs `execute_job`.
4. **Finish** — success sets `SUCCEEDED`; if the result's `run_status` is
   `PARTIAL` (some records rejected), the job is marked `PARTIAL`. After each
   job the worker also runs the default semantic consumers
   (`run_default_consumers`) and emits an audit event with
   `event_type: "ingestion"`.
5. **Retries** — a `ConnectorError` in category `timeout`,
   `transport_error`, `rate_limited`, or `remote_error` is retried up to 3
   attempts with backoff `next_attempt = now + 2**attempts`, then `FAILED`.
   `httpx.HTTPError`/`OSError` get the same 3-attempt treatment. Any other
   exception marks the job `FAILED` immediately with `error` set to the
   exception type name.
6. **HELD** — jobs restored from a backup snapshot are re-imported as `HELD`
   with `recovery` metadata (`packages/eoip/snapshot.py`). They never run
   until re-admitted.
7. **CANCELLED** — see next section.

Watch progress: `GET /api/v1/admin/jobs` (list), `GET /api/v1/admin/jobs/{id}`
(detail, payload hidden), `GET /api/v1/admin/worker` (worker heartbeat), or the
Admin dashboard **Worker jobs** panel. Note the cross-tenant guard: a job
belonging to tenant `t-001` raises `403 "Cross-tenant job access forbidden"`
for other tenants.

---

## Cancelling and re-admitting jobs

**Cancel** — `POST /api/v1/admin/jobs/{job_id}/cancel`.

- Works for `PENDING` and `HELD` jobs → status becomes `CANCELLED` with a
  `finished_at` stamp.
- A `RUNNING` job returns `409 "Running jobs cannot be cancelled safely"` —
  wait for it to finish instead.
- Unknown job → `404 "Job not found"`; cross-tenant → `403`.

**Readmit** — `POST /api/v1/admin/jobs/{job_id}/readmit` (202). This is the
recovery path for `HELD` jobs (e.g. after a snapshot restore):

- Only `HELD` jobs are eligible; anything else returns `409 "Only held
  recovery jobs can be re-admitted"` (plain queue jobs) or `"Only held source
  operation jobs can be re-admitted"` (`SOURCE_OPERATION`).
- Readmission re-checks admission policy, resets `attempts` to 0, stamps a new
  `correlation_id`, clears `started_at`/`finished_at`/`next_attempt`/`error`/
  `result`, and records `recovery.readmitted_at` — your audit trail that a
  human confirmed the retry.
- Allowed kinds: `SOURCE_OPERATION`, `SOURCE_WEBHOOK` (which additionally
  re-validates the captured webhook receipt, including that the receipt file
  name matches the SHA-256 of the `delivery_id`), plus `DEMO`, `JIRA_JSON`,
  `GITLAB_JSON`, `REPLAY`, `CONFLUENCE`, `SERVICENOW`. Other kinds return
  `409 "Job kind cannot be re-admitted"`.
- A `HELD` job without `recovery` metadata returns `422 "Held job lacks
  recovery metadata"`.

```bash
curl -s -X POST http://localhost:8000/api/v1/admin/jobs/7c9e2f1e-.../readmit
```

---

## The dead-letter queue (DLQ)

**What it does.** Every rejected source record is written once, idempotently,
to `<data root>/dlq/<event_id>.json` with the unified envelope from
`packages/eoip/ingestion/dlq.py`: `event_id`, `source_system`,
`source_record_id`, `payload_hash`, `stage` (e.g. `mapping`),
`error_category` (e.g. `mapping_error`, `parse_error`, `schema_drift`,
`invalid_fact`), `error`/`errors` (safe messages, never secrets), `run_id`,
`correlation_id`, `replay_ref`, `retry_state` (default `"UNPROCESSED"`), and
the embedded `source_event`.

**How to access.**

- `GET /api/v1/admin/dlq` or `GET /api/v1/ingestion/dlq` (`?limit=1..500`).
- `POST /api/v1/admin/dlq/{event_id}/replay` (202) — replay one dead-lettered
  event.
- Bulk: `POST /api/v1/admin/ingestion/replay` or `/api/v1/ingestion/replay`
  with `{"source_system": "jira"|"gitlab"|"git", "event_ids": [...],
  "repository_id": "demo", "dry_run": false}`.

**Step by step (single-record replay).**

1. `GET /api/v1/admin/dlq` and copy the `event_id` (a 64-char hex SHA-256).
2. Fix the root cause (mapping file, source data).
3. `POST /api/v1/admin/dlq/<event_id>/replay`.

The endpoint verifies before queueing: the captured raw event must exist
(`409 "Captured source event is unavailable"`), its `event_id` and
`payload_hash` must match the DLQ record (`409 "Captured source event does
not match the dead-letter record"`), and the source system must be one of
`jira`, `gitlab`, `git`, `github`, `confluence`, `servicenow` (`422 "This
dead-letter source does not support replay"`).

**Errors and recovery.**

- `404 "Dead-letter record not found"` — bad id, or the id is not lowercase
  hex (the route enforces `^[a-f0-9]{64}$`).
- Bulk replay with non-hex ids → `422 "Replay event IDs must be lowercase
  SHA-256 values"`.
- Replay of event ids that were never captured → the replay job fails with
  `ValueError("captured events not found: [...]")` (`packages/eoip/ingestion/replay.py`).

A `REPLAY` job result includes `run_status`, `records_seen`,
`records_replayed`, `source_system`, and a `logical_diff` of stable graph
additions/removals/changes — replay is idempotent by construction.

---

## Profiling JSON datasets

**What it does.** The schema profiler (`packages/eoip/ingest/profile.py`,
requirements SR-ING-010/012/013/016) profiles raw JSON records: per-field
types, nullability, cardinality (capped at 10,000 distinct values), uniqueness,
enum candidates (≤20 distinct values with ≥80% fill), format detection
(`email`, `uuid`, `url`, `ip`, `iso_datetime`, `currency`, `phone`, `iban`,
`git_sha`, `ticket_key`, `file_path`), key candidates with stability scores,
and explicit cross-dataset relationships. It is deterministic — same records,
same report, any order.

**How to access** (router built by `build_router()`, mounted at
`/api/v1/ingest/profile`):

- `POST /api/v1/ingest/profile` — body `{"dataset": "checkout-events", "records": [...]}` → `ProfileReport`
- `POST /api/v1/ingest/profile/drift` — body `{"before": <ProfileReport>, "after": <ProfileReport>}` → `ProfileDrift`
- `POST /api/v1/ingest/profile/keys` — same body as profile → `KeyCandidate[]`
- `POST /api/v1/ingest/profile/relationships` — body `{"datasets": [DatasetProfile...]}` → `RelationshipCandidate[]`

**Step by step.**

1. Profile:

```bash
curl -s -X POST http://localhost:8000/api/v1/ingest/profile \
  -H 'Content-Type: application/json' \
  -d '{"dataset": "checkout-events", "records": [
        {"order_id": "EOIP-123", "email": "arivera@example.com",
         "total": 42.50, "currency": "USD",
         "created_at": "2026-01-05T12:00:00Z"},
        {"order_id": "EOIP-124", "email": "bshen@example.com",
         "total": 9.99, "currency": "USD",
         "created_at": "2026-01-05T12:04:11Z"}
      ]}'
```

2. Detect keys:

```bash
curl -s -X POST http://localhost:8000/api/v1/ingest/profile/keys \
  -H 'Content-Type: application/json' -d '<same body>'
```

3. Diff two profiles after a schema change: save both `ProfileReport`
   responses and POST them as `{"before": ..., "after": ...}` to
   `/api/v1/ingest/profile/drift`.
4. Discover relationships between two datasets: profile each, then POST
   `{"datasets": [{"name": "checkout-events", "report": <report>, "records":
   [...], "primary_key": "order_id"}, {"name": "...", ...}]}`.

**Response/result.**

- `ProfileReport`: `profile_id` (`urn:eoip:ingest:profile:<slug>`),
  `record_count`, `fields[]` — each a `FieldProfile` with `path`, `kind`,
  `observed_types`, `total_count`, `null_count`, `cardinality`,
  `cardinality_capped`, `unique_ratio`, `enum_candidate`, `enum_values`,
  `formats`, `array_item_types`, `object_fields`, `max_nesting_depth`.
- `KeyCandidate`: `key_id`, `dataset`, `fields`, `composite`, `stability`
  (0..1), `name_hint`, `non_null_ratio`, `unique_ratio`, `minting`
  (`"deterministic-namespaced"`).
- `ProfileDrift`: `drift_id`, `changes[]` — each a `FieldDrift` with `path`,
  `change` ∈ `added | removed | type_changed | format_changed |
  nullability_changed | cardinality_changed | enum_value_added`, `detail`.
- `RelationshipCandidate`: `relationship_id`
  (`urn:eoip:ingest:relationship:<slug>`), `method` ∈ `foreign_key_like |
  parent_pointer | url_reference | array_of_ids | type_id_pair`,
  `edge_class` (`ASSERTED` by default — the honesty hook; see
  [Provenance](#provenance-and-evidence)), `confidence`, `from_dataset`,
  `from_field`, `to_dataset`, `to_field`, `evidence` (sample values).

**Errors and recovery.** Bodies forbid extra keys (`extra="forbid"`); unknown
fields → `422`. Statistical relationship discovery (MinHash/LSH, embeddings)
is **ADR-gated / deferred** — only the explicit signals above are implemented;
the profiler's own docstring says so. Value-overlap inclusion-dependency
discovery is marked partial (SR-ING-014).

---

## Graph-build endpoints

**What they do.** Twelve deterministic builders under
`POST /api/v1/graphbuild/*` (`packages/eoip/graphbuild/router.py`). They are
pure functions: they **propose** — they do not write the graph. Results are
`GraphDelta` envelopes with `delta_id`, `vertices`, `edges`
(`ProposedEdge`: `edge_id`, `label`, `from_id`, `to_id`, `score`, `method`,
`evidence`), `classes`, `properties`, `notes`.

### Schema induction

`POST /api/v1/graphbuild/schema/induce` — profile records, then propose one
class per object-level field path plus scalar properties
(`packages/eoip/graphbuild/schema.py`).

```bash
curl -s -X POST http://localhost:8000/api/v1/graphbuild/schema/induce \
  -H 'Content-Type: application/json' \
  -d '{"dataset": "checkout-events", "root_class": "Order",
       "records": [{"order_id": "EOIP-123", "buyer": {"email": "a@b.c"}}]}'
```

Returns `InducedSchema`: `schema_id`, `dataset`, `classes[]` (`class_id`,
`name`, `source`, `member_count`, `evidence`), `properties[]`
(`property_id`, `name`, `domain`, `range`, `functional`, `required`).

### Construction plan

`POST /api/v1/graphbuild/plan` — order the build steps for a mode
(`ontology-first`, `data-first`, `hybrid`; default `hybrid`).

```json
{"mode": "hybrid", "dataset": "checkout-events",
 "ontology_classes": ["WorkItem", "Person"]}
```

Returns `ConstructionPlan`: `plan_id`, `mode`, `dataset`, `steps[]` (e.g.
`validate-ontology-manifest`, `profile-dataset`, `induce-schema`,
`anchor-core-classes`, `reconcile-conflicts-to-review`, `validated-write`),
`reconciliation` (`match:existing` / `propose:extension` / `add:induced` /
`review:conflict`).

### Co-change edges

`POST /api/v1/graphbuild/cochange` — files that change together in commits.

```json
{"commits": [{"sha": "abc1", "files": ["src/checkout.py", "src/cart.py"]}],
 "config": {"min_support": 2, "min_confidence": 0.2,
            "min_files_per_commit": 2, "max_files_per_commit": 200,
            "top_k": 1000}}
```

### Inclusion dependencies

`POST /api/v1/graphbuild/inclusion-dependencies` — MinHash/LSH containment
between columns. Body: `{"columns": {"a": [...], "b": [...]}, "config":
{"num_hashes": 64, "num_bands": 16, "sample_size": 500, "min_containment": 0.8}}`.

### Mentions

`POST /api/v1/graphbuild/mentions` — gazetteer entity extraction over
documents. Body: `{"entities": {"EOIP-123":
"urn:eoip:work:item:jira:EOIP-123"}, "aliases": {"gift-wrap bug":
"urn:eoip:work:item:jira:EOIP-123"}, "documents": {"doc1": "The gift-wrap bug
blocks checkout on t-001."}}` (aliases are case-folded).

### Hierarchy

`POST /api/v1/graphbuild/hierarchy` — induce parent/child structure from
records. Config (`HierarchyConfig`): `method` ∈ `parent_pointer |
path_string | lexical_clustering` (default `parent_pointer`), `parent_field`
(default `parent_id`), `path_field` (`path`), `name_field` (`name`),
`id_field` (`id`), `delimiter` (`/`).

### Rollup

`POST /api/v1/graphbuild/rollup` — hierarchical community rollup over an
adjacency map: `{"adjacency": {"a": ["b"], "b": ["a","c"]},
"base_partition": null, "max_levels": 4}`.

### Similarity

`POST /api/v1/graphbuild/similarity` — k-NN cosine graph over embeddings:
`{"embeddings": {"doc1": [0.1, 0.2], "doc2": [0.1, 0.21]}, "config": {"k": 5,
"min_similarity": 0.5, "include_mutual_only": false}}`.

### Link prediction

`POST /api/v1/graphbuild/link-prediction` — score candidate pairs:
`{"adjacency": {...}, "config": {"method": "adamic_adar", "top_k": 500,
"max_candidates_per_node": 500, "min_score": 0.0}}`; methods:
`common_neighbors`, `adamic_adar`, `preferential_attachment`.

### Repair

`POST /api/v1/graphbuild/repair` — structural audit:
`{"vertices": ["urn:eoip:work:item:jira:EOIP-123"], "edges": [...]}` returns a
repair report.

### Enrichment submit

The `build_graphbuild_router()` docstring lists
`POST /api/v1/graphbuild/enrichment/submit`, but **no handler for it is
defined in `packages/eoip/graphbuild/router.py`** — only the ten routes above
are registered. Treat this route as documented-but-not-implemented; calling it
returns `404`.

**Errors and recovery.** All builders validate their config with pydantic
(`extra="forbid"`): out-of-range values (`min_confidence > 1.0`) or unknown
keys → `422`. These endpoints never touch the store, so failures leave no
partial state.

---

## Provenance and evidence

**What is captured per fact.**

- Every accepted source record becomes an `Evidence` vertex, e.g.
  `urn:eoip:evidence:source-event:jira:<event_id>`, with `source_system`,
  `source_ref` (e.g. `jira://issue/EOIP-123`), `source_id`, `source_version`,
  `method: "SOURCE_EVENT"`, `captured_at`, `evidence_key` (the event id),
  `content_hash` (the payload SHA-256), `mapper_version` (e.g.
  `jira-json/1.0`), plus `ontology_version` and `schema_version`.
- Domain vertices carry `source_system`, `source_id`, `source_version`,
  `mapper_version`, `first_seen`, `last_seen`, `valid_from`, `modified_at`,
  and `ingestion_run_id` (see `packages/eoip/ingestion/jira.py`, the `shared`
  dict).
- Edges carry `fact_key` (stable identity), `evidence_key`, `source_ref`,
  `source_system`, `ingestion_run_id`, and `creation_status` (default
  `"DETERMINISTIC"`).
- Edge honesty classes: the profiler tags discovered relationships as
  `ASSERTED`, `DERIVED`, `INFERRED`, or `CURATED`
  (`packages/eoip/ingest/profile.py`, SR-ING-016 hook). Asserted facts come
  straight from a source; inferred ones say so.
- Every run is an `IngestionRun` vertex (`run_kind`, `run_status`,
  `counts`, `ontology_version`, `schema_version`) with `INGESTED_IN` edges
  from each touched entity, and every job completion emits a hash-chained
  audit event (`GET /api/v1/admin/audit`).

**Where to inspect it.**

- `GET /api/v1/entities/{canonical_id}` — vertex with its properties
  (provenance fields included).
- `GET /api/v1/ingestion/runs` — run history with statuses and counts.
- `GET /api/v1/graph/as-of`, `/api/v1/graph/versions`, `/api/v1/graph/diff`,
  `/api/v1/change-journal` — temporal and evolution views.
- On disk: raw captures in `<data root>/raw/<source_system>/<event_id>.json`,
  DLQ in `<data root>/dlq/`, receipts in `<data root>/receipts/<source_id>/`,
  reconciliation reports in `<data root>/state/reconciliation/<source_id>/`.

---

*Grounding note: endpoints and field names were read directly from
`apps/api/main.py`, `apps/worker/main.py`, `packages/eoip/connectors/`,
`packages/eoip/ingestion/`, `packages/eoip/ingest/profile.py`, and
`packages/eoip/graphbuild/`. Items marked **[not runtime-verified]** were not
exercised against a running server while writing this chapter.*
