# EPIC-03FUNCTIONAL-AMB: EOIP-engg-doc-pkg/03-functional-requirements.md · ambiguous_tests

*Mapped tests both pass and fail on the audited commit.* 4 tasks, ~9.5 h, priorities {'P1': 2, 'P2': 2}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-FR-CONN-003 [P1] FR-CONN-003: Git repository connector

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:31-40` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 2, failed 1)
- **Gaps:** Mapped tests both pass and fail on the audited commit; ID defined at 1 other site(s): see duplicate task DUP-FR-CONN-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F07, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CONN-003 — Git repository connector
**WHAT:** Inspect local Git repositories without network access.  
**WHY:** The MVP must link work to commits and code.  
**HOW:** Read refs, commits, authors, changed paths and commit messages using local git.  
**DATA / INTERFACES:** Local repository path, git metadata  
**FAILURE:** Invalid repo/path traversal rejected; repository errors do not corrupt prior data.  
**TEST:** Temporary repository integration tests.  
**COMPLETE WHEN:** Repository, branch and commit nodes plus modifications exist.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_github_connector.py::test_github_webhook_delete_and_error_categories_are_safe
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)
4. Resolve duplicate definition first: DUP-FR-CONN-003

**Acceptance criteria**
- [ ] Delivers: Inspect local Git repositories without network access.
- [ ] Interfaces: Local repository path, git metadata
- [ ] Failure behaviour: Invalid repo/path traversal rejected; repository errors do not corrupt prior data.
- [ ] Verified by: Temporary repository integration tests.
- [ ] Complete when: Repository, branch and commit nodes plus modifications exist.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L7-L7)
- tests: `tests/unit/test_github_connector.py:25`, `tests/unit/test_github_connector.py::test_github_baseline_discovers_and_emits_versioned_engineering_events`
- failing: `tests/unit/test_github_connector.py::test_github_webhook_delete_and_error_categories_are_safe`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-CONN-005 [P1] FR-CONN-005: Connector resiliency

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:51-60` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Ambiguous / L2 (tests passed 5, failed 1)
- **Gaps:** Mapped tests both pass and fail on the audited commit; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D03, FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CONN-005 — Connector resiliency
**WHAT:** Implement pagination, retry/backoff, rate-limit handling, checkpointing and resume.  
**WHY:** Enterprise ingestion must survive partial failure.  
**HOW:** Persist checkpoint atomically in local state volume after committed graph batch.  
**DATA / INTERFACES:** Checkpoint JSON, job state  
**FAILURE:** Bounded retries then DLQ/failure state.  
**TEST:** Fault-injection restart tests.  
**COMPLETE WHEN:** Restart resumes without duplicate canonical nodes.  
**TARGET PHASE:** P1-MVP
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_phase2_connectors.py::test_servicenow_sync_paginates_supported_tables_and_maps_records
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)

**Acceptance criteria**
- [ ] Delivers: Implement pagination, retry/backoff, rate-limit handling, checkpointing and resume.
- [ ] Interfaces: Checkpoint JSON, job state
- [ ] Failure behaviour: Bounded retries then DLQ/failure state.
- [ ] Verified by: Fault-injection restart tests.
- [ ] Complete when: Restart resumes without duplicate canonical nodes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/tick_phase2_batch1.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/tick_phase2_batch1.py#L7-L7)
- tests: `tests/unit/test_phase2_connectors.py:204`, `tests/unit/test_phase2_connectors.py::test_connector_errors_use_stable_categories_without_exposing_credentials`
- failing: `tests/unit/test_phase2_connectors.py::test_servicenow_sync_paginates_supported_tables_and_maps_records`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-CONF-001 [P2] FR-CONF-001: Confluence connector

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:81-90` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Ambiguous / L2 (tests passed 54, failed 1)
- **Gaps:** Mapped tests both pass and fail on the audited commit; ID defined at 1 other site(s): see duplicate task DUP-FR-CONF-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D03, FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-CONF-001 — Confluence connector
**WHAT:** Add on-prem Confluence connector through Connector SDK.  
**WHY:** Documentation traceability requires enterprise wiki ingestion.  
**HOW:** Deferred from MVP; support pages, spaces, attachments metadata and deltas.  
**DATA / INTERFACES:** Confluence API records  
**FAILURE:** Same connector failure model.  
**TEST:** Contract tests in P2.  
**COMPLETE WHEN:** Incremental sync and provenance pass.  
**TARGET PHASE:** P2
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/unit/test_phase2_connectors.py::test_servicenow_sync_paginates_supported_tables_and_maps_records
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)
4. Resolve duplicate definition first: DUP-FR-CONF-001

**Acceptance criteria**
- [ ] Delivers: Add on-prem Confluence connector through Connector SDK.
- [ ] Interfaces: Confluence API records
- [ ] Failure behaviour: Same connector failure model.
- [ ] Verified by: Contract tests in P2.
- [ ] Complete when: Incremental sync and provenance pass.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_tested_p2.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_tested_p2.py#L4-L4), [`scripts/inspect_wp21_tasks.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_tasks.py#L6-L6), [`scripts/update_phase2_wp23.py:8`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L8-L8)
- tests: `tests/runtime_dlq/test_confluence_acquisition.py:8`, `tests/runtime_dlq/test_confluence_failures.py:7`, `tests/runtime_dlq/test_confluence_rejection.py:8`, `tests/unit/test_confluence_body.py:102`, `tests/unit/test_confluence_body.py::test_invalid_body_is_captured_and_dlq_before_business_writes`, `tests/unit/test_confluence_body.py::test_structure_is_persisted_versioned_and_replayable`, `tests/unit/test_confluence_metadata.py:45`, `tests/unit/test_confluence_metadata.py::test_acquisition_completes_truncated_labels_without_following_remote_links`
- failing: `tests/unit/test_phase2_connectors.py::test_servicenow_sync_paginates_supported_tables_and_maps_records`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-SNOW-001 [P2] FR-SNOW-001: ServiceNow connector

