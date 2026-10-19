# Deployment Assets

Start with [Getting Started](../docs/getting-started.md) and [Operations](../docs/operations-runbook.md). The normal entry points are `scripts/container.ps1` and `scripts/container.sh`, run from repository root. Do not run deployment commands against customer data without confirming the intended environment.

## Asset Map

| Asset | Purpose and qualification boundary |
|---|---|
| `docker-compose.yml` | Default local HugeGraph/API/worker/MCP/web/Hubble topology with optional profiles |
| `Dockerfile`, `Containerfile` | Python runtime/test image recipes; inspect actual build selection for your runtime |
| `docker-compose.acceptance.yml` | Isolated acceptance/recovery topology used by launcher actions |
| `docker-compose.dlq-acceptance.yml` | Disposable live DLQ acceptance fixtures/services |
| `docker-compose.observability.yml`, `prometheus.yml` | Observability configuration; not automatically enabled in every run |
| `docker-compose.ha.yml`, `helm/`, `argocd/`, `environments/` | Additional deployment templates; their presence does not establish production HA or supported upgrade paths |
| `hubble/` | Customized graph administration image/assets |
| `nginx/` | Proxy configurations for selected topologies |

The default profile uses named volumes and binds published ports to loopback. API is normally 8000, MCP 8001, web 8080, Hubble 8088. Optional profiles include `neo4j`, `test`, `tools`, `restore-test`, `observability` and the local model profile defined by the Compose file. Confirm exact names in the file before enabling them.

## Configuration and Secrets

On first `up`, the helper generates private `deploy/.env` values. Compose passes configured secrets through process environments; the example directory is not an automatic secret mount. Never publish expanded Compose configuration if it contains resolved credentials.

The runtime image installs locked core/file-parsing dependencies and copies application/config/demo/schema/script assets. A host editable install is not identical to that image. Optional neural/report/enterprise profiles require separate dependency and license review. Review Dockerfile and Containerfile differences rather than assuming equivalent behavior from filenames.

## Operational Safety

`down` retains volumes. `rebuild` is not a migration. `demo-data` writes synthetic graph content. `hubble-local-admin` deliberately changes a local graph account to demo credentials and must not be used as a production hardening operation.

`backup` pauses the worker only; quiesce other writers separately. `backup-bundle` stops selected application writers but cannot control every external writer. Restore into an isolated empty target and verify actual contents. See the [full recovery procedure](../docs/operations-runbook.md#backup-and-restore).

For any new profile, test fresh installation, service identity, secrets, persistence, authorized/denied requests, restart, worker replay, backup/restore, upgrade and rollback. Keep profile-specific evidence and make unqualified templates explicit in release notes.
