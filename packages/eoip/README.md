# EOIP Domain Package Map

This package contains the shared domain implementation used by the API, worker, MCP integration and test harnesses. The number of modules and their names are not a capability-completion metric. Consult [architecture](../../docs/architecture-guide.md), [requirements index](../../docs/README.md) and source-bound evidence for current qualification.

## Start Here

| Concern | Primary source areas | Boundary |
|---|---|---|
| Runtime selection | `runtime.py`, `graph/backends.py`, `graph/store.py` | Environment/config to graph interface; memory is process-local |
| Ontology and validation | `ontology/`, `validation/`, `contracts/`, root `schemas/` | Canonical labels/contracts and mutation/query validation |
| Acquisition | `connectors/`, `ingestion/`, `ingest/`, `fileparse/`, `codegraph/`, `mapping/` | Source access, parsing, normalization and provenance; trace actual registered handlers |
| Jobs/recovery | `jobs.py`, `scheduling/`, `recovery/`, `snapshot.py`, `recovery_bundle.py` | Lifecycle, persistence and restore; not all helpers share a transactional store |
| Query and retrieval | `query/`, `qlang/`, `search/`, `retrieval/`, `ragx/`, `federation/` | Validated execution and evidence-aware retrieval; backend/provider capabilities vary |
| Identity and policy | `authn/`, `authz/`, `identity/`, `tenancy/`, `security/`, `policies/`, `privacy/` | Trusted context, permission decisions and data handling |
| Agents and tools | `agents/`, `agentarch/`, `tools_contract/`, `workflows/` | Governed agents, tool schemas and external MCP; annotations are not authority |
| Trust and semantics | `provenance/`, `claims/`, `truth/`, `journal/`, `temporal/`, `aspeii/` | Evidence, semantic changes, action checks and receipts; preserve one authority per record |
| Wisdom and reasoning | `wisdom/`, `reasoning/`, `causal/`, `intelligence/`, `brain/` | Decisions, counsel and reasoning; inference is not observation |
| Optional models | `neural/`, `gnn/`, `embeddings/`, `models/`, `model_management/`, `mlops/` | Profile-gated numerics/models with explicit qualification |
| Reporting and operations | `reports/`, `analytics/`, `dashboards/`, `observability/`, `health/`, `ops/` | User outputs and operational visibility; validate durable backing per service |
| Product/distribution | `catalog/`, `product/`, `marketplace/`, `plugins/`, `licensing/`, `billing/` | Domain extensions and distribution-related surfaces, not automatic commercial clearance |
| Quality/evidence | `verification/`, `qualification/`, `testing/`, `qa/`, `ci/` | Test/evidence mechanisms; inspect verifier strength rather than trusting verdict labels |

This is an orientation map, not an exhaustive list of every package. The [generated inventory](../../docs/generated/README.md) records every in-scope file, Python symbols/imports and route candidates. Use `rg` to trace call sites and registrations; a class that has no runtime path is not automatically a usable feature.

## Runtime Composition

`apps/api/main.py` constructs the persistent runtime; `apps/api/app.py` builds an injected-store query app; `apps/api/extended.py` and route modules add domain surfaces. `apps/worker/main.py` independently creates its store and dispatches jobs. Never assume process globals are shared between them.

Configuration loaders are not uniform: some use `EOIP_CONFIG_DIR`, some explicit relative files. Run from root and inspect loaders before relocating code. Existing overlapping package names need consumer analysis before consolidation, not mechanical renaming.

## Development Contract

Keep business logic in its owning service, graph-specific behavior in adapters, and schemas synchronized with public interfaces. Resolve principal/tenant from trusted context; preserve evidence identity, timestamps and no-upgrade rules. For persistence changes, test interruption/restart/replay/concurrency and recovery rather than only object construction.

Add focused tests under the relevant existing test area and use the applicable requirement IDs. Update affected component guides, deployment/configuration and [migration procedures](../../docs/migration-refactoring-guide.md). Do not import optional GPU/model packages into core startup. Unavailable models/connectors must fail honestly, not substitute synthetic success.
