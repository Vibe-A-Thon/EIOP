# EPIC-KGR-UNTR-01: EOIP-engg-doc-pkg/KGR-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~372.0 h, priorities {'P1': 5, 'P2': 55}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-AC-05 [P1] AC-05: 12 layout algorithms available and switchable without data loss

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1036-1036` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-05 | 12 layout algorithms available and switchable without data loss | Graphify: 1, code2flow: 1
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-05 | 12 layout algorithms available and switchable without data loss | Graphify: 1, code2flow: 1»
- [ ] 12 layout algorithms available and switchable without data loss
- [ ] Graphify: 1, code2flow: 1
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-015 [P1] FR-KGR-015: Community Auto-Labeling

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:467-478` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-015: Community Auto-Labeling

Addresses a gap in all competitors except Graphify (which has basic community labeling).

- Automatically name detected communities based on the most prevalent entity types and shared properties within the cluster
- Labeling algorithm: extract top-3 most common vertex labels + top-3 most common property values (e.g., "Code: auth-service, API, security")
- Community labels displayed on convex hull overlays in the graph
- Community labels shown in the community filter dropdown
- Override: user can rename a community label (persisted in localStorage)
- Community summary card: click a hull to see member count, dominant types, key hub nodes, intra-community density
- **Surpasses Graphify** which labels communities but doesn't allow user overrides or show summary cards
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Community Auto-Labeling Addresses a gap in all competitors except Graphify (which has basic community labeling). - Automatically name detected communities based on the most prevalent entity types and shared properties within the cluster - Labeling algorithm: extract top-3 most common vertex labels + top-3 most common property values (e.g., "Code: auth-service, API, security") -
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-016 [P1] FR-KGR-016: PR / Change Impact Dashboard

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:479-491` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-016: PR / Change Impact Dashboard

Inspired by Graphify's PR dashboard (`graphify prs`) with community-based conflict detection.

- **PR list**: display open pull requests/merge requests with title, branch, author, status
- **Community overlap detection**: for each PR, identify which graph communities are touched by its changes
- **Conflict risk indicator**: when two or more PRs touch the same community, flag as potential conflict (HIGH: >50% overlap, MEDIUM: 20-50%, LOW: <20%)
- **Change heatmap**: overlay on the graph showing which nodes/edges are affected by each PR
- **PR comparison view**: select two PRs to see their blast radius overlap
- Data source: GitLab MR API / GitHub PR API via existing connectors
- Available as a dedicated dashboard accessible from the KGR lens toolbar
- **Surpasses Graphify** by providing visual overlap analysis (Graphify only lists PRs with community labels)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): PR / Change Impact Dashboard Inspired by Graphify's PR dashboard (graphify prs) with community-based conflict detection. - PR list: display open pull requests/merge requests with title, branch, author, status - Community overlap detection: for each PR, identify which graph communities are touched by its changes - Conflict risk indicator: when two or more PRs touch the same comm
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-029 [P1] FR-KGR-029: Engineering Disciplines (8 Patterns)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:666-684` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 9.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-029: Engineering Disciplines (8 Patterns)

The system SHALL implement 8 engineering discipline patterns that compose RAG, agents, and graph analysis into higher-order intelligence systems.

| # | Discipline | Purpose | Use Case |
|---|---|---|---|
| 1 | Loop Engineering | Iterative refinement cycles with convergence detection | Refining community detection thresholds, sensitivity tuning |
| 2 | Graph Engineering | Structured graph construction, optimization, and maintenance | Schema optimization, index recommendations, migration planning |
| 3 | Harness Engineering | Controlled execution environments with safety bounds | Sandboxed what-if simulations, rate limiting, circuit breakers |
| 4 | Memory Engineering | 5-tier memory system (short-term, working, long-term, episodic, semantic) | Agents that learn from prior analysis sessions |
| 5 | Context Engineering | Optimal context assembly within token budgets | Assembling relevant graph context for LLM queries |
| 6 | Prompt Engineering | Structured prompt construction with template library | Effective prompts for graph analysis, chain-of-thought reasoning |
| 7 | Graph-over-Loop Engineering | Graph traversal drives iteration control flow | Automated dependency chain analysis, root cause search |
| 8 | Loop-over-Graph Engineering | Iterative loops progressively refine graph understanding | Progressive intelligence that improves each pass |

