# C15 — Tree-sitter (incremental parser generator and runtime)

| Field | Value |
|---|---|
| Registry ID | T-C15-tree-sitter |
| Tier | A — parser reuse for BL-42; the open syntactic layer under almost every modern code-graph tool |
| Versions examined | tree-sitter core v0.27.1 (marked Latest, 08 Oct 2026 per release page; asset timestamps 2026), v0.27.0 (30 Aug 2026, breaking), v0.26.13 (23 Aug), a rolling "nightly" pre-release dated 25 Oct. `py-tree-sitter` on PyPI: `info.version` read as 0.26.0 via a summarised fetch (confidence 0.5); `requires_python >=3.10`, MIT |
| Verified on | 2026-10-18 (brief date; fetches ran 2026-10-26) |
| Worker | V09 (W27 scope) |

## 1. Identity, current status, tier, and sources

| Item | Finding | Claim |
|---|---|---|
| What | "An incremental parsing system for programming tools": a parser generator CLI plus a dependency-free C runtime embeddable anywhere | [CLAIM-tree-sitter-01] |
| Owner / governance | `tree-sitter` GitHub organisation; creator Max Brunsfeld (copyright 2018); contributors list not shown on the page; formal governance NOT PUBLICLY VERIFIED | [CLAIM-tree-sitter-02] |
| Activity | 27.3k stars, 3.0k forks, 6,670 commits on the repo page; releases roughly monthly in 2026 (0.26.12 on 08 Aug, 0.26.13 on 23 Aug, 0.27.0 on 30 Aug, 0.27.1 on 08 Oct) | [CLAIM-tree-sitter-03] |
| Licence | MIT (core). `py-tree-sitter` MIT. Grammar licences vary per repository: UNVERIFIED per grammar | [CLAIM-tree-sitter-02][CLAIM-tree-sitter-05] |
| Status | active, production (embedded in editors and code-intel tools) | [CLAIM-tree-sitter-03] |
| Breaking-change cadence | 0.27.0: `Node::child_count` now `u32`, Rust crate edition 2024, MSRV 1.90; 0.27.1 fixes UTF-16 surrogate decoding and query capture ranges | [CLAIM-tree-sitter-03] |
| Name collision | none material; distinct from Sourcegraph's `syntect` highlighter and from GitHub stack-graphs (which builds on Tree-sitter, separate entry) | |

## 2. Primary problem, target workloads, concrete example workflows

Problem: get a concrete syntax tree for any language, fast enough to re-parse on every keystroke, robust to syntax errors, with a uniform query API. Workloads: editor highlighting/folding/navigation, code chunking for RAG, symbol/definition extraction, structural search, and linters.

| Workflow | Use | EOIP journey |
|---|---|---|
| Re-parse changed file after a commit, diff old/new trees, emit changed symbols | incremental + `changed_ranges` | J1, J10 |
| Extract function/class/import nodes for Java, Go, Rust where EOIP has no parser | query files per language | J9 |
| Chunk source for retrieval along AST boundaries | tree walk | J9 |
| Map a diff hunk to enclosing symbol | byte-range -> `descendant_for_byte_range` | J1 |

## 3. Feature inventory

| Feature | Status | Surface | Claim |
|---|---|---|---|
| Incremental parse (edit + reparse with old tree, shared structure) | present | C API `ts_tree_edit`, `ts_parser_parse`; Python `tree.edit`, `parser.parse(src, old_tree)` | [CLAIM-tree-sitter-04][CLAIM-tree-sitter-05] |
| Changed ranges between trees | present | `ts_tree_get_changed_ranges`; Python `tree.changed_ranges(new_tree)` | [CLAIM-tree-sitter-05] |
| Error recovery (`ERROR`, `MISSING` nodes) | present | tree + query patterns `(ERROR)`, `(MISSING ";")` | [CLAIM-tree-sitter-06] |
| Query language (S-expressions) | present: node patterns, fields, negated fields `!field`, anonymous nodes, wildcards `_`/`(_)`, supertypes, `@captures` | `Query`, `QueryCursor.captures/matches` | [CLAIM-tree-sitter-06][CLAIM-tree-sitter-05] |
| Quantifiers, alternations, anchors, predicates `#eq? #match?` | present per Tree-sitter docs, not on the page read here | | [CLAIM-tree-sitter-06] (0.7) |
| Multi-language documents (included ranges) | present | `ts_parser_set_included_ranges` | [CLAIM-tree-sitter-04] |
| Cheap tree copy, thread note: tree not thread-safe, copy per thread | present | `ts_tree_copy` (atomic refcount) | [CLAIM-tree-sitter-04] |
| Official bindings | Go, Java, JavaScript (Node), Kotlin, Python, Rust, Zig | | [CLAIM-tree-sitter-04] |
| Python bindings | `pip install tree-sitter`, precompiled wheels, no library deps; grammars separate (`tree-sitter-python` etc.) | | [CLAIM-tree-sitter-05] |
| Highlighting / tags libraries | present (UTF-16 support in highlighting since 0.27.0) | | [CLAIM-tree-sitter-03] |
| Semantic resolution (types, cross-file references) | **absent** by design: syntactic only | | reasoned, 0.9 |
| Symbol identity across repos/revisions | absent | | reasoned |

