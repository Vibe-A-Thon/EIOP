# Phase 1 test and verification report

## Verified local results

- Focused documentation-audit acceptance tests: **13 passed**.
- Scoped Ruff for the audit tool/tests: **passed**.
- Documentation audit CLI regenerated the current ledger: **172 documents**,
  **29,538 lines**, **1,428 candidate records**.
- Source-bound full Python regression: **PASS**.
  JUnit receipt records **1,518 test cases**, **1,487 passed**, **31 skipped**, **0 failures**,
  **0 errors**, 260.590 seconds. The console emitted the existing duplicate ZIP
  member warning from `test_invalid_bundle_refused_before_graph_or_destination_writes`.
- Source-binding receipt: **PASS**, command exit code 0,
  `source_content_bound=true`, `source_revision_bound=false`,
  `source_unchanged=true`.
- Latest receipt completed after the audit-tool evidence-lead fix.
  This supersedes the earlier execution; skips are excluded from the passed
  count. It certifies its tested snapshot, not subsequent edits.

## Acceptance coverage

| Requirement | Automated evidence | Verification boundary |
|---|---|---|
| REQ-001 | nested/KGR/secret/ignored/encoding/byte-budget/symlink tests | Mechanical read completeness only |
| REQ-002 | explicit IDs, unnumbered statements, historical-report classification | Atomic semantic requirements still pending |
| REQ-003 | code/test mentions cannot produce Done | Does not infer actual behavior from missing IDs |
| REQ-004 | persisted JSON/Markdown, rerun stability, CLI subprocess and refusal tests | Current generated outputs excluded from their own receipts |
| REQ-005 | workflow dependency-extra assertion; full local native parser tests | Remote CI not executed or asserted |

Commands run from the repository root:

```powershell
python -m pytest tests/unit/test_documentation_audit.py
python -m ruff check scripts/documentation_audit.py tests/unit/test_documentation_audit.py
python -m scripts.documentation_audit
python -X utf8 -m scripts.validate_with_evidence --project-root . --output test-results\audit-current-rerun-source-bound-validation.json --artifact test-results\audit-current-rerun-regression.xml -- python -X utf8 -m pytest -q --junitxml=test-results\audit-current-rerun-regression.xml
```

## Manual and live integration gates

Not run in this phase:

1. Isolated live infrastructure through `scripts/docker.ps1 dlq-acceptance` and
   the 15 `tests/runtime_dlq` HTTP/persistence/replay scenarios.
2. HugeGraph persistence, API authentication, accepted/rejected ingestion,
   immutable capture and replay against the isolated deployment.
3. Browser upload, artifact download and graph inspection against a live local
   API/UI stack.
4. LibreOffice legacy import filters, opt-in Tesseract OCR and compressed RAR
   backend on a machine with the corresponding external tools.
5. Remote validation-evidence workflow and review gate.

## Provenance and publication

- The regression worktree is dirty, so the receipt is content-bound, not
  immutable revision-bound.
- The existing source-binding wrapper still excludes KGR by its older policy;
  the new documentation inventory independently hashes KGR catalogs, but no
  live KGR/UI acceptance is established by the Python regression receipt.
- Latest instruction remains local continuation only; no commit, push, PR or
  remote CI execution was performed.

## Final scoped rerun

The documentation inventory and source-bound regression were rerun after the
audit-tool evidence-lead fix. Report/checklist wording edits after the receipt do
not change executable source behavior.

- Source HEAD: `0108cbea1e66e3c465fa3262a105baf12b0ea449`.
- Tested source fingerprint:
  `58fdc0511058751455511d7833be6da03053e7c396212a9618a03204a1486472`.
- Local receipt: `test-results/audit-current-rerun-source-bound-validation.json`.
- Local JUnit: `test-results/audit-current-rerun-regression.xml`.
- Current documentation ledger: **172 documents, 29,538 lines**, including both
  KGR catalogs. Candidate triage: **1,428 records** (230 Partial evidence maps,
  1,198 Missing evidence maps). These are discovery counts, not verified atomic
  requirement or completion counts.
