# Dependency-Ordered Implementation Backlog

Status of every work package below at publication: **not executed by this documentation task**. This is a build plan, not a migrated-suite completion ledger. Preserve the existing `SUITE-WP-*` and programme IDs; the `MULTI-*` IDs identify additional multi-repository work.

## Wave 0: Decisions and Reproducible Baseline

### MULTI-001: Organization and Ownership

- Depends on: actual administrator/repository-creation authority in the user-confirmed organization `AvyukthiAI`; the handle is no longer pending.
- Implement: private pilot repos, named maintainers, access/review policies, package-consumer permissions and recovery contacts per guide 03.
- Deliver: repository URLs, permission matrix, validated policy settings and decision register.
- Verify: authorized clone succeeds; denied identity cannot clone/publish; protected-branch policy blocks an invalid change.
- Exit: no invented accounts/owners, no broad automation credentials, no unresolved licensing/visibility default.
- Maps to: `SUITE-WP-02`.

### MULTI-002: Baseline, Ownership and Route Inventory

- Depends on: none for local read-only work; owner acceptance before source moves.
- Implement: both frontend route/tab inventories, import/resource graphs, current startup/profile map and requirement-to-owner mapping.
- Deliver: source commit and dirty-state record; capability dispositions; known failures; old behavior evidence.
- Verify: every discovered route/tab/entry point has a destination or explicit retained owner; a second pass finds no unexplained omission.
- Exit: no silent feature loss; existing incomplete requirements remain open.
- Maps to: `SUITE-WP-01`, `SUITE-WP-02`.

### MULTI-003: Workspace and Bootstrap Tooling

- Depends on: MULTI-001 for remote cloning; can test path logic with disposable local repositories first.
- Implement: validated repo manifest, safe clone/inspect tool, local/shared workspaces, environment preflight, profile selection and scoped tasks.
- Deliver: actual scripts/configuration from guides 04-05, with tests for missing tools, access denial, wrong remote, dirty existing clone, invalid path and interrupted clone.
- Verify: one VS Code window opens independent repositories; rerunning preserves work; no parent Git repo/nested clone is created.
- Exit: clean-machine documented setup succeeds for the selected OS profile; empty apps are not advertised as runnable.
- Maps to: `SUITE-WP-02`, `SUITE-WP-05`.

## Wave 1: Foundations and Real Pilot

### MULTI-004: Shared UI and Contract Packaging

- Depends on: MULTI-002, repository ownership from MULTI-001.
- Implement: selected UI/shell components, typed transport boundary, contract generation/drift checks, exact package publication and isolated consumer builds. Create `eoip-sdk` here for the shared generated/client foundation; MULTI-009 later qualifies its broader channel distribution, not its first availability.
- Deliver: package contents, notices, dependency/peer contracts, registry permissions, published candidate versions and two consumer builds.
- Verify: no sibling-source imports, duplicate React runtime or secret-bearing package files; install from a clean consumer.
- Exit: coherent accessible shell and real API results, not mock-only reusable components.
- Maps to: `SUITE-WP-03`, `SUITE-WP-05`.

### MULTI-005: Gateway and Trusted Session

- Depends on: baseline; actual identity-provider/profile decision before session integration.
- Implement: local R1 routing separately from R2 session boundary, catalog validation, base paths, error/disabled behavior, operator trust separation and revocation-aware context.
- Deliver: gateway artifact, explicit auth adapter, config model, readiness, request correlation and tests.
- Verify: identity failure cannot synthesize admin; logout/expiry/revocation deny access; deep links work; tenant switch discards stale in-flight data; direct operator route denied.
- Exit: two independent app builds use a real reviewed session path. R1 token mode alone cannot close this package.
- Maps to: `SUITE-WP-04`, `SUITE-WP-05`.

### MULTI-006: Query and Explorer Extraction

- Depends on: MULTI-002 and MULTI-004; release requires MULTI-005.
- Implement: real Query/Explorer slices, preserved IDs/bookmarks, bounded queries, graph/table states, cancellation and available-language/capability controls.
- Deliver: separate app repos/builds, portable source/resource dependencies, parity report, old-to-new route map and rollback artifacts.
- Verify: fixed data yields compatible old/new results and policy refusals; base-path refresh and mobile/keyboard use work; rollback changes only the selected app.
- Exit: no duplicate query engine, no regression hidden by screenshot-only evidence.
- Maps to: `SUITE-WP-06`.

### MULTI-007: Suite Home and Catalog

- Depends on: MULTI-004, MULTI-005; can show unavailable entries while features remain incomplete.
- Implement: server-reviewed installed/qualified/entitled/authorized availability, safe app links and shared context.
- Deliver: catalog schema, validation, launcher and disabled/incompatible states.
- Verify: unauthorized/missing modules cannot be entered through direct APIs; absent optional apps do not break Query/Explorer.
- Exit: listing a repo does not turn it into an enabled product.
- Maps to: `SUITE-WP-03`, `SUITE-WP-05`.

## Wave 2: Runtime Packaging and First Suite Release

### MULTI-008: Platform, API and Worker Separation

- Depends on: MULTI-002; implement after the UI pilot establishes value, unless a concrete packaging blocker requires earlier work.
- Implement: platform wheel/resources, separate API/worker distributions and images, explicit configuration/resource loading and unchanged qualified state ownership.
- Deliver: clean install artifacts, scoped tests, startup/health/shutdown contracts and deployment migration plan.
- Verify: startup outside source cwd; API-to-worker ingestion survives process restart; no hidden legacy import; queue effects and retries independently observed.
- Exit: compatibility with existing graph/authority state proven; no unsupported distributed-worker claim.
- Maps to: `SUITE-WP-05`, `SUITE-WP-15`.

