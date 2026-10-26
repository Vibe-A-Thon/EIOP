# EPIC-PROCESSINGUNIT-NOTRUN-02: processing-units-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 37 tasks, ~37.0 h, priorities {'P2': 37}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-PUR-FND-004 [P2] PUR-FND-004: Maintain CPU reference implementations for every v1 operator, including model/simulator operators in their optional environments

- **Source:** `processing-units-requirements.md:103-103` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-FND-004 | Maintain CPU reference implementations for every v1 operator, including model/simulator operators in their optional environments. | The complete v1 operator matrix executes on CPU; absent artifacts are not counted as passes.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] The complete v1 operator matrix executes on CPU; absent artifacts are not counted as passes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-FND-005 [P2] PUR-FND-005: Preserve proprietary first-party licensing and third-party notices; inventory native runtimes, models, fonts/language data and codecs separately

- **Source:** `processing-units-requirements.md:104-104` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-FND-005 | Preserve proprietary first-party licensing and third-party notices; inventory native runtimes, models, fonts/language data and codecs separately. | Distributable artifact scan matches SBOM and license notices; no unreviewed redistribution.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Distributable artifact scan matches SBOM and license notices; no unreviewed redistribution
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-FND-006 [P2] PUR-FND-006: Reconcile ADR-H16 and neural-tier documentation before releasing any optional accelerator artifact

- **Source:** `processing-units-requirements.md:105-105` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-FND-006 | Reconcile ADR-H16 and neural-tier documentation before releasing any optional accelerator artifact. | Reviewed decision, unchanged core CPU compliance and new profile-specific distribution checks all agree.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Reviewed decision, unchanged core CPU compliance and new profile-specific distribution checks all agree
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-FND-008 [P2] PUR-FND-008: Keep new processing state and contracts compatible with future suite extraction into the platform owner

- **Source:** `processing-units-requirements.md:107-107` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-FND-008 | Keep new processing state and contracts compatible with future suite extraction into the platform owner. | Import-boundary checks and an installed-package API/worker run succeed without source-tree-only imports.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Import-boundary checks and an installed-package API/worker run succeed without source-tree-only imports
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-GPU-004 [P2] PUR-GPU-004: sparse.matmul: validated CSR-by-dense multiplication, stable row IDs, no implicit densification of the sparse input

- **Source:** `processing-units-requirements.md:308-308` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-GPU-004 | `sparse.matmul`: validated CSR-by-dense multiplication, stable row IDs, no implicit densification of the sparse input. | Sparse reference parity plus peak-memory observation; unsupported accelerator path explicitly uses CPU or rejects.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Sparse reference parity plus peak-memory observation; unsupported accelerator path explicitly uses CPU or rejects
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-GPU-005 [P2] PUR-GPU-005: Qualify optional GPU execution for the supported dense ONNX subset of the preceding operators, with actual placement and transfer accounting

- **Source:** `processing-units-requirements.md:309-309` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-GPU-005 | Qualify optional GPU execution for the supported dense ONNX subset of the preceding operators, with actual placement and transfer accounting. | A physical eligible GPU runs real operations; CPU-forced, missing-device and strict-no-fallback cases are separately observed.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A physical eligible GPU runs real operations; CPU-forced, missing-device and strict-no-fallback cases are separately observed
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-INT-002 [P2] PUR-INT-002: Extend the existing CLI with processing capabilities, devices, plan, submit, status, cancel, receipt and verify-evidence

- **Source:** `processing-units-requirements.md:399-399` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-INT-002 | Extend the existing CLI with `processing capabilities`, `devices`, `plan`, `submit`, `status`, `cancel`, `receipt` and `verify-evidence`. | Installed CLI reaches the same governed service; no alternate unrestricted local execution path.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Installed CLI reaches the same governed service; no alternate unrestricted local execution path
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-INT-003 [P2] PUR-INT-003: Integrate DPU/VPU outputs with the real ingestion pipeline and preserve source/provenance/quality records

- **Source:** `processing-units-requirements.md:400-400` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-INT-003 | Integrate DPU/VPU outputs with the real ingestion pipeline and preserve source/provenance/quality records. | A document/record artifact becomes reviewable knowledge through existing ingestion, with reconciled counts.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A document/record artifact becomes reviewable knowledge through existing ingestion, with reconciled counts
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-INT-007 [P2] PUR-INT-007: Add Operations views for physical resources, logical capabilities, jobs, limits, errors and actual execution placement

- **Source:** `processing-units-requirements.md:404-404` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-INT-007 | Add Operations views for physical resources, logical capabilities, jobs, limits, errors and actual execution placement. | A CPU-only session and a qualified accelerated session show truthful distinct states.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A CPU-only session and a qualified accelerated session show truthful distinct states
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-INT-010 [P2] PUR-INT-010: Preserve feature usability without LLM/GPU/NPU and expose loading/empty/denied/unavailable/stale/partial/error/cancelled states accessibly

