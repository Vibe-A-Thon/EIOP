# Worker brief — KG competitive research v3 (read fully before starting)

You are one of 35 parallel research workers (W01–W35) executing the Master Prompt v3.0 for **KnowGridFlow / EOIP**, a self-hosted, white-label, multi-tenant, multi-backend enterprise knowledge-graph platform ("living organisation brain"). Today is **2026-10-18 (UTC)**; record this as the access date of everything you verify.

## 1. Read first (in this order)

All paths are relative to the repository root `F:\code\EIP\EIOP`.

1. `KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md` — read **lines 114–192** (§4 baseline, constraints, reference sources and customer questions; §5 traps), **your category paragraph in §6 (lines 193–260)**, **lines 262–383** (§7 the 24 research dimensions, §8 evidence protocol, §9 the 15-heading deep-dive template, §10.3–10.5 strength cards, inversion cards, seed inversion hypotheses) and **lines 450–481** (§14 journeys J1–J16, §15 prohibited shortcuts).
2. `EOIP-engg-doc-pkg/competitive-research-v3/03-RESEARCH-METHODOLOGY.md` — evidence rubric, tiers, ID conventions and the **shared capability taxonomy CAP-01..CAP-80** (§6). You must map findings to CAP-IDs.
3. `EOIP-engg-doc-pkg/competitive-research-v3/01-SYSTEM-BASELINE.md` — the verified EOIP baseline with BL-IDs. Compare against **this**, not against EOIP's requirements documents. Do not re-audit the EOIP code; you may open specific files cited there if a comparison needs it.
4. `EOIP-engg-doc-pkg/competitive-research-v3/_work/registry-seed.txt` — your assigned rows (column 5 = your worker ID). Columns: category | tier | slug | name | worker | tier reason.

Optional prior internal material (lower trust; never cite as evidence for a competitor fact): `competitive-research-analysis.md`, `competitive-research-analysis-agg.md`, `EOIP-engg-doc-pkg/ontology-competitive-analysis.md`, `research/competitive/*.yaml`.

## 2. Hard rules

- **Write only inside** `EOIP-engg-doc-pkg/competitive-research-v3/04-COMPETITOR-DEEP-DIVES/` and `EOIP-engg-doc-pkg/competitive-research-v3/_work/registry-fragments/`. Do not modify any other file. Do not modify production source code. Do not run git commands that change state.
- **Lawful research only**: public documentation, official repositories within licence terms, release notes, specifications, papers, independent benchmarks. No leaked or proprietary material, no bypassing access controls, no copying protected implementation assets.
- **Never fabricate** versions, release dates, licences, benchmark numbers, citations, URLs or features. If you could not verify something, write `UNVERIFIED` or `NOT PUBLICLY VERIFIED` and give confidence ≤ 0.3. Unknowns stay unknown. Vendor performance claims are quoted as vendor claims with workload and hardware context.
- Use the web tools (WebSearch, WebFetch — load them with ToolSearch `select:WebSearch,WebFetch` if they are not already available). Prefer official docs, GitHub releases/tags, licence files, standards bodies, peer-reviewed papers. Verify current version, release date, maintenance/archival status and licence for **every** entry. Budget guide: Tier A 6–15 sources, Tier B 3–6, Tier C 1–3.
- Resolve the traps in Master Prompt §5 that touch your entries (renames, archival, EOL, name collisions, shipped-vs-announced). For ambiguous names, pin the exact project/owner/URL; if several exist, record each candidate and state which one the registry means.
- **Do not ask questions and do not stop early.** Record assumptions inside the deep dive under "Assumptions".
- Respect EOIP constraints when judging fit: air-gap capable, no mandatory cloud, default-local LLMs with egress policy, backend neutrality (HugeGraph, Neo4j, Neptune and others), connectors never mutate the graph directly, permissions and tenant isolation survive everything, one-node first, redistribution-safe licensing (flag GPL/AGPL/SSPL/BSL/Elastic/Commons Clause/community-vs-enterprise splits/patent clauses as legal-review triggers — record, do not give legal conclusions).

## 3. Outputs

