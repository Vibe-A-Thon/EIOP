# EPIC-KGRG-CI: EOIP-engg-doc-pkg/KGR-g-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 10 tasks, ~12.8 h, priorities {'P0': 6, 'P1': 4}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-KGR-G-011 [P0] KGR-G-011: Formal Behavioral Verification at Merge Gate

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:452-461` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-011: Formal Behavioral Verification at Merge Gate
- **Classification:** Functional / Quality | **Priority:** P0 (Core)
- **Description:** The system SHALL integrate a behavioral verification gate into the PR/merge workflow that combines SHACL contract testing, property-based hypothesis testing (`hypothesis` library), and AST contract diffing to prove that new code changes preserve prior ontology contracts. When a function, schema, or API endpoint cannot be formally verified due to type complexity, the gate SHALL emit a structured `abstain` record (scope, reason, confidence boundary) rather than a false positive.
- **Verification Criteria:**
  - Behavioral gate runs automatically for every PR touching ingestion, query, or ontology code paths.
  - Successfully verifies behavioral equivalence for pure functions with typed primitive/collection signatures.
  - Emits structured JSON `abstain` with `unverified_symbols`, `abstain_reason`, and `coverage_percent` when verification scope is exceeded.
  - Blocking threshold configurable: R1 (peer) blocks on any verified failure; R0 (auto) blocks only on critical-path failures.
- **Target Implementation:** `packages/eoip/verification/behavioral_gate.py` + CI hook
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-KGR-G-011

**Acceptance criteria**
- [ ] The system SHALL integrate a behavioral verification gate into the PR/merge workflow that combines SHACL contract testing, property-based hypothesis testing (hypothesis library), and AST contract diffing to prove that new code changes preserve prior ontology contracts. When a function, schema, or API endpoint cannot be formally verified due to type complexity, the gate SHALL emit a structured abst
- [ ] Classification: Functional / Quality | Priority: P0 (Core)
- [ ] Behavioral gate runs automatically for every PR touching ingestion, query, or ontology code paths
- [ ] Successfully verifies behavioral equivalence for pure functions with typed primitive/collection signatures
- [ ] Blocking threshold configurable: R1 (peer) blocks on any verified failure; R0 (auto) blocks only on critical-path failures
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/verification/behavioral_gate.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/verification/behavioral_gate.py#L1-L1), [`scripts/inspect_progress.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/inspect_progress.py#L7-L7)
- tests: `tests/unit/test_behavioral_gate.py:16`, `tests/unit/test_behavioral_gate.py::test_behavioral_gate_abstains_with_unverified_symbols_and_coverage`, `tests/unit/test_behavioral_gate.py::test_behavioral_gate_cli_writes_ci_report_for_git_diff`, `tests/unit/test_behavioral_gate.py::test_behavioral_gate_detects_observable_pure_function_change`, `tests/unit/test_behavioral_gate.py::test_behavioral_gate_fails_public_signature_break`, `tests/unit/test_behavioral_gate.py::test_behavioral_gate_supports_r0_and_r1_blocking_thresholds`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-KGR-G-012 [P0] KGR-G-012: Incremental Differential AST Re-Index (Git Hook Integration)

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:462-471` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.2 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-012: Incremental Differential AST Re-Index (Git Hook Integration)
- **Classification:** Performance / Operational | **Priority:** P0 (Core)
- **Description:** The system SHALL provide a git hook integration that detects which source files changed in the most recent commit diff, re-parses only those files' AST deltas using tree-sitter, propagates cross-file symbol impact through the existing graph, and applies a patch-style graph update — without triggering a full workspace re-ingestion.
- **Verification Criteria:**
  - Incremental re-index for a commit changing ≤ 100 files completes in < 2.0 seconds on standard CPU.
  - Cross-file `CALLS` and `IMPORTS` edges correctly updated when a renamed/moved symbol is detected.
  - Full correctness equivalence: incremental result matches full re-index result on the same commit set.
  - Git hook installs cleanly via `eoip install-hooks` CLI command.
- **Target Implementation:** `packages/eoip/ingestion/incremental_indexer.py` + `scripts/install_git_hooks.py`
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-KGR-G-012

**Acceptance criteria**
- [ ] The system SHALL provide a git hook integration that detects which source files changed in the most recent commit diff, re-parses only those files' AST deltas using tree-sitter, propagates cross-file symbol impact through the existing graph, and applies a patch-style graph update — without triggering a full workspace re-ingestion.
- [ ] Incremental re-index for a commit changing ≤ 100 files completes in < 2.0 seconds on standard CPU
- [ ] Cross-file CALLS and IMPORTS edges correctly updated when a renamed/moved symbol is detected
- [ ] Full correctness equivalence: incremental result matches full re-index result on the same commit set
- [ ] Git hook installs cleanly via eoip install-hooks CLI command
- [ ] Target Implementation: packages/eoip/ingestion/incrementalindexer.py + scripts/installgithooks.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/cli.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/cli.py#L21-L21), [`packages/eoip/ingestion/incremental_indexer.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingestion/incremental_indexer.py#L1-L1), [`scripts/install_git_hooks.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/install_git_hooks.py#L3-L3)
- tests: `tests/unit/test_incremental_indexer.py:37`, `tests/unit/test_incremental_indexer.py::test_incremental_index_event_matches_schema`, `tests/unit/test_incremental_indexer.py::test_incremental_indexer_handles_hundred_file_diff_under_two_seconds`, `tests/unit/test_incremental_indexer.py::test_incremental_indexer_matches_fresh_full_symbol_index_for_same_commit_set`, `tests/unit/test_incremental_indexer.py::test_incremental_indexer_updates_only_changed_files_and_propagates_cross_file_impact`, `tests/unit/test_incremental_indexer.py::test_install_hooks_command_writes_real_incremental_hook`, `tests/unit/test_incremental_indexer.py::test_run_incremental_index_writes_report_for_git_diff`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-KGR-G-013 [P0] KGR-G-013: Native Per-Tenant Named-Graph Isolation Protocol

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:472-481` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.2 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-013: Native Per-Tenant Named-Graph Isolation Protocol
- **Classification:** Multi-Tenancy / Security | **Priority:** P0 (Core)
- **Description:** The system SHALL formalize a Named-Graph Isolation Protocol in the `GraphStore` port, enabling each tenant to receive a fully isolated named graph instance (e.g., `g:<tenant_id>`) within the same backend process, sharing connection pools and memory without any possibility of cross-tenant data access. Implemented across HugeGraph, Neo4j, AWS Neptune, and In-Memory backends.
- **Verification Criteria:**
  - Tenant A's nodes and edges are completely invisible to Tenant B's queries across all backends.
  - Named-graph creation and deletion complete in < 50ms.
  - Cross-tenant isolation verified by adversarial query injection tests targeting cross-namespace traversal.
  - Supports ≥ 1,000 named-graph tenants in a single HugeGraph instance.
- **Target Implementation:** `packages/eoip/graph/named_graph.py` + backend adapter extensions
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-KGR-G-013

**Acceptance criteria**
- [ ] The system SHALL formalize a Named-Graph Isolation Protocol in the GraphStore port, enabling each tenant to receive a fully isolated named graph instance (e.g., g:<tenant_id>) within the same backend process, sharing connection pools and memory without any possibility of cross-tenant data access. Implemented across HugeGraph, Neo4j, AWS Neptune, and In-Memory backends.
- [ ] Tenant A's nodes and edges are completely invisible to Tenant B's queries across all backends
- [ ] Named-graph creation and deletion complete in < 50ms
- [ ] Cross-tenant isolation verified by adversarial query injection tests targeting cross-namespace traversal
- [ ] Supports ≥ 1,000 named-graph tenants in a single HugeGraph instance
- [ ] Target Implementation: packages/eoip/graph/namedgraph.py + backend adapter extensions
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/adapters/manifests.py:170`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/adapters/manifests.py#L170-L170), [`packages/eoip/graph/named_graph.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/named_graph.py#L1-L1)
- tests: `tests/unit/test_named_graph.py:13`, `tests/unit/test_named_graph.py::test_cross_tenant_access_raises_violation`, `tests/unit/test_named_graph.py::test_named_graph_edge_isolation_and_find_edges`, `tests/unit/test_named_graph.py::test_named_graph_find_vertex_by_property_and_count`, `tests/unit/test_named_graph.py::test_named_graph_manager`, `tests/unit/test_named_graph.py::test_named_graph_vertex_isolation`, `tests/unit/test_named_graph_isolation.py:24`, `tests/unit/test_named_graph_isolation.py::test_named_graph_blocks_adversarial_cross_namespace_edges`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-KGR-G-016 [P0] KGR-G-016: Co-Located HNSW Vector + Graph Index (VectorGraph Adapter)

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:502-511` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-016; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.2 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-016: Co-Located HNSW Vector + Graph Index (VectorGraph Adapter)
- **Classification:** Performance / Storage | **Priority:** P0 (Core)
- **Description:** The system SHALL provide a VectorGraph adapter that co-locates an HNSW approximate nearest neighbor vector index within the same graph storage engine, eliminating cross-store ETL between the graph database and a separate vector database. Unified queries of the form "find the 10 nodes semantically closest to embedding E that are within 2 hops of node N" SHALL execute in a single query plan.
- **Verification Criteria:**
  - Combined vector similarity + 2-hop graph traversal executes in < 5ms at P95 on a 1M-node graph.
  - HNSW index build over 500K node embeddings (768-dim) completes in < 120 seconds.
  - Zero data duplication between vector index and property graph store — embeddings stored as node properties.
  - Backward compatible with existing separate vector store configuration via adapter toggle.
- **Target Implementation:** `packages/eoip/graph/vector_graph.py` + integration into `rag/engine.py`
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-KGR-G-016

**Acceptance criteria**
- [ ] The system SHALL provide a VectorGraph adapter that co-locates an HNSW approximate nearest neighbor vector index within the same graph storage engine, eliminating cross-store ETL between the graph database and a separate vector database. Unified queries of the form "find the 10 nodes semantically closest to embedding E that are within 2 hops of node N" SHALL execute in a single query plan.
- [ ] Combined vector similarity + 2-hop graph traversal executes in < 5ms at P95 on a 1M-node graph
- [ ] HNSW index build over 500K node embeddings (768-dim) completes in < 120 seconds
- [ ] Zero data duplication between vector index and property graph store — embeddings stored as node properties
- [ ] Backward compatible with existing separate vector store configuration via adapter toggle
- [ ] Target Implementation: packages/eoip/graph/vectorgraph.py + integration into rag/engine.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/graph/vector_graph.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/vector_graph.py#L1-L1), [`scripts/update_phase3_wp31.py:29`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp31.py#L29-L29)
- tests: `tests/unit/test_vector_graph.py:11`, `tests/unit/test_vector_graph.py::test_hnsw_index_insert_and_search`, `tests/unit/test_vector_graph.py::test_hnsw_index_removal`, `tests/unit/test_vector_graph.py::test_unified_graph_then_vector_colocated`, `tests/unit/test_vector_graph.py::test_unified_vector_then_traverse_colocated`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-KGR-G-017 [P0] KGR-G-017: PR-Level Cross-Repository Graph Impact Triage MCP Tools

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:512-521` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-017; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.2 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-017: PR-Level Cross-Repository Graph Impact Triage MCP Tools
- **Classification:** Functional / Developer Tooling | **Priority:** P0 (Core)
- **Description:** The system SHALL expose dedicated MCP tools for PR-level impact triage: `list_prs(repo, status)`, `get_pr_impact(pr_id)` returning full cross-repository blast radius as structured JSON subgraph, and `triage_prs(repo)` returning a risk-scored list of open PRs ranked by ontology-weighted change impact. Each PR impact response SHALL include: affected downstream services, data ownership classifications, regulatory flags, SLA impact scores, and suggested reviewers based on graph ownership attribution.
- **Verification Criteria:**
  - `get_pr_impact` responds in < 150ms for PRs affecting ≤ 5,000 graph nodes.
  - Cross-repository blast radius correctly identifies dependencies across ≥ 3 connected repositories.
  - Risk score is deterministic for identical PR diffs.
  - MCP tool definitions conform to MCP v1.0 JSON schema specification.
