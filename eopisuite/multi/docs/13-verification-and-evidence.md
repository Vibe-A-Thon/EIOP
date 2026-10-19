# Verification and Evidence Gates

## Completion Rule

A repository, file, route, package, screenshot, test reference, green unit count or generated ledger does not alone prove implementation/integration completion. Preserve the original programme's evidence depth and status vocabulary. If its rules are stricter than this handbook, follow those rules.

Separate **implemented**, **executed**, **evidenced** and **independently verified** states. Do not call a skipped profile passed. Record defects found during migration instead of rewriting requirements to match incomplete behavior.

## Mandatory Gates

| Gate | Execute | Required observation |
|---|---|---|
| MR-G01 Organization/bootstrap | Clone as authorized and denied identities; rerun bootstrap | Correct private org/repos, no overwritten dirty work, denied access enforced |
| MR-G02 Workspace | Open pilot roots in one VS Code window and reopen | Independent Git roots, correct folder scopes, working tasks/interpreters and no hidden parent repo |
| MR-G03 Isolation build | Build each artifact in a fresh isolated checkout | No sibling imports, untracked assets, developer-only dependencies or shared node_modules/venv |
| MR-G04 Package resources | Install wheels outside source cwd and start services | Config/schema/templates/resources resolve correctly; missing inputs fail honestly |
| MR-G05 Contract boundary | Compatible and incompatible client/provider combinations | Correct supported responses; incompatible combinations rejected explicitly |
| MR-G06 Shared identity | Login across two apps; fail identity lookup; expire/revoke/logout | Trusted identity preserved; no synthetic admin; revoked sessions unusable |
| MR-G07 Tenant/context | Two tenants/roles, direct API calls, cache switch and in-flight requests | No unauthorized records, jobs, search, exports, events or stale cross-tenant rendering |
| MR-G08 Gateway/UI | Refresh deep URLs, missing assets, disabled app, HMR/dev and static prod | Correct app/base paths, 404 where required, no API-to-HTML fallback |
| MR-G09 Query/Explorer parity | Fixed authorized snapshot; denied, limit and cancellation cases | Matching intended semantics and bounds, nonblank usable graph/table rendering |
| MR-G10 Settings/admin | Concurrent edits, invalid config, promotion, rollback, role change | Durable intended state and denied unauthorized mutation |
| MR-G11 Ingestion | Real supported source, worker restart/retry and reconciliation | Correct persisted effects/provenance; no duplicate or silently lost work |
| MR-G12 Reporting | Scheduled real report, worker restart, revoke before download | Content matches allowed snapshot; restricted download denied |
| MR-G13 Recovery | Backup and isolated restore with pending authority/job state | Logical integrity, recoverable lifecycle and no improper approval replay |
| MR-G14 Clients | Real MCP session, extension host, CLI/SDK install and calls | Correct identities/errors/bounds, multi-root source restrictions and compatibility |
| MR-G15 Accessibility/layout | Keyboard/screen-reader/reduced-motion plus desktop/mobile journeys | Usable complete workflows; no overlap, inaccessible control or blank visualization |
| MR-G16 Optional modules | Disable absent model/report/REVA/extension modules | Core browsing/query remains functional; unavailable state is explicit |
| MR-G17 Release lifecycle | Fresh install, compatible upgrade, app rollback and data recovery | Exact digest combination works; no hidden rebuild or unsafe migration reversal |
| MR-G18 Offline | Run qualified installed workflows with outbound network denied | No undeclared cloud/auth/font/model/license dependency; explicit unavailable integrations |
| MR-G19 Evidence integrity | Delete, alter, stale or mismatch required evidence | Verification refuses completion; correct scope/commit/artifacts are enforced |
| MR-G20 Operator plane | Ordinary tenant/admin attempts Database/Fleet actions | Separate privilege/origin/network controls hold; access and support sessions audited |

Performance qualification additionally records workload, hardware, data size, concurrency, tenant mix and measured percentiles. Preserve any existing normative budgets. Do not invent a universal throughput/SLO from this plan or a single development-machine run.

## Evidence Record Contract

Each run must record:

1. Run ID, start/end time, verifier identity/version and profile.
2. Every source repository commit, relevant dirty-state statement and artifact digest.
3. Dependency/toolchain/configuration versions and redacted effective settings.
4. Dataset/snapshot identifiers, tenant/role setup and required preconditions.
5. Exact commands, exit codes, pass/fail/skip counts and reasons.
6. Relevant API traces, logs, browser/video/screenshots and persisted-state/effect observations.
7. Requirement and gate IDs with explicit evidence depth, expected/actual behavior and known limitations.
8. Content hashes, retention location, access policy and verification result.

Use durable controlled artifact storage for raw evidence. Commit the redacted manifest and stable references; ignored local `.audit-scratch` or `test-results` must not be the only retained release record. A screenshot cannot replace a persistent-state check, and a signed claim is not proof its inputs were honestly observed.

## Test Distribution

- Component unit tests follow the owning repository and may use clearly identified test doubles.
- Package/contract tests verify installed artifacts and public boundaries.
- Integration tests run real dependencies required by their claim, in disposable environments.
- Cross-app/browser/lifecycle tests run the selected suite artifacts through the real gateway/auth path.
- Independent negative controls ensure failed identity, missing effects and invalid evidence cannot be reported as success.

Use the current tests as migration inputs, not a claim that the new artifacts passed them. Remove root-path fixtures only after a reviewed replacement and equivalent observations exist. Test collection with zero selected required tests is a gate failure, not a successful run.

## Requirement Traceability

Maintain `requirement ID -> primary repo/domain -> app surfaces -> contract/artifact version -> required cases/depth -> executed run -> independent verdict`. Keep original ASPEII, CIP, IP, GN, WG, GUI, gap, competitive and REVA identifiers. A requirement spanning several repositories needs integrated evidence, not several source-file links.

## Handover Verdict

The release report states exactly which modules/profiles are qualified, unavailable, deferred or blocked. It lists test skips and residual risks. A partial first release is acceptable when scope is explicit; renaming it "100% suite complete" while optional or promised requirements remain unverified is not.
