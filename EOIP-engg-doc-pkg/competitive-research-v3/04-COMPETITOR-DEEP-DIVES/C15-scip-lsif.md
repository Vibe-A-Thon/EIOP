# C15 — SCIP (Code Intelligence Protocol) and LSIF (Language Server Index Format)

| Field | Value |
|---|---|
| Registry ID | T-C15-scip-lsif |
| Tier | A — precise code-index formats; the missing precise layer of BL-42 |
| Versions examined | SCIP: `scip.proto` on `main` (ProtocolVersion has only `UnspecifiedProtocolVersion=0`; no tagged release visible on the repo page), 344 commits; repo pages exist at `sourcegraph/scip` and `scip-code/scip` (both Apache-2.0). LSIF: specification 0.6.0 ("currently under construction"; 0.5.0 previous); `sourcegraph/lsif-go` archived 2023-09-26 |
| Verified on | 2026-10-18 (brief date; fetches ran 2026-10-26) |
| Worker | V09 (W27 scope) |

## 1. Identity, current status, tier, and sources

| Item | Finding | Claim |
|---|---|---|
| SCIP | Language-agnostic protobuf format "for indexing source code", created at Sourcegraph (about 2022), Apache-2.0 | [CLAIM-scip-lsif-01] |
| Governance | Sourcegraph announced (blog "The future of SCIP", dated 2026-03-25 on a mirror) a move from Sourcegraph-owned to an independent project with a Core Steering Committee (engineers from Uber and Meta), changes via SCIP Enhancement Proposals; community site scip-code.org; the `scip-code/scip` and `scip-code/scip-go` GitHub repos exist. Whether `sourcegraph/scip` redirects or mirrors: UNVERIFIED | [CLAIM-scip-lsif-02] |
| LSIF | Microsoft-originated JSON graph dump of LSP answers; spec 0.6.0 labelled both "Current" and "under construction" | [CLAIM-scip-lsif-03] |
| LSIF status | Sourcegraph states "LSIF support has been fully deprecated and removed" in its design doc; `lsif-go` archived (MIT) pointing to scip-go | [CLAIM-scip-lsif-04][CLAIM-scip-lsif-05] |
| Maintenance | SCIP org-level repos active (scip-clang 330 commits, scip-go 228, scip-java 938, scip-typescript 347, scip-python 6,077 incl. pyright history); no repo archived | [CLAIM-scip-lsif-06] |
| Name-collision note | "SCIP" also names the unrelated SCIP optimisation suite; here only the Sourcegraph protocol | |
| Tier reason | Open, Apache-2.0, offline, produces compiler-grade facts: best candidate to fill BL-42's precise tier | |

## 2. Primary problem, target workloads, concrete example workflows

Problem: transmit precise "find definition / references / implementations / hover" data computed by a compiler-aware indexer so that a server does not need to run language servers. Workloads: code-host navigation, cross-repo impact analysis, dead-code and API-usage analysis, agent grounding.

| Workflow | Steps | Journey |
|---|---|---|
| CI index upload | build -> `scip-<lang>` -> `index.scip` -> ingest | J1, J10 |
| Who calls function F across services | symbol string -> occurrences with `Definition` role absent -> group by document | J1 |
| Cross-repo link | package manager+name+version inside the symbol string resolves owner repo | J9 |
| Blast radius of a changed class | relationships (`is_implementation`, `is_reference`) + occurrences | J1, J10 |

## 3. Feature inventory

