# EOIP (kgf) — Enhanced Audit Prompt (Authoritative)

**Version:** 1.1.0  
**Audience:** AI coding agents, multi-agent audit teams, human auditors  
**Kit root:** `eoip-audit-kit/`  
**Companion artifacts:** `schemas/`, `examples/`, `tracker.html`, `audit-scripts/`

This document is the **single authoritative** instruction set for auditing the EOIP (kgf) application. It merges overlapping prior prompts, adds a strict proof-of-completion model, evidence import into the executive tracker, and an audit-memory protocol for delta and multi-agent continuation.

---

## 1. Purpose

Perform a **comprehensive, evidence-backed, unbiased** audit of EOIP (kgf) by comparing every `.md` requirement (and related ADRs/design/policy docs) to the actual implementation (code, infra, CI/CD, tests, runtime, observability).

**Primary outputs** (under the audited repo’s `audit-output/`):

| Artifact | Role |
|---|---|
| `audit_gaps_requirements.md` | Authoritative human report |
| `requirements.md` | Consolidated requirements catalogue: every requirement ID with verbatim text, source doc:line link, type, priority, acceptance criteria (verbatim, or derived and marked as derived), dependencies, duplicate definition sites, plus orphan test-only IDs |
| `implementation.md` | Implementation status against requirements: executive summary (status, tiers, tests), architecture/stack from repo reading, coverage per component, and per ID the status, tier, code links, mapped tests with pass/fail, residual gaps, fix-task IDs and what is needed to reach Implemented; known defects |
| `tracker.html` | Executive remediation dashboard with the run's data embedded (works from file://; the kit root `tracker.html` is a copy of `audit-output/tracker.html`) |
| `evidence/evidence.json` | Machine evidence for tracker import |
| `audit-memory.json` | Continuity across agents/LLMs and delta audits |
| `requirements_index.json` | Parsed requirements |
| `traceability_matrix.csv` | Req → code/test/infra map |
| `audit_tasks.json` | Remediation task queue |
| `evidence/` | Raw reproducible artifacts |
| `audit-scripts/` | Deterministic automation |

**This kit does not claim a live EOIP repo was audited.** It is the instruction + tooling shell. (A first-pass run against the target below lives in `audit-output/`; it states its own limits.)

### Audit target (from `audit-config.json`)

| Placeholder | Value |
|---|---|
| `{{REPO_URL}}` | `https://github.com/Vibe-A-Thon/EIOP` |
| `{{BRANCH}}` | `dev_local` |
| `{{BASELINE_COMMIT}}` | see `audit-config.json → repo.baseline_commit` (first pass: `3ed3acd50e47ab8867aa6885d202f9956358dc3a`) |
| `{{CODE_LINE_LINK}}` | `https://github.com/Vibe-A-Thon/EIOP/blob/<commit>/<path>#L<a>-L<b>` |
| `{{CI_RUN_LINK}}` | `https://github.com/Vibe-A-Thon/EIOP/actions/runs/<run_id>` |
| `{{CI_JOB_LINK}}` | `https://github.com/Vibe-A-Thon/EIOP/actions/runs/<run_id>/job/<job_id>` |

Every L1 evidence item MUST carry a `{{CODE_LINE_LINK}}` pinned to the audited commit (never a branch name). L3 is only allowed from workflows listed in `ci.l3_eligible_workflows`; placeholder workflows (`reva-*.yml`, which only `echo`) never count.

---

## 2. Roles (Multi-Disciplinary)

Simulate or staff as needed:

| Role | Focus |
|---|---|
| Audit Lead | Coordination, report finalization, sign-off |
| Technical Lead / Developer / Code Reviewer | Traceability, implementation fidelity |
| Senior Enterprise Architect | Architecture, NFRs, scalability, resilience |
| AI Architect / Gen AI / Agentic AI (Arch & Eng) | LLM usage, prompts, model governance, agent safety |
| Digital / AI-First Product Owner | Acceptance criteria, product intent |
| CTO / Controller / Auditor | Risk, governance, executive health |
| Compliance Reviewer | Licenses, regulatory, export controls |
| Cybersecurity Specialist / Security Reviewer | Threat model, SAST/DAST, secrets, authn/authz |