## 4. Architecture diagram

```
 grammar.js (DSL)                         source text (bytes) + old tree + TSInputEdit list
     |  tree-sitter generate                       |
     v                                             v
 [Parser generator: LR(1) tables with GLR conflict handling, lexer DFA, external scanner hook]
     |  emits parser.c  (language tables + optional scanner.c)       RUNTIME (pure C, lib/src)
     +------------------------------------> [Lexer] --tokens--> [GLR stack, multiple versions]
                                                  ^                 |  reuse old subtrees (reusable node cursor)
                                                  |                 v
                                           [Error recovery]    [Subtree store: immutable, refcounted, shared across trees]
                                                                    |
                                       Tree (root, positions)  --> [TreeCursor | Node API | Query engine | changed_ranges]
 Bindings (Rust, Python, Node, Go, Java, Kotlin, Zig, WASM) wrap the C API.
 State: in-memory only; no persistence, no network. Control plane: caller. Data plane: tree.
```

## 5. Under-the-hood reconstruction

Basis: public API docs read this session [CLAIM-tree-sitter-04/05], plus knowledge of the C sources `lib/src/parser.c`, `subtree.c`, `reusable_node.h`, `get_changed_ranges.c`, `query.c`, `lexer.c`. The repo page confirmed `lib/` and `crates/` exist but not file contents, so **internal details below are hypothesis grade 0.6; pin to tag v0.27.1 and verify before relying on them.** The design follows Wagner and Graham style incremental parsing: reuse unchanged subtrees; re-lex and re-parse only the damaged region.

**5.1 Data model.** Immutable, reference-counted `Subtree` nodes (leaf tokens and internal nodes) storing *padding* (whitespace before) and *size* (bytes and row/column extent) rather than absolute offsets; absolute positions are computed when navigating. Flags: named/visible/extra/missing, `has_changes`, `fragile_left/right`, error cost, parse state. Because nodes are relative and immutable, one subtree can sit in many trees (cheap `tree_copy` via atomic refcount [CLAIM-tree-sitter-04]).

**5.2 Grammar to tables.** `grammar.js` -> JSON -> LR(1) item sets with precedence/associativity and declared `conflicts`. Conflicts that remain become GLR split points (the runtime forks the stack). Lexing is context-aware: each parse state has its own valid-token set, so the DFA is run per state; `externals` give hand-written scanners for indentation (Python), heredocs, template strings.

**5.3 Incremental re-parse (reconstruction).**
```
# 1. caller applies text edit, then tells the old tree
tree.edit(start_byte, old_end_byte, new_end_byte, start_point, old_end_point, new_end_point)   # [CLAIM-tree-sitter-04/05]
   -> walk root->leaf along the edited range; for each overlapping subtree: shift start/size by delta,
      set has_changes = true  (siblings after the edit just have padding/offset adjusted lazily)

# 2. reparse using old tree as hint
new_tree = parser.parse(read_callback, old_tree)
   init ReusableNode cursor at old_tree.root
   loop until accept:
      for each active stack version v (GLR):
          pos = v.position
          # try reuse
          cand = reusable_node.at(pos)               # old subtree that starts exactly at pos
          while cand:
              if cand.has_changes or cand.is_error or cand.is_missing or cand.fragile or
                 cand.parse_state != v.state (when not a token) or
                 not table_has_action(v.state, cand.first_leaf_symbol) or
                 cand.extends_past_included_range_boundary:
                  cand = reusable_node.descend_into_children()   # break the node down, try its children
                  continue
              push cand as a whole onto v (goto on its symbol)  # skip its entire byte span without lexing
              reusable_node.advance_past(cand); break
          if nothing reusable: lex next token (also reuse old *token* if unchanged and lex state compatible),
              look up action: SHIFT / REDUCE / (multiple -> fork version) / ERROR -> recovery
      periodically merge versions with identical state+position, drop versions whose error cost is worse
# 3. diff
ranges = old_tree.changed_ranges(new_tree)   # tree walk comparing structure/sizes, yields syntactic ranges whose subtree differs
```
Result: work is O(size of edit + depth) plus the re-lexed/re-reduced frontier, not O(file) (claimed behaviour; vendor statement of the design goal, not a benchmark). `changed_ranges` is *syntactic* (nodes whose structure changed), usually narrower than the textual edit extents.

