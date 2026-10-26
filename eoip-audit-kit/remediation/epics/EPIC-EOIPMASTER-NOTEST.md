# EPIC-EOIPMASTER-NOTEST: EOIP-master-requirements.md · code_no_test

*Code references the ID but no test is mapped.* 14 tasks, ~36.0 h, priorities {'P0': 10, 'P1': 3, 'P2': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-CAP-01 [P0] CAP-01: Property-graph storage and indexing · D01 Storage · P0

- **Source:** `EOIP-master-requirements.md:39-39` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-01` | **Property-graph storage and indexing** | D01 Storage | `P0` | 100% Implemented (Implemented (BL-01, BL-02)) | **VERIFIED**
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:326, scripts/enhance_master_suite.py:179
2. Write one test per acceptance criterion; mark with @pytest.mark.req('CAP-01') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-01 | Property-graph storage and indexing | D01 Storage | P0 | 100% Implemented (Implemented (BL-01, BL-02)) | VERIFIED»
- [ ] Property-graph storage and indexing
- [ ] 100% Implemented (Implemented (BL-01, BL-02))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:326`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L326-L326), [`scripts/enhance_master_suite.py:179`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L179-L179)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-70 [P0] CAP-70: Large-graph WebGL visual rendering · D09 Agents · P0

- **Source:** `EOIP-master-requirements.md:108-108` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-70` | **Large-graph WebGL visual rendering** | D09 Agents | `P0` | 100% Implemented (Implemented (BL-54)) | **VERIFIED**
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:388, scripts/enhance_master_suite.py:241
2. Write one test per acceptance criterion; mark with @pytest.mark.req('CAP-70') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-70 | Large-graph WebGL visual rendering | D09 Agents | P0 | 100% Implemented (Implemented (BL-54)) | VERIFIED»
- [ ] Large-graph WebGL visual rendering
- [ ] 100% Implemented (Implemented (BL-54))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:388`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L388-L388), [`scripts/enhance_master_suite.py:241`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L241-L241)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-CAP-80 [P0] CAP-80: Organizational and wisdom intelligence · D10 UI/UX · P0

