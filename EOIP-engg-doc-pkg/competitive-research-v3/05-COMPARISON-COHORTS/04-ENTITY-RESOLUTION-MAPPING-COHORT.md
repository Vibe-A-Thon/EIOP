# Cohort 04 — Entity Resolution, Declarative Mapping, OBDA and Schema Inference

| Field | Value |
|---|---|
| Cohort ID | COH-04 |
| Workload class | Identity and linking stage of the canonical pipeline (Master Prompt §4.3 item 4): entity resolution (ER), declarative source-to-graph mapping, ontology-based data access (OBDA), schema inference |
| ER members | [Senzing](../04-COMPETITOR-DEEP-DIVES/C04-senzing.md), [Splink](../04-COMPETITOR-DEEP-DIVES/C04-splink.md), [Zingg](../04-COMPETITOR-DEEP-DIVES/C04-zingg.md), [Dedupe](../04-COMPETITOR-DEEP-DIVES/C04-dedupe.md), [JedAI/pyJedAI](../04-COMPETITOR-DEEP-DIVES/C04-jedai.md), [Ditto](../04-COMPETITOR-DEEP-DIVES/C04-ditto.md), [LLM entity matching](../04-COMPETITOR-DEEP-DIVES/C04-llm-entity-matching.md) |
| Mapping/OBDA/inference members | [Ontop](../04-COMPETITOR-DEEP-DIVES/C04-ontop.md), [RML tools](../04-COMPETITOR-DEEP-DIVES/C04-rml-tools.md), [OpenRefine](../04-COMPETITOR-DEEP-DIVES/C04-openrefine.md), [Ontology alignment](../04-COMPETITOR-DEEP-DIVES/C04-ontology-alignment.md), [Schema inference](../04-COMPETITOR-DEEP-DIVES/C04-schema-inference.md), zero-ETL cross-reference [PuppyGraph](../04-COMPETITOR-DEEP-DIVES/C01-puppygraph.md) |
| Tier C records | [C04-tier-c-records-V12](../04-COMPETITOR-DEEP-DIVES/C04-tier-c-records-V12.md): SPARQL-Generate, Karma, py_entitymatching (Magellan), recordlinkage (all REFERENCE-ONLY) |
| Reference columns | HugeGraph, Neo4j, Neptune (only where an ER/mapping capability applies; none of the three is an ER product) |
| EOIP status basis | `01-SYSTEM-BASELINE.md` (BL, commit ad9937b) superseded by `01a-BASELINE-DELTA-HEAD.md` (HEAD 896e06d, NB rows) |
| Journeys | J7 resilient incremental ingest; J12 arbitrary JSON onboarding |
| Date | 2026-10-26 |

Count: 12 deep dives (7 ER, 5 mapping/inference) + 4 Tier C records + 1 cross-reference (PuppyGraph).

## 1. Workload class and comparison basis

**Customer workloads served.** (a) Deciding that records from Jira, Confluence, ServiceNow, GitLab, HR or CMDB sources describe the same person, team, service or asset, without duplicating identities under replay or out-of-order events (J7). (b) Turning an unknown relational or JSON export into a mapped, validated graph with a reviewable ontology extension (J12). (c) Reading relational data as a graph without copying it (OBDA / zero-ETL).

**Why comparable.** All members act between "parsing / normalization / schema inference" and "ontology mapping and validation" in the canonical pipeline. They are compared on four axes: how candidates are generated (blocking), how pairs/clusters are scored, whether decisions are durable and reversible, and whether the licence allows EOIP to ship them in a white-label, air-gapped bundle.

**Sub-groups.** ER engines (Senzing, Splink, Zingg, Dedupe, JedAI) are direct competitors. Ditto and LLM matching are *pair scorers*, not engines. Ontop, RML tools and PuppyGraph share the mapping/virtualisation problem. OpenRefine, ontology alignment and schema inference are adjacent tooling; they are compared only on the capabilities they actually provide.

**Excluded.** Graph engines (HugeGraph, Neo4j, Neptune) appear only as reference columns; none ships ER (no CAP-31 row in their deep-dive capability mappings). Tier C records are reference-only and are not scored in the tables. Spark-scale distributed ER is out of scope under the one-node-first rule (§4.3 item 10).

## 2. Capability comparison

