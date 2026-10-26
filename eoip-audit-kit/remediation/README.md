# remediation/: work queue for fixing EIOP

Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a` (Vibe-A-Thon/EIOP @ dev_local). Proof policy 1.1.0.
Nothing here has been applied to the repo. These are tasks for humans and agents.

| File | What |
|---|---|
| `SECRET_ROTATION_AND_PURGE_PLAN.md` | **Do first.** F-01/F-02 incident runbook (containment → rotation → purge → prevention → log review → closure) |
| `evidence.secret-rotation.template.json` | Closure evidence template for F-01/F-02. Placeholders are ignored by the engine until filled |
| `findings_tasks.md` / `.json` | 34 hand-written full-template tasks: FT-F01…F11 (findings), FT-D01…D15 (defects), and from the extended run FT-X03/X04/X07/X10/X11/X12, FT-H01 (test harness), FT-SEC-HUBBLE (security), FT-K01 (kit, done). All 28 failing test cases map to a task; no env-only failures remain |
| `sources/apply_extended_run_tasks.py` | Idempotent script that applied extended-run defects X-01..X-12 to findings_tasks.json (updates overlapping tasks, adds new ones) |
| `requirement_tasks.json` / `.csv` | One generated task per requirement ID (RT-<ID>, 3383), via `audit-scripts/generate_fix_tasks.py` |
| `epics.json`, `epics/<EPIC>.md` | Requirement tasks batched by source doc × gap category, ≤60 tasks each. One epic = one agent work session |
| `duplicate_id_tasks.md` / `.json` | One task per ID that is really defined more than once (DUP-<ID>, 629). Sub-clause numbering (`CRA-001.1`) is not counted as a duplicate |
| `orphan_test_ids.json` | IDs that tests reference but no requirement doc defines (146) |
| `../audit-output/audit_tasks.json` | Merged queue (finding + defect + requirement + duplicate tasks), shown in `audit-output/tracker.html` |

## 1. Picking work

1. **Order:**
   1. FT-F01 and FT-F02 (secrets).
   2. FT-F04 (real CI; it unblocks L3 for every RT-* task).
   3. Other P0/P1 FT-*: FT-X03 + FT-X04 first among the new ones (the compose stack cannot start without them), then FT-F03, FT-D01.
   4. FT-X10: record a decision per drift test before working its child tasks (FT-D04/05/06/09/11/12).
   5. Epics, by priority mix: open `epics.json` and sort by `by_priority.P0`.
2. **Gap categories** (field `gap_category`) tell you what kind of work an RT-* task is:

   | Category | Meaning | Typical work |
   |---|---|---|
   | `ambiguous_tests` | mapped tests pass **and** fail | fix the failing ones (see `depends_on` → FT-D*) |
   | `untraced` | no code, test or infra mentions the ID | discovery: find the implementation under another name; trace it plus tests. If absent, implement it, or record negative proof (status *Not Implemented*) |
   | `code_no_test` | code mentions the ID, no test | write tests per acceptance criterion |
   | `tests_not_executed` | tests mapped but didn't run (integration markers, JS tests, excluded files) | run them in the right env (worker C for heavy suites) |
   | `needs_ci_l3` | passing tests (L2) | after FT-F04: get a same-commit green L3 run; spot-check the tests really assert the criteria |

3. Each RT task carries:
   - the verbatim requirement text and source `doc:line`;
   - current status and tier;
   - gaps and next steps;
   - mapped code/test paths, with GitHub links pinned to the audited commit;
   - acceptance criteria derived from the text;
   - the proof plan (what is missing to reach *Implemented*);
   - priority with its reason, an effort estimate, and `depends_on`.

   **UNKNOWN** in a field means "do the discovery step first".

## 2. Claim / lock (audit-memory.json `open_locks`)

Never work on a task another agent holds. Use the helper; it enforces a 24 h maximum, refuses overlaps and writes atomically:

```bash
S=audit-scripts/claim_tasks.py
python3 $S list    --memory audit-output/audit-memory.json
python3 $S claim   --memory audit-output/audit-memory.json --agent-id <you> --scope EPIC-03FUNCTIONAL-AMB --hours 8
#   scope may be epic ids, task ids (RT-*, FT-*, DUP-*) or requirement ids
python3 $S release --memory audit-output/audit-memory.json --agent-id <you> --lock-id LOCK-xxxx --action completed --notes "evidence: <path>"
python3 $S expire  --memory audit-output/audit-memory.json --agent-id AUDIT-LEAD   # Audit Lead only
```

A claim writes an `open_locks[]` entry `{lock_id, agent_id, scope, claimed_at, expires_at}` plus an `agents[]` record (`action: claimed`). A release removes the lock and records `completed`, `released` or `handoff`. If two agents share one memory file, keep it in one place, e.g. a shared branch of the kit, not per agent.

## 3. Producing evidence.json for a task

Work on a branch of the repo (**your** fork or clone; the audit never pushes). Then, on the fix commit `C`:

```bash
KIT=/path/to/eoip-audit-kit; S=$KIT/audit-scripts; O=$KIT/audit-output; R=/path/to/EIOP; C=$(git -C $R rev-parse HEAD)
python3 $S/parse_md_requirements.py --root $R --out $O/requirements_index.json --commit $C          # IDs/text may have changed
python3 $S/generate_traceability.py --repo-root $R --requirements $O/requirements_index.json \
   --out $O/traceability_matrix.csv --json-out $O/traceability_detail.json --commit $C --test-map $R/requirements-test-map.json
