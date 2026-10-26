# EPIC-CRARCPCCAGGCC-NOTRUN: CRAr_cpccaggcc-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 4 tasks, ~13.0 h, priorities {'P0': 4}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-CRA-010 [P0] CRA-010: Durable Source Events and Incremental Synchronization

- **Source:** `CRAr_cpccaggcc-requirements.md:826-856` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); ID defined at 4 other site(s): see duplicate task DUP-CRA-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-010. Durable Source Events and Incremental Synchronization

*Aggregated title: Bitemporal Event Journal & Resumable Checkpoint Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-003/004/031 | C (First acquisition slice) | M3 | G16 | — | — | INV-24, INV-31, INV-38, INV-40, INV-44, INV-52 | — | H-14 |

**Base statement:** Priority P0. Depends on CRA-003/004/031. Sources INV-31/39/40/44.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-010.1** `[CRAr]` Version the SourceEvent contract for upsert, delete, ACL-only change, rename/move and reconciliation. Include source instance, stable event identity, source/resource revision, observed time, payload hash/reference and cursor.
- **CRA-010.2** `[CRAr]` Preserve event order guarantees exactly as supplied; use stable deduplication and explicit conflict handling when revisions are opaque or incomparable. A content hash cannot hide ACL changes or repeated temporal events.
- **CRA-010.3** `[CRAr]` Implement durable checkpoints/leases and at-least-once acquisition with idempotent published effects. Acknowledge only after the declared durable boundary; reconcile crash windows instead of claiming distributed exactly-once.
- **CRA-010.4** `[CRAr]` Handle source absence, partial pages, invalid cursors and expired history with visible reconciliation/backfill states. Do not treat partial baseline absence as deletion.
- **CRA-010.5** `[CRAr]` Bind accepted assertions and projections to source/ontology/policy revisions and expose freshness/watermarks. Replay must preserve deletion and policy epochs without resurrecting data.
- **CRA-010.6** `[AGG]` Every pushed or pulled event is appended to an immutable append-only event journal; per source instance, each entry stores the SHA-256 of the previous entry so tampering or gaps are detectable.
- **CRA-010.7** `[AGG]` Bitemporal stamping: `observed_at` (platform receipt time) and `source_timestamp` (source-recorded time) are both stored; neither is inferred from the other.
- **CRA-010.8** `[AGG]` A persistent high-watermark checkpoint per connector instance is written transactionally with (or reconciled against) the publication intent so that a crashed worker resumes from the last durable checkpoint with zero loss and zero duplicate published assertions.

**Acceptance obligation CRA-010.A** (only after every clause above is ACCEPTED):

