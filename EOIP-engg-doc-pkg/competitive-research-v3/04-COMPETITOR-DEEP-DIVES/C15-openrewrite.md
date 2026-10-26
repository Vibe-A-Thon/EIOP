# C15 - OpenRewrite / Moderne

| Field | Value |
|---|---|
| Registry ID | T-C15-openrewrite |
| Tier | B - lossless semantic trees (LST) and multi-repo refactoring; type-attributed code model |
| Versions examined | openrewrite/rewrite v8.93.11 (2026-10-18); rewrite-recipe-bom v3.41.0 (2026-10-09); Moderne CLI repo `moderneinc/moderne-cli-releases` v3.57.16 (2026-03-19, repo archived) |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V29 |

## 1. Identity, status, tier, sources

| Item | Finding | Claim |
|---|---|---|
| What | OpenRewrite: open-source automated refactoring ecosystem; Moderne: commercial platform running recipes across many repositories | [CLAIM-openrewrite-01] |
| Owner | Moderne, Inc. (maintainer of OpenRewrite) | [CLAIM-openrewrite-01] |
| Activity | `openrewrite/rewrite` ~3.8k stars, pushed 2026-10-26, Apache-2.0 repo licence flag; near-daily releases | [CLAIM-openrewrite-02] |
| Licence split | Apache-2.0: core, Java/Groovy/Kotlin/XML/Properties/YAML/HCL, Maven/Gradle plugins, building-block recipes. Moderne Source Available License: newer language modules (JavaScript, TypeScript, C#, Python, Go, Ruby, Scala, Android) and some recipes - may not be "commercialized or provided to others as a managed service"; no paid consulting running them. Moderne Proprietary: commercial recipes (security remediation, AI-agent context, analysis at scale) | [CLAIM-openrewrite-03] |
| Status of Moderne CLI | public-releases repo is archived (2026-03-19); successor distribution NOT PUBLICLY VERIFIED. Docs say recipes are moving from Maven Central to a "Code Genome Project" | [CLAIM-openrewrite-04] |
| Name collision | none material | |

## 2. Problem and workloads

Mass, behaviour-preserving source changes: framework migrations, dependency upgrades, security fixes, style. Workflow: run recipe via Maven/Gradle plugin on one repo (local, in memory), or on Moderne across thousands of repos with mass commits/PRs and "search" recipes for impact analysis [CLAIM-openrewrite-01].

## 3. Feature inventory

| Feature | Status |
|---|---|
| LST with type attribution + formatting preservation | present |
| Recipes (visitors, declarative YAML, Refaster-like templates) | present |
| Languages: Java, Kotlin, Groovy, XML, YAML, properties, HCL (Apache); JS/TS, C#, Python, Go, Ruby, Scala (source-available) | present/partial per licence |
| Search recipes with markers; data tables output | present |
| Multi-repo mass ingest, LST store, org-wide run, mass PRs | Moderne only (commercial) |
| Persistent LST across runs | local: no; Moderne: yes (artifact repository) |
| Cross-source graph, permissions model | absent |

## 4. Architecture

```
local:   source files -> parse LST (in memory, needs classpath) -> recipe visitors -> print -> overwrite files
Moderne: SCM -> mass-ingest container -> LST artifacts (Maven/Artifactory/Nexus) -> agent -> SaaS UI/CLI
          (agent encrypts artifacts; key in customer vault; PRs via customer SCM)
```

## 5. Under-the-hood reconstruction

Data model: LST = tree preserving whitespace/comments and resolved types (fully qualified types, method signatures, even for references from dependencies), with markers attached to nodes; nothing persists between local runs, a new LST is generated each time [CLAIM-openrewrite-05]. Parsing requires a resolvable classpath/compilation for Java type attribution (inferred from "type attribution" doc; build details UNVERIFIED). Transform pipeline: recipe -> visitor tree -> mutated LST -> printer emits minimal diff. Moderne scales by building LSTs in a separate mass-ingest step (sizing 2 cores/16 GB/32 GB per ~1,000 repos, vendor) and storing them as artifacts in Artifactory/Nexus, read by an agent [CLAIM-openrewrite-06]. Query: search recipes, data tables (columnar results); no declarative graph query. Concurrency/versioning: per-commit LSTs; versioning follows the artifact repository. Security: agent-mediated; encrypted artifacts; SCM credentials stay in customer network.

## 7. Performance and resource model

Local mode needs the whole LST in memory (stated). Sizing above is vendor; throughput NOT PUBLICLY VERIFIED. Unresolved dependencies degrade type attribution (hypothesis).

## 8. Strengths

STR-openrewrite-01 type-attributed, format-lossless model enabling safe automated edits. STR-openrewrite-02 mass-ingest + artifact-store separation. STR-openrewrite-03 reusable recipe catalogue.

## 9. Limitations

| Class | Finding |
|---|---|
| Algorithmic | high precision only where LSTs exist; Java-centric maturity, other languages newer (hypothesis from licence/language split) |
| Operational | build-dependent ingest; LST must fit memory locally |
| Friction | licence matrix by module; distribution moving off Maven Central; CLI releases repo archived |
| Licensing | source-available modules forbid managed-service use and paid recipe consulting - EOIP white-label/SaaS packaging collides |
| Governance | writes code (PRs); EOIP is read-oriented (ADR-007) |

## 10. Deployment, licensing, viability

Apache-2.0 core is embeddable (JVM). Source-available/Proprietary parts: legal-review trigger (managed-service and OEM clauses). Moderne platform is SaaS with on-prem agent and ingest; whether a fully air-gapped Moderne exists: NOT PUBLICLY VERIFIED. Air-gap for Apache core: yes.

## 11. Delta vs EOIP

| Area | OpenRewrite/Moderne | EOIP |
|---|---|---|
| Type-accurate symbols | LST, compile-level (Java) | BL-42 syntactic (ast for Python, heuristic TS) |
| Multi-repo impact | Moderne search recipes | BL-42 + `polyglot_linker.py` Partial |
| Change execution | PRs / mass commits | BL-47 read-oriented; actions library-only (see 01a) |
| Evidence of change | git diff | BL-41 lineage |
| Permissions | SCM-delegated | BL-18 Partial |

## 12. Cards

| ID | Card |
|---|---|
| STR-openrewrite-01 | [CLAIM-openrewrite-05] types disambiguate `logger.info`; value: exact blast radius; **integrate** (Apache core only) as optional JVM extractor emitting SourceEvents; test: Java fixture, symbol-type precision >= SCIP-java |
| STR-openrewrite-02 | [CLAIM-openrewrite-06] decouple heavy ingest from query; **match** via SCIP/LSIF-style batch indexers feeding BL-42 |
| INV-openrewrite-01 | Target Moderne platform, licence. Limitation: source-available modules cannot be offered as managed service [CLAIM-openrewrite-03]; cause licensing (proven). Options: (a) use only Apache modules; (b) SCIP-based precise indexers; (c) own typed-edge model with optional OpenRewrite adapter. Selected (a)+(b). Benchmark: licence audit of module list passes policy checker in `compliance/sbom.py`. ADOPT. |
| INV-openrewrite-02 | Writes code, not provenance graph; EOIP differentiates by joining recipe runs to Jira/PR/incident lineage [CLAIM-openrewrite-01]; cause semantics (hypothesis). Decision EXPERIMENT. No 10.5 seed applies. |

## 13. Decisions

CAP-66: INTEGRATE (Apache JVM modules, optional extractor) / EXPERIMENT. CAP-69: BUILD (cross-source thread; OpenRewrite search recipes as input). Mass code changes: REJECT for EOIP core (read-oriented), REFERENCE for action proposals. Moderne platform: REFERENCE-ONLY. CAP-77 licence matrix: BUILD in policy checker.

## 14. Tests/POC

Run `rewrite-java` search recipe on a Maven fixture, emit data-table CSV, ingest as SourceEvents, assert tenant-scoped nodes carry source revision. Acceptance: type-resolved call edges differ from name-based edges on an overload fixture.

## 15. Risks

Distribution channel change breaks air-gapped mirrors; licence drift as more modules go source-available; JVM footprint on one node. Open: Moderne offline licensing; LST serialisation format publicness.

## Appendix A - Dimensions

| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | Apache + source-available + proprietary |
| D2 | 2 | mass refactoring |
| D3 | 4 | local vs Moderne topology |
| D4 | 5 | LST; store = artifacts |
| D5 | 5 | typed tree, markers |
| D6 | 5 | visitors; no planner |
| D7 | N/A | none |
| D8 | 7 | N/A, memory-bound |
| D9 | 5 | mass ingest |
| D10 | N/A | none |
| D11 | 5 | per-commit LST |
| D12 | N/A | none |
| D13 | 3 | Moderne AI recipes (vendor) |
| D14 | N/A | none |
| D15 | N/A | none |
| D16 | 3 | Moderne UI |
| D17 | 3 | plugins, YAML recipes |
| D18 | 5 | agent, encryption |
| D19 | N/A | not tenant-model product |
| D20 | 7 | vendor sizing only |
| D21 | 1,10 | tiered licence |
| D22 | 5 | NOT PUBLICLY VERIFIED |
| D23 | N/A | none found |
| D24 | all | docs-only, no source read |

## Appendix B - Capabilities

| CAP | Tech | Claim | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-66 | native (Java), partial others | 05 | BL-42 | INTEGRATE | P2 |
| CAP-67 | partial | 06 | BL-42 | REFERENCE | P3 |
| CAP-69 | partial | 01 | BL-41/42 | BUILD | P1 |
| CAP-77 | enterprise-only | 03 | n/a | BUILD | P1 |

## Appendix C - Evidence

| ID | Product/date | Claim | Class | Source | Dates/conf | Contra |
|---|---|---|---|---|---|---|
| CLAIM-openrewrite-01 | docs | definition, Moderne role | Officially documented | https://docs.openrewrite.org/ | 2026-10-26, 0.85 | none |
| CLAIM-openrewrite-02 | rewrite v8.93.11 | stars, release, Apache flag | Officially documented | https://github.com/openrewrite/rewrite | 0.8 | mixed-licence repo |
| CLAIM-openrewrite-03 | licensing page | licence split and restrictions | Officially documented | https://docs.openrewrite.org/licensing/openrewrite-licensing | 0.85 | legal text not read |
| CLAIM-openrewrite-04 | CLI repo | archived 2026-03-19; Code Genome note | Officially documented | https://github.com/moderneinc/moderne-cli-releases ; docs front page | 0.6 | successor unknown |
| CLAIM-openrewrite-05 | LST doc | types, whitespace, in-memory, not persisted | Officially documented | https://docs.openrewrite.org/concepts-and-explanations/lossless-semantic-trees | 0.85 | none |
| CLAIM-openrewrite-06 | Moderne admin docs | mass ingest, artifact repo, agent | Officially documented | https://docs.moderne.io/administrator-documentation/moderne-platform-v1/references/architecture | 0.7 | via search summary |

## Appendix D - Assumptions

Maven Central move is as docs state. No source code read; internals beyond docs are inference.
