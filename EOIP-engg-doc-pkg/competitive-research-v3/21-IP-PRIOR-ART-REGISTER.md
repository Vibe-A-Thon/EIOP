# 21 — IP and Prior-Art Register

| Field | Value |
|---|---|
| Document | 21-IP-PRIOR-ART-REGISTER.md (Master Prompt §16 item 22; dimension 23, §7) |
| Generated | 2026-10-26 by the coordinator, from `06-MASTER-CAPABILITY-MATRIX.md` §2 (differentiation map), `09-CON-TO-PRO-INVERSION-REGISTER.md` §3 (self-inversion cards) and the 329-entry technology registry |
| Scope | Candidate novel mechanisms in EOIP's target architecture; related prior art found during this research programme; a novelty-risk note; items flagged for legal/patent-counsel review. **This register records facts and flags items for review. It gives no legal conclusion on patentability, freedom-to-operate, or infringement** (Master Prompt §7 dimension 23). |
| Method | A mechanism is listed here only if `06-MASTER-CAPABILITY-MATRIX.md` §2 marks its capability as having **no native provider among the 329 researched technologies**, or if a self-inversion card's selected design combines known techniques in a way not observed together in any single researched technology. |

## 1. Candidate mechanisms

### IP-01 — ACL-and-tenant-principal propagation through every subsystem, including agent memory and exports, with a single consistency-token revocation path

- **Description:** every fact, chunk, edge and agent-memory record carries an ACL-principal set and tenant scope at write time; every retrieval stage (keyword, vector, graph, hybrid, GraphRAG, agent memory, MCP tools, file/vault exports) pre-filters by the caller's resolved principal set and tenant, with a mandatory delivery-time re-check; a single consistency token (Zanzibar-style zookie/ZedToken pattern) invalidates cached and in-flight results on any permission or tenant change. See `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-01, INV-SELF-02, INV-SELF-04, INV-SELF-09.
- **Prior art found:** partial, component-level prior art only. OpenFGA/SpiceDB implement the Zanzibar consistency-token pattern for authorization checks (`04-COMPETITOR-DEEP-DIVES/C19-rebac.md`, STR-rebac-01) but not for retrieval candidate generation. Onyx tags per-chunk ACL principals in its search index (`C07-onyx.md`, STR-onyx-01). OpenSearch and pgvector enforce document/row-level security inside their own engines (`C10-opensearch.md`, `C10-pgvector.md`). No researched technology propagates the *same* principal model through keyword + vector + graph + agent memory + MCP tools + file export in one consistency domain; each researched system that has any of these pieces has it for one subsystem only.
- **Novelty risk:** the individual techniques (ACL tagging, consistency tokens, candidate pre-filtering) are each well established and likely not independently patentable. The combination — one propagated model across every knowledge-access surface including agent memory and MCP, verified by one benchmark (BM-04/BM-05) — is the candidate novel element. **Legal-review trigger: yes** (method claims combining known techniques across a new surface may be a defensible combination patent; counsel should assess).
- **Status:** DEFER to legal/patent counsel; EOIP should not publicly describe this mechanism in marketing before that review, per standard trade-secret/patent-filing practice (not a legal conclusion — a scheduling note).

### IP-02 — Backend-neutral typed query intermediate representation with per-backend conformance certification, spanning property-graph and RDF dialects

