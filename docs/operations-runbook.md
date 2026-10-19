# Operations and Troubleshooting

Scope: the current local Compose topology and host-development entry points. This is not a certified production HA runbook. Operators need an agreed deployment profile, data retention policy, recovery objectives and access policy before serving customer data.

## Routine Operations

From the repository root, PowerShell:

```powershell
.\scripts\container.ps1 detect
.\scripts\container.ps1 status
.\scripts\container.ps1 logs
```

The Bash helper accepts the corresponding actions. `detect` discovers tooling; it is not a full deployment health check. `up` initializes missing local credentials, builds and starts the default stack, and waits for health. `down` stops the default project without deleting its volumes. `rebuild` rebuilds/recreates application components while retaining volumes; it is not a data migration or recovery procedure.

The launcher's `test` action runs tests against the configured stack and can mutate demo data. `demo-data` loads synthetic content additively. Use dedicated test installations, not customer environments. Acceptance actions create isolated project names and remove those disposable volumes during cleanup; review their script before running them.

## What Must Be Preserved

| State | Location in default Compose | Recovery concern |
|---|---|---|
| Graph | `graph-data` volume, HugeGraph | Canonical facts, ontology and provenance; logical exports and physical vendor backups have different guarantees |
| Application state | `application-data`, mounted as `/data` | Jobs, raw source evidence, checkpoints, audit, registry and service-specific records |
| Hubble | `hubble-data`, `hubble-uploads` | Administration metadata/uploads; not the canonical graph backup |
| Local model | `model-data` when enabled | Optional model files and separate licensing/resource considerations |
| Configuration and secrets | Repository config plus private deployment configuration | Configuration compatibility and independent secure credential recovery |
| Metrics | `metrics-data` with observability | Operational history; not authoritative graph or business state |

Some domain modules use process-local state. Inventory the exact service before promising restart recovery. An API process and worker process using `memory` each have their own graph; shared `EOIP_DATA_DIR` does not make their graph stores shared.

## Health and Diagnosis

1. Check service status and `/health/live`, then `/health/ready` on the correct API URL.
2. Make an authorized bounded query for an expected entity and inspect source/job state. Liveness alone proves neither data availability nor authorization correctness.
3. Correlate request and worker logs using `X-Correlation-ID`, job ID and audit ID where emitted. Redact tokens and payloads before sharing logs.
4. Inspect current and failed jobs, connector error categories and checkpoint history. Do not manually edit job JSON to declare success.
5. Verify storage capacity, mounts and permissions. Confirm the intended backend and dataset, not just the default port.

| Symptom | Likely boundary to inspect | Safe next action |
|---|---|---|
| Token startup error | `EOIP_API_TOKEN` missing/too short in this process | Set a private valid token in the actual process/container environment; do not print it |
| Host cannot resolve `hugegraph-server` | Container DNS URL used outside Compose | Select disposable memory mode or configure a reachable persistent backend |
| Web `/api` returns HTML/404 | Wrong frontend/proxy configuration | Check `EOIP_DEV_API_URL` for `apps/web`; alternate frontend has different wiring |
| UI works until reload then needs token | Current in-memory browser credential handling | Reconnect; persistent suite SSO is a proposal, not current default behavior |
| API 401/403 | Identity, token or service authorization | Verify grants without adding broad roles or trusting caller tenant headers |
| Admin mutation 503 | Audit preflight or service unavailable | Inspect audit/storage health; do not bypass audit to force the mutation |
| Empty graph after restart | Memory backend or wrong backend selection | Use a persistent profile; confirm intended data source before re-ingestion |
| Jobs remain pending | Worker stopped, wrong data root, backend failure or lease contention | Inspect heartbeat, mounts and logs; keep one qualified writer |
| API cannot see worker-ingested entities | Separate in-memory stores | Use the same reachable persistent graph service for both processes |
| MCP failure | Wrong API URL/token, transport host policy or unsupported tool | Inspect real MCP initialization/discovery and local allowlist |
| Report/model dependency error | Optional extra/model profile unavailable | Install/qualify only the needed profile; do not fabricate output |
| Browser test cannot reach `eoip-web` | Container hostname in host-side test defaults | Set `PLAYWRIGHT_BASE_URL` for the chosen host and test profile |
| Port already occupied | Another service or deployment | Inspect the owner; select another port and update clients instead of killing unrelated services |

## Backup and Restore

The helpers expose `backup`, `backup-bundle` and `restore-test`. Read [backup.py](../scripts/backup.py), [restore.py](../scripts/restore.py), [snapshot.py](../packages/eoip/snapshot.py) and [recovery_bundle.py](../packages/eoip/recovery_bundle.py) before applying them to valuable data.

`backup` stops the worker but leaves the API running. Establish a maintenance window and prevent all other writers, including vendor consoles and external integrations, before claiming a consistent snapshot. `backup-bundle` stops selected running application writers and exports the bundle using a tool container; external/vendor writers still need explicit quiescence. Neither helper proves every future module's state is included.

1. Record the exact source backend, configuration, versions and writer shutdown procedure.
2. Create the chosen backup in a private location with sufficient capacity; inspect its manifest and checksums.
3. Retain a copy outside the running installation with appropriate access/encryption/retention.
4. Restore into an empty, isolated graph and data root. Bundle restore requires explicit empty configuration and model targets.
5. Independently compare canonical records, relationships, provenance and required state; test authentication, denied access, pending jobs and replay safety.
6. Record elapsed recovery time and observed loss boundary. A successful checksum is not proof of external-effect consistency or the business recovery objective.

Never point restore at the only working source. Never use `down --volumes` as a troubleshooting step for data you need. `restore-test` exercises its declared disposable target; it does not automatically authorize a production cutover.

## Incident Handover

Provide the build/commit, deployment profile, UTC interval, sanitized configuration differences, affected tenant/source/job IDs, correlation IDs, errors, observed impact and actions taken. Preserve original evidence in controlled storage. Do not attach private `.env` files, credentials, unrestricted raw source captures or customer exports.

For schema changes, upgrades and rollback decisions, use [Migration and Refactoring](migration-refactoring-guide.md). For release authorization, use [Release Checklist](release-checklist.md).
