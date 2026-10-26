# Chapter 0 — Overview and Quickstart

> **Audience:** first-time users and administrators with no prior EOIP knowledge.
> **Status:** every command, endpoint, route and variable below was read from the repository source (`README.md`, `scripts/container.ps1`, `scripts/container.sh`, `deploy/.env.example`, `deploy/docker-compose.yml`, `apps/api/`, `apps/web/src/`). Behavior described here was **verified statically against the code**, not executed against a live deployment; where a step's runtime result could not be exercised, it is marked *not runtime-verified*.

This chapter gets you from a fresh checkout of the repository to a running local EOIP environment you can explore safely. You will learn what the platform is, which of the two local deployment profiles to pick, how to run the container helper end to end (detect → up → backup → restore-test → down), how `deploy/.env` and the `EOIP_API_TOKEN` credential work, how to sign in to the web UI and reach the `/app`, `/demo`, `/admin` and `/studio` routes, how to load the synthetic demo dataset, how to verify the deployment with `/health/ready`, `/metrics` and `/docs`, and how to recover from the most common first-run failures.

**In this chapter**

1. [What the platform is](#1-what-the-platform-is)
2. [Choosing a deployment profile](#2-choosing-a-deployment-profile)
3. [Container quickstart: detect, up, backup, restore-test, down](#3-container-quickstart-detect-up-backup-restore-test-down)
4. [How deploy/.env is generated and how EOIP_API_TOKEN works](#4-how-deployenv-is-generated-and-how-eoip_api_token-works)
5. [First connection: the web UI routes](#5-first-connection-the-web-ui-routes)
6. [Loading the demo dataset](#6-loading-the-demo-dataset)
7. [Verifying the deployment: /health/ready, /metrics, /docs](#7-verifying-the-deployment-healthready-metrics-docs)
8. [Common first-run errors and fixes](#8-common-first-run-errors-and-fixes)

---

## 1. What the platform is

**What it does.** EOIP (Enterprise Ontology & Intelligence Platform), also called KnowGridFlow (KGF) in parts of this repository, is a **local-first knowledge graph application**. Per `README.md`, it provides "authenticated graph/query APIs, ingestion connectors and jobs, provenance and validation services, a React web app, an MCP server, a worker, a VS Code extension, and local container deployment assets." `EOIP-master-requirements.md` describes the product intent as "a governed knowledge and intelligence platform" spanning "acquisition, graph core, query, ontology, local AI, agents, reports, governance, operations, configuration and developer channels."

The runtime pieces you will actually meet in this chapter are:

| Component | Source path | Role |
|---|---|---|
| API | `apps/api/` | FastAPI application factory, authentication, middleware, HTTP routes |
| Worker | `apps/worker/` | Filesystem-backed job worker and ingestion handlers |
| MCP server | `apps/mcp/` | Read-only MCP facade over the authenticated API |
| Web UI | `apps/web/` | React/Vite explorer and administration UI |
| Graph service | `deploy/docker-compose.yml` | HugeGraph (`hugegraph/hugegraph:1.7.0`) in the default container profile |
| Hubble | `deploy/docker-compose.yml` | HugeGraph's graph-inspection UI on port 8088 |

**Honest status note (from `README.md`):** "A module, test, backlog checkbox, or demo result is not proof that a feature is production-qualified." The master requirements file states it is a "consolidated audit specification; no feature is certified by this document." Treat what you start here as a working local environment, not a qualified production release.

---

## 2. Choosing a deployment profile

**What it does.** The repository supports two local profiles. Pick one before continuing.

### Profile A — Integrated containers (recommended for a first run)

- One command builds and starts HugeGraph, schema/Hubble initialization, the API, worker, MCP server, web UI, and Hubble (`README.md`, "Fastest Local Run").
- Data is durable: it lives in named volumes (`graph-data`, `application-data`, `model-data`, `metrics-data`, `hubble-data`, `hubble-uploads` — see the `volumes:` block at the bottom of `deploy/docker-compose.yml`).
- Requires an installed, running OCI runtime with Compose: Docker, Podman, nerdctl, or Finch.

### Profile B — Host-only development with the memory graph

- No containers. You run the FastAPI factory (`apps.api.main:create_app`) directly under Python 3.11+ and the Vite dev server under Node.js 22.
- `EOIP_GRAPH_BACKEND=memory` selects an **in-process, non-durable graph**: per `README.md`, "The `memory` graph backend is process-local and does not survive a restart."
- Intended for code development only; do not evaluate persistence, backup, or multi-service behavior here.

| | Profile A (containers) | Profile B (host dev) |
|---|---|---|
| Command | `scripts/container.ps1 up` / `scripts/container.sh up` | `python -m uvicorn apps.api.main:create_app --factory ...` |
| Graph | HugeGraph, durable | `memory` backend, lost on exit |
| Web UI | <http://localhost:8080/app> | Vite dev URL from the terminal |
| Use for | Realistic first look, demo data, backup drills | Editing API/UI code |

---

## 3. Container quickstart: detect, up, backup, restore-test, down

**What it does.** `scripts/container.ps1` (Windows/PowerShell) and `scripts/container.sh` (Linux/macOS/Git Bash) are a single entry point that auto-detects your container runtime and delegates to Compose. Valid actions are declared in the script's parameter validation (`container.ps1` lines 20–25): `up`, `rebuild`, `hubble-local-admin`, `demo-data`, `test`, `status`, `logs`, `down`, `backup`, `backup-bundle`, `extension`, `restore-test`, `acceptance`, `recovery-acceptance`, `dlq-acceptance`, `detect`, `info`.

**How to access.** A terminal at the repository root (`f:/code/EIP/EIOP` on this machine).

### Step by step

1. **Detect the runtime.** PowerShell:

   ```powershell
   .\scripts\container.ps1 detect
   ```

   Bash:

   ```bash
   ./scripts/container.sh detect
   ```

   Expected output (from `container.ps1` lines 151–174):

   ```
   EOIP Container Runtime: docker (Docker version ...)
     Compose: docker compose (...)
   Runtime:          docker
   CLI:              docker
   ...
   All detected runtimes:
     docker: available (active)
     podman: not found
     ...
   ```

   The script probes candidates in order `docker`, `podman`, `nerdctl`, `finch`, `lima-nerdctl` (`container.ps1` lines 32–38). Override with `$env:EOIP_CONTAINER_RUNTIME = 'podman'` or `$env:EOIP_COMPOSE_COMMAND = 'podman-compose'` (documented in the script header, lines 9–11).

2. **Start the platform.** PowerShell:

   ```powershell
   .\scripts\container.ps1 up
   ```

   Bash:

   ```bash
   ./scripts/container.sh up
   ```

   This executes `compose up --build -d --wait --wait-timeout 420` (`container.ps1` line 254), so it waits up to 7 minutes for health. On the **first** `up` only, the script creates `deploy/.env` (see section 4). Expected final line (line 255):

   ```
   EOIP (docker): http://localhost:8080/app | API: http://localhost:8000/docs | MCP: http://localhost:8001/mcp | Hubble: http://localhost:8088
   ```

3. **Confirm containers are healthy.**

   ```powershell
   .\scripts\container.ps1 status
   ```

   Runs `compose ps` (line 294). Expect services including `hugegraph-server`, `schema-init`, `hubble`, `hubble-init`, `eoip-api`, `eoip-worker`, `eoip-mcp`, `eoip-web` (service names from `deploy/docker-compose.yml`).

4. **Take a backup.**

   ```powershell
   .\scripts\container.ps1 backup
   ```

   The script stops `eoip-worker`, runs `python -m scripts.backup` inside the `eoip-api` container, then restarts the worker (lines 297–301). `scripts/backup.py` exists in the repository. *The exact console output of a backup run was not runtime-verified here; check the printed backup location and keep it.*

5. **Verify the backup is restorable.**

   ```powershell
   .\scripts\container.ps1 restore-test
   ```

   This runs the `restore-check` service under the `restore-test` Compose profile, then force-removes the temporary `restore-graph` container (lines 378–385). A successful run proves the snapshot can actually be mounted and read — a completed backup label alone is not proof of recoverability (a point also made in the help-center troubleshooting page generated by `scripts/build_self_help.py`).

6. **Shut down (keeping your data).**

   ```powershell
   .\scripts\container.ps1 down
   ```

   Runs plain `compose down` (line 296), which **preserves named volumes**. Per `README.md`: "avoid `down --volumes` unless you intentionally want to delete local graph and application data."

**Errors and recovery.**

- `No OCI container runtime found on this system.` (thrown at `container.ps1` lines 139–145) — install Docker/Podman/nerdctl/Finch, or set `EOIP_CONTAINER_RUNTIME` to the one you have.
- `Compose tool not found for runtime '...'` (line 178) — install the compose plugin for your runtime.
- `Run scripts/container.ps1 up once to initialize the local configuration.` (line 193) — you ran another action before the first `up`; run `up` once to create `deploy/.env`.

---

## 4. How deploy/.env is generated and how EOIP_API_TOKEN works

**What it does.** `deploy/.env` holds the local credentials the Compose deployment and the web sign-in depend on. It is created **once**, on the first `up`, and is ignored by Git (`README.md`: "that file is ignored by Git").

**How to access.** File at `deploy/.env`; template/documentation at `deploy/.env.example`.

### Step by step (what the script does for you)

1. Run `.\scripts\container.ps1 up` (or `./scripts/container.sh up`) with no existing `deploy/.env`.
2. The script generates (`container.ps1` lines 191–204):
   - `EOIP_API_TOKEN` — 32 random bytes as 64 hex characters (256-bit), via `New-RandomHex -ByteCount 32` (PowerShell) or `openssl rand -hex 32` (Bash).
   - `HUGEGRAPH_PASSWORD` — 24 random bytes as 48 hex chars, sized for Hubble's `VARCHAR(48)` column (comment "FT-X04" at line 196).
   - `EOIP_ADMIN_USERNAME` / `EOIP_ADMIN_PASSWORD` — the first admin account. The username comes from `$env:EOIP_ADMIN_USERNAME` if you set it, otherwise your current login name; the password is random. Per `.env.example`: "there is no default account. The first administrator is provisioned from these two values when the API starts ('eoip-admin from-env'); the password is hashed with argon2id."
   - `EOIP_API_TOKEN_ROLES=analyst` and `EOIP_API_TOKEN_PRINCIPAL=svc-mcp`.
   - `EOIP_LOAD_DEMO=true`.
3. The script prints: `Created deploy/.env. Sign in as '<user>' with EOIP_ADMIN_PASSWORD from deploy/.env.` (Bash additionally sets file mode 600 via `umask 077`, `container.sh` lines 120–122.)
4. **Read the token locally when you need it** (never paste it into tickets, chat, or screenshots — `README.md`: "Do not print or commit the token"):

   ```powershell
   Get-Content deploy\.env | Select-String '^EOIP_API_TOKEN='
   ```

   ```bash
   grep '^EOIP_API_TOKEN=' deploy/.env
   ```

**Response/result.** `deploy/.env` exists with the seven values above. `deploy/.env.example` documents additional optional keys you can add: `EOIP_SESSION_SECRET` (required only with several API replicas), connector credentials (`EOIP_CONFLUENCE_*`, `EOIP_SERVICENOW_*`), and port overrides `EOIP_WEB_PORT=8080`, `EOIP_API_PORT=8000`, `EOIP_MCP_PORT=8001`, `EOIP_HUBBLE_PORT=8088`.

**What EOIP_API_TOKEN actually is** (from `deploy/.env.example` lines 8–12): "Service token used by the MCP facade. It is mapped to principal EOIP_API_TOKEN_PRINCIPAL with exactly EOIP_API_TOKEN_ROLES; without roles it grants nothing." So the token alone is inert — its powers come from the roles list. The API middleware (`apps/api/main.py` lines 511–527) returns `401 {"detail": "A valid Bearer token is required"}` for any request without a valid `Authorization: Bearer` header, except an explicit allowlist that includes `/health/live`, `/health/ready`, `/metrics`, `/docs`, `/openapi.json`, and the `/api/v1/auth/*` login paths.

**Errors and recovery.**

- Lost `deploy/.env`: delete is destructive — credentials cannot be recovered; delete the file and named volumes only if you accept data loss, then rerun `up` to regenerate. Prefer asking whoever ran `up` for the file first.
- Token rejected (`401`): you are sending the wrong value or no `Bearer` prefix; re-read the exact line from `deploy/.env`.
- Rotating the graph admin password: use `.\scripts\container.ps1 hubble-local-admin` (lines 262–282), which rotates `HUGEGRAPH_PASSWORD` to a fresh random value and saves it back to `deploy/.env` without printing it.

---

## 5. First connection: the web UI routes

**What it does.** The container profile serves the built `apps/web` React app at <http://localhost:8080>. Its workspace navigation is defined in `apps/web/src/app/navigation.ts` with these real routes and labels:

| Path | Label in UI | Purpose |
|---|---|---|
| `/app` | Knowledge explorer | Search, inspect entities, relationship map, impact tracing |
| `/cognitive` | Cognitive Engineering | Cognitive workbench |
| `/dashboards` | Cognitive Dashboards | Metrics panels (polls `/metrics` and `/api/v1/admin/stats`) |
| `/studio` | Ontology studio | Schema and query tools |
| `/admin` | Administration | Sources, ingestion, validation, audit, DLQ |
| `/demo` | Guided demo | Scenario walkthroughs (backed by `GET /api/v1/demo/scenarios`) |
| `/settings` | Appearance | Theme settings |

### Step by step

1. Start the stack (section 3) and wait for the `up` success line.
2. Open <http://localhost:8080/app> in a browser. You land on the **connection screen** (`apps/web/src/app/shell/Connection.jsx`), which shows a local service readiness indicator and an **Access token** field with a show/hide control.
3. Paste the `EOIP_API_TOKEN` value from `deploy/.env` and choose **Connect**.
4. On success you enter the workspace shell (`WorkspaceShell.jsx`) with the navigation listed above. Click a nav item or go directly to <http://localhost:8080/admin>, <http://localhost:8080/studio>, or <http://localhost:8080/demo>.

**Response/result.** The workspace loads with the "Knowledge explorer" view at `/app` (the root path `/` maps to `/app` per `destinationFor` in `navigation.ts`). The token is held in browser memory only until you choose **Disconnect** or reload (help-center "Connect and first session" page).

**Errors and recovery.**

- *Service status unavailable on the connection screen* — expected when the API is unhealthy or the web proxy can't reach it. Check `http://localhost:8000/health/ready` (section 7) and `.\scripts\container.ps1 status` before entering a token.
- *Connect fails even though health is ready* — Connect calls administrative summary endpoints (`/api/v1/admin/stats`, `/api/v1/admin/system`, `/api/v1/admin/jobs`; see `apps/web/src/App.jsx` line 964), so a token whose roles don't cover those routes can be denied. Verify you used `EOIP_API_TOKEN` (roles `analyst`) or sign in with the admin credentials; read the error toast and record its correlation ID, never the token.
- *A visible menu item doesn't work* — per the help center, "A visible menu item is not proof that its backing service is configured." Roles and backend configuration can restrict actions.

---

## 6. Loading the demo dataset

**What it does.** The demo corpus is **synthetic** Jira, Git, code, pipeline and documentation evidence (`README.md`: "Demo datasets are synthetic… they are not customer data"). Source data lives under `demo/demodata/` (e.g. `demo/demodata/enterprise/` contains a `scenario-pack.json`, `source-fixtures/gitlab.json`, and a `services/checkout` example service). Two mechanisms load it:

- **Automatic at worker start**: the Compose default sets `EOIP_LOAD_DEMO: ${EOIP_LOAD_DEMO:-true}` (`deploy/docker-compose.yml` line 26) and the worker honors it (`apps/worker/main.py` line 219). Because the generated `deploy/.env` contains `EOIP_LOAD_DEMO=true`, the demo loads on first `up` with no action from you.
- **On demand**: the Administration UI button **"Load / replay demo"** and the Demo dataset card's **"Load dataset"** button both `POST /api/v1/admin/demo` (`apps/web/src/App.jsx` lines 713, 722), or you can run the `demo-data` container action.

**How to access.** UI: <http://localhost:8080/admin> → Demo dataset card → **Load dataset**. API: `POST /api/v1/admin/demo`. Container: `scripts/container.ps1 demo-data`.

### Step by step (API)

1. Export your token (PowerShell):

   ```powershell
   $token = (Select-String -Path deploy\.env -Pattern '^EOIP_API_TOKEN=(.+)$').Matches.Groups[1].Value
   ```

   Bash:

   ```bash
   token=$(grep '^EOIP_API_TOKEN=' deploy/.env | cut -d= -f2)
   ```

2. Queue the demo ingestion job:

   ```bash
   curl -i -X POST http://localhost:8000/api/v1/admin/demo \
     -H "Authorization: Bearer $token"
   ```

3. Alternatively, load the full demo corpus inside the API container (what `demo-data` does, `container.sh` lines 151–155):

   ```powershell
   .\scripts\container.ps1 demo-data
   ```

   which runs `compose exec -T eoip-api python -m scripts.load_demo_corpus`.

**Response/result.** `POST /api/v1/admin/demo` returns **HTTP 202** (`apps/api/main.py` line 1469: `@app.post("/api/v1/admin/demo", status_code=202)`) with a queued-job body — the endpoint submits a job of type `"DEMO"` with your tenant, correlation ID, and actor (lines 1474–1479). Key fields to note from the response: the job id and `correlation_id` (also in the `X-Correlation-ID` response header). Track progress in Administration → jobs, or inspect the graph in Hubble at <http://localhost:8088>. The `demo-data` action prints `Demo corpus loaded into the existing graph. Hubble: http://localhost:8088.`

**Errors and recovery.**

- `401 {"detail": "A valid Bearer token is required"}` — missing/expired `Authorization` header; fix step 1.
- Demo seems absent after `up`: check the worker loaded it — `.\scripts\container.ps1 logs` and search for the worker service; remember the demo load happens in the worker, and "A worker and API configured with separate memory stores cannot share graph state" (`README.md`) — relevant only in host dev, not containers.
- Non-demo deployment: explicitly set `EOIP_LOAD_DEMO=false` in `deploy/.env` before `up` (`README.md`: "explicitly disable `EOIP_LOAD_DEMO` for non-demo deployments").

---

## 7. Verifying the deployment: /health/ready, /metrics, /docs

**What it does.** Three unauthenticated endpoints confirm the API is alive and observable. All three are in the auth-bypass allowlist in `apps/api/main.py` lines 511–524, so no token is needed.

### Step by step

1. **Readiness** — `GET http://localhost:8000/health/ready`:

   ```bash
   curl -i http://localhost:8000/health/ready
   ```

   Expected (`apps/api/app.py` lines 341–346): `HTTP/1.1 200 OK` with body `{"status":"ready"}`. If the graph store health check fails, the API returns **503** with `{"status":"not_ready"}`. Sibling endpoint `/health/live` always returns `{"status":"ok"}` (lines 337–339) — liveness is not readiness.

2. **Metrics** — `GET http://localhost:8000/metrics`:

   ```bash
   curl -s http://localhost:8000/metrics | head -20
   ```

   Expected: Prometheus text exposition (`apps/api/extended.py` lines 1407–1410, `response_class=PlainTextResponse`), rendering request counters/histograms registered by the API middleware. In the default deployment, Prometheus itself is also available at <http://localhost:9090> (`deploy/docker-compose.yml`, service `prometheus`, port mapping `127.0.0.1:9090:9090`).

3. **API documentation** — `GET http://localhost:8000/docs`:

   Open <http://localhost:8000/docs> in a browser. This is FastAPI's Swagger UI over `/openapi.json`. Use it to read exact request/response contracts before scripting. The raw schema is at <http://localhost:8000/openapi.json>. Do not use Swagger's "Authorize" to paste tokens on a shared machine.

4. **Confirm the actual graph backend** (optional, needs token):

   ```bash
   curl -s http://localhost:8000/api/v1/graph/backend -H "Authorization: Bearer $token"
   ```

   Returns `configured_backend`, `active_backend`, sanitized `connection` details (passwords/tokens stripped — `apps/api/app.py` lines 348–368), `ping`, and `capabilities`. Use this to prove you are on HugeGraph, not the memory backend — the help center notes a case where a service panel misleadingly said "HugeGraph READY" in a memory profile; verify here instead.

**Response/result summary.** 200 + `{"status":"ready"}` means the graph store passed its health check; `/metrics` returns plain-text Prometheus lines; `/docs` renders Swagger UI.

**Errors and recovery.**

- `curl: (7) Failed to connect ... port 8000` — API container not up or port overridden; check `.\scripts\container.ps1 status` and `EOIP_API_PORT` in `deploy/.env`.
- 503 `not_ready` — the graph backend is still starting or misconfigured; inspect logs: `.\scripts\container.ps1 logs` (runs `compose logs --tail 100`).
- Empty `/metrics` — the middleware only records what has served traffic; make a few API calls, then re-fetch.

---

## 8. Common first-run errors and fixes

| Symptom | Meaning | Fix |
|---|---|---|
| `No OCI container runtime found on this system.` | Script probed docker/podman/nerdctl/finch and none answered (`container.ps1` lines 139–145) | Install one runtime, start it, rerun `detect`; or set `$env:EOIP_CONTAINER_RUNTIME` |
| `Compose tool not found for runtime '...'` | CLI exists but no compose plugin (line 178) | Install `docker compose` plugin / `podman-compose`; or set `$env:EOIP_COMPOSE_COMMAND` |
| `Run scripts/container.ps1 up once to initialize the local configuration.` | You ran `status`/`backup`/etc. before any `up`, so `deploy/.env` doesn't exist (line 193) | Run `.\scripts\container.ps1 up` once |
| Port already in use on 8080/8000/8001/8088 | Another process holds a published port (`deploy/docker-compose.yml` binds `127.0.0.1:${EOIP_*_PORT}`) | Stop the other process, or add `EOIP_WEB_PORT=…` etc. to `deploy/.env` (documented in `.env.example` lines 28–31), then rerun `up` |
| Web UI loads but connection screen says service unavailable | Web container is up but the API isn't ready, or the proxy can't reach it | `curl http://localhost:8000/health/ready`; then `.\scripts\container.ps1 status` and `logs` |
| `401 {"detail": "A valid Bearer token is required"}` | Missing or invalid `Authorization: Bearer` header (`apps/api/main.py` lines 525–527) | Re-read `EOIP_API_TOKEN` from `deploy/.env`; ensure the `Bearer ` prefix; never URL-encode or truncate it |
| Token valid but Connect still fails | Connect calls `/api/v1/admin/stats`, `/api/v1/admin/system`, `/api/v1/admin/jobs`; roles may not cover them | Use the generated token (role `analyst`) or the admin account; capture the toast's correlation ID |
| `/health/ready` returns 503 `not_ready` | Graph store health check failing (`apps/api/app.py` lines 341–346) | Check HugeGraph startup in logs; first boot can be slow — the `up` command waits up to 420 s |
| Graph empty after everything is "ready" | Demo load is a worker-side step gated by `EOIP_LOAD_DEMO` | See section 6; run `demo-data` or **Load dataset** in `/admin` |
| `down` deleted nothing but data is gone | You ran a manual `compose down --volumes` | Named volumes are deleted by that flag; `README.md` warns to avoid it. Restore from your `backup` snapshot (`restore-test` proved it mounts) |
| Host-dev API forgets all data on restart | Expected: `EOIP_GRAPH_BACKEND=memory` is process-local (`README.md` line 90) | Use the container profile for anything durable |

**If all else fails — support bundle contents** (from the help-center troubleshooting page): application version or git revision, deployment profile, UTC time, affected route, steps to reproduce, correlation/job ID, expected vs. observed behavior, and redacted logs. **Exclude** access tokens, raw source payloads, and private graph exports.

---

## Appendix: exact commands used in this chapter (copy-paste block)

PowerShell, from the repository root:

```powershell
.\scripts\container.ps1 detect
.\scripts\container.ps1 up
.\scripts\container.ps1 status
curl.exe http://localhost:8000/health/ready
.\scripts\container.ps1 backup
.\scripts\container.ps1 restore-test
.\scripts\container.ps1 demo-data
.\scripts\container.ps1 logs
.\scripts\container.ps1 down
```

Bash equivalent:

```bash
./scripts/container.sh detect
./scripts/container.sh up
./scripts/container.sh status
curl http://localhost:8000/health/ready
./scripts/container.sh backup
./scripts/container.sh restore-test
./scripts/container.sh demo-data
./scripts/container.sh logs
./scripts/container.sh down
```

*Verification honesty: all commands, outputs and routes above were transcribed from source files in this repository. The end-to-end container run, backup contents, and restore-test pass were not executed as part of producing this chapter; run them in your environment before relying on them operationally.*
