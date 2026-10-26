# C17 — Tier C records (V31)

Access date for all records: 2026-10-26. Prices are list prices seen that day and change often.

### T-C17-atlas-research — "Atlas" research-mapping product (identity unresolved)

| Field | Value |
|---|---|
| Official URL | https://www.atlasworkspace.ai/ (leading candidate) |
| Owner | AgentScale AI Pte. Ltd. (footer); founder Jet New |
| Latest version | rolling SaaS, no version; beta/Pro $20/mo or $204/yr per search snippet |
| Status | active (UNVERIFIED depth) |
| Licence + class | proprietary SaaS |
| Deployment / air-gap | SaaS; hosting not stated; air-gap no |
| Tier reason | ambiguous name |

Candidates found: (1) Atlas Workspace, "visual and verifiable AI research workspace" with research maps and cited answers [CLAIM-atlas-01]; (2) Atlas of Human-AI Interaction, MIT Media Lab, academic extraction of [cause, relationship, effect] triplets (2,037 findings, arXiv 2509.25499 per snippet); (3) Atlas of Progress, a literature-synthesis nonprofit project (Manifund); (4) Nomic Atlas, an embedding data-map platform (unrelated to citation mapping). Apache Atlas is the C06 metadata catalog. The registry text ("research-mapping") most likely means candidate (1) but this is an assumption; all four are recorded. Touches CAP-60, CAP-38, CAP-70.

**Decision:** REFERENCE-ONLY (claim-to-source tracing UX idea).

| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| atlas-01 | Atlas Workspace: AgentScale AI Pte. Ltd., research maps | Official | https://www.atlasworkspace.ai/about (2026-10-26) | 0.6 |
| atlas-02 | Other "Atlas" research projects exist (MIT Media Lab, Atlas of Progress, Nomic) | Search results | https://www.media.mit.edu/projects/atlas-of-human-ai-interaction/overview/ | 0.5 |

### T-C17-researchrabbit — ResearchRabbit

| Field | Value |
|---|---|
| Official URL | https://www.researchrabbit.ai/ |
| Owner | Litmap Limited (acquired May 2025 per secondary sources) |
| Latest version | rolling SaaS |
| Status | active |
| Licence + class | proprietary SaaS; free tier, paid "RR+" (price conflicting, about $10/mo) |
| Deployment / air-gap | SaaS; no |
| Tier reason | literature mapping |

Visual literature-discovery tool: start from seed papers, iteratively explore citations, references and co-authors; site claims 320M+ papers, data sources unnamed [CLAIM-rr-01]. Relevant as UX reference for exploratory citation navigation; no import/export licence for graph data verified. CAP-70, CAP-71, CAP-38.

**Decision:** REFERENCE-ONLY.

| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| rr-01 | Footer Litmap Limited; 320M+ papers claim | Official | https://www.researchrabbit.ai/ | 0.7 |
| rr-02 | Acquired by Litmaps May 2025 | Third-party | https://www.toolsforhumans.ai/ai-tools/research-rabbit | 0.5 |

### T-C17-connected-papers — Connected Papers

| Field | Value |
|---|---|
| Official URL | https://www.connectedpapers.com/ |
| Owner | NOT PUBLICLY VERIFIED this run |
| Latest version | rolling SaaS |
| Status | active (UNVERIFIED) |
| Licence + class | proprietary; free tier limited graphs (5/month per aggregator), paid about $6/mo billed annually (aggregators disagree) |
| Deployment / air-gap | SaaS; no |
| Tier reason | literature mapping |

Builds a similarity graph around one origin paper (co-citation and bibliographic-coupling style similarity; mechanism from general knowledge, UNVERIFIED here). Useful reference for "related by shared citations" ranking and a one-shot graph view. Data licence and upstream source (reported to be Semantic Scholar) UNVERIFIED. CAP-70, CAP-19.

**Decision:** REFERENCE-ONLY.

| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| cp-01 | Free 5 graphs/month; about $6/mo paid | Third-party | https://tooliverse.ai/compare/connected-papers-vs-researchrabbit | 0.3 |

### T-C17-semantic-scholar — Semantic Scholar

| Field | Value |
|---|---|
| Official URL | https://www.semanticscholar.org/product/api |
| Owner | Ai2 (Allen Institute for AI) |
| Latest version | Academic Graph API (rolling) |
| Status | active |
| Licence + class | free API under a separate API License Agreement (terms not read) ; proprietary terms, class source-available/UNVERIFIED |
| Deployment / air-gap | datasets downloadable (S2AG, S2ORC) so offline use partial; API cloud |
| Tier reason | scholarly graph |

REST Academic Graph (papers, authors, citations, venues, SPECTER2 embeddings), Recommendations and Datasets APIs; about 214M papers, 2.49B citations, 79M authors; key gives 1 req/s introductory limit [CLAIM-s2-01]. Alternative/complement to OpenAlex with embeddings and recommendations, but licence must be read before redistribution (legal-review trigger). CAP-26, CAP-53, CAP-38.

