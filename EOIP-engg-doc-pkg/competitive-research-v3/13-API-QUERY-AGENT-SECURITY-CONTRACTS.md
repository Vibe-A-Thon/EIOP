# 13 — API, Query, Agent and Security Contracts

| Field | Value |
|---|---|
| Document | 13-API-QUERY-AGENT-SECURITY-CONTRACTS.md |
| Supersedes | The 2026-10-19 placeholder pass at this path; overwritten in full |
| Scope | Typed query AST/IR, backend compilers, parameterized query gateway, REST/MCP, NL-query and suggestion contracts, policy hooks, error contracts needed by the P0/P1 requirements in `11-REQUIREMENTS-FINAL.md` |
| Companion | `12-DATA-ONTOLOGY-EVENT-CONTRACTS.md` defines the data shapes (ACL envelope, tenant context, epistemic state, action-intent) this document's interfaces carry over the wire |

---

## 1. QueryPlan → AST → {gremlin-lang, openCypher, SPARQL} compiler interface

**Requirements:** REQ-QRY-03 (make this the only production path), REQ-SEC-06 (remove string-built Gremlin), REQ-QRY-05 (explicit path modes), REQ-QRY-02 (typed NL-query candidates), REQ-STOR-01 (conformance gate on compiled output).
**Existing code:** `packages/eoip/contracts/query_plan.py QueryPlan` (v1 — `intent: SEARCH|PATH|IMPACT|NEIGHBORHOOD|LINEAGE|TRACEABILITY`, `anchors, relationship_allowlist, max_depth (1–8), result_limit (1–500), timeout_ms, evidence_mode, filters`), `packages/eoip/query/ast_compiler.py ASTCompiler` (`compile_cypher`, `compile_gremlin`, `compile_sparql` — typed filter/match/projection/order nodes, variable-length paths, `from_dict`, **output is query text only, no execution hookup, no caller outside `query/`**), `packages/eoip/query/plan_engine.py TypedPlanEngine` (`parse_to_plan`, `inject_scope` — regex-based plan construction, **not mounted**), `packages/eoip/query/executor.py` (the actual production path today: intent → named bounded template, no compilation step).

### 1.1 Compiler contract

```
QueryPlan (v2, extends v1):
  intent: QueryIntent                    # (existing) SEARCH | PATH | IMPACT | NEIGHBORHOOD | LINEAGE | TRACEABILITY
  anchors: list[string]                  # (existing) canonical_ids the traversal starts from
  relationship_allowlist: list[string] | null  # (existing)
  path_mode: enum[any, shortest, trail] | null  # (added, REQ-QRY-05) explicit semantics instead of implicit Python-loop order
  max_depth: integer (1-8)               # (existing)
  result_limit: integer (1-500)          # (existing)
  timeout_ms: integer (50-30000)         # (existing)
  evidence_mode: enum[none, summary, full]  # (existing)
  filters: object | null                 # (existing)
  tenant: TenantContext                   # (added, required — see 12 §2) refused if absent
  scope: TrustedScope                      # (added, required — see 12 §2/§7) ACL principal set for SEC-05/SEC-06

AstNode (abstract, extends query/ast_compiler.py's existing typed nodes):
  node_kind: enum[match, filter, projection, order, path, limit]
  children: list[AstNode]

CompiledQuery:                            # NEW — the missing execution half of ast_compiler.py
  backend_kind: enum[hugegraph, neo4j, neptune, rdf]
  dialect: enum[gremlin_lang, opencypher, sparql]
  query_text: string                      # parameterised, never string-interpolated (REQ-SEC-06)
  bound_parameters: dict[string, any]      # typed parameter bindings, never spliced into query_text
  explain_only: boolean                    # true for NL-query safety checks (REQ-QRY-02) before a user selects a candidate
  budget: QueryBudget

QueryBudget:                               # NEW — closes GAP-32's supernode blow-up risk (REQ-QRY-08, dependency)
  max_degree_expansion: integer | null
  partial_on_exceed: boolean               # true: return partial=true rather than truncate silently

CompilerError:                             # NEW — typed, not a generic 500
  stage: enum[parse, bind, compile, policy_reject]
  reason: string
  offending_node: AstNode | null
```

