**Persona**: You are the Senior Engineer. Resolve EOIP's cross-component defects at their root while preserving tested contracts and behavior.

# EOIP Current Coordination Context

**Snapshot timestamp**: 2026-10-04T20:21:37.8018964+05:30
**Active role**: Senior Engineer
**Repo root**: F:\code\EOIP\EIOP
**Branch**: feature/audit-evidence-foundation
**Last commit**: dea10fc1d0a4d5bb8923b253d5e2c4af723e1c6b
**Active ticket**: ticket-20261004-005
**Last worked ticket**: ticket-20261004-005
**Last worked status**: In Progress
**Next ticket**: ticket-20261004-003 QA acceptance work after the demo handoff
**Next role**: QA Lead
**Publication**: not requested for this audit update; prior phase publication/review remains pending

Branch/HEAD describe the observed checkout, not a commit of this session's edits.
Recheck Git state on resume; this is not a live automatically refreshed snapshot.

## Goal and scope

The current bounded assignment is ticket-20261004-005: completing the guided
enterprise demo and full console runner. The earlier comprehensive
documentation/application audit remains active under QA-owned ticket-20261004-003.
Its reports are audit artifacts, not independent release acceptance.
The user selected canonical `demo\demodata`, `demo\script` and `demo\autodemo`
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
Current continuation evidence: focused demo/RAG/LAYA/NLQ pytest command exited 0;
full console mode exited 0 with 104/106 passed, zero failures and two explicitly
unsupported query examples skipped. The guided-demo browser suite and web build
passed in the prior implementation pass and were not rerun here. Independent QA
and live-stack validation remain pending.
Historical evidence: Stable-source full regression passed at HEAD 47bc851: 1,207 outcomes (1,192 passed, 15 skipped, zero failures/errors), receipt test-results/audit-source-bound-validation.json (content-bound, not revision-bound). All five active gaps from docs/audit-2026-10-04/mvp-gap-report were verified resolved then (23 new NFR/security/e2e/performance tests pass; demo/autodemo 10/10). Demo script artifacts include `demo/script/walkthrough.md` and `demo/script/presentation.pptx`; the PPTX passed ZIP/XML structural validation, while artifact-tool visual rendering was unavailable because the bundled package was missing locally. The web build and VS Code extension host passed in prior runs; the extension receipt test-results/extension-host-dca6d363-9f4f-4d23-964f-c4b2b6a92c1c.json records 4/4 journeys. Remote CI and independent review remain pending; no publication performed. See [phase test report](docs/validation-evidence-phase1.md).

The fresh [full-document gap report](docs/audit-2026-10-04/full-doc-gap-report.md)
and [structured JSON](docs/audit-2026-10-04/full-doc-gap-report.json) opened 156
source Markdown/text files, excluding generated report self-input, the two KGR
documents and secret-like token content. It extracted 761 IDs/requirement-like
IDs: 108 Partial and 653 Missing under a conservative policy with zero Done
without current full acceptance and independent review. The prior
[partial documentation audit](docs/audit-2026-10-04/gap-report.md) remains a
dated bounded artifact.

## Working tree and next work

- HEAD observed for this pass is `dea10fc1d0a4d5bb8923b253d5e2c4af723e1c6b`.
  The branch has many pre-existing modified and untracked files; all were
  preserved. This continuation changed the RAG/LAYA implementation, NLQ fixture,
  focused tests and ticket/coordination handoff records. No files were staged.
- Current owned dirty/untracked scope includes the VS Code extension test runner
  environment fix, MVP report synchronization, demo artifacts, active-gap tests
  and coordination updates. Additional tracked modifications observed outside
  this pass: `deploy/Dockerfile`, `packages/eoip/demo.py`,
  `packages/eoip/demo_scenarios.py`, `tests/e2e/test_clean_recovery.py` and
  `tests/e2e/test_enterprise_demo_scenarios.py`; preserve them for coordination.
  A failed presentation-tool setup left `.tmp/presentation-build/package.json`;
  removal was blocked by command policy. No staged files were observed before
  this handoff.
- No branch switch/create, commit, push, PR, reset, shared deployment, dependency
  install, live source/model access or Docker reset was performed.
- Next: hand off ticket-20261004-005 for independent QA and authorized live-stack
  verification. Keep ticket In Progress pending that review; then resume
  QA-owned ticket-20261004-003. Ticket-004 remote CI/publication/review blockers
  remain separate.

For exact queue/status see [todo-status](todo-status.md), gates see
[checklist](checklist.md), and field-level handoff rules see
[handoff template](handoff_template.md).