| Feature | SCIP | LSIF | Claim |
|---|---|---|---|
| Definitions / references (occurrences with roles) | present | present (definitionResult/referenceResult edges) | [CLAIM-scip-lsif-07][CLAIM-scip-lsif-03] |
| Hover / documentation | present (`SymbolInformation.documentation`, `override_documentation`) | present (hoverResult) | same |
| Implementations / type definitions | present via `Relationship` flags | present (implementationResult edges, recalled) | [CLAIM-scip-lsif-07] |
| Cross-repo identity | symbol strings carry package manager/name/version | monikers (`scheme`, `identifier`, `kind` import/export/local) | [CLAIM-scip-lsif-07][CLAIM-scip-lsif-03] |
| Diagnostics, syntax kinds (highlighting) | present | partial/other | [CLAIM-scip-lsif-07] |
| Streaming/parallel/incremental per file | design goal: file-level incrementality, parallel indexing | whole-graph integer-ID dump | [CLAIM-scip-lsif-08] |
| Position encodings | UTF-8, UTF-16, UTF-32 code units per document | UTF-16 only | [CLAIM-scip-lsif-07][CLAIM-scip-lsif-03] |
| Embedded source text | optional (`Document.text`), off by default | optional base64 | [CLAIM-scip-lsif-07][CLAIM-scip-lsif-03] |
| CLI | `scip` CLI (build `go build ./cmd/scip` or releases): inspect/convert; exact subcommands not read (recalled `print`, `lint`, `stats`, `snapshot`: 0.6) | none official | [CLAIM-scip-lsif-01] |
| Query/storage engine | **absent** (transmission format, not a store) | absent | [CLAIM-scip-lsif-08] |
| Bindings | protobuf: any language with protoc; Go bindings in repo | JSON | |

## 4. Architecture diagram

```
  source tree + build config
        | (compile / typecheck / semanticdb / LSP-grade analysis)
        v
 [Indexer per language]  scip-typescript | scip-java (scip-javac, scip-kotlinc, Gradle/Maven/Bazel) | scip-python (pyright fork)
                         scip-clang (needs compile_commands.json) | scip-go | scip-ruby | scip-dotnet | rust-analyzer | scip-dart | scip-php
        |  writes ONE protobuf file  index.scip
        v
 index.scip = Index{ Metadata, repeated Document{path, language, occurrences[], symbols[]}, external_symbols[] }
        |
        +--> consumer A: Sourcegraph server (upload API; closed source)
        +--> consumer B: `scip` CLI (print/lint/convert)
        +--> consumer C (EOIP): ingestor -> SourceEvents -> validation gate -> governed graph mutation
 LSIF legacy: language server -> lsif-* dump (JSON lines of vertices/edges, integer ids) -> converter -> SCIP (deprecated path)
 State: file on disk/object store per (repo, commit, indexer). No network, no daemon.
```

## 5. Under-the-hood reconstruction

### 5.1 SCIP schema (reconstructed from `scip.proto` on `main`, summarised by fetch; field numbers as read)

```proto
message Index { Metadata metadata = 1; repeated Document documents = 2; repeated SymbolInformation external_symbols = 3; }
message Metadata { ProtocolVersion version = 1; ToolInfo tool_info = 2; string project_root = 3; TextEncoding text_document_encoding = 4; }
message ToolInfo { string name = 1; string version = 2; repeated string arguments = 3; }
message Document {
  string language = 4; string relative_path = 1;
  repeated Occurrence occurrences = 2; repeated SymbolInformation symbols = 3;
  string text = 5;                       // optional, not expected by default
  PositionEncoding position_encoding = 6; // UTF8/UTF16/UTF32 code unit offset from line start
}
message Symbol { string scheme = 1; Package package = 2; repeated Descriptor descriptors = 3; }  // wire form is a string
message Package { string manager = 1; string name = 2; string version = 3; }
message Descriptor { string name = 1; string disambiguator = 2; Suffix suffix = 3; }
enum Suffix { Unspecified=0; Namespace=1; Type=2; Term=3; Method=4; TypeParameter=5; Parameter=6; Meta=7; Local=8; Macro=9; }
message SymbolInformation {
  string symbol = 1; repeated string documentation = 3; repeated Relationship relationships = 4;
  Kind kind = 5; string display_name = 6; Signature signature_documentation = 7; string enclosing_symbol = 8;
}
message Relationship { string symbol = 1; bool is_reference = 2; bool is_implementation = 3; bool is_type_definition = 4; bool is_definition = 5; }
message Occurrence {
  repeated int32 range = 1;            // deprecated: 3 elements (line,startChar,endChar) or 4 (startLine,startChar,endLine,endChar)
  oneof typed_range { SingleLineRange single_line_range = 8; MultiLineRange multi_line_range = 9; }
  string symbol = 2; int32 symbol_roles = 3;   // bitset
  repeated string override_documentation = 4; SyntaxKind syntax_kind = 5;
  repeated Diagnostic diagnostics = 6;
  repeated int32 enclosing_range = 7;  // deprecated; typed_enclosing_range = 10/11
}
enum SymbolRole { Unspecified=0; Definition=0x1; Import=0x2; WriteAccess=0x4; ReadAccess=0x8; Generated=0x10; Test=0x20; ForwardDefinition=0x40; }
message SingleLineRange { int32 line = 1; int32 start_character = 2; int32 end_character = 3; }
message MultiLineRange  { int32 start_line = 1; int32 start_character = 2; int32 end_line = 3; int32 end_character = 4; }
// Also: Diagnostic{severity,code,message,source,tags}; enums SyntaxKind (36 values), Kind (about 86 values:
// Class, Function, Method, Interface, Module, Struct, Trait, Enum ...), Language (about 100 values, Python=15, TypeScript=23, Java=6, Go=33, Rust=40, CSharp=1 ...).
```
Positions are zero-based line and character in the document's `position_encoding`. [CLAIM-scip-lsif-07]