Notation: claim IDs are shortened (`sz-10` = CLAIM-senzing-10, `sp-` Splink, `zg-` Zingg, `dd-` dedupe, `jd-` jedai, `dt-` ditto, `lm-` llmem, `on-` ontop, `rml-`, `or-` OpenRefine, `oa-` ontology alignment, `si-` schema inference, `pg-` puppygraph, `nep-` amazon-neptune, `hg-` apache-hugegraph, `n4-` neo4j). `§n` means a deep-dive section with no separate CLAIM row. `unknown` = not publicly verified in the deep dive.

### 2.1 ER engines and pair scorers

| Capability | Senzing | Splink | Zingg | Dedupe | JedAI | Ditto | LLM matching | EOIP @HEAD |
|---|---|---|---|---|---|---|---|---|
| CAP-30 deterministic keys / rules | native, principle-based feature behaviours (sz-08) | partial, rules only as blocking/lambda inputs (sp-09) | enterprise-only (`deterministic`, zg-05) | absent | absent | absent | absent | Implemented for persons only: BL-34 (`identity/resolver.py:49`) |
| Blocking | native, generic values excluded from candidates (sz-09) | native, multi-rule UNION with exclusion, `max_pairs` (sp-12, sp-15) | native, learned blocking tree (zg-04); poorly learned tree can stall jobs (zg-05) | native, learned predicates (dd-04, confidence 0.5) | native, schema-agnostic + meta-blocking (jd-02) | absent | absent | partial: blocking inside `er/splink_engine.py` (NB via BL-36 HEAD row); library-only |
| Matching model | native, rule/principle with comparator buckets, no training (sz-08, sz-09) | native, Fellegi-Sunter with EM and term-frequency (sp-08..11) | native, logistic regression (zg-04) | native, regularised classifier from labels (dd-04) | native, supervised/unsupervised, DL optional (jd-02) | native, fine-tuned transformer pair classifier (dt-01) | partial, zero-shot pair verdicts (lm-01) | partial: Fellegi-Sunter with fixed m/u constants, not EM-trained, stdlib Jaro-Winkler; does not use Splink (BL-36 HEAD) |
| Clustering | native, entity-centric (sz-09) | native, iterative SQL connected components (sp-13) | native, GraphFrames connected components (zg-04) | native, hierarchical (dd-04) | native (jd-02) | absent, pairwise only (dt-01) | absent | partial: connected components in engine (BL-36 HEAD) |
| Incremental / real-time | native: add/delete/reevaluate, redo queue (sz-10) | absent: `find_matches_to_new_records` removed; `predict_between` added (sp-15, sp-18) | enterprise-only (`runIncremental`, zg-05) | unknown | unknown | absent | absent | partial: `IdentityMergeLedger.merge()` scans O(E) per absorbed node, library-only (BL-34 HEAD) |
| Merge/split reversibility | native: automatic unmerge on re-evaluation (sz-09, sz-10) | absent (sp-18); operators unmerge manually in production (sp-16) | enterprise-only (`reassignZinggId`, zg-05) | absent | absent | absent | absent | Implemented as library: immutable ledger, lossless split, approval gate, not mounted (BL-34/35 HEAD) |
| Persistent IDs | native (DATA_SOURCE+RECORD_ID, entity ids; sz-10) | absent (sp-18) | enterprise-only (zg-05) | absent | absent | absent | absent | Implemented: canonical `urn:eoip:identity:person:email:*` plus ledger aliases (BL-34) |
| Survivorship / golden record | unknown (sz-18 unverified) | absent (sp-18) | absent | absent | absent | absent | absent | absent (no survivorship in BL-34/35 rows) |
| Explainability (CAP-24) | native: why/how/virtual-entity APIs (sz-10) | native: waterfall and match-weight charts (sp-17) | enterprise-only (`explainOutput`, zg-05) | partial: weights inspectable (dd §3) | unknown | absent | partial: free-text rationale, non-authoritative (lm §8) | partial: per-feature weights in engine; no waterfall persisted (BL-36 HEAD, BL-41) |
| Possible / related outcome | native three-way (sz-08) | partial: review threshold band (sp-09) | unknown | partial | unknown | absent | absent | Implemented: match 0.85 / review 0.60 / NIL (BL-36 HEAD) |
| Human review loop | absent in SDK (sz §11) | absent (sp-17, L8) | approval "coming soon" (zg-05) | partial: console labelling (dd-01) | absent | absent | n/a | Partial: `IdentityCandidate` queue (BL-35) |
| Evaluation harness (CAP-78) | blocked: EULA forbids publishing comparisons (sz-05) | partial (sp-17) | partial (CI runs Febrl120K, ncVoters5M; zg-08) | absent | native blocking metrics (jd-02) | benchmark sets (dt-01) | n/a | partial: `identity/evaluation.py` helpers (BL-34 HEAD) |
| Air-gap (CAP-50) | plausible; offline licence activation unverified (sz-18) | viable, telemetry unverified (sp-20) | viable only with telemetry off (zg-09) | viable (dd §10) | viable (jd §10) | viable after weight download (dt §10) | needs local model (lm §10) | design goal; Ollama in compose (BL-45, 01 §3) |
| White-label / OEM (CAP-52) | blocked: no right to distribute (sz-05) | permitted, MIT (sp-01) | AGPL-3.0 Community, proprietary Enterprise (zg-01, zg-06) | permitted, MIT (dd-02) | permitted, Apache-2.0 (jd-01, jd-02) | code permitted, weight licences separate (dt-02) | per-model licence (lm §10) | n/a (own code) |

