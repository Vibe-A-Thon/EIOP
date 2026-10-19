# 12 — Data, Ontology & Event Contracts (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 12-DATA-ONTOLOGY-EVENT-CONTRACTS.md |
| Standards | RFC 8785 (JCS), W3C RDF 1.1, W3C PROV-O, JSON Schema Draft 2020-12 |
| Verification Cutoff | 2026-10-18 UTC |
| Status | Canonical Data Schema Contracts |

---

## 1. SourceEvent v2 Contract (`schemas/source_event.v2.json`)
Every external event ingested by KnowGridFlow conforms to this schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SourceEventV2",
  "type": "object",
  "required": ["event_id", "source_type", "tenant_id", "timestamp", "entity_type", "entity_key", "payload", "permission_metadata"],
  "properties": {
    "event_id": {"type": "string", "pattern": "^evt_[a-f0-9]{32}$"},
    "source_type": {"type": "string", "enum": ["jira", "gitlab", "github", "servicenow", "confluence", "slack", "s3", "sql", "file"]},
    "tenant_id": {"type": "string", "minLength": 3, "maxLength": 64},
    "timestamp": {"type": "integer", "description": "Epoch milliseconds (RFC 8785 strict integer)"},
    "entity_type": {"type": "string"},
    "entity_key": {"type": "string"},
    "operation": {"type": "string", "enum": ["upsert", "delete", "tombstone"]},
    "payload": {"type": "object"},
    "permission_metadata": {
      "type": "object",
      "required": ["source_acl", "acl_hash"],
      "properties": {
        "source_acl": {"type": "array", "items": {"type": "string"}},
        "acl_hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"}
      }
    },
    "evidence_locator": {
      "type": "object",
      "properties": {
        "uri": {"type": "string"},
        "line_start": {"type": "integer"},
        "line_end": {"type": "integer"},
        "byte_offset": {"type": "integer"}
      }
    }
  },
  "additionalProperties": false
}
```

---

## 2. Derivation-Aware Claim Assertion Contract (`schemas/claim_assertion.json`)
Every fact in the graph carries explicit epistemic status and derivation ACLs:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ClaimAssertion",
  "type": "object",
  "required": ["claim_id", "subject", "predicate", "object", "epistemic_status", "confidence", "derivation_acls", "warrant_id"],
  "properties": {
    "claim_id": {"type": "string", "pattern": "^clm_[a-f0-9]{32}$"},
    "subject": {"type": "string"},
    "predicate": {"type": "string"},
    "object": {"type": "string"},
    "epistemic_status": {
      "type": "string",
      "enum": ["OBSERVED_FACT", "INFERRED_RULE", "PREDICTED_ML", "HUMAN_APPROVED", "DISPUTED"]
    },
    "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
    "premises": {
      "type": "array",
      "items": {"type": "string", "pattern": "^clm_[a-f0-9]{32}$"}
    },
    "derivation_acls": {
      "type": "array",
      "items": {"type": "string"}
    },
    "policy_epoch": {"type": "integer"},
    "warrant_id": {"type": "string", "pattern": "^wr1_[a-f0-9]{64}$"},
    "bitemporal": {
      "type": "object",
      "required": ["valid_from", "tx_from"],
      "properties": {
        "valid_from": {"type": "integer"},
        "valid_to": {"type": ["integer", "null"]},
        "tx_from": {"type": "integer"},
        "tx_to": {"type": ["integer", "null"]}
      }
    }
  },
  "additionalProperties": false
}
```

---

## 3. Cryptographic Merkle Warrant Contract (`wr1_...`)
Every committed state mutation emits a tamper-evident warrant:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MerkleWarrant",
  "type": "object",
  "required": ["warrant_id", "prev_warrant_hash", "tenant_id", "root_merkle_sha256", "timestamp_ms", "mutation_count"],
  "properties": {
    "warrant_id": {"type": "string", "pattern": "^wr1_[a-f0-9]{64}$"},
    "prev_warrant_hash": {"type": "string", "pattern": "^(wr1_)?[a-f0-9]{64}$"},
    "tenant_id": {"type": "string"},
    "root_merkle_sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
    "timestamp_ms": {"type": "integer"},
    "mutation_count": {"type": "integer"},
    "producer": {"type": "string"}
  },
  "additionalProperties": false
}
```
