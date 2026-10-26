# C17 — Obsidian

| Field | Value |
|---|---|
| Registry ID | T-C17-obsidian |
| Tier | B (local-first PKM; EOIP exports to it) |
| Versions examined | Desktop 1.15.0 (2026-10-22) per changelog fetch; 1.12.4 (2026-02-27) CLI release; Bases core plugin since 1.9.10 (2025-08-18) |
| Verified on | 2026-10-26 (brief said 2026-10-18; actual access date used) |
| Worker | V31 |

## 1. Identity, status, sources
Obsidian is a local-first Markdown knowledge-base app by Obsidian (Dynalist Inc., ownership UNVERIFIED). Active; latest desktop 1.15.0 on 2026-10-22 [CLAIM-obsidian-01]. Closed-source app, free for all purposes including commercial; Commercial and Catalyst licences are optional [CLAIM-obsidian-02]. Tier B: it is the consumer of an existing EOIP exporter.

## 2. Problem and workflows
Personal/team notes as plain files with `[[wikilinks]]`, backlinks, graph view, properties (YAML), Bases (database views over notes), Canvas, community plugins. Workflows relevant to EOIP: browse a generated vault; query with Dataview/Bases; add human annotations next to machine notes.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Vault = folder of Markdown files, `.obsidian` config | present [CLAIM-obsidian-03] |
| Wikilinks, backlinks, graph view | present [CLAIM-obsidian-03] |
| Properties/YAML, Bases | present (Bases core since 1.9.10) [CLAIM-obsidian-04] |
| CLI (terminal control) | present since 1.12.4 [CLAIM-obsidian-04] |
| Obsidian Sync (E2E, paid), headless sync client | present (paid) [CLAIM-obsidian-04] |
| Community plugins (incl. Dataview, Mermaid is built-in) | present; plugins not audited |
| Multi-user permissions / tenancy | absent |
| Open-source licence | absent (proprietary app) |

## 4. Architecture
```
 vault/ (*.md, attachments) --watch--> metadata cache (IndexedDB) --> graph view / backlinks / Bases
 vault/.obsidian (settings, plugins)      ^ external edits picked up automatically
 sync: Obsidian Sync | Git | Dropbox | iCloud
 EOIP: GraphStore -> ObsidianVaultExporter -> vault/<Label>/<name>.md (one way)
```

## 5. Under the hood
Plain-text files are the system of record; the metadata cache is derived and rebuildable [CLAIM-obsidian-03]. Links are name-based; renames update links inside the app only. No server component. Plugin API internals not examined.

EOIP exporter (verified in code, `packages/eoip/exporters/obsidian_vault.py`): one note per vertex under folder-by-label, YAML frontmatter, relationships as `[[links]]`, Mermaid subgraph, index and MOC notes; skips unchanged files by comparing content; overwrites changed notes with `write_text`. No ACL, tenant, or redaction references found in the file (grep for acl/permission/tenant/redact empty) [CLAIM-obsidian-05].

## 6. Requirements inferred
Exports need: stable filename-to-canonical-ID mapping (`canonical_id` in frontmatter), regeneration that preserves human-written sections, permission-filtered content, deterministic output, vault portability.

## 7. Performance and resource model
No benchmarks verified; large-vault behaviour UNVERIFIED. EOIP exporter issues per-vertex `edges_from`/`edges_to`/`get_vertex` calls (N+1 pattern in code), so cost grows with edge count; unmeasured.

## 8. Strengths
Plain files survive tool death; zero server; strong linking UX; works air-gapped; Bases/Dataview give no-code querying over exported metadata; huge plugin ecosystem.

## 9. Limitations
| Class | Item |
|---|---|
| Licensing | Closed-source app; free incl. commercial use but no redistribution right to embed the app [CLAIM-obsidian-02] (legal-review trigger for bundling) |
| Product | Single-user model; sync paid; graph view degrades on large vaults (hypothesis) |
| EOIP exporter | One-way, destructive on changed notes (user edits overwritten); no ACL filtering, so a vault copy can leak restricted facts [CLAIM-obsidian-05]; filename collisions possible after sanitisation |
| Friction | Sensitive data lands in files outside platform audit |

## 10. Deployment, licensing, viability
Desktop/mobile apps; no server; air-gap viable. EOIP should never bundle Obsidian; it only emits an open Markdown format. Plugin licences vary (legal review per plugin).

