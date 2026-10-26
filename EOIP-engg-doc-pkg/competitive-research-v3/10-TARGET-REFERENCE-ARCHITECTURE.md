# 10 — Target Reference Architecture (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 10-TARGET-REFERENCE-ARCHITECTURE.md (Master Prompt v3.0 §11, composed from `06-MASTER-CAPABILITY-MATRIX.md`, `07-GAP-REGISTER.md`, `08-STRENGTH-ADOPTION-REGISTER.md` §1, `09-CON-TO-PRO-INVERSION-REGISTER.md` §3) |
| Supersedes | The 2026-10-19 placeholder version of this file, which carried no CLAIM records and at least one unsupported figure (a "60 FPS on 100,000+ nodes" Sigma.js claim with no benchmark). Overwritten in full. |
| EOIP status basis | `01-SYSTEM-BASELINE.md` (commit `ad9937b`), superseded where different by `01a-BASELINE-DELTA-HEAD.md` (commit `896e06d`, HEAD) |
| ADR numbering | This package uses `ADR-KG3-01`..`ADR-KG3-12` (`18-ADRS/`), distinct from `ADR-001`..`ADR-010` in `EOIP-engg-doc-pkg/64-decisions-and-adrs.md` and `ADR-H15`/`H16`/`H17` in `docs/decisions/` |
| Decision scope | This document composes and sequences decisions already made in `06-MASTER-CAPABILITY-MATRIX.md` (per-CAP-ID BUILD/REUSE/INTEGRATE/EXPERIMENT/DEFER/REJECT) and in the 11 self-inversion cards (`09-CON-TO-PRO-INVERSION-REGISTER.md` §3). No new decision is introduced here. |

---

## 1. Principles

These derive directly from Master Prompt §4.3 (non-negotiable constraints) and the forced-P0 gaps in `07-GAP-REGISTER.md` §1. Each principle names the constraint and the gap(s) that make it non-negotiable rather than aspirational.

1. **Backend neutrality is a protocol guarantee, not a marketing claim (§4.3.3).** EOIP already has adapters for HugeGraph, Neo4j, Neptune, JanusGraph, Fuseki and GraphDB behind one `GraphStore` protocol (BL-01..06, Implemented/live-unverified). The principle this architecture enforces is narrower than "we support many backends": every capability must be labelled backend-native, emulated, or unavailable per backend (CAP matrix column 6), and no capability may silently assume HugeGraph-only behaviour. GAP-01 (adapters unproven live, known defects) and GAP-04/05 (query IR not on the production path, string-built Gremlin) are the two gaps that currently violate this principle in practice, not in design.
2. **ACL/tenant correctness is a storage-level guarantee, not an application convention.** This is the architecture's central correction. Permission metadata is captured at ingest (BL-17, Implemented) and an evaluator exists (`authz/pdp.py`, `authz/derivation_acl.py`), but it is wired into exactly one branch of one retrieval path, gated on an optional `scope` argument that no deployed caller passes (GAP-02, Critical, forced P0). Tenant isolation is worse: zero adapter code reads a tenant context (GAP-03, Critical, forced P0). Per Master Prompt §4.3 items 8–9, these are platform defects regardless of what any competitor does, and INV-SELF-01/02 already select the target design (ACL principals on every chunk/fact/edge, pre-filtered at every candidate-generation stage, re-checked at delivery, invalidated by a consistency token on revocation; tenant placement chosen per backend's native isolation unit). This architecture treats "mandatory, unconditional" as the only acceptable shape for both — optional parameters are the bug class being removed.
3. **Epistemic separation is a storage-level guarantee, not a contract class.** `ai/boundary.py` enforces PROPOSED-until-promoted in its own logic (BL-40, Implemented as contract), but nothing stops a write that bypasses the boundary module from landing as an observed fact on any given backend (GAP-07, forced P0, CAP-43 — a differentiator candidate because no researched competitor provides this natively). INV-SELF-06 selects the fix: a required `epistemic_state` property enforced by the mutation gateway's validation gate, with per-backend namespace/label separation as the medium-term target.
4. **CPU-first.** Every mandatory code path runs on CPU. GPU/TPU/NPU/APU/etc. labels in the processing-unit catalog are logical families, not physical accelerators (NB-01, `physical: False` for non-CPU families) — this is honest scaffolding, not a capability claim, and the architecture does not promote it to one. The neural tier (`torch`-based encoders, BL-44) is EXPERIMENT-only (GAP-38) until it is executable in a shipped environment and beats a tabular baseline; it is never a dependency of a mandatory path.
5. **Air-gap capable.** One-node, offline operation (HugeGraph or Neo4j CE) is the default deployable tier; Neptune, being AWS-managed, is excluded from the air-gap tier by construction, not by configuration (CAP-50, GAP-21). GAP-21's own evidence record ("Neptune cannot be air-gapped") already rules this out; this architecture makes that exclusion structural in §6 rather than leaving it as an operational note.
6. **Licence-clean by construction.** The platform is sold and white-labelled (§4.3.12); GAP-19 (forced P0) found no CI gate gating this and named specific components (Zingg AGPL-3.0, FalkorDB SSPL, Vault BUSL, Grafana AGPL-3.0, Elasticsearch AGPL/SSPL/ELv2, Airbyte mixed, Redpanda BUSL, TruffleHog AGPL-3.0, PM4Py AGPL-3.0, igraph GPL-2.0, Raphtory GPL-3.0, several OWL reasoners LGPL/AGPL) that would block OEM resale if adopted without review. INV-SELF-11 selects a CI allow-list as the structural fix; this architecture treats "not yet on the allow-list" as a blocking condition for every INTEGRATE/REUSE decision below, not a post-hoc legal review.
7. **Deterministic first, AI second (§4.3, J6).** Typed, parameterized graph/text queries execute before any optional local-LLM synthesis; GraphRAG synthesis exists today with a claim-support check (BL-16, Implemented: deterministic + local-LLM with citation checking) but has never been benchmarked against a strong plain-RAG baseline (GAP-33) — so its placement in §2 is EXPERIMENT, not a default path.
8. **One-node first (§4.3.10).** Distributed scale-out is explicitly deferred (CAP-05, DEFER, demand-gated) pending BM-02 evidence at 10M+ nodes; this architecture's deployment tiers (§6) make the single-node profile the shipped default and the distributed tier a documented non-goal until that evidence exists.

