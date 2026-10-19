# 13 — API, Query, Agent & Security Contracts (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 13-API-QUERY-AGENT-SECURITY-CONTRACTS.md |
| Protocols | REST OpenAPI 3.1, Model Context Protocol (MCP), WebSocket |
| Verification Cutoff | 2026-10-18 UTC |
| Status | Canonical API & Interface Contracts |

---

## 1. Portable QueryPlan v2 IR Specification
The user-facing query coordinator compiles structured QueryPlans across heterogeneous backends:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "QueryPlanV2",
  "type": "object",
  "required": ["intent", "target_backend", "root_selection", "traversal_steps", "limits"],
  "properties": {
    "intent": {
      "type": "string",
      "enum": ["NEIGHBORHOOD", "SHORTEST_PATH", "CYPHER_MATCH", "SPARQL_SELECT", "IMPACT_RADIUS", "DIGITAL_THREAD"]
    },
    "target_backend": {
      "type": "string",
      "enum": ["hugegraph", "neo4j", "neptune", "memory", "auto"]
    },
    "root_selection": {
      "type": "object",
      "required": ["entity_type", "match_criteria"],
      "properties": {
        "entity_type": {"type": "string"},
        "match_criteria": {"type": "object"}
      }
    },
    "traversal_steps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["direction", "edge_labels"],
        "properties": {
          "direction": {"type": "string", "enum": ["OUT", "IN", "BOTH"]},
          "edge_labels": {"type": "array", "items": {"type": "string"}},
          "filter_predicate": {"type": "string"},
          "depth": {"type": "integer", "maximum": 6}
        }
      }
    },
    "limits": {
      "type": "object",
      "required": ["max_vertices", "max_degree"],
      "properties": {
        "max_vertices": {"type": "integer", "default": 200},
        "max_degree": {"type": "integer", "default": 500},
        "timeout_ms": {"type": "integer", "default": 10000}
      }
    }
  }
}
```

---

## 2. Model Context Protocol (MCP) Tool Contracts
Exposed via `apps/mcp/main.py` over stdio and SSE for Claude, GitHub Copilot, and Cursor:

| Tool Name | Parameters | Behavior | Security Level |
|---|---|---|---|
| `query_graph(plan)` | `plan: QueryPlanV2` | Executes validated, parameterized QueryPlan | Read-Only (Safe) |
| `get_entity_evidence(entity_id)` | `entity_id: str` | Returns byte-exact source locators & PROV-O claims | Read-Only (Safe) |
| `trace_digital_thread(story_id)` | `story_id: str` | Traces Story -> Commit -> Code -> Service -> Incident | Read-Only (Safe) |
| `suggest_queries(user_prompt)` | `user_prompt: str` | Returns 3 ranked candidate QueryPlans | Read-Only (Safe) |
| `propose_action(spec)` | `spec: ActionWritebackSpec` | Generates dry-run simulation & review ticket | Read-Only (Proposal) |
| `execute_approved_action(ticket_id)` | `ticket_id: str, signature: str` | Two-phase transactional execution of approved writeback | Dual-Key Human Approval |

---

## 3. Natural Language Query Suggestion API
`POST /suggest/candidates`

**Request:**
```json
{
  "user_prompt": "What services will break if I deprecate the UserAuth class?",
  "tenant_id": "tenant_alpha",
  "max_candidates": 3
}
```

**Response:**
```json
{
  "status": "success",
  "candidates": [
    {
      "candidate_id": "cand_01",
      "paraphrase": "Find all services with downstream call dependencies on UserAuth.authenticate()",
      "intent": "IMPACT_RADIUS",
      "estimated_hops": 3,
      "estimated_records": 14,
      "confidence": 0.94,
      "query_plan_preview": {
        "intent": "IMPACT_RADIUS",
        "root_selection": {"entity_type": "Class", "match_criteria": {"name": "UserAuth"}},
        "traversal_steps": [{"direction": "IN", "edge_labels": ["CALLS", "DEPENDS_ON"], "depth": 3}]
      }
    }
  ]
}
```