**5.4 Error recovery.** On a token with no action, the runtime tries (a) inserting a `MISSING` token if that makes the lookahead valid, (b) skipping tokens into an `ERROR` node, (c) popping stack states to find one that accepts the lookahead; versions are scored with a cost = skipped bytes/nodes/missing tokens and the cheapest survives. `ERROR`/`MISSING` are queryable [CLAIM-tree-sitter-06] and 0.26.13 fixed wide error nodes on unparseable input [CLAIM-tree-sitter-03].

**5.5 Query engine.** A pattern compiles to a state machine over tree-cursor moves; the cursor walks the subtree once while advancing many partial matches in parallel (steps with field, symbol, capture ids, quantifier and anchor flags). Predicates (`#eq?`, `#match?`) are evaluated by the host binding after structural match, not inside C core (hypothesis 0.6). Captures are returned in document order.

**5.6 Concurrency.** Tree instances not thread-safe; copy per thread [CLAIM-tree-sitter-04]. Parser objects are single-threaded. A cancellation/timeout hook exists in the parse API (recalled; verify, 0.5).

**5.7 Storage / versioning / security.** None: library only. No persistence, no permissions. Security surface = untrusted input to C parsers and external scanners (memory safety bugs possible; grammar scanners are C by rule [CLAIM-tree-sitter-07]); parse with timeouts and size limits.

**5.8 Mapping to symbols (what EOIP must add).** Tree-sitter yields *definitions* and *syntactic references* only. To produce stable symbol IDs: derive `(language, repo, path, qualified-name-from-enclosing-scopes, kind, arity/signature-text)`; resolve imports by file path and module system; mark each edge `resolution=syntactic`, never `semantic`. This is the exact boundary where SCIP indexers take over (see C15-scip-lsif).

## 6. Functional and non-functional requirements inferred

| ID | Requirement | Basis |
|---|---|---|
| FR-1 | Re-parse in-place from byte edits, returning changed ranges | [CLAIM-tree-sitter-04/05] |
| FR-2 | Query-driven extraction without code changes per language (query files as data) | [CLAIM-tree-sitter-06] |
| FR-3 | Tolerate broken code (partial files in diffs) | [CLAIM-tree-sitter-06] |
| FR-4 | Node range -> file/line/column with encoding awareness (UTF-8 bytes, UTF-16 option) | [CLAIM-tree-sitter-03/05] |
| NFR-1 | Zero runtime network access; grammar compiled to native/WASM lib, installable offline from wheel mirrors | [CLAIM-tree-sitter-01/05] |
| NFR-2 | Per-grammar licence check recorded in an SBOM | [CLAIM-tree-sitter-07] |
| NFR-3 | Pin grammar and core ABI versions together (language ABI version must match runtime) | recalled 0.6 |

## 7. Performance and resource model

No benchmark retrieved; **NOT PUBLICLY VERIFIED** here. Model: memory proportional to the syntax tree (node count x subtree size, shared across edits); incremental reparse cost proportional to edited region and tree depth (design intent). Failure modes: error-recovery cascades on unparseable files produce wide `ERROR` nodes (fixed partially in 0.26.13 [CLAIM-tree-sitter-03]); GLR ambiguity blow-up in poorly written grammars; external scanners being the main source of crashes; ABI mismatch between prebuilt grammar wheels and the core. EOIP must measure (section 14).

## 8. Strengths and use-case-specific advantages