- **Target Implementation:** `packages/eoip/agents/mcp_pr_tools.py` + extension to `mcp_server.py`
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-KGR-G-017

**Acceptance criteria**
- [ ] The system SHALL expose dedicated MCP tools for PR-level impact triage: list_prs(repo, status), get_pr_impact(pr_id) returning full cross-repository blast radius as structured JSON subgraph, and triage_prs(repo) returning a risk-scored list of open PRs ranked by ontology-weighted change impact. Each PR impact response SHALL include: affected downstream services, data ownership classifications, reg
- [ ] getprimpact responds in < 150ms for PRs affecting ≤ 5,000 graph nodes
- [ ] Cross-repository blast radius correctly identifies dependencies across ≥ 3 connected repositories
- [ ] Risk score is deterministic for identical PR diffs
- [ ] MCP tool definitions conform to MCP v1.0 JSON schema specification
- [ ] Target Implementation: packages/eoip/agents/mcpprtools.py + extension to mcpserver.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/agents/mcp_pr_tools.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/mcp_pr_tools.py#L1-L1), [`scripts/update_phase3_wp31.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp31.py#L40-L40)
- tests: `tests/unit/test_mcp_pr_tools.py:14`, `tests/unit/test_mcp_pr_tools.py::test_mcp_pr_tools_invocation_through_registry`, `tests/unit/test_mcp_pr_tools.py::test_pr_impact_calculation_direct_and_transitive`, `tests/unit/test_mcp_pr_tools.py::test_pr_risk_scoring_and_reviewer_suggestion`, `tests/unit/test_mcp_pr_tools.py::test_triage_prs_ranking`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-KGR-G-019 [P0] KGR-G-019: Calibrated Uncertainty & Honest Abstain MCP Response Protocol

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:532-541` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-019; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.2 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-019: Calibrated Uncertainty & Honest Abstain MCP Response Protocol
- **Classification:** Trust / AI Quality | **Priority:** P0 (Core)
- **Description:** The system SHALL embed a standardized uncertainty schema in every MCP tool response: `confidence_score` (float 0.0–1.0 reflecting data completeness, freshness, graph coverage), `uncertainty_reason` (explanation when confidence < 0.7), `abstain` (boolean when system cannot reliably answer), `evidence_chain` (array of source node/edge IDs used), and `coverage_percent` (fraction of relevant subspace consulted). AI coding assistants SHALL display `abstain=true` responses with a distinct visual indicator rather than showing them as authoritative answers.
- **Verification Criteria:**
  - Every MCP tool response includes all five schema fields with correct types.
  - `confidence_score` correlates with actual accuracy on a held-out evaluation set (Spearman ρ ≥ 0.6).
  - `abstain=true` triggered when: graph coverage < 30%, data staleness > 7 days, or query spans unindexed subgraph.
  - Backward compatible — existing MCP clients ignoring new fields continue to work.
- **Target Implementation:** `packages/eoip/agents/uncertainty_protocol.py` + MCP response schema update
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-KGR-G-019

**Acceptance criteria**
- [ ] The system SHALL embed a standardized uncertainty schema in every MCP tool response: confidence_score (float 0.0–1.0 reflecting data completeness, freshness, graph coverage), uncertainty_reason (explanation when confidence < 0.7), abstain (boolean when system cannot reliably answer), evidence_chain (array of source node/edge IDs used), and coverage_percent (fraction of relevant subspace consulted)
- [ ] Every MCP tool response includes all five schema fields with correct types
- [ ] confidencescore correlates with actual accuracy on a held-out evaluation set (Spearman ρ ≥ 0.6)
- [ ] abstain=true triggered when: graph coverage < 30%, data staleness > 7 days, or query spans unindexed subgraph
- [ ] Backward compatible — existing MCP clients ignoring new fields continue to work
- [ ] Target Implementation: packages/eoip/agents/uncertaintyprotocol.py + MCP response schema update
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/agents/uncertainty_protocol.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/uncertainty_protocol.py#L1-L1), [`scripts/update_phase3_wp31.py:66`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp31.py#L66-L66)
- tests: `tests/unit/test_uncertainty_protocol.py:13`, `tests/unit/test_uncertainty_protocol.py::test_coverage_and_staleness_sensors`, `tests/unit/test_uncertainty_protocol.py::test_uncertainty_protocol_abstain_on_no_evidence`, `tests/unit/test_uncertainty_protocol.py::test_uncertainty_protocol_contradictions_and_staleness`, `tests/unit/test_uncertainty_protocol.py::test_uncertainty_protocol_high_confidence`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-KGR-G-014 [P1] KGR-G-014: Streaming Temporal Agent Memory (Dual-Timeline Incremental Updates)

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:482-491` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.2 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-014: Streaming Temporal Agent Memory (Dual-Timeline Incremental Updates)
- **Classification:** AI / Agentic | **Priority:** P1 (Enterprise)
- **Description:** The system SHALL extend AGAM (MS-8) with a streaming real-time update path that processes agent interaction events continuously without batch recomputation, storing each fact with dual-timeline indexing: `event_time` (when the event occurred) and `ingestion_time` (when the system recorded it). Enables AI agents to query "what did the system know at time T?" vs "what actually happened at time T?" — critical for incident response.
- **Verification Criteria:**
  - Streaming agent events reflected in graph within < 500ms of arrival without triggering full rebuild.
  - Point-in-time queries using `(event_time=T1, ingestion_time=T2)` coordinates return correct facts.
  - Memory throughput: ≥ 500 agent events/second sustained ingestion rate.
  - Backward compatible with existing AGAM salience decay.
