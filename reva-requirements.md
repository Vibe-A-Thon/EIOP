# REVA — Requirements Specification

**REVA = Reverse-engineering, Evidence, Verification & Assurance layer for EOIP / KnowGridFlow (KGF)**

| Field | Value |
|---|---|
| Document | `reva-requirements.md` |
| Version | 1.0.0 |
| Date | 2026-10-18 |
| Status | Approved for implementation (all open decisions pre-decided in §17) |
| Companion | `reva-implementation-plan.md` (step-by-step build plan, same ID scheme) |
| Target system | EOIP / KnowGridFlow (KGF): Python/FastAPI backend, React frontend, multi-backend graph (Apache HugeGraph, Neo4j, Amazon Neptune), local-first, multi-tenant, white-label |
| Research subject | `morluto/rea` ("REA: Reverse Engineer Anything"), commit `b0b485a`, package `rea-agents@6.7.0`, analysed 2026-10-18 |
| Clean-room status | No REA source code, schema text, identifiers, prose or test assets are copied. REVA reuses *ideas* that were evaluated, and every adopted idea is redesigned and extended (see §2.9). |

---

## 0. How to use this document

### 0.1 Audience
An autonomous AI coding agent (or a human engineer) who implements REVA inside the KGF codebase. Treat this file as the single source of truth for *what* must be built. Treat `reva-implementation-plan.md` as the single source of truth for *how and in what order*.

### 0.2 Normative language
- **MUST / MUST NOT**: mandatory. A REVA build with any unmet MUST is incomplete.
- **SHOULD / SHOULD NOT**: mandatory unless §17 records a decision that overrides it.
- **MAY**: optional; the implementation plan states whether to build it.

### 0.3 Identifier scheme
| Prefix | Meaning | Example |
|---|---|---|
| `REVA-<MOD>-NNN` | Functional requirement in module `<MOD>` | `REVA-WK-004` |
| `REVA-NFR-NNN` | Non-functional requirement | `REVA-NFR-012` |
| `REVA-IF-NNN` | Interface requirement (REST/MCP/CLI/event) | `REVA-IF-021` |
| `REVA-SEC-NNN` | Security, privacy and tenancy requirement | `REVA-SEC-007` |
| `REVA-TST-NNN` | Test and verification requirement | `REVA-TST-010` |
| `RJ-NN` | REVA acceptance journey | `RJ-04` |
| `D-NN` | Pre-decided design decision | `D-07` |
| `E-NN` | Empirical research result | `E-03` |
| `RC-NN` | REA capability family (research inventory) | `RC-14` |

Module codes: `WK` Warrant Kernel · `TL` Transparency Log · `CV` Coverage · `KG` Knowledge-Gap Registry · `CX` Contradictions · `PD` Proof-of-Done · `VS` Verifier Sandbox · `AI` Artifact Inventory · `SP` Shipped-Artifact Provenance & SBOM · `AB` Application Boundary Extractor · `AS` API Surface Miner · `DB` Database Schema Introspector · `RR` Static↔Runtime Reconciler · `FT` Feature & Impact Trace · `GD` Graph Version Diff · `DV` Source↔Deployed Drift Verifier · `VW` Views, Paging & Budgets · `MC` MCP/REST/CLI surface · `GA` Grounded Answers & Evaluation · `DR` Doctor/Readiness · `UI` User Interface · `OB` Observability/Operations · `XP` Optional Forensics Extension Pack.

### 0.4 The completion rule (read this before writing any code)
**A file path, a function name, a test file name, a green test count, or a coverage percentage is never, on its own, proof that a requirement is implemented.** Completion of every requirement is decided by REVA's own Proof-of-Done engine (module `PD`, §7.6) using the policy in §14. In short, a requirement is complete only when:
1. a declared **obligation** exists for it, with required case kinds and a required verification depth;
2. a **verifier run** executed in the REVA sandbox from a clean checkout at a recorded commit, with process lineage and hashed result artifacts;
3. the obligation's tests **actually executed the owning code** (per-test coverage contexts) and **killed mutants** above the threshold;
4. the verification **authority/depth is comparable** to the claim (a unit test cannot close an end-to-end claim);
5. for user-visible behaviour, an **acceptance journey** captured runtime evidence (API responses, screenshots, logs) against the running stack;
6. no **open contradiction** or **blocking knowledge gap** is linked to it.

The implementation plan builds the Proof-of-Done engine early (Phase P2) so that REVA verifies its own completion ("dogfooding").

---

## 1. Executive summary

### 1.1 What REVA is
REVA is a KGF platform layer that makes every fact, relationship, answer and "done" claim in KGF **warranted**: backed by tamper-evident, signed, tenant-scoped evidence with an explicit authority, epistemic state, calibrated confidence, coverage and limitations. Around that kernel REVA adds evidence-producing extractors that KGF does not have today, plus a verification engine that refuses to call work complete without comparable proof.

REVA is also the natural **runtime substrate for Warrant Engineering**, Vikram's agentic-AI engineering discipline built into KGF. REVA supplies the concrete warrant record, authority lattice, closure rules and proof ledgers that the discipline's methods operate on (§4.4).

### 1.2 Why (problem statement)
KGF answers questions such as "what is impacted if service account `abc` changes?", "what must be retested when rule R changes?" and "which build is running and what commit is it from?". Today those answers can mix static guesses, runtime facts and LLM inference without saying which is which, can present "no result" as "no impact", and cannot prove that an AI developer agent's work is really finished. REVA closes those gaps.

### 1.3 Scope summary
**In scope (built):** Warrant Kernel; signed transparency log; coverage semantics; knowledge-gap registry; contradiction ledger; Proof-of-Done engine with sandboxed verifier runs and attestation; safe artifact inventory; shipped-artifact provenance and SBOM (Go, Rust, .NET, JVM, Python, npm, OCI images); application boundary extraction (JS/TS/Electron, Java/Spring, Python/FastAPI) with client↔server endpoint linking; API-surface mining from HAR, OpenTelemetry and access logs; database schema introspection; static↔runtime reconciliation; feature and impact tracing; graph version diff; source↔deployed drift verification; evidence views, paging and response budgets; MCP, REST and CLI interfaces; grounded-answer contract and known-answer evaluation; doctor/readiness; UI; observability.

**Out of scope (rejected, with reasons in §16):** native decompilation and disassembly, debuggers and dynamic instrumentation, Android/ADB/JADX/JEB/Flutter/Harmony device analysis, firmware extraction, packet-capture and logic-signal decoding, EVM/WASM interface recovery, legacy DOS/console profiles, native UI automation. These appear in the optional **Forensics Extension Pack** (§7.24), which stays disabled unless a tenant licenses it.

---

## 2. REA research findings (deep, code-level, honest)

### 2.1 Method and provenance
| Item | Value |
|---|---|
| Repository | https://github.com/morluto/rea |
| Commit analysed | `b0b485a` ("fix(hopper): verify and repair the Linux embedding runtime (#5041)") |
| Package analysed | `rea-agents@6.7.0` (npm), installed in an isolated directory with `--ignore-scripts` |
| Methods | (a) Read architecture map, MCP contracts, tool design, testing, ledger, coverage, readiness and graph docs. (b) Read domain source: evidence record, bundle, residual unknowns, completion ledger, completion verifier report, conformance trust gate, relationship coverage, canonical digest, application graph, feature trace, version comparison, AST fingerprint, change graph, RPC/GraphQL endpoint scanners, web capture redaction, API-surface accumulator, resource limits, prompt contracts, agent skill. (c) Ran the published CLI on synthetic fixtures built for this study (E-01…E-07). |
| Limits of this research | Not run: real-provider lanes (Hopper/Ghidra/IDA/JADX/Frida), the SQLite tool (needs Node ≥ 24.15; host had Node 22.22), browser capture. Popularity metrics come from a public page snapshot and were not independently audited. |

### 2.2 What REA is
REA is a local MCP stdio server plus a CLI (`rea`, `rea-agents`) that lets an AI agent inspect **shipped software without source**: native binaries (through Hopper, Ghidra, IDA, Kuna, Rizin, objdump), JavaScript/Electron bundles and ASAR archives, .NET assemblies, Android APKs, Apple bundles, firmware, WASM, EVM bytecode, SQLite files, HAR/SAZ/mitmproxy/qlog captures, pcap files, logic-signal recordings, recorded crashes, and runtime behaviour (browser/Electron CDP, V8 Inspector, Frida, GDB, process PTY capture).

Architecture (from `docs/architecture.mermaid` and code):
- **Entry points:** `scripts/rea.mjs` dispatcher → CLI (`src/cli*`) or MCP server (`src/main*`).
- **Composition:** `src/composition/` builds typed provider and session factories.
- **Adapters:** `src/server/` (MCP tool registration, ~127 `registerTool` calls), bridges into Hopper (Python), Ghidra (Java headless script), IDA (external MCP), JADX, Cutter, mitmproxy, pwntools.
- **Application layer:** `src/application/` (workflows, sessions, investigation records, setup/doctor/update).
- **Domain layer:** `src/domain/` (~101k LOC of pure, side-effect-free modules: evidence, comparisons, application graphs, ledgers).
- **Process foundation:** `src/process/` (owned process groups, private roots, deadlines, bounded output, rlimits, cleanup); `src/windows/` + `native/windows` (Job Objects, DACLs).
- **Contracts:** `src/contracts/` (Zod schemas advertised as MCP input/output schemas, error schemas, prompt contracts).

Size: ~337k lines of non-test TypeScript in `src/`, 557 colocated `*.test.ts` files in `src/`, plus 1,362 files under `tests/` (tests, fixtures and support). Tooling: Vitest, Stryker mutation testing, jscpd duplication check, knip dead-code check, oxlint/oxfmt, turbo, release-please.

### 2.3 Verified project facts and red flags
| Fact | Value | Assessment |
|---|---|---|
| License | MIT (REA code); third-party notices retained | Permissive. REVA copies nothing anyway (§2.9). |
| Release cadence | 38 releases from 0.2.0 (2026-07-12) to 6.7.0 (2026-10-18); 6 majors in ~14 weeks | Very high churn; breaking migrations (e.g. `docs/migration-6.2.md`). **Not suitable as a runtime dependency of a sellable product.** |
| Commits | 3,705 (page snapshot) | High velocity |
| Authorship (last 50 commits) | 36 by `morluto`, the rest by 4 humans plus a bot | Effectively single-maintainer; bus-factor risk |
| Stars / forks | 318k / 80.7k (page snapshot) | Highly unusual for a ~3-month-old niche tool. **Not independently verifiable; do not cite as a quality signal.** |
| Open issues / PRs | 668 / 560 | Large unreviewed backlog |
| Runtime | Node ≥ 22.19; some tools need Node ≥ 24.15 | Fragmented prerequisites |
| Self-scoping | Own agent skill: "Skip REA for ordinary source-repository architecture analysis." | Confirms REA targets shipped artifacts, not KGF's main sources (repos, Jira, Confluence, ITSM) |

### 2.4 REA capability inventory (every family) with code locations
| ID | REA capability family | Primary code/doc locations |
|---|---|---|
| RC-01 | Content-addressed Evidence record (subject digest, provider, analysis profile, operation, parameters, raw/normalized result, confidence, authority, environment, limitations, relationship coverage, locations, evidence links) | `src/domain/evidence.ts`, `src/domain/canonicalDigest.ts` |
| RC-02 | Evidence bundles (deterministic manifests of artifacts, providers, environments, scenarios, captures, unknowns, records; canonical ordering; duplicate rejection; target filtering) | `src/domain/evidenceBundle.ts` |
| RC-03 | Relationship coverage (`complete` / `partial` / `unknown`; empty set ≠ no relationships) | `src/domain/relationshipCoverage.ts`, `docs/mcp-contracts.md` |
| RC-04 | Residual unknowns (stable IDs from question+domain+scope; hash-chained revisions; status; severity; required authority/confidence/environment; recommended probes; depends-on/related/contradicts links; verified resolution) | `src/domain/residualUnknown.ts`, `src/application/investigation/*` |
| RC-05 | Reconstruction obligation ledger (reviewed obligations, case kinds, required original/fixture/verifier authority, manifest bindings with owner digest, verifier enumerating obligation IDs, closure digest) | `docs/reconstruction-obligation-ledgers.md`, `src/application/ReconstructionObligation*` |
| RC-06 | Reconstruction coverage evaluator (verifier authority must match contract authority; inference cannot be promoted) | `docs/reconstruction-coverage.md`, `src/domain/reconstructionCoverage*.ts` |
| RC-07 | Readiness conformance (9 stages, fail-closed aggregation: fail/unknown/unsupported/truncated/skipped never become pass) | `docs/reconstruction-readiness.md`, `src/domain/reconstructionReadiness*.ts` |
| RC-08 | Completion ledger and verifier report with process lineage (run ID, PIDs, process group, descendants) | `src/domain/evidenceCompletionLedger.ts`, `src/domain/completionLedgerGeneration.ts` |
| RC-09 | Conformance trust gate (per-dimension match/mismatch/unknown/truncated, volatile dimensions ignored, first divergence) | `src/domain/conformanceTrustGate.ts`, `conformancePackage.ts`, `conformanceReplay.ts` |
| RC-10 | JavaScript Application Graph (provider-neutral nodes/edges, observations separated from entity identity, 7 identity strategies with stability scopes, authority vs epistemic state vs confidence, explicit unavailable values, coverage) | `docs/javascript-application-graph.md`, `src/domain/javascript/javascriptApplicationGraph*.ts` |
| RC-11 | JavaScript/Electron static reconstruction (directory/ASAR, BrowserWindow, preload, contextBridge, IPC pairing, utility processes, native bindings, endpoints incl. partial templates, GraphQL/tRPC operations, source maps) | `src/application/javascript/*`, `src/domain/javascript/*` |
| RC-12 | Feature trace from typed seeds (node-id, route, string, channel, module, native-export, API) with paths, authorities, `contains_inference`, native hand-offs and recommended tools | `src/domain/javascript/javascriptFeatureTrace*.ts` |
| RC-13 | Application version comparison (tiered matching: exact identity → content digest → module source digest → source-map identity → structural fingerprint → semantic key; ambiguous kept with candidates) and change graph (`changed_from`) | `src/domain/javascript/javascriptApplicationVersion*.ts`, `javascriptApplicationChangeGraph.ts`, `javascriptAstFingerprint.ts` |
| RC-14 | Static/runtime reconciliation (`observed_as` edges as cross-layer inference linking static and runtime evidence) | `docs/javascript-runtime-reconciliation.md`, `src/domain/javascript/javascriptRuntimeReconciliation.ts` |
| RC-15 | Source-to-bundle comparison (historical source tree vs shipped bundle) and reference-source import | `src/server/registerApplicationTools/compareSourceToBundle.ts`, `src/domain/referenceSource*.ts` |
| RC-16 | Web network capture inspection (HAR/SAZ/mitmproxy/qlog) with credential redaction by RFC 6901 pointer and API-surface grouping (method, origin, path template with numeric/uuid/hex/iso-date rules) | `src/domain/webNetworkCapture.ts`, `src/domain/analysisView/WebNetworkApiSurfaceAccumulator.ts` |
| RC-17 | SQLite schema and row-sample inspection (DB + WAL identity) | `src/domain/sqlite/sqliteDatabase.ts`, `docs/sqlite-databases.md` |
| RC-18 | Embedded build metadata: Go buildinfo (modules, settings), Rust cargo-auditable dependency list, .NET PE/CLI metadata, Flutter build identity | `src/go/*`, `src/rust/*`, `src/dotnet/*`, `src/flutter/*` |
| RC-19 | Artifact inventory graph (containers, occurrences, digests, extraction boundaries, decompression budgets, integrity contradictions, record-and-continue policy) | `src/domain/artifactGraph.ts`, `artifactDecompressionBudget.ts`, `artifactIntegrityPolicy.ts` |
| RC-20 | Analysis views and paging over retained evidence (summary/facet/item/page; coverage with `next_offset`; view digest bound to parent evidence) | `src/domain/analysisView/*` |
| RC-21 | MCP response budget (10 MiB), oversized-result retention with continuation, summary-mode bundle discovery, filters | `src/config/mcpResponseBudget.ts`, `docs/mcp-contracts.md` |
| RC-22 | MCP tool design discipline (inspect/search/trace/compare/workflow/observe shapes; strict schemas; truthful effects; lifecycle ownership; cancellation semantics) | `docs/tool-design.md` |
| RC-23 | Error contract (typed codes, categories, retryable flag, remediation, partial observations; user-visible error catalog with harm ranking) | `docs/error-contract.schema.json`, `docs/user-visible-errors.csv` |
| RC-24 | Untrusted target content marking (`_meta.provenance.untrusted_content`) and prompt-injection discipline | `docs/mcp-contracts.md` § Untrusted target content |
| RC-25 | Guided prompts with evidence discipline (Observation / Inference / Unknown; absence ≠ equivalence) | `src/contracts/promptContracts.ts` |
| RC-26 | Known-answer agent evaluation (claims checked against delivered evidence: value, authority, confidence, subject, parameters, links) | `src/evaluation/KnownAnswerEvaluation.ts`, `AgentEvaluationReport.ts` |
| RC-27 | Owned process supervision (process groups, deadlines, bounded stdout/stderr, Linux prlimit AS/FSIZE/CPU/core, private runtime roots, cleanup retention) | `src/process/*` |
| RC-28 | Doctor / setup / update (per-client registration diagnosis, dry-run plans, backups, approval) for ~20 agent clients | `src/application/Doctor*.ts`, `Setup*.ts`, `Update*.ts` |
| RC-29 | Behavioural test depth taxonomy (module, composition, boundary, MCP boundary, acceptance, conformance, evaluation; "paths and suite names do not establish depth") | `docs/testing.md` |
| RC-30 | Native analysis via Hopper/Ghidra/IDA/Kuna/Rizin/objdump (pseudocode, assembly, xrefs, CFG, call paths, byte search) | `src/hopper`, `src/ghidra`, `src/ida`, `src/kuna`, `src/rizin`, `src/objdump`, `bridge/*` |
| RC-31 | Debugging and instrumentation (GDB/MI, pwndbg, Rizin debug, Frida, LLDB tracer) | `src/gdb`, `src/frida`, `bridge/native/rea_lldb_tracer.py` |
| RC-32 | Android/ADB/JADX/Apktool/JEB/Flutter/Harmony analysis | `src/adb`, `src/android`, `src/apktool`, `src/jeb`, `src/flutter`, `src/domain/harmony` |
| RC-33 | Firmware (Binwalk/Unblob), pcap/TShark, sigrok signal decoding, EVM, WASM, DOS/PSP/MIPS/PPC/RISC-V profiles, Apple bundles, PE resources, recorded crashes | `src/firmware`, `src/pcap`, `src/signals`, `src/evm`, `src/wasm`, `src/ghidra/*Profile.ts`, `src/domain/apple` |
| RC-34 | Runtime observation: browser/Electron CDP capture and scenarios, V8 Inspector, process PTY capture, native UI capture | `src/browser`, `src/inspector`, `src/process/capture`, `bridge/native` |

### 2.5 Empirical results (reproduced by this study)
All fixtures below were authored for this study and contain no third-party code.

| ID | Experiment | Observed result | Implication for REVA |
|---|---|---|---|
| E-01 | `rea analyze-javascript-application` on a 5-file synthetic Electron app (main, preload, renderer, store, HTML) with an IPC channel `accounts:rotate` that calls `https://iam.internal.example/api/v2/service-accounts/${accountId}/rotate` | Exit 0 in 2.3 s. Graph coverage `complete`; 33 nodes and 46 edges. Correct preload→contextBridge→renderer `invokes`→`ipc-handler` `handles` `ipc-channel`; endpoint captured as a *partial* template with its source range. **Output 370 KB of JSON for 5 small files.** | Boundary extraction is valuable. Output size shows the need for summary-first views and budgets (REVA-VW). |
| E-02 | Same app: `fs.writeFileSync('/tmp/kgf-store.json', …)` in `store.js` | Present only as a low-level call-site in the semantic graph; **no storage/persistence node**. | REVA-AB MUST model file, DB, cache and queue persistence as first-class resources. |
| E-03 | `rea trace-application-feature` seeded with channel `accounts:rotate` | 2 terminal paths, channel→handler→main asset→module→endpoint; authorities listed per path; `contains_inference: true`; coverage `complete-within-source`. | Seed-based tracing with path authority is directly useful for KGF impact questions (REVA-FT). |
| E-04 | Tampered record (edited `limitations`, kept ID) | Rejected: "Evidence semantic identifier does not match its record". | Integrity check works. |
| E-05 | Forged record (changed endpoint host, **recomputed the outer evidence ID** with sorted-key canonical JSON + SHA-256) | The outer evidence-ID check **passed**; rejection came only from nested node/observation/graph IDs, which are equally deterministic and recomputable. | **REA's "authenticated" Evidence proves internal consistency, not authenticity.** REVA MUST sign records (Ed25519) and anchor them in an append-only Merkle log (REVA-WK, REVA-TL). |
| E-06 | `rea compare-application-versions`, v1 vs v2 (endpoint `/v2/`→`/v3/`, `store.save`→`store.persist`, one new IPC handler) | Summary: unchanged 9, added 16, removed 13, changed 2, unknown 9. The 9 modules and the existing `accounts:rotate` handler appear as **removed + added** instead of changed, because artifact-local identity commits the containing artifact digest. | Identity churn makes diffs noisy. REVA-GD MUST separate *logical identity* (stable across versions) from *version identity* (content digest). |
| E-07 | `rea inspect-web-network-capture` + `inspect-analysis-view` (`api-surface`) on a synthetic HAR (3 POST `/service-accounts/{slug}/rotate`, 1 GET with query, 1 DELETE with UUID) | Bearer token **redacted** (absent from output). UUID path templated. Slug IDs `svc-abc`, `svc-def`, `svc-123` **not templated**: 3 separate groups. | Redaction design is good. REVA-AS MUST add cardinality-based templating and OpenAPI alignment. |

### 2.6 Strengths worth learning from
1. **Epistemic discipline is encoded in types, not prose.** Authority, epistemic state and confidence are separate fields with cross-field validation (e.g. static inference cannot claim `observed`; `exact` confidence only for observations).
2. **Absence is never silently evidence of absence.** Coverage objects travel with results; empty caller lists with partial coverage are not "no callers"; `goal_status: unknown` vs `not_reached`.
3. **Fail-closed aggregation.** `unknown`, `unsupported`, `truncated`, `skipped` and `fail` never roll up into `pass`.
4. **Completion requires comparable proof.** An obligation closes only with a unique owner digest, required fixtures for every case kind, and a verifier whose authority matches the original observation. A green unit test cannot close a packaged-process claim.
5. **Deterministic, content-derived identities** (RFC 8785 canonical JSON + SHA-256) make records reproducible and diffable.
6. **Explicit identity strategies with stability scopes** (content digest, canonical path, artifact-local key, structural fingerprint, runtime instance, …).
7. **Unknowns are first-class, revisioned and actionable** (required authority, recommended probes, dependency/contradiction links).
8. **Contradictions are recorded and the run continues**; affected conclusions are blocked, unaffected ones kept.
9. **Large results are never truncated silently**: retained-evidence views, paging with `next_offset`, and continuation calls instead.
10. **Untrusted-content marking** for prompt-injection resistance.
11. **Lifecycle ownership rigour** for subprocesses (deadlines, bounded output, cleanup retention).
12. **Agent evaluation against evidence**, not against free text.