### 5.2 Symbol string grammar (from proto comments, fetched)

```
<symbol>     ::= <scheme> ' ' <package> ' ' (<descriptor>)+   |   'local ' <local-id>
<package>    ::= <manager> ' ' <package-name> ' ' <version>        ('.' = empty placeholder; spaces escaped by doubling)
<descriptor> ::= <namespace> | <type> | <term> | <method> | <type-parameter> | <parameter> | <meta> | <macro>
```
Descriptor suffix characters (`/` namespace, `#` type, `.` term, `().` method, `[]` type parameter, `()` parameter, `:` meta, `!` macro) are recalled from the proto comments: confidence 0.75, verify. Local symbols are valid only within one Document. Example (illustrative, constructed, not copied): `scip-python python mypkg 1.2.0 mypkg/orders/Order#total().` [CLAIM-scip-lsif-07]

### 5.3 Why it differs from LSIF (design doc) [CLAIM-scip-lsif-08]
String symbols instead of integer IDs (an off-by-one in one LSIF indexer broke navigation repo-wide); document/array-oriented rather than one adjacency-list graph (no need to merge everything in memory); streamable; varint-packed ranges (benchmarks showed large savings over message encoding); goals: cross-repo navigation, file-level incrementality, parallel indexing, multiple implementation languages, easier debugging.

### 5.4 LSIF data model [CLAIM-scip-lsif-03]
JSON elements each with `id`, `type` (`vertex`|`edge`), `label`. Vertices: `metaData` (version, positionEncoding utf-16), `document` (uri, languageId), `range` (zero-based start/end), `resultSet` (hub for shared results), `hoverResult`, `definitionResult`, `referenceResult`, `moniker`. Edges: `contains` (document -> ranges, non-overlapping), `next` (range -> resultSet), method edges (`textDocument/hover`, `textDocument/definition`, `textDocument/references`), `item` (with `shard`/`property`). Monikers (scheme, identifier, kind export/import/local, unique) link dumps across projects.

### 5.5 Resolution algorithm (consumer side, reconstruction)
```
find_references(sym):
   defs   = {doc.path : occ for occ in docs if occ.symbol==sym and occ.roles & Definition}
   refs   = {occ for doc in docs for occ in doc.occurrences if occ.symbol==sym}
   extra  = relationships where related.symbol==sym and is_reference       # include implementations/overrides
   cross  = external_symbols & other repos' indexes with same <package manager,name,version>-qualified symbol string
   return refs U extra U cross
```
Exact server algorithms are not public (Sourcegraph core closed); this is the minimum a consumer must implement. EOIP loads into the graph so the traversal is a graph query rather than a bespoke store.

