| Field | Value |
|---|---|
| Registry ID | T-C09-mcp |
| Tier | A (protocol EOIP already exposes via `apps/mcp`; agent-facing security boundary) |
| Versions examined | MCP spec 2026-07-28 (current; Final predecessor 2025-11-25); Python SDK `mcp` v2.3.0 (2026-10-02) and v1.30.0 (1.x maintenance, 2026-09-07); Neo4j `mcp-neo4j` (pushed 2026-09-09); FalkorDB-MCPServer (pushed 2026-10-25); `memgraph/ai-toolkit` (2026-10-25); `awslabs/mcp` Neptune server (2026-10-23); TigerGraph `tigergraph-mcp` (2026-10-08) |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V06 |

## 1. Identity, current status, tier, sources

MCP is an open JSON-RPC 2.0 protocol letting LLM applications (clients) call tools, read resources and use prompts exposed by servers. Specification and SEP process live at modelcontextprotocol.io and the `modelcontextprotocol` GitHub org. Versions are date strings marking the last backwards-incompatible change; the **current** revision is **2026-07-28**; features follow an Active/Deprecated/Removed lifecycle with a >=12-month deprecation window [CLAIM-mcp-01].

Registry meaning: "MCP incl. graph-database MCP servers" = the protocol plus the inventory below. Ambiguity: "Memgraph MCP" is `integrations/mcp-memgraph` inside `memgraph/ai-toolkit`; "Neo4j MCP" has a Labs project (`neo4j-contrib/mcp-neo4j`) that Neo4j states is not supported by the product team, distinct from any official product server (not examined) [CLAIM-mcp-09].

**Graph-DB MCP server inventory (verified via GitHub API/README on 2026-10-26)**

| Server | Owner | Licence | Writes? | Auth / transport (as documented) |
|---|---|---|---|---|
| mcp-neo4j-cypher/memory/data-modeling/cloud-aura-api | neo4j-contrib (Neo4j Labs, Field GenAI team), ~989 stars | MIT | cypher server runs read and write Cypher; no read-only flag in README | stdio default, SSE, Streamable HTTP; auth not described; no SLA [CLAIM-mcp-09] |
| FalkorDB-MCPServer | FalkorDB | MIT | create/manage nodes, delete graphs; `query_graph_readonly`; `FALKORDB_DEFAULT_READONLY` is overridable per query | stdio; HTTP with static `MCP_API_KEY` bearer; empty key in compose disables auth; HTTP README still describes `initialize` + `Mcp-Session-Id` (pre-2026-07-28) [CLAIM-mcp-10] |
| mcp-memgraph | memgraph (ai-toolkit) | MIT | not stated in README fetched | UNVERIFIED (tools/transport not in fetched text) [CLAIM-mcp-11] |
| Amazon Neptune MCP | awslabs (Apache-2.0 monorepo, ~9.8k stars) | Apache-2.0 | **Not read-only**; runs any openCypher/Gremlin; docs say restrict via IAM role | AWS profile/IAM; stdio (inferred from client configs) [CLAIM-mcp-12] |
| tigergraph-mcp | TigerGraph | NOASSERTION ("Other") - legal review; 5 stars | UNVERIFIED | UNVERIFIED [CLAIM-mcp-13] |
| ArangoDB | community wrapper (33 tools via python-arango) and reportedly an official image | UNVERIFIED | UNVERIFIED | secondary source only, confidence 0.3 [CLAIM-mcp-14] |
| HugeGraph, JanusGraph, Stardog, GraphDB | none found by search | n/a | n/a | NOT PUBLICLY VERIFIED |

Reference servers: the official `modelcontextprotocol/servers` repo lists 7 active (Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking, Time) and archives PostgreSQL, SQLite, Redis, GitHub, etc.; no graph-DB connector is official there [CLAIM-mcp-15].

## 2. Problem, workloads, workflows