- **Source:** `EOIP-master-requirements.md:118-118` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`CAP-80` | **Organizational and wisdom intelligence** | D10 UI/UX | `P0` | 100% Implemented (Implemented (BL-56, WisdomGraphMiner)) | **VERIFIED**
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:326, scripts/enhance_master_suite.py:179
2. Write one test per acceptance criterion; mark with @pytest.mark.req('CAP-80') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «CAP-80 | Organizational and wisdom intelligence | D10 UI/UX | P0 | 100% Implemented (Implemented (BL-56, WisdomGraphMiner)) | VERIFIED»
- [ ] Organizational and wisdom intelligence
- [ ] 100% Implemented (Implemented (BL-56, WisdomGraphMiner))
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:326`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L326-L326), [`scripts/enhance_master_suite.py:179`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L179-L179)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GAP-02 [P0] GAP-02: CAP-10 / BL-29 · CLOSED · Existing SHACL validator is a custom subset over in-memory MemoryGraphStore; pySHACL adapter is present but pySHACL is omitted from locked dependencies.

- **Source:** `EOIP-master-requirements.md:2651-2651` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GAP-02` | **`CAP-10 / BL-29`** | `CLOSED` | `Existing SHACL validator is a custom subset over in-memory MemoryGraphStore; pySHACL adapter is present but pySHACL is omitted from locked dependencies.` | **P0**
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:384, scripts/enhance_master_suite.py:237
2. Write one test per acceptance criterion; mark with @pytest.mark.req('GAP-02') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GAP-02 | CAP-10 / BL-29 | CLOSED | Existing SHACL validator is a custom subset over in-memory MemoryGraphStore; pySHACL adapter is present but pySHACL is omitted from locked dependencies. | P0»
- [ ] Existing SHACL validator is a custom subset over in-memory MemoryGraphStore; pySHACL adapter is present but pySHACL is omitted from locked dependencies.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:384`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L384-L384), [`scripts/enhance_master_suite.py:237`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L237-L237)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-02 [P0] INV-02: Protégé / WebProtégé · Desktop client crashes on large graphs; lacks GitOps collaboration and branching · Web-native collaborative Schema Studio over out-of-core memory-mapped store with GitOps ontolo

- **Source:** `EOIP-master-requirements.md:2665-2665` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-02` | **Protégé / WebProtégé** | Desktop client crashes on large graphs; lacks GitOps collaboration and branching | **Web-native collaborative Schema Studio over out-of-core memory-mapped store with GitOps ontology-as-code** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:385, scripts/enhance_master_suite.py:238
2. Write one test per acceptance criterion; mark with @pytest.mark.req('INV-02') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-02 | Protégé / WebProtégé | Desktop client crashes on large graphs; lacks GitOps collaboration and branching | Web-native collaborative Schema Studio over out-of-core memory-mapped store with GitOps ontology-as-code | ADOPT (P0)»
- [ ] Desktop client crashes on large graphs; lacks GitOps collaboration and branching
- [ ] Web-native collaborative Schema Studio over out-of-core memory-mapped store with GitOps ontology-as-code
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:385`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L385-L385), [`scripts/enhance_master_suite.py:238`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L238-L238)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-05 [P0] INV-05: Microsoft GraphRAG · Batch extraction and Leiden community summarization costs hundreds of dollars per run · LightRAG/HippoRAG dual-level routing, deterministic NER pre-extraction, and incremental on-

- **Source:** `EOIP-master-requirements.md:2668-2668` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-05` | **Microsoft GraphRAG** | Batch extraction and Leiden community summarization costs hundreds of dollars per run | **LightRAG/HippoRAG dual-level routing, deterministic NER pre-extraction, and incremental on-demand community summarization** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:384, scripts/enhance_master_suite.py:237
2. Write one test per acceptance criterion; mark with @pytest.mark.req('INV-05') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-05 | Microsoft GraphRAG | Batch extraction and Leiden community summarization costs hundreds of dollars per run | LightRAG/HippoRAG dual-level routing, deterministic NER pre-extraction, and incremental on-demand community summarization | ADOPT (P0)»
- [ ] Batch extraction and Leiden community summarization costs hundreds of dollars per run
- [ ] LightRAG/HippoRAG dual-level routing, deterministic NER pre-extraction, and incremental on-demand community summarization
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:384`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L384-L384), [`scripts/enhance_master_suite.py:237`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L237-L237)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-06 [P0] INV-06: Palantir / Glean / Rovo · Customer enterprise data sent to proprietary SaaS cloud runtimes; cannot run on-prem · 100% Self-Hosted, Local-First, Air-Gap-Capable Architecture with zero external data egr

- **Source:** `EOIP-master-requirements.md:2669-2669` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-06` | **Palantir / Glean / Rovo** | Customer enterprise data sent to proprietary SaaS cloud runtimes; cannot run on-prem | **100% Self-Hosted, Local-First, Air-Gap-Capable Architecture with zero external data egress** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:390, scripts/enhance_master_suite.py:243
2. Write one test per acceptance criterion; mark with @pytest.mark.req('INV-06') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-06 | Palantir / Glean / Rovo | Customer enterprise data sent to proprietary SaaS cloud runtimes; cannot run on-prem | 100% Self-Hosted, Local-First, Air-Gap-Capable Architecture with zero external data egress | ADOPT (P0)»
- [ ] Palantir / Glean / Rovo
- [ ] Customer enterprise data sent to proprietary SaaS cloud runtimes; cannot run on-prem
- [ ] 100% Self-Hosted, Local-First, Air-Gap-Capable Architecture with zero external data egress
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:390`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L390-L390), [`scripts/enhance_master_suite.py:243`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L243-L243)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-09 [P0] INV-09: Gephi / Cytoscape · Canvas/SVG rendering stalls and crashes on graphs larger than 5,000 nodes · WebGL hardware-accelerated Sigma.js canvas (100k+ nodes @ 60 FPS) + server-side progressive disclosure

- **Source:** `EOIP-master-requirements.md:2672-2672` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-09` | **Gephi / Cytoscape** | Canvas/SVG rendering stalls and crashes on graphs larger than 5,000 nodes | **WebGL hardware-accelerated Sigma.js canvas (100k+ nodes @ 60 FPS) + server-side progressive disclosure** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:388, scripts/enhance_master_suite.py:241
2. Write one test per acceptance criterion; mark with @pytest.mark.req('INV-09') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-09 | Gephi / Cytoscape | Canvas/SVG rendering stalls and crashes on graphs larger than 5,000 nodes | WebGL hardware-accelerated Sigma.js canvas (100k+ nodes @ 60 FPS) + server-side progressive disclosure | ADOPT (P0)»
- [ ] Canvas/SVG rendering stalls and crashes on graphs larger than 5,000 nodes
- [ ] WebGL hardware-accelerated Sigma.js canvas (100k+ nodes @ 60 FPS) + server-side progressive disclosure
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:388`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L388-L388), [`scripts/enhance_master_suite.py:241`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L241-L241)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-10 [P0] INV-10: Stardog (Join Variance) vs GraphDB (Write Amp) · GraphDB slows ingestion 10x; Stardog causes query timeouts on deep recursion · Hybrid Tiered Reasoning (HTRE): forward-materialize static taxonomy; rew

- **Source:** `EOIP-master-requirements.md:2673-2673` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-10` | **Stardog (Join Variance) vs GraphDB (Write Amp)** | GraphDB slows ingestion 10x; Stardog causes query timeouts on deep recursion | **Hybrid Tiered Reasoning (HTRE): forward-materialize static taxonomy; rewrite complex axioms at query time** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:389, scripts/enhance_master_suite.py:242
2. Write one test per acceptance criterion; mark with @pytest.mark.req('INV-10') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-10 | Stardog (Join Variance) vs GraphDB (Write Amp) | GraphDB slows ingestion 10x; Stardog causes query timeouts on deep recursion | Hybrid Tiered Reasoning (HTRE): forward-materialize static taxonomy; rewrite complex axioms at query time | ADOPT (P0)»
- [ ] Stardog (Join Variance) vs GraphDB (Write Amp)
- [ ] GraphDB slows ingestion 10x; Stardog causes query timeouts on deep recursion
- [ ] Hybrid Tiered Reasoning (HTRE): forward-materialize static taxonomy; rewrite complex axioms at query time
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:389`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L389-L389), [`scripts/enhance_master_suite.py:242`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L242-L242)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-INV-SELF-01 [P0] INV-SELF-01: KnowGridFlow Baseline (BL-18) · Existing retrieval service evaluates graph edges without checking caller's ACL tokens · Build derivation ACL filter into retrieval pipeline; discard unauthorized paths 

- **Source:** `EOIP-master-requirements.md:2674-2674` (table_row) · **Type:** Security · **Severity:** Critical
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04 · **Effort:** 3.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`INV-SELF-01` | **KnowGridFlow Baseline (BL-18)** | Existing retrieval service evaluates graph edges without checking caller's ACL tokens | **Build derivation ACL filter into retrieval pipeline; discard unauthorized paths before LLM context generation** | ``ADOPT (P0)``
```
</details>

