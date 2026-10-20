# Secret Examples

This directory contains placeholders and examples only. The default container
launcher creates the local ignored file `deploy/.env` and generates
`EOIP_API_TOKEN` and `HUGEGRAPH_PASSWORD` on first startup. The current Compose
configuration passes configured values through service environments; the
`secrets.example/` directory is **not automatically mounted as Docker Compose
secrets**.

## Configuration

For disposable local development, use the container helper:

```powershell
.\scripts\container.ps1 up
```

For host-only development, set a local token and select the in-memory backend:

```powershell
$env:EOIP_API_TOKEN = 'local-development-token-at-least-32-characters'
$env:EOIP_GRAPH_BACKEND = 'memory'
```

The API requires `EOIP_API_TOKEN` to be at least 32 characters (FT-F02). Live connector
credentials are read from their configured environment/secret source by the
worker; do not put raw credentials in source registry payloads, job payloads,
URLs, fixtures, or logs. A `secret_refs` field is a reference contract, not a
secret store by itself. Before adding a production credential path, verify the
provider adapter, access policy, secret injection, redaction, rotation, and
deployment configuration.

The `api-token.txt` file is a placeholder, not a usable credential. Never copy
real credentials into this directory or commit them to version control.

## Maintenance and Rotation

Changing a local environment file does not automatically rotate database accounts, existing principal credentials or every consumer process. Coordinate rotation with the owning provider/database and verify old-credential refusal as well as new-credential success. Do not use the demo `hubble-local-admin` action as a secure rotation procedure.

For injection precedence, startup behavior and incident-safe handling, see [Configuration Reference](../docs/configuration-reference.md) and [Operations](../docs/operations-runbook.md). Browser/Vite environment variables are public bundle inputs and must never receive server secrets. The documentation inventory intentionally excludes potential secret files rather than copying their values.
