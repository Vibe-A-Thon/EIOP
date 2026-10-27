# KnowGridFlow (EOIP) API Reference

## API Contract and Authentication

The active application is created by `apps.api.main:create_app` and exposes OpenAPI at `/openapi.json`; the interactive schema browser is `/docs` when enabled. `apps/api/app.py` contains the injected-store graph/query app used by the main factory. Route declarations may be added by the factory and mounted routers, so runtime OpenAPI—not a static list in this guide—is authoritative for the deployed build. Route count changes with modules and configuration.

Protected routes require an authenticated principal; the application rejects missing/invalid credentials with 401 (and insufficient roles with 403). There is no default account: principals are provisioned explicitly with `eoip-admin` (argon2id password login via `POST /api/v1/auth/login`, per-user `eoip_pat_...` API tokens) or through an `EOIP_ASG_FILE` token file, and the API refuses to start when no principal exists. `EOIP_API_TOKEN` is **not** a login credential: it is the outgoing service token used by the MCP facade, accepted by the API only when `eoip-admin from-env` maps it to a principal with `EOIP_API_TOKEN_ROLES` — without roles it grants nothing. See [Authentication and roles](authentication.md) for the full precedence. Local container credentials (admin password and the mapped service token) are generated into ignored `deploy/.env`; host-only development must provision a principal explicitly. Never put real tokens into URLs, example request bodies, logs, or committed files.

Unauthenticated liveness/readiness probes are available at `/health/live` and `/health/ready`; Prometheus metrics are available at `/metrics`. Most functional APIs are under `/api/v1`. Use the generated OpenAPI schema for exact request/response models, parameters, and status codes.

## Core REST API Endpoints (Route Families)

| Family | Representative active paths | Purpose |
|---|---|---|
| Graph query | `GET /api/v1/search`, `POST /api/v1/query`, `/path`, `/impact`, `/lineage`, `/neighborhood`, `/traceability`, `/query/nl` | Search, structured/NL query, bounded traversal, impact, provenance, and traceability |
| Graph operations | `/api/v1/graph/schema`, `/statistics`, `/metrics`, `/versions`, `/as-of`, `/diff`, `/events`, `/link-prediction`, `/what-if` | Schema/health views, snapshots, graph analysis, changes, and simulations; individual operations may require a backend capability |
| Ontology and semantics | `/api/v1/ontology/export`, `/import`, `/shacl`, `/validate`, `/diff`, `/drift`, `/proposals` | JSON-LD import/export, shape validation, ontology review, and drift surfaces |
| Source registry and ingestion | `/api/v1/sources`, `/api/v1/sources/{source_id}/sync`, `/reconcile`, `/replay`, `/api/v1/admin/ingestion/*` | Source configuration, baseline/incremental jobs, manual ingestion, reconciliation, and replay |
| Jobs, validation, and audit | `/api/v1/admin/jobs`, `/api/v1/ingestion/runs`, `/api/v1/validation/runs`, `/api/v1/admin/audit`, `/api/v1/admin/dlq` | Job state, validation history, restricted audit reads, dead-letter inspection/replay |
| Agents and proposals | `/api/v1/agents`, `/api/v1/agents/{agent_id}/runs`, `/api/v1/agents/runs/{run_id}/explanation`, `/api/v1/agents/proposals` | Bounded agent execution, run inspection, explanations, and inert review proposals |
| Evidence and retrieval | `/api/v1/evidence/manifest`, `/api/v1/rag`, `/api/v1/retrieval/search`, `/api/v1/lineage` | Retrieval and evidence/provenance APIs; availability and output depend on configured route and data |
| Governance and identity | `/api/v1/auth/*`, `/api/v1/authz/*`, `/api/v1/governance/*`, `/api/v1/identity/*`, `/api/v1/tenancy/*` | Authentication health/login, policy evaluation, governance state, identity, and tenancy controls |
| Federation, truth, and products | `/api/v1/federation/*`, `/api/v1/truth/*`, `/api/v1/catalog/products/*`, `/api/v1/taxonomy/*` | Source federation, claims/contradictions, persisted products, and taxonomy mappings |
| Platform/operations | `/api/v1/platform/*`, `/api/v1/ops/*`, `/api/v1/health/*`, `/api/v1/brain/*` | Admin platform modules, readiness/health, operations, and brain-oriented interfaces |
| MCP | `POST /api/v1/platform/tools/mcp/connect-external`, `POST /api/v1/platform/tools/attest-execution` | Authenticated operator selects a configured server/transport and invokes an allowlisted read-only external MCP tool |

