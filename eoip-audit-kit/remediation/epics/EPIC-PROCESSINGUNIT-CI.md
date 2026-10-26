# EPIC-PROCESSINGUNIT-CI: processing-units-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 40 tasks, ~20.0 h, priorities {'P0': 7, 'P1': 7, 'P2': 26}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-PUR-CON-003 [P0] PUR-CON-003: Resolve inputs by authorized artifact/snapshot references; enforce tenant, workspace, revision and classification at submission and execution

- **Source:** `processing-units-requirements.md:134-134` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CON-003 | Resolve inputs by authorized artifact/snapshot references; enforce tenant, workspace, revision and classification at submission and execution. | Forged references, expired grants and cross-tenant inputs produce denial with no worker data access.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Forged references, expired grants and cross-tenant inputs produce denial with no worker data access
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py:94`, `tests/processing/test_contracts.py::test_artifact_ref_validation`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-CPU-001 [P0] PUR-CPU-001: records.validate: bounded JSON records against a registered JSON Schema; return per-record paths/codes without echoing secret values

- **Source:** `processing-units-requirements.md:295-295` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CPU-001 | `records.validate`: bounded JSON records against a registered JSON Schema; return per-record paths/codes without echoing secret values. | Valid/invalid/missing/null/oversized records match a golden error manifest.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Valid/invalid/missing/null/oversized records match a golden error manifest
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/catalog.py:70`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L70-L70)
- tests: `tests/processing/test_backends.py:37`, `tests/processing/test_backends.py::test_cpu_records_validate`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-DPU-003 [P0] PUR-DPU-003: data.classifyredact: reuse classification/DLP with bounded recursive structures and approved field policies; propagate labels

- **Source:** `processing-units-requirements.md:337-337` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DPU-003 | `data.classify_redact`: reuse classification/DLP with bounded recursive structures and approved field policies; propagate labels. | Known secret/PII fixtures redact correctly; unknown/failed classification blocks model-bound delivery.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Known secret/PII fixtures redact correctly; unknown/failed classification blocks model-bound delivery
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/data_prep.py:103`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/data_prep.py#L103-L103)
- tests: `tests/processing/test_backends.py:67`, `tests/processing/test_backends.py::test_dpu_classify_and_redact`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-IPU-001 [P0] PUR-IPU-001: graph.tocsr: export an authorized bounded immutable graph snapshot with stable node/edge IDs, direction and weight rules

- **Source:** `processing-units-requirements.md:377-377` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-IPU-001 | `graph.to_csr`: export an authorized bounded immutable graph snapshot with stable node/edge IDs, direction and weight rules. | Round-trip node/edge reconciliation; no authorization bypass during graph-to-array conversion.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Round-trip node/edge reconciliation; no authorization bypass during graph-to-array conversion
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/graph_intel.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/graph_intel.py#L1-L1), [`packages/eoip/processing/catalog.py:424`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L424-L424)
- tests: `tests/processing/test_backends.py:200`, `tests/processing/test_backends.py::test_ipu_graph_csr_and_components`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-LPU-002 [P0] PUR-LPU-002: text.retrieve: reuse authorized lexical/graph retrieval and optional approved embeddings; return source spans and ranking method

- **Source:** `processing-units-requirements.md:367-367` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-LPU-002 | `text.retrieve`: reuse authorized lexical/graph retrieval and optional approved embeddings; return source spans and ranking method. | Known corpus recall and cross-tenant denial are measured; fabricated citations cannot enter the result.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Known corpus recall and cross-tenant denial are measured; fabricated citations cannot enter the result
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py:168`, `tests/processing/test_backends.py::test_lpu_structured_extraction_with_abstention`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-QPU-005 [P0] PUR-QPU-005: quantum.maxcutexperiment: a bounded, seeded QAOA-style experiment on <=12 authorized graph vertices with p<=2 and <=50 objective evaluations, using Qiskit primitives and a standard optimizer