### 2.7 Weaknesses and their root causes (Con → REVA Pro)
| # | REA weakness | Root cause | REVA inversion |
|---|---|---|---|
| W-01 | Evidence "authentication" is a self-certifying hash; forgery with recomputed IDs is possible (E-05) | No producer keys, no external anchor | Ed25519 producer signatures + tenant-scoped append-only Merkle transparency log with signed tree heads and inclusion proofs (REVA-WK-010, REVA-TL) |
| W-02 | Session-scoped, in-memory ledgers; bundles are files | Single-user CLI/MCP design | Durable multi-tenant evidence store with ACLs, retention and graph projection (REVA-WK-007, REVA-WK-009, REVA-SEC-012) |
| W-03 | No tenancy, no access control, no data classification | Local single-analyst tool | Tenant isolation, ACL inheritance from source systems, classification and redaction-preserving commitments (REVA-SEC) |
| W-04 | Identity churn across versions (E-06) | Entity identity commits artifact digest | Dual identity: logical key (repo/service/path/symbol) + version digest; rename/move detection (REVA-GD-003) |
| W-05 | Persistence effects missed (E-02) | Resource vocabulary centred on web storage/endpoints | First-class Resource nodes: file, DB table, cache key, queue/topic, secret, env var, service account (REVA-AB-010) |
| W-06 | API templating limited to numeric/uuid/hex/date (E-07) | Rule-only, per-segment heuristics | Cardinality + position + OpenAPI-guided templating with confidence (REVA-AS-004) |
| W-07 | Huge outputs (E-01: 370 KB for 5 files) | Complete canonical records returned by default | Summary-first responses, token-aware budgets, retained full evidence, stable paging (REVA-VW) |
| W-08 | JS-centric application graph; no Java/Python/Go service modelling | Product focus on shipped JS/Electron | Multi-language boundary extraction (JS/TS, Java/Spring, Python/FastAPI) + cross-service endpoint linking (REVA-AB, REVA-FT) |
| W-09 | No time model beyond revision chains | Investigation-session scope | Bitemporal evidence (valid time + transaction time), as-of queries (REVA-WK-006) |
| W-10 | Obligation closure trusts a declared verifier `status: pass` plus evidence references | Verifier result is caller-supplied evidence | REVA runs the verifier itself in a sandbox, parses raw results, checks per-test coverage contexts and mutation kills, and signs an attestation (REVA-PD, REVA-VS) |
| W-11 | Extreme API churn and single-maintainer risk | Release-driven development | REVA is owned code in KGF with semantic-versioned contracts and migration tooling (REVA-NFR-030) |
| W-12 | Dense, hard-to-navigate documentation | Spec-by-accretion | Generated, example-led contract docs plus the UI explainers (REVA-MC-009, REVA-UI) |
| W-13 | No graph database or query language; graphs are JSON blobs | Pure-domain design | Projection into KGF's multi-backend graph with typed REVA ontology (§6.10, REVA-OB-006) |
| W-14 | Agent-client setup sprawl (~20 clients) | Distribution strategy | One standards-based MCP server + doctor; registration helpers only for clients KGF supports (REVA-DR) |