Problem: a uniform, model-discoverable tool interface so agents/IDEs reach enterprise data without bespoke integrations. Workloads relevant to EOIP: (a) IDE/agent clients (Claude Desktop, VS Code, Cursor) querying the organisation graph; (b) agent-to-graph read paths with evidence; (c) graph-DB admin/text-to-Cypher helpers (Neo4j Labs); (d) agent memory servers (Neo4j memory, reference Memory server).
Workflows: client -> `tools/list` -> model picks `search`/`entity`/`path` -> EOIP REST -> JSON result -> model answer with evidence. Failure workflow: a poisoned third-party server beside EOIP in the same client steals EOIP results (tool shadowing / cross-server exfiltration, section 9).

## 3. Feature inventory (spec 2026-07-28)

| Feature | Status | Note |
|---|---|---|
| Tools with `inputSchema`/`outputSchema`, `structuredContent` | present | JSON Schema 2020-12; `$ref` rules [CLAIM-mcp-02] |
| Tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`, `title`) | present, **hints only** | defaults: readOnly=false, destructive=true, openWorld=true; clients MUST treat as untrusted unless server trusted [CLAIM-mcp-03] |
| Resources, prompts | present | `CacheableResult` with `ttlMs`/`cacheScope` on list/read |
| Stateless core (no `initialize`, no `Mcp-Session-Id`), `server/discover`, per-request `_meta` version | present (new) | breaking vs 2025-11-25 [CLAIM-mcp-04] |
| `subscriptions/listen` for change notifications | present | replaces GET stream and resources/subscribe |
| Multi round-trip requests (`input_required`) | present | replaces server-initiated sampling/elicitation/roots requests |
| Tasks | extension `io.modelcontextprotocol/tasks` | out of core |
| Roots, Sampling, Logging | **Deprecated** | |
| HTTP+SSE transport | **Deprecated** | stdio and Streamable HTTP remain [CLAIM-mcp-05] |
| Authorization (OAuth 2.1 profile) | optional, for HTTP only | PRM RFC 9728 MUST; RFC 8707 `resource` MUST; Client ID Metadata Documents SHOULD; DCR deprecated; RFC 9207 `iss` validation MUST by clients [CLAIM-mcp-06] |
| Per-principal tool lists | allowed | list MAY vary by presented authorization, MUST NOT vary per connection |
| SDKs | Python v2.3.0 (`MCPServer`, formerly `FastMCP`), v1.30.0 maintenance; TS, others (not examined) | v2 breaking: FastMCP import warning, generic handler errors [CLAIM-mcp-07] |

## 4. Architecture

```
 MCP host (IDE/agent) --[MCP client 1]--> server A (EOIP)    \  all tool descriptions land
                      --[MCP client 2]--> server B (3rd party) > in ONE model context window
 Transport: stdio (subprocess, newline JSON-RPC) | Streamable HTTP (POST per message, JSON or request-scoped SSE)
 Per-request: _meta{protocolVersion, clientCapabilities, clientInfo, logLevel}; headers Mcp-Method, Mcp-Name, Mcp-Param-*
 AuthZ plane (HTTP): client --401+WWW-Authenticate(resource_metadata)--> PRM --> AS metadata --> PKCE+resource --> token(aud=server)
 Data plane: tools/call -> server -> backend API (EOIP: REST with one static bearer)