| ID | Strength | Match / exceed approach |
|---|---|---|
| STR-tree-sitter-01 | One uniform tree + query API across hundreds of languages (about 650 parser entries on the community list, many duplicates) [CLAIM-tree-sitter-07] | Reuse; ship query packs per language in EOIP as versioned data |
| STR-tree-sitter-02 | Incremental, error-tolerant parsing, fast enough for per-commit file-level reindex | Reuse in `incremental_indexer.py`: keep last tree keyed by blob SHA or reparse from scratch if absent |
| STR-tree-sitter-03 | Pure-C, dependency-free, MIT; wheels for Python; offline friendly | Reuse; fits air-gap |
| STR-tree-sitter-04 | Diff-hunk to enclosing syntax node mapping | Reuse to improve `diff_hunk.py` accuracy for polyglot repos |

## 9. Limitations with root causes

| Class | Limitation | Type | Claim |
|---|---|---|---|
| Semantics | No name resolution, no types, no cross-file references | intentional trade-off (syntactic parser) | reasoned 0.9 |
| Algorithmic dead-ends | LR/GLR cannot natively parse context-sensitive constructs; needs hand-written C scanners (Python indentation, heredocs); macros/templates unparsed | verified design constraint | [CLAIM-tree-sitter-07] |
| Algorithmic | Error recovery heuristic can yield surprising trees on malformed code | verified fixes recurring | [CLAIM-tree-sitter-03] |
| Operational | Grammar quality, version and ABI vary; ~650 community entries of uneven maintenance; licence per grammar | verified (list), licences UNVERIFIED | [CLAIM-tree-sitter-07] |
| Developer friction | Frequent breaking releases (0.27.0), pre-1.0 versioning; Node IDs and kind names differ per grammar so queries are not portable across languages | verified for 0.27.0 | [CLAIM-tree-sitter-03] |
| Concurrency | Tree not thread-safe | verified | [CLAIM-tree-sitter-04] |
| Python | Two-package model (core + each grammar); grammar wheels' availability/licences vary | verified | [CLAIM-tree-sitter-05] |

## 10. Deployment, licensing, redistribution, operational viability under EOIP constraints

| Constraint | Assessment |
|---|---|
| Self-hosted/air-gap | Fully viable: library, no network. Mirror wheels in an internal index |
| One-node | Trivial footprint |
| Licence | Core MIT [CLAIM-tree-sitter-02], py binding MIT [CLAIM-tree-sitter-05]. Each grammar repo must be checked individually: **legal-review trigger** is only for grammars not MIT/Apache (e.g., GPL grammars exist in the community list: UNVERIFIED, scan needed) |
| Redistribution / white-label | MIT notice retention only for core; grammar scan required |
| Backend neutrality | n/a; produces facts for the mutation gateway |
| Permissions/tenancy | None provided; EOIP attaches ACLs at node ingest |

## 11. Competitive delta against the EOIP verified baseline

| Area | Tree-sitter capability | EOIP baseline | Delta |
|---|---|---|---|
| Languages | hundreds of grammars | BL-42: Python and TypeScript in `codegraph/parser.py:45`; "Tree-sitter referenced in 2 files" (usage depth unverified) | EOIP can add Java, Go, C#, Rust etc. by shipping grammars + queries |
| Incremental | tree-level edit + reparse | `ingestion/incremental_indexer.py:30` file-level incremental (mechanism not re-audited) | Tree-sitter adds sub-file granularity if needed; file-level is probably enough for batch commits |
| Diff hunks | byte-range to node | `codegraph/diff_hunk.py` | candidate accuracy upgrade |
| Semantic precision | none | none (SCIP absent) | both need SCIP for precise references |
| Polyglot linking | none | `ingestion/polyglot_linker.py` | EOIP owns cross-language edges |

## 12. Strength-adoption cards and inversion cards

| Card | Detail |
|---|---|
| STR-tree-sitter-01 | [CLAIM-tree-sitter-06/07]; **integrate/reuse**; design: `CodeGrammarRegistry` (language -> grammar wheel version + `tags.scm` query pack + licence), loaded at startup, offline; acceptance: Java/Go/Rust sample repos produce definitions with 100% file/line round-trip (re-read the range, text equals symbol name) |
| STR-tree-sitter-02 | [CLAIM-tree-sitter-04/05]; **integrate**; acceptance: after a one-line edit in a 5k-line file, reparse + changed_ranges returns a range containing only the edited function in 100% of 50 sampled edits, and graph delta touches only that symbol |