- `[CRAr]
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/integration/test_event_journal_resilience.py:4
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow
4. Resolve duplicate definition first: DUP-CRA-010

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-003/004/031. Sources INV-31/39/40/44.
- [ ] CRA-010.1 [CRAr] Version the SourceEvent contract for upsert, delete, ACL-only change, rename/move and reconciliation. Include source instance, stable event identity, source/resource revision, observed time, payload hash/reference and cursor
- [ ] CRA-010.2 [CRAr] Preserve event order guarantees exactly as supplied; use stable deduplication and explicit conflict handling when revisions are opaque or incomparable. A content hash cannot hide ACL changes or repeated temporal events
- [ ] CRA-010.3 [CRAr] Implement durable checkpoints/leases and at-least-once acquisition with idempotent published effects. Acknowledge only after the declared durable boundary; reconcile crash windows instead of claiming distributed exactly-once
- [ ] CRA-010.4 [CRAr] Handle source absence, partial pages, invalid cursors and expired history with visible reconciliation/backfill states. Do not treat partial baseline absence as deletion
- [ ] CRA-010.5 [CRAr] Bind accepted assertions and projections to source/ontology/policy revisions and expose freshness/watermarks. Replay must preserve deletion and policy epochs without resurrecting data
- [ ] CRA-010.6 [AGG] Every pushed or pulled event is appended to an immutable append-only event journal; per source instance, each entry stores the SHA-256 of the previous entry so tampering or gaps are detectable
- [ ] CRA-010.7 [AGG] Bitemporal stamping: observedat (platform receipt time) and sourcetimestamp (source-recorded time) are both stored; neither is inferred from the other
- [ ] CRA-010.8 [AGG] A persistent high-watermark checkpoint per connector instance is written transactionally with (or reconciled against) the publication intent so that a crashed worker resumes from the last durable checkpoint with zero loss and zero duplicate published assertions
- [ ] obligation CRA-010.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] inject crashes before/after raw persistence, graph publication, outbox delivery and cursor acknowledgement. Replay duplicate/reordered/ACL/delete events and compare canonical graph and projections with independently computed expected state
- [ ] [MERGED] Kill the ingestion worker at ~50% of a baseline sync, restart, and compare the canonical graph with an independently computed expected graph: zero duplicates, zero gaps, deletes and ACL changes preserved (AGG + CRAr)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/journal/event_journal.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/journal/event_journal.py#L3-L3)
- tests: `tests/integration/test_event_journal_resilience.py:4`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CRA-031 [P0] CRA-031: Durable Jobs, Publication and Event Delivery

- **Source:** `CRAr_cpccaggcc-requirements.md:1592-1626` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); ID defined at 4 other site(s): see duplicate task DUP-CRA-031; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-031. Durable Jobs, Publication and Event Delivery

*Aggregated title: Durable Distributed Jobs & Dead-Letter Queue (DLQ)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/003 | B (Safe platform) | M8 | G16 | — | — | INV-12, INV-22, INV-29, INV-30, INV-31, INV-36, INV-39, INV-41, INV-44, INV-45, INV-47 | — | — |

**Base statement:** Priority P0. Depends on CRA-002/003. Sources G16 and INV-12/25/29/30/31/36/39/41/44/45.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-031.1** `[CRAr]` Reuse and qualify the existing job/control plane for durable queueing, scope, leases, heartbeats, deadlines, retries, cancellation and terminal status. No process-local state as the only job authority in real deployments.
- **CRA-031.2** `[CRAr]` Persist publication intent/mutation/outbox identity consistently. Use a real transaction where available; otherwise implement documented idempotency/reconciliation and expose incomplete states.
- **CRA-031.3** `[CRAr]` Define replay/resume/retention/gap semantics for events and consumers, bounded buffers and per-principal authorization. Never put durable bearer credentials in URLs.
- **CRA-031.4** `[CRAr]` Enforce retry policy by operation safety; do not blindly retry mutations. Preserve poison events in a governed DLQ with reason, redaction, requeue authority and audit.
- **CRA-031.5** `[CRAr]` Fence expired leases/workers and prevent cancelled/revoked jobs from committing later. API/worker restarts and multi-instance claims must be tested on the selected real durable backend.
- **CRA-031.6** `[AGG]` All jobs live in a durable database queue; workers hold leases with heartbeats every 10 s (lease TTL 30 s); an expired lease is reclaimed from the last valid checkpoint.
- **CRA-031.7** `[AGG]` Repeatedly failing payloads move to a governed DLQ with redacted diagnostics (stack trace with secrets removed), reason, attempt count and replay authority.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| heartbeat / lease TTL | 10 s / 30 s | AGG + RES |

**Acceptance obligation CRA-031.A** (only after every clause above is ACCEPTED):

- `[CRAr]` kill process/network/storage at each commit boundary; race two workers; replay a DLQ item; cancel and revoke scope mid-job. Demonstrate expected published effects, event sequence, cursor and restored job state using independent read-back.
- `
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/integration/test_durable_jobs.py:1
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow
4. Resolve duplicate definition first: DUP-CRA-031

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-002/003. Sources G16 and INV-12/25/29/30/31/36/39/41/44/45.
- [ ] CRA-031.1 [CRAr] Reuse and qualify the existing job/control plane for durable queueing, scope, leases, heartbeats, deadlines, retries, cancellation and terminal status. No process-local state as the only job authority in real deployments
- [ ] CRA-031.2 [CRAr] Persist publication intent/mutation/outbox identity consistently. Use a real transaction where available; otherwise implement documented idempotency/reconciliation and expose incomplete states
- [ ] CRA-031.3 [CRAr] Define replay/resume/retention/gap semantics for events and consumers, bounded buffers and per-principal authorization. Never put durable bearer credentials in URLs
- [ ] CRA-031.4 [CRAr] Enforce retry policy by operation safety; do not blindly retry mutations. Preserve poison events in a governed DLQ with reason, redaction, requeue authority and audit
- [ ] CRA-031.5 [CRAr] Fence expired leases/workers and prevent cancelled/revoked jobs from committing later. API/worker restarts and multi-instance claims must be tested on the selected real durable backend
- [ ] CRA-031.6 [AGG] All jobs live in a durable database queue; workers hold leases with heartbeats every 10 s (lease TTL 30 s); an expired lease is reclaimed from the last valid checkpoint
- [ ] CRA-031.7 [AGG] Repeatedly failing payloads move to a governed DLQ with redacted diagnostics (stack trace with secrets removed), reason, attempt count and replay authority
- [ ] obligation CRA-031.A (only after every clause above is ACCEPTED)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/jobs.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/jobs.py#L1-L1), [`scripts/build_master_suite.py:91`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L91-L91), [`scripts/enhance_master_suite.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L7-L7), [`scripts/patch_dashboard_html.py:117`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_dashboard_html.py#L117-L117)
- tests: `tests/integration/test_durable_jobs.py:1`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-032 [P0] CRA-032: Observability and Operational Truth

