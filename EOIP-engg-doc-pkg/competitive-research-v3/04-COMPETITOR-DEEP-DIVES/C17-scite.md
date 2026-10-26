# C17 — scite

| Field | Value |
|---|---|
| Registry ID | T-C17-scite |
| Tier | B (supporting vs contrasting citation classification; reference for contradiction tracking) |
| Versions examined | SaaS, rolling; pricing page updated 2026-10-19; Nicholson et al. 2021 paper |
| Verified on | 2026-10-26 (brief said 2026-10-18; actual access date used) |
| Worker | V31 |

## 1. Identity, status, sources
scite (scite.ai) is a commercial "smart citation" index: for each citation it shows the citing sentence and classifies it as supporting, contrasting or mentioning, using a deep-learning model [CLAIM-scite-01]. Operator and ownership details UNVERIFIED this run. Active (pricing page dated 2026-10-19) [CLAIM-scite-02]. Proprietary SaaS; not self-hostable as far as verified.

## 2. Problem and workflows
Plain citation counts hide whether a citing paper agrees or disputes. Workflows: open a Smart Citation Report for a paper; read citing statements; set citation alerts; ask the Assistant (answers grounded on cited papers); Pro users call an API; paid users use MCP connectors (Claude, ChatGPT) [CLAIM-scite-02].

## 3. Feature inventory
| Feature | Status |
|---|---|
| Smart Citation Reports (supporting/contrasting/mentioning with context) | present (all paid plans) [CLAIM-scite-02] |
| Full-text search, Assistant, alerts | present [CLAIM-scite-02] |
| API | Pro and above [CLAIM-scite-02] |
| MCP access | paid / trial / Enterprise [CLAIM-scite-02] |
| Private collections, SAML SSO | Team / Enterprise [CLAIM-scite-02] |
| Self-hosted / air-gapped | absent / NOT PUBLICLY VERIFIED |
| Open-licensed data export | NOT PUBLICLY VERIFIED |

## 4. Architecture (hypothesis from paper abstract)
```
 publisher full text (agreements) -> reference-string extraction -> citation-statement segmentation
   -> classifier (supporting | contrasting | mentioning) -> index -> UI / API / MCP / Assistant (LLM, cited)
```
Hypothesis: pipeline stages inferred from the paper title/abstract; code not public.

## 5. Under the hood
Per the 2021 paper, a deep-learning model assigns one of three labels to each citation statement; reported scale over 25M full-text articles and 880M+ classified statements (developer claims) [CLAIM-scite-01]. Reported per-class accuracy (secondary library review): about 97% mentioning, 64% supporting, 59% contrasting [CLAIM-scite-03]. Model family (SciBERT) is a secondary claim, UNVERIFIED. Training data: manually annotated snippets (interview, secondary).

## 6. Requirements inferred for EOIP
A contradiction/support edge must carry: stance label, confidence, evidence span (sentence plus offsets), citing and cited IDs, model/version, human override. Three labels are insufficient for enterprise claims (add "qualifies", "retracts", "supersedes" as options; hypothesis).

## 7. Performance and resource model
No latency or throughput benchmarks verified. The meaningful number is classifier quality: contrasting-class accuracy about 59% is vendor-adjacent evidence that stance detection is noisy, so EOIP must keep human review and never auto-resolve on it.

## 8. Strengths
Evidence-span-first design (the sentence is the proof); stance beyond counts; alerts when a claim is contested; integrations through MCP/API.

## 9. Limitations
| Class | Item |
|---|---|
| Verified | Basic plan has no API; Pro $50/mo or $480/yr; Enterprise custom [CLAIM-scite-02] |
| Quality | Weak recall/precision on supporting and contrasting classes per secondary review [CLAIM-scite-03] |
| Intentional | Coverage depends on full-text access agreements (hypothesis) |
| Licensing | Proprietary; data reuse/redistribution terms NOT PUBLICLY VERIFIED; cloud only |

## 10. Deployment, licensing, viability
SaaS only; egress to a third party conflicts with default-local EOIP unless the customer opts in via the egress gateway (BL-45). Air-gap: no. Legal review trigger: proprietary data, ToS on caching citation statements.

