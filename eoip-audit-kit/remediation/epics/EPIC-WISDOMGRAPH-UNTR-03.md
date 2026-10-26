# EPIC-WISDOMGRAPH-UNTR-03: wisdom-graph-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~364.0 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-WG-CTX-006 [P2] WG-CTX-006: Supersession and staleness: when a fact in a decision's read set is later corrected or retracted, the decision is marked contextsuperseded = true with the change event ids (it is not edited); preceden

- **Source:** `wisdom-graph-requirements.md:542-542` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-CTX-006 | Supersession and staleness: when a fact in a decision's read set is later corrected or retracted, the decision is marked `context_superseded = true` with the change event ids (it is not edited); precedent ranking and lesson induction treat the decision per WG-COH-002.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-CTX-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-CTX-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-CTX-006 | Supersession and staleness: when a fact in a decision's read set is later corrected or retracted, the decision is marked context_superseded = true with the change event ids (it is not edited); precedent ranking and lesson induction treat the decision per WG-COH-002.»
- [ ] Supersession and staleness: when a fact in a decision's read set is later corrected or retracted, the decision is marked context_superseded = true with the change event ids (it is not edited); precedent ranking and lesson induction treat the decision per WG-COH-002.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-CTX-007 [P2] WG-CTX-007: Replay package: POST /wisdom/decisions/{id}/replay builds a package with the decision-time context, inputs, model and policy versions, counsel shown and the action, and re-evaluates the decision's che

- **Source:** `wisdom-graph-requirements.md:543-543` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-CTX-007 | Replay package: `POST /wisdom/decisions/{id}/replay` builds a package with the decision-time context, inputs, model and policy versions, counsel shown and the action, and re-evaluates the decision's checkpoint logic and counsel against that frozen context on a shadow branch (REQ-SHB-001). It returns `SAME`, `DIFFERENT` with `differences[]`, or `NOT_REPLAYABLE` with a `reason`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-CTX-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-CTX-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-CTX-007 | Replay package: POST /wisdom/decisions/{id}/replay builds a package with the decision-time context, inputs, model and policy versions, counsel shown and the action, and re-evaluates the decision's checkpoint logic and counsel against that frozen context on a shadow branch (REQ-SHB-001). It returns SAME, DIFFERENT with differences[], or NOT_REPLAYABLE with a reason.»
- [ ] Replay package: POST /wisdom/decisions/{id}/replay builds a package with the decision-time context, inputs, model and policy versions, counsel shown and the action, and re-evaluates the decision's checkpoint logic and counsel against that frozen context on a shadow branch (REQ-SHB-001). It returns SAME, DIFFERENT with differences[], or NOT_REPLAYABLE with a reason.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-CTX-008 [P2] WG-CTX-008: Present-day comparison: POST /wisdom/decisions/{id}/reconsider evaluates the same situation against the current state, current policies, current lessons and current world model, and returns what couns

- **Source:** `wisdom-graph-requirements.md:544-544` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-CTX-008 | Present-day comparison: `POST /wisdom/decisions/{id}/reconsider` evaluates the same situation against the current state, current policies, current lessons and current world model, and returns what counsel would say today, with a diff against the original counsel. It never changes the original trace.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-CTX-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-CTX-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-CTX-008 | Present-day comparison: POST /wisdom/decisions/{id}/reconsider evaluates the same situation against the current state, current policies, current lessons and current world model, and returns what counsel would say today, with a diff against the original counsel. It never changes the original trace.»
- [ ] Present-day comparison: POST /wisdom/decisions/{id}/reconsider evaluates the same situation against the current state, current policies, current lessons and current world model, and returns what counsel would say today, with a diff against the original counsel. It never changes the original trace.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-CTX-009 [P2] WG-CTX-009: Performance: context capture p95 < 150 ms asynchronous for read sets ≤ 2,000 assertions; timeline query p95 < 300 ms for ≤ 10,000 events per entity; replay of a decision with ≤ 2,000 context assertion

- **Source:** `wisdom-graph-requirements.md:545-545` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-CTX-009 | Performance: context capture p95 < 150 ms asynchronous for read sets ≤ 2,000 assertions; timeline query p95 < 300 ms for ≤ 10,000 events per entity; replay of a decision with ≤ 2,000 context assertions p95 < 5 s.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-CTX-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-CTX-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-CTX-009 | Performance: context capture p95 < 150 ms asynchronous for read sets ≤ 2,000 assertions; timeline query p95 < 300 ms for ≤ 10,000 events per entity; replay of a decision with ≤ 2,000 context assertions p95 < 5 s.»
- [ ] Performance: context capture p95 < 150 ms asynchronous for read sets ≤ 2,000 assertions; timeline query p95 < 300 ms for ≤ 10,000 events per entity; replay of a decision with ≤ 2,000 context assertions p95 < 5 s.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-CTX-010 [P2] WG-CTX-010: The event clock and contexts are retained per wisdom.contextretentiondays (default 1,095). Retention never deletes a context referenced by an ACTIVE lesson's supporting decisions; such contexts are re

- **Source:** `wisdom-graph-requirements.md:546-546` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-CTX-010 | The event clock and contexts are retained per `wisdom.context_retention_days` (default 1,095). Retention never deletes a context referenced by an `ACTIVE` lesson's supporting decisions; such contexts are reduced to ids, versions and digests only when payload retention expires.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-CTX-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-CTX-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-CTX-010 | The event clock and contexts are retained per wisdom.context_retention_days (default 1,095). Retention never deletes a context referenced by an ACTIVE lesson's supporting decisions; such contexts are reduced to ids, versions and digests only when payload retention expires.»
- [ ] The event clock and contexts are retained per wisdom.context_retention_days (default 1,095). Retention never deletes a context referenced by an ACTIVE lesson's supporting decisions; such contexts are reduced to ids, versions and digests only when payload retention expires.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-EMG-001 [P2] WG-EMG-001: Situation kinds: nightly HDBSCAN (minclustersize wisdom.situationmincluster = 15) over situation fingerprints per decision type; clusters stable across 3 runs (Jaccard ≥ 0.7 of members) become propose