**Next steps**
1. Read the referenced code: scripts/enhance_master_suite.py:415
2. Write one test per acceptance criterion; mark with @pytest.mark.req('INV-SELF-01') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «INV-SELF-01 | KnowGridFlow Baseline (BL-18) | Existing retrieval service evaluates graph edges without checking caller's ACL tokens | Build derivation ACL filter into retrieval pipeline; discard unauthorized paths before LLM context generation | ADOPT (P0)»
- [ ] Existing retrieval service evaluates graph edges without checking caller's ACL tokens
- [ ] Build derivation ACL filter into retrieval pipeline; discard unauthorized paths before LLM context generation
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/enhance_master_suite.py:415`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L415-L415)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-GAP-06 [P1] GAP-06: CAP-32 / C05 · CLOSED · Document extraction lacks byte-exact locator tracking across audio/video and complex PDF diagram bounding boxes.

- **Source:** `EOIP-master-requirements.md:2654-2654` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GAP-06` | **`CAP-32 / C05`** | `CLOSED` | `Document extraction lacks byte-exact locator tracking across audio/video and complex PDF diagram bounding boxes.` | **P1**
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:390, scripts/enhance_master_suite.py:243
2. Write one test per acceptance criterion; mark with @pytest.mark.req('GAP-06') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GAP-06 | CAP-32 / C05 | CLOSED | Document extraction lacks byte-exact locator tracking across audio/video and complex PDF diagram bounding boxes. | P1»
- [ ] Document extraction lacks byte-exact locator tracking across audio/video and complex PDF diagram bounding boxes.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:390`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L390-L390), [`scripts/enhance_master_suite.py:243`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L243-L243)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GAP-09 [P1] GAP-09: CAP-21 / BL-51 · CLOSED · Existing federation planner handles simple SQL queries but lacks self-join elimination and W3C R2RML compliance.

- **Source:** `EOIP-master-requirements.md:2657-2657` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GAP-09` | **`CAP-21 / BL-51`** | `CLOSED` | `Existing federation planner handles simple SQL queries but lacks self-join elimination and W3C R2RML compliance.` | **P1**
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:388, scripts/enhance_master_suite.py:241
2. Write one test per acceptance criterion; mark with @pytest.mark.req('GAP-09') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GAP-09 | CAP-21 / BL-51 | CLOSED | Existing federation planner handles simple SQL queries but lacks self-join elimination and W3C R2RML compliance. | P1»
- [ ] Existing federation planner handles simple SQL queries but lacks self-join elimination and W3C R2RML compliance.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:388`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L388-L388), [`scripts/enhance_master_suite.py:241`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L241-L241)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GAP-10 [P1] GAP-10: CAP-70 / BL-54 · CLOSED · apps/web contains legacy Cytoscape components alongside modern Sigma.js WebGL canvas, creating redundant bundle weight and inconsistent UX.

- **Source:** `EOIP-master-requirements.md:2658-2658` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GAP-10` | **`CAP-70 / BL-54`** | `CLOSED` | `apps/web contains legacy Cytoscape components alongside modern Sigma.js WebGL canvas, creating redundant bundle weight and inconsistent UX.` | **P1**
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:336, scripts/enhance_master_suite.py:189
2. Write one test per acceptance criterion; mark with @pytest.mark.req('GAP-10') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GAP-10 | CAP-70 / BL-54 | CLOSED | apps/web contains legacy Cytoscape components alongside modern Sigma.js WebGL canvas, creating redundant bundle weight and inconsistent UX. | P1»
- [ ] apps/web contains legacy Cytoscape components alongside modern Sigma.js WebGL canvas, creating redundant bundle weight and inconsistent UX.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:336`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L336-L336), [`scripts/enhance_master_suite.py:189`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L189-L189)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GAP-08 [P2] GAP-08: CAP-64 / BL-44 · CLOSED · Neural modules under packages/eoip/neural/ import numpy and torch which were not in base requirements.lock.

- **Source:** `EOIP-master-requirements.md:2656-2656` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GAP-08` | **`CAP-64 / BL-44`** | `CLOSED` | `Neural modules under packages/eoip/neural/ import numpy and torch which were not in base requirements.lock.` | **P2**
```
</details>

**Next steps**
1. Read the referenced code: scripts/build_master_suite.py:385, scripts/enhance_master_suite.py:238
2. Write one test per acceptance criterion; mark with @pytest.mark.req('GAP-08') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GAP-08 | CAP-64 / BL-44 | CLOSED | Neural modules under packages/eoip/neural/ import numpy and torch which were not in base requirements.lock. | P2»
- [ ] Neural modules under packages/eoip/neural/ import numpy and torch which were not in base requirements.lock.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`scripts/build_master_suite.py:385`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L385-L385), [`scripts/enhance_master_suite.py:238`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L238-L238)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