## 11. Delta vs baseline
EOIP `TruthStore` (BL-39) detects contradictions among claims about one subject/predicate but not stance between documents; evidence manifests (BL-41) hold spans. No document-to-document stance classification found in the inspected baseline (UNKNOWN beyond BL-39/BL-41). The CAP-39 / BL-39 mapping holds.

## 12. Cards
STR-scite-01 | scite | stance-labelled citation with evidence sentence | CLAIM-01,03 | customers see why a source supports or disputes a claim | match | `Stance` claim type: (src_span, tgt_entity, label, confidence, model_id, reviewer); feeds TruthStore as contradicting/supporting claims | on a 200-sentence gold set, contrasting-class F1 reported with confidence intervals, human override audited.
INV-scite-01 | target scite SaaS 2026 | black-box 3-class labels, ~59-64% class accuracy; root cause: algorithm/semantics (reported, not reproduced) | alternative: local NLI model + rule cues with abstention and reviewer queue; worse where throughput matters. Options: quick = call scite API when allowed; native = local NLI classifier behind PROPOSED-until-promoted boundary (BL-40); long = domain-tuned stance model with active learning. Select native. POC: gold set of 500 enterprise sentence pairs, metric macro-F1 and abstention precision vs LLM baseline. Defensibility: tenant-specific labelled data. Decision EXPERIMENT. No seed hypothesis targets scite.

## 13. Decisions
| Capability | Decision |
|---|---|
| Stance-labelled evidence (CAP-39, CAP-38) | BUILD |
| scite API as optional external signal | INTEGRATE only if tenant opts in (EXPERIMENT) |
| Hosting/using scite data offline | REJECT (not available) |
| Contradiction UX (alerts) | EXPERIMENT |

## 14. Tests
Gold-set stance test; verify unsupported auto-resolution is impossible (stance claims stay PROPOSED); verify egress manifest logs any scite call; verify evidence span round-trips.

## 15. Risks and open questions
Legal status of storing citing sentences; mismatch between scholarly and enterprise stance; low accuracy tempts over-trust; scite API schema unverified.

## Appendix A — Dimension coverage
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1 | commercial SaaS |
| D2 | 2 | citation context |
| D3,D4 | 4 | hypothesis only |
| D5–D8 | N/A | closed |
| D9 | 4 | publisher feeds (hypothesis) |
| D10 | 5,6 | evidence spans, stance |
| D11–D12 | N/A | not offered |
| D13 | 2,3 | Assistant, MCP |
| D14 | N/A | N/A |
| D15 | N/A | N/A |
| D16–D17 | 3 | UI, API |
| D18 | 10 | SAML on Enterprise |
| D19 | 3 | Team/Enterprise seats |
| D20 | 7,9 | pricing |
| D21 | 9,10 | tiers |
| D22 | 10 | export unverified |
| D23 | N/A | not searched |
| D24 | 5,9 | accuracy secondary |

## Appendix B — Capability mapping
| CAP | scite | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-39 | partial (stance across papers) | 01 | BL-39 Implemented | BUILD | P1 |
| CAP-38 | native (evidence sentence) | 01 | BL-41 Implemented | BUILD | P1 |
| CAP-59 | native (MCP) | 02 | BL-47 Implemented | REFERENCE | P3 |
| CAP-60 | partial (cited Assistant) | 02 | BL-16 Implemented | EXPERIMENT | P2 |

## Appendix C — Evidence
| ID | Product/date | Claim | Class | Source | Access | Conf | Contra |
|---|---|---|---|---|---|---|---|
| scite-01 | 2021 paper | smart citation index classifies intent via deep learning: supporting/contrasting/mentioning; 25M+ articles, 880M+ statements | Peer-reviewed (via secondary summary) | https://doi.org/10.1162/qss_a_00146 | 2026-10-26 | 0.6 | not read in full |
| scite-02 | 2026-10-19 | plan table: Basic $20/mo no API; Pro $50/mo, API; Enterprise custom, SAML; MCP paid | Official pricing | https://scite.ai/pricing.md | 2026-10-26 | 0.85 | third-party sites list other prices |
| scite-03 | 2021 | per-class accuracy about 97/64/59% | Third-party (library review) | https://library.hkust.edu.hk/sc/trial-scite/ | 2026-10-26 | 0.4 | not verified against the paper |

## Appendix D — Assumptions
Pipeline stages hypothetical. Stance semantics differ between scholarly citations and enterprise claims. Access date 2026-10-26.