### MULTI-009: MCP, Extension, CLI and SDK Channels

- Depends on: published contracts and relevant runtime artifacts; new identity behavior depends on MULTI-005.
- Implement: move existing MCP/extension, publish SDKs, extract thin CLI without conflicting console-script ownership, preserve protocol and command IDs.
- Deliver: wheel/image/VSIX/npm artifacts with separate tests and support matrix.
- Verify: real MCP discovery/invocation; extension host multi-root navigation and denied file paths; API error/refusal propagation; clean CLI/SDK install.
- Exit: no second extension or direct database shortcut; remote identity only claimed when separately verified.
- Maps to: `SUITE-WP-10`.

### MULTI-010: Configuration and Organization Administration

- Depends on: MULTI-005, API contracts and required authority services.
- Implement: effective config/revision/diff/validation, promotion/rollback, memberships/roles and scoped entitlement views.
- Deliver: separate apps and owning domain API work; no portal-local authoritative state.
- Verify: concurrent edits conflict correctly; invalid settings denied; revoked access takes effect; tenant admin cannot become platform/database operator.
- Exit: state changes and rollback independently verified after restart.
- Maps to: `SUITE-WP-07`.

### MULTI-011: Database Operations

- Depends on: restricted operator trust boundary and persistence ownership.
- Implement: authorized diagnostics, backend capabilities, controlled maintenance and isolated backup/restore workflows.
- Deliver: separate restricted app, operational procedures, privileges and reconciliation gates.
- Verify: restore to isolated target, compare logical contents/authority state, reject wrong target and unauthorized user; no raw-console bypass.
- Exit: no restore overwrites the only source and no replay of consumed approvals.
- Maps to: `SUITE-WP-08`.

### MULTI-012: Reporting and Analytics

- Depends on: trusted identity, supported data contracts and qualified job storage.
- Implement: definitions, filters, schedule lifecycle, bounded rendering jobs, immutable artifact metadata and download checks.
- Deliver: report portal and domain/worker changes; snapshots, policy/template/query versions recorded.
- Verify: worker/scheduler restart, output content comparison, revoked downloader refusal, stale/partial data labels and bounded resource use.
- Exit: no generated sample output counted as a real scheduled report.
- Maps to: `SUITE-WP-09`.

### MULTI-013: Coordinated Releases and Independent Verification

- Depends on: first candidate component artifacts; build this capability alongside Wave 1, not only at the end.
- Implement: reusable CI, candidate lock validation, artifact assembly, real deployment tests, retained evidence, approvals and rollback selection.
- Deliver: complete tested release manifest and qualified profile matrix.
- Verify: broken test, incompatible contract, tampered/missing evidence and undeclared artifact all block release.
- Exit: seven initial portals plus existing MCP/extension channels only marked qualified to their demonstrated feature scope.
- Maps to: `SUITE-WP-05`, `SUITE-WP-14`.

## Wave 3: Data and Governed Intelligence

| Work package | Repositories | Dependencies | Required observed exit |
|---|---|---|---|
| MULTI-014: integration, ontology, catalog | APP-08/09/10, platform/worker | Identity, contracts, qualified connector/job/semantic boundaries | Real source -> mapping -> ingestion -> provenance/quality -> query; denied/failed semantic release and successful governed change |
| MULTI-015: REVA packaging and assurance integration | `eoip-reva`, API, Governance, verification | Explicit clean packaging, kernel lifecycle, trusted tenant binding, evidence policy | Health versus real readiness distinguished; negative authority cases and evidence tamper/staleness refusal; no inherited unverified completion ledger |
| MULTI-016: governance, automation and wisdom | APP-11/12/13, platform, REVA as qualified | Existing ASPEII/CIP/IP/WG prerequisites | Revoked/expired approval cannot dispatch; actual effects match receipts; decision/outcome/counsel semantics pass original gates |
| MULTI-017: optional Model Lab | APP-14, optional runtime packages | Existing Graph Neurons/other model gates | Reproducible qualified datasets, anti-stub controls, calibration, abstention and resource/offline behavior |

These correspond to `SUITE-WP-11` and `SUITE-WP-12`. Original programme requirements are not weakened to fit the new repository layout.

## Wave 4: Operations, Ecosystem and Distribution

| Work package | Scope | Exit |
|---|---|---|
| MULTI-018 | Operations and Developer portals | Real incident diagnosis, traces, API/MCP/webhook contracts and safe developer credentials |
| MULTI-019 | Private Extension Catalog | Verified package provenance, compatibility, install/rollback, permissions, quarantine and revocation |
| MULTI-020 | Private Fleet Console and distribution | Customer-consented support access, approved entitlements, exact deployed-version inventory, hosted/installed/offline qualification |
| MULTI-021 | Legacy retirement and selective service extraction | No unowned consumer/feature; migration and recovery proven; measured reason before adding services |

These correspond to `SUITE-WP-13` through `SUITE-WP-15`. Do not create billing integrations, paid subscriptions or externally published extensions merely because their future repo exists.

## Coding-Agent Work Order

Every task must state permitted repositories, baseline commits, owning requirements, exact behavior, dependency versions, migration effects, tests/evidence depth, rollback and out-of-scope work. Begin with MULTI-002 and confirmed parts of MULTI-001/003. Never start all application scaffolds as a substitute for completing a vertical slice.

Estimate effort after baseline/resource findings; no calendar, staffing or scale numbers have been invented. Block only the work that needs an unresolved decision, while progressing independently safe inventory, packaging or tests.
