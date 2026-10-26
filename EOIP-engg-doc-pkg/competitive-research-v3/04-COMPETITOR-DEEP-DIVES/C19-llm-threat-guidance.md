# C19 — OWASP Top 10 for LLM Applications, OWASP agentic-AI guidance, MITRE ATLAS

| Field | Value |
|---|---|
| Registry ID | T-C19-llm-threat-guidance |
| Tier | B (threat-model references; not software) |
| Versions examined | OWASP LLM Top 10 **2025** (official page); OWASP Top 10 for Agentic Applications 2026 (published 2025-12-09); MITRE ATLAS (release naming conflicts, see 1) |
| Verified on | 2026-10-26 |
| Worker | V11 |

## 1. Identity, status, sources
| Member | Owner | Licence | Status |
|---|---|---|---|
| OWASP Top 10 for LLM Applications | OWASP GenAI Security Project | UNVERIFIED (OWASP content is typically CC BY-SA; 0.5) | Official page lists the **2025** edition as current [CLAIM-lt-01]. Secondary sources claim a **2026 edition released 2026-08-04** with different ordering (Excessive Agency moved to #3, "Hidden Context Exposure" replacing System Prompt Leakage) - NOT confirmed on the official page, confidence 0.3 [CLAIM-lt-02] |
| OWASP Top 10 for Agentic Applications (ASI) | OWASP GenAI Security Project, Agentic Security Initiative | UNVERIFIED | Official resource page dated 2025-12-09; the ten entries were not retrievable from that page. Secondary sources name goal hijacking, tool misuse, privilege abuse, memory poisoning, rogue agents [CLAIM-lt-03] |
| MITRE ATLAS | MITRE | data licence UNVERIFIED | Active. Secondary: v5.1.0 (Nov 2025, 16 tactics/84 techniques); v5.4.0 (Feb 2026, agent-focused additions); Speakeasy reports "v2026.09" (2026-09-15; 16 tactics, 120 techniques, 88 sub-techniques, 40 mitigations, 73 case studies). Official site fetch returned no version data [CLAIM-lt-04] |
Resolution: use the verified 2025 LLM list as baseline; re-check official 2026 claim before citing a 2026 list. Name collision: "OWASP Top 10" (web) is unrelated.

## 2. Problem and workflows
Shared vocabulary for threat modelling EOIP's LLM, retrieval, MCP and agent surfaces; used for security requirements, red-team plans and acceptance tests. Workflow: map each threat to a control and a test in CI.

## 3. Feature inventory (what the references provide)
| Reference | Provides | Absent |
|---|---|---|
| LLM Top 10 2025 | ten risk categories: LLM01 Prompt Injection, 02 Sensitive Information Disclosure, 03 Supply Chain, 04 Data and Model Poisoning, 05 Improper Output Handling, 06 Excessive Agency, 07 System Prompt Leakage, 08 Vector and Embedding Weaknesses, 09 Misinformation, 10 Unbounded Consumption [CLAIM-lt-01] | test suite, controls code |
| Agentic Top 10 | agent-specific risks list [CLAIM-lt-03] | detail unverified |
| ATLAS | tactic/technique matrix, mitigations, case studies, agentic tags (secondary) [CLAIM-lt-04] | licence verified |

## 4. Architecture of use
```
Threat reference --> EOIP threat model (per surface: ingest, retrieval, MCP, agents, egress)
        --> control (code/policy) --> automated test (red-team corpus) --> release gate
```

## 5. Reconstruction: mapping to EOIP surfaces (inference, hypotheses marked)
| Threat | EOIP surface | Existing control (code observed) | Gap |
|---|---|---|---|
| LLM01 prompt injection / ATLAS agent injection | GraphRAG context | `retrieval/service.py` synthesis via GraphRAGPipeline with fenced context, cited-span claim-support check (commit c264c07) | no indirect-injection test corpus from connectors found |
| LLM02 sensitive disclosure | egress | `egress/gateway.py`, `dlp.py`, tokenisation vault, manifest (BL-45) | vault cipher is XOR keystream (see C19-vault-openbao) |
| LLM03 supply chain | build | none found | see C19-supply-chain |
| LLM06 excessive agency / ASI tool misuse, privilege abuse | `apps/mcp`, agents (BL-47/48) | write tools absent by design (ADR-007); governed tools | single static bearer token (INV-mcp-02); no per-user scopes |
| LLM08 vector and embedding weaknesses | vector/hybrid retrieval | tenant-limited indexes (commit df724e4); `DerivationACLEvaluator` on graph contexts | per-document source-ACL enforcement at lexical/vector stage not confirmed (BL-18 re-audit); embedding inversion untested |
| LLM04 poisoning / ASI memory poisoning | ingestion, truth store | PROPOSED-until-validated boundary (BL-40), validation gate (BL-28) | adversarial-document tests absent |
| LLM09 misinformation | answers | claim-support check removes unsupported claims | no hallucination-rate benchmark |
| LLM10 unbounded consumption | queries/LLM | CRA-024.9 query budgets (commit 099eb38) | LLM token budgets per tenant: UNVERIFIED |
| LLM05 improper output handling | UI/API | UNVERIFIED | |

## 6. Requirements inferred
REQ-SEC: every surface has a mapped threat ID and test; MCP tools carry per-principal authorisation; retrieval gates ACL before generation; agents cannot write graph without governed action.

## 7. Performance and resource model
N/A (documents). Effort: one threat-model workshop plus a red-team test harness; no vendor numbers.

## 8. Strengths
Authoritative shared taxonomy customers' auditors recognise; agentic list targets EOIP's MCP/agent roadmap; ATLAS adds adversary behaviours and case studies. Match: already aligned on several controls (fenced context, claim support, budgets).

## 9. Limitations
| Class | Item |
|---|---|
| Verified | edition churn: 2025 list official, 2026 claims unconfirmed; ATLAS version naming inconsistent across sources |
| Intentional | lists describe risks, not tests or conformance levels |
| Friction | overlapping categories; secondary summaries disagree |
| Licensing | reference licences UNVERIFIED; do not copy text into product docs without checking |

## 10. Deployment, licensing, viability
Documentation only; air-gap trivial (store a pinned copy once licence verified). No redistribution of text until licence confirmed.

## 11. Delta vs EOIP baseline
No BL covers threat-model traceability; BL-45, BL-47, BL-48, BL-28, BL-40 hold controls; BL-18 and MCP identity are the open P0 findings (C09-mcp INV-mcp-02; C07-onyx STR-onyx-01; C10-opensearch STR-opensearch-01). EOIP has no red-team corpus, so CAP-49 is partial.

## 12. Cards
**STR-lt-01** | OWASP LLM08 + ASI | vector/embedding and memory risks named | CLAIM-lt-01,03 | justifies ACL-before-retrieval as release gate | match | requirement "ACL filter precedes ranking and generation", test J5 | zero forbidden chunks across 3 retrieval modes.
**STR-lt-02** | ATLAS | adversary-behaviour matrix | CLAIM-lt-04 | red-team scenario library | integrate | tag EOIP tests with ATLAS technique IDs | each in-scope technique has a test or documented risk acceptance.
**INV-lt-01** (edition ambiguity, verified conflict) | cite versions explicitly; pin to 2025 until official 2026 page confirmed. Decision ADOPT process.
**INV-lt-02** (no executable conformance, intentional) | build `security/redteam` corpus: injected connector documents, cross-tenant probes, tool-abuse prompts. Benchmark: attack success rate before/after fenced context, target hypothesis <1%. Decision EXPERIMENT. Failure case: tests leak real data - use synthetic fixtures.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-49 injection defence | BUILD red-team harness; REFERENCE lists |
| CAP-46 vector weaknesses | map to BL-18 work (INTEGRATE ReBAC) |
| Threat traceability | BUILD (matrix in docs) |
| Copying lists verbatim | DEFER pending licence |

## 14. Tests
Indirect-injection corpus through each connector; cross-tenant retrieval probe; MCP tool-abuse suite; token-budget exhaustion; poisoning test against validation gate.

## 15. Risks
Chasing unstable 2026 edition; false assurance from checklist coverage; ATLAS licence unknown.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | owners, versions, conflicts |
| D13 | 5 | LLM/RAG/agent threats |
| D18 | 5,11 | trust and security mapping |
| D15 | 12 | governance process |
| D21 | 1,10 | licence unverified |
| D23 | N/A | no patents involved |
| D24 | App C | secondary-source conflicts |
| D2,D3 | 2,4 | usage |
| D4-D12,D14,D16,D17,D19,D20,D22 | N/A | documents, not systems |

## Appendix B — Capabilities
| CAP | Reference coverage | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-49 | native | 01,04 | BL-45/28/40 partial | BUILD | P1 |
| CAP-46 | named risk | 01 | BL-18 re-audit | INTEGRATE | P0 |
| CAP-51 | named risk (LLM02) | 01 | BL-45 Implemented | REUSE | P2 |
| CAP-59 | ASI | 03 | BL-47 | BUILD per-user scopes | P0 |

## Appendix C — Evidence
| CLAIM | product | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-lt-01 | OWASP LLM Top 10 2025 | ten entries LLM01-LLM10 as listed; page shows 2025 as current | Officially documented | https://genai.owasp.org/llm-top-10/ | page footer 2025 / 2026-10-26 | 0.85 | secondary 2026 claim |
| CLAIM-lt-02 | OWASP LLM Top 10 "2026" | released 2026-08-04, re-ordered list | Third-party report | https://www.superblocks.com/blog/owasp-llm-top-10 ; https://www.akamai.com/blog/ai/2026/aug/owasp-top-10-llm-applications-2026-realistic-security-model | 2026-08 / 2026-10-26 | 0.3 (not on official page) | CLAIM-lt-01 |
| CLAIM-lt-03 | OWASP Agentic Top 10 | published 2025-12-09; entries not on fetched page | Officially documented (date) / third-party (entries) | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | 2025-12-09 / 2026-10-26 | 0.7 date, 0.4 entries | none |
| CLAIM-lt-04 | MITRE ATLAS | v5.1.0 84 techniques (Nov 2025); "v2026.09" 120 techniques | Third-party report | https://www.speakeasy.com/blog/mitre-atlas-explained ; https://vectra.ai/topics/mitre-atlas | 2026-09 / 2026-10-26 | 0.4 | official site gave no data |

## Appendix D — Assumptions
2025 list treated as authoritative; ATLAS and 2026 OWASP figures marked low confidence; EOIP code observations from working tree HEAD 896e06d.
