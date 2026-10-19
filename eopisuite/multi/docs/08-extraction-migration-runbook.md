# Extraction and Migration Runbook

## Non-Negotiable Safety

Work from a recorded source baseline. Preserve dirty changes, current remotes, tags and runtime data. Never run history filtering in the active source checkout. Do not push a full mirror to a new private repository without inspecting its entire history for credentials, customer data and unrelated material. Private visibility does not make leaked secrets safe.

Prefer a reviewed **snapshot extraction with provenance** for mixed frontend/domain slices. Record source repository, commit, original paths, file hashes and transformed paths in `migration/provenance.json`; retain access to the historical repository for investigation. A fresh repository history does not erase original copyright or attribution obligations.

When historical commits are required, use a disposable fresh clone and a reviewed filter plan that includes required renames and dependency paths. Filtering changes commit IDs and may remove signatures; inspect the result and remote configuration before a normal initial push to an empty destination. Never force-push rewritten history into an established destination as a default migration step. Credential exposure requires revocation/rotation as well as any coordinated history cleanup. [GitHub sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

## Phase A: Establish the Baseline

1. Record HEAD, dirty status, enabled features, dependency locks, OS/runtime and deployment profile.
2. Build a route inventory for both `apps/web` and `frontend`, including tab-only workflows and external bookmarks.
3. Record API calls, permissions, domain owner, storage/resources, data shape, errors, keyboard/accessibility behavior and current consumers for each workflow.
4. Run representative existing journeys and known-failure controls against an isolated, reproducible data snapshot.
5. Assign every route/feature one destination and one disposition: reuse, repair, combine, retain or retire after parity.
6. Map original requirement IDs to new owners. Preserve requirements that currently have no implementation.

Inventory columns must include: original path/route, feature ID, owning requirement IDs, new repo, shared dependencies, old/new API contracts, migration of saved state, evidence location, known defects, acceptance depth, rollback and owner. No route can be dropped merely because its component looks duplicated.

## Phase B: Extract Shared UI and Read-Only Pilots

Extract the smallest proven visual tokens/components and shared transport/context interfaces. Do not copy two shell/auth models into every new portal. Remove the alternate frontend's synthetic-admin-on-identity-error behavior before any adoption of that provider. Preserve denied/unavailable states and use existing Lucide icons/accessibility conventions.

For Query and Explorer, move complete vertical slices: route, state, transport usage, renderer, export/security behavior, tests, fixtures and documentation. The backend remains the legacy API in B1. Introduce no new query engine or duplicate graph semantics. Verify saved queries, identifiers, output semantics and deep links before switching gateway routes.

## Phase C: Package Backend Boundaries

| Source set | Destination | Required adaptation before cutover |
|---|---|---|
| `packages/eoip/**`, related platform tests/resources | `eoip-platform` | Clean wheel/resource install; ownership audit; remove application-startup imports |
| `apps/api/**`, API-specific tests | `eoip-core-api` | Package application entry points, preserve middleware/routes, explicit config/resource inputs |
| `apps/worker/**`, dispatch-specific tests | `eoip-ingestion-worker` | Explicit mapping paths, qualified queue/data semantics, retry/restart behavior |
| `apps/mcp/**`, protocol tests | `eoip-mcp-server` | API URL/auth/protocol compatibility; declare minimal dependencies |
| `apps/vscode-extension/**` | `eoip-vscode-extension` | Preserve identity/commands; portable package output; multi-root tests |
| `packages/eoip/cli.py` | `eoip-cli` | Separate thin client first; remove old console entry only after compatibility/deprecation release |
| `reva/**`, REVA tests/tools/docs | `eoip-reva` | Explicit dependencies, wheel discovery, initialization, tenant binding and claimed evidence validation |
| Global requirements/plans/ADRs | `eoip-engineering` | Requirement IDs/history preserved, links rebuilt and authoritative ownership declared |
| Cross-app acceptance/release checks | `eoip-verification` | Run against artifacts and real deployment, not sibling-source imports |
| Orchestration/release metadata | `eoip-suite` | Per-profile compose/config, immutable artifacts, workspace and release locks |

Do not move all `tests/` to one repository. Unit tests follow code; contract tests involve owners and consumers; deployed cross-app tests belong in verification. Curated shared fixtures get versioned hashes and ownership. Raw audit scratch, local credentials, databases, node_modules and `.venv` are never blanket-copied.

`config/` and `schemas/` need a file-level ownership decision. Platform defaults, deployment settings, source mapping templates and tenant secrets have different lifecycles. Assign a single source of truth and an explicit distribution method for each, instead of copying all of them into API and worker repositories.

## Application Namespace Transition

Target Python process packages are `eoip_api`, `eoip_worker` and `eoip_mcp`; preserve `eoip` for platform imports. Package those modules explicitly and update the application images/entry commands in one reviewed change. Temporary compatibility wrappers may retain old module entry points if existing consumers need them, with a removal gate. Do not create several unrelated installed distributions that all provide an ambiguous top-level `apps` package.

Test startup outside repository cwd, from a wheel-installed environment. If a compatibility mode still requires repository-relative assets, label it and keep production cutover blocked until resource ownership is resolved.

## Per-Slice Cutover Checklist

1. Freeze the slice's baseline and announce source-of-truth ownership; do not freeze unrelated development.
2. Produce an import manifest and verify its allowlisted files before committing to the destination.
3. Build and test in isolation; inventory all first- and third-party artifacts/notices.
4. Run old/new parity and negative controls on a fixed snapshot; compare persisted effects where relevant.
5. Add exact component versions to a candidate suite manifest; qualify dependent consumers.
6. Switch only the selected gateway route/client entry behind an explicit rollback decision.
7. Keep old artifacts and compatible route redirects through the agreed observation window.
8. Remove old source only after consumers, bookmarks, saved state and required journeys have verified destinations.

The observation window is an explicit release-owner decision based on actual usage/support obligations, not a fabricated number of days. Emergency rollback routes to the known artifact combination; it does not blindly roll back incompatible data migrations.

## Cross-Repository Change Example

A new query response field starts in the platform/API owner. Publish a backward-compatible contract snapshot and SDK, then update Query and Explorer in separate PRs. Link all PRs through one change ID. Suite CI assembles the candidate combination; old clients must continue to work or the unsupported combination must be rejected clearly. Only after verified adoption can the old contract be deprecated. There is no atomic Git merge across repositories.

## Retirement Gate

No old frontend, preview backend, route or package entry is removed until all owned requirements, actual consumers, saved links/state, operational procedures and rollback paths have been accounted for. Retain historical evidence with its original profile/source identity; do not relabel a legacy test run as evidence for the extracted artifact.
