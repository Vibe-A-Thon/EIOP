# EOIP Ticket Template

Use an unused `ticket-YYYYMMDD-NNN.md` ID. Follow [instruction](../instruction.md),
choose a role from [roles](../roles.md) and update [queue](../todo-status.md),
[checklist](../checklist.md) and [requirements map](requirements-map.md) together.
This file is a template, not a live ticket or backlog item.

```text
**ID**: <ticket-YYYYMMDD-NNN>
**Title**: <observable outcome>
**Priority**: <P0, P1, P2 or P3; urgency, not phase>
**Status**: <Open, In Progress, Blocked, Done or Cancelled>
**Accountable role**: <exact charter name>
**Phase**: <approved roadmap phase, coordination-only or unapproved proposal>
**Requirement IDs**: <real IDs or explicit non-product scope>
**Reporter**: <known identity/role or not recorded>
**Assignee**: <known identity/role or unassigned>
**Verifier**: <separate assigned reviewer or pending; no self-certification>
**Dependencies**: <existing ticket IDs and actual prerequisites, or none>
**ETA**: <agreed date or not agreed>
**Description**: <observed gap, intended behavior, evidence and scope>
**Doc code reference**: <real source/spec/code links and compatibility boundaries>
**Acceptance criteria**:
- <observable positive/negative behavior and measured threshold where applicable>
**Test plan**: <existing exact commands, prerequisites and expected outcomes>
**Files to modify**: <scoped files, preserving unrelated work>
**Failure / rollback / approval**: <explicit safety and human authority>
**Estimated effort**: <qualified estimate or not estimated>
**Evidence**: <revision/environment/commands/exit codes/receipts and verifier state>
**Remaining work / blockers**: <explicit missing acceptance or none within scope>
**Publication**: <not requested, pending approval, completed or failed>
**Change log**:
- <timestamp with timezone; transition, reason, evidence and synchronized surfaces>
```

Do not promote unsupported example requirements to implementation. Done requires
scoped acceptance evidence, not just populated fields; independent product/risk
approval stays pending until actually supplied.
