# ADR-001: G2 source-event compatibility and revision model

- Status: accepted
- Date: 2026-10-03
- Requirements: G2-ARCH-001..015, G2-EKAF-003, G2-EVOL-009, G2-EVENT-001

## Decision

EOIP retains `SourceEvent` v1 for existing Jira, Git, GitLab and code ingestion and adds
`SourceEventV2` as the acquisition-fabric boundary contract. The deterministic
`upgrade_source_event` adapter preserves the v1 event ID, payload, capture time and content hash.
New or upgraded connectors must emit v2. Source-specific adapters never mutate HugeGraph.

V2 adds operation, source instance, event time, cursor, permission metadata and an optional
payload reference. Delete events may omit payload; other operations require payload or a payload
reference. Payload references point to capture storage and must not contain credentials.

The revision model is hybrid:

1. Current entity and relationship values remain directly queryable on their normal graph records.
2. Immutable `GraphRevision` and `RelationshipRevision` records retain historical values and
   validity intervals.
3. Every revision references its originating SourceEvent and optionally its previous revision.
4. A current revision has an open `valid_to`; an expired revision has a closed `valid_to`.
5. The evolution engine must validate a replacement before closing the current revision.

This balances bounded current-state traversals with reproducible as-of queries. HugeGraph schema
changes for revision vertices/edges will be introduced with the G2-P2 evolution engine, after the
contracts are stable.

## Compatibility changes

| Existing surface | Compatibility behavior |
|---|---|
| `SourceEvent` v1 JSON/schema | Unchanged |
| Existing Jira/Git/GitLab/code capture | Continues to emit/read v1 |
| Confluence/ServiceNow REST capture | Emits v2; existing ingestion uses compatibility properties |
| Event content hash | v1 `payload_hash`; v2 `content_hash` plus equal serialized `payload_hash` compatibility field |
| Raw capture deduplication | Accepts either serialized hash field |
| Connector implementations | New adapters implement `SourceConnector`; legacy adapters migrate incrementally |
| Current graph queries | Unchanged until G2-P2 adds as-of/diff operations |

## Security and operations

The source registry persists only non-secret configuration and opaque `env://`, `file://`, or
`vault://` secret references. Inline secret-like configuration keys are rejected. Registry writes
use same-directory atomic replacement. API operations remain behind the existing bearer-token and
audit middleware.
