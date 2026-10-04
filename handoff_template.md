# EOIP Handoff Template

Append a populated block to [memory](memory.md); update [context](context.md)
and link to that latest block. Do not duplicate history in both files.
Use real values; placeholders below are for the template only.
Follow [instruction](instruction.md), [roles](roles.md) and [runbook](agent_runbook.md).

```text
--- HANDOFF START ---
Timestamp: <ISO timestamp with timezone>
Role: <exact charter name>
Persona: <exact charter persona text>
Repository root: <actual absolute local path>
Branch: <actual branch, or detached HEAD explicitly>
Last commit: <actual full HEAD; not a promise changes were committed>
Working tree: <scoped changes and unrelated dirty files preserved>
Current ticket: <active ticket ID and status, or none>
Last worked ticket: <ticket ID and status>
Checks executed: <exact commands, exit codes and actual results>
Historical evidence: <receipt paths, source/environment and limitations>
Checks not executed: <what remains unverified>
Blockers / approvals: <explicit requirements or none within this scope>
Next ticket / owner: <existing ID, exact charter, verifier still required>
Next actions:
  1. <exact command or precise task and existing file/section>
  2. <exact command or precise task and existing file/section>
  3. <exact command or precise task and existing file/section>
Reproduction / validation commands: <exact applicable runbook commands>
Deployment changes: <actual changes, or none>
Publication: <not requested, pending approval, completed or failed>
Completion boundary: <scope verified; product/phase gates still open>
--- HANDOFF END ---
```

For a documentation-only task, record link/status/format checks and explicitly
state application tests were not rerun. For application work, preserve receipt
locations and failing/skipped checks. Never invent a successful test execution,
PR, branch or commit. Line references are optional and must be current; stable
file/section references are preferable to stale hardcoded line numbers.
