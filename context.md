**Persona**: You are the Senior Engineer. Resolve EOIP's cross-component defects at their root while preserving tested contracts and behavior.

# EOIP Current Coordination Context

**Snapshot timestamp**: 2026-10-04T12:17:13.0324741+05:30
**Active role**: Senior Engineer
**Repo root**: F:\code\EOIP\EIOP
**Branch**: feature/audit-evidence-foundation
**Last commit**: e671ae884a11cd6cb2e4c6d11fcd90761326f5a9
**Active ticket**: ticket-20261004-004
**Last worked ticket**: ticket-20261004-004
**Last worked status**: Blocked
**Next ticket**: ticket-20261004-003
**Next role**: QA Lead
**Publication**: pending approval (phase publication authorized; review before next phase required)

Branch/HEAD describe the observed checkout, not a commit of this session's edits.
Recheck Git state on resume; this is not a live automatically refreshed snapshot.

## Goal and scope

The comprehensive documentation/application audit has begun. QA Lead verified
the empty validation wrapper and handed its implementation to Senior Engineer in
ticket-20261004-004. This first review phase restores trustworthy validation
tooling while the broader acceptance assessment remains In Progress.
The user selected canonical `Demo\demodata`, `Demo\script` and `Demo\autodemo`
paths because Windows cannot maintain three case-only root directories.
No full application certification or primary deployment change is claimed.

Follow [instruction](instruction.md), choose personas from [roles](roles.md)
and use [onboarding/resume prompts](onboarding_prompts.md). Preserve the two KGR
scope exclusions in instruction; no completion claim is made for excluded scope.

## Actual components

| Component | Existing location |
|---|---|
| API | [apps/api/main.py](apps/api/main.py) |
| Worker | [apps/worker/main.py](apps/worker/main.py) |
| MCP | [apps/mcp/main.py](apps/mcp/main.py) |
| Web user/admin UI | [apps/web](apps/web), [main.jsx](apps/web/src/main.jsx) |
| VS Code extension | [apps/vscode-extension](apps/vscode-extension) |
| Shared graph/contracts/ingestion/query/agents | [packages/eoip](packages/eoip) |
| Local deployment | [Compose manifest](deploy/docker-compose.yml), [wrapper](scripts/docker.ps1) |
| Requirements | [MVP requirements](EOIP-engg-doc-pkg/MVP-requirements.md), [traceability](EOIP-engg-doc-pkg/traceability/mvp-traceability.csv) |

The default inspected endpoints are web `http://localhost:8080/app`, API
`http://localhost:8000`, readiness `http://localhost:8000/health/ready` and MCP
`http://localhost:8001/mcp`. Runtime overrides must be checked without exposing
secrets. Readiness is not under `/api/v1`.

## Commands and evidence

Use the exact commands and approval/prerequisite classifications in
[agent runbook](agent_runbook.md). Existing venv path:
`F:\code\EOIP\EIOP\.venv\Scripts\python.exe`; configure it before Python execution.
Do not use generic `npm test`, `flake8`, fictitious shell scripts or assumed CI.

Latest handoff and historical receipts: [memory](memory.md#latest-handoff).
Current author checks: 45 focused tests pass, scoped Ruff passes, and ordinary
full Python regression has 1,106 outcomes (1,091 passed, 15 skipped, no failures
or errors). The full run overlapped edits and is not source-bound. Final
source-bound regression is Blocked by concurrent edits; the user explicitly
authorizes focused publication with that limitation. Remote CI is pending. See the
[phase test report](docs/validation-evidence-phase1.md). No UI/deployment/live
readiness or whole-product acceptance was freshly certified.

The [documentation audit](docs/audit-2026-10-04/gap-report.md) is explicitly
partial: 22 fully read, 1 partially read and 130 unread safe documents; all
109 core identifiers and all 28 MVP rows remain assessment_pending. Mechanical
identifier scans are not semantic review or verified requirement completion.

## Working tree and next work

- The startup working tree was clean; the previous coordination changes are now
  committed by another session. Fresh HEAD supersedes the old snapshot.
- After the authorized branch creation, both excluded KGR files appeared modified.
  These unrelated edits are not read, modified, staged or relied on.
- Concurrent edits also appeared in API/query/UI/test code and query specs;
  preserve them without staging. This phase owns only evidence tooling, CI and
  its audit/coordination documents. Do not fix or certify another session's changes.
- Phase branch/commit/PR are explicitly authorized by the user's latest request.
  GitHub CLI authentication is absent; GitHub MCP authentication is available.
  No reset, shared deployment or merge is authorized.
- Next: resume [ticket-20261004-003](tickets/ticket-20261004-003.md) as QA Lead
  only after phase PR review,
  reconcile newer source-bound/recovery receipts with acceptance/audits, then
  assign only verified gaps. Do not implement the blocked import proposal.

For exact queue/status see [todo-status](todo-status.md), gates see
[checklist](checklist.md), and field-level handoff rules see
[handoff template](handoff_template.md).