### 5.6 Mapping to the EOIP graph (blueprint)
| SCIP | Graph element | Key / properties |
|---|---|---|
| Index.metadata | `CodeIndexRun` node | tool_info, project_root, repo, commit, indexed_at |
| Document | `SourceFile` node | repo, commit, relative_path, language, blob SHA |
| SymbolInformation | `Symbol` node | symbol string (primary key), kind, display_name, enclosing_symbol -> `CONTAINS` |
| Occurrence | `OCCURS_IN` edge/node | document, range (line, col, end line, col, encoding), roles bitset, syntax_kind |
| Relationship | `IMPLEMENTS` / `REFERENCES` / `TYPE_DEFINITION` edges | flags |
| Package inside symbol | `Package` node | manager, name, version, linked to SBOM nodes (CAP-68) |
Every node/edge carries evidence: (repo, commit, path, range, indexer name+version, resolution=`scip`) so an answer can cite file/line/symbol/revision. ACLs inherit from `SourceFile`. Idempotency: key = (repo, commit, indexer, path); re-ingest replaces facts for changed documents only; tombstone symbols absent from a re-indexed document. At scale store occurrences compactly (columnar per document) and keep only definitions + relationships as graph edges, expanding references on demand (design hypothesis to benchmark).

### 5.7 Other dimensions
Concurrency, transactions, partitioning, caching, reasoning: N/A (file format); security: index files are untrusted input (protobuf parse limits, path traversal in `relative_path`, size caps); versioning: `ProtocolVersion` only has an unspecified value, so format evolution relies on additive proto fields and SEPs [CLAIM-scip-lsif-02].

## 6. Functional and non-functional requirements inferred

| ID | Requirement |
|---|---|
| FR-1 | Ingest `index.scip` and, via converter, legacy LSIF; reject malformed input safely |
| FR-2 | Preserve symbol strings verbatim as stable IDs; never re-derive |
| FR-3 | Per-document replace semantics for incremental updates |
| FR-4 | Honour per-document `position_encoding` when converting to line/column or byte offsets |
| FR-5 | Cross-repo link through package triple |
| FR-6 | Record indexer name/version/arguments for reproducibility |
| NFR-1 | Offline: indexers run in CI with no network except dependency resolution (mirror needed) |
| NFR-2 | scip-clang: about 2 GB RAM per core, build before index, no PCH [CLAIM-scip-lsif-09] |
| NFR-3 | Indexes may be large; stream-process per document |

## 7. Performance and resource model

No benchmark retrieved: **NOT PUBLICLY VERIFIED**. Known resource statements: scip-clang about 2 MB temp space per translation unit, 2 MB `/dev/shm` per core, roughly 2 GB RAM per core, Linux x86_64 and macOS arm64 binaries [CLAIM-scip-lsif-09]. Indexer cost is compiler-grade (full type-check/build), typically far above Tree-sitter parse cost (reasoned). Failure modes: build failure => no index; stale index vs HEAD; Node v22/v24 only for scip-typescript [CLAIM-scip-lsif-10]; scip-python needs Python 3.10+ and Node 16+ [CLAIM-scip-lsif-11]; incomplete symbols for dynamic features.

## 8. Strengths and use-case-specific advantages

| ID | Strength | Approach |
|---|---|---|
| STR-scip-lsif-01 | Compiler-grade definitions/references/implementations with stable cross-repo symbol IDs | **Integrate**: ingestor as new connector (source adapter), flowing through the mutation gateway |
| STR-scip-lsif-02 | Open, Apache-2.0, protobuf, offline, plus a neutral-governance path | Reuse proto; track SEPs |
| STR-scip-lsif-03 | Document-scoped design allows incremental per-file replacement | Match in `incremental_indexer.py` keyed by (repo, path, blob SHA) |
| STR-scip-lsif-04 | Indexers exist for 10+ languages (below) | Integrate per language by customer demand |

Indexer inventory:

| Language | Indexer / repo | Licence (page) | Status notes | Claim |
|---|---|---|---|---|
| Java, Scala, Kotlin | `sourcegraph/scip-java` | Apache-2.0 | active; Gradle, Maven, Bazel; 938 commits | [CLAIM-scip-lsif-06] |
| TypeScript, JavaScript | `sourcegraph/scip-typescript` | Apache-2.0 | active; Node 22/24 | [CLAIM-scip-lsif-10] |
| Python | `sourcegraph/scip-python` | `LICENSE.txt` present, type NOT shown (upstream pyright is MIT): UNVERIFIED | fork of pyright, active | [CLAIM-scip-lsif-11] |
| Go | `scip-code/scip-go` (formerly lsif-go -> scip-go) | Apache-2.0 | active | [CLAIM-scip-lsif-12] |
| C, C++, CUDA | `sourcegraph/scip-clang` | Apache-2.0 | **Beta**, Clang 21, compdb needed | [CLAIM-scip-lsif-09] |
| Rust | `rust-lang/rust-analyzer` (emits SCIP) | recalled MIT/Apache-2.0: UNVERIFIED here | active | [CLAIM-scip-lsif-01] |
| Ruby | `sourcegraph/scip-ruby` | UNVERIFIED | listed | [CLAIM-scip-lsif-01] |
| C#, VB | `sourcegraph/scip-dotnet` | UNVERIFIED | listed | [CLAIM-scip-lsif-01] |
| Dart | `Workiva/scip-dart` | UNVERIFIED | third-party | [CLAIM-scip-lsif-01] |
| PHP | `davidrjenni/scip-php` | UNVERIFIED | personal project | [CLAIM-scip-lsif-01] |
| Debian packaging | `jelmer/debian-lsp` | UNVERIFIED | third-party | [CLAIM-scip-lsif-01] |

## 9. Limitations with root causes

| Class | Limitation | Type | Claim |
|---|---|---|---|
| Scope | Transmission format only: no store, no query language, no reasoning, no history | intentional trade-off | [CLAIM-scip-lsif-08] |
| Operational | Needs a buildable project per language (compdb, dependency resolution, toolchains); index is per commit | verified | [CLAIM-scip-lsif-09/10] |
| Maturity | scip-clang Beta; several indexers third-party/personal; licences unconfirmed | verified / UNVERIFIED | [CLAIM-scip-lsif-09] |
| Coverage | No indexer for many languages (Rust via rust-analyzer; Go via scip-go; none for e.g. Swift/Elixir listed here); Language enum lists names, not indexers | verified | [CLAIM-scip-lsif-01][CLAIM-scip-lsif-07] |
| Governance | Transition to independent governance announced 2026; steering details and repo canonical location unclear | verified (blog) / unverified (repo move) | [CLAIM-scip-lsif-02] |
| Algorithmic | Symbol strings are indexer-defined; two indexers may name the same entity differently across languages (polyglot FFI links not solved) | reasoned 0.7 | [CLAIM-scip-lsif-07] |
| LSIF | Deprecated by its main consumer; spec perpetually "under construction"; integer-ID graph is fragile and memory-heavy; UTF-16 only | verified | [CLAIM-scip-lsif-03/08] |
| Security | No provenance signing of index files | reasoned | |

## 10. Deployment, licensing, redistribution, operational viability under EOIP constraints

| Constraint | Assessment |
|---|---|
| Air-gap / one-node | Viable: protobuf file + CLI; indexers run in customer CI. Dependency mirrors needed for scip-java/typescript/python builds |
| Licence | Protocol and core indexers Apache-2.0 (patent grant is a standard Apache clause: record, no legal conclusion). Unconfirmed licences: scip-python, scip-ruby, scip-dotnet, scip-dart, scip-php, debian-lsp, rust-analyzer. **Legal-review trigger**: scip-python (fork of Microsoft pyright, licence file unseen) and any indexer embedding GPL toolchains (none seen) |
| Redistribution/white-label | Ship ingestor + proto; indexers either bundled (Apache) or customer-installed. Preferred: customer-installed for unconfirmed licences |
| Backend neutrality | Graph mapping is backend-agnostic (nodes/edges via GraphStore, BL-01) |
| Permissions/tenancy | None in the format; EOIP attaches ACLs at ingest |
| Dependency on Sourcegraph | None required: format is consumable without the closed server |

