# EPIC-KGRG-NOTEST: EOIP-engg-doc-pkg/KGR-g-requirements.md · code_no_test

*Code references the ID but no test is mapped.* 4 tasks, ~12.0 h, priorities {'P0': 3, 'P1': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-KGR-G-001 [P0] KGR-G-001: Polyglot Cross-Repository AST Linker

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:215-223` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-001: Polyglot Cross-Repository AST Linker
- **Classification:** Functional Requirement | **Priority:** P0 (Core)
- **Description:** The system SHALL parse source code across multi-repository workspaces using deterministic Tree-Sitter grammars (Python, TypeScript, JavaScript, Go, Java, Rust, C/C++) and resolve cross-service invocations (REST, gRPC, GraphQL) into directed `CALLS_ENDPOINT` edges.
- **Verification Criteria:**
  - Parsing 100,000 lines of code across 3 languages completes in < 5.0 seconds on standard CPU.
  - Zero external LLM API calls are triggered for base symbol extraction.
  - Generates verified `Symbol`, `Function`, `Class`, `Module`, and `ApiEndpoint` nodes with deterministic SHA-256 entity hashes.
- **Target Implementation:** `packages/eoip/ingestion/code_graph.py` & `polyglot_linker.py`
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/ingestion/polyglot_linker.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('KGR-G-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-KGR-G-001

**Acceptance criteria**
- [ ] The system SHALL parse source code across multi-repository workspaces using deterministic Tree-Sitter grammars (Python, TypeScript, JavaScript, Go, Java, Rust, C/C++) and resolve cross-service invocations (REST, gRPC, GraphQL) into directed CALLS_ENDPOINT edges.
- [ ] Parsing 100,000 lines of code across 3 languages completes in < 5.0 seconds on standard CPU
- [ ] Zero external LLM API calls are triggered for base symbol extraction
- [ ] Generates verified Symbol, Function, Class, Module, and ApiEndpoint nodes with deterministic SHA-256 entity hashes
- [ ] Target Implementation: packages/eoip/ingestion/codegraph.py & polyglotlinker.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingestion/polyglot_linker.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingestion/polyglot_linker.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-003 [P0] KGR-G-003: Obsidian Vault & Interactive Knowledge Artifact Generator

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:233-240` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-003: Obsidian Vault & Interactive Knowledge Artifact Generator
- **Classification:** Functional Requirement | **Priority:** P0 (Core)
- **Description:** The system SHALL export any selected subgraph or entire enterprise ontology as a self-contained, bi-directionally linked Markdown vault compatible with Obsidian, complete with YAML frontmatter, `[[wiki-links]]`, embedded Mermaid syntax diagrams, and interactive HTML visualizer bundles.
- **Verification Criteria:**
  - Exported vault opens seamlessly in standard Markdown viewers with zero broken relative links.
  - Frontmatter contains metadata properties: `tags`, `aliases`, `type`, `temporal_valid_from`, and `merkle_hash`.
- **Target Implementation:** `packages/eoip/exporters/obsidian_vault.py`
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/exporters/obsidian_vault.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('KGR-G-003') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-KGR-G-003

**Acceptance criteria**
- [ ] The system SHALL export any selected subgraph or entire enterprise ontology as a self-contained, bi-directionally linked Markdown vault compatible with Obsidian, complete with YAML frontmatter, [[wiki-links]], embedded Mermaid syntax diagrams, and interactive HTML visualizer bundles.
- [ ] Exported vault opens seamlessly in standard Markdown viewers with zero broken relative links
- [ ] Frontmatter contains metadata properties: tags, aliases, type, temporalvalidfrom, and merklehash
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/exporters/obsidian_vault.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/exporters/obsidian_vault.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-004 [P0] KGR-G-004: In-Memory High-Performance Graph Algorithm Engine

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:241-249` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-004: In-Memory High-Performance Graph Algorithm Engine
- **Classification:** Non-Functional / Algorithmic | **Priority:** P0 (Core)
- **Description:** The system SHALL provide embedded, high-performance implementations of Leiden community detection, Louvain modularity, PageRank centrality, and shortest-path BFS without requiring external database plugins or GPU hardware.
- **Verification Criteria:**
  - Leiden community detection executes on a 20,000-node graph in < 1,500ms.
  - PageRank converges within 30 iterations in < 500ms on 20,000 nodes.
  - Unit tests verify deterministic community assignment across identical input graphs.
- **Target Implementation:** `packages/eoip/analytics/algorithms.py`
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/analytics/algorithms.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('KGR-G-004') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-KGR-G-004

**Acceptance criteria**
- [ ] The system SHALL provide embedded, high-performance implementations of Leiden community detection, Louvain modularity, PageRank centrality, and shortest-path BFS without requiring external database plugins or GPU hardware.
- [ ] Leiden community detection executes on a 20,000-node graph in < 1,500ms
- [ ] PageRank converges within 30 iterations in < 500ms on 20,000 nodes
- [ ] Unit tests verify deterministic community assignment across identical input graphs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/analytics/algorithms.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/analytics/algorithms.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-KGR-G-002 [P1] KGR-G-002: Local Multimodal Audio & Document Ingestion Pipeline

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:224-232` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-002: Local Multimodal Audio & Document Ingestion Pipeline
- **Classification:** Functional Requirement | **Priority:** P1 (Enterprise)
- **Description:** The system SHALL ingest audio and video recordings (`.mp3`, `.mp4`, `.wav`) using local `faster-whisper`, extract spoken engineering dialogue, recognize entity mentions corresponding to existing ontology nodes, and create `SpokenDecision` nodes linked to respective code components.
- **Verification Criteria:**
  - 10-minute audio file is transcribed on local CPU/GPU within 60 seconds with word-level timestamps.
  - Extracted ADR nodes contain speaker attribution, transcript snippet, timestamp, and confidence score.
  - Fallback cleanly when audio dependencies are absent without halting text/code pipelines.
- **Target Implementation:** `packages/eoip/ingestion/multimodal_audio.py`
```
</details>

**Next steps**
1. Read the referenced code: packages/eoip/ingestion/multimodal_audio.py:1
2. Write one test per acceptance criterion; mark with @pytest.mark.req('KGR-G-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-KGR-G-002

**Acceptance criteria**
- [ ] The system SHALL ingest audio and video recordings (.mp3, .mp4, .wav) using local faster-whisper, extract spoken engineering dialogue, recognize entity mentions corresponding to existing ontology nodes, and create SpokenDecision nodes linked to respective code components.
- [ ] 10-minute audio file is transcribed on local CPU/GPU within 60 seconds with word-level timestamps
- [ ] Extracted ADR nodes contain speaker attribution, transcript snippet, timestamp, and confidence score
- [ ] Fallback cleanly when audio dependencies are absent without halting text/code pipelines
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingestion/multimodal_audio.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingestion/multimodal_audio.py#L1-L1)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

