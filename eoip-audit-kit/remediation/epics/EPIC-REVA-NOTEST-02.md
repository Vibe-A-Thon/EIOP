# EPIC-REVA-NOTEST-02: reva-requirements.md · code_no_test

*Code references the ID but no test is mapped.* 26 tasks, ~66.3 h, priorities {'P2': 26}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REVA-PD-004 [P2] REVA-PD-004: Anti-gaming checks: AG-01 skipped, xfail, xpass and error outcomes are not passes. AG-02 each counted test carries the obligation marker (@pytest.mark.reva_obligation("OBL-…"), Playwright tag @OBL-…, 

- **Source:** `reva-requirements.md:787-787` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 3.8 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-004 | Anti-gaming checks: **AG-01** skipped, xfail, xpass and error outcomes are not passes. **AG-02** each counted test carries the obligation marker (`@pytest.mark.reva_obligation("OBL-…")`, Playwright tag `@OBL-…`, or JUnit `<property name="reva_obligation">`). **AG-03** per-test coverage contexts show the test executed ≥ 1 line inside each owner span (Python via coverage contexts; for TS/JS UI owners, Istanbul coverage from the instrumented acceptance build). **AG-04** REVA mutation probe (REVA-PD-005) kill ratio ≥ `REVA_MUTATION_MIN` (default 0.70) for Python owners at unit/component depth. **AG-05** each counted test function contains ≥ 1 meaningful assertion (AST check: `assert` on a non-constant, `pytest.raises`, `expect(...)`, `assertThat`); `assert True` and asserting literals are flagged. **AG-06** the test does not patch or mock the owner symbol itself. **AG-07** reruns (`REVA_RERUNS`, default 3) all pass, otherwise `flaky`. **AG-08** owner digest at run time equals the current owner digest, otherwise `stale`. **AG-09** the run came from a clean checkout (`git status --porcelain` empty, tree digest recorded). **AG-10** environment fingerprint recorded (image digest or interpreter + OS + lockfile digest). **AG-11** the verifier argv equals the binding's argv (no ad-hoc commands). **AG-12** the result artifacts referenced by the attestation exist in the blob store with matching digests. **AG-13** test count for the obligation > 0 after filtering. **AG-14** a fixture's declared sha256 matches the file at the run commit. | One failing fixture per AG rule demonstrates the rejection reason; a fully compliant fixture closes. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/antigaming.py:1, reva/pd/closure.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-PD-004') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] One failing fixture per AG rule demonstrates the rejection reason; a fully compliant fixture closes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/antigaming.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/antigaming.py#L1-L1), [`reva/pd/closure.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/closure.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-007 [P2] REVA-PD-007: Staleness monitor: on every commit ingested by KGF's git connector (or every git pull in local mode), recompute owner digests for bound obligations and mark changed ones stale without running anything

- **Source:** `reva-requirements.md:790-790` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-007 | Staleness monitor: on every commit ingested by KGF's git connector (or every `git pull` in local mode), recompute owner digests for bound obligations and mark changed ones `stale` without running anything. | Commit touching an owner flips status within one ingestion cycle; untouched obligations remain closed. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/staleness.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-PD-007') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Commit touching an owner flips status within one ingestion cycle; untouched obligations remain closed
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/staleness.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/staleness.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-009 [P2] REVA-PD-009: Readiness gates: a gate is an ordered list of stages, each with required obligations and/or checks. Aggregation is fail-closed: any open, failed, blocked, stale, flaky, unknown in a stage makes the st