- API: `POST /api/v1/engineering/{discipline}` for each pattern
- Composable: disciplines can be combined (e.g., Loop + Graph-over-Loop for multi-pass traversal)
- **Unique to KGR** — no competitor has formalized engineering discipline patterns
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-029' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-029') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] The system SHALL implement 8 engineering discipline patterns that compose RAG, agents, and graph analysis into higher-order intelligence systems.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-NFR-KGR-005 [P1] NFR-KGR-005: Security

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:732-740` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### NFR-KGR-005: Security
- No data leaves the browser except to the local API
- No external CDN dependencies in production
- Token-based API authentication for all data requests
- No telemetry (fixes Sourcegraph's data collection concerns)
- Annotations stored only in localStorage (never sent to API)

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'NFR-KGR-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('NFR-KGR-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] No data leaves the browser except to the local API - No external CDN dependencies in production - Token-based API authentication for all data requests - No telemetry (fixes Sourcegraph's data collection concerns) - Annotations stored only in localStorage (never sent to API)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-01 [P2] AC-01: User can switch between 10 graph types with appropriate visualization

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1032-1032` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-01 | User can switch between 10 graph types with appropriate visualization | Graphify: 1 type, Bloom: 1, Gephi: 1
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-01' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-01') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-01 | User can switch between 10 graph types with appropriate visualization | Graphify: 1 type, Bloom: 1, Gephi: 1»
- [ ] User can switch between 10 graph types with appropriate visualization
- [ ] Graphify: 1 type, Bloom: 1, Gephi: 1
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-02 [P2] AC-02: 8-tab inspector shows properties, relationships, impact, evidence, similarity, history, annotations, raw

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1033-1033` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-02 | 8-tab inspector shows properties, relationships, impact, evidence, similarity, history, annotations, raw | Graphify: properties only
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-02' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-02') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-02 | 8-tab inspector shows properties, relationships, impact, evidence, similarity, history, annotations, raw | Graphify: properties only»
- [ ] 8-tab inspector shows properties, relationships, impact, evidence, similarity, history, annotations, raw
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-03 [P2] AC-03: Blast radius renders concentric rings with depth/type breakdown and risk

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1034-1034` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-03 | Blast radius renders concentric rings with depth/type breakdown and risk | No competitor has this
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-03 | Blast radius renders concentric rings with depth/type breakdown and risk | No competitor has this»
- [ ] Blast radius renders concentric rings with depth/type breakdown and risk
- [ ] No competitor has this
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-04 [P2] AC-04: Centrality metrics computed and displayed as radar chart

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1035-1035` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-04 | Centrality metrics computed and displayed as radar chart | Gephi: desktop only, Bloom: GDS required
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-04 | Centrality metrics computed and displayed as radar chart | Gephi: desktop only, Bloom: GDS required»
- [ ] Centrality metrics computed and displayed as radar chart
- [ ] Gephi: desktop only, Bloom: GDS required
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-06 [P2] AC-06: Graph renders 1,000 nodes in < 2 seconds

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1037-1037` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-06 | Graph renders 1,000 nodes in < 2 seconds | Sourcetrail: crashes, code2flow: cluttered
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-06' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-06') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-06 | Graph renders 1,000 nodes in < 2 seconds | Sourcetrail: crashes, code2flow: cluttered»
- [ ] Graph renders 1,000 nodes in < 2 seconds
- [ ] Sourcetrail: crashes, code2flow: cluttered
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-07 [P2] AC-07: Progressive WebGL rendering handles 50,000 nodes

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1038-1038` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-07 | Progressive WebGL rendering handles 50,000 nodes | Graphify: 5K limit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-07' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-07') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-07 | Progressive WebGL rendering handles 50,000 nodes | Graphify: 5K limit»
- [ ] Progressive WebGL rendering handles 50,000 nodes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-08 [P2] AC-08: All existing EOIP lenses continue unchanged

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1039-1039` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-08 | All existing EOIP lenses continue unchanged | N/A
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-08' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-08') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-08 | All existing EOIP lenses continue unchanged | N/A»
- [ ] All existing EOIP lenses continue unchanged
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-09 [P2] AC-09: Export produces valid PNG, SVG, PDF, JSON-LD, GraphML, CSV, GEXF, Obsidian, Mermaid, Cypher

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1040-1040` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-09 | Export produces valid PNG, SVG, PDF, JSON-LD, GraphML, CSV, GEXF, Obsidian, Mermaid, Cypher | Graphify: HTML/JSON/GraphML/SVG/Obsidian/Mermaid/Cypher — KGR matches all + adds PDF/JSON-LD/GEXF
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-09' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-09') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-09 | Export produces valid PNG, SVG, PDF, JSON-LD, GraphML, CSV, GEXF, Obsidian, Mermaid, Cypher | Graphify: HTML/JSON/GraphML/SVG/Obsidian/Mermaid/Cypher — KGR matches all + adds PDF/JSON-LD/GEXF»
- [ ] Export produces valid PNG, SVG, PDF, JSON-LD, GraphML, CSV, GEXF, Obsidian, Mermaid, Cypher
- [ ] Graphify: HTML/JSON/GraphML/SVG/Obsidian/Mermaid/Cypher — KGR matches all + adds PDF/JSON-LD/GEXF
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-10 [P2] AC-10: 10-dimensional filter state persists across graph type switches

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1041-1041` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-10 | 10-dimensional filter state persists across graph type switches | Graphify: label only
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-10' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-10') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-10 | 10-dimensional filter state persists across graph type switches | Graphify: label only»
- [ ] 10-dimensional filter state persists across graph type switches
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-11 [P2] AC-11: Minimap, fisheye, semantic zoom all function

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1042-1042` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-11 | Minimap, fisheye, semantic zoom all function | No competitor bundles all three
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-11' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-11') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-11 | Minimap, fisheye, semantic zoom all function | No competitor bundles all three»
- [ ] Minimap, fisheye, semantic zoom all function
- [ ] No competitor bundles all three
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-12 [P2] AC-12: Full keyboard navigation without mouse

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1043-1043` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-12 | Full keyboard navigation without mouse | No competitor achieves full keyboard nav
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-12' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-12') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-12 | Full keyboard navigation without mouse | No competitor achieves full keyboard nav»
- [ ] Full keyboard navigation without mouse
- [ ] No competitor achieves full keyboard nav
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-13 [P2] AC-13: 166+ existing tests continue to pass

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1044-1044` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-13 | 166+ existing tests continue to pass | N/A
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-13' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-13') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-13 | 166+ existing tests continue to pass | N/A»
- [ ] 166+ existing tests continue to pass
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-14 [P2] AC-14: New components have > 80% test coverage

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1045-1045` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-14 | New components have > 80% test coverage | N/A
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-14' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-14') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-14 | New components have > 80% test coverage | N/A»
- [ ] New components have > 80% test coverage
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-15 [P2] AC-15: No external network requests in production

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1046-1046` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-15 | No external network requests in production | Fixes Sourcegraph, CodeSee, Graphistry
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-15' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-15') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-15 | No external network requests in production | Fixes Sourcegraph, CodeSee, Graphistry»
- [ ] No external network requests in production
- [ ] Fixes Sourcegraph, CodeSee, Graphistry
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-16 [P2] AC-16: Community detection clusters visible as hull overlays

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1047-1047` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-16 | Community detection clusters visible as hull overlays | Gephi: desktop only
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-16' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-16') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-16 | Community detection clusters visible as hull overlays | Gephi: desktop only»
- [ ] Community detection clusters visible as hull overlays
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-17 [P2] AC-17: WebSocket real-time updates with fade-in animation

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1048-1048` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-17 | WebSocket real-time updates with fade-in animation | Graphify: git hooks only
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-17' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-17') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-17 | WebSocket real-time updates with fade-in animation | Graphify: git hooks only»
- [ ] WebSocket real-time updates with fade-in animation
- [ ] Graphify: git hooks only
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-18 [P2] AC-18: Graph diff shows added/removed/modified entities

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1049-1049` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-18 | Graph diff shows added/removed/modified entities | No free competitor has this
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-18' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-18') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-18 | Graph diff shows added/removed/modified entities | No free competitor has this»
- [ ] Graph diff shows added/removed/modified entities
- [ ] No free competitor has this
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-19 [P2] AC-19: What-if simulation shows impact of entity removal

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1050-1050` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-19 | What-if simulation shows impact of entity removal | No competitor has this
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-19' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-19') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-19 | What-if simulation shows impact of entity removal | No competitor has this»
- [ ] What-if simulation shows impact of entity removal
- [ ] No competitor has this
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-20 [P2] AC-20: Annotations on nodes/edges persist and export with reports

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1051-1051` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-20 | Annotations on nodes/edges persist and export with reports | No free competitor has this
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-20' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-20') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-20 | Annotations on nodes/edges persist and export with reports | No free competitor has this»
- [ ] Annotations on nodes/edges persist and export with reports
- [ ] No free competitor has this
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-21 [P2] AC-21: Node group collapsing works with domain/type/community/custom grouping

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1052-1052` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-21 | Node group collapsing works with domain/type/community/custom grouping | yFiles (€9.2K), KeyLines (commercial), Linkurious (commercial) — KGR does it free
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-21' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-21') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-21 | Node group collapsing works with domain/type/community/custom grouping | yFiles (€9.2K), KeyLines (commercial), Linkurious (commercial) — KGR does it free»
- [ ] Node group collapsing works with domain/type/community/custom grouping
- [ ] yFiles (€9.2K), KeyLines (commercial), Linkurious (commercial) — KGR does it free
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-22 [P2] AC-22: Code + graph side-by-side view with synchronized navigation

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1053-1053` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-22 | Code + graph side-by-side view with synchronized navigation | Sourcetrail (discontinued, desktop, 4 langs) — KGR is browser-based, all languages
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-22' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-22') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-22 | Code + graph side-by-side view with synchronized navigation | Sourcetrail (discontinued, desktop, 4 langs) — KGR is browser-based, all languages»
- [ ] Code + graph side-by-side view with synchronized navigation
- [ ] Sourcetrail (discontinued, desktop, 4 langs) — KGR is browser-based, all languages
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-23 [P2] AC-23: Visual query builder produces valid QueryPlans without writing code

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1054-1054` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-23 | Visual query builder produces valid QueryPlans without writing code | Linkurious (commercial) — KGR does it free
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-23' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-23') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-23 | Visual query builder produces valid QueryPlans without writing code | Linkurious (commercial) — KGR does it free»
- [ ] Visual query builder produces valid QueryPlans without writing code
- [ ] Linkurious (commercial) — KGR does it free
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-24 [P2] AC-24: Dead code / orphaned entity detection with visual indicators

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1055-1055` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-24 | Dead code / orphaned entity detection with visual indicators | code2flow (4 langs, CLI only) — KGR covers all entity types
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-24' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-24') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-24 | Dead code / orphaned entity detection with visual indicators | code2flow (4 langs, CLI only) — KGR covers all entity types»
- [ ] Dead code / orphaned entity detection with visual indicators
- [ ] code2flow (4 langs, CLI only) — KGR covers all entity types
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-25 [P2] AC-25: Community auto-labeling with user override and summary cards

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1056-1056` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-25 | Community auto-labeling with user override and summary cards | Graphify (basic labeling only, no override)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-25' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-25') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-25 | Community auto-labeling with user override and summary cards | Graphify (basic labeling only, no override)»
- [ ] Community auto-labeling with user override and summary cards
- [ ] Graphify (basic labeling only, no override)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-26 [P2] AC-26: PR/change impact dashboard with community overlap detection

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1057-1057` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-26 | PR/change impact dashboard with community overlap detection | Graphify (list only, no visual overlap)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-26' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-26') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-26 | PR/change impact dashboard with community overlap detection | Graphify (list only, no visual overlap)»
- [ ] PR/change impact dashboard with community overlap detection
- [ ] Graphify (list only, no visual overlap)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-27 [P2] AC-27: 11+ export formats covering every competitor's export capability

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1058-1058` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-27 | 11+ export formats covering every competitor's export capability | Surpasses all: matches Graphify's 7 + adds PDF/JSON-LD/GEXF/clipboard
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-27' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-27') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-27 | 11+ export formats covering every competitor's export capability | Surpasses all: matches Graphify's 7 + adds PDF/JSON-LD/GEXF/clipboard»
- [ ] 11+ export formats covering every competitor's export capability
- [ ] Surpasses all: matches Graphify's 7 + adds PDF/JSON-LD/GEXF/clipboard
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-28 [P2] AC-28: AMBIGUOUS evidence status supported alongside DETERMINISTIC/INFERRED/MANUAL

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1059-1059` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-28 | AMBIGUOUS evidence status supported alongside DETERMINISTIC/INFERRED/MANUAL | Matches Graphify's 3-tier evidence (EXTRACTED/INFERRED/AMBIGUOUS)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-28' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-28') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-28 | AMBIGUOUS evidence status supported alongside DETERMINISTIC/INFERRED/MANUAL | Matches Graphify's 3-tier evidence (EXTRACTED/INFERRED/AMBIGUOUS)»
- [ ] AMBIGUOUS evidence status supported alongside DETERMINISTIC/INFERRED/MANUAL
- [ ] Matches Graphify's 3-tier evidence (EXTRACTED/INFERRED/AMBIGUOUS)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-29 [P2] AC-29: Geo-mode positions entities on map when location metadata available

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1060-1060` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-29 | Geo-mode positions entities on map when location metadata available | Linkurious, Ogma (commercial) — KGR does it free
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-29' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-29') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-29 | Geo-mode positions entities on map when location metadata available | Linkurious, Ogma (commercial) — KGR does it free»
- [ ] Geo-mode positions entities on map when location metadata available
- [ ] Linkurious, Ogma (commercial) — KGR does it free
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-30 [P2] AC-30: Semantic zoom shows 3 levels (cluster/entity/detail) with smooth transitions

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1061-1061` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-30 | Semantic zoom shows 3 levels (cluster/entity/detail) with smooth transitions | No free competitor has this
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-30' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-30') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-30 | Semantic zoom shows 3 levels (cluster/entity/detail) with smooth transitions | No free competitor has this»
- [ ] Semantic zoom shows 3 levels (cluster/entity/detail) with smooth transitions
- [ ] No free competitor has this
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-31 [P2] AC-31: Fisheye distortion provides 2x magnification at cursor with gradual falloff

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1062-1062` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-31 | Fisheye distortion provides 2x magnification at cursor with gradual falloff | yFiles (€9.2K) — KGR does it free
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-31' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-31') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-31 | Fisheye distortion provides 2x magnification at cursor with gradual falloff | yFiles (€9.2K) — KGR does it free»
- [ ] Fisheye distortion provides 2x magnification at cursor with gradual falloff
- [ ] yFiles (€9.2K) — KGR does it free
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-32 [P2] AC-32: Force-directed edge bundling declutters high-degree nodes

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1063-1063` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-32 | Force-directed edge bundling declutters high-degree nodes | yFiles (€9.2K) — KGR does it free
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-32' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-32') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-32 | Force-directed edge bundling declutters high-degree nodes | yFiles (€9.2K) — KGR does it free»
- [ ] Force-directed edge bundling declutters high-degree nodes
- [ ] yFiles (€9.2K) — KGR does it free
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-33 [P2] AC-33: Color-blind safe palette with 3 modes (deuteranopia/tritanopia/high-contrast)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1064-1064` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-33 | Color-blind safe palette with 3 modes (deuteranopia/tritanopia/high-contrast) | No competitor has 3 palette modes
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-33' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-33') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-33 | Color-blind safe palette with 3 modes (deuteranopia/tritanopia/high-contrast) | No competitor has 3 palette modes»
- [ ] Color-blind safe palette with 3 modes (deuteranopia/tritanopia/high-contrast)
- [ ] No competitor has 3 palette modes
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-34 [P2] AC-34: Self-contained interactive HTML export with search/filter/inspect

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1065-1065` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-34 | Self-contained interactive HTML export with search/filter/inspect | Graphify (basic zoom only) — KGR adds full interaction
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-34' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-34') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-34 | Self-contained interactive HTML export with search/filter/inspect | Graphify (basic zoom only) — KGR adds full interaction»
- [ ] Self-contained interactive HTML export with search/filter/inspect
- [ ] Graphify (basic zoom only) — KGR adds full interaction
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-35 [P2] AC-35: Automated graph report with 7 analysis sections

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1066-1066` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-35 | Automated graph report with 7 analysis sections | Graphify (basic topology) — KGR adds centrality, health, recommendations
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-35' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-35') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-35 | Automated graph report with 7 analysis sections | Graphify (basic topology) — KGR adds centrality, health, recommendations»
- [ ] Automated graph report with 7 analysis sections
- [ ] Graphify (basic topology) — KGR adds centrality, health, recommendations
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-36 [P2] AC-36: Hub exclusion filter with visual indicator of excluded nodes

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1067-1067` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-36 | Hub exclusion filter with visual indicator of excluded nodes | Graphify (flag only, no visual)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-36' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-36') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-36 | Hub exclusion filter with visual indicator of excluded nodes | Graphify (flag only, no visual)»
- [ ] Hub exclusion filter with visual indicator of excluded nodes
- [ ] Graphify (flag only, no visual)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-37 [P2] AC-37: Surprising connection detection with cross-domain and absence analysis

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1068-1068` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-37 | Surprising connection detection with cross-domain and absence analysis | Graphify (basic ranking only)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-37' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-37') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-37 | Surprising connection detection with cross-domain and absence analysis | Graphify (basic ranking only)»
- [ ] Surprising connection detection with cross-domain and absence analysis
- [ ] Graphify (basic ranking only)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-38 [P2] AC-38: Rule-based conditional styling with composable IF/THEN rules

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1069-1069` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-38 | Rule-based conditional styling with composable IF/THEN rules | Neo4j Bloom, Linkurious (both commercial) — KGR does it free
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-38' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-38') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-38 | Rule-based conditional styling with composable IF/THEN rules | Neo4j Bloom, Linkurious (both commercial) — KGR does it free»
- [ ] Rule-based conditional styling with composable IF/THEN rules
- [ ] Neo4j Bloom, Linkurious (both commercial) — KGR does it free
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-39 [P2] AC-39: Lasso and rectangle multi-selection for large graphs

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1070-1070` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-39 | Lasso and rectangle multi-selection for large graphs | KeyLines, yFiles (commercial) — KGR does it free
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-39' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-39') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-39 | Lasso and rectangle multi-selection for large graphs | KeyLines, yFiles (commercial) — KGR does it free»
- [ ] Lasso and rectangle multi-selection for large graphs
- [ ] KeyLines, yFiles (commercial) — KGR does it free
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-40 [P2] AC-40: URL deep linking encodes full graph state (filters, zoom, selection, layout)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1071-1071` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-40 | URL deep linking encodes full graph state (filters, zoom, selection, layout) | Neo4j Bloom (selection only) — KGR encodes full state
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-40' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-40') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-40 | URL deep linking encodes full graph state (filters, zoom, selection, layout) | Neo4j Bloom (selection only) — KGR encodes full state»
- [ ] URL deep linking encodes full graph state (filters, zoom, selection, layout)
- [ ] Neo4j Bloom (selection only) — KGR encodes full state
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-41 [P2] AC-41: Alternative table view provides WCAG-accessible data browsing

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1072-1072` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-41 | Alternative table view provides WCAG-accessible data browsing | No competitor has this
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-41' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-41') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-41 | Alternative table view provides WCAG-accessible data browsing | No competitor has this»
- [ ] Alternative table view provides WCAG-accessible data browsing
- [ ] No competitor has this
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-42 [P2] AC-42: Investigation playbooks guide multi-step analysis workflows

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1073-1073` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-42 | Investigation playbooks guide multi-step analysis workflows | Graphistry (GPU-only, commercial) — KGR does it free
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-42' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-42') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-42 | Investigation playbooks guide multi-step analysis workflows | Graphistry (GPU-only, commercial) — KGR does it free»
- [ ] Investigation playbooks guide multi-step analysis workflows
- [ ] Graphistry (GPU-only, commercial) — KGR does it free
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-43 [P2] AC-43: Cross-project graph merge with preview and undo

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1074-1074` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-43 | Cross-project graph merge with preview and undo | Graphify (multi-repo, no preview)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-43' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-43') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-43 | Cross-project graph merge with preview and undo | Graphify (multi-repo, no preview)»
- [ ] Cross-project graph merge with preview and undo
- [ ] Graphify (multi-repo, no preview)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-44 [P2] AC-44: 17 RAG patterns route queries to optimal retrieval strategy

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1075-1075` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-44 | 17 RAG patterns route queries to optimal retrieval strategy | No graph viz tool has RAG
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-44' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-44') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-44 | 17 RAG patterns route queries to optimal retrieval strategy | No graph viz tool has RAG»
- [ ] 17 RAG patterns route queries to optimal retrieval strategy
- [ ] No graph viz tool has RAG
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-45 [P2] AC-45: 40+ agent types with perceive-decide-act lifecycle

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1076-1076` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-45 | 40+ agent types with perceive-decide-act lifecycle | No graph viz tool has agents
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-45' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-45') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-45 | 40+ agent types with perceive-decide-act lifecycle | No graph viz tool has agents»
- [ ] 40+ agent types with perceive-decide-act lifecycle
- [ ] No graph viz tool has agents
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-46 [P2] AC-46: 8 engineering disciplines compose RAG + agents into higher-order intelligence

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1077-1077` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-46 | 8 engineering disciplines compose RAG + agents into higher-order intelligence | Unique to KGR
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-46' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-46') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-46 | 8 engineering disciplines compose RAG + agents into higher-order intelligence | Unique to KGR»
- [ ] 8 engineering disciplines compose RAG + agents into higher-order intelligence
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-47 [P2] AC-47: AI Explorer panel provides chat-based graph exploration with LLM-optional fallback

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1078-1078` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-47 | AI Explorer panel provides chat-based graph exploration with LLM-optional fallback | Neo4j Bloom (NL, cloud-only) — KGR is local-first + multi-RAG
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-47' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-47') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-47 | AI Explorer panel provides chat-based graph exploration with LLM-optional fallback | Neo4j Bloom (NL, cloud-only) — KGR is local-first + multi-RAG»
- [ ] AI Explorer panel provides chat-based graph exploration with LLM-optional fallback
- [ ] Neo4j Bloom (NL, cloud-only) — KGR is local-first + multi-RAG
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-AC-48 [P2] AC-48: MCP tools expose RAG/agent/engineering capabilities to external clients

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:1079-1079` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
AC-48 | MCP tools expose RAG/agent/engineering capabilities to external clients | Graphify (basic MCP) — KGR has full RAG+agent MCP
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'AC-48' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('AC-48') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «AC-48 | MCP tools expose RAG/agent/engineering capabilities to external clients | Graphify (basic MCP) — KGR has full RAG+agent MCP»
- [ ] MCP tools expose RAG/agent/engineering capabilities to external clients
- [ ] Graphify (basic MCP) — KGR has full RAG+agent MCP
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-002 [P2] FR-KGR-002: Node Intelligence (8-Tab Inspector)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:171-231` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 9.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-002: Node Intelligence (8-Tab Inspector)

When a node is selected, the system SHALL display an 8-tab inspector. This surpasses every competitor's node inspection (Graphify: properties only, Neo4j Bloom: properties + NL, Sourcetrail: 3-panel, yFiles: custom required).

#### Tab 1: Overview
- Canonical ID, display name, entity label/type, domain membership
- All stored properties with type-aware formatting (timestamps as locale dates, URLs as links, code refs as monospace)
- Creation metadata: source system, ingestion run, timestamp
- Quick actions: expand neighborhood, trace lineage, compute blast radius

#### Tab 2: Relationships
- Incoming edge count by type with expandable list
- Outgoing edge count by type with expandable list
- Bidirectional relationship detection
- Relationship type distribution bar chart
- Click any edge to navigate to it
- Total degree, in-degree, out-degree prominently displayed

#### Tab 3: Impact
- **Blast radius summary**: N entities at M depth, risk level badge
- **Blast radius depth breakdown**: by-depth and by-type bar charts
- **Centrality radar chart** (SVG): 5 axes — degree, betweenness, closeness, PageRank, blast radius
- **Change propagation score**: percentage of graph affected
- **Reverse impact** (upstream): who depends on this entity
- "Explore Blast Radius" button opens concentric ring view
- "Run What-If" button simulates removal
- **Unique to KGR** — no competitor has integrated impact analysis in the inspector

#### Tab 4: Evidence
- Direct evidence references (source_ref, evidence_key, method)
- Evidence chain depth: hops to nearest source-of-truth
- Trust score based on evidence completeness
- Source system diversity: entities backed by multiple independent sources
- Evidence provenance graph (mini inline view)
- **Unique to KGR** — only Graphify has partial evidence (EXTRACTED/INFERRED), KGR goes much deeper

#### Tab 5: Similarity
- Top 10 structurally similar nodes (by Jaccard neighbor similarity)
- Common neighbor count and list
- Shared relationship patterns
- Community/cluster membership
- Link prediction score: likelihood of missing connections
- **Unique to KGR** — no competitor offers node similarity analysis

#### Tab 6: History
- Temporal changes when available (property modifications over ingestion runs)
- Ingestion runs that touched this entity with timestamps
- Modification timeline (sparkline)
- Source system origin trail

#### Tab 7: Annotations
- Text annotations stored in localStora
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] When a node is selected, the system SHALL display an 8-tab inspector.
- [ ] This surpasses every competitor's node inspection (Graphify: properties only, Neo4j Bloom: properties + NL, Sourcetrail: 3-panel, yFiles: custom required).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-003 [P2] FR-KGR-003: Edge Intelligence

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:232-243` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-003: Edge Intelligence

