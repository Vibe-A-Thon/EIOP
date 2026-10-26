| Field | Value |
|---|---|
| Registry ID | T-C09-guardrails |
| Tier | B (agent safety layer; maps directly onto EOIP egress and agent firewall) |
| Versions examined | NeMo Guardrails 0.24.1 (2026-09-16); Llama Guard 4 12B (Llama 4 Community License effective 2025-04-05); Llama Prompt Guard 2 86M |
| Verified on | 2026-10-26 |
| Worker | V22 |

## 1. Identity, current status, tier, sources

| Member | Owner | Version | Licence | Notes |
|---|---|---|---|---|
| NeMo Guardrails | NVIDIA (repo now `NVIDIA-NeMo/Guardrails`) | 0.24.1, 2026-09-16 [CLAIM-grd-01] | **Apache-2.0**; Python 3.10-3.13 [CLAIM-grd-02] | programmable rails; five rail types input, dialog, retrieval, execution, output; Colang 1.0 default and 2.0 supported [CLAIM-grd-02] |
| Llama Guard 4 | Meta | 12B parameters, text and images | **Llama 4 Community License** (effective 2025-04-05); gated on Hugging Face (name, birth date, organisation) [CLAIM-grd-03] | safe/unsafe label plus violated categories |
| Llama Prompt Guard 2 | Meta | 86M backbone (listed 0.3B), 8 languages | Llama 4 Community License, gated [CLAIM-grd-04] | classifies prompts benign/malicious for injection and jailbreak |
| Prompt-injection defences (patterns) | n/a | n/a | n/a | spotlighting/delimiting, dual-LLM, privilege separation, output filtering: described from general knowledge, no source read this run (UNVERIFIED) |

