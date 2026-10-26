| Field | Value |
|---|---|
| Registry ID | T-C09-agent-frameworks |
| Tier | B (orchestration references; EOIP has an in-house governed agent runtime, BL-48) |
| Versions examined | AG2 1.2.1 (2026-10-21); autogen-agentchat 0.7.5 (2025-09-30, archived); Microsoft Agent Framework `agent-framework` 1.23.0 (2026-10-22); semantic-kernel 1.45.0 (2026-10-06); crewai 1.15.30 (2026-10-24); openai-agents 0.24.0 (2026-10-15); claude-agent-sdk 0.2.174 (2026-10-24); google-adk 2.13.0 (2026-10-23); pydantic-ai 2.61.0 (2026-10-24) (all PyPI versions/dates) |
| Verified on | 2026-10-26 |
| Worker | V22 |

## 1. Identity, current status, tier, sources

Grouped file; one identity line per member. LangGraph is covered in `C08-langchain-langgraph` / the placeholder `C09-langgraph-agent-protocols.md` and is not repeated.

| Member | Owner | Version (PyPI date) | Licence (source) | Status |
|---|---|---|---|---|
| AutoGen (microsoft/autogen) | Microsoft | 0.7.5 (2025-09-30) | MIT | **Archived**: README states no bug or security fixes, advises against production use, points to Microsoft Agent Framework [CLAIM-agfw-01] |
| AG2 (ag2ai/ag2) | AG2 community (fork lineage of AutoGen 0.2) | 1.2.1 (2026-10-21) | Apache-2.0 (PyPI) | active; fork lineage per project history, not re-verified |
| Microsoft Agent Framework (MAF) | Microsoft | 1.23.0 (2026-10-22) | MIT (PyPI classifier) | active; .NET, Python, Go; graph workflows, durability, HITL [CLAIM-agfw-02] |
| Semantic Kernel | Microsoft | 1.45.0 (2026-10-06) | MIT (classifier) | active release; relationship to MAF (successor vs coexisting) UNVERIFIED |
| CrewAI | crewAI, Inc. | 1.15.30 (2026-10-24) | MIT-style permission grant in LICENSE, copyright "2025 crewAI, Inc." [CLAIM-agfw-03] | active; commercial platform tier UNVERIFIED |
| OpenAI Agents SDK | OpenAI | 0.24.0 (2026-10-15) | MIT | active, 0.x |
| Claude Agent SDK | Anthropic | 0.2.174 (2026-10-24) | PyPI metadata says MIT; repository LICENSE not read; use of Claude service governed by Anthropic terms (legal-review flag) | active, 0.x |
| Google ADK | Google | 2.13.0 (2026-10-23) | Apache-2.0 (classifier) | active |
| PydanticAI | Pydantic | 2.61.0 (2026-10-24) | MIT | active |

Trap resolved: "AutoGen" now means three things (archived Microsoft repo, AG2 fork, MAF successor). The registry entry is satisfied by recording each [CLAIM-agfw-01].

## 2. Problem, workloads, workflows

These libraries give a loop around an LLM: tool calling, handoffs, multi-agent topologies, memory, tracing. EOIP-relevant workflow: planner agent chooses read-only MCP tools (BL-47), retrieves evidence, drafts a cited answer; humans approve any proposed graph change (BL-40 PROPOSED state).

## 3. Feature inventory (capability level; per-member detail UNVERIFIED beyond the table above)

| Feature | AG2 | MAF | CrewAI | OpenAI SDK | Claude SDK | ADK | PydanticAI |
|---|---|---|---|---|---|---|---|
| Multi-agent orchestration | present | present (sequential, concurrent, handoff, group) [CLAIM-agfw-02] | present | present (handoffs) | unknown | present | partial |
| Durable/restartable workflows, HITL | unknown | present (stated) [CLAIM-agfw-02] | unknown | unknown | unknown | unknown | unknown |
| Typed structured outputs | unknown | unknown | unknown | unknown | unknown | unknown | present (core design; not re-verified) |
| MCP client | unknown for all; widely stated in each project's docs, not verified here | | | | | | |
| Local/OpenAI-compatible model endpoints | unknown | present (provider-flexible, stated) | unknown | unknown | not applicable (Claude models) | unknown | unknown |
| Built-in tenancy, ACL, egress policy | absent | absent | absent | absent | absent | absent | absent |

## 4. Architecture (common pattern)

```
 app -> Agent(loop: model call -> tool call -> result -> model call)
          |-- tools (functions / MCP servers)    |-- handoffs / group chat / graph workflow
          |-- memory + session store             |-- tracing/telemetry exporter
 model provider adapter (hosted API or OpenAI-compatible local endpoint)
```
Control plane is application code; none of the libraries carries a policy plane for data egress (reasoned inference from the absence in the docs examined).

## 5. Under-the-hood reconstruction

Only the shared loop is supportable from public documentation read this run; per-framework internals (state machines, checkpoint stores) were not source-read: UNVERIFIED. MAF's stated graph patterns and durability suggest a checkpointed workflow engine (hypothesis, as in LangGraph).

## 6. Requirements inferred

An EOIP agent needs: tool allowlist with per-principal scopes; every model call through the egress gateway; deterministic replay; evidence-bearing outputs; no direct graph writes. None is delivered by these libraries.

## 7. Performance and resource model

No benchmarks gathered; cost is dominated by model latency. Failure modes: unbounded tool loops, context growth, non-deterministic handoffs. Release cadence of 0.x SDKs (OpenAI 0.24, Claude 0.2) implies API breakage risk (inference).

## 8. Strengths

