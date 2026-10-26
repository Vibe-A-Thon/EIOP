# EPIC-SUPER-NOTRUN-01: EOIP-engg-doc-pkg/super-requirements.md · tests_not_executed

*Tests are mapped/referenced but none ran in the audit (excluded or not collected).* 60 tasks, ~65.0 h, priorities {'P0': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-SR-AGT-001 [P0] SR-AGT-001: Agent contract (JSON schema): identity, purpose, allowed tools, input/output schemas, budgets (steps, tokens, time, expansions), risk class, approval mode, memory scope, evaluation hooks. Agents are d

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:681-681` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-001 | **Agent contract** (JSON schema): identity, purpose, allowed tools, input/output schemas, budgets (steps, tokens, time, expansions), risk class, approval mode, memory scope, evaluation hooks. Agents are data, versioned and reviewable. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-001 | Agent contract (JSON schema): identity, purpose, allowed tools, input/output schemas, budgets (steps, tokens, time, expansions), risk class, approval mode, memory scope, evaluation hooks. Agents are data, versioned and reviewable. | P0»
- [ ] Agent contract (JSON schema): identity, purpose, allowed tools, input/output schemas, budgets (steps, tokens, time, expansions), risk class, approval mode, memory scope, evaluation hooks. Agents are data, versioned and reviewable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-002 [P0] SR-AGT-002: Bounded runtime: tool allowlist, budget enforcement, circuit breaker, loop/stall detection, deterministic replay from traces

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:682-682` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-002 | **Bounded runtime:** tool allowlist, budget enforcement, circuit breaker, loop/stall detection, deterministic replay from traces. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-002 | Bounded runtime: tool allowlist, budget enforcement, circuit breaker, loop/stall detection, deterministic replay from traces. | P0»
- [ ] Bounded runtime: tool allowlist, budget enforcement, circuit breaker, loop/stall detection, deterministic replay from traces.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-003 [P0] SR-AGT-003: Autonomy modes: HITL (human approves each action), HOTL (human monitors, can intervene), HIC (human in command; autonomy scoped by policy). Mode is a policy per agent × action risk class × tenant

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:683-683` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-003 | **Autonomy modes:** HITL (human approves each action), HOTL (human monitors, can intervene), HIC (human in command; autonomy scoped by policy). Mode is a policy per agent × action risk class × tenant. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-003 | Autonomy modes: HITL (human approves each action), HOTL (human monitors, can intervene), HIC (human in command; autonomy scoped by policy). Mode is a policy per agent × action risk class × tenant. | P0»
- [ ] Autonomy modes: HITL (human approves each action), HOTL (human monitors, can intervene), HIC (human in command; autonomy scoped by policy). Mode is a policy per agent × action risk class × tenant.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-004 [P0] SR-AGT-004: Read/write separation: default agents are read-only; any write/action tool requires an explicit approval boundary, audit and (where configured) dual control

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:684-684` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-004 | **Read/write separation:** default agents are read-only; any write/action tool requires an explicit approval boundary, audit and (where configured) dual control. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-004 | Read/write separation: default agents are read-only; any write/action tool requires an explicit approval boundary, audit and (where configured) dual control. | P0»
- [ ] Read/write separation: default agents are read-only; any write/action tool requires an explicit approval boundary, audit and (where configured) dual control.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-005 [P0] SR-AGT-005: MCP servers: a read-only MCP server exposing graph, query, evidence and lineage tools; a separately governed action server; inventories generated from code; per-tenant auth and rate limits

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:685-685` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-005 | **MCP servers:** a read-only MCP server exposing graph, query, evidence and lineage tools; a separately governed action server; inventories generated from code; per-tenant auth and rate limits. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-005 | MCP servers: a read-only MCP server exposing graph, query, evidence and lineage tools; a separately governed action server; inventories generated from code; per-tenant auth and rate limits. | P0»
- [ ] MCP servers: a read-only MCP server exposing graph, query, evidence and lineage tools; a separately governed action server; inventories generated from code; per-tenant auth and rate limits.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-006 [P0] SR-AGT-006: Memory: scoped (turn/session/user/workspace/tenant), policy-governed, expiring, inspectable and erasable; no cross-tenant memory

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:686-686` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-006 | **Memory:** scoped (turn/session/user/workspace/tenant), policy-governed, expiring, inspectable and erasable; no cross-tenant memory. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-006 | Memory: scoped (turn/session/user/workspace/tenant), policy-governed, expiring, inspectable and erasable; no cross-tenant memory. | P0»
- [ ] Memory: scoped (turn/session/user/workspace/tenant), policy-governed, expiring, inspectable and erasable; no cross-tenant memory.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-009 [P0] SR-AGT-009: Controlled self-improvement is OFF by default; proposals (prompt, mapping, ontology, rule changes) are generated as reviewable change requests, never self-applied

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:689-689` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-009 | **Controlled self-improvement is OFF by default;** proposals (prompt, mapping, ontology, rule changes) are generated as reviewable change requests, never self-applied. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-009 | Controlled self-improvement is OFF by default; proposals (prompt, mapping, ontology, rule changes) are generated as reviewable change requests, never self-applied. | P0»
- [ ] Controlled self-improvement is OFF by default; proposals (prompt, mapping, ontology, rule changes) are generated as reviewable change requests, never self-applied.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-AGT-022 [P0] SR-AGT-022: Freshness and knowledge-decay scoring: per node/edge/source; stale knowledge is visibly flagged and down-ranked

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:699-699` (table_row) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-AGT-022 | **Freshness and knowledge-decay scoring:** per node/edge/source; stale knowledge is visibly flagged and down-ranked. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-AGT-022 | Freshness and knowledge-decay scoring: per node/edge/source; stale knowledge is visibly flagged and down-ranked. | P0»
- [ ] Freshness and knowledge-decay scoring: per node/edge/source; stale knowledge is visibly flagged and down-ranked.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-001 [P0] SR-ARC-001: Modular monolith first, service-extractable: modules communicate through typed interfaces/events and MUST be separable into independently scalable services without code rewrite (preserves the prior NF

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:162-162` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-001 | **Modular monolith first, service-extractable:** modules communicate through typed interfaces/events and MUST be separable into independently scalable services without code rewrite (preserves the prior `NFR-MAINT-001` boundary). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-001 | Modular monolith first, service-extractable: modules communicate through typed interfaces/events and MUST be separable into independently scalable services without code rewrite (preserves the prior NFR-MAINT-001 boundary). | P0»
- [ ] Modular monolith first, service-extractable: modules communicate through typed interfaces/events and MUST be separable into independently scalable services without code rewrite (preserves the prior NFR-MAINT-001 boundary).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-002 [P0] SR-ARC-002: Ports-and-adapters: Graph Store, Vector Store, Search, Object Store, Relational Store, Event Bus, Model Provider, Identity Provider, Secret/KMS, Scheduler and Notification are ports with versioned con

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:163-163` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-002 | **Ports-and-adapters:** Graph Store, Vector Store, Search, Object Store, Relational Store, Event Bus, Model Provider, Identity Provider, Secret/KMS, Scheduler and Notification are ports with versioned contracts and a conformance test kit. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-002 | Ports-and-adapters: Graph Store, Vector Store, Search, Object Store, Relational Store, Event Bus, Model Provider, Identity Provider, Secret/KMS, Scheduler and Notification are ports with versioned contracts and a conformance test kit. | P0»
- [ ] Ports-and-adapters: Graph Store, Vector Store, Search, Object Store, Relational Store, Event Bus, Model Provider, Identity Provider, Secret/KMS, Scheduler and Notification are ports with versioned contracts and a conformance test kit.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-ARC-003 [P0] SR-ARC-003: Event backbone: an append-only event log (pluggable: embedded log for DP-0; NATS JetStream/Kafka-class for clustered) carries ingestion, mutation, policy and audit events; consumers are idempotent (ou

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:164-164` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-003 | **Event backbone:** an append-only event log (pluggable: embedded log for DP-0; NATS JetStream/Kafka-class for clustered) carries ingestion, mutation, policy and audit events; consumers are idempotent (outbox pattern). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-003 | Event backbone: an append-only event log (pluggable: embedded log for DP-0; NATS JetStream/Kafka-class for clustered) carries ingestion, mutation, policy and audit events; consumers are idempotent (outbox pattern). | P0»
- [ ] Event backbone: an append-only event log (pluggable: embedded log for DP-0; NATS JetStream/Kafka-class for clustered) carries ingestion, mutation, policy and audit events; consumers are idempotent (outbox pattern).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-004 [P0] SR-ARC-004: Single canonical contract per concept: one versioned schema registry for entities, edges, events, QueryPlan, agent contract, config and plugin manifest; all APIs and UIs derive from it (generated, not

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:165-165` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-004 | **Single canonical contract per concept:** one versioned schema registry for entities, edges, events, QueryPlan, agent contract, config and plugin manifest; all APIs and UIs derive from it (generated, not hand-copied). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-004 | Single canonical contract per concept: one versioned schema registry for entities, edges, events, QueryPlan, agent contract, config and plugin manifest; all APIs and UIs derive from it (generated, not hand-copied). | P0»
- [ ] Single canonical contract per concept: one versioned schema registry for entities, edges, events, QueryPlan, agent contract, config and plugin manifest; all APIs and UIs derive from it (generated, not hand-copied).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-005 [P0] SR-ARC-005: Distributed by design: stateless API/query/worker tiers scale horizontally; stateful tiers (graph, vector, search, relational, object, log) support replication and partitioning per backend capability

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:166-166` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-005 | **Distributed by design:** stateless API/query/worker tiers scale horizontally; stateful tiers (graph, vector, search, relational, object, log) support replication and partitioning per backend capability. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-005 | Distributed by design: stateless API/query/worker tiers scale horizontally; stateful tiers (graph, vector, search, relational, object, log) support replication and partitioning per backend capability. | P0»
- [ ] Distributed by design: stateless API/query/worker tiers scale horizontally; stateful tiers (graph, vector, search, relational, object, log) support replication and partitioning per backend capability.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-006 [P0] SR-ARC-006: Consistency model documented and tested: strong consistency within a graph partition for writes and read-your-writes for the writer; eventual consistency for derived indexes (vector, search, materiali

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:167-167` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-006 | **Consistency model documented and tested:** strong consistency within a graph partition for writes and read-your-writes for the writer; eventual consistency for derived indexes (vector, search, materialized views) with measurable lag SLOs and a staleness indicator surfaced to users. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-006 | Consistency model documented and tested: strong consistency within a graph partition for writes and read-your-writes for the writer; eventual consistency for derived indexes (vector, search, materialized views) with measurable lag SLOs and a staleness indicator surfaced to users. | P0»
- [ ] Consistency model documented and tested: strong consistency within a graph partition for writes and read-your-writes for the writer; eventual consistency for derived indexes (vector, search, materialized views) with measurable lag SLOs and a staleness indicator surfaced to users.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-007 [P0] SR-ARC-007: Exactly-once effects via idempotency keys, deterministic IDs and replay-safe mutations; at-least-once delivery acceptable at transport level

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:168-168` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-007 | **Exactly-once effects** via idempotency keys, deterministic IDs and replay-safe mutations; at-least-once delivery acceptable at transport level. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-007 | Exactly-once effects via idempotency keys, deterministic IDs and replay-safe mutations; at-least-once delivery acceptable at transport level. | P0»
- [ ] Exactly-once effects via idempotency keys, deterministic IDs and replay-safe mutations; at-least-once delivery acceptable at transport level.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-010 [P0] SR-ARC-010: Sandboxed extension runtime: plugins execute in isolated containers or WASM sandboxes with declared capabilities, CPU/memory/egress limits and signed manifests (§12.5)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:171-171` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-010 | **Sandboxed extension runtime:** plugins execute in isolated containers or WASM sandboxes with declared capabilities, CPU/memory/egress limits and signed manifests (§12.5). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-010 | Sandboxed extension runtime: plugins execute in isolated containers or WASM sandboxes with declared capabilities, CPU/memory/egress limits and signed manifests (§12.5). | P0»
- [ ] Sandboxed extension runtime: plugins execute in isolated containers or WASM sandboxes with declared capabilities, CPU/memory/egress limits and signed manifests (§12.5).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-011 [P0] SR-ARC-011: Architecture fitness tests in CI: forbidden imports, layering rules, adapter-only vendor SDK usage, no hand-maintained inventories, no cross-tenant code paths without tenant context

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:172-172` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-011 | **Architecture fitness tests** in CI: forbidden imports, layering rules, adapter-only vendor SDK usage, no hand-maintained inventories, no cross-tenant code paths without tenant context. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-011 | Architecture fitness tests in CI: forbidden imports, layering rules, adapter-only vendor SDK usage, no hand-maintained inventories, no cross-tenant code paths without tenant context. | P0»
- [ ] Architecture fitness tests in CI: forbidden imports, layering rules, adapter-only vendor SDK usage, no hand-maintained inventories, no cross-tenant code paths without tenant context.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ARC-012 [P0] SR-ARC-012: Mandatory ADR process: every decision that changes a port, a default component or a supported-backend tier needs an ADR with alternatives, license review and benchmark evidence

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:173-173` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ARC-012 | **Mandatory ADR process:** every decision that changes a port, a default component or a supported-backend tier needs an ADR with alternatives, license review and benchmark evidence. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ARC-012 | Mandatory ADR process: every decision that changes a port, a default component or a supported-backend tier needs an ADR with alternatives, license review and benchmark evidence. | P0»
- [ ] Mandatory ADR process: every decision that changes a port, a default component or a supported-backend tier needs an ADR with alternatives, license review and benchmark evidence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-COM-002 [P0] SR-COM-002: PoC kit: 30-day evaluation license, per-industry demo datasets, scripted demo flows, sizing tool, ROI calculator, 10-question "prove it on your data" workshop template

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1001-1001` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-002 | **PoC kit:** 30-day evaluation license, per-industry demo datasets, scripted demo flows, sizing tool, ROI calculator, 10-question "prove it on your data" workshop template. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-002 | PoC kit: 30-day evaluation license, per-industry demo datasets, scripted demo flows, sizing tool, ROI calculator, 10-question "prove it on your data" workshop template. | P0»
- [ ] PoC kit: 30-day evaluation license, per-industry demo datasets, scripted demo flows, sizing tool, ROI calculator, 10-question "prove it on your data" workshop template.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-COM-003 [P0] SR-COM-003: Legal and procurement kit: EULA, MSA, DPA, SLA, OEM and partner agreements, BAA template, security questionnaire answers (SIG/CAIQ-style), SBOM and third-party notices, export-control classification, 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1002-1002` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-003 | **Legal and procurement kit:** EULA, MSA, DPA, SLA, OEM and partner agreements, BAA template, security questionnaire answers (SIG/CAIQ-style), SBOM and third-party notices, export-control classification, accessibility conformance report. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-003 | Legal and procurement kit: EULA, MSA, DPA, SLA, OEM and partner agreements, BAA template, security questionnaire answers (SIG/CAIQ-style), SBOM and third-party notices, export-control classification, accessibility conformance report. | P0»
- [ ] Legal and procurement kit: EULA, MSA, DPA, SLA, OEM and partner agreements, BAA template, security questionnaire answers (SIG/CAIQ-style), SBOM and third-party notices, export-control classification, accessibility conformance report.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-COM-004 [P0] SR-COM-004: Support: Standard / Priority / Enterprise / Mission-critical tiers with response targets, escalation paths, named technical account managers, support-bundle workflow

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1003-1003` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-004 | **Support:** Standard / Priority / Enterprise / Mission-critical tiers with response targets, escalation paths, named technical account managers, support-bundle workflow. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-004 | Support: Standard / Priority / Enterprise / Mission-critical tiers with response targets, escalation paths, named technical account managers, support-bundle workflow. | P0»
- [ ] Support: Standard / Priority / Enterprise / Mission-critical tiers with response targets, escalation paths, named technical account managers, support-bundle workflow.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-COM-005 [P0] SR-COM-005: Services: onboarding, connector development, ontology engineering, NL tuning, training, compliance-pack onboarding, managed operations

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1004-1004` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-005 | **Services:** onboarding, connector development, ontology engineering, NL tuning, training, compliance-pack onboarding, managed operations. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-005 | Services: onboarding, connector development, ontology engineering, NL tuning, training, compliance-pack onboarding, managed operations. | P0»
- [ ] Services: onboarding, connector development, ontology engineering, NL tuning, training, compliance-pack onboarding, managed operations.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-COM-007 [P0] SR-COM-007: Documentation set: admin, user, API/SDK, connector developer, ontology guide, security whitepaper, architecture, reference deployments, runbooks, compliance mappings, release notes, upgrade guides, tr

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1006-1006` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-007 | **Documentation set:** admin, user, API/SDK, connector developer, ontology guide, security whitepaper, architecture, reference deployments, runbooks, compliance mappings, release notes, upgrade guides, training curriculum. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-007 | Documentation set: admin, user, API/SDK, connector developer, ontology guide, security whitepaper, architecture, reference deployments, runbooks, compliance mappings, release notes, upgrade guides, training curriculum. | P0»
- [ ] Documentation set: admin, user, API/SDK, connector developer, ontology guide, security whitepaper, architecture, reference deployments, runbooks, compliance mappings, release notes, upgrade guides, training curriculum.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-COM-009 [P0] SR-COM-009: Lifecycle policy: versioning, LTS, end-of-support, security-patch commitments published

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1008-1008` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-009 | **Lifecycle policy:** versioning, LTS, end-of-support, security-patch commitments published. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-009 | Lifecycle policy: versioning, LTS, end-of-support, security-patch commitments published. | P0»
- [ ] Lifecycle policy: versioning, LTS, end-of-support, security-patch commitments published.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-COM-010 [P0] SR-COM-010: Strategy decisions to record as ADRs: open-core vs source-available vs closed; trademark and white-label rights; third-party component redistribution rights; IP assignment for plugins and marketplace 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:1009-1009` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-COM-010 | **Strategy decisions to record as ADRs:** open-core vs source-available vs closed; trademark and white-label rights; third-party component redistribution rights; IP assignment for plugins and marketplace content. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-COM-010 | Strategy decisions to record as ADRs: open-core vs source-available vs closed; trademark and white-label rights; third-party component redistribution rights; IP assignment for plugins and marketplace content. | P0»
- [ ] Strategy decisions to record as ADRs: open-core vs source-available vs closed; trademark and white-label rights; third-party component redistribution rights; IP assignment for plugins and marketplace content.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-001 [P0] SR-CON-001: Self-contained: the default distribution MUST run with zero external network dependencies (no SaaS, no cloud API, no phone-home, no CDN assets, no package fetch at runtime)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:98-98` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-001 | **Self-contained:** the default distribution MUST run with zero external network dependencies (no SaaS, no cloud API, no phone-home, no CDN assets, no package fetch at runtime). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-001 | Self-contained: the default distribution MUST run with zero external network dependencies (no SaaS, no cloud API, no phone-home, no CDN assets, no package fetch at runtime). | P0»
- [ ] Self-contained: the default distribution MUST run with zero external network dependencies (no SaaS, no cloud API, no phone-home, no CDN assets, no package fetch at runtime).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-002 [P0] SR-CON-002: Local-first: all processing, storage, indexing, embedding, inference and UI serving happen inside the customer-controlled boundary by default; the system MUST function fully offline

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:99-99` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-002 | **Local-first:** all processing, storage, indexing, embedding, inference and UI serving happen inside the customer-controlled boundary by default; the system MUST function fully offline. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-002 | Local-first: all processing, storage, indexing, embedding, inference and UI serving happen inside the customer-controlled boundary by default; the system MUST function fully offline. | P0»
- [ ] Local-first: all processing, storage, indexing, embedding, inference and UI serving happen inside the customer-controlled boundary by default; the system MUST function fully offline.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-003 [P0] SR-CON-003: No egress by default: outbound traffic MUST be denied by default via network policy and application-level egress gateway; any permitted egress is allowlisted, logged and attributable

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:100-100` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-003 | **No egress by default:** outbound traffic MUST be denied by default via network policy and application-level egress gateway; any permitted egress is allowlisted, logged and attributable. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-003 | No egress by default: outbound traffic MUST be denied by default via network policy and application-level egress gateway; any permitted egress is allowlisted, logged and attributable. | P0»
- [ ] No egress by default: outbound traffic MUST be denied by default via network policy and application-level egress gateway; any permitted egress is allowlisted, logged and attributable.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-004 [P0] SR-CON-004: Everything configurable, safely: every behavior in this document that says "configurable" MUST be a typed, versioned, validated, auditable setting with a safe default (§12.3)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:101-101` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-004 | **Everything configurable, safely:** every behavior in this document that says "configurable" MUST be a typed, versioned, validated, auditable setting with a safe default (§12.3). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-004 | Everything configurable, safely: every behavior in this document that says "configurable" MUST be a typed, versioned, validated, auditable setting with a safe default (§12.3). | P0»
- [ ] Everything configurable, safely: every behavior in this document that says "configurable" MUST be a typed, versioned, validated, auditable setting with a safe default (§12.3).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-005 [P0] SR-CON-005: LLM-optional: ingestion, graph construction, validation, deterministic query, impact analysis, lineage and reporting MUST work with no LLM present

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:102-102` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-005 | **LLM-optional:** ingestion, graph construction, validation, deterministic query, impact analysis, lineage and reporting MUST work with no LLM present. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-005 | LLM-optional: ingestion, graph construction, validation, deterministic query, impact analysis, lineage and reporting MUST work with no LLM present. | P0»
- [ ] LLM-optional: ingestion, graph construction, validation, deterministic query, impact analysis, lineage and reporting MUST work with no LLM present.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-006 [P0] SR-CON-006: Evidence-first: every returned fact carries source, method (asserted/derived/inferred/curated), confidence, freshness and policy-filter notice

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:103-103` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-006 | **Evidence-first:** every returned fact carries source, method (asserted/derived/inferred/curated), confidence, freshness and policy-filter notice. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-006 | Evidence-first: every returned fact carries source, method (asserted/derived/inferred/curated), confidence, freshness and policy-filter notice. | P0»
- [ ] Evidence-first: every returned fact carries source, method (asserted/derived/inferred/curated), confidence, freshness and policy-filter notice.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-007 [P0] SR-CON-007: Clean-room and license-clean: study external products and papers for ideas only; produce an independent implementation, SBOM and license report per release

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:104-104` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-007 | **Clean-room and license-clean:** study external products and papers for ideas only; produce an independent implementation, SBOM and license report per release. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-007 | Clean-room and license-clean: study external products and papers for ideas only; produce an independent implementation, SBOM and license report per release. | P0»
- [ ] Clean-room and license-clean: study external products and papers for ideas only; produce an independent implementation, SBOM and license report per release.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-008 [P0] SR-CON-008: Adapters over lock-in: no component outside an adapter may import a vendor-specific graph, vector, model, bus or storage SDK. Enforced by architecture tests

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:105-105` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-008 | **Adapters over lock-in:** no component outside an adapter may import a vendor-specific graph, vector, model, bus or storage SDK. Enforced by architecture tests. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-008 | Adapters over lock-in: no component outside an adapter may import a vendor-specific graph, vector, model, bus or storage SDK. Enforced by architecture tests. | P0»
- [ ] Adapters over lock-in: no component outside an adapter may import a vendor-specific graph, vector, model, bus or storage SDK. Enforced by architecture tests.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-009 [P0] SR-CON-009: Vendor-neutral data ownership: customers can export all data, ontology, config and audit trails in open formats at any time (§7.9)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:106-106` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-009 | **Vendor-neutral data ownership:** customers can export all data, ontology, config and audit trails in open formats at any time (§7.9). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-009 | Vendor-neutral data ownership: customers can export all data, ontology, config and audit trails in open formats at any time (§7.9). | P0»
- [ ] Vendor-neutral data ownership: customers can export all data, ontology, config and audit trails in open formats at any time (§7.9).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-CON-011 [P0] SR-CON-011: Every plugin MUST ship a Data-Flow Manifest declaring data classes sent/received, destinations, regions, retention and whether data can leave the tenant boundary. Installation MUST display it and requ

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:125-125` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-CON-011 | Every plugin MUST ship a **Data-Flow Manifest** declaring data classes sent/received, destinations, regions, retention and whether data can leave the tenant boundary. Installation MUST display it and require admin approval; the egress gateway enforces it at runtime. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-CON-011 | Every plugin MUST ship a Data-Flow Manifest declaring data classes sent/received, destinations, regions, retention and whether data can leave the tenant boundary. Installation MUST display it and require admin approval; the egress gateway enforces it at runtime. | P0»
- [ ] Every plugin MUST ship a Data-Flow Manifest declaring data classes sent/received, destinations, regions, retention and whether data can leave the tenant boundary. Installation MUST display it and require admin approval; the egress gateway enforces it at runtime.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/egress/provider.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/provider.py#L7-L7), [`packages/eoip/egress/router.py:89`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/egress/router.py#L89-L89)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-DEP-001 [P0] SR-DEP-001: Docker Compose distribution for DP-0 with healthy-start verification and one-command clean-reset demo including backup/restore (inherited MVP-FR-028)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:922-922` (table_row) · **Type:** Infra · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-DEP-001 | **Docker Compose** distribution for DP-0 with healthy-start verification and one-command clean-reset demo including backup/restore (inherited `MVP-FR-028`). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-DEP-001 | Docker Compose distribution for DP-0 with healthy-start verification and one-command clean-reset demo including backup/restore (inherited MVP-FR-028). | P0»
- [ ] Docker Compose distribution for DP-0 with healthy-start verification and one-command clean-reset demo including backup/restore (inherited MVP-FR-028).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-DEP-003 [P0] SR-DEP-003: Offline delivery: signed OCI image archives, model bundles, ontology/industry packs, connector catalog, docs, license file, checksum manifest; verified by an installer preflight checker (OS, kernel, C

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:924-924` (table_row) · **Type:** Infra · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-DEP-003 | **Offline delivery:** signed OCI image archives, model bundles, ontology/industry packs, connector catalog, docs, license file, checksum manifest; verified by an installer **preflight checker** (OS, kernel, CPU/GPU, storage, ports, time sync, certificates). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-DEP-003 | Offline delivery: signed OCI image archives, model bundles, ontology/industry packs, connector catalog, docs, license file, checksum manifest; verified by an installer preflight checker (OS, kernel, CPU/GPU, storage, ports, time sync, certificates). | P0»
- [ ] Offline delivery: signed OCI image archives, model bundles, ontology/industry packs, connector catalog, docs, license file, checksum manifest; verified by an installer preflight checker (OS, kernel, CPU/GPU, storage, ports, time sync, certificates).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-DEP-006 [P0] SR-DEP-006: Supported-platform matrix (OS, kernel, Kubernetes, container runtime, browsers, GPUs) maintained and tested per release

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:927-927` (table_row) · **Type:** Infra · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-DEP-006 | **Supported-platform matrix** (OS, kernel, Kubernetes, container runtime, browsers, GPUs) maintained and tested per release. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-DEP-006 | Supported-platform matrix (OS, kernel, Kubernetes, container runtime, browsers, GPUs) maintained and tested per release. | P0»
- [ ] Supported-platform matrix (OS, kernel, Kubernetes, container runtime, browsers, GPUs) maintained and tested per release.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-DEP-009 [P0] SR-DEP-009: Reference architectures and hardening guides per profile and tier, including network diagrams for air-gapped and connected variants

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:930-930` (table_row) · **Type:** Infra · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-DEP-009 | **Reference architectures and hardening guides** per profile and tier, including network diagrams for air-gapped and connected variants. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-DEP-009 | Reference architectures and hardening guides per profile and tier, including network diagrams for air-gapped and connected variants. | P0»
- [ ] Reference architectures and hardening guides per profile and tier, including network diagrams for air-gapped and connected variants.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-EXT-001 [P0] SR-EXT-001: Headless first: every UI capability is available through public, versioned APIs — REST (OpenAPI 3.1), GraphQL (ontology-generated), gRPC (high-volume), WebSocket/SSE (streaming answers, subscriptions)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:776-776` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-001 | **Headless first:** every UI capability is available through public, versioned APIs — REST (OpenAPI 3.1), GraphQL (ontology-generated), gRPC (high-volume), WebSocket/SSE (streaming answers, subscriptions), webhooks, MCP, CLI. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-001 | Headless first: every UI capability is available through public, versioned APIs — REST (OpenAPI 3.1), GraphQL (ontology-generated), gRPC (high-volume), WebSocket/SSE (streaming answers, subscriptions), webhooks, MCP, CLI. | P0»
- [ ] Headless first: every UI capability is available through public, versioned APIs — REST (OpenAPI 3.1), GraphQL (ontology-generated), gRPC (high-volume), WebSocket/SSE (streaming answers, subscriptions), webhooks, MCP, CLI.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-EXT-002 [P0] SR-EXT-002: API standards: semantic versioning, ≥ 12-month deprecation window, idempotency keys, cursor pagination, async job pattern, consistent error model, rate-limit headers, generated reference and SDKs

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:777-777` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-002 | API standards: semantic versioning, ≥ 12-month deprecation window, idempotency keys, cursor pagination, async job pattern, consistent error model, rate-limit headers, generated reference and SDKs. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-002 | API standards: semantic versioning, ≥ 12-month deprecation window, idempotency keys, cursor pagination, async job pattern, consistent error model, rate-limit headers, generated reference and SDKs. | P0»
- [ ] API standards: semantic versioning, ≥ 12-month deprecation window, idempotency keys, cursor pagination, async job pattern, consistent error model, rate-limit headers, generated reference and SDKs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-EXT-003 [P0] SR-EXT-003: Admin APIs cover tenants, users, config, branding, licenses, connectors, policies — enabling partner automation

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:778-778` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-003 | **Admin APIs** cover tenants, users, config, branding, licenses, connectors, policies — enabling partner automation. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-003 | Admin APIs cover tenants, users, config, branding, licenses, connectors, policies — enabling partner automation. | P0»
- [ ] Admin APIs cover tenants, users, config, branding, licenses, connectors, policies — enabling partner automation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-EXT-004 [P0] SR-EXT-004: Official SDKs: Python, TypeScript at P0; Java/Kotlin, Go, .NET at P1; Jupyter/notebook integrations

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:779-779` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-004 | Official SDKs: Python, TypeScript at P0; Java/Kotlin, Go, .NET at P1; Jupyter/notebook integrations. | P0/P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-004 | Official SDKs: Python, TypeScript at P0; Java/Kotlin, Go, .NET at P1; Jupyter/notebook integrations. | P0/P1»
- [ ] Official SDKs: Python, TypeScript at P0; Java/Kotlin, Go, .NET at P1; Jupyter/notebook integrations.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-EXT-005 [P0] SR-EXT-005: Integration surface: Slack/Teams-class ChatOps, ITSM (ServiceNow/Jira), CI/CD bots (PR impact comments, merge-risk gates), SIEM, email, calendar, BI tools (SR-ING-071), IDE extensions (VS Code at P0; 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:780-780` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-005 | **Integration surface:** Slack/Teams-class ChatOps, ITSM (ServiceNow/Jira), CI/CD bots (PR impact comments, merge-risk gates), SIEM, email, calendar, BI tools (SR-ING-071), IDE extensions (VS Code at P0; JetBrains at P1). | P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-005 | Integration surface: Slack/Teams-class ChatOps, ITSM (ServiceNow/Jira), CI/CD bots (PR impact comments, merge-risk gates), SIEM, email, calendar, BI tools (SR-ING-071), IDE extensions (VS Code at P0; JetBrains at P1). | P1»
- [ ] Integration surface: Slack/Teams-class ChatOps, ITSM (ServiceNow/Jira), CI/CD bots (PR impact comments, merge-risk gates), SIEM, email, calendar, BI tools (SR-ING-071), IDE extensions (VS Code at P0; JetBrains at P1).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-EXT-010 [P0] SR-EXT-010: Extension points: connectors, parsers/extractors, relationship-discovery methods, identity-resolution matchers, graph algorithms, store adapters, query-dialect adapters, model providers, agents/skills

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:786-786` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-010 | **Extension points:** connectors, parsers/extractors, relationship-discovery methods, identity-resolution matchers, graph algorithms, store adapters, query-dialect adapters, model providers, agents/skills, UI pages/widgets, report templates, validation/policy/ontology packs, notification channels, auth providers, export formats. | P0 (core 8) / P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-010 | Extension points: connectors, parsers/extractors, relationship-discovery methods, identity-resolution matchers, graph algorithms, store adapters, query-dialect adapters, model providers, agents/skills, UI pages/widgets, report templates, validation/policy/ontology packs, notification channels, auth providers, export formats. | P0 (core 8) / P1»
- [ ] Extension points: connectors, parsers/extractors, relationship-discovery methods, identity-resolution matchers, graph algorithms, store adapters, query-dialect adapters, model providers, agents/skills, UI pages/widgets, report templates, validation/policy/ontology packs, notification channels, auth providers, export formats.
- [ ] P0 (core 8) / P1
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-EXT-011 [P0] SR-EXT-011: Isolation: each plugin runs in a container or WASM sandbox with declared capabilities (network, filesystem, secrets, graph read/write scopes), CPU/memory/time limits, health checks and no ambient auth

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:787-787` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-011 | **Isolation:** each plugin runs in a container or WASM sandbox with declared capabilities (network, filesystem, secrets, graph read/write scopes), CPU/memory/time limits, health checks and no ambient authority. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-011 | Isolation: each plugin runs in a container or WASM sandbox with declared capabilities (network, filesystem, secrets, graph read/write scopes), CPU/memory/time limits, health checks and no ambient authority. | P0»
- [ ] Isolation: each plugin runs in a container or WASM sandbox with declared capabilities (network, filesystem, secrets, graph read/write scopes), CPU/memory/time limits, health checks and no ambient authority.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-EXT-012 [P0] SR-EXT-012: Signed, versioned packages with manifest, compatibility range, Data-Flow Manifest, SBOM and test fixtures; trust levels (first-party / certified partner / community / private)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:788-788` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-EXT-012 | **Signed, versioned packages** with manifest, compatibility range, Data-Flow Manifest, SBOM and test fixtures; trust levels (first-party / certified partner / community / private). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-EXT-012 | Signed, versioned packages with manifest, compatibility range, Data-Flow Manifest, SBOM and test fixtures; trust levels (first-party / certified partner / community / private). | P0»
- [ ] Signed, versioned packages with manifest, compatibility range, Data-Flow Manifest, SBOM and test fixtures; trust levels (first-party / certified partner / community / private).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-001 [P0] SR-GDB-001: All graph access MUST go through the Graph Store Port exposing: schema ops, bulk load, transactional upsert (idempotent by canonical ID), traversal, path, neighborhood, aggregation, full-scan with cur

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:183-183` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-001 | All graph access MUST go through the **Graph Store Port** exposing: schema ops, bulk load, transactional upsert (idempotent by canonical ID), traversal, path, neighborhood, aggregation, full-scan with cursor, index management, snapshot/export, health and statistics. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-001 | All graph access MUST go through the Graph Store Port exposing: schema ops, bulk load, transactional upsert (idempotent by canonical ID), traversal, path, neighborhood, aggregation, full-scan with cursor, index management, snapshot/export, health and statistics. | P0»
- [ ] All graph access MUST go through the Graph Store Port exposing: schema ops, bulk load, transactional upsert (idempotent by canonical ID), traversal, path, neighborhood, aggregation, full-scan with cursor, index management, snapshot/export, health and statistics.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-002 [P0] SR-GDB-002: Each adapter MUST publish a Capability Manifest (example in §5.6). The planner uses it to choose pushdown vs in-engine execution and to refuse or degrade unsupported plans explicitly (never silently)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:184-184` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-002 | Each adapter MUST publish a **Capability Manifest** (example in §5.6). The planner uses it to choose pushdown vs in-engine execution and to refuse or degrade unsupported plans *explicitly* (never silently). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-002 | Each adapter MUST publish a Capability Manifest (example in §5.6). The planner uses it to choose pushdown vs in-engine execution and to refuse or degrade unsupported plans explicitly (never silently). | P0»
- [ ] Each adapter MUST publish a Capability Manifest (example in §5.6). The planner uses it to choose pushdown vs in-engine execution and to refuse or degrade unsupported plans explicitly (never silently).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/adapters/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/adapters/__init__.py#L1-L1), [`packages/eoip/adapters/catalog.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/adapters/catalog.py#L1-L1), [`packages/eoip/adapters/manifests.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/adapters/manifests.py#L1-L1)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-003 [P0] SR-GDB-003: A backend-neutral conformance suite (contract tests + golden queries + performance probes + failure injection) MUST gate every adapter. Backend-specific behavior (e.g., HugeGraph 1.7 not honoring UNIQ

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:185-185` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-003 | A **backend-neutral conformance suite** (contract tests + golden queries + performance probes + failure injection) MUST gate every adapter. Backend-specific behavior (e.g., HugeGraph 1.7 not honoring UNIQUE edge indexes, requiring SECONDARY + sort-key emulation) is recorded in the manifest, not scattered in code. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-003 | A backend-neutral conformance suite (contract tests + golden queries + performance probes + failure injection) MUST gate every adapter. Backend-specific behavior (e.g., HugeGraph 1.7 not honoring UNIQUE edge indexes, requiring SECONDARY + sort-key emulation) is recorded in the manifest, not scattered in code. | P0»
- [ ] A backend-neutral conformance suite (contract tests + golden queries + performance probes + failure injection) MUST gate every adapter. Backend-specific behavior (e.g., HugeGraph 1.7 not honoring UNIQUE edge indexes, requiring SECONDARY + sort-key emulation) is recorded in the manifest, not scattered in code.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/adapters/janusgraph.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/adapters/janusgraph.py#L13-L13), [`packages/eoip/adapters/manifests.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/adapters/manifests.py#L6-L6)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-004 [P0] SR-GDB-004: Certification tiers: Tier A Certified (full conformance, benchmarked, HA validated, supported under SLA); Tier B Compatible (documented capability gaps); Tier C Community/Experimental. Marketing MUST 

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:186-186` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-004 | **Certification tiers:** Tier A *Certified* (full conformance, benchmarked, HA validated, supported under SLA); Tier B *Compatible* (documented capability gaps); Tier C *Community/Experimental*. Marketing MUST NOT claim support beyond the tier. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-004 | Certification tiers: Tier A Certified (full conformance, benchmarked, HA validated, supported under SLA); Tier B Compatible (documented capability gaps); Tier C Community/Experimental. Marketing MUST NOT claim support beyond the tier. | P0»
- [ ] Certification tiers: Tier A Certified (full conformance, benchmarked, HA validated, supported under SLA); Tier B Compatible (documented capability gaps); Tier C Community/Experimental. Marketing MUST NOT claim support beyond the tier.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/adapters/manifests.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/adapters/manifests.py#L6-L6)
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-010 [P0] SR-GDB-010: Embedded engine option for DP-0/edge nodes with no server process, and an in-memory engine for tests only (selection is explicit configuration, never a silent fallback)

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:192-192` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-010 | **Embedded engine option** for DP-0/edge nodes with no server process, and an in-memory engine for tests only (selection is explicit configuration, never a silent fallback). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-010 | Embedded engine option for DP-0/edge nodes with no server process, and an in-memory engine for tests only (selection is explicit configuration, never a silent fallback). | P0»
- [ ] Embedded engine option for DP-0/edge nodes with no server process, and an in-memory engine for tests only (selection is explicit configuration, never a silent fallback).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-012 [P0] SR-GDB-012: Object/raw store: filesystem (DP-0), S3-compatible (clustered), and cloud blob adapters. Raw captures are immutable, content-addressed (SHA-256), encrypted, and retention-managed

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:217-217` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-012 | **Object/raw store:** filesystem (DP-0), S3-compatible (clustered), and cloud blob adapters. Raw captures are immutable, content-addressed (SHA-256), encrypted, and retention-managed. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-012 | Object/raw store: filesystem (DP-0), S3-compatible (clustered), and cloud blob adapters. Raw captures are immutable, content-addressed (SHA-256), encrypted, and retention-managed. | P0»
- [ ] Object/raw store: filesystem (DP-0), S3-compatible (clustered), and cloud blob adapters. Raw captures are immutable, content-addressed (SHA-256), encrypted, and retention-managed.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-GDB-013 [P0] SR-GDB-013: Event bus adapters: embedded log, NATS JetStream-class, Kafka/Redpanda-class, RabbitMQ, cloud queues

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:218-218` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-013 | **Event bus adapters:** embedded log, NATS JetStream-class, Kafka/Redpanda-class, RabbitMQ, cloud queues. | P0/P1
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-013 | Event bus adapters: embedded log, NATS JetStream-class, Kafka/Redpanda-class, RabbitMQ, cloud queues. | P0/P1»
- [ ] Event bus adapters: embedded log, NATS JetStream-class, Kafka/Redpanda-class, RabbitMQ, cloud queues.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-014 [P0] SR-GDB-014: Cache: in-process plus a Redis-protocol-compatible adapter; every cache key MUST include tenant, policy-version and graph-revision

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:219-219` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-014 | **Cache:** in-process plus a Redis-protocol-compatible adapter; every cache key MUST include tenant, policy-version and graph-revision. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-014 | Cache: in-process plus a Redis-protocol-compatible adapter; every cache key MUST include tenant, policy-version and graph-revision. | P0»
- [ ] Cache: in-process plus a Redis-protocol-compatible adapter; every cache key MUST include tenant, policy-version and graph-revision.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-GDB-016 [P0] SR-GDB-016: Component license matrix: every bundled and optional component is classified (permissive / weak copyleft / strong copyleft or network-copyleft / source-available / commercial). Anything other than per

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:221-221` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-GDB-016 | **Component license matrix:** every bundled and optional component is classified (permissive / weak copyleft / strong copyleft or network-copyleft / source-available / commercial). Anything other than permissive MUST NOT be bundled without legal sign-off and MUST be offered as bring-your-own where needed. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-GDB-016 | Component license matrix: every bundled and optional component is classified (permissive / weak copyleft / strong copyleft or network-copyleft / source-available / commercial). Anything other than permissive MUST NOT be bundled without legal sign-off and MUST be offered as bring-your-own where needed. | P0»
- [ ] Component license matrix: every bundled and optional component is classified (permissive / weak copyleft / strong copyleft or network-copyleft / source-available / commercial). Anything other than permissive MUST NOT be bundled without legal sign-off and MUST be offered as bring-your-own where needed.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-001 [P0] SR-ING-001: Connector SDK (Python and TypeScript at P0; Go/Java at P1) with a stable contract: discover, authenticate, fetch(cursor), schema, health, metrics, capabilities, deletionsemantics; connectors run sandb

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:345-345` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-001 | **Connector SDK** (Python and TypeScript at P0; Go/Java at P1) with a stable contract: `discover`, `authenticate`, `fetch(cursor)`, `schema`, `health`, `metrics`, `capabilities`, `deletion_semantics`; connectors run sandboxed with declared scopes. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-001 | Connector SDK (Python and TypeScript at P0; Go/Java at P1) with a stable contract: discover, authenticate, fetch(cursor), schema, health, metrics, capabilities, deletion_semantics; connectors run sandboxed with declared scopes. | P0»
- [ ] Connector SDK (Python and TypeScript at P0; Go/Java at P1) with a stable contract: discover, authenticate, fetch(cursor), schema, health, metrics, capabilities, deletion_semantics; connectors run sandboxed with declared scopes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-SR-ING-002 [P0] SR-ING-002: Resiliency: pagination, rate-limit adaptation, retry with jitter, circuit breaker, checkpoint/cursor, partial-failure isolation, DLQ, replay, dry-run, backfill and incremental sync

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:346-346` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-002 | Resiliency: pagination, rate-limit adaptation, retry with jitter, circuit breaker, checkpoint/cursor, partial-failure isolation, DLQ, replay, dry-run, backfill and incremental sync. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-002 | Resiliency: pagination, rate-limit adaptation, retry with jitter, circuit breaker, checkpoint/cursor, partial-failure isolation, DLQ, replay, dry-run, backfill and incremental sync. | P0»
- [ ] Resiliency: pagination, rate-limit adaptation, retry with jitter, circuit breaker, checkpoint/cursor, partial-failure isolation, DLQ, replay, dry-run, backfill and incremental sync.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-003 [P0] SR-ING-003: Change capture: polling, webhooks, CDC (log-based where the source supports it), file watchers, stream consumers; deletes handled by tombstones with configurable semantics (soft delete, retire edge, h

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:347-347` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-003 | **Change capture:** polling, webhooks, CDC (log-based where the source supports it), file watchers, stream consumers; deletes handled by tombstones with configurable semantics (soft delete, retire edge, hard delete on policy). | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-003 | Change capture: polling, webhooks, CDC (log-based where the source supports it), file watchers, stream consumers; deletes handled by tombstones with configurable semantics (soft delete, retire edge, hard delete on policy). | P0»
- [ ] Change capture: polling, webhooks, CDC (log-based where the source supports it), file watchers, stream consumers; deletes handled by tombstones with configurable semantics (soft delete, retire edge, hard delete on policy).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-SR-ING-004 [P0] SR-ING-004: Credential isolation: connector secrets live only in the secret store, scoped per tenant/connector, rotated, never logged, never visible to plugins other than the owning connector

- **Source:** `EOIP-engg-doc-pkg/super-requirements.md:348-348` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** Tests are mapped/referenced but none ran in the audit (excluded or not collected); No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 2.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
SR-ING-004 | **Credential isolation:** connector secrets live only in the secret store, scoped per tenant/connector, rotated, never logged, never visible to plugins other than the owning connector. | P0
```
</details>

**Next steps**
1. Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): tests/unit/test_sr_wave_api_routes.py
2. Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites
3. Attach the junit (L2) and make the suite part of an L3-eligible workflow

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «SR-ING-004 | Credential isolation: connector secrets live only in the secret store, scoped per tenant/connector, rotated, never logged, never visible to plugins other than the owning connector. | P0»
- [ ] Credential isolation: connector secrets live only in the secret store, scoped per tenant/connector, rotated, never logged, never visible to plugins other than the owning connector.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_sr_wave_api_routes.py`

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

