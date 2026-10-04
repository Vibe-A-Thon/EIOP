**Persona**: You are the QA Lead. Own EOIP's independent validation coverage, requirement evidence and honest release/demo gates.

# EOIP Current Coordination Context

**Snapshot timestamp**: 2026-10-04T12:31:12.2191665+05:30
**Active role**: QA Lead
**Repo root**: F:\code\EOIP\EIOP
**Branch**: feature/audit-evidence-foundation
**Last commit**: cb36bb667d02323617010361e277b0d2f9880fd0
**Active ticket**: ticket-20261004-003
**Last worked ticket**: ticket-20261004-003
**Last worked status**: In Progress
**Next ticket**: ticket-20261004-004 blocker resolution / phase review, then scoped implementation tickets
**Next role**: QA Lead / Senior Engineer as assigned by ticket
**Publication**: not requested for this audit update; prior phase publication/review remains pending

Branch/HEAD describe the observed checkout, not a commit of this session's edits.
Recheck Git state on resume; this is not a live automatically refreshed snapshot.

## Goal and scope

The comprehensive documentation/application audit is active under
ticket-20261004-003. The allowed Markdown/text corpus was opened for a fresh
structured scan, excluding the two KGR files and withholding secret-like example
token content. The new full-document report is an audit artifact, not
implementation or independent release acceptance.
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
Historical author checks: 45 focused tests pass, scoped Ruff passes, and ordinary
full Python regression has 1,106 outcomes (1,091 passed, 15 skipped, no failures
or errors). The full run overlapped edits and is not source-bound. Final
source-bound regression is Blocked by concurrent edits; the user explicitly
authorizes focused publication with that limitation. Remote CI is pending. See the
[phase test report](docs/validation-evidence-phase1.md). No UI/deployment/live
readiness or whole-product acceptance was freshly certified.

The fresh [full-document gap report](docs/audit-2026-10-04/full-doc-gap-report.md)
and [structured JSON](docs/audit-2026-10-04/full-doc-gap-report.json) opened 156
source Markdown/text files, excluding generated report self-input, the two KGR
documents and secret-like token content. It extracted 761 IDs/requirement-like
IDs: 108 Partial and 653 Missing under a conservative policy with zero Done
without current full acceptance and independent review. The prior
[partial documentation audit](docs/audit-2026-10-04/gap-report.md) remains a
dated bounded artifact.

## Working tree and next work

- HEAD advanced during this session from `cbef5d392e3d395d1e9aeeac24b4ae67e55801b8`
  to `cb36bb667d02323617010361e277b0d2f9880fd0` by another session. The new
  commit message is "kgr changes and new export formats for interactive HTML and
  graph report implemented"; this audit did not certify those changes.
- Current unrelated dirty files observed: `apps/api/app.py`,
  `tests/unit/test_kgr_ai_intelligence.py` and
  `tests/unit/test_kgr_competitive_parity.py`. Preserve them unstaged unless
  their owner assigns them to this work.
- This session owns only `docs/audit-2026-10-04/full-doc-gap-report.md`,
  `docs/audit-2026-10-04/full-doc-gap-report.json` and synchronized
  coordination/handoff edits.
- No branch switch/create, commit, push, PR, reset, shared deployment, dependency
  install, live source/model access or broad test run was performed.
- Next: review the full report, decide which Missing/Partial items are active for
  the current phase, create scoped implementation tickets, and run stable
  source-bound validation before any Done or release claim.

For exact queue/status see [todo-status](todo-status.md), gates see
[checklist](checklist.md), and field-level handoff rules see
[handoff template](handoff_template.md).
