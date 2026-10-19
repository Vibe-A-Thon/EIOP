# Repository Catalog and Ownership

All names below are proposed lowercase repositories under the user-confirmed organization `AvyukthiAI`, for example `AvyukthiAI/eoip-suite` and `AvyukthiAI/eoip-query-portal`. Each application is distinct. A local folder has exactly the repository name. GitHub organization permissions do not replace runtime customer permissions.

## Eighteen Browser Applications

Port numbers are reserved local-development proposals, not currently running services. Vite must fail on a port conflict rather than silently select another. Database/Fleet applications are not routed through the customer gateway in hosted deployments.

| ID | Repository | Root / dev port | Scope and initial source candidates | Wave |
|---|---|---|---|---|
| APP-01 | `eoip-suite-home` | `/suite/` / 5100 | Entitled app launcher, context, recent work; existing shells/navigation plus new catalog | Pilot |
| APP-02 | `eoip-configuration-portal` | `/configure/` / 5101 | Validated settings, revisions, promotion, rollback; settings/config screens | First release |
| APP-03 | `eoip-admin-portal` | `/admin/` / 5102 | Organizations, membership, roles, entitlements; admin and tenant screens | First release |
| APP-04 | `eoip-database-portal` | restricted `/database/` / 5103 | Backend capabilities, indexes, maintenance, isolated recovery; operations tooling | First release |
| APP-05 | `eoip-query-portal` | `/query/` / 5104 | Query authoring, plans, bounded results, saved queries; `studio/QueryConsole.jsx`, `frontend/src/screens/Query.tsx` | Pilot |
| APP-06 | `eoip-knowledge-portal` | `/explore/` / 5105 | Graph/entity/provenance/impact/temporal views; `apps/web/src/kgr`, explorer lenses | Pilot |
| APP-07 | `eoip-reporting-portal` | `/reports/` / 5106 | Dashboards, schedules, exports, artifact history; report and dashboard screens | First release |
| APP-08 | `eoip-integration-studio` | `/integrate/` / 5107 | Sources, mapping, ingestion, reconciliation, DLQ; mixed Studio/Admin screens | Data expansion |
| APP-09 | `eoip-ontology-studio` | `/ontology/` / 5108 | Types, vocabularies, constraints, governed semantic releases | Data expansion |
| APP-10 | `eoip-catalog-portal` | `/catalog/` / 5109 | Ownership, discovery, quality, lineage, freshness and resolution | Data expansion |
| APP-11 | `eoip-automation-studio` | `/automate/` / 5110 | Agents, intents, delegation, proposals and supervised workflows | Governed intelligence |
| APP-12 | `eoip-governance-portal` | `/governance/` / 5111 | Policies, approvals, warrants, evidence and REVA views | Foundations early; full app later |
| APP-13 | `eoip-wisdom-portal` | `/wisdom/` / 5112 | Decisions, outcomes, lessons, counsel and precedent | Governed intelligence |
| APP-14 | `eoip-model-lab` | `/models/` / 5113 | Optional model profiles, evaluations, calibration and promotion | Optional qualified profile |
| APP-15 | `eoip-operations-portal` | `/operations/` / 5114 | Health, jobs, traces, incidents and recovery coordination | Operations expansion |
| APP-16 | `eoip-developer-portal` | `/developers/` / 5115 | API/SDK/MCP discovery, webhook inspection and sandboxes | Developer expansion |
| APP-17 | `eoip-extension-catalog` | `/extensions/` / 5116 | Reviewed private connector/domain/template packages | Private catalog first |
| APP-18 | `eoip-fleet-console` | private `/fleet/` / 5117 | Product-operator deployments, support, entitlements and rollout inventory | Restricted operator phase |

Source candidates are not instructions to copy complete directories into several apps. The route/feature inventory assigns a single owner per workflow and records every dependency first.

## Channels and Runtime Applications

| ID | Repository | Starting point | Artifact / boundary |
|---|---|---|---|
| CH-01 | `eoip-vscode-extension` | `apps/vscode-extension/` | VSIX; preserve command IDs and stored-secret compatibility |
| CH-02 | `eoip-mcp-server` | `apps/mcp/` | Python service/image; supported protocol and authentication explicitly pinned |
| CH-03 | `eoip-cli` | `packages/eoip/cli.py` | Thin client distribution; transfer console-script ownership without duplicate `eoip` commands |
| CH-04 | `eoip-sdk` | Existing contracts/clients plus generation work | Python and TypeScript SDK packages in one library repository; not two duplicate engines |
| RT-01 | `eoip-core-api` | `apps/api/` | FastAPI application image; consumes the platform wheel |
| RT-02 | `eoip-ingestion-worker` | `apps/worker/` | Worker application image; consumes the same qualified platform version |
| RT-03 | `eoip-suite-gateway` | Existing web proxy patterns plus new work | Reverse proxy/static routing and reviewed session adapter; no business-domain duplication |

## Shared Foundations and Coordination

| ID | Repository | Owns | Does not own |
|---|---|---|---|
| LIB-01 | `eoip-platform` | Existing `packages/eoip` domain library, domain schemas/resources, unit tests and public Python interfaces | Portal source, operator UI, all suite deployment secrets |
| LIB-02 | `eoip-ui` | Tokens, accessible components, shared shell/context interfaces; several published packages allowed | Domain persistence, API authorization, copied app screens |
| LIB-03 | `eoip-contracts` | Released API snapshots, event/app-catalog schemas and compatibility rules | A second editable copy of backend Pydantic models |
| LIB-04 | `eoip-reva` | Root `reva/`, its packaging, component tests and REVA-owned tools/docs | Automatic certification of every suite component |
| CO-01 | `eoip-suite` | Repo manifest, workspace, local infrastructure, suite lock/release manifest, deployment profiles and reusable CI workflows | All app source, developer secrets, raw production/customer evidence |
| CO-02 | `eoip-engineering` | Normative requirements/plans, ADRs, ownership/traceability and cross-suite docs/research | Mutable runtime state or claims manufactured from source paths |
| CO-03 | `eoip-verification` | Cross-app acceptance, upgrade/restore/negative controls, evidence manifests | Implementation self-certification without independently executed checks |

An organization `.github` repository is optional administration infrastructure, outside these 32 product repositories. Do not make it public merely to obtain default community files. GitHub plan/visibility support must be checked before relying on inherited policies.

## Ownership Rules

1. Every repository has a named accountable maintainer, backup/reviewer where available, security contact and release approver. Role names in this plan are not invented staff assignments.
2. Every requirement retains its original ID, one primary owner, affected consumers and required evidence depth. UI and backend owners collaborate; neither closes the other's requirements by moving files.
3. Backend business models remain in `eoip-platform` until a justified package extraction. Do not split each subpackage into a new repository in the first migration.
4. REVA is optional until its clean install, lifecycle, trusted identity and evidence requirements pass. Governance can display unavailable capability honestly.
5. Same GitHub organization is the default for new repositories. Transfer the existing repository only through a separately reviewed operation; do not change its remote as a shortcut.

## Dependency Direction

```text
contracts -> generated SDK types/clients
ui packages + SDK -> portals
platform -> core-api and ingestion-worker
platform public interfaces + REVA adapters -> optional REVA integration
API contracts -> MCP, CLI, VS Code and SDK
component artifacts -> suite deployment manifest
suite deployment -> independently executed verification
```

Contracts snapshots are extracted from reviewed backend source and compared in CI; the arrow does not mean two schema authorities. Break import cycles with explicit interfaces. Portals cannot import one another, API cannot import worker startup, and a package cannot require a sibling Git checkout to function.