When an edge is selected, the system SHALL display:
- Source and target entity summaries with mini-preview cards
- Edge type with semantic meaning from ontology manifest
- All edge properties with type-aware formatting
- Evidence backing: source_ref, evidence_key, method, creation_status badge
- Temporal context: when was this relationship established
- Path context: which known paths use this edge
- Parallel edges: other relationships between the same two entities
- Trust badge: DETERMINISTIC (green), INFERRED (amber), AMBIGUOUS (orange), MANUAL (blue)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] When an edge is selected, the system SHALL display: - Source and target entity summaries with mini-preview cards - Edge type with semantic meaning from ontology manifest - All edge properties with type-aware formatting - Evidence backing: source_ref, evidence_key, method, creation_status badge - Temporal context: when was this relationship established - Path context: which known paths use this edg
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-004 [P2] FR-KGR-004: Interactive Graph Exploration

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:244-305` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 9.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-004: Interactive Graph Exploration

#### 2.4.1 Navigation
- Click to select node/edge and populate inspector
- Double-click to expand neighborhood (configurable depth 1-3)
- Right-click context menu (node): expand (1/2/3 hop), blast radius, find paths, trace lineage, hide, pin/unpin position, copy canonical ID, add annotation
- Right-click context menu (edge): inspect, show evidence, find parallel edges, hide edge type, copy details
- Right-click context menu (canvas): fit all, reset filters, export view, toggle minimap
- Keyboard navigation: Tab through nodes, Enter to select, Arrow keys to traverse edges, `E` expand, `I` toggle inspector, `F` toggle filters, `1-8` switch graph types, `Esc` deselect
- Exploration history breadcrumb with undo/redo (fixes Graphify's lack of undo)
- Focus mode: isolate selected node + N-hop neighborhood, dim everything else

#### 2.4.2 Filtering (10-Dimensional)
This surpasses every competitor's filtering (Graphify: label only, Neo4j Bloom: perspective, Gephi: partition, Linkurious: faceted).

1. **Domain filter**: Multi-select dropdown of GraphDomains
2. **Entity type filter**: Checkbox list of vertex labels with live counts
3. **Relationship filter**: Checkbox list of edge types with live counts
4. **Trust filter**: Deterministic / Inferred / Manual / All (radio)
5. **Evidence filter**: Evidenced / Unevidenced / All (radio)
6. **Temporal filter**: Date range slider for entity/edge creation
7. **Property filter**: Key-value filter builder (property operator value)
8. **Centrality filter**: Min/max degree threshold slider
9. **Community filter**: Show/hide by detected cluster
10. **Search-within-view**: text filter on visible graph without new API call

- Active filter chips with click-to-remove
- Filter state persists across graph type switches
- Saved filter presets in localStorage with named configurations
- "Reset all filters" button

#### 2.4.3 Layout Algorithms (12)
This surpasses yFiles (20 but €9.2K), Gephi (7), and every free tool.

1. **Force-directed (COSE)**: Default organic layout
2. **Hierarchical (Dagre)**: Top-down or left-right for dependency trees
3. **Breadthfirst**: Tree-like expansion from root node
4. **Circle**: All nodes on a circle
5. **Grid**: Regular grid for comparing entities
6. **Concentric**: Selected node at center, neighbors in rings
7. **Radial**: Radial tree from selected root
8. **Cola (constraint-based)**: Constraint layout for aligned groupings
9. **Euler (force with edge-leng
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Search-within-view: text filter on visible graph without new API call - Active filter chips with click-to-remove - Filter state persists across graph type switches - Saved filter presets in localStorage with named configurations - "Reset all filters" button #### 2.4.3 Layout Algorithms (12) This surpasses yFiles (20 but €9.2K), Gephi (7), and every free tool.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-005 [P2] FR-KGR-005: Data Feed Integration

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:306-343` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 9.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-005: Data Feed Integration