Licence mechanics for the Llama licence (per a third-party copy of the Llama 4 text on Wind River's licence list, secondary source): redistributors must supply a copy of the agreement and display "Built with Llama"; the acceptable-use policy is incorporated by reference; a 700M-monthly-active-user commercial threshold is reported by a secondary summary only [CLAIM-grd-05]. Whether Llama Guard 4 shares exactly those terms was confirmed only by the model card licence tag. Status: all active; NeMo 0.x.

## 2. Problem, workloads, workflows

Problem: constrain what goes into and out of an LLM and what tools it may call. EOIP workflows: (1) untrusted source text entering agent context (injection via a Confluence page); (2) model output checked before showing to a user (unsupported claims, leaks); (3) tool calls validated against allowlists. EOIP controls today: `KnowledgeFirewall` (`packages/eoip/agents/firewall.py`) with regex secret/PII/restricted/injection patterns and GAP-KFW-001..008; `EgressGateway` (`packages/eoip/egress/gateway.py`) with kill switch, policy matrix, DLP, canary registry, vault, per-call manifest, default S0.

## 3. Feature inventory

| Feature | NeMo Guardrails | Llama Guard 4 | Prompt Guard 2 |
|---|---|---|---|
| Input / output moderation | present (self-check flows) [CLAIM-grd-02] | present (classifier) | input only |
| Jailbreak and injection detection | present (library flow) [CLAIM-grd-02] | partial | present |
| Retrieval and execution (tool) rails | present [CLAIM-grd-02] | absent | absent |
| Fact/hallucination checks | present (LLM self-check) [CLAIM-grd-02] | absent | absent |
| Dialog flow DSL (Colang) | present | absent | absent |
| Runs fully local | yes if a local LLM is configured (inference) | yes (12B, needs significant CPU/GPU) | yes (small) |
| Multimodal | not examined | text + images | text |
| Tenant policy, ACL awareness | absent | absent | absent |
| Llama Guard integration in NeMo | not stated in README read | n/a | n/a |

## 4. Architecture

```
 user/source text -> [input rails] -> LLM -> [output rails] -> answer
                       |  retrieval rails on RAG chunks;  execution rails on tool calls
 rails = Colang flows + actions; checks call an LLM (self-check) or a classifier (Llama Guard / Prompt Guard)
 EOIP: firewall (pre-context) + egress gateway (pre-model) + claim-support check (post-model, CRA-026)
```

## 5. Under-the-hood reconstruction

NeMo wraps an LLM in an orchestrating runtime that matches user intent to Colang flows and executes configured rails around each generation [CLAIM-grd-02]; self-check rails are themselves LLM prompts, so their quality tracks the checker model (inference). Classifier models (Llama Guard, Prompt Guard) are fine-tuned LLMs/encoders emitting labels. No source read at pinned tag; internals beyond README are hypotheses.

## 6. Requirements inferred

Guard decisions must be deterministic-first (regex/allowlists), model-assisted second; every block has a reason (GAP-KFW-008); guard model runs locally under S0; results logged into the egress manifest; false-positive budget measured; fail closed for tool execution, fail open-with-flag for read-only display (policy choice).

## 7. Performance and resource model

Each LLM-based rail adds a model call (latency and cost multiply); a 12B guard on CPU is expensive (inference, not measured). Prompt Guard 2 at 86M backbone is CPU-feasible. Adaptive prompt-injection attacks can defeat classifiers (general literature, not cited here): treat as defence in depth, not a guarantee.

## 8. Strengths

NeMo: a policy-as-config model with rails at five points including retrieval and tool execution, Apache-2.0. Llama Guard/Prompt Guard: purpose-trained small safety classifiers usable locally. Match: pluggable `Classifier` stage in the firewall. Exceed: ACL- and tenant-aware guards that know source trust level and permissions, which none of these have.

## 9. Limitations

Algorithmic: classifier recall on novel injections unknown; LLM self-checks are non-deterministic. Operational: extra latency; Llama 12B footprint. Licensing: Llama licence is not OSI open source (branding, AUP, MAU threshold, gated access) and weights cannot be silently bundled; legal review. Friction: Colang learning curve (1.0 vs 2.0 split); NeMo's LangChain optionality. Product gap: none address graph-specific attacks (poisoned nodes, relation injection).

## 10. Deployment, licensing, viability

NeMo Guardrails Apache-2.0: embeddable, redistributable. Llama Guard/Prompt Guard: customer downloads under Meta's licence (gated), EOIP documents the procedure, does not bundle (consistent with ADR-H15 weight rule). Air-gap viable with local checker models. Legal triggers: Llama licence terms; any LLM-judge model's own licence.

## 11. Competitive delta vs EOIP baseline

EOIP has regex-based injection and DLP controls (BL-45, BL-48 firewall) and egress gateway; no learned classifier, no retrieval/tool rails DSL, no guard evaluation set. Absent: source-ACL enforcement (BL-18), which is a larger risk than injection.

## 12. Cards

STR-grd-01 | NeMo Guardrails | rails at input, retrieval, execution, output points as configuration | CLAIM-grd-02 | consistent policy placement across agent steps | match | map firewall hooks to the same five points with typed decisions; no hard dependency | red-team suite of 200 injection payloads: block rate and false-positive rate recorded vs regex baseline.
STR-grd-02 | Prompt Guard 2 | small local injection classifier | CLAIM-grd-04 | CPU-feasible learned detection | integrate (customer-supplied weights) | optional `InjectionClassifier` plugin under firewall, label to `RuleDecision` | detection uplift over regex on the suite with measured latency.
INV-grd-01 | KnowledgeFirewall regex patterns (EOIP self-inversion) | pattern list is brittle (proven by reading file) | root cause algorithm, proven | layered: regex first, classifier second, structural isolation (untrusted spans never become instructions, GAP-KFW-004); worse if classifier latency unacceptable | options: (1) keep regex; (2) plug-in classifier; (3) provenance-aware isolation with taint tracking | select 2 now, 3 differentiator | POC: taint-tracked agent run where injected instruction cannot trigger a tool | defensibility: tie to graph provenance (BL-41) | decision EXPERIMENT.
INV-grd-02 | Llama licence family | non-OSI, gated (proven) | root cause licensing, proven | document-and-customer-download plus Apache-2.0 alternatives | options: (1) skip; (2) customer-supplied; (3) in-house trained classifier | select 2 | POC: plugin works with weights path configured, absent by default | defensibility: low | decision ADOPT (customer-supplied).

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-49 injection defence, deterministic layer | BUILD (extend firewall) |
| CAP-49 learned classifier | INTEGRATE (Prompt Guard 2, customer-supplied) / EXPERIMENT |
| Rails DSL (Colang) as dependency | DEFER; adopt placement pattern |
| NeMo Guardrails as optional adapter | EXPERIMENT |
| Llama Guard output moderation | EXPERIMENT |
| CAP-51 egress control | REUSE existing gateway |
| CAP-60 grounded answers | REUSE CRA-026 claim-support check |

## 14. Tests

Red-team corpus incl. indirect injection in documents, graph-property injection, tool-argument injection; measure block and false-positive rates; fail-closed test for tool rail; verify no guard call leaves the perimeter under S0; latency on CPU reference hardware.

## 15. Risks and open questions

Llama licence reading and Llama Guard 4 vs earlier versions' licences; NeMo's Llama Guard support unverified; Colang 2.0 stability; classifier robustness to adaptive attacks; no verified third-party benchmark collected.

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Versions, licences |
| D2 | 2 | Agent safety workflows |
| D3 | 4 | Rail points |
| D4-D7 | N/A | none |
| D8 | N/A | none |
| D9 | N/A | none |
| D10 | 11 | Provenance link |
| D11-D12 | N/A | none |
| D13 | 2, 3 | Retrieval/execution rails |
| D14 | N/A | query safety not examined |
| D15-D16 | N/A | none |
| D17 | 3 | Colang |
| D18 | all | Core topic |
| D19 | 3, 8 | Tenant-aware guards absent |
| D20 | 7 | No numbers |
| D21 | 1, 10 | Licences |
| D22 | N/A | none |
| D23 | N/A | none found |
| D24 | App. C | README + model cards; no benchmarks |

## Appendix B. Capability mapping

| CAP-ID | This technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-49 | native/partial | grd-02,04 | BL-48 Partial | BUILD + EXPERIMENT | P1 |
| CAP-51 | absent | grd-02 | BL-45 Implemented | REUSE | P1 |
| CAP-60 | partial | grd-02 | CRA-026 (commit c264c07) | REUSE | P2 |
| CAP-46 | absent | grd-02 | BL-18 Absent | BUILD | P0 |
| CAP-33 | partial | grd-02 | BL-46 | REUSE | P2 |

## Appendix C. Evidence records

| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-grd-01 | NeMo Guardrails 0.24.1 | released 2026-09-16 | Officially documented | https://github.com/NVIDIA-NeMo/Guardrails/releases/latest | 2026-09-16 / 2026-10-26 | 0.9 | none |
| CLAIM-grd-02 | NeMo README | Apache-2.0; five rail types; Colang 1.0/2.0; jailbreak/self-check flows; Python 3.10-3.13 | Officially documented | https://raw.githubusercontent.com/NVIDIA-NeMo/Guardrails/develop/README.md | undated / 2026-10-26 | 0.85 | none |
| CLAIM-grd-03 | Llama Guard 4 12B | Llama 4 Community License, gated, text+image, 12B | Officially documented | https://huggingface.co/meta-llama/Llama-Guard-4-12B | undated / 2026-10-26 | 0.85 | none |
| CLAIM-grd-04 | Llama Prompt Guard 2 86M | Llama 4 licence, gated, benign/malicious classifier, 8 languages | Officially documented | https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M | undated / 2026-10-26 | 0.85 | none |
| CLAIM-grd-05 | Llama 4 Community License text (third-party copy) | copy of agreement, "Built with Llama", AUP incorporated; 700M MAU per secondary summary | Third-party report | https://open.windriver.com/info/uni-license-list/licenses/llama-4-cla-2025.html | 2025-04-05 / 2026-10-26 | 0.6 | read Meta's own text |

## Appendix D. Assumptions

EOIP code characterisation read directly from `agents/firewall.py` and `egress/gateway.py` headers. Prompt-injection design patterns are named without citations and marked UNVERIFIED. Llama Guard 4 licence = Llama 4 Community License per model card tag.
