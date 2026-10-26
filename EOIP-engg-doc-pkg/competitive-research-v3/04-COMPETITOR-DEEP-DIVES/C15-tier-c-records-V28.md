# C15 — Tier C records (batch V28)

Verified 2026-10-26 (brief date 2026-10-18). Worker V28 (W27 scope). The older file `C15-tier-c-records.md` is untouched.

### T-C15-kythe — Kythe

| Field | Value |
|---|---|
| Official URL | https://kythe.io ; https://github.com/kythe/kythe (old `google/kythe` redirects) |
| Owner | Kythe team (originated at Google) and contributors |
| Latest version + date | v0.0.76, 2026-07-16 (GitHub releases API) |
| Status | Active (last push 2026-09-18) |
| Licence + class | Apache-2.0, permissive |
| Deployment | self-hosted tools and server; build-integrated indexers |
| Air-gap viable | yes (no cloud dependency evidenced) |
| Tier reason | Cross-reference graph standard, predecessor idea to SCIP |

Relevance: language-agnostic graph schema (nodes, edges, facts) plus indexers and a self-contained cross-reference server; grew out of Google's internal index. The overview page names C++ and Java indexers and "soon" Go and looks dated; current coverage NOT PUBLICLY VERIFIED. For EOIP it is a schema design reference; SCIP (C15-scip-lsif.md) is the lighter, better ingestion target. CAP-66, CAP-67.

**Decision:** REFERENCE-ONLY — schema ideas only; ingest via SCIP, not Kythe.

| CLAIM | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-kythe-01 | Kythe v0.0.76 | repo kythe/kythe, Apache-2.0, release 2026-07-16, pushed 2026-09-18 | Observed | GitHub API https://api.github.com/repos/google/kythe (redirect) | 2026-07-16 / 2026-10-26 | 0.85 | none |
| CLAIM-kythe-02 | overview page (undated) | graph schema, Google origin, C++/Java indexers, self-contained xref server | Officially documented | https://kythe.io/docs/kythe-overview.html | n/a / 2026-10-26 | 0.7 (page dated) | current indexer list may differ |

### T-C15-lsp — Language Server Protocol ecosystems

| Field | Value |
|---|---|
| Official URL | https://microsoft.github.io/language-server-protocol/ ; https://github.com/microsoft/language-server-protocol |
| Owner | Microsoft (spec); servers by many language communities |
| Latest version + date | Spec 3.18 current, 3.19 "upcoming"; 3.18 release date NOT PUBLICLY VERIFIED |
| Status | Active (spec repo pushed 2026-10-20) |
| Licence + class | Spec repo CC-BY-4.0; language servers vary, UNVERIFIED |
| Deployment | local processes, JSON-RPC 2.0 |
| Air-gap viable | yes |
| Tier reason | Protocol; the live-query counterpart to batch index formats |

Relevance: definition, references, call hierarchy, semantic tokens and workspace symbols from a live language server holding project state. Good for current answers on a dirty working tree; weak as an index (warmed server per language/project, no cross-repo identity). LSIF, its offline dump, is deprecated by Sourcegraph (C15-scip-lsif.md). For EOIP: optional read-only enrichment, never a mutation path (BL-23); batch truth from SCIP/tree-sitter (BL-42). CAP-66, CAP-59.

**Decision:** INTEGRATE (optional) — on-demand LSP lookups as read-only enrichment; not the system of record.

| CLAIM | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-lsp-01 | LSP 3.17 page | 3.17 labelled previous; 3.18 current, 3.19 upcoming; JSON-RPC with Content-Length header; definition/references/call hierarchy/semantic tokens/workspace symbol | Officially documented | https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/ | n/a / 2026-10-26 | 0.85 | none |
| CLAIM-lsp-02 | spec repo | CC-BY-4.0, pushed 2026-10-20 | Observed | https://api.github.com/repos/microsoft/language-server-protocol | 2026-10-20 / 2026-10-26 | 0.85 | none |