### 2.8 Disposition: what KGF needs, and what it does not
Decision values: **ADOPT+** (adopt the idea, substantially enhanced) · **ADAPT** (re-target the idea to KGF's domain) · **DEFER** (optional extension pack, off by default) · **REJECT** (not built).

| RC | Needed for KGF? | Decision | REVA module(s) | Reason |
|---|---|---|---|---|
| RC-01 | Yes, core | ADOPT+ | WK | Every KGF fact and answer needs a warrant |
| RC-02 | Yes | ADOPT+ | WK, TL | Portable, verifiable bundles for audits and hand-offs |
| RC-03 | Yes, core | ADOPT+ | CV | Impact analysis must state completeness |
| RC-04 | Yes | ADOPT+ | KG | Knowledge gaps become owned, prioritized work |
| RC-05 | Yes, core | ADOPT+ | PD | Directly enforces "code/test references are not proof" |
| RC-06 | Yes | ADOPT+ | PD | Authority comparability for closure |
| RC-07 | Yes | ADOPT+ | PD, DR | Fail-closed release and phase gates |
| RC-08 | Yes | ADOPT+ | PD, VS | Verifier-run lineage becomes signed attestation |
| RC-09 | Yes | ADAPT | PD, GD | Golden-graph regression and connector idempotency checks |
| RC-10 | Yes | ADOPT+ | WK, AB | Identity strategies and epistemic fields for KGF's code graph |
| RC-11 | Partly | ADAPT | AB | KGF needs service boundaries for JS/TS **and** Java/Python |
| RC-12 | Yes, core | ADOPT+ | FT | Answers the reference impact questions |
| RC-13 | Yes | ADOPT+ | GD | Version-to-version graph diff without churn |
| RC-14 | Yes | ADAPT | RR | Static "may call" vs runtime "did call" from OTel/logs |
| RC-15 | Yes | ADAPT | DV | Deployed artifact ↔ commit drift verification |
| RC-16 | Yes | ADOPT+ | AS | Discover real API dependencies between systems |
| RC-17 | Yes | ADAPT | DB | Enterprise DB schemas for lineage (not only SQLite) |
| RC-18 | Yes | ADOPT+ | SP | Running build → commit → Jira linkage and SBOM |
| RC-19 | Yes | ADOPT+ | AI | Safe ingestion of uploaded archives/exports |
| RC-20 | Yes | ADOPT+ | VW | LLM-context-safe access to large evidence |
| RC-21 | Yes | ADOPT+ | VW, MC | Budgets for MCP/REST responses |
| RC-22 | Yes | ADOPT | MC | KGF MCP tool design rules |
| RC-23 | Yes | ADOPT+ | MC | Typed, remediable, localized errors |
| RC-24 | Yes | ADOPT+ | SEC, GA | Ingested enterprise content is untrusted input to LLMs |
| RC-25 | Yes | ADOPT+ | GA | Answer contract: Observed / Derived / Inferred / Unknown |
| RC-26 | Yes | ADOPT+ | GA | Regression evaluation of KGF answers and agents |
| RC-27 | Yes | ADOPT+ | VS | Sandboxing for extractors, connectors and verifiers |
| RC-28 | Partly | ADAPT | DR | KGF installation readiness; minimal client registration |
| RC-29 | Yes | ADOPT+ | PD, TST | Verification depth ladder used for closure |
| RC-30 | No | DEFER | XP | Binary decompilation is not KGF's job; commercial tool licensing |
| RC-31 | No | REJECT | — | Debuggers/instrumentation conflict with enterprise safety posture |
| RC-32 | No | DEFER | XP | Mobile device forensics only on explicit tenant demand |
| RC-33 | No | REJECT (firmware/pcap/signals/EVM/DOS) · DEFER (WASM, PE resources) | XP | No KGF use case; high maintenance |
| RC-34 | Partly | ADAPT (HAR/OTel import only) · DEFER (live browser/process capture) | AS, RR, XP | KGF consumes recorded telemetry; it does not drive applications |

### 2.9 Clean-room and licensing statement
1. REVA MUST NOT include REA source files, generated schemas, test fixtures, documentation text, identifier prefixes (`ev_`, `unk_`, `jag_`, `ecl_`, `javc_`, …) or tool names.
2. REVA uses its own vocabulary (warrant, gap, obligation, attestation, boundary, resource), its own identifier prefixes (§6.2) and its own algorithms. Where a public standard is shared (RFC 8785 canonical JSON, SHA-256, Ed25519, RFC 6962-style Merkle trees, RFC 6901 JSON Pointer, OpenTelemetry, CycloneDX, SPDX, in-toto/SLSA), REVA implements or uses the standard directly.
3. REA is MIT-licensed, so even incidental similarity carries low legal risk. The clean-room rule exists because the product is sold and white-labelled, and because the user requires an original build.
4. REVA MUST NOT require REA at runtime. The optional Forensics Extension Pack (§7.24) MAY integrate external tools only through REVA's own adapter ports.

---

## 3. Glossary
| Term | Definition |
|---|---|
| **Warrant** | REVA's evidence record: one signed, content-addressed statement of an observation, derivation or inference, with authority, epistemic state, confidence, coverage, limitations, locations and links. |
| **Producer** | Any component that creates warrants: connector, extractor, rule engine, ML model, LLM, verifier, human reviewer. Every producer has an identity and a signing key. |
| **Subject** | The thing a warrant is about: an artifact (bytes with digest), a source-system record (system + key + version), a graph entity, a runtime instance, or nothing (with a reason). |
| **Authority** | *How* the producer came to know the fact (source-system record, static code analysis, shipped artifact, runtime observation, controlled execution, human attestation, rule derivation, model inference, historical reference, external service). |
| **Epistemic state** | *What kind* of fact it is: `observed`, `derived`, `inferred`, `unknown`, `unavailable`. |
| **Confidence** | Calibrated probability in [0,1] plus a band (`exact`, `high`, `medium`, `low`, `unknown`). |
| **Coverage** | A statement of how complete a result set is: `complete`, `partial` (with named limits and omitted counts), `unknown` (with reason), `unavailable`. |
| **Knowledge gap** | A tracked, unanswered material question (REA calls these residual unknowns). |
| **Contradiction** | Two or more warrants that cannot both hold, recorded with affected conclusions. |
| **Obligation** | A verifiable claim that must hold for a requirement or story to be "done". |
| **Verification depth** | The strength of a verification: `static` < `unit` < `component` < `integration` < `acceptance` < `deployed` < `production-observed`. |
| **Verifier run** | A sandboxed execution of a verification command from a clean checkout, producing hashed raw results and process lineage. |
| **Attestation** | A signed in-toto-style statement binding a verifier run's inputs (commit, owner digests, environment) to its outputs (results, coverage, mutation score). |
| **Closure** | The decision that an obligation is satisfied, made only by the Proof-of-Done engine. |
| **Boundary** | An application interaction point: HTTP route, outbound endpoint call, message topic, IPC channel, RPC operation, DB access, file/cache/secret access. |
| **Logical identity** | A version-independent key for an entity (e.g. `svc:billing/route:POST /invoices`). |
| **Version identity** | A content digest that identifies one concrete version of an entity. |
| **Transparency log** | An append-only Merkle tree of warrant digests per tenant, with signed tree heads and inclusion/consistency proofs. |
| **Governed mutation gateway** | KGF's single write path into the authoritative graph (connectors never write directly). |

---

## 4. Architectural context and binding constraints

### 4.1 KGF platform constraints that REVA inherits (all MUST)
| ID | Constraint |
|---|---|
| C-01 | **Local-first, air-gap capable.** Every REVA capability works with no internet access. No mandatory SaaS, cloud service or external LLM. |
| C-02 | **External-LLM egress policy.** REVA never sends raw enterprise content to an external model unless the tenant's egress policy explicitly allows that data class. The default is local models only. |
| C-03 | **Multi-backend graph neutrality.** REVA writes to the authoritative graph only through KGF's graph abstraction / governed mutation gateway. It must work with HugeGraph, Neo4j and Neptune, and declare per-backend capability gaps rather than silently degrading. |
| C-04 | **Governed mutation.** Extractors and connectors produce warrants and *proposed* graph mutations. They never write directly to the graph. |
| C-05 | **Epistemic separation.** Observed, derived, inferred, predicted and human-approved facts stay distinct end to end (storage, API, UI, LLM context). |
| C-06 | **Permissions survive everything.** Source ACLs are preserved through warrants, graph projection, search, traces, views, caches, exports and answers. |
| C-07 | **Tenant isolation.** Data, keys, logs, caches, blobs and indexes are tenant-scoped; cross-tenant leakage is a P0 defect. |
| C-08 | **White-label.** All user-visible strings are localizable resources; product name, logo and colours come from tenant branding configuration. |
| C-09 | **Single node first.** All of REVA runs on one node via Docker Compose; scale-out is optional. |
| C-10 | **Preserve working functionality.** REVA is additive. Changes to existing KGF modules are limited to the integration points in §5.4, each behind a feature flag defaulting to the pre-REVA behaviour until enabled. |

### 4.2 Baseline discovery requirement
Before writing REVA code, the implementer MUST run the discovery procedure in `reva-implementation-plan.md` Phase P0. It produces `docs/reva/BASELINE.md`, recording the actual KGF module paths, graph abstraction API, mutation gateway API, auth/tenancy middleware, configuration system, task queue, frontend routing and test runner. Every integration point in §5.4 is bound to the discovered paths. Where something does not exist, the default in §17 applies; nothing is left to guesswork.

### 4.3 Technology baseline for REVA (pre-decided; see §17 for alternatives)
| Concern | Choice |
|---|---|
| Language | Python ≥ 3.11 (same interpreter as KGF backend) |
| Web/API | FastAPI routers mounted into the KGF app under `/api/reva/v1` |
| Data validation | Pydantic v2 models (strict mode) as the single schema source; JSON Schema generated from them |
| Canonical JSON | REVA's own RFC 8785 implementation (`reva.core.jcs`), cross-checked in tests against the RFC 8785 test vectors and the independent `rfc8785` PyPI package |
| Hashing / signing | SHA-256 (`hashlib`); Ed25519 via `cryptography`; DSSE envelopes for attestations |
| Relational store | PostgreSQL ≥ 14 when KGF already runs it; otherwise SQLite (WAL mode) for single node (D-03) |
| Blob store | Content-addressed filesystem store under the KGF data volume (`<data>/reva/blobs/sha256/ab/cd/<hex>`); S3-compatible (MinIO) when configured (D-04) |
| Parsing | `tree-sitter` with JavaScript, TypeScript/TSX, Java and Python grammars |
| Binary metadata | `pyelftools`, `pefile`, `macholib`, `dnfile` (all permissive licences) |
| DB introspection | SQLAlchemy 2.x inspector (read-only) plus stdlib `sqlite3` with `mode=ro&immutable=1` |
| Background work | KGF's existing task queue if present; otherwise REVA's built-in asyncio worker with a durable job table (D-05) |
| Sandbox | Linux subprocess with new session, `prlimit`-equivalent `resource` limits, cgroup v2 when available, no-network by namespace or container; Docker/Podman runner when available (D-06) |
| Frontend | KGF React app; REVA screens under `/reva/*` |
| Tests | pytest, pytest-cov (per-test contexts), Hypothesis, mutmut, Playwright (journeys) |

### 4.4 Relationship to Warrant Engineering
REVA implements the *runtime mechanics* the Warrant Engineering discipline needs:

| Warrant Engineering need | REVA mechanism |
|---|---|
| Every agent claim carries a warrant | Warrant record (§6.3), signed and logged (§6.9) |
| Warrants have graded strength | Authority × epistemic state × confidence × depth lattice (§6.7) |
| Claims close only with comparable proof | Proof-of-Done closure rules (§7.6) |
| Open questions are explicit | Knowledge-gap registry (§7.4) |
| Conflicts never vanish | Contradiction ledger (§7.5) |
| Answers expose their warrant structure | Grounded-answer contract (§7.19) |

REVA's names, schemas and APIs are product-neutral, so the discipline can be documented and patented independently of this implementation.

---

## 5. REVA architecture overview

### 5.1 Layered view
```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Interfaces: REST /api/reva/v1 · MCP server (reva.*) · CLI `kgf reva …` · UI   │  M: MC, UI
├──────────────────────────────────────────────────────────────────────────────┤
│ Workflows: Feature/Impact Trace · Graph Diff · Drift Verify · Proof-of-Done   │  M: FT, GD, DV, PD
│            Grounded Answers & Eval · Doctor/Readiness · Views/Budgets         │  M: GA, DR, VW
├──────────────────────────────────────────────────────────────────────────────┤
│ Extractors (warrant producers):                                               │
│   Artifact Inventory · Shipped Provenance & SBOM · App Boundary Extractor     │  M: AI, SP, AB
│   API Surface Miner · DB Schema Introspector · Static↔Runtime Reconciler      │  M: AS, DB, RR
├──────────────────────────────────────────────────────────────────────────────┤
│ Kernel: Warrant Kernel · Transparency Log · Coverage · Knowledge Gaps ·       │  M: WK, TL, CV, KG, CX
│         Contradictions · Verifier Sandbox                                     │  M: VS
├──────────────────────────────────────────────────────────────────────────────┤
│ Ports (bound in P0): GraphPort → KGF graph abstraction / mutation gateway     │
│   AuthPort → KGF auth/tenancy · StorePort → Postgres|SQLite · BlobPort → FS|S3 │
│   QueuePort → KGF queue|built-in · LLMPort → KGF model abstraction (local)    │
│   SourcePort → KGF connectors (git, Jira, Confluence, ITSM, observability)    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Package layout (MUST, relative to the KGF backend source root discovered in P0)
```
reva/
  __init__.py
  core/            jcs.py, digest.py, ids.py, time.py, errors.py, result.py, registry.py
  kernel/          warrant.py, authority.py, coverage.py, signing.py, keys.py, store.py,
                   blobs.py, translog.py, gaps.py, contradictions.py, bundles.py, acl.py
  pd/              obligations.py, bindings.py, closure.py, ledger.py, depth.py, antigaming.py,
                   owner_digest.py, readiness.py
  sandbox/         runner.py, profiles.py, lineage.py, limits.py, collectors.py, attest.py
  extract/
    artifacts/     inventory.py, safe_extract.py, formats.py
    provenance/    go_buildinfo.py, rust_audit.py, dotnet_meta.py, jvm_archive.py,
                   python_dist.py, npm_pkg.py, oci_image.py, sbom.py
    boundaries/    ts_js.py, electron.py, java_spring.py, python_web.py, resources.py,
                   endpoint_match.py, model.py
    apisurface/    har.py, otel.py, access_log.py, templating.py, openapi_align.py, redact.py
    dbschema/      introspect.py, sqlite_ro.py
  workflows/       trace.py, diff.py, drift.py, reconcile.py, answers.py, evaluation.py, doctor.py
  views/           views.py, paging.py, budgets.py
  graph/           ontology.py, projection.py, port.py
  api/             routes_*.py (FastAPI routers), schemas.py
  mcp/             server.py, tools/*.py
  cli/             main.py
  config.py
  migrations/      (DB migrations for REVA tables)
tests/reva/        unit/, component/, integration/, acceptance/, conformance/, evaluation/, fixtures/
frontend/src/reva/ (React screens; path bound in P0)
docs/reva/         BASELINE.md, CONTRACTS.md (generated), RUNBOOK.md, BUILD_STATE.md, DECISIONS.md
```

### 5.3 Data flow (canonical path)
1. A **producer** (connector, extractor, rule engine, model, verifier, human) emits an `ObservationDraft`.
2. `WarrantKernel.issue()` validates the draft against the predicate registry, normalizes and canonicalizes the body, computes `warrant_id`, signs it, stores the raw payload as a blob, persists the warrant, appends it to the tenant transparency log, and returns the sealed warrant.
3. The producer emits **proposed graph mutations** referencing warrant IDs. They go to KGF's governed mutation gateway via `GraphPort`.
4. The **projection** updates warrant summaries on graph elements (§6.10).
5. **Contradiction detection** runs on new warrants that share a subject+predicate key with existing warrants.
6. **Workflows** (trace, diff, answers, closure) read the graph and warrants through ACL-filtered queries and return results carrying coverage, warrant references and limitations.
7. **Views** page and budget large results; full results remain retrievable by reference.

### 5.4 Integration points in existing KGF (bound in P0; each behind a flag)
| ID | Integration point | Flag (default) |
|---|---|---|
| IP-01 | Mount REVA FastAPI routers under `/api/reva/v1` | `REVA_ENABLED` (false until P1 is complete, then true) |
| IP-02 | Register REVA DB migrations with KGF's migration runner | — |
| IP-03 | `GraphPort` adapter onto KGF's graph abstraction and mutation gateway | `REVA_GRAPH_PROJECTION` (true) |
| IP-04 | Hook into KGF's ingestion pipeline after normalization, so connectors can attach source-record warrants | `REVA_INGEST_WARRANTS` (false → true after RJ-01 passes) |
| IP-05 | Hook into KGF's answer/NL-query pipeline to enforce the grounded-answer contract | `REVA_ANSWER_CONTRACT` (false → true after RJ-08 passes) |
| IP-06 | Register REVA MCP tools with KGF's MCP server, or start REVA's own MCP server if KGF has none | `REVA_MCP` (true) |
| IP-07 | Add REVA screens and navigation entries to the KGF frontend | `REVA_UI` (true) |
| IP-08 | Wire REVA's Proof-of-Done into KGF's completion boards (KGF completion board, Phase 4 board) as the source of done-status | `REVA_PD_BOARDS` (true) |
| IP-09 | Add `reva` services and volumes to the KGF Docker Compose file | — |
| IP-10 | Add REVA health checks to KGF's health endpoint | — |

---

## 6. Canonical data model (normative)

### 6.1 Conventions
1. **Encoding:** JSON, UTF-8, `snake_case` keys. Timestamps are RFC 3339 UTC with a `Z` suffix and millisecond precision (`2026-10-18T10:00:00.000Z`).
2. **Canonicalization:** every hashed or signed structure is serialized with RFC 8785 (JSON Canonicalization Scheme). Hash-bearing structures MUST NOT contain floating-point numbers. Use integers, e.g. confidence in basis points `score_bp` 0–10000 and durations in milliseconds.
3. **Digests:** SHA-256, lowercase hex, 64 characters.
4. **Prefixed identifiers:** `<prefix><algorithm-version>_<hex>`, e.g. `wr1_<sha256>`. The algorithm version allows future migration (`wr2_` = a future hash) without ambiguity.
5. **Sets** (arrays whose order carries no meaning) MUST be sorted by Unicode code point of their canonical JSON and de-duplicated before hashing. Arrays whose order carries meaning (paths, ordered steps) MUST be documented as ordered.
6. **Explicit absence:** optional facts are represented by `null` plus a reason field where required, never by omitting the key, so missing data can never be read as "no such fact".
7. **Strictness:** all Pydantic models use `extra="forbid"` and strict types. Unknown fields are rejected with error `REVA_E_SCHEMA_UNKNOWN_FIELD`.

### 6.2 Identifier prefixes
| Prefix | Object | Derivation |
|---|---|---|
| `wr1_` | Warrant | SHA-256 of JCS(warrant `body`) |
| `art1_` | Artifact | SHA-256 of artifact bytes |
| `blb1_` | Blob (raw payload) | SHA-256 of blob bytes |
| `gap1_` | Knowledge gap (stable identity) | SHA-256 of JCS({tenant_id, domain, question_normalized, scope}) |
| `cx1_` | Contradiction | SHA-256 of JCS({tenant_id, conflict_key, member_warrant_ids sorted}) |
| `obl1_` | Obligation content digest | SHA-256 of JCS(obligation definition) |
| `bnd1_` | Obligation binding digest | SHA-256 of JCS(binding) |
| `vr1_` | Verifier run | SHA-256 of JCS(run record without signature) |
| `att1_` | Attestation | SHA-256 of DSSE envelope payload |
| `cls1_` | Closure decision | SHA-256 of JCS(decision body) |
| `ldg1_` | Proof-of-Done ledger | SHA-256 of JCS({scope, sorted closure decision ids}) |
| `bun1_` | Warrant bundle | SHA-256 of JCS(bundle manifest) |
| `sth1_` | Signed tree head | SHA-256 of JCS(tree head body) |
| `ent1_` | Logical entity identity | SHA-256 of JCS({tenant_id, entity_type, logical_key}) |
| `ver1_` | Entity version identity | SHA-256 of JCS({entity_id, version_basis, version_digest}) |
| `trc1_` | Trace result | SHA-256 of JCS(trace result body) |
| `dif1_` | Diff result | SHA-256 of JCS(diff result body) |
| `vw1_` | View | SHA-256 of JCS({parent_id, view_request, page}) |
| `prd1_` | Producer | SHA-256 of JCS({tenant_id, producer_type, name, version}) |
| `key1_` | Signing key | SHA-256 of the raw 32-byte Ed25519 public key |

### 6.3 Warrant record
A warrant has an immutable **body** (hashed and signed) and a mutable **envelope** (administrative metadata that can change without changing the fact).

#### 6.3.1 Body fields
| Field | Type | Required | Rules |
|---|---|---|---|
| `schema` | const `"reva.warrant/1"` | yes | |
| `tenant_id` | string | yes | From AuthPort; never from client input in multi-tenant mode |
| `subject` | Subject (§6.4) | yes | |
| `producer` | ProducerRef `{producer_id, producer_type, name, version, build_digest\|null, key_id}` | yes | `producer_type` ∈ `connector, extractor, rule_engine, ml_model, llm, verifier, human, system` |
| `operation` | string, namespaced (`reva.sp.go_buildinfo`) | yes | Registered in the operation registry |
| `predicate` | string, namespaced (`reva.pred.built_from_commit`) | yes | Registered in the predicate registry, with a Pydantic model for `statement` |
| `parameters` | object | yes | Inputs that influence the result (no secrets; redacted per §7.21) |
| `statement` | object | yes | Validated by the predicate's model |
| `raw_ref` | `{blob_id, sha256, size_bytes, media_type}` \| null | yes | Raw producer output is stored as a blob, never inline |
| `authority` | Authority (§6.6) | yes | |
| `epistemic_state` | `observed \| derived \| inferred \| unknown \| unavailable` | yes | |
| `confidence` | `{band, score_bp, calibration_ref\|null}` | yes | `band` ∈ `exact, high, medium, low, unknown`; `score_bp` 0–10000 |
| `coverage` | Coverage (§6.5) \| null | yes | Required (non-null) for set-valued statements (lists of relationships, members, results) |
| `locations` | [Location] (§6.4.2) | yes | Sorted set |
| `limitations` | [`{code, message}`] | yes | Sorted set; `code` from the limitation catalog (§10.3) |
| `environment` | `{environment_id, platform, arch, runtime, isolation}` \| null | yes | `isolation` ∈ `none, process, container, vm` |
| `observed_at` | timestamp | yes | When the observation was made |
| `valid_time` | `{from, to\|null}` | yes | Business validity interval of the fact (bitemporal "valid time") |
| `links` | [`{rel, warrant_id}`] | yes | `rel` ∈ `derived_from, supports, contradicts, supersedes, context, reconciles_static, reconciles_runtime`; sorted set |

#### 6.3.2 Envelope fields
| Field | Type | Rules |
|---|---|---|
| `warrant_id` | `wr1_…` | Recomputed on every read from storage and on import; a mismatch raises `REVA_E_INTEGRITY` |
| `signature` | `{alg:"ed25519", key_id, sig}` | `sig` = base64url Ed25519 signature over the bytes `"REVA-WARRANT-V1\n" + warrant_id` |
| `recorded_at` | timestamp | Transaction time (bitemporal); set by the kernel |
| `log` | `{log_id, leaf_index}` | Position in the tenant transparency log |
| `acl` | `{source_acl_refs:[…], allow:[principal], deny:[principal]}` | Effective access = source ACL ∩ allow − deny (§7.21) |
| `classification` | `{level, pii, tags}` | `level` ∈ `public, internal, confidential, restricted` |
| `retention` | `{policy_id, expires_at\|null, legal_hold}` | |
| `display` | `{subject_label, local_path\|null, url\|null}` | Never hashed; for UI only |
| `status` | `active \| superseded \| retracted` | Retraction never deletes; it adds a `supersedes`/retraction warrant |

#### 6.3.3 Cross-field validation rules (MUST; each has a test)
| Rule | Condition → requirement |
|---|---|
| V-01 | `authority = model_inferred` ⇒ `epistemic_state = inferred` |
| V-02 | `authority = rule_derived` ⇒ `epistemic_state ∈ {derived, inferred}` |
| V-03 | `epistemic_state = observed` ⇒ `authority ∈ {source_system_record, source_code_static, shipped_artifact, runtime_observed, controlled_execution, human_attested, external_service}` |
| V-04 | `confidence.band = exact` ⇒ `epistemic_state = observed` and `score_bp = 10000` |
| V-05 | `epistemic_state ∈ {unknown, unavailable}` ⇒ `band = unknown`, `score_bp = 0`, ≥ 1 limitation, and `statement.reason` non-empty |
| V-06 | `epistemic_state ∈ {inferred, derived}` ⇒ ≥ 1 limitation and ≥ 1 link with `rel ∈ {derived_from, context}` |
| V-07 | `predicate = reva.pred.observed_as` (static↔runtime reconciliation) ⇒ `epistemic_state = inferred`, ≥ 1 `reconciles_static` link and ≥ 1 `reconciles_runtime` link |
| V-08 | `coverage.status = partial` ⇒ ≥ 1 entry in `coverage.limits` or `coverage.reasons`; `coverage.truncated = true` ⇒ `status = partial` and `omitted_count` is null or > 0 |
| V-09 | `coverage.status = complete` ⇒ `truncated = false` and `omitted_count = 0` |
| V-10 | `authority ∈ {source_code_static, shipped_artifact}` ⇒ no `runtime` location kinds |
| V-11 | `authority = runtime_observed` ⇒ ≥ 1 location of kind `runtime`, `log`, or `url` |
| V-12 | `subject.kind = artifact` ⇒ `subject.sha256` equals the stored artifact digest when the artifact is in the blob store |
| V-13 | `valid_time.to` is null or ≥ `valid_time.from` |
| V-14 | Every `links[].warrant_id` exists in the same tenant (or in an imported, verified bundle) |
| V-15 | `producer.key_id` is an active key of that producer at `recorded_at` |
| V-16 | `statement` validates against the predicate model registered for `predicate` |

### 6.4 Subject and Location

#### 6.4.1 Subject (discriminated union on `kind`)
| `kind` | Fields |
|---|---|
| `artifact` | `artifact_id`, `sha256`, `size_bytes`, `media_type`, `format` (from §7.8 format list) |
| `source_record` | `system_type` (`git, jira, confluence, servicenow, gitlab, github, bitbucket, azure_devops, sharepoint, kibana, datadog, grafana, database, file_share, http_api, other`), `system_instance_id`, `record_type`, `record_key`, `record_version` (string; commit SHA, Jira `updated` timestamp, page version…) |
| `graph_entity` | `entity_id` (`ent1_…`), `entity_type`, `version_id` (`ver1_…` \| null) |
| `runtime_instance` | `environment_id`, `instance_key`, `capture_id` |
| `none` | `reason` (non-empty) |

#### 6.4.2 Location (discriminated union on `kind`)
| `kind` | Fields |
|---|---|
| `artifact_range` | `artifact_id`, `offset`, `length` |
| `archive_member` | `artifact_id`, `member_path` (normalized, POSIX), `member_sha256` |
| `source_span` | `repo_id`, `commit`, `path`, `start_line`, `start_col`, `end_line`, `end_col` (1-based lines, 0-based columns) |
| `record_field` | `system_instance_id`, `record_key`, `json_pointer` (RFC 6901) |
| `url` | `url` (credentials stripped), `method` \| null |
| `runtime` | `environment_id`, `service`, `instance` \| null, `trace_id` \| null, `span_id` \| null, `at` |
| `log` | `stream`, `cursor` (offset or line), `at` |
| `graph` | `entity_id` |

### 6.5 Coverage
| Field | Type | Rules |
|---|---|---|
| `status` | `complete \| partial \| unknown \| unavailable` | |
| `scope` | string | Human/machine description of what was examined, e.g. `repo:billing@9f3c… paths:**/*.java` |
| `examined_count` | int ≥ 0 \| null | |
| `omitted_count` | int ≥ 0 \| null | null = not knowable |
| `truncated` | bool | |
| `limits` | [`{name, value, unit}`] | Effective numeric limits that applied, e.g. `{name:"max_depth", value:6, unit:"hops"}` |
| `reasons` | [`{code, message}`] | Required when status ≠ complete |
| `directions` | [`incoming \| outgoing`] \| null | For relationship sets: which directions the coverage describes |
| `per_source` | [`{source_id, status, watermark}`] \| null | Coverage per contributing connector/extractor; `watermark` = last successful sync position |

**Semantics (MUST):**
- `complete` means every item *within `scope`* was examined and returned. It never claims anything about items outside `scope`.
- An empty result with status ≠ `complete` MUST be presented as **"unknown"**, never as "none".
- When several coverages are composed (e.g. a multi-hop trace), the result status is the **minimum** under the order `complete > partial > unknown > unavailable`. Limits and reasons are unioned.

### 6.6 Authority vocabulary
| Authority | Meaning | Typical producer |
|---|---|---|
| `source_system_record` | Read from the system of record via its API/export | Jira, Confluence, ServiceNow, Git connectors |
| `source_code_static` | Parsed from source code at an identified commit (no execution) | Boundary extractor, code graph |
| `shipped_artifact` | Read from built/deployed artifact bytes (no execution) | Provenance/SBOM extractor, inventory |
| `runtime_observed` | Observed from a running system (traces, logs, metrics, HAR) | OTel/log/HAR importers |
| `controlled_execution` | Observed by executing code under REVA's control (verifier run) | Verifier sandbox |
| `human_attested` | A named, authenticated human asserted it (signed) | Reviewers, approvers |
| `rule_derived` | Deterministic derivation from other warrants by a versioned rule | Rule engine, reasoner |
| `model_inferred` | ML/LLM inference | GNN, LLM, entity resolution |
| `historical_reference` | From an older document or source snapshot not tied to the current version | Archived docs, legacy source |
| `external_service` | From a third-party service (e.g. vulnerability feed mirror) | Optional feeds |

### 6.7 Verification depth and authority comparability
**Depth ladder:** `static(0) < unit(1) < component(2) < integration(3) < acceptance(4) < deployed(5) < production_observed(6)`.

| Depth | Definition | Acceptable producing authority |
|---|---|---|
| `static` | Claim checked without executing the code (schema check, type check, static rule) | `source_code_static`, `shipped_artifact`, `rule_derived` |
| `unit` | One module through its public surface, all collaborators faked | `controlled_execution` |
| `component` | One service/package with real in-process collaborators, external boundaries faked | `controlled_execution` |
| `integration` | Crosses ≥ 1 real production boundary (DB, filesystem, HTTP, graph backend) | `controlled_execution` |
| `acceptance` | Compiled/assembled product surface (REST/MCP/CLI/UI) exercised end to end with real backends in Compose | `controlled_execution` |
| `deployed` | Exercised against a deployed environment (staging) | `controlled_execution` (env-tagged) or `runtime_observed` |
| `production_observed` | Observed in production telemetry | `runtime_observed` |

**Comparability rule (MUST):** an obligation with `required_depth = d` closes only with verifier evidence at depth ≥ `d`, produced by an authority acceptable at that depth. Inferred or derived warrants can never satisfy a depth ≥ `unit`.

### 6.8 Supporting record schemas

#### 6.8.1 Knowledge gap (revisioned)
| Field | Rules |
|---|---|
| `gap_id` | `gap1_…`, stable across revisions (§6.2); `question_normalized` = NFKC, trimmed, whitespace collapsed, lower-cased |
| `revision` | int ≥ 1 |
| `previous_revision_digest` | hex \| null; null only when `revision = 1` |
| `revision_digest` | SHA-256 of JCS(revision without `revision_digest`) |
| `question`, `domain` | non-empty |
| `scope` | `{entity_ids[], artifact_ids[], query\|null}` |
| `status` | `open, investigating, blocked, contradicted, resolved, withdrawn, out_of_scope` |
| `severity` | `low, medium, high, critical` |
| `impact_score_bp` | int; computed (§7.4) |
| `owner` | principal \| null; `due_at` timestamp \| null |
| `required_authority` | Authority \| null; `required_depth` Depth \| null; `required_band` band |
| `recommended_probes` | [`{probe_type: tool\|connector_sync\|human_question\|verifier, operation, parameters, rationale, auto_executable}`] |
| `relationships` | [`{type: depends_on\|related_to\|contradicts\|blocks, target_kind: gap\|obligation\|entity, target_id}`] |
| `supporting_warrant_ids`, `contradicting_warrant_ids` | sorted sets |
| `resolution` | `{disposition: verified\|withdrawn\|out_of_scope, rationale, warrant_ids, check_result}` \| null; non-null iff status ∈ {resolved, withdrawn, out_of_scope} |
| `mutation_warrant_id` | The warrant recording this revision (who changed what, when) |

#### 6.8.2 Contradiction
| Field | Rules |
|---|---|
| `contradiction_id` | `cx1_…` |
| `conflict_key` | `{subject_key, predicate, aspect}`, where `aspect` names the conflicting field (JSON pointer into `statement`) |
| `conflict_kind` | `value_conflict, integrity_mismatch, temporal_overlap, identity_collision, authority_conflict` |
| `member_warrant_ids` | ≥ 2, sorted |
| `affected` | `{entity_ids[], obligation_keys[], gap_ids[], answer_ids[]}` |
| `status` | `open, resolved, accepted_both` (accepted_both = both true in different valid-time intervals or contexts) |
| `resolution` | `{rule: authority_precedence\|recency\|valid_time_split\|human_decision, winner_warrant_id\|null, decided_by, decision_warrant_id}` \| null |

#### 6.8.3 Obligation, binding, verifier run, attestation, closure, ledger
Defined normatively in §7.6 (REVA-PD) and §7.7 (REVA-VS); field tables are in §7.6.2–§7.6.6.

### 6.9 Transparency log
- One append-only Merkle log per tenant (`log_id = tenant_id + ":warrants"`), plus one per tenant for attestations (`":attestations"`).
- Hashing follows RFC 6962 §2.1: `leaf_hash = SHA256(0x00 ‖ leaf_data)`, `node_hash = SHA256(0x01 ‖ left ‖ right)`; `leaf_data` = ASCII bytes of the warrant or attestation ID.
- A **Signed Tree Head** (STH) `{log_id, tree_size, root_hash, issued_at}` is signed by the tenant log key, issued at least every `REVA_STH_INTERVAL_S` (default 60 s) when the log grew, and on demand.
- Inclusion proofs and consistency proofs MUST be served (REVA-IF-030/031) and verified by the CLI and UI.

### 6.10 Graph projection model (REVA ontology)
REVA writes through `GraphPort` only. Element names are prefixed `reva_` to avoid collisions in shared label namespaces.

**Vertex labels**
| Label | Key properties |
|---|---|
| `reva_Artifact` | `artifact_id`, `sha256`, `format`, `media_type`, `size_bytes` |
| `reva_Component` (SBOM package) | `purl`, `name`, `version`, `ecosystem`, `licenses` |
| `reva_Service` | `entity_id`, `logical_key`, `language`, `framework` |
| `reva_Boundary` | `entity_id`, `boundary_kind` (`http_route, http_call, message_publish, message_consume, ipc_channel, rpc_operation, graphql_operation, scheduled_job, cli_command`), `logical_key`, `method`, `path_template`, `topic` |
| `reva_Resource` | `entity_id`, `resource_kind` (`file, db_table, db_view, cache_key, queue, topic, secret, env_var, service_account, config_key, bucket`), `logical_key` |
| `reva_ApiOperation` | `entity_id`, `origin`, `method`, `path_template`, `statuses`, `content_types` |
| `reva_DbObject` | `entity_id`, `db_instance`, `schema`, `name`, `object_kind` |
| `reva_Gap` | `gap_id`, `status`, `severity`, `impact_score_bp` |
| `reva_Contradiction` | `contradiction_id`, `status`, `conflict_kind` |
| `reva_Obligation` | `obligation_key`, `version`, `closure_status`, `required_depth` |
| `reva_VerifierRun` | `run_id`, `commit`, `exit_code`, `depth` |
| `reva_Build` | `entity_id`, `artifact_id`, `vcs_revision`, `vcs_time`, `builder` |

**Edge labels**
| Label | From → To | Meaning |
|---|---|---|
| `reva_CONTAINS` | Artifact → Artifact | Archive membership |
| `reva_DEPENDS_ON` | Artifact/Component → Component | SBOM dependency |
| `reva_BUILT_FROM` | Build/Artifact → (KGF Commit vertex) | Shipped-artifact provenance |
| `reva_EXPOSES` | Service → Boundary | Service owns a route/consumer/channel |
| `reva_CALLS` | Boundary(http_call) → Boundary(http_route) or ApiOperation | Client↔server link |
| `reva_ACCESSES` | Service/Boundary → Resource | Reads/writes a resource (`mode` property: read/write/delete) |
| `reva_OBSERVED_AS` | static element → runtime element | Reconciliation (inferred) |
| `reva_CHANGED_FROM` | new version → old version | Diff lineage |
| `reva_CLOSES` | VerifierRun → Obligation | Closure evidence |
| `reva_OWNS` | Obligation → (KGF code symbol vertex) | Owner binding |
| `reva_BLOCKS` | Gap/Contradiction → Obligation/Entity | Blocking relation |
| `reva_ABOUT` | Gap/Contradiction → any entity | Scope |

**Warrant summary properties (MUST) on every REVA-created element and, when `REVA_INGEST_WARRANTS=true`, on KGF elements produced through the mutation gateway:**
`reva_warrant_ids` (list, capped at `REVA_GRAPH_WARRANT_REF_CAP` = 32 most recent; full list via REST), `reva_epistemic` (strongest state across warrants under `observed > derived > inferred > unknown`), `reva_authority_best`, `reva_confidence_bp` (max), `reva_has_contradiction` (bool), `reva_valid_from`, `reva_valid_to`.

Warrants themselves are **not** stored as graph vertices by default (D-09); they live in the warrant store and are joined by ID. This avoids graph bloat while keeping every element traceable.

---

## 7. Functional requirements

Each module section lists: **purpose**, **what REVA does better than REA**, and the **requirements**. In the tables, *Depth* is the minimum verification depth (§6.7) whose evidence is needed to close the requirement's obligations.

### 7.1 Module WK — Warrant Kernel
**Purpose:** issue, validate, sign, store, retrieve, supersede and export warrants.
**Better than REA:** signatures + transparency log (W-01); durable multi-tenant store (W-02); ACL/classification envelope (W-03); bitemporal fields (W-09); raw payloads as blobs so records stay small (W-07); machine-readable limitation codes; predicate registry with typed statements.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-WK-001 | Implement RFC 8785 canonical JSON in `reva.core.jcs.canonicalize(value) -> bytes`. Reject NaN/Infinity, non-string keys, circular references, and floats in hash-bearing structures (`allow_float=False` default). | Passes every RFC 8785 Appendix test vector; byte-identical to the `rfc8785` package for 10,000 Hypothesis-generated JSON values without floats; rejects each invalid class with `REVA_E_CANONICALIZATION`. | unit |
| REVA-WK-002 | Implement the identifier derivations in §6.2 in `reva.core.ids`, with one function per prefix and a `verify_id(obj, id)` helper. | Golden tests: fixed inputs produce fixed IDs (golden file committed); any single-field mutation changes the ID; set-ordering permutations do not. | unit |
| REVA-WK-003 | Implement Pydantic v2 models for the warrant body, envelope, Subject, Location, Coverage, Authority, epistemic state and confidence exactly as in §6.3–§6.6, strict and `extra="forbid"`. | JSON Schema is generated to `docs/reva/schemas/warrant.schema.json`; unknown fields are rejected; every enum value round-trips. | unit |
| REVA-WK-004 | Enforce validation rules V-01…V-16 (§6.3.3) in a single `validate_warrant_body()` that returns *all* violations, not only the first. | One positive and one negative test per rule; a body violating three rules reports all three with JSON pointers. | unit |
| REVA-WK-005 | Provide a **predicate registry**: `register_predicate(name, statement_model, allowed_authorities, allowed_epistemic, requires_coverage: bool)`. `issue()` rejects unregistered predicates. REVA registers every predicate it produces in `reva/kernel/predicates.py` (catalogue in §10.4). | Issuing with an unknown predicate fails with `REVA_E_PREDICATE_UNKNOWN`; registry listing is exposed via REST `GET /predicates`. | component |
| REVA-WK-006 | Support bitemporal semantics: `valid_time` in the body, `recorded_at` in the envelope. Queries accept `as_of_valid` and `as_of_recorded` and return the warrants that were valid / known at those instants. | Fixture with three supersessions returns the correct warrant for six (valid, recorded) query pairs. | integration |
| REVA-WK-007 | `issue(draft) -> SealedWarrant`: validate → normalize sets → store raw payload as blob → canonicalize body → compute ID → sign → persist (idempotent on ID) → append to transparency log → emit `reva.warrant.issued` event. The whole operation is atomic: no stored warrant without a log entry, and no log entry without a stored warrant. | Killing the process at each of 6 injected fault points leaves either nothing or a complete warrant+log entry (recovery job reconciles); re-issuing the same draft returns the same ID without duplicates. | integration |
| REVA-WK-008 | Batch issue: `issue_many(drafts)` with one transaction per batch (default 500) and one log append per warrant. | 50,000 warrants issued in batches; counts in store and log are equal; throughput meets REVA-NFR-001. | integration |
| REVA-WK-009 | Retrieval by ID, by subject, by predicate, by producer, by link (in/out), by time window, with ACL filtering (§7.21) and paging (§7.17). IDs and signatures are verified on every read. A failed verification raises `REVA_E_INTEGRITY` and quarantines the record. | Corrupting one stored byte makes the read fail and records a `reva.pred.integrity_violation` warrant; unauthorized principals receive 404 (not 403) to avoid existence leaks. | integration |
| REVA-WK-010 | Signing: each producer has ≥ 1 Ed25519 key (`key1_` ID). Private keys are encrypted at rest with a KEK (`REVA_KEK` from the KGF secret store or env) using AES-256-GCM. Support rotation (new key active, old key verify-only) and revocation (revoked keys fail verification for warrants recorded after `revoked_at`). | Rotation test: warrants by old and new keys both verify; revocation test: a warrant recorded after revocation fails; private key files are never readable by other OS users (0600) and never logged. | integration |
| REVA-WK-011 | Supersession and retraction: `supersede(old_id, new_draft, reason)` and `retract(id, reason)` issue new warrants with `supersedes` links and flip the old envelope status. Nothing is ever deleted except by the retention engine (REVA-SEC-012). | Superseded warrants are excluded from "current" queries but returned by as-of queries and audit views. | integration |
| REVA-WK-012 | Warrant bundles: export a set of warrants (plus their link closure to a configurable depth, required blobs, producer public keys, STH and inclusion proofs) as a `.revabundle` (zip with `manifest.json`, `warrants.jsonl`, `blobs/`, `keys.json`, `proofs.json`). Import verifies every ID, signature and inclusion proof before accepting anything (all-or-nothing). | Round-trip export/import into a second tenant preserves IDs; any tampered byte rejects the whole import with a precise error list; import never partially mutates state. | integration |
| REVA-WK-013 | Draft builder helpers for producers: `WarrantDraftBuilder` with fluent methods (`about_artifact()`, `about_record()`, `at_span()`, `with_coverage()`, `limitation()`, `derived_from()`), so producers cannot forget required fields. | Every REVA extractor uses the builder (static check: no direct body construction outside `reva.kernel`). | unit |
| REVA-WK-014 | Producer registry: register producers (`prd1_` ID, type, name, version, build digest, owner) and their keys; list and deactivate. Human producers map 1:1 to KGF principals. | Issuing with an unregistered or deactivated producer fails with `REVA_E_PRODUCER`. | component |
| REVA-WK-015 | Emit domain events (`reva.warrant.issued`, `.superseded`, `.retracted`, `.integrity_violation`) on the KGF event bus if present, else on REVA's internal outbox table, with at-least-once delivery and consumer idempotency keys = warrant ID. | Consumer receives every event exactly once after deduplication in a crash-restart test. | integration |

### 7.2 Module TL — Transparency Log
**Purpose:** make warrant and attestation history tamper-evident and externally verifiable.
**Better than REA:** REA has none (W-01).

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-TL-001 | Implement an append-only Merkle tree per log (§6.9) with persistent leaf storage and cached internal nodes, supporting `append(leaf_data) -> leaf_index`. | Root hashes match an independent reference implementation written in the test suite for trees of size 1…2,049; appends survive restarts. | unit |
| REVA-TL-002 | Signed Tree Heads issued every `REVA_STH_INTERVAL_S` when the tree grew, and on demand; stored and served. | STH signatures verify with the tenant log public key; STHs are monotonic in `tree_size`. | component |
| REVA-TL-003 | Inclusion proof `GET /logs/{log_id}/proof/inclusion?leaf_index=&tree_size=` and consistency proof `…/consistency?first=&second=` per RFC 6962 §2.1.1–2.1.2. | Proofs verify for random pairs across 10,000 appends; altered proof bytes fail. | integration |
| REVA-TL-004 | Background auditor: re-verifies log consistency between the last audited STH and the current one, and verifies a random sample (`REVA_AUDIT_SAMPLE`, default 1%) of stored warrants against their leaves. Failures raise a critical alert and an integrity warrant. | Deleting a leaf row or editing a stored warrant is detected within one audit cycle. | integration |
| REVA-TL-005 | Optional STH witnessing: export STHs to an external, write-once location (`REVA_STH_WITNESS_DIR` or an S3 bucket with object lock) for third-party verification. | When configured, every STH appears in the witness location; `kgf reva verify-log --witness` checks continuity. | integration |

### 7.3 Module CV — Coverage semantics
**Purpose:** make completeness explicit for every set-valued result in KGF.
**Better than REA:** coverage composes across hops and sources, carries per-source watermarks, and is enforced in KGF answers and UI, not only in REA tool payloads.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-CV-001 | Implement the Coverage model (§6.5) and `compose(*coverages) -> Coverage` with min-status, union of limits/reasons, summed examined counts and null-propagating omitted counts. | Property tests: composition is associative and commutative; complete only if all inputs are complete. | unit |
| REVA-CV-002 | Every REVA workflow and extractor returning a set MUST attach Coverage. A static check in CI fails if a registered predicate with `requires_coverage=True` is issued without coverage. | CI check `reva-lint coverage` passes; a deliberately broken extractor fails it. | static |
| REVA-CV-003 | Presentation rule: API, MCP and UI render an empty set with non-complete coverage as **"Unknown — not proven empty"** and show the reasons. | Acceptance test on the Impact Trace screen and the REST response for a partial trace. | acceptance |
| REVA-CV-004 | Connector coverage: KGF connectors report sync watermarks and gaps (failed pages, rate-limited windows) through `SourcePort.coverage(source_id)`. REVA stores them and composes them into `per_source` coverage for any query touching data from that source. | A trace touching Jira data during a simulated rate-limit outage reports `partial` with the Jira watermark. | integration |
| REVA-CV-005 | Coverage-aware absence assertions: the helper `assert_absent(query) -> AbsenceResult` returns `proven_absent` only under complete coverage of the relevant scope; otherwise `not_found_unknown`. | Used by the trace engine and the answer contract; unit tests for both branches. | unit |

### 7.4 Module KG — Knowledge-Gap Registry
**Purpose:** track unanswered material questions as owned, prioritized, revisioned work.
**Better than REA:** gaps are tenant-wide, assigned to owners with due dates, prioritized by graph impact, and linked to obligations and entities; probes can run automatically; resolution is verified mechanically.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-KG-001 | Implement the gap model (§6.8.1) with stable `gap1_` identity and a hash-chained revision history; every revision is itself recorded by a warrant (`reva.pred.gap_revision`). | Editing a stored revision breaks chain verification; recording the same question twice returns the existing gap. | integration |
| REVA-KG-002 | Optimistic concurrency: updates require `expected_revision`; a mismatch returns `REVA_E_CONFLICT` with the current head. | Two concurrent updates: one succeeds, one gets a conflict. | integration |
| REVA-KG-003 | State machine: `open → investigating → (blocked \| contradicted \| resolved \| withdrawn \| out_of_scope)`, `blocked → investigating`, `contradicted → investigating`, `resolved → open` (reopen on new contradicting evidence). Invalid transitions are rejected. | Table-driven test of all allowed and disallowed transitions. | unit |
| REVA-KG-004 | Resolution check: `resolved` requires ≥ 1 warrant meeting `required_authority`, `required_depth` and `required_band`, with no open contradiction on those warrants. The check result is stored in `resolution.check_result`. | A resolution citing only inferred warrants for an authority-`runtime_observed` gap is rejected with reason `GAP_AUTHORITY_INSUFFICIENT`. | component |
| REVA-KG-005 | Impact score: `impact_score_bp = severity_weight × (1 + log2(1 + downstream_entity_count)) × blocked_obligation_factor`, normalized to 0–10000, recomputed on graph changes touching the scope (debounced). Weights are configurable (`REVA_GAP_WEIGHTS`). | Golden test on a fixture graph; ordering of the gap board matches expected priority. | component |
| REVA-KG-006 | Probes: each recommended probe is executable when `auto_executable=true` and the tenant policy allows automatic probes (`REVA_AUTO_PROBES`). Execution results become warrants linked to the gap; a probe never mutates source systems. | A connector-sync probe runs, issues warrants and moves the gap to `investigating`. | integration |
| REVA-KG-007 | Automatic gap creation: workflows create gaps for (a) partial/unknown coverage on a material question, (b) ambiguous matches (endpoint matching, diff matching, entity resolution), (c) runtime-only observations without static source, (d) missing commits for shipped revisions, (e) unresolved trace frontiers. Each kind has a template (§10.5). | Each of the five triggers creates exactly one gap per scope (deduplicated by identity). | integration |
| REVA-KG-008 | Gap board API and UI: filter by status, severity, owner, domain, entity; bulk assign; SLA breach highlighting. | Acceptance journey RJ-05. | acceptance |

### 7.5 Module CX — Contradiction Ledger
**Purpose:** detect, record and govern conflicting facts without overwriting history.
**Better than REA:** automatic detection across sources, typed conflict kinds, valid-time splitting, resolution rules, and propagation to answers and obligations.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-CX-001 | Conflict keys: each predicate declares its functional aspects (JSON pointers into `statement` that must be single-valued per subject at a given valid time). Detection runs on issue for warrants sharing `(tenant, subject_key, predicate, aspect)` with overlapping valid time and different values. | Two warrants giving different owners for the same service in overlapping intervals create one `value_conflict`. | component |
| REVA-CX-002 | Integrity contradictions: declared digest ≠ observed digest (archives, manifests, SBOM entries, commit claims) create `integrity_mismatch`. | Fixture with a tampered JAR member produces an integrity contradiction; the member is quarantined from nested expansion. | integration |
| REVA-CX-003 | Resolution rules, in order of configuration: `valid_time_split` (both true in different intervals) → `authority_precedence` (configurable per predicate, default: `human_attested > controlled_execution > runtime_observed > source_system_record > shipped_artifact > source_code_static > rule_derived > historical_reference > model_inferred`) → `recency` (only if enabled for the predicate) → `human_decision`. Automatic rules never discard members; they mark a winner and keep all members visible. | Each rule has a fixture; resolution is recorded as a decision warrant. | component |
| REVA-CX-004 | Propagation: open contradictions set `reva_has_contradiction=true` on affected graph elements, block closure of linked obligations (`CLOSURE_BLOCKED_CONTRADICTION`), and appear in grounded answers that use any member warrant. | Acceptance check through RJ-02. | acceptance |
| REVA-CX-005 | Record-and-continue policy for extractors: `integrity_policy ∈ {fail_closed (default), record_and_continue}`. Under `record_and_continue`, verified siblings continue, contradicted items are quarantined, and result coverage becomes `partial`. | Inventory of an archive with one corrupted member under both policies behaves as specified. | integration |

### 7.6 Module PD — Proof-of-Done Engine
**Purpose:** decide, mechanically and verifiably, whether a requirement, story or obligation is complete. This module enforces the completion rule (§0.4).
**Better than REA (W-10):** REA accepts a caller-supplied verifier status. REVA *runs* the verifier in its sandbox, parses raw outputs itself, proves that tests executed the owning code (per-test coverage contexts), measures test strength (REVA's own mutation probe), detects flakiness and staleness, signs an attestation, and integrates with Jira stories and KGF boards.

#### 7.6.1 Concepts
- **Obligation:** a versioned, reviewable claim. Defined in YAML under `docs/reva/obligations/` (for REVA itself and for KGF modules) or proposed from Jira acceptance criteria via the KGF Jira connector and then reviewed.
- **Binding:** maps an obligation to its owner symbol(s), contract types, fixtures and verifier.
- **Verifier run:** executed by module VS.
- **Closure decision:** computed by `closure.evaluate(obligation, binding, runs)`.
- **Ledger:** canonical set of closure decisions for a scope (a requirement set, Jira epic, sprint or board).

#### 7.6.2 Obligation definition (YAML → model)
| Field | Type | Rules |
|---|---|---|
| `key` | string `^OBL-[A-Z0-9-]+$` | Unique within tenant |
| `version` | int ≥ 1 | Any semantic change increments it |
| `title` | string | |
| `requirement_refs` | [string] | REVA requirement IDs, KGF requirement IDs and/or Jira keys; ≥ 1 |
| `layer` | `domain, service, api, mcp, cli, ui, connector, data, infra, docs` | |
| `required` | bool | |
| `case_kinds` | sorted set of `positive, negative, malformed, boundary, cancellation, concurrency, idempotency, security, permission, performance, migration, teardown, accessibility, localization, recovery` | ≥ 1 |
| `required_depth` | Depth | |
| `requires_contract_type` | bool | If true, the binding must name a schema/parser/model |
| `dependencies` | [obligation key] | Acyclic (validated) |
| `blocking_gaps` | [gap id] | |
| `disposition` | `active, blocked, deferred, out_of_scope` | Non-active obligations never count as closed |
| `nondeterminism` | `{mode: deterministic\|partial_order\|statistical, spec}` | `statistical` requires `{runs, min_pass_ratio}` |
| `performance_budget` | `{metric, p95_ms\|throughput, dataset}` \| null | Required when `performance` ∈ `case_kinds` |
| `review` | `{reviewed_by, review_warrant_id}` | Human-attested review warrant required before closure can be evaluated |

#### 7.6.3 Binding
| Field | Rules |
|---|---|
| `obligation_key`, `obligation_version` | Must match an active obligation |
| `owners` | [`{repo_id, path, symbol, language, owner_digest}`] ≥ 1. `symbol` is a qualified name (`module.Class.method`, `ComponentName`) or `"*file*"` for whole-file owners (docs, configs) |
| `contract_type` | `{schema_ref, parser_ref, model_ref}` \| null |
| `fixtures` | [`{fixture_id, case_kind, depth, path, sha256}`] |
| `verifier` | `{verifier_id, argv: [..], workdir, depth, profile, timeout_s, env_allow: [..], network: none\|loopback\|compose}` |
| `journeys` | [journey id] (required when `layer ∈ {ui, api, mcp, cli}` and `required_depth ≥ acceptance`) |

**Owner digest algorithm (MUST):** parse the file with tree-sitter for the declared language; locate the symbol by qualified name; take its exact byte span including decorators/annotations; normalize line endings to `\n` and strip trailing whitespace per line; SHA-256 the bytes. For `"*file*"`, hash the normalized whole file. If the symbol is not found or is ambiguous, closure is `open` with reason `OWNER_NOT_FOUND` / `OWNER_AMBIGUOUS`.

#### 7.6.4 Requirements
| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-PD-001 | Load and validate obligation YAML and bindings (schema, unique keys, acyclic dependencies, case-kind coverage of fixtures, journey presence rules). Validation errors list every violation with file:line. | Invalid fixtures produce precise errors; valid set loads; dependency cycle detected. | unit |
| REVA-PD-002 | Owner digest per §7.6.3 for Python, TypeScript/TSX, JavaScript and Java; whole-file mode for others. | Golden digests for fixture symbols; reformatting trailing whitespace does not change the digest; changing one token does. | unit |
| REVA-PD-003 | Closure evaluation (deterministic, pure function) with these ordered checks, each producing reason codes (§10.6): (1) obligation active and reviewed; (2) dependencies closed; (3) no blocking gap open; (4) no open contradiction on linked warrants; (5) binding valid, owners resolvable, owner digests current; (6) ≥ 1 verifier run for the binding's verifier at the current commit, with a valid attestation; (7) run depth ≥ required depth and authority acceptable (§6.7); (8) anti-gaming checks AG-01…AG-14 (REVA-PD-004) pass; (9) every required case kind has ≥ 1 passing test tagged with it; (10) nondeterminism and performance budgets satisfied; (11) for acceptance-depth obligations, each listed journey has a passing journey run with runtime artifacts. Outcome ∈ `closed, open, failed, blocked, stale, flaky, unknown`. | Table-driven tests: one fixture per reason code; outcome is never `closed` if any check is non-pass; `unknown`/`truncated`/`skipped` never aggregate to `closed`. | unit |
| REVA-PD-004 | Anti-gaming checks: **AG-01** skipped, xfail, xpass and error outcomes are not passes. **AG-02** each counted test carries the obligation marker (`@pytest.mark.reva_obligation("OBL-…")`, Playwright tag `@OBL-…`, or JUnit `<property name="reva_obligation">`). **AG-03** per-test coverage contexts show the test executed ≥ 1 line inside each owner span (Python via coverage contexts; for TS/JS UI owners, Istanbul coverage from the instrumented acceptance build). **AG-04** REVA mutation probe (REVA-PD-005) kill ratio ≥ `REVA_MUTATION_MIN` (default 0.70) for Python owners at unit/component depth. **AG-05** each counted test function contains ≥ 1 meaningful assertion (AST check: `assert` on a non-constant, `pytest.raises`, `expect(...)`, `assertThat`); `assert True` and asserting literals are flagged. **AG-06** the test does not patch or mock the owner symbol itself. **AG-07** reruns (`REVA_RERUNS`, default 3) all pass, otherwise `flaky`. **AG-08** owner digest at run time equals the current owner digest, otherwise `stale`. **AG-09** the run came from a clean checkout (`git status --porcelain` empty, tree digest recorded). **AG-10** environment fingerprint recorded (image digest or interpreter + OS + lockfile digest). **AG-11** the verifier argv equals the binding's argv (no ad-hoc commands). **AG-12** the result artifacts referenced by the attestation exist in the blob store with matching digests. **AG-13** test count for the obligation > 0 after filtering. **AG-14** a fixture's declared sha256 matches the file at the run commit. | One failing fixture per AG rule demonstrates the rejection reason; a fully compliant fixture closes. | component |
| REVA-PD-005 | **Mutation probe** (REVA's own implementation for Python): AST mutation operators restricted to owner spans: comparison operator swap (`<`↔`<=`, `==`↔`!=`), boolean operator swap, `not` insertion/removal, arithmetic operator swap, numeric constant ±1, string constant replacement, `return X` → `return None`, removal of a call statement, `if` condition forced True/False. Each mutant runs only the obligation's tests in the sandbox with a per-mutant timeout; equivalent mutants surviving can be suppressed only by a human-attested waiver warrant. | On a fixture module with a strong and a weak test suite, the strong suite reaches ≥ 0.9 and the weak one ≤ 0.4; results are deterministic for a fixed seed. | integration |
| REVA-PD-006 | Ledger generation for a scope: the canonical set of closure decisions, summary counts by outcome, `complete = (all required obligations closed)`, `ldg1_` ID, signed by the tenant PD key and logged. | Re-running on unchanged inputs yields the identical ledger ID; changing one owner line flips the affected obligation to `stale`. | integration |
| REVA-PD-007 | Staleness monitor: on every commit ingested by KGF's git connector (or every `git pull` in local mode), recompute owner digests for bound obligations and mark changed ones `stale` without running anything. | Commit touching an owner flips status within one ingestion cycle; untouched obligations remain closed. | integration |
| REVA-PD-008 | Jira integration: (a) propose obligations from a story's acceptance criteria (one candidate per criterion, layer guessed, `review` empty, disposition `active` only after human review); (b) write back nothing to Jira by default (`REVA_JIRA_WRITEBACK=false`); (c) show per-story closure status in KGF. When write-back is enabled, write only a comment containing the ledger summary and a link. | Candidate obligations are created from a fixture story with 4 criteria; no Jira write occurs by default (asserted via connector call log). | integration |
| REVA-PD-009 | Readiness gates: a gate is an ordered list of stages, each with required obligations and/or checks. Aggregation is fail-closed: any `open, failed, blocked, stale, flaky, unknown` in a stage makes the stage non-pass. Each finding reports `stage, reason_code, obligation_key, warrant/attestation ids, next_action`. | REVA's own release gate (§14.3) evaluates correctly on fixtures; a single stale obligation blocks the gate. | component |
| REVA-PD-010 | Board integration (IP-08): KGF completion boards read done-status from REVA ledgers via REST. A board item is "Done" only if its linked obligations are closed. Manual status changes on boards are recorded as human-attested warrants but cannot override a non-closed ledger state (they appear as "Asserted done — unproven"). | Acceptance journey RJ-06. | acceptance |
| REVA-PD-011 | Ledger exports: `reva-ledger.json` (canonical), `reva-ledger.md` (human summary) and a self-contained `reva-ledger.html` tracker (filters by status, layer, requirement, owner; drill-down to reasons, runs, attestations; no external network requests). | HTML opens offline; numbers match the JSON; Playwright snapshot test. | acceptance |
| REVA-PD-012 | Waivers: a human-attested waiver can set an obligation's disposition to `deferred` or `out_of_scope`, or suppress a named equivalent mutant, with mandatory rationale and expiry. Waived obligations are reported separately and never counted as closed. | Waiver without expiry is rejected; expired waivers reopen automatically. | component |

#### 7.6.5 Verifier-run record (produced by VS, consumed by PD)
| Field | Rules |
|---|---|
| `run_id` | `vr1_…` |
| `verifier_id`, `binding_digest` | |
| `repo_id`, `commit`, `tree_digest`, `clean` (must be true) | `tree_digest` = SHA-256 of the sorted `git ls-files -s` output |
| `environment` | `{image_digest\|null, interpreter, os, arch, lockfile_digests{}}` |
| `profile`, `depth`, `network` | |
| `argv`, `started_at`, `finished_at`, `exit_code`, `timed_out` | |
| `lineage` | `{root_pid, pgid, session_id, descendants:[{pid, ppid, cmd_digest}], status: verified\|unavailable, reason\|null}` |
| `artifacts` | [`{kind, blob_id, sha256, size_bytes}`], where `kind` ∈ `junit_xml, coverage_json, mutation_json, playwright_json, playwright_trace, har, screenshot, stdout, stderr, server_log` |
| `tests` | [`{test_id, outcome, duration_ms, obligation_keys[], case_kinds[], owner_lines_hit{owner_digest: count}}`] (parsed by REVA from raw artifacts, never caller-supplied) |
| `reruns` | int; `rerun_outcomes` per test |
| `mutation` | `{owner_digest: {generated, killed, survived, timeout, waived}}` \| null |

#### 7.6.6 Attestation
A DSSE envelope (`payloadType = "application/vnd.in-toto+json"`) containing an in-toto Statement v1:
- `subject`: the owner files (path + sha256) and the commit (`gitCommit` digest).
- `predicateType`: `https://reva.kgf/verification/v1` (a URI used as a name only; nothing is fetched).
- `predicate`: the verifier-run record without raw artifact bytes (artifact digests only), plus the binding digest and obligation keys.
- Signed with the tenant `verifier` key; logged in the tenant attestations log.

### 7.7 Module VS — Verifier Sandbox & Attestation Runner
**Purpose:** execute verifiers, extractors that call external tools, and probes safely and observably.
**Better than REA:** container/cgroup isolation profiles, network policy per depth, signed attestations, Compose-backed acceptance environments, and lineage captured for every run.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-VS-001 | Profiles: `static` (no execution beyond parsers), `unit` (subprocess, no network, rlimits), `component` (as unit, plus local temp DB allowed), `integration` (container or netns with loopback + declared service network), `acceptance` (ephemeral Compose project `reva-verify-<run>` with the full KGF stack, torn down afterwards). | Each profile has a conformance test proving its network policy (attempted external connect fails in `unit`). | integration |
| REVA-VS-002 | Clean checkout: verifier runs use a fresh `git worktree` (or clone) at the target commit in a REVA-owned temp root; untracked files are forbidden; the tree digest is recorded. | A run requested with a dirty tree is refused with `REVA_E_DIRTY_TREE`. | integration |
| REVA-VS-003 | Resource limits per profile (defaults): CPU seconds 900, address space 4 GiB, file size 1 GiB, open files 4,096, processes 512, wall timeout 1,800 s; output capture capped at 16 MiB per stream, with overflow recorded as truncation (never silently cut). | A fork bomb fixture is contained; an infinite-output fixture is truncated with a recorded limit. | integration |
| REVA-VS-004 | Process lineage: new session and process group; descendants tracked by `/proc` polling (Linux) or psutil; on timeout or cancellation, the whole group receives SIGTERM, then SIGKILL after a 10 s grace; cleanup outcome recorded. No REVA-owned process survives a run. | Orphan-detection test: after cancellation, no process with the run's pgid remains. | integration |
| REVA-VS-005 | Environment hygiene: only `env_allow` variables pass through; secrets are never injected unless an obligation explicitly requires a named secret from the KGF secret store; HOME and TMP point into the run root. | Env dump fixture shows only allowed variables. | integration |
| REVA-VS-006 | Collectors: pytest is invoked with `--junitxml`, `--cov` with `--cov-context=test` and JSON export with contexts; Playwright with JSON reporter, trace and screenshots; server-side coverage for acceptance runs via `COVERAGE_PROCESS_START`; HAR capture for API journeys. All artifacts are hashed into the blob store. | A sample run produces all declared artifact kinds with digests matching blob content. | integration |
| REVA-VS-007 | Result parsing is done by REVA from raw artifacts (JUnit XML, coverage JSON, Playwright JSON). Malformed artifacts make the run `unknown`, never `pass`. | Fuzzed/malformed JUnit XML yields `unknown` with reason `ARTIFACT_MALFORMED`. | unit |
| REVA-VS-008 | Attestation creation and signing (§7.6.6); verification utility `kgf reva verify-attestation <file>`. | Tampering with any predicate field fails verification. | integration |
| REVA-VS-009 | Queue and concurrency: runs are jobs with priority; max concurrent runs per tenant (`REVA_MAX_RUNS`, default 2); cancellable via API with cancellation recorded on the run. | Cancellation mid-run yields `cancelled` status, cleaned resources and a partial-artifact list. | integration |
| REVA-VS-010 | Extractor isolation: extractors that parse untrusted bytes (archives, binaries, HAR, logs) run in the `unit` profile as worker subprocesses with memory limits, so parser crashes or zip bombs cannot affect the API process. | Malicious fixtures (zip bomb, deeply nested JSON, gigantic line) are contained and reported. | integration |

### 7.8 Module AI — Artifact Inventory & Safe Extraction
**Purpose:** inventory uploaded or connector-fetched archives and build outputs safely and completely, as the base for provenance, SBOM, boundary extraction and drift checks.
**Better than REA:** enterprise formats (JAR/WAR/EAR, wheels, npm tarballs, OCI images), tenant quotas, deduplication across tenants' blob stores without cross-tenant leakage, and warrants with coverage for every inventory.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-AI-001 | Supported containers: ZIP (incl. JAR/WAR/EAR/APK-as-zip/whl/nupkg), TAR (+gzip/bzip2/xz), npm `.tgz`, Electron ASAR (header JSON + offsets), OCI image layout directories and `docker save` tarballs (manifest + layers), plain files and directories. Format detection uses magic bytes first, extension second; disagreements are recorded as limitations. | Fixture of each format inventories completely; a `.zip`-named TAR is detected as TAR with a limitation. | integration |
| REVA-AI-002 | Safety limits (configurable): max total uncompressed bytes (default 8 GiB), max member count (500,000), max nesting depth (6), max compression ratio per member (200:1) and overall (100:1), max path length (4,096), max single member (2 GiB). Breaches stop expansion of that subtree, record the limit, and set coverage `partial`. | Zip-bomb (42.zip-style, generated by the test suite) and deep-nesting fixtures are contained with correct limits recorded. | integration |
| REVA-AI-003 | Path safety: reject absolute paths, `..` traversal, drive letters, NUL bytes and device files; symlinks and hard links are recorded as link entries and **never followed or materialized outside the extraction root**. Case-colliding names are kept as distinct members. | Traversal and symlink-escape fixtures produce rejections recorded as limitations; nothing is written outside the root. | integration |
| REVA-AI-004 | Member identity: every member gets `{member_path (normalized POSIX), size, sha256, media_type, format, mode, mtime (recorded but non-semantic)}`; nested containers recurse within limits. Duplicate content is stored once per tenant blob namespace. | Inventory of a JAR containing nested JARs lists all levels with digests; re-inventory yields identical warrant IDs. | integration |
| REVA-AI-005 | Integrity: when a container declares member digests (JAR signature digests in `META-INF/*.SF`/`MANIFEST.MF`, wheel `RECORD`, npm `integrity` in lockfiles, OCI layer digests, ASAR integrity blocks), REVA verifies them and creates `integrity_mismatch` contradictions on mismatch, honouring the integrity policy (REVA-CX-005). | Fixtures with one tampered member for each declaring format raise exactly one contradiction each. | integration |
| REVA-AI-006 | Output: one `reva.pred.artifact_inventory` warrant per container (statement = member table digest + counts + nested container list; the full member table stored as a blob), `reva_Artifact` vertices and `reva_CONTAINS` edges (projection batched). | A 10,000-member archive produces one warrant and 10,001 projected vertices; the view API pages the member table. | integration |
| REVA-AI-007 | Safe extraction API (`extract(artifact_id, members[], dest)`) for downstream extractors only: writes into a REVA-owned temp root, applies the same safety rules, and returns digests verified after write. | Extracted file digests equal inventory digests. | integration |

### 7.9 Module SP — Shipped-Artifact Provenance & SBOM
**Purpose:** answer "what exactly is running, what is it built from, and what does it contain?", and link deployed artifacts to commits, Jira stories and dependencies in the KGF graph.
**Better than REA:** REA reads Go, Rust and .NET metadata and stops. REVA adds JVM, Python, npm and OCI, builds the **artifact → commit → story** link, produces CycloneDX/SPDX, raises gaps for missing commits, and feeds drift verification.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-SP-001 | **Go buildinfo** (ELF, PE, Mach-O): locate the build-info header by its public magic, parse the inline-string format (Go ≥ 1.18): Go version, main module path/version/sum, dependencies (path, version, sum, replacements), build settings (`-compiler`, `CGO_ENABLED`, `GOOS`, `GOARCH`, `vcs`, `vcs.revision`, `vcs.time`, `vcs.modified`, …). The pre-1.18 pointer format yields an `unavailable` warrant with reason `GO_LEGACY_BUILDINFO` unless pointer resolution succeeds via section mapping. | Fixtures built in CI from a tiny Go program (with and without VCS stamping) parse exactly; a non-Go binary yields `unavailable` with reason, not "no dependencies". | integration |
| REVA-SP-002 | **Rust cargo-auditable**: read the `.dep-v0` section (ELF, PE, Mach-O `__DATA`), zlib-decompress with a 64 MiB output cap, parse packages (name, version, source, kind, dependency indices, root flag) and build the dependency DAG; detect invalid indices as a malformed-input error. | Fixture built with `cargo auditable build` parses; a stripped binary yields `unavailable`. | integration |
| REVA-SP-003 | **.NET**: via `dnfile`, read assembly identity (name, version, culture, public key token), referenced assemblies, `TargetFrameworkAttribute`, informational version (often containing `+<commit>`), embedded resource names; read sibling `*.deps.json` for NuGet package graphs when present. | Fixture assembly and deps.json produce the expected package graph; a commit suffix in the informational version yields a `built_from_commit` warrant with `derived` epistemic state. | integration |
| REVA-SP-004 | **JVM archives** (JAR/WAR/EAR, Spring Boot fat JARs): parse `META-INF/MANIFEST.MF` (Implementation-*, Build-Jdk-Spec, Created-By, Main-Class, Start-Class, Spring-Boot-Version), every `META-INF/maven/**/pom.properties` (+ `pom.xml` coordinates), `BOOT-INF/lib/*.jar` and `WEB-INF/lib/*.jar` recursively, `git.properties` (`git.commit.id`, `git.commit.id.abbrev`, `git.branch`, `git.commit.time`, `git.dirty`, `git.build.version`), and `META-INF/build-info.properties`; class-file major version → Java release; package inventory. | Fixture Spring Boot JAR (built in CI from a minimal project with git-commit-id plugin) yields components, the commit and the Java release; a JAR without metadata yields components from embedded pom.properties only, with limitations. | integration |
| REVA-SP-005 | **Python distributions**: wheel/sdist/installed dist-info: `METADATA` (name, version, requires-dist), `RECORD` (with digest verification), `direct_url.json` (PEP 610 `vcs_info.commit_id`, `requested_revision`), `top_level.txt`; virtualenv/site-packages scans. | Fixture venv with a VCS-installed package yields its commit; RECORD mismatch raises an integrity contradiction. | integration |
| REVA-SP-006 | **npm**: `package.json` (`name`, `version`, `gitHead`, `repository`), `package-lock.json` v2/v3 `packages` map (resolved, integrity, dev/optional flags), `node_modules/.package-lock.json`; integrity verification for tarballs present in the inventory. | Fixture app with lockfile v3 yields the full dependency graph; dev dependencies are flagged. | integration |
| REVA-SP-007 | **OCI images**: image config (`created`, `architecture`, `os`, labels incl. `org.opencontainers.image.revision`, `.source`, `.version`, `.created`), history, layer digests verification, per-layer inventory, then recursive detection of the ecosystems above inside layers (respecting whiteout files for the final filesystem view). | Fixture image (built in CI with `docker buildx --output type=oci`) yields the revision label, OS packages are listed as `unavailable` unless a dpkg/apk/rpm database is present, and its embedded JAR/venv is detected. | integration |
| REVA-SP-008 | OS packages inside images: parse `/var/lib/dpkg/status`, `/lib/apk/db/installed` and (if present) the RPM sqlite DB (`/var/lib/rpm/rpmdb.sqlite`) read-only for name/version/arch. | Debian- and Alpine-based fixture images list packages. | integration |
| REVA-SP-009 | SBOM export: CycloneDX 1.5 JSON and SPDX 2.3 JSON for any artifact or image, with component PURLs, hashes, dependency relationships and REVA warrant IDs as external references. Outputs validate against the official JSON Schemas (vendored in the repo under `tests/reva/fixtures/schemas/`). | Schema validation passes for all fixtures. | integration |
| REVA-SP-010 | Commit linking: when a revision is found (`vcs.revision`, `git.commit.id`, PEP 610 commit, `gitHead`, OCI revision label, .NET `+sha`), issue `reva.pred.built_from_commit` and, if KGF's git graph contains that commit, project `reva_BUILT_FROM` to it. Otherwise create a gap from template `GAP_COMMIT_NOT_INGESTED` with probe "sync repo X". Abbreviated SHAs match only if unique in the tenant's repos; otherwise the link is ambiguous (candidates listed, no edge). | Three-fixture test: full SHA linked, unique short SHA linked with `derived`, ambiguous short SHA produces a gap with candidates. | integration |
| REVA-SP-011 | Dirty-build flag: `vcs.modified=true`, `git.dirty=true` or equivalent creates a `reva.pred.dirty_build` warrant and marks the build vertex; drift verification (DV) treats dirty builds as `unverifiable_dirty`. | Dirty fixture is flagged in graph and UI. | integration |
| REVA-SP-012 | Optional vulnerability matching (off by default, `REVA_VULN_MATCH=false`): match PURLs against a locally mirrored OSV dataset directory (tenant-supplied, no network calls); results are `external_service` warrants with the mirror snapshot date in limitations. | With a fixture mirror, a known vulnerable version is matched; with matching disabled no lookup happens. | integration |

### 7.10 Module AB — Application Boundary Extractor
**Purpose:** extract, from source code at a commit, every service's inbound and outbound boundaries and the resources it touches, then link clients to servers across repositories.
**Better than REA:** multi-language (JS/TS/Electron **and** Java/Spring **and** Python FastAPI/Flask/Django), first-class resources (W-05), cross-repo client↔server matching, logical identities stable across versions (W-04), and graph projection into KGF.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-AB-001 | Parsing with tree-sitter (JavaScript, TypeScript, TSX, Java, Python). Parse errors are localized (error nodes counted per file); files with errors are still processed for unaffected subtrees, and coverage records the error count. | Fixture with a syntax error in one function still yields boundaries from the rest, with a limitation. | unit |
| REVA-AB-002 | **Inbound HTTP routes** — JS/TS: Express/Router (`app\|router.<method>(path, …)`, `.route(path).<method>()`), Fastify (`fastify.<method>`, `route({method,url})`), Koa-router, NestJS (`@Controller(base)` + `@Get/@Post/...(path)`), Next.js (`pages/api/**` files, `app/**/route.(ts\|js)` exported `GET/POST/...`). Java: Spring `@RestController`/`@Controller` with class-level `@RequestMapping` combined with method-level `@GetMapping/@PostMapping/@PutMapping/@DeleteMapping/@PatchMapping/@RequestMapping(method=…)`, `value`/`path` arrays, JAX-RS `@Path` + `@GET/...`. Python: FastAPI `@app\|router.<method>(path)` with `APIRouter(prefix=…)` and `include_router(prefix=…)` composition, Flask `@app\|bp.route(path, methods=[…])` with blueprint `url_prefix`, Django `path()/re_path()` in `urls.py` with `include()` prefixes. | Fixture repos per framework (authored for REVA) yield the exact expected route sets (golden files), including composed prefixes. | integration |
| REVA-AB-003 | **Outbound HTTP calls** — JS/TS: `fetch`, `axios(.get/.post/…/request)`, `axios.create({baseURL})` instances, `got`, `node:http(s).request`, `ky`. Java: `RestTemplate.*`, `WebClient…uri(…)`, `@FeignClient(name\|url)` interfaces with mapping annotations, `HttpClient` (`java.net.http`). Python: `requests.*`, `httpx.*` (sync/async clients with `base_url`), `aiohttp.ClientSession.*`. | Golden outbound sets per fixture, including base-URL composition. | integration |
| REVA-AB-004 | **Messaging and RPC**: Kafka (kafkajs `producer.send({topic})`, `consumer.subscribe({topic})`; Spring `KafkaTemplate.send(topic, …)`, `@KafkaListener(topics=…)`; confluent-kafka/kafka-python `produce(topic)`/`subscribe([...])`), RabbitMQ/AMQP (`sendToQueue`, `publish(exchange, routingKey)`, `@RabbitListener(queues=…)`), GraphQL client operations (`gql`/`graphql` tagged templates: operation type and name), gRPC service/method definitions from `.proto` files and client stub calls (by generated method names), Electron IPC (`ipcMain.handle/on`, `ipcRenderer.invoke/send`, `contextBridge.exposeInMainWorld`), scheduled jobs (`@Scheduled`, node-cron, Celery beat), CLI commands (argparse/click/typer/commander/picocli). | Golden sets per fixture; IPC pairing produces `invokes→handles` links only for literal channel matches; dynamic channels are kept unpaired with a gap. | integration |
| REVA-AB-005 | **Constant and template resolution**: resolve string literals, same-file constants, simple cross-file imported constants (depth ≤ 2), Spring `@Value("${prop}")` and `@ConfigurationProperties` against `application*.yml/properties` (profile-aware: default + each named profile listed), `process.env.X` / `os.environ["X"]` against `.env*`, Compose and Helm values files present in the repo. Templates (`${id}`, f-strings, `String.format`, concatenation, `{id}` in annotations, `:id` Express params, `<int:id>` Flask converters) normalize to canonical `{}` segments. Unresolvable parts make the boundary `resolution: partial`, keeping the expression text and source span. | Fixture with each resolution style yields the expected canonical templates; unresolved parts keep the original expression. | integration |
| REVA-AB-006 | **Resources (W-05)**: detect and model as `reva_Resource` with access mode: files (`fs.*`, `open()`, `java.nio.file.Files.*`), DB tables (SQL string literals parsed with a lightweight SQL tokenizer for `FROM/JOIN/INTO/UPDATE/DELETE` table names; JPA `@Entity/@Table(name)`; SQLAlchemy `__tablename__`; Prisma model calls; Mongoose model names), cache keys (Redis client `get/set/del` with literal or templated keys), queues/topics (from AB-004), secrets and env vars (`process.env`, `os.getenv`, `System.getenv`, Spring placeholders), service accounts (identifiers matching configured patterns `REVA_SERVICE_ACCOUNT_PATTERNS`, plus Kubernetes `serviceAccountName`, IAM role ARNs and connection-string user names in config files), buckets (S3/GCS SDK calls with literal names). | E-02 regression: the fixture's `fs.writeFileSync` becomes a `file` resource with `write` mode; each resource kind has a fixture. | integration |
| REVA-AB-007 | **Service identity**: a service = a deployable unit determined by, in order, (1) an explicit `reva-service.yaml` in the repo, (2) build descriptors (Maven/Gradle module, `package.json` with `start` script, `pyproject.toml`), (3) Dockerfile/Compose/Helm service names. Logical key = `svc:<repo_id>/<service_name>`. | Mono-repo fixture with three services is split correctly. | integration |
| REVA-AB-008 | **Logical identities**: boundaries `bnd:<service>/<kind>:<METHOD> <template>` (or topic/channel/operation), resources `res:<kind>:<canonical_name>`; version identity = digest of the defining source span. These identities are stable across commits when the defining facts are unchanged, even if files move (W-04). | Moving a controller file between packages keeps the boundary's logical identity; editing the handler body changes only its version identity. | integration |
| REVA-AB-009 | **Client↔server matching** (`endpoint_match.py`): for each outbound call, resolve the target service from base URL/config mapping (`REVA_SERVICE_URL_MAP` + discovered config keys), then match `(method, canonical template)` against that service's inbound routes. Scoring: exact template = 0.95; same segment count with parameter positions aligned = 0.75; prefix-only = 0.4 (never projected; becomes candidates in a gap). Ties produce `ambiguous` (no edge, gap with candidates). Matched pairs are projected as `reva_CALLS` with `inferred` epistemic state and the score as confidence. | Two-repo fixture (client JS + server Spring) produces the expected calls; an ambiguous fixture yields a gap with both candidates. | integration |
| REVA-AB-010 | **Electron specifics**: BrowserWindow creation and `webPreferences` (contextIsolation, nodeIntegration, sandbox, preload path), preload discovery, exposed API members, renderer → preload → main IPC chains (cf. E-01, E-03). | E-01 fixture reproduces the chain renderer→contextBridge→`invokes`→handler→channel and the endpoint call. | integration |
| REVA-AB-011 | **Coverage and limitations**: per repo and per file: files examined/skipped (by language, size limit `REVA_AB_MAX_FILE_BYTES` default 2 MiB, generated-code patterns, vendored dirs), parse errors, unresolved dynamic dispatch, reflection, runtime registration. Statements never claim runtime reachability. | Coverage counts equal the fixture's file counts; limitation codes match §10.3. | integration |
| REVA-AB-012 | **Incremental extraction**: given the previous run's per-file digests, re-extract only changed files plus files whose resolved constants depend on changed files (dependency index); results equal a full re-extraction. | Property test on random edit sequences: incremental result == full result. | integration |
| REVA-AB-013 | **Projection**: `reva_Service`, `reva_Boundary`, `reva_Resource` vertices; `reva_EXPOSES`, `reva_CALLS`, `reva_ACCESSES` edges; links to KGF's code-graph symbol vertices (by repo/path/symbol) when they exist (`reva_DEFINED_IN` property `symbol_ref`). | Graph queries on each backend return the expected subgraph for the fixture (conformance suite across HugeGraph, Neo4j, Neptune-compatible Gremlin). | integration |

### 7.11 Module AS — API Surface Miner
**Purpose:** discover the APIs systems actually call, from recorded traffic and telemetry, and turn them into runtime-observed service dependencies.
**Better than REA:** OpenTelemetry and access logs (not only browser captures), cardinality- and OpenAPI-guided templating (W-06), caller attribution, schema-shape inference, and runtime-observed dependency edges in KGF.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-AS-001 | Inputs: HAR 1.2; OTLP/JSON trace exports (resource + scope spans) using OpenTelemetry semantic conventions (`http.request.method`, `http.route`, `url.full`, `url.path`, `server.address`, `server.port`, `http.response.status_code`, `messaging.system`, `messaging.destination.name`, `db.system`, `db.collection.name`/`db.sql.table`, `peer.service`, `service.name`); NGINX/Apache combined log format; JSON-lines logs with a configurable field mapping (`REVA_AS_LOG_MAPPINGS`). | Fixture per input type parses with exact record counts; malformed lines are counted and reported, not dropped silently. | integration |
| REVA-AS-002 | Streaming processing with bounded memory (≤ 512 MiB for 10 M records) using per-group accumulators; inputs up to 50 GiB per job. | Performance test meets REVA-NFR-006. | integration |
| REVA-AS-003 | Redaction (before anything is stored): remove values of `Authorization`, `Proxy-Authorization`, `Cookie`, `Set-Cookie`, `X-Api-Key`, `X-Auth-Token` and configurable headers; query parameters whose names match `(?i)(token\|secret\|password\|passwd\|pwd\|key\|sig\|signature\|code\|session\|auth)`; any value matching JWT, AWS access key, private-key PEM or generic high-entropy (≥ 4.0 bits/char over ≥ 32 chars) patterns. Bodies are **not** stored by default; only JSON key-shape summaries are kept. Every redaction is recorded with an RFC 6901 pointer and a reason. | Fixture with secrets in headers, query, body and URL path: no secret value appears in any warrant, blob, log or projection (byte search over the whole data volume). | integration |
| REVA-AS-004 | Templating, highest authority first: (1) OpenAPI/AsyncAPI specs ingested in KGF for that origin → exact template (`observed` for the match, `source_system_record` for the template); (2) OTel `http.route` → template as observed; (3) value-class rules per segment (integer, UUID, hex ≥ 8, ISO date, ULID, email, base64url ≥ 16); (4) cardinality inference: in a segment trie per `(method, origin)`, a position becomes `{param}` when ≥ `K` (default 3) distinct sibling values share the same prefix and suffix structure and each value's request volume share is < 50%. Each template records its basis and confidence. | E-07 regression: the three `svc-*` rotate calls collapse into `/api/v2/service-accounts/{param}/rotate` (basis `cardinality`); an OpenAPI fixture overrides with the named parameter `{accountId}`. | integration |
| REVA-AS-005 | Per operation: methods, statuses histogram, content types, request/response JSON key-shapes (key paths with types and presence ratios, no values), query parameter names, first/last seen, call count, p50/p95 latency when timings exist, callers. | Golden summary per fixture. | integration |
| REVA-AS-006 | Caller attribution: OTel client spans (`service.name` → `peer.service`/`server.address`); access logs via `REVA_AS_CALLER_MAP` (source CIDR/user-agent → service); HAR via a capture-level `caller_service` parameter. Unattributable calls keep `caller: unknown`. | Fixture with mixed attribution yields correct callers and an explicit unknown bucket. | integration |
| REVA-AS-007 | Output: `reva_ApiOperation` vertices, runtime-observed `reva_CALLS` edges (caller service → operation), and links from operations to static routes (via RR). Coverage records the time window, sampling (OTel sampled flag or configured rate) and dropped/malformed counts; sampled data always yields `partial`. | Coverage fields present and correct; sampled fixture reports partial. | integration |
| REVA-AS-008 | OpenAPI alignment report: operations observed but not in the spec (undocumented), in the spec but never observed in the window (unobserved, not "dead"), and parameter mismatches. | Fixture spec vs traffic yields all three categories. | integration |

### 7.12 Module DB — Database Schema Introspector
**Purpose:** bring database structure into the graph for lineage and impact analysis.
**Better than REA:** REA reads SQLite files. REVA introspects enterprise databases read-only, links tables to code resources and services, and never reads row data by default.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-DB-001 | SQLite: open with URI `file:<path>?mode=ro&immutable=1`, inventory tables, columns, PKs, FKs, indexes, views (SQL), triggers; record the DB file and `-wal` sibling digests; warn that a live DB/WAL copy may be non-atomic. | Fixture DB inventories exactly; the DB file's digest is unchanged after inspection. | integration |
| REVA-DB-002 | PostgreSQL, MySQL/MariaDB, SQL Server and Oracle via SQLAlchemy 2.x inspector: schemas, tables, columns (type, nullable, default), PKs, FKs, unique constraints, indexes, views (+ definition where the dialect exposes it), comments; optional row-count estimates from catalog statistics. Connections use KGF-stored credentials and are verified read-only before introspection (`SET TRANSACTION READ ONLY` / equivalent; refuse when the role can write, unless `REVA_DB_ALLOW_WRITABLE_ROLE=true`). | Integration tests against PostgreSQL and MySQL containers in CI; SQL Server and Oracle via optional CI lane (named skip when unavailable). | integration |
| REVA-DB-003 | Row sampling is disabled by default. When enabled per connection by tenant policy, sample ≤ `REVA_DB_SAMPLE_ROWS` (default 20) rows per table with PII masking (column-name heuristics + classification rules); samples are stored as restricted blobs. | Sampling off: no `SELECT` on user tables appears in the DB audit log of the test container. | integration |
| REVA-DB-004 | Linking: `reva_DbObject` vertices; FK edges; `reva_Resource(db_table)` from AB matched to DbObjects by `(db_instance mapping, schema, name)`, case-normalized per dialect; ambiguous matches → gap. | Fixture links code tables to DB tables; an ambiguous same-name table in two schemas produces a gap. | integration |
| REVA-DB-005 | Schema diff over time through GD (tables/columns added, removed, changed) with valid-time history. | Two snapshots yield the correct diff. | integration |

### 7.13 Module RR — Static↔Runtime Reconciler
**Purpose:** reconcile what code says *may* happen (AB) with what telemetry shows *did* happen (AS), without confusing the two.
**Better than REA:** REA reconciles JS static graphs with browser CDP captures. REVA reconciles service boundaries with production-grade telemetry across languages and produces actionable categories.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-RR-001 | Matching rules: static `http_route` ↔ observed server operation (same service, method, canonical template); static `http_call` ↔ observed client call (caller service, target operation); static topics ↔ messaging spans; static `db_table` resources ↔ DB spans. Each match issues a `reva.pred.observed_as` warrant (`inferred`, links to both sides, V-07). | Fixture with 10 static and 10 runtime items yields the expected 7 matches. | integration |
| REVA-RR-002 | Categories: `matched`, `static_only_unobserved` (never "dead" unless REVA-RR-003 holds), `runtime_only` (creates gap `GAP_RUNTIME_WITHOUT_SOURCE`), `ambiguous` (gap with candidates). | Each category is present in the fixture output. | integration |
| REVA-RR-003 | "Unused" claims: a static boundary may be labelled `unobserved_with_complete_coverage` only when runtime coverage for that service is `complete` for a window ≥ `REVA_RR_MIN_WINDOW_DAYS` (default 30) and unsampled. Otherwise it stays `static_only_unobserved`. | Partial-coverage fixture never yields the stronger label. | unit |
| REVA-RR-004 | Results project `reva_OBSERVED_AS` edges and update static elements with `observed_count`, `last_observed_at`. | Projection verified on each backend. | integration |

### 7.14 Module FT — Feature & Impact Trace Engine
**Purpose:** answer impact and feature questions over the whole KGF graph with paths, warrants, coverage and explicit frontiers.
**Better than REA:** REA traces within one application graph. REVA traces across services, repositories, resources, deployments, Jira stories, tests and owners, with typed question templates, valid-time as-of traversal, ACL filtering, weakest-link path strength and test-scope recommendations drawn from verifier-run coverage.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-FT-001 | Seeds (typed): `entity_id`, `string`, `service_account`, `config_key`, `env_var`, `route`, `topic`, `table`, `file_path`, `symbol`, `rule_id`, `jira_key`, `commit`, `api_operation`, `artifact`. Match modes `exact` (default for all but `string`) and `contains`; case sensitivity flag; an empty value is only allowed with `exact`. Seed resolution returns matches with a basis (`id, logical_key, label, property, alias`). | Each seed kind has a fixture; an empty `contains` seed is rejected. | unit |
| REVA-FT-002 | Traversal policies per question template, each a set of allowed edge labels with directions: `impact.downstream` (dependents), `impact.upstream` (dependencies), `impact.both`, plus named templates `impact.service_account`, `impact.rule_change`, `impact.feature_change`, `who_changed.symbol`, `incident.root_candidates`, `test_scope.change`. Templates are data (YAML in `reva/workflows/trace_templates/`), versioned, and listed by API. | Each template returns the golden result on the reference fixture graph (§13 RJ-03/RJ-04). | integration |
| REVA-FT-003 | Bounds: `max_depth` (default 6), `max_frontier` (default 5,000 nodes per hop), `max_paths` (default 200 returned; all counted). Hitting a bound records it in coverage and lists the unexpanded frontier with reasons (`DEPTH_LIMIT`, `FRONTIER_LIMIT`, `ACL_HIDDEN`, `EDGE_COVERAGE_UNKNOWN`). | A deep fixture reports exact frontier counts; ACL-hidden nodes are counted but never named. | integration |
| REVA-FT-004 | Path strength: per edge `(authority, epistemic, confidence_bp)` from the edge's warrant summary; path epistemic = weakest; path confidence = product of edge confidences (bp arithmetic, floor); path authority set = union. `contains_inference = true` if any edge is inferred. Results sort by confidence desc, then length asc. | Golden ordering on fixture. | unit |
| REVA-FT-005 | Output groups: impacted services, boundaries, resources, deployments/builds, repositories/files/symbols, Jira stories/epics, owners/teams, tests (REVA-FT-006), open gaps and contradictions in the subgraph; each item lists supporting paths and warrant IDs. | Group counts match the fixture expectations. | integration |
| REVA-FT-006 | Test-scope recommendation: tests whose per-test coverage contexts (from REVA verifier runs) touched any impacted symbol, ranked by number of impacted symbols hit; tests with stale coverage data (older than the symbol's current version) are flagged; when no coverage data exists, say so (gap), never "no tests needed". | Fixture with coverage maps recommends the expected tests; missing data produces a gap. | integration |
| REVA-FT-007 | As-of traversal: `as_of_valid` and `as_of_recorded` parameters restrict the graph to elements valid / known at those instants. | Fixture with time-varying ownership returns different owners for two as-of dates. | integration |
| REVA-FT-008 | Every trace result is itself a warrant (`reva.pred.trace_result`, `derived`, links to all edge warrants used, coverage composed) with a `trc1_` ID, so answers can cite it. | Re-running on unchanged data yields the same trace ID. | integration |
| REVA-FT-009 | Performance: REVA-NFR-004. Traversal pushes filters down to the backend where the GraphPort reports capability; otherwise it runs in REVA with batched neighbour fetches. | Benchmark passes on each backend in CI (Neptune via a Gremlin-compatible lane, or named skip). | integration |

### 7.15 Module GD — Graph Version Diff
**Purpose:** compare two versions of any REVA/KGF subgraph (service at commit A vs B; graph at time t1 vs t2; ontology versions) without identity churn.
**Better than REA:** fixes E-06 by matching on logical identity first, uses git rename detection, and works for any subgraph type.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-GD-001 | Inputs: two snapshot selectors (`{scope, commit}` or `{scope, as_of}`) or two warrant-backed graph exports. | Each selector type works on fixtures. | integration |
| REVA-GD-002 | Matching tiers, in order: (1) equal logical identity; (2) equal version identity (moved/renamed); (3) git rename/copy detection (`git diff -M50% -C`) mapping old→new paths; (4) structural fingerprint (identifier-insensitive normalized AST token hash, plus a MinHash similarity ≥ 0.8 for near matches); (5) semantic key (kind + sorted neighbour signature). Unresolved one-to-many matches are `ambiguous` with candidates (gap). | Each tier has a fixture where only that tier can match. | integration |
| REVA-GD-003 | Statuses: `unchanged, changed, added, removed, moved, renamed, ambiguous`; changed items list dimensions (`content, location, properties, relationships, coverage`) and property-level deltas. | **E-06 regression:** the v1→v2 fixture from §2.5 reports the 9 modules and the `accounts:rotate` handler as `changed`/`unchanged`, not removed+added; the new handler is `added`; the endpoint template change is `changed` with a property delta. | integration |
| REVA-GD-004 | Change graph projection: `reva_CHANGED_FROM` edges new→old with match basis and confidence; diff result warrant `reva.pred.graph_diff` with coverage (min of both sides). | Projection and warrant verified. | integration |
| REVA-GD-005 | Ontology/schema diff mode: classes, properties, constraints and DB schema objects compared with semantic categories (breaking / non-breaking / additive). | Fixture ontology pair yields correct categories. | integration |

### 7.16 Module DV — Source↔Deployed Drift Verifier
**Purpose:** prove (or refute) that a deployed artifact corresponds to the commit it claims, and surface configuration drift.
**Better than REA:** REA compares historical source with JS bundles. REVA verifies JARs, wheels, npm bundles, Go/Rust binaries and OCI images against commits and records the strength of each proof.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-DV-001 | Claim inputs: an artifact (or image) plus an expected commit (from a deployment record, Jira release, or user input). | API accepts all three sources. | integration |
| REVA-DV-002 | Checks (each a warrant): (a) embedded revision equals expected (SP-010); (b) not dirty (SP-011); (c) **JS bundles**: source-map `sourcesContent` digests equal the repo files at the commit (per file, with coverage); (d) **JVM**: class list/packages in the JAR equal the compiled output of the commit when a CI build artifact for that commit is registered in KGF; otherwise `unknown` with gap `GAP_NO_REFERENCE_BUILD`; (e) **Python/npm**: RECORD/lockfile digests equal the commit's lockfile resolution; (f) **reproducible-build mode** (optional): if a build recipe is registered (`reva-build.yaml`), rebuild in the sandbox and compare digests. | Fixture matrix covers match, mismatch and unknown for each check. | integration |
| REVA-DV-003 | Verdict: `verified_match` (all applicable checks pass at observed authority), `mismatch` (any check fails → contradiction), `unverifiable_dirty`, `unknown` (insufficient evidence; gaps created). Never `verified_match` from revision labels alone; labels give at most `claimed_match`. | Verdict table tests. | unit |
| REVA-DV-004 | Configuration drift: compare deployed config files found in artifacts/images with repo config at the commit (key-level diff, values hashed when classified sensitive). | Fixture with one changed key reports it with hashed values for a secret key. | integration |

### 7.17 Module VW — Views, Paging & Response Budgets
**Purpose:** let humans, APIs and LLM agents consume large evidence safely.
**Better than REA:** token-aware budgets, signed continuation tokens, summary-first defaults across REST, MCP and UI (W-07).

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-VW-001 | View kinds over any warrant or workflow result: `summary`, `facet` (named section), `item` (by key), `page` (offset/limit over a declared collection). Each view returns `{view_id, parent_id, coverage{status: complete_within_view\|page\|empty, examined, total, next_offset, exhausted}, items, limitations}`. | Paging through a 10,000-item collection returns every item exactly once in stable order. | integration |
| REVA-VW-002 | Budgets: every REST/MCP response has a byte budget (`REVA_RESPONSE_MAX_BYTES`, default 262,144) and an approximate token budget (`REVA_RESPONSE_MAX_TOKENS`, default 32,000; estimator `ceil(utf8_bytes/4)`). Workflows default to `summary` and include a ready-to-call continuation (`{tool\|endpoint, arguments}`) for the next page or facet. Over-budget results are never truncated mid-structure; the full result is retained and referenced. | Over-budget workflow returns summary + continuation; following continuations reconstructs the full result (digest equality). | integration |
| REVA-VW-003 | Continuation tokens are opaque, HMAC-SHA256-signed with a tenant key, bound to `(tenant, principal, parent_id, view request, offset)` and expire after `REVA_CONTINUATION_TTL_S` (default 3,600). | A token used by another principal or after expiry is rejected. | integration |
| REVA-VW-004 | Stable ordering: collections are ordered by a documented key (default: canonical ID). | Two identical requests return identical pages. | unit |

### 7.18 Module MC — MCP, REST and CLI surface
**Purpose:** expose REVA to agents, the UI and operators with strict, documented contracts.
**Better than REA:** one tenant-aware, authenticated server; tool catalogue grouped by task shape; contracts generated from the same Pydantic models; localized, remediable errors.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-MC-001 | REST API under `/api/reva/v1` implementing every endpoint in §9.1, authenticated and tenant-scoped through KGF's auth middleware (AuthPort). OpenAPI 3.1 is generated and published at `/api/reva/v1/openapi.json`. | Contract tests for every endpoint (success, validation error, unauthorized, not found, budget overflow). | acceptance |
| REVA-MC-002 | MCP server tools exactly as in §9.2, with JSON Schemas generated from Pydantic models; input schemas strict; output schemas describe successful results; errors use the error contract (§10.1). Tools are registered in KGF's MCP server when it exists (IP-06); otherwise REVA starts its own stdio and streamable-HTTP MCP server. | MCP conformance test: list tools, call each tool with valid and invalid input, check schemas and error shape. | acceptance |
| REVA-MC-003 | Tool shapes follow §9.2 categories (inspect, search, trace, compare, workflow, record, verify). No tool mixes discovery, execution and mutation modes. | Static review checklist in CI (tool metadata declares shape and effects). | static |
| REVA-MC-004 | Effect declarations: each tool/endpoint declares `effects ∈ {read_only, records_warrants, runs_sandbox, mutates_graph_via_gateway, external_io}` and MCP annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) consistent with them. | Metadata test. | unit |
| REVA-MC-005 | Untrusted-content marking: results that can include ingested content carry `_meta.reva.untrusted_content = true` and the content is wrapped in delimited fields (never interpolated into instructions). | Marker present on every content-bearing tool (test enumerates the catalogue). | acceptance |
| REVA-MC-006 | Progress and cancellation: long workflows emit progress notifications (MCP progress tokens; REST server-sent events at `/jobs/{id}/events`) and honour cancellation; cancellation results keep partial observations and report cleanup status. | Cancel mid-trace and mid-run; partial results and cleanup status are returned. | acceptance |
| REVA-MC-007 | CLI `kgf reva <command>` (or a standalone `reva` entry point if KGF has no CLI) covering §9.3, with `--json`, `--tenant`, exit codes (§10.2) consistent with the REST/MCP errors. | CLI acceptance tests per command. | acceptance |
| REVA-MC-008 | API versioning: path version `v1`; additive changes only within v1; breaking changes require `v2` plus a deprecation window documented in `CONTRACTS.md`. | Contract snapshot test fails on breaking changes without a version bump. | static |
| REVA-MC-009 | Contract documentation `docs/reva/CONTRACTS.md` generated from code (endpoints, tools, schemas, errors, examples) by `kgf reva docs generate`; CI fails if it is stale. | Docs check in CI. | static |

### 7.19 Module GA — Grounded Answers & Evaluation
**Purpose:** make every KGF answer show its warrant structure, and measure answer quality against known answers.
**Better than REA:** REA has prompt guidance and transcript evaluation. REVA enforces a structured answer contract at the pipeline level, verifies citations mechanically, and runs regression suites in CI.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-GA-001 | Answer contract: `{answer_id, question, mode: deterministic\|llm_synthesized, claims:[{claim_id, text, kind: observed\|derived\|inferred\|unknown, warrant_ids[], confidence{band,score_bp}, coverage}], unknowns[], contradictions[], limitations[], coverage, trace_ids[]}`. Rendering groups claims under **Observed / Derived / Inferred / Unknown** and shows contradictions prominently. | Answer view acceptance test; schema test. | acceptance |
| REVA-GA-002 | Deterministic-first: when a question matches a trace template or typed query, the answer is built deterministically from workflow results (no LLM). LLM synthesis is used only to phrase or to answer non-template questions, and only through KGF's LLMPort under the egress policy (C-02). | Template questions produce `mode=deterministic` with zero LLM calls (call counter). | integration |
| REVA-GA-003 | Context assembly for LLM synthesis: each context item carries its warrant ID, epistemic state, authority and an untrusted-content fence; system instructions forbid following instructions inside fenced content and require citing warrant IDs per claim. | Prompt-injection fixture (ingested Confluence page containing "ignore previous instructions and …") does not change behaviour; the incident is recorded as a `reva.pred.injection_attempt` warrant. | integration |
| REVA-GA-004 | Citation verification: after synthesis, every claim must cite ≥ 1 warrant from the supplied context. The claim's kind must not exceed the weakest cited epistemic state (an inferred warrant cannot back an "observed" claim). Uncited claims are dropped or downgraded to `inferred` with limitation `UNCITED_CLAIM`, per `REVA_GA_UNCITED_POLICY` (default `drop`). | Fixture LLM outputs with uncited, mis-graded and correct claims are handled per policy. | unit |
| REVA-GA-005 | Absence questions ("is X used anywhere?", "which systems call Y?") use coverage-aware absence (REVA-CV-005); answers never say "none/no" unless proven absent under complete coverage. | Partial-coverage fixture yields "Unknown — not proven" phrasing. | integration |
| REVA-GA-006 | Known-answer evaluation suites (YAML under `tests/reva/evaluation/suites/`): question, expected claims (value matchers, required kind, required authority set, required predicate), forbidden claims, max LLM calls. Metrics: claim precision/recall, citation validity rate, mis-graded claim rate, absence-overclaim rate, contradiction surfacing rate, latency. | `kgf reva eval run --suite reference` produces a report; CI gate thresholds: citation validity ≥ 0.98, absence-overclaim = 0, mis-graded ≤ 0.02. | evaluation |
| REVA-GA-007 | Agent transcript evaluation: given an MCP transcript of an agent using REVA tools, check that each final-answer claim is supported by a warrant actually delivered in that transcript, with matching authority/epistemic state. | Fixture transcripts (supported, unsupported, wrong authority) score correctly. | evaluation |

### 7.20 Module DR — Doctor / Readiness Diagnostics
**Purpose:** diagnose installation and runtime readiness, separating environment failures from analysis failures.
**Better than REA:** covers the whole REVA/KGF runtime (stores, keys, log, graph backends, sandbox, connectors, models), not agent-client registration.

| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-DR-001 | `kgf reva doctor [--json] [--scope all\|kernel\|sandbox\|graph\|extractors\|connectors\|models]` checks: Python version; REVA migrations applied; relational store connectivity and write test; blob store writable with free space ≥ `REVA_MIN_FREE_GB`; KEK present; producer and log keys present, decryptable, file mode 0600; latest STH verifies and log consistency since the last audit; graph backend reachable with a capability probe per backend (traversal, property filters, batch writes, transactions); tree-sitter grammars load; sandbox capabilities (namespaces, cgroup v2, docker/podman availability, prlimit); git available; connectors healthy (SourcePort); LLMPort local model reachable when GA synthesis is enabled; clock skew vs NTP reference (if reachable, else unknown); feature flags state. | Each check has pass/fail/unknown fixtures; JSON output validates against its schema. | integration |
| REVA-DR-002 | Each finding: `{check_id, status: pass\|fail\|warn\|unknown, category: environment\|configuration\|integrity\|capability, message, remediation, evidence}`. Exit code 0 only if no `fail`. | Exit code tests. | integration |
| REVA-DR-003 | Doctor results are exposed at `GET /doctor` (admin only) and summarized in KGF's health endpoint (IP-10) as `reva: ok\|degraded\|down`. | Health endpoint shows degraded when the blob store is read-only. | acceptance |

### 7.21 Module SEC — Security, privacy and tenancy
| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-SEC-001 | Tenant scoping: every REVA table has `tenant_id`; every query filters by the authenticated tenant at the data-access layer (repository base class), never only in routers. Blob paths include the tenant namespace; signing keys are per tenant. | Cross-tenant test suite: every endpoint and tool is called with tenant A credentials against tenant B IDs → 404, and nothing leaks in errors, timings beyond noise, or counts. | acceptance |
| REVA-SEC-002 | ACL inheritance: source-record warrants carry `source_acl_refs` from connectors (e.g. Confluence space permissions, Jira project roles, Git repo access). Effective visibility = source ACL ∩ envelope allow − deny. Derived warrants and workflow results inherit the **intersection** of the ACLs of all inputs (most restrictive). | A trace combining a restricted Confluence fact with public code facts is invisible to a user without Confluence access, and the trace reports `ACL_HIDDEN` frontier counts to users who lack access. | acceptance |
| REVA-SEC-003 | ACL revocation: when a connector reports revoked access, affected warrants, cached views, continuation tokens and trace results become invisible to the revoked principals within `REVA_ACL_PROPAGATION_S` (default 60 s). | Revocation journey (part of RJ-07). | acceptance |
| REVA-SEC-004 | Classification: warrants inherit classification from sources; statements of `restricted` warrants storing PII values use salted commitments (HMAC-SHA256 with a tenant secret) instead of raw values where the predicate declares `pii_fields`. | Fixture PII fields are stored as commitments; equality search via commitment works; raw values are absent from storage. | integration |
| REVA-SEC-005 | Redaction library shared by AS, VS (logs), MC (errors) and exports (§7.11 REVA-AS-003 patterns + configurable). | Secret-scan test over all REVA outputs in the acceptance run finds nothing. | acceptance |
| REVA-SEC-006 | Untrusted input handling: all parsers run in sandboxed workers (REVA-VS-010); REVA never fetches URLs found in content (no SSRF); archive extraction rules (REVA-AI-003). | Static check: no HTTP client usage in extractor modules; SSRF fixture with URLs in content triggers no network call (network namespace audit). | integration |
| REVA-SEC-007 | Keys: KEK-encrypted private keys; rotation and revocation (REVA-WK-010); public keys exportable; no private key ever in logs, errors, bundles or API responses. | Log and response scans in tests. | integration |
| REVA-SEC-008 | Authorization roles (mapped to KGF roles): `reva.viewer` (read warrants/results within ACL), `reva.analyst` (run workflows, record gaps), `reva.reviewer` (review obligations, resolve contradictions, waivers), `reva.verifier` (start verifier runs), `reva.admin` (keys, policies, doctor). | Role matrix test across endpoints/tools. | acceptance |
| REVA-SEC-009 | Audit: every mutating action (record gap, resolve contradiction, waive, start run, change policy, rotate key) is itself a warrant by the acting human/system producer. | Audit view lists actions with verifiable signatures. | integration |
| REVA-SEC-010 | Export control: bundles and ledger exports exclude warrants the exporting principal cannot see, and `restricted` warrants unless the policy allows; exports are logged as warrants. | Export by a limited user omits restricted items. | integration |
| REVA-SEC-011 | Sandbox hardening: verifier containers run as non-root, read-only root filesystem except the work dir, no Docker socket, `no-new-privileges`, dropped capabilities, seccomp default profile. | Container inspect test asserts each setting. | integration |
| REVA-SEC-012 | Retention: per-tenant policies (by predicate/classification) expire warrant envelopes and blobs while keeping the log leaf and a tombstone (`retracted_by_retention`); legal hold prevents expiry. Log proofs still verify after expiry. | Retention job fixture; proofs verify; expired content is unreadable. | integration |

### 7.22 Module UI — User Interface (React, inside KGF)
All screens use KGF's design system and tenant branding (C-08), WCAG 2.2 AA, keyboard navigable, localizable strings, and light/dark themes.

| ID | Screen / component | Must show / do | Depth |
|---|---|---|---|
| REVA-UI-001 | Shared components: `EpistemicBadge` (Observed/Derived/Inferred/Unknown/Unavailable, with colour **and** icon + text), `AuthorityChip`, `ConfidenceMeter` (band + %), `CoverageMeter` (status, examined/omitted, limits, "Unknown — not proven empty" rule), `WarrantDrawer` (body, envelope, signature status, log inclusion proof verification, links graph), `GapCallout`, `ContradictionBanner`. | Storybook stories plus Playwright visual tests; axe accessibility checks pass. | acceptance |
| REVA-UI-002 | **Warrant Explorer**: search/filter warrants (subject, predicate, producer, authority, epistemic, time, classification); open WarrantDrawer; verify signature/proof client-side (WebCrypto Ed25519 where available, else server verify endpoint). | Journey RJ-01 steps. | acceptance |
| REVA-UI-003 | **Transparency Log**: STH timeline, tree size, auditor status, proof verifier tool (paste a warrant ID → inclusion proof result). | Proof verification on a fixture warrant. | acceptance |
| REVA-UI-004 | **Proof-of-Done Board**: obligations matrix (rows = obligations, columns = case kinds × status), filters (requirement, layer, owner, status), per-obligation detail with the ordered closure checks and reason codes, linked verifier runs, attestations, coverage hits and mutation scores; "Asserted done — unproven" lane for board items without closure; export buttons (JSON/MD/HTML). | RJ-06. | acceptance |
| REVA-UI-005 | **Verifier Run Detail**: lineage tree, environment fingerprint, test outcomes, rerun matrix, per-owner coverage, mutation results, artifacts (download), attestation verification. | RJ-06. | acceptance |
| REVA-UI-006 | **Knowledge-Gap Board** (kanban by status; sort by impact; owner/due date; probes with "Run probe" action; revision history diff). | RJ-05. | acceptance |
| REVA-UI-007 | **Contradiction Center**: open conflicts with members side by side (values, authority, valid time), suggested rule outcome, resolve with rationale (human decision), affected items list. | RJ-02. | acceptance |
| REVA-UI-008 | **Artifact & SBOM Explorer**: inventory tree (paged), integrity status, components table, commit linkage (with gap if missing), dirty flag, CycloneDX/SPDX download. | RJ-09. | acceptance |
| REVA-UI-009 | **Service Boundary Map**: services, routes, calls (static inferred vs runtime observed styled distinctly), resources; filter by service/repo; click-through to source spans. Large graphs use server-side aggregation and progressive disclosure (≤ 2,000 rendered elements at once). | RJ-03. | acceptance |
| REVA-UI-010 | **API Surface Explorer**: operations with templates (basis badge), statuses, callers, key-shapes, OpenAPI alignment categories. | RJ-10. | acceptance |
| REVA-UI-011 | **Reconciliation View**: matched / static-only / runtime-only / ambiguous lists with counts and window/coverage banner. | RJ-10. | acceptance |
| REVA-UI-012 | **Impact Trace Studio**: seed picker (typed), template picker, as-of pickers, results grouped (§7.14 FT-005), path viewer with per-edge warrants and epistemic styling, frontier panel with reasons, test-scope list, "Create gap" from frontier, export as answer. | RJ-03, RJ-04. | acceptance |
| REVA-UI-013 | **Graph Diff Viewer**: side-by-side and change list with statuses and match bases; ambiguous items queue. | RJ-11. | acceptance |
| REVA-UI-014 | **Drift Verification**: verdict, check list with authority, evidence links, gaps. | RJ-09. | acceptance |
| REVA-UI-015 | **Answer View integration** in KGF's NL query screen: claims grouped by kind with badges, citations open the WarrantDrawer, contradictions and unknowns sections. | RJ-08. | acceptance |
| REVA-UI-016 | **Evaluation Dashboard**: suite runs, metrics over time, failing cases with diffs. | RJ-08. | acceptance |
| REVA-UI-017 | **Doctor & Settings** (admin): doctor results with remediation; policies (egress, integrity, budgets, auto-probes, retention, mutation threshold), key management (rotate, revoke, export public keys). | Admin journey within RJ-12. | acceptance |

### 7.23 Module OB — Observability & Operations
| ID | Requirement | Acceptance criteria | Depth |
|---|---|---|---|
| REVA-OB-001 | Prometheus metrics: `reva_warrants_issued_total{predicate,producer_type}`, `reva_issue_seconds` (histogram), `reva_translog_size{log}`, `reva_sth_age_seconds`, `reva_integrity_violations_total`, `reva_closure_status{status}`, `reva_verifier_run_seconds{profile}`, `reva_sandbox_failures_total{reason}`, `reva_extractor_seconds{extractor}`, `reva_coverage_partial_total{producer}`, `reva_view_budget_overflows_total`, `reva_gaps_open{severity}`, `reva_contradictions_open`. | `/metrics` scrape test lists all metrics. | integration |
| REVA-OB-002 | Structured JSON logs with `tenant_id`, `correlation_id`, `principal`, `operation`, no secrets (redaction filter). | Log scan test. | integration |
| REVA-OB-003 | OpenTelemetry traces for REVA workflows and extractor jobs (exported to KGF's collector if configured; no-op otherwise). | Span names present in an in-memory exporter test. | integration |
| REVA-OB-004 | Runbook `docs/reva/RUNBOOK.md`: key rotation, log audit failure response, restore from backup with log consistency verification, sandbox troubleshooting, re-projection of the graph from warrants (`kgf reva reproject`). | Each runbook procedure is executed in the acceptance environment at least once (RJ-12). | acceptance |
| REVA-OB-005 | Backup/restore: relational store dump + blob store + keys (encrypted) + logs; restore verifies every warrant ID and log consistency before serving. | Restore drill in RJ-12. | acceptance |
| REVA-OB-006 | Re-projection: `kgf reva reproject [--backend X]` rebuilds all REVA graph elements from warrants (idempotent), enabling backend migration without data loss. | Reprojection into an empty backend yields the same element counts and properties. | integration |

### 7.24 Module XP — Optional Forensics Extension Pack (DEFER; disabled by default)
These capture the remaining REA families for completeness. They are **not** part of the REVA 1.0 completion scope. Each is enabled per tenant with `REVA_XP_<NAME>=true` and requires a reviewed, approved obligation set before implementation starts.

| ID | Capability (enhanced design) | Notes |
|---|---|---|
| REVA-XP-001 | Native binary inventory without decompilation: headers, sections, imports/exports, symbols, linked libraries, signatures (ELF/PE/Mach-O via pyelftools/pefile/macholib), producing warrants and SBOM hints. | Useful for licence/SBOM completeness of closed-source vendor binaries. |
| REVA-XP-002 | Decompiler adapter port (Ghidra headless only, open-source), sandboxed, outputs function inventories as `shipped_artifact` warrants. | Requires a separate security review; Ghidra installed by the tenant. |
| REVA-XP-003 | WASM module interface inventory (imports/exports/sections) via a pure-Python parser. | |
| REVA-XP-004 | Android APK manifest/permissions/components inventory (zip + binary XML parser), no device interaction. | |
| REVA-XP-005 | PE resource inventory (version info, manifests) for Windows software catalogues. | |
| REVA-XP-006 | Live browser capture producing HAR for AS (Playwright, sandboxed, explicit origin allowlist). | Live interaction requires a tenant opt-in. |
| — | Debuggers, dynamic instrumentation, firmware, pcap, logic signals, EVM, DOS/console profiles | **Rejected**; see §16. |

---

## 8. Non-functional requirements
Reference hardware for budgets: single node, 8 vCPU, 32 GiB RAM, NVMe SSD, PostgreSQL 16 on the same node, HugeGraph (RocksDB) on the same node.

| ID | Requirement | Measurement |
|---|---|---|
| REVA-NFR-001 | Warrant issue throughput ≥ 1,000 warrants/s in batch mode (≤ 4 KiB statements, blobs ≤ 64 KiB) on PostgreSQL; ≥ 300/s on SQLite. | `tests/reva/perf/test_issue_throughput.py`, 5 runs, median reported |
| REVA-NFR-002 | Single `issue()` latency p95 ≤ 25 ms (excluding blobs > 1 MiB). | Same harness |
| REVA-NFR-003 | Warrant read by ID with signature + ID verification p95 ≤ 10 ms. | Perf harness |
| REVA-NFR-004 | Impact trace p95 ≤ 3 s for depth ≤ 6 and ≤ 50,000 traversed edges on HugeGraph and Neo4j; the result includes coverage and frontier. | `perf/test_trace.py` on the synthetic 1M-edge enterprise fixture |
| REVA-NFR-005 | Boundary extraction ≥ 1,500 source files/min per worker; incremental re-extraction of a 1-file change in a 10k-file repo ≤ 20 s. | `perf/test_ab.py` |
| REVA-NFR-006 | API surface mining ≥ 100,000 log records/s per worker for access logs; memory ≤ 512 MiB at 10M records. | `perf/test_as.py` |
| REVA-NFR-007 | Artifact inventory of a 1 GiB JAR/OCI image ≤ 90 s; memory ≤ 1 GiB. | `perf/test_ai.py` |
| REVA-NFR-008 | Transparency log append p95 ≤ 5 ms; inclusion proof generation ≤ 20 ms at 100M leaves (logarithmic node cache). | `perf/test_tl.py` (simulated sizes) |
| REVA-NFR-009 | UI: views render first content ≤ 1.5 s, interactions p95 ≤ 200 ms for pages ≤ 500 rows; graph views ≤ 2,000 rendered elements. | Playwright performance marks |
| REVA-NFR-010 | Availability: REVA failures degrade gracefully; KGF core keeps working with REVA disabled or down (flags), and REVA health reports `degraded`/`down`. | Chaos test: stop the REVA worker; KGF core journeys still pass |
| REVA-NFR-011 | Durability: no acknowledged warrant is lost on process crash (fsync/transaction commit before acknowledgement). | Crash-injection test (REVA-WK-007) |
| REVA-NFR-012 | Determinism: identical inputs produce identical warrant IDs, trace IDs, diff IDs and ledger IDs across runs, machines and backends. | Determinism suite run twice on two CI runners; IDs compared |
| REVA-NFR-013 | Portability: Linux x86-64 and arm64 containers; extractors pure Python except tree-sitter wheels; sandbox degrades to subprocess+rlimits when containers/cgroups are unavailable (recorded as environment limitation). | CI matrix |
| REVA-NFR-014 | Air-gap: full test suite passes with network disabled (except container image pulls pre-cached). | CI job with `--network none` |
| REVA-NFR-015 | Scalability: warrant store tested to 100M warrants (partitioned by tenant and month on PostgreSQL); indexes on `(tenant_id, subject_key)`, `(tenant_id, predicate)`, `(tenant_id, recorded_at)`, link table indexes. | Synthetic load test (nightly lane) |
| REVA-NFR-016 | Accessibility WCAG 2.2 AA; i18n: all UI strings in resource bundles (en default; structure ready for more locales); dates and numbers localized. | axe + i18n lint |
| REVA-NFR-017 | Code quality: type-checked (mypy strict for `reva/`), lint clean (ruff), no duplicated blocks > 40 lines (jscpd or ruff equivalent), no dead code (vulture with allowlist). | CI static lane |
| REVA-NFR-018 | Test coverage: line ≥ 90% and branch ≥ 85% for `reva/core`, `reva/kernel`, `reva/pd`; ≥ 80% line for other packages. **Coverage is a floor, never proof of completion** (§0.4). | CI coverage lane |
| REVA-NFR-019 | Mutation score (REVA's own probe, REVA-PD-005) ≥ 0.75 for `reva/core`, `reva/kernel`, `reva/pd`. | Nightly lane |
| REVA-NFR-020 | Security: dependency audit (pip-audit, npm audit) with no known high/critical vulnerabilities at release; SBOM of REVA itself generated by REVA (dogfooding SP). | Release lane |
| REVA-NFR-030 | Contract stability: semantic versioning of REST/MCP/warrant schemas; a migration tool for warrant schema versions (`reva.warrant/1` → future versions) without changing existing IDs. | Contract snapshot tests |

---

## 9. Interface catalogue

### 9.1 REST endpoints (`/api/reva/v1`)
All endpoints: tenant from auth context; JSON; errors per §10.1; list endpoints support `view`, `offset`, `limit`, `continuation`.

| ID | Method & path | Purpose | Role |
|---|---|---|---|
| REVA-IF-001 | `POST /warrants` | Issue warrant from draft (system/human producers; extractors use internal API) | analyst+ |
| REVA-IF-002 | `GET /warrants/{warrant_id}` | Get warrant (verified) | viewer |
| REVA-IF-003 | `GET /warrants` | Query by subject, predicate, producer, authority, epistemic, time, as-of | viewer |
| REVA-IF-004 | `GET /warrants/{id}/links?direction=in\|out&rel=` | Link neighbourhood | viewer |
| REVA-IF-005 | `POST /warrants/{id}/supersede`, `POST /warrants/{id}/retract` | Supersede/retract | reviewer |
| REVA-IF-006 | `POST /bundles/export`, `POST /bundles/import`, `GET /bundles/{id}` | Bundles | analyst / admin (import) |
| REVA-IF-007 | `GET /predicates`, `GET /operations` | Registries | viewer |
| REVA-IF-008 | `GET /producers`, `POST /producers`, `POST /producers/{id}/keys/rotate`, `POST /keys/{key_id}/revoke`, `GET /keys/public` | Producers and keys | admin |
| REVA-IF-010 | `GET /gaps`, `POST /gaps`, `GET /gaps/{gap_id}`, `PATCH /gaps/{gap_id}` (with `expected_revision`), `GET /gaps/{gap_id}/revisions`, `POST /gaps/{gap_id}/probes/{n}/run` | Knowledge gaps | viewer / analyst |
| REVA-IF-015 | `GET /contradictions`, `GET /contradictions/{id}`, `POST /contradictions/{id}/resolve` | Contradictions | viewer / reviewer |
| REVA-IF-020 | `GET /obligations`, `POST /obligations/sync` (load YAML), `POST /obligations/propose-from-jira/{issue_key}`, `POST /obligations/{key}/review`, `GET /obligations/{key}` | Obligations | viewer / reviewer |
| REVA-IF-021 | `GET /bindings`, `PUT /bindings/{obligation_key}` | Bindings | reviewer |
| REVA-IF-022 | `POST /runs` (start verifier run for binding(s)), `GET /runs/{run_id}`, `POST /runs/{run_id}/cancel`, `GET /runs/{run_id}/artifacts/{kind}` | Verifier runs | verifier |
| REVA-IF-023 | `POST /closure/evaluate` (scope), `GET /ledgers/{ledger_id}`, `GET /ledgers/{id}/export?format=json\|md\|html` | Closure and ledgers | viewer |
| REVA-IF-024 | `GET /gates`, `POST /gates/{gate_id}/evaluate` | Readiness gates | viewer / verifier |
| REVA-IF-025 | `POST /waivers`, `GET /waivers` | Waivers | reviewer |
| REVA-IF-026 | `GET /attestations/{att_id}`, `POST /attestations/verify` | Attestations | viewer |
| REVA-IF-030 | `GET /logs/{log_id}/sth`, `GET /logs/{log_id}/sth/history` | Tree heads | viewer |
| REVA-IF-031 | `GET /logs/{log_id}/proof/inclusion`, `GET /logs/{log_id}/proof/consistency` | Proofs | viewer |
| REVA-IF-040 | `POST /artifacts` (upload, streaming) , `GET /artifacts/{artifact_id}`, `GET /artifacts/{id}/inventory` (view) | Artifacts | analyst |
| REVA-IF-041 | `POST /provenance/analyze` (artifact or image), `GET /sbom/{artifact_id}?format=cyclonedx\|spdx` | Provenance/SBOM | analyst |
| REVA-IF-042 | `POST /boundaries/extract` (repo, commit, incremental), `GET /services`, `GET /services/{id}/boundaries` | Boundaries | analyst |
| REVA-IF-043 | `POST /apisurface/ingest` (HAR/OTLP/log upload or connector source), `GET /apisurface/operations` | API surface | analyst |
| REVA-IF-044 | `POST /dbschema/introspect` (connection id), `GET /dbschema/{db_instance}` | DB schema | analyst |
| REVA-IF-045 | `POST /reconcile` (service scope, window) | Reconciliation | analyst |
| REVA-IF-050 | `POST /trace` (seed, template, bounds, as-of), `GET /trace/templates`, `GET /trace/{trace_id}` | Feature/impact trace | viewer (results ACL-filtered) |
| REVA-IF-051 | `POST /diff` (two selectors), `GET /diff/{diff_id}` | Graph diff | viewer |
| REVA-IF-052 | `POST /drift/verify` (artifact, expected commit) | Drift verification | analyst |
| REVA-IF-060 | `POST /answers/ground` (question + optional template) → answer contract | Grounded answers | viewer |
| REVA-IF-061 | `POST /eval/runs` (suite), `GET /eval/runs/{id}` | Evaluation | analyst |
| REVA-IF-070 | `GET /views/{parent_id}` (view request params) | Views/paging | viewer |
| REVA-IF-071 | `GET /jobs/{job_id}`, `GET /jobs/{job_id}/events` (SSE), `POST /jobs/{job_id}/cancel` | Jobs | owner of job |
| REVA-IF-080 | `GET /doctor` | Readiness | admin |
| REVA-IF-081 | `GET /policies`, `PUT /policies/{name}` | Policies | admin |

### 9.2 MCP tools (names prefixed `reva_`)
| Tool | Shape | Effects | Maps to |
|---|---|---|---|
| `reva_inspect_warrant` | inspect | read_only | IF-002/004 |
| `reva_search_warrants` | search | read_only | IF-003 |
| `reva_trace_impact` | trace | records_warrants | IF-050 |
| `reva_list_trace_templates` | search | read_only | IF-050 |
| `reva_compare_graph_versions` | compare | records_warrants | IF-051 |
| `reva_verify_drift` | workflow | records_warrants | IF-052 |
| `reva_inspect_artifact` | inspect | records_warrants | IF-040/041 |
| `reva_get_sbom` | inspect | read_only | IF-041 |
| `reva_list_services` / `reva_inspect_service` | search / inspect | read_only | IF-042 |
| `reva_extract_boundaries` | workflow | records_warrants, runs_sandbox | IF-042 |
| `reva_inspect_api_surface` | inspect | read_only | IF-043 |
| `reva_reconcile_runtime` | workflow | records_warrants | IF-045 |
| `reva_inspect_db_schema` | inspect | read_only | IF-044 |
| `reva_list_gaps` / `reva_record_gap` / `reva_update_gap` | search / record / record | read_only / records_warrants | IF-010 |
| `reva_list_contradictions` | search | read_only | IF-015 |
| `reva_get_closure_status` | inspect | read_only | IF-023 |
| `reva_evaluate_closure` | verify | records_warrants | IF-023 |
| `reva_start_verifier_run` | workflow | runs_sandbox, records_warrants | IF-022 |
| `reva_ground_answer` | workflow | records_warrants (LLM via egress policy) | IF-060 |
| `reva_inspect_view` | inspect | read_only | IF-070 |
| `reva_verify_proof` | verify | read_only | IF-026/031 |

MCP prompts (optional starting points, never mandatory sequences): `reva_investigate_impact`, `reva_verify_completion`, `reva_audit_gaps`, `reva_compare_releases`. Each embeds the evidence discipline: report observations only from cited warrants; label inference with confidence and alternatives; keep incomplete coverage explicit as Unknown; never turn absence under incomplete coverage into "none".

### 9.3 CLI (`kgf reva …`)
`doctor`, `warrant get|search|export|import`, `log sth|verify|prove`, `gap list|record|update`, `contradiction list|resolve`, `obligation sync|list|review|propose-jira`, `binding set|show`, `run start|show|cancel`, `closure evaluate`, `ledger export --format json|md|html`, `gate evaluate`, `artifact add|inventory|sbom`, `provenance analyze`, `boundaries extract`, `apisurface ingest`, `dbschema introspect`, `reconcile`, `trace`, `diff`, `drift verify`, `answer`, `eval run`, `reproject`, `keys rotate|revoke|export`, `docs generate`, `verify-attestation`. Every command supports `--json`, `--tenant`, `--quiet`; exit codes per §10.2.

### 9.4 Events
`reva.warrant.issued|superseded|retracted|integrity_violation`, `reva.gap.changed`, `reva.contradiction.opened|resolved`, `reva.obligation.stale|closed|reopened`, `reva.run.started|finished|cancelled`, `reva.ledger.published`, `reva.sth.issued`. Payload: `{event_id, tenant_id, type, occurred_at, subject_id, summary}` (no content bodies).

---

## 10. Catalogues

### 10.1 Error contract
Every error (REST body, MCP `isError` text, CLI `--json` output):
```json
{
  "error": {
    "code": "REVA_E_…",
    "category": "invalid_input | not_found | conflict | unauthorized | forbidden | integrity | resource_limit | unavailable | timeout | cancelled | internal",
    "message": "Localized, user-safe message (no internals, no secrets)",
    "retryable": false,
    "remediation": {"action": "What the caller should do next", "continuation": null},
    "details": {"issues": [{"pointer": "/seed/value", "reason": "…"}], "partial": null, "limits": null},
    "correlation_id": "…"
  }
}
```
Minimum codes: `REVA_E_SCHEMA_UNKNOWN_FIELD`, `REVA_E_VALIDATION`, `REVA_E_CANONICALIZATION`, `REVA_E_PREDICATE_UNKNOWN`, `REVA_E_PRODUCER`, `REVA_E_SIGNATURE`, `REVA_E_INTEGRITY`, `REVA_E_NOT_FOUND`, `REVA_E_CONFLICT`, `REVA_E_UNAUTHORIZED`, `REVA_E_FORBIDDEN`, `REVA_E_BUDGET_EXCEEDED`, `REVA_E_CONTINUATION_INVALID`, `REVA_E_RESOURCE_LIMIT`, `REVA_E_DIRTY_TREE`, `REVA_E_SANDBOX_UNAVAILABLE`, `REVA_E_TIMEOUT`, `REVA_E_CANCELLED`, `REVA_E_BACKEND_CAPABILITY`, `REVA_E_EGRESS_DENIED`, `REVA_E_UNSUPPORTED_FORMAT`, `REVA_E_MALFORMED_INPUT`, `REVA_E_INTERNAL`. A user-visible error catalogue (`docs/reva/errors.csv`: code, trigger, message, risk, remediation, test) is generated and kept complete by a CI check.

### 10.2 CLI exit codes
`0` success · `1` completed with findings (e.g. doctor fail, gate not passed, verdict mismatch) · `2` invalid input · `3` not found · `4` integrity failure · `5` unavailable/environment · `6` timeout · `7` cancelled · `8` unauthorized/forbidden · `70` internal error.

### 10.3 Limitation codes (minimum set)
`STATIC_NOT_RUNTIME`, `DYNAMIC_DISPATCH_UNRESOLVED`, `REFLECTION_UNRESOLVED`, `RUNTIME_REGISTRATION_UNSEEN`, `PARSE_ERRORS_PRESENT`, `FILE_SIZE_LIMIT`, `GENERATED_CODE_SKIPPED`, `VENDORED_SKIPPED`, `TEMPLATE_PARTIAL`, `CONFIG_PROFILE_AMBIGUOUS`, `SAMPLED_TELEMETRY`, `WINDOW_LIMITED`, `CALLER_UNATTRIBUTED`, `REDACTED_VALUES`, `ARCHIVE_LIMIT_REACHED`, `INTEGRITY_CONTINUED`, `LEGACY_FORMAT_UNSUPPORTED`, `METADATA_ABSENT_NOT_PROOF`, `SUBJECT_IDENTITY_UNAVAILABLE`, `ACL_HIDDEN_ITEMS`, `DEPTH_LIMIT`, `FRONTIER_LIMIT`, `EDGE_COVERAGE_UNKNOWN`, `MODEL_INFERENCE`, `RULE_DERIVATION`, `HISTORICAL_SOURCE`, `NON_ATOMIC_SNAPSHOT`, `UNCITED_CLAIM`, `ENVIRONMENT_DEGRADED_SANDBOX`.

### 10.4 Predicate catalogue (minimum set; each with a Pydantic statement model)
`reva.pred.source_record` · `reva.pred.artifact_inventory` · `reva.pred.integrity_violation` · `reva.pred.go_buildinfo` · `reva.pred.rust_dependencies` · `reva.pred.dotnet_assembly` · `reva.pred.jvm_archive` · `reva.pred.python_distribution` · `reva.pred.npm_package` · `reva.pred.oci_image` · `reva.pred.os_packages` · `reva.pred.built_from_commit` · `reva.pred.dirty_build` · `reva.pred.vulnerability_match` · `reva.pred.service_identity` · `reva.pred.boundary` · `reva.pred.resource_access` · `reva.pred.endpoint_match` · `reva.pred.api_operation` · `reva.pred.api_caller` · `reva.pred.openapi_alignment` · `reva.pred.db_object` · `reva.pred.db_link` · `reva.pred.observed_as` · `reva.pred.reconciliation_summary` · `reva.pred.trace_result` · `reva.pred.graph_diff` · `reva.pred.drift_check` · `reva.pred.drift_verdict` · `reva.pred.gap_revision` · `reva.pred.contradiction_decision` · `reva.pred.obligation_review` · `reva.pred.waiver` · `reva.pred.verifier_run` · `reva.pred.closure_decision` · `reva.pred.ledger` · `reva.pred.answer` · `reva.pred.eval_result` · `reva.pred.injection_attempt` · `reva.pred.policy_change` · `reva.pred.key_event` · `reva.pred.human_assertion`.

### 10.5 Gap templates
`GAP_COVERAGE_PARTIAL`, `GAP_AMBIGUOUS_ENDPOINT_MATCH`, `GAP_AMBIGUOUS_DIFF_MATCH`, `GAP_RUNTIME_WITHOUT_SOURCE`, `GAP_COMMIT_NOT_INGESTED`, `GAP_TRACE_FRONTIER`, `GAP_NO_REFERENCE_BUILD`, `GAP_NO_TEST_COVERAGE_DATA`, `GAP_DYNAMIC_IPC_CHANNEL`, `GAP_AMBIGUOUS_DB_LINK`, `GAP_UNRESOLVED_SERVICE_URL`. Each template defines question text (with placeholders), domain, default severity, required authority/depth, and recommended probes.

### 10.6 Closure reason codes
`OBLIGATION_INACTIVE`, `OBLIGATION_UNREVIEWED`, `DEPENDENCY_OPEN`, `CLOSURE_BLOCKED_GAP`, `CLOSURE_BLOCKED_CONTRADICTION`, `BINDING_INVALID`, `OWNER_NOT_FOUND`, `OWNER_AMBIGUOUS`, `OWNER_STALE`, `NO_RUN_AT_COMMIT`, `ATTESTATION_INVALID`, `DEPTH_INSUFFICIENT`, `AUTHORITY_INSUFFICIENT`, `AG01_NON_PASS_OUTCOME`, `AG02_MARKER_MISSING`, `AG03_OWNER_NOT_EXECUTED`, `AG04_MUTATION_SCORE_LOW`, `AG05_NO_MEANINGFUL_ASSERTION`, `AG06_OWNER_MOCKED`, `AG07_FLAKY`, `AG08_STALE_DIGEST`, `AG09_DIRTY_CHECKOUT`, `AG10_ENVIRONMENT_UNRECORDED`, `AG11_VERIFIER_ARGV_MISMATCH`, `AG12_ARTIFACT_MISSING`, `AG13_NO_TESTS`, `AG14_FIXTURE_DIGEST_MISMATCH`, `CASE_KIND_UNCOVERED`, `NONDETERMINISM_SPEC_UNMET`, `PERFORMANCE_BUDGET_UNMET`, `JOURNEY_MISSING`, `JOURNEY_FAILED`, `ARTIFACT_MALFORMED`, `CLOSED`.

---

## 11. Configuration catalogue (environment variables; all have defaults)
| Variable | Default | Meaning |
|---|---|---|
| `REVA_ENABLED` | `false` (→ `true` after P1) | Master flag (IP-01) |
| `REVA_STORE_URL` | KGF Postgres URL if present, else `sqlite:///<data>/reva/reva.db` | Relational store |
| `REVA_BLOB_ROOT` | `<data>/reva/blobs` | Blob store root (or `s3://…` with `REVA_S3_*`) |
| `REVA_KEK` | (required; from KGF secret store) | Key-encryption key (32 bytes, base64) |
| `REVA_STH_INTERVAL_S` | `60` | STH cadence |
| `REVA_AUDIT_SAMPLE` | `0.01` | Auditor sample ratio |
| `REVA_STH_WITNESS_DIR` | unset | Optional witness export |
| `REVA_GRAPH_PROJECTION` | `true` | Project into graph (IP-03) |
| `REVA_GRAPH_WARRANT_REF_CAP` | `32` | Warrant refs stored on graph elements |
| `REVA_INGEST_WARRANTS` | `false` | Connector warrants (IP-04) |
| `REVA_ANSWER_CONTRACT` | `false` | Enforce grounded answers (IP-05) |
| `REVA_MCP` / `REVA_UI` / `REVA_PD_BOARDS` | `true` | Integration flags |
| `REVA_MAX_RUNS` | `2` | Concurrent verifier runs per tenant |
| `REVA_RERUNS` | `3` | Closure reruns |
| `REVA_MUTATION_MIN` | `0.70` | Mutation kill threshold |
| `REVA_SANDBOX_MODE` | `auto` (`container` if Docker/Podman available, else `process`) | Sandbox engine |
| `REVA_RESPONSE_MAX_BYTES` / `REVA_RESPONSE_MAX_TOKENS` | `262144` / `32000` | Budgets |
| `REVA_CONTINUATION_TTL_S` | `3600` | Continuation lifetime |
| `REVA_AB_MAX_FILE_BYTES` | `2097152` | Boundary extractor file cap |
| `REVA_SERVICE_URL_MAP` | `{}` (JSON) | Base URL → service mapping |
| `REVA_SERVICE_ACCOUNT_PATTERNS` | `["svc-[a-z0-9-]+", "sa-[a-z0-9-]+", "[a-z0-9-]+@[a-z0-9-]+\\.iam\\.gserviceaccount\\.com"]` | Service-account detection |
| `REVA_AS_LOG_MAPPINGS` / `REVA_AS_CALLER_MAP` | `{}` | API surface mappings |
| `REVA_DB_SAMPLE_ROWS` | `0` (disabled) | Row sampling |
| `REVA_DB_ALLOW_WRITABLE_ROLE` | `false` | Safety override |
| `REVA_RR_MIN_WINDOW_DAYS` | `30` | Unused-claim window |
| `REVA_AUTO_PROBES` | `false` | Automatic probe execution |
| `REVA_GAP_WEIGHTS` | `{"low":1,"medium":2,"high":4,"critical":8}` | Impact weights |
| `REVA_JIRA_WRITEBACK` | `false` | Jira comment write-back |
| `REVA_VULN_MATCH` / `REVA_OSV_MIRROR_DIR` | `false` / unset | Offline vulnerability matching |
| `REVA_GA_UNCITED_POLICY` | `drop` | Uncited claim policy |
| `REVA_ACL_PROPAGATION_S` | `60` | Revocation propagation |
| `REVA_MIN_FREE_GB` | `10` | Doctor threshold |
| `REVA_XP_<NAME>` | `false` | Forensics pack toggles |
| `REVA_BOOTSTRAP_REVIEWER` | unset | Human principal who reviews obligations in bulk (never an agent) |
| `REVA_ALLOW_DEGRADED_UNIT` | `false` | Accept unit runs without network isolation (recorded as a limitation) |
| `REVA_MUTATION_MAX_MUTANTS` | `60` | Mutants per owner (deterministic sampling above this) |
| `REVA_SP_MAX_BINARY_SCAN` | `200` | Executables scanned per image for Go/Rust metadata |
| `REVA_AS_MAX_RECORD_BYTES` | `8388608` | Max bytes per HAR entry / log record |
| `REVA_DB_INSTANCE_MAP` | `{}` | Connection id → logical DB instance name for linking |
| `REVA_SERVICE_NAME_MAP` | `{}` | Telemetry `service.name` → REVA service logical key |
| `REVA_FIXTURE_CACHE` | `.reva-fixtures` | Built-fixture cache (tests only) |
| `REVA_TEST_FAULTS` | unset | Test-only fault injection; doctor fails if set in production |

---

## 12. Test and verification requirements
| ID | Requirement |
|---|---|
| REVA-TST-001 | Test depth taxonomy mirrors §6.7. Directories: `tests/reva/unit`, `component`, `integration`, `acceptance`, `conformance` (per graph backend and per sandbox profile), `evaluation`, `perf`. A test's directory must match its declared depth marker (`@pytest.mark.reva_depth("unit")`); CI enforces the match. |
| REVA-TST-002 | Unit tests may not touch the filesystem (beyond `tmp_path` for pure parsers), network, subprocesses or databases; integration tests cross exactly the boundary they name; acceptance tests run against the Compose stack via REST/MCP/CLI/UI only. |
| REVA-TST-003 | All fixtures are authored for REVA (synthetic) or built in CI from tiny source programs (Go, Rust, Java/Spring Boot, .NET, Python, Node). No third-party application binaries, no REA fixtures. Fixture build scripts live in `tests/reva/fixtures/build/` with pinned toolchain images. |
| REVA-TST-004 | Golden files (expected warrant IDs, route sets, SBOMs, diffs, traces) are committed and regenerated only by `kgf reva fixtures regen`, which prints a diff that requires review. |
| REVA-TST-005 | Property-based tests (Hypothesis) for JCS, IDs, coverage composition, Merkle proofs, templating, incremental extraction equivalence and closure monotonicity (adding a failing check can never turn a non-closed outcome into closed). |
| REVA-TST-006 | Conformance suites: (a) GraphPort conformance for each backend (HugeGraph, Neo4j; Neptune via a Gremlin-compatible lane or named skip); (b) sandbox profile conformance; (c) MCP contract conformance; (d) cross-tenant isolation conformance. |
| REVA-TST-007 | Every requirement in this document has ≥ 1 obligation in `docs/reva/obligations/reva.yaml` with marker-tagged tests, per §14. CI computes the REVA ledger on every main-branch build. |
| REVA-TST-008 | Negative-path coverage: each requirement's obligation lists `negative` and `malformed` case kinds unless it is pure presentation. |
| REVA-TST-009 | Unavailable environments (no Docker, no Oracle) are named skips with reasons; skipped tests never count as passes (AG-01). |
| REVA-TST-010 | Security tests: secret-scan of all outputs, cross-tenant suite, ACL propagation, prompt-injection fixtures, zip-bomb/path-traversal fixtures, SSRF network audit. |

---

## 13. Acceptance journeys (run in the Compose stack; each produces runtime evidence: HTTP exchange logs, screenshots, Playwright traces)
| ID | Journey | Pass conditions |
|---|---|---|
| RJ-01 | **Warrant lifecycle and tamper evidence.** Ingest a Git repo and a Jira project with `REVA_INGEST_WARRANTS=true`; open a KGF entity; open its warrants in the WarrantDrawer; verify signature and inclusion proof in the UI; corrupt one stored warrant row directly in the DB; run the auditor. | Warrants visible with correct authority/epistemic badges; proof verifies; corruption is detected within one audit cycle, the record is quarantined, and an alert and integrity warrant appear. |
| RJ-02 | **Contradiction governance.** Confluence says service `billing` is owned by Team A; ServiceNow CMDB says Team B, with overlapping validity. | One `value_conflict` opens; affected entities show the banner; an answer about ownership shows both claims and the contradiction; a reviewer resolves by human decision; history keeps both; as-of queries before and after the decision behave correctly. |
| RJ-03 | **Service-account blast radius.** Fixture estate: 3 repos (Spring Boot billing service, FastAPI notifications service, Electron admin app), Helm values, OTel export, DB schemas. Seed `service_account = svc-billing-rotator`, template `impact.service_account`. | Results list the services, routes, resources, deployments, Jira stories and owners in the golden file; paths show weakest-link epistemic states; coverage is complete for the fixture scope; a deliberately unindexed repo produces a frontier gap and the UI shows "Unknown — not proven empty" for that branch. |
| RJ-04 | **Rule-change test scope.** Seed `rule_id = DISCOUNT_RULE_7`, template `impact.rule_change`, after verifier runs have collected coverage data. | Impacted symbols match golden; recommended tests include exactly the tests whose coverage contexts hit them; stale coverage is flagged; removing coverage data yields a gap instead of an empty list. |
| RJ-05 | **Knowledge-gap workflow.** A runtime-only API call (no static source) creates a gap; assign owner; run the connector-sync probe; ingest the missing repo; resolve. | Gap auto-created once; probe result warrants linked; resolution passes the authority check; revision chain verifies; board ordering by impact is correct. |
| RJ-06 | **Proof-of-Done.** For a fixture KGF feature with 6 obligations: (a) only test files exist → nothing closes; (b) tests exist but one is `assert True` → AG-05; (c) one mocks the owner → AG-06; (d) all good → closed with attestation; (e) commit changes an owner → `stale`; (f) a board item manually set to Done appears as "Asserted done — unproven". Export the HTML ledger. | Each sub-step shows the exact expected reason codes in UI and API; ledger IDs are stable; the HTML export works offline. |
| RJ-07 | **Permission-aware tracing and revocation.** Two users with different Confluence permissions run the same trace; then revoke user 2's access. | User 2 never sees restricted nodes and gets `ACL_HIDDEN` counts; after revocation, cached views and continuations stop working for user 2 within 60 s. |
| RJ-08 | **Grounded answers and evaluation.** Ask template and free-form questions, including an absence question under partial coverage and a prompt-injection document. Run the reference evaluation suite. | Template answers are deterministic (0 LLM calls); claims are grouped by kind with valid citations; the absence answer says "Unknown — not proven"; injection is ignored and recorded; suite metrics meet REVA-GA-006 thresholds. |
| RJ-09 | **Shipped-artifact provenance and drift.** Upload the CI-built Spring Boot JAR, Go binary and OCI image for commit C; then a JAR built from a dirty tree; then a JAR whose embedded commit is not ingested. | Components, SBOM (valid CycloneDX/SPDX), `BUILT_FROM` edges to C; drift verdicts `verified_match` (with reference build), `unverifiable_dirty`, and `unknown` + `GAP_COMMIT_NOT_INGESTED` respectively. |
| RJ-10 | **API surface and reconciliation.** Ingest HAR + OTel + NGINX logs for the fixture estate; reconcile with static boundaries. | Templating collapses slug IDs (E-07 regression); secrets never stored (byte scan); OpenAPI alignment categories correct; matched/static-only/runtime-only/ambiguous counts equal golden; no "dead" claim under sampled coverage. |
| RJ-11 | **Graph diff without churn.** Extract boundaries at commits A and B of the Electron fixture (E-06 changes) and of the Spring fixture (controller moved to a new package + one route added). | E-06 regression passes; moved controller shows `moved` with routes `unchanged`; added route `added`; the diff warrant cites both snapshots. |
| RJ-12 | **Operations.** Run doctor (all pass); rotate a producer key; back up; destroy the volume; restore; verify the log; reproject into an empty Neo4j; disable REVA and confirm KGF core still works. | Every step passes; post-restore verification checks all IDs and log consistency; reprojection counts match; KGF core journeys pass with REVA disabled. |

---

## 14. Definition of Done and Proof-of-Completion policy

### 14.1 Policy (MUST)
1. **References are not proof.** A requirement is not done because a file, function, test file, test name, commit message, PR description, coverage percentage or agent statement says so.
2. **Done = closed in the REVA ledger.** A requirement is done when *all* its obligations are `closed` by the Proof-of-Done engine under §7.6, at the current main-branch commit.
3. **Comparable proof.** Each obligation's closing evidence must reach its `required_depth` with an acceptable authority (§6.7). User-visible requirements (`layer ∈ {ui, api, mcp, cli}`) need `acceptance` depth with journey evidence.
4. **Executed, strong, fresh tests.** Anti-gaming checks AG-01…AG-14 must pass.
5. **No open blockers.** No linked open contradiction or blocking gap.
6. **Signed and logged.** The closing attestation and ledger are signed and included in the transparency log; `kgf reva log verify` passes.
7. **Agents report ledger IDs, not claims.** An AI coding agent reporting progress MUST cite the ledger ID and per-obligation outcomes. A statement such as "implemented and tested" without a ledger ID is treated as unproven.

### 14.2 Bootstrapping (before PD exists)
Phases P0–P1 of the implementation plan run before the PD engine exists. Their completion is provisional: recorded in `docs/reva/BUILD_STATE.md` with test outputs. After PD is operational (end of P2), every P0–P2 requirement MUST be re-closed through the ledger before P3 starts. Provisional status never counts towards final completion.

### 14.3 REVA release gate (fail-closed)
| Stage | Required |
|---|---|
| G1 Kernel integrity | All WK, TL, CV obligations closed; determinism suite (NFR-012) passes |
| G2 Proof engine | All PD, VS obligations closed; RJ-06 passes |
| G3 Extractors | All AI, SP, AB, AS, DB, RR obligations closed; RJ-09, RJ-10 pass |
| G4 Workflows | All FT, GD, DV, VW, GA obligations closed; RJ-03, RJ-04, RJ-08, RJ-11 pass |
| G5 Surface & security | All MC, SEC, UI, DR, OB obligations closed; RJ-01, RJ-02, RJ-05, RJ-07, RJ-12 pass; cross-tenant and secret-scan suites pass |
| G6 Non-functional | NFR-001…NFR-020 and NFR-030 measured and passing on reference hardware (or documented CI-equivalent scaling) |
| G7 Ledger | REVA ledger `complete = true`, signed, logged, exported (JSON/MD/HTML) and attached to the release |

---

## 15. Traceability (REA capability → REVA requirements → journeys)
| RC | REVA requirements | Journeys |
|---|---|---|
| RC-01 | REVA-WK-001…015, REVA-SEC-004/007 | RJ-01 |
| RC-02 | REVA-WK-012, REVA-TL-001…005 | RJ-01, RJ-12 |
| RC-03 | REVA-CV-001…005, REVA-FT-003, REVA-GA-005 | RJ-03, RJ-08 |
| RC-04 | REVA-KG-001…008 | RJ-05 |
| RC-05 | REVA-PD-001…012 | RJ-06 |
| RC-06 | REVA-PD-003/004, §6.7 | RJ-06 |
| RC-07 | REVA-PD-009, §14.3 | RJ-06 |
| RC-08 | REVA-VS-001…010, REVA-PD-006 | RJ-06 |
| RC-09 | REVA-TST-004/006, REVA-GD-* | RJ-11 |
| RC-10 | §6.3–6.6, REVA-AB-008 | RJ-03, RJ-11 |
| RC-11 | REVA-AB-001…013 | RJ-03 |
| RC-12 | REVA-FT-001…009 | RJ-03, RJ-04 |
| RC-13 | REVA-GD-001…005 | RJ-11 |
| RC-14 | REVA-RR-001…004 | RJ-10 |
| RC-15 | REVA-DV-001…004 | RJ-09 |
| RC-16 | REVA-AS-001…008 | RJ-10 |
| RC-17 | REVA-DB-001…005 | RJ-03 |
| RC-18 | REVA-SP-001…012 | RJ-09 |
| RC-19 | REVA-AI-001…007, REVA-CX-002/005 | RJ-09 |
| RC-20/21 | REVA-VW-001…004 | RJ-03, RJ-08 |
| RC-22/23 | REVA-MC-001…009, §10.1 | all |
| RC-24 | REVA-MC-005, REVA-GA-003, REVA-SEC-006 | RJ-08 |
| RC-25 | REVA-GA-001…005 | RJ-08 |
| RC-26 | REVA-GA-006/007 | RJ-08 |
| RC-27 | REVA-VS-003/004/010, REVA-SEC-011 | RJ-06 |
| RC-28 | REVA-DR-001…003 | RJ-12 |
| RC-29 | §6.7, REVA-TST-001/002 | RJ-06 |
| RC-30…34 | REVA-XP-001…006 (deferred) or rejected | — |

Weakness inversions: W-01 → WK-010, TL-* · W-02 → WK-007/009 · W-03 → SEC-001…004 · W-04 → AB-008, GD-002/003 · W-05 → AB-006 · W-06 → AS-004 · W-07 → VW-* · W-08 → AB-002…004/009 · W-09 → WK-006, FT-007 · W-10 → PD-003…005, VS-* · W-11 → NFR-030 · W-12 → MC-009, UI-* · W-13 → §6.10, OB-006 · W-14 → DR-*.

---

## 16. Out of scope (rejected) — with reasons
| Item | Reason |
|---|---|
| Native decompilation/disassembly as a core feature (Hopper, IDA, Ghidra, Kuna, Rizin, objdump) | KGF analyses enterprise systems with source access; decompilation adds heavy commercial-licence and legal exposure (vendor EULAs restrict automation and output sharing) and large maintenance cost. Only an optional, sandboxed Ghidra adapter is deferred (XP-002). |
| Debuggers and dynamic instrumentation (GDB, pwndbg, Frida, LLDB) | Executing and instrumenting third-party code conflicts with KGF's enterprise safety posture and air-gapped deployments; no KGF journey needs it. |
| Android device control (ADB), JADX/JEB/Apktool decompilation, Flutter/Harmony | Not part of KGF's sources; static manifest inventory deferred (XP-004). |
| Firmware extraction, pcap/TShark decoding, sigrok signals, EVM, DOS/console profiles, recorded core dumps | No KGF use case. |
| Live browser/Electron/process automation | KGF consumes recorded telemetry; live capture deferred (XP-006). |
| Agent-client registration for ~20 clients | KGF exposes a standards-based MCP server; doctor covers KGF's own runtime. |
| Using REA as a dependency | Churn, single-maintainer risk, clean-room requirement (§2.3, §2.9). |

---

## 17. Pre-decided decisions (no open choices remain)
| ID | Decision | Default | Rule if baseline differs |
|---|---|---|---|
| D-01 | Implementation language | Python (KGF backend interpreter) | If the KGF backend is not Python, REVA still runs as a Python service behind REST, and KGF calls it via an HTTP adapter. |
| D-02 | Package location | `reva/` beside KGF's top-level backend package | Bind the actual path in BASELINE.md. |
| D-03 | Relational store | Reuse KGF PostgreSQL (schema `reva`) | No PostgreSQL → SQLite WAL at `<data>/reva/reva.db`; the PostgreSQL-only partitioning (NFR-015) applies only when on PostgreSQL. |
| D-04 | Blob store | Filesystem CAS under the KGF data volume | If KGF already uses MinIO/S3, use a `reva` bucket prefix per tenant. |
| D-05 | Background jobs | KGF's existing queue (Celery/RQ/Arq/Dramatiq) | None → REVA built-in asyncio worker with a `reva_jobs` table (lease-based, at-least-once). |
| D-06 | Sandbox engine | Docker/Podman if the daemon is reachable; else Linux process sandbox | Process sandbox records `ENVIRONMENT_DEGRADED_SANDBOX`; `integration`/`acceptance` profiles then require Docker and become named skips without it. |
| D-07 | Graph write path | KGF mutation gateway | No gateway → REVA calls KGF's graph abstraction through a REVA-owned "gateway shim" that enforces the same validation and audit, and the shim is reported in BASELINE.md as a KGF gap. |
| D-08 | Graph backends in CI | HugeGraph + Neo4j containers | Neptune: Gremlin-compatible conformance lane (TinkerPop Gremlin Server) plus an optional real-Neptune lane (named skip without credentials). |
| D-09 | Warrants in graph | Not projected as vertices; referenced by ID on elements | — |
| D-10 | Auth/tenancy | KGF auth middleware via AuthPort | No tenancy in KGF → single tenant `default`; all tenant columns still populated. |
| D-11 | Frontend | KGF React app, REVA under `/reva/*` | No React app → REVA ships a standalone Vite React app served by FastAPI at `/reva-ui/`. |
| D-12 | MCP | Register into KGF MCP server | None → REVA stdio + streamable HTTP MCP server (`reva-mcp`) using the official Python MCP SDK. |
| D-13 | LLM usage | Only GA synthesis, through KGF's LLMPort, local by default | No LLMPort → GA runs deterministic-only; synthesis is disabled and doctor reports it. |
| D-14 | Mutation testing | REVA's own Python mutation probe | Frontend owners close via acceptance-depth journey evidence + Istanbul coverage (no JS mutation in 1.0). |
| D-15 | Ed25519 library | `cryptography` | — |
| D-16 | JCS | Own implementation, cross-checked against `rfc8785` | — |
| D-17 | SBOM formats | CycloneDX 1.5 and SPDX 2.3 JSON | — |
| D-18 | Jira write-back | Off | — |
| D-19 | Vulnerability matching | Off (offline mirror only when enabled) | — |
| D-20 | Row sampling | Off | — |
| D-21 | Forensics pack | Off, not implemented in 1.0 | — |
| D-22 | Obligation storage | YAML in repo (`docs/reva/obligations/`) + DB mirror after sync | — |
| D-23 | Coverage tool for Python | `coverage.py` via pytest-cov with `--cov-context=test` | — |
| D-24 | Path/endpoint canonical form | `{}` per parameter segment; lowercase method; no trailing slash except root | — |

---

## 18. Risks
| Risk | Impact | Mitigation |
|---|---|---|
| Graph bloat from warrant references | Backend performance | D-09 summaries and caps; full lists in the warrant store |
| Per-test coverage and mutation runs are slow | Long closure cycles | Mutation only for unit/component owners; incremental runs keyed by owner digest; nightly full runs |
| Heuristic extraction errors (routes, templates, matching) | Wrong impact answers | Inferred epistemic state, confidence, ambiguity gaps, golden fixtures, RR runtime confirmation |
| Teams perceive PD as friction | Adoption | Clear reason codes, waivers with expiry, Jira proposals, "Asserted done — unproven" lane instead of blocking boards |
| Key compromise | Forged warrants | KEK encryption, rotation/revocation, log witnessing, audit |
| Multi-backend capability gaps | Feature divergence | GraphPort capability probes, per-backend conformance, explicit `REVA_E_BACKEND_CAPABILITY` |
| Sandbox unavailable on customer hosts | Weaker verification | Degraded profile recorded as a limitation; depth-gated closure prevents over-claiming |

---

## Appendix A — Example warrant (illustrative values)
```json
{
  "warrant_id": "wr1_3b0c…(64 hex)",
  "body": {
    "schema": "reva.warrant/1",
    "tenant_id": "acme",
    "subject": {"kind": "artifact", "artifact_id": "art1_9a1f…", "sha256": "9a1f…", "size_bytes": 48211234,
                "media_type": "application/java-archive", "format": "jar"},
    "producer": {"producer_id": "prd1_51c2…", "producer_type": "extractor", "name": "reva.sp.jvm_archive",
                 "version": "1.0.0", "build_digest": null, "key_id": "key1_77ab…"},
    "operation": "reva.sp.jvm_archive",
    "predicate": "reva.pred.built_from_commit",
    "parameters": {"source": "git.properties"},
    "statement": {"repo_hint": "billing-service", "commit": "4e1d0c…(40 hex)", "commit_time": "2026-10-12T09:14:03.000Z",
                  "dirty": false, "basis": "git.properties:git.commit.id"},
    "raw_ref": {"blob_id": "blb1_c0de…", "sha256": "c0de…", "size_bytes": 512, "media_type": "text/x-java-properties"},
    "authority": "shipped_artifact",
    "epistemic_state": "observed",
    "confidence": {"band": "high", "score_bp": 9500, "calibration_ref": null},
    "coverage": null,
    "locations": [{"kind": "archive_member", "artifact_id": "art1_9a1f…", "member_path": "BOOT-INF/classes/git.properties",
                   "member_sha256": "c0de…"}],
    "limitations": [{"code": "STATIC_NOT_RUNTIME", "message": "Embedded build metadata does not prove which code is running."}],
    "environment": null,
    "observed_at": "2026-10-18T10:00:00.000Z",
    "valid_time": {"from": "2026-10-12T09:14:03.000Z", "to": null},
    "links": [{"rel": "derived_from", "warrant_id": "wr1_inventory…"}]
  },
  "envelope": {
    "signature": {"alg": "ed25519", "key_id": "key1_77ab…", "sig": "base64url…"},
    "recorded_at": "2026-10-18T10:00:00.123Z",
    "log": {"log_id": "acme:warrants", "leaf_index": 182734},
    "acl": {"source_acl_refs": ["git:billing-service:read"], "allow": [], "deny": []},
    "classification": {"level": "internal", "pii": false, "tags": []},
    "retention": {"policy_id": "default", "expires_at": null, "legal_hold": false},
    "display": {"subject_label": "billing-service-2.14.0.jar", "local_path": null, "url": null},
    "status": "active"
  }
}
```

## Appendix B — Example obligation and binding
```yaml
# docs/reva/obligations/reva.yaml (excerpt)
- key: OBL-REVA-WK-004-01
  version: 1
  title: Warrant validation reports every rule violation with pointers
  requirement_refs: [REVA-WK-004]
  layer: domain
  required: true
  case_kinds: [positive, negative, malformed, boundary]
  required_depth: unit
  requires_contract_type: true
  dependencies: [OBL-REVA-WK-003-01]
  blocking_gaps: []
  disposition: active
  nondeterminism: {mode: deterministic, spec: null}
  performance_budget: null
  review: {reviewed_by: null, review_warrant_id: null}   # filled by `kgf reva obligation review`
bindings:
  OBL-REVA-WK-004-01:
    owners:
      - {repo_id: kgf, path: reva/kernel/warrant.py, symbol: validate_warrant_body, language: python}
    contract_type: {schema_ref: reva.kernel.warrant.WarrantBody, parser_ref: null, model_ref: reva.kernel.warrant.WarrantBody}
    fixtures:
      - {fixture_id: wk004-rules, case_kind: negative, depth: unit, path: tests/reva/fixtures/warrants/rule_violations.json,
         sha256: "<written by `kgf reva binding set`>"}
    # owner_digest is computed and stored by `kgf reva binding set`; it is never hand-written.
    verifier:
      verifier_id: pytest-unit-wk
      argv: [python, -m, pytest, tests/reva/unit/kernel/test_validation.py, -m, "reva_obligation", --junitxml=out/junit.xml,
             --cov=reva.kernel, --cov-context=test, --cov-report=json:out/coverage.json]
      workdir: .
      depth: unit
      profile: unit
      timeout_s: 600
      env_allow: [PYTHONHASHSEED]
      network: none
    journeys: []
```