Many route families contain experimental, profile-gated, or incomplete capabilities. A route's presence in OpenAPI does not by itself imply a qualified integration, durable backing store, or production readiness. Check readiness, configuration, response state, tests, and the owning workstream evidence before relying on an advanced route.

The newly added REVA router uses `/api/reva/v1` when `REVA_ENABLED=true`, outside the usual `/api/v1` prefix. Its static health endpoint is exempt from the generic bearer check; the optional mount can silently fail, and the inspected host factory does not initialize its warrant kernel. Do not generalize the trusted-identity guarantees above to caller-provided REVA tenant/principal headers without verification. See [REVA component and deployment boundaries](../reva/README.md).

## Representative Calls

Search and query examples use authenticated requests. `TOKEN` below is any provisioned credential — a session token from `POST /api/v1/auth/login`, a per-user `eoip-admin issue-token` API token, or an `EOIP_ASG_FILE` entry. The precise schemas are in `/openapi.json`.

```bash
curl -H "Authorization: Bearer $TOKEN" \
	"http://localhost:8000/api/v1/search?q=checkout&limit=10"

curl -X POST http://localhost:8000/api/v1/query \
	-H "Authorization: Bearer $TOKEN" \
	-H "Content-Type: application/json" \
	-d '{"intent":"SEARCH","anchors":["urn:eoip:service:checkout"],"max_depth":2,"result_limit":10,"evidence_mode":"FULL"}'
```

`POST /api/v1/admin/ingestion/*` and source sync/replay operations typically submit worker jobs and return an operation/job reference instead of waiting for ingestion to finish. Poll the job/status routes in OpenAPI for the returned operation. Dry-run and idempotency behavior are endpoint-specific; consult the request schema and service documentation.

State-changing endpoints require authentication and apply route/service-specific authorization. Read-only access, proposal approval, execution, and external effects are distinct capabilities. Do not treat proposal approval as authorization to directly mutate an external system.

## External MCP Configuration

Configure external MCP servers in the EOIP deployment environment. `EOIP_MCP_ALLOWED_HOSTS` is a comma-separated host allowlist for Streamable HTTP. `EOIP_MCP_READ_ONLY_TOOLS` is a JSON object mapping each configured server name to its allowed read-only tool names. `EOIP_MCP_STDIO_SERVERS` is a JSON object mapping server names to trusted process configurations:

```json
{
	"local-docs": {
		"command": "/opt/eoip/bin/mcp-docs-server",
		"args": ["--stdio"],
		"env": {"DOCS_ROOT": "/srv/approved-docs"},
		"cwd": "/srv/approved-docs"
	}
}
```

Only deployment configuration may select a stdio command, arguments, environment, or working directory. The API request for stdio omits `endpoint`; caller-supplied `command` or other unknown fields are rejected. Both transports use live MCP discovery and the configured read-only tool allowlist. Stdio processes receive the MCP SDK's safe inherited environment plus explicitly configured variables; do not place secrets in arguments or logs.

## Contributing Guidelines

1. **Evidence honesty:** Test doubles and synthetic data are valid for isolated component tests, but never represent them as live integration or production results. Demo loading is an explicit local profile and should be disabled for non-demo operation.
2. **Schema invariants:** Use the canonical mutation boundary, ontology manifest and relevant contracts; do not bypass validation through vendor-specific routes.
3. **Traceability:** Attach the owning requirement IDs to relevant tests. Marker presence and unit success alone do not satisfy integration, persistence, security or independent-effect gates.
4. **Verification:** Exercise the real factory and domain boundary where required. Gate-integrity tests are component checks, not universal release certification. See [Testing Guide](testing-guide.md).

## Operational Contract Notes

The main boundary handles schema/docs, liveness/readiness, metrics, preflight and source webhooks separately from normal bearer-protected functional requests. Webhooks require their source-specific authentication. Do not expose metrics/docs publicly without deployment review. Body buffering has a 4,000,000-byte cap; the web proxy has its own request-size limit.

Inspect both status and response body for partial/unavailable outcomes. Job submission is not job completion. An OpenAPI route or a client-side admin label does not establish permission, storage durability or successful effects. For exact entry-point ownership and change rules, see the [API README](../apps/api/README.md) and [migration guide](migration-refactoring-guide.md).