### 2.2 Mapping, OBDA, inference

| Capability | Ontop | RML tools | OpenRefine | Ontology alignment | Schema inference tools | PuppyGraph | EOIP @HEAD |
|---|---|---|---|---|---|---|---|
| CAP-29 declarative mapping | native R2RML and Ontop mapping (on-01) | native RML/R2RML, YARRRML; five engines (rml-01..04) | absent | absent | absent | partial: mapping to graph schema (pg-01) | Implemented CML to IR; R2RML partial, 76-line importer, not conformance-tested (BL-33 HEAD, NB-09) |
| CAP-21 virtualisation / OBDA | native, SPARQL to SQL (on-01, on-06) | absent (materialise only, rml-01) | absent | absent | absent | native, Gremlin/openCypher over live stores (pg-01) | Partial: planner contracts (BL-51); `OBDAPushdownEngine` builds SQL by f-string (rml-07) |
| Materialisation | native `materialize` batch (on-05) | native (rml-01, rml-03) | n/a | n/a | n/a | absent | Implemented: mapping executor to LPG/RDF (BL-33) |
| CAP-28 schema inference | partial, `bootstrap` (on-05) | absent | absent | absent | partial, types/nullability only (si-01..03); join discovery research-grade (si-06) | unknown | Implemented: `ingest/profile.py` with 5 relationship signals (BL-26, si-08); JSON Schema emission absent |
| Ontology proposal and review (J12) | absent | absent | absent | plugin: proposals only (oa-01) | absent (si §9) | absent | Partial: induction schema + `GovernedPullRequest`, PR flow not mounted (BL-27 HEAD, NB-12) |
| Reconciliation / authority lookup | absent | partial: stateful functions in Morph-KGC (rml-03) | native, W3C CG Reconciliation API v0.2 (or-03, or-04) | n/a | n/a | n/a | absent |
| Source-ACL on virtual reads (CAP-46) | absent, DB account only (on §9) | absent | absent | n/a | n/a | partial, source-side row-level security guidance (pg-02) | Partial: PDP exists, not applied on deployed retrieval paths (BL-18 HEAD) |
| Query surface | SPARQL 1.1, read-only (on-01) | n/a | n/a | n/a | n/a | Gremlin, openCypher (pg-01) | `QueryPlan` templates; SPARQL via rdflib/Fuseki (BL-08, HEAD) |
| White-label / OEM | permitted, Apache-2.0; JDBC drivers separate (on-02) | permitted, MIT/Apache-2.0 (rml-01..05) | permitted, BSD (or-01) | Apache-2.0 repos; transitive licences unverified (oa-01, oa-02) | permissive where verified; ydata-profiling blank (si-03) | closed engine; OEM terms not publicly verified (pg-03) | n/a |

### 2.3 Reference columns (HugeGraph, Neo4j, Neptune)

| Capability | HugeGraph | Neo4j | Neptune | EOIP @HEAD |
|---|---|---|---|---|
| CAP-31 probabilistic ER | absent (no row in deep dive) | absent (no row) | absent (no row) | Partial, own implementation (BL-36 HEAD); "available upstream / not integrated": Splink MIT |
| CAP-30 identity keys | native `PRIMARY_KEY` id strategy derives vertex id from label + key (hg-13) | native, constraint-backed `MERGE` (n4-20, n4-22) | partial, ID uniqueness only (nep-12) | Implemented, person-only (BL-34); tenant-scoped table `identity/scoped_table.py` (HEAD) |
| CAP-21 virtualisation | absent | absent | partial, SPARQL `SERVICE` only (nep-12) | Partial (BL-51) |
| CAP-50 air-gap | native (hg §10) | native with usage report disabled (n4-30) | absent, VPC-only (nep-08) | design goal (BL-45) |

