# Ingestion Worker

`main.py:main` is the default filesystem-backed polling worker. `execute_job` dispatches jobs into ingestion services. It is separate from the API process but shares the configured persistent graph and application data directory in Compose.

## Supported Dispatch Paths

Current dispatch includes `DEMO`, `JIRA_JSON`, `GITLAB_JSON`, `REPLAY`, configured Confluence/ServiceNow jobs, `SOURCE_OPERATION` and `SOURCE_WEBHOOK`. Registered source handling selects source-specific services; adding a connector class alone does not add a working worker job.

Run `python -m apps.worker.main` only after selecting the same persistent graph connection and `EOIP_DATA_DIR` as the API. Prefer the [default deployment](../../deploy/README.md) for an integrated run. A memory backend is process-local and therefore unsuitable for separate API/worker graph sharing.

## State and Failure Semantics

The worker polls job JSON, processes eligible `PENDING`/`RUNNING` records, writes state transitions and emits audit information. Interrupted processing can be retried, so handlers must be idempotent. Retryable connector/transport failures have bounded retries and backoff. Some service outcomes are `PARTIAL`; they must not be displayed as full success.

Heartbeat writes `state/worker.json` under the data root. `EOIP_LEASE_PATH` enables an advisory filesystem leader lease. Neither heartbeat nor lease proves multi-host correctness or exactly-once effects. Do not scale replicas just because an HA deployment file exists.

`EOIP_LOAD_DEMO` defaults to true in this worker. Disable it explicitly for non-demo deployments. Raw evidence, DLQ and checkpoints can contain sensitive source data; apply access/retention controls.

## Maintenance

Inspect job state, heartbeat, graph connectivity and logs before replaying work. Do not manually rewrite JSON statuses or reset checkpoints to mask failures. Add dispatch/handler tests, duplicate/restart tests and independent source-to-graph reconciliation for a new job. Use [testing](../../docs/testing-guide.md), [operations](../../docs/operations-runbook.md) and [connector qualification](../../docs/connectors/qualification.md).
