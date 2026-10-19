# EOIP / KnowGridFlow Application Suite Plan

Date: 2026-10-18

Status: Proposed architecture and migration roadmap. This document does not authorize a rewrite, certify existing functionality, or replace the acceptance criteria in the existing programme requirements.

## 1. Recommendation

Turn EOIP into a **suite of focused applications on a shared knowledge and intelligence platform**.

Keep one repository initially. Give each application a clear purpose, owned screens, build artifact, permission boundary, and release contract. Share the engine, domain services, identity, design system, API contracts, and evidence infrastructure. Introduce additional backend processes only where security isolation, workload scaling, deployment needs, or team ownership justify them.

Three different separations must not be confused:

| Separation | Meaning | Recommended timing |
|---|---|---|
| Application separation | A focused user experience with its own entry point and build | Start here, after the foundation and baseline gates |
| Service separation | Independently deployed backend with owned state and operational responsibility | Selectively, after domain and persistence boundaries are proven |
| Repository separation | Independently managed source repository, CI, releases, and dependency distribution | Later, only for a concrete ownership or distribution need |

A suite does not require a database for each portal, a login system for each portal, or a backend microservice for every screen. Independent builds are useful even when several static applications are served by the same web server.

**First suite release:** Suite Home, Knowledge Explorer, Query Workbench, Configuration Center, Organization Administration, Database Operations, and Reports & Analytics. Keep the existing MCP server and VS Code extension as suite clients. Release this set incrementally, not in one large replacement.

**Longer-term catalog:** 18 browser-facing application areas, four developer/machine channels, and a shared headless platform. The catalog below is a destination, not a direction to create 22 deployments immediately. Suite Home is the launcher and shared experience; specialist applications can begin as owned modules before independent packaging is worthwhile.

## 2. What Exists and What This Review Establishes

This is a targeted source and architecture inspection, not a full runtime audit. No application tests, production deployments, or acceptance journeys were run for this planning task. Existing files establish migration candidates, not completed features.

| Observed foundation | Inspected source | Implication for the suite |
|---|---|---|
| Authenticated API composition, graph store, queue, source registry, audit and agent setup | [API factory](../apps/api/main.py) | Refactor composition into owned modules gradually; preserve the public API during portal extraction |
| Shared graph/query sub-application | [Query application](../apps/api/app.py) | The engine is already separable from a particular portal; do not duplicate query logic in new apps |
| Separate worker entry point and file-backed job queue | [Worker](../apps/worker/main.py), [jobs](../packages/eoip/jobs.py) | Retain the supported local profile; do not infer multi-host durability from separate containers |
| Read-oriented MCP facade using a configured deployment token for API calls | [MCP](../apps/mcp/main.py) | Retain local behavior; design authenticated per-principal delegation before SaaS/multi-tenant exposure |
| Existing separately packaged read-only VS Code extension | [Extension manifest](../apps/vscode-extension/package.json) | Evolve this client, not a second extension |
| React/Vite application with shared shell and API client | [Web manifest](../apps/web/package.json), [shell](../apps/web/src/app/shell/WorkspaceShell.jsx), [navigation](../apps/web/src/app/navigation.ts) | Reuse tested conventions where suitable; break out destinations by workflow |
| Studio mixes schema, query, connectors, mapping, pipelines and systems | [Studio](../apps/web/src/studio/Studio.jsx) | Split into Query Workbench, Ontology Studio and Data Integration Studio |
| Admin combines access, connectors, ingestion, recovery, quality and telemetry | [Administration](../apps/web/src/admin/index.jsx) | Separate tenant administration from data engineering, governance and infrastructure operations |
| A second substantial TypeScript frontend has its own shell, routing and API client | [Alternate frontend](../frontend/src/App.tsx), [manifest](../frontend/package.json) | Compare both implementations before choosing components; do not discard either by assumption |
| Alternate frontend authentication synthesizes a bootstrap-admin UI principal when `whoami` fails | [Auth provider](../frontend/src/lib/auth.tsx) | Remove this fallback before adopting it into suite identity. This source observation is not a finding of demonstrated backend privilege escalation |
| Deployment-token connection flow in the other frontend | [Connection](../apps/web/src/app/shell/Connection.jsx) | A shared browser session and tenant-grant flow are prerequisites for seamless multi-app navigation |
| Default Compose and web CI target `apps/web` | [Compose](../deploy/docker-compose.yml), [CI](../.github/workflows/ci.yml) | Preserve that deployment path until a verified replacement is registered |
| Preview backend delegates to the real API with development defaults | [Backend shim](../backend/server.py) | Do not mistake the shim for a second domain backend or deploy its development defaults as a suite production profile |
| Optional numerical foundation and unqualified advanced neural tiers | [Neural installation](install-neural.md) | Model Lab is optional; graph/query functionality must work without neural packages |
| Limited existing CLI | [CLI](../packages/eoip/cli.py) | Suite login, deployment and evidence commands would be extensions, not already available commands |

The current [README](../README.md) explicitly separates code existence from production qualification. Follow that policy. Older architecture descriptions and screen labels must not override observed runtime evidence.

### 2.1 Reconcile the two frontends first

Create a route-by-route inventory for `apps/web` and `frontend`. Record screen purpose, APIs called, permissions, state handling, accessibility, visual components, automated coverage, actual deployment consumers, and observed runtime results.

For each capability choose one outcome: reuse unchanged, extract and repair, combine non-duplicated behavior, retain temporarily, or retire after parity. A visually richer screen is not automatically the authoritative implementation. A screen in default Compose is not automatically complete either.

Do not introduce a third independent design system, API client, auth model, or implementation of the same business screen. Extract shared foundations from the two existing implementations through an explicit decision record. Preserve active preview/supervisor entry points until their users have a replacement.

## 3. Application Catalog

Routes below are proposed target roots, not claims that these endpoints exist. Preserve exact domain API names and required routes from existing specifications unless an approved compatibility decision changes them. The fleet application uses a private operator origin; its `/fleet` path is not a tenant-origin route.