**Decision:** INTEGRATE on demand as secondary source after licence review; OpenAlex preferred.

| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| s2-01 | Corpus size, API services, rate limits, Ai2 | Official | https://www.semanticscholar.org/product/api (2026-10-26) | 0.8 |

### T-C17-litmaps-inciteful — Litmaps and Inciteful

| Field | Value |
|---|---|
| Official URL | https://www.litmaps.com/ ; https://inciteful.xyz/ (redirects to incitefulmed.com/academic/) |
| Owner | Litmap Limited (NZ) ; Inciteful: independent, reportedly launched 2020 (secondary, UNVERIFIED) |
| Latest version | rolling SaaS |
| Status | both active |
| Licence + class | Litmaps proprietary (Free; Pro about $10/mo per aggregators); Inciteful free to use, code licence UNVERIFIED |
| Deployment / air-gap | web; no |
| Tier reason | citation mapping |

Litmaps: seed-based citation maps with monthly alerts and Zotero sync on Pro. Inciteful: graph from seed paper, ranks by PageRank-style importance and similarity; data from OpenAlex, Semantic Scholar and Crossref (secondary) [CLAIM-lit-01]. Reference for alerts on new related work and PageRank-style paper ranking over a citation graph. CAP-19, CAP-62, CAP-70.

**Decision:** REFERENCE-ONLY.

| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| lit-01 | Litmaps free plus Pro $10/mo; Inciteful data sources and ranking | Third-party | https://www.casrai.org/guides/litmaps ; https://library.hkust.edu.hk/sc/inciteful/ | 0.4 |

### T-C17-elicit-consensus — Elicit and Consensus

| Field | Value |
|---|---|
| Official URL | https://elicit.com/ ; https://consensus.app/ |
| Owner | UNVERIFIED for both |
| Latest version | rolling SaaS |
| Status | both active |
| Licence + class | proprietary SaaS. Elicit: Basic free, Pro $49/user/mo, Scale $229, Enterprise custom with SSO and API; Consensus: free plus paid tiers, prices conflicting |
| Deployment / air-gap | SaaS (Elicit Enterprise mentions "custom deployments", unspecified); no |
| Tier reason | AI research assistants |

Elicit: search over "more than 138 million papers", structured extraction into tables, systematic-review screening (5,000 papers on Pro), API on Pro [CLAIM-el-01]. Consensus: claims 5M+ users and 200M+ papers; ask a question, get evidence-based answers from papers (feature details not verified). Both ground answers in cited papers: reference for CAP-60 (citation-grounded answers, abstention) and extraction-to-table (CAP-32). Neither self-hostable.

**Decision:** REFERENCE-ONLY (benchmark targets for grounded-answer UX).

| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| el-01 | Elicit plan table | Official | https://elicit.com/pricing (2026-10-26) | 0.8 |
| el-02 | Consensus 5M users; pricing page lists Individual, Team, Enterprise | Official | https://consensus.app/pricing/ | 0.6 |

### T-C17-pkm-tools — Logseq, Tana, Roam Research, Heptabase

| Field | Value |
|---|---|
| Official URL | https://github.com/logseq/logseq ; https://tana.inc ; https://roamresearch.com ; https://heptabase.com |
| Owner | Logseq, Tana, Roam owners UNVERIFIED; Hepta Platforms, Inc. |
| Latest version | Logseq 2.0.1 beta 2026-07-13 (secondary); others rolling SaaS |
| Status | all active |
| Licence + class | Logseq AGPL-3.0 (network-copyleft, legal-review trigger); Tana, Roam, Heptabase proprietary SaaS |
| Deployment / air-gap | Logseq local-first (file graphs; DB version beta, data-loss warning), air-gap yes; Tana, Roam web SaaS, no; Heptabase desktop/mobile apps, offline UNVERIFIED |
| Tier reason | PKM references |

Logseq: outliner with block references; DB version in beta with read-only Markdown mirror (secondary) [CLAIM-pkm-01]. Tana: typed nodes via supertags; Pro $20 early bird/$30, Business $35 with SAML, MCP support [CLAIM-pkm-02]. Roam: block-level backlinks; Pro $15/mo or $165/yr, Believer $500 five-year (secondary). Heptabase: whiteboard cards; $8.99/$17.99/$53.99 per month, owner Hepta Platforms [CLAIM-pkm-03]. References for typed-node authoring (supertags ~ ontology labels, CAP-08, CAP-71) and block references (CAP-38). Do not embed Logseq (AGPL).

**Decision:** REFERENCE-ONLY; possible EXPERIMENT exporting EOIP typed nodes to Logseq/Tana-style structures.

| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| pkm-01 | Logseq AGPL-3.0; DB version beta; 45.4k stars | Official repo | https://github.com/logseq/logseq | 0.8 |
| pkm-02 | Tana plans and MCP | Official | https://tana.inc/pricing | 0.8 |
| pkm-03 | Heptabase plans, Hepta Platforms | Official | https://heptabase.com/pricing | 0.8 |