**Access (minimum):** read repo + CI logs; checkout a fixed commit; run builds/tests in an isolated sandbox; read infra manifests and OpenAPI. **No production secrets or PII.**

---

## 3. Hard Constraints & LLM / Redaction Rules

1. **Never** send secrets, PII, production data, or live credentials to external LLMs.
2. Before any LLM call, run `audit-scripts/redact_sensitive.py` (or equivalent) and store a redaction log.
3. Record for every LLM call: model name, version, **prompt hash**, redacted input ref, output ref, human verifier id (opaque).
4. Prefer deterministic Python for parsing, scoring, and report assembly; LLM only for drafting when redacted.
5. Evidence must be reproducible from included commands/scripts at a **named git commit**.
6. Prefer Python + CLI flags; scripts must be deterministic.
7. `audit-memory.json` and `evidence.json` **must never** contain secrets or PII (owners = hashed/opaque ids).

**Allowed LLM uses:** boilerplate, test stubs, remediation wording, non-sensitive summaries.  
**Prohibited:** raw logs with tokens, PII, production dumps, private keys.

---

## 4. Scope, Inputs, Assumptions

### Inputs (required)

- All `.md` (requirements, ADRs, architecture, design, standards, policies)
- Source tree (branches specified by Audit Lead)
- CI/CD definitions and recent run logs
- Test suites and results (unit, integration, e2e)
- Runtime/infra: Dockerfiles, k8s, Terraform, Helm
- API contracts (OpenAPI), DB schemas, diagrams

### Inputs (recommended)

- Deployment logs, monitoring/metrics exports
- Prior SAST/DAST/SBOM outputs
- Prior `audit-memory.json` (for delta audits — **read first**)

### Assumptions (auto-record if missing)

- Default OS / language runtime / container runtime
- Default branch + exact commit under audit
- Missing input ⇒ documented gap with discovery steps

### Environment matrix (required to record)

| Env | Audited? | Notes |
|---|---|---|
| local / CI | Yes/No | |
| staging / non-prod | Yes/No | Preferred for L4 |
| production | Usually No | Never pull prod secrets |

---

## 5. Stepwise Methodology

Each step produces artifacts under `audit-output/` and raw evidence under `audit-output/evidence/`.

### 5.1 Inventory & Requirements Parsing

- Parse every `.md` into: `id`, `title`, `type`, `priority`, `owner`, `acceptance_criteria`, `related_files`, `line_range`, `raw_text`.
- **Out:** `requirements_index.json`, `.csv`
- **Script:** `parse_md_requirements.py --root . --out audit-output/requirements_index.json`

### 5.2 Implementation Traceability

- Map each requirement to code, tests, infra, docs (search + AST + OpenAPI refs).
- **Out:** `traceability_matrix.csv`  
  Columns: `requirement_id, code_paths, test_paths, infra_paths, evidence_type, confidence_score, git_commit`
- **Script:** `generate_traceability.py ...`

### 5.3 Behavioral Verification

- Run unit / integration / e2e; map pass/fail to requirements.
- Missing tests ⇒ `missing_tests.json` + minimal stubs/plans for agents.
- **Out:** `test_results/`, `missing_tests.json`

### 5.4 Static & Dynamic Analysis (+ SBOM)

- Linters, SAST, dependency vulns, **SBOM / license**, secrets scanners.
- DAST / safe load tests against non-prod if available.
- **Out:** `security_scan/`, `vuln_report.json`, `sbom.json` / CycloneDX, `license_report.csv`

### 5.5 Architecture & NFR Review

