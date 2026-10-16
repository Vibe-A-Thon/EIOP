# EOIP Agent Orchestration Instructions and Contracts

**Goal:** Deliver the documented EOIP application phase by phase, preserving a
working local demo while closing functional, nonfunctional and acceptance gaps.
Completion requires evidence, not code presence or a persona's assertion.

**Scope:** Repository coordination, audits, implementation, validation and handoff.
This is the canonical workflow contract; [roles](roles.md) are the canonical role
catalog. Neither document overrides the master constraints, execution permissions
or an explicit user scope/approval decision.

## Sources of truth and synchronization

| Subject | Authoritative file | Other files' responsibility |
|---|---|---|
| Product constraints and phase scope | [Master specification](source-master-prompt.txt), [MVP requirements](MVP-requirements.md), [roadmap](66-phase-roadmap.md) | Link requirements; never silently rewrite scope |
| Roles, persona text and ownership | [roles.md](roles.md) | Copy only the active persona; link the catalog instead of duplicating role lists |
| Workflow, safety and status rules | [instruction.md](instruction.md) | Onboarding/runbook/templates must follow this contract |
| Ticket details and status | Individual tickets in [tickets](tickets) | Roll up exact ID/title/status/owner/priority; do not invent tickets |
| Requirement mappings | [requirements-map.md](tickets/requirements-map.md) and [MVP traceability](traceability/mvp-traceability.csv) | Track only real IDs and qualified evidence |
| Prioritized queue | [todo-status.md](todo-status.md) | Derive from existing tickets, dependencies and evidence |
| Gate checklist | [checklist.md](checklist.md) | Distinguish coordination completion from product acceptance |
| Current session snapshot | [context.md](context.md) | Use actual branch/HEAD/role and verified paths |
| Session history and last handoff | [memory.md](memory.md) | Preserve qualified history; mark stale/example material explicitly |
| Startup/resume procedure | [onboarding_prompts.md](onboarding_prompts.md), [onboarding_checklist.md](onboarding_checklist.md) | Reference the same files, queue and permissions |
| Commands and operating cautions | [agent_runbook.md](agent_runbook.md) | Use existing repository tools; qualify side effects |
| Handoff and ticket formats | [handoff_template.md](handoff_template.md), [ticket-template.md](tickets/ticket-template.md) | Populate actual values; placeholders belong only in templates |

When sources disagree, record the conflict and resolve it against specifications,
actual code and receipts. A stale summary must not overwrite newer verified
evidence. Unknown status, owner, ETA, PR or test results must be labelled unknown,
not fabricated. Application completion percentage is unknown until the approved
requirement/gate assessment supports it.

## Read and scope contract

At session start read this file, [context](context.md), [memory](memory.md),
[todo-status](todo-status.md), [checklist](checklist.md), [roles](roles.md), the
[runbook](agent_runbook.md), the [onboarding prompts](onboarding_prompts.md),
[onboarding checklist](onboarding_checklist.md), [handoff template](handoff_template.md),
[requirements map](tickets/requirements-map.md), [ticket template](tickets/ticket-template.md)
and existing ticket files. Read the selected task's applicable specs/code before
changing it. Do not claim an entire repository audit from reading this packet.

Retain the user's existing scope exclusions unless explicitly changed:
[KGR requirements](KGR-requirements.md) and
[KGR implementation plan](KGR-implementation-plan.md)
must not be read, audited or changed under this coordination workflow.
They are exclusions, not claims that their obligations have been completed.
Report any resulting full-product assessment limitation.

## Role and execution contract

Use an exact charter name from [roles](roles.md), or its documented CTO alias,
and the charter's exact persona text at the top of [context](context.md).
Assign one accountable role and identify the implementer, verifier and required
human approver in each ticket. Role assignment is not application RBAC or runtime
agent permission. All 55 charters remain available; activate only needed roles.