## 11. Competitive delta against the EOIP verified baseline

| Area | SCIP/LSIF | EOIP baseline | Delta |
|---|---|---|---|
| Precise symbols/cross-references | yes, 10+ languages | BL-42: Python/TypeScript parser, Tree-sitter in 2 files, **SCIP/LSIF absent** | gap: precision, languages |
| Incremental | per-document replace | `ingestion/incremental_indexer.py:30` | compatible; SCIP adds symbol-level determinism |
| Provenance | indexer tool_info per index | BL-41 evidence manifests | EOIP stronger across sources; map tool_info into manifest |
| Cross-repo linking | package triple in symbols | `ingestion/polyglot_linker.py` | complementary |
| Permissions | none | BL-17/18 | EOIP must add |

## 12. Strength-adoption cards and inversion cards

| Card | Detail |
|---|---|
| STR-scip-lsif-01 | [CLAIM-scip-lsif-07]; value: exact file/line/symbol/revision traceability; **integrate**; acceptance: for fixture repo, every function/class from `scip print` appears as a `Symbol` with `SourceFile` and range; round-trip compare 100% |
| STR-scip-lsif-03 | [CLAIM-scip-lsif-08]; acceptance: modify 1 of 500 files, re-ingest touches only that document's facts (graph delta count assertion) |

**INV-scip-lsif-01 — format is transmission-only (scope/coupling, proven).** Limitation: SCIP has no store or query [CLAIM-scip-lsif-08]; Sourcegraph's store is closed. Alternative: ingest into EOIP's governed graph, so code facts are queryable with permissions, time and non-code nodes. Worse when: occurrence volume makes graph storage costly (100M+ references). Options: (1) keep `.scip` blobs in object store, graph holds only symbols+definitions+relationships, references resolved by lazy scan; (2) full occurrence edges in graph; (3) hybrid columnar occurrence store joined to graph by symbol key (selected after measurement). POC: index a 1M-LOC polyglot repo, measure graph size, RAM, load time, impact-query p95 on HugeGraph and Neo4j; success = impact query returns exactly the `scip`-derived reference set, load time budget agreed in POC. Dependencies: protobuf, indexers in CI; failure cases: ACL leak via occurrence snippets; stale commit mismatch (store commit on every fact). Defensibility: joins code facts to Jira/CI/incident nodes. Decision: **ADOPT** (option 1 first, EXPERIMENT option 3).

**INV-scip-lsif-02 — indexer coverage, build-dependence and licence variance (operational/maturity, proven).** Alternative: tiered code graph (SCIP -> Tree-sitter -> text) with explicit `resolution` tier and a coverage report per repo. Worse when: customer only needs breadth. POC: coverage report across 10 repos; success = every repo has a defined tier per language and no unlabelled edges. Decision: **ADOPT**.

**INV-scip-lsif-03 — LSIF deprecation (maturity, proven).** Do not implement LSIF as a first-class path; provide converter only if a customer holds LSIF dumps. Decision: **DEFER**/REJECT as primary.

Seed hypothesis check: none in Master Prompt 10.5 targets SCIP/LSIF; N/A.

## 13. Per-capability decisions

| CAP | Decision |
|---|---|
| CAP-66 precise code graph | INTEGRATE SCIP via new `connectors/scip_index.py`-style adapter (BUILD adapter, REUSE proto and indexers) |
| CAP-67 incremental re-indexing | BUILD per-document replace on existing indexer |
| CAP-68 dependency/SBOM risk | EXPERIMENT: use `Package` triples to seed dependency nodes; link to SBOM sources (separate C15 entry) |
| CAP-69 change-impact thread | BUILD on SCIP references + diff hunks |
| CAP-46 ACL | BUILD; inherit from SourceFile |
| LSIF ingestion | DEFER |
| Writing our own indexers | REJECT (use upstream) |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