**INV-tree-sitter-01 — syntactic-only facts (semantics, proven).** Target: v0.27.1, any workload needing precise references. Root cause: parser has no resolver. Alternative: combine Tree-sitter (breadth, fallback) with SCIP (precision), each fact carrying `resolution` tier. Worse when: language has no SCIP indexer and dynamic dispatch dominates (Python, JS): then heuristics unavoidable. Options: (1) accept syntactic edges flagged low-confidence; (2) ingest SCIP where available (selected); (3) own resolver per language (reject: cost). POC: 3 repos, measure definition-edge precision/recall of syntactic vs SCIP on hand-labelled 200 references; success = SCIP tier >= 95%, syntactic tier measured and recorded. Defensibility: tier-labelled provenance + ACL + digital thread. Decision: **ADOPT**.

**INV-tree-sitter-02 — grammar/ABI/licence heterogeneity (maturity/licensing, proven for variety, hypothesis for licence risk).** Alternative: curated, pinned grammar set with SBOM and conformance fixtures per grammar. POC: scan the 10 target grammars' licences, parse 100 real files each, fail-rate budget (set in POC). Decision: **ADOPT**.

**INV-tree-sitter-03 — error-cascade on broken code (algorithm, proven by release fixes).** Alternative: flag files with ERROR ratio above threshold and keep prior facts rather than replacing them (living-graph rule: do not delete on parse failure). Decision: **ADOPT** (cheap).

Seed hypotheses (Master Prompt 10.5): none targets Tree-sitter; N/A.

## 13. Per-capability decisions

| CAP | Decision | Note |
|---|---|---|
| CAP-66 precise code graph | REUSE as fallback tier; INTEGRATE SCIP for precision | |
| CAP-67 incremental re-indexing | REUSE (`edit` + reparse) inside `incremental_indexer.py`, file-level trigger | |
| CAP-69 change-impact | BUILD on top (diff hunk -> symbol -> dependants) | |
| CAP-40..41 style provenance | BUILD: attach (repo, commit, path, byte range, grammar version) per fact | |
| Structural search | EXPERIMENT: expose query packs through bounded typed query plan | |
| Own parser generator | REJECT | |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

1. Language pack POC: Java, Go, Rust, C#, TypeScript, Python via offline wheels; assert extraction of definitions matches `ctags`-independent gold for 20 files each.
2. Incremental correctness: random edits; `reparse(old_tree)` tree S-expression equals `parse(new_text)` from scratch (differential test, 1,000 edits).
3. Throughput: measure files/s and MB RSS per language on one node; record hardware; compare with current `parser.py`.
4. Failure injection: truncated files, binary blobs, 50 MB generated file with timeout; assert no crash, timeout honoured, prior facts retained.
5. Offline test: build venv from internal mirror with network blocked.
6. Licence/SBOM scan: every shipped grammar has recorded SPDX id.

## 15. Risks, trade-offs, and open research questions

| Risk / question | Note |
|---|---|
| Internal algorithm details (section 5.3, 5.5) are recalled from source, not re-read | verify at tag v0.27.1 before design freeze |
| py-tree-sitter latest version and Python-support matrix | UNVERIFIED (PyPI summary conflicted with 0.27.1 core) |
| Per-grammar licences, including any copyleft grammars | scan needed |
| Whether current EOIP "Tree-sitter referenced in 2 files" means runtime use or comments | check `parser.py` before the POC |
| Pre-1.0 API breaks (0.27.0) | pin versions, wrap in adapter |
| Syntactic edges polluting a graph that must keep observed vs inferred separate (BL-40) | tag edges `inferred:syntactic` |

## Appendix A. Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | MIT, active, monthly releases |
| D2 | 2 | editors, code-intel, chunking |
| D3 | 4 | generator + runtime + bindings |
| D4 | 5.1 | immutable relative-size subtrees, refcounted |
| D5 | N/A | grammar defines node types, not an ontology |
| D6 | 5.3, 5.5 | incremental parse, query state machine |
| D7 | N/A | none |
| D8 | 5.6 | thread rules only |
| D9 | 2, 5.8 | feeds ingestion; no connectors |
| D10 | N/A (5.8) | symbol identity must be built by EOIP |
| D11 | 5.3 | edits and changed ranges; no history |
| D12 | N/A | none |
| D13 | 2 | chunking for retrieval |
| D14 | N/A | none |
| D15 | N/A | none |
| D16 | N/A | library |
| D17 | 3 | bindings, query files |
| D18 | 5.7 | native-code input risk |
| D19 | N/A | library |
| D20 | 7 | no benchmark verified |
| D21 | 10 | MIT, free |
| D22 | 5.8 | S-expression trees; no graph standard |
| D23 | N/A | no patents examined |
| D24 | App. C | official docs/repo pages; internals partly recalled |