| ID | Application | Primary user and purpose | Target root | Delivery |
|---|---|---|---|---|
| APP-01 | Suite Home | Everyone: entitled apps, recent work, approvals, search and workspace context | `/suite` | First suite release |
| APP-02 | Configuration Center | Configuration managers: environment and tenant settings, promotion, validation and rollback | `/configure` | First suite release |
| APP-03 | Organization Administration | Customer administrators: organizations, workspaces, members, roles and entitlements | `/admin` | First suite release |
| APP-04 | Database Operations | Authorized database operators: storage, indexes, backup, restore and migrations | `/database` | First suite release, restricted |
| APP-05 | Query Workbench | Analysts and engineers: governed queries, plans, results and saved queries | `/query` | First extraction pilot |
| APP-06 | Knowledge Explorer | Knowledge users: graph, entities, provenance, impact, temporal context and grounded answers | `/explore` | First extraction pilot |
| APP-07 | Reports & Analytics | Analysts and leaders: dashboards, report schedules, exports and reproducibility | `/reports` | First suite release |
| APP-08 | Data Integration Studio | Data engineers: connectors, discovery, mappings, ingestion, pipelines and reconciliation | `/integrate` | Next expansion |
| APP-09 | Ontology Studio | Ontology engineers: types, vocabularies, constraints and governed semantic releases | `/ontology` | Next expansion |
| APP-10 | Data Catalog & Quality | Data stewards: discovery, lineage, ownership, quality, freshness and resolution | `/catalog` | Next expansion |
| APP-11 | Agent & Automation Studio | Automation engineers: intents, agents, delegation, workflows and supervised execution | `/automate` | After action-safety foundation |
| APP-12 | Governance & Evidence | Security reviewers and auditors: policies, approvals, claims, warrants and verification | `/governance` | Safety foundation work starts early; full app follows |
| APP-13 | Wisdom & Decisions | Decision owners: rationale, precedents, outcomes, lessons, counsel and review | `/wisdom` | After cross-programme dependencies |
| APP-14 | Model & Evaluation Lab | ML engineers: model profiles, datasets, calibration, evaluations and promotion | `/models` | Optional, qualified profiles only |
| APP-15 | Operations & Reliability | Operators: health, jobs, incidents, traces, capacity and recovery coordination | `/operations` | Expand after initial suite |
| APP-16 | Developer & Integration Hub | Developers: API contracts, SDKs, MCP tools, webhook subscriptions and sandboxes | `/developers` | Expand after stable contracts |
| APP-17 | Extension & Solution Catalog | Tenant administrators and publishers: approved connectors, domain packs and templates | `/extensions` | Later; private catalog before marketplace |
| APP-18 | Commercial & Fleet Console | Product operators: deployments, entitlements, metering, upgrades and support access | Private `/fleet` | Later; separate operator security plane |

### 3.1 Required boundaries for the applications you named

**Configuration Center:** Own schema-driven settings, effective-value inspection, source/override precedence, secret references, validation, draft comparison, approval, environment promotion, reload/restart requirements and rollback. User appearance preferences remain shared user settings. This app does not own users, physical database tables or business approval records. Configuration writes call the owning domain service and cannot bypass its invariants.

**Organization Administration:** Own tenant/workspace lifecycle, memberships, service accounts, role assignments, SSO integration settings, quotas, customer-visible entitlements and organization audit views. Tenant administrators do not automatically receive platform-operator or database privileges. Account deletion is a governed lifecycle operation, not a UI-only delete.

**Database Operations:** Own database connectivity diagnostics, backend capability inspection, physical indexes, capacity, snapshots, restore drills, migration jobs and controlled maintenance. Reuse vendor administration tools where appropriate, with separate authentication and network restrictions; do not blindly embed or expose Hubble. Ontology meaning changes belong to Ontology Studio. Arbitrary SQL/Gremlin/vendor-console writes must not become a bypass around graph validation, warrants or approvals. Exceptional maintenance requires explicit privilege, audit and reconciliation before serving affected data.

**Query Workbench:** Own saved queries, parameters, supported language selection, explain/plan, cancellation, limits, result tables/graphs, query history and export handoff. Show only languages actually supported by the active backend and policy. Initially read-only. Any later mutation mode must use the same governed command path as every other client. Query history and saved credentials must not leak between tenants or principals.

**Reports & Analytics:** Own report definitions, dashboards, schedules, delivery configuration and export history. Heavy exports execute as jobs. Record the data snapshot/time, filters, policy version, template and query versions. Recheck permission at execution and download, not only when a schedule was created. Present stale or partial materializations honestly. Never turn access to a report URL into permanent access to restricted data.

**Core Engine and Portal:** Separate the headless core from its UI. The core owns graph contracts, validated mutations, query execution, ontology enforcement, provenance, temporal interpretation and public service interfaces. Knowledge Explorer is its main human-facing portal, not the owner of the engine. Query, reports, agents, MCP and VS Code use the same governed core.

**VS Code Plugin:** Keep the existing extension as the IDE channel. Improve authentication, tenant/workspace selection, source navigation, code context, query results, diagnostics and links to the right suite app. Keep read-only behavior until explicit action-safety requirements are met. Store secrets using the host's secure storage and maintain workspace path restrictions.

**MCP:** Treat MCP as a protocol gateway, not a replacement backend or a portal. The Developer Hub provides its management UI. Keep tool contracts, allowed effects, limits, tenant authorization and revocation consistent with REST. Tool annotations alone do not grant authority. Do not claim current deployment-token behavior is a multi-user OAuth architecture.

### 3.2 Additional application scopes and build gaps

The following are candidate expansion boundaries. Existing modules or screens may provide a starting point; each full application remains unverified until its end-to-end release gates pass.