- **Target Implementation:** `packages/eoip/moonshot/streaming_agent_memory.py` + extension to `neuro_symbolic_memory.py`
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-KGR-G-014

**Acceptance criteria**
- [ ] The system SHALL extend AGAM (MS-8) with a streaming real-time update path that processes agent interaction events continuously without batch recomputation, storing each fact with dual-timeline indexing: event_time (when the event occurred) and ingestion_time (when the system recorded it). Enables AI agents to query "what did the system know at time T?" vs "what actually happened at time T?" — cri
- [ ] Streaming agent events reflected in graph within < 500ms of arrival without triggering full rebuild
- [ ] Point-in-time queries using (eventtime=T1, ingestiontime=T2) coordinates return correct facts
- [ ] Memory throughput: ≥ 500 agent events/second sustained ingestion rate
- [ ] Backward compatible with existing AGAM salience decay
- [ ] Target Implementation: packages/eoip/moonshot/streamingagentmemory.py + extension to neurosymbolicmemory.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/agents/memory.py:307`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/agents/memory.py#L307-L307), [`packages/eoip/moonshot/streaming_agent_memory.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/moonshot/streaming_agent_memory.py#L1-L1), [`scripts/update_phase3_wp31.py:5`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp31.py#L5-L5)
- tests: `tests/unit/test_streaming_agent_memory.py:14`, `tests/unit/test_streaming_agent_memory.py::test_streaming_agent_memory_conflict_resolution`, `tests/unit/test_streaming_agent_memory.py::test_streaming_agent_memory_decay_and_pruning`, `tests/unit/test_streaming_agent_memory.py::test_streaming_agent_memory_dual_timeline_indexing`, `tests/unit/test_streaming_agent_memory.py::test_streaming_agent_memory_integration`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-KGR-G-015 [P1] KGR-G-015: LLM-Assisted Dynamic Ontology Induction with Anti-Drift Guards

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:492-501` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 3, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-015; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.2 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-015: LLM-Assisted Dynamic Ontology Induction with Anti-Drift Guards
- **Classification:** Functional / AI | **Priority:** P1 (Enterprise)
- **Description:** The system SHALL extend MS-10 (Generative Studio) to ingest unstructured text corpora (engineering wikis, architecture documents, meeting transcripts, incident post-mortems) and jointly extract entities and induce OWL/SHACL schema classes using a local LLM. The pipeline SHALL enforce: (a) type consolidation guard — merge semantically equivalent induced types into existing ontology classes; (b) SHACL validation gate — reject induced schemas violating existing constraints; (c) human review queue — route low-confidence inductions (< 0.6) for ontologist approval before persistence.
- **Verification Criteria:**
  - Induces entity types and relationships from a 50-page technical whitepaper with ≥ 80% semantic alignment to a human-curated reference schema.
  - Type consolidation guard prevents ontology sprawl — induced type count grows ≤ 20% per corpus batch.
  - SHACL validation gate rejects 100% of schema violations before persistence.
  - Full pipeline operates air-gapped with local LLM (no cloud API calls).
- **Target Implementation:** `packages/eoip/moonshot/ontology_induction.py` + extension to `generative_studio.py`
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-KGR-G-015

**Acceptance criteria**
- [ ] The system SHALL extend MS-10 (Generative Studio) to ingest unstructured text corpora (engineering wikis, architecture documents, meeting transcripts, incident post-mortems) and jointly extract entities and induce OWL/SHACL schema classes using a local LLM. The pipeline SHALL enforce: (a) type consolidation guard — merge semantically equivalent induced types into existing ontology classes; (b) SHA
- [ ] Induces entity types and relationships from a 50-page technical whitepaper with ≥ 80% semantic alignment to a human-curated reference schema
- [ ] Type consolidation guard prevents ontology sprawl — induced type count grows ≤ 20% per corpus batch
- [ ] SHACL validation gate rejects 100% of schema violations before persistence
- [ ] Full pipeline operates air-gapped with local LLM (no cloud API calls)
- [ ] Target Implementation: packages/eoip/moonshot/ontologyinduction.py + extension to generativestudio.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/moonshot/ontology_induction.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/moonshot/ontology_induction.py#L1-L1), [`scripts/update_phase3_wp31.py:19`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp31.py#L19-L19)
- tests: `tests/unit/test_ontology_induction.py:22`, `tests/unit/test_ontology_induction.py::test_ontology_induction_anti_drift_validation`, `tests/unit/test_ontology_induction.py::test_ontology_induction_from_text`, `tests/unit/test_ontology_induction.py::test_ontology_type_consolidation`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-KGR-G-018 [P1] KGR-G-018: Massively Parallel Deep Multi-Hop Analytics Engine (5+ Hops)

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:522-531` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-018; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.2 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-018: Massively Parallel Deep Multi-Hop Analytics Engine (5+ Hops)
- **Classification:** Performance / Analytics | **Priority:** P1 (Enterprise)
- **Description:** The system SHALL provide a parallel sparse-matrix deep analytics engine using SciPy sparse CSR/CSC matrix operations and NumPy vectorized kernels to execute 5–10 hop traversal and analytics algorithms on 1M+ node graphs. Target use cases: fraud ring detection, AML path discovery, supply chain dependency chains, and blast-radius cascade simulations.
- **Verification Criteria:**
  - 5-hop BFS on a 1M-node graph completes in < 500ms on a single CPU core.
  - 7-hop reachability matrix computation for fraud ring detection on 500K nodes in < 2.0 seconds.
  - Results numerically equivalent to single-threaded baseline (deterministic).
  - CPU cores saturated via `multiprocessing.Pool` partitioned subgraph decomposition.
