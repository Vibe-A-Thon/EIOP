# 00 — Executive Summary

| Field | Value |
|---|---|
| Document | 00-EXECUTIVE-SUMMARY.md — the final deliverable of `KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md`, written last as the prompt requires |
| System under design | KnowGridFlow / EOIP (the candidate rebrand "Semaplexvell" is not used anywhere in this package — its spelling was never confirmed; see `22-OPEN-QUESTIONS-AND-ASSUMPTIONS.md` A-01) |
| Programme dates | Baseline verified 2026-10-18 (commit `ad9937b`); re-verified at HEAD `896e06d` on 2026-10-26 after a large concurrent merge; all subsequent research accessed 2026-10-26 |
| Supersedes | A non-evidence-based pass dated 2026-10-19 wrote placeholder versions of most files in this package (no `CLAIM-` evidence records, several fabricated figures and one fabricated test "PASS"). Every one is identified and overwritten in this run; see §7 below. |
| Status | Single continuous research pass, interrupted repeatedly by the execution environment's own rate limits (never by a deliberate pause for approval) — see §6 |

---

## 1. What was researched

**329 technologies** across the 20 mandated categories (C01–C20), every one carrying a tier assignment with a stated reason:

| Tier | Count | Depth |
|---|---|---|
| A — full reconstruction | 44 | 15-heading deep dive, all 24 research dimensions, strength/inversion cards |
| B — capability and architecture profile | 145 | 15-heading deep dive, compact |
| C — inventory record | 140 | identity, licence, status, one relevance paragraph, decision |

