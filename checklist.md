# EOIP Coordination and Completion Checklist

**Snapshot:** 2026-10-04. Status comes from real [tickets](tickets) and evidence,
not the former "Phase 1 Complete" template label.

## Ticket rollup

| Ticket | Title | Priority | Status | Accountable role |
|---|---|---|---|---|
| [ticket-20261004-004](tickets/ticket-20261004-004.md) | Restore executable source-bound validation receipts | P1 | Blocked | Senior Engineer |
| [ticket-20261004-003](tickets/ticket-20261004-003.md) | Reconcile current MVP acceptance evidence and remaining gates | P1 | In Progress | QA Lead |
| [ticket-20261004-001](tickets/ticket-20261004-001.md) | Implement user import API endpoint and tests | P2 | Blocked | Product Manager |
| [ticket-20261004-002](tickets/ticket-20261004-002.md) | Synchronize EOIP coordination documents and ticket contracts | P1 | Done | Senior Engineer |

## Coordination gate (ticket-20261004-002)

- [x] Read all supplied coordination files and existing ticket content.
- [x] Align roles/personas with the 55-charter [catalog](roles.md).
- [x] Establish authoritative files, common status rules and coherent handoffs.
- [x] Replace placeholder services/commands/branch with inspected repository values.
- [x] Repair onboarding/template/architecture pointers and add a real ticket template.
- [x] Qualify unsupported import/PR/ETA/test claims; retain ticket history.
- [x] Reconcile all real ticket rows in queue/checklist/requirements map.
- [x] Validate local links, ticket metadata/rollups, active/next state, persona
  and populated handoff. Whitespace check passes.
- [x] Preserve unrelated source changes; no reset, rebuild, commit or push.

This gate is author-executed document consistency verification, not independent
application/QA certification.

## Audit evidence foundation (ticket-20261004-004)

- [x] Confirm empty validation producer and reproduce missing execution behavior.
- [x] Restore argument-vector command execution and failure/source/artifact receipts.
- [x] Verify output ownership and Git metadata protections with failed-first tests.
- [x] Run 45 focused tests and scoped Ruff successfully.
- [x] Run ordinary full Python regression: 1,091 passes, 15 skips, no failures/errors.
- [ ] Run final source-bound full regression against stable sources: Blocked by
  concurrent unrelated edits; user authorizes focused publication instead.
- [x] Define existing-extras CI and validate YAML structure.
- [ ] Observe a passing remote CI run; workflow presence is not proof.
- [ ] Publish phase PR and obtain review before proceeding.

See the [phase test report](docs/validation-evidence-phase1.md). The
[partial documentation audit](docs/audit-2026-10-04/gap-report.md) does not claim
all documents read or all requirements verified.

## Product acceptance gates (ticket-20261004-003)

- [x] Open/read the allowed source Markdown/text corpus for a full documentation
  gap scan, excluding the two KGR files and withholding secret-like token content.
- [x] Persist conservative structured JSON and Markdown gap artifacts:
  [full-doc-gap-report.json](docs/audit-2026-10-04/full-doc-gap-report.json)
  and [full-doc-gap-report.md](docs/audit-2026-10-04/full-doc-gap-report.md).
- [ ] Reconcile newest receipts and source binding against current HEAD/dirty scope.
- [ ] Evaluate all 28 MVP traceability rows against actual acceptance behavior;
  separate missing annotations from missing implementation.
- [ ] Reconcile newer webhook/memory/audit/trace recovery evidence with older audits.
- [ ] Verify current admin and packaged/live VS Code journeys where claimed.
- [ ] Verify real local-model inference and core no-model utility where claimed.
- [ ] Verify live-source/attachment coverage; label fixture-only integrations.
- [ ] Verify native/crash-consistent recovery and measured RPO/RTO where required.
- [ ] Verify SBOM/licenses, offline/no-egress and hardware-backed performance gates.
- [ ] Assign remaining verified gaps to owned, phased, dependency-aware tickets.
- [ ] Obtain independent QA/risk and designated human release approval.

Unchecked items are assessment/acceptance obligations, not proof their code is
absent. See [requirements map](tickets/requirements-map.md) and
[memory evidence notes](memory.md#evidence-observed-not-rerun) for bounded history.
The full-document gap report extracted 761 IDs/requirement-like IDs: 108 Partial,
653 Missing and zero Done under the conservative policy; those labels are audit
triage and not independent product acceptance.
