# Documentation Review and Handover Findings

Date: 2026-10-18. Scope: repository documentation refresh based on current working-tree source, configuration, deployment/test definitions and a reproducible static inventory. This is not a certification of every feature or an exhaustive line-by-line semantic audit of all code.

Continuation review: 2026-10-19. The working tree changed concurrently during this task, including REVA code/workflows and competitive research. Those additions were preserved. A bounded review of REVA's settings, host mount, router lifecycle, CLI and packaging is recorded in its [component guide](../reva/README.md); its separate completion ledger was not independently validated here.

## Coverage and Method

The initial Git census contained 2,888 tracked files. The repository also contains nonignored working files, ignored local state and dependencies. [repository_inventory.py](../scripts/repository_inventory.py) inventories Git-listed tracked/nonignored untracked paths, reads in-scope UTF-8 text fully, hashes content and statically parses Python definitions/imports/route candidates without executing inspected modules. [Generated inventory](generated/README.md) records exact counts, paths, hashes, exceptions and generation/source identity. JavaScript/TypeScript are mechanically read, not fully semantically parsed.

Potential credentials, runtime/dependency directories, symlinks, oversized files and the inventory itself are explicitly excluded. Binary content is hashed, not semantically reviewed. Ignored files are not silently counted as audited. Reading all bytes does not mean every behavior was analyzed; full requirement closure still needs the programme's independent runtime evidence.

Direct review covered the root/current guides, all originally tracked README documents, both frontend entry points/auth/transport/navigation, API factory/security boundary, graph backend resolution, worker dispatch/retry/lease behavior, MCP gateway, package manifests, container launch/build/proxy configuration, backup/restore entry points, CI, pytest bootstrap, release-gate CLI and relevant evidence tools.

## Documentation Changes

Added a task-oriented documentation index; component READMEs for apps, API, worker, MCP, web, alternate frontend, preview backend, shared packages, connectors, configuration, schemas, deployment, scripts, tests, tools, benchmarks, data, research, compliance, licenses and historical notes; and detailed guides for configuration, operations, frontend reconciliation, testing, migration/refactoring and documentation maintenance.

Updated existing project/demo/research READMEs with maintenance paths and qualification limits. Corrected the enterprise scenario pack description from 1.1.0/11/70/114 to the inspected 1.2.0/13/80/134 source inventory. Corrected stale extension coverage wording and schematic JSON labeling. Updated the root/current guides without discarding pre-existing working-tree changes.

The README inside `demo/demodata/core/demo-repo` was read but intentionally preserved: it is ingested fixture content and changing it can alter captured hashes/demo commits. Its current maintenance boundaries are documented in the parent demo guide. Historical audit reports, normative requirements and legal license texts were not rewritten to manufacture current results.

## Implementation Risks Still Open

| Finding from source inspection | Consequence | Handover action |
|---|---|---|
| Two substantial frontends with different hosts, routers, clients and design systems | Editing one does not necessarily change the default deployed UI | Reconcile routes and actual behavior before suite extraction; preserve unique functionality |
| Alternate frontend creates a bootstrap-admin UI principal on identity lookup failure | UI can describe authority it has not established; this is not a demonstrated backend escalation finding | Fix fail-closed identity handling in a separately tested implementation change |
| Release-gate CLI wires document checking, not full independent release evaluation | Zero exit or helper-created receipts can be misinterpreted as certification | Implement/review actual evidence collection/verification; do not rely on parsed-but-unwired options |
| Release checklist previously labeled every gate passed without a release-bound run | Maintainers could mistake documentation for evidence | Replaced with unverified requirements and exact CLI limitations |
| API/worker memory graph instances are process-local | Separate processes cannot share graph writes through the file data root | Use the same persistent backend for integrated ingestion |
| Filesystem worker and optional advisory leader lease | Multi-host durability/exactly-once effects not established by a topology file | Qualify durable claims, fencing/recovery and effect checks before scaling |
| Worker demo loading defaults true | Unintended synthetic content in a non-demo deployment | Explicitly disable and verify startup behavior |
| Basic backup helper stops worker but not all writers | Consistency is not guaranteed under concurrent API/vendor writes | Quiesce all writers and verify isolated recovery before relying on the backup |
| Existing runtime/scratch files remain tracked | Ignore rules do not untrack historical content; some acceptance tests reference baseline files | Plan fixture relocation, retention and index cleanup separately; no deletion performed here |
| Advanced modules, route families and neural tiers have incomplete qualification | Names/screens/registrations can overstate production readiness | Keep owning ASPEII/CIP/IP/GN/WG/GUI gates open until independent evidence exists |
| New REVA mount suppresses errors, exposes a static health response and does not initialize the warrant kernel in the inspected factory | Host health does not demonstrate REVA readiness; caller-provided tenant/principal headers need trusted binding review | Keep deployment unqualified pending lifecycle, clean packaging, key management and authorization verification; see component guide |

These are handover risks discovered during documentation work, not a complete security or code-review report. Application behavior was not changed to address them in this refresh.

## Validation and Boundaries

The inventory tooling has focused tests for path/secret exclusion, nonexecution of inspected code, binary/syntax-error reporting and avoiding source-value disclosure. Documentation validation checks local references and whitespace; remote links, live vendor integrations, deployment safety and every requirement's acceptance remain separate work.

The existing broad Markdown checker has historical exclusions and simple parsing. Report its actual outcome separately from checks of changed documentation. Do not interpret documentation or inventory tests as full product regression. Retain current command results in the task closeout and regenerate the inventory after settled edits.

### Executed Checks

The focused documentation/tooling run completed with **49 passed, 1 skipped and 2 warnings**. It selected `tests/unit/test_repository_inventory.py`, `tests/unit/test_documentation_audit.py` and `tests/unit/test_qa_gate_integrity.py` with `-o addopts= -q -ra`. The skip explicitly requires the separately enabled `eoip.qa.pytest_plugin`; it was not counted as a pass. Warnings concerned a dataclass collected as a test candidate and Starlette/httpx deprecation. Local receipts are `test-results/documentation-refresh-final.xml` and `test-results/documentation-refresh-final-receipt.json`; these ignored runtime paths are not promised as committed handover artifacts.

The broad link checker passed after adding the REVA component guide: 1,248 Markdown files, 382 local links, zero broken links within that checker's scope. A separate check of the 55 edited documentation files resolved 297 local links with zero broken targets. Ruff for the inventory tool/tests and `git diff --check` also passed. The release-checklist CLI reported its document/ID-presence check passed; this did **not** run release qualification. Re-run the documented checks after further edits; generated inventory counts belong to the timestamped JSON snapshot, not a fixed total in this report.

No full application regression, live vendor integration, production deployment, backup/restore exercise or independent REVA acceptance run was performed for this documentation refresh. No product-runtime code was edited by this task. Concurrent changes and a sequential inventory scan mean the snapshot is not an atomic capture of a frozen checkout.

## Recommended Next Work

1. Resolve trusted identity behavior and release-verifier limitations with real positive/negative tests.
2. Execute the suite plan's route/ownership baseline, reconciling both frontends.
3. Establish profile-specific persistence/recovery and connector qualification evidence.
4. Migrate required baseline fixtures out of scratch before any tracked-runtime cleanup.
5. Maintain component docs and evidence links in every behavior-changing pull request using [documentation policy](documentation-policy.md).