- Diagrams vs code/infra; scalability, resilience, **observability**, **backup/DR** (RPO/RTO), performance budgets.
- **Accessibility** checks if UI is in scope (keyboard, ARIA, contrast — at least checklist + automated axe/lighthouse where feasible).
- **Out:** `architecture_review.md`, `load_test_results/`, `a11y_checklist.md` (if UI)

### 5.6 Security, Privacy & Threat Model

- Data flows, trust boundaries, authn/authz, sessions, encryption in transit/at rest.
- **Secrets management & key rotation** evidence.
- **Data classification & residency** (what classes exist; where stored/processed; cross-border).
- **Out:** `threat_model.json`, `security_checklist.md`, `data_classification.md`

### 5.7 AI / LLM Governance

- Inventory models, prompts, tool/agent loops, RAG stores.
- Verify redaction, prompt versioning, output validation, human-in-the-loop, rate limits, cost/abuse controls.
- **Out:** `ai_inventory.json`, `ai_governance.md`

### 5.8 Compliance & Licensing

- Third-party licenses, export controls, domain regulations applicable to EOIP.
- **Out:** `license_report.csv`, `compliance_gaps.md`

### 5.9 Risk Assessment & Prioritization

- Per gap: severity, impact, likelihood, residual risk, estimate hours, complexity.
- **Out:** `audit_tasks.json`

### 5.10 Remediation Plan, Evidence Bundle & Tracker

- Produce `evidence/evidence.json` conforming to `schemas/evidence.schema.json`.
- Update `audit-memory.json` per `schemas/audit-memory.schema.json`.
- Generate `requirements.md` and `implementation.md` (`audit-scripts/generate_requirements_and_implementation_md.py`) from the index, traceability, merged evidence, memory and tasks. Both are deterministic, and verbatim text is read from the audited commit.
- Generate or refresh `tracker.html`; operators import evidence for executive status.

---

## 6. Strict Proof of Completion Model

**Proof policy version: `1.1.0`** (field `proof_policy_version` required on evidence.json and audit-memory.json).

Code paths and test *file names alone are not proof*. Status updates follow these tiers and **closure rules**.

| Tier | Name | What counts | Counts toward Partial/Implemented? |
|---|---|---|---|
| **L0** | Claim only | Narrative assertion | **No** — forbidden in evidence.json |
| **L1** | Source linkage | Code path + line range at audited commit | **Never** — ignored for closure |
| **L2** | Automated test evidence | Named test + pass log + exact repro command | Required baseline for Partial & Implemented |
| **L3** | CI evidence | Job name + run id + green on **same audited git_commit** | With L2 → Implemented (non-Critical) |
| **L4** | Runtime / observability | Logs, metrics, screenshots from **non-prod** | With L2 → Implemented when CI absent (document why) |
| **L5** | Independent verification | Second verifier with `reviewer_id` **≠** `generated_by.agent_id` | Required with L3 for Critical Implemented |

### Closure rules (proof policy 1.1.0)

1. **L1 never** contributes to **Implemented** or **Partially Implemented** alone (or at all as the sole tier).
2. **Partially Implemented** requires **≥ L2** **and** explicit non-empty `residual_gaps`.
3. **Implemented** requires **L2 AND (L3 on the same `git_commit` OR L4 non-prod runtime)**. Both sides must be present and passing.
4. **Critical** severity **Implemented** additionally requires **L5 dual-control** (distinct `reviewer_id`). Without L5, max status is **Partially Implemented** (and still needs L2 + gaps if not fully closed).
5. **Ambiguous** if conflicting evidence on the same commit (e.g. negative_proof + positive L2+, or pass vs fail in L2/L3 `actual_result`).
6. **Not Verified** is the default: L1-only, failing-only, or no evidence. Failing L2/L3 items are never proof. Passing and failing items on the same commit → **Ambiguous**.
7. **Not Implemented** requires `type: negative_proof` **OR** a documented absence search with `repro_command` (and actual showing absence).
7. Evidence items are **STALE** (ignored for closure, flagged in tracker) when `item.git_commit` or bundle commit **≠** audited commit.
8. Manual overrides require justification; they do not erase stale flags.

