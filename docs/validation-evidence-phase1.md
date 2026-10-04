# Audit phase 1: validation evidence foundation

## Scope and acceptance

[Ticket 004](../tickets/ticket-20261004-004.md) restores the previously empty
[validation command](../scripts/validate_with_evidence.py) and
[focused tests](../tests/unit/test_validation_source_binding.py).
This supports MVP-FR-027; it does not close the complete requirement or certify
the application. The comprehensive documentation audit and per-requirement
acceptance assessment remain incomplete.

The wrapper executes explicit argument vectors without a shell, captures source
before/after, validates fresh artifacts, and persists command/source/artifact
failures. It refuses protected or Git-tracked outputs, including paths staged by
the child. Credentials, environment values, child output, runtime directories
and the two excluded KGR documents are not read into source fingerprints.
Arguments are recorded and must not contain credentials.

## Author-executed checks

Commands ran from the repository root in the existing Windows/Python 3.11 venv.
Receipts live in the ignored `test-results` directory; they are not bundled in
Git. Use the [runbook](../agent_runbook.md) to reproduce them.

| Check | Exit | Observed result | Local receipt |
|---|---|---|---|
| Failed-first initial focused tests | 2 | Missing wrapper exports prevented collection | `test-results/audit-evidence-red.xml` |
| Failed-first output-ownership reproductions | 1 | Both new tests failed: a child-staged artifact incorrectly passed and a child-staged receipt was overwritten | `test-results/audit-output-ownership-red.xml` |
| Failed-first Git metadata protections | 1 | Both metadata destinations were wrongly writable | `test-results/audit-git-metadata-red.xml` |
| Final focused wrapper + evidence-mapper regression | 0 | 45 passed; zero failures/errors/skips | `test-results/audit-evidence-focused.xml` |
| Ordinary full Python regression | 0 | 1,106 outcomes: 1,091 passed, 15 skipped, zero failures/errors | `test-results/audit-phase1-regression.xml` |
| Scoped Ruff | 0 | Both changed Python files passed | Console output |
| Editor problems | n/a | No errors reported for the two Python files and CI YAML | Editor tool result |
| CI YAML structure | 0 | Triggers, read-only permissions, Windows runner and always-upload step checked | In-process assertion output |
| Final source-bound full regression | Blocked | Concurrent unrelated edits; user authorizes focused publication with this blocker recorded | None |
| Remote GitHub CI | Pending | Workflow added; no passing remote run observed | None yet |

Exact focused command:

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m pytest -q tests\unit\test_validation_source_binding.py tests\unit\test_requirement_evidence.py --junitxml=test-results\audit-evidence-focused.xml
& .\.venv\Scripts\python.exe -m ruff check scripts\validate_with_evidence.py tests\unit\test_validation_source_binding.py
```

Exact ordinary full-regression command:

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m pytest -q --junitxml=test-results\audit-phase1-regression.xml
```

The ordinary full run overlapped source edits; it is not source-bound evidence
for the final snapshot. Its 15 skipped checks are not passes. It also emitted an
upstream Starlette/httpx deprecation warning and an intentional duplicate-ZIP
fixture warning. Neither was suppressed or treated as a new product defect.
Later API/query/UI/test/specification edits belong to other sessions and remain
unstaged by this phase. The user chose focused publication rather than pausing
those sessions for a final source-bound full rerun.

## Coverage and limitations

Focused tests cover actual execution, CLI refusal/failure exits, nonzero child
exits, missing executable, timeout, source additions/removals/content drift,
HEAD changes, dirty-tree binding, missing/stale/fresh artifacts, old timestamps,
output-path ownership, Git metadata refusal, case-insensitive protection, excluded-file non-reading,
symlink non-dereferencing and post-command capture failure.

No shared deployment, data reset, live external source, real model inference,
native graph recovery, UI journey or extension-host verification was performed
in this tooling phase. Author-executed tests are not independent QA approval.
Before/after fingerprints do not detect transient edits reverted during a run.
Dirty-tree content binding is not immutable revision certification, and fresh
artifacts are not semantic acceptance or full requirement coverage.

[The CI workflow](../.github/workflows/validation-evidence.yml) uses the existing
development/codeparse extras and Python 3.11. It is an optional validation
surface, not a new runtime/cloud dependency. Packaging/runtime compatibility on
other operating systems and repository-wide lint are outside this scoped check.

## Review stop

Publish this bounded phase against the originating `dev_local` branch rather
than including its unrelated history against `main`. Stop after the phase PR
for review. Resume [ticket 003](../tickets/ticket-20261004-003.md) only after that
gate; unread documentation, pending requirements, demo deliverables and later
implementation phases must not be marked Completed by assumption.
