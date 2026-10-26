# C15 - Graphify (Graphify-Labs/graphify) and "Graphify Enterprise"

| Field | Value |
|---|---|
| Registry ID | T-C15-graphify |
| Tier | B - named code-graph tool; pattern source for confidence-labelled edges |
| Versions examined | v0.9.95 (2026-10-23), repo pushed 2026-10-23; README/ARCHITECTURE at `main` |
| Verified on | 2026-10-26 (brief date 2026-10-18; fetches ran 2026-10-26) |
| Worker | V29 |

## 1. Identity, current status, tier, sources

Name collision (Master Prompt 5.7). Candidates, GitHub API 2026-10-26 [CLAIM-graphify-01]:

| Repo | Stars | Last push | Licence | Description |
|---|---|---|---|---|
| **Graphify-Labs/graphify** (formerly safishamsi/graphify, API answers "Moved Permanently") | ~135.5k | 2026-10-23 | Apache-2.0 | codebase+docs+SQL+PDF to queryable knowledge graph; skill for Claude Code, Cursor, Codex, Gemini CLI |
| kbastani/graphify | 450 | 2020-04-04 | Apache-2.0, archived | Neo4j unmanaged extension, text classification |
| Graphitti/graphify, raufer/graphify | 108 / 98 | 2018 / 2023 | MIT / none | unrelated small libraries |
| elbruno/graphify-dotnet | 95 | 2026-07-01 | MIT | .NET port of the above |

**Registry means Graphify-Labs/graphify**: by far the most adopted code-knowledge-graph tool of that name; others are unrelated or ports. Star counts in third-party snippets varied 63k-80k; the API figure is used (growth plausible, UNVERIFIED independently) [CLAIM-graphify-02].

**"Graphify Enterprise" exists, early access only.** graphify.com/enterprise: "Early access", "Merge-gate verification, graph-aware review, and an engineering digest", "self-hosted in your VPC"; no pricing [CLAIM-graphify-03]. A third-party note (2026-09-15) lists an Enterprise tier with custom pricing and hosted tiers (Free 25k nodes, Pro $15/mo, Teams $29/seat) [CLAIM-graphify-04]. Not the UK vendor Graphifi (taxonomy tooling). Enterprise internals: NOT PUBLICLY VERIFIED.

## 2. Problem and workloads

Give coding agents a persistent, compact map of a mixed corpus (code, markdown, PDFs, images) instead of re-reading files. Workflows: `/graphify .`; `query`, `path`, `explain`; `--update` re-extraction; `--watch`; post-commit hook; exports to Obsidian, GraphML, Cypher, MCP stdio [CLAIM-graphify-05].

## 3. Feature inventory

| Feature | Status |
|---|---|
| Tree-sitter AST extraction for ~13 languages, call-graph second pass | present (deterministic, no LLM) |
| Docs/PDF/image concept extraction | present, uses the host assistant's model (egress) |
| Edge confidence EXTRACTED / INFERRED / AMBIGUOUS | present |
| Leiden communities, god nodes, "surprising connections" report | present |
| SHA256 cache, incremental `--update`, watcher, git hook | present |
| MCP stdio server, Neo4j Cypher export, GraphML | present |
| Multi-user server, ACLs, tenancy, audit | absent (Enterprise claims unverified) |
| SCIP/compiler-grade resolution | absent |

## 4. Architecture

```
files -> detect -> extract (tree-sitter | LLM) -> build_graph (NetworkX)
      -> cluster (Leiden) -> analyze -> report -> export (graph.json/html/obsidian)
state: graphify-out/ (graph.json, cache/) per user, no server
```

## 5. Under-the-hood reconstruction

Pipeline `detect -> extract -> build_graph -> cluster -> analyze -> report -> export`, stages exchange plain dicts and `nx.Graph`; extraction schema `{nodes[id,label,source_file,source_location], edges[source,target,relation,confidence]}` validated by `validate.py` [CLAIM-graphify-06]. Per-language extractor = tree-sitter parse, walk, then INFERRED `calls` pass. Storage is one JSON file; no query planner (graph traversal in NetworkX). Concurrency, versioning, security: file-level only; `security.py` validates URLs/paths. Hypothesis: confidence is assigned by extractor type, not calibrated.

## 7. Performance and resource model

Vendor claim: 71.5x fewer tokens per query on a 52-file mixed corpus (code, papers, images); 5.4x on 4 files; ~1x on 6 files, vendor states value scales with corpus size [CLAIM-graphify-07]. Methodology and hardware not independently reproduced. Failure modes: stale LLM-derived edges (doc changes only notify), whole-graph in memory.

## 8. Strengths

STR-graphify-01 confidence-tagged edges (match in EOIP, see 12). STR-graphify-02 deterministic AST path needs no LLM. STR-graphify-03 cheap hooks for freshness (watch, post-commit).

## 9. Limitations

| Class | Finding |
|---|---|
| Algorithmic | name-based call inference (INFERRED) without type resolution - hypothesis; no SCIP |
| Operational | in-memory NetworkX, single JSON file; scale beyond one repo unverified |
| Friction | built as a Claude Code skill; PyPI name `graphifyy` pending reclaim (vendor note) [CLAIM-graphify-05] |
| Governance | no permissions, tenants, audit in OSS core |
| Egress | doc/image extraction uses the assistant's model; data leaves unless local model |

## 10. Deployment, licensing, viability

Apache-2.0 core, local, air-gap viable for the AST path only. Enterprise terms unknown (legal review when GA). Hosted tiers are SaaS (excluded by constraint 1).