### Confidence aggregation

Per requirement: max active (non-stale) tier + mean confidence of items ≥ L2. Confidence &lt; 0.6 → weak flag.

---

## 7. Negative Evidence / Absence Proofs

When status is Not Implemented (or claiming a control is absent):

- Record `type: negative_proof` with `repro_command` (e.g. `rg`, `find`, CI job list).
- Store command output under `evidence/absence/`.
- Include expected vs actual (“expected SBOM job; actual: 0 matches”).

---

## 8. Delta-Audit Protocol (using audit-memory)

1. **Load** `audit-memory.json` first.
2. Diff `baseline_commit` → `HEAD` (or requested tip).
3. **Deep-audit** only:
   - Requirements whose `files_touched` intersect the diff;
   - New/changed `.md` requirements;
   - Open Critical/High or Partial/Not Implemented;
   - Anything with stale proof (commit moved and tests/CI not re-verified).
4. **Minimal re-audit** for Implemented with unchanged files: verify commit still contains linked paths; spot-check one L2/L3 artifact; else inherit status.
5. Update `last_verified_commit`, `health_score`, `changelog`, and release/claim locks.

---

## 9. Multi-Agent Handoff Protocol

1. Agent writes an entry to `open_locks[]` with `scope` (REQ ids or globs), `claimed_at`, `expires_at` (≤ 24h).
2. Append `agents[]` with `action: claimed|released|completed|handoff|delta_audit|full_audit`, `prompt_hash`, refs to redacted I/O.
3. Do not overwrite another agent’s lock; Audit Lead may expire stale locks.
4. On handoff: update `changelog`, leave residual_gaps clear, no secrets in memory.
5. Prompt hashes only — never store full prompts with sensitive content.

---

## 10. Deliverable Layout

```text
audit-output/
  audit_gaps_requirements.md
  requirements.md              # consolidated requirements catalogue (generate_requirements_and_implementation_md.py)
  implementation.md            # implementation status per requirement (same script)
  requirements/ implementation/  # per-source-doc split + index.md, only when a single file would exceed ~15 MB
  tracker.html                 # embedded data; generate_tracker.py also copies it to the kit root
  requirements_index.json
  traceability_matrix.csv
  audit_tasks.json
  audit-memory.json
  evidence/
    evidence.json
    static_analysis.txt
    tests.xml
    sbom.json
    absence/
    runtime/
    reviews/
  README.md
audit-scripts/
  parse_md_requirements.py
  generate_traceability.py
  run_tests_and_map.py
  run_static_analysis.sh
  generate_audit_report.py
  generate_tracker.py
  redact_sensitive.py
  validate_evidence.py
  update_audit_memory.py
```

---

## 11. `audit_gaps_requirements.md` Structure

- **Header:** project, repo URL (no creds), commit, date, auditors (roles + opaque names)
- **Executive Summary:** core objective, health score, top 5 risks, remediation summary (KPIs: % Implemented, Critical open, avg proof tier, evidence coverage)
- **Core Objective:** one paragraph from requirements
- **Traceability Summary:** counts Implemented / Partial / Ambiguous / Not Verified / Not Implemented / N/A
- **Detailed Findings** per requirement:
  - ID, verbatim text, Type, Status, Proof tier achieved
  - Evidence (paths, tests, CI run ids, repro commands, commit)
  - Gap, Severity, Residual risk
  - Remediation steps, Estimate hours, Acceptance criteria
- **Appendices:** matrix, scripts, evidence index, redaction & LLM logs, dual-control sign-offs

---

## 12. Severity Matrix

| Severity | Impact | Likelihood cue | Action |
|---|---|---|---|
| Critical | Data loss, breach, systemic outage | High | Block release; dual-control close |
| High | Major feature broken or material security risk | Medium–High | Current sprint |
| Medium | Degraded UX / missing non-critical | Medium | Next sprint |
| Low | Cosmetic / docs | Low | Backlog |

