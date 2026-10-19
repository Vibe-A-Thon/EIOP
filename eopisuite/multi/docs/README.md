# EOIP / KnowGridFlow Multi-Repository Suite Handbook

Prepared: 2026-10-19. Source baseline: `d802c5e4c2fb8b360b0f13a9eda4bbcf2e9d95d1`, plus inspected working-tree files. Status: implementation specification and setup templates; not an already deployed suite.

## The Answer

Use **one GitHub organization, one repository per application, and one VS Code multi-root workspace**. Keep a small `eoip-suite` repository for workspace configuration, local orchestration and the exact supported release combination. Publish shared libraries instead of copying them into applications. Keep backend domain logic modular and shared; separate repositories do not require a separate database or backend service for each portal.

Your new repository requirement replaces the monorepo-first recommendation in [the earlier suite plan](../../../docs/EOIP-suite-architecture-plan.md). Its application IDs, security boundaries, migration safeguards and evidence requirements remain in force. This handbook does not silently change existing product requirements.

The catalog defines **32 target repositories**: 18 portals, four developer channels, three runtime applications, four shared foundations and three coordination/assurance repositories. This is a destination map, not a request to build or operate 32 applications immediately. Start with the foundation and Query/Explorer pilot; add repositories as their work starts.

## Reading and Execution Order

| Step | Guide | Outcome |
|---|---|---|
| 1 | [Current state and decisions](01-current-state-and-decisions.md) | Understand what exists, what changes and what remains unresolved |
| 2 | [Repository catalog and ownership](02-repository-catalog-and-ownership.md) | Assign every application/library a distinct repository and owner |
| 3 | [GitHub organization setup](03-github-organization-setup.md) | Create private repositories, access controls and review policies |
| 4 | [Local bootstrap](04-local-workspace-bootstrap.md) | Clone sibling repositories without changing the existing project |
| 5 | [One VS Code instance](05-vscode-workspace-tasks-debugging.md) | Open all selected repositories; configure tasks, debugging and interpreters |
| 6 | [Packages and contracts](06-shared-packages-contracts-versioning.md) | Build without sibling-source imports or hidden monorepo dependencies |
| 7 | [Local runtime and gateway](07-local-runtime-and-gateway.md) | Run today's baseline, then introduce independently built portals |
| 8 | [Extraction runbook](08-extraction-migration-runbook.md) | Move source safely, preserve provenance and prove parity |
| 9 | [Repository templates](09-repository-templates.md) | Standardize each repository's build, tests, configuration and documentation |
| 10 | [CI/CD and releases](10-ci-cd-release-management.md) | Validate component changes and release tested combinations |
| 11 | [Security, data and licensing](11-security-configuration-data-licensing.md) | Preserve identity, state ownership and distribution boundaries |
| 12 | [Implementation backlog](12-implementation-backlog.md) | Execute dependency-ordered work packages with explicit exits |
| 13 | [Verification and evidence](13-verification-and-evidence.md) | Decide completion from observed behavior, not files or checkboxes |
| 14 | [Daily work and troubleshooting](14-daily-work-and-troubleshooting.md) | Maintain the suite efficiently from one editor |
| 15 | [Decisions, sources and handover](15-decisions-sources-and-handover.md) | Resolve inputs, review official references and hand work to coding agents |

## What This Change Does and Does Not Do

This delivery creates Markdown documents only under `eopisuite/multi/docs/`. It does not create GitHub repositories, transfer ownership, change billing, clone repositories, rewrite history, launch services, publish packages, move existing code or change licenses. Examples are materialization instructions for later implementation. An absent target file remains absent until the corresponding task is completed.

The user confirmed [AvyukthiAI](https://github.com/AvyukthiAI) as the suite's GitHub organization. Repository references use `AvyukthiAI/<repository>`; npm packages use lowercase `@avyukthiai/<package>` and container references use `ghcr.io/avyukthiai/<image>`. These are target namespaces, not claims that repositories or packages have already been created. Organization administrator permissions, team membership and package access still require verification. Default local destination: `F:\code\EIP\eopisuite-workspace`, outside the current repository. No purchase or hosted identity-provider selection is implied.

## First Practical Milestone

1. Verify the signed-in account's permissions in `AvyukthiAI`, then create the seven pilot repositories listed in guide 03 through an authorized setup operation.
2. Materialize the local workspace from guide 04; keep this checkout as the legacy runtime.
3. Inventory both frontends and publish a compatible shared UI/contract foundation.
4. Extract a real Query and Explorer workflow into separate repositories.
5. Prove separate clean builds, shared navigation, authorization, deep links and rollback.
6. Only then expand to Configuration, Admin, Database Operations and Reporting.

One developer can hold several ownership roles. Independent verification still needs a distinct verification execution and durable evidence; do not invent team members or claim independent human review when none occurred.

## Vocabulary

- **Existing:** observed source or configuration, with explicit limits.
- **Target:** architecture to implement, not current behavior.
- **Template:** configuration/code requiring materialization and validation.
- **Gate:** an observable acceptance condition; a test path alone does not satisfy it.
- **Component release:** a versioned package/image/application artifact.
- **Suite release:** an exact, tested combination of component artifacts and configuration.

The mechanism for opening independent folders together is native [VS Code multi-root workspaces](https://code.visualstudio.com/docs/editing/workspaces/multi-root-workspaces). Product architecture choices in this handbook are repository-specific recommendations, not guarantees supplied by the editor or GitHub.
