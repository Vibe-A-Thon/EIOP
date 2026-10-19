# EOIP (kgf) Enhanced Audit Kit

Instruction set + offline executive tracker + JSON schemas for **strict, evidence-backed** audits of the EOIP (kgf) application. This kit does **not** include a live audit of a real EOIP repository — it is the prompt and tooling shell.

## Contents

| Path | Purpose |
|---|---|
| `ENHANCED_AUDIT_PROMPT.md` | Authoritative merged audit prompt (paste-ready block at end) |
| `tracker.html` | Offline executive dashboard with evidence/memory import |
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
5. Open **`tracker.html`** in a browser (file:// works; fully client-side).
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
   - **negative_proof** / absence → Not Implemented; conflicts → Ambiguous
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

1. Open `tracker.html` — seed KPIs and 8 sample requirements.
2. Import `examples/audit-memory.json`.
3. Import `examples/evidence.json` — under 1.1: REQ-FUNC-0001 Implemented (L2+L3); REQ-SEC-0002 Implemented (L2+L3+L5); REQ-AI-0003 Implemented (L2+L4); REQ-NFR-0005 Partial (L2+gaps); REQ-COMP-0004 Not Implemented (negative_proof); REQ-INFRA-0006 Implemented (L2+L3).

## Open decisions (for the user)

See the parent report: repo URL placement, CI provider link templates, whether production is ever in-scope for L4, and who holds Audit Lead / Security dual-control identities.

## Script pipeline

```bash
cd /path/to/eoip-repo   # or use kit fixtures
python3 -m venv .venv && source .venv/bin/activate
pip install -r /path/to/eoip-audit-kit/requirements.txt

SCRIPTS=/path/to/eoip-audit-kit/audit-scripts
KIT=/path/to/eoip-audit-kit
mkdir -p audit-output/evidence

python3 $SCRIPTS/parse_md_requirements.py --root . --out audit-output/requirements_index.json --commit "$(git rev-parse HEAD)" \
  --csv audit-output/requirements_index.csv
python3 $SCRIPTS/generate_traceability.py --repo-root . \
  --requirements audit-output/requirements_index.json \
  --out audit-output/traceability_matrix.csv --commit "$(git rev-parse HEAD)"
python3 $SCRIPTS/run_tests_and_map.py --repo-root . \
  --requirements audit-output/requirements_index.json --out audit-output/test_results/
$SCRIPTS/run_static_analysis.sh --repo-root . > audit-output/evidence/static_analysis.txt
# ... produce audit-output/evidence/evidence.json via remediation agents ...
python3 $SCRIPTS/validate_evidence.py --schema $KIT/schemas/evidence.schema.json \
  --in audit-output/evidence/evidence.json --memory audit-output/audit-memory.json
python3 $SCRIPTS/update_audit_memory.py --mode full --memory audit-output/audit-memory.json \
  --evidence audit-output/evidence/evidence.json --commit "$(git rev-parse HEAD)"
python3 $SCRIPTS/generate_audit_report.py --requirements audit-output/requirements_index.json \
  --traceability audit-output/traceability_matrix.csv --evidence audit-output/evidence/ \
  --memory audit-output/audit-memory.json --out audit-output/audit_gaps_requirements.md \
  --commit "$(git rev-parse HEAD)"
python3 $SCRIPTS/generate_tracker.py --evidence-json audit-output/evidence/evidence.json \
  --audit-memory audit-output/audit-memory.json --out audit-output/tracker.html \
  --data-out audit-output/tracker_data.json
```

Redaction example:

```bash
echo 'password="SuperSecret123" email=user@example.com' | \
  python3 $SCRIPTS/redact_sensitive.py --in - --out /tmp/redacted.txt --log /tmp/redaction.json
```