---

## 13. Requirement Template for AI Agents

When creating or correcting requirements, use **all** fields (UNKNOWN + discovery step if needed):

```text
ID: REQ-<TYPE>-<NNNN>          # TYPE ∈ FUNC|NFR|SEC|COMP|AI|INFRA (mapped to display types)
Title: <one line>
Type: Functional | Non-Functional | Security | Compliance | AI | Infra
Priority: P0 | P1 | P2 | P3
Severity_Hint: Critical | High | Medium | Low
Description: <narrative, examples, edge cases>
Preconditions: <env, data, config>
API Contracts: <request/response schema; status codes; headers>
Data Model: <fields, types, validation, migrations>
Data Classification: <Public|Internal|Confidential|Restricted>; residency notes
Acceptance Criteria: <numbered, testable>
Automated Tests: <unit/integration/e2e with samples>
Security Controls: <authn/authz, encryption, rate limits, validation, key rotation>
Performance Targets: <latency, throughput, budgets>
Observability: <logs, metrics, traces, alerts>
Accessibility: <if UI — WCAG target>
Backup/DR: <RPO/RTO if data-bearing>
Backward Compatibility: <migrations>
SBOM/Dependencies: <new deps? license constraints>
Implementation Notes: <paths, symbols, env vars, infra>
Environment Matrix: <local|CI|staging|prod expectations>
Estimated Effort: <hours; complexity>
Proof Plan: <required tiers L2/L3/L4/L5>
```

---

## 14. Evidence.json & Import Conflict Rules

- Conform to `schemas/evidence.schema.json` (`schema_version: 1.1.0`, `proof_policy_version: 1.1.0`).
- Tracker / `validate_evidence.py` must:
  1. Reject unknown schema / proof_policy_version (expect 1.1.0).
  2. Warn on git_commit mismatch vs memory baseline (allow import with flag).
  3. Run secret heuristics; **reject** items that look like keys/tokens/PII.
  4. Match by `requirement_id`; attach evidence; recompute max tier.
  5. Apply closure rules (§6); never promote to Implemented on L1-only.
  6. **Conflicts:** if imported status would *downgrade* a manually justified override, keep override and log conflict; if upgrade is valid by tiers, apply upgrade and clear override.
  7. Append `import_history` (in tracker localStorage and optionally audit-memory).

---

## 15. Executive KPIs (Tracker)

- **% Implemented**
- **Critical open** (Critical and not Implemented)
- **Evidence coverage** (mean max proof tier as 0–5 or L-label average)
- **Requirements total**
- Optional: health score = weighted blend of the above

---

## 16. Acceptance Criteria & Sign-off

- [ ] Every requirement has a status
- [ ] Every Implemented meets proof tiers (§6)
- [ ] Every Critical Implemented has L3 + L5 dual-control
- [ ] Negative evidence for Not Implemented where claimed
- [ ] No Critical open at release sign-off
- [ ] All evidence reproducible at named commit
- [ ] Redaction / LLM logs reviewed
- [ ] `audit-memory.json` updated (baseline_commit, health_score, changelog)
- **Sign-off:** Audit Lead + Security Specialist + Product Owner (date + commit)

---

## 17. Thoughtful Extras (beyond original prompts)

Auditors and agents **must** also consider:

1. **SBOM / dependency risk** — generate SBOM; gate on critical CVEs and forbidden licenses.
2. **Data classification & residency** — map stores and processors; flag cross-border LLM egress.
3. **Secrets & key rotation** — presence of vault/KMS; rotation evidence; no long-lived keys in repo.
4. **Backup / DR** — documented RPO/RTO; restore drill evidence (L2/L4).
5. **Accessibility (UI)** — checklist + automated scan when UI in scope.
6. **Environment matrix** — what was actually tested where.
7. **Schema versioning** — evidence & audit-memory `schema_version`; importers reject incompatible majors.
8. **Import conflict rules** — see §14.
9. **Executive KPIs** — see §15.
10. **Dual-control for Critical closures** — L5 independent reviewer mandatory.