1. Fixtures: tiny Python, TypeScript, Java projects; run scip-python, scip-typescript, scip-java offline from mirrors; commit `.scip` files as golden.
2. Ingest test: golden `.scip` -> graph; assert counts of Symbols, Documents, definition edges vs `scip print` JSON.
3. Incremental test: change one file, re-index, assert only that document's facts change and removed symbols tombstoned (BL-25).
4. Position test: non-ASCII lines with UTF-8/UTF-16/UTF-32 `position_encoding`; recomputed byte offsets slice to the symbol name.
5. Hostile input: oversize index, path traversal in `relative_path`, duplicate documents: ingestor rejects with DLQ entry (BL-24).
6. Permission test: user lacking repo access gets no symbols, occurrences, or counts.
7. Licence scan of each indexer binary shipped; record SPDX.
8. Impact query: "what breaks if `Order.total` signature changes" returns exact referencing files/lines at pinned commit; compare with compiler-based rename tool output on fixture.

## 15. Risks, trade-offs, and open research questions

| Risk / question | Note |
|---|---|
| Protocol governance transition: canonical repo, release process, versioning (`ProtocolVersion` has only an unspecified value) | follow SEP process; pin proto at a commit |
| Descriptor suffix characters and example are recalled | verify against `scip.proto` comments |
| Licence of scip-python/ruby/dotnet/dart/php | UNVERIFIED; check before bundling |
| Graph blow-up from occurrences | measured in INV-01 POC |
| Symbol-name stability across versions and renames | EOIP must map symbol history (rename detection) |
| Polyglot FFI/RPC edges are not in SCIP | remain EOIP's `polyglot_linker` |
| Indexers need build environments; air-gapped customers must mirror dependencies | operational runbook |

## Appendix A. Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0, governance move 2026, LSIF deprecated |
| D2 | 2 | CI index, impact, cross-repo |
| D3 | 4 | indexer -> file -> consumers |
| D4 | 5.1, 5.4 | protobuf documents vs LSIF graph; no store |
| D5 | 5.1 | Kind/Language/Suffix enums; no ontology |
| D6 | 5.5 | consumer algorithms (reconstruction) |
| D7 | N/A | none; relationships only |
| D8 | N/A | file format |
| D9 | 2, 5.6 | CI-produced artifact feeding ingestion |
| D10 | 5.2 | symbol strings are identity |
| D11 | 5.6 | per-commit indexes; no bitemporal |
| D12 | N/A | none |
| D13 | 2 | grounding for agents |
| D14 | N/A | none |
| D15 | 1 | SEP governance only |
| D16 | N/A | format |
| D17 | 3, 8 | indexers, CLI, proto bindings |
| D18 | 5.7 | untrusted file handling |
| D19 | N/A | format |
| D20 | 7 | resource statements for scip-clang only |
| D21 | 10 | Apache-2.0 mostly |
| D22 | 5.3, 5.6 | open protobuf; LSIF converter path |
| D23 | 10 | Apache patent clause noted; no patents searched |
| D24 | App. C | repo pages, proto, design doc |

## Appendix B. Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-66 | native (format) | scip-lsif-07 | BL-42 Partial, SCIP absent | INTEGRATE | P1 |
| CAP-67 | partial (document granularity) | scip-lsif-08 | BL-42 Implemented | BUILD | P1 |
| CAP-68 | partial (package triple) | scip-lsif-07 | none cited | EXPERIMENT | P2 |
| CAP-69 | plugin (supplies references) | scip-lsif-07 | BL-42 Partial | BUILD | P1 |
| CAP-38 | partial (tool_info) | scip-lsif-07 | BL-41 Implemented | BUILD mapping | P2 |
| CAP-46 | absent | n/a | BL-18 Absent | BUILD | P0 |

## Appendix C. Evidence records