**Registry disposition:** 329 KEEP, 0 EXCLUDE, 2 DEFER (sub-members: RML-Streamer, FinBench/SPB inside the LDBC record), 0 ADD beyond the one the methodology itself proposed (`T-C20-shacl-test-suites`, added at seeding to close a conformance-test gap the master prompt's own registry did not name). Full log in `02-TECHNOLOGY-REGISTRY.md` §2.

**Evidence base:** 210 deep-dive files (189 Tier A/B reports + 21 Tier C batch records) carrying 804 CAP-ID strength/inversion card references and 1,696 capability-mapping rows extracted mechanically for the matrix; 16 workload-aligned cohort comparisons; a verified system baseline re-audited at two commits six working days apart.

## 2. Top 10 gaps (full register: `07-GAP-REGISTER.md`, 46 gaps)

| Rank | GAP-ID | Gap | Priority | Class |
|---|---|---|---|---|
| 1 | GAP-02 | Source-ACL enforcement exists in code but is not applied on any deployed retrieval, answer, memory, export or MCP path | P0 (forced) | Security |
| 2 | GAP-03 | Tenant isolation is a contract, not a guarantee — zero tenant handling in the graph adapters themselves | P0 (forced) | Security |
| 3 | GAP-09 | The MCP surface authenticates one shared bearer token; every caller is the same principal | P0 (forced) | Security |
| 4 | GAP-19 | No CI licence allow-list; several attractive components (Zingg, FalkorDB, Vault, Grafana, Elasticsearch, Airbyte, Redpanda, TruffleHog, PM4Py, igraph, Raphtory, Logseq, several OWL reasoners) would block white-label OEM if adopted without review | P0 (forced) | Differentiator-protecting / Operability |
| 5 | GAP-08 | The egress vault encrypts with an unauthenticated XOR keystream cipher | P0 (forced) | Security |
| 6 | GAP-36 | Local model runtime (Ollama) is pinned about a year old, runs as root, has no authentication | P0 (forced) | Security + Operability |
| 7 | GAP-01 | Backend adapters are unproven live, with three named code-level defects (JanusGraph key-prefix mismatch, Neptune has no SigV4 signing, HugeGraph forces a Groovy closure that will not run on gremlin-lang-only backends) | P0 (forced) | Quality |
| 8 | GAP-07 | Epistemic separation (observed/inferred/predicted/approved) is enforced in application code but not as a storage-level guarantee on every backend | P0 (forced) | Differentiator-at-risk |
| 9 | GAP-43 | No unified evaluation harness with regression gates — every other claim in this package, and every future claim about EOIP, is unverifiable without one | P0 (forced) | Quality |
| 10 | GAP-05 | String-built Gremlin in two backend adapters plus a regex-only prompt-injection firewall | P0 (forced) | Security |

All ten are **forced P0** under the priority rule (correctness, lineage, permission and tenant protection override the numeric score). This is not a coincidence of scoring — it means EOIP's most urgent work is closing its own security and reliability debt, not chasing a competitor feature. 11 gaps in total are forced P0; the 11th (GAP-34, agent memory lacking ACL/tenant/evidence fields) ties with GAP-05 at rank 11.

## 3. Top 10 strength-adoption and inversion opportunities (full registers: `08`, `09`)

| Rank | ID | From | What to adopt / invert |
|---|---|---|---|
| 1 | STR-onyx-01 | Onyx | Per-chunk ACL principal strings filtered at query time — the concrete pattern that closes GAP-02 |
| 2 | STR-rebac-01 | OpenFGA / SpiceDB (Zanzibar) | Consistency tokens so a permission revocation is never served stale |
| 3 | STR-opensearch-01 / STR-pgvector-01 | OpenSearch / pgvector | Engine-enforced document- and row-level security as optional VectorPort adapters |
| 4 | STR-tinkerpop-01 | Apache TinkerPop 4.0 (beta) | Parameterised gremlin-lang with typed parameters — closes GAP-05 by construction once adopted |
| 5 | STR-n4gr-02 | Neo4j GraphRAG | EXPLAIN-based read-only validation of LLM-generated queries — closes part of GAP-35 |
| 6 | STR-lancedb-01 | LanceDB | Embedded persistent ANN + full-text + hybrid search with no separate service — the default VectorPort engine candidate (closes GAP-46) |
| 7 | STR-pyshacl-01 | pySHACL | Already Apache-2.0 and installed at HEAD — the conformance oracle for GAP-11, ready to use now |
| 8 | STR-edg-01 | TopBraid EDG | Git-backed ontology governance with role-gated commit and SHACL-gated review — the design target for GAP-17 |
| 9 | INV-msgraphrag-01 | Microsoft GraphRAG | The §10.5 seed hypothesis on costly indexing is validated for cost but refuted as to cause (~75% of cost is extraction, not summarisation) — redirects the fix for GAP-33 |
| 10 | INV-sourcegraph-01 | Sourcegraph | Its core went closed-source in 2023/2024 — the opening for a native SCIP-based code-intelligence graph (GAP-39/40) that stays open |

**Seed hypotheses (Master Prompt §10.5):** every one of the ten was investigated and none was accepted unexamined. Verdicts range from fully validated (Graphiti/agent-memory's LLM-dependent extraction cost) through partially validated with correction (Protégé, TopBraid EDG, Neo4j, Microsoft GraphRAG, Ontop, Gephi, Palantir/Glean/Rovo — each validated on some claims and rejected on others) to mixed (Stardog). Full table in `09-CON-TO-PRO-INVERSION-REGISTER.md` §1.

## 4. Investment and complexity

- **P0 (11 gaps, 14 requirements, Phase 0 of the roadmap):** the structural prerequisite for everything else. Two sequencing chains, surfaced during architecture and roadmap synthesis and not visible in the gap register's own tables, must be respected: the typed query-IR compiler (GAP-04) is a near-term-patchable / long-term-structural fix for GAP-01 and GAP-05 (fix the three named defects now; retire string-built Gremlin by construction later), and tenant isolation (GAP-03) is a precondition for correctly scoping source-ACL enforcement (GAP-02) and the epistemic planes (GAP-07). Full dependency-aware sequencing in `14-IMPLEMENTATION-ROADMAP.md` (52 work packages across Phase 0–2 and a research track).
- **P1 (25 requirements):** high-value integration and parity work — REUSE-grade items (pySHACL, Splink, LanceDB, BGE-M3 embeddings) are comparatively cheap; BUILD-grade items (typed constraint layer, governed ontology workflow, digital-thread journeys) are not.
- **P2/P3 (18 requirements):** demand-gated and research-track; explicitly not scheduled by default (Master Prompt §13 "distinguish product priority from research priority").
- **Licensing:** every REUSE/INTEGRATE decision in `02-TECHNOLOGY-REGISTRY.md` carries a licence class; the registry's §3 lists every legal-review trigger found (GPL/AGPL/SSPL/BUSL/ELv2/proprietary components). None blocks the roadmap; several block *bundling* and are marked customer-opt-in or reference-only instead.

## 5. Honest limits of this research

- **No benchmark was executed.** All 22 benchmark specifications (`15-VALIDATION-BENCHMARK-PLAN.md`) and both POC specifications (`20-POC-EXPERIMENTS/`) are PROPOSED. No performance number anywhere in this package is a result of this programme's own testing; every systems or ML figure is either EOIP's own prior test history (clearly cited) or a competitor's own published claim (labelled as a vendor claim).
- **Live backend behaviour is unverified.** Every adapter defect found (JanusGraph, Neptune, HugeGraph) came from reading code, not running it against a live cluster. `BASELINE_UNCERTAINTIES` U-01 through U-17 (`01-SYSTEM-BASELINE.md`, `01a-BASELINE-DELTA-HEAD.md`) catalogue every such open question.
- **Commercial SaaS internals are documented-or-hypothesis only.** No trial accounts were used; anything not in public documentation is marked NOT PUBLICLY VERIFIED.
- **Several evidence conflicts between independent researchers were found and are tracked, not silently resolved** — `22-OPEN-QUESTIONS-AND-ASSUMPTIONS.md` §5 lists twelve, including a genuinely contested memory-benchmark literature (LoCoMo) that this package treats as unusable for ranking.
- **IP/patent register is a scheduling aid, not legal advice.** Six candidate novel mechanisms are recorded in `21-IP-PRIOR-ART-REGISTER.md` with their closest prior art; every one is explicitly deferred to counsel, with no view given on patentability.

## 6. Environment limitations encountered

This run did **not** pause for approval at any point; every interruption was the execution environment's own usage limit (documented per Master Prompt §3.4). The research was carried out as 35 initial parallel workers plus 14 further coordinator-dispatched batches across roughly 8 days of wall-clock time (2026-10-18 to 2026-10-26), resuming each interrupted worker from its own saved state rather than restarting. One coordinator error occurred during final cleanup — a real Tier C research file (`C02-tier-c-records-V16.md`, 8 RDF/Datalog engine records) was accidentally deleted alongside genuinely stale placeholders; it was recovered without fabrication from its surviving machine-readable registry fragment and is now back in the package with its original facts, sources and a matching evidence table. This is recorded here in the interest of not understating what happened during the run.

## 7. What superseded what

A prior, non-evidence-based process had written placeholder content into this exact package on 2026-10-19: 27 zero-evidence deep-dive files (all now removed, replaced by real research), draft versions of `00`, `02`, `05`–`23`, all 12 ADRs, and one proof-of-concept. Every one was identified during this run (most self-identified by containing no `CLAIM-` evidence records) and completely overwritten with evidence-based content, with two defects worth naming specifically because they illustrate exactly what this programme's evidence discipline is for:

- `ADR-KG3-10` (as it existed on 2026-10-19) proposed deprecating Cytoscape for Sigma.js, citing "60 FPS on 100,000+ nodes" with no source. The real visualisation research (`04-COMPETITOR-DEEP-DIVES/C16-sigma.md`, cohort `08-VISUALIZATION-ENGINES-COHORT.md`) found that claim unsupported by any vendor or independent benchmark at that scale, for either library. The corrected `ADR-KG3-10` (now "Local model runtime hardening" — the ADRs were renumbered to match real content) recommends measuring before deciding.
- `20-POC-EXPERIMENTS/poc-01-multi-backend-compilation/run_poc.py` (as it existed on 2026-10-19) hardcoded three fixed output strings that ignored their input entirely, then printed `POC-01 PASS: All 3 dialects compiled deterministically.` regardless of input — a fabricated pass, exactly what Master Prompt §15 prohibits. It is replaced with an honest specification stub that runs cleanly and claims nothing.

## 8. Quality gates (Master Prompt §17)

| Gate | Result |
|---|---|
| Coverage | Every user-named technology resolved (329/329); every Tier A/B entry has a full deep dive |
| Depth | Every deep dive addresses all 24 dimensions and all 15 template headings, or marks N/A with a reason |
| Verification | Every substantive competitive claim carries a classification, date and confidence; unknowns are marked unknown throughout |
| Baseline | Status vocabulary (Implemented/Partial/Planned/Absent/Unknown) is applied consistently from code and test evidence, re-verified at two commits |
| Standards | RDF/OWL and LPG semantics are kept distinct throughout (`15-STANDARDS-INTEROPERABILITY-COHORT.md`); standards are labelled by exact current status (REC/CR/WD/published ISO/de facto) |
| Architecture | No mandatory cloud, hidden egress, backend lock-in or ungoverned agent writes in `10-TARGET-REFERENCE-ARCHITECTURE.md` |
| Security and tenancy | The single largest cluster of P0 findings in this package (GAP-02/03/07/09/34) — not treated as solved by self-hosting alone |
| Licensing | Every REUSE/INTEGRATE decision records licence class and redistribution notes; every legal-review trigger is logged, none concluded |
| Performance | No fabricated numbers survive in this package (see §7); every benchmark is PROPOSED |
| Engineering | All 57 requirements carry use case, source gap, NFRs, dependencies, tests and effort |
| Product | Feature bloat explicitly rejected where found (e.g. CAP-03 multi-model storage marked "unnecessary complexity, avoid") |
| Traceability | 57/57 requirements and 46/46 gaps appear in `19-TRACEABILITY-MATRIX.md`; every requirement maps to exactly one roadmap work package |
| Single-pass | No deliberate pause for approval occurred; every interruption was the environment's own rate limit, resumed from saved state |

**No unsupported declaration of completeness is made here.** Every number in this summary is drawn from the registers it summarises, and every one of those registers states, in its own evidence appendix, exactly what remains unverified.