```

## 5. Under-the-hood reconstruction

- **Message model**: JSON-RPC requests/notifications client->server only; servers never initiate requests (MRTR returns `InputRequiredResult{inputRequests, requestState}`; client retries with `inputResponses`, new JSON-RPC id) [CLAIM-mcp-04]. `requestState` is server-minted opaque state; the spec warns state handles are names, not capabilities.
- **Statelessness**: any replica can serve any request; cross-call state uses explicit handles bound server-side to the verified principal (`<user_id>:<handle>`) [CLAIM-mcp-08]. This suits horizontally scaled, one-node-first deployments.
- **Auth reconstruction**: MCP server = OAuth 2.1 resource server. Pseudocode: `tok = bearer(req); claims = verify(tok, issuer=AS); assert aud == canonical_uri(this_server); if need(scope) not in claims.scope: 403 insufficient_scope + WWW-Authenticate(scope=..., resource_metadata=...)`. Token passthrough to downstream is forbidden; a proxy MCP server fronting a third-party OAuth API needs per-client consent, exact redirect-URI match, single-use `state`, `__Host-` cookies [CLAIM-mcp-08].
- **Python SDK entry points**: `mcp.server.fastmcp.FastMCP(...).streamable_http_app()` (1.x; EOIP uses this); in 2.x `MCPServer`, with `validate_token_resource`, `session_idle_timeout`, `max_sessions` for legacy connections [CLAIM-mcp-07].
- **Tool poisoning mechanics** (non-spec): the full `tools/list` text enters model context; hidden instructions in descriptions (or any schema field) steer the agent; `list_changed` allows post-approval mutation (rug pull); another server's tool can shadow names. Invariant Labs disclosed this 2025-04-01, testing Cursor [CLAIM-mcp-16]. Spec mitigations are SHOULD-level: human in the loop, show inputs, annotations untrusted, server MUST validate inputs, rate-limit, sanitise outputs [CLAIM-mcp-03]. Hash-pinning of tool definitions is a recommended mitigation, not a spec feature.
- Caching/versioning: deterministic tool ordering SHOULD, `ttlMs`/`cacheScope` for prompt-cache stability. Concurrency/transactions: none in protocol.

## 6. Inferred requirements for EOIP

FR: expose read-only graph tools with `readOnlyHint:true`, `destructiveHint:false`, `openWorldHint:false`; OAuth 2.1 resource-server mode for HTTP with per-request principal; `tools/list` filtered by granted scope; structured outputs with evidence IDs. NFR: stateless horizontal scale; tool-definition hash published in the release manifest; every call logged with principal, tool, args hash and ACL decision; MCP results carry only ACL-filtered facts (BL-18) and pass egress policy when the client is a cloud model (BL-45).

## 7. Performance and resource model

Protocol overhead is negligible versus backend work; no vendor benchmarks used. Resource risk is context size: all tool descriptions occupy prompt tokens (no figure verified). Stateless HTTP removes sticky-session memory; SDK 2.2+ expires idle legacy sessions after 30 min. Failure modes: lost in-flight request on broken stream (no resumability in 2026-07-28; client must re-issue) [CLAIM-mcp-04]; SSRF in discovery fetchers; rug-pull drift.

## 8. Strengths and how to match/exceed

| Strength | How |
|---|---|
| Universal client ecosystem (IDEs, agents) | keep MCP as an adapter over the governed REST/QueryPlan; do not fork protocol |
| Stateless core, cache hints | already partly aligned (`stateless_http=True`); adopt `ttlMs` once on SDK v2 |
| OAuth profile with audience binding, scope step-up | exceed: map scopes to EOIP ABAC and per-source ACL |
| Annotations as hints | exceed: enforce server-side; publish annotations and a signed tool manifest |

## 9. Limitations with root causes

| Class | Item |
|---|---|
| Algorithmic/semantic | LLM cannot distinguish description from instruction: tool poisoning is inherent to the in-context design (mechanism reported widely; root cause is hypothesis-grade) |
| Intentional trade-off | Auth optional; annotations advisory; human-in-loop only SHOULD [CLAIM-mcp-03] |
| Operational | Spec churn: 2026-07-28 is breaking (no handshake, sessions, SSE resumability) and SDK 2.x is breaking vs 1.x; FalkorDB README already lags [CLAIM-mcp-10] |
| Ecosystem | Graph-DB servers are Labs/community grade; Neptune server executes mutations; static-key auth; TigerGraph licence unclear |
| User reports | Attack-success figures for poisoning conflict (36.5% MCPTox across 20 models vs >60% in a CSA note): NOT reconciled, unverified |

## 10. Deployment, licensing, viability

Spec text licence and Python SDK licence were not examined (UNVERIFIED; verify before redistribution). Graph servers: MIT (Neo4j Labs, FalkorDB, Memgraph), Apache-2.0 (AWS), TigerGraph unknown -> legal review trigger. Air-gap: yes; stdio and Streamable HTTP need no cloud. OAuth CIMD fetches client metadata URLs: in air-gap use pre-registration. Do not bundle third-party servers in the white-label package; EOIP ships its own.

## 11. Competitive delta against EOIP baseline

| Item | EOIP verified (BL-47) | Gap |
|---|---|---|
| Server | `apps/mcp/main.py`, 228 lines, 18 tools, `mcp==1.30.0` FastMCP, `stateless_http=True`, `json_response=True` | on SDK 1.x maintenance line; 2026-07-28 support UNVERIFIED (1.30.0 notes silent) |
| Auth | one static bearer, `hmac.compare_digest` against `api_token()` | no OAuth 2.1, no PRM, no audience binding, no per-user identity, no scopes; all callers = one principal (code inspection) |
| Annotations | none found (grep `annotations|readOnlyHint` empty) | ADR-007 read-only is by convention, not declared |
| Write path | `run_agent` POSTs a run; docstring says mutations are inert proposals | not annotated; spec defaults would read as destructive/open-world |
| ACL | tools `entity`, `document`, `evidence`, `search` call REST | BL-18 absent: MCP is a leakage amplifier for agents |
| Host/Origin | `TransportSecuritySettings` allowlist for localhost and `eoip-mcp` | good DNS-rebinding hygiene (matches spec local-server guidance) |
| Strengths vs graph servers | typed QueryPlan not raw Cypher; read-oriented; ADR-007 | Neo4j/Neptune servers expose raw query languages; EOIP safer by design |

## 12. Strength and inversion cards

STR-mcp-01 | MCP | universal agent/IDE interface | [mcp-01,02] | reach without per-client plugins | match | keep `apps/mcp` as thin facade over governed API | a stock MCP client lists and calls all tools against a test tenant.
STR-mcp-02 | MCP | OAuth audience binding + scope step-up | [mcp-06] | auditable per-user agent access | exceed | resource-server mode; scopes mapped to ABAC/ACL | token for another audience rejected 401; insufficient scope returns 403 with `scope=`.
STR-mcp-03 | MCP | annotations/`outputSchema` | [mcp-03] | client UX and safe auto-approve of read tools | match | annotate all 18 tools | schema test asserts every tool carries hints.

**INV-mcp-01 (tool poisoning / rug pull).** Target: MCP clients, 2025-2026. Limitation: model-visible descriptions are untrusted input [mcp-16]. Root cause: in-context design; mechanism *proven* by disclosure, success rates *hypothesis*. Options: (1) quick - publish SHA-256 of `tools/list` in release manifest, client pins; (2) native - signed tool manifest plus egress policy blocking cross-server data flow in EOIP-controlled clients (VS Code ext, web); (3) long-term - capability-based tool broker where the model sees only EOIP-curated schemas, third-party servers mediated with taint tracking. Selected: 1 then 2. Benchmark: red-team corpus of 50 poisoned third-party descriptions co-resident with EOIP; success = zero EOIP-derived bytes sent to non-allowlisted tool arguments; baseline stock client. Failure: pinned hash breaks on legitimate update (needs re-approval UX). Defensibility: signed manifest tied to EOIP ACL/egress ledger is hard to copy without our graph policy. Decision: EXPERIMENT. Alternative is worse when users bring arbitrary servers EOIP cannot mediate.
**INV-mcp-02 (confused-deputy via single shared token).** Root cause: *proven by code inspection*: server authenticates one static secret and has no principal. Options: quick - per-user static tokens; native - OAuth RS with token exchange to REST carrying `sub`; long-term - MCP gateway with ReBAC. Selected: native. Test: user A cannot retrieve user B-only document via MCP (J5 leakage test). Decision: ADOPT (P0 with BL-18).
**INV-mcp-03 (raw-query graph servers).** Neo4j/Neptune servers run LLM-written Cypher/Gremlin with write capability [mcp-09,12]; EOIP QueryPlan templates (ADR-006) are the inversion; keep, add `readOnlyHint`. Decision: ADOPT. No 10.5 seed hypothesis targets MCP.

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-59 MCP tool interface | REUSE protocol; BUILD annotations, OAuth RS, ACL filtering; EXPERIMENT SDK v2 migration |
| CAP-46 source-ACL on agent results | BUILD (blocked on BL-18) |
| CAP-49 injection defence for tool descriptions | EXPERIMENT (manifest pinning) |
| CAP-51 egress | REUSE gateway; apply to MCP outputs |
| Third-party graph MCP servers | REJECT bundling; INTEGRATE only as optional dev-time client connections |

## 14. Tests and acceptance

1. Conformance: run the official MCP conformance suite pinned to 2026-07-28 against EOIP (suite referenced in SDK 2.1.0 notes; confirm). 2. All tools expose annotations; read tools `readOnlyHint:true`. 3. Replay a token minted for another audience: 401. 4. Two-user ACL test through MCP (J5). 5. DNS-rebinding test against `TransportSecuritySettings`. 6. Poisoned co-server red-team (INV-mcp-01). 7. SBOM lists pinned SDK version and licence.

## 15. Risks and open questions

SDK 2.x migration cost and whether 1.30.0 negotiates 2026-07-28 (UNVERIFIED); whether to run EOIP's own OAuth AS (OIDC exists, BL-19) in air-gap; whether annotations help since clients treat them untrusted; SDK and spec licence verification; HugeGraph has no MCP server found (opportunity or gap).

## Appendix A. Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | spec versions, governance via SEPs, licences of servers |
| D2 | 2 | agent/IDE access |
| D3 | 4,5 | client/server/AS roles, transports |
| D4 | N/A | protocol has no storage |
| D5 | 3,5 | JSON Schema 2020-12 |
| D6 | N/A | no query engine; backend servers pass raw queries |
| D7 | N/A | none |
| D8 | 5,7 | stateless; no transactions |
| D9 | N/A | not ingestion; read path |
| D10 | 9,11 | no evidence model; EOIP `evidence` tool |
| D11 | 3 | spec versioning, deprecation |
| D12 | N/A | |
| D13 | 2,5,8 | core topic |
| D14 | 1,9 | text-to-Cypher in Neo4j Labs server; accuracy not measured |
| D15 | N/A | |
| D16 | 3 | human-in-loop UI requirements |
| D17 | 3,5 | SDKs, conformance |
| D18 | 5,9,12 | OAuth, poisoning, SSRF, confused deputy |
| D19 | 11 | tenancy not in protocol; per-principal lists allowed |
| D20 | 7 | no numbers verified |
| D21 | 10 | free/open; servers MIT/Apache |
| D22 | 3 | transport/protocol versions, deprecations |
| D23 | N/A | no patents examined (UNVERIFIED) |
| D24 | 9 | conflicting poisoning stats flagged |

## Appendix B. Capability mapping

| CAP | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-59 | native | mcp-02,03 | BL-47 Implemented | REUSE + BUILD hardening | P1 |
| CAP-44 | native (OAuth profile) | mcp-06 | BL-19 Implemented/Partial; MCP static token | BUILD | P0 |
| CAP-46 | absent in protocol (server duty) | mcp-08 | BL-18 Absent | BUILD | P0 |
| CAP-49 | partial (SHOULD guidance) | mcp-03,16 | not covered | EXPERIMENT | P1 |
| CAP-51 | absent | - | BL-45 Implemented | REUSE | P2 |
| CAP-50 | native (stdio/HTTP) | mcp-05 | compose | REUSE | P2 |

## Appendix C. Evidence records (accessed 2026-10-26)

| CLAIM | product/version/date | claim | class | source | pub/access | conf + rationale | contradictory |
|---|---|---|---|---|---|---|---|
| mcp-01 | spec 2026-07-28 | Current revision is 2026-07-28; date-string versioning; Draft/Current/Final; deprecation >=12 months | Officially documented | MCP Versioning, https://modelcontextprotocol.io/specification/versioning | n/a / 2026-10-26 | 0.95 primary | none |
| mcp-02 | 2026-07-28 | Tools have inputSchema/outputSchema (JSON Schema 2020-12), structuredContent; servers MUST validate inputs, rate-limit, sanitise outputs | Officially documented | Tools spec, https://modelcontextprotocol.io/specification/2026-07-28/server/tools | /2026-10-26 | 0.95 | none |
| mcp-03 | 2026-07-28 | Clients MUST consider tool annotations untrusted unless from trusted servers; ToolAnnotations fields readOnlyHint (default false), destructiveHint (true), idempotentHint (false), openWorldHint (true) are hints; human in loop SHOULD | Officially documented | Tools spec; schema.ts https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2026-07-28/schema.ts | /2026-10-26 | 0.9 (schema read via summarizer) | none |
| mcp-04 | 2026-07-28 | Removes initialize handshake and Mcp-Session-Id; adds server/discover, subscriptions/listen, MRTR, removes SSE resumability, tasks to extension | Officially documented | Key Changes, https://modelcontextprotocol.io/specification/2026-07-28/changelog | /2026-10-26 | 0.95 | FalkorDB README still describes sessions |
| mcp-05 | 2026-07-28 | Standard transports are stdio and Streamable HTTP; HTTP+SSE Deprecated | Officially documented | Transports, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports ; changelog | /2026-10-26 | 0.95 | none |
| mcp-06 | 2026-07-28 | Authorization optional; HTTP SHOULD conform; PRM RFC 9728 MUST; RFC 8707 resource MUST; CIMD SHOULD; DCR deprecated; clients MUST validate `iss`; servers MUST validate audience and MUST NOT accept other tokens | Officially documented | Authorization, https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | /2026-10-26 | 0.95 | none |
| mcp-07 | Python SDK v2.3.0 2026-10-02; v1.30.0 2026-09-07 | v2 line current; 1.30.0 maintenance, release notes do not mention 2026-07-28 support; tasks extension and DPoP not yet implemented in 2.2.0 | Officially documented | GitHub releases, https://github.com/modelcontextprotocol/python-sdk/releases | /2026-10-26 | 0.8 (summarised notes) | support may exist undocumented |
| mcp-08 | 2026-07-28 | Token passthrough forbidden; confused-deputy mitigations; handle hijacking: bind to principal; SSRF mitigations | Officially documented | Security Best Practices, https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices | /2026-10-26 | 0.95 | none |
| mcp-09 | mcp-neo4j, pushed 2026-09-09 | MIT, not archived; Labs, not supported by product team; cypher server runs read/write Cypher; stdio/SSE/HTTP | Officially documented | https://github.com/neo4j-contrib/mcp-neo4j ; GitHub API | /2026-10-26 | 0.85 | official product server separate, not examined |
| mcp-10 | FalkorDB-MCPServer 2026-10-25 | MIT; `query_graph_readonly`; default read-only env overridable; bearer MCP_API_KEY, empty disables | Officially documented | https://github.com/FalkorDB/FalkorDB-MCPServer | /2026-10-26 | 0.85 | none |
| mcp-11 | memgraph/ai-toolkit 2026-10-25 | MIT; mcp-memgraph integration exists; tools not verified | Officially documented | https://github.com/memgraph/ai-toolkit | /2026-10-26 | 0.6 | none |
| mcp-12 | awslabs/mcp 2026-10-23 | Apache-2.0; Neptune server not read-only, runs any query, scope via IAM | Officially documented | https://github.com/awslabs/mcp (src/amazon-neptune-mcp-server) | /2026-10-26 | 0.85 | none |
| mcp-13 | tigergraph-mcp 2026-10-08 | Licence NOASSERTION/"Other"; 5 stars | Officially documented (API) | https://github.com/tigergraph/tigergraph-mcp | /2026-10-26 | 0.6 | owner org not independently confirmed |
| mcp-14 | ArangoDB MCP | community 33-tool wrapper; official image reported | Third-party report | search aggregators (chatforest, agentpedia) | /2026-10-26 | 0.3 | mixed sources |
| mcp-15 | servers repo | 7 active reference servers; PostgreSQL, SQLite, Redis etc. archived; no graph DB server | Officially documented | https://github.com/modelcontextprotocol/servers | /2026-10-26 | 0.8 | none |
| mcp-16 | n/a | Tool poisoning, rug pull, shadowing disclosed 2025-04-01; tested only Cursor | Third-party report | Invariant Labs, https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks | 2025-04-01 / 2026-10-26 | 0.8 | success-rate figures conflict (36.5% vs >60%) unverified |
| mcp-17 | EOIP repo | `apps/mcp/main.py`: FastMCP stateless_http, json_response, static bearer via hmac.compare_digest, 18 tools, no annotations | Observed in source code | local repo | /2026-10-26 | 0.95 | none |

## Appendix D. Assumptions

Verified-on date set to actual access date 2026-10-26. Official Neo4j product MCP server not examined. Spec/SDK licences not checked. EOIP statements come from direct reading of `apps/mcp/main.py` plus the baseline; no live run. WebFetch summaries were produced by a small model; page text was not independently diffed.