| CLAIM-ID | Product/version/date | Claim | Class | Source | Dates | Confidence | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-scip-lsif-01 | scip repo | Apache-2.0; indexer list (Java/Scala/Kotlin, TS/JS, Rust via rust-analyzer, C/C++, Ruby, Python, C#/VB, Dart, PHP, Debian); `scip` CLI | Officially documented | https://github.com/sourcegraph/scip | 2026-10-26 | 0.85 | no release/tags shown |
| CLAIM-scip-lsif-02 | governance, 2026 | Transition to independent project, Core Steering Committee (Uber, Meta engineers), SEP process; scip-code.org; repos at `scip-code/*` | Vendor blog (mirror) + repo pages | https://sourcegraph.com/blog/the-future-of-scip ; https://github.com/scip-code/scip | blog 2026-03-25 (mirror date) / 2026-10-26 | 0.7 | canonical repo location unconfirmed |
| CLAIM-scip-lsif-03 | LSIF 0.6.0 | JSON vertices/edges, document/range/resultSet/moniker, utf-16, "under construction" | Specification | https://microsoft.github.io/language-server-protocol/specifications/lsif/0.6.0/specification/ | 2026-10-26 | 0.85 | page labels 0.6.0 both Current and under construction |
| CLAIM-scip-lsif-04 | Sourcegraph design doc | "LSIF support has been fully deprecated and removed" | Officially documented | https://raw.githubusercontent.com/sourcegraph/scip/main/docs/DESIGN.md | 2026-10-26 | 0.8 | |
| CLAIM-scip-lsif-05 | lsif-go | Archived 2023-09-26; MIT; use scip-go | Observed (repo page) | https://github.com/sourcegraph/lsif-go | 2026-10-26 | 0.9 | |
| CLAIM-scip-lsif-06 | indexer repos | Commit counts/activity, none archived (scip-java 938 commits, scip-clang 330, scip-python 6,077, scip-typescript 347) | Observed | repo pages under https://github.com/sourcegraph/ | 2026-10-26 | 0.75 | last-commit dates not shown |
| CLAIM-scip-lsif-07 | `scip.proto` main | Messages, field numbers, enums, symbol grammar, roles bitset, typed ranges, position encodings, relationships | Observed in source (via summarising fetch) | https://raw.githubusercontent.com/sourcegraph/scip/main/scip.proto | 2026-10-26 | 0.85 (descriptor suffix chars 0.75 recalled) | |
| CLAIM-scip-lsif-08 | design doc | Transmission not storage; string IDs vs integer IDs; file-level incrementality, parallelism; varint ranges | Officially documented | https://raw.githubusercontent.com/sourcegraph/scip/main/docs/DESIGN.md | 2026-10-26 | 0.85 | |
| CLAIM-scip-lsif-09 | scip-clang | Apache-2.0; Beta; Clang 21; compdb; ~2 GB RAM/core; no PCH | Officially documented | https://github.com/sourcegraph/scip-clang | 2026-10-26 | 0.85 | |
| CLAIM-scip-lsif-10 | scip-typescript | Apache-2.0; Node v22/v24 | Observed | https://github.com/sourcegraph/scip-typescript | 2026-10-26 | 0.85 | |
| CLAIM-scip-lsif-11 | scip-python | Pyright fork; LICENSE.txt type not shown; Python 3.10+, Node 16+ | Observed | https://github.com/sourcegraph/scip-python | 2026-10-26 | 0.8 (licence 0.2) | |
| CLAIM-scip-lsif-12 | scip-go | Apache-2.0; active; release by manual workflow | Observed | https://github.com/sourcegraph/scip-go | 2026-10-26 | 0.8 | URL fetched redirected to scip-code org |
| CLAIM-scip-lsif-13 | Sourcegraph usage | Precise navigation uses SCIP; auto-indexing via executors; language list | Officially documented | https://sourcegraph.com/docs/code-search/code-navigation/precise_code_navigation | 2026-10-26 | 0.9 | |

## Appendix D. Assumptions

1. "SCIP and LSIF" are treated as formats plus their indexer ecosystems, not as Sourcegraph's closed consumer.
2. Where a fetch summary lacked a field (release tags, licences), the field stays UNVERIFIED.
3. The `.scip` to graph mapping in 5.6 is an EOIP design proposal, not a vendor feature.
4. Schema field numbers are from a summarised fetch of `main`; re-diff against a pinned commit before coding.