## Appendix B. Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-66 | partial (syntactic only) | tree-sitter-01,04 | BL-42 Partial | REUSE fallback + INTEGRATE SCIP | P1 |
| CAP-67 | native (tree-level) | tree-sitter-04,05 | BL-42 Implemented | REUSE | P1 |
| CAP-69 | plugin (diff hunk mapping) | tree-sitter-05 | BL-42 Partial | BUILD | P1 |
| CAP-38 | absent | n/a | BL-41 Implemented | BUILD provenance fields | P1 |
| CAP-54 | absent (structural search only) | tree-sitter-06 | BL-15 | EXPERIMENT | P3 |

## Appendix C. Evidence records

| CLAIM-ID | Product/version/date | Claim | Class | Source | Dates | Confidence | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-tree-sitter-01 | core | Incremental parser generator + pure-C dependency-free runtime | Officially documented | https://github.com/tree-sitter/tree-sitter | 2026-10-26 | 0.9 | |
| CLAIM-tree-sitter-02 | core | MIT, copyright Max Brunsfeld 2018 | Officially documented | https://raw.githubusercontent.com/tree-sitter/tree-sitter/master/LICENSE | 2026-10-26 | 0.9 | |
| CLAIM-tree-sitter-03 | v0.27.1 / 0.27.0 / 0.26.12-13 | Release dates and notes (UTF-16 fixes, `child_count` u32, edition 2024, MSRV 1.90, wide error node fix); nightly 25 Oct | Officially documented | https://github.com/tree-sitter/tree-sitter/releases | 2026-10-26 | 0.8 (year inferred from asset timestamps) | |
| CLAIM-tree-sitter-04 | using-parsers docs | `ts_tree_edit` + `ts_parser_parse(old_tree)` shares structure; included ranges; `ts_tree_copy` atomic refcount, trees not thread-safe; official bindings list | Officially documented | https://tree-sitter.github.io/tree-sitter/using-parsers/ and /3-advanced-parsing.html | 2026-10-26 | 0.9 | page does not explain internals |
| CLAIM-tree-sitter-05 | py-tree-sitter (PyPI 0.26.0 read, unconfirmed) | MIT; `pip install tree-sitter`; wheels; `Parser`, `Tree.edit`, `changed_ranges`, `Query`, `QueryCursor`; Python >=3.10 | Officially documented | https://github.com/tree-sitter/py-tree-sitter ; https://pypi.org/pypi/tree-sitter/json | 2026-10-26 | 0.7 | version vs core 0.27.1 unreconciled |
| CLAIM-tree-sitter-06 | query docs | Pattern syntax: fields, `!field`, anonymous nodes, wildcards, `ERROR`/`MISSING`, supertypes, captures | Officially documented | https://tree-sitter.github.io/tree-sitter/using-parsers/queries/1-syntax.html | 2026-10-26 | 0.85 (quantifiers/predicates 0.7, not on page) | |
| CLAIM-tree-sitter-07 | grammar ecosystem | ~650 parser entries on community list (duplicates); Python/TS/Java/Go grammars under the `tree-sitter` org; external scanners must be C; per-grammar licences not stated | Third-party/community list | https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers | 2026-10-26 | 0.7 | |
| CLAIM-tree-sitter-08 | internals | GLR/LR(1), reusable-node subtree reuse, per-state lexing, error cost scoring | Reasoned inference from recalled source (`lib/src/parser.c`, `subtree.c`, `reusable_node.h`) | not re-read this session | | 0.6 | none seen |

## Appendix D. Assumptions

1. Release years inferred from asset timestamps reported by the fetch; release page omits years.
2. Section 5 internals are source-recalled hypotheses; pin to v0.27.1 for verification.
3. "Tree-sitter referenced in 2 files" in BL-42 is taken at face value without re-auditing code.
4. Grammar licences left UNVERIFIED rather than assumed MIT.
