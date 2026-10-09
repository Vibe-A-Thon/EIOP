# EOIP Agent Runbook

Follow [instruction.md](instruction.md); select roles from [roles.md](roles.md).
Current values belong in [context.md](context.md), history in [memory.md](memory.md).

## Start, work and stop

1. Complete [onboarding checklist](onboarding_checklist.md) or the
   [resume procedure](onboarding_prompts.md); inspect the working tree.
2. Select a real ticket from [todo-status](todo-status.md); verify requirements,
   dependencies, acceptance and approvals. Do not create work from placeholder examples.
3. Transition ticket status using [instruction](instruction.md); update its log,
   queue, [checklist](checklist.md) and [requirements map](tickets/requirements-map.md).
4. Run the smallest relevant existing checks and capture commands/exit codes.
5. Update context, append the [handoff](handoff_template.md) to memory and check consistency.
6. Publish only with explicit approval; otherwise record working-tree persistence.

## Verified repository command catalog

Run from the repository root in Windows PowerShell. Paths/entry points below
were inspected on 2026-10-04; their presence is not a claim every command was
executed in this documentation session. Honor exit codes. Do not chain with
PowerShell 7-only operators. Resolve/configure the existing Python interpreter
before Python execution; do not install dependencies just to populate templates.

| Purpose | Exact command | Prerequisites / side effects |
|---|---|---|
| Inspect branch | `git branch --show-current` | Read-only; do not assume main |
| Inspect revision | `git rev-parse HEAD` | Read-only; record dirty state separately |
| Inspect dirty files | `git --no-pager status --short` | Read-only |
| Whitespace check | `git --no-pager diff --check` | Does not check untracked documentation; also inspect it |
| Python unit tests | `& .\.venv\Scripts\python.exe -X utf8 -m pytest -q tests\unit` | Existing configured venv required; writes caches |
| Targeted temporal/recovery tests | `& .\.venv\Scripts\python.exe -X utf8 -m pytest -q tests\unit\test_graph_evolution.py tests\e2e\test_clean_recovery.py` | Existing venv; use only when relevant |
| Full Python regression | `& .\.venv\Scripts\python.exe -X utf8 -m pytest -q --junitxml=test-results\coordination-regression.xml` | Explicit broader validation; creates/replaces this receipt |
| Source-bound Python regression | `& .\.venv\Scripts\python.exe -X utf8 -m scripts.validate_with_evidence --project-root . --output test-results\audit-source-bound-validation.json --artifact test-results\audit-full-regression.xml -- .\.venv\Scripts\python.exe -X utf8 -m pytest -q --junitxml=test-results\audit-full-regression.xml` | Existing venv/Git; runs the explicit command, refuses stale artifacts or source/HEAD drift, creates XML and JSON receipts |
| Python lint | `& .\.venv\Scripts\python.exe -m ruff check packages apps scripts tests` | Narrow to changed paths for small changes |
| Web build | `npm --prefix apps\web run build` | Existing node_modules required; writes web build output |
| Extension host tests | `npm --prefix apps\vscode-extension test` | Installed dev dependencies; may download/launch VS Code; approve network/runtime requirements first |
| Existing Compose status | `& .\scripts\docker.ps1 status` | Docker daemon and existing local configuration; no initialization |
| API readiness | `(Invoke-WebRequest -UseBasicParsing http://localhost:8000/health/ready).Content` | Running local API; read-only and unauthenticated; nondefault ports must be reconciled |
| Local start/rebuild | `& .\scripts\docker.ps1 up` | Approval required; may create local secrets, build images and load demo data |
| Combined Docker regression/smoke/UI | `& .\scripts\docker.ps1 test` | Running configured stack; builds/runs test services and exercises demo APIs |
| Isolated graph acceptance | `& .\scripts\docker.ps1 acceptance` | Docker/configuration required; builds fresh HugeGraph fixtures; wrapper cleans only its disposable project |
| Isolated application recovery | `& .\scripts\docker.ps1 recovery-acceptance` | Same isolation requirement; synthetic model/source fixtures are not live inference/tenant certification |
| Isolated DLQ acceptance | `& .\scripts\docker.ps1 dlq-acceptance` | Builds disposable upstream/API/worker/graph fixtures |
| MVP evidence mapping | `& .\.venv\Scripts\python.exe -X utf8 -m scripts.verify_requirement_evidence . EOIP-engg-doc-pkg\traceability\mvp-traceability.csv test-results\temporal-compatibility-full.xml --output test-results\coordination-requirement-evidence.json` | Uses an existing historical JUnit; output is not current-source certification; exit 1 means evidence gaps, not success |

The actual tooling is defined in [pyproject.toml](pyproject.toml),
[web package manifest](apps/web/package.json),
[extension package manifest](apps/vscode-extension/package.json) and
[Docker wrapper](scripts/docker.ps1).
[Validation evidence CI](.github/workflows/validation-evidence.yml) installs the
existing development extras, runs scoped evidence-tooling lint and the full
Python suite on Windows/Python 3.11, and retains receipts even on failure.
Its presence is not a passing CI result; observe the published run separately.

The [validation wrapper](scripts/validate_with_evidence.py) requires an explicit
argument vector after `--`; it does not run a shell or deploy implicitly. Do not
put credentials in command arguments, which are recorded. Environment values
and child stdout/stderr are not stored in receipts. Source fingerprints omit the
two KGR exclusions, secret/environment paths, runtime/dependency directories and
declared output artifacts. Outputs cannot overwrite protected or Git-tracked
source, including paths newly staged by the child command. Freshness requires a
changed artifact state and a modification timestamp at/after command start.
Dirty checkouts can be content-bound, not immutable revision-bound. Before/after
snapshots cannot detect transient edits that are reverted during execution.
Command success/fresh artifacts do not certify artifact semantics, requirement
completeness, live integrations or independent QA acceptance.

For deployment/backup/restore details consult the [local Docker guide](docs/docker-local.md).
Do not run primary backup/restore/reset commands merely as a routine handoff step.
Never expose local secret values in tracking files or logs.

## Naming and publication

- Ticket: `ticket-YYYYMMDD-NNN.md`; canonical [template](tickets/ticket-template.md).
- Optional approved branch: `feature/<ticket-ID>` or
  `onboarding/<role-slug>-YYYYMMDD`; do not create/switch it automatically.
- Approved commit: `<ticket-ID>: <scoped description>`; stage explicit files and
  include required attribution. Confirm only intended content is staged.
- Push/PR/deployment: separate explicit approval; record actual result, not planned state.
- A failed command, missing prerequisite or blocked approval must be recorded,
  never hidden by an unconditional subsequent success.
