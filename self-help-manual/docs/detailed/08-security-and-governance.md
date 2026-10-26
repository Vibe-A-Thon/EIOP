# Chapter 8 — Security and Governance

This chapter covers everything that controls **who can do what**, **which tenant's data is being touched**, and **what is allowed to leave the platform** in EOIP. It is written for administrators and end users with no prior knowledge of the system. Every endpoint, field name, and behavior below is quoted from the actual source code in `apps/api/` and `packages/eoip/`; where a feature is only partially built (a stub or placeholder), that is stated plainly.

**Index of sections**

1. [Token authentication — how `/api/v1/*` is protected](#81-token-authentication)
2. [User management — login, logout, whoami, SSO providers](#82-user-management-and-login)
3. [RBAC/ABAC — roles, permissions, policies, decisions](#83-rbac-and-abac)
4. [Tenancy — context, isolation, quotas, lifecycle, metering](#84-tenancy)
5. [Licensing — status, verify, module checks, metering](#85-licensing)
6. [Layered configuration — set, explain, bounds, rollback, export/import, flags](#86-layered-configuration)
7. [Egress gateway — endpoints, consent, policy, dry-run, kill switch, reports, plugins](#87-egress-gateway)
8. [Branding — theme, terminology, locales, legal content](#88-branding)
9. [Privacy — classify, DSAR, consents, retention, residency](#89-privacy)
10. [Compliance — packs, gap analysis, AI governance, changes, roles, exceptions](#810-compliance)
11. [Knowledge firewall — inspect endpoint](#811-knowledge-firewall)

All examples assume the API is at `http://localhost:8000`, demo tenant `t-001`, and a shell variable:

```bash
export TOKEN="<your bearer token>"
```

---

## 8.1 Token authentication

**What it does.** Every route under `/api/v1/*` (and everything else, except a small allow-list) requires an `Authorization: Bearer <token>` header. This is enforced by an HTTP middleware named `boundary` in `apps/api/main.py` (see `@app.middleware("http")` at `apps/api/main.py:431`). If no valid token is present, the request never reaches the route — it gets a `401`.

The only paths that do **not** require a token are (`apps/api/main.py:511-524`):

- `/health/live`, `/health/ready`, `/metrics`
- `/docs`, `/openapi.json`, `/docs/oauth2-redirect`
- `/ontology/docs`, `/api/v1/ontology/docs`
- `/api/reva/v1/health`
- `/api/v1/auth/login`, `/api/v1/auth/health`, `/api/v1/auth/providers`
- anything under `/api/v1/auth/sso/`
- the ingestion webhook path `/api/v1/sources/<id>/webhooks`

**The service token (`EOIP_API_TOKEN`).** Machine-to-machine access uses a token from the environment. Per `packages/eoip/authn/provision.py:70-86`:

- `EOIP_API_TOKEN` — the raw token. **Must be at least 32 characters** (`provision.py:74` raises `CredentialError` otherwise; also enforced at startup by `packages/eoip/runtime.py:34-41`, which additionally rejects a revoked token).
- `EOIP_API_TOKEN_ROLES` — comma-separated roles mapped to the token, e.g. `admin,operator`.
- `EOIP_API_TOKEN_PRINCIPAL` — optional principal name, default `svc-api-token`.
- `EOIP_API_TOKEN_TENANT` — optional tenant binding, default `default`.

Important honest caveat (from `packages/eoip/authn/provision.py:86` and `apps/api/asg.py:15`): if `EOIP_API_TOKEN` is set **without** `EOIP_API_TOKEN_ROLES`, the token is *not* mapped to any principal — there is no bootstrap or default admin. You must provision credentials first (see 8.2).

**Step by step — call a protected endpoint.**

```bash
curl -i http://localhost:8000/api/v1/auth/whoami \
  -H "Authorization: Bearer $TOKEN"
```

**Response/result.** A valid call returns the principal record (see 8.2). A missing/invalid token returns:

```json
{"detail": "A valid Bearer token is required"}
```

with HTTP `401` (`apps/api/main.py:527`).

**Role gate on top of the token.** Authenticated is not the same as authorized. The middleware classifies every mutating route (`POST/PUT/PATCH/DELETE`) and, for high-risk admin prefixes (`/api/v1/admin`, `/api/v1/sources`, `/api/v1/authz`, `/api/v1/security`, `/api/v1/tenancy`, egress admin routes, marketplace install, snapshots, destructive ontology gitops — see `apps/api/main.py:548-576`), requires one of the admin roles `admin`, `system`, or `superadmin` (`apps/api/route_policy.py:25`, `ADMIN_ROLES`). Otherwise: `403 {"detail": "Administrative role required"}`. Non-admin mutations that fail the route policy return `403 {"detail": "Role not permitted: <class> access required"}` (`apps/api/main.py:626`).

**Errors and recovery.**

| Symptom | Meaning | Fix |
|---|---|---|
| `401 "A valid Bearer token is required"` | no/expired/revoked token | log in again (8.2) or check the env token |
| `403 "Administrative role required"` | token works, role doesn't | assign an admin role to the user/token |
| `413 "Request body too large"` | body over 4,000,000 bytes (`main.py:542`) | split the request |
| `503 "Audit service unavailable; admin mutation was not executed"` | the audit preflight failed, so the admin write was **refused** | restore the audit sink, then retry |

Every response also carries `X-Correlation-ID` and, for audited operations, `X-Audit-ID` headers — quote these when reporting a problem.

---

## 8.2 User management and login

**What it does.** Local users authenticate with username/password against an argon2id credential store and receive a session bearer token. SSO (OIDC/SAML) is a **placeholder only** — see below.

### Login

**Access:** `POST /api/v1/auth/login` (`apps/api/extended.py:1040`). This route is token-free by design.

```bash
curl -s http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "correct-horse-battery-staple"}'
```

**Response:** `{"token": "<session token>"}` (`extended.py:1051`). Use it as `Authorization: Bearer <token>`. A wrong username or password returns `401 {"detail": "invalid credentials"}` — deliberately indistinguishable.

### Whoami / logout / health / providers

- `GET /api/v1/auth/whoami` (`apps/api/main.py:745`) — returns `{id, username, roles, tenant_id, provider, is_superadmin, is_admin}` for the current token; `401` without one.
- `POST /api/v1/auth/logout` (`main.py:725`) — revokes the presented session token; returns `204`.
- `GET /api/v1/auth/health` (`extended.py:1053`) — identity backend liveness; no secrets.
- `GET /api/v1/auth/providers` (`main.py:732`) — returns the enabled methods: `{"local": {"enabled": true, "method": "password"}, "api_tokens": {"enabled": true}, "sso": [...]}`.

### Provisioning the first admin (operators)

Per `packages/eoip/authn/provision.py`, set `EOIP_ADMIN_USERNAME` + `EOIP_ADMIN_PASSWORD` (or `EOIP_ADMIN_PASSWORD_FILE`) and run the CLI:

```bash
eoip-admin from-env      # or: eoip-admin create-admin --username alice
```

The same command maps `EOIP_API_TOKEN` + `EOIP_API_TOKEN_ROLES` to a service principal. Passwords must meet the store's policy; a username without a password raises `CredentialError("EOIP_ADMIN_USERNAME is set but EOIP_ADMIN_PASSWORD(_FILE) is not")`.

### OIDC / SAML / LDAP — honest status

- `packages/eoip/authn/sso.py` defines `OIDCProviderStub` and `SAMLProviderStub`, both **disabled placeholders**. Calling `GET /api/v1/auth/sso/{provider}/login` (`main.py:738`) returns `501 "<PROTOCOL> SSO is a placeholder and not implemented"`. Setting `EOIP_SSO_PROVIDER` to a real value fails closed at startup (`sso.py:83 check_sso_configuration`).
- `packages/eoip/authn/oauth_sso.py` contains a fuller OAuth2/OIDC toolkit (`OAuthProvider.create_authorization_url`, PKCE generation, `OIDCDiscovery` for well-known configuration) — usable library code, but **not wired to any runtime route**.
- There is **no LDAP provider** in the codebase. Do not plan on LDAP without adding an integration.

---

## 8.3 RBAC and ABAC

**What it does.** EOIP combines roles (RBAC) with YAML policy statements that can match resource attributes (ABAC). All of these routes are in `apps/api/extended.py:1062-1149` and are **admin-protected** by the middleware.

### Roles and the permission catalog

The known permissions (`packages/eoip/authz/core.py:36-45`) are exactly:

`graph:read`, `graph:mutate`, `ontology:publish`, `agents:approve`, `admin:*` (wildcard), `audit:read`, `policy:manage`, `user:manage`.

**List roles:** `GET /api/v1/authz/roles` → `{"roles": [...]}`.
**Create a role:** `POST /api/v1/authz/roles` (201):

```bash
curl -s http://localhost:8000/api/v1/authz/roles \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name": "checkout-ops", "description": "Checkout service operators",
       "permissions": ["graph:read", "graph:mutate"]}'
```

Unknown permissions are rejected (`422`); a duplicate name returns `409`. `GET /api/v1/authz/roles/export` downloads a deterministic JSON export.

### Users

```bash
# create user EOIP-123's operator
curl -s http://localhost:8000/api/v1/authz/users \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"user_id": "u-42", "roles": ["checkout-ops"], "attributes": {"team": "payments"}}'
```

`POST /api/v1/authz/users` (201) returns the user dict; duplicate → `409`. `GET /api/v1/authz/users` lists all; `GET /api/v1/authz/users/export` exports JSON. (Note: this is the *authorization* user store, separate from the login credential store in 8.2.)

### Policy YAML load/reload

`GET /api/v1/authz/policies` shows loaded statements. `POST /api/v1/authz/policies/reload` accepts a raw YAML body (`Content-Type: application/yaml`) and appends statements; add `?replace_existing=true` to replace the whole set (`extended.py:1119`). Statement shape (`packages/eoip/authz/core.py:122 PolicyStatement`): `role`, `action`, optional `resource` `Condition` attributes, and an effect.

```bash
curl -s -X POST "http://localhost:8000/api/v1/authz/policies/reload?replace_existing=false" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/yaml" \
  --data-binary @policies/checkout.yaml
```

**Response:** `{"loaded": <count>}`. Malformed YAML or bad keys → `422` with the parser message.

### Evaluate and the decisions audit

```bash
curl -s http://localhost:8000/api/v1/authz/evaluate \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"user_id": "u-42", "action": "graph:mutate",
       "resource_attrs": {"service": "checkout", "env": "prod"}}'
```

**Response:** an audit record from `Decision.to_audit_record()` (`core.py:216`) — decision allow/deny (default is **deny** when nothing matches), matched statement, timestamp. Every evaluation is appended to the in-memory decision log; read it with `GET /api/v1/authz/decisions` (requires `audit:read`).

**Errors and recovery.** `404 "unknown user: <id>"` → create the user first. `403 "Administrative role required"` → these routes need an admin role. Decisions are kept in memory (`state.decision_log`), so they are lost on restart — export them before restarting if they matter.

---

## 8.4 Tenancy

**What it does.** All routes live under `/api/v1/tenancy` (`packages/eoip/tenancy/router.py`) and resolve a **tenant context** from headers (`packages/eoip/tenancy/context.py:32-33`):

- `X-Tenant-Id` — tenant URN or short id, e.g. `t-001` or `urn:eoip:tenancy:tenant:t-001`
- `X-Principal` — the authenticated principal name

Fail-closed: missing headers produce `403`. Lifecycle mutations additionally need the principal header.

### Context echo

```bash
curl -s http://localhost:8000/api/v1/tenancy/context \
  -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: t-001" -H "X-Principal: alice"
```

**Response:** `{"tenant_id": "t-001", "urn": "...", "principal": "alice"}`.

### Isolation models and placement

`GET /isolation/models` returns the catalog. The models (`packages/eoip/tenancy/isolation.py:46-49`) are **`silo`, `bridge`, `pool`**.

```bash
curl -s -X POST http://localhost:8000/api/v1/tenancy/isolation/placement \
  -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: t-001" -H "X-Principal: alice" \
  -H "Content-Type: application/json" \
  -d '{"model": "silo", "layers": {"graph": "named-graph", "storage": "dedicated"}}'
```

`GET /isolation/placement` returns the current placement; `404` if none is registered. Bad model/layer values → `400`.

### Quotas

Dimensions (`packages/eoip/tenancy/quotas.py:35-41`): `graph_size`, `ingestion_rate`, `concurrent_queries`, `llm_tokens`, `storage_bytes`.

```bash
# dry check — does not consume
curl -s -X POST http://localhost:8000/api/v1/tenancy/quotas/check \
  -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: t-001" -H "X-Principal: alice" \
  -H "Content-Type: application/json" -d '{"dimension": "llm_tokens", "amount": 5000}'

# consume (idempotent with a key)
curl -s -X POST http://localhost:8000/api/v1/tenancy/quotas/consume \
  -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: t-001" -H "X-Principal: alice" \
  -H "Content-Type: application/json" \
  -d '{"dimension": "llm_tokens", "amount": 5000, "idempotency_key": "req-EOIP-123-1"}'
```

`GET /quotas` returns `{tenant_id, lane, spec, usage}`. **Over quota:** `consume` returns HTTP `429` with the decision dict in `detail`. `POST /quotas/refund` returns quota. Unknown dimension → `400 "unknown quota dimension: ..."`.

### Lifecycle

`POST /lifecycle/provision` (body: `{"model": "...", "layers": {...}}`) then `POST /lifecycle/{configure|suspend|resume|clone|export|delete}` — no body, tenant from headers. Each returns a lifecycle event dict; invalid transitions → `400`.

### Metering

```bash
curl -s -X POST http://localhost:8000/api/v1/tenancy/metering/record \
  -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: t-001" -H "X-Principal: alice" \
  -H "Content-Type: application/json" \
  -d '{"dimensions": {"llm_tokens": 1234, "graph_size": 42}, "note": "EOIP-123 batch"}'
```

`GET /metering/verify` → `{"tenant_id", "verified": true|false, "chain_head"}` — re-verifies the tamper-evident hash chain. `GET /metering/export` returns the full billing export including the chain head.

---

## 8.5 Licensing

**What it does.** Routes under `/api/v1/licensing` (`packages/eoip/licensing/api.py`). License keys come from the `EOIP_LICENSE_KEY` env var or a file path in `EOIP_LICENSE_KEY_FILE` (air-gapped friendly — `packages/eoip/licensing/cli.py:30`, `license_file.py:17`).

- `GET /api/v1/licensing/status` — entitlement summary plus any compliance notice (`checker.summary()`).
- `POST /api/v1/licensing/verify` — body `{"document": {...license JSON...}, "vendor_key": "<key>"}`; returns a `LicenseVerification` (signature validity etc.).
- `POST /api/v1/licensing/check-module` — body `{"module": "graph"}`; returns a `CheckOutcome` after applying the degradation policy (`checker.degrade(...)`).
- Metering: `POST /meter/record` with `{"metric": "api_calls", "value": 1, "tenant_id": "t-001"}`; `GET /meter/verify` re-verifies the meter hash chain; `GET /meter/export` downloads usage for billing. Meter files live under `$EOIP_DATA_DIR/meter` (`meter.py:75`).

**Errors:** an invalid signature in `verify` returns a verification object with a failure status (not an exception); a module you are not entitled to returns a degraded/denied `CheckOutcome` — enable the module in the license or accept the degraded mode.

---

## 8.6 Layered configuration

**What it does.** Settings live in a seven-layer hierarchy (`packages/eoip/config/layered.py:60-79`), lowest precedence first:

`product-default` → `edition` → `partner` → `tenant` → `business-unit` → `workspace` → `user`

Higher layers win. Keys containing `security`, `auth`, `egress`, `privacy`, `compliance`, `encryption`, or `retention` are *security-relevant*: the **most restrictive** floor/ceiling across layers wins, and lower layers cannot loosen an upper layer's bound (`layered.py:81-91`). All routes are under `/api/v1/config` (`packages/eoip/config/router.py`).

### Worked multi-layer example

```bash
# 1. set a product-wide default
curl -s -X POST http://localhost:8000/api/v1/config/set -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "retention.days", "layer": {"kind": "product-default", "instance": "global"},
       "value": 365, "actor": "alice", "reason": "baseline"}'

# 2. tenant t-001 tightens it (allowed: lower layer within upper bounds, more restrictive)
curl -s -X POST http://localhost:8000/api/v1/config/set -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "retention.days", "layer": {"kind": "tenant", "instance": "t-001"},
       "value": 90, "actor": "alice", "reason": "DPO decision EOIP-123"}'

# 3. explain the effective value
curl -s "http://localhost:8000/api/v1/config/explain?key=retention.days&tenant=t-001" \
  -H "Authorization: Bearer $TOKEN"
```

**Response to explain** (`ExplainResult`): the winning value plus a `LayerContribution` entry per layer (who contributed what, or absence), after precedence and floor/ceiling clamping.

### Other operations

- `GET /definitions` — registered setting definitions (schema, bounds, whether `structural`).
- `GET /effective?key=...&tenant=...&business_unit=...&workspace=...&user_id=...` — the resolved value only; `404` for an unknown key.
- `POST /bounds` — `{"key", "layer", "floor": ..., "ceiling": ..., "actor"}` sets hard bounds (SR-CFG-002).
- `GET /audit?key=...` — full `ConfigChangeRecord` trail for a key.
- `POST /rollback` — `{"key", "layer", "to_version": <int>, "actor"}` reverts to a prior version.
- `POST /export` — `{"layer": {...}}` → a `ConfigArchive` JSON document.
- `POST /import` — `{"payload": <archive or string>, "format": "json", "dry_run": true, "actor", "approved_by"}`; response `{ok, dry_run, errors, applied}`. **Always run with `"dry_run": true` first.**
- `POST /diff` — `{"from": <archive>, "to": <archive>}` → the diff plus `changed_count`.
- `GET /flags` / `POST /flags` (`{"key", "enabled": true|false, "actor"}`) — feature flags. Flags are a separate namespace: they carry no schema layering and **never bypass bounds** (`layered.py:270-274`).
- `POST /reload-subscribe` — `{"key": "..."}`; returns `{"key", "reloadable": bool}`. Honest note (`router.py:188-193`): this only *checks* whether a key is hot-reloadable; the actual streaming subscription is external.

**Errors:** unknown key → `404`; value outside bounds or failed validation → `422`.

---

## 8.7 Egress gateway

**What it does.** The egress gateway is the only way data reaches external services (e.g. LLM providers). Default posture is **S0 — nothing leaves** — until an administrator enables an endpoint with a signed consent record (`packages/eoip/egress/gateway.py:6`). Routes: `/api/v1/egress` (`packages/eoip/egress/router.py`). Admin routes (`/endpoints`, `/plugins`, `/policy`, `/kill`) require an admin role via the middleware (`apps/api/main.py:570-573`); `/call` is open to authenticated users and governed by policy.

### Sharing levels S0–S7

From `packages/eoip/egress/policy.py:13-15` and `54-64`:

| Level | Meaning |
|---|---|
| S0 | None (default) |
| S1 | Schema-only |
| S2 | Aggregates |
| S3 | Synthetic |
| S4 | Tokenized/pseudonymized |
| S5 | Redacted excerpts |
| S6 | Minimized full context, per-request human approval (exact preview) |
| S7 | Full |

Data classes: `D0` public, `D1` metadata/schema, `D2` internal business facts, `D3` confidential, `D4` restricted — **D4 may never leave** (`policy.py:46 RESTRICTED_CLASSES`). Tags: `PII, PHI, PCI, SECRET, SOURCE_CODE, IP, LEGAL_PRIVILEGED, EXPORT_CONTROLLED, EMPLOYEE, CUSTOMER, FINANCIAL, GEO`. Sensitive tags (`PII/PHI/PCI/SECRET/SOURCE_CODE`) force a schema-only ceiling unless a rule explicitly lifts it — and the implicit ceiling wins on conflict (fail closed, `policy.py:120-129`). Evaluation is **most-restrictive-wins**: the effective level is the minimum `max_level` of all matching rules, floored at the default (S0).

### Enable an endpoint (with consent record)

```bash
curl -s -X POST http://localhost:8000/api/v1/egress/endpoints/llm-eu-1/enable \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"endpoint_id": "llm-eu-1", "admin": "alice", "signer": "dpo@example.com",
       "dpa_ref": "DPA-2026-041", "residency_region": "eu-west-1",
       "scope": "summarize,classify"}'
```

**Response:** `{"enabled": "llm-eu-1"}`. The consent record is stored immutably; inspect it with `GET /endpoints/{id}/consent` (returns `current`, `history`, `reapproval_required`). Changing contract terms via `POST /endpoints/{id}/consent/amend` marks the endpoint as requiring re-approval (`409` if terms conflict). `POST /endpoints/{id}/disable` (body `{"admin", "reason"}`) turns it off. `GET /endpoints` lists endpoints plus `kill_switch_global` and `killed_endpoints`.

### Policy rules

```bash
curl -s -X POST http://localhost:8000/api/v1/egress/policy/rules \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"rule": {"rule_id": "checkout-summarize",
        "classes": ["D2"], "tags": [], "tasks": ["summarize"],
        "endpoints": ["llm-eu-1"], "roles": [], "regions": ["eu-west-1"],
        "max_level": 5, "approval": "none",
        "reason": "redacted excerpts OK for EU summarization"}}'
```

`GET /policy/rules` returns `{"rules": [...], "default_level": 0}`.

### Call with dry-run preview

```bash
curl -s -X POST http://localhost:8000/api/v1/egress/call \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"endpoint_id": "llm-eu-1", "task": "summarize",
       "payload": {"text": "Order EOIP-123 delayed for customer Jane Doe, email jane@example.com"},
       "user_id": "u-42", "role": "checkout-ops",
       "data_classes": ["D2"], "tags": ["PII"], "region": "eu-west-1",
       "dry_run": true, "estimated_cost": 0.002}'
```

**Response/result:** with `dry_run: true`, the gateway evaluates policy and returns the decision and the **exact transformed payload that would leave** (after DLP redaction/tokenization for the allowed level) without sending anything. A denial returns `403` with `{"detail": {"reason": ..., "fallback_notice": ...}}` — e.g. `"endpoint llm-eu-1 is disabled (default S0)"` or `"policy default deny (S0): ..."` (`gateway.py:301,327`). Budget overrun → `429`. Every executed call seals an immutable `EgressManifest`.

### Kill switch, manifests, "what left the building"

- `POST /kill` with `{"admin": "alice", "reason": "incident"}` — global kill; add `"endpoint_id"` to kill one endpoint.
- `GET /manifests` — every sealed per-call manifest (SR-LLM-013).
- `GET /report` — the "what left the building" export (`gateway.report()`), aggregating manifests.

### Plugin data-flow manifests

Providers submit a `ServiceProviderManifest` including a `data_flow` section:

```bash
curl -s -X POST http://localhost:8000/api/v1/egress/plugins/submit \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"manifest": {"id": "acme-ocr", "name": "Acme OCR", "capability": "ocr",
       "data_flow": {"fields": ["image"], "regions": ["eu-west-1"], "retention": "none"}}}'
```

Then `GET /plugins/{manifest_id}/install-preview` shows exactly what installing implies, and:

```bash
curl -s -X POST http://localhost:8000/api/v1/egress/plugins/install \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"manifest_id": "acme-ocr", "approved_by": "alice",
       "acknowledged_fingerprint": "<fingerprint from preview>", "consent_ref": "DPA-2026-041"}'
```

The install is admin-approved; if the API carries a principal, the approver is the authenticated admin, overriding `approved_by` (`router.py:241-245`). `GET /plugins` lists manifests with install state and their `data_flow`.

**Errors and recovery.** `404 unknown endpoint` → register/enable first. `403 EgressDenied` → read `reason`, add a rule or request approval (S6 needs `approval_id`). `400` on install → fingerprint mismatch or unknown manifest.

---

## 8.8 Branding

**What it does.** Per-tenant white-labeling under `/api/v1/branding` (`packages/eoip/branding/router.py`). Cross-tenant access is forbidden (`403 "Cross-tenant branding access forbidden"`); the tenant comes from the authenticated principal or an explicit `tenant_id` query parameter.

- `GET /theme?tenant_id=t-001&mode=light` — the resolved theme view (`ThemeMode` `light`/`dark`).
- `POST /terminology/rename?tenant_id=t-001` — body `{"canonical_types": ["Issue", "Service"]}` → `{"renames": {...}}`, applying the tenant's display names.
- `POST /terminology/canonicalize?tenant_id=t-001` — body `{"labels": ["Ticket", "Microservice"]}` → `{"canonical": {"Ticket": "Issue", ...}}` (maps tenant labels back to canonical names).
- `GET /locales/{locale}/message?tenant_id=t-001&key=welcome&default=Hello` — a localized message with fallback.
- `GET /legal?tenant_id=t-001&kind=privacy` — published legal content records (impressum, privacy notice, terms; filter optional).

**Errors:** missing `tenant_id` on locales/legal → `422`; cross-tenant → `403`.

---

## 8.9 Privacy

**What it does.** Data classification, GDPR-style subject requests (DSAR), consent, retention, and residency under `/api/v1/privacy` (`packages/eoip/privacy/router.py`). The tenant is taken from the authenticated principal; a body `tenant_id` may only *repeat* it (`403` on mismatch). Platform principals must name the tenant explicitly (`422` otherwise).

### Classify

```bash
curl -s -X POST http://localhost:8000/api/v1/privacy/classify \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"payload": {"customer": "Jane Doe", "email": "jane@example.com",
                  "note": "called about EOIP-123"},
       "source_ref": "checkout/tickets/EOIP-123", "tenant_id": "t-001"}'
```

**Response:** a `ClassificationResult` — detected classes/labels per field (e.g. email → PII), usable to feed egress `data_classes`/`tags`.

### DSAR

- `POST /dsar/locate` — `{"subject_id": "jane@example.com", "tenant_id": "t-001"}` → a location report of every record about the subject.
- `POST /dsar/export` — same body → `{"export": <name>, "bundle": {...}, "proof": {...}}`. Requires tenant stores; otherwise `501 "DSAR export needs tenant stores"`.
- `POST /dsar/rectify` — `{"subject_id", "old_value", "new_value", "tenant_id"}`; `422` if `old_value` is empty or equals `new_value`.
- `POST /dsar/erase` — same body as locate → erasure report, propagated to derived stores via `ErasurePropagator`.

### Consents, retention, residency

- `GET /consents/allowed?subject_id=jane@example.com&purpose=marketing&tenant_id=t-001` → `{"allowed": true|false}`.
- `POST /consents` — record a `ConsentRecord`; returns `{"recorded": true, "id": ...}`.
- `POST /retention/evaluate` — `{"records": [...]}` → expiry decisions per record.
- `POST /residency/validate` — `{"tenant_id": "t-001", "placements": [...]}` → validation result of placements against the residency policy.

---

## 8.10 Compliance

**What it does.** Framework packs, gap analysis, AI governance, change governance, governance roles, and policy exceptions under `/api/v1/compliance` (`packages/eoip/compliance/router.py`). Stores default to on-disk JSON under `EOIP_DATA_DIR`.

### Packs and gap analysis

Built-in frameworks (`packages/eoip/compliance/packs.py:239-273`): **GDPR, SOC2, ISO27001, HIPAA, DPDP-2023** (additional packs may exist in `extended_packs.py`).

```bash
curl -s http://localhost:8000/api/v1/compliance/packs -H "Authorization: Bearer $TOKEN"
curl -s -X POST http://localhost:8000/api/v1/compliance/packs/GDPR/gap-analysis \
  -H "Authorization: Bearer $TOKEN"
```

Gap analysis returns the pack's requirements with per-requirement status computed from live evidence sources (policy exceptions, AI governance records). Unknown framework → `404 "Unknown pack: ..."`.

### AI governance

- `GET/POST /ai/model-cards` — list / register (201) model cards; `GET /ai/model-cards/{id}/label` returns the AI-disclosure label for a model.
- `GET/POST /ai/evaluations` — evaluation records; filter with `?model_card_id=`.
- `POST /ai/oversight` (201) — register a `HumanOversightConfig`.

### Change proposals

```bash
curl -s -X POST "http://localhost:8000/api/v1/compliance/changes" \
  -H "Authorization: Bearer $TOKEN" \
  --data-urlencode "kind=config" --data-urlencode "title=Tighten retention for t-001" \
  --data-urlencode "requested_by=alice"
# then transition it
curl -s -X POST "http://localhost:8000/api/v1/compliance/changes/<proposal_id>/transition" \
  -H "Authorization: Bearer $TOKEN" \
  --data-urlencode "to_state=approved" --data-urlencode "actor=bob" \
  --data-urlencode "at=2026-02-14T10:00:00Z" --data-urlencode "reason=reviewed"
```

(`kind`, `title`, `to_state`, etc. are **query/form parameters**, not a JSON body — see the signatures at `router.py:106-133`.) `GET /changes?state=...&kind=...` lists. Unknown proposal → `404`; illegal state transition → `409`.

### Roles and exceptions

- `GET /roles`, `GET /roles/{role}`, `GET /roles/auditor-view` — the governance role catalog (read-only view for auditors).
- `GET /exceptions?active_only=true` — policy exceptions; `POST /exceptions` (`policy_ref`, `subject`, `justification`, `approved_by`, `expires_at` as parameters) creates one (201); `POST /exceptions/{id}/revoke?actor=alice` revokes it. Unknown exception → `404`.

---

## 8.11 Knowledge firewall

**What it does.** Screens content *before* it crosses into an agent context, redacting secrets and PII and optionally blocking restricted material (`packages/eoip/agents/firewall.py`).

**Access:** `POST /api/v1/knowledge/firewall/inspect` (`apps/api/app.py:1378`). Request model (`app.py:173-177`): `content` (1–50,000 chars), `boundary` (default `"agent_context"`), `source_ref` (optional), `block_on_restricted` (default `false`).

```bash
curl -s -X POST http://localhost:8000/api/v1/knowledge/firewall/inspect \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"content": "Deploy key AKIAIOSFODNN7EXAMPLE for service checkout; contact jane@example.com",
       "boundary": "agent_context", "source_ref": "checkout/deploy-notes",
       "block_on_restricted": true}'
```

**Response/result:**

```json
{
  "content": "Deploy key [REDACTED] for service checkout; contact [REDACTED-PII]",
  "blocked": false,
  "untrusted": true,
  "classifications": ["secret", "pii"],
  "boundary": "agent_context",
  "decisions": [
    {"rule_id": "KFW-SECRET-REDACTION", "outcome": "REDACT",
     "summary": "Secret-like source content was removed before agent use."},
    {"rule_id": "KFW-PII-REDACTION", "outcome": "REDACT",
     "summary": "PII-like source content was removed before boundary crossing."}
  ],
  "provenance": {...}
}
```

Use the returned `content` (never the original) downstream. `blocked: true` means the content hit a restricted pattern while `block_on_restricted` was set — do not forward it; review the `decisions` list instead.

**Errors:** `422` for empty or >50,000-character `content`. `401` without a token — this route is not on the allow-list.