- **Source:** `CRAr_cpccaggcc-requirements.md:1627-1657` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); ID defined at 4 other site(s): see duplicate task DUP-CRA-032; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-032. Observability and Operational Truth

*Aggregated title: OpenTelemetry Tracing, Prometheus Metrics & Audit Observability*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001/003/031 | B (Safe platform) | M8 | — | — | — | INV-44 | — | — |

**Base statement:** Priority P0. Depends on CRA-001/003/031. Sources INV-39/44/45 and all D16 gaps.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-032.1** `[CRAr]` Integrate existing structured logging, OpenTelemetry and metrics with source event/job/semantic/publication/projection/query/action correlation and stage timings.
- **CRA-032.2** `[CRAr]` Record latency/throughput/error/cancel/denied/unsupported/timeout, queue age, source freshness, projection/policy lag, resource usage, inference amplification and model cost/quality. Unknown/stale telemetry is distinct from zero/healthy.
- **CRA-032.3** `[CRAr]` Restrict metrics-label cardinality and sensitive content; protect tenant-specific diagnostics, traces and support bundles. Redact credentials/query literals/raw prompts unless explicitly authorized under retention policy.
- **CRA-032.4** `[CRAr]` Provide dashboards and alerts tied to actual measured service behavior, thresholds and runbooks. Avoid initialized example metrics or always-success health endpoints.
- **CRA-032.5** `[CRAr]` Test collector absence/backpressure without corrupting critical data flows. Audit and publication durability must not depend on best-effort telemetry alone.
- **CRA-032.6** `[AGG]` Prometheus metrics (bounded labels): `eoip_ingestion_triples_total{source,status}`, `eoip_shacl_validation_duration_seconds{shape_id,conforms}`, `eoip_query_execution_duration_seconds{dialect}` (tenant only in access-controlled traces, not unbounded labels), `eoip_reasoning_amplification_ratio{ruleset}`, `eoip_acl_derivation_pruned_triples_total`, `eoip_outbox_action_lag_seconds{target_system}`.
- **CRA-032.7** `[AGG]` Every API response carries a W3C `traceparent`; security-relevant events (login, permission change, ontology merge, action execution) emit structured JSON audit records with principal, timestamp, action and payload digest.
- **CRA-032.8** `[OCA]` Alerting rules (currently absent) are defined for queue age, projection/policy lag, connector failure, validator unavailability and outbox lag, each linked to a runbook.

