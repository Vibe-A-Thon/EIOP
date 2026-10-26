# EPIC-SUPER-CI: EOIP-engg-doc-pkg/super-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 47 tasks, ~24.5 h, priorities {'P0': 44, 'P1': 3}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-SR-CFG-001 [P0] SR-CFG-001: Layered configuration: product default → edition → partner → tenant → business unit → workspace → user. Each setting is typed (JSON Schema), documented, validated, versioned and audited

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:747-747` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 33, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CFG-001 | **Layered configuration:** product default → edition → partner → tenant → business unit → workspace → user. Each setting is typed (JSON Schema), documented, validated, versioned and audited. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CFG-001 | Layered configuration: product default → edition → partner → tenant → business unit → workspace → user. Each setting is typed (JSON Schema), documented, validated, versioned and audited. | P0»
- [ ] Layered configuration: product default → edition → partner → tenant → business unit → workspace → user. Each setting is typed (JSON Schema), documented, validated, versioned and audited.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:270`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L270-L270), [`packages/eoip/config/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/__init__.py#L1-L1), [`packages/eoip/config/ascode.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/ascode.py#L17-L17), [`packages/eoip/config/layered.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/layered.py#L1-L1), [`packages/eoip/config/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/router.py#L1-L1)
- tests: `tests/unit/test_layered_config.py:1`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:5`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-CFG-002 [P0] SR-CFG-002: Floors and ceilings: upper layers may set security/compliance floors and ceilings lower layers cannot loosen (e.g., tenant cannot enable external LLMs beyond partner-allowed levels). Most-restrictive-

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:748-748` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CFG-002 | **Floors and ceilings:** upper layers may set security/compliance *floors* and *ceilings* lower layers cannot loosen (e.g., tenant cannot enable external LLMs beyond partner-allowed levels). Most-restrictive-wins for security settings. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CFG-002 | Floors and ceilings: upper layers may set security/compliance floors and ceilings lower layers cannot loosen (e.g., tenant cannot enable external LLMs beyond partner-allowed levels). Most-restrictive-wins for security settings. | P0»
- [ ] Floors and ceilings: upper layers may set security/compliance floors and ceilings lower layers cannot loosen (e.g., tenant cannot enable external LLMs beyond partner-allowed levels). Most-restrictive-wins for security settings.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/config/ascode.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/ascode.py#L11-L11), [`packages/eoip/config/layered.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/layered.py#L1-L1), [`packages/eoip/config/router.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/router.py#L14-L14)
- tests: `tests/unit/test_layered_config.py:110`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-CFG-003 [P0] SR-CFG-003: Effective-config explain: "why does this setting have this value?" shows the layer chain and last change

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:749-749` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CFG-003 | **Effective-config explain:** "why does this setting have this value?" shows the layer chain and last change. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CFG-003 | Effective-config explain: "why does this setting have this value?" shows the layer chain and last change. | P0»
- [ ] Effective-config explain: "why does this setting have this value?" shows the layer chain and last change.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/config/__init__.py:11`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/__init__.py#L11-L11), [`packages/eoip/config/layered.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/layered.py#L1-L1), [`packages/eoip/config/router.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/router.py#L12-L12)
- tests: `tests/unit/test_layered_config.py:178`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-CFG-004 [P0] SR-CFG-004: Config as code: export/import (YAML/JSON), GitOps promotion dev → stage → prod, diff, dry-run, rollback, change approval workflow

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:750-750` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CFG-004 | **Config as code:** export/import (YAML/JSON), GitOps promotion dev → stage → prod, diff, dry-run, rollback, change approval workflow. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CFG-004 | Config as code: export/import (YAML/JSON), GitOps promotion dev → stage → prod, diff, dry-run, rollback, change approval workflow. | P0»
- [ ] Config as code: export/import (YAML/JSON), GitOps promotion dev → stage → prod, diff, dry-run, rollback, change approval workflow.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/config/__init__.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/__init__.py#L14-L14), [`packages/eoip/config/ascode.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/ascode.py#L1-L1), [`packages/eoip/config/router.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/router.py#L16-L16)
- tests: `tests/unit/test_layered_config.py:207`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-CFG-005 [P0] SR-CFG-005: Feature flags and entitlements distinct from configuration; flags never bypass policy

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:751-751` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CFG-005 | **Feature flags and entitlements** distinct from configuration; flags never bypass policy. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CFG-005 | Feature flags and entitlements distinct from configuration; flags never bypass policy. | P0»
- [ ] Feature flags and entitlements distinct from configuration; flags never bypass policy.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/config/__init__.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/__init__.py#L12-L12), [`packages/eoip/config/layered.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/layered.py#L2-L2), [`packages/eoip/config/router.py:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/router.py#L20-L20)
- tests: `tests/unit/test_layered_config.py:334`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-COM-001 [P0] SR-COM-001: Licensing models supported by the entitlement system: perpetual + annual support, annual subscription, size-tier/usage-based, per-tenant (OEM/managed), seat-based add-ons, revenue-share/royalty for OE

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1000-1000` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 38, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-001 | **Licensing models** supported by the entitlement system: perpetual + annual support, annual subscription, size-tier/usage-based, per-tenant (OEM/managed), seat-based add-ons, revenue-share/royalty for OEM. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-001 | Licensing models supported by the entitlement system: perpetual + annual support, annual subscription, size-tier/usage-based, per-tenant (OEM/managed), seat-based add-ons, revenue-share/royalty for OEM. | P0»
- [ ] Licensing models supported by the entitlement system: perpetual + annual support, annual subscription, size-tier/usage-based, per-tenant (OEM/managed), seat-based add-ons, revenue-share/royalty for OEM.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:242`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L242-L242), [`packages/eoip/licensing/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/__init__.py#L1-L1), [`packages/eoip/licensing/entitlements.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/entitlements.py#L3-L3), [`packages/eoip/licensing/license_file.py:28`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/license_file.py#L28-L28)
- tests: `tests/unit/test_licensing.py:1`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:4`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-COM-020 [P0] SR-COM-020: Pack SDK and signed distribution format: ontology layer, mapping templates, connector bundles, validation/policy rules, glossary, sample dataset generator, golden questions, report templates, complian

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1034-1034` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-020 | Pack SDK and signed distribution format: ontology layer, mapping templates, connector bundles, validation/policy rules, glossary, sample dataset generator, golden questions, report templates, compliance pack references. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-020 | Pack SDK and signed distribution format: ontology layer, mapping templates, connector bundles, validation/policy rules, glossary, sample dataset generator, golden questions, report templates, compliance pack references. | P0»
- [ ] Pack SDK and signed distribution format: ontology layer, mapping templates, connector bundles, validation/policy rules, glossary, sample dataset generator, golden questions, report templates, compliance pack references.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_domain_packs_wave2.py:1`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-COM-021 [P0] SR-COM-021: Ship the Software/IT pack and two non-IT packs at GA to prove horizontal applicability; remaining packs on the roadmap (§20)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1035-1035` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-021 | Ship the Software/IT pack and **two non-IT packs** at GA to prove horizontal applicability; remaining packs on the roadmap (§20). | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-021 | Ship the Software/IT pack and two non-IT packs at GA to prove horizontal applicability; remaining packs on the roadmap (§20). | P0»
- [ ] Ship the Software/IT pack and two non-IT packs at GA to prove horizontal applicability; remaining packs on the roadmap (§20).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_domain_packs_wave2.py:3`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-CON-010 [P0] SR-CON-010: Cloud capabilities MUST be delivered as Service Provider plugins (e.g., object storage, managed graph DB, managed search, KMS/HSM, IdP, queue, LLM endpoint, monitoring sink) selectable per capability,

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:124-124` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 53, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-010 | Cloud capabilities MUST be delivered as **Service Provider plugins** (e.g., object storage, managed graph DB, managed search, KMS/HSM, IdP, queue, LLM endpoint, monitoring sink) selectable per capability, per tenant. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-010 | Cloud capabilities MUST be delivered as Service Provider plugins (e.g., object storage, managed graph DB, managed search, KMS/HSM, IdP, queue, LLM endpoint, monitoring sink) selectable per capability, per tenant. | P0»
- [ ] Cloud capabilities MUST be delivered as Service Provider plugins (e.g., object storage, managed graph DB, managed search, KMS/HSM, IdP, queue, LLM endpoint, monitoring sink) selectable per capability, per tenant.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:277`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L277-L277), [`packages/eoip/egress/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/__init__.py#L1-L1), [`packages/eoip/egress/provider.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/provider.py#L1-L1), [`packages/eoip/egress/router.py:88`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/router.py#L88-L88)
- tests: `tests/unit/test_egress_gateway.py:1`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:6`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-DEP-007 [P0] SR-DEP-007: Offline licensing: signed license files encoding edition, modules, size tier, tenants, seats, expiry; grace periods; no license check may ever delete or lock customer data (read-only degrade only); us

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:928-928` (table_row) · **Type:** Infra · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 38, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-DEP-007 | **Offline licensing:** signed license files encoding edition, modules, size tier, tenants, seats, expiry; grace periods; **no license check may ever delete or lock customer data** (read-only degrade only); usage export for manual reporting. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-DEP-007 | Offline licensing: signed license files encoding edition, modules, size tier, tenants, seats, expiry; grace periods; no license check may ever delete or lock customer data (read-only degrade only); usage export for manual reporting. | P0»
- [ ] Offline licensing: signed license files encoding edition, modules, size tier, tenants, seats, expiry; grace periods; no license check may ever delete or lock customer data (read-only degrade only); usage export for manual reporting.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:242`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L242-L242), [`packages/eoip/licensing/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/__init__.py#L1-L1), [`packages/eoip/licensing/api.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/api.py#L1-L1), [`packages/eoip/licensing/cli.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/cli.py#L1-L1), [`packages/eoip/licensing/entitlements.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/entitlements.py#L4-L4), [`packages/eoip/licensing/license_file.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/license_file.py#L1-L1), [`packages/eoip/licensing/meter.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/meter.py#L1-L1)
- tests: `tests/unit/test_licensing.py:1`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:4`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-GOV-002 [P0] SR-GOV-002: AI governance: model cards, AI-BOM, evaluation records, intended-use and prohibited-use settings, human-oversight configuration, user-visible AI labeling, AI incident workflow

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:869-869` (table_row) · **Type:** Compliance · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 30, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GOV-002 | **AI governance:** model cards, AI-BOM, evaluation records, intended-use and prohibited-use settings, human-oversight configuration, user-visible AI labeling, AI incident workflow. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GOV-002 | AI governance: model cards, AI-BOM, evaluation records, intended-use and prohibited-use settings, human-oversight configuration, user-visible AI labeling, AI incident workflow. | P0»
- [ ] AI governance: model cards, AI-BOM, evaluation records, intended-use and prohibited-use settings, human-oversight configuration, user-visible AI labeling, AI incident workflow.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/compliance/__init__.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/__init__.py#L3-L3), [`packages/eoip/compliance/ai.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/ai.py#L1-L1), [`packages/eoip/compliance/packs.py:90`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/packs.py#L90-L90), [`packages/eoip/compliance/router.py:73`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/router.py#L73-L73)
- tests: `tests/unit/test_compliance_packs.py:130`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-GOV-003 [P0] SR-GOV-003: Change governance: ontology, mapping, policy, model and agent changes use proposal → review → approval → rollout with audit and rollback

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:870-870` (table_row) · **Type:** Compliance · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 30, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GOV-003 | **Change governance:** ontology, mapping, policy, model and agent changes use proposal → review → approval → rollout with audit and rollback. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GOV-003 | Change governance: ontology, mapping, policy, model and agent changes use proposal → review → approval → rollout with audit and rollback. | P0»
- [ ] Change governance: ontology, mapping, policy, model and agent changes use proposal → review → approval → rollout with audit and rollback.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/compliance/__init__.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/__init__.py#L4-L4), [`packages/eoip/compliance/change.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/change.py#L1-L1), [`packages/eoip/compliance/roles.py:57`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/roles.py#L57-L57), [`packages/eoip/compliance/router.py:98`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/router.py#L98-L98), [`packages/eoip/reports/generator.py:178`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/reports/generator.py#L178-L178)
- tests: `tests/unit/test_compliance_packs.py:177`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-GOV-004 [P0] SR-GOV-004: Roles: data owners, stewards, custodians, ontology curators, security admins, auditors (read-only, tamper-evident views)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:871-871` (table_row) · **Type:** Compliance · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 30, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GOV-004 | **Roles:** data owners, stewards, custodians, ontology curators, security admins, auditors (read-only, tamper-evident views). | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GOV-004 | Roles: data owners, stewards, custodians, ontology curators, security admins, auditors (read-only, tamper-evident views). | P0»
- [ ] Roles: data owners, stewards, custodians, ontology curators, security admins, auditors (read-only, tamper-evident views).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/compliance/__init__.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/__init__.py#L4-L4), [`packages/eoip/compliance/packs.py:59`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/packs.py#L59-L59), [`packages/eoip/compliance/roles.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/roles.py#L1-L1), [`packages/eoip/compliance/router.py:135`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/router.py#L135-L135)
- tests: `tests/unit/test_compliance_packs.py:223`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-ING-010 [P0] SR-ING-010: The Schema Profiler MUST infer types, nullability, cardinality, uniqueness, enumerations, formats (email, UUID, URL, IP/CIDR, ISO date/time, currency, phone, IBAN, ARN/URN, git SHA, ticket keys like A

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:379-379` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 33, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-010 | The **Schema Profiler** MUST infer types, nullability, cardinality, uniqueness, enumerations, formats (email, UUID, URL, IP/CIDR, ISO date/time, currency, phone, IBAN, ARN/URN, git SHA, ticket keys like `ABC-123`, file paths), nesting shape, and drift across versions of a payload. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-010 | The Schema Profiler MUST infer types, nullability, cardinality, uniqueness, enumerations, formats (email, UUID, URL, IP/CIDR, ISO date/time, currency, phone, IBAN, ARN/URN, git SHA, ticket keys like ABC-123, file paths), nesting shape, and drift across versions of a payload. | P0»
- [ ] The Schema Profiler MUST infer types, nullability, cardinality, uniqueness, enumerations, formats (email, UUID, URL, IP/CIDR, ISO date/time, currency, phone, IBAN, ARN/URN, git SHA, ticket keys like ABC-123, file paths), nesting shape, and drift across versions of a payload.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:1454`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L1454-L1454), [`packages/eoip/ingest/__init__.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingest/__init__.py#L3-L3), [`packages/eoip/ingest/profile.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingest/profile.py#L3-L3)
- tests: `tests/unit/test_schema_profiler.py:2`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:9`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-ING-012 [P0] SR-ING-012: Key detection: natural/surrogate key candidates; composite keys; stability scoring across runs; canonical ID minting strategy per type (deterministic, namespaced, collision-safe)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:381-381` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-012 | **Key detection:** natural/surrogate key candidates; composite keys; stability scoring across runs; canonical ID minting strategy per type (deterministic, namespaced, collision-safe). | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-012 | Key detection: natural/surrogate key candidates; composite keys; stability scoring across runs; canonical ID minting strategy per type (deterministic, namespaced, collision-safe). | P0»
- [ ] Key detection: natural/surrogate key candidates; composite keys; stability scoring across runs; canonical ID minting strategy per type (deterministic, namespaced, collision-safe).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingest/profile.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingest/profile.py#L5-L5)
- tests: `tests/unit/test_schema_profiler.py:2`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-ING-013 [P0] SR-ING-013: Relationship discovery — explicit: foreign-key-like fields, $ref/JSON Pointer, URLs to known entities, id/parent/owner conventions, join-table detection (junction → edge with properties), polymorphic 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:382-382` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-013 | **Relationship discovery — explicit:** foreign-key-like fields, `$ref`/JSON Pointer, URLs to known entities, `*_id`/`parent`/`owner` conventions, join-table detection (junction → edge with properties), polymorphic `type`+`id` pairs, array-of-IDs, hierarchy via parent pointers or path strings. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-013 | Relationship discovery — explicit: foreign-key-like fields, $ref/JSON Pointer, URLs to known entities, *_id/parent/owner conventions, join-table detection (junction → edge with properties), polymorphic type+id pairs, array-of-IDs, hierarchy via parent pointers or path strings. | P0»
- [ ] Relationship discovery — explicit: foreign-key-like fields, $ref/JSON Pointer, URLs to known entities, *_id/parent/owner conventions, join-table detection (junction → edge with properties), polymorphic type+id pairs, array-of-IDs, hierarchy via parent pointers or path strings.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingest/profile.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingest/profile.py#L6-L6)
- tests: `tests/unit/test_schema_profiler.py:2`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-ING-016 [P0] SR-ING-016: Edge classes and honesty: every edge is ASSERTED (source says so), DERIVED (deterministic rule), INFERRED (statistical/ML/LLM), or CURATED (human-approved), with confidence and method. Inferred edges 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:385-385` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-016 | **Edge classes and honesty:** every edge is `ASSERTED` (source says so), `DERIVED` (deterministic rule), `INFERRED` (statistical/ML/LLM), or `CURATED` (human-approved), with confidence and method. Inferred edges are excluded from "authoritative" answers unless the query opts in. *(Analogous to Graphify's EXTRACTED / INFERRED / AMBIGUOUS confidence tags, extended with CURATED and DERIVED.)* | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-016 | Edge classes and honesty: every edge is ASSERTED (source says so), DERIVED (deterministic rule), INFERRED (statistical/ML/LLM), or CURATED (human-approved), with confidence and method. Inferred edges are excluded from "authoritative" answers unless the query opts in. (Analogous to Graphify's EXTRACTED / INFERRED / AMBIGUOUS confidence tags, extended with CURATED an»
- [ ] Edge classes and honesty: every edge is ASSERTED (source says so), DERIVED (deterministic rule), INFERRED (statistical/ML/LLM), or CURATED (human-approved), with confidence and method. Inferred edges are excluded from "authoritative" answers unless the query opts in. (Analogous to Graphify's EXTRACTED / INFERRED / AMBIGUOUS confidence tags, extended with CURATED and DERIVED.)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingest/profile.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingest/profile.py#L8-L8)
- tests: `tests/unit/test_schema_profiler.py:2`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-LLM-010 [P0] SR-LLM-010: Egress Gateway is the only path to any external model; enforced by network policy so bypass is technically impossible

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:661-661` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 53, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-010 | **Egress Gateway** is the *only* path to any external model; enforced by network policy so bypass is technically impossible. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-010 | Egress Gateway is the only path to any external model; enforced by network policy so bypass is technically impossible. | P0»
- [ ] Egress Gateway is the only path to any external model; enforced by network policy so bypass is technically impossible.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:277`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L277-L277), [`packages/eoip/egress/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/__init__.py#L1-L1), [`packages/eoip/egress/gateway.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L1-L1), [`packages/eoip/egress/router.py:79`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/router.py#L79-L79)
- tests: `tests/unit/test_egress_gateway.py:1`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:6`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-LLM-011 [P0] SR-LLM-011: Policy engine evaluates every outbound call against the matrix, transforms the payload to the permitted level (schema-strip, aggregate, synthesize, tokenize, redact), and blocks on failure. Default is

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:662-662` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 41, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-011 | **Policy engine** evaluates every outbound call against the matrix, transforms the payload to the permitted level (schema-strip, aggregate, synthesize, tokenize, redact), and blocks on failure. Default is S0 for all tenants. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-011 | Policy engine evaluates every outbound call against the matrix, transforms the payload to the permitted level (schema-strip, aggregate, synthesize, tokenize, redact), and blocks on failure. Default is S0 for all tenants. | P0»
- [ ] Policy engine evaluates every outbound call against the matrix, transforms the payload to the permitted level (schema-strip, aggregate, synthesize, tokenize, redact), and blocks on failure. Default is S0 for all tenants.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/gateway.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L16-L16), [`packages/eoip/egress/policy.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/policy.py#L1-L1), [`packages/eoip/egress/router.py:83`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/router.py#L83-L83), [`packages/eoip/egress/transforms.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/transforms.py#L1-L1)
- tests: `tests/unit/test_egress_gateway.py:100`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-LLM-012 [P0] SR-LLM-012: Dry-run preview: administrators and (for S6) requesters see the exact payload that would be sent before approval

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:663-663` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 41, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-012 | **Dry-run preview:** administrators and (for S6) requesters see the *exact* payload that would be sent before approval. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-012 | Dry-run preview: administrators and (for S6) requesters see the exact payload that would be sent before approval. | P0»
- [ ] Dry-run preview: administrators and (for S6) requesters see the exact payload that would be sent before approval.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/gateway.py:20`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L20-L20), [`packages/eoip/egress/router.py:82`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/router.py#L82-L82), [`packages/eoip/egress/transforms.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/transforms.py#L12-L12)
- tests: `tests/unit/test_egress_gateway.py:209`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-LLM-013 [P0] SR-LLM-013: Per-call Egress Manifest (immutable): who, what data classes, which level, which fields/tokens, endpoint, region, byte counts, approval id, response hash. A "what left the building" report is exportab

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:664-664` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 41, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-013 | **Per-call Egress Manifest** (immutable): who, what data classes, which level, which fields/tokens, endpoint, region, byte counts, approval id, response hash. A "what left the building" report is exportable for auditors. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-013 | Per-call Egress Manifest (immutable): who, what data classes, which level, which fields/tokens, endpoint, region, byte counts, approval id, response hash. A "what left the building" report is exportable for auditors. | P0»
- [ ] Per-call Egress Manifest (immutable): who, what data classes, which level, which fields/tokens, endpoint, region, byte counts, approval id, response hash. A "what left the building" report is exportable for auditors.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/gateway.py:23`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L23-L23), [`packages/eoip/egress/manifest.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/manifest.py#L1-L1), [`packages/eoip/egress/router.py:86`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/router.py#L86-L86)
- tests: `tests/unit/test_egress_gateway.py:248`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-LLM-014 [P0] SR-LLM-014: DLP and canary testing: outbound payloads are scanned (PII/secret/PHI patterns, entropy, customer-defined dictionaries); CI plants canary values in test tenants and fails the build if any canary appea

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:665-665` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 41, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-014 | **DLP and canary testing:** outbound payloads are scanned (PII/secret/PHI patterns, entropy, customer-defined dictionaries); CI plants canary values in test tenants and fails the build if any canary appears in outbound traffic below the allowed level. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-014 | DLP and canary testing: outbound payloads are scanned (PII/secret/PHI patterns, entropy, customer-defined dictionaries); CI plants canary values in test tenants and fails the build if any canary appears in outbound traffic below the allowed level. | P0»
- [ ] DLP and canary testing: outbound payloads are scanned (PII/secret/PHI patterns, entropy, customer-defined dictionaries); CI plants canary values in test tenants and fails the build if any canary appears in outbound traffic below the allowed level.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/dlp.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/dlp.py#L1-L1), [`packages/eoip/egress/gateway.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L19-L19)
- tests: `tests/unit/test_egress_gateway.py:280`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-LLM-015 [P0] SR-LLM-015: Reversible tokenization vault (local, per-tenant keys) re-identifies model responses locally; responses are also scanned before display

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:666-666` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 41, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-015 | **Reversible tokenization vault** (local, per-tenant keys) re-identifies model responses locally; responses are also scanned before display. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-015 | Reversible tokenization vault (local, per-tenant keys) re-identifies model responses locally; responses are also scanned before display. | P0»
- [ ] Reversible tokenization vault (local, per-tenant keys) re-identifies model responses locally; responses are also scanned before display.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/gateway.py:22`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L22-L22), [`packages/eoip/egress/transforms.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/transforms.py#L1-L1), [`packages/eoip/egress/vault.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/vault.py#L1-L1)
- tests: `tests/unit/test_egress_gateway.py:387`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-LLM-016 [P0] SR-LLM-016: Kill switch and budgets: global/tenant/endpoint disable, rate and cost budgets, anomaly alerts on egress volume

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:667-667` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 41, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-016 | **Kill switch and budgets:** global/tenant/endpoint disable, rate and cost budgets, anomaly alerts on egress volume. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-016 | Kill switch and budgets: global/tenant/endpoint disable, rate and cost budgets, anomaly alerts on egress volume. | P0»
- [ ] Kill switch and budgets: global/tenant/endpoint disable, rate and cost budgets, anomaly alerts on egress volume.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/gateway.py:14`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L14-L14), [`packages/eoip/egress/router.py:85`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/router.py#L85-L85)
- tests: `tests/unit/test_egress_gateway.py:331`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-LLM-018 [P0] SR-LLM-018: Same policy applies to embeddings, OCR, speech, reranking and telemetry — not only chat models

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:669-669` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 41, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-LLM-018 | **Same policy applies to embeddings, OCR, speech, reranking and telemetry** — not only chat models. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-LLM-018 | Same policy applies to embeddings, OCR, speech, reranking and telemetry — not only chat models. | P0»
- [ ] Same policy applies to embeddings, OCR, speech, reranking and telemetry — not only chat models.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/gateway.py:67`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/gateway.py#L67-L67)
- tests: `tests/unit/test_egress_gateway.py:406`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-NLQ-001 [P0] SR-NLQ-001: Template/semantic-parser tier first: common intents (§1.2) compile deterministically without an LLM; an LLM-assisted tier handles open-ended phrasing using constrained decoding against the ontology sc

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:580-580` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-001 | **Template/semantic-parser tier first:** common intents (§1.2) compile deterministically without an LLM; an LLM-assisted tier handles open-ended phrasing using constrained decoding against the ontology schema; both emit QueryPlan IR. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-001 | Template/semantic-parser tier first: common intents (§1.2) compile deterministically without an LLM; an LLM-assisted tier handles open-ended phrasing using constrained decoding against the ontology schema; both emit QueryPlan IR. | P0»
- [ ] Template/semantic-parser tier first: common intents (§1.2) compile deterministically without an LLM; an LLM-assisted tier handles open-ended phrasing using constrained decoding against the ontology schema; both emit QueryPlan IR.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/suggest/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/suggest/__init__.py#L1-L1), [`packages/eoip/suggest/engine.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/suggest/engine.py#L3-L3), [`packages/eoip/suggest/parser.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/suggest/parser.py#L4-L4)
- tests: `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_suggestion_engine.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-NLQ-002 [P0] SR-NLQ-002: Intelligent suggestion engine (core differentiator): when a question is ambiguous, under-specified, too broad, or maps to multiple plans, the system MUST present a ranked set of candidate questions/qu

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:581-581` (table_row) · **Type:** Non-Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-002 | **Intelligent suggestion engine (core differentiator):** when a question is ambiguous, under-specified, too broad, or maps to multiple plans, the system MUST present a ranked set of **candidate questions/queries** each with: plain-language paraphrase, the exact QueryPlan/dialect preview, expected result shape, entity bindings (with alternatives), estimated cost/latency, confidence, data-coverage note, and a permission check. The user selects and **fires** one (or edits first). | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-002 | Intelligent suggestion engine (core differentiator): when a question is ambiguous, under-specified, too broad, or maps to multiple plans, the system MUST present a ranked set of candidate questions/queries each with: plain-language paraphrase, the exact QueryPlan/dialect preview, expected result shape, entity bindings (with alternatives), estimated cost/latency, co»
- [ ] Intelligent suggestion engine (core differentiator): when a question is ambiguous, under-specified, too broad, or maps to multiple plans, the system MUST present a ranked set of candidate questions/queries each with: plain-language paraphrase, the exact QueryPlan/dialect preview, expected result shape, entity bindings (with alternatives), estimated cost/latency, confidence, data-coverage note, and
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:1450`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L1450-L1450), [`packages/eoip/suggest/engine.py:47`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/suggest/engine.py#L47-L47), [`packages/eoip/suggest/models.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/suggest/models.py#L1-L1)
- tests: `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:9`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-NLQ-003 [P0] SR-NLQ-003: Entity disambiguation UX: "service account abc" resolving to several entities (dev/prod, duplicates across systems) shows candidates with context and lets the user pin one for the session

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:582-582` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-003 | **Entity disambiguation UX:** "service account `abc`" resolving to several entities (dev/prod, duplicates across systems) shows candidates with context and lets the user pin one for the session. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-003 | Entity disambiguation UX: "service account abc" resolving to several entities (dev/prod, duplicates across systems) shows candidates with context and lets the user pin one for the session. | P0»
- [ ] Entity disambiguation UX: "service account abc" resolving to several entities (dev/prod, duplicates across systems) shows candidates with context and lets the user pin one for the session.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/suggest/engine.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/suggest/engine.py#L4-L4), [`packages/eoip/suggest/models.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/suggest/models.py#L1-L1)
- tests: `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_suggestion_engine.py:63`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-NLQ-008 [P0] SR-NLQ-008: Reports: templates (impact assessment, incident RCA, change-risk review, compliance evidence, executive brief), scheduled/recurring, parameterized, multi-format export (HTML, PDF, DOCX, PPTX, Markdown

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:587-587` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 60, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-NLQ-008 | **Reports:** templates (impact assessment, incident RCA, change-risk review, compliance evidence, executive brief), scheduled/recurring, parameterized, multi-format export (HTML, PDF, DOCX, PPTX, Markdown, JSON), evidence appendix with provenance, approval workflow, white-label styling. | P0 (HTML/MD/PDF) / P1
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-NLQ-008 | Reports: templates (impact assessment, incident RCA, change-risk review, compliance evidence, executive brief), scheduled/recurring, parameterized, multi-format export (HTML, PDF, DOCX, PPTX, Markdown, JSON), evidence appendix with provenance, approval workflow, white-label styling. | P0 (HTML/MD/PDF) / P1»
- [ ] Reports: templates (impact assessment, incident RCA, change-risk review, compliance evidence, executive brief), scheduled/recurring, parameterized, multi-format export (HTML, PDF, DOCX, PPTX, Markdown, JSON), evidence appendix with provenance, approval workflow, white-label styling.
- [ ] P0 (HTML/MD/PDF) / P1
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:1438`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L1438-L1438), [`packages/eoip/reports/__init__.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/reports/__init__.py#L3-L3), [`packages/eoip/reports/generator.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/reports/generator.py#L1-L1), [`packages/eoip/reports/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/reports/router.py#L1-L1), [`packages/eoip/reports/schedule.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/reports/schedule.py#L1-L1), [`packages/eoip/reports/store.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/reports/store.py#L1-L1)
- tests: `tests/unit/test_reports.py:1`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:8`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-ONT-007 [P0] SR-ONT-007: Tenant-renamable terminology (white-label semantics): a tenant may rename "Service" → "Application", "Incident" → "Case", etc., without changing the underlying canonical type

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:501-501` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 27, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ONT-007 | **Tenant-renamable terminology (white-label semantics):** a tenant may rename "Service" → "Application", "Incident" → "Case", etc., without changing the underlying canonical type. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ONT-007 | Tenant-renamable terminology (white-label semantics): a tenant may rename "Service" → "Application", "Incident" → "Case", etc., without changing the underlying canonical type. | P0»
- [ ] Tenant-renamable terminology (white-label semantics): a tenant may rename "Service" → "Application", "Incident" → "Case", etc., without changing the underlying canonical type.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:283`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L283-L283), [`packages/eoip/branding/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/__init__.py#L1-L1), [`packages/eoip/branding/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/router.py#L1-L1), [`packages/eoip/branding/terminology.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/terminology.py#L1-L1)
- tests: `tests/unit/test_branding.py:1`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:6`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-PRV-001 [P0] SR-PRV-001: Classification engine at ingest (patterns, dictionaries, NER, ML; customer-extensible) labels PII/PHI/PCI/secrets/IP/legal-privileged/export-controlled; labels propagate to derived data

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:848-848` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 34, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-PRV-001 | **Classification engine** at ingest (patterns, dictionaries, NER, ML; customer-extensible) labels PII/PHI/PCI/secrets/IP/legal-privileged/export-controlled; labels propagate to derived data. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-PRV-001 | Classification engine at ingest (patterns, dictionaries, NER, ML; customer-extensible) labels PII/PHI/PCI/secrets/IP/legal-privileged/export-controlled; labels propagate to derived data. | P0»
- [ ] Classification engine at ingest (patterns, dictionaries, NER, ML; customer-extensible) labels PII/PHI/PCI/secrets/IP/legal-privileged/export-controlled; labels propagate to derived data.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:1424`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L1424-L1424), [`packages/eoip/privacy/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/__init__.py#L1-L1), [`packages/eoip/privacy/classification.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/classification.py#L1-L1), [`packages/eoip/privacy/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/router.py#L1-L1)
- tests: `tests/unit/test_privacy.py:1`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:167`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-PRV-006 [P0] SR-PRV-006: Residency enforcement: region pinning for storage, processing and model endpoints; cross-border transfer controls

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:853-853` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 22, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-PRV-006 | **Residency enforcement:** region pinning for storage, processing and model endpoints; cross-border transfer controls. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-PRV-006 | Residency enforcement: region pinning for storage, processing and model endpoints; cross-border transfer controls. | P0»
- [ ] Residency enforcement: region pinning for storage, processing and model endpoints; cross-border transfer controls.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/privacy/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/__init__.py#L1-L1), [`packages/eoip/privacy/residency.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/residency.py#L1-L1), [`packages/eoip/privacy/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/router.py#L1-L1)
- tests: `tests/unit/test_privacy.py:1`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-QA-010 [P0] SR-QA-010: Every SR- requirement maps to ≥ 1 executable acceptance test; the mapping is stored as structured data (test-ID → requirement-ID), and references in comments or docstrings never count as evidence

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:962-962` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QA-010 | Every `SR-` requirement maps to ≥ 1 executable acceptance test; the mapping is stored as structured data (test-ID → requirement-ID), **and references in comments or docstrings never count as evidence.** | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QA-010 | Every SR- requirement maps to ≥ 1 executable acceptance test; the mapping is stored as structured data (test-ID → requirement-ID), and references in comments or docstrings never count as evidence. | P0»
- [ ] Every SR- requirement maps to ≥ 1 executable acceptance test; the mapping is stored as structured data (test-ID → requirement-ID), and references in comments or docstrings never count as evidence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:1446`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L1446-L1446), [`packages/eoip/qa/__init__.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/__init__.py#L2-L2), [`packages/eoip/qa/dashboard.py:68`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/dashboard.py#L68-L68), [`packages/eoip/qa/evidence.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/evidence.py#L1-L1), [`packages/eoip/qa/pytest_plugin.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/pytest_plugin.py#L1-L1), [`packages/eoip/qa/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/router.py#L1-L1)
- tests: `tests/unit/test_qa_gate_integrity.py:1`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_collector_records_marker_and_call`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_docstring_references_never_count`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_explicit_call_declaration_drains`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_invalid_requirement_id_rejected`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_persistence_roundtrip`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_register_and_query_mapping`, `tests/unit/test_qa_gate_integrity.py::TestCodeIntrospection::test_api_routes_from_real_code`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-QA-011 [P0] SR-QA-011: A requirement is Done only if its mapped tests pass and a mutation/negative check proves the test fails when the behavior is broken (sampled per release)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:963-963` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 19, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QA-011 | A requirement is `Done` only if its mapped tests pass **and** a mutation/negative check proves the test fails when the behavior is broken (sampled per release). | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QA-011 | A requirement is Done only if its mapped tests pass and a mutation/negative check proves the test fails when the behavior is broken (sampled per release). | P0»
- [ ] A requirement is Done only if its mapped tests pass and a mutation/negative check proves the test fails when the behavior is broken (sampled per release).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/qa/__init__.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/__init__.py#L13-L13), [`packages/eoip/qa/dashboard.py:69`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/dashboard.py#L69-L69), [`packages/eoip/qa/mutation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/mutation.py#L1-L1), [`packages/eoip/qa/router.py:39`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/router.py#L39-L39)
- tests: `tests/unit/test_qa_gate_integrity.py:35`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_collector_records_marker_and_call`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_docstring_references_never_count`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_explicit_call_declaration_drains`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_invalid_requirement_id_rejected`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_persistence_roundtrip`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_register_and_query_mapping`, `tests/unit/test_qa_gate_integrity.py::TestCodeIntrospection::test_api_routes_from_real_code`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-QA-012 [P0] SR-QA-012: Status dashboards MUST report three numbers separately: tests passing, requirements with behavioral evidence, requirements with external-gate evidence; a single "% complete" is prohibited

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:964-964` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 31, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QA-012 | Status dashboards MUST report three numbers separately: *tests passing*, *requirements with behavioral evidence*, *requirements with external-gate evidence*; a single "% complete" is prohibited. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QA-012 | Status dashboards MUST report three numbers separately: tests passing, requirements with behavioral evidence, requirements with external-gate evidence; a single "% complete" is prohibited. | P0»
- [ ] Status dashboards MUST report three numbers separately: tests passing, requirements with behavioral evidence, requirements with external-gate evidence; a single "% complete" is prohibited.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/qa/__init__.py:15`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/__init__.py#L15-L15), [`packages/eoip/qa/dashboard.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/dashboard.py#L1-L1), [`packages/eoip/qa/router.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/router.py#L42-L42)
- tests: `tests/unit/test_qa_gate_integrity.py:35`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_collector_records_marker_and_call`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_docstring_references_never_count`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_explicit_call_declaration_drains`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_invalid_requirement_id_rejected`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_persistence_roundtrip`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_register_and_query_mapping`, `tests/unit/test_qa_gate_integrity.py::TestCodeIntrospection::test_api_routes_from_real_code`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-QA-013 [P0] SR-QA-013: Generated inventories (API routes, tools, labels, algorithms, commands) come from code introspection; hand-written counts fail the docs build

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:965-965` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 19, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QA-013 | Generated inventories (API routes, tools, labels, algorithms, commands) come from code introspection; hand-written counts fail the docs build. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QA-013 | Generated inventories (API routes, tools, labels, algorithms, commands) come from code introspection; hand-written counts fail the docs build. | P0»
- [ ] Generated inventories (API routes, tools, labels, algorithms, commands) come from code introspection; hand-written counts fail the docs build.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/qa/__init__.py:16`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/__init__.py#L16-L16), [`packages/eoip/qa/introspection.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/introspection.py#L1-L1), [`packages/eoip/qa/router.py:45`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/router.py#L45-L45)
- tests: `tests/unit/test_qa_gate_integrity.py:35`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_collector_records_marker_and_call`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_docstring_references_never_count`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_explicit_call_declaration_drains`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_invalid_requirement_id_rejected`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_persistence_roundtrip`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_register_and_query_mapping`, `tests/unit/test_qa_gate_integrity.py::TestCodeIntrospection::test_api_routes_from_real_code`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-QA-014 [P0] SR-QA-014: Linters/type-checkers/security scanners run at zero-error policy on main (the prior baseline carried 165 lint errors, mostly mechanical)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:966-966` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 19, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-QA-014 | Linters/type-checkers/security scanners run at zero-error policy on main (the prior baseline carried 165 lint errors, mostly mechanical). | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-QA-014 | Linters/type-checkers/security scanners run at zero-error policy on main (the prior baseline carried 165 lint errors, mostly mechanical). | P0»
- [ ] Linters/type-checkers/security scanners run at zero-error policy on main (the prior baseline carried 165 lint errors, mostly mechanical).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/qa/__init__.py:18`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/__init__.py#L18-L18), [`packages/eoip/qa/policy.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/policy.py#L1-L1), [`packages/eoip/qa/router.py:47`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/router.py#L47-L47)
- tests: `tests/unit/test_qa_gate_integrity.py:1`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_collector_records_marker_and_call`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_docstring_references_never_count`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_explicit_call_declaration_drains`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_invalid_requirement_id_rejected`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_persistence_roundtrip`, `tests/unit/test_qa_gate_integrity.py::TestBehavioralEvidenceRegistry::test_register_and_query_mapping`, `tests/unit/test_qa_gate_integrity.py::TestCodeIntrospection::test_api_routes_from_real_code`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-TEN-001 [P0] SR-TEN-001: Tenant context is mandatory in every API, query, job, event, cache key, log line, metric label, agent call and plugin invocation; code paths without tenant context fail closed

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:718-718` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 86, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-TEN-001 | **Tenant context is mandatory** in every API, query, job, event, cache key, log line, metric label, agent call and plugin invocation; code paths without tenant context fail closed. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-TEN-001 | Tenant context is mandatory in every API, query, job, event, cache key, log line, metric label, agent call and plugin invocation; code paths without tenant context fail closed. | P0»
- [ ] Tenant context is mandatory in every API, query, job, event, cache key, log line, metric label, agent call and plugin invocation; code paths without tenant context fail closed.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:238`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L238-L238), [`packages/eoip/config/layered.py:120`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/layered.py#L120-L120), [`packages/eoip/config/router.py:23`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/router.py#L23-L23), [`packages/eoip/tenancy/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/__init__.py#L1-L1), [`packages/eoip/tenancy/context.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/context.py#L1-L1), [`packages/eoip/tenancy/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/router.py#L1-L1), [`packages/eoip/tenancy/service.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/service.py#L4-L4)
- tests: `tests/security/test_http_and_realtime_contract.py:16`, `tests/security/test_http_and_realtime_contract.py::test_admin_jobs_and_runs_cross_tenant_isolation`, `tests/security/test_http_and_realtime_contract.py::test_brain_llm_stream_incremental_sse`, `tests/security/test_http_and_realtime_contract.py::test_cross_tenant_isolation_on_entity_and_ontology_routes`, `tests/security/test_http_and_realtime_contract.py::test_enterprise_middleware_tenant_isolation_cross_tenant_denial`, `tests/security/test_http_and_realtime_contract.py::test_http_boundary_accepts_signed_token_and_emits_dynamic_audit_actor`, `tests/security/test_http_and_realtime_contract.py::test_http_boundary_rejects_tampered_or_expired_token`, `tests/security/test_http_and_realtime_contract.py::test_idle_websocket_disconnect_releases_subscription`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-TEN-002 [P0] SR-TEN-002: Three isolation models, selectable per tenant/edition: Silo (dedicated stack), Bridge (shared compute, dedicated data stores/namespaces), Pool (shared everything, logical isolation)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:719-719` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 49, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-TEN-002 | **Three isolation models**, selectable per tenant/edition: *Silo* (dedicated stack), *Bridge* (shared compute, dedicated data stores/namespaces), *Pool* (shared everything, logical isolation). | P0 (Silo, Bridge) / P1 (Pool)
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-TEN-002 | Three isolation models, selectable per tenant/edition: Silo (dedicated stack), Bridge (shared compute, dedicated data stores/namespaces), Pool (shared everything, logical isolation). | P0 (Silo, Bridge) / P1 (Pool)»
- [ ] Three isolation models, selectable per tenant/edition: Silo (dedicated stack), Bridge (shared compute, dedicated data stores/namespaces), Pool (shared everything, logical isolation).
- [ ] P0 (Silo, Bridge) / P1 (Pool)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tenancy/__init__.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/__init__.py#L6-L6), [`packages/eoip/tenancy/isolation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/isolation.py#L1-L1), [`packages/eoip/tenancy/router.py:55`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/router.py#L55-L55)
- tests: `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_tenancy.py:68`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-TEN-006 [P0] SR-TEN-006: Noisy-neighbor control: quotas (graph size, ingestion rate, concurrent queries, LLM tokens, storage), fair scheduling, priority lanes, per-tenant rate limits and circuit breakers

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:723-723` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 49, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-TEN-006 | **Noisy-neighbor control:** quotas (graph size, ingestion rate, concurrent queries, LLM tokens, storage), fair scheduling, priority lanes, per-tenant rate limits and circuit breakers. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-TEN-006 | Noisy-neighbor control: quotas (graph size, ingestion rate, concurrent queries, LLM tokens, storage), fair scheduling, priority lanes, per-tenant rate limits and circuit breakers. | P0»
- [ ] Noisy-neighbor control: quotas (graph size, ingestion rate, concurrent queries, LLM tokens, storage), fair scheduling, priority lanes, per-tenant rate limits and circuit breakers.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tenancy/__init__.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/__init__.py#L7-L7), [`packages/eoip/tenancy/quotas.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/quotas.py#L1-L1), [`packages/eoip/tenancy/router.py:84`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/router.py#L84-L84)
- tests: `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_tenancy.py:115`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-TEN-007 [P0] SR-TEN-007: Tenant lifecycle: provision (API + console + IaC), configure, suspend, resume, clone (staging), migrate (cluster/region), export, delete (verified, certificate of destruction)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:724-724` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 49, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-TEN-007 | **Tenant lifecycle:** provision (API + console + IaC), configure, suspend, resume, clone (staging), migrate (cluster/region), export, delete (verified, certificate of destruction). | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-TEN-007 | Tenant lifecycle: provision (API + console + IaC), configure, suspend, resume, clone (staging), migrate (cluster/region), export, delete (verified, certificate of destruction). | P0»
- [ ] Tenant lifecycle: provision (API + console + IaC), configure, suspend, resume, clone (staging), migrate (cluster/region), export, delete (verified, certificate of destruction).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tenancy/__init__.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/__init__.py#L8-L8), [`packages/eoip/tenancy/lifecycle.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/lifecycle.py#L1-L1), [`packages/eoip/tenancy/router.py:140`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/router.py#L140-L140), [`packages/eoip/tenancy/service.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/service.py#L6-L6)
- tests: `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_tenancy.py:181`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-TEN-009 [P0] SR-TEN-009: Metering and entitlements: local, tamper-evident usage meters (records ingested, graph size, queries, LLM tokens, storage, seats, connectors) with export for billing; entitlements enforce edition/modu

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:726-726` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 87, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-TEN-009 | **Metering and entitlements:** local, tamper-evident usage meters (records ingested, graph size, queries, LLM tokens, storage, seats, connectors) with export for billing; entitlements enforce edition/module limits; offline-capable. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-TEN-009 | Metering and entitlements: local, tamper-evident usage meters (records ingested, graph size, queries, LLM tokens, storage, seats, connectors) with export for billing; entitlements enforce edition/module limits; offline-capable. | P0»
- [ ] Metering and entitlements: local, tamper-evident usage meters (records ingested, graph size, queries, LLM tokens, storage, seats, connectors) with export for billing; entitlements enforce edition/module limits; offline-capable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:242`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L242-L242), [`packages/eoip/licensing/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/__init__.py#L1-L1), [`packages/eoip/licensing/api.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/api.py#L1-L1), [`packages/eoip/licensing/meter.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/licensing/meter.py#L1-L1), [`packages/eoip/tenancy/__init__.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/__init__.py#L9-L9), [`packages/eoip/tenancy/metering.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/metering.py#L1-L1), [`packages/eoip/tenancy/router.py:183`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/router.py#L183-L183), [`packages/eoip/tenancy/service.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tenancy/service.py#L6-L6)
- tests: `tests/unit/test_licensing.py:1`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:5`, `tests/unit/test_tenancy.py:262`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-WL-001 [P0] SR-WL-001: Brand tokens: logo(s), favicon, app name, colors, typography, spacing, icon sets, node/edge visual styles per ontology type, light/dark themes — all via theme packages, no code change

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:733-733` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 27, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-WL-001 | **Brand tokens:** logo(s), favicon, app name, colors, typography, spacing, icon sets, node/edge visual styles per ontology type, light/dark themes — all via theme packages, no code change. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-WL-001 | Brand tokens: logo(s), favicon, app name, colors, typography, spacing, icon sets, node/edge visual styles per ontology type, light/dark themes — all via theme packages, no code change. | P0»
- [ ] Brand tokens: logo(s), favicon, app name, colors, typography, spacing, icon sets, node/edge visual styles per ontology type, light/dark themes — all via theme packages, no code change.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:283`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L283-L283), [`packages/eoip/branding/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/__init__.py#L1-L1), [`packages/eoip/branding/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/router.py#L1-L1), [`packages/eoip/branding/theme.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/theme.py#L1-L1)
- tests: `tests/unit/test_branding.py:1`, `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:150`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-WL-004 [P0] SR-WL-004: De-vendoring: vendor identifiers removable from UI, docs, CLI binary names, container/image names, package names, API hostnames, error pages and installers; "powered by" is a licensed toggle

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:736-736` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 15, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-WL-004 | **De-vendoring:** vendor identifiers removable from UI, docs, CLI binary names, container/image names, package names, API hostnames, error pages and installers; "powered by" is a licensed toggle. | P0
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-WL-004 | De-vendoring: vendor identifiers removable from UI, docs, CLI binary names, container/image names, package names, API hostnames, error pages and installers; "powered by" is a licensed toggle. | P0»
- [ ] De-vendoring: vendor identifiers removable from UI, docs, CLI binary names, container/image names, package names, API hostnames, error pages and installers; "powered by" is a licensed toggle.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/branding/devendoring.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/branding/devendoring.py#L1-L1)
- tests: `tests/unit/test_branding.py:1`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-CFG-006 [P1] SR-CFG-006: Hot reload for non-structural settings; structural changes (backend bindings, ontology major versions) go through migration plans

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:752-752` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CFG-006 | **Hot reload** for non-structural settings; structural changes (backend bindings, ontology major versions) go through migration plans. | P1
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CFG-006 | Hot reload for non-structural settings; structural changes (backend bindings, ontology major versions) go through migration plans. | P1»
- [ ] Hot reload for non-structural settings; structural changes (backend bindings, ontology major versions) go through migration plans.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/config/__init__.py:12`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/__init__.py#L12-L12), [`packages/eoip/config/layered.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/layered.py#L2-L2), [`packages/eoip/config/router.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/config/router.py#L21-L21)
- tests: `tests/unit/test_layered_config.py:353`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-GOV-001 [P1] SR-GOV-001: Compliance Pack format: control catalog, mapping to platform capabilities, automated evidence queries over the graph/audit, report templates, gap analysis

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:868-868` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GOV-001 | **Compliance Pack format:** control catalog, mapping to platform capabilities, automated evidence queries over the graph/audit, report templates, gap analysis. | P1
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GOV-001 | Compliance Pack format: control catalog, mapping to platform capabilities, automated evidence queries over the graph/audit, report templates, gap analysis. | P1»
- [ ] Compliance Pack format: control catalog, mapping to platform capabilities, automated evidence queries over the graph/audit, report templates, gap analysis.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`apps/api/extended.py:1434`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/apps/api/extended.py#L1434-L1434), [`packages/eoip/compliance/__init__.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/__init__.py#L3-L3), [`packages/eoip/compliance/pack.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/pack.py#L1-L1), [`packages/eoip/compliance/packs.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/packs.py#L1-L1), [`packages/eoip/compliance/router.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/router.py#L1-L1), [`packages/eoip/reports/generator.py:185`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/reports/generator.py#L185-L185)
- tests: `tests/unit/test_sr_wave_api_routes.py`, `tests/unit/test_sr_wave_api_routes.py:7`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-SR-GOV-005 [P1] SR-GOV-005: Policy exceptions are time-boxed, approved, visible and auto-expiring

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:872-872` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 30, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.5 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GOV-005 | **Policy exceptions** are time-boxed, approved, visible and auto-expiring. | P1
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GOV-005 | Policy exceptions are time-boxed, approved, visible and auto-expiring. | P1»
- [ ] Policy exceptions are time-boxed, approved, visible and auto-expiring.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/compliance/__init__.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/__init__.py#L5-L5), [`packages/eoip/compliance/exceptions.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/exceptions.py#L1-L1), [`packages/eoip/compliance/packs.py:86`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/packs.py#L86-L86), [`packages/eoip/compliance/router.py:151`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/router.py#L151-L151)
- tests: `tests/unit/test_compliance_packs.py:248`, `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

