# Local Runtime and Gateway

## Three Explicit Runtime Stages

| Stage | What can run | What it does not prove |
|---|---|---|
| R0: current baseline | Existing API/worker/MCP/graph/web through current launchers | No independent portal repositories or shared browser session |
| R1: extracted UI pilot | Query/Explorer builds against the legacy API, using explicit local bootstrap authentication | Not a SaaS identity architecture; repeated token handling is not SSO |
| R2: suite runtime | Independent app artifacts, reviewed session boundary, qualified API/worker/package combination | Only the profiles and journeys actually verified |

Do not start empty pilot repositories and report success. First materialize their implementation and build contracts. Local frontend previews cannot substitute for backend, persistence or tenant tests.

## Run Today's Baseline

From `F:\code\EIP\EIOP`, after reviewing [current getting started](../../../docs/getting-started.md) and selecting the intended data/profile:

```powershell
.\scripts\container.ps1 detect
.\scripts\container.ps1 up
```

These are existing commands, not new suite commands. They can build containers, create local configuration and persistent volumes, and load demo content by default. Use disposable development state; explicitly disable `EOIP_LOAD_DEMO` for a non-demo profile. Do not run against production databases. Inspect the launcher's actual supported commands before shutdown; never use volume-deleting cleanup as a routine stop.

Default host ports are web 8080, API 8000, MCP 8001 and loopback Hubble 8088. Read effective settings and existing port use before launching another stack. A separate worker cannot share an API's in-memory graph. Use the same qualified persistent backend and configured data store for integrated ingestion.

## Port and Process Plan

| Component | Proposed local address | Notes |
|---|---|---|
| Legacy web | `http://127.0.0.1:8080` | Remains available during parity checks |
| Core API | `http://127.0.0.1:8000` | Legacy or extracted runtime, never both on the same port |
| MCP | `http://127.0.0.1:8001/mcp` | Preserve existing client compatibility |
| Customer suite gateway | `http://127.0.0.1:8081` | R1 local-only prototype; deployed profiles require HTTPS/session controls |
| Restricted operator gateway | separate reserved loopback port 8082 | Hosted operator origin/credentials/network separate from customer gateway |
| Portal dev servers | 5100-5117 | As assigned in the catalog; start only the selected slice |
| Session adapter | internal-only proposed port 8010 | New work; provider and upstream authorization integration must be implemented |
| Graph/state services | container/internal addresses | Do not expose database credentials to portals |

No server auto-falls back to another port. If occupied, change the selected profile's entire routing/port map and revalidate it. Do not kill unrelated processes.

## Portal Base Paths

Each portal builds for its assigned root, for example `/query/`. Vite's build `base` controls asset URL rewriting; configure the router's basename separately where a router is used. Test both. [Vite public base path](https://vite.dev/guide/build.html#public-base-path).

The extracted Query portal's Vite configuration must set `base: '/query/'`, bind development traffic to loopback, reserve port 5104, fail on conflicts and proxy `/api` to the explicitly selected local API only in R1. Do not copy the alternate frontend's unrestricted host setting or fixed HMR port without review. In gateway development mode, preserve app-specific websocket routing and verify live updates through port 8081, not only the direct Vite port.

## R1 Gateway Routing Template

The following Nginx fragment illustrates **local-only Docker Desktop** routing to host processes. It belongs in Nginx's `http` context, such as an appropriate `conf.d` include; it is not a complete standalone `nginx.conf`, production configuration or implemented gateway artifact. Other runtimes must supply a tested host-reachability mapping rather than assuming `host.docker.internal` exists. Run gateway containers on an explicitly selected network; pin the actual image by digest in the suite lock. Probe host-service reachability from the actual container first, including firewall/listener behavior; do not broadly expose dev servers to fix a routing problem. [Docker Desktop networking](https://docs.docker.com/desktop/features/networking/).

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}
server {
    listen 8081;
    server_name localhost 127.0.0.1;

    location = / { return 302 /suite/; }
    location = /query { return 308 /query/; }
    location = /explore { return 308 /explore/; }
    location = /suite { return 308 /suite/; }

    location /query/ {
        proxy_pass http://host.docker.internal:5104;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
    }
    location /explore/ {
        proxy_pass http://host.docker.internal:5105;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
    }
    location /suite/ {
        proxy_pass http://host.docker.internal:5100;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
    }
    location /api/ {
        proxy_pass http://host.docker.internal:8000;
        proxy_set_header Host $host;
    }
    location / { return 404; }
}
```

The no-trailing-URI `proxy_pass` preserves `/query/...` and `/api/...`; websocket proxying requires explicit upgrade handling. [Nginx proxy behavior](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass), [websocket proxying](https://nginx.org/en/docs/http/websocket.html). Validate the fragment using its pinned image and `nginx -t` before starting. R1 forwards the client's API authorization; it does not inject a shared privileged token or create a session. Bind the container port to `127.0.0.1:8081:8081`. Do not route Database or Fleet through this customer listener.

For production static apps, serve only the selected artifact directory, retain immutable hashed assets, return 404 for missing assets, and use an app-specific SPA fallback for valid deep routes. Do not return Suite Home's HTML for every unknown `/api`, asset or disabled-app request. CSP, cache policy, content type, security headers, TLS and proxy trust must be reviewed with the actual deployment.

## R2 Session and Deployment Work

The session adapter must integrate a selected reviewed identity provider, retain upstream credentials server-side, validate requested tenant/workspace against grants, enforce CSRF/origin protections and implement login/logout/expiry/revocation. Never derive privilege from client headers or navigation state. Same-origin app paths are not isolation boundaries. Do not call this complete because two tabs share a browser token.

`eoip-suite` will own Compose/profile orchestration; `eoip-suite-gateway` owns routing/session application code and its artifact. Per-app repositories own their own production builds. Release Compose references published digests; local source-build overrides are explicitly non-release profiles. The parent workspace is not a giant build context.

## Startup and Shutdown Contract to Implement

1. Preflight required repositories/artifacts, available ports, disk capacity, secrets and selected profile.
2. Start persistent infrastructure and verify actual readiness, not only container existence.
3. Apply compatible migrations once through the migration owner; do not start competing migrators.
4. Start API, qualified worker and MCP; probe an authenticated read and denied request.
5. Start selected portal artifacts/dev servers and the gateway; verify base paths and websocket behavior.
6. On startup failure, report failed dependency and retain diagnostics. Stop only resources created by this invocation when safe.
7. On shutdown, stop accepting work, drain/cancel according to job contracts, stop services and retain data volumes.

Do not add a `suite up` command to documentation as already available. Implement and test it under the backlog before advertising it. Destructive reset, restore and database migration commands must be separate explicit operations with target checks.
