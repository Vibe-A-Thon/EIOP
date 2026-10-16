# Data Contracts

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Versioned data contracts used across the platform

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Contract rules

All contracts are versioned, additive within a minor version, and validated at process boundaries. Unknown required semantics require a new major contract version. Internal HugeGraph IDs are not external contract identities.

## SourceEvent v1

Schema file: `schemas/source_event.schema.json`

```json
{
  "schema_version": null,
  "event_id": "example",
  "source_system": "example",
  "source_record_id": "example",
  "captured_at": "example",
  "payload_hash": "example",
  "payload": {}
}
```

## NormalizedEntity v1

Schema file: `schemas/normalized_entity.schema.json`

```json
{
  "schema_version": null,
  "canonical_id": "example",
  "entity_type": "example",
  "graph_domain": "example",
  "source_refs": [],
  "properties": {}
}
```

## NormalizedRelationship v1

Schema file: `schemas/normalized_relationship.schema.json`

```json
{
  "schema_version": null,
  "relationship_id": "example",
  "relationship_type": "example",
  "from_id": "example",
  "to_id": "example",
  "evidence_refs": [],
  "creation_status": null
}
```

## GraphMutation v1

Schema file: `schemas/graph_mutation.schema.json`

```json
{
  "mutation_id": "example",
  "operation": null,
  "target_kind": null,
  "payload": {},
  "ingestion_run_id": "example"
}
```

## QueryPlan v1

Schema file: `schemas/query_plan.schema.json`

```json
{
  "intent": null,
  "anchors": [],
  "max_depth": 1,
  "result_limit": 1,
  "evidence_mode": null
}
```

## GraphResult v1

Schema file: `schemas/graph_result.schema.json`

```json
{
  "query_id": "example",
  "nodes": [],
  "edges": [],
  "evidence": [],
  "partial": false
}
```

## RetrievalResult v1

Schema file: `schemas/retrieval_result.schema.json`

```json
{
  "retrieval_id": "example",
  "strategy": "example",
  "contexts": [],
  "evidence_refs": []
}
```

## Evidence v1

Schema file: `schemas/evidence.schema.json`

```json
{
  "evidence_id": "example",
  "source_system": "example",
  "source_ref": "example",
  "captured_at": "example",
  "method": "example"
}
```

## AgentRequest v1

Schema file: `schemas/agent_request.schema.json`

```json
{
  "request_id": "example",
  "agent_id": "example",
  "goal": "example"
}
```

## AgentResult v1

Schema file: `schemas/agent_result.schema.json`

```json
{
  "request_id": "example",
  "status": null,
  "summary": "example",
  "evidence_refs": []
}
```

## ToolRequest v1

Schema file: `schemas/tool_request.schema.json`

```json
{
  "tool_call_id": "example",
  "tool_name": "example",
  "arguments": {}
}
```

## ToolResult v1

Schema file: `schemas/tool_result.schema.json`

```json
{
  "tool_call_id": "example",
  "status": null
}
```

## MemoryRecord v1

Schema file: `schemas/memory_record.schema.json`

```json
{
  "memory_id": "example",
  "kind": "example",
  "scope": "example",
  "owner": "example",
  "source": "example",
  "created_at": "example",
  "provenance_refs": [],
  "classification": "example"
}
```

## AuditEvent v1

Schema file: `schemas/audit_event.schema.json`

```json
{
  "audit_id": "example",
  "timestamp": "example",
  "event_type": "example",
  "actor": "example",
  "correlation_id": "example",
  "outcome": "example"
}
```
