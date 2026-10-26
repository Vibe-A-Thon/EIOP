# C15 - CodeGraph (colbymchenry/codegraph)

| Field | Value |
|---|---|
| Registry ID | T-C15-codegraph |
| Tier | B - named code-graph tool; strongest local incremental-index design among the named five |
| Versions examined | v1.6.2 (2026-10-03); repo pushed 2026-10-24; README at `main` |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V29 |

## 1. Identity, status, tier, sources

Name collision (Master Prompt 5.7). Candidates, GitHub search API 2026-10-26 [CLAIM-codegraph-01]:

| Repo | Stars | Last push | Licence | Description |
|---|---|---|---|---|
| **colbymchenry/codegraph** | ~75.4k | 2026-10-24 | MIT | pre-indexed code knowledge graph, auto-sync, MCP for Claude Code/Codex/Cursor etc., 100% local |
| CodeGraphContext/CodeGraphContext | ~4.4k | 2026-10-22 | MIT | MCP server + CLI indexing code into a graph database |
| Jakedismo/codegraph-rust | ~0.9k | 2026-10-12 | none stated | Rust code graphRAG, SurrealDB |
| xnuinside/codegraph | ~0.5k | 2026-05-19 | MIT | static Python dependency graph, HTML |
| codegraph-ai/CodeGraph | 132 | 2026-10-06 | Apache-2.0 | semantic graph over MCP |
| optave/ops-codegraph-tool | 99 | 2026-10-24 | Apache-2.0 | function-level graph, 34 languages |