MAF: enterprise workflow primitives; PydanticAI: typed outputs reduce parsing failures; ADK/OpenAI/Claude SDK: first-party patterns for tool use and handoffs. Match or exceed: adopt typed-output discipline and checkpoint/HITL patterns inside `packages/eoip/agents`.

## 9. Limitations

User/developer friction: churn (AutoGen archived within about a year of wide adoption), vendor gravity (Azure/Foundry for MAF, Gemini/Vertex for ADK, Claude models for Claude SDK). Licensing: Claude Agent SDK needs verification of repository LICENSE vs service terms. Operational: no framework ships tenant isolation or egress control, so adopting one adds a dependency without closing a gap.

## 10. Deployment, licensing, viability

All MIT or Apache-2.0 per metadata: redistribution-friendly, but each pulls large transitive trees (not measured) against the nine-package core (ADR-H15). Air-gap viable only with a local model endpoint. Legal review: Claude Agent SDK terms; CrewAI commercial tier boundaries.

## 11. Competitive delta vs EOIP baseline

EOIP has governed tools, XAI and a `KnowledgeFirewall` (BL-48, `agents/firewall.py`) in-house and Partial. Frameworks offer richer orchestration and tracing; EOIP offers policy. Source-ACL gap (BL-18) and the no-write rule (BL-23/ADR-007) are not provided by any framework.

## 12. Cards

STR-agfw-01 | PydanticAI / MAF | typed outputs and checkpointed HITL workflows | CLAIM-agfw-02 | fewer malformed agent outputs; auditable approvals | match | typed `AgentResult` contract and resumable run state in `contracts/agent.py` | 100 replayed runs reproduce identical decisions.
INV-agfw-01 | target all, versions above | no policy plane (hypothesis from docs) and high churn (AutoGen archived, proven) | root cause maturity/governance, AutoGen archival *proven* | an in-house thin loop with swappable adapters avoids lock-in; worse when team lacks agent expertise | options: (1) wrap one framework behind an `AgentRuntime` protocol; (2) keep native runtime, adopt patterns; (3) pluggable runtime with conformance suite | select 2 now, 3 later | POC: same 20 evidence tasks on native and one framework behind the protocol, equal answers, zero policy bypass | defensibility: policy plane is EOIP's differentiator | decision ADOPT (native + patterns).

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-59 agent tool interface | REUSE MCP; BUILD native runtime |
| Typed outputs (PydanticAI-style) | EXPERIMENT |
| MAF/ADK/CrewAI as embedded dependency | REJECT for core; DEFER as customer-side integrations |
| AutoGen (archived) | REJECT |
| AG2 | DEFER |

## 14. Tests

Dependency footprint measurement (pip install size, transitive licences) per framework; run a tool-allowlist bypass test (agent tries an unlisted tool) against any candidate; egress test that no provider SDK calls bypass the gateway.

## 15. Risks and open questions

Licence of Claude Agent SDK repo; SK vs MAF fate; AG2 governance; per-framework MCP support not verified.

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 | 1 | Identity table per member |
| D2 | 2 | Agent loops |
| D3 | 4 | Common pattern |
| D4 | N/A | No storage focus |
| D5 | N/A | none |
| D6 | N/A | none |
| D7 | N/A | none |
| D8 | 5 | Checkpointing hypothesis |
| D9 | N/A | none |
| D10 | 11 | Not provided |
| D11 | 5 | Replay/checkpoint only |
| D12 | N/A | none |
| D13 | 2, 3, 8 | Core |
| D14 | N/A | none |
| D15 | N/A | none |
| D16 | N/A | none |
| D17 | 3, 8 | SDK ergonomics |
| D18 | 6, 9 | No policy plane |
| D19 | 3, 9 | Absent |
| D20 | 7 | No numbers |
| D21 | 1, 10 | Licences |
| D22 | 9 | Vendor gravity |
| D23 | N/A | none found |
| D24 | App. C | Metadata level only; sources thin |

## Appendix B. Capability mapping

| CAP-ID | This technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-59 | native | agfw-02 | BL-47/BL-48 | BUILD+REUSE | P2 |
| CAP-57 agent memory | partial/unknown | agfw-02 | Partial BL-48 | EXPERIMENT | P3 |
| CAP-49 | absent | agfw-02 | Partial (firewall) | BUILD | P1 |
| CAP-47 | absent | agfw-02 | BL-20 Partial | BUILD | P0 |

## Appendix C. Evidence records

| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-agfw-01 | microsoft/autogen README | archived, no fixes, not for production, migrate to MAF | Officially documented | https://github.com/microsoft/autogen | undated / 2026-10-26 | 0.9 | AG2 continues the lineage |
| CLAIM-agfw-02 | MAF README | open multi-language framework (.NET, Python, Go); sequential, concurrent, handoff, group patterns; durability, HITL, observability, provider flexibility | Officially documented | https://github.com/microsoft/agent-framework | undated / 2026-10-26 | 0.85 | marketing text |
| CLAIM-agfw-03 | crewAI LICENSE | "Copyright (c) 2025 crewAI, Inc." with MIT-style permission grant | Observed in source (header) | https://raw.githubusercontent.com/crewAIInc/crewAI/main/LICENSE | 2026-10-26 | 0.7 | PyPI has no licence field |
| CLAIM-agfw-04 | PyPI metadata, versions in header | versions, dates, licence classifiers | Officially documented | https://pypi.org/pypi/<pkg>/json for each package | per package / 2026-10-26 | 0.85 | classifier may differ from repo LICENSE |

## Appendix D. Assumptions

Per-framework feature rows not read from docs are UNVERIFIED and given confidence <= 0.3; this file is a licence/status/positioning record, not a feature comparison.