Preserve local-first operation, HugeGraph authority, no-cloud/no-external-LLM MVP,
deterministic fallbacks, provenance, read-only MVP AI/MCP and no MVP RBAC.
URL namespaces are not authorization. Apply the detailed constraints in
[roles](roles.md); do not duplicate or weaken them in onboarding prompts.

## Ticket and status contract

Use `ticket-YYYYMMDD-NNN.md`, with an unused ID, and the
[ticket template](tickets/ticket-template.md). Create a ticket only for a verified
gap or clearly labelled proposal; do not force three tickets during onboarding.
Preserve existing ticket history when correcting unsupported examples.

Statuses: **Open**, **In Progress**, **Blocked**, **Done**, **Cancelled**.
Priority P0/P1/P2/P3 expresses urgency, not roadmap Phase 0/1/2/3.

- Open -> In Progress: assign an owner, inspect dependencies and record session start.
- In Progress -> Blocked: record concrete missing evidence/access/decision and next owner.
- Open/Blocked -> In Progress: record resolution and resume only within approved scope.
- In Progress -> Done: satisfy all scoped acceptance criteria, attach evidence and
  record verifier status. Independent verification cannot be claimed by the author.
- Any state -> Cancelled: retain rationale/history; it is not a completed requirement.
- Done -> Open: document the regression/reopened acceptance criterion and evidence.

On every transition update the ticket change log, [todo-status](todo-status.md),
[checklist](checklist.md) and relevant [requirement mapping](tickets/requirements-map.md)
as one coherent change. Before stopping, reconcile current [context](context.md)
and [memory](memory.md). No active ticket may reference a missing file.

## Verification, safety and publication

Inspect the working tree before edits; preserve unrelated changes. Use existing
tests/builds for changed application surfaces and check documentation links,
ticket rollups, persona consistency and command paths for documentation changes.
Declare checks not run; a historical receipt is not fresh current-HEAD validation.
Commands that initialize/rebuild, ingest/replay, stop services, restore, install
dependencies, change branches or modify shared data require their stated scope
and approval. Never print credentials from local environment/secret files.

Do not automatically create/switch branches, pull, commit, push or publish a PR
as part of onboarding or a resume prompt. Only do those actions when explicitly
requested/approved. Stage exact scoped files, never the whole dirty repository.
Record publication as **not requested**, **pending approval**, **completed** or
**failed**, with actual evidence. A persona cannot authorize publication.

## Session lifecycle and handoff

1. Read the packet and current ticket; record the start timestamp/role in memory.
2. Verify actual branch/HEAD, paths, dependencies and dirty-file ownership.
3. Select the highest-priority dependency-ready verified ticket, or the explicitly
   requested task. For `continue from left over`, use the resume procedure below.
4. Implement/verify within scope; update state and evidence without inflating coverage.
5. Update context's snapshot and append the canonical handoff to memory. Context
   links to that latest handoff rather than keeping a second drifting history.
6. Reconcile packet links, ticket summaries and commands; report remaining blockers.
7. Commit/push only if approved; otherwise leave scoped changes in the working tree
   and state that explicitly.

Use the [handoff template](handoff_template.md): current/last-worked ticket status,
role, branch/HEAD, dirty scope, exact commands, results/receipts, limitations,
next actions and publication/approval state. Missing evidence makes the handoff
incomplete, not implicitly successful.

## Resume prompt

`continue from left over`

Read context and the latest memory handoff, reconcile them with Git and the ticket
queue, and continue the next dependency-ready action. Do not rerun onboarding,
invent a branch, reset the demo or assume old tests still certify current sources.
For an explicit assignment use:

```text
Resume work on ticket: <existing ticket ID>
Role: <charter name>
Goal: <observable acceptance outcome>
Max work for this session: <bounded actions>
```

Workflow changes are permitted when explicitly requested, as in this packet
synchronization. Update dependent runbooks/prompts/templates in the same change;
agents must not independently weaken enforcement rules to make their work pass.