## 3. Operational and licensing comparison

| Member | Licence class | Redistribution / OEM trigger | Deployment and one-node footprint | Air-gap | Maintenance (as verified 2026-10) |
|---|---|---|---|---|---|
| Senzing | Proprietary EULA May 2026.v1; $58,560/yr per 10M records at list (sz-05, sz-06) | **Legal review: yes.** No distribution, no sublicence, one production instance, hardware owned by licensee, no benchmark publication (sz-05) | C core + RDBMS; PostgreSQL on same node viable; SQLite <1M, MySQL <100M (sz-04) | plausible, offline licence unverified | Active, 4.4.2 on 2026-10-01 (sz-01) |
| Splink | MIT (sp-01) | none; SBOM scan of DuckDB/sqlglot/PyArrow | pure Python, in-process DuckDB; PyArrow required (sp-15) | viable, telemetry to verify (sp-20) | Active, 5.0.0 on 2026-09-28; single dominant maintainer (sp-02, sp §9) |
| Zingg | AGPL-3.0 Community; proprietary Enterprise (zg-01, zg-06) | **Legal review: yes.** AGPL section 13 network use and combined-work questions; Enterprise terms unpublished | Spark/JVM even for 100k records; docker image; local Spark mode (zg §10) | viable only with `collectMetrics` off (zg-09) | Active, 0.7.0 Aug 2026 (zg-02, zg-03) |
| Dedupe | MIT (dd-02) | none | in-memory single process | viable | Low activity, last release 2024-08-15 (dd-03) |
| JedAI / pyJedAI | Apache-2.0 (jd-01, jd-02) | none (patents not checked) | JVM or Python; PyTorch optional | viable | Java line stale since 2021; pyJedAI 0.3.6 (jd-03) |
| Ditto | Apache-2.0 code (dt-02) | model weight licences must be checked | GPU, Python 3.7 / PyTorch 1.9 pins; not CPU-first (dt-01) | viable after weights download | Unmaintained since 2021-09-24 (dt-02) |
| LLM matching | per-model licence | Llama-community-style terms need review | local model; CPU slow, GPU preferred (lm §7) | needs local model | research approach (lm-01) |
| Ontop | Apache-2.0 (on-02) | none; CLA on contributions, JDBC drivers user-supplied | stateless JVM, Docker (on §10) | yes | Active, slow cadence: 5.5.0 on 2026-02-14 (on-02, on-03); Ontopic ownership change unverified (on §1) |
| RML tools | MIT / Apache-2.0 (rml-01..05) | none | JVM, Node, Python | yes | RMLMapper, Morph-KGC, SDM-RDFizer active; RML-Streamer stale since 2023 (rml-02) |
| OpenRefine | BSD (or-01) | none | local Java app | yes except Wikidata | Active, 3.10.1 (or-02) |
| PuppyGraph | Closed engine; Developer free (1 node, 2 sources), Enterprise priced by memory/CPU (pg-02, pg-03) | **Legal review: yes.** OEM terms not publicly verified | Docker; AWS AMI | partial, licence enforcement unverified | Commercial, active |

## 4. Performance evidence

No comparable evidence exists across products. Everything below is vendor, maintainer or user attribution; none was reproduced.

| Source | Figure | Workload / hardware | Class |
|---|---|---|---|
| Splink maintainers | ~1M records in about a minute (sp-06) | laptop and model unspecified | maintainer claim, confidence 0.3 |
| Homes England via Splink docs | ~30M addresses in under 5 h (sp-07) | Databricks, cluster size unknown | user report, 0.4 |
| Zingg docs | 120k Febrl in ~5 min; 5M voters in ~4 h (4 cores, 10 GB); 9M x 3 fields in ~45 min (96 cores, 384 GB) (zg-08) | stated hardware; re-measurable via CI jobs | maintainer sizing |
| Senzing | ~10M records in ~3 h for under $100 (2020); 100B records claim (sz-12) | no hardware stated | vendor marketing, 0.2 to 0.25 |
| SDM-RDFizer | v4.0 best in authors' testbeds (rml-05) | hardware not given | vendor claim |
| OAEI 2025 | Anatomy aligned in under 100 s by LogMap, LogMapLt, LogMapKG, LSMatch, Matcha (oa-04) | campaign hardware not stated here | independent but preliminary |
| PuppyGraph | 10-hop queries in 2 s (pg-04) | MotherDuck/DuckDB, hardware not stated | vendor claim, 0.4 |
| EOIP | none measured; `merge()` is O(E) per absorbed node (BL-34 HEAD) | n/a | static code reading |

