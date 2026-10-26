# Chapter 9 — Platform Operations

This chapter covers running EOIP in production: preflight checks, upgrades,
support bundles, metrics and tracing, worker high availability, federation,
the backend adapter catalog, the marketplace, knowledge products, the KGCI
pipeline, QA gate integrity, backup/restore, and HA deployment.

Everything below is grounded in the repository source. Where a behavior was
read from code but **not exercised against a running deployment**, it is
marked *(not runtime-verified)*.

**In this chapter**

1. [Preflight checks](#preflight-checks)
2. [Upgrade planning](#upgrade-planning)
3. [Support bundle](#support-bundle)
4. [Metrics and OpenTelemetry](#metrics-and-opentelemetry)
5. [Worker HA leader lease](#worker-ha-leader-lease)
6. [Federated queries](#federated-queries)
7. [Adapter catalog](#adapter-catalog)
8. [Marketplace packages](#marketplace-packages)
9. [Knowledge products (catalog)](#knowledge-products-catalog)
10. [KGCI pipeline and CI workflow](#kgci-pipeline-and-ci-workflow)
11. [QA gate integrity](#qa-gate-integrity)
12. [Backup, restore, and drills](#backup-restore-and-drills)
13. [HA Compose and Helm deployment](#ha-compose-and-helm-deployment)
14. [Troubleshooting quick table](#troubleshooting-quick-table)

All API examples assume the API is reachable at `http://localhost:8000` and
that you hold a token (`EOIP_API_TOKEN` on the server, sent as a Bearer
header). Example tenant: `t-001`; example issue: `EOIP-123`; example
service: `checkout`.

```bash
TOKEN=...   # value of EOIP_API_TOKEN from deploy/.env
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/ops/preflight
```

---

## Preflight checks

**What it does.** Runs a battery of node-fitness checks before traffic is
admitted: required environment variables, `EOIP_API_TOKEN` configuration,
ontology YAML parseability, graph-store reachability, disk headroom, and
port availability. Implemented in `packages/eoip/ops/preflight.py`
(`run_preflight`); checks never raise — each reports `pass` / `warn` /
`fail`.

**How to access.** `GET /api/v1/ops/preflight`
(`apps/api/extended.py:1354`). From Python, call `eoip.ops.run_preflight(...)`
directly — that is the CLI/library pattern.

**Step by step.**

1. Run it over HTTP:

   ```bash
   curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/ops/preflight
   ```

   The API wires the check with `ontology_paths` from
   `config/ontology/*.yaml` and `port=8000` (`apps/api/extended.py:1358-1364`).

2. Or run it as a library call (e.g. in a deploy pipeline):

   ```bash
   .venv/Scripts/python -c "from eoip.ops import run_preflight; \
     import json; print(json.dumps(run_preflight(port=8000).to_dict(), indent=2))"
   ```

3. Read the report. Every check carries `name`, `status`, `detail`.

**Response/result.**

```json
{
  "id": "urn:eoip:ops:preflight-report:current",
  "ok": true,
  "checks": [
    {"name": "env", "status": "pass", "detail": "0 required env var(s) present"},
    {"name": "token", "status": "pass", "detail": "EOIP_API_TOKEN is configured"},
    {"name": "ontology", "status": "pass", "detail": "3 ontology YAML file(s) parseable"},
    {"name": "graph_store", "status": "pass", "detail": "graph store reachable"},
    {"name": "disk_space", "status": "pass", "detail": "12.34 GiB free on ."},
    {"name": "port", "status": "pass", "detail": "0.0.0.0:8000 is available"}
  ]
}
```

`ok` is true only when no check is `fail` (warnings do not block).

**Errors and recovery.**

- `token` is `warn` ("`EOIP_API_TOKEN` is not set; auth endpoints will be
  disabled") — set the variable in `deploy/.env` before exposing the API.
- `ontology` is `fail` with a parse error — fix the named YAML file under
  `config/ontology/`.
- `graph_store` is `fail` ("unreachable: ...") — check `EOIP_HUGEGRAPH_URL`
  and that the graph container is up (`docker compose -f deploy/docker-compose.yml ps`).
- `disk_space` is `warn` when free space drops below 1 GiB
  (`DEFAULT_MIN_FREE_BYTES`).
- `port` is `fail` when something already holds `0.0.0.0:8000` — stop the
  conflicting process or change `EOIP_API_PORT`.

---

## Upgrade planning

**What it does.** Produces a deterministic version-to-version upgrade plan:
pre-checks, migration steps classified from the ontology semantic-diff
machinery (`eoip.ontology.gitops.diff_manifests`), and a rollback note. No
network or LLM involvement (`packages/eoip/ops/upgrade.py`).

**How to access.** `POST /api/v1/ops/upgrade-plan`
(`apps/api/extended.py:1367`). Note: this endpoint is in the **READ**
authorization tier in `apps/api/route_policy.py:78`.

**Step by step.**

1. Plan a forward upgrade:

   ```bash
   curl -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/v1/ops/upgrade-plan \
     -d '{"current_version": "1.0.0", "target_version": "1.1.0"}'
   ```

   Optional fields `current_manifest` / `target_manifest` (ontology
   manifest dicts) enable migration-step classification.

2. Review `prechecks_ok` and each entry of `migration_steps`.

**Response/result.**

```json
{
  "id": "urn:eoip:ops:upgrade-plan:1.0.0-to-1.1.0",
  "current_version": "1.0.0",
  "target_version": "1.1.0",
  "prechecks": [
    {"name": "version_order", "status": "pass", "detail": "1.0.0 -> 1.1.0 is a forward upgrade"},
    {"name": "graph_store", "status": "pass", "detail": "graph store reachable"},
    {"name": "ontology_diff", "status": "warn", "detail": "manifests not provided; migration steps limited to version bump"}
  ],
  "prechecks_ok": true,
  "ontology_diff": {},
  "migration_steps": [],
  "rollback_note": "Rollback: redeploy version 1.0.0 and restore the pre-upgrade graph snapshot ..."
}
```

With manifests supplied, `migration_steps` items carry `change_type`,
`subject`, `detail`, and `severity` (`breaking` for
`label_removed` / `property_removed` / `edge_removed`, else `safe`).

**Errors and recovery.**

- `prechecks` entry `current_version` / `target_version` `fail` —
  versions must match `^\d+\.\d+\.\d+$` (e.g. `1.0.0-rc.1` is rejected).
- `version_order` `fail` — target is not newer than current; downgrades
  are not planned.
- Always take a snapshot first (`scripts/backup.py`, below); breaking
  ontology changes "require snapshot restore to undo" per the rollback note.

---

## Support bundle

**What it does.** Collects a redacted support handoff document: config
environment variables, recent audit events, graph-store stats, and runtime
versions (`packages/eoip/ops/bundle.py`, schema
`urn:eoip:ops:support-bundle:v1`).

**How to access.** `GET /api/v1/ops/support-bundle`
(`apps/api/extended.py:1378`).

**Step by step.**

1. `curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/ops/support-bundle > bundle.json`
2. Attach `bundle.json` to the support ticket.

**Response/result.** Keys: `id` (`urn:eoip:ops:support-bundle:<epoch>`),
`schema`, `config`, `audit_events` (up to 50 most recent), `graph_stats`,
`versions` (`python`, `platform`, `eoip`).

**What is included/excluded.** Included env vars by default:
`EOIP_GRAPH_BACKEND`, `EOIP_GRAPH_CONFIG`, `EOIP_GRAPH_URL`,
`EOIP_HUGEGRAPH_URL`, `EOIP_API_TOKEN`, `EOIP_ENV`. Any variable whose name
contains `TOKEN`, `SECRET`, `PASSWORD`, `PASS`, `KEY`, or `CREDENTIAL` is
replaced with `***REDACTED***`, and all values additionally pass through
`eoip.audit.redaction.redact_secrets` — secrets never leave the system in a
bundle.

**Errors and recovery.** A missing graph store yields
`graph_stats.available: false`; an audit-sink read failure appears as
`{"error": "..."}` inside `audit_events`. The endpoint itself does not fail
on partial collection.

---

## Metrics and OpenTelemetry

**What it does.** The API exposes a Prometheus text endpoint and records
per-request counters/histograms via middleware; an optional OpenTelemetry
integration ships spans to an OTLP collector.

**How to access.** `GET /metrics` (plaintext, `apps/api/extended.py:1407`;
no auth required — it is in the allowlist at `apps/api/main.py:514`).

**Step by step.**

1. Scrape the endpoint:

   ```bash
   curl http://localhost:8000/metrics
   ```

2. Point Prometheus at it — `deploy/prometheus.yml` and
   `deploy/docker-compose.observability.yml` provide a ready stack.

3. Enable tracing (optional): install the extra
   (`pip install eoip[otel]`) and set the OTLP/HTTP endpoint:

   ```bash
   EOIP_OTEL_ENDPOINT=http://otel-collector:4318/v1/traces
   ```

**Response/result.** The runtime registers these metric families
(`apps/api/main.py:344-370`):

- `eoip_http_requests_total{method,status,tenant}` — completed HTTP requests
- `eoip_operations{operation,status,tenant}` — completed EOIP operations
- `eoip_failures{operation,status,tenant}` — failed operations
- `eoip_operation_duration_seconds{operation,tenant}` — operation latency histogram
- `eoip_ingestion_job_status_transitions{kind,status}` — job status transitions

Every request flows through the `boundary` middleware
(`apps/api/main.py:431`), which assigns/propagates the `X-Correlation-ID`
header (max 128 chars, else regenerated), records an audit event for known
operations, and increments the metrics above. With OTel enabled,
`eoip.observability.otel.setup_tracing` adds the correlation ID to every
span as the attribute `eoip.correlation_id`
(`packages/eoip/observability/otel.py`).

There is also a zero-dependency stdlib metrics registry in
`packages/eoip/observability/metrics.py` (`Registry`, `record_request`,
`timed_request`) for embedding metrics in your own components; it renders
the same Prometheus text format.

**Errors and recovery.**

- Tracing silently off: `setup_tracing` logs "OpenTelemetry not installed;
  tracing disabled" once and returns `False` — install `eoip[otel]`.
- No `EOIP_OTEL_ENDPOINT`: a `TracerProvider` is still installed but no
  exporter is added, so spans go nowhere.
- `/metrics` empty of `eoip_*` series: metrics are in-memory per process;
  a fresh restart or an unreplicated scrape target shows zeros until
  traffic flows. *(not runtime-verified for multi-replica scrape
  aggregation)*

---

## Worker HA leader lease

**What it does.** A filesystem-advisory leader lease guarantees exactly one
worker executes single-writer jobs (indexing, ontology publication,
snapshots) while replicas stand by (`packages/eoip/ha.py`, `LeaderLease`).

**How to access.** Configured by environment on the worker
(`apps/worker/main.py:192-198`):

- `EOIP_LEASE_PATH` — lock-file path on a **shared** volume (e.g.
  `/leases/worker.lock`)
- `EOIP_LEASE_TTL_SECONDS` — TTL, default `30`

**Step by step.**

1. Mount a shared volume into all worker replicas and set both variables.
   The HA compose file does this for you (see
   [HA Compose](#ha-compose-and-helm-deployment)):
   `EOIP_LEASE_PATH=/leases/worker.lock`, `EOIP_LEASE_TTL_SECONDS=30`,
   volume `worker-leases:/leases`.
2. Start the workers: `python -m apps.worker.main`. On startup a worker
   calls `lease.acquire()`; a loser logs the event `worker.lease_contended`
   and idles.
3. During operation `ensure_leader()` renews the lease if held, or
   re-acquires it after the holder's TTL expires; on shutdown the holder
   calls `lease.release()` (`apps/worker/main.py:328-329`).

**Response/result.** The lock file contains
`{"owner": "<uuid>", "expires_at": <monotonic-ts>}`, written atomically
(temp file + `os.replace`) and created with `O_CREAT|O_EXCL` so two
processes on one host cannot both win.

**Errors and recovery.**

- Split-brain safety: the lease is *advisory* on shared filesystems —
  correctness relies on the TTL. Per the module contract, the TTL "must
  exceed the maximum expected GC/pause of the holder."
- A crashed holder blocks others only until `expires_at`; `acquire()`
  steals stale or unparseable leases automatically. `steal()` refuses to
  take a lease that has not expired.
- Windows note: lease coordination across *hosts* requires a genuinely
  shared filesystem; local paths only coordinate processes on one machine.

---

## Federated queries

**What it does.** Splits a semantic query into per-source fragments, pushes
filters/projections down where the source supports it, merges rows locally
with per-row provenance, degrades gracefully when sources are offline, and
returns an explainable routing plan (`packages/eoip/federation/planner.py`,
GAP-FABRIC-001..008).

**How to access.**

- `GET /api/v1/federation/sources` — registered source capabilities
  (`apps/api/extended.py:501`)
- `POST /api/v1/federation/query` — execute (`apps/api/extended.py:508`)

**Step by step.**

1. List sources:

   ```bash
   curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/federation/sources
   ```

2. Query across sources:

   ```bash
   curl -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/v1/federation/query \
     -d '{
       "entity_types": ["Service"],
       "filters": {"domain": "payments"},
       "projection": ["canonical_id", "name"],
       "merge_key": "canonical_id",
       "policy_context": {"tenant_id": "t-001"}
     }'
   ```

   Request fields (`FederationQueryRequest`): `entity_types` (≤ 50),
   `filters`, `projection` (≤ 50), `merge_key` (default `canonical_id`),
   `policy_context`.

**Response/result.**

```json
{
  "rows": [{"canonical_id": "svc-checkout", "name": "checkout",
            "_provenance": {"sources": ["hugegraph-local"]}}],
  "plan": {
    "fragments": [{"source_id": "hugegraph-local", "status": "executed", "cost": 1.0, "..." : "..."}],
    "total_cost": 1.0,
    "degraded_sources": [],
    "policy_denied_sources": []
  },
  "row_count": 1,
  "degraded": false
}
```

Reading the plan: each `fragments[]` decision records which source was
chosen, whether filters were pushed down or re-applied locally, a `cost`,
and a `status` of `planned` / `executed` / `degraded` / `policy_denied`.
`degraded: true` at the top level means at least one source was offline and
results are partial — treat the row set as a lower bound, not truth.

**Errors and recovery.**

- Rows missing that you expected: check `plan.degraded_sources` and
  `policy_denied_sources`; a `policy_denied` source means `policy_context`
  (e.g. tenant) disallowed it.
- A deeper, older engine (`eoip.federation.engine.FederatedGraph`) also
  exists for cross-database graph federation (Neo4j/Neptune/TigerGraph/
  Memgraph catalog bootstrap) and returns `subquery_plans` plus merged
  records with `_provenance_backend`; it is a library API, not the HTTP
  route above.

---

## Adapter catalog

**What it does.** Publishes one `CapabilityManifest` per database backend —
54 manifests total — so the planner can choose pushdown vs in-engine
execution and refuse unsupported plans explicitly
(`packages/eoip/adapters/manifests.py`, SR-GDB-002/003).

**The honesty model.** Every manifest carries
`adapter_status: "real" | "manifest-only"`. Only a handful are `real`
(in-repo protocol-compatible adapters): `neo4j`, `neptune`, `hugegraph`
(default backend), `memory`, `janusgraph`, plus `apache_age` (a SQL-wrapped
openCypher query builder at `packages/eoip/adapters/apache_age.py`) and the
full JanusGraph Gremlin adapter at `packages/eoip/adapters/janusgraph.py`.
Everything else is `manifest-only`: a capability record only — the catalog
**refuses to instantiate it** rather than faking a client. Manifests also
carry `external_gate: true` when live transport needs a protocol EOIP does
not implement in-repo (Bolt/RESP, vendor SDKs), certification tiers
`A`/`B`/`C`/`P2`, and honest notes (e.g. the Kùzu `archived_warning`).

**How to access.**

- `GET /api/v1/adapters/` — list, filter by `category`, `tier`, `role`
- `GET /api/v1/adapters/{backend}` — one manifest (404 unknown)
- `GET /api/v1/adapters/{backend}/statements` — SQL statement preview,
  `apache_age` only

(`packages/eoip/graphbuild/router.py:99-133`.)

**Step by step.**

```bash
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/adapters/?role=graph_store&tier=A"
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/adapters/janusgraph
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/adapters/apache_age/statements
```

**Response/result.** Manifest fields: `backend`, `display_name`,
`category` (`native_graph`/`rdf_store`/`multimodel`/`vector`/`operational`),
`native_surface`, `deployment`, `tier`, `role`, `notes`, `adapter_status`,
`conformance`, `external_gate`, `connection_config`.

**Errors and recovery.**

- 404 on `GET /api/v1/adapters/{backend}` — unknown backend key; list first.
- 400 on `/statements` for anything but `apache_age` — by design.
- Trying to connect a `manifest-only` backend through
  `BackendCatalog.create_store` raises a catalog error; pick a `real`
  backend (`hugegraph` or `memory` are the deployed defaults).

---

## Marketplace packages

**What it does.** Installs, lists, searches, and uninstalls extension
packages distributed as `.eoipkg` zip archives, with HMAC-SHA256 integrity
signatures (`packages/eoip/marketplace/`, GAP-MKT-001..008).

**How to access.**

- `POST /api/v1/marketplace/install` — body is the raw zip bytes
  (`Content-Type: application/zip`)
- `GET /api/v1/marketplace/installed` — list installed
- `GET /api/v1/marketplace/installed/search?q=<term>` — search
  name/description
- `POST /api/v1/marketplace/uninstall/{name}`

All are in the **ADMIN** authorization tier
(`apps/api/route_policy.py:36`, `apps/api/main.py:559-562`).

**Step by step.**

1. Set the shared install key on the server: `EOIP_INSTALL_KEY=<secret>`
   (`packages/eoip/marketplace/signing.py`, `ENV_INSTALL_KEY`). Without it
   signed-package verification cannot run.
2. Build/sign a package (library): `eoip.marketplace.packager` creates the
   archive; `sign_package_archive(archive, key)` embeds `signature.bin`
   inside the zip (self-contained signed package, GAP-MKT-008).
3. Install:

   ```bash
   curl -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/zip" --data-binary @my-pack-1.2.0.eoipkg \
     http://localhost:8000/api/v1/marketplace/install
   ```

4. Verify: `curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/marketplace/installed/search?q=my-pack"`
5. Uninstall: `curl -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/marketplace/uninstall/my-pack`

**Response/result.** Install returns the `PackageManifest` as JSON (name,
version, dependencies, …). Uninstall returns
`{"name": "my-pack", "uninstalled": true}`.

**Errors and recovery.**

- 422 "package signature verification failed" / "package integrity failure"
  — wrong `EOIP_INSTALL_KEY` or a corrupted/tampered archive; re-download
  or re-sign.
- 409 dependency conflict — install the missing dependency first, or the
  package you are uninstalling still has dependents (`dependents_of`
  refuses removal).
- 404 on uninstall — package not installed.
- 401/403 — marketplace routes are admin-only; use an admin-role token.

---

## Knowledge products (catalog)

**What it does.** First-class Knowledge Product records with lifecycle
states, CRUD, filtered listing, JSON export/import, and lineage (source
graphs → product → consumers). Stored as `KnowledgeProduct` vertices in the
graph store (`packages/eoip/catalog/products.py`, GAP-KP-001..005).

**How to access.**

- `GET /api/v1/catalog/products` (filters: `owner`, `domain`, `state`,
  `access_policy`, `consumer`)
- `POST /api/v1/catalog/products` (201)
- `GET / PUT / DELETE /api/v1/catalog/products/{product_id}`
- `POST /api/v1/catalog/products/{product_id}/transition`
- `GET /api/v1/catalog/products/{product_id}/lineage`
- `GET /api/v1/catalog/products/{product_id}/export`
- `POST /api/v1/catalog/products/import`

**Step by step.**

1. Create:

   ```bash
   curl -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/v1/catalog/products \
     -d '{
       "name": "Checkout Impact View",
       "owner": "team-payments",
       "domain": "payments",
       "source_graphs": ["hugegraph-local"],
       "consumers": ["checkout-ops-dashboard"],
       "quality_slo": {"metric": "freshness_lag", "threshold": 300, "unit": "seconds"}
     }'
   ```

   The catalog assigns the canonical id
   `urn:eoip:catalog:knowledge-product:checkout-impact-view`.

2. Promote it through its lifecycle:

   ```bash
   curl -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/v1/catalog/products/urn:eoip:catalog:knowledge-product:checkout-impact-view/transition \
     -d '{"to_state": "Experimental"}'
   ```

3. Inspect lineage: `GET .../products/{id}/lineage`; export a definition:
   `GET .../products/{id}/export` (JSON download).

**Response/result.** Product fields include `name`, `owner`, `domain`,
`source_graphs`, `ontology_version`, `quality_slo` / `freshness_slo`
(`{metric, threshold, unit, window}`), `access_policy` (default
`internal`), `apis`, `dashboards`, `consumers`, `state`, `created_at`,
`updated_at`.

**Errors and recovery.** 404 unknown product; 422 validation error or
**illegal transition**. Allowed transitions (`ALLOWED_TRANSITIONS`):
`Draft → Experimental|Deprecated`, `Experimental → Trusted|Draft|Deprecated`,
`Trusted → Certified|Experimental|Deprecated`, `Certified → Deprecated`,
`Deprecated →` (terminal). DELETE tombstones the record. Import is an admin
route (`/api/v1/catalog/products/import` is in the ADMIN tier,
`apps/api/route_policy.py:49`).

---

## KGCI pipeline and CI workflow

**What it does.** A deterministic knowledge-graph CI/CD pipeline with nine
stages, runnable over HTTP or as a CLI that exits 0/1 for gating
(`packages/eoip/ci/pipeline.py`, GAP-KGCI-001..004).

**Stages** (in `STAGE_ORDER`): `lint`, `schema_validation`,
`contract_checks`, `graph_invariants`, `quality_gates`, `compatibility`,
`security`, `migration`, `publish`. Stages whose inputs are absent report
`skipped` rather than failing.

**How to access.**

- `POST /api/v1/kgci/run` — run synchronously (`apps/api/extended.py:1325`)
- `GET /api/v1/kgci/report` — most recent report (404 before the first run)
- CLI: `python -m eoip.ci --ontology-dir config/ontology --scan-dirs packages/eoip config --output-dir test-results/kgci --report test-results/kgci/kgci-report.json`

**Step by step.**

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/kgci/run \
  -d '{"ontology_dir": "config/ontology", "fail_on": "any"}'
```

`fail_on` must be one of `FAIL_ON_CHOICES` (default `any`; other choices
include gating only on breaking stages — invalid values get a 422 listing
the choices). The API fixes `scan_dirs` to `["packages/eoip", "config"]`
and disables the publish stage (`output_dir=None`).

**Response/result.** `KGCIReport`: `passed`, `failed_stages`, and a
`stages[]` list of `{stage, status: passed|failed|skipped, findings[]}`.
The CLI exits with `report.exit_code()` (1 on failure per `fail_on`).

**CI integration.** `.github/workflows/ci.yml` step "KG CI pipeline
(GAP-KGCI-001..004)" runs the CLI with `--output-dir test-results/kgci
--report test-results/kgci/kgci-report.json` and uploads the report as the
`kgci-report` artifact; `validation-evidence.yml` has an equivalent
release-gate job.

**Errors and recovery.** Read `failed_stages`, then the `findings[]` of
each failed stage (file + message). Fix and re-run; the pipeline has no
side effects unless `--output-dir`/`publish` is enabled via CLI.

---

## QA gate integrity

**What it does.** Honest quality reporting: an explicit behavioral-evidence
registry, mutation checks, a three-number dashboard, live code inventory,
and a ruff policy gate (`packages/eoip/qa/`, SR-QA-010..014). Docstrings
and comments never count as evidence — every number comes from structured,
explicitly recorded data.

**How to access** (router built by `packages/eoip/qa/router.py`, prefix
`/api/v1/qa`):

- `GET /api/v1/qa/evidence/coverage?requirement_ids=REQ-A,REQ-B`
- `POST /api/v1/qa/evidence/register` — record `{requirement_id, test_id, source}`
- `GET /api/v1/qa/evidence/coverage/{requirement_id}`
- `POST /api/v1/qa/mutation-checks` — body needs `fixture_test_file`
  (plus optional `check_id`, `requirement_id`, `test_id`, `release`)
- `GET /api/v1/qa/mutation-checks` and `.../mutation-checks/release/{release}`
- `GET /api/v1/qa/dashboard`
- `POST /api/v1/qa/dashboard/test-runs` and `.../dashboard/external-gates`
- `GET /api/v1/qa/inventory`, `POST /api/v1/qa/inventory/validate`
- `POST /api/v1/qa/policy-gate/run`, `GET /api/v1/qa/policy-gate/latest`

**Step by step.**

1. Register evidence:

   ```bash
   curl -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/v1/qa/evidence/register \
     -d '{"requirement_id": "REQ-OPS-001", "test_id": "tests/ops/test_preflight.py::test_preflight", "source": "pytest"}'
   ```

2. Run a mutation check (deliberately break a fixture and confirm the test
   catches it):

   ```bash
   curl -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/v1/qa/mutation-checks \
     -d '{"fixture_test_file": "tests/qa/fixtures/example_test.py", "release": "1.0.0"}'
   ```

3. Read the dashboard: `curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/qa/dashboard`

**Response/result — the three numbers.** SR-QA-012 mandates three *separate*
numbers and prohibits a single "% complete": (1) tests passing, (2)
requirements with behavioral evidence (explicit registry entries), (3)
requirements with external-gate evidence (pen tests, vendor certifications,
recorded via `ExternalGateRecord`). Stores persist under
`EOIP_DATA_DIR` (default `.data`), e.g. `.data/state/qa-external-gates.json`.

**Errors and recovery.** 422 when `fixture_test_file` is missing; 404 from
`policy-gate/latest` before the first run. `POST /api/v1/qa/inventory/validate`
diffs a stored snapshot against live code to catch drift between documented
and actual capabilities.

---

## Backup, restore, and drills

**What it does.** Snapshot the graph plus operational state to a JSON
archive, or a full recovery bundle (zip) that also carries configuration
and local model bytes; restore into an *empty, isolated* deployment; verify
a restore byte-for-byte in a disposable container.

**How to access** (CLI scripts, run from the repo root with the platform
environment loaded):

| Command | Purpose |
|---|---|
| `python scripts/backup.py [--output PATH] [--bundle --model-dir DIR]` | Graph snapshot (`.json`) or full bundle (`.zip`) |
| `python scripts/restore.py SOURCE [--config-dir DIR --model-dir DIR]` | Restore snapshot/bundle into an empty deployment |
| `python scripts/verify_restore.py [--source PATH] [--config-dir DIR] [--model-dir DIR]` | Containerized restore drill |
| `python scripts/smoke_test.py` | End-to-end API smoke test |
| `scripts/container.ps1 backup / restore-test / recovery-acceptance` | Wrapper actions on Windows |

**Step by step.**

1. Backup (default destination
   `<EOIP_DATA_DIR>/backups/eoip-<UTC-timestamp>.json`):

   ```bash
   .venv/Scripts/python scripts/backup.py
   .venv/Scripts/python scripts/backup.py --bundle --model-dir "$HOME/.ollama/models" \
     --output backups/eoip-2026-01-01.zip
   ```

   `--bundle` **requires** `--model-dir`; bundles are capped by
   `--max-bytes` (default `MAX_BYTES` = 64 GiB,
   `packages/eoip/recovery_bundle.py`).

2. Restore into an empty deployment:

   ```bash
   .venv/Scripts/python scripts/restore.py backups/eoip-....json
   .venv/Scripts/python scripts/restore.py backups/eoip-....zip \
     --config-dir /tmp/restore-config --model-dir /tmp/restore-models
   ```

   A `.zip` source is treated as a bundle and **requires** both
   `--config-dir` and `--model-dir` pointing at empty targets.

3. Drill (verifies checksums, graph records, raw/DLQ evidence, and
   operational files in a disposable container):

   ```bash
   .venv/Scripts/python scripts/verify_restore.py --source backups/eoip-....json
   ```

4. Smoke test against a running stack (base URL from `EOIP_API_URL`,
   default `http://eoip-api:8000`): exercises `/api/v1/auth/login`,
   search, path, impact, RAG, admin validation/stats, and a demo replay
   round-trip (`scripts/smoke_test.py`).

**Response/result.** Both scripts print a result dict with `vertices` and
`edges` counts, and emit audit events (`backup_intent`/`backup`,
`restore_intent`/`restore`) with a correlation ID into the audit sink under
`<data_root>/audit`. Snapshots embed a SHA-256 digest (`snapshot.py
digest`) and up to `MAX_OPERATIONAL_FILES = 100_000` operational records /
64 MB.

**Errors and recovery.**

- Restore is refused unless the target is empty — restoring over live data
  is not supported; spin up an isolated deployment instead.
- "Snapshot checksum mismatch" from the drill — archive corruption;
  re-take the backup.
- Bundle validation failures mention the offending path; check
  `--max-bytes` and model-dir contents.
- Every failure is audited with `outcome="failure"` and a `reason_code`.

---

## HA Compose and Helm deployment

**What it does.** Two deployment paths beyond single-node: a multi-replica
Compose stack, and a Helm chart for Kubernetes.

**Docker Compose (single node).**

```powershell
scripts/container.ps1 up        # detects docker/podman/nerdctl/finch, creates deploy/.env
```

or directly: `docker compose -f deploy/docker-compose.yml up -d`.
`container.ps1` actions: `up`, `rebuild`, `hubble-local-admin`,
`demo-data`, `test`, `status`, `logs`, `down`, `backup`, `backup-bundle`,
`extension`, `restore-test`, `acceptance`, `recovery-acceptance`,
`dlq-acceptance`, `detect`, `info`. On success it prints the endpoints:
`http://localhost:8080/app` (web), `http://localhost:8000/docs` (API),
`http://localhost:8001/mcp` (MCP), `http://localhost:8088` (Hubble).

**HA Compose** (`deploy/docker-compose.ha.yml`):

```bash
docker compose -f deploy/docker-compose.ha.yml --env-file deploy/.env up -d
```

Topology: 2 stateless API replicas (`eoip-api-1/2`) behind an nginx LB
(`deploy/nginx/api-lb.conf`, `least_conn`, `max_fails=3 fail_timeout=10s`,
`proxy_next_upstream error timeout http_502 http_503`), 2 worker replicas
sharing the `worker-leases` volume with `EOIP_LEASE_PATH=/leases/worker.lock`
and `EOIP_LEASE_TTL_SECONDS=30`, plus HugeGraph PD/Store placeholders behind
`hugegraph-lb`. Required secrets in `deploy/.env`: `EOIP_API_TOKEN`,
`HUGEGRAPH_PASSWORD`, and `EOIP_SESSION_SECRET` (≥ 32 chars — replicas must
share one session-signing secret). Honest caveat in the file header: it is
"validated for YAML shape only"; HugeGraph PD/Store need enterprise/infra
images. *(not runtime-verified)*

**Helm** (`deploy/helm/eoip`, chart `eoip` 1.0.0, appVersion `1.0.0-rc.1`):

```bash
helm install eoip deploy/helm/eoip -n eoip --create-namespace
helm upgrade eoip deploy/helm/eoip -n eoip -f my-values.yaml
```

Key `values.yaml`: `image.repository/tag`, `api.replicaCount: 2` (port
8000, default pod anti-affinity across `kubernetes.io/hostname`),
`mcp.enabled/replicaCount` (port 8001), plus templates for configmap,
deployment, hpa, ingress, pvc, redis, service. Review a values file before
applying with `POST /api/v1/ops/helm-summary` (`helm_release_summary`), and
inspect HA readiness with `GET /api/v1/ops/ha-topology`.

**Errors and recovery.**

- Compose fails on `${EOIP_API_TOKEN:?...}` — run `scripts/container.ps1`
  to generate `deploy/.env`.
- 502/503 at the LB — check replica health: readiness is
  `GET /health/ready`, served without auth by any replica.
- Session errors across replicas — `EOIP_SESSION_SECRET` differs between
  pods; set one shared value.

---

## Troubleshooting quick table

| Symptom | Likely cause | Where to check | Fix |
|---|---|---|---|
| API down / connection refused | container stopped or port busy | `scripts/container.ps1 status`; `GET /api/v1/ops/preflight` `port` check | `container.ps1 up`; free port 8000 |
| 503 "Graph Service Unavailable" (`application/problem+json`) | HugeGraph unreachable | `EOIP_HUGEGRAPH_URL`; preflight `graph_store` check | restart graph container; fix URL |
| 401 "A valid Bearer token is required" | missing/expired token | `apps/api/main.py` auth middleware; `/api/v1/auth/login` | re-login; check `EOIP_API_TOKEN` |
| 403 on admin route (marketplace, import, sources) | token lacks admin role | `apps/api/route_policy.py` tiers | use an admin-role token |
| Query returns no results | degraded or policy-denied federated source | `plan.degraded_sources` / `policy_denied_sources` in `/api/v1/federation/query` | restore source; fix `policy_context` tenant |
| Stalled ingestion job | lease holder died; job runner idle | `GET /api/v1/admin/jobs`; worker logs for `worker.lease_contended`; lease file TTL | wait for TTL expiry or delete stale lock; restart worker |
| Slow `/api/v1/admin/stats` or queries | large graph, no pushdown | `eoip_operation_duration_seconds` histogram on `/metrics`; adapter manifest `adapter_status` | check OTel traces (`EOIP_OTEL_ENDPOINT`); use a `real` backend |
| Marketplace install 422 | bad signature / corrupt archive | `EOIP_INSTALL_KEY` set on server? | re-sign with the same key; re-upload |
| Restore fails | non-empty target or bad bundle | script error message; audit `restore` events `reason_code` | restore into an empty, isolated deployment; re-run `verify_restore.py` drill |
| KGCI gate red in CI | failed stage findings | `test-results/kgci/kgci-report.json` artifact; `GET /api/v1/kgci/report` | fix findings, re-run `python -m eoip.ci` |
| Tracing absent | OTel extra not installed | one-time log "OpenTelemetry not installed; tracing disabled" | `pip install eoip[otel]`, set `EOIP_OTEL_ENDPOINT` |

---

*Chapter grounded in: `packages/eoip/ops/*`, `packages/eoip/ha.py`,
`packages/eoip/observability/metrics.py` + `otel.py`,
`packages/eoip/federation/*`, `packages/eoip/adapters/*`,
`packages/eoip/marketplace/*`, `packages/eoip/catalog/products.py`,
`packages/eoip/ci/pipeline.py`, `packages/eoip/qa/*`,
`packages/eoip/recovery_bundle.py`, `packages/eoip/snapshot.py`,
`scripts/backup.py`, `scripts/restore.py`, `scripts/verify_restore.py`,
`scripts/smoke_test.py`, `scripts/container.ps1`,
`deploy/docker-compose*.yml`, `deploy/helm/eoip`, `deploy/nginx`,
`apps/api/extended.py`, `apps/api/main.py`, `apps/api/route_policy.py`,
`apps/worker/main.py`, `.github/workflows/ci.yml`.*