| Application | Initial useful scope | Work to qualify or build |
|---|---|---|
| Data Integration Studio | Source registry, connector onboarding, schema discovery, mappings, jobs and DLQ | Secret lifecycle, connector capability matrix, incremental sync, idempotency, rate limiting, resumability, schema drift and independent reconciliation |
| Ontology Studio | Schema and vocabulary editing, validation, semantic diffs | Versioned drafts, dependencies, review, compatibility assessment, migration/revalidation, rollback and governed publication; no autonomous schema promotion |
| Data Catalog & Quality | Entity/dataset ownership, lineage, freshness and quality findings | Cross-store catalog consistency, issue assignment, quality rules, entity-resolution review, freshness SLAs and repair integration |
| Agent & Automation Studio | Agent registry, intents, task views and dry-run proposals | Durable workflows, attenuated delegation, budgets, approval binding, revocation, execution receipts, cancellation and effect verification |
| Governance & Evidence | Policy review, audit browsing and evidence inspection | Authoritative approval lifecycle, provenance challenges, no-upgrade checks, retention/hold/purge, independent verification and tamper detection |
| Wisdom & Decisions | Decision traces, precedent search and outcome views | Decision-time reconstruction, outcome attribution, lesson review, calibrated counsel, exceptions, values, replay and no unsupported promotion from prediction to fact |
| Model & Evaluation Lab | Installed model/profile inventory and evaluation results | Reproducible datasets/splits, baselines, anti-stub probes, resource controls, drift, calibration, promotion/rollback and offline packaging |
| Operations & Reliability | Service health, worker status, traces and alert views | Cross-service correlation, SLOs, incident workflows, restore exercises, runbooks, capacity and deployment-safe recovery |
| Developer & Integration Hub | API explorer, SDK examples and MCP tool inventory | Versioned client generation, webhook delivery inspection, credential scopes, compatibility checks, isolated test tenants and connector conformance |
| Extension & Solution Catalog | Private catalog of vetted connector/domain/report packages | Signed manifests, capability permissions, dependency compatibility, quarantine, install rollback, vulnerabilities and provenance |
| Commercial & Fleet Console | Deployment and entitlement inventory | Metering reconciliation, subscription integration, offline entitlement lifecycle, rollout rings, supported-version inventory and consent-bound support sessions |

### 3.3 Additional channels, not more web portals

| ID | Channel | Role |
|---|---|---|
| CH-01 | Existing VS Code extension | IDE-native graph/context consumption and suite deep links |
| CH-02 | Existing MCP server | Governed machine access for compatible AI clients |
| CH-03 | Extended EOIP CLI | Automation, diagnostics, configuration import/export, migration and verification commands when implemented |
| CH-04 | Versioned SDK/API/webhook interface | Python/TypeScript integrations and event consumers, with authenticated delivery and compatibility contracts |

Do not initially create separate applications for notifications, help, appearance, collaboration comments, branding or approvals. Implement reusable experiences with domain ownership: for example, an approval inbox links to the authoritative approval in Governance, and a report annotation references the report instead of copying its data. Dedicated collaboration or industry applications can follow demonstrated user demand.

## 4. Shared Platform and Ownership

Use logical domain boundaries first. The table does not mandate one process per row.

| Platform area | Owns | Initial deployment direction |
|---|---|---|
| Identity and access | Authenticated identity, tenant grants, service identity, policy enforcement and revocation | Shared backend module plus reviewed identity-provider integration |
| Configuration and capabilities | Versioned configuration, effective settings, supported capabilities and module activation | Shared backend module; deployment automation applies infrastructure changes |
| Knowledge core | Graph adapters, canonical entities, queries, ontology validation, provenance and temporal access | Existing API/domain packages with explicit module interfaces |
| Acquisition and jobs | Connector work, schedules, checkpoints, reconciliation and job lifecycle | Existing worker; split worker pools only after durable coordination gates |
| Trust and action control | Claims, warrants, approvals, delegation, leases, budgets, certificates and effect receipts | Shared authoritative domain services; keep atomic authority checks together |
| Analytics and reporting | Query-backed reports, projections, schedules and export artifacts | API module and jobs; separate worker when contention is measured |
| Intelligence and wisdom | Retrieval, agents, neural inference, counsel and lessons | Optional modules; isolated model runtime when required by resources/security |
| Operations and distribution | Telemetry, release manifests, support bundles, update and restore coordination | Shared instrumentation plus restricted operator services |

### 4.1 Dependency rules

1. Browser apps and external clients call supported APIs. They do not import backend business logic or connect directly to graph/authority databases.
2. Backend applications compose domain modules. Domain modules must not import browser apps or depend on `apps.api` initialization to function.
3. Shared UI packages contain design components, shell behavior and typed client infrastructure, not a second business engine.
4. Cross-domain calls use owned contracts. Direct mutation of another module's internal tables, JSON files or state objects is prohibited in the target architecture.
5. The knowledge core must not depend on a particular portal, cloud billing integration, marketplace, GPU package or optional model provider.
6. The same approval, policy, warrant, lease and receipt must retain one authoritative identity across apps. New portals present those records rather than manufacture their own equivalents.
7. Add import-boundary checks and contract tests incrementally; initially report existing violations, then block new ones and remove old ones per migration package.

### 4.2 Data ownership and durable state

Retain graph storage behind `GraphStore`. Use owned repositories for transactional metadata, durable jobs and authority records. Portals may share physical infrastructure while domain ownership and access controls remain separate.

The [ASPEII implementation plan](../aspeii-implementation-plan.md) already specifies SQLite for its one-host authority profile and PostgreSQL for its multi-worker/SaaS authority profile. Reuse that decision and its required concurrency semantics; do not create an unrelated suite authority database. This does not assert those repositories are implemented today.

| Data | Authority | Other applications consume through |
|---|---|---|
| Canonical graph and provenance | Knowledge core and graph adapter | Governed query/entity APIs |
| Ontology releases | Ontology domain | Versioned schema/capability APIs and release events |
| Configuration revisions | Configuration domain, with owning-domain validation | Effective configuration APIs |
| User and tenant grants | Identity/access domain | Trusted session/principal context and authorization checks |
| Approvals, leases, budgets, action state | Existing cross-programme authority owner | Atomic domain commands; reference IDs in other records |
| Source registry, checkpoints and jobs | Acquisition/job domain | Job and connector APIs |
| Decisions, outcomes and lessons | Wisdom domain, referencing shared warrants/actions | Authorized Wisdom APIs |
| Reports and derived analytics | Reporting domain | Permission-checked artifacts and projections |
| Evidence bundles and attachments | Owned artifact store with retention and access policy | Authorized download/verification APIs |

