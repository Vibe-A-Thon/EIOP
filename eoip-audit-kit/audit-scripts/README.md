# Audit scripts (implemented)

Python 3.11+ (verified on CPython 3.11.17). Optional: `pip install -r ../requirements.txt` for `jsonschema`.

Shared closure logic: `proof_policy.py` (**proof policy 1.1.0**).

| Script | Purpose |
|---|---|
| `parse_md_requirements.py` | Walk `.md`, extract REQ blocks / headings → `requirements_index.json` |
| `generate_traceability.py` | Search code for req ids/tokens → `traceability_matrix.csv` |
| `run_tests_and_map.py` | Run pytest/npm if present; map junit; `missing_tests.json` |
| `run_static_analysis.sh` | ruff/flake8/bandit/pip-audit/npm audit/gitleaks when installed |
| `generate_audit_report.py` | Build `audit_gaps_requirements.md` |
| `generate_tracker.py` | Emit `tracker_data.json` + standalone HTML with embedded data |
| `redact_sensitive.py` | Redact secrets/PII → out + log |
| `validate_evidence.py` | Schema + proof policy 1.1 enforcement |
| `update_audit_memory.py` | Merge evidence into `audit-memory.json` |
| `proof_policy.py` | Canonical status computation (importable) |

## Additions for the first real run

- `audit-config.json` (kit root) is the default `--config` for build_evidence, update_audit_memory, generate_audit_report and generate_tracker.
- `parse_md_requirements.py`: definition sites are headings, table rows, list items and `ID:` blocks. Uses the generic ID regex `[A-Z][A-Z0-9]*(-[A-Z0-9]+)*-\d+`, include/exclude globs, `--exclude-prefixes` (ADR/DEC/RISK...), `--all-md`. Falls back to `DOC-<ABBR>-NNNN` heading IDs for normative docs without IDs (`--no-fallback` disables this).
- `generate_traceability.py`: single-pass ID index over code/test/infra, plus `--test-map` and `--claims`.
- `run_tests_and_map.py`: `--python`, `--isolate` (copies the repo to a temp dir), `--reuse-junit`, `--test-map`, `--timeout`.
- `run_static_analysis.sh`: ruff, bandit, pip-audit, npm audit, gitleaks (if present). Options `--tools-bin`, `--out-dir`.
- `build_evidence.py` (new): evidence.json + residual_gaps.json from facts only.
- `reportlog_to_junit.py` (new): merges pytest-reportlog JSONL files into one JUnit XML, so killed or hung chunks keep their per-test results. Later files override earlier results.
- `proof_policy.py`: adds the **Not Verified** status; failing items are never proof; pass+fail → Ambiguous.

- `generate_fix_tasks.py` (new): deterministic task generator. Produces one RT-<ID> task per requirement (verbatim text, gap category, next steps, criteria, proof plan, priority with reason, effort), epics ≤60 tasks, DUP-<ID> duplicate tasks, orphan test IDs, `findings_tasks.md`, and the merged `audit-output/audit_tasks.json`. `--repo-root` (read-only) classifies duplicate sites.
- `claim_tasks.py` (new): claim / release / list / expire locks in `audit-memory.json` (24 h max, no overlap, atomic write).
- `proof_policy.py`: template placeholders (`REPLACE`, `<…>`, all-zero commit) are never proof.
- `generate_tracker.py --tasks audit-output/audit_tasks.json`: embeds the queue in a paginated Tasks tab (filters: kind, priority, epic, category, req status, search).

## Changes for the extended-run merge

- `run_tests_and_map.py`: works on Python 3.11 (regex moved out of the f-string).
- `update_audit_memory.py`: with `--requirements`, evidence for unknown IDs is stored under `orphan_evidence` (schema updated), not as new requirements.
- `generate_fix_tasks.py`: reads `test_results_merged/` if present. Renders extended-run evidence, parent/children/sub-items and resolved env-only failures. New queue kinds: `test_harness`, `security`, `kit`.
- `generate_audit_report.py`: §5a 'Extended test run' (suites, merged totals, status changes, defects → tasks).
- `generate_tracker.py`: skips orphan IDs. FT task cards show extended-run evidence and X-10 decisions.

## Documents and tracker outputs

- `generate_requirements_and_implementation_md.py`: writes `audit-output/requirements.md` and `implementation.md` deterministically. It also writes `requirements/` and `implementation/` per-doc splits when a file exceeds `--split-threshold-mb` (15), or with `--force-split`.
- `generate_tracker.py`: template `templates/tracker_template.html`. Canonical output is `audit-output/tracker.html`, which is also copied to `<kit>/tracker.html` (`--no-root-copy` to skip, `--also-out` for more). Header links to the documents are relative to each output.

## CLI examples

```bash
python3 parse_md_requirements.py --root ../fixtures/sample-reqs --out /tmp/req.json --commit abcdef1 --csv /tmp/req.csv
python3 generate_traceability.py --repo-root ../fixtures/sample-reqs --requirements /tmp/req.json --out /tmp/trace.csv --commit abcdef1
python3 run_tests_and_map.py --repo-root ../fixtures/sample-reqs --requirements /tmp/req.json --out /tmp/test_results
./run_static_analysis.sh --repo-root ../fixtures/sample-reqs
python3 validate_evidence.py --schema ../schemas/evidence.schema.json --in ../examples/evidence.json --memory ../examples/audit-memory.json
python3 update_audit_memory.py --mode full --memory /tmp/mem.json --evidence ../examples/evidence.json --commit a1b2c3d4e5f6789012345678901234567890abcd --repo local
python3 generate_audit_report.py --requirements /tmp/req.json --traceability /tmp/trace.csv --evidence ../examples --out /tmp/report.md --commit abcdef1 --memory ../examples/audit-memory.json
python3 generate_tracker.py --evidence-json ../examples/evidence.json --audit-memory ../examples/audit-memory.json --out /tmp/tracker.html
python3 redact_sensitive.py --in sample.txt --out redacted.txt --log redaction.json
```

All scripts accept `--help`. They must not print secrets; `update_audit_memory` / `validate_evidence` refuse secret-like payloads.
