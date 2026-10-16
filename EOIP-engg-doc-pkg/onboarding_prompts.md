# EOIP Onboarding and Resume Prompts

Canonical workflow: [instruction](instruction.md). Canonical personas:
[roles](roles.md). This file is the actual onboarding pointer; there is no
separate `agent_prompts.md`.

## One-time prompt: ONBOARD-AND-RECONCILE

```text
Read instruction.md, context.md, memory.md, todo-status.md, checklist.md,
roles.md, agent_runbook.md, onboarding_checklist.md, onboarding_prompts.md,
handoff_template.md, tickets/requirements-map.md, tickets/ticket-template.md
and existing ticket files.

Respect the two KGR scope exclusions in instruction.md. Read only the selected
work's applicable product specifications and code beyond this packet.

Verify actual repository root, branch, HEAD, dirty files, command prerequisites
and component paths. Do not assume main, fabricate PRs/ETAs or copy example data
into live status. Preserve valid existing records; reconcile stale/conflicting
claims with explicit evidence and history.

Select a charter from roles.md matching the assignment and use its exact persona
in context.md. Record a session start in memory.md and select a real,
dependency-ready ticket from todo-status.md. Create tickets only for verified
gaps or clearly labelled proposals using tickets/ticket-template.md; do not
force three tickets or implement unsupported example requirements.

Keep ticket state, requirements-map.md, todo-status.md and checklist.md aligned.
Use the real commands and safety classifications in agent_runbook.md.
Do not run full tests, install tools, change branches, ingest demo data or
modify the shared deployment just to fill in templates.

Before stopping, update context.md and append the handoff_template.md block
to memory.md. Link that latest handoff from context.md. Record actual checks,
historical evidence, limitations, remaining approvals and exact next actions.
Validate links and ticket/persona/status consistency.

Do not commit, push, publish or deploy unless explicitly requested/approved.
Persist scoped edits in the working tree and record publication status.
```

## Short resume prompt

`continue from left over`

1. Follow the read contract in [instruction](instruction.md).
2. Read context's snapshot and the latest handoff in [memory](memory.md).
3. Compare actual Git state, ticket state, evidence timestamps and dependencies.
   Stop on conflicting shared-file changes; otherwise preserve unrelated work.
4. Resume the active ticket if it is In Progress and ready. If none is active,
   select the highest-priority dependency-ready Open ticket. For a Blocked ticket,
   verify the blocker is resolved before resuming; do not skip approvals.
5. Use a role appropriate to that ticket from [roles](roles.md), updating the
   active persona explicitly. Complete a bounded coherent slice and verify it.
6. Update ticket/queue/map/checklist and context/memory together. Do not reopen
   onboarding or automatically create/publish a branch.

## Explicit bounded assignment

```text
Resume work on ticket: <existing ticket ID>
Role: <exact role charter name>
Goal: <observable acceptance outcome>
Max work for this session: <one to three bounded actions>
Approvals: <explicit permissions; none implied by role>
```

Unknown or missing information is a documented blocker, not automatically a P0
defect. Priority must reflect actual impact. All completion and publication rules
come from [instruction](instruction.md), not from a shortened prompt.