### 3.1 Tier A and Tier B — one file per registry entry

Path: `EOIP-engg-doc-pkg/competitive-research-v3/04-COMPETITOR-DEEP-DIVES/<category>-<slug>.md` (e.g. `C01-neo4j.md`).

Front matter table (first lines of the file):

| Field | Value |
|---|---|
| Registry ID | T-<cat>-<slug> |
| Tier | A or B (+ reason) |
| Versions examined | exact versions + dates |
| Verified on | 2026-10-18 |
| Worker | Wxx |

Then **exactly these 15 numbered headings** (Master Prompt §9), in order:

1. Identity, current status, tier, and sources
2. Primary problem, target workloads, concrete example workflows
3. Feature inventory (present / partial / optional / enterprise-only / absent / unknown — across UI, API, CLI, SDK, integrations) — as a table
4. Text-based architecture diagram (boundaries, flows, state, control and data planes) — in a fenced code block
5. Under-the-hood reconstruction (data model; storage layout and indexing; query pipeline and planning; reasoning; concurrency and transactions; partitioning and consistency; caching; versioning; security) — a blueprint to re-implement equivalent behaviour from public evidence; pseudocode only where supportable; mark hypotheses
6. Functional and non-functional requirements inferred from verified behaviour
7. Performance and resource model (methodology, hardware, dataset, scaling behaviour, uncertainty, failure modes) — no fabricated numbers
8. Strengths and use-case-specific advantages — and how each could be matched or exceeded
9. Limitations with root causes — separate verified defects, intentional trade-offs, licensing restrictions, user-reported complaints, outdated claims, hypotheses; organise root causes as algorithmic dead-ends / operational and hardware overhead / user and developer friction
10. Deployment, licensing, redistribution, and operational viability under EOIP constraints
11. Competitive delta against the EOIP verified baseline (cite BL-IDs and CLAIM-IDs)
12. Strength-adoption cards and Con-to-Pro inversion cards
13. Per-capability decisions — BUILD / REUSE / INTEGRATE / EXPERIMENT / DEFER / REJECT — **per capability, not per vendor**
14. Concrete tests, proof-of-concept, and acceptance conditions
15. Risks, trade-offs, and open research questions

Then these appendices:

- **A. Research-dimension coverage** — a table with one row per dimension D1–D24 (Master Prompt §7): `Dimension | Covered in section(s) | Summary or N/A reason`. Every row filled.
- **B. Capability mapping** — table `CAP-ID | This technology (native / partial / plugin / enterprise-only / absent / unknown) | Evidence CLAIM-ID | EOIP baseline (BL-ID + status) | Decision for EOIP (BUILD/REUSE/INTEGRATE/EXPERIMENT/DEFER/REJECT) | Priority hint P0–P3`. Include only CAP-IDs that are relevant.
- **C. Evidence records** — table `CLAIM-ID | product / version / date | exact claim | classification | source title + URL | publication date / access date | confidence + rationale | contradictory evidence`. Every substantive claim in the file links to a CLAIM-ID like `[CLAIM-neo4j-03]`.
- **D. Assumptions** made instead of asking.

**Strength-adoption card format** (one per verified strength relevant to EOIP customers):
`STR-<slug>-NN | competitor | strength | evidence (CLAIM-IDs) | value to EOIP customers | match / exceed / integrate / reject | design approach | acceptance test`

**Inversion card format** (one per material verified drawback) — all fields from Master Prompt §10.4: INV-<slug>-NN; target, version, workload; evidence-supported limitation; root cause (data model / algorithm / coupling / storage / deployment / semantics / governance / UX / licensing / maturity) marked *proven* or *hypothesis*; why an alternative design mitigates it and when the alternative would be worse; three options (quick integration / pragmatic native enhancement / long-term differentiated architecture); selected option with trade-offs, design pattern and a small diagram/pseudocode/API sketch; falsifiable benchmark or POC with dataset, success metric and cost/resource baseline; dependencies, migration, backward compatibility, security and privacy failure cases; defensibility (why value persists if competitors copy it); decision ADOPT / EXPERIMENT / DEFER / REJECT. Validate or reject any seed hypothesis from Master Prompt §10.5 that targets your technology, and say which.

