# EOIP (kgf) Enhanced Audit Kit

Instruction set, offline executive tracker, JSON schemas and audit tooling for **strict, evidence-backed** reviews of EOIP (kgf).

## Current Snapshot Audit

The current application audit is in the repository-root [audit-output/](../audit-output/README.md), pinned to `78ff6d914ea15fbd10a5ae905d4ebeb02f527601`. Start with its [report](../audit-output/audit_gaps_requirements.md) or [offline tracker](../audit-output/tracker.html). The kit-root `tracker.html` is a self-contained copy of that tracker. Its strict assessor preserves unknown/stale evidence and does not treat source paths, test files or placeholder workflows as acceptance.

The first-pass artifacts and remediation plan under this kit's own `audit-output/` and `remediation/` directories are retained as history. Their older counts and verification results are not the current baseline. The legacy generator/importer path remains subject to the AUD-001 policy-consolidation finding; use `snapshot_audit.py` and the root bundle instructions for this run.

## Audit target & config

`audit-config.json` holds the target and link templates; scripts read it by default (`--config`).

- Repo: https://github.com/Vibe-A-Thon/EIOP (branch `dev_local`), baseline commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`
- Code link: `https://github.com/Vibe-A-Thon/EIOP/blob/{commit}/{path}#L{start}-L{end}`
- CI run link: `https://github.com/Vibe-A-Thon/EIOP/actions/runs/{run_id}` (job: `/job/{job_id}`)
- L3-eligible workflows: `validation-evidence.yml`, `ci.yml`. `reva-*.yml` are placeholders and are never L3.

The first real run is in `audit-output/`, starting with `audit_gaps_requirements.md`.

## Remediation

`remediation/` holds the fix plan for the first real run: the secret rotation and purge runbook, 25 finding/defect tasks, 3383 requirement tasks in 92 epics, and 629 duplicate-ID tasks. Start with `remediation/README.md`. The tracker's **Tasks** tab shows the merged `audit-output/audit_tasks.json`.

## Contents

| Path | Purpose |
|---|---|
| `ENHANCED_AUDIT_PROMPT.md` | Authoritative merged audit prompt (paste-ready block at end) |
| `tracker.html` | Current snapshot dashboard; identical to repository-root `audit-output/tracker.html`, written by `snapshot_audit.py` |
| `templates/tracker_template.html` | Blank tracker template (seed sample data, import buttons); the generator embeds data into it |
| `audit-output/requirements.md` | Consolidated requirements catalogue (3383 IDs, verbatim text, ACs, sources, duplicates, orphans) |
| `audit-output/implementation.md` | Implementation status per requirement, architecture, coverage per component, known defects |
| `schemas/evidence.schema.json` | Strict schema for agent-produced evidence |
| `schemas/audit-memory.schema.json` | Continuity / delta-audit / multi-agent handoff |
| `examples/evidence.json` | Sample evidence bundle (fictional) |
| `examples/audit-memory.json` | Sample audit memory (fictional) |
| `audit-scripts/README.md` | Required script CLI signatures (stubs) |

## Run order (typical)

1. **Checkout** the audited commit in the EOIP repo.
2. **Read** `audit-memory.json` if one exists (delta audit).
3. **Paste** the final prompt block from `ENHANCED_AUDIT_PROMPT.md` into your AI coding agent / audit team.
4. Agent produces under `audit-output/`:
   - `audit_gaps_requirements.md`
   - `requirements_index.json`, `traceability_matrix.csv`, `audit_tasks.json`
   - `evidence/evidence.json` (validate against `schemas/evidence.schema.json`)
   - Updated `audit-memory.json`
