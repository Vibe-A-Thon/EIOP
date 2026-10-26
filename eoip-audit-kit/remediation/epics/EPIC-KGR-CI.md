# EPIC-KGR-CI: EOIP-engg-doc-pkg/KGR-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 1 tasks, ~0.8 h, priorities {'P2': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-FR-KGR-001 [P2] FR-KGR-001: Multi-Graph Type Rendering

- **Source:** `EOIP-engg-doc-pkg/KGR-requirements.md:99-170` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 14, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 0.8 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### FR-KGR-001: Multi-Graph Type Rendering

The system SHALL render 8 graph types from the same underlying data, each with a purpose-built visualization. This surpasses every competitor (Graphify: 1 type, Neo4j Bloom: 1, Gephi: 1, yFiles: configurable but no built-in types).

#### 2.1 Knowledge Graph (Primary)
- Entity-centric view: nodes represent canonical entities (WorkItem, Commit, File, CodeSymbol, Document, Person, etc.)
- Directed edges with type labels, evidence status, and trust indicators
- Domain coloring with automatic palette assignment per vertex label
- Evidence overlay: solid (deterministic) vs. dashed (inferred) edges
- Evidence thickness: edges backed by source references rendered thicker
- Semantic zoom: labels appear/hide at zoom thresholds
- This is the default view, extending the existing Graph lens

#### 2.2 Relationship Graph
- Edge-centric analysis: relationship types become nodes, connected by shared endpoint types
- Node size proportional to edge instance count
- Co-occurrence matrix heatmap view (toggle between graph and matrix)
- Click a relationship-type node to show all instances
- Frequency-encoded bar chart per relationship type
- **Unique to KGR** — no competitor offers edge-centric analysis

#### 2.3 Metadata Graph
- Schema topology: vertex labels as nodes, edge labels as connecting edges
- Property schema overlay: show required/optional properties per label on hover
- Index coverage map: checkmarks for indexed labels, highlights for unindexed
- Instance count badges on each label node
- Data from `/api/v1/graph/schema` endpoint
- Ingestion lineage: source system → connector → ingestion run → entity creation flow
- Validation topology: ValidationRun → Finding → affected entity connections

#### 2.4 Enterprise Ontology Establishment Graph
- Class hierarchy tree layout: GraphDomain → vertex labels with domain grouping
- Property list per type from ontology manifest with cardinality indicators
- Ontology version display with schema version
- Semantic alignment: map EOIP ontology to standard vocabularies (Dublin Core, SKOS, PROV-O)
- Index coverage per type
- Uses hierarchical (breadthfirst) layout by default
- **Unique to KGR** — no competitor has ontology establishment views

#### 2.5 Temporal Graph
- Time-windowed filtering by creation/modification timestamps
- Timeline scrubber with dual-handle range slider and histogram overlay
- Animated playback of graph evolution with configurable speed (1x, 2x, 5x, 10x)
- Entities ou
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run

**Acceptance criteria**
- [ ] The system SHALL render 8 graph types from the same underlying data, each with a purpose-built visualization.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/unit/test_documentation_audit.py:59`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

