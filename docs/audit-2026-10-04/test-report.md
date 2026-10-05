# Test and verification report

## Latest enterprise remediation evidence

- Pre-what-if-fix full local regression: **1,880 passed, 0 failed, 22 skipped, exit 0**,
  1,316.21 seconds. [JUnit](../../test-results/enterprise-final-source-junit.xml).
- Focused query/schema/API/metrics tests: **62 passed, exit 0**.
  [JUnit](../../test-results/enterprise-search-focused-junit.xml).
- Final audit acceptance tests: **14 passed, exit 0**.
  [JUnit](../../test-results/enterprise-audit-final-junit.xml).
  Final reporting regeneration was verified separately from the full run.
- Node demo tests: **19 passed, exit 0**, including rejection of silently
  omitted code facts and relationships.
- Actual live source-extension: **17 steps passed, exit 0**, six NLQ intents
  and eleven MCP tools against the persisted graph. An earlier post-rebuild
  SEARCH attempt exceeded 5,000 ms; the passing rerun does not establish a
  cold-start SLO or certify the installed VSIX.
- Actual administration rehearsal: **42 steps passed, exit 0**; operation
  coverage remains PARTIAL.
- Current seed: **1.2.0, 13 scenarios, 80 entities, 134 relationships**.
  Current selected corpus: **85 Documents, 1,144 chunks**.
- All six local Docker services are healthy; enterprise Hubble page HTTP 200.
- Actual application rehearsal: **166 steps passed, one failed, exit 1**.
  What-if exceeded the unchanged 120-second request timeout.
  [Failure receipt](../../test-results/enterprise-application-demo.json).
- What-if repair: partition the remaining neighbor components once per
  invocation; avoid repeated pairwise traversal and report exact split counts.
  New tests reproduced both defects before repair and verify freshness and
  non-mutation. What-if/metrics: **22 passed, exit 0**; scoped Ruff clean.
  [Focused JUnit](../../test-results/enterprise-whatif-fix-junit.xml).
- Deployed what-if API: HTTP 200 in **15.903 seconds**, unchanged 120-second budget.
- Post-fix full local regression: **1,883 passed, 0 failed, 22 skipped,
  exit 0**, 1,258.37 seconds.
  [Post-fix JUnit](../../test-results/enterprise-whatif-source-junit.xml).
  Audit receipt reporting changed during the run and independently passed
  14 tests (exit 0), with scoped Ruff clean.
- Post-fix actual application: **183 steps passed, zero failures, exit 0**;
  operation coverage remains PARTIAL.
  [Receipt](../../test-results/enterprise-application-whatif-fixed.json).
- Pipeline rehearsal: **187 steps passed, one failed, exit 1**, caused by
  53 missing-endpoint errors for the code export.
  [Preserved failure](../../test-results/enterprise-pipeline-demo.json).
  Regression tests also exposed silent omission of manual code facts and
  inline forward references. The code-export adapter and explicit dependency
  declarations passed focused importer/API/audit validation: **59 passed,
  exit 0**, scoped Ruff clean.
  [Focused receipt](../../test-results/enterprise-code-ingestion-focused-junit.xml).
  Application-only Docker rebuild/recreation completed with exit 0; all six
  services healthy and API/web/enterprise explorer HTTP 200.
  Live code-export acceptance: **2 passed, exit 0**, with authentication,
  exact counts, Hubble read-back and replay identity.
  [Live receipt](../../test-results/enterprise-code-ingestion-live-junit.xml).
  Initial test-query failures (unindexed property scan / logical edge label)
  are retained separately; final tests use bounded physical-edge adjacency.
  The preceding 1,883-pass receipt does not certify subsequent source changes.
- Post-importer full regression: **1,897 passed, 24 skipped, zero failures,
  exit 0**, 1,467.13 seconds.
  [Final importer JUnit](../../test-results/enterprise-code-ingestion-final-junit.xml).
  The two added opt-in live tests explain the increased skip count. Their
  query implementation changed during the ordinary run, but they executed
  separately with two passes; production Python source remained unchanged.
- Fresh repaired pipeline rehearsal: **213 passing steps, zero failures,
  exit 0**, including code export, complete batch ingestion and exports.
  [Pipeline receipt](../../test-results/enterprise-pipeline-code-fixed.json).
  Coverage remains **PARTIAL: 66/271 operations demonstrated, 205 not demonstrated**.
- Additive corpus refresh: **loaded 2 / retained 83**; unchanged rerun:
  **loaded 0 / retained 85**, both exit 0. Exact complete **2,474 vertex /
  6,897 edge identity sets** remained unchanged around the latter run.
  [Retention receipt](../../test-results/enterprise-code-corpus-retention.json).
- Full current corpus Hubble read-back: **1 passed, exit 0**, covering every
  expected Document/chunk and both Jira fixture sets.
  [Live corpus JUnit](../../test-results/enterprise-code-corpus-live-junit.xml).
- Remote CI, installed VSIX and all-product completion are not asserted.

See [current runtime evidence](../hubble-runtime-validation.md) and
[generated inventory/counts](./current-gap-report.json). The older counts and
scope below are historical phase evidence, not current progress.

## Historical phase 1 results

## Verified local results

- Focused documentation-audit acceptance tests: **13 passed**.
- Focused EKAF drift controls tests: **5 passed**.
- Focused EKAF conflict/truth handoff tests: **24 passed**.
- Scoped Ruff for the audit tool/tests: **passed**.
- Documentation audit CLI regenerated the current ledger: **175 documents**,
  **29,764 lines**, **1,431 candidate records**.
- Source-bound full Python regression: **PASS**.
  JUnit receipt records **1,543 test cases**, **1,519 passed**, **24 skipped**, **0 failures**,
  **0 errors**, 409.854 seconds. The console emitted the existing duplicate ZIP
  member warning from `test_invalid_bundle_refused_before_graph_or_destination_writes`.
- Source-binding receipt: **PASS**, command exit code 0,
  `source_content_bound=true`, `source_revision_bound=false`,
  `source_unchanged=true`.
- Latest receipt completed after webhook-recovery and current-tree audit updates.
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
audit-tool evidence-lead fix and webhook-recovery implementation. Report/checklist
wording edits after the receipt do not change executable source behavior.

- Source HEAD at receipt start: `28229963bc0753a5e173238ba473caa4f70ef1fd`.
- Source-binding receipt: `PASS`; `source_content_bound=true`,
  `source_revision_bound=false`, `source_unchanged=true`.
- Local receipt: `test-results/audit-current-rerun-source-bound-validation.json`.
- Local JUnit: `test-results/audit-current-rerun-regression.xml`.
- Current documentation ledger: **175 documents, 29,764 lines**, including both
  KGR catalogs. Candidate triage: **1,431 records** (238 Partial evidence maps,
  1,193 Missing evidence maps). These are discovery counts, not verified atomic
  requirement or completion counts.