Senzing's EULA forbids publishing performance comparisons without consent (sz-05), so independent public benchmarks cannot be produced for it without a licence agreement. The ER literature also warns that benchmark F1 tends to overstate real-world results (sz-16). Acceptance tests POC-ER-01 and POC-ER-02 (Splink deep dive §12) and the Dedupe label-efficiency curve (dd §14) remain PROPOSED, not run.

## 5. Findings

1. **No open-source ER engine ships durable merge/split with survivorship.** Splink recomputes clusters each run and has no persistent IDs or survivorship (sp-18, reasoned inference, confidence 0.55); Zingg gates incremental runs, explain and ID reassignment to Enterprise (zg-05); Dedupe and JedAI have none (dd §3, jd §9). Falsifiable by finding a documented unmerge API in any of the three. EOIP's `IdentityMergeLedger` is therefore a real design lead, but only as an unmounted library (BL-34/35 HEAD).
2. **Only Splink is both strong and freely redistributable.** Senzing forbids distribution (sz-05), Zingg Community is AGPL-3.0 (zg-01), while Splink (sp-01) and Dedupe (dd-02) are MIT. Dedupe is low-activity (dd-03). Hence Splink is the sole REUSE candidate for the matcher.
3. **EOIP's `SplinkProbabilisticEREngine` is not Splink.** It imports no Splink, uses fixed m/u constants rather than EM-trained values, and no caller exists outside its test (BL-36 HEAD). Any quality comparison with Splink would be a comparison with a different algorithm configuration; no accuracy evidence exists for it (`identity/evaluation.py` helpers only).
4. **Real-time ER with automatic re-evaluation is a Senzing-only capability among members** (sz-09, sz-10, sz-11). Splink removed its new-record API in 5.0 (sp-15). J7 (no duplicate identities under replay) therefore needs an EOIP-owned incremental layer in either case.
5. **Explainability is available upstream except where gated.** Splink exposes waterfall/match-weight charts (sp-17) and Senzing exposes why/how APIs (sz-10); Zingg gates explain to Enterprise (zg-05). EOIP persists no per-pair terms yet (BL-41 evidence manifests could hold them).
6. **EOIP's mapping layer is not standards-conformant, and the gap is cheap to close.** CML/IR is Implemented, R2RML is partial and not conformance-tested (BL-33 HEAD, NB-09); permissive RML engines exist (rml-01..05) and the RML spec is a W3C Community Group deliverable (rml-06). One baseline defect: `OBDAPushdownEngine.rewrite_point_query` composes SQL with an f-string (rml-07).
7. **Virtual graphs are read-mostly and carry no ACL model.** Ontop has no permission model and mapping versioning is absent in OSS (on §9); PuppyGraph relies on source-side row-level security (pg-02). Any EOIP integration inherits BL-18, which is only Partial at HEAD.
8. **BL-26 profiling exceeds every open tool on the J12 spec but stops short of governed proposals.** si-08 records deterministic streaming profiling with five relationship signals; open tools stop at types (si §9). Missing: JSON Schema emission, mergeable partial profiles, global join selection, and a mounted review flow (BL-27 HEAD).
9. **Neural and LLM matchers are advisory only.** Ditto is unmaintained and GPU-bound (dt-02); LLM matching is prompt-sensitive per model and dataset (lm-01). Both fit as grey-zone rerankers emitting INFERRED claims, not as primary matchers.
10. **The Zingg and Senzing licences would each trigger legal review before any bundling; PuppyGraph's OEM terms are unpublished** (zg-01, sz-05, pg-03). Falsifiable by a vendor OEM agreement.

## 6. Implications for EOIP

