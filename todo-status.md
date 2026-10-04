# EOIP Ticket Queue

**Snapshot:** 2026-10-04. Individual [tickets](tickets) own their state; this
table is their ordered rollup under [instruction](instruction.md).
P0-P3 are urgency priorities, not roadmap phases. ETAs are not agreed.

| Ticket | Title | Priority | Status | Accountable role | Dependency / next action |
|---|---|---|---|---|---|
| [ticket-20261004-005](tickets/ticket-20261004-005.md) | Make the complete enterprise demo runnable in the web UI and console | P1 | In Progress | Senior Engineer | Full console now exits 0 (104/106 passed, 2 explicit skips); independent QA and live-stack verification pending |
| [ticket-20261004-004](tickets/ticket-20261004-004.md) | Restore executable source-bound validation receipts | P1 | Blocked | Senior Engineer | Source-bound full regression now PASS locally; remote CI, publication and independent review pending |
| [ticket-20261004-003](tickets/ticket-20261004-003.md) | Reconcile current MVP acceptance evidence and remaining gates | P1 | In Progress | QA Lead | MVP gap report active implementation gaps verified resolved locally; release/live/independent gates still pending |
| [ticket-20261004-001](tickets/ticket-20261004-001.md) | Implement user import API endpoint and tests | P2 | Blocked | Product Manager | Unverified proposal; source/spec/code references do not exist; obtain a scope decision before implementation |
| [ticket-20261004-002](tickets/ticket-20261004-002.md) | Synchronize EOIP coordination documents and ticket contracts | P1 | Done | Senior Engineer | Packet consistency verified; independent product acceptance not claimed |

**Active ticket:** ticket-20261004-005. **Next ticket:** return ticket-20261004-003
to its QA-owned acceptance work after the demo implementation handoff; ticket-004
remains blocked on remote CI, publication and independent review.
Select the next dependency-ready ticket using [resume instructions](onboarding_prompts.md);
change context's role/persona when actually starting it.

## Milestone boundaries

- Coordination packet: scoped synchronization complete, not product completion.
- Phase 1/MVP: MVP gap-report implementation closure is locally verified; release
  acceptance remains pending in ticket-20261004-003.
- Demo: demo artifacts and automated demo were run locally; current deployed/live
  journeys were not re-certified by this pass.
- Release and full roadmap: not certified complete; no defensible total completion
  percentage is established here.

The earlier references to `ticket-20261005-002`, `ticket-20261006-003` and
`ticket-20261010-010` had no ticket files. They are retained as historical examples
in [memory](memory.md), not executable backlog, assigned commitments or agreed ETAs.