- **Source:** `EOIP-engg-doc-pkg/03-functional-requirements.md:91-100` (heading) · **Type:** Functional · **Severity:** Low
- **Now:** Ambiguous / L2 (tests passed 23, failed 5)
- **Gaps:** Mapped tests both pass and fail on the audited commit; ID defined at 1 other site(s): see duplicate task DUP-FR-SNOW-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-D03, FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-SNOW-001 — ServiceNow connector
**WHAT:** Add on-prem ServiceNow incident/problem/change/KB connector.  
**WHY:** Operations traceability needs service-management data.  
**HOW:** Deferred from MVP behind Connector SDK.  
**DATA / INTERFACES:** ServiceNow table API  
**FAILURE:** Rate limits and schema drift isolated.  
**TEST:** Contract tests in P2.  
**COMPLETE WHEN:** Incremental sync and mappings pass.  
**TARGET PHASE:** P2
```
</details>

**Next steps**
1. Run the mapped tests: python -m pytest -q tests/runtime_dlq/test_servicenow_acquisition.py::test_servicenow_http_baseline_incremental_and_replay tests/runtime_dlq/test_servicenow_rejection.py::test_servicenow_fetched_rejection_and_admission_controls tests/unit/test_phase2_connectors.py::test_servicenow_sync_paginates_supported_tables_and_maps_records tests/unit/test_servicenow_upstream_fixture.py::test_fixture_paginates_and_filters_incremental_queries tests/unit/test_servicenow_upstream_fixture.py::test_fixture_returns_genuine_mapping_rejection
2. Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)
3. Confirm passing tests actually assert this requirement (not just mention the ID)
4. Resolve duplicate definition first: DUP-FR-SNOW-001

**Acceptance criteria**
- [ ] Delivers: Add on-prem ServiceNow incident/problem/change/KB connector.
- [ ] Interfaces: ServiceNow table API
- [ ] Failure behaviour: Rate limits and schema drift isolated.
- [ ] Verified by: Contract tests in P2.
- [ ] Complete when: Incremental sync and mappings pass.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/inspect_tested_p2.py:4`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_tested_p2.py#L4-L4), [`scripts/inspect_wp21_tasks.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_wp21_tasks.py#L6-L6), [`scripts/update_phase2_wp23.py:9`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase2_wp23.py#L9-L9)
- tests: `tests/runtime_dlq/test_servicenow_acquisition.py:8`, `tests/runtime_dlq/test_servicenow_authentication.py:7`, `tests/runtime_dlq/test_servicenow_rejection.py:9`, `tests/unit/test_phase2_connectors.py:134`, `tests/unit/test_phase2_connectors.py::test_servicenow_rejects_schema_drift_without_dropping_raw_record`, `tests/unit/test_phase2_connectors.py::test_servicenow_sync_paginates_supported_tables_and_maps_records`, `tests/unit/test_phase2_ingestion.py:13`, `tests/unit/test_phase2_ingestion.py::test_rest_refetch_preserves_capture_provenance_and_replay_freshness[confluence]`
- failing: `tests/runtime_dlq/test_servicenow_acquisition.py::test_servicenow_http_baseline_incremental_and_replay`, `tests/runtime_dlq/test_servicenow_rejection.py::test_servicenow_fetched_rejection_and_admission_controls`, `tests/unit/test_phase2_connectors.py::test_servicenow_sync_paginates_supported_tables_and_maps_records`, `tests/unit/test_servicenow_upstream_fixture.py::test_fixture_paginates_and_filters_incremental_queries`, `tests/unit/test_servicenow_upstream_fixture.py::test_fixture_returns_genuine_mapping_rejection`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