- **Source:** `processing-units-requirements.md:407-407` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-INT-010 | Preserve feature usability without LLM/GPU/NPU and expose loading/empty/denied/unavailable/stale/partial/error/cancelled states accessibly. | Keyboard, narrow desktop/mobile, reduced-motion and screen-reader journeys succeed without clipping or misleading success states.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Keyboard, narrow desktop/mobile, reduced-motion and screen-reader journeys succeed without clipping or misleading success states
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-IPU-003 [P2] PUR-IPU-003: graph.aggregatefeatures: one or bounded repeated sparse neighbor sum/mean steps with explicit self-loop/normalization semantics

- **Source:** `processing-units-requirements.md:379-379` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-IPU-003 | `graph.aggregate_features`: one or bounded repeated sparse neighbor sum/mean steps with explicit self-loop/normalization semantics. | Small analytic graph outputs match; high-degree/memory limits and missing features are handled explicitly.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Small analytic graph outputs match; high-degree/memory limits and missing features are handled explicitly
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/graph_intel.py:107`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/graph_intel.py#L107-L107)
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-IPU-005 [P2] PUR-IPU-005: graph.modelinfer: approved bounded graph-model artifact through shared CPU neural backend, preserving model-space and provenance

- **Source:** `processing-units-requirements.md:381-381` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-IPU-005 | `graph.model_infer`: approved bounded graph-model artifact through shared CPU neural backend, preserving model-space and provenance. | Real inference, held-out task evaluation, CPU baseline and missing-model denial; never substitute random vectors or zero scores.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Real inference, held-out task evaluation, CPU baseline and missing-model denial; never substitute random vectors or zero scores
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-NPU-003 [P2] PUR-NPU-003: model.classify: approved small classifier with labels, score semantics and abstention threshold from its evaluated manifest

- **Source:** `processing-units-requirements.md:327-327` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-NPU-003 | `model.classify`: approved small classifier with labels, score semantics and abstention threshold from its evaluated manifest. | Held-out task metrics beat/meet the declared baseline; scores are not falsely presented as calibrated probabilities.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Held-out task metrics beat/meet the declared baseline; scores are not falsely presented as calibrated probabilities
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-NPU-005 [P2] PUR-NPU-005: Qualify Intel OpenVINO NPU as a separate optional provider for at least one approved bounded inference model

- **Source:** `processing-units-requirements.md:329-329` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-NPU-005 | Qualify Intel OpenVINO NPU as a separate optional provider for at least one approved bounded inference model. | Physical-device trace, CPU comparison, unsupported-op/shape handling and missing-driver failure are retained.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Physical-device trace, CPU comparison, unsupported-op/shape handling and missing-driver failure are retained
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-OPS-001 [P2] PUR-OPS-001: Ship explicit core/numerical/ONNX/text/vision/quantum profiles with per-OS locks and offline wheel/artifact manifests

- **Source:** `processing-units-requirements.md:419-419` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-OPS-001 | Ship explicit core/numerical/ONNX/text/vision/quantum profiles with per-OS locks and offline wheel/artifact manifests. | Clean install, uninstall, missing-extra and offline reinstall execute real workload fixtures.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Clean install, uninstall, missing-extra and offline reinstall execute real workload fixtures
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-OPS-002 [P2] PUR-OPS-002: Separate mutually incompatible accelerator runtimes into owned worker environments; do not install CPU/GPU variants over each other blindly

- **Source:** `processing-units-requirements.md:420-420` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-OPS-002 | Separate mutually incompatible accelerator runtimes into owned worker environments; do not install CPU/GPU variants over each other blindly. | Dependency checks and actual session creation pass in each declared profile; core environment remains CPU-only.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Dependency checks and actual session creation pass in each declared profile; core environment remains CPU-only
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-OPS-008 [P2] PUR-OPS-008: Publish operator catalog, support matrix, limits, security/runbooks, model cards and customer-facing notices with each release

- **Source:** `processing-units-requirements.md:426-426` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-OPS-008 | Publish operator catalog, support matrix, limits, security/runbooks, model cards and customer-facing notices with each release. | Documentation generated from the actual release manifest agrees with runtime capabilities and observed evidence.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Documentation generated from the actual release manifest agrees with runtime capabilities and observed evidence
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-QPU-006 [P2] PUR-QPU-006: Estimate exponential memory before allocating; enforce method-specific caps and label every result simulation=true, physicalqpu=false

- **Source:** `processing-units-requirements.md:350-350` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-QPU-006 | Estimate exponential memory before allocating; enforce method-specific caps and label every result `simulation=true`, `physical_qpu=false`. | Oversized request is rejected; UI/report/export cannot hide simulated status or turn a result into a production decision automatically.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_quantum.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Oversized request is rejected; UI/report/export cannot hide simulated status or turn a result into a production decision automatically
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/quantum_sim.py:51`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/quantum_sim.py#L51-L51)
- tests: `tests/processing/test_quantum.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-RUN-002 [P2] PUR-RUN-002: Require non-null trusted tenant scope for customer jobs; privileged fleet actions use an explicit separate scope

- **Source:** `processing-units-requirements.md:188-188` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-002 | Require non-null trusted tenant scope for customer jobs; privileged fleet actions use an explicit separate scope. | Missing/empty/default tenant values cannot read, claim, cancel or replay another tenant's work.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Missing/empty/default tenant values cannot read, claim, cancel or replay another tenant's work
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-RUN-004 [P2] PUR-RUN-004: Enforce limits outside the event loop and, for untrusted native/model workloads, outside the main API process

- **Source:** `processing-units-requirements.md:190-190` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-004 | Enforce limits outside the event loop and, for untrusted native/model workloads, outside the main API process. | A hung native operation is terminated without hanging API health or another tenant's jobs.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A hung native operation is terminated without hanging API health or another tenant's jobs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-RUN-005 [P2] PUR-RUN-005: Bound CPU threads, process count, RAM, disk, queue depth, input/output size and wall time before admission and during execution

- **Source:** `processing-units-requirements.md:191-191` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-005 | Bound CPU threads, process count, RAM, disk, queue depth, input/output size and wall time before admission and during execution. | Oversized plans fail before allocation; overruns terminate and clean up without host exhaustion.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Oversized plans fail before allocation; overruns terminate and clean up without host exhaustion
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-RUN-007 [P2] PUR-RUN-007: Use per-tenant fair queues and bounded concurrency; no tenant controls priority through untrusted payload fields

- **Source:** `processing-units-requirements.md:193-193` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-007 | Use per-tenant fair queues and bounded concurrency; no tenant controls priority through untrusted payload fields. | Under two-tenant saturation, each eligible tenant progresses within the configured queue-age bound.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Under two-tenant saturation, each eligible tenant progresses within the configured queue-age bound
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-RUN-010 [P2] PUR-RUN-010: Track estimates separately from measured time/memory/device placement; include model loading, transfers and compilation

- **Source:** `processing-units-requirements.md:196-196` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-010 | Track estimates separately from measured time/memory/device placement; include model loading, transfers and compilation. | Receipts expose queue/startup/compute/transfer/end-to-end timings without claiming estimates are measurements.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Receipts expose queue/startup/compute/transfer/end-to-end timings without claiming estimates are measurements
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/devices.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/devices.py#L1-L1)
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-RUN-012 [P2] PUR-RUN-012: Provide crash/restart recovery and artifact reconciliation using the owned persistence layer

- **Source:** `processing-units-requirements.md:198-198` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-012 | Provide crash/restart recovery and artifact reconciliation using the owned persistence layer. | Restart tests identify abandoned work, reject stale fences and leave no successful result with missing or mismatched artifacts.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_router.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Restart tests identify abandoned work, reject stale fences and leave no successful result with missing or mismatched artifacts
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-TPU-004 [P2] PUR-TPU-004: tensor.graphinfer: execute an approved ONNX graph with fixed allowed opsets/shapes and no custom executable operations

- **Source:** `processing-units-requirements.md:318-318` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-TPU-004 | `tensor.graph_infer`: execute an approved ONNX graph with fixed allowed opsets/shapes and no custom executable operations. | Real CPU execution and output comparison; unknown nodes/external data paths/oversized shapes are rejected.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Real CPU execution and output comparison; unknown nodes/external data paths/oversized shapes are rejected
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-TPU-005 [P2] PUR-TPU-005: model.quantizationevaluate: evaluate an approved quantized artifact against its reference using local calibration/evaluation manifests. No automatic production promotion

- **Source:** `processing-units-requirements.md:319-319` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-TPU-005 | `model.quantization_evaluate`: evaluate an approved quantized artifact against its reference using local calibration/evaluation manifests. No automatic production promotion. | Report task metrics, numerical deltas, memory and latency; reject a worse model under the declared task threshold.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Report task metrics, numerical deltas, memory and latency; reject a worse model under the declared task threshold
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-001 [P2] PUR-VER-001: Maintain a machine-readable registry of every PUR- requirement, operator, task, gate and evidence reference

- **Source:** `processing-units-requirements.md:447-447` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-001 | Maintain a machine-readable registry of every `PUR-*` requirement, operator, task, gate and evidence reference. | A validator detects missing IDs, duplicates, unassigned requirements and unsupported completion states.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A validator detects missing IDs, duplicates, unassigned requirements and unsupported completion states
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-003 [P2] PUR-VER-003: Compare deterministic outputs against independent analytic/golden references and declared tolerances

- **Source:** `processing-units-requirements.md:449-449` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-003 | Compare deterministic outputs against independent analytic/golden references and declared tolerances. | Deliberately broken operators are rejected by the verifier, not merely by their own health report.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Deliberately broken operators are rejected by the verifier, not merely by their own health report
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-004 [P2] PUR-VER-004: Evaluate model tasks on held-out, licensed/local fixtures with baselines, split identities and failure analysis

- **Source:** `processing-units-requirements.md:450-450` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-004 | Evaluate model tasks on held-out, licensed/local fixtures with baselines, split identities and failure analysis. | Toy inference smoke tests cannot close business-quality requirements; no train/evaluation leakage.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Toy inference smoke tests cannot close business-quality requirements; no train/evaluation leakage
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-007 [P2] PUR-VER-007: Qualify actual hardware placement on each advertised accelerator tuple

- **Source:** `processing-units-requirements.md:453-453` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-007 | Qualify actual hardware placement on each advertised accelerator tuple. | Real provider traces/counters and result parity accompany the exact driver/runtime/device; absence is BLOCKED, not PASS.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Real provider traces/counters and result parity accompany the exact driver/runtime/device; absence is BLOCKED, not PASS
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-008 [P2] PUR-VER-008: Execute crash, stale lease, duplicate submit, cancel/commit race, disk pressure and resource-overrun drills

- **Source:** `processing-units-requirements.md:454-454` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-008 | Execute crash, stale lease, duplicate submit, cancel/commit race, disk pressure and resource-overrun drills. | Persisted effects and cleanup match the state-machine contract after restart.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Persisted effects and cleanup match the state-machine contract after restart
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-009 [P2] PUR-VER-009: Benchmark reproducibly, including cold/warm/model-load/transfer costs, hardware details and raw samples

- **Source:** `processing-units-requirements.md:455-455` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-009 | Benchmark reproducibly, including cold/warm/model-load/transfer costs, hardware details and raw samples. | Speedup compares equal work/precision/quality with recorded CPU baseline; no fabricated TOPS or unqualified SLA.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Speedup compares equal work/precision/quality with recorded CPU baseline; no fabricated TOPS or unqualified SLA
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-010 [P2] PUR-VER-010: Verify accessibility/responsiveness and truthful states in the actual deployed frontend

- **Source:** `processing-units-requirements.md:456-456` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-010 | Verify accessibility/responsiveness and truthful states in the actual deployed frontend. | Screenshots plus interaction/accessibility results and API/worker correlation establish behavior; screenshots alone do not.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Screenshots plus interaction/accessibility results and API/worker correlation establish behavior; screenshots alone do not
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VER-011 [P2] PUR-VER-011: Verify packaged/offline installation and license/security inventory for every advertised release profile

- **Source:** `processing-units-requirements.md:457-457` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VER-011 | Verify packaged/offline installation and license/security inventory for every advertised release profile. | A clean machine/environment executes the shipped artifact without hidden caches or runtime downloads.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_contracts.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] A clean machine/environment executes the shipped artifact without hidden caches or runtime downloads
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VPU-004 [P2] PUR-VPU-004: vision.duplicatescore: exact pixel/content identity plus optional documented perceptual hash distance; near-duplicates remain candidates

- **Source:** `processing-units-requirements.md:390-390` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VPU-004 | `vision.duplicate_score`: exact pixel/content identity plus optional documented perceptual hash distance; near-duplicates remain candidates. | Known identical/resized/distinct images produce measured distances without automatic entity merging.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Known identical/resized/distinct images produce measured distances without automatic entity merging
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/vision_proc.py:56`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/vision_proc.py#L56-L56)
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VPU-005 [P2] PUR-VPU-005: vision.keyframes: bounded uploaded-video decode, explicit sampling interval/timestamps and provenance; no network camera/URL acquisition

- **Source:** `processing-units-requirements.md:391-391` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VPU-005 | `vision.keyframes`: bounded uploaded-video decode, explicit sampling interval/timestamps and provenance; no network camera/URL acquisition. | Known short video yields expected count/time bounds; malformed/unsupported codec and over-limit inputs fail safely.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Known short video yields expected count/time bounds; malformed/unsupported codec and over-limit inputs fail safely
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-PUR-VPU-006 [P2] PUR-VPU-006: vision.modelinfer: approved ONNX image classifier/detector using shared inference with explicit preprocessing/label/box schema

- **Source:** `processing-units-requirements.md:392-392` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VPU-006 | `vision.model_infer`: approved ONNX image classifier/detector using shared inference with explicit preprocessing/label/box schema. | Actual local model output and held-out accuracy/coordinate tests pass; acceleration only through qualified providers.
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/processing/test_backends.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Actual local model output and held-out accuracy/coordinate tests pass; acceleration only through qualified providers
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