- **Source:** `processing-units-requirements.md:349-349` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-QPU-005 | `quantum.maxcut_experiment`: a bounded, seeded QAOA-style experiment on <=12 authorized graph vertices with p<=2 and <=50 objective evaluations, using Qiskit primitives and a standard optimizer. | Compare objective/time/resource use with exhaustive classical solution on the same graph; report failures and no claimed advantage without measurements.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Compare objective/time/resource use with exhaustive classical solution on the same graph; report failures and no claimed advantage without measurements
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/quantum_sim.py:265`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/quantum_sim.py#L265-L265)
- tests: `tests/processing/test_quantum.py:101`, `tests/processing/test_quantum.py::test_maxcut_qaoa_vs_classical`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-SEC-001 [P0] PUR-SEC-001: Authenticate every API/SDK/MCP/agent invocation and derive tenant/workspace/grants from trusted context

- **Source:** `processing-units-requirements.md:232-232` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-SEC-001 | Authenticate every API/SDK/MCP/agent invocation and derive tenant/workspace/grants from trusted context. | Cross-tenant and forged-context negative journeys fail before data or device access.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Cross-tenant and forged-context negative journeys fail before data or device access
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py:208`, `tests/processing/test_router.py::test_router_tenant_isolation`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-CON-004 [P1] PUR-CON-004: Use canonical serialization for plan/request hashes and idempotency binding, including nested data and versions

- **Source:** `processing-units-requirements.md:135-135` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CON-004 | Use canonical serialization for plan/request hashes and idempotency binding, including nested data and versions. | Key-order changes preserve a digest; changed nested values, policy or model invalidate it.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Key-order changes preserve a digest; changed nested values, policy or model invalidate it
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py:39`, `tests/processing/test_contracts.py::test_canonical_json_hashing_invariance`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-DPU-004 [P1] PUR-DPU-004: data.deduplicate: content/key-based duplicate detection with collision-safe digest verification and tenant-scoped indexes

- **Source:** `processing-units-requirements.md:338-338` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DPU-004 | `data.deduplicate`: content/key-based duplicate detection with collision-safe digest verification and tenant-scoped indexes. | Duplicates across batches/retries are identified without cross-tenant existence leakage.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Duplicates across batches/retries are identified without cross-tenant existence leakage
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/data_prep.py:145`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/data_prep.py#L145-L145)
- tests: `tests/processing/test_backends.py:82`, `tests/processing/test_backends.py::test_dpu_deduplicate_records`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-LPU-001 [P1] PUR-LPU-001: text.chunk and text.tokenize: deterministic Unicode-safe offsets, chunk IDs, overlap and pinned tokenizer identity; no model generation

- **Source:** `processing-units-requirements.md:366-366` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-LPU-001 | `text.chunk` and `text.tokenize`: deterministic Unicode-safe offsets, chunk IDs, overlap and pinned tokenizer identity; no model generation. | Non-ASCII and boundary fixtures reconstruct source spans; tokenizer mismatch is explicit.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Non-ASCII and boundary fixtures reconstruct source spans; tokenizer mismatch is explicit
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/text_local.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/text_local.py#L1-L1), [`packages/eoip/processing/catalog.py:375`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L375-L375)
- tests: `tests/processing/test_backends.py:154`, `tests/processing/test_backends.py::test_lpu_chunking_with_offsets`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-LPU-003 [P1] PUR-LPU-003: text.extract: local model output constrained to a registered schema, evidence spans for extracted fields and explicit abstention