- **Target Implementation:** `packages/eoip/analytics/parallel_multihop.py` + integration into `algorithms.py`
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-KGR-G-018

**Acceptance criteria**
- [ ] The system SHALL provide a parallel sparse-matrix deep analytics engine using SciPy sparse CSR/CSC matrix operations and NumPy vectorized kernels to execute 5–10 hop traversal and analytics algorithms on 1M+ node graphs. Target use cases: fraud ring detection, AML path discovery, supply chain dependency chains, and blast-radius cascade simulations.
- [ ] 5-hop BFS on a 1M-node graph completes in < 500ms on a single CPU core
- [ ] 7-hop reachability matrix computation for fraud ring detection on 500K nodes in < 2.0 seconds
- [ ] Results numerically equivalent to single-threaded baseline (deterministic)
- [ ] CPU cores saturated via multiprocessing.Pool partitioned subgraph decomposition
- [ ] Target Implementation: packages/eoip/analytics/parallelmultihop.py + integration into algorithms.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/analytics/parallel_multihop.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/analytics/parallel_multihop.py#L1-L1), [`scripts/update_phase3_wp31.py:54`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp31.py#L54-L54)
- tests: `tests/unit/test_parallel_multihop.py:12`, `tests/unit/test_parallel_multihop.py::test_from_graph_store`, `tests/unit/test_parallel_multihop.py::test_influence_propagation`, `tests/unit/test_parallel_multihop.py::test_parallel_multihop_bfs_deep_traversal`, `tests/unit/test_parallel_multihop.py::test_sparse_graph_builder_and_csr`, `tests/unit/test_parallel_multihop.py::test_subgraph_partitioning_and_fraud_ring_detector`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-KGR-G-020 [P1] KGR-G-020: Real-Time Graph Mutation Streaming & Webhook Notification

