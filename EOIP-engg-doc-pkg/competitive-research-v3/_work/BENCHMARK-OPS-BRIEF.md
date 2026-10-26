# Benchmark, threat model, and operations brief — read fully before starting

You write `15-VALIDATION-BENCHMARK-PLAN.md`, `16-SECURITY-PRIVACY-THREAT-MODEL.md`, `17-OPERATIONS-SRE-COST-MODEL.md` and one POC experiment folder under `20-POC-EXPERIMENTS/` for the KnowGridFlow/EOIP competitive research package. Repository root: `F:\code\EIP\EIOP`. Package: `EOIP-engg-doc-pkg/competitive-research-v3/`.

## Inputs

1. `KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md` lines 412–427 (§12 benchmark protocol), lines 450–481 (§14 journeys J1–J16, §15 prohibited shortcuts), and §16 item 21 (POC experiments, "run only if authorized and possible" — none are authorized in this run, so every POC in this package is a **specification**, not an execution).
2. `07-GAP-REGISTER.md` — every gap already cites BM-IDs in its Tests column. **Do not invent new BM numbers.** The exact BM-ID → CAP/GAP mapping already established is below; use it as your BM-01..BM-22 definitions and expand each into a full benchmark spec.
3. `08-STRENGTH-ADOPTION-REGISTER.md` and `09-CON-TO-PRO-INVERSION-REGISTER.md` §3 (self-inversion cards — each P0 card already names its own falsifiable benchmark; make sure BM-04, BM-05, BM-08, BM-09, BM-18 etc. match what the self-inversion cards describe).
4. `01-SYSTEM-BASELINE.md` / `01a-BASELINE-DELTA-HEAD.md` for what test infrastructure already exists (`qa_bench/`, `retrieval/eval.py`, `tests/`) — note in §15 that NO full-suite run completed in this research programme (it hung in `tests/unit/test_brain_and_living_system.py` at the baseline date, later resolved per 01a) and note in your plan that the harness itself (BM-22-adjacent, GAP-43) is what this plan specifies into existence.
5. `02-TECHNOLOGY-REGISTRY.md` §3 and the LDBC/benchmark Tier B deep dives (`04-COMPETITOR-DEEP-DIVES/C20-*.md`) for licence/fair-use rules on benchmark publication (TigerGraph Community licence, RDFox evaluation licence, LDBC's "LDBC Benchmark Results" trademark restriction — all already researched, cite them).

BM-ID → CAP/GAP context already established (use exactly these numbers; expand each into hardware/dataset/workload/measure/threshold):

- BM-01 backend conformance (CAP-01,13,14,18-20; GAP-01,04,05,06,19,43)
- BM-02 scale/sizing (CAP-01-07,...,62,70; GAP-01,06,23,24,30-32,37,41)
- BM-03 ingest/CDC chaos (CAP-04-06,25-27,32,34-41; GAP-12,15-17,26,29-31)
- BM-04 ACL/tenant leakage — retrieval (CAP-30-33,38,44-47,53,55-57; GAP-02,10,13,28,33,34)
- BM-05 ACL/tenant leakage — cross-tenant adversarial (CAP-45-47,53,55-57; GAP-02,03,33,34)
- BM-06 retrieval/answer quality incl. GraphRAG-vs-plain-RAG (CAP-09,13,19-24,30-32,38,43,46,47,53-56,58-60; GAP-04,06,09,13,22,23,25,28,33,35,46)
- BM-07 query safety/NL-to-query execution accuracy (CAP-13,14,18-20,46,47,56-58; GAP-04,05,06,33,34,35)
- BM-08 standards conformance — SHACL/W3C suites, OWL, RDF round-trip (CAP-01,02,08-11,13-15,22,23,27-29,41,43,46; GAP-01,05,11,12,14,22-24,27)
- BM-09 entity resolution precision/recall (CAP-28-31,41,47; GAP-13,14,27)
- BM-10 schema-inference / ontology-proposal quality (CAP-20,26-28,41; GAP-14,26)
- BM-11 temporal/bitemporal/contradiction correctness (CAP-08,09,19,20,22-25,32,34,38,39,41,71-73; GAP-06,12,15,16,23)
- BM-12 code-intelligence / digital-thread journeys J1,J9,J10 (CAP-17-20,66-69; GAP-06,39,40)
- BM-13 large-graph rendering (CAP-20,70,71; GAP-41)
- BM-14 local model serving / MCP latency (CAP-46,59-61; GAP-09,36)
- BM-15 epistemic-plane and ML-prediction integrity (CAP-10,20,28,41-43,47,62-64; GAP-07,17,37,38)
- BM-16 backup/restore/DR drills (CAP-74-76; GAP-42)
- BM-17 ontology governance workflow (CAP-08,10-12,20,25,34-37,39-41,70-72; GAP-11,12,15-18,29,41)
- BM-18 security/injection/audit/supply-chain (CAP-13,20,44,46-51,53,57-59,79; GAP-02,03,05,08,09,20,21,34,35)
- BM-19 air-gap install drill (CAP-02-04,13,48-50,79; GAP-05,20,21,24,30)
- BM-20 licence CI gate / white-label packaging (CAP-28,43,50-52,75-79; GAP-08,19,21,43,44)
- BM-21 temporal graph learning / GNN leakage-safe eval (CAP-34,43,63-65; GAP-38)
- BM-22 wisdom/process-intelligence + evaluation-harness meta-test (CAP-38,78-80; GAP-43,44,45)

Note: a prior, non-evidence-based pass on 2026-10-19 wrote placeholder files at these paths with fabricated-looking pass/fail claims. **Overwrite each completely** (Read then Write); every test in your version must be marked **PROPOSED** (never PASSED) per Master Prompt §12 and §15 — nothing in this research programme executed a benchmark.

## What to write

### `15-VALIDATION-BENCHMARK-PLAN.md` (4,000–6,000 words)

1. Intro: reproducibility rules (state hardware, workload generator, dataset licence, query mix, warm-up, cache state, repetitions, variance, configuration, versions — every one, every time; no universal "fastest" claims; regression thresholds and rollback conditions defined per benchmark; everything here is PROPOSED).
2. One subsection per BM-01..BM-22: name, purpose (which GAP/CAP it validates), data tier (100k/1M/10M+ per Master Prompt §12), workload/query mix, backends in scope, measures (cite the Master Prompt §12 measure categories — systems/retrieval/ML/UX — that apply), dataset and its licence (note PROVISIONAL datasets with restrictive licences from the C20 research, e.g. CRAG CC BY-NC-4.0, HotpotQA share-alike — these need legal clearance before use), pass/fail threshold, regression/rollback rule.
3. A chaos/stress matrix (degree skew, bursty CDC, clock skew, duplicate/out-of-order events, partial failure, replay, corrupt checkpoints, permission revocation, offline restart, noisy tenants) mapped to which BM-IDs exercise each.
4. A note that LoCoMo-style memory benchmarks are **contested evidence** (per the GraphRAG/memory cohort finding: internally contradictory vendor numbers, one audit found a judge model accepting 62.81% wrong answers) and must not be used alone to validate BM-06/BM-07 memory claims; use task-completion/citation-accuracy measures instead.
5. Benchmark-publication constraints: TigerGraph Community licence, RDFox evaluation licence and LDBC's "LDBC Benchmark Results" trademark rule all restrict how EOIP may publish comparative numbers — state the rule for each and how this plan complies (e.g. "not LDBC Benchmark Results" labelling).

### `16-SECURITY-PRIVACY-THREAT-MODEL.md` (3,000–5,000 words)

Structure: assets (graph facts, embeddings, agent memory, egress credentials, ontology), trust boundaries (source systems → ingest → graph → retrieval/MCP → agents/UI → customer), actors (end user, agent, admin, attacker-as-tenant, attacker-as-source), and a STRIDE-style or attack-tree pass over the 11 P0 self-inversion cards specifically (`09-CON-TO-PRO-INVERSION-REGISTER.md` §3) plus: query/prompt injection (GAP-05), tool poisoning/confused deputy on MCP (GAP-09), supply-chain compromise (GAP-19/44, citing the 2026 Trivy compromise finding from C19 research), cross-tenant and cross-user leakage (GAP-02/03), egress data exfiltration (GAP-08). For each threat: likelihood/impact (qualitative), existing control (if any, cite BL/NB-ID), proposed control (cite the self-inversion card's selected option), residual risk, detection (observability hook). Cite OWASP Top 10 for LLM Applications and MITRE ATLAS per the C19 research (`C19-llm-threat-guidance.md`) where applicable.

### `17-OPERATIONS-SRE-COST-MODEL.md` (2,500–4,000 words)

Sizing tiers (one-node small/medium/large, per the baseline's A-10 scale assumption of ~10M nodes/~50M edges per tenant), deployment (Docker Compose/Helm per `deploy/`), backup/restore/PITR (BM-16), monitoring (OTel/Prometheus per CAP-75, no bundled Grafana per the AGPL finding), runbooks (what's missing today per GAP-20/42), TCO model inputs (licence costs avoided/incurred per `02-TECHNOLOGY-REGISTRY.md` §3, compute cost per tier, support burden), air-gapped install procedure outline (BM-19) and its known gaps (Neptune excluded from air-gap tier per the baseline).

### One POC under `20-POC-EXPERIMENTS/poc-0X-<slug>/README.md`

Pick the single highest-value POC implied by the P0 gaps — recommend: **poc-02-acl-scoped-retrieval** — a minimal, Docker-first reproducible experiment specification (not executed) proving BM-04/BM-05 is measurable: two synthetic tenants/users with disjoint permissions, a small fact set with ACL principals, a retrieval call, and a pass/fail script outline. Include a `run_poc.py` stub (argument parsing and TODOs only, clearly marked NOT EXECUTED, no fabricated output) mirroring the style of the existing `poc-01-multi-backend-compilation/run_poc.py` if it exists (read it first for style consistency, but do not copy its content check if it's a 2026-10-19 placeholder — read it with a critical eye and only match style, not substance).

## Rules

- Every test is PROPOSED. Never state or imply a benchmark ran in this programme.
- Every BM-ID must match the mapping given above exactly (same number, same GAP/CAP associations); do not renumber.
- Never delete, move or rename files; never run git commands that change state. Write only the four named deliverables (three files + one POC folder with its README and run_poc.py stub).

## Final reply (≤200 words)

Files written, confirmation that BM-01..BM-22 all appear with the given GAP/CAP associations preserved, the POC chosen and why, and any dataset-licence or benchmark-publication restriction you flagged for legal review.