- **Source:** `processing-units-requirements.md:368-368` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-LPU-003 | `text.extract`: local model output constrained to a registered schema, evidence spans for extracted fields and explicit abstention. | Held-out labelled examples, unsupported-field and injection cases meet the task gate; invalid JSON is failure, not parsed by eval.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Held-out labelled examples, unsupported-field and injection cases meet the task gate; invalid JSON is failure, not parsed by eval
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/text_local.py:81`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/text_local.py#L81-L81)
- tests: `tests/processing/test_backends.py:186`, `tests/processing/test_backends.py::test_lpu_grounded_summarization`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-RUN-001 [P1] PUR-RUN-001: Use the existing durable job owner with explicit processing job kinds and typed state mapping. Repair the tenant claim defect before use

- **Source:** `processing-units-requirements.md:187-187` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 16, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-001 | Use the existing durable job owner with explicit processing job kinds and typed state mapping. Repair the tenant claim defect before use. | Two tenants and multiple claimers never cross scope across pending, expired, retry or cancelled states.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Two tenants and multiple claimers never cross scope across pending, expired, retry or cancelled states
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/service.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/service.py#L1-L1)
- tests: `tests/integration/test_durable_jobs.py:233`, `tests/processing/test_router.py:113`, `tests/processing/test_router.py::test_router_idempotency_keys`, `tests/processing/test_router.py::test_router_submit_job_lifecycle`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-RUN-008 [P1] PUR-RUN-008: Retry only classified transient, idempotent stages with bounded backoff; do not replay graph writes blindly

- **Source:** `processing-units-requirements.md:194-194` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-008 | Retry only classified transient, idempotent stages with bounded backoff; do not replay graph writes blindly. | Injected device/worker failures cause bounded attempts and one published result, not duplicate effects.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Injected device/worker failures cause bounded attempts and one published result, not duplicate effects
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py:115`, `tests/processing/test_router.py::test_router_submit_job_lifecycle`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-RUN-009 [P1] PUR-RUN-009: Support cancellation for queued/running work and revoke publish authority immediately