---

## 18. Quick Checklist & Commands

```bash
git clone --branch dev_local https://github.com/Vibe-A-Thon/EIOP repos/EIOP && cd repos/EIOP   # {{REPO_URL}} / {{BRANCH}}
git rev-parse HEAD   # record as {{BASELINE_COMMIT}}; never commit/push from the audit
# If prior memory exists:
#   cp path/to/audit-memory.json audit-output/
#   python3 audit-scripts/update_audit_memory.py --mode delta --memory audit-output/audit-memory.json

python3 audit-scripts/parse_md_requirements.py --root . --out audit-output/requirements_index.json
python3 audit-scripts/generate_traceability.py --repo-root . \
  --requirements audit-output/requirements_index.json \
  --out audit-output/traceability_matrix.csv --commit <commit-hash>
./audit-scripts/run_static_analysis.sh > audit-output/evidence/static_analysis.txt
pytest --junitxml=audit-output/evidence/tests.xml || true
python3 audit-scripts/generate_audit_report.py \
  --requirements audit-output/requirements_index.json \
  --traceability audit-output/traceability_matrix.csv \
  --evidence audit-output/evidence/ \
  --out audit-output/audit_gaps_requirements.md --commit <commit-hash>
python3 audit-scripts/validate_evidence.py --schema schemas/evidence.schema.json \
  --in audit-output/evidence/evidence.json
# Open eoip-audit-kit/tracker.html (embedded run data) or templates/tracker_template.html (blank) → Import Evidence JSON → Import Audit Memory
```

---

## 19. Paste-Ready Final Prompt (single block)

```text
You are an external multidisciplinary audit team (Technical Lead, Developer, Code Reviewer, Senior Enterprise Architect, AI Architect, AI Developer, AI Tech Lead, Gen AI Architect, Agentic AI Architect, Agentic AI Engineer, Digital Product Owner, AI-First Product Owner, CTO, Auditor, Controller, Compliance Reviewer, Cybersecurity Specialist, Security Reviewer). Perform a deep, evidence-backed audit of the EOIP (kgf) application by comparing every .md requirement file to the actual implementation (code, infra, CI/CD, tests, runtime, observability).

Produce under audit-output/: audit_gaps_requirements.md, requirements_index.json, traceability_matrix.csv, audit_tasks.json, audit-memory.json, evidence/evidence.json (schema 1.0.0), evidence/ raw artifacts, and audit-scripts/.

STRICT PROOF POLICY 1.1.0: L0 forbidden in evidence.json; L1 NEVER counts toward Partial or Implemented; Partial requires ≥ L2 + explicit residual_gaps; Implemented requires L2 AND (L3 on same git_commit OR L4 non-prod); Critical Implemented requires L3 + L5 dual-control (reviewer_id ≠ producer agent_id); conflicting evidence → Ambiguous; NI needs negative_proof or absence repro_command; evidence stale if git_commit ≠ audited commit. Set proof_policy_version to 1.1.0 on evidence.json and audit-memory.json.

Read audit-memory.json first for delta audits: deep-audit new/changed requirements and touched files; minimal re-verify unchanged Implemented work. Use claim/locks + prompt hashes for multi-agent handoff; never store secrets/PII in evidence or memory.

Also assess: SBOM/dependency risk, data classification & residency, secrets/key rotation, backup/DR, accessibility if UI, environment matrix, schema versioning.

Follow the Enhanced Audit Prompt (kit ENHANCED_AUDIT_PROMPT.md) for methodology, templates, severity matrix, import conflict rules, and sign-off. Prefer Python automation; redact before any LLM use. Sign-off requires Audit Lead, Security Specialist, and Product Owner with date and commit hash. Operators will import evidence.json into tracker.html for executive KPIs and automatic status updates.
```

---

*End of authoritative Enhanced Audit Prompt.*