## 11. Delta vs baseline
Baseline has the exporter (KGR-G-003; not in the BL list) and collaboration annotations (BL-53). Gap: BL-18 (source-ACL enforcement) is Absent in retrieval; the same gap applies to this export path. No import-back of human edits as proposed claims.

## 12. Cards
STR-obsidian-01 | Obsidian | files-as-truth, link-first UX | CLAIM-03 | zero-install browsable output for customers | integrate | keep export open-format; add managed regions (`%% eoip:begin %%`) so user text survives | re-export after user edit loses zero user text.
INV-obsidian-01 | target EOIP exporter vs Obsidian vault | export bypasses permissions; root cause governance (proven by code reading) | alternative: export through the retrieval/ACL path per principal, per-tenant vault, audit entry per export; worse when full admin export is required. Options: quick = label allow-list; native = principal-scoped export plus manifest; long = bidirectional sync with annotations proposed as claims. Select native. POC: seed restricted vertices, export as low-privilege principal, grep vault for restricted IDs, metric zero hits. Defensibility: governance. Decision ADOPT. No seed hypothesis targets Obsidian.

## 13. Decisions
| Capability | Decision |
|---|---|
| Markdown/YAML vault export (CAP-70/71 adjacent) | REUSE existing exporter, harden |
| ACL-filtered export (CAP-46) | BUILD |
| Round-trip human annotations as PROPOSED claims (CAP-38) | EXPERIMENT |
| Bundling Obsidian | REJECT |

## 14. Tests
Permission-leak test; idempotent export (zero writes on second run); user-edit preservation; filename collision test; Bases/Dataview query smoke test on exported frontmatter.

## 15. Risks and open questions
Exfiltration through files; Obsidian ToS changes; Markdown dialect drift; whether Bases property schema should be emitted.

## Appendix A — Dimension coverage
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1 | app, licence |
| D2 | 2 | PKM |
| D3 | 4 | local app |
| D4 | 5 | files |
| D5–D8 | N/A | no graph engine, no reasoning |
| D9 | 4 | EOIP export |
| D10 | 5 | frontmatter lineage |
| D11 | 3 | sync only |
| D12–D14 | N/A | N/A |
| D15 | N/A | N/A |
| D16 | 3,8 | graph view |
| D17 | 3 | plugins, CLI |
| D18 | 9 | no ACL |
| D19 | N/A | single-user |
| D20 | 7 | UNVERIFIED |
| D21 | 9,10 | pricing |
| D22 | 5 | open format |
| D23 | N/A | not searched |
| D24 | 1 | version from changelog fetch |

## Appendix B — Capability mapping
| CAP | Obsidian | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-46 | absent | 05 | BL-18 Absent | BUILD | P0 |
| CAP-50 | native | 03 | n/a | REUSE | P3 |
| CAP-71 | partial (graph, Bases) | 04 | BL-54 Implemented | REFERENCE | P3 |
| CAP-38 | absent | 03 | BL-41 Implemented | EXPERIMENT | P2 |

## Appendix C — Evidence
| ID | Product/date | Claim | Class | Source | Access | Conf | Contra |
|---|---|---|---|---|---|---|---|
| obsidian-01 | 2026-10-22 | latest desktop 1.15.0 | Official (summarised fetch) | https://obsidian.md/changelog/ | 2026-10-26 | 0.6 | summary tool parse; recheck |
| obsidian-02 | 2026 | free for all purposes; commercial licence optional | Official | https://obsidian.md/license | 2026-10-26 | 0.85 | one aggregator says $50/user/yr |
| obsidian-03 | 2026 | vault = folder of Markdown; .obsidian config; metadata cache rebuildable | Official docs | https://obsidian.md/help/Files+and+folders/How+Obsidian+stores+data | 2026-10-26 | 0.9 | none |
| obsidian-04 | 2025-08-18 to 2026-02-27 | Bases core 1.9.10; CLI and headless Sync 2026-02-27 | Official changelog (search summary) | https://obsidian.md/changelog/2026-02-27-desktop-v1.12.4/ | 2026-10-26 | 0.6 | none |
| obsidian-05 | repo HEAD (dev_local) | exporter code behaviour | Source code | F:\code\EIP\EIOP\packages\eoip\exporters\obsidian_vault.py | 2026-10-26 | 0.9 | n/a |

## Appendix D — Assumptions
Owner of Obsidian not verified. Dataview/Mermaid behaviour assumed standard. Access date 2026-10-26.