- **Source:** `processing-units-requirements.md:195-195` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-009 | Support cancellation for queued/running work and revoke publish authority immediately. | Cancellation wins or completion wins atomically; killed/late workers never replace a terminal result.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Cancellation wins or completion wins atomically; killed/late workers never replace a terminal result
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py:181`, `tests/processing/test_router.py::test_router_job_cancellation`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-APU-001 [P2] PUR-APU-001: workflow.plan: validated typed DAG with compatible artifacts, stable ordering, aggregate budgets and no arbitrary code

- **Source:** `processing-units-requirements.md:356-356` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-APU-001 | `workflow.plan`: validated typed DAG with compatible artifacts, stable ordering, aggregate budgets and no arbitrary code. | CPU-only mixed-unit DAG executes; cycles, unsupported operators and cumulative oversubscription reject.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] CPU-only mixed-unit DAG executes; cycles, unsupported operators and cumulative oversubscription reject
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/catalog.py:357`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L357-L357), [`packages/eoip/processing/planner.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/planner.py#L1-L1)
- tests: `tests/processing/test_backends.py:261`, `tests/processing/test_backends.py::test_apu_heterogeneous_workflow`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-CON-001 [P2] PUR-CON-001: Publish schemas for all objects above and version independently of internal Python classes

- **Source:** `processing-units-requirements.md:132-132` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 17, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CON-001 | Publish schemas for all objects above and version independently of internal Python classes. | Valid/invalid conformance fixtures run through both API and installed SDK; breaking schema changes fail compatibility checks.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Valid/invalid conformance fixtures run through both API and installed SDK; breaking schema changes fail compatibility checks
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:1486`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L1486-L1486), [`packages/eoip/processing/contracts.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/contracts.py#L1-L1), [`packages/eoip/processing/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/router.py#L1-L1), [`packages/eoip/processing/service.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/service.py#L1-L1)
- tests: `tests/processing/test_contracts.py:1`, `tests/processing/test_contracts.py::test_all_ten_logical_units_defined`, `tests/processing/test_contracts.py::test_pydantic_extra_forbidden`, `tests/processing/test_router.py:1`, `tests/processing/test_router.py::test_router_get_capabilities`, `tests/processing/test_router.py::test_router_get_devices`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-CON-002 [P2] PUR-CON-002: Accept only registered operator IDs and typed parameters; prohibit module names, pickle, Python expressions, shell commands and custom executable kernels

- **Source:** `processing-units-requirements.md:133-133` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CON-002 | Accept only registered operator IDs and typed parameters; prohibit module names, pickle, Python expressions, shell commands and custom executable kernels. | Malicious payload corpus is rejected before process launch or artifact reads.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Malicious payload corpus is rejected before process launch or artifact reads
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py:71`, `tests/processing/test_contracts.py::test_processing_request_validation`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-CON-005 [P2] PUR-CON-005: Distinguish cpuonly, preferaccelerator, requiregpu and requirenpu; preference never overrides policy

- **Source:** `processing-units-requirements.md:136-136` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CON-005 | Distinguish `cpu_only`, `prefer_accelerator`, `require_gpu` and `require_npu`; preference never overrides policy. | Required-device jobs fail when the actual graph would fall back; preferred-device jobs disclose each fallback.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Required-device jobs fail when the actual graph would fall back; preferred-device jobs disclose each fallback
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py:118`, `tests/processing/test_contracts.py::test_execution_preference_matrix`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-CON-008 [P2] PUR-CON-008: Persist result and receipt references atomically with successful completion and an owned publication protocol

- **Source:** `processing-units-requirements.md:139-139` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CON-008 | Persist result and receipt references atomically with successful completion and an owned publication protocol. | Killing a worker at each commit point cannot produce a successful job with missing result artifacts.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Killing a worker at each commit point cannot produce a successful job with missing result artifacts
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py:127`, `tests/processing/test_contracts.py::test_execution_receipt_digest_integrity`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-CON-010 [P2] PUR-CON-010: Separate job execution success, capability qualification and business-result quality

- **Source:** `processing-units-requirements.md:141-141` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-CON-010 | Separate job execution success, capability qualification and business-result quality. | A successful low-quality OCR/LLM result remains unqualified for its task and is not promoted into verified facts.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] A successful low-quality OCR/LLM result remains unqualified for its task and is not promoted into verified facts
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_contracts.py:152`, `tests/processing/test_contracts.py::test_job_record_lifecycle_states`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-DPU-001 [P2] PUR-DPU-001: data.preparebatches: stream bounded records from an already acquired artifact, validate schema, batch by bytes/rows and preserve source offsets

- **Source:** `processing-units-requirements.md:335-335` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DPU-001 | `data.prepare_batches`: stream bounded records from an already acquired artifact, validate schema, batch by bytes/rows and preserve source offsets. | Large synthetic input uses bounded memory and downstream backpressure; no connector network call from the worker.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Large synthetic input uses bounded memory and downstream backpressure; no connector network call from the worker
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/data_prep.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/data_prep.py#L1-L1), [`packages/eoip/processing/catalog.py:266`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L266-L266)
- tests: `tests/processing/test_backends.py:37`, `tests/processing/test_backends.py::test_dpu_checksum_and_compression`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-DPU-002 [P2] PUR-DPU-002: data.checksum: approved SHA-256 content checks; data.compress/data.decompress: standard gzip with decompressed-byte, ratio and nesting limits

- **Source:** `processing-units-requirements.md:336-336` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-DPU-002 | `data.checksum`: approved SHA-256 content checks; `data.compress`/`data.decompress`: standard gzip with decompressed-byte, ratio and nesting limits. | Round-trip/digest parity and compressed-bomb rejection before resource exhaustion.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Round-trip/digest parity and compressed-bomb rejection before resource exhaustion
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/data_prep.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/data_prep.py#L22-L22)
- tests: `tests/processing/test_backends.py:56`, `tests/processing/test_backends.py::test_dpu_checksum_and_compression`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-FND-001 [P2] PUR-FND-001: Expose exactly the ten logical profile aliases above with descriptive names and explicit physical/simulated execution metadata

- **Source:** `processing-units-requirements.md:100-100` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-FND-001 | Expose exactly the ten logical profile aliases above with descriptive names and explicit physical/simulated execution metadata. | A CPU-only inventory displays all ten catalog entries without claiming ten devices; unavailable extras have reasons.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] A CPU-only inventory displays all ten catalog entries without claiming ten devices; unavailable extras have reasons
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/catalog.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L1-L1), [`packages/eoip/processing/devices.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/devices.py#L1-L1)
- tests: `tests/processing/test_contracts.py:33`, `tests/processing/test_contracts.py::test_all_ten_logical_units_defined`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-GPU-001 [P2] PUR-GPU-001: vector.cosinetopk: finite numeric candidate matrix/query, stable source-ID tie breaks, exact CPU baseline, explicit zero-vector reject/zero-score policy

- **Source:** `processing-units-requirements.md:305-305` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-GPU-001 | `vector.cosine_top_k`: finite numeric candidate matrix/query, stable source-ID tie breaks, exact CPU baseline, explicit zero-vector reject/zero-score policy. | Known vectors give expected rank/scores; ties/zero rows/dimension mismatches behave as specified.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Known vectors give expected rank/scores; ties/zero rows/dimension mismatches behave as specified
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/cpu_numerical.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/cpu_numerical.py#L1-L1), [`packages/eoip/processing/catalog.py:114`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L114-L114)
- tests: `tests/processing/test_backends.py:97`, `tests/processing/test_backends.py::test_gpu_cosine_top_k`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-GPU-002 [P2] PUR-GPU-002: tensor.matmul: 2D and bounded batched matmul using shared tensor backend; validate broadcast rules and output allocation

- **Source:** `processing-units-requirements.md:306-306` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-GPU-002 | `tensor.matmul`: 2D and bounded batched matmul using shared tensor backend; validate broadcast rules and output allocation. | Independent small analytic examples and randomized CPU-reference comparisons pass.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Independent small analytic examples and randomized CPU-reference comparisons pass
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py:110`, `tests/processing/test_backends.py::test_gpu_matmul`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-GPU-003 [P2] PUR-GPU-003: vector.reduce: sum/mean/min/max and L2 norm along a declared axis; no unsupported precision promotion

- **Source:** `processing-units-requirements.md:307-307` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-GPU-003 | `vector.reduce`: sum/mean/min/max and L2 norm along a declared axis; no unsupported precision promotion. | Empty-axis, extreme-value and normal fixtures follow the documented schema and tolerance.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Empty-axis, extreme-value and normal fixtures follow the documented schema and tolerance
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py:120`, `tests/processing/test_backends.py::test_gpu_vector_reduce`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-IPU-002 [P2] PUR-IPU-002: graph.components: weak/strong components using SciPy; graph.shortestpaths: bounded source set and supported weight rules, not unrestricted all-pairs allocation

- **Source:** `processing-units-requirements.md:378-378` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-IPU-002 | `graph.components`: weak/strong components using SciPy; `graph.shortest_paths`: bounded source set and supported weight rules, not unrestricted all-pairs allocation. | Golden graphs include isolated vertices, directed cycles and invalid weights; results match independent expected sets/paths.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Golden graphs include isolated vertices, directed cycles and invalid weights; results match independent expected sets/paths
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/graph_intel.py:67`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/graph_intel.py#L67-L67)
- tests: `tests/processing/test_backends.py:218`, `tests/processing/test_backends.py::test_ipu_graph_shortest_paths`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-NPU-001 [P2] PUR-NPU-001: model.infer: approved ONNX artifact with typed named inputs/outputs, CPU default, explicit precision and bounded batch/shape

- **Source:** `processing-units-requirements.md:325-325` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-NPU-001 | `model.infer`: approved ONNX artifact with typed named inputs/outputs, CPU default, explicit precision and bounded batch/shape. | Actual inference on a known fixture; missing model/runtime and malformed input fail truthfully.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Actual inference on a known fixture; missing model/runtime and malformed input fail truthfully
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/catalog.py:227`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L227-L227)
- tests: `tests/processing/test_backends.py:261`, `tests/processing/test_backends.py::test_npu_text_embedding_offline`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-QPU-001 [P2] PUR-QPU-001: quantum.simulate: validated JSON circuit with H/X/Y/Z/S/T/RX/RY/RZ/CX/CZ gates, finite angles, declared qubit indices and end-of-circuit measurement. Compile to Qiskit; no executable circuit upload

- **Source:** `processing-units-requirements.md:345-345` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-QPU-001 | `quantum.simulate`: validated JSON circuit with H/X/Y/Z/S/T/RX/RY/RZ/CX/CZ gates, finite angles, declared qubit indices and end-of-circuit measurement. Compile to Qiskit; no executable circuit upload. | Bell/GHZ and rotation fixtures match analytic probabilities; unsupported gates/control flow fail before simulation.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Bell/GHZ and rotation fixtures match analytic probabilities; unsupported gates/control flow fail before simulation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/quantum_sim.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/quantum_sim.py#L1-L1), [`packages/eoip/processing/catalog.py:319`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L319-L319)
- tests: `tests/processing/test_quantum.py:1`, `tests/processing/test_quantum.py::test_bell_state_simulation_statevector`, `tests/processing/test_quantum.py::test_qpu_receipt_simulation_flags`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-QPU-002 [P2] PUR-QPU-002: Support explicit statevector and density-matrix CPU methods; density mode may apply bounded depolarizing noise with probability in [0,1]

- **Source:** `processing-units-requirements.md:346-346` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-QPU-002 | Support explicit statevector and density-matrix CPU methods; density mode may apply bounded depolarizing noise with probability in [0,1]. | Normalization, known noise-free cases and a declared noisy case pass tolerance checks; no real-hardware calibration claim.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Normalization, known noise-free cases and a declared noisy case pass tolerance checks; no real-hardware calibration claim
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_quantum.py:54`, `tests/processing/test_quantum.py::test_density_matrix_with_depolarizing_noise`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-QPU-003 [P2] PUR-QPU-003: quantum.sample: bounded shots/seed and ordered bitstring counts with declared endianness; randomness is simulator pseudorandomness

- **Source:** `processing-units-requirements.md:347-347` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-QPU-003 | `quantum.sample`: bounded shots/seed and ordered bitstring counts with declared endianness; randomness is simulator pseudorandomness. | Counts sum to shots and seeded repeats on the pinned profile reproduce results; independent probability checks use a predeclared statistical rule.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Counts sum to shots and seeded repeats on the pinned profile reproduce results; independent probability checks use a predeclared statistical rule
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_quantum.py:72`, `tests/processing/test_quantum.py::test_qpu_bounds_and_limits`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-QPU-004 [P2] PUR-QPU-004: quantum.expectation: bounded sums of Pauli observables; no unrestricted matrix upload

- **Source:** `processing-units-requirements.md:348-348` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-QPU-004 | `quantum.expectation`: bounded sums of Pauli observables; no unrestricted matrix upload. | Known states/observables match analytic expectation values and validate Hermitian/shape constraints.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Known states/observables match analytic expectation values and validate Hermitian/shape constraints
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/quantum_sim.py:339`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/quantum_sim.py#L339-L339)
- tests: `tests/processing/test_quantum.py:87`, `tests/processing/test_quantum.py::test_pauli_expectation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-RUN-006 [P2] PUR-RUN-006: Use deterministic topological ordering with stable node-ID tie breaks for DAGs; reject cycles and incompatible schemas

- **Source:** `processing-units-requirements.md:192-192` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-006 | Use deterministic topological ordering with stable node-ID tie breaks for DAGs; reject cycles and incompatible schemas. | Repeated plans have identical node order; cyclic/malformed DAGs launch no work.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Repeated plans have identical node order; cyclic/malformed DAGs launch no work
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/planner.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/planner.py#L1-L1)
- tests: `tests/processing/test_router.py:58`, `tests/processing/test_router.py::test_router_compile_plan_cyclic_fails`, `tests/processing/test_router.py::test_router_compile_plan_valid`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-RUN-011 [P2] PUR-RUN-011: Check capability evidence freshness and runtime health again at dispatch; no sticky success after driver/model/policy changes

- **Source:** `processing-units-requirements.md:197-197` (table_row) · **Type:** Infra · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-RUN-011 | Check capability evidence freshness and runtime health again at dispatch; no sticky success after driver/model/policy changes. | Version changes or failed probes invalidate admission until requalification.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Version changes or failed probes invalidate admission until requalification
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_router.py:228`, `tests/processing/test_router.py::test_router_profile_probing`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-TPU-001 [P2] PUR-TPU-001: Reuse tensor.matmul; add tensor.elementwise for add/multiply/ReLU/sigmoid and tensor.softmax with explicit axis and stable computation

- **Source:** `processing-units-requirements.md:315-315` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-TPU-001 | Reuse `tensor.matmul`; add `tensor.elementwise` for add/multiply/ReLU/sigmoid and `tensor.softmax` with explicit axis and stable computation. | Known outputs and bounded extreme inputs match CPU references; no duplicate arithmetic engine.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Known outputs and bounded extreme inputs match CPU references; no duplicate arithmetic engine
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/cpu_numerical.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/cpu_numerical.py#L1-L1), [`packages/eoip/processing/catalog.py:153`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L153-L153)
- tests: `tests/processing/test_backends.py:130`, `tests/processing/test_backends.py::test_tpu_elementwise_and_softmax`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-TPU-002 [P2] PUR-TPU-002: tensor.conv2d: NCHW input/kernel, explicit pads/stride/dilation/groups; v1 groups=1; tensor.pool2d: max/average with explicit edge semantics

- **Source:** `processing-units-requirements.md:316-316` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-TPU-002 | `tensor.conv2d`: NCHW input/kernel, explicit pads/stride/dilation/groups; v1 groups=1; `tensor.pool2d`: max/average with explicit edge semantics. | Analytic small filters and ONNX CPU comparisons pass; unsupported layouts/groups rejected.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Analytic small filters and ONNX CPU comparisons pass; unsupported layouts/groups rejected
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py:134`, `tests/processing/test_backends.py::test_tpu_elementwise_and_softmax`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-TPU-003 [P2] PUR-TPU-003: tensor.normalize: L2 and layer normalization with declared axes/epsilon; tensor.reshape: validated element count/layout

- **Source:** `processing-units-requirements.md:317-317` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-TPU-003 | `tensor.normalize`: L2 and layer normalization with declared axes/epsilon; `tensor.reshape`: validated element count/layout. | Zero-norm/constant arrays and reshape mistakes follow exact documented policy.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Zero-norm/constant arrays and reshape mistakes follow exact documented policy
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py:143`, `tests/processing/test_backends.py::test_tpu_conv2d_nchw`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-VPU-001 [P2] PUR-VPU-001: vision.preprocess: allowlisted image decode, orientation, resize, grayscale/threshold and deskew through OpenCV; preserve coordinate transforms

- **Source:** `processing-units-requirements.md:387-387` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VPU-001 | `vision.preprocess`: allowlisted image decode, orientation, resize, grayscale/threshold and deskew through OpenCV; preserve coordinate transforms. | Known image fixtures and inverse-coordinate checks pass; decompression bombs/unsupported formats are rejected.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Known image fixtures and inverse-coordinate checks pass; decompression bombs/unsupported formats are rejected
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/vision_proc.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/vision_proc.py#L1-L1), [`packages/eoip/processing/catalog.py:471`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/catalog.py#L471-L471)
- tests: `tests/processing/test_backends.py:232`, `tests/processing/test_backends.py::test_vpu_image_preprocess_and_duplicate`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-VPU-002 [P2] PUR-VPU-002: vision.ocr: approved local Tesseract/language bundle; text plus page/box/confidence fields, engine identity and raw-source reference

- **Source:** `processing-units-requirements.md:388-388` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VPU-002 | `vision.ocr`: approved local Tesseract/language bundle; text plus page/box/confidence fields, engine identity and raw-source reference. | Real rendered documents produce measured CER and valid boxes; missing language/binary returns unavailable.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Real rendered documents produce measured CER and valid boxes; missing language/binary returns unavailable
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/processing/test_backends.py:236`, `tests/processing/test_backends.py::test_vpu_image_preprocess_and_duplicate`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-PUR-VPU-003 [P2] PUR-VPU-003: vision.layoutevidence: deterministic grouping of OCR lines/blocks and evidence coordinates; no unsupported table/chart understanding claim

- **Source:** `processing-units-requirements.md:389-389` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 18, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
PUR-VPU-003 | `vision.layout_evidence`: deterministic grouping of OCR lines/blocks and evidence coordinates; no unsupported table/chart understanding claim. | Annotated page fixtures verify reading-order and coordinate mapping; ambiguous layouts are marked uncertain.
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Annotated page fixtures verify reading-order and coordinate mapping; ambiguous layouts are marked uncertain
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/processing/backends/vision_proc.py:113`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/processing/backends/vision_proc.py#L113-L113)
- tests: `tests/processing/test_backends.py:248`, `tests/processing/test_backends.py::test_vpu_layout_evidence`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