Do not claim atomicity across SQL authority and an external graph database without a proven protocol. Use the existing programme's outbox/CDC or explicitly approved recoverable mutation protocol, with pending/failed states, effect verification and reconciliation. A failed publish is not a successful graph mutation. A stale reporting projection must not grant access after revocation.

Keep the current file-backed local worker profile restricted to its qualified topology. Moving its JSON files to a shared network volume does not qualify distributed execution. Multi-worker dispatch needs durable claims, leases/fencing, crash recovery, deduplication, bounded retries and independently observed effects.

### 4.3 Events and read models

Reuse the existing cross-programme event ownership and the canonical `kgf.graph.changed` stream where required. Do not introduce a second graph-change bus merely for the suite.

New event contracts must identify schema version, event ID, tenant, subject/revision, producer, timestamp and correlation/causation IDs, consistent with existing required fields. Consumers must tolerate duplicates, bound retries, isolate poison events, record checkpoints and support replay. Ordering is defined per affected subject or aggregate; global order is not assumed.

Reporting and global search may use derived read models. Their UI shows freshness and partial-result states. Authorization remains checked against authoritative grants. Cache keys include tenant, workspace, principal/permission context and relevant data/policy revision; invalidate or discard cached sensitive results on scope change and revocation.

## 5. Identity, Trust Zones and Suite Experience

### 5.1 Authentication and isolation

For the first browser suite, use same-origin path routing for customer applications with a shared server-side session boundary. The proposed web-session adapter authenticates through a reviewed identity-provider integration and holds upstream credentials server-side. The browser receives a Secure, HttpOnly session cookie in deployed HTTPS environments. State-changing requests require CSRF and origin protections; logout, expiry and revocation must invalidate active sessions. Define explicit local-development exceptions rather than weakening the deployed default.

Do not implement a new password database or authentication protocol solely for the suite. Select an identity solution supporting the customer-installed/offline profile as well as SaaS. Confirm the exact integration in an ADR. The existing API-token path can remain an explicitly limited local/bootstrap compatibility mode, not a shortcut to shared SaaS identity.

Tenant/workspace selection expresses requested context only. The server resolves and validates grants from authenticated identity on every operation. Never trust arbitrary `X-Tenant-Id`, `X-Principal`, role fields, or navigation visibility as authorization.

Same-origin portals are not security-isolated from each other by their URL paths. Untrusted plugins, infrastructure control, and the operator fleet console must not rely on path separation for isolation. Use separate origins, credentials and network/policy boundaries where that isolation is required. Do not share a parent-domain auth cookie across untrusted applications.

Database Operations should be served on a restricted operator surface for hosted deployments. A tenant-facing database page can show authorized diagnostics without credentials or physical control. Customer-installed operators may enable the full surface explicitly under a separate privilege and authentication policy.