- **Source:** `EOIP-engg-doc-pkg/KGR-g-requirements.md:542-555` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 4, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-KGR-G-020; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.2 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### KGR-G-020: Real-Time Graph Mutation Streaming & Webhook Notification
- **Classification:** Integration / Operational | **Priority:** P1 (Enterprise)
- **Description:** The system SHALL expose a real-time streaming interface for graph mutation events using Server-Sent Events (SSE) or WebSocket protocol, emitting structured change events (node_created, node_updated, node_deleted, edge_created, edge_deleted) with full metadata. Subscribers SHALL filter streams by entity label, property patterns, or subgraph scope. An optional webhook push notification service SHALL deliver filtered mutation events to registered HTTP endpoints within 1 second.
- **Verification Criteria:**
  - End-to-end latency from graph mutation to SSE client delivery < 100ms at P95.
  - Subscriber filter expressions correctly include/exclude events for ≥ 1,000 concurrent subscribers.
  - Webhook delivery achieves ≥ 99.5% success rate with exponential backoff retry (3 attempts).
  - Air-gapped capable — operates without external message broker (no Kafka dependency in default mode).
- **Target Implementation:** `packages/eoip/streaming/mutation_stream.py` + `api/v1/stream.py`

---

---
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-KGR-G-020

**Acceptance criteria**
- [ ] The system SHALL expose a real-time streaming interface for graph mutation events using Server-Sent Events (SSE) or WebSocket protocol, emitting structured change events (node_created, node_updated, node_deleted, edge_created, edge_deleted) with full metadata. Subscribers SHALL filter streams by entity label, property patterns, or subgraph scope. An optional webhook push notification service SHALL
- [ ] End-to-end latency from graph mutation to SSE client delivery < 100ms at P95
- [ ] Subscriber filter expressions correctly include/exclude events for ≥ 1,000 concurrent subscribers
- [ ] Webhook delivery achieves ≥ 99.5% success rate with exponential backoff retry (3 attempts)
- [ ] Air-gapped capable — operates without external message broker (no Kafka dependency in default mode)
- [ ] Target Implementation: packages/eoip/streaming/mutationstream.py + api/v1/stream.py
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/streaming/mutation_stream.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/streaming/mutation_stream.py#L1-L1), [`scripts/update_phase3_wp31.py:77`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_phase3_wp31.py#L77-L77)
- tests: `tests/unit/test_mutation_stream.py:12`, `tests/unit/test_mutation_stream.py::test_mutation_event_bus_sse_delivery_and_replay`, `tests/unit/test_mutation_stream.py::test_mutation_event_sse_and_serialization`, `tests/unit/test_mutation_stream.py::test_subscription_filter`, `tests/unit/test_mutation_stream.py::test_webhook_registration`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