- **Source:** `reva-requirements.md:792-792` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-009 | Readiness gates: a gate is an ordered list of stages, each with required obligations and/or checks. Aggregation is fail-closed: any `open, failed, blocked, stale, flaky, unknown` in a stage makes the stage non-pass. Each finding reports `stage, reason_code, obligation_key, warrant/attestation ids, next_action`. | REVA's own release gate (§14.3) evaluates correctly on fixtures; a single stale obligation blocks the gate. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/gates.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-PD-009') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] REVA's own release gate (§14.3) evaluates correctly on fixtures; a single stale obligation blocks the gate
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/gates.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/gates.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-011 [P2] REVA-PD-011: Ledger exports: reva-ledger.json (canonical), reva-ledger.md (human summary) and a self-contained reva-ledger.html tracker (filters by status, layer, requirement, owner; drill-down to reasons, runs, a

- **Source:** `reva-requirements.md:794-794` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-011 | Ledger exports: `reva-ledger.json` (canonical), `reva-ledger.md` (human summary) and a self-contained `reva-ledger.html` tracker (filters by status, layer, requirement, owner; drill-down to reasons, runs, attestations; no external network requests). | HTML opens offline; numbers match the JSON; Playwright snapshot test. | acceptance
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/export_html.py:1, reva/pd/ledger.py:1, scripts/reva/build_reva_ledger.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-PD-011') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] HTML opens offline; numbers match the JSON; Playwright snapshot test
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/export_html.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/export_html.py#L1-L1), [`reva/pd/ledger.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/ledger.py#L1-L1), [`scripts/reva/build_reva_ledger.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/reva/build_reva_ledger.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-PD-012 [P2] REVA-PD-012: Waivers: a human-attested waiver can set an obligation's disposition to deferred or out_of_scope, or suppress a named equivalent mutant, with mandatory rationale and expiry. Waived obligations are rep

- **Source:** `reva-requirements.md:795-795` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-PD-012 | Waivers: a human-attested waiver can set an obligation's disposition to `deferred` or `out_of_scope`, or suppress a named equivalent mutant, with mandatory rationale and expiry. Waived obligations are reported separately and never counted as closed. | Waiver without expiry is rejected; expired waivers reopen automatically. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/waivers.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-PD-012') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Waiver without expiry is rejected; expired waivers reopen automatically
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/waivers.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/waivers.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-RO-001 [P2] REVA-RO-001: Supervised headless browser controller. Manages headless Chrome or Chromium instances via Playwright/CDP; restricts network connections to isolated loopback network or explicit tenant allowlists; enfo

- **Source:** `reva-requirements.md:1153-1153` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-RO-001 | Supervised headless browser controller. Manages headless Chrome or Chromium instances via Playwright/CDP; restricts network connections to isolated loopback network or explicit tenant allowlists; enforces session cleanup. | Spawns headless browser; navigates to target local test app; terminates cleanly without orphaned processes on host. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/obs/browser_cdp.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-RO-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Spawns headless browser; navigates to target local test app; terminates cleanly without orphaned processes on host
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/obs/browser_cdp.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/obs/browser_cdp.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-RO-003 [P2] REVA-RO-003: DOM and accessibility tree state snapshot engine. Captures DOM snapshots and accessibility trees at key interaction milestones; synthesizes deterministic, resilient CSS and XPath selectors for interac