- **Source:** `wisdom-graph-requirements.md:891-891` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-EMG-001 | Situation kinds: nightly HDBSCAN (min_cluster_size `wisdom.situation_min_cluster` = 15) over situation fingerprints per decision type; clusters stable across 3 runs (Jaccard ≥ 0.7 of members) become proposed situation labels with suggested names generated through the SDK (`GENERATED`) and defining features (features whose distribution differs most from the rest, top 5 by standardized mean difference).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-EMG-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-EMG-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-EMG-001 | Situation kinds: nightly HDBSCAN (min_cluster_size wisdom.situation_min_cluster = 15) over situation fingerprints per decision type; clusters stable across 3 runs (Jaccard ≥ 0.7 of members) become proposed situation labels with suggested names generated through the SDK (GENERATED) and defining features (features whose distribution differs most from the rest, top 5 »
- [ ] Situation kinds: nightly HDBSCAN (min_cluster_size wisdom.situation_min_cluster = 15) over situation fingerprints per decision type; clusters stable across 3 runs (Jaccard ≥ 0.7 of members) become proposed situation labels with suggested names generated through the SDK (GENERATED) and defining features (features whose distribution differs most from the rest, top 5 by standardized mean difference).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-EMG-002 [P2] WG-EMG-002: Proposed situation labels and decision subtypes are submitted to the Ontology Advisor queue (REQ-INV4-006) with impact simulation; approved proposals become meaning-release drafts (REQ-MMG-010). The W

- **Source:** `wisdom-graph-requirements.md:892-892` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-EMG-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-EMG-002 | Proposed situation labels and decision subtypes are submitted to the Ontology Advisor queue (`REQ-INV4-006`) with impact simulation; approved proposals become meaning-release drafts (`REQ-MMG-010`). The Wisdom Graph never edits the ontology.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-EMG-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-EMG-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-EMG-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-EMG-002 | Proposed situation labels and decision subtypes are submitted to the Ontology Advisor queue (REQ-INV4-006) with impact simulation; approved proposals become meaning-release drafts (REQ-MMG-010). The Wisdom Graph never edits the ontology.»
- [ ] Proposed situation labels and decision subtypes are submitted to the Ontology Advisor queue (REQ-INV4-006) with impact simulation; approved proposals become meaning-release drafts (REQ-MMG-010). The Wisdom Graph never edits the ontology.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-EMG-003 [P2] WG-EMG-003: Trajectory-informed relevance: traversal frequencies of relation types and metapaths in agent trajectories that led to decisions with successful outcomes are counted per decision type; relation types 

- **Source:** `wisdom-graph-requirements.md:893-893` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-EMG-003 | Trajectory-informed relevance: traversal frequencies of relation types and metapaths in agent trajectories that led to decisions with successful outcomes are counted per decision type; relation types with high success-conditional traversal are proposed as `wg:situationFeature` annotations (steward approval required).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-EMG-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-EMG-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-EMG-003 | Trajectory-informed relevance: traversal frequencies of relation types and metapaths in agent trajectories that led to decisions with successful outcomes are counted per decision type; relation types with high success-conditional traversal are proposed as wg:situationFeature annotations (steward approval required).»
- [ ] Trajectory-informed relevance: traversal frequencies of relation types and metapaths in agent trajectories that led to decisions with successful outcomes are counted per decision type; relation types with high success-conditional traversal are proposed as wg:situationFeature annotations (steward approval required).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-EMG-006 [P2] WG-EMG-006: Acceptance on the seeded tenant: the two planted recurring situation kinds (plan §4.3) are proposed with ≥ 80% member overlap with the planted sets; the planted unwritten rule ("always notify the acco

- **Source:** `wisdom-graph-requirements.md:896-896` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-EMG-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-EMG-006 | Acceptance on the seeded tenant: the two planted recurring situation kinds (plan §4.3) are proposed with ≥ 80% member overlap with the planted sets; the planted unwritten rule ("always notify the account owner before a discount above 10%") appears in the unwritten-rules list.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-EMG-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-EMG-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-EMG-006

**Acceptance criteria**
- [ ] on the seeded tenant: the two planted recurring situation kinds (plan §4.3) are proposed with ≥ 80% member overlap with the planted sets; the planted unwritten rule ("always notify the account owner before a discount above 10%") appears in the unwritten-rules list
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-ENT-001 [P2] WG-ENT-001: identity-resolution-service maintains SAMEAS candidate links between knowledge-layer entities from different source systems with score, method and status (CANDIDATE, CONFIRMED, REJECTED). Candidates c

- **Source:** `wisdom-graph-requirements.md:564-564` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-ENT-001 | `identity-resolution-service` maintains `SAME_AS` candidate links between knowledge-layer entities from different source systems with score, method and status (`CANDIDATE`, `CONFIRMED`, `REJECTED`). Candidates come from Invention 11 blocking and embedding search (`REQ-INV11-001`) plus exact matches on configured identifier properties (`wisdom.identity_keys` per type).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-ENT-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-ENT-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-ENT-001 | identity-resolution-service maintains SAME_AS candidate links between knowledge-layer entities from different source systems with score, method and status (CANDIDATE, CONFIRMED, REJECTED). Candidates come from Invention 11 blocking and embedding search (REQ-INV11-001) plus exact matches on configured identifier properties (wisdom.identity_keys per type).»
- [ ] identity-resolution-service maintains SAME_AS candidate links between knowledge-layer entities from different source systems with score, method and status (CANDIDATE, CONFIRMED, REJECTED). Candidates come from Invention 11 blocking and embedding search (REQ-INV11-001) plus exact matches on configured identifier properties (wisdom.identity_keys per type).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-ENT-002 [P2] WG-ENT-002: SAMEAS links are used for timeline, event and attribution joins only when CONFIRMED, or when CANDIDATE with score ≥ wisdom.identityautothreshold (default 0.97) and both entities are OBSERVED. Links ne

- **Source:** `wisdom-graph-requirements.md:565-565` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-ENT-002 | `SAME_AS` links are used for timeline, event and attribution joins only when `CONFIRMED`, or when `CANDIDATE` with score ≥ `wisdom.identity_auto_threshold` (default 0.97) and both entities are `OBSERVED`. Links never merge entities (merging stays the Invention 11 workflow).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-ENT-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-ENT-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-ENT-002 | SAME_AS links are used for timeline, event and attribution joins only when CONFIRMED, or when CANDIDATE with score ≥ wisdom.identity_auto_threshold (default 0.97) and both entities are OBSERVED. Links never merge entities (merging stays the Invention 11 workflow).»
- [ ] SAME_AS links are used for timeline, event and attribution joins only when CONFIRMED, or when CANDIDATE with score ≥ wisdom.identity_auto_threshold (default 0.97) and both entities are OBSERVED. Links never merge entities (merging stays the Invention 11 workflow).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-ENT-003 [P2] WG-ENT-003: Event joins: events from different systems are grouped into one occurrence when they share a correlation id, or share at least one resolved about-entity within wisdom.eventjoinwindow (default 30 min) 

- **Source:** `wisdom-graph-requirements.md:566-566` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-ENT-003 | Event joins: events from different systems are grouped into one occurrence when they share a correlation id, or share at least one resolved about-entity within `wisdom.event_join_window` (default 30 min) and the configured event-kind pairing rules. Each grouping stores its evidence.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-ENT-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-ENT-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-ENT-003 | Event joins: events from different systems are grouped into one occurrence when they share a correlation id, or share at least one resolved about-entity within wisdom.event_join_window (default 30 min) and the configured event-kind pairing rules. Each grouping stores its evidence.»
- [ ] Event joins: events from different systems are grouped into one occurrence when they share a correlation id, or share at least one resolved about-entity within wisdom.event_join_window (default 30 min) and the configured event-kind pairing rules. Each grouping stores its evidence.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-ENT-004 [P2] WG-ENT-004: Semantic joins between policies, decision types and situation labels from different systems use embedding similarity ≥ wisdom.semanticjointhreshold (default 0.88) and are proposals for steward confirm

- **Source:** `wisdom-graph-requirements.md:567-567` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-ENT-004 | Semantic joins between policies, decision types and situation labels from different systems use embedding similarity ≥ `wisdom.semantic_join_threshold` (default 0.88) and are proposals for steward confirmation, never automatic.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-ENT-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-ENT-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-ENT-004 | Semantic joins between policies, decision types and situation labels from different systems use embedding similarity ≥ wisdom.semantic_join_threshold (default 0.88) and are proposals for steward confirmation, never automatic.»
- [ ] Semantic joins between policies, decision types and situation labels from different systems use embedding similarity ≥ wisdom.semantic_join_threshold (default 0.88) and are proposals for steward confirmation, never automatic.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-ENT-006 [P2] WG-ENT-006: Benchmark on the seeded cross-system set (evals/wisdom/identity-v1, ≥ 400 labelled pairs): precision ≥ 0.95 at recall ≥ 0.85 for links used automatically

- **Source:** `wisdom-graph-requirements.md:569-569` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-ENT-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-ENT-006 | Benchmark on the seeded cross-system set (`evals/wisdom/identity-v1`, ≥ 400 labelled pairs): precision ≥ 0.95 at recall ≥ 0.85 for links used automatically.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-ENT-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-ENT-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-ENT-006

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-ENT-006 | Benchmark on the seeded cross-system set (evals/wisdom/identity-v1, ≥ 400 labelled pairs): precision ≥ 0.95 at recall ≥ 0.85 for links used automatically.»
- [ ] Benchmark on the seeded cross-system set (evals/wisdom/identity-v1, ≥ 400 labelled pairs): precision ≥ 0.95 at recall ≥ 0.85 for links used automatically.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-IPH-001 [P2] WG-IPH-001: The CI gate of REQ-IPH-001 (ip.publicreleaseallowed, default false) covers every Wisdom module path (§4.3). No public package, public remote or public documentation containing those paths may be publi

- **Source:** `wisdom-graph-requirements.md:187-187` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-IPH-001 | The CI gate of `REQ-IPH-001` (`ip.public_release_allowed`, default `false`) covers every Wisdom module path (§4.3). No public package, public remote or public documentation containing those paths may be published while the flag is `false`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-IPH-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-IPH-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-IPH-001 | The CI gate of REQ-IPH-001 (ip.public_release_allowed, default false) covers every Wisdom module path (§4.3). No public package, public remote or public documentation containing those paths may be published while the flag is false.»
- [ ] The CI gate of REQ-IPH-001 (ip.public_release_allowed, default false) covers every Wisdom module path (§4.3). No public package, public remote or public documentation containing those paths may be published while the flag is false.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-IPH-002 [P2] WG-IPH-002: Source files implementing the candidate inventions in §29.2 carry the repository licence header (rules of REQ-IPH-002)

- **Source:** `wisdom-graph-requirements.md:188-188` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-IPH-002 | Source files implementing the candidate inventions in §29.2 carry the repository licence header (rules of `REQ-IPH-002`).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-IPH-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-IPH-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-IPH-002 | Source files implementing the candidate inventions in §29.2 carry the repository licence header (rules of REQ-IPH-002).»
- [ ] Source files implementing the candidate inventions in §29.2 carry the repository licence header (rules of REQ-IPH-002).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-IPH-004 [P2] WG-IPH-004: Code comments, READMEs and API descriptions describe behaviour and never claim novelty. Do not write "patented", "patent pending" or "novel". Each candidate invention module contains an internal INVEN

- **Source:** `wisdom-graph-requirements.md:190-190` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-IPH-004 | Code comments, READMEs and API descriptions describe behaviour and never claim novelty. Do not write "patented", "patent pending" or "novel". Each candidate invention module contains an internal `INVENTION.md` (not published) with: candidate number (§29.2), requirement IDs, algorithm IDs, the date the first working version produced an Evidence Pack, and the person who directed the work.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-IPH-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-IPH-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-IPH-004 | Code comments, READMEs and API descriptions describe behaviour and never claim novelty. Do not write "patented", "patent pending" or "novel". Each candidate invention module contains an internal INVENTION.md (not published) with: candidate number (§29.2), requirement IDs, algorithm IDs, the date the first working version produced an Evidence Pack, and the person wh»
- [ ] Code comments, READMEs and API descriptions describe behaviour and never claim novelty. Do not write "patented", "patent pending" or "novel". Each candidate invention module contains an internal INVENTION.md (not published) with: candidate number (§29.2), requirement IDs, algorithm IDs, the date the first working version produced an Evidence Pack, and the person who directed the work.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-002 [P2] WG-LES-002: No-upgrade for lessons. A lesson's warrant status is PREDICTED (computed) or ATTESTED (a steward approved it). It is never OBSERVED. A lesson never overwrites or deletes any knowledge-layer assertion,

- **Source:** `wisdom-graph-requirements.md:714-714` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-LES-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-002 | **No-upgrade for lessons.** A lesson's warrant status is `PREDICTED` (computed) or `ATTESTED` (a steward approved it). It is never `OBSERVED`. A lesson never overwrites or deletes any knowledge-layer assertion, policy or decision. Any attempt returns `WSD_LESSON_UPGRADE`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-LES-002

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-LES-002 | No-upgrade for lessons. A lesson's warrant status is PREDICTED (computed) or ATTESTED (a steward approved it). It is never OBSERVED. A lesson never overwrites or deletes any knowledge-layer assertion, policy or decision. Any attempt returns WSD_LESSON_UPGRADE.»
- [ ] No-upgrade for lessons. A lesson's warrant status is PREDICTED (computed) or ATTESTED (a steward approved it). It is never OBSERVED. A lesson never overwrites or deletes any knowledge-layer assertion, policy or decision. Any attempt returns WSD_LESSON_UPGRADE.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-004 [P2] WG-LES-004: Applicability evaluation: POST /wisdom/lessons/applicable {situation} returns lessons whose scope matches and no exclusion matches (applicable), lessons whose scope matches but an exclusion matches (e

- **Source:** `wisdom-graph-requirements.md:716-716` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-004 | Applicability evaluation: `POST /wisdom/lessons/applicable {situation}` returns lessons whose scope matches and no exclusion matches (`applicable`), lessons whose scope matches but an exclusion matches (`excluded`, with the exclusion), and lessons that would match if one numeric feature moved within `wisdom.near_boundary_margin` (default 10% of its standardized range) (`near_boundary`, with the condition).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-LES-004 | Applicability evaluation: POST /wisdom/lessons/applicable {situation} returns lessons whose scope matches and no exclusion matches (applicable), lessons whose scope matches but an exclusion matches (excluded, with the exclusion), and lessons that would match if one numeric feature moved within wisdom.near_boundary_margin (default 10% of its standardized range) (nea»
- [ ] Applicability evaluation: POST /wisdom/lessons/applicable {situation} returns lessons whose scope matches and no exclusion matches (applicable), lessons whose scope matches but an exclusion matches (excluded, with the exclusion), and lessons that would match if one numeric feature moved within wisdom.near_boundary_margin (default 10% of its standardized range) (near_boundary, with the condition).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-005 [P2] WG-LES-005: Each lesson reports its effect as a Beta credible interval at wisdom.lessoncrediblelevel (default 0.90) and uses the lower bound (not the point estimate) wherever it drives counsel

- **Source:** `wisdom-graph-requirements.md:717-717` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-005 | Each lesson reports its effect as a Beta credible interval at `wisdom.lesson_credible_level` (default 0.90) and uses the lower bound (not the point estimate) wherever it drives counsel.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-LES-005 | Each lesson reports its effect as a Beta credible interval at wisdom.lesson_credible_level (default 0.90) and uses the lower bound (not the point estimate) wherever it drives counsel.»
- [ ] Each lesson reports its effect as a Beta credible interval at wisdom.lesson_credible_level (default 0.90) and uses the lower bound (not the point estimate) wherever it drives counsel.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-006 [P2] WG-LES-006: Conflicting lessons: two ACTIVE lessons whose scopes overlap on ≥ 30 decisions and predict opposite effects for the same option are flagged LESSONCONFLICT; counsel shows both with their counts; the go

- **Source:** `wisdom-graph-requirements.md:718-718` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-006 | Conflicting lessons: two `ACTIVE` lessons whose scopes overlap on ≥ 30 decisions and predict opposite effects for the same option are flagged `LESSON_CONFLICT`; counsel shows both with their counts; the governance process WG-PRC-002 resolves them.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-LES-006 | Conflicting lessons: two ACTIVE lessons whose scopes overlap on ≥ 30 decisions and predict opposite effects for the same option are flagged LESSON_CONFLICT; counsel shows both with their counts; the governance process WG-PRC-002 resolves them.»
- [ ] Conflicting lessons: two ACTIVE lessons whose scopes overlap on ≥ 30 decisions and predict opposite effects for the same option are flagged LESSON_CONFLICT; counsel shows both with their counts; the governance process WG-PRC-002 resolves them.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-007 [P2] WG-LES-007: Lessons are linked to the dissent record: if a lesson's supporting decisions include decisions with minority reports later vindicated (REQ-DIS-007), the lesson view shows it, and the vindicated minori

- **Source:** `wisdom-graph-requirements.md:719-719` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-007 | Lessons are linked to the dissent record: if a lesson's supporting decisions include decisions with minority reports later vindicated (`REQ-DIS-007`), the lesson view shows it, and the vindicated minority position is offered as a candidate exclusion.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-LES-007 | Lessons are linked to the dissent record: if a lesson's supporting decisions include decisions with minority reports later vindicated (REQ-DIS-007), the lesson view shows it, and the vindicated minority position is offered as a candidate exclusion.»
- [ ] Lessons are linked to the dissent record: if a lesson's supporting decisions include decisions with minority reports later vindicated (REQ-DIS-007), the lesson view shows it, and the vindicated minority position is offered as a candidate exclusion.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-008 [P2] WG-LES-008: Incremental updates: a new eligible outcome updates alpha/beta, SUPPORTS/CONTRADICTS and freshness within 5 minutes p95, without waiting for the nightly induction

- **Source:** `wisdom-graph-requirements.md:720-720` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-008 | Incremental updates: a new eligible outcome updates `alpha`/`beta`, `SUPPORTS`/`CONTRADICTS` and freshness within 5 minutes p95, without waiting for the nightly induction.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-LES-008 | Incremental updates: a new eligible outcome updates alpha/beta, SUPPORTS/CONTRADICTS and freshness within 5 minutes p95, without waiting for the nightly induction.»
- [ ] Incremental updates: a new eligible outcome updates alpha/beta, SUPPORTS/CONTRADICTS and freshness within 5 minutes p95, without waiting for the nightly induction.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-009 [P2] WG-LES-009: Planted-lesson benchmark evals/wisdom/lessons-v1 on the seeded tenant (plan §4.3: 6 planted lessons with planted exclusions and 4 planted null effects). Acceptance: ≥ 5 of 6 planted lessons recovered 

- **Source:** `wisdom-graph-requirements.md:721-721` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-LES-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-009 | Planted-lesson benchmark `evals/wisdom/lessons-v1` on the seeded tenant (plan §4.3: 6 planted lessons with planted exclusions and 4 planted null effects). Acceptance: ≥ 5 of 6 planted lessons recovered with the correct condition set (allowing equivalent thresholds within 10%), ≥ 4 of 6 planted exclusions recovered by W6 after the counterexample stream, ≤ 1 spurious `CANDIDATE` lesson per 10 kept, and 0 of 4 null effects promoted.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-LES-009

**Acceptance criteria**
- [ ] ≥ 5 of 6 planted lessons recovered with the correct condition set (allowing equivalent thresholds within 10%), ≥ 4 of 6 planted exclusions recovered by W6 after the counterexample stream, ≤ 1 spurious CANDIDATE lesson per 10 kept, and 0 of 4 null effects promoted
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-010 [P2] WG-LES-010: Leakage control: induction uses only outcomes observed before the run time and features of the decision-time context, never present-day state. A test injects a future-dated outcome and asserts it is e

- **Source:** `wisdom-graph-requirements.md:722-722` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-010 | Leakage control: induction uses only outcomes observed before the run time and features of the decision-time context, never present-day state. A test injects a future-dated outcome and asserts it is excluded (same discipline as GN-005).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-LES-010 | Leakage control: induction uses only outcomes observed before the run time and features of the decision-time context, never present-day state. A test injects a future-dated outcome and asserts it is excluded (same discipline as GN-005).»
- [ ] Leakage control: induction uses only outcomes observed before the run time and features of the decision-time context, never present-day state. A test injects a future-dated outcome and asserts it is excluded (same discipline as GN-005).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-011 [P2] WG-LES-011: Every lesson has GET /wisdom/lessons/{id} with scope, exclusions, statistics, supporting and contradicting decisions (paginated), freshness history, versions, approvals and the induction run; GET /wis

- **Source:** `wisdom-graph-requirements.md:723-723` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-011 | Every lesson has `GET /wisdom/lessons/{id}` with scope, exclusions, statistics, supporting and contradicting decisions (paginated), freshness history, versions, approvals and the induction run; `GET /wisdom/lessons?state&decision_type&domain`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-LES-011 | Every lesson has GET /wisdom/lessons/{id} with scope, exclusions, statistics, supporting and contradicting decisions (paginated), freshness history, versions, approvals and the induction run; GET /wisdom/lessons?state&decision_type&domain.»
- [ ] Every lesson has GET /wisdom/lessons/{id} with scope, exclusions, statistics, supporting and contradicting decisions (paginated), freshness history, versions, approvals and the induction run; GET /wisdom/lessons?state&decision_type&domain.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-013 [P2] WG-LES-013: Lesson statements are human-readable and always include n, the rate, the baseline and the exclusions, e.g., "Deployments of criticality-5 services on Fridays were rolled back in 31% of 142 cases, vers

- **Source:** `wisdom-graph-requirements.md:725-725` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-013 | Lesson statements are human-readable and always include n, the rate, the baseline and the exclusions, e.g., "Deployments of criticality-5 services on Fridays were rolled back in 31% of 142 cases, versus 7% otherwise; does not apply when a canary stage is used."
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-LES-013 | Lesson statements are human-readable and always include n, the rate, the baseline and the exclusions, e.g., "Deployments of criticality-5 services on Fridays were rolled back in 31% of 142 cases, versus 7% otherwise; does not apply when a canary stage is used."»
- [ ] Lesson statements are human-readable and always include n, the rate, the baseline and the exclusions, e.g., "Deployments of criticality-5 services on Fridays were rolled back in 31% of 142 cases, versus 7% otherwise; does not apply when a canary stage is used."
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-LES-014 [P2] WG-LES-014: Lesson calibration metric kgfwglessonbrier (Brier score of lesson-predicted success probability against subsequent outcomes in scope, per decision type) is reported; a lesson whose own Brier over its 

- **Source:** `wisdom-graph-requirements.md:726-726` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-LES-014 | Lesson calibration metric `kgf_wg_lesson_brier` (Brier score of lesson-predicted success probability against subsequent outcomes in scope, per decision type) is reported; a lesson whose own Brier over its last 50 in-scope outcomes exceeds the baseline Brier is set `STALE` with reason `UNCALIBRATED`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-LES-014' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-LES-014') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-LES-014 | Lesson calibration metric kgf_wg_lesson_brier (Brier score of lesson-predicted success probability against subsequent outcomes in scope, per decision type) is reported; a lesson whose own Brier over its last 50 in-scope outcomes exceeds the baseline Brier is set STALE with reason UNCALIBRATED.»
- [ ] Lesson calibration metric kgf_wg_lesson_brier (Brier score of lesson-predicted success probability against subsequent outcomes in scope, per decision type) is reported; a lesson whose own Brier over its last 50 in-scope outcomes exceeds the baseline Brier is set STALE with reason UNCALIBRATED.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-MEM-001 [P2] WG-MEM-001: wisdom-curator implements W12 exactly; every critic run is stored (GET /wisdom/critic/runs, GET /wisdom/critic/runs/{id}) with Q values, guarded metrics and the decision

- **Source:** `wisdom-graph-requirements.md:928-928` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-MEM-001 | `wisdom-curator` implements W12 exactly; every critic run is stored (`GET /wisdom/critic/runs`, `GET /wisdom/critic/runs/{id}`) with Q values, guarded metrics and the decision.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-MEM-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-MEM-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-MEM-001 | wisdom-curator implements W12 exactly; every critic run is stored (GET /wisdom/critic/runs, GET /wisdom/critic/runs/{id}) with Q values, guarded metrics and the decision.»
- [ ] wisdom-curator implements W12 exactly; every critic run is stored (GET /wisdom/critic/runs, GET /wisdom/critic/runs/{id}) with Q values, guarded metrics and the decision.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-MEM-002 [P2] WG-MEM-002: No derived-layer change reaches production without a passing critic run, except the first fingerprint version, which is established by the precedent benchmark (WG-PRE-008)

- **Source:** `wisdom-graph-requirements.md:929-929` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-MEM-002 | No derived-layer change reaches production without a passing critic run, except the first fingerprint version, which is established by the precedent benchmark (WG-PRE-008).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-MEM-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-MEM-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-MEM-002 | No derived-layer change reaches production without a passing critic run, except the first fingerprint version, which is established by the precedent benchmark (WG-PRE-008).»
- [ ] No derived-layer change reaches production without a passing critic run, except the first fingerprint version, which is established by the precedent benchmark (WG-PRE-008).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-MEM-003 [P2] WG-MEM-003: Archetypes appear in precedent results as a single entry "N similar decisions (archetype)" with outcome rate and a drill-down; a toggle returns raw members instead

- **Source:** `wisdom-graph-requirements.md:930-930` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-MEM-003 | Archetypes appear in precedent results as a single entry "N similar decisions (archetype)" with outcome rate and a drill-down; a toggle returns raw members instead.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-MEM-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-MEM-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-MEM-003 | Archetypes appear in precedent results as a single entry "N similar decisions (archetype)" with outcome rate and a drill-down; a toggle returns raw members instead.»
- [ ] Archetypes appear in precedent results as a single entry "N similar decisions (archetype)" with outcome rate and a drill-down; a toggle returns raw members instead.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-MEM-004 [P2] WG-MEM-004: Pruning never deletes source records; a test seeds 10,000 traces, runs pruning and asserts all traces, contexts and outcomes remain byte-identical (canonical digests)

- **Source:** `wisdom-graph-requirements.md:931-931` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-MEM-004 | Pruning never deletes source records; a test seeds 10,000 traces, runs pruning and asserts all traces, contexts and outcomes remain byte-identical (canonical digests).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-MEM-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-MEM-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-MEM-004 | Pruning never deletes source records; a test seeds 10,000 traces, runs pruning and asserts all traces, contexts and outcomes remain byte-identical (canonical digests).»
- [ ] Pruning never deletes source records; a test seeds 10,000 traces, runs pruning and asserts all traces, contexts and outcomes remain byte-identical (canonical digests).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-MEM-007 [P2] WG-MEM-007: Wisdom memory for agents: agent memory consolidation (REQ-MET-001) may include lesson statements only as PREDICTED-status items with their n, rate, baseline and exclusions, and refreshes them when the

- **Source:** `wisdom-graph-requirements.md:934-934` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-MEM-007 | Wisdom memory for agents: agent memory consolidation (`REQ-MET-001`) may include lesson statements only as `PREDICTED`-status items with their n, rate, baseline and exclusions, and refreshes them when the lesson changes state (a `STALE` lesson is removed from agent memory on its next refresh).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-MEM-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-MEM-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-MEM-007 | Wisdom memory for agents: agent memory consolidation (REQ-MET-001) may include lesson statements only as PREDICTED-status items with their n, rate, baseline and exclusions, and refreshes them when the lesson changes state (a STALE lesson is removed from agent memory on its next refresh).»
- [ ] Wisdom memory for agents: agent memory consolidation (REQ-MET-001) may include lesson statements only as PREDICTED-status items with their n, rate, baseline and exclusions, and refreshes them when the lesson changes state (a STALE lesson is removed from agent memory on its next refresh).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-MET-001 [P2] WG-MET-001: wisdom-metrics-service computes every metric above hourly, stores daily snapshots for ≥ 400 days and exposes them on /metrics and GET /wisdom/metrics?from&to&decisiontype&domain

- **Source:** `wisdom-graph-requirements.md:1022-1022` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-MET-001 | `wisdom-metrics-service` computes every metric above hourly, stores daily snapshots for ≥ 400 days and exposes them on `/metrics` and `GET /wisdom/metrics?from&to&decision_type&domain`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-MET-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-MET-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-MET-001 | wisdom-metrics-service computes every metric above hourly, stores daily snapshots for ≥ 400 days and exposes them on /metrics and GET /wisdom/metrics?from&to&decision_type&domain.»
- [ ] wisdom-metrics-service computes every metric above hourly, stores daily snapshots for ≥ 400 days and exposes them on /metrics and GET /wisdom/metrics?from&to&decision_type&domain.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-MET-002 [P2] WG-MET-002: Decision-quality uplift: for decision types with wisdom.counselmode = ENFORCE, a holdout share wisdom.counselholdout (default 0.05; 0 disables) of eligible ADVISE-level decisions receives counsel comp

- **Source:** `wisdom-graph-requirements.md:1023-1023` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-MET-002 | Decision-quality uplift: for decision types with `wisdom.counsel_mode = ENFORCE`, a holdout share `wisdom.counsel_holdout` (default 0.05; 0 disables) of eligible `ADVISE`-level decisions receives counsel computed but not shown (shadow). Uplift = success rate (shown) − success rate (holdout), with a 95% bootstrap CI (1,000 resamples, seed 20261018). Holdout never applies to `REQUIRE_ACK` or `ESCALATE` counsel (safety controls are never withheld).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-MET-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-MET-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-MET-002 | Decision-quality uplift: for decision types with wisdom.counsel_mode = ENFORCE, a holdout share wisdom.counsel_holdout (default 0.05; 0 disables) of eligible ADVISE-level decisions receives counsel computed but not shown (shadow). Uplift = success rate (shown) − success rate (holdout), with a 95% bootstrap CI (1,000 resamples, seed 20261018). Holdout never applies »
- [ ] Decision-quality uplift: for decision types with wisdom.counsel_mode = ENFORCE, a holdout share wisdom.counsel_holdout (default 0.05; 0 disables) of eligible ADVISE-level decisions receives counsel computed but not shown (shadow). Uplift = success rate (shown) − success rate (holdout), with a 95% bootstrap CI (1,000 resamples, seed 20261018). Holdout never applies to REQUIRE_ACK or ESCALATE counse
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-MET-003 [P2] WG-MET-003: Replay-based uplift for tenants without live holdout: Q from W12 step 3 on the latest replay benchmark, reported as kgfwgdecisionqualityuplift{method="replay"}

- **Source:** `wisdom-graph-requirements.md:1024-1024` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-MET-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-MET-003 | Replay-based uplift for tenants without live holdout: Q from W12 step 3 on the latest replay benchmark, reported as `kgf_wg_decision_quality_uplift{method="replay"}`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-MET-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-MET-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-MET-003

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-MET-003 | Replay-based uplift for tenants without live holdout: Q from W12 step 3 on the latest replay benchmark, reported as kgf_wg_decision_quality_uplift{method="replay"}.»
- [ ] Replay-based uplift for tenants without live holdout: Q from W12 step 3 on the latest replay benchmark, reported as kgf_wg_decision_quality_uplift{method="replay"}.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-MET-005 [P2] WG-MET-005: The Wisdom discipline is added to the IP discipline registry (REQ-DSC-001) as entry wisdom with the canonical definition "The practice of recording how an organisation decides, learning from what its 

- **Source:** `wisdom-graph-requirements.md:1026-1026` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-MET-005 | The Wisdom discipline is added to the IP discipline registry (`REQ-DSC-001`) as entry `wisdom` with the canonical definition "The practice of recording how an organisation decides, learning from what its decisions led to, and bringing that experience to the next decision with honest limits.", metrics of this section, processes of §24 and screen 26.14. The owner may change the wording through configuration.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-MET-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-MET-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-MET-005 | The Wisdom discipline is added to the IP discipline registry (REQ-DSC-001) as entry wisdom with the canonical definition "The practice of recording how an organisation decides, learning from what its decisions led to, and bringing that experience to the next decision with honest limits.", metrics of this section, processes of §24 and screen 26.14. The owner may cha»
- [ ] The Wisdom discipline is added to the IP discipline registry (REQ-DSC-001) as entry wisdom with the canonical definition "The practice of recording how an organisation decides, learning from what its decisions led to, and bringing that experience to the next decision with honest limits.", metrics of this section, processes of §24 and screen 26.14. The owner may change the wording through configura
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-MET-006 [P2] WG-MET-006: Dashboard 26.14 shows every metric over time by decision type, domain and agent class, and the Wisdom Index with met and unmet criteria linked to the screens or settings that fix them

- **Source:** `wisdom-graph-requirements.md:1027-1027` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-MET-006 | Dashboard 26.14 shows every metric over time by decision type, domain and agent class, and the Wisdom Index with met and unmet criteria linked to the screens or settings that fix them.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-MET-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-MET-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-MET-006 | Dashboard 26.14 shows every metric over time by decision type, domain and agent class, and the Wisdom Index with met and unmet criteria linked to the screens or settings that fix them.»
- [ ] Dashboard 26.14 shows every metric over time by decision type, domain and agent class, and the Wisdom Index with met and unmet criteria linked to the screens or settings that fix them.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OBS-001 [P2] WG-OBS-001: GET /wisdom/decisions/{id}/why returns, in one response: the situation, decision-time context summary, options, chosen option, rationale with statuses, policies and results, exceptions with justificat

- **Source:** `wisdom-graph-requirements.md:942-942` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OBS-001 | `GET /wisdom/decisions/{id}/why` returns, in one response: the situation, decision-time context summary, options, chosen option, rationale with statuses, policies and results, exceptions with justifications, approvals and escalations with approvers, precedents shown and cited, counsel and acknowledgements, values at stake, the action and its ASPEII certificate/receipt ids when present, and the outcomes with attribution.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OBS-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OBS-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OBS-001 | GET /wisdom/decisions/{id}/why returns, in one response: the situation, decision-time context summary, options, chosen option, rationale with statuses, policies and results, exceptions with justifications, approvals and escalations with approvers, precedents shown and cited, counsel and acknowledgements, values at stake, the action and its ASPEII certificate/receip»
- [ ] GET /wisdom/decisions/{id}/why returns, in one response: the situation, decision-time context summary, options, chosen option, rationale with statuses, policies and results, exceptions with justifications, approvals and escalations with approvers, precedents shown and cited, counsel and acknowledgements, values at stake, the action and its ASPEII certificate/receipt ids when present, and the outco
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OBS-002 [P2] WG-OBS-002: GET /wisdom/entities/{id}/decisions?from&to lists decisions about an entity in event-clock order (answers "what have we decided about X and why")

- **Source:** `wisdom-graph-requirements.md:943-943` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OBS-002 | `GET /wisdom/entities/{id}/decisions?from&to` lists decisions about an entity in event-clock order (answers "what have we decided about X and why").
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OBS-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OBS-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OBS-002 | GET /wisdom/entities/{id}/decisions?from&to lists decisions about an entity in event-clock order (answers "what have we decided about X and why").»
- [ ] GET /wisdom/entities/{id}/decisions?from&to lists decisions about an entity in event-clock order (answers "what have we decided about X and why").
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OBS-003 [P2] WG-OBS-003: Agent decision observability: per agent identity, decision type and week: decisions, escalations, repeat-mistake escalations, acknowledgements, overrides of counsel, outcome success rate, confidence c

- **Source:** `wisdom-graph-requirements.md:944-944` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OBS-003 | Agent decision observability: per agent identity, decision type and week: decisions, escalations, repeat-mistake escalations, acknowledgements, overrides of counsel, outcome success rate, confidence capture, calibration. `GET /wisdom/agents/{id}/decision-stats`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OBS-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OBS-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OBS-003 | Agent decision observability: per agent identity, decision type and week: decisions, escalations, repeat-mistake escalations, acknowledgements, overrides of counsel, outcome success rate, confidence capture, calibration. GET /wisdom/agents/{id}/decision-stats.»
- [ ] Agent decision observability: per agent identity, decision type and week: decisions, escalations, repeat-mistake escalations, acknowledgements, overrides of counsel, outcome success rate, confidence capture, calibration. GET /wisdom/agents/{id}/decision-stats.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OBS-004 [P2] WG-OBS-004: Replay and reconsider (WG-CTX-007/008) are available from the UI decision view and the API; replay results are stored and linked to the trace

- **Source:** `wisdom-graph-requirements.md:945-945` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OBS-004 | Replay and reconsider (WG-CTX-007/008) are available from the UI decision view and the API; replay results are stored and linked to the trace.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OBS-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OBS-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OBS-004 | Replay and reconsider (WG-CTX-007/008) are available from the UI decision view and the API; replay results are stored and linked to the trace.»
- [ ] Replay and reconsider (WG-CTX-007/008) are available from the UI decision view and the API; replay results are stored and linked to the trace.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OBS-005 [P2] WG-OBS-005: Every Wisdom state change writes an audit event (WG-PLT-006); GET /wisdom/decisions/{id}/audit lists them; the IP audit chain verification (GET /audit/verify-chain) covers them

- **Source:** `wisdom-graph-requirements.md:946-946` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OBS-005 | Every Wisdom state change writes an audit event (WG-PLT-006); `GET /wisdom/decisions/{id}/audit` lists them; the IP audit chain verification (`GET /audit/verify-chain`) covers them.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OBS-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OBS-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OBS-005 | Every Wisdom state change writes an audit event (WG-PLT-006); GET /wisdom/decisions/{id}/audit lists them; the IP audit chain verification (GET /audit/verify-chain) covers them.»
- [ ] Every Wisdom state change writes an audit event (WG-PLT-006); GET /wisdom/decisions/{id}/audit lists them; the IP audit chain verification (GET /audit/verify-chain) covers them.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OBS-007 [P2] WG-OBS-007: Debug view for failed decisions: for a decision with a failed outcome, the view shows which counsel elements were present (precedents with failure, applicable lessons, novelty), whether they were ackn

- **Source:** `wisdom-graph-requirements.md:948-948` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OBS-007 | Debug view for failed decisions: for a decision with a failed outcome, the view shows which counsel elements were present (precedents with failure, applicable lessons, novelty), whether they were acknowledged, and what counsel would say today (WG-CTX-008).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OBS-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OBS-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OBS-007 | Debug view for failed decisions: for a decision with a failed outcome, the view shows which counsel elements were present (precedents with failure, applicable lessons, novelty), whether they were acknowledged, and what counsel would say today (WG-CTX-008).»
- [ ] Debug view for failed decisions: for a decision with a failed outcome, the view shows which counsel elements were present (precedents with failure, applicable lessons, novelty), whether they were acknowledged, and what counsel would say today (WG-CTX-008).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OBS-008 [P2] WG-OBS-008: Performance: why p95 < 400 ms; entity decision list p95 < 300 ms for ≤ 5,000 decisions per entity

- **Source:** `wisdom-graph-requirements.md:949-949` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OBS-008 | Performance: `why` p95 < 400 ms; entity decision list p95 < 300 ms for ≤ 5,000 decisions per entity.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OBS-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OBS-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OBS-008 | Performance: why p95 < 400 ms; entity decision list p95 < 300 ms for ≤ 5,000 decisions per entity.»
- [ ] Performance: why p95 < 400 ms; entity decision list p95 < 300 ms for ≤ 5,000 decisions per entity.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-ONT-002 [P2] WG-ONT-002: Every Wisdom record node is linked (:Warrant)-[:JUSTIFIES]->(record) (REQ-WAR-013). Records without a warrant are rejected with WSDUNWARRANTED

- **Source:** `wisdom-graph-requirements.md:292-292` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-ONT-002 | Every Wisdom record node is linked `(:Warrant)-[:JUSTIFIES]->(record)` (REQ-WAR-013). Records without a warrant are rejected with `WSD_UNWARRANTED`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-ONT-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-ONT-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-ONT-002 | Every Wisdom record node is linked (:Warrant)-[:JUSTIFIES]->(record) (REQ-WAR-013). Records without a warrant are rejected with WSD_UNWARRANTED.»
- [ ] Every Wisdom record node is linked (:Warrant)-[:JUSTIFIES]->(record) (REQ-WAR-013). Records without a warrant are rejected with WSD_UNWARRANTED.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-ONT-003 [P2] WG-ONT-003: Wisdom records are append-only. A correction creates a new record with a SUPERSEDES edge; the old record stays readable for audit and replay. The only physical deletion is retention/purge (WG-SEC-005)

- **Source:** `wisdom-graph-requirements.md:293-293` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-ONT-003 | Wisdom records are append-only. A correction creates a new record with a `SUPERSEDES` edge; the old record stays readable for audit and replay. The only physical deletion is retention/purge (WG-SEC-005).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-ONT-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-ONT-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-ONT-003 | Wisdom records are append-only. A correction creates a new record with a SUPERSEDES edge; the old record stays readable for audit and replay. The only physical deletion is retention/purge (WG-SEC-005).»
- [ ] Wisdom records are append-only. A correction creates a new record with a SUPERSEDES edge; the old record stays readable for audit and replay. The only physical deletion is retention/purge (WG-SEC-005).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-ONT-004 [P2] WG-ONT-004: The JSON Schemas of §5 are stored as schemas/wisdom/.schema.json (one file per record type) and typed models are generated from them for every backend language and the front-end. Validation failures r

- **Source:** `wisdom-graph-requirements.md:294-294` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-ONT-004 | The JSON Schemas of §5 are stored as `schemas/wisdom/*.schema.json` (one file per record type) and typed models are generated from them for every backend language and the front-end. Validation failures return `WSD_SCHEMA_INVALID` with the JSON pointer of the first failure.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-ONT-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-ONT-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-ONT-004 | The JSON Schemas of §5 are stored as schemas/wisdom/*.schema.json (one file per record type) and typed models are generated from them for every backend language and the front-end. Validation failures return WSD_SCHEMA_INVALID with the JSON pointer of the first failure.»
- [ ] The JSON Schemas of §5 are stored as schemas/wisdom/*.schema.json (one file per record type) and typed models are generated from them for every backend language and the front-end. Validation failures return WSD_SCHEMA_INVALID with the JSON pointer of the first failure.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-ONT-005 [P2] WG-ONT-005: Each tenant declares its decision types as subtypes of Decision with: decisiontype, owning domain (kgf:domain), default action class, at least one OutcomeSpec, and the situation features to extract (§

- **Source:** `wisdom-graph-requirements.md:295-295` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-ONT-005 | Each tenant declares its decision types as subtypes of `Decision` with: `decision_type`, owning domain (`kgf:domain`), default action class, at least one `OutcomeSpec`, and the situation features to extract (§9.1). A decision of an undeclared type is stored with `decision_type = "UNCLASSIFIED"` and appears in the steward queue for classification.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-ONT-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-ONT-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-ONT-005 | Each tenant declares its decision types as subtypes of Decision with: decision_type, owning domain (kgf:domain), default action class, at least one OutcomeSpec, and the situation features to extract (§9.1). A decision of an undeclared type is stored with decision_type = "UNCLASSIFIED" and appears in the steward queue for classification.»
- [ ] Each tenant declares its decision types as subtypes of Decision with: decision_type, owning domain (kgf:domain), default action class, at least one OutcomeSpec, and the situation features to extract (§9.1). A decision of an undeclared type is stored with decision_type = "UNCLASSIFIED" and appears in the steward queue for classification.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-ONT-006 [P2] WG-ONT-006: Wisdom record types are added to the meaning-migration term dependency graph (REQ-MMG-001..003) so renaming an ontology term used in a situation pattern, lesson scope or trade-off rule produces rewrit

- **Source:** `wisdom-graph-requirements.md:296-296` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-ONT-006 | Wisdom record types are added to the meaning-migration term dependency graph (`REQ-MMG-001..003`) so renaming an ontology term used in a situation pattern, lesson scope or trade-off rule produces rewrite proposals in a meaning release.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-ONT-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-ONT-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-ONT-006 | Wisdom record types are added to the meaning-migration term dependency graph (REQ-MMG-001..003) so renaming an ontology term used in a situation pattern, lesson scope or trade-off rule produces rewrite proposals in a meaning release.»
- [ ] Wisdom record types are added to the meaning-migration term dependency graph (REQ-MMG-001..003) so renaming an ontology term used in a situation pattern, lesson scope or trade-off rule produces rewrite proposals in a meaning release.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OUT-001 [P2] WG-OUT-001: Each declared decision type has ≥ 1 approved OutcomeSpec (§5.3). Specs are versioned; changing a spec never rewrites past outcomes, which keep specversion

- **Source:** `wisdom-graph-requirements.md:648-648` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OUT-001 | Each declared decision type has ≥ 1 approved `OutcomeSpec` (§5.3). Specs are versioned; changing a spec never rewrites past outcomes, which keep `spec_version`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OUT-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OUT-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OUT-001 | Each declared decision type has ≥ 1 approved OutcomeSpec (§5.3). Specs are versioned; changing a spec never rewrites past outcomes, which keep spec_version.»
- [ ] Each declared decision type has ≥ 1 approved OutcomeSpec (§5.3). Specs are versioned; changing a spec never rewrites past outcomes, which keep spec_version.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OUT-002 [P2] WG-OUT-002: outcome-service schedules an observation for every committed decision at committedat + horizon (and at wisdom.outcomeearlychecks intermediate points, default none), runs the spec's observer, and recor

- **Source:** `wisdom-graph-requirements.md:649-649` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OUT-002 | `outcome-service` schedules an observation for every committed decision at `committed_at + horizon` (and at `wisdom.outcome_early_checks` intermediate points, default none), runs the spec's observer, and records an `Outcome` with an `OBSERVED` warrant (observer class OBSERVER) and `success` evaluated by the predicate.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OUT-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OUT-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OUT-002 | outcome-service schedules an observation for every committed decision at committed_at + horizon (and at wisdom.outcome_early_checks intermediate points, default none), runs the spec's observer, and records an Outcome with an OBSERVED warrant (observer class OBSERVER) and success evaluated by the predicate.»
- [ ] outcome-service schedules an observation for every committed decision at committed_at + horizon (and at wisdom.outcome_early_checks intermediate points, default none), runs the spec's observer, and records an Outcome with an OBSERVED warrant (observer class OBSERVER) and success evaluated by the predicate.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OUT-004 [P2] WG-OUT-004: Outcomes that cannot be observed (source unavailable, entity deleted, access revoked) are recorded NOTOBSERVABLE with a reason and retried per wisdom.outcomeretry (default 3 attempts, 24 h apart). The

- **Source:** `wisdom-graph-requirements.md:651-651` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OUT-004 | Outcomes that cannot be observed (source unavailable, entity deleted, access revoked) are recorded `NOT_OBSERVABLE` with a reason and retried per `wisdom.outcome_retry` (default 3 attempts, 24 h apart). They never count as success or failure.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OUT-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OUT-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OUT-004 | Outcomes that cannot be observed (source unavailable, entity deleted, access revoked) are recorded NOT_OBSERVABLE with a reason and retried per wisdom.outcome_retry (default 3 attempts, 24 h apart). They never count as success or failure.»
- [ ] Outcomes that cannot be observed (source unavailable, entity deleted, access revoked) are recorded NOT_OBSERVABLE with a reason and retried per wisdom.outcome_retry (default 3 attempts, 24 h apart). They never count as success or failure.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OUT-005 [P2] WG-OUT-005: outcome-service implements W4 exactly; attribution weights are stored on RESULTEDIN edges. Lessons and calibration use an outcome for a decision only if its weight ≥ wisdom.attributionuseweight (defau

- **Source:** `wisdom-graph-requirements.md:652-652` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-OUT-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OUT-005 | `outcome-service` implements W4 exactly; attribution weights are stored on `RESULTED_IN` edges. Lessons and calibration use an outcome for a decision only if its weight ≥ `wisdom.attribution_use_weight` (default 0.5) and it is not `confounded`, unless a steward attested the attribution.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OUT-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OUT-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-OUT-005

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OUT-005 | outcome-service implements W4 exactly; attribution weights are stored on RESULTED_IN edges. Lessons and calibration use an outcome for a decision only if its weight ≥ wisdom.attribution_use_weight (default 0.5) and it is not confounded, unless a steward attested the attribution.»
- [ ] outcome-service implements W4 exactly; attribution weights are stored on RESULTED_IN edges. Lessons and calibration use an outcome for a decision only if its weight ≥ wisdom.attribution_use_weight (default 0.5) and it is not confounded, unless a steward attested the attribution.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OUT-006 [P2] WG-OUT-006: Delayed and revised outcomes: a later observation for the same decision and spec creates a new Outcome with SUPERSEDES; lessons and calibration recompute incrementally (WG-LES-008, WG-CAL-004)

- **Source:** `wisdom-graph-requirements.md:653-653` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OUT-006 | Delayed and revised outcomes: a later observation for the same decision and spec creates a new `Outcome` with `SUPERSEDES`; lessons and calibration recompute incrementally (WG-LES-008, WG-CAL-004).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OUT-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OUT-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OUT-006 | Delayed and revised outcomes: a later observation for the same decision and spec creates a new Outcome with SUPERSEDES; lessons and calibration recompute incrementally (WG-LES-008, WG-CAL-004).»
- [ ] Delayed and revised outcomes: a later observation for the same decision and spec creates a new Outcome with SUPERSEDES; lessons and calibration recompute incrementally (WG-LES-008, WG-CAL-004).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OUT-007 [P2] WG-OUT-007: Outcome-linked commitments and dissent: when a decision had a deliberation (REQ-DIS-) with a minority report, its outcome is shown to the decision owner with a prompt to record vindication (REQ-DIS-00

- **Source:** `wisdom-graph-requirements.md:654-654` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OUT-007 | Outcome-linked commitments and dissent: when a decision had a deliberation (`REQ-DIS-*`) with a minority report, its outcome is shown to the decision owner with a prompt to record vindication (`REQ-DIS-007`); when a decision fulfilled a commitment (`REQ-CMT-007`), the commitment id is linked.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OUT-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OUT-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OUT-007 | Outcome-linked commitments and dissent: when a decision had a deliberation (REQ-DIS-*) with a minority report, its outcome is shown to the decision owner with a prompt to record vindication (REQ-DIS-007); when a decision fulfilled a commitment (REQ-CMT-007), the commitment id is linked.»
- [ ] Outcome-linked commitments and dissent: when a decision had a deliberation (REQ-DIS-*) with a minority report, its outcome is shown to the decision owner with a prompt to record vindication (REQ-DIS-007); when a decision fulfilled a commitment (REQ-CMT-007), the commitment id is linked.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OUT-009 [P2] WG-OUT-009: Acceptance on the seeded tenant: for the 600 seeded change→affected pairs (IP seed §4.2) and the Wisdom seed decisions with planted outcomes, attribution assigns the planted decision the highest weigh

- **Source:** `wisdom-graph-requirements.md:656-656` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 1 other site(s): see duplicate task DUP-WG-OUT-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OUT-009 | Acceptance on the seeded tenant: for the 600 seeded change→affected pairs (IP seed §4.2) and the Wisdom seed decisions with planted outcomes, attribution assigns the planted decision the highest weight in ≥ 85% of cases and flags ≥ 90% of the planted confounded cases.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OUT-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OUT-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-WG-OUT-009

**Acceptance criteria**
- [ ] on the seeded tenant: for the 600 seeded change→affected pairs (IP seed §4.2) and the Wisdom seed decisions with planted outcomes, attribution assigns the planted decision the highest weight in ≥ 85% of cases and flags ≥ 90% of the planted confounded cases
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-OUT-010 [P2] WG-OUT-010: Outcome coverage metric kgfwgoutcomecoverageratio = decisions past their horizon with an OBSERVED/ATTESTED outcome ÷ decisions past their horizon, per decision type; target ≥ 0.9

- **Source:** `wisdom-graph-requirements.md:657-657` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-OUT-010 | Outcome coverage metric `kgf_wg_outcome_coverage_ratio` = decisions past their horizon with an `OBSERVED`/`ATTESTED` outcome ÷ decisions past their horizon, per decision type; target ≥ 0.9.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-OUT-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-OUT-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-OUT-010 | Outcome coverage metric kgf_wg_outcome_coverage_ratio = decisions past their horizon with an OBSERVED/ATTESTED outcome ÷ decisions past their horizon, per decision type; target ≥ 0.9.»
- [ ] Outcome coverage metric kgf_wg_outcome_coverage_ratio = decisions past their horizon with an OBSERVED/ATTESTED outcome ÷ decisions past their horizon, per decision type; target ≥ 0.9.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PLT-002 [P2] WG-PLT-002: Every capability is behind a tenant-scoped feature flag listed in §27.1, default off, switchable at runtime without restart, with the dependency checks of §27.1 (FLAGDEPENDENCY)

- **Source:** `wisdom-graph-requirements.md:169-169` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PLT-002 | Every capability is behind a tenant-scoped feature flag listed in §27.1, default **off**, switchable at runtime without restart, with the dependency checks of §27.1 (`FLAG_DEPENDENCY`).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PLT-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PLT-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PLT-002 | Every capability is behind a tenant-scoped feature flag listed in §27.1, default off, switchable at runtime without restart, with the dependency checks of §27.1 (FLAG_DEPENDENCY).»
- [ ] Every capability is behind a tenant-scoped feature flag listed in §27.1, default off, switchable at runtime without restart, with the dependency checks of §27.1 (FLAG_DEPENDENCY).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-WG-PLT-004 [P2] WG-PLT-004: Every graph read and write goes through KGF's graph abstraction layer (GraphPort in ip-requirements.md §4.2) and works on every graph database KGF supports. Database-specific code lives only in adapte

- **Source:** `wisdom-graph-requirements.md:171-171` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
WG-PLT-004 | Every graph read and write goes through KGF's graph abstraction layer (`GraphPort` in `ip-requirements.md` §4.2) and works on every graph database KGF supports. Database-specific code lives only in adapters.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'WG-PLT-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('WG-PLT-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «WG-PLT-004 | Every graph read and write goes through KGF's graph abstraction layer (GraphPort in ip-requirements.md §4.2) and works on every graph database KGF supports. Database-specific code lives only in adapters.»
- [ ] Every graph read and write goes through KGF's graph abstraction layer (GraphPort in ip-requirements.md §4.2) and works on every graph database KGF supports. Database-specific code lives only in adapters.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