For remote MCP, validate tokens intended for the MCP resource and obtain properly scoped downstream authority without blindly forwarding the incoming bearer token. Preserve the requesting principal and tenant in authorization and audit. Pin the supported protocol revision and test it; the referenced MCP draft guidance is not a version pin. See the official [MCP security guidance](https://modelcontextprotocol.io/docs/draft/tutorials/security/security_best_practices).

### 5.2 One coherent experience across many apps

Share the application switcher, authenticated context, environment banner, breadcrumbs, global search, notification entry, accessibility behavior, theme and consistent error presentation. Each app has a focused local navigation menu. Do not show all 18 applications as permanent sidebar items.

Preserve entity, query, job, decision and evidence IDs in deep links. Do not put credentials, entire datasets or sensitive prompts in URLs. Cross-app navigation passes references and rechecks access at the destination. Protect return URLs against open redirects. Workspace switches cancel outstanding requests and discard data from the previous security context.

Reuse the existing React/Vite investment and Lucide icon system. Select one token and component contract after the frontend comparison; do not force a complete CSS/framework rewrite as part of the split. Support keyboard use, visible focus, reduced motion, empty/error/denied/unavailable states and responsive information density. Target WCAG 2.2 AA and verify complete journeys, not only individual components. See [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/).

### 5.3 Capability and application manifests

Introduce one server-reviewed application catalog. Each application declaration includes:

- Stable application ID, display name, owner and help/support link.
- Route root and allowed origin; entry/build artifact and integrity/release reference.
- Minimum compatible API/contract and shared-shell versions.
- Required capabilities, optional capabilities and deployment-profile dependencies.
- Permission requirements and server-provided effective availability for the current principal.
- Entitlement/module activation, feature-flag and maintenance requirements.
- Data classification, network/egress needs and offline support.
- Health source and explicit unavailable/unsupported-version states.

Effective access is the intersection of installed capability, qualified deployment profile, module activation/entitlement and user authorization. A catalog entry never grants backend access. An unavailable paid module must not masquerade as a working feature; an installed free capability must not bypass tenant permissions.

Start with trusted first-party build-time composition and ordinary links between independently built apps. Do not add runtime remote-code loading or a microfrontend framework unless a documented requirement needs it. Browser failure containment does not imply backend fault isolation.

## 6. Repository and Packaging Plan

Keep the existing Python package structure initially. Add frontend workspace packaging after an ADR establishes the package manager and lockfile transition. A conservative option is npm workspaces because both current frontends already have npm manifests; verify versions and build compatibility before adopting it.

Proposed destination layout, created only as applications are extracted:

```text
apps/
  api/                    existing API composition; keep compatible routes
  worker/                 existing worker entry point
  mcp/                    existing protocol gateway
  vscode-extension/       existing independently packaged IDE client
  web/                    current app; temporary host for unmigrated routes
  suite-home/             launcher and shared user entry
  knowledge-portal/
  query-portal/
  config-portal/
  admin-portal/
  database-portal/
  reports-portal/
  integration-studio/     later extraction
  ontology-studio/        later extraction
  catalog-portal/         later extraction
  automation-studio/      gated expansion
  governance-portal/      gated expansion
  wisdom-portal/          gated expansion
  model-lab/              optional expansion
  operations-portal/     later extraction
  developer-portal/      later expansion
  extension-catalog/     later expansion
  fleet-console/         private operator application
packages/
  eoip/                   existing Python domains and their owned interfaces
  suite-ui/               shared visual components and tokens
  suite-shell/            shared navigation/context integration
  suite-api-client/       shared transport and generated contract types
  suite-app-contracts/    application catalog schemas and validation
schemas/                  existing schemas, extended by owning domain
deploy/                   existing deployment assets plus suite profiles
docs/suite/               decisions, inventory, ownership and release matrices
tests/suite/              cross-application and deployed release checks
```

`frontend/` remains intact until its routes and unique behavior have a verified destination. `apps/web/` is also retired only after a parity inventory and active-client check. Neither is deleted merely because new folders exist.

Each extracted app needs its own build/typecheck/test commands, production base path, SPA deep-link handling, assets, health/deployment metadata and license/notice bundle. Use immutable content-hashed assets; retain prior assets for an in-progress rollout and an audited rollback window. The gateway routes a path to one active artifact revision at a time.

Do not split `packages/eoip` into separately published Python distributions as the first step. Enforce module boundaries and optional dependencies first. Later package extraction requires a clear supported API, dependency direction, release owner and compatibility tests.

### 6.1 API compatibility

Keep existing `/api/v1` contracts and protocol entry points during portal extraction. A new UI URL is not a reason to rename APIs. Introduce adapters and deprecation notices when a genuine contract change is required.

Generate a release compatibility matrix for app, API, MCP, extension, schemas and deployment profile. Start with coordinated suite releases. Once version-skew tests exist, support the current and immediately preceding supported client release against the selected API release, or record a stricter supported combination explicitly. Never imply arbitrary version compatibility.

Long-running work returns an owned job/operation identity with explicit state, cancellation behavior and polling/event semantics. Define stable error codes, pagination, result bounds, concurrency preconditions and idempotency for new contracts. Reuse equivalent current contracts rather than creating a second transport dialect.

### 6.2 Existing route migration

| Current area | Destination | Migration rule |
|---|---|---|
| `apps/web` `/app`, graph lenses and KGR | Knowledge Explorer | Preserve entity links, renderer behavior, provenance and query result semantics |
| Studio query console; `frontend` `/query` | Query Workbench | Select one implementation after runtime comparison; retain saved history compatibility |
| Studio schema; `frontend` `/ontology`, `/schema`, `/meta-graph` | Ontology Studio, with read-only meta-graph views in Explorer | Keep one editing authority and cross-link read views |
| Connector/mapping/pipeline/system tabs; `frontend` `/ingestion` | Data Integration Studio | Preserve source IDs, jobs, checkpoints and credentials references |
| Admin users/roles; `frontend` `/tenant` | Organization Administration | Same server authorization, no synthetic admin fallback |
| Governance/quality/recovery tabs | Governance, Catalog, Operations or Database Operations | Classify by owned operation, not by original tab location |
| `frontend` `/reports`; web dashboard/export components | Reports & Analytics | Compare actual data and scheduler contracts before consolidation |
| Cognitive hubs and agent views | Automation, Model Lab, Wisdom or Knowledge Explorer | Split by workflow; do not promote experimental features through navigation |
| Appearance, `/settings`, `/brand`, `/help` | Shared settings/help and Configuration modules | Retain preferences with validation and versioned migrations |
| Existing `/wisdom/...` requirements | Wisdom portal | Preserve the exact required deep links and their authorization |

Redirects must preserve safe query parameters and bookmarks where their semantics remain valid. Some tab state currently has no stable URL; introduce explicit deep links before removing its host. Retain legacy routes behind a compatibility mapping until measured usage and acceptance gates permit retirement.

## 7. Deployment and Distribution Profiles

| Profile | Packaging | Qualification boundary |
|---|---|---|
| Developer/local | Selected portals, API, worker, MCP and chosen local graph profile | Local bootstrap mode clearly marked; no multi-tenant SaaS claim |
| Customer-installed standard | Signed/versioned suite bundle with selected modules, persistent stores, local identity integration and backup tooling | Fresh install, upgrade, restore and approved dependency inventory verified |
| Customer-installed offline | Same permitted modules with offline dependencies, notices, entitlements and documentation | No mandatory cloud login, licensing callback, model download or hidden egress |
| Hosted SaaS | Customer apps plus durable multi-worker services as qualified; private fleet/operator surface | Tenant isolation, revocation, concurrency, usage controls and restore verified |
| Enterprise isolated | Dedicated deployment/storage or regional isolation based on recorded requirements | Exact isolation, residency, support and operational objectives agreed before claiming support |

The same owned domain contracts should serve these profiles. Do not promise that every optional model or external connector works offline; show profile-specific availability. Continue supporting Compose for small installations. Add orchestration complexity only when a measured deployment need warrants it.

Possible commercial bundles are Core Knowledge, Data Engineering, Governance, Intelligence/Wisdom, and Full Suite. These are product packaging proposals, not drafted license terms or approved pricing. Entitlements must never disable critical access enforcement, audit integrity, emergency stop, or the agreed data-exit path. Package first-party terms and applicable third-party notices per distributed artifact using the existing [licensing guide](../LICENSING.md).

## 8. Phased Implementation Roadmap

No reliable calendar estimate is possible from the repository alone. Team capacity, target deployment scale, existing defects and qualification scope are not confirmed. Estimate effort after Phase 0; use the gates below instead of invented completion dates.

### Phase 0: Baseline, frontend reconciliation and decisions

1. Inventory routes, screen behavior, domain APIs, storage, jobs, external clients and deployments across both frontends and the backend.
2. Record each requirement ID's owning domain, primary app and current evidence status. Preserve all existing programme identifiers.
3. Run the supported current deployment and capture representative workflows, access refusals and known failures before changes.
4. Decide the shell/component baseline, session model, workspace packaging, application roots and database/operator trust boundary.
5. Classify each current screen as reuse, repair, combine, retain or retire; identify state migration and compatibility obligations.

Deliverables: `docs/suite/inventory.md`, `ownership.md`, frontend comparison, decision records, baseline evidence manifest and scoped backlog. These are proposed follow-on artifacts, not files created by this planning task.

Exit gate: every current route and externally used entry point has an owner and disposition; no feature is dropped silently. Known failures remain recorded rather than being hidden by the reorganization.

### Phase 1: Shared foundation

1. Extract the chosen UI tokens/components, shell and typed API transport into shared packages without changing business behavior.
2. Implement the trusted browser session/context path; reject failed identity lookup instead of inventing a privileged UI principal.
3. Add the application catalog, permission-aware launcher and unavailable-module states.
4. Add gateway routing, base-path/deep-link handling, security headers and restrictive defaults.
5. Establish cross-app trace IDs, error contracts, compatibility checks and module-boundary CI.
6. Establish reusable independent evidence capture and verification for new suite requirements.

Exit gate: two small application builds work against the real API with shared login, refresh, logout, expired session, tenant switching and direct unauthorized requests tested. The existing deployed app remains usable. Rollback selects the previous web artifacts without changing domain data.

### Phase 2: Pilot Knowledge Explorer and Query Workbench

1. Extract read-only query and explorer vertical slices, including real APIs, errors, permissions and data views.
2. Reuse the proven graph components and query constraints; avoid new query or inference implementations.
3. Preserve entity/query links and add cross-app navigation with authorized context.
4. Add capability-driven controls for unavailable backend languages and optional neural features.
5. Run old/new read-path comparisons on fixed snapshots, plus negative authorization and cancellation cases.

Exit gate: independently built apps deliver the same verified read behavior; old bookmarks work or redirect correctly; one app can be rolled back without corrupting the other. Suite Home links only to verified enabled slices.

### Phase 3: Complete the first suite release

1. Build/extract Configuration, Organization Administration, Database Operations and Reports with their domain APIs, not placeholder screens.
2. Add configuration validation, version comparison, concurrency preconditions, promotion and rollback according to risk.
3. Prove separation among configuration manager, tenant administrator, database operator and report consumer.
4. Run backup/restore against an isolated target and verify contents; do not test restore by overwriting the only source database.
5. Verify scheduled report execution, restarted workers, restricted download and revoked access.
6. Keep MCP and VS Code backward-compatible; qualify new shared identity paths separately where needed.

Exit gate: the seven initial browser areas and the existing two client channels have a documented supported release combination. Incomplete features are disabled or labeled unavailable, with their requirements still open. Rollback for data-changing features requires compatible schemas or the tested restore/forward-repair procedure, not just a frontend redirect.

### Phase 4: Separate data engineering and semantics

1. Extract Data Integration Studio, Ontology Studio and Catalog & Quality.
2. Move ownership out of mixed Studio/Admin components without duplicating connector, schema or quality services.
3. Qualify one real representative connector before expanding the connector catalog.
4. Exercise source onboarding, discovery, mapping, ingestion, quality findings, entity review, lineage and fresh query results as one journey.
5. Exercise a governed ontology change, dependency impact, failed validation and successful rollback/revalidation.

Exit gate: data engineering can evolve without modifying the main Explorer UI; semantic changes still pass the shared validation, approval and repair paths. Vendor credentials and rate limits remain isolated per connector/tenant.

### Phase 5: Governed intelligence and decision applications

1. Complete the required shared identity, authority, event and effect-verification prerequisites before exposing consequential agent actions.
2. Build Governance & Evidence as the human review surface over those services; start its foundations earlier when required by configuration or ontology operations.
3. Extract Agent & Automation Studio using the existing ASPEII and IP contracts.
4. Build Wisdom screens using decision traces, warrants, receipts and CTAR repair references, not parallel records.
5. Add Model Lab for explicitly qualified numerical/model profiles with reproducible evaluation and resource controls.

Exit gate: applicable ASPEII, CIP, IP, GN and WG evidence gates pass at actual API, worker, storage and UI boundaries. A portal split does not close an algorithm, action-safety or model qualification requirement.

### Phase 6: Operations, ecosystem and distribution

1. Extract Operations and Developer Hub from existing working views and add missing runbooks, delivery inspection and contract tools.
2. Start Extension Catalog as a private first-party catalog; allow external publishing only after package trust and isolation are qualified.
3. Add Commercial & Fleet on a private operator origin; scope support access to explicit customer approval and audited expiry.
4. Qualify install/upgrade/restore/offline distribution, entitlement behavior and per-artifact license notices.
5. Add deployment profiles and commercial bundles without forking the core codebase for each customer.

Exit gate: each supported profile is installable from documented artifacts and has a tested recovery path. Optional modules can be absent without breaking the core; removal cannot orphan data without an explicit export/retention procedure.

### Phase 7: Selective service or repository extraction

Measure workload and ownership pressure before proceeding. Candidate first service extractions are report rendering, connector acquisition pools, and model inference because they can have distinct resource or failure profiles. Maintain the already separate MCP and worker processes.

Extract a service only after all of these exist: owned contracts/state, a concrete reason, authentication, durable job/event semantics, an SLO, failure isolation, telemetry, an operational owner, compatible migrations and a tested rollback/recovery procedure. Do not split the lease/approval/dispatch atomic boundary just to achieve a service count.

Split repositories only when independent teams, access restrictions, external SDK distribution or release ownership require it. Shared contracts and published package compatibility then become explicit release obligations.

## 9. Work Packages for Coding Agents

Each package starts with a narrowly scoped behavior and keeps existing feature work intact. The references below are starting points, not proof of completion.

| Package | Scope | Depends on | Required observed result |
|---|---|---|---|
| SUITE-WP-01 | Baseline and two-frontend route/contract inventory | None | Reproducible old behavior, known failures and no unowned route |
| SUITE-WP-02 | Architecture decisions and domain/app ownership | WP-01 | Accepted boundary, identity, packaging and deployment decisions |
| SUITE-WP-03 | Shared UI, shell, API client and app catalog | WP-02 | Two independent builds with coherent navigation and actual backend results |
| SUITE-WP-04 | Trusted identity/context and session lifecycle | WP-02 | Failed identity, logout, expiry, revocation and cross-tenant attempts handled correctly |
| SUITE-WP-05 | Gateway, artifact/version compatibility and release CI | WP-03, WP-04 | Refresh/deep links and mixed-version acceptance/refusal behave as documented |
| SUITE-WP-06 | Query and Explorer extraction | WP-05 | Read-path parity, policy refusal, cancellation and rollback evidence |
| SUITE-WP-07 | Configuration and Organization Administration | WP-05, required authority services | Versioned settings and access changes persist safely and deny unauthorized operations |
| SUITE-WP-08 | Database Operations and restricted trust zone | WP-05 | Isolated restore succeeds; ordinary tenant admin cannot perform physical operations |
| SUITE-WP-09 | Reports, schedules and artifacts | WP-05, qualified job storage | Real scheduled run survives restart; revoked user cannot download its restricted result |
| SUITE-WP-10 | MCP/VS Code/CLI/SDK compatibility | WP-04, WP-05 | Real client calls preserve tenant/policy boundaries and compatible errors |
| SUITE-WP-11 | Integration, Ontology, Catalog and Quality | WP-06, WP-07 | Source-to-query and governed schema-change journeys pass |
| SUITE-WP-12 | Governance, Automation, Wisdom and Model Lab | Relevant programme prerequisites | Independent action, evidence, decision and model gates pass, not UI-only demos |
| SUITE-WP-13 | Operations, Developer Hub and private extensions | WP-05 plus owning domains | Diagnosable incidents, contract checks and safe install/rollback workflows |
| SUITE-WP-14 | Fleet, packaging, entitlements and offline profiles | Relevant app gates | Fresh install, upgrade, restore and no-egress profile evidence |
| SUITE-WP-15 | Selective extraction and legacy retirement | Measured need plus parity | No required old consumer remains; recovery is tested before removal |

The first coding increment should be WP-01 and WP-02, followed by the shared foundation and the read-only Query/Explorer pilot. Do not generate all application folders with empty pages and count that as suite implementation.

## 10. Mapping to Existing Programmes

| Existing requirements | Primary suite ownership | Integration obligation |
|---|---|---|
| [GUI/UIX](../GUI-UIX-requirements.md) and [GUI plan](../GUI-UIX-implementation-plan.md) | Shared shell plus owning apps | Redistribute screens while preserving all user journeys, accessibility and real-backend gates |
| [Gap audit](../gaps-audit-cp.md) and [plan](../gaps-audit-cp-implementation-plan.md) | Every affected domain | Attach suite work to existing gaps; do not relabel open features complete because they moved |
| [Competitive requirements](../CRAr_cpccaggcc-requirements.md) and [implementation](../CRAr_cpccaggcc-implementation.md) | Data, query, operations and integration owners | Map each in-scope capability to its owning app/domain and qualification profile |
| [ASPEII](../aspeii-reqirements.md) and [plan](../aspeii-implementation-plan.md) | Automation, Governance, Developer Hub and shared authority | Preserve action identity, delegation, approvals, receipts and independent verification |
| [Community/IP](../community-ip-requirements.md) and [plan](../community-ip-implementation-plan.md) | Catalog, Governance and shared repair services | Reuse change intake, invalidation, repair and revocation across all app projections |
| [IP/Warrant](../ip-requirements.md) and [plan](../ip-requirements-implementation-plan.md) | Knowledge core, Governance and Automation | Keep shared warrants, checkpoints, leases and consequence controls authoritative |
| [Graph Neurons](../Graph-Neurons-requirements.md) and [plan](../Graph-Neurons-implementation-plan.md) | Model Lab and shared optional neural runtime | Preserve optional tiers, anti-stub probes, temporal evaluation and prediction/fact distinction |
| [Wisdom Graph](../wisdom-graph-requirements.md) and [plan](../wisdom-graph-implementation-plan.md) | Wisdom app and shared knowledge/trust services | Preserve exact decision, precedent, counsel, outcome and evidence semantics |

These programme mappings are ownership guidance, not a line-by-line re-audit of their entire scope. Phase 0 produces the full requirement-to-owner matrix. Resolve normative conflicts with the existing decision process and owner acceptance; this proposal does not silently override them.

## 11. Definition of Done and Release Evidence

An application is not complete because it has a folder, URL, screenshot, mock server, tests, or a successful build. Track it as planned, implemented, evidenced, or independently verified using the owning programme's exact status vocabulary. A skipped deployment profile remains unqualified.

For each release, capture commit and artifact digests, configuration/profile, migrations, dataset/snapshot, redacted request traces, user/tenant roles, actual command output, persistent-state/effect observations and independent verifier results. Store raw evidence in durable controlled artifact storage; keep curated fixtures and evidence manifests in Git. Do not make an ignored local `.audit-scratch` folder the only location for release evidence.

Mandatory suite scenarios:

| Scenario | Evidence needed |
|---|---|
| Login and navigation | A real user signs in, opens two separately built apps, refreshes a deep link and signs out; old sessions no longer work |
| Identity failure | Identity lookup fails; no synthetic admin session or privileged UI state appears |
| Tenant isolation | Two tenants and differently scoped users attempt reads, queries, jobs, exports, search, events and direct API access; unauthorized data is not revealed |
| Context switch | In-flight requests and cached results from the old tenant cannot populate the new tenant's view |
| Role separation | Tenant admin, configuration manager, auditor and database operator receive only their intended operations |
| Query parity | Fixed authorized data yields equivalent old/new results, warnings and limits; denied queries remain denied |
| Source-to-knowledge | Configure a real supported source, ingest, verify counts/provenance, query and inspect lineage |
| Semantic change | Invalid release is refused; approved valid release publishes once and triggers required revalidation/repair |
| Configuration safety | Concurrent edits conflict correctly; promotion and rollback leave an independently checked effective configuration |
| Reporting safety | Scheduler/worker restart preserves lifecycle; export content matches source and access is rechecked at download |
| Database recovery | Restore to an isolated target, compare logical data and authority state, then prove pending approvals cannot be replayed improperly |
| Agent effects | Invalid/revoked/expired approval prevents dispatch; an admitted action has independently observed effect and matching receipt |
| Wisdom and models | Applicable programme benchmarks, abstentions, calibration and evidence-status constraints pass in the running system |
| Failure isolation | A missing report/model app does not break graph browsing; backend outages produce honest errors and no synthetic success |
| Client compatibility | Supported VS Code and MCP clients call real services with correct identity, bounds and refusal semantics |
| UI quality | Desktop/mobile workflows, keyboard and screen-reader checks, reduced motion, nonblank graphs and text/layout fit verified |
| Release lifecycle | Fresh install, compatible upgrade, app rollback, data recovery and optional module disable/uninstall are exercised |
| Offline profile | Required workflows run without undeclared egress; unavailable external integrations are explicit |
| Evidence negative control | Missing, stale or tampered mandatory evidence prevents verified/completed release status |

Measure performance before setting release budgets. Use existing programme budgets where already normative. Otherwise record agreed workload, hardware, data size, tenant/concurrency distribution and p95/p99 targets before performance qualification. Do not invent universal latency or scale claims from a development machine.

## 12. Main Challenges and Controls

| Challenge | Control |
|---|---|
| Turning one large UI into many confusing UIs | Shared launcher/context; persona-oriented local navigation; no portal for every small feature |
| Duplicating work across the two existing frontends | Route-by-route parity decision and one owner for each capability |
| Repeated logins and inconsistent permissions | One trusted session model and server-side domain authorization; separate operator trust zones |
| Moving code without reducing coupling | Owned contracts, import boundaries, stable identifiers and single-writer domain ownership |
| Increasing deployment cost before gaining value | Monorepo, coordinated releases and shared backend modules first; extract services only with evidence |
| Broken approval/dispatch consistency | Keep atomic authority together and qualify distributed effects before service extraction |
| Reporting or search leaking stale restricted data | Authoritative permission checks, scope-aware caches and revocation tests |
| Raw database tools bypassing governance | Restricted maintenance boundary, audited exceptional access and post-maintenance reconciliation |
| Different app versions breaking each other | Published compatibility matrix, contract tests and supported skew policy |
| Losing existing features during migration | Baseline inventory, old/new behavioral parity and delayed retirement |
| Promising unlimited integrations | Adapter SDK and conformance matrix; qualify each connector's actual auth, semantics and effects |
| Optional ML dependencies overwhelming local installations | Explicit optional profiles and resource-isolated runtimes; deterministic core remains usable |
| Plugin catalog becoming remote-code execution | First-party/private catalog first; signed packages, capability review, isolation and revocation before external publishers |
| Calling a reorganization 100% product completion | Preserve original requirement gates and require independent runtime evidence |

## 13. Decisions Before Implementation

These are proposed defaults, not hidden assumptions. Record accepted decisions and their consequences in Phase 0.

| Decision | Recommended default | What remains to resolve |
|---|---|---|
| Product identity | EOIP / KnowGridFlow suite, one coherent brand | Final commercial naming; do not mass-rename APIs/packages |
| Repository strategy | One monorepo | Separate repositories only with named owners and distribution need |
| UI composition | Independent static builds, common shell packages and gateway paths | Frontend comparison and exact baseline selection |
| Frontend toolchain | Reuse React/Vite; evaluate npm workspaces | Version alignment, lockfile and dependency/license changes |
| Browser identity | Reviewed provider integration and server-side session boundary | Provider/profile choice, migration and offline setup |
| Core backend | Modular existing Python/FastAPI code | Explicit module interfaces and circular dependency remediation |
| Durable authority | Reuse existing ASPEII local/SaaS storage decisions | Implementation and qualification gaps, not a competing repository |
| Operator access | Separate privilege plane; separate origin/network where required | Hosted and installed deployment-specific policy |
| First product milestone | Seven browser areas plus existing MCP/VS Code clients | Exact feature subset after baseline; every deferral stays visible |
| Scope/schedule | Gate-driven roadmap | Staffing, support obligations, target workloads and priorities |

## 14. External Architecture References

These references inform the approach; the application catalog and migration choices are recommendations for this repository, not claims prescribed by a standard.

- Incremental replacement with a compatibility facade is an established migration approach. Use it to move one proven workflow at a time. [Microsoft: Strangler Fig pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig).
- Domain boundaries should follow business models and invariants, rather than arbitrary screen or table counts. [Microsoft: Tactical domain-driven design](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design).
- MCP access needs resource-specific authorization and protection against token passthrough/confused-deputy behavior. Pin and test the chosen released protocol revision separately from this evolving guidance. [MCP: Security best practices](https://modelcontextprotocol.io/docs/draft/tutorials/security/security_best_practices).
- Shared accessibility requirements apply to whole workflows across applications. [W3C: WCAG 2.2](https://www.w3.org/TR/WCAG22/).

## 15. Immediate Next Step

Execute the baseline and frontend reconciliation, then build the shared identity/shell foundation and extract Query Workbench plus Knowledge Explorer as the first independently built vertical slice. Use that slice to prove navigation, permissions, packaging, compatibility and rollback before expanding to the full suite.

This is how EOIP becomes multiple maintainable applications while remaining one coherent product and one governed knowledge platform.
