# Configuration Reference

Run commands from the repository root unless a component README says otherwise. Configuration is distributed across several loaders; there is no single universal precedence rule. This guide covers the active entry points. The source loaders remain authoritative for exact validation and defaults.

## Runtime Variables

| Variable | Consumer | Behavior and caution |
|---|---|---|
| `EOIP_API_TOKEN` | API and MCP via `eoip.runtime.api_token` | Required, at least 32 characters; inject from the secret store, never commit it; startup refuses a missing, short or revoked value. Registered as the bootstrap superadmin unless `EOIP_BOOTSTRAP_SUPERADMIN=false` (then `admin`+`system`) |
| `EOIP_ASG_FILE` | API ASG/RBAC loader (`apps/api/asg.py`) | Optional path to the principal file (`sha256:<hex> \| roles \| tenant \| user`, see `Logins_credentials.keys.example`). No repository default. Startup fails if the file is missing, group/world accessible, malformed, or holds plaintext tokens |
| `EOIP_REVOKED_TOKEN_SHA256_FILE` | API ASG loader and `api_token` | Optional newline list of sha256 digests of revoked tokens; any match refuses startup |
| `EOIP_ASG_ALLOW_PLAINTEXT` | API ASG loader | `true` accepts plaintext ASG entries **only** together with `EOIP_ENV=dev`; never in shared environments |
| `EOIP_DATA_DIR` | API/worker/runtime services | File-backed state root; defaults to `/data`; set an explicit writable path on a host |
| `EOIP_CONFIG_DIR` | Graph loader and selected services | Graph loader defaults to `config`; not every module necessarily honors this override |
| `EOIP_GRAPH_CONFIG` | Graph backend loader | Overrides graph configuration file path |
| `EOIP_GRAPH_BACKEND` | Graph backend loader | Selects a configured connection key or backend type, ahead of YAML `primary` |
| `EOIP_GRAPH_URL` | Graph backend loader | Nonempty generic override ahead of backend-specific URL |
| `EOIP_GRAPH_DATABASE`, `EOIP_GRAPH_GRAPH` | Graph backend loader | Logical graph/database override; database is considered first |
| `EOIP_GRAPH_USER`, `EOIP_GRAPH_PASSWORD` | Graph backend loader | Generic credential overrides; do not log resolved configuration |
| `EOIP_HUGEGRAPH_URL/GRAPH/USER/PASSWORD` | HugeGraph configuration | Backend-specific/legacy fallback; Compose maps `HUGEGRAPH_PASSWORD` into the application environment |
| `EOIP_LOAD_DEMO` | Worker startup | Defaults to `true` in worker code; local launchers also set it; set `false` for a non-demo deployment |
| `EOIP_API_URL` | MCP and some scripts | API URL; MCP default uses container DNS `http://eoip-api:8000`; use a reachable URL outside Compose |
| `EOIP_CORS_ORIGINS` | API query-app composition | Comma-separated explicit HTTP(S) origins without paths, credentials or wildcards |
| `EOIP_ENV`, `APP_ENV` | API CORS configuration; `backend/server.py` | `production` disables the development origin fallback; `EOIP_ENV` is considered first. `dev` lets `backend/server.py` generate an ephemeral token (`<data dir>/dev-token`, mode 0600) and enables plaintext ASG entries when `EOIP_ASG_ALLOW_PLAINTEXT=true` |
| `EOIP_DEV_API_URL` | `apps/web/vite.config.js` | Enables development proxies for `/api`, `/health`, `/metrics`; not the other frontend's setting |
| `REACT_APP_BACKEND_URL` | `frontend/src/lib/api.ts` | Alternate frontend API origin; build-time public value, never a secret; see frontend guide |
| `EOIP_LEASE_PATH`, `EOIP_LEASE_TTL_SECONDS` | Worker | Optional filesystem advisory leader lease; not proof of distributed failover safety |
| `EOIP_CONTAINER_RUNTIME`, `EOIP_COMPOSE_COMMAND` | Container helpers | Runtime/Compose discovery preferences; installed tooling and compatible behavior still required |

Graph selection is implemented in [backends.py](../packages/eoip/graph/backends.py): explicit `EOIP_GRAPH_BACKEND`, then YAML `primary`, then the applicable fallback. Nonempty generic connection environment values override backend-specific values and YAML fields. The checked-in [graph configuration](../config/graph-store.yaml) selects HugeGraph. Merely switching a variable neither migrates data nor starts the selected database.

REVA introduces a separate `REVA_` settings model, optional API mount and persistence paths. `REVA_ENABLED` defaults false; its source default key is not suitable for production, and the module CLI currently selects a home-directory database instead of `REVA_STORE_URL`. See the [REVA configuration and integration limits](../reva/README.md) before enabling it. Setting the enable flag is not sufficient to initialize or qualify the service.

## Configuration Files

| Location | Ownership |
|---|---|
| `config/graph-store.yaml` | Graph connection definitions and default selection |
| `config/ontology/` | Ontology-related configuration; runtime manifest and validators still enforce mutation rules |
| `config/mappings/` | Source-to-canonical mapping definitions |
| `config/query-policies/` | Query/traversal policy profiles |
| `config/agents/` | Agent configuration; registry composition may use explicit loader paths |
| `config/memory-policy.yaml` | Agent-memory policy |
| `config/architecture/`, `domain-packs/`, `benchmarks/`, `verification/` | Domain-specific configuration; inspect the consuming loader before editing |
| `config/systems-registry.json` | System registry configuration; distinguish configuration from persisted source instances |
| `deploy/.env` | Ignored local Compose interpolation values created by the launcher; not automatically read by host Uvicorn |

Do not assume editing any YAML file causes live reload. Identify which process loads it, at what time, and whether the affected service must restart. Record a config/schema version and a rollback plan for consequential changes.

## Secrets and Trust

The local helper generates credentials only when initializing `deploy/.env` on `up`. Changing that file does not itself migrate database users/passwords or rotate already-issued principal tokens. Coordinate credential rotation with the owning identity/database service and all consumers. Never run `hubble-local-admin` as a production rotation procedure: it deliberately sets a demo account.

Outside production, the API's current default CORS list includes localhost/127.0.0.1 on ports 3000, 8080 and 5173 when no explicit list is configured. Confirm the actual origin and policy rather than relying on a permissive browser setup. CORS is not authentication or tenant authorization.

Connector credentials are injected through the specific connector/worker configuration. A `secret_refs` field is a reference, not a universal implemented vault. The [secret examples](../secrets.example/README.md) are not automatically mounted as Compose secrets. Browser build variables are public and must never contain server credentials.

External MCP uses `EOIP_MCP_ALLOWED_HOSTS`, `EOIP_MCP_READ_ONLY_TOOLS` and `EOIP_MCP_STDIO_SERVERS`. See the exact trusted configuration shape in [API reference](api-reference.md#external-mcp-configuration). Do not allow API callers to choose arbitrary stdio commands or process environments.

## Safe Change Procedure

1. Identify the loader, runtime profile and owner; capture only a redacted current configuration.
2. Validate the new shape and test invalid/missing values in an isolated environment.
3. Confirm graph backend, tenant scope, egress policy, storage path and secret references.
4. Apply through the supported deployment method; restart only affected processes when required.
5. Verify authenticated behavior and negative authorization cases, not only health endpoints.
6. Record the change and observe worker/queue state. Restore prior configuration only when its data/schema compatibility is established.