| CAP | Parity needed (STR) | Exploitable weakness (INV) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-31 probabilistic matcher | STR-splink-01/02/04 (calibrated weights, TF, bounded blocking) | INV-splink-01 (no memory) | **REUSE** Splink as optional extra after POC-ER-01; replace or rename the in-house engine | "Probabilistic ER exists only as an unvalidated in-house reimplementation (BL-36 HEAD); Splink MIT is available upstream, not integrated." |
| CAP-31 merge/split, persistent IDs, survivorship | STR-senzing (re-evaluation, outcomes) | INV-splink-01, INV-dedupe-01 | **BUILD**: mount `IdentityMergeLedger`, make `merge()` incremental, add survivorship | "Reversible identity ledger is library-only and O(E); no survivorship; not on any API route." |
| CAP-30 deterministic keys | STR-senzing feature-behaviour pattern | n/a | **BUILD** (extend BL-34 beyond persons) | "Deterministic identity covers persons only." |
| CAP-24 / CAP-38 pair explanation | STR-splink waterfall, sz why/how | n/a | **BUILD** on Splink terms, persist in BL-41 manifests | "Match evidence is not persisted as terms." |
| CAP-31 senzing | n/a | L1/L2 (sz-05) | **INTEGRATE** only as customer-licensed authority; **REJECT** bundling | legal review item |
| CAP-31 Zingg | STR-zingg-01/02 (active learning, learned blocking) | INV-zingg-01 | **EXPERIMENT** process-isolated; **REJECT** Enterprise dependency | defer AGPL to legal |
| Active learning / uncertain-pair queue | STR-dedupe-01 | INV-dedupe-01 | **EXPERIMENT** over BL-35 | "Review queue not ranked by model uncertainty." |
| Pair reranker (Ditto, LLM) | STR-ditto-01, STR-llmem-01 | INV-ditto-01, INV-llmem-01 | **EXPERIMENT**, advisory-only INFERRED; verdict cache BUILD | |
| Blocking diagnostics | STR-jedai-01/02 | INV-jedai-01 | **BUILD** metrics, **EXPERIMENT** meta-blocking as evaluator | |
| CAP-29 RML/R2RML | STR-rml-01/02 | INV-rml-01 | **BUILD** Turtle importer + conformance CI; **INTEGRATE** Morph-KGC and yarrrml-parser optionally | "R2RML/RML import is a dict adapter; no conformance suite." |
| CAP-21 OBDA | Ontop sidecar | INV-ontop-01 (hybrid virtualise/materialise), INV-ontop-02 (ACL) | **INTEGRATE** Ontop; **BUILD** hybrid policy and ACL pushdown; **REJECT** PuppyGraph bundling | "Virtualisation exists as contracts; no engine." |
| CAP-28 / CAP-41 J12 | STR-si-01 (schema fusion), STR-si-02 | INV-si-01 | **BUILD** JSON Schema emission and review wiring; **EXPERIMENT** join ranking | "Proposals are not wired to review and promotion." |
| Reconciliation endpoint | STR-or-01/02 | INV-or-01 | **BUILD** tenant-aware endpoint | |
| Ontology alignment | STR-oa-01/02 | INV-oa-01 | **EXPERIMENT** LogMap sidecar; **REJECT** AML (stale) | |
| CAP-78 ER evaluation | STR-jedai-02 | n/a | **BUILD** harness; **REUSE** Magellan/OAEI datasets | "No ER accuracy measurement." |

Backend neutrality: none of these members touches HugeGraph, Neo4j or Neptune; Splink and Senzing consume staging tables built from SourceEvents (sp §10, sz §10), so behaviour is backend-independent. Senzing would hold a second identity store (sz §10).

## 7. Open questions

1. Does Splink 5 phone home? Verify with egress blocked (sp-20, POC-ER-01).
2. Can Senzing activate licences offline, and does it offer native multi-tenancy or configurable survivorship (sz-18, all unverified)?
3. Which mounted route should expose `IdentityMergeLedger`, given `/api/v1/identity/*` still uses the older resolver (BL-34 HEAD)?
4. What are the Zingg AGPL implications of a process-isolated, customer-installed deployment (zg §10)?
5. Is Ontopic acquisition by Digital Science real (on §1, unverified), and how does it affect the Ontop roadmap?
6. Can the in-house engine reach pairwise F1 of at least 0.90 without EM-trained m/u values (POC-ER-01)?
7. Which entity types beyond persons need principle profiles for IT assets (sz L5)?
8. Evidence conflicts noted: Senzing PostgreSQL minimum differs between pages (sz-04); Splink 5.0.0 date differs between PyPI and GitHub (sp-02); the Senzing 4.3.2 versus 4.3.3 retry attribution differs between summaries (sz-15). None changes a decision.
