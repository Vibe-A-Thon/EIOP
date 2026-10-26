# EPIC-LIVINGAIAGGGRA-UNTR: living-AI-agg-Graffin-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 4 tasks, ~29.0 h, priorities {'P1': 4}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-GRF-OPS-001 [P1] GRF-OPS-001: Autonomic Self-Healing Loop Execution

- **Source:** `living-AI-agg-Graffin-requirements.md:273-279` (heading) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-GRF-OPS-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### `GRF-OPS-001`: Autonomic Self-Healing Loop Execution
- **Description**: Graffin **MUST** autonomously detect and repair database inconsistencies, Merkle tree lag, and outbox stalls.
- **Specification**: Executes an hourly OODA loop (Observe DB stats, Orient vs. thresholds, Decide repair recipe, Act with rollback protection).
- **Done-When**:
  - `GRF-OPS-001.D01`: Simulated SQLite corruption triggers automatic quarantine and repair notification.
  - `GRF-OPS-001.D02`: 100% of outbox events older than 60s are processed without loss.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GRF-OPS-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GRF-OPS-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GRF-OPS-001

**Acceptance criteria**
- [ ] Graffin MUST autonomously detect and repair database inconsistencies, Merkle tree lag, and outbox stalls.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GRF-OPS-002 [P1] GRF-OPS-002: Continuous Performance & Index Governor

- **Source:** `living-AI-agg-Graffin-requirements.md:280-286` (heading) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-GRF-OPS-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### `GRF-OPS-002`: Continuous Performance & Index Governor
- **Description**: Graffin **MUST** continuously optimize graph query performance.
- **Specification**: Tracks query execution plans using SQLite `EXPLAIN QUERY PLAN`. If an unindexed table scan is detected on a query executed $\ge 50$ times, Graffin creates an index proposal.
- **Done-When**:
  - `GRF-OPS-002.D01`: Slow query detection triggers automated index creation under Autonomy L3/L4.
  - `GRF-OPS-002.D02`: p95 query latency improves by $\ge 25\%$ on synthetic load tests.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GRF-OPS-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GRF-OPS-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GRF-OPS-002

**Acceptance criteria**
- [ ] Graffin MUST continuously optimize graph query performance.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GRF-OPS-003 [P1] GRF-OPS-003: Autonomous REVA Proof-of-Done Orchestration

- **Source:** `living-AI-agg-Graffin-requirements.md:287-293` (heading) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-GRF-OPS-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### `GRF-OPS-003`: Autonomous REVA Proof-of-Done Orchestration
- **Description**: Graffin **MUST** run the REVA verifier pipeline on every code change and emit signed ledgers.
- **Specification**: Invokes `reva.pd.runs.run_verifier`, evaluates 11-step closure checks, computes `ldg1_...` ID, signs with PD key, and updates `reva-tracker.html`.
- **Done-When**:
  - `GRF-OPS-003.D01`: Git commit triggers automated closure evaluation resulting in signed `reva-ledger.json`.
  - `GRF-OPS-003.D02`: Tracker HTML progress updates to reflect closed items automatically.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GRF-OPS-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GRF-OPS-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GRF-OPS-003

**Acceptance criteria**
- [ ] Graffin MUST run the REVA verifier pipeline on every code change and emit signed ledgers.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GRF-OPS-004 [P1] GRF-OPS-004: Autonomous Repository Ingestion & Continuous Knowledge/Wisdom Graph Maintenance

- **Source:** `living-AI-agg-Graffin-requirements.md:294-312` (heading) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 3 other site(s): see duplicate task DUP-GRF-OPS-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### `GRF-OPS-004`: Autonomous Repository Ingestion & Continuous Knowledge/Wisdom Graph Maintenance
- **Description**: Whenever a GitHub, GitLab, Bitbucket, or Git repository URL is provided, Graffin **MUST** autonomously ingest the repository into an isolated sandbox, execute pure-Python extractors to project the codebase into the Knowledge Graph (GL0–GL3) and Wisdom Graph (GW), and strictly prevent any proprietary code or secret leaks to LLMs.
- **Specification**:
  1. Clones the remote repository using REVA's sandboxed `GitRepositoryCloner` with shallow depth (`--depth 1` default), time budget ($\le 300\text{s}$), and size quota ($\le 5\text{ GiB}$).
  2. Executes pure-Python extraction ($\ge 95\%$ deterministic Python logic using Tree-sitter, Capstone, `pyelftools`, and `axml`):
     - Maps application boundaries, services, routes, and resources into the Knowledge Graph.
     - Disassembles embedded native libraries (`.so`, `.dll`) and maps JNI native bridges (`reva_CALLS_NATIVE`).
     - Parses Architectural Decision Records (ADRs) and Conventional Commits into Wisdom Graph `wg_Decision`, `wg_Precedent`, and `wg_Lesson` nodes.
  3. Enforces the **Zero-Data-Leak LLM Egress Gate** (`REVA-SEC-013`):
     - Local offline LLMs (via Ollama/vLLM) are the mandatory default; external LLM calls are blocked unless explicitly authorized.
     - Automated RFC 6901 pointer redaction scrubs all tokens, keys, passwords, database URLs, and PII.
     - Proprietary source code is never transmitted raw; it is abstracted into pseudonymized structural tokens.
- **Done-When**:
  - `GRF-OPS-004.D01`: Submitting a repository URL triggers automated cloning, boundary extraction, and Knowledge Graph projection without manual intervention.
  - `GRF-OPS-004.D02`: ADRs and commit histories are synthesized into the Wisdom Graph with `reva_JUSTIFIED_BY` edges.
  - `GRF-OPS-004.D03`: 100% of LLM egress payloads pass DLP byte-scans with zero secret leaks and zero raw source code.

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GRF-OPS-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GRF-OPS-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GRF-OPS-004

**Acceptance criteria**
- [ ] Whenever a GitHub, GitLab, Bitbucket, or Git repository URL is provided, Graffin MUST autonomously ingest the repository into an isolated sandbox, execute pure-Python extractors to project the codebase into the Knowledge Graph (GL0–GL3) and Wisdom Graph (GW), and strictly prevent any proprietary code or secret leaks to LLMs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

