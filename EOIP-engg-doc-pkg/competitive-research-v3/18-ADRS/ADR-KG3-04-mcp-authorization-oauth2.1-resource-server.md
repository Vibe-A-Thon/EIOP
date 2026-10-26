# ADR-KG3-04: MCP Authorization — Per-User OAuth 2.1 Resource Server

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-04 |
| Gap | GAP-09 (`07-GAP-REGISTER.md`, forced P0, Critical severity, score 4.1 — second-highest score in the register) |
| Capability | CAP-59 (MCP / agent tool interface) |

## Context

`apps/mcp/main.py` exposes 18 read-oriented tools (unchanged in count at HEAD, BL-47) and, on its own terms, does real work: every response is wrapped with an uncertainty envelope (`eoip.agents.uncertainty_protocol.annotate_mcp_payload`). But authentication is a single shared bootstrap API token (`main.py:220-223`, `hmac.compare_digest` against one static value) — every MCP caller, regardless of which human or agent is actually behind it, acts as that one token's principal. No per-user identity or tenant context propagates through MCP at all. This is a textbook confused-deputy risk: any agent or integration holding the shared token can act with the full privilege of whatever that token grants, and the platform cannot distinguish or audit which human initiated a given tool call. Separately, `tools_contract/mcp_server.py` (`EOIPMCPServer`) implements a richer model — ontology/graph/action tools, an identity-spoof argument check, budgets, a provenance log — but it is in-process only, exercised solely by `tests/acceptance/test_developer_ecosystem_acceptance.py`, and is not mounted by `apps/mcp`. It also trusts a `caller_identity` dict supplied by the host and dereferences it even when `None` is passed (`invoke_tool`, `:279`) — so even the richer, unmounted implementation has its own gap.

## Options considered

1. **Quick integration** — issue per-deployment tokens instead of one global token, so at least different customer deployments are distinguishable, without yet solving per-user attribution within a deployment.
2. **Pragmatic native enhancement** — an OAuth 2.1 resource-server model, per the MCP specification's own authorization extension, where each agent or user carries its own token mapped to the existing RBAC/ABAC role model (`authz/core.py`, `apps/api/route_policy.py`) rather than a parallel authorization system.
3. **Long-term** — signed, hash-pinned tool manifests (closing the tool-poisoning risk identified in C09-mcp INV-mcp-01) plus server-enforced tool annotations (read-only hints that the server itself verifies, not just a label the client trusts).

## Options rejected and why

Option 1 alone is rejected as insufficient: it solves "which customer" but not "which user," and GAP-02 (source-ACL enforcement) depends on knowing the calling principal to filter correctly — a per-deployment token cannot support per-user ACL filtering, so shipping only option 1 would leave MCP permanently unable to participate in the GAP-02 fix regardless of how well that fix is built elsewhere.

## Decision

Adopt option 2 now as the primary fix — an OAuth 2.1 resource server in front of `apps/mcp`, issuing scoped tokens per user/agent that map onto the existing role classes (ADMIN/READ/ANALYST/WRITE from `apps/api/route_policy.py`), so MCP authorization reuses the platform's one authorization model rather than inventing a second one. Adopt option 3 alongside, not after, because tool-poisoning and confused-deputy risk are both live concerns the same body of research (C09-mcp) raises together. The unmounted `EOIPMCPServer`/`tools_contract/mcp_server.py` is folded into this effort rather than mounted as-is: its `caller_identity` dereference-of-None defect (`:279`) must be fixed as part of making it the real MCP implementation, not inherited.

## Consequences

**Positive:** closes the platform's second-highest-scoring forced P0 gap. Makes the MCP surface composable with the GAP-02 ACL fix (ADR-KG3-01) rather than a permanent exception to it — today, even a perfect GAP-02 fix in the REST API would not protect MCP, since MCP forwards to REST under one shared principal. No researched competitor's MCP server (Neo4j, Memgraph, FalkorDB, Neptune all have MCP servers per CAP-59's evidence row) is documented as combining per-user OAuth 2.1 with ACL-aware tools — this would be a genuine, currently unclaimed differentiator if it ships and passes BM-18.

**Negative:** every existing MCP integration built against the shared-token model breaks and must be migrated to per-user tokens — this is a breaking change for any customer who has already automated against the current MCP endpoint. The OAuth 2.1 resource-server flow adds a real implementation surface (token issuance, refresh, scope mapping) that does not exist today.

## Reversibility

Medium. The authorization layer is additive in principle (tokens can be validated at a gateway in front of the existing tool handlers without rewriting the handlers themselves), but any customer integration built against the shared-token model requires migration work on both sides once the change ships — this is not a config flip for an already-integrated customer.
