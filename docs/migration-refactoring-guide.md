# Migration, Refactoring and New Development

This guide applies to application changes, storage/schema migrations, new connectors and the proposed suite split. It is a procedure, not an assertion that a universal migration engine exists.

## Before Changing Code

1. Check the working tree and preserve unrelated work. Read the component README and owning requirements.
2. Identify the actual deployment entry point and all consumers, including both frontends, MCP, VS Code, worker, scripts and tests.
3. Trace one behavior from client through route, principal/policy, domain service, storage, jobs/events and response. Record failure and unavailable states.
4. Identify data ownership and whether state is graph-backed, file-backed or process-local. List external effects separately.
5. Define a falsifiable acceptance check and capture baseline behavior on a named dataset/profile.
6. Record the proposed contract change, backward-compatibility obligation, rollout order, rollback limits and owner decision.

## Dependency and Ownership Rules

- Keep graph-vendor code inside adapters; application logic uses the graph contract.
- Reuse Pydantic/schema contracts and existing policy/evidence boundaries. Avoid duplicate approvals, warrants, receipts or query engines.
- Do not assume similarly named packages are interchangeable: `ingest`/`ingestion`, `ontology`/`validation`, `models`/`model_management`, and other overlapping domains have distinct call sites. Inspect imports and registered routes before consolidation.
- Prefer explicit injection/composition over adding more global runtime state. A facade or package move alone does not fix persistence or tenant isolation.
- Do not add heavy neural/GPU dependencies to the core installation. Preserve optional tier boundaries and licensing gates.
- Keep preview shims and legacy routes until their consumers have a verified replacement.

## API or Contract Change

Capture the deployed OpenAPI and actual accepted payloads; source decorators alone omit prefixes/dynamic registrations. Compare field semantics, defaults, unknown-field behavior, error codes, pagination, result bounds, idempotency and authorization. Add a compatibility adapter when required. Update both frontend clients and MCP/extension consumers affected by the change.

For additive fields, test old clients against new responses. For removal/renaming, publish a supported deprecation and version transition. Retain stable canonical IDs and evidence references. A translated schema must not silently upgrade confidence, authority or fact status.

## Data and Schema Migration

1. Inventory the exact stores and versions. Stop or coordinate every writer, not only the web UI.
2. Produce and verify a backup using the [operations procedure](operations-runbook.md).
3. Prefer an expand/backfill/validate/contract sequence where feasible. Define migration IDs, restart checkpoints and safe retry behavior.
4. Test empty, existing, duplicate, malformed, interrupted and partially migrated states in an isolated target.
5. Compare entity/edge identities, constraints, provenance, timestamps, tenant scope and permissions; raw row counts alone are insufficient.
6. Validate derived indexes, caches, reports, change consumers, leases and repair queues. Rebuild projections from authoritative records where supported.
7. Cut over only after the agreed evidence gate. Preserve an explicit recovery or forward-repair path.
8. Remove old representations only after all consumers have migrated and retention requirements permit it.

Changing `EOIP_GRAPH_BACKEND` is connection selection, not data migration. There is no basis to promise identical transaction, query or export semantics across every adapter. Qualify each selected backend.

Cross-store writes need a proven recovery protocol; do not call an SQL transaction plus a remote graph request atomic. Approvals and dispatch must preserve single consumption, revision binding, revocation and replay safety throughout migration.

## Frontend and Suite Refactoring

The [suite architecture plan](EOIP-suite-architecture-plan.md) is proposed, not current deployment. Start with inventory/reconciliation of `apps/web` and `frontend`. Select a single owner per workflow and verify both versions before extracting shared packages.

Preserve deep links, source/entity IDs, permission failures, loading/empty/error states, accessibility and export behavior. Test refresh, back/forward navigation, session expiry and tenant switches. A new application path does not establish a security boundary. Keep same-origin customer apps separate from privileged operator and untrusted plugin origins when required.

Extract read-only Query/Explorer workflows first after identity/shell foundations. Keep the engine headless. Introduce independently deployed services only when owned state, safe delivery semantics, operational responsibility and a concrete scaling/security reason exist.

## New Capability Checklist

| Area | Required review |
|---|---|
| Requirement | Stable ID, explicit behavior, owning programme and acceptance criteria |
| Interface | Registered route/tool/job, schema, supported profile and honest unavailable state |
| Security | Trusted identity/tenant, object access, input/egress controls, secrets and redaction |
| Storage | Authority, durability, concurrency, migration, retention and restore |
| Reliability | Retry/idempotency, cancellation, timeout, replay and observable failure |
| UX | Discoverable workflow, errors, keyboard/reduced-motion support and layout checks |
| Evidence | Real boundary execution, negative cases, independent effects and verifier |
| Delivery | Optional dependencies, notices, configuration, deployment and support procedure |

## Pull Request and Team Handover

Describe behavior changed, requirements affected, source of truth, compatible versions, migrations, secrets/configuration changes, exact commands/results, tests not run, rollback limitations and documentation updates. Do not hide known failures or mark tests skipped for missing infrastructure as passes.

Handover includes a reproducible local run, architecture walkthrough, key flows, dependency/config inventory, durable-state map, active decisions, open blockers, release evidence and recovery exercise. Assign maintainers through the team's actual ownership process; this guide does not invent staff or service-level commitments.
