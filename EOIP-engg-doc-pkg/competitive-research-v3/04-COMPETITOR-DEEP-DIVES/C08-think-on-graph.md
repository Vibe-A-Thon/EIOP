# C08 Think-on-Graph (ToG)

| Field | Value |
|---|---|
| Registry ID | T-C08-think-on-graph |
| Tier | B (LLM-guided KG exploration; method) |
| Versions examined | arXiv:2307.07697 v6 (2024-03-24, ICLR 2024); `IDEA-FinAI/ToG` HEAD (2024-03-24) |
| Verified on | 2026-10-26 |
| Worker | V20 |

## 1. Identity, status, sources
"Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph", Sun, Xu, Tang, Wang, Lin, Gong, Ni, Shum, Guo; ICLR 2024 [CLAIM-tog-01]. Code: `IDEA-FinAI/ToG` (README: original repo at GasolSun36/ToG); last commit 2024-03-24; **no LICENSE file found at repo root** (licence UNVERIFIED, treat as all-rights-reserved for redistribution) [CLAIM-tog-02]. A follow-up ToG-2 repository (GasolSun36/ToG-2) returned "not found" on 2026-10-26. Research code, dormant.

## 2. Problem and workloads
KGQA with hallucination reduction: the LLM acts as an agent that beam-searches a KG (Freebase, Wikidata), iteratively choosing relations and entities, then reasons over the explored paths; training-free and "plug-and-play" across LLMs (authors' claim) [CLAIM-tog-01].

## 3. Feature inventory
| Feature | Status |
|---|---|
| Iterative beam search: relation pruning, entity pruning, reasoning check | present (repo `ToG/main_freebase.py`, `main_wiki.py`, `prompt_list.py`) [CLAIM-tog-02] |
| Freebase (SPARQL server) and Wikidata API environments | present |
| Evaluation scripts, CoT baselines | present |
| Property-graph support, Cypher/Gremlin | absent |
| ACL, tenancy, provenance output | paths returned as triples; no ACL |
| Packaging as library/service | absent |

## 4. Architecture
```
question -> LLM extracts topic entities -> loop depth D (beam width N):
   expand relations (KG API) -> LLM scores/prunes relations
   expand entities along kept relations -> LLM scores/prunes entities
   LLM: "enough to answer?" yes -> answer from paths ; no -> continue
```

## 5. Under-the-hood reconstruction
Exploration is LLM-driven pruning with a fixed beam and depth cap (paper; files above). Cost per question = depth x beam x (relation-score + entity-score calls) (hypothesis from structure). Access to the KG is via SPARQL/API for each hop, so latency is dominated by LLM calls, not the store. Returned reasoning paths are explicit triples, which is the "responsible/traceable" claim. Exact hyperparameters (width 3, depth 3 default) recalled, 0.5.

## 6. Requirements inferred
A KG neighbourhood API (relations of entity, tails by relation); path scoring; step budget; trace persisted with the answer.

## 7. Performance
Authors report overall SOTA on 6 of 9 datasets, training-free; small models can outperform GPT-4 in certain scenarios [CLAIM-tog-01]. Datasets are Freebase/Wikidata KGQA benchmarks, not enterprise graphs; no latency/cost table seen in the abstract. Many LLM calls per question; local 7-14B models are expected to be weaker at relation scoring (hypothesis). No comparison with strong non-graph RAG by the authors (Master Prompt 5.3).

## 8. Strengths
Typed neighbourhood expansion with auditable triple paths; no pre-built index; works on live KGs (freshness). Directly relevant to the J-journeys needing multi-hop impact analysis with evidence.

## 9. Limitations
Algorithmic: greedy beam can prune the right path; LLM scoring noise. Operational: 2 x D x N LLM calls per question; slow and costly. Friction: research code, no licence file, SPARQL/Freebase-specific. Safety: LLM sees raw neighbour labels, so ACL must be applied inside the neighbour API (BL-18).

## 10. Deployment and licensing
Licence **not found**: legal-review trigger before any code reuse; concept/algorithm reimplementation from the paper is the safe path pending review (record only). Air-gap viable with local LLM and local KG (0.6).

## 11. Delta vs EOIP baseline
EOIP has typed, bounded query plans (BL-08) and `GraphStore` neighbourhood (BL-01); an LLM-guided expansion would sit as a *planner* proposing bounded hops, never emitting queries. No agent loop on retrieval today (BL-48 Partial).

## 12. Cards
| ID | Card |
|---|---|
| STR-tog-01 | LLM-guided pruned multi-hop expansion with explicit path trace; CLAIM-tog-01; value: explainable multi-hop answers over fresh graph; **match** as bounded "guided traversal" tool; design: LLM picks among permitted relation types returned by an ACL-filtered `neighbourhood()`; hop/beam/token budgets in policy; acceptance: path trace stored with evidence IDs, no inaccessible entity ever shown to the LLM |
| INV-tog-01 | High LLM-call cost and greedy pruning (hypothesis from structure). Alternatives: (1) run ToG as-is [licence], (2) hybrid: deterministic PPR/BFS candidate generation, LLM only to rerank top relations (selected), (3) differentiated: learned relation scorer from query logs. POC: multi-hop set on EOIP code/ticket graph; success: equal accuracy at <=30% LLM calls. Decision **EXPERIMENT**. No seed hypothesis targets ToG. |

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-19 multi-hop exploration | EXPERIMENT (bounded LLM-guided traversal) |
| CAP-24 explanation traces | REUSE idea: persist path trace |
| Code | REJECT (no licence) |

## 14. Tests
Multi-hop questions with gold paths; measure path precision, LLM calls, latency on local model; ACL canary entities.

## 15. Risks and questions
Does local model quality suffice? Path explosion at supernodes (CAP-07); licence status.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | ICLR 2024; no licence |
| D2 | 2 | KGQA |
| D3 | 4 | agent loop |
| D4-D5,D7-D8,D11-D12 | N/A | no storage of its own |
| D6 | 5 | per-hop KG API |
| D9 | N/A | no ingest |
| D10 | 12 | triple paths |
| D13 | 2,5 | guided retrieval |
| D14 | 11 | adjacent: uses SPARQL APIs not NL-to-query |
| D15-D17 | 3 | research code |
| D18-D19 | 9 | none |
| D20 | 7 | call cost |
| D21 | 10 | unlicensed |
| D22 | 3 | Freebase/Wikidata only |
| D23 | N/A | none verified |
| D24 | 7 | author results |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-19 | native (LLM-guided) | tog-01 | BL-08 templates | EXPERIMENT | P2 |
| CAP-24 | partial | tog-01 | BL-48 Partial | REUSE idea | P2 |
| CAP-46 | absent | tog-02 | BL-18 Absent | BUILD | P0 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates/conf | Contradiction |
|---|---|---|---|---|---|---|
| tog-01 | arXiv:2307.07697 v6 | training-free; SOTA on 6 of 9 datasets; plug-and-play across LLMs; ICLR 2024 | Peer-reviewed | arxiv.org/abs/2307.07697 | 2023-07-15, rev 2024-03-24; acc 2026-10-26; 0.85 | rap-03 (GraphRAG may underperform RAG) |
| tog-02 | IDEA-FinAI/ToG HEAD 2024-03-24 | Files main_freebase.py, main_wiki.py, prompt_list.py; no LICENSE at root; ToG-2 repo not found | Observed in source | github.com/IDEA-FinAI/ToG | acc 2026-10-26; 0.85 | none |

## Appendix D. Assumptions
Beam/depth defaults and cost formula are reasoned inference. Licence absence means "not found at root", not "none exists".