Depth guide (HARD CAPS — usage limits are binding): Tier A ≈ 3,000–6,000 words, never more than ~40 KB, with a real reconstruction in heading 5 (cite source code paths at pinned tags for OSS where you can). Tier B ≈ 1,200–2,500 words, never more than ~18 KB. Write densely: tables over prose, no repetition between headings. Use the Write tool for files (long Bash heredocs fail in this shell). Never pad; never compress a material topic to a generic bullet.

### 3.2 Tier C — one shared file per worker

Path: `EOIP-engg-doc-pkg/competitive-research-v3/04-COMPETITOR-DEEP-DIVES/<category>-tier-c-records-Wxx.md` (if your Tier C rows span several categories, use the first category). One section per entry:

`### T-<cat>-<slug> — <name>` then a table (official URL, owner, latest version + date, status, licence + class, deployment modes, air-gap viable, tier reason) then a **relevance paragraph** (what it is, why it matters or not to EOIP, which CAP-IDs it touches) then **Decision** (BUILD/REUSE/INTEGRATE/EXPERIMENT/DEFER/REJECT/REFERENCE-ONLY + one line) then its evidence records (same CLAIM format).

### 3.3 Registry fragment — machine-readable

Path: `EOIP-engg-doc-pkg/competitive-research-v3/_work/registry-fragments/Wxx.json` — a JSON array, one object per assigned entry plus any ADD/EXCLUDE/DEFER proposals:

```json
{
  "id": "T-C01-neo4j",
  "slug": "neo4j",
  "name": "Neo4j",
  "category": "C01",
  "tier": "A",
  "tier_reason": "…",
  "members": ["Neo4j Community", "Neo4j Enterprise", "GDS", "Bloom", "NeoDash", "Aura"],
  "official_url": "https://…",
  "owner": "…",
  "latest_version": "…",
  "version_date": "YYYY-MM-DD or UNVERIFIED",
  "release_cadence": "…",
  "status": "active | maintenance | archived | end-of-life | renamed | acquired | unknown",
  "license": "exact licence name(s) per edition",
  "license_class": "permissive | weak-copyleft | strong-copyleft | network-copyleft | source-available | proprietary | mixed | n/a",
  "redistribution_notes": "OEM/embedding/SaaS terms in one or two sentences",
  "legal_review_trigger": true,
  "legal_review_reason": "…",
  "community_vs_enterprise": "…",
  "deployment_modes": ["self-hosted", "docker", "kubernetes", "managed-cloud", "embedded", "desktop", "saas"],
  "air_gap_viable": "yes | no | partial | unknown",
  "maturity": "production | early-production | beta | research | historical",
  "resolution_note": "rename / ambiguity / archival resolution, or empty",
  "registry_action": "KEEP | ADD | EXCLUDE | DEFER",
  "action_reason": "one line",
  "decision_summary": "e.g. INTEGRATE as supported backend; REUSE GDS patterns",
  "top_strengths": ["STR-neo4j-01", "…"],
  "top_inversions": ["INV-neo4j-01", "…"],
  "deep_dive_path": "04-COMPETITOR-DEEP-DIVES/C01-neo4j.md",
  "sources": [{"title": "…", "url": "…", "accessed": "2026-10-18"}],
  "verification_confidence": 0.8
}
```

Registry growth rule (Master Prompt §6): you may propose **ADD** entries only if they fill a demonstrable architectural or product gap, are a credible counterexample, or have meaningful adoption — at most 3 per worker, each with a Tier C record. Use **EXCLUDE / DEFER** with a reason for anything assigned that turns out to be a duplicate, non-existent, renamed or out of scope (never silently drop a user-named technology).

## 4. Your final reply to the coordinator (keep it under 400 words)

List: files written (paths), entries completed per tier, any entry you could not complete and why, ADD/EXCLUDE/DEFER proposals, the 3 most important strengths and 3 most important inversions for EOIP (IDs + one line each), and the main verification gaps. Do not paste the deep dives into the reply.