- **Source:** `reva-requirements.md:1155-1155` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-RO-003 | DOM and accessibility tree state snapshot engine. Captures DOM snapshots and accessibility trees at key interaction milestones; synthesizes deterministic, resilient CSS and XPath selectors for interactive elements. | Emits DOM snapshots with sanitized text; generates stable element selectors; links UI elements to observed API network calls (`reva_BrowserInteraction` -> `reva_Boundary`). | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/obs/interaction_recorder.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-RO-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Emits DOM snapshots with sanitized text; generates stable element selectors; links UI elements to observed API network calls (revaBrowserInteraction -> revaBoundary)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/obs/interaction_recorder.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/obs/interaction_recorder.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-001 [P2] REVA-SP-001: Go buildinfo (ELF, PE, Mach-O): locate the build-info header by its public magic, parse the inline-string format (Go ≥ 1.18): Go version, main module path/version/sum, dependencies (path, version, sum

- **Source:** `reva-requirements.md:856-856` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-001 | **Go buildinfo** (ELF, PE, Mach-O): locate the build-info header by its public magic, parse the inline-string format (Go ≥ 1.18): Go version, main module path/version/sum, dependencies (path, version, sum, replacements), build settings (`-compiler`, `CGO_ENABLED`, `GOOS`, `GOARCH`, `vcs`, `vcs.revision`, `vcs.time`, `vcs.modified`, …). The pre-1.18 pointer format yields an `unavailable` warrant with reason `GO_LEGACY_BUILDINFO` unless pointer resolution succeeds via section mapping. | Fixtures built in CI from a tiny Go program (with and without VCS stamping) parse exactly; a non-Go binary yields `unavailable` with reason, not "no dependencies". | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/extract/provenance/extractor.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-SP-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Fixtures built in CI from a tiny Go program (with and without VCS stamping) parse exactly; a non-Go binary yields unavailable with reason, not "no dependencies"
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/extract/provenance/extractor.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/extract/provenance/extractor.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TL-001 [P2] REVA-TL-001: Implement an append-only Merkle tree per log (§6.9) with persistent leaf storage and cached internal nodes, supporting append(leaf_data) -> leaf_index. · Root hashes match an independent reference imp

- **Source:** `reva-requirements.md:694-694` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TL-001 | Implement an append-only Merkle tree per log (§6.9) with persistent leaf storage and cached internal nodes, supporting `append(leaf_data) -> leaf_index`. | Root hashes match an independent reference implementation written in the test suite for trees of size 1…2,049; appends survive restarts. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/translog.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-TL-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Root hashes match an independent reference implementation written in the test suite for trees of size 1…2,049; appends survive restarts
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/translog.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/translog.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TL-003 [P2] REVA-TL-003: Inclusion proof GET /logs/{log_id}/proof/inclusion?leaf_index=&tree_size= and consistency proof …/consistency?first=&second= per RFC 6962 §2.1.1–2.1.2. · Proofs verify for random pairs across 10,000 a

- **Source:** `reva-requirements.md:696-696` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TL-003 | Inclusion proof `GET /logs/{log_id}/proof/inclusion?leaf_index=&tree_size=` and consistency proof `…/consistency?first=&second=` per RFC 6962 §2.1.1–2.1.2. | Proofs verify for random pairs across 10,000 appends; altered proof bytes fail. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/translog.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-TL-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Proofs verify for random pairs across 10,000 appends; altered proof bytes fail
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/translog.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/translog.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TL-005 [P2] REVA-TL-005: Optional STH witnessing: export STHs to an external, write-once location (REVA_STH_WITNESS_DIR or an S3 bucket with object lock) for third-party verification. · When configured, every STH appears in t

- **Source:** `reva-requirements.md:698-698` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TL-005 | Optional STH witnessing: export STHs to an external, write-once location (`REVA_STH_WITNESS_DIR` or an S3 bucket with object lock) for third-party verification. | When configured, every STH appears in the witness location; `kgf reva verify-log --witness` checks continuity. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/sth.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-TL-005') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] When configured, every STH appears in the witness location; kgf reva verify-log --witness checks continuity
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/sth.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/sth.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VS-001 [P2] REVA-VS-001: Profiles: static (no execution beyond parsers), unit (subprocess, no network, rlimits), component (as unit, plus local temp DB allowed), integration (container or netns with loopback + declared servic

- **Source:** `reva-requirements.md:825-825` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VS-001 | Profiles: `static` (no execution beyond parsers), `unit` (subprocess, no network, rlimits), `component` (as unit, plus local temp DB allowed), `integration` (container or netns with loopback + declared service network), `acceptance` (ephemeral Compose project `reva-verify-<run>` with the full KGF stack, torn down afterwards). | Each profile has a conformance test proving its network policy (attempted external connect fails in `unit`). | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/sandbox/profiles.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-VS-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Each profile has a conformance test proving its network policy (attempted external connect fails in unit)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/sandbox/profiles.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/sandbox/profiles.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VS-002 [P2] REVA-VS-002: Clean checkout: verifier runs use a fresh git worktree (or clone) at the target commit in a REVA-owned temp root; untracked files are forbidden; the tree digest is recorded. · A run requested with a d

- **Source:** `reva-requirements.md:826-826` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VS-002 | Clean checkout: verifier runs use a fresh `git worktree` (or clone) at the target commit in a REVA-owned temp root; untracked files are forbidden; the tree digest is recorded. | A run requested with a dirty tree is refused with `REVA_E_DIRTY_TREE`. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/sandbox/checkout.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-VS-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] A run requested with a dirty tree is refused with REVAEDIRTYTREE
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/sandbox/checkout.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/sandbox/checkout.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VS-006 [P2] REVA-VS-006: Collectors: pytest is invoked with --junitxml, --cov with --cov-context=test and JSON export with contexts; Playwright with JSON reporter, trace and screenshots; server-side coverage for acceptance ru

- **Source:** `reva-requirements.md:830-830` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VS-006 | Collectors: pytest is invoked with `--junitxml`, `--cov` with `--cov-context=test` and JSON export with contexts; Playwright with JSON reporter, trace and screenshots; server-side coverage for acceptance runs via `COVERAGE_PROCESS_START`; HAR capture for API journeys. All artifacts are hashed into the blob store. | A sample run produces all declared artifact kinds with digests matching blob content. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/sandbox/collectors.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-VS-006') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] A sample run produces all declared artifact kinds with digests matching blob content
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/sandbox/collectors.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/sandbox/collectors.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VS-007 [P2] REVA-VS-007: Result parsing is done by REVA from raw artifacts (JUnit XML, coverage JSON, Playwright JSON). Malformed artifacts make the run unknown, never pass. · Fuzzed/malformed JUnit XML yields unknown with re

- **Source:** `reva-requirements.md:831-831` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VS-007 | Result parsing is done by REVA from raw artifacts (JUnit XML, coverage JSON, Playwright JSON). Malformed artifacts make the run `unknown`, never `pass`. | Fuzzed/malformed JUnit XML yields `unknown` with reason `ARTIFACT_MALFORMED`. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/sandbox/collectors.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-VS-007') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Fuzzed/malformed JUnit XML yields unknown with reason ARTIFACTMALFORMED
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/sandbox/collectors.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/sandbox/collectors.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VS-009 [P2] REVA-VS-009: Queue and concurrency: runs are jobs with priority; max concurrent runs per tenant (REVA_MAX_RUNS, default 2); cancellable via API with cancellation recorded on the run. · Cancellation mid-run yields 

- **Source:** `reva-requirements.md:833-833` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VS-009 | Queue and concurrency: runs are jobs with priority; max concurrent runs per tenant (`REVA_MAX_RUNS`, default 2); cancellable via API with cancellation recorded on the run. | Cancellation mid-run yields `cancelled` status, cleaned resources and a partial-artifact list. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/pd/runs.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-VS-009') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Cancellation mid-run yields cancelled status, cleaned resources and a partial-artifact list
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/pd/runs.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/pd/runs.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VW-001 [P2] REVA-VW-001: View kinds over any warrant or workflow result: summary, facet (named section), item (by key), page (offset/limit over a declared collection). Each view returns `{view_id, parent_id, coverage{status: 

- **Source:** `reva-requirements.md:974-974` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VW-001 | View kinds over any warrant or workflow result: `summary`, `facet` (named section), `item` (by key), `page` (offset/limit over a declared collection). Each view returns `{view_id, parent_id, coverage{status: complete_within_view\|page\|empty, examined, total, next_offset, exhausted}, items, limitations}`. | Paging through a 10,000-item collection returns every item exactly once in stable order. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/views/budget.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-VW-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Paging through a 10,000-item collection returns every item exactly once in stable order
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/views/budget.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/views/budget.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-001 [P2] REVA-WK-001: Implement RFC 8785 canonical JSON in reva.core.jcs.canonicalize(value) -> bytes. Reject NaN/Infinity, non-string keys, circular references, and floats in hash-bearing structures (allow_float=False def

- **Source:** `reva-requirements.md:672-672` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-001 | Implement RFC 8785 canonical JSON in `reva.core.jcs.canonicalize(value) -> bytes`. Reject NaN/Infinity, non-string keys, circular references, and floats in hash-bearing structures (`allow_float=False` default). | Passes every RFC 8785 Appendix test vector; byte-identical to the `rfc8785` package for 10,000 Hypothesis-generated JSON values without floats; rejects each invalid class with `REVA_E_CANONICALIZATION`. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/core/jcs.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Passes every RFC 8785 Appendix test vector; byte-identical to the rfc8785 package for 10,000 Hypothesis-generated JSON values without floats; rejects each invalid class with REVAECANONICALIZATION
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/core/jcs.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/core/jcs.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-002 [P2] REVA-WK-002: Implement the identifier derivations in §6.2 in reva.core.ids, with one function per prefix and a verify_id(obj, id) helper. · Golden tests: fixed inputs produce fixed IDs (golden file committed); any

- **Source:** `reva-requirements.md:673-673` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-002 | Implement the identifier derivations in §6.2 in `reva.core.ids`, with one function per prefix and a `verify_id(obj, id)` helper. | Golden tests: fixed inputs produce fixed IDs (golden file committed); any single-field mutation changes the ID; set-ordering permutations do not. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/core/digest.py:1, reva/core/ids.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Golden tests: fixed inputs produce fixed IDs (golden file committed); any single-field mutation changes the ID; set-ordering permutations do not
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/core/digest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/core/digest.py#L1-L1), [`reva/core/ids.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/core/ids.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-004 [P2] REVA-WK-004: Enforce validation rules V-01…V-16 (§6.3.3) in a single validate_warrant_body() that returns all violations, not only the first. · One positive and one negative test per rule; a body violating three r

- **Source:** `reva-requirements.md:675-675` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-004 | Enforce validation rules V-01…V-16 (§6.3.3) in a single `validate_warrant_body()` that returns *all* violations, not only the first. | One positive and one negative test per rule; a body violating three rules reports all three with JSON pointers. | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/validation.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-004') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] One positive and one negative test per rule; a body violating three rules reports all three with JSON pointers
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/validation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/validation.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-005 [P2] REVA-WK-005: Provide a predicate registry: register_predicate(name, statement_model, allowed_authorities, allowed_epistemic, requires_coverage: bool). issue() rejects unregistered predicates. REVA registers every 

- **Source:** `reva-requirements.md:676-676` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-005 | Provide a **predicate registry**: `register_predicate(name, statement_model, allowed_authorities, allowed_epistemic, requires_coverage: bool)`. `issue()` rejects unregistered predicates. REVA registers every predicate it produces in `reva/kernel/predicates.py` (catalogue in §10.4). | Issuing with an unknown predicate fails with `REVA_E_PREDICATE_UNKNOWN`; registry listing is exposed via REST `GET /predicates`. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/registry.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-005') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Issuing with an unknown predicate fails with REVAEPREDICATEUNKNOWN; registry listing is exposed via REST GET /predicates
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/registry.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/registry.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-006 [P2] REVA-WK-006: Support bitemporal semantics: valid_time in the body, recorded_at in the envelope. Queries accept as_of_valid and as_of_recorded and return the warrants that were valid / known at those instants. · Fi

- **Source:** `reva-requirements.md:677-677` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-006 | Support bitemporal semantics: `valid_time` in the body, `recorded_at` in the envelope. Queries accept `as_of_valid` and `as_of_recorded` and return the warrants that were valid / known at those instants. | Fixture with three supersessions returns the correct warrant for six (valid, recorded) query pairs. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/query.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-006') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Fixture with three supersessions returns the correct warrant for six (valid, recorded) query pairs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/query.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/query.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-008 [P2] REVA-WK-008: Batch issue: issue_many(drafts) with one transaction per batch (default 500) and one log append per warrant. · 50,000 warrants issued in batches; counts in store and log are equal; throughput meets RE

- **Source:** `reva-requirements.md:679-679` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-008 | Batch issue: `issue_many(drafts)` with one transaction per batch (default 500) and one log append per warrant. | 50,000 warrants issued in batches; counts in store and log are equal; throughput meets REVA-NFR-001. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/kernel.py:259
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-008') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] 50,000 warrants issued in batches; counts in store and log are equal; throughput meets REVA-NFR-001
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/kernel.py:259`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/kernel.py#L259-L259)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-011 [P2] REVA-WK-011: Supersession and retraction: supersede(old_id, new_draft, reason) and retract(id, reason) issue new warrants with supersedes links and flip the old envelope status. Nothing is ever deleted except by t

- **Source:** `reva-requirements.md:682-682` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-011 | Supersession and retraction: `supersede(old_id, new_draft, reason)` and `retract(id, reason)` issue new warrants with `supersedes` links and flip the old envelope status. Nothing is ever deleted except by the retention engine (REVA-SEC-012). | Superseded warrants are excluded from "current" queries but returned by as-of queries and audit views. | integration
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/kernel.py:289
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-011') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Superseded warrants are excluded from "current" queries but returned by as-of queries and audit views
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/kernel.py:289`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/kernel.py#L289-L289)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-013 [P2] REVA-WK-013: Draft builder helpers for producers: WarrantDraftBuilder with fluent methods (about_artifact(), about_record(), at_span(), with_coverage(), limitation(), derived_from()), so producers cannot forget re

- **Source:** `reva-requirements.md:684-684` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-013 | Draft builder helpers for producers: `WarrantDraftBuilder` with fluent methods (`about_artifact()`, `about_record()`, `at_span()`, `with_coverage()`, `limitation()`, `derived_from()`), so producers cannot forget required fields. | Every REVA extractor uses the builder (static check: no direct body construction outside `reva.kernel`). | unit
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/builder.py:1, reva/kernel/producers.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-013') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Every REVA extractor uses the builder (static check: no direct body construction outside reva.kernel)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/builder.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/builder.py#L1-L1), [`reva/kernel/producers.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/producers.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-WK-014 [P2] REVA-WK-014: Producer registry: register producers (prd1_ ID, type, name, version, build digest, owner) and their keys; list and deactivate. Human producers map 1:1 to KGF principals. · Issuing with an unregistere

- **Source:** `reva-requirements.md:685-685` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-WK-014 | Producer registry: register producers (`prd1_` ID, type, name, version, build digest, owner) and their keys; list and deactivate. Human producers map 1:1 to KGF principals. | Issuing with an unregistered or deactivated producer fails with `REVA_E_PRODUCER`. | component
```
</details>

**Next steps**
1. Read the referenced code: reva/kernel/builder.py:1, reva/kernel/producers.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('REVA-WK-014') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Issuing with an unregistered or deactivated producer fails with REVAEPRODUCER
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/kernel/builder.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/builder.py#L1-L1), [`reva/kernel/producers.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/kernel/producers.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