**Acceptance obligation CRA-032.A** (only af
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/integration/test_observability_truth.py:1
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow
4. Resolve duplicate definition first: DUP-CRA-032

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-001/003/031. Sources INV-39/44/45 and all D16 gaps.
- [ ] CRA-032.1 [CRAr] Integrate existing structured logging, OpenTelemetry and metrics with source event/job/semantic/publication/projection/query/action correlation and stage timings
- [ ] CRA-032.2 [CRAr] Record latency/throughput/error/cancel/denied/unsupported/timeout, queue age, source freshness, projection/policy lag, resource usage, inference amplification and model cost/quality. Unknown/stale telemetry is distinct from zero/healthy
- [ ] CRA-032.3 [CRAr] Restrict metrics-label cardinality and sensitive content; protect tenant-specific diagnostics, traces and support bundles. Redact credentials/query literals/raw prompts unless explicitly authorized under retention policy
- [ ] CRA-032.4 [CRAr] Provide dashboards and alerts tied to actual measured service behavior, thresholds and runbooks. Avoid initialized example metrics or always-success health endpoints
- [ ] CRA-032.5 [CRAr] Test collector absence/backpressure without corrupting critical data flows. Audit and publication durability must not depend on best-effort telemetry alone
- [ ] CRA-032.6 [AGG] Prometheus metrics (bounded labels): eoipingestiontriplestotal{source,status}, eoipshaclvalidationdurationseconds{shapeid,conforms}, eoipqueryexecutiondurationseconds{dialect} (tenant only in access-controlled traces, not unbounded labels), eoipreasoningamplificationratio{ruleset}, eoipaclderivationprunedtriplestotal, eoipoutboxactionlagseconds{targetsystem}
- [ ] CRA-032.7 [AGG] Every API response carries a W3C traceparent; security-relevant events (login, permission change, ontology merge, action execution) emit structured JSON audit records with principal, timestamp, action and payload digest
- [ ] CRA-032.8 [OCA] Alerting rules (currently absent) are defined for queue age, projection/policy lag, connector failure, validator unavailability and outbox lag, each linked to a runbook
- [ ] obligation CRA-032.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] trigger a real failed connector, timeout validator, stuck lease and policy-stale index. Confirm trace correlation, correct alert/state and no secrets in logs/metrics/bundles. Validate observed metric values against independent counters/workload timestamps
- [ ] [MERGED] /metrics conforms to the Prometheus text format; a sampled request's traceparent resolves to a complete trace (AGG)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/observability/truth.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/observability/truth.py#L1-L1)
- tests: `tests/integration/test_observability_truth.py:1`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-040 [P0] CRA-040: Privacy, Retention, Deletion and No-Egress Guarantees

- **Source:** `CRAr_cpccaggcc-requirements.md:1899-1928` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); ID defined at 4 other site(s): see duplicate task DUP-CRA-040; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-040. Privacy, Retention, Deletion and No-Egress Guarantees

*Aggregated title: Data Privacy, Right-to-be-Forgotten & Strict No-Egress Firewalls*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-003/010/018/031 | B (Safe platform) | M8 | — | — | — | INV-11, INV-24, INV-25, INV-37, INV-42, INV-43, INV-49, INV-51, INV-52 | — | — |