5. Open **`tracker.html`** in a browser (file:// works; fully client-side; data embedded, no tracker_data.json needed). Read `audit-output/requirements.md` and `audit-output/implementation.md` for the full catalogue and status.
6. **Import Audit Memory** (optional baseline), then **Import Evidence JSON**.
7. Review KPI cards, per-row evidence panels, and import trail.
8. **Export CSV** for exec packs; keep overrides justified.

## How AI agents produce `evidence.json`

For each requirement they claim progress on, append an `evidence_items[]` entry with:

- `requirement_id`, `evidence_id`, `proof_tier` (L1–L5), `type`, `summary`
- `links`, `repro_command`, `expected_result`, `actual_result`
- `confidence` (0–1), `redaction_status`

**Never** put secrets or PII in the bundle. Prefer opaque owner/agent ids.

Validate:

```bash
# Example — implement validate_evidence.py per audit-scripts/README.md
python3 audit-scripts/validate_evidence.py \
  --schema schemas/evidence.schema.json \
  --in audit-output/evidence/evidence.json
```

## How tracker import updates status

On **Import Evidence JSON**, the tracker:

1. Checks `schema_version == 1.0.0`.
2. Rejects payloads that look like secrets (private keys, AWS keys, GitHub PATs, Slack tokens).
3. Matches items by `requirement_id` and attaches evidence (expandable per row).
4. Recomputes max **proof tier** and applies **proof policy 1.1**:
   - **L1 ignored** for Partial/Implemented
   - **Partial** = L2 + residual_gaps
   - **Implemented** = L2 + (L3 same commit | L4)
   - **Critical Implemented** = L3 + L5 (distinct reviewer)
   - **Stale** evidence (commit mismatch) flagged and ignored
   - **negative_proof** / absence → Not Implemented; conflicts (incl. pass+fail on the same commit) → Ambiguous
   - L1-only, failing-only or no evidence → **Not Verified** (the default; never "Not Implemented")
5. Records an import trail in **localStorage**.
6. Manual status change requires a **justification** (override badge).

**Import Audit Memory** restores owners, residual gaps, estimates, and baseline statuses when no stronger evidence is present. If evidence already exists, tiers win over stale memory status.

## Proof policy 1.1

Field `proof_policy_version` must be **`1.1.0`** on both `evidence.json` and `audit-memory.json` (`schema_version` is also `1.1.0`).

| Rule | Detail |
|---|---|
| L1 | Never contributes to Partial or Implemented |
| Partial | Requires ≥ L2 **and** explicit non-empty `residual_gaps` |
| Implemented | Requires **L2 AND (L3 on same git_commit OR L4 non-prod)** |
| Critical Implemented | Additionally **L5** with `reviewer_id` ≠ `generated_by.agent_id` |
| Ambiguous | Conflicting evidence on same commit |
| Not Verified | default: L1 only / failing only / no evidence |
| Not Implemented | `negative_proof` **or** absence search with `repro_command` |
| Stale | Evidence `git_commit` ≠ audited commit → ignored for closure, flagged in tracker |

### Proof-tier reference

| Tier | Meaning | Counts toward Partial/Implemented? |
|---|---|---|
| L0 | Claim only | No (forbidden in evidence.json) |
| L1 | Code path + lines | **Never** |
| L2 | Named test + pass log + command | Required baseline |
| L3 | CI job + run id green on **audited** commit | With L2 |
| L4 | Non-prod runtime/observability | With L2 (if no CI) |
| L5 | Independent reviewer (distinct id) | With L3 for Critical |

## How `audit-memory` enables the next audit

1. Next agent loads `audit-memory.json` first.
2. Diff `baseline_commit` → new tip.
3. **Deep-audit** changed files / new requirements / open Critical·High / Partial·NI.
4. **Minimal re-verify** unchanged Implemented (path still exists + spot-check).
5. Update locks, changelog, health_score, `last_verified_commit`.

No secrets/PII in memory. Owners are hashed ids. Prompt hashes only.

## Suggested demo

1. Open `templates/tracker_template.html` for seed KPIs and 8 sample requirements (the top-level `tracker.html` holds the real run).
2. Import `examples/audit-memory.json`.
3. Import `examples/evidence.json` — under 1.1: REQ-FUNC-0001 Implemented (L2+L3); REQ-SEC-0002 Implemented (L2+L3+L5); REQ-AI-0003 Implemented (L2+L4); REQ-NFR-0005 Partial (L2+gaps); REQ-COMP-0004 Not Implemented (negative_proof); REQ-INFRA-0006 Implemented (L2+L3).

## Open decisions (for the user)

See the parent report: repo URL placement, CI provider link templates, whether production is ever in-scope for L4, and who holds Audit Lead / Security dual-control identities.

## Script pipeline (as run for the first pass)

```bash
KIT=/workspace/eoip-audit-kit; S=$KIT/audit-scripts; O=$KIT/audit-output; R=/workspace/repos/EIOP
C=$(git -C $R rev-parse HEAD)
python3 $S/parse_md_requirements.py --root $R --out $O/requirements_index.json --csv $O/requirements_index.csv --commit $C
python3 $S/generate_traceability.py --repo-root $R --requirements $O/requirements_index.json \
  --out $O/traceability_matrix.csv --json-out $O/traceability_detail.json --commit $C \
  --test-map $R/requirements-test-map.json --claims $R/requirements-registry.json
python3 $S/run_tests_and_map.py --repo-root $R --python /path/venv/bin/python --isolate \
  --requirements $O/requirements_index.json --test-map $R/requirements-test-map.json --out $O/test_results
#   (or run pytest yourself and pass --reuse-junit <xml>)
$S/run_static_analysis.sh --repo-root $R --tools-bin /path/tools-venv/bin --out-dir $O/evidence/static > $O/evidence/static_analysis.txt
# CI runs for the commit (public API, no auth): save to $O/evidence/ci_runs.json
python3 $S/build_evidence.py --requirements $O/requirements_index.json --traceability-detail $O/traceability_detail.json \
  --test-results $O/test_results --ci-runs $O/evidence/ci_runs.json --commit $C --out $O/evidence/evidence.json --gaps-out $O/residual_gaps.json
python3 $S/validate_evidence.py --schema $KIT/schemas/evidence.schema.json --in $O/evidence/evidence.json
python3 $S/update_audit_memory.py --mode full --memory $O/audit-memory.json --evidence $O/evidence/evidence.json \
  --requirements $O/requirements_index.json --gaps $O/residual_gaps.json --commit $C --repo https://github.com/Vibe-A-Thon/EIOP
python3 $S/generate_audit_report.py --out-dir $O          # reads findings.json, stack.json, skipped.json if present
python3 $S/generate_tracker.py --audit-memory $O/audit-memory.json --evidence-json $O/evidence/evidence.json \
  --requirements $O/requirements_index.json --tasks $O/audit_tasks.json --out $O/tracker.html   # also writes $KIT/tracker.html
python3 $S/generate_requirements_and_implementation_md.py --repo-root $R   # audit-output/requirements.md + implementation.md (run before the tracker so its header links them)
```

`build_evidence.py` only writes facts (L1 code links, L2 test results, L3 from eligible green CI). It never fabricates L4 or L5.

## Extended run merge (2026-10-19)

Heavy suites ran in a second pass (`audit-output/test_results_extended/`). To merge without double-counting a re-run test:

1. `merge_junit.py --base $O/test_results/tests.xml --override $O/test_results_extended/tests.xml --out $O/test_results_merged/tests.xml` builds the main junit, where an extended result replaces the same `classname::name` case, plus extended-only cases.
2. `run_tests_and_map.py --reuse-junit --out $O/test_results_merged`, then `build_evidence.py --test-results $O/test_results_merged`.
3. Union with `evidence_extended.json` (de-dup by `evidence_id`, same commit) into `evidence.json` and validate it.
4. `update_audit_memory.py --mode full`. With `--requirements`, evidence for IDs no requirement doc defines goes to `orphan_evidence`, not to requirements.
5. `generate_fix_tasks.py` (prefers `test_results_merged/`), `generate_audit_report.py` (adds §5a from `test_results_extended/`), `generate_tracker.py`.