- **Description:** a single typed `QueryPlan`/AST compiled to gremlin-lang, openCypher and SPARQL, with a conformance test suite certifying semantic equivalence per backend (HugeGraph, Neo4j, Neptune, JanusGraph, plus an optional RDF sidecar). See `06-MASTER-CAPABILITY-MATRIX.md` CAP-20 (no native provider among 329 researched technologies), `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-08, GAP-04/GAP-05.
- **Prior art found:** query abstraction layers across SQL dialects are long-established (e.g. ORMs, Apache Calcite). Cross-paradigm graph abstraction specifically — one IR compiled to both property-graph dialects *and* SPARQL, with a certified conformance suite — was not found as a shipped product among the 329 researched technologies; PuppyGraph and Ontop virtualise relational-to-graph but do not compile one IR to multiple graph query languages (`C01-puppygraph.md`, `C04-ontop.md`). Apache Calcite (not in this registry; general industry knowledge) does this for SQL dialects, which is the closest prior art pattern, though not for Gremlin/Cypher/SPARQL.
- **Novelty risk:** the pattern (one IR, multiple target compilers, conformance suite) is well established in the SQL-dialect world; applying it to Gremlin/Cypher/SPARQL may be a novel application rather than a novel mechanism. **Legal-review trigger: yes**, scope limited to "novel application of known technique" assessment.
- **Status:** DEFER to counsel; proceed with engineering regardless (Master Prompt: IP review does not gate the roadmap, only public disclosure and filing decisions).

### IP-03 — Storage-level epistemic-state enforcement with mandatory promotion workflow, backend-neutral

- **Description:** observed/inferred/predicted/approved states are enforced as a required, backend-native label or namespace that the mutation gateway refuses to omit — not an application convention — so that bypassing the state guarantee requires bypassing the gateway itself; promotion from one state to another requires a recorded review step. See `06-MASTER-CAPABILITY-MATRIX.md` CAP-43 (no native provider among 329 researched technologies), `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-06, GAP-07.
- **Prior art found:** the general pattern of staged/graded data quality (e.g. medallion architecture bronze/silver/gold in data lakes; draft/published content states in CMSs) is widespread and not novel in the abstract. Specific to knowledge graphs, no researched engine enforces an observed/inferred/predicted/approved state at the storage layer as a backend-neutral guarantee; competitors with any related concept (e.g. RDFox's materialisation vs query-time facts, `C02-rdfox.md`) do not expose it as a governed, reviewable promotion workflow.
- **Novelty risk:** likely a novel application of a known pattern (staged data states) to a new domain (knowledge-graph epistemic status) with a specific enforcement mechanism (gateway-level refusal). **Legal-review trigger: yes.**
- **Status:** DEFER to counsel.

### IP-04 — Digital thread combining code-symbol graph, bitemporal validity, evidence spans and ACL in one queryable structure

- **Description:** the change-impact digital thread (Jira Story → PR → commit → function → service → deployment → incident) carries, on every edge and node, a validity interval (bitemporal), an evidence span back to its source, and an ACL principal set — answered through one query rather than joined across separate systems at query time. See `06-MASTER-CAPABILITY-MATRIX.md` CAP-69 ("no competitor natively"), journeys J1/J9/J10, GAP-40.
- **Prior art found:** code-intelligence products (Sourcegraph, CodeQL — `C15-sourcegraph.md`, `C15-codeql.md`) provide precise code graphs but not bitemporal validity or an ACL/evidence model combined in the same structure. Enterprise work-graph platforms (Palantir Foundry, ServiceNow — `C07-palantir-foundry.md`, `C07-servicenow-kg.md`) provide object-linking and lineage but were not found to combine code-symbol precision with bitemporal validity.
- **Novelty risk:** a combination of several known graph-modelling patterns (temporal edges, evidence provenance, ACL tagging) applied jointly to the code-to-incident thread. **Legal-review trigger: yes**, combination-patent scope only.
- **Status:** DEFER to counsel; this is currently unbuilt end-to-end (GAP-40), so filing (if pursued) should wait until the mechanism is implemented and tested (BM-12).

### IP-05 — Backend-neutral tenant-isolation placement model enforced identically across graph, vector, search, cache, log and agent-memory layers, certified by one cross-layer benchmark

- **Description:** one isolation-model contract (SILO/BRIDGE/POOL) with a per-layer placement requirement (graph namespace, vector collection, search index, relational schema, object prefix, event topic, secrets path, KMS key, cache-key prefix, log stream, agent memory) proven by one benchmark (BM-05) across every backend simultaneously. See `06-MASTER-CAPABILITY-MATRIX.md` CAP-47, `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-02, GAP-03.
- **Prior art found:** per-engine tenant isolation is common (Weaviate shard-per-tenant, FalkorDB graph-per-tenant key, Neo4j EE multi-database, Apache AGE row-level security — `C10-weaviate.md`, `C01-falkordb.md`, `C01-apache-age.md`). A single contract enforced and *benchmark-certified* identically across all layers of a heterogeneous multi-backend system (not one engine) was not found among the 329 researched technologies.
- **Novelty risk:** likely a novel combination/application rather than a novel primitive — each per-layer mechanism already exists somewhere; the cross-layer, cross-backend certification is the candidate novel element. **Legal-review trigger: yes.**
- **Status:** DEFER to counsel.

### IP-06 — Wisdom/decision graph layer above the knowledge graph, with governed rationale, outcome and context-applicability records

- **Description:** a layer above the fact/evidence graph recording decisions, their rationale, observed outcomes and the context in which they remain applicable, queryable alongside the knowledge graph it sits above (Master Prompt §11 hypothesis 5). See `07-GAP-REGISTER.md` GAP-45, `01-SYSTEM-BASELINE.md` BL-56 (currently library-only).
- **Prior art found:** none of the 329 researched technologies implements this as a product feature. The closest adjacent work is process mining's object-centric event logs (OCEL 2.0, `C07-process-mining.md`) and organisational decision-record practices (ADRs themselves, as a documentation convention, are widely used but not graph-modelled as a queryable layer in any researched product).
- **Novelty risk:** the concept is currently unimplemented at EOIP (library-only) and the scope is still vague per the self-inversion/gap analysis (GAP-45 notes "scope must be defined"). **This is the least mature candidate in this register** — too early for a meaningful novelty assessment. **Legal-review trigger: not yet** — revisit once the design is concrete.
- **Status:** DEFER (design); not yet ready for IP review.

### IP-07 — White-label, multi-tenant, backend-neutral, air-gap-capable "organisation brain" as one combined offering

- **Description:** the combination itself — self-hosted, backend-neutral across property-graph and RDF engines, white-label/OEM-ready, air-gap capable, with epistemic separation and ACL/tenant guarantees proven by a public (non-"LDBC Benchmark Results"-labelled) benchmark suite — as a single product positioning. See `00-EXECUTIVE-SUMMARY.md` (once written) and the enterprise work-graph cohort (`05-COMPARISON-COHORTS/05-ENTERPRISE-WORK-GRAPHS-COHORT.md`).
- **Prior art found:** every closest commercial competitor researched combines only a subset: Palantir Foundry is heavyweight and not OEM-able (`C07-palantir-foundry.md` INV-palantir-foundry-01); Glean and Atlassian Rovo are SaaS/limited air-gap (`C07-glean-enterprise.md`, `C07-atlassian-rovo.md`); Onyx is open and self-hosted but gates permission-sync behind its Enterprise licence and is not backend-neutral across graph engines (`C07-onyx.md`).
- **Novelty risk:** this is a product-positioning combination, not a technical mechanism; it is unlikely to be independently patentable on its own, but the underlying mechanisms (IP-01 through IP-05) that make the combination credible are the actual candidates.
- **Status:** not a patent candidate by itself; recorded for competitive-positioning purposes, cross-referenced from the executive summary.

## 2. Related prior art inventory (non-exhaustive, from this research programme)

| Area | Closest prior art | Deep dive |
|---|---|---|
| ACL-aware search indexing | Onyx per-chunk ACL principals; OpenSearch document-level security; pgvector row-level security | C07-onyx.md, C10-opensearch.md, C10-pgvector.md |
| Consistency-token revocation | OpenFGA / SpiceDB (Zanzibar model) | C19-rebac.md |
| Cross-dialect query compilation | Apache Calcite (SQL dialects, general knowledge, not in registry); openCypher→GQL convergence effort | C18-opencypher.md |
| Virtual/federated graph over relational sources | Ontop (OBDA); PuppyGraph (zero-ETL) | C04-ontop.md, C01-puppygraph.md |
| Bitemporal storage | XTDB; Datomic; TerminusDB | C13-xtdb.md, C13-datomic.md, C01-terminusdb.md |
| Staged/graded knowledge state (analogy only, different domain) | Data-lake medallion architecture (general industry knowledge, not in registry) | — |
| Object-centric process/event modelling | OCEL 2.0; Celonis | C07-process-mining.md |

## 3. Items for legal review (summary)

| IP-ID | Trigger reason | Urgency |
|---|---|---|
| IP-01 | Novel combination across access surfaces; competitive sensitivity | Before public disclosure of the mechanism |
| IP-02 | Known technique in a new application domain | Before public disclosure |
| IP-03 | Known pattern (staged data), new enforcement domain | Before public disclosure |
| IP-04 | Combination of known graph-modelling techniques | After implementation (GAP-40), before disclosure |
| IP-05 | Cross-layer, cross-backend certification claim | Before public disclosure |
| IP-06 | Design not yet concrete | Revisit after design (GAP-45) |

This register is a factual record and a scheduling aid for legal counsel. It is not legal advice and gives no view on patentability, prior-art invalidation risk, or freedom to operate.