**Registry means colbymchenry/codegraph** (most adopted by an order of magnitude; the only one the Master Prompt's agent-tool context fits). CodeGraphContext is the credible graph-database variant and is recorded as a counterexample (ADD not proposed; low adoption). Star figures from API only [CLAIM-codegraph-02].

## 2. Problem and workloads

Agents "stop crawling files and answer from the graph": architecture questions, callers/callees, impact before edit. Workflow: `codegraph install` (wires agents), `codegraph init -i` (index), auto-sync daemon, MCP tools `codegraph_explore`, `_search`, `_callers`, `_callees`, `_impact`, `_node`, `_files`, `_status` [CLAIM-codegraph-03].

## 3. Feature inventory

| Feature | Status |
|---|---|
| 20 languages via native Rust kernel; 34 listed incl. COBOL, Terraform, Vue; per-file fallback | present |
| Cross-file reference resolution (calls, imports, inheritance) | present |
| Framework route nodes (17 frameworks), cross-language bridges (Swift/ObjC, React Native, Expo) with `resolvedBy` metadata | present |
| FTS5 full-text search | present |
| File watcher, 300 ms debounce, per-file staleness banner in MCP responses | present |
| Embedding/semantic search | absent in README (UNVERIFIED) |
| Multi-user, ACL, tenancy | absent |
| Temporal history / git lineage | absent |

## 4. Architecture

```
agent <-MCP/CLI-> codegraph daemon (one writer per project)
   watcher -> Rust tree-sitter kernel -> extract -> resolve
   -> .codegraph/codegraph.db  (SQLite WAL, FTS5: symbols, edges, files)
```

## 5. Reconstruction

Data model: nodes (symbol, file, route), edges (`calls`, `imports`, `references`, `navigates`, inheritance) with `metadata.resolvedBy` provenance on bridged hops. Storage: single SQLite file in WAL mode via `node:sqlite`, FTS5 index; concurrency: concurrent readers, exactly one writer (shared daemon) [CLAIM-codegraph-04]. Pipeline: extraction (parallel, cgroup-aware worker pools) then a resolution pass; parity of Rust output with the reference TS engine verified byte-for-byte on real repos (vendor). Incremental: watcher syncs only changed files, 0.3-0.4 s on 4.4k-27k files (vendor). Query: dense pre-assembled payloads (`explore` returns relevant source). Hypothesis: impact = bounded BFS over reverse edges. Security: local only; no authz.

## 6. Inferred requirements

One-writer index with WAL; staleness signalling to the consumer; provenance on resolved-by-heuristic edges; measurable edge-coverage metric ("fair coverage").

## 7. Performance and resource model

Vendor benchmark: 7 repos, 7 languages, Claude Code headless, median of 4 runs, re-measured 2026-08-05: 44% lower cost, 62% fewer tokens on average, up to 43 tool calls avoided [CLAIM-codegraph-05]. Vendor discloses the counter-finding: ~80% more retrieval context stays resident (VS Code 67k vs 18k tokens). Fail modes: SQLite on network shares/WSL (journal not WAL), second writer contention [CLAIM-codegraph-04]. No independent benchmark found.

## 8. Strengths

STR-codegraph-01 sub-second incremental sync with staleness banners. STR-codegraph-02 edge provenance (`resolvedBy`). STR-codegraph-03 published coverage metric and honest context-residency finding. STR-codegraph-04 single-file embedded store (one-node first).

## 9. Limitations

| Class | Finding |
|---|---|
| Algorithmic | tree-sitter + heuristic resolution, no compiler types; coverage per language varies (README publishes "fair coverage") |
| Operational | single writer; WAL unavailable on some filesystems |
| Friction | one project = one DB; no cross-repo graph beyond `projectPath` |
| Governance | no permissions, tenants, audit; MCP responses carry raw source |
| Evidence | all performance numbers vendor-run |

## 10. Deployment and licensing

MIT, bundled runtime (no Node required), air-gap viable. No copyleft; dependency licences of bundled grammars UNVERIFIED.

## 11. Delta vs EOIP

| Area | CodeGraph | EOIP |
|---|---|---|
| Languages | 20+ | BL-42: Python/TS (2) |
| Incremental | watcher, per-file | BL-42 `incremental_indexer.py`, plus BL-24 replay |
| Resolution | cross-file heuristic + framework bridges | `polyglot_linker.py` partial |
| Permissions | none | BL-18 Partial |
| Mutation path | writes own DB | BL-23 via SourceEvents |
| MCP | read tools only | BL-47 18 tools |

## 12. Cards

| ID | Card |
|---|---|
| STR-codegraph-01 | [CLAIM-codegraph-03,05] staleness banner when index lags; **match**; test: edit file, query within debounce, response flags file as pending |
| STR-codegraph-02 | `resolvedBy` provenance; **match** into BL-41 evidence on code edges; test: every cross-language edge has resolver id |
| STR-codegraph-03 | published coverage metric; **match** as CAP-78 harness item |
| INV-codegraph-01 | Target v1.6.2, multi-agent shared repo. Limitation: no source ACL, MCP returns verbatim source [CLAIM-codegraph-03]; cause governance (proven). Options: (a) wrap behind EOIP MCP with ACL filter; (b) native per-file permission on code nodes; (c) ACL-aware graph with path-level policy. Selected (b) tied to BL-18. Benchmark: user lacking repo read gets 0 symbols, source snippets and impact paths. Defensibility: permission-preserving digital thread. ADOPT. |
| INV-codegraph-02 | One-writer SQLite per project; cross-repo impact impossible [CLAIM-codegraph-04]; cause storage (proven). EOIP keeps graph in backend-neutral store; cross-repo edges via polyglot linker. ADOPT (already differentiated). No 10.5 seed applies. |

## 13. Decisions

CAP-67 incremental re-index: EXPERIMENT (match watcher+staleness). CAP-66: INTEGRATE alternative - run CodeGraph as an optional external extractor feeding SourceEvents? DEFER (MIT licence fine, but its DB is not an event source). CAP-69 impact digital thread: BUILD (cross-source). CAP-59: REFERENCE. Product: REFERENCE-ONLY.

## 14. Tests/POC

Index a 3-language fixture with both; compare caller recall on 100 labelled call sites; edit-to-visible latency p95 under 2 s; accept staleness flag correct on 100% of pending edits.

## 15. Risks

Licence of bundled grammars; vendor benchmark may not transfer; Rust-kernel binary provenance for air-gapped supply chain (CAP-79). Open: does byte-parity hold for new languages?

## Appendix A - Dimensions

| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | MIT, active, solo-owner lineage |
| D2 | 2 | agent context |
| D3 | 4 | daemon+MCP+SQLite |
| D4 | 5 | SQLite WAL, FTS5 |
| D5 | 5 | typed node/edge kinds |
| D6 | 5 | N/A planner; BFS hypothesis |
| D7 | N/A | none |
| D8 | 5,9 | one writer |
| D9 | 3 | watcher incremental |
| D10 | 5 | resolvedBy only |
| D11 | 3 | no history |
| D12 | N/A | none |
| D13 | 2,7 | MCP tools |
| D14 | N/A | via agent |
| D15 | N/A | none |
| D16 | N/A | CLI |
| D17 | 3 | CLI, installer |
| D18 | 9 | no authz |
| D19 | 9 | none |
| D20 | 7 | vendor |
| D21 | 10 | free MIT |
| D22 | N/A | SQLite file |
| D23 | N/A | none found |
| D24 | 7 | vendor-run |

## Appendix B - Capabilities

| CAP | Tech | Claim | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-66 | partial | 03 | BL-42 | REFERENCE | P2 |
| CAP-67 | native | 04 | BL-42 | EXPERIMENT | P1 |
| CAP-69 | partial | 03 | BL-41/42 | BUILD | P1 |
| CAP-46 | absent | 03 | BL-18 | BUILD | P0 |
| CAP-59 | native | 03 | BL-47 | REFERENCE | P3 |

## Appendix C - Evidence

| ID | Product/date | Claim | Class | Source | Dates/conf | Contra |
|---|---|---|---|---|---|---|
| CLAIM-codegraph-01 | search API | candidate table | Officially documented | https://api.github.com/search/repositories?q=codegraph | 2026-10-26, 0.9 | none |
| CLAIM-codegraph-02 | repo | 75,365 stars, MIT, v1.6.2 2026-10-03 | Officially documented | https://github.com/colbymchenry/codegraph | 0.85 | blogs differ |
| CLAIM-codegraph-03 | README | tools, languages, install | Officially documented | same, README | 0.8 | Node requirement stated inconsistently by blogs |
| CLAIM-codegraph-04 | README | SQLite WAL, one writer, FTS5 | Officially documented | same | 0.8 | none |
| CLAIM-codegraph-05 | README | benchmark | Vendor claim | same | 0.4 | vendor notes +80% residual context |

## Appendix D - Assumptions

Registry "CodeGraph" = colbymchenry. Language count "20 (kernel) / 34 (listed)" taken from README as written.