A ninth, cross-cutting observation ties these together: every one of the eight principles above describes a gap between a *mechanism that exists in code* and a *guarantee that mechanism is supposed to provide*. This is the pattern `01a-BASELINE-DELTA-HEAD.md` names "library-only" or "available if called" across more than a dozen rows (BL-09, BL-18, BL-20, BL-40, BL-47, NB-03, NB-07, NB-09, NB-12, NB-14 among them): real, tested code that is reachable but not reached by any deployed caller. The eleven self-inversion cards in `09-CON-TO-PRO-INVERSION-REGISTER.md` §3 independently converge on the same three-option shape for closing this pattern — (1) a quick, scoped patch, (2) a pragmatic enhancement that makes the mechanism mandatory rather than optional, (3) a long-term structural fix that makes bypassing it impossible rather than merely undesirable — and this architecture's layered diagram in §2 is drawn specifically to make option (2) visible as a set of **[MANDATORY STAGE]** gates rather than leaving it implicit in prose. Where this document departs from treating every gap identically is in sequencing: GAP-43 (the evaluation harness) is drawn out as the one gap that is purely infrastructural — it has no user-facing capability of its own, but every other gap's benchmark (BM-01 through BM-22) depends on it existing, which is why ADR-KG3-07 frames it as precondition rather than parallel work.

## 2. Layered reference architecture

Every box below traces to a CAP-ID from `06-MASTER-CAPABILITY-MATRIX.md`; GAP-IDs mark where the box differs from what HEAD actually does. Boxes marked **[MANDATORY STAGE]** are gates that the mutation/retrieval path cannot bypass under this architecture — this is the structural answer to GAP-02, GAP-03 and GAP-07, each of which is today an optional call rather than a mandatory stage.