python3 $S/run_tests_and_map.py --repo-root $R --python <venv>/bin/python --isolate \
   --pytest-args "<the task's tests>" --requirements $O/requirements_index.json --out $O/test_results --test-map $R/requirements-test-map.json
python3 $S/build_evidence.py --requirements $O/requirements_index.json --traceability-detail $O/traceability_detail.json \
   --test-results $O/test_results --ci-runs $O/evidence/ci_runs.json --commit $C --agent-id <you> \
   --out $O/evidence/evidence.json --gaps-out $O/residual_gaps.json
#   L1 code links + L2 test runs are built from facts. Add L3 by refreshing ci_runs.json for C
#   (GET https://api.github.com/repos/Vibe-A-Thon/EIOP/actions/runs?head_sha=$C).
#   L4 (runtime logs/screenshots) and L5 (independent review) are added by hand, following examples/evidence.json.
python3 $S/validate_evidence.py --schema $KIT/schemas/evidence.schema.json --in $O/evidence/evidence.json --audited-commit $C
python3 $S/update_audit_memory.py --mode delta --memory $O/audit-memory.json --evidence $O/evidence/evidence.json --commit $C
python3 $S/generate_fix_tasks.py --repo-root $R            # refresh the queue
```

Rules that bite:
- L1 never counts toward Partial or Implemented.
- Failing items are never proof; pass and fail together on one commit → **Ambiguous**.
- Evidence from another commit is stale.
- Implemented needs L2 and (same-commit L3, or L4).
- Critical needs L3 plus L5 from a reviewer whose id differs from yours.
- Template placeholders (`REPLACE`, `<…>`, all-zero commit) count for nothing.
- Never put secrets or PII in evidence; run `redact_sensitive.py` on any log you attach.

## 4. Regenerating

```bash
python3 audit-scripts/generate_fix_tasks.py --repo-root /workspace/repos/EIOP          # deterministic; same inputs → same bytes
python3 audit-scripts/generate_tracker.py --audit-memory audit-output/audit-memory.json --evidence-json audit-output/evidence/evidence.json \
  --requirements audit-output/requirements_index.json --tasks audit-output/audit_tasks.json --out audit-output/tracker.html --data-out audit-output/tracker_data.json   # also writes ./tracker.html
```