### 1.2 Per-backend compiler contract

| Backend | Dialect target | Push-down | Parameter binding | Notes |
|---|---|---|---|---|
| HugeGraph | gremlin-lang (TinkerPop 4.0 direction, STR-tinkerpop-01) | Native traversal where `path_mode` is supported | Bound via gremlin-lang typed parameters, not string splice (closes GAP-05 at this backend) | Groovy-closure dependency removed per REQ-STOR-01 |
| Neo4j | openCypher (Cypher 25) | Native path expressions | Driver-level bound parameters | Already parameterised at HEAD; this requirement makes it the *only* path, not an alternative one |
| Amazon Neptune | openCypher over HTTPS | Native where available; falls back to bounded Python traversal otherwise | Bound parameters + AWS SigV4 request signing (REQ-STOR-01 dependency) | SigV4 absence today is a blocking defect for any IAM-enabled cluster |
| JanusGraph | gremlin-lang | Vertex-centric indexes for supernode queries (REQ-QRY-08) | Parameterised (closes the `p_`-prefix and string-splice defects) | |
| RDF sidecar (Fuseki/GraphDB) | SPARQL 1.1 | `RdflibSparqlBackend` algebra-level validation (rejects updates/SERVICE/unbounded paths) | `bind_parameters` (existing, `query/sparql_backend.py:105`) | Read-only by default (`enable_updates=False`) |

A `CompilerError` with `stage = policy_reject` is returned, never silently dropped, when a compiled query would violate `relationship_allowlist`, exceed `QueryBudget`, or fail the ACL/tenant scope check in §3 — this is the single choke point REQ-SEC-06's "no hand-built script ever reaches a backend" guarantee depends on.

### 1.3 Why this interface, not an incremental patch

