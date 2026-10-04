**Persona**: You are the Senior Engineer. Resolve EOIP's cross-component defects at their root while preserving tested contracts and behavior.

# EOIP Current Coordination Context

**Snapshot timestamp**: 2026-10-04T11:32:50.8200737+05:30
**Active role**: Senior Engineer
**Repo root**: F:\code\EOIP\EIOP
**Branch**: dev_local
**Last commit**: b54127245c7af1189082648c5bce9cc0e4579df7
**Active ticket**: none
**Last worked ticket**: ticket-20261004-002
**Last worked status**: Done
**Next ticket**: ticket-20261004-003
**Next role**: QA Lead
**Publication**: not requested

Branch/HEAD describe the observed checkout, not a commit of this session's edits.
Recheck Git state on resume; this is not a live automatically refreshed snapshot.

## Goal and scope

Continue evidence-backed EOIP delivery phase by phase while preserving demo
utility and local-first constraints. This session synchronized only the supplied
coordination packet and tickets; it did not re-audit every application file,
certify every phase or change the primary deployment.

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
Known passing receipts are historical; no application tests/builds were rerun in
this documentation session. Current failures, PRs and live readiness are not
freshly verified. Full product completion is not established.

## Working tree and next work

- The original coordination packet is tracked and modified; three new ticket/template
  files are untracked and all changes are left on disk.
- Only packet files are dirty at verification; prior web graph/layout work is
  untouched. Do not assume an earlier session's dirty list is still current.
- No branch switch, pull, commit, push, reset or deployment is authorized by this snapshot.
- Next: start [ticket-20261004-003](tickets/ticket-20261004-003.md) as QA Lead,
  reconcile newer source-bound/recovery receipts with acceptance/audits, then
  assign only verified gaps. Do not implement the blocked import proposal.

For exact queue/status see [todo-status](todo-status.md), gates see
[checklist](checklist.md), and field-level handoff rules see
[handoff template](handoff_template.md).