**Base statement:** Priority P0. Depends on CRA-003/010/018/031. Sources INV-13/24/25/37/42/43/49/51/52/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-040.1** `[CRAr]` Classify source data and derivatives, record lawful/contractual handling policy, residence, retention, consent where applicable and legal holds. Code/model/dataset/content licenses are distinct.
- **CRA-040.2** `[CRAr]` Enforce egress policy for connectors, parsers/imports, model calls, linting, telemetry, docs and support bundles. No-egress mode must be measured at the network boundary, not inferred from configuration.
- **CRA-040.3** `[CRAr]` Track all copies/derivatives including graph assertions/inferences, raw objects, indexes/vectors, caches, answers, exports, jobs, traces and backups. A deletion workflow must locate and process each according to retention/hold policy.
- **CRA-040.4** `[CRAr]` Prevent replay, restore, re-embedding or resynchronization from resurrecting deleted/revoked content. Immutable history requires documented retention/access treatment; it is not an excuse to ignore erasure obligations.
- **CRA-040.5** `[CRAr]` Support data-subject/administrative access and deletion workflows with authorization, audit, scoped reports and explicit conflict/escalation for legal hold. Do not claim regulatory certification from a policy module name.
- **CRA-040.6** `[AGG]` Erasure cascade: a deletion request for a subject locates and processes every derivative across the eight graph planes (raw, canonical, schema references, provenance, lineage, policy, temporal, vector), caches, exports and backups under retention/hold policy, producing a scoped report.
- **CRA-040.7** `[AGG]` No-egress verification: a network socket monitor records zero external bytes during a full ingestion plus GraphRAG cycle in no-egress mode; allowed destinations are limited to configured enterprise systems.

**Acceptance obligation CRA-040.A** (only after every clause above is ACCEPTED):

- `[CRAr]` delete and revoke a subject/source while jobs and 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/integration/test_privacy_governance_and_no_egress.py:1
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow
4. Resolve duplicate definition first: DUP-CRA-040

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-003/010/018/031. Sources INV-13/24/25/37/42/43/49/51/52/54.
- [ ] CRA-040.1 [CRAr] Classify source data and derivatives, record lawful/contractual handling policy, residence, retention, consent where applicable and legal holds. Code/model/dataset/content licenses are distinct
- [ ] CRA-040.2 [CRAr] Enforce egress policy for connectors, parsers/imports, model calls, linting, telemetry, docs and support bundles. No-egress mode must be measured at the network boundary, not inferred from configuration
- [ ] CRA-040.3 [CRAr] Track all copies/derivatives including graph assertions/inferences, raw objects, indexes/vectors, caches, answers, exports, jobs, traces and backups. A deletion workflow must locate and process each according to retention/hold policy
- [ ] CRA-040.4 [CRAr] Prevent replay, restore, re-embedding or resynchronization from resurrecting deleted/revoked content. Immutable history requires documented retention/access treatment; it is not an excuse to ignore erasure obligations
- [ ] CRA-040.5 [CRAr] Support data-subject/administrative access and deletion workflows with authorization, audit, scoped reports and explicit conflict/escalation for legal hold. Do not claim regulatory certification from a policy module name
- [ ] CRA-040.6 [AGG] Erasure cascade: a deletion request for a subject locates and processes every derivative across the eight graph planes (raw, canonical, schema references, provenance, lineage, policy, temporal, vector), caches, exports and backups under retention/hold policy, producing a scoped report
- [ ] obligation CRA-040.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] delete and revoke a subject/source while jobs and streams are active, restore/replay older state, then inspect every derivative and network log. Demonstrate retained held material is restricted and reported accurately, with reviewed retention/backup exceptions
- [ ] [MERGED] After a GDPR purge, a deep sweep across graph, vector, cache and object store finds zero remaining records except documented held material (AGG)
- [ ] Not evidence of completion
- [ ] Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/privacy/governance.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/governance.py#L1-L1), [`scripts/build_master_suite.py:390`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L390-L390), [`scripts/enhance_master_suite.py:243`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L243-L243)
- tests: `tests/integration/test_privacy_governance_and_no_egress.py:1`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