Three self-inversion cards (`09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-05, INV-SELF-08, and the GAP-04 root-cause analysis) converge on the same root cause: every backend-specific defect found in this research run — the JanusGraph `p_`-prefix mismatch, the Neptune LIMIT-before-filter truncation, the two string-spliced Gremlin call sites — is a symptom of the production path being Python-template traversal rather than a compiled, typed plan. Patching each defect individually (REQ-STOR-01, REQ-SEC-06's quick-integration option) closes today's three known instances; routing every backend call through `ASTCompiler` (REQ-QRY-03) closes the *class* of defect, because a hand-built per-backend string can no longer exist on the production path at all. This is why REQ-QRY-03 is the structural dependency of REQ-SEC-06, REQ-STOR-01's conformance gate, and REQ-QRY-05's path modes: each of those requirements ships a narrower fix first (so correctness does not wait on an 8–12 week compiler rollout) but names the compiler as its target architecture, not an alternative to it.

### 1.4 NL-query → compiled query path

`NlQueryCandidate.plan` (§4) and `CompiledQuery` (§1.1) are the same type family deliberately: a candidate a user selects in REQ-QRY-02's suggestion flow is compiled through exactly this interface, not through a separate "LLM-generated query" execution path. This is what makes GAP-35's "typed plan candidates, not raw queries" requirement enforceable rather than aspirational — there is no code path by which an LLM-authored string reaches a backend; only a `QueryPlan` can.

---

## 2. MCP tool contract: OAuth 2.1 resource-server auth and per-tool ACL/annotation schema

**Requirements:** REQ-SEC-02, REQ-SEC-03.
**Existing code:** `apps/mcp/main.py` (18 `@mcp.tool` handlers, each forwards to the REST API using **one shared static bootstrap token**, `hmac.compare_digest` against a single secret — confirmed unchanged in shape at HEAD), `packages/eoip/tools_contract/mcp_server.py EOIPMCPServer` (ontology/graph/action tools, identity-spoof argument check, budgets, provenance log — **in-process only**, not mounted by `apps/mcp`), `packages/eoip/tools_contract/mcp_bridge.py` (460 lines, **outbound** external-MCP client with host allowlist, schema digests, read-only filtering — already a good pattern to mirror inbound).

### 2.1 Auth flow (REQ-SEC-02)

```
McpAuthRequest:
  bearer_token: string                    # OAuth 2.1 access token, NOT the shared bootstrap secret
  resource: string                         # "eoip-mcp" — this server as an OAuth 2.1 resource server

McpPrincipal:                              # resolved from token introspection, replaces the single shared principal
  principal_id: string                     # (existing shape, TrustedScope.principal_id)
  principal_type: enum[user, service_account, agent]  # (existing enum, canonical.py PrincipalType)
  tenant_id: string                        # (existing, TrustedScope.tenant_id)
  scopes: list[string]                     # OAuth scopes mapped to existing RBAC/ABAC roles
  delegation_chain: list[string]           # (existing, TrustedScope.delegation_chain) — who is this agent acting on behalf of

McpAuthError:                              # NEW — typed, not a bare 401
  reason: enum[invalid_token, expired_token, insufficient_scope, no_principal_resolved]
```

Every MCP request resolves a `McpPrincipal` before any tool executes; the shared-bootstrap-token path is **removed**, not deprecated alongside it, per REQ-SEC-02's requirement that "no caller can act as any principal but its own." The resolved `McpPrincipal` is what REQ-SEC-05's read-path ACL enforcement filters against — MCP is one more caller of the same `authz/pdp.py can_read`, not a parallel enforcement path.

### 2.2 Tool ACL/annotation schema (REQ-SEC-03)

```
McpToolManifest:                           # extends contracts/tool.py ToolContract (see 12 §11)
  name: string                             # (existing)
  version: string                          # (existing)
  read_only: boolean                       # (existing)
  risk_level: enum[R0,R1,R2,R3,R4]         # (existing)
  acl_scope: list[string]                   # (added, 12 §11) principal scopes required to invoke
  manifest_digest: string                   # (added, 12 §11) RFC 8785 hash, re-verified client-side before each call
  input_schema: dict                        # (existing)
  annotations: ToolAnnotations               # (added, NEW)

ToolAnnotations:                            # NEW — model-visible hints the server itself enforces, not just advertises
  destructive: boolean                      # true blocks execution without approval_required = true (ToolContract validator already enforces this for risk >= R2)
  idempotent: boolean
  open_world: boolean                       # true = tool result may include content the model did not request (untrusted-input fencing applies, see §4)
```

A tool call whose resolved `McpPrincipal.scopes` does not cover `McpToolManifest.acl_scope` is denied before `ToolRequest` construction, closing the MCP-specific instance of GAP-02; a mismatched `manifest_digest` (the manifest changed since the client last saw it) is treated as a tool-poisoning signal and the call is denied, not merely logged — this is the concrete mechanism behind BM-18's tool-poisoning test corpus.

---

## 3. AuthzPort interface (check/expand/list-objects, STR-rebac-01 pattern)

**Requirements:** REQ-SEC-04, REQ-SEC-05, REQ-SEC-07, REQ-TEN-01, used by both retrieval (§4) and MCP (§2).
**Existing code:** `authz/pdp.py can_read`, `authz/derivation_acl.py DerivationACLEvaluator.filter_graph_contexts`/`filter_traversal_paths`, `authz/core.py` (route-level RBAC/ABAC, unrelated to this port — kept separate, not merged).

A single `AuthzPort` interface is the one choke point every caller (search, graph traversal, MCP, export, UI) goes through — this is STR-sourcegraph-02's "permissions enforced across every feature" pattern, matched rather than exceeded (the exceed-grade addition is the consistency token in §3.2).

```
AuthzPort (interface):
  check(principal: McpPrincipal, resource_ref: string, action: enum[read, write, derive]) -> AuthzDecision
  expand(principal: McpPrincipal, resource_refs: list[string]) -> list[AuthzDecision]   # batch form, used by retrieval candidate-filtering stages
  list_objects(principal: McpPrincipal, resource_kind: string, limit: integer) -> list[string]  # used by export/DSAR (privacy/dsr.py) to enumerate what a principal may access

AuthzDecision:                             # NEW — wraps authz/pdp.py's existing boolean can_read with a reason
  resource_ref: string
  allowed: boolean
  reason: enum[acl_match, classification_denied, tenant_mismatch, epoch_stale, no_acl_found]
  policy_epoch_checked: integer             # (12 §7 PolicyEpochToken.policy_epoch)
```

`check` wraps `authz/pdp.py can_read` directly; `expand` wraps `authz/derivation_acl.py filter_graph_contexts`/`filter_traversal_paths` for the batch case retrieval's keyword/vector/hybrid/graph stages all need (REQ-SEC-05); `list_objects` is the enumeration primitive DSAR (`privacy/dsr.py`, already implemented for locate/export/rectify/erase) and MCP's `list_objects`-style tools both need, instead of each reimplementing "what can this principal see."

### 3.2 Consistency-token revocation (REQ-SEC-07, exceed-grade)

```
AuthzPort.check_with_epoch(principal, resource_ref, action, cached_epoch: integer) -> AuthzDecision
  # if cached_epoch < PolicyEpochRegistry.current_epoch(principal.tenant_id): forces a fresh check,
  # never serves a decision computed under a superseded epoch (12 §7 StalenessCheck)
```

Every retrieval cache, tenant search index and memory read (12 §4, §7) calls `check_with_epoch`, not the plain `check`, so a revocation is visible in O(1) without a re-index — the falsifiable claim behind BM-04's revocation cases.

---

## 4. Error/abstention contract for NL query and GraphRAG

**Requirements:** REQ-QRY-02 (typed plan candidates, not raw queries), REQ-QRY-06/07 (GraphRAG benchmark-gated adoption), GAP-35's explicit framing.
**Existing code:** `suggest/engine.py` (deterministic suggestion tier, mounted; `LLMAssistHook` optional tier), `query/nlq.py` (NLQ response contract), `ai/graphrag.py GraphRAGPipeline` (`PromptInjectionFence`, `ModelManifest.from_provider` tokenizer-budget, `answer_question` with extractive fallback and `degraded_reason`, already implemented and wired at `retrieval/service.py:215-247`), `ai/claim_support.py` (cited-span claim-support check, already implemented).

```
NlQueryCandidate:                          # NEW — what the LLM tier emits instead of raw Gremlin/Cypher/SPARQL text
  candidate_id: string
  plan: QueryPlan                          # (12 §2/§7 scoped) — never executable text, always a typed plan
  explanation: string                       # plain-language, shown to the user before execution
  rank: number                              # confidence/ranking score
  safety_check: ExplainSafetyResult          # (added, NEW) STR-n4gr-02 pattern

ExplainSafetyResult:                       # NEW
  read_only_verified: boolean               # planner-based check (EXPLAIN-equivalent) before any candidate is selectable
  rejected_reason: string | null            # populated if read_only_verified = false; candidate is hidden from the user, not shown-then-blocked

NlQueryResponse:
  candidates: list[NlQueryCandidate]        # ranked; user must select one — J11's "the user picks one" step
  fallback: enum[deterministic_tier, none]  # which tier produced these candidates if the LLM tier is degraded/unavailable

AbstentionResult:                          # extends ai/graphrag.py's existing degraded_reason into a typed contract
  status: enum[answered, abstained, degraded]
  degraded_reason: string | null             # (existing pattern) e.g. "no grounding evidence found", "model unavailable"
  answer_citations: list[CitedSpan]          # (existing, retrieval.py RetrievalResult.answer_citations) sentence -> evidence span
  unsupported_claims_removed: integer        # (existing behaviour per ai/claim_support.py, now surfaced as a count)

CitedSpan:
  sentence_ref: string
  evidence_ref: string                       # ties to 12 §6 Evidence/EvidenceLocator
  char_start: integer
  char_end: integer
```

`AbstentionResult.status = abstained` is returned, not a confident-sounding templated answer, whenever `ai/claim_support.py`'s claim-support check finds no citable span for a generated sentence — this is the existing behaviour (`retrieval/service.py` already strips unsupported/fabricated-citation/wrong-number/negated claims per the commit history) formalised as a typed, testable contract rather than an implicit side effect of the synthesis pipeline.

---

## 5. Policy-hook points (mandatory, not optional)

**Requirements:** every P0 security/tenancy requirement; this section is the enforcement map, not a new contract.

| Hook point | File (existing) | Today | Required (P0) |
|---|---|---|---|
| Ingestion write | `validation/gate.py check_vertex/check_edge` | Label + required-property only | + ACL (SEC-04), + tenant (TEN-01), + epistemic_state (GOV-01), + typed constraints (GOV-08, P2) |
| Keyword retrieval | `retrieval/service.py search_keyword` | Tenant-ownership filter only (`owned_by`) | + mandatory ACL filter via AuthzPort.expand (SEC-05) |
| Vector retrieval | `retrieval/service.py search_vector`, `retrieval/tenant_index.py` | Tenant-ownership filter only | + mandatory ACL filter (SEC-05) |
| Hybrid retrieval | `retrieval/service.py search_hybrid` | Tenant-ownership filter only | + mandatory ACL filter (SEC-05) |
| Graph-traversal retrieval | `retrieval/service.py retrieve()` | ACL filter exists but gated on an optional `scope` argument no deployed caller passes | `scope` becomes a required argument (SEC-05) |
| Answer synthesis / RAG | `apps/api/main.py /api/v1/rag`, `ai/graphrag.py` | No ACL/scope passed today | + mandatory AuthzPort check before synthesis (SEC-05) |
| Agent queries | `agents/governed.py` | Calls `retrieve` without scope or `allow` | + mandatory scope (SEC-05) |
| MCP tool calls | `apps/mcp/main.py` | Single shared principal, no per-tool ACL | OAuth 2.1 principal (SEC-02) + per-tool ACL/annotations (SEC-03) |
| Export | `exporters/obsidian_vault.py` and other exporters | No ACL check | + mandatory AuthzPort.list_objects/check (SEC-05) |
| Agent memory read/write | `memory_eng/engine.py`, `reasoning/memory.py`, `agents/memory.py` | No ACL/tenant/evidence fields at all | Full MemoryRecord v2 (12 §4) + AuthzPort.check_with_epoch (MEM-01, SEC-07) |
| DSAR locate/export/erase | `privacy/dsr.py` | Admin-only routes, tenant-store scoped | Already correct pattern; `list_objects` (§3) reuses it, not replaces it |

Every row's "Required" column is a hard dependency for its REQ-ID's acceptance test (BM-04/BM-05/BM-18) — none of these hooks are optional stages a caller may skip; the whole point of REQ-SEC-04/05/02/03/07 and REQ-TEN-01 is converting every row in this table from "exists but optional" or "absent" to "mandatory and tested."

The reason the hook map is written as a table rather than a narrative is that `01a-BASELINE-DELTA-HEAD.md` BL-18 found the exact same shape of defect at every row independently — a real evaluator, called from exactly one place, gated on an argument no production caller supplies. A reviewer checking this requirement set for completeness should re-derive this table directly from a repository grep (`grep -rn "def retrieve\|def search_keyword\|def search_vector\|def search_hybrid" retrieval/`) rather than trust it as prose; the table is a checklist precisely because the underlying defect pattern recurred enough times that an ad hoc per-caller fix would plausibly miss one.

### 5.1 Typed error contracts across the surface

| Contract | Raised by | Carries |
|---|---|---|
| `CompilerError` (§1.1) | `ASTCompiler`, `TypedPlanEngine` | `stage`, `reason`, `offending_node` |
| `McpAuthError` (§2.1) | MCP auth resolution | `reason` (invalid/expired token, insufficient scope, no principal) |
| `AuthzDecision` (§3) with `allowed = false` | `AuthzPort.check`/`expand` | `reason` (acl_match failure, classification_denied, tenant_mismatch, epoch_stale, no_acl_found) |
| `AbstentionResult` with `status = abstained` (§4) | `ai/graphrag.py` synthesis | `degraded_reason`, `unsupported_claims_removed` |
| `ConstraintViolation` (12 §5) | `validation/gate.py` | `constraint`, `mutation_id`, `reason` |
| `TenantScopeRequiredError` (12 §2) | `GraphStore` protocol | — (refusal, no partial result) |

Every one of these is a typed, inspectable object, not a bare HTTP status code or a generic exception string — this is deliberate: J6 ("deterministic first, AI second... abstain with actionable evidence gaps when ungrounded") and J5 ("enforce source ACLs... invalidate inaccessible memory") both require that a caller (human or agent) can distinguish *why* a result was withheld, not just that it was. A UI or agent that receives `AuthzDecision.reason = epoch_stale` can retry after a fresh check; one that receives `reason = classification_denied` should not retry at all. Collapsing these into one generic "403 Forbidden" would satisfy the letter of REQ-SEC-05 while defeating its purpose for J11's "ranked candidates with plain-language explanations" requirement.

---

## 6. REST and SDK surface notes

The existing FastAPI surface (`apps/api/app.py`, `apps/api/main.py`, `apps/api/extended.py`) and the SDK generators (`sdk/openapi_generator.py`, `sdk/python_client.py`, `sdk/typescript_client.py`, library-only per NB-13) are **not redesigned** by this package — every contract above is additive to existing routes (`POST /api/v1/retrieval`, `POST /api/v1/rag`, `/api/v1/ontology/*`, `/api/processing/v1/*`) or newly mounts an existing library-only module (`query/sparql_protocol.py SparqlProtocolHandler` for REQ-STD-01, `actions/router.py` for the Actions engine, `ontology/governance.py` for REQ-GOV-05). No new top-level API surface is introduced except the MCP auth flow (§2.1), which replaces rather than adds to the existing MCP transport.

---

## 7. Worked example — J5 across this document's interfaces

Master Prompt §14's J5 ("two employees with different permissions ask the same question; enforce source ACLs in retrieval and answers; invalidate inaccessible memory and index entries after revocation") exercises every interface in this document in one request, which is why it is the acceptance journey BM-04 is built around:

1. A user asks a question through the REST API or an MCP tool. If MCP, §2.1 resolves an `McpPrincipal` from the OAuth 2.1 token — not the old shared bootstrap token — before anything else runs.
2. The NL-query tier (§4) proposes `NlQueryCandidate` objects, each carrying a `QueryPlan` already scoped with the resolved principal's `TrustedScope` (12 §2/§7). The user selects one.
3. The selected plan compiles through §1's `ASTCompiler` into a `CompiledQuery`; before execution, `AuthzPort.check_with_epoch` (§3.2) validates the caller's cached policy epoch is current, not stale from before a prior revocation.
4. Retrieval candidate stages (keyword, vector, hybrid, graph-traversal) each call `AuthzPort.expand` (§3) over their candidate sets — the mandatory hook map in §5 is what guarantees none of these four stages can skip this call.
5. Synthesis runs through `ai/graphrag.py`; `ai/claim_support.py` strips any sentence that cannot be tied to a `CitedSpan` (§4) the caller is permitted to see — a cited span pointing at a fact the caller cannot read is itself an ACL violation, so the claim-support check and the ACL check compose, not run independently.
6. The response carries `AbstentionResult` (§4), with `status = abstained` if nothing citable survived filtering — the honest "don't know" J6 requires, not a confidently wrong answer built from the pre-filtered context.
7. If this user's permissions were revoked between step 1 and step 6 (the specific case BM-04's revocation corpus tests), step 3's epoch check catches it on this request; nothing in steps 4–6 depends on a background re-index job having already run.

A second user with disjoint permissions asking the identical question at the identical moment produces a different `CompiledQuery` result set at step 4 (different candidates survive `AuthzPort.expand`), a different or empty `AbstentionResult` at step 6, and — critically for the zero-leakage bar — no artefact from steps 2–6 (cache entry, index posting, memory record) is shared between the two users' sessions without passing through the same `check_with_epoch` gate on its own next read.

---

## 8. Traceability

Every interface in this document is cited against at least one REQ-ID in `11-REQUIREMENTS-FINAL.md` and at least one data contract in `12-DATA-ONTOLOGY-EVENT-CONTRACTS.md`: the compiler (§1) carries `QueryPlan`/`TenantContext`/`TrustedScope` (12 §1, §2, §7); the MCP contract (§2) carries `McpToolManifest`/`ActionIntent` (12 §11); the `AuthzPort` (§3) wraps `FactPremise`/`PolicyEpochToken` (12 §1, §7); the abstention contract (§4) carries `Evidence`/`EvidenceLocator` (12 §6). No interface here is specified without a corresponding data shape in document 12, and no data shape in document 12 is left without a carrying interface here, except the purely storage-side contracts (bitemporal index, audit hash-chain, typed mutation constraints) that have no API surface by design — they are enforced at the gateway (§5), not exposed as an endpoint.