#### 2.5.1 Live Graph Feed
- WebSocket subscription to graph change events (`WS /ws/graph/events`)
- Event types: vertex_upserted, edge_upserted, vertex_deleted, edge_deleted, ingestion_completed, validation_completed
- Real-time node/edge addition with fade-in animation
- Incremental layout adjustment (pin existing, only layout new nodes)
- Notification badge for off-screen changes
- Polling fallback: `GET /api/v1/graph/events?since=<timestamp>`
- Reconnect with exponential backoff (fixes Graphistry's WebSocket reliability issues)

#### 2.5.2 Search Feed
- Full-text search with typeahead suggestions from recent entities
- Faceted search results grouped by domain AND type
- Search history with re-execution
- "Search within current view" (filter existing graph, no API call)
- Quick filters from suggestions: "Show all WorkItems", "Show all Files"

#### 2.5.3 Query Feed
- Path finding between entities (all shortest paths, not just one — fixes code2flow's single-path limitation)
- Impact traversal with configurable depth/breadth
- Neighborhood expansion (1-3 hops)
- Traceability chain
- Custom QueryPlan execution

#### 2.5.4 Analytics Feed
- Graph-level statistics: node/edge counts, density, diameter, clustering coefficient, connected components
- Domain-level statistics: entities per domain, cross-domain edge counts
- Quality metrics: evidence coverage, provenance coverage, finding counts
- Temporal statistics: ingestion rate, graph growth over time
- Degree distribution histogram

#### 2.5.5 Event Feed Panel
- Collapsible panel showing real-time graph change events
- Clickable events navigate to affected entity
- Filter by event type
- Pause/resume event stream
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Data Feed Integration #### 2.5.1 Live Graph Feed - WebSocket subscription to graph change events (WS /ws/graph/events) - Event types: vertex_upserted, edge_upserted, vertex_deleted, edge_deleted, ingestion_completed, validation_completed - Real-time node/edge addition with fade-in animation - Incremental layout adjustment (pin existing, only layout new nodes) - Notification bad
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-006 [P2] FR-KGR-006: Graph Comparison & Diff

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:344-353` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-006: Graph Comparison & Diff

- Snapshot comparison: compare graph state at two points in time
- Diff visualization: added (green), removed (red), modified (yellow), unchanged (gray)
- Side-by-side view with synchronized zoom/pan
- Overlay diff mode (toggle between side-by-side and overlay)
- Change list panel with sortable table
- Structural diff: changes in topology (new connections, broken paths)
- **Unique to KGR** — only yFiles has basic diff; KGR adds structural analysis
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Graph Comparison & Diff - Snapshot comparison: compare graph state at two points in time - Diff visualization: added (green), removed (red), modified (yellow), unchanged (gray) - Side-by-side view with synchronized zoom/pan - Overlay diff mode (toggle between side-by-side and overlay) - Change list panel with sortable table - Structural diff: changes in topology (new connection
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-007 [P2] FR-KGR-007: Export & Sharing (11+ Formats)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:354-372` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-007: Export & Sharing (11+ Formats)

This surpasses every competitor's export (Graphify: HTML/JSON/GraphML/SVG/Obsidian/Mermaid/Cypher, Gephi: PNG/SVG/PDF/GEXF, yFiles: PNG-PDF-SVG-VSDX but €9.2K, Graphistry: CSV/JSON/Parquet).

- **PNG export**: current canvas at 2x resolution
- **SVG export**: vector graph via `cy.svg()`
- **PDF report**: graph image + node table + relationship summary + metrics
- **JSON-LD export**: graph data with EOIP ontology context
- **GraphML export**: standard graph interchange format
- **GEXF export**: Gephi-compatible graph exchange format (matches Gephi's native format)
- **CSV export**: separate nodes.csv and edges.csv files
- **Obsidian vault export**: entity-per-note structure with `[[wikilinks]]` for graph relationships, preserving domain hierarchy as folder structure (matches Graphify's Obsidian export)
- **Mermaid diagram export**: entity relationships as Mermaid flowchart/graph syntax for embedding in Markdown documentation (matches Graphify's Mermaid callflow)
- **Cypher script export**: graph as Neo4j-compatible Cypher CREATE/MERGE statements for pushing to Neo4j or FalkorDB (matches Graphify's Cypher export)
- **Clipboard**: copy selected node/edge as formatted Markdown
- **Context export**: current lens context as reusable JSON
- Export dialog with format selector, resolution options, scope (visible/all)
- Annotations included in PDF/JSON-LD/context exports when "Include annotations" is checked
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Export & Sharing (11+ Formats) This surpasses every competitor's export (Graphify: HTML/JSON/GraphML/SVG/Obsidian/Mermaid/Cypher, Gephi: PNG/SVG/PDF/GEXF, yFiles: PNG-PDF-SVG-VSDX but €9.2K, Graphistry: CSV/JSON/Parquet). - PNG export: current canvas at 2x resolution - SVG export: vector graph via cy.svg() - PDF report: graph image + node table + relationship summary + metrics 
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-008 [P2] FR-KGR-008: Annotation & Collaboration

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:373-383` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-008: Annotation & Collaboration

- Node annotations: text notes stored in localStorage keyed by canonical_id
- Edge annotations: text notes keyed by edge_id
- Annotation indicator icon on annotated nodes/edges in graph
- Graph bookmarks: save named views (query + filters + graph type + layout + viewport)
- Quick-access bookmark bar below filter bar
- Export/import bookmarks as JSON
- Annotation export: include in PDF/JSON reports
- Character limit: 500 per annotation
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Annotation & Collaboration - Node annotations: text notes stored in localStorage keyed by canonical_id - Edge annotations: text notes keyed by edge_id - Annotation indicator icon on annotated nodes/edges in graph - Graph bookmarks: save named views (query + filters + graph type + layout + viewport) - Quick-access bookmark bar below filter bar - Export/import bookmarks as JSON -
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-FR-KGR-009 [P2] FR-KGR-009: AI-Assisted Exploration (Future-Ready)

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:384-392` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-009: AI-Assisted Exploration (Future-Ready)

- Natural language graph queries via MCP integration (query → QueryPlan conversion)
- "Explain this cluster" summarization via local LLM
- Auto-suggested interesting paths based on graph structure
- Anomaly highlighting: nodes with unusual degree patterns
- Recommended next expansions based on current exploration context
- **Surpasses** Neo4j Bloom's NL queries by using local-first LLM (no cloud)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'FR-KGR-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('FR-KGR-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): AI-Assisted Exploration (Future-Ready) - Natural language graph queries via MCP integration (query → QueryPlan conversion) - "Explain this cluster" summarization via local LLM - Auto-suggested interesting paths based on graph structure - Anomaly highlighting: nodes with unusual degree patterns - Recommended next expansions based on current exploration context - Surpasses Neo4j 
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

