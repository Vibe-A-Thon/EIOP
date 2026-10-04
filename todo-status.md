# EOIP Ticket Queue

**Snapshot:** 2026-10-04. Individual [tickets](tickets) own their state; this
table is their ordered rollup under [instruction](instruction.md).
P0-P3 are urgency priorities, not roadmap phases. ETAs are not agreed.

| Ticket | Title | Priority | Status | Accountable role | Dependency / next action |
|---|---|---|---|---|---|
| [ticket-20261004-004](tickets/ticket-20261004-004.md) | Restore executable source-bound validation receipts | P1 | Blocked | Senior Engineer | 45 focused tests pass; user authorizes publication, but source-bound full regression is blocked by concurrent edits; CI/review pending |
| [ticket-20261004-003](tickets/ticket-20261004-003.md) | Reconcile current MVP acceptance evidence and remaining gates | P1 | In Progress | QA Lead | Assess documentation and all 28 MVP rows; wrapper defect handed to ticket-20261004-004 |
| [ticket-20261004-001](tickets/ticket-20261004-001.md) | Implement user import API endpoint and tests | P2 | Blocked | Product Manager | Unverified proposal; source/spec/code references do not exist; obtain a scope decision before implementation |
| [ticket-20261004-002](tickets/ticket-20261004-002.md) | Synchronize EOIP coordination documents and ticket contracts | P1 | Done | Senior Engineer | Packet consistency verified; independent product acceptance not claimed |

**Active ticket:** ticket-20261004-004. **Next ticket:** ticket-20261004-003 after phase review.
Select the next dependency-ready ticket using [resume instructions](onboarding_prompts.md);
change context's role/persona when actually starting it.

## Milestone boundaries

- Coordination packet: scoped synchronization complete, not product completion.
- Phase 1/MVP: implementation/evidence reconciliation pending in ticket-20261004-003.
- Demo: prior bounded automated receipts exist; current deployment/journeys were
  not re-certified by this tooling phase.
- Release and full roadmap: not certified complete; no defensible total completion
  percentage is established here.

The earlier references to `ticket-20261005-002`, `ticket-20261006-003` and
`ticket-20261010-010` had no ticket files. They are retained as historical examples
in [memory](memory.md), not executable backlog, assigned commitments or agreed ETAs.