## 11. Delta vs EOIP baseline

| Area | Graphify | EOIP |
|---|---|---|
| Code symbols | ~13 languages, tree-sitter | BL-42: Python/TS, tree-sitter in 2 files |
| Edge confidence | 3-level label | BL-40 epistemic contract, not on code edges |
| Permissions | none | BL-18 Partial, BL-20 Partial |
| Governed mutation | none (writes file) | BL-23 connectors never mutate graph |
| Egress | assistant model | BL-45 gateway |

## 12. Cards

| ID | Card |
|---|---|
| STR-graphify-01 | [CLAIM-graphify-06] confidence-labelled edges; value: honest code-graph answers; **match**: map EXTRACTED/INFERRED/AMBIGUOUS onto BL-40 classes; test: every code edge in fixture repo carries class + extractor id |
| STR-graphify-02 | [CLAIM-graphify-05] LLM-free AST path; **match** (exists); test: air-gapped index run with network denied |
| INV-graphify-01 | Target v0.9.95 single-user graph.json. Limitation: no ACL/tenancy [CLAIM-graphify-05]. Cause: storage/governance (proven by README scope). Options: (a) export-only integration via a connector emitting SourceEvents; (b) native tenant-scoped code graph; (c) permission-propagating code graph with repo ACL per node. Selected (b)+(c) via BL-42 and BL-18 work. Benchmark: cross-tenant query returns 0 nodes on 2-tenant corpus. Defensibility: ACL-preserving digital thread. Decision ADOPT. |
| INV-graphify-02 | LLM semantic pass on docs causes egress [CLAIM-graphify-05]; cause: deployment (proven). Selected: route via egress gateway BL-45, local model default. Decision ADOPT. No Master Prompt 10.5 seed targets this tool. |

## 13. Per-capability decisions

CAP-66 precise code graph: REFERENCE (use SCIP route, see C15-scip-lsif). CAP-43/38 confidence labelling: BUILD (adopt pattern). CAP-59 MCP: DEFER (BL-47 exists). CAP-56 community/god-node report: EXPERIMENT. Product: REJECT as dependency (flat file, skill-centric); Enterprise: DEFER pending GA.

## 14. Tests/POC

3-language fixture; compare symbol/call recall with EOIP `codegraph` and SCIP truth; target EXTRACTED precision >= 0.95.

## 15. Risks and open questions

Enterprise scope and licence unknown; star-count volatility; skill-first design may drift. Open: does INFERRED precision hold on dynamic languages?

## Appendix A - Dimensions

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, active, Graphify Labs |
| D2 | 2 | agent context compaction |
| D3 | 4 | pipeline modules, no server |
| D4 | 5 | NetworkX + JSON |
| D5 | 5 | untyped relation strings + confidence |
| D6 | 5 | N/A traversal only |
| D7 | N/A | none |
| D8 | 5,9 | N/A single process |
| D9 | 3 | file cache, watch, hook |
| D10 | 12 | confidence label only |
| D11 | 3 | git hook, no history model |
| D12 | 3 | Leiden, centrality |
| D13 | 2 | MCP/skill |
| D14 | N/A | natural language via assistant |
| D15 | N/A | none |
| D16 | 3 | graph.html |
| D17 | 3 | CLI, skill |
| D18 | 9 | path validation only |
| D19 | 9 | absent |
| D20 | 7 | vendor token claims |
| D21 | 1,10 | free core, hosted tiers |
| D22 | 3 | GraphML, Cypher export |
| D23 | N/A | none found |
| D24 | 7 | vendor claims, unreproduced |

## Appendix B - Capability mapping

| CAP | Technology | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-66 | partial (heuristic) | 06 | BL-42 Implemented/Partial | REFERENCE | P2 |
| CAP-67 | native | 05 | BL-42 | REFERENCE | P3 |
| CAP-43 | partial | 06 | BL-40 | BUILD | P2 |
| CAP-51 | absent | 05 | BL-45 | REJECT | P3 |
| CAP-59 | native | 05 | BL-47 | DEFER | P3 |

## Appendix C - Evidence

| ID | Product/ver/date | Claim | Class | Source | Dates/conf | Contra |
|---|---|---|---|---|---|---|
| CLAIM-graphify-01 | repo list 2026-10-26 | candidates table | Officially documented | api.github.com/repos/Graphify-Labs/graphify and search API | 2026-10-26, 0.9 | search snippets: 63-80k stars |
| CLAIM-graphify-02 | same | 135,540 stars, Apache-2.0, v0.9.95 | Officially documented | GitHub API releases | 0.8 | snippet star counts |
| CLAIM-graphify-03 | Enterprise page | early access, VPC, no pricing | Officially documented | https://www.graphify.com/enterprise | 2026-10-26, 0.7 | #04 |
| CLAIM-graphify-04 | third-party | tiers and pricing | Third-party report | https://rywalker.com/research/graphify | 2026-09-15, 0.5 | page says "available" |
| CLAIM-graphify-05 | README | features, install, tech stack | Officially documented | https://github.com/Graphify-Labs/graphify | 2026-10-26, 0.8 | none |
| CLAIM-graphify-06 | ARCHITECTURE.md | pipeline, schema, labels | Observed in docs | raw.githubusercontent.com/Graphify-Labs/graphify/main/ARCHITECTURE.md | 0.8 | none |
| CLAIM-graphify-07 | README | token benchmark | Vendor claim | README | 0.4 | 1x on small |

## Appendix D - Assumptions

Registry "Graphify" = Graphify-Labs. API stars treated as true. Verification date 2026-10-26.
