# Decision Register, Sources and Agent Handover

## Required Inputs and Safe Defaults

| Item | Current decision / unresolved input | Work blocked until resolved |
|---|---|---|
| Repository strategy | User requires separate application repositories in one organization | Not blocked; MULTI-D01 supersedes old monorepo recommendation |
| GitHub handle | User confirmed `AvyukthiAI`; lowercase package scope `avyukthiai` | Naming resolved; administrator authority and remote changes remain separately gated |
| Organization access | Private membership, administrator permissions and package access not verified | Remote creation, transfers, access grants and publishing |
| Local parent | Proposed `F:\code\EIP\eopisuite-workspace` | Confirm before materializing local clones; docs can proceed |
| Existing checkout | Keep `F:\code\EIP\EIOP` intact | No migration task may rewrite/delete it by default |
| Repository naming | `eoip-*` catalog proposed in guide 02 | Confirm collisions before creation; do not mass-rename product APIs/imports |
| License ownership | Existing project legal files remain authoritative | New legal terms/public redistribution decisions require owner/legal review |
| Organization plan | Not assumed or purchased | Verify private-repo enforcement/package features before declaring access gates passed |
| Actual maintainers/reviewers | Role slots specified, people not invented | Production approval and independent human-review claims |
| Browser identity provider | Must support chosen hosted and installed profiles; vendor not selected | R2 session production qualification, not R1 local UI extraction |
| Shared UI baseline | Reconcile existing two frontends first | Wide component rollout before parity/dependency decision |
| Runtime toolchain | Current source CI baseline Python 3.11 / Node 22.18.0; reviewed exact pins required | New release security/support qualification |
| Python distribution | Bootstrap verified Release wheel assets; future private index by ADR | Managed registry deployment/cost not authorized |
| Hosted infrastructure | No cloud, region, capacity or billing selection made | Hosted deployment/procurement claims |
| Scale/SLO/staffing/dates | Not established; measure and agree per profile | Performance/capacity/calendar promises |
| Optional modules | Disabled/unqualified until their own gates pass | Promotion of models, REVA, external effects or marketplaces as ready |

No placeholder is silently converted into a production default. Conversely, do not block the whole migration because one deployment-specific decision is pending: baseline inventory, repository templates and isolated packaging can proceed independently.

Organization confirmation: the user supplied [AvyukthiAI](https://github.com/AvyukthiAI), whose public page identifies it as a GitHub organization. This resolves the namespace only; it does not verify the signed-in user's permissions, inventory private repositories, or authorize creating/transferring repositories. No GitHub mutation was performed for this documentation update.

## Existing Programme Continuity

Keep the [original suite plan](../../../docs/EOIP-suite-architecture-plan.md), [migration guide](../../../docs/migration-refactoring-guide.md), [testing guide](../../../docs/testing-guide.md) and [configuration guide](../../../docs/configuration-reference.md) as baseline context. This handbook changes repository strategy, not the required authority, persistence, usability or evidence behavior.

The engineering migration must preserve these requirement families and their companion plans:

| Family | Existing authoritative entry | Target owners |
|---|---|---|
| Gap closure | [Gap audit](../../../gaps-audit-cp.md) | Every affected domain/application |
| GUI | [GUI/UIX requirements](../../../GUI-UIX-requirements.md) | Shared UI plus owning app |
| Competitive capabilities | [Competitive requirements](../../../CRAr_cpccaggcc-requirements.md) | Data/query/governance/developer owners |
| ASPEII | [Requirements](../../../aspeii-reqirements.md) | Platform authority, Automation, Governance |
| Community/IP | [Requirements](../../../community-ip-requirements.md) | Repair/catalog/governance owners |
| IP/Warrant | [Requirements](../../../ip-requirements.md) | Platform trust/authority and consumers |
| Graph Neurons | [Requirements](../../../Graph-Neurons-requirements.md) | Optional platform runtime and Model Lab |
| Wisdom Graph | [Requirements](../../../wisdom-graph-requirements.md) | Wisdom and shared knowledge/trust services |
| REVA | [Requirements](../../../reva-requirements.md) | REVA, Governance and independent verification |

This is a family-level ownership map, not a claim that every normative line has already been assigned and verified. MULTI-002 produces the full requirement-to-owner matrix.

## Official Technical References

Consulted 2026-10-19. Recheck before materializing automation because hosted tooling and plan capabilities can change. These sources support tooling mechanics; repository names, boundaries and migration waves are recommendations tailored to this project.

| Topic | Primary reference |
|---|---|
| VS Code multiple roots, scoped settings/tasks/debugging | [Multi-root workspaces](https://code.visualstudio.com/docs/editing/workspaces/multi-root-workspaces) |
| Explicit Python debugger interpreter | [Python debugging](https://code.visualstudio.com/docs/python/debugging) |
| Organization team permissions | [GitHub teams](https://docs.github.com/en/organizations/organizing-members-into-teams/about-teams) |
| Repository creation flags | [GitHub CLI repo create](https://cli.github.com/manual/gh_repo_create) |
| Review ownership | [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) |
| Branch/tag policy availability | [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) |
| Supported registries | [GitHub Packages introduction](https://docs.github.com/en/packages/learn-github-packages/introduction-to-github-packages) |
| Private npm authentication | [GitHub npm registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry) |
| Reusable workflow mechanics | [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) |
| Workflow token boundary | [GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token) |
| Asset base paths | [Vite build guide](https://vite.dev/guide/build.html#public-base-path) |
| Proxy prefix and websocket handling | [Nginx proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass), [websocket proxying](https://nginx.org/en/docs/http/websocket.html) |
| Container-to-host networking | [Docker Desktop networking](https://docs.docker.com/desktop/features/networking/) |
| History and leaked credentials | [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) |

## Coding-Agent Handover Instruction

Use the following as the task contract for each implementation increment, substituting actual approved inputs:

```text
Implement one approved MULTI work package from this handbook.
Read its dependencies, existing programme requirements and current repository state.
Allowed repositories: specify exact names and local roots.
Baseline commits: record each; preserve pre-existing dirty changes.
Do not create remote resources or publish artifacts unless that action is authorized.
Resolve required placeholders; stop only the affected operation if input is missing.
Implement real behavior and tests; do not replace missing integration with synthetic success.
Keep one domain/data owner; use versioned artifacts and supported contracts.
Run clean-build, denied-case and integration checks at the required evidence depth.
Record exact commands/results, source/artifact hashes, failures/skips and retained evidence.
Update owning docs, compatibility manifest and requirement traceability.
Do not mark complete from code/test references, file counts or screenshots alone.
Report what changed, what was executed, what remains open and how to roll back.
```

## Documentation Delivery Boundary

This handbook is the deliverable for the requested multi-repository setup plan. Runtime implementation, actual GitHub organization setup, migration, shared session integration and suite acceptance remain future work packages. Validation of these Markdown links and configuration examples checks documentation quality, not those future systems' readiness.

Documentation checks performed: 16 Markdown files; 49 local links resolved; six JSON examples parsed; seven PowerShell examples passed parser checks; the workflow YAML parsed; the catalog contains 32 unique repository names and 18 unique portal development ports. No bootstrap/GitHub mutation command, runtime process, Nginx configuration test or application acceptance test was executed. Placeholder rejection, clone safety, end-to-end setup and deployment remain implementation verification tasks, not results inferred from syntax checks.