```
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ SOURCE ADAPTERS (CAP-26)                                                                     │
│  Jira/Confluence/ServiceNow/GitHub-GitLab/Datadog/Grafana/Kibana/Snowflake/Artifactory/Slack/ │
│  SharePoint*/Salesforce*/Workday* (* = CAP-26 breadth gap, GAP-26, general-enterprise sources │
│  under-represented today)                                                                    │
│  — never mutate the graph directly (BL-23, Implemented; §4.3.4)                              │
└───────────────────────────────────┬────────────────────────────────────────────────────────┘
                                     │ SourceEvent v2 (PermissionMetadata, acl_hash: BL-17)
                                     ▼
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ CANONICAL INGEST PIPELINE (§4.3.4 pipeline order; BL-23/24/27/28)                             │
│  1. Raw capture + event log → replay, DLQ, webhook dedupe (BL-24, Implemented)                │
│  2. Normalisation / schema profiling (BL-26, Implemented — key detection, relationship        │
│     discovery from arbitrary JSON; CAP-28 differentiator candidate)                           │
│  3. [MANDATORY STAGE] PII / secret scan at ingest, not only at egress (GAP-10: today only      │
│     5 regex PII types, raw values retained, no secret scan at ingest — CAP-33 fix: Presidio   │
│     MIT recognisers + gitleaks MIT rules, store hashes not raw values)                        │
│  4. Identity resolution: deterministic keys for all entity types (CAP-30, BUILD, extends       │
│     BL-34 beyond person-only) + probabilistic ER via an ER port (CAP-31, INTEGRATE: Splink     │
│     MIT behind the port; BL-36's in-house "Splink" engine is a stdlib reimplementation that    │
│     does not call Splink and stays as the no-dependency fallback, not the primary path)        │
│  5. Ontology mapping + validation: CML → engine-neutral IR (BL-33, Implemented) → typed        │
│     constraint layer (CAP-08, GAP-12: today only label/required-property checks; BUILD a       │
│     TypeDB-style cardinality/role layer) → SHACL gate using pySHACL as the conformance oracle   │
│     (CAP-10, GAP-11: pySHACL is installed @HEAD but not in the runtime lock; REUSE)            │
│  6. [MANDATORY STAGE] Ontology-proposal governance: induce_schema output must land as a         │
│     reviewable PROPOSED ontology extension in gitops before promotion (CAP-28/CAP-41, GAP-14:  │
│     today induce_schema exists but is not wired into the governance review — BUILD the wire)   │
│  7. [MANDATORY STAGE] epistemic_state assignment: every candidate fact is labelled              │
│     observed/inferred/predicted before it reaches the mutation gateway (CAP-43, GAP-07)         │
└───────────────────────────────────┬────────────────────────────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ MUTATION GATEWAY (BL-28, Implemented; GAP-12 typed constraints add-on)                        │
│  validation/gate.py: label + required-property checks (today) → typed constraint layer         │
│  (cardinality, role, value-range — CAP-08 BUILD) → [MANDATORY STAGE] tenant-scope stamp         │
│  (CAP-47, GAP-03) → [MANDATORY STAGE] epistemic_state required property (CAP-43, GAP-07) →      │
│  commit via the GraphStore protocol, never direct adapter writes                                │
└───────────────────────────────────┬────────────────────────────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ MULTI-BACKEND GRAPHSTORE PROTOCOL + TYPED QUERY-IR COMPILER (CAP-01/CAP-20, GAP-01/GAP-04/05)  │
│  GraphStore protocol (BL-01, Implemented): CRUD + neighbourhood + bulk load + tombstone         │
│  QueryPlan v1 → policy → bounded templates (BL-08, Implemented) is TODAY's only production      │
│  path. Target: QueryPlan → typed AST (BL-09, Partial, library-only) → {parameterised            │
│  gremlin-lang, openCypher, SPARQL 1.1} (CAP-20, BUILD, P1, GAP-04) compiled per backend,         │
│  replacing string-built Gremlin in two adapters (GAP-05, forced P0) and the HugeGraph forced    │
│  Groovy closure (INV-SELF-05/08). Backend conformance suite (CAP-01, GAP-01, forced P0) runs    │
│  the same workload on HugeGraph/Neo4j/Neptune/JanusGraph before every release (BM-01).          │
│  Adapters: HugeGraph(native)/Neo4j(native)/Neptune(native,cloud)/JanusGraph(native)/            │
│  Fuseki+GraphDB(SPARQL 1.1, BL-06 Implemented/live-unverified)/Memory(test only)                 │
└──────────────┬────────────────────────────────────────┬───────────────────────────────────┘
               │                                         │
               ▼                                         ▼
┌──────────────────────────────┐   ┌───────────────────────────────────────────────────────┐
│ EPISTEMIC PLANES (CAP-43)     │   │ SECURITY & TENANCY PLANE (CAP-46/47, GAP-02/03)         │
│  [MANDATORY STAGE, per        │   │  [MANDATORY STAGE] ACL-principal pre-filter at every     │
│  backend] observed /          │   │  candidate-generation stage (keyword/vector/hybrid/graph)│
│  inferred / predicted /       │   │  — today only one branch of retrieve() does this, gated  │
│  approved kept in distinct    │   │  on an optional scope arg nothing passes (GAP-02)         │
│  namespaces/labels; promotion │   │  Tenant scope resolved per backend's native isolation unit│
│  workflow with audit trail    │   │  (HugeGraph graph space / Neo4j multi-db / Neptune        │
│  (BL-40 contract → storage    │   │  cluster-per-tenant) — today zero tenant refs in adapters │
│  guarantee, GAP-07)           │   │  (GAP-03). Consistency token checked on every revocation  │
│                                │   │  (STR-rebac-01, exceed target)                            │
└──────────────────────────────┘   └───────────────────────────────────────────────────────┘
               │                                         │
               └───────────────────┬─────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ RETRIEVAL STACK (CAP-53..60)                                                                  │
│  VectorPort (CAP-53, INTEGRATE P1, GAP-46: today in-memory HNSW + hashing embedder default,    │
│  BL-14 Partial — target LanceDB embedded default + Qdrant/pgvector/OpenSearch adapters,         │
│  BGE-M3 local embeddings replacing the hashing default, STR-lancedb-01/STR-emb-01)              │
│  Full-text (CAP-54, BL-13 Implemented in-process BM25 — persisted via the same VectorPort       │
│  engine, GAP-46)                                                                                │
│  Hybrid fusion (CAP-55, BL-15 Implemented — RRF and a separate weighted fusion coexist; REUSE,  │
│  add a local reranker)                                                                          │
│  GraphRAG — **EXPERIMENT, not default** (CAP-56, GAP-33): deterministic graph-first retrieval   │
│  (BL-16, Implemented) plus local-LLM synthesis with a claim-support check is real and wired;     │
│  the community/diffusion layer (dual-level, HippoRAG-style PPR) is library-only and MUST be      │
│  benchmarked against strong plain-RAG/graph-only baselines (BM-06) before any claim of benefit — │
│  §4.3 and the Master Prompt's own corrections section are explicit that GraphRAG is not          │
│  automatically superior                                                                          │
│  Agent memory (CAP-57, BUILD P1, GAP-34): today no ACL/tenant/evidence/validity fields on        │
│  memory records (INV-SELF-09) — target: memory as a governed epistemic type, re-checked on read  │
│  NL→query (CAP-58, BUILD P1, GAP-35): LLM proposes ranked typed QueryPlan candidates with a      │
│  planner-based read-only check (STR-n4gr-02, STR-t2q-01), never raw generated query text          │
└───────────────────────────────────┬────────────────────────────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ AGENT / MCP SURFACE (CAP-59, GAP-09, forced P0, Critical)                                     │
│  Today: 18 read-oriented tools, one shared static bearer token — every caller is the same      │
│  principal, no per-user identity propagates (BL-47). Target (INV-SELF-04): per-user OAuth 2.1  │
│  resource server mapped to the existing RBAC/ABAC model, tool read-only/write annotations,      │
│  signed tool manifests, ACL check on every tool call (shares infrastructure with CAP-46)        │
└───────────────────────────────────┬────────────────────────────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ UI (CAP-70..73): React 19 + Cytoscape 3.30 + Sigma 2.4 (BL-54, Implemented; performance        │
│  unmeasured — GAP-41; measure before any library consolidation decision, see §7 Hypothesis 15) │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

Three structural points this diagram makes that the HEAD codebase does not yet enforce, each tracing to a self-inversion card:

- The three boxes marked **[MANDATORY STAGE]** in the ingest pipeline and mutation gateway, and the one in the security plane, are the architecture's answer to GAP-02/03/07/10/14: today each of these is reachable but optional (a library call nobody wires in, or a parameter nobody passes). The fix in every case is the same shape — move the check from "available if called" to "the gateway refuses the mutation/query without it."
- The query-IR compiler sits beside the GraphStore protocol, not inside it — `BL-09`/`BL-09a` already exist as a typed AST compiler and plan engine, library-only. This architecture's only change is making it the one production path (ADR-KG3-12), which is also what removes the GAP-05 string-building defects by construction rather than by patching two call sites.
- GraphRAG and the neuro-symbolic/temporal-learning layers are drawn as EXPERIMENT branches off the retrieval stack and epistemic planes respectively, not as core-path boxes — this is a direct rendering of the CAP-56/CAP-64/CAP-65 EXPERIMENT decisions and Master Prompt §5.3's correction that graph retrieval is not automatically superior to strong baselines.

## 3. Data, control, evidence, security and tenancy planes

### 3.1 Data plane
**Change vs. HEAD:** none structural — the SourceEvent log, replay, DLQ and webhook dedupe (BL-23/24, Implemented) and the schema profiler (BL-26, Implemented) are kept as-is; these are real, working capabilities and this architecture does not touch their internals. The profiler's key-detection and relationship-discovery logic (FK-like fields, arrays of IDs, parent pointers, URL references, polymorphic type+id — `ingest/profile.py`, 1,023 lines) is the mechanism behind CAP-28's differentiator-candidate status: no researched competitor was found to do this natively from arbitrary JSON (06-MASTER-CAPABILITY-MATRIX.md §2). The one addition to this plane is the mandatory PII/secret scan at ingest (§2 stage 3, GAP-10): today `privacy/scanner.py` covers five regex PII types and keeps `raw_value` rather than a hash, and DLP scanning only runs at the egress gateway, not at ingest — meaning a secret or PII value that never leaves the platform via an LLM call is still indexed and retained in the clear inside the graph and retrieval index. The fix adds Presidio's (MIT) checksum/context-aware recognisers with character offsets (STR-pres-01) and gitleaks's (MIT) secret-rule corpus (STR-sec-01) as an ingest-time stage, storing a hash rather than the raw value wherever a match is found, so the "never index secrets or unmanaged PII" user problem (CAP-33) is addressed at the point of entry rather than only at the point of exit.
**Gap closed:** GAP-10 (High, P1).

### 3.2 Control plane
**Change vs. HEAD:** the mutation gateway becomes the single place mutations can enter any backend — `validation/gate.py` already occupies this position (BL-28, Implemented) but checks only labels and required properties (`check_vertex`/`check_edge`), which is enough to stop a malformed record but not enough to stop a type-correct one that violates cardinality, role or value-range constraints. The typed constraint layer this plane adds (CAP-08, GAP-12) is modelled on TypeDB's write-time type/role/cardinality checking (STR-typedb-01) but implemented backend-neutrally in the gateway rather than relying on any one backend's native schema engine, because HugeGraph, Neo4j and Neptune each expose a different (or no) native constraint model — pushing the constraint check into the gateway, once, is what keeps the "same guarantee on every backend" promise from §1 principle 1 true for data quality, not just for CRUD availability. Two further mandatory stamps are added at this same gate, not scattered across individual callers: the tenant-scope stamp (feeding §3.5) and the epistemic-state stamp (feeding the epistemic planes box in §2 and §3.3's successor). Ontology evolution (CAP-37, GAP-18) is the other major addition to this plane: `migration/protocol.py` already implements an 8-stage migration protocol (discovery & pin, ... CDC catch-up, rollback — NB-09) with a CLI, but it has no live caller and its "semantic-equivalence golden queries" stage is a harness, not a wired check against real impacted queries. This plane makes the migration protocol the only path by which a schema change reaches a backend, so "dry-run migration, impacted-query analysis, rollback" (J4) stops being an available tool and becomes the only door.
**Gap closed:** GAP-12, GAP-18.

### 3.3 Evidence plane
**Change vs. HEAD:** evidence manifests, lineage and warrant composition already exist and are kept (`provenance/evidence.py`, `provenance/lineage.py`, `provenance/warrant_composition.py`, BL-41, Implemented) — every mutation already carries a provenance pointer, and this is not being rebuilt. Two additions close named gaps. First, parser-neutral character-offset span anchors on every extracted fact (CAP-32, GAP-28): today's extraction tools (`fileparse`, the NLP pipeline) lack consistent offsets into the source document, which is exactly the limitation research into both `unstructured` (C05-unstructured INV-unstr-01) and GLiNER (C05-gliner INV-gli-01) names independently — without a stable offset, a citation in a generated answer can point at the right document but the wrong passage, and re-parsing a document can silently invalidate every existing span. Docling's (MIT, offline-capable) page-and-bounding-box provenance model (STR-docl-01) is the adopted pattern: every extracted item carries its page and bounding box, not just a document ID, which is what makes citation accuracy (CAP-60) a number BM-06 can actually measure rather than an assertion. Second, claims and contradictions move from in-memory-only (`truth/engine.py`'s `TruthStore`, BL-39, Implemented but volatile across restarts) to a plane that persists identically on every backend (CAP-39, GAP-15) — this closes the same "in-memory loss on restart" risk the capability matrix names for CAP-25 (inconsistency handling). Wikidata's statement model — qualifiers, references, rank, and an explicit unknown/no-value state (STR-wikidata-01) — is the adopted pattern for what a persisted claim record looks like, rather than inventing a new claims schema from scratch.
**Gap closed:** GAP-28, GAP-15.

### 3.4 Security plane
**Change vs. HEAD:** this is the plane carrying the most forced-P0 work — four of the platform's eleven forced-P0 self-inversion cards land here, and together they are the largest single body of work in this architecture. Each is already selected by its own self-inversion card and detailed in its own ADR (§7 table, `18-ADRS/`):
- ACL-principal pre-filtering made mandatory at every retrieval stage — keyword, vector, hybrid and graph alike, not only the one graph-traversal branch that calls it today — with a delivery-time re-check and a policy-epoch consistency token so a permission revocation is honoured immediately rather than on the next cache expiry or re-index (GAP-02, INV-SELF-01, ADR-KG3-01).
- The egress vault's XOR keystream replaced with an AEAD cipher (AES-GCM), closing a real, proven liability — `tenancy/layers.py` already uses AES-256-GCM elsewhere in the same codebase, so this is adopting an existing internal pattern rather than introducing a new cryptographic dependency (GAP-08, INV-SELF-03, ADR-KG3-03).
- String-built Gremlin in the JanusGraph and HugeGraph adapters parameterised immediately, with the regex-only agent firewall supplemented — not replaced — by routing every backend call through the query-IR compiler (§5, ADR-KG3-12) so that no hand-built script reaches a backend regardless of what the firewall catches or misses (GAP-05, INV-SELF-08, ADR-KG3-08).
- MCP authentication moved from one shared bearer token, under which every caller acts as the same principal, to a per-user OAuth 2.1 resource server mapped onto the existing RBAC/ABAC role model, closing both the confused-deputy risk and MCP's inherited share of the ACL gap in one move (GAP-09, INV-SELF-04, ADR-KG3-04).

Two P1 items share this plane without being forced P0s: authentication/SSO hardening (CAP-44, already strong at HEAD — argon2id password hashing, signed expiring sessions, per-principal API tokens, deny-by-default route-role policy, BL-19) is extended with Keycloak/OIDC certification rather than rebuilt; and audit-log tamper-evidence (CAP-48, GAP-20) adds hash-chaining to the existing audit event stream, whose tamper-resistance is currently unverified rather than proven absent.
**Gap closed:** GAP-02, GAP-05, GAP-08, GAP-09 — four of the platform's eleven forced P0s.

### 3.5 Tenancy plane
**Change vs. HEAD:** `tenancy/layers.py` already enforces real, tested isolation for embedded vector/search/SQLite/secrets/caches/logs/backups/exports (BL-20, "Partial (improved)" at HEAD — this is genuine work, not a placeholder) and the API layer wraps non-system-tenant graph access in a named-graph store (`apps/api/main.py:680`, `NamedGraphStore`). What is missing, and what this plane adds, is tenant awareness **inside** the graph adapters themselves — a grep across `graph/hugegraph.py`, `graph/neo4j.py`, `graph/neptune.py`, `graph/memory.py`, `graph/store.py`, `graph/rdf_backend.py` and `adapters/janusgraph.py` finds zero occurrences of `tenant` (GAP-03, confirmed by code reading, not a hypothesis). This matters because the embedded-layer isolation that already exists protects the retrieval index, the cache and the vector store — but the graph itself, which is where the actual knowledge lives, currently has no backend-level tenant boundary at all; a bug anywhere in the API-layer `NamedGraphStore` wrapper (the only thing standing between a query and cross-tenant graph data today) is a full cross-tenant leak with nothing underneath to catch it. The fix is per-backend, chosen by the existing `IsolationPlacement` contract (SILO/BRIDGE/POOL) rather than inventing a new placement model: HugeGraph graph spaces for distributed deployments, Neo4j multi-database for Community or Enterprise, Neptune cluster-per-tenant since Neptune has no sub-cluster multi-tenancy primitive of its own. FalkorDB's graph-per-tenant key (STR-falkordb-02) and Weaviate's shard-per-tenant lifecycle states — active/inactive/offloaded (STR-weaviate-01) — are the adopted patterns for what a tenant's lifecycle state should look like once the backend-level boundary exists, extended to be backend-neutral rather than tied to one engine.
**Gap closed:** GAP-03.

### 3.6 How the five planes interact under the mandatory acceptance journeys

The planes above are not independent subsystems; Master Prompt §14's acceptance journeys are precisely the cases where two or more planes must agree. J5 (permission-aware GraphRAG) requires the security plane's ACL pre-filter (§3.4) to run before the evidence plane's citation assembly (§3.3) selects spans to quote — a citation correctly sourced from an inaccessible document is still a leak, so the ordering is not incidental. J2 (evolving organisational truth — Confluence and ServiceNow disagree about an owning team) requires the evidence plane's persisted-claims model (§3.3, GAP-15 fix) to coexist with the control plane's bitemporal reads (BL-37) so that "preserve both claims, validity time, evidence, the resolution decision" is answerable as an as-of query rather than requiring a human to remember which source said what. J8 (predictions without fact contamination) requires the epistemic-planes mandatory stage (§2, GAP-07) to be enforced by the same mutation gateway that the control plane (§3.2) uses for every other write, so a prediction cannot reach the graph through a path that skips the gateway's typed-constraint check. J13 (multi-tenant isolation) is the tenancy plane (§3.5) directly, and is the one journey this architecture cannot yet claim passes today — it names exactly the gap (GAP-03) that plane exists to close.

## 4. The multi-backend layer

The `GraphStore` protocol (BL-01) and its factory/registry (`graph/backends.py`) are kept as the integration point; this architecture does not replace them. Three things change:

1. **Named adapter defects get fixed, not just documented.** Research identified concrete, code-read defects, not hypotheses: the JanusGraph adapter writes `p_`-prefixed property keys but reads them back unprefixed, which will silently break non-canonical-ID lookups (`adapters/janusgraph.py`, INV-SELF-05); the Neptune adapter has no SigV4/IAM signing path at all (confirmed negatively at HEAD — U-03 resolved negative, `01a-BASELINE-DELTA-HEAD.md` BL-04) and filters edge labels *after* applying `LIMIT`, which silently truncates results; the HugeGraph adapter forces a Groovy closure that will not run against a gremlin-lang-only backend under TinkerPop's 4.0 direction (C12-tinkerpop INV-tinkerpop-02). All three are near-term, scoped patches — option (1) on INV-SELF-05 — independent of the query-IR work.
2. **A conformance suite becomes a release gate, not a design artifact.** `graph/conformance.py` exists (BL-07, Partial) but has never run against live engines (U-01). This architecture makes BM-01 — the same read/write/traversal workload against live HugeGraph, Neo4j, Neptune and JanusGraph containers — a CI gate before any backend-facing release, per INV-SELF-05 option (2).
3. **The long-term fix is structural, not a patch list.** The typed query-IR compiler (§5, ADR-KG3-12) removes an entire class of per-backend string-building defects by construction, because no adapter builds a query by string interpolation once QueryPlan→AST→dialect is the only path. The near-term patches above are necessary because the structural fix is L-effort (8–12 weeks, CAP-20) and the defects are live risks today.

Backend support is not uniform and this architecture does not pretend otherwise: HugeGraph and Neo4j CE support the air-gap tier; Neptune does not and is excluded from it (§6); RDF (Fuseki/GraphDB) is an optional interoperability sidecar (CAP-02, INTEGRATE, P2), not a primary store, because its LPG-shaped API over SPARQL has unmeasured semantic loss (BL-06).

**Per-backend capability table.** Per §4.3.3's requirement to state, for every capability, whether it is backend-native, emulated, or unavailable, the following summarises the matrix's backend-support column for the capabilities this architecture changes or depends on most:

| Capability | HugeGraph | Neo4j | Neptune | JanusGraph | Fuseki/GraphDB |
|---|---|---|---|---|---|
| CRUD + neighbourhood (CAP-01) | native | native | native (cloud) | native | n/a (SPARQL-shaped) |
| Typed constraint layer (CAP-08, GAP-12) | emulated (gateway) | emulated (gateway); Neo4j constraints exist but are EE-gated for some forms | emulated (gateway); schemaless natively | emulated (gateway) | emulated (gateway) |
| Tenant isolation unit (CAP-47, GAP-03) | native (graph spaces, distributed) | native (multi-database) | native (cluster-per-tenant — costliest unit) | emulated (gateway predicate) | emulated (named graph) |
| SHACL validation (CAP-10) | unavailable natively | partial (n10s plugin) | unavailable natively | unavailable natively | native (GraphDB), native via Jena/pySHACL (Fuseki) |
| SPARQL (CAP-15) | unavailable | unavailable (n10s maps a subset) | native | unavailable | native |
| OWL reasoning (CAP-09/23) | unavailable | partial (n10s) | unavailable | unavailable | GraphDB OWL-RL native; Jena via ELK sidecar |
| Air-gap tier eligibility (CAP-50) | yes | yes (CE) | **no — AWS-managed, excluded by construction** | yes | yes |

This table is deliberately conservative: several rows (e.g., Neptune's tenant-isolation unit, JanusGraph's gateway-predicate isolation) describe the *target* design from §3.5, not a capability proven live today — U-01 (live adapter behaviour unexercised) and U-05 (physical tenant isolation untested on any backend) remain open uncertainties in `01a-BASELINE-DELTA-HEAD.md`, and this architecture's BM-01/BM-05 benchmarks (ADR-KG3-05, ADR-KG3-02) exist specifically to close them before any "native" claim in this table is treated as verified rather than designed.

## 5. Interfaces

- **QueryPlan → AST → {gremlin-lang, openCypher, SPARQL}.** `contracts/query_plan.py` (BL-08) is the caller-facing contract today and stays so. `query/ast_compiler.py` (BL-09) already compiles typed filter/match/projection/order nodes with variable-length paths to Cypher, Gremlin and SPARQL text — the architecture's change is making this the *only* path a query reaches a backend through, retiring the regex-based `moonshot/universal_transpiler.py` and the hand-built scripts in the JanusGraph/HugeGraph adapters. This is ADR-KG3-12, the structural decision the rest of the backend layer depends on (GAP-04).
- **VectorPort.** A backend-neutral interface over the current in-memory HNSW/hashing-embedder default (BL-14) with adapters for LanceDB (embedded default per STR-lancedb-01), Qdrant, pgvector and OpenSearch (STR-opensearch-01, STR-pgvector-01) selectable per deployment; BGE-M3 (MIT, local) replaces the hashing embedder as the default encoder (STR-emb-01). ACL-aware filtering happens inside this port, not bolted on after (CAP-53, GAP-46).
- **AuthzPort / SecretsPort.** `authz/core.py` and `authz/pdp.py` (BL-19) are kept as the policy evaluator; this architecture's change is making every surface — retrieval, MCP, export, UI — call through one `AuthzPort` rather than each surface re-implementing its own filtering (STR-sourcegraph-02: "permissions enforced across every feature" via a single port). Secrets stay in the existing per-tenant AES-256-GCM vault (`tenancy/layers.py`), extended to replace the egress vault's XOR cipher (GAP-08).
- **ModelPort.** `models/port.py` (NB-10) already abstracts model providers; Ollama (pinned, outdated, root, unauthenticated — GAP-36) is joined by llama.cpp as a lighter CPU-only alternative (STR-llcpp-01) behind the same port, so a deployment can choose either without an application-code change.
- **ER port.** A new seam, not a HEAD capability: EOIP's own identity resolver (BL-34, person-only, deterministic) and the in-house Fellegi–Sunter reimplementation misleadingly named "Splink" (BL-36, which does not call the real Splink library) sit behind an ER port alongside an actual Splink (MIT) integration (CAP-31, GAP-13) for probabilistic cross-system matching, so a deployment without the Splink dependency still gets the deterministic + in-house fallback.
- **AlgoPort.** Pure-Python graph algorithms (BL-43) and the new SciPy-CSR runtime (NB-01) sit behind a port with rustworkx (Apache-2.0, 2.4 MB wheel, STR-rustworkx-01) as the fast-path engine over tenant-filtered snapshots (CAP-62, GAP-37) — never over the live unfiltered graph, so algorithm results cannot leak across the tenant boundary this architecture otherwise enforces. NetworkX is kept as a correctness test oracle for the rustworkx port's outputs (REUSE, not a production dependency, avoiding igraph's GPL-2.0 and Raphtory's GPL-3.0 licensing under GAP-19's allow-list).

Each port above is deliberately an *interface* decision, not an implementation mandate: a deployment that cannot or will not add the rustworkx/LanceDB/Splink dependency still runs on the pure-Python/hashing-embedder/in-house-ER fallback behind the same port, with a documented capability difference rather than a hard failure. This is what makes the ports compatible with the air-gap tier (§6) — every optional dependency named in this section is exactly that, optional, per §4.3.7 ("RDF/OWL/SPARQL/SHACL services, vector indexes, event buses, graph OLAP, and GNN stacks are optional modules, adopted only on demonstrated value"). The acceptance criterion for promoting any of these from "available" to "default" is the same across all five ports: a passing BM-ID result, not an architectural preference. VectorPort's LanceDB default is the one exception already justified by STR-lancedb-01's own evidence (embedded, no service process, persistent ANN+full-text+hybrid) rather than deferred to a future benchmark, because the capability it replaces — the hashing embedder — is not a real embedding at all (confirmed at HEAD: `RealSemanticProvider` in `retrieval/hybrid_vector_service.py:129` generates vectors from a SHA-256 hash of `model:text:i`, not from a model) and therefore has no retrieval-quality floor worth preserving as a comparison baseline.

## 6. Deployment tiers

- **One-node, air-gapped.** HugeGraph (RocksDB standalone) or Neo4j CE, local models only (Ollama with a current, non-root, authenticated pin — GAP-36, ADR-KG3-10 — or llama.cpp as a dependency-free CPU alternative, STR-llcpp-01), no external vector database required (VectorPort defaults to LanceDB embedded, STR-lancedb-01), pinned images with an SBOM (GAP-44, CAP-79) and a licence allow-list check in the build pipeline (GAP-19, ADR-KG3-11) so no image in the air-gap bundle silently carries a blocked licence. **Neptune is excluded from this tier by construction** — it is AWS-managed and cannot run without AWS connectivity (CAP-50, GAP-21 evidence: "Neptune cloud-only"). This is the default shipped tier per §4.3.10 (one-node first) and §4.3.1 (no mandatory cloud), and is the tier every acceptance journey in Master Prompt §14 must pass on, since J16 (air-gapped operation) is itself one of the sixteen mandatory journeys. One-node sizing profiles are not yet measured (GAP-30, CAP-04): this architecture does not claim a specific node count/RAM/disk figure until BM-02 and BM-19 produce one, and treats "publish measured one-node profiles" as a release gate for this tier's documentation, not an assumption baked into the architecture.
- **One-node, cloud-connected.** Same single-node topology, with Neptune available as a backend choice and external LLM endpoints usable only under explicit, auditable egress policy (BL-45, S0-default-none egress gateway, per-endpoint contract-term amendment, kill switch) — never as a default, and never for a deployment that has not explicitly opted in per §4.3.2. Any customer choosing this tier still gets the same ACL/tenant/epistemic guarantees from §3; cloud connectivity changes which backend and which model endpoint are reachable, not which security guarantees apply.
- **Distributed.** Explicitly deferred (CAP-05, DEFER). HugeGraph's own PD/Store distribution and Neo4j Enterprise clustering exist upstream and are not reimplemented by this platform; building a competing distribution layer before any customer has outgrown the one-node tier would be exactly the "premature distribution" risk the capability matrix names for CAP-05. This tier is demand-gated on BM-02 evidence at 10M+ nodes, matching GAP-30's sibling decision not to build scale-out speculatively, and remains a documented non-goal (§8) rather than a committed roadmap item until that evidence exists.

**Backup, restore and release gates common to all tiers.** Backup/restore scripts exist (`scripts/backup.py`, `scripts/restore.py`, `recovery/wal.py`, BL-50, Implemented but live-unverified) and restore drills have never actually been run (GAP-42, P1) — this architecture treats a successful, evidence-preserving restore drill (CAP-74, BM-16) as a release gate for every tier, not an optional operational nicety, because a backup nobody has restored from is not a backup, it is an unverified assumption. Supply-chain integrity (SBOM generation, signing, scanner pinning — GAP-44, CAP-79) and the evaluation harness (GAP-43, ADR-KG3-07) are the other two cross-tier release gates: no tier ships a release that has not passed BM-01 (backend conformance), BM-04/BM-05 (ACL/tenant leakage), and the SBOM/licence check together, regardless of which backend or connectivity mode that release targets.

## 7. Mapping of the 18 architecture hypotheses

Every hypothesis from Master Prompt §11 is listed. "Decision" reproduces the CAP-matrix/self-inversion decision already made; this document does not re-decide any of them.

| # | Hypothesis | Decision | Justifying IDs | Section above |
|---|---|---|---|---|
| 1 | Multi-backend graph abstraction | **INTEGRATE** (keep multi-backend, fix adapters) **+ BUILD** (typed query IR, the structural follow-on) | CAP-01, CAP-20, GAP-01, GAP-04, GAP-05, STR-tinkerpop-01, INV-SELF-05/08 | §2 (GraphStore+IR box), §4, §5 (ADR-KG3-12) |
| 2 | Semantic fabric (RDF/OWL/SHACL sidecar) | **INTEGRATE** (optional module), SHACL **REUSE** (pySHACL as oracle) | CAP-02, CAP-09, CAP-10, CAP-15, GAP-24, GAP-23, GAP-11, STR-pyshacl-01 | §4 (RDF sidecar note), §2 (mutation gateway SHACL gate) |
| 3 | Enterprise digital thread and graph-of-graphs | **BUILD** | CAP-69, CAP-38, CAP-35, GAP-40, GAP-17 | §3.2, §3.3 |
| 4 | Evidence-first assertion graph | **BUILD** | CAP-38, CAP-39, CAP-25, CAP-43, GAP-15, GAP-07 | §3.3, §2 (epistemic planes box) |
| 5 | Wisdom graph and context-graph layer | **EXPERIMENT** | CAP-80, GAP-45, STR-pm-01 | §8 (non-goal for this release; library-only at HEAD, BL-56) |
| 6 | Ontology-as-code lifecycle | **BUILD** | CAP-41, CAP-35, CAP-37, GAP-17, GAP-18, STR-edg-01, STR-robot-01 | §3.2 |
| 7 | Automatic schema/ER inference from arbitrary JSON | **BUILD** | CAP-28, GAP-14, STR-si-01 | §2 (ingest pipeline stage 6) |
| 8 | Identity plane | **BUILD** (deterministic keys, all entity types) **+ INTEGRATE** (probabilistic ER via Splink) | CAP-30, CAP-31, GAP-13, STR-sf-01, STR-zingg-01, STR-llmem-01 | §2 (ingest pipeline stage 4), §5 (ER port) |
| 9 | Incremental living graph | **BUILD** (chaos/reliability tests) **+ EXPERIMENT** (external event bus) | CAP-27, CAP-06, CAP-36, GAP-31 | §2 (ingest pipeline stage 1), §3.1 |
| 10 | Adaptive retrieval and NL query | **BUILD** (NL→typed-plan, grounded answers) **+ INTEGRATE** (vector/hybrid search) | CAP-53, CAP-55, CAP-58, CAP-60, GAP-46, GAP-35, STR-n4gr-02, STR-t2q-01 | §2 (retrieval stack box), §5 (VectorPort) |
| 11 | Neuro-symbolic inference | **EXPERIMENT** (Datalog materialisation, GNN link prediction) **+ REUSE** (ELK for OWL EL profile) | CAP-22, CAP-23, CAP-63, CAP-64, GAP-22, GAP-23, GAP-38 | §2 (retrieval-stack EXPERIMENT branches), §8 |
| 12 | Temporal graph learning | **EXPERIMENT** | CAP-65, GAP-38 (shared research-gap status with #11) | §8 |
| 13 | Policy-aware agent workbench | **BUILD** | CAP-59, CAP-57, CAP-49, GAP-09, GAP-34, GAP-05, INV-SELF-04/08/09 | §2 (agent/MCP surface box), §3.4 |
| 14 | Multi-tenant, white-label platform | **BUILD** | CAP-47, CAP-52, CAP-44, GAP-03, GAP-19, INV-SELF-02/11 | §3.5, §1 principle 2 and 6 |
| 15 | Multi-scale UI | **BUILD (measure first)** for large-graph rendering; **DEFER** for real-time co-editing | CAP-70, CAP-71, CAP-72, CAP-73, GAP-41 | §2 (UI box) |
| 16 | Interoperable export and backup | **BUILD** (restore drills) **+ INTEGRATE** (OpenLineage opt-in, R2RML/RML) | CAP-74, CAP-40, CAP-29, GAP-42, GAP-29, GAP-27 | §3.2 (dry-run migration) |
| 17 | Reliability and supply chain | **BUILD** | CAP-27, CAP-78, CAP-79, CAP-50, CAP-77, GAP-43, GAP-44, GAP-21, GAP-19, INV-SELF-07/10/11 | §1 principles 5–6, §6 |
| 18 | Customer use cases (J1–J16, incl. non-IT) | **BUILD**, validated through the acceptance journeys, not a separate component | CAP-66..69, CAP-46, CAP-28, CAP-80 (HR/finance/legal via J15) | Composed across §2–§6; see note below |

Hypothesis 18 has no dedicated box because it is a validation requirement, not an architectural layer: J1 (change impact) exercises the code-graph and digital-thread capabilities (§3.3, §2 retrieval stack); J5 (permission-aware GraphRAG) and J13 (multi-tenant isolation) exercise §3.4–3.5 directly; J16 (air-gapped operation) exercises §6; J15 (non-IT, e.g. HR/finance/legal) exercises the same evidence and governance guarantees as the IT journeys, with no IT-specific architecture — the connectors differ (§2 source adapters), the planes do not.

## 8. What this architecture does NOT do

Per Master Prompt §13's instruction to reject features whose complexity outweighs value, and matching the DEFER/REJECT decisions already recorded in `06-MASTER-CAPABILITY-MATRIX.md`:

- **No distributed scale-out in this release** (CAP-05, DEFER). HugeGraph/Neo4j EE's own clustering is used if and when BM-02 shows single-node limits are actually hit; this architecture does not build a competing distribution layer.
- **No multi-model/document storage engine** (CAP-03, DEFER) — raw capture stays on the filesystem per ADR-004 in the pre-existing ADR set; adding a document database is assessed as unnecessary complexity.
- **No SQL/PGQ or GraphQL server as a first-class surface** (CAP-16/CAP-17, DEFER). Library-only adapters exist (BL-58/59) from the prior delta but mounting them is deferred pending demand evidence; a governed query gateway, if ever mounted, must sit behind the same QueryPlan policy as every other surface, not bypass it.
- **No incremental Datalog/rule materialisation as a shipped feature** (CAP-22, EXPERIMENT only) — this is explicitly research-tier pending correctness proof of incremental maintenance.
- **No GNN/link-prediction promotion to facts without human approval** (CAP-64, EXPERIMENT, J8) — predictions live in the isolated prediction plane only; "checkbox ML" that cannot beat a tabular baseline is rejected by design, not merely untested.
- **No bundling of AGPL/SSPL/BSL components** (Zingg, FalkorDB, Vault, Grafana, Elasticsearch, Airbyte, Redpanda, TruffleHog, PM4Py, igraph, Raphtory, several OWL reasoners) under the current licence allow-list (GAP-19) — these appear in the research as *reference* implementations or test oracles only (e.g., XTDB and Splink's design patterns are adopted; their GPL-family cousins such as Zingg's exact code are not shipped).
- **No library consolidation (Sigma vs. Cytoscape) before measurement.** The prior placeholder pass recommended deprecating Cytoscape for Sigma citing an unsupported "60 FPS on 100,000+ nodes" figure; no independent benchmark for either library at that scale exists in this research. This architecture explicitly keeps both renderers until BM-13 produces a real number (CAP-70, GAP-41, "BUILD (measure)" not "BUILD (migrate)").
- **No GraphRAG community/diffusion layer as a default retrieval path** (CAP-56, EXPERIMENT) until BM-06 shows it beats strong non-graph baselines — per Master Prompt §5.3's explicit correction and the uncommitted status of `rag/dual_level_diffusion.py` at HEAD.
- **No "living AI worker" / autonomous agent loop** (CAP-80, part of hypothesis 5). `wisdom/*` modules are real but library-only and unmounted (BL-56); no autonomous-agent supervisor beyond a 41-line stub exists. This is out of scope for the current architecture pending a defined, bounded use case.
- **No claim of air-gap superiority over on-prem competitors** (per the seed-inversion verdict on Palantir: its on-prem/air-gap posture is independently documented and real). This architecture competes on one-node footprint, white-label/OEM packaging, open formats and backend neutrality — not on being the only on-prem option.
