# 12 — Data, Ontology and Event Contracts

| Field | Value |
|---|---|
| Document | 12-DATA-ONTOLOGY-EVENT-CONTRACTS.md |
| Supersedes | The 2026-10-19 placeholder pass at this path; overwritten in full |
| Scope | Canonical types, identity, temporal, provenance, inference, versioning and tenancy schemas needed by the P0/P1 requirements in `11-REQUIREMENTS-FINAL.md` |
| Method | Every type below either **extends** a named file under `packages/eoip/contracts/*.py` / `schemas/*.schema.json` (cited by path) or is marked **NEW**. Field lists use JSON-Schema-like pseudocode, not full schema files. Fields already present in the baseline code are marked `(existing)`; fields this package's requirements add are marked `(added)`. |

## 0. How to read this document

Each section names the REQ-IDs that need the contract, the file it extends or replaces, and whether the change is additive (safe, non-breaking) or a required-field addition (a breaking change to the mutation/write path, deliberately, so that bypassing the guarantee requires bypassing the contract). Contracts already implemented as Pydantic models are cited by their real class name so an implementer opens the right file first.

This package's own baseline audit (`01-SYSTEM-BASELINE.md`, `01a-BASELINE-DELTA-HEAD.md`) found that most of the field-level gaps named in `07-GAP-REGISTER.md` are not missing infrastructure — they are infrastructure that exists in one file (often already well-designed: `contracts/canonical.py TrustedScope` already carries `policy_epoch`; `authz/pdp.py` already composes derivation ACLs) but is not required, not wired to every caller, or not persisted on every backend. The contracts in this document are therefore overwhelmingly **extensions of real code**, not inventions: eleven of the thirteen numbered sections below extend a named existing file; only the typed mutation-gateway constraint layer (§5) and a handful of individual fields (character-offset spans in §6, the bitemporal index in §9, hash-chaining in §10) introduce genuinely new structure. Every NEW type is marked inline so an implementer never has to guess which parts are design and which parts are already running code.

---

## 1. ACL-principal-bearing fact/chunk/edge envelope

**Needed by:** REQ-SEC-04, REQ-SEC-05, REQ-SEC-07, REQ-TEN-01, REQ-MEM-01.
**Extends:** `packages/eoip/contracts/graph_mutation.py GraphMutation` (currently `mutation_id, operation, target_kind, payload, ingestion_run_id` — no ACL field) and `packages/eoip/contracts/source_event.py PermissionMetadata` (currently `principal_refs: list[str]`, `acl_hash`). Also consumed by `packages/eoip/authz/pdp.py FactPremise` (`acl_vector: list[str]`, already defined for derivation checks) and `packages/eoip/contracts/normalized.py NormalizedEntity`/`NormalizedRelationship` (currently no ACL field).

```
AclPrincipalSet:
  acl_principals: list[string]       # (added) tenant-prefixed principal refs, e.g. "tenant:alpha#user:jdoe", "tenant:alpha#role:finance"
  acl_hash: string | null            # (existing, PermissionMetadata) stable hash of the source-system ACL for change detection
  classification: enum[public, internal, confidential, restricted]  # (added) maps to authz/pdp.py clearance levels
  derivation: DerivationRecord | null  # (added, NEW) present only on inferred facts

DerivationRecord:                     # NEW — composition record for derivation-aware ACL (INV-SELF-01 target architecture)
  premise_refs: list[string]          # fact/chunk/edge IDs this assertion was derived from
  composition_rule: enum[intersection, union]  # default "intersection": ACL(E) = ACL(P1) ∩ ACL(P2) ∩ ...
  composed_at: string (RFC 3339 timestamp)

FactEnvelope (extends GraphMutation.payload):
  acl: AclPrincipalSet                # (added, required once REQ-SEC-04 lands)
  tenant_id: string                   # (added, required) see §2
  epistemic_state: KnowledgeState     # (added, required) see §3
  evidence_ref: string                # (existing pattern, Evidence.evidence_id) see §4
```

`validation/gate.py` rejects any `GraphMutation` whose `payload` lacks `acl` or whose `acl.acl_principals` is empty when the source event's `PermissionMetadata.principal_refs` was non-empty (a mutation cannot silently drop a known ACL). Chunks (retrieval/search-index documents) and edges carry the identical `AclPrincipalSet` shape so `retrieval/service.py` and `authz/derivation_acl.py filter_graph_contexts` can apply one evaluation path regardless of asset kind.

---

## 2. Tenant-scoped envelope

**Needed by:** REQ-TEN-01, REQ-SEC-04, REQ-SEC-05, REQ-MEM-01, REQ-ING-05.
**Extends:** `packages/eoip/contracts/tenant_scope.py` (currently an ambient `ContextVar`-based `tenant_scope()`/`current_tenant()` pair with no payload — "never blank," defaults to `_platform`) and `packages/eoip/contracts/canonical.py TrustedScope` (currently `tenant_id, workspace_id, principal_id, principal_type, roles, effective_acls, policy_epoch, delegation_chain, autonomy_level, expires_at` — already close to complete). Also consumed by `packages/eoip/tenancy/isolation.py IsolationPlacement` (`IsolationModel` enum: `SILO | BRIDGE | POOL`, already defined) and `packages/eoip/tenancy/layers.py TenantLayers`/`TenantHandle` (embedded-layer isolation, already implemented).

```
TenantContext:                        # extends GraphStore protocol call signatures (NEW requirement, existing shape)
  tenant_id: string                   # (existing, TrustedScope.tenant_id) never blank — refusal, not a default, if absent
  isolation_model: enum[silo, bridge, pool]  # (existing, IsolationModel)
  placement: BackendPlacement          # (added) resolved physical placement, one per backend kind

BackendPlacement:                     # NEW — what REQ-TEN-01 adds to tenancy/isolation.py
  backend_kind: enum[hugegraph, neo4j, neptune, janusgraph, rdf, memory]
  isolation_unit: string               # e.g. "graph_space:acme", "database:acme_db", "cluster:acme-neptune-1", "named_graph:urn:eoip:tenant:acme"
  native: boolean                      # true if the backend enforces this unit itself (HugeGraph graph space, Neo4j multi-db); false if emulated (Neptune cluster-per-tenant, RDF named graph)
```

Every `GraphStore` protocol method (`graph/store.py:56` — `get_vertex`, `get_neighborhood`, `commit_mutation_batch`, `compile_and_execute_plan`) gains a required `tenant: TenantContext` parameter. A call without a resolved `TenantContext` raises `TenantScopeRequiredError` (NEW exception type, same family as `tenancy/isolation.py PlacementValidationError`) rather than falling through to a default scope — this is the mechanism that makes REQ-TEN-01 a refusal-by-default guarantee rather than an opt-in one.

---

## 3. Epistemic-state envelope

**Needed by:** REQ-GOV-01, REQ-MEM-01, REQ-ML-03, REQ-GOV-12.
**Extends:** `packages/eoip/contracts/canonical.py KnowledgeState` (existing enum: `ASSERTED | INFERRED | PROPOSED | REJECTED | HISTORICAL`) and `packages/eoip/ai/boundary.py` (`ProposalEvaluation`, `DualPathOrchestrator`, `AgreementState: CORROBORATED | DISPUTED | UNCORROBORATED`, already implemented as application-layer logic only).

```
EpistemicEnvelope:
  epistemic_state: KnowledgeState      # (existing enum, now required on every FactEnvelope/MemoryRecord)
  agreement: AgreementState | null     # (existing enum) set only when a dual-path (deterministic + probabilistic) check ran
  plane: enum[GL0, GL1, GL2, GW, GP]   # (added, NEW) maps to 10-TARGET-REFERENCE-ARCHITECTURE.md §1's five planes:
                                        #   GL0 raw blobs/SourceEvents, GL1 explicit LPG facts, GL2 neural/SHACL schemas,
                                        #   GW wisdom graph, GP isolated prediction plane
  promotion: PromotionRecord | null    # (added, NEW) present once a PROPOSED item is reviewed
  prediction_meta: PredictionMeta | null  # (added, NEW) required when plane = GP (REQ-ML-03 dependency)

PromotionRecord:                      # NEW — feeds provenance/warrant_composition.py
  reviewer_id: string
  decision: enum[approve, reject]
  decided_at: string (RFC 3339)
  rationale: string | null

PredictionMeta:                       # NEW — isolated prediction plane (J8), required before any GP-plane write
  model_run_id: string                 # ties to contracts/warrant.py WarrantGroundKind.MODEL_RUN
  calibration_score: number | null      # null is a legitimate (uncalibrated) state but blocks promotion
  beats_tabular_baseline: boolean | null
```

`validation/gate.py` refuses any `FactEnvelope` whose `epistemic_state` is `ASSERTED` without a `promotion` record present, and any write with `plane = GP` whose `prediction_meta` is absent — this is the storage-level guarantee REQ-GOV-01 adds on top of `ai/boundary.py`'s existing application-level discipline.

---

## 4. Agent-memory record (ACL/tenant/evidence/validity)

**Needed by:** REQ-MEM-01.
**Extends:** `packages/eoip/contracts/memory.py MemoryRecord` (currently `memory_id, kind, scope, owner, source, created_at, ttl_seconds, provenance_refs, confidence, classification, deletion_policy, content` — normative schema `schemas/memory_record.schema.json`; **no** `acl_principals`, **no** `tenant_id`, **no** structured validity window today, confirmed by direct code read).

```
MemoryRecord (v2, extends v1):
  memory_id: string                    # (existing)
  kind: string                         # (existing)
  scope: string                        # (existing) — distinct from tenant_id; kept for backward compatibility
  owner: string                        # (existing)
  source: string                       # (existing)
  created_at: string                   # (existing, default utc_now_iso)
  ttl_seconds: integer | null          # (existing)
  provenance_refs: list[any]           # (existing)
  confidence: number | null            # (existing)
  classification: string               # (existing)
  deletion_policy: string | null       # (existing)
  content: object | null               # (existing)
  acl_principals: list[string]         # (added, required) same shape as §1's AclPrincipalSet.acl_principals
  tenant_id: string                    # (added, required) same shape as §2's TenantContext.tenant_id
  evidence_ref: string                 # (added, required) points to an Evidence record (§6) backing the memory
  valid_from: string (RFC 3339)        # (added, required)
  valid_to: string (RFC 3339) | null   # (added) null = still current; mirrors contracts/revision.py RevisionMetadata's pattern
  epistemic_state: KnowledgeState      # (added, required) default PROPOSED — memory is write-gated the same as graph facts
  policy_epoch_at_write: integer       # (added, required) snapshot of authz/pdp.py PolicyEpochRegistry at write time, re-checked on every read (§7)
```

A memory write without `acl_principals`, `tenant_id` or `evidence_ref` is rejected by the same mutation gateway as graph facts (REQ-MEM-01's "propose-not-write" requirement) — `memory_eng/engine.py`, `reasoning/memory.py` and `agents/memory.py` converge on this one schema instead of each keeping its own ad hoc record shape.

---

## 5. Typed mutation-gateway constraint schema

**Needed by:** REQ-GOV-08 (dependency of REQ-GOV-01).
**Extends:** `packages/eoip/validation/gate.py` (`check_vertex`/`check_edge` — currently label and required-property checks only, per `01-SYSTEM-BASELINE.md` BL-28). **NEW** constraint types below; no existing contract covers cardinality, role or value-range constraints today.

```
TypeConstraint:                        # NEW
  applies_to: enum[vertex_label, edge_label]
  target: string                       # the label this constraint governs, e.g. "Person", "OWNS"

CardinalityConstraint (extends TypeConstraint):   # NEW
  property_name: string
  min_count: integer                   # 0 = optional
  max_count: integer | null            # null = unbounded

RoleConstraint (extends TypeConstraint):          # NEW — TypeDB-pattern (STR-typedb-01), backend-neutral
  role_name: string                    # e.g. "owner", "approver"
  allowed_player_labels: list[string]   # which vertex labels may play this role on this edge label
  min_players: integer
  max_players: integer | null

ValueRangeConstraint (extends TypeConstraint):    # NEW
  property_name: string
  value_type: enum[integer, number, string, date]
  min_value: any | null
  max_value: any | null
  pattern: string | null                # regex, for string types only

ConstraintViolation:                    # NEW — returned by validation/gate.py, not a generic 500
  constraint: TypeConstraint
  mutation_id: string                   # ties to GraphMutation.mutation_id
  reason: string
```

These constraints are evaluated by `validation/gate.py` before any `GraphMutation` reaches `commit_mutation_batch`, backend-neutral by construction (no backend's native schema language is relied on, since HugeGraph/Neo4j/Neptune disagree on what they can express natively) — this is the "typed constraint layer at the mutation gateway" the capability matrix (CAP-08) calls for.

---

## 6. Provenance, evidence and warrant schemas

**Needed by:** REQ-ING-03, REQ-STOR-02, REQ-SEC-04 (evidence_ref), REQ-MEM-01 (evidence_ref).
**Extends:** `packages/eoip/contracts/evidence.py Evidence` (`evidence_id, source_system, source_ref, captured_at, method, parser_version, mapper_version, confidence` — normative `schemas/evidence.schema.json`), `packages/eoip/contracts/canonical.py EvidenceLocator` (`document_id, source_system, source_revision, page_number, slide_number` — already structured but **no character-offset span**), and `packages/eoip/contracts/warrant.py` (`WarrantStatus: OBSERVED | ATTESTED | PREDICTED | GENERATED | HEARSAY | UNKNOWN`; `WarrantGroundKind: GRAPH_NODE | GRAPH_EDGE | GRAPH_PROPERTY | SOURCE_RECORD | DOC_SPAN | TOOL_RECEIPT | ATTESTATION | MODEL_RUN | RULE` — already rich; normative "IP Warrant 1.0").

```
EvidenceLocator (v2, extends canonical.py EvidenceLocator):
  document_id: string                  # (existing)
  source_system: string                # (existing)
  source_revision: string              # (existing)
  page_number: integer | null          # (existing)
  slide_number: integer | null         # (existing)
  char_start: integer | null           # (added, NEW) required when the source is text-extractable
  char_end: integer | null             # (added, NEW)
  parser_version: string | null        # (added) ties to Evidence.parser_version, lets span drift be detected on re-parse
```

Parser-neutral span anchors (REQ-ING-03) are a required pair of fields on `EvidenceLocator`, not a new type — this keeps every extraction tool (Docling, GLiNER, Unstructured, spaCy) emitting the same shape regardless of which one produced the span. `Warrant` records (per `warrant.py`, RFC 8785 canonical-JSON-hashed, already implemented) are unchanged in shape; REQ-STOR-02's bulk-load provenance requirement is satisfied by ensuring every record a native bulk loader writes carries a `Warrant` with `ground_kind = SOURCE_RECORD` pointing at the originating `SourceEvent`, not a synthetic one generated after the fact.

---

## 7. Inference and derivation-ACL schema

**Needed by:** REQ-SEC-04, REQ-SEC-05, REQ-SEC-07, REQ-GOV-01.
**Extends:** `packages/eoip/authz/pdp.py FactPremise` (`acl_vector: list[str]`, `PolicyEpochRegistry`, `can_read(...)` — already implemented) and `packages/eoip/authz/derivation_acl.py TraversalHop`/`TraversalPath` (`composite_acl_vector()`, `max_classification()`, `DerivationACLEvaluator.filter_graph_contexts` — already implemented, reachable only from one optional branch today per BL-18).

```
PolicyEpochToken:                      # extends canonical.py TrustedScope.policy_epoch (existing int field)
  tenant_id: string                    # (existing, TrustedScope.tenant_id)
  policy_epoch: integer                # (existing) monotonically increasing per tenant
  issued_at: string (RFC 3339)         # (added, NEW) when this token was attached to a cache key / index entry / memory read

CacheEntryEnvelope:                    # NEW — wraps any cached retrieval/search-index/memory result
  payload_ref: string                  # pointer to the cached object
  policy_epoch_at_cache: integer       # snapshot taken when the entry was written
  tenant_id: string

StalenessCheck(entry: CacheEntryEnvelope, registry: PolicyEpochRegistry) -> boolean:
  # returns true (STALE) if entry.policy_epoch_at_cache < registry.current_epoch(entry.tenant_id)
  # a STALE result is re-evaluated against can_read(), never served directly (REQ-SEC-07)
```

`DerivationFilterResult` (existing, `authz/derivation_acl.py:74`) is unchanged in shape; what REQ-SEC-05 changes is that `filter_graph_contexts` becomes a mandatory call in every retrieval branch (`retrieval/service.py` keyword/vector/hybrid/graph-traversal), not an optional one gated on a `scope` argument a caller can omit.

---

## 8. Identity and entity-resolution schema

**Needed by:** REQ-ING-05, REQ-ING-06.
**Extends:** `packages/eoip/contracts/normalized.py NormalizedEntity`/`NormalizedRelationship` (`canonical_id, entity_type, graph_domain, source_refs, creation_status: DETERMINISTIC | INFERRED | AMBIGUOUS | MANUAL | HUMAN_CONFIRMED, confidence, properties` — already implemented) and `packages/eoip/identity/merger.py IdentityMergeLedger` (immutable merge ledger with high-impact approval gate, already implemented but library-only per `01a-BASELINE-DELTA-HEAD.md` BL-34).

```
DeterministicIdentityKey:              # NEW — extends identity/resolver.py beyond person-only
  entity_type: string                  # no longer restricted to "person"
  tenant_id: string                    # (existing pattern, TenantContext.tenant_id)
  canonical_id: string                 # hash(tenant_id, natural_key) — collision policy documented per entity_type

ProbabilisticMatchCandidate:           # NEW — ER port output (REQ-ING-06), feeds identity/candidates.py review queue
  candidate_id: string
  left_ref: string                     # canonical_id or source ref
  right_ref: string
  match_score: number                  # Fellegi-Sunter posterior from the integrated Splink engine
  decision: enum[match, review, non_match]  # thresholds: match >= 0.85, review >= 0.60, else non_match (existing thresholds in er/splink_engine.py, now backed by a trained model)
  reviewer_verdict: enum[approve, reject] | null  # (added) feeds active-learning retraining (STR-zingg-01 pattern)

MergeRecord (extends identity/merger.py IdentityMergeLedger entries):
  absorbed_id: string
  surviving_id: string
  reversible: boolean                  # (existing) true unless a high-impact threshold was crossed
  approval: PromotionRecord | null      # (added) reuses §3's PromotionRecord shape for consistency
```

---

## 9. Temporal and versioning schema

**Needed by:** REQ-GOV-09, REQ-GOV-03.
**Extends:** `packages/eoip/contracts/revision.py RevisionMetadata` (`revision_id, valid_from, valid_to, observed_at, is_current, previous_revision, source_version` — already implemented, with a validator that forbids a current revision from carrying `valid_to`) and `GraphRevision`/`RelationshipRevision` (`schema_version, canonical_id, entity_type, revision, properties, source_event_id`). Also `packages/eoip/graph/bitemporal.py` (reconstruction logic, already implemented, unindexed per GAP-16).

```
BitemporalIndexEntry:                  # NEW — the index REQ-GOV-09 adds
  canonical_id: string
  valid_time_range: [string, string | null]      # [valid_from, valid_to]
  transaction_time_range: [string, string | null] # [observed_at, superseded_at]
  revision_id: string                   # (existing, RevisionMetadata.revision_id)

ClaimRecord:                            # extends truth/engine.py TruthStore in-memory shape, now persisted (REQ-GOV-03)
  claim_id: string
  subject_ref: string                   # canonical_id this claim is about
  asserted_value: any
  source_system: string                 # e.g. "confluence", "servicenow"
  asserted_at: string (RFC 3339)
  qualifier: string | null              # (added) Wikidata-pattern (STR-wikidata-01): scope of the claim
  rank: enum[preferred, normal, deprecated] | null  # (added) Wikidata-pattern
  contradiction_of: list[string]        # other claim_ids this one disagrees with
  resolution: ResolutionDecision | null

ResolutionDecision:                     # NEW
  decided_value: any
  decided_by: string
  decided_at: string (RFC 3339)
  evidence_refs: list[string]           # ties to §6 Evidence
```

An as-of query against `BitemporalIndexEntry` answers "what was true, and what did we know, at time T" (J2/J3) without reconstructing full revision chains at read time — the index is additive over `graph/bitemporal.py`'s existing reconstruction function, used as a cache, not a replacement for the underlying revision log.

---

## 10. Audit schema

**Needed by:** REQ-SEC-10.
**Extends:** `packages/eoip/contracts/audit.py AuditEvent` (`audit_id, timestamp, event_type, actor, correlation_id, resource_refs, outcome, reason_code, safe_summary` — normative `schemas/audit_event.schema.json`, already implemented, not currently hash-chained).

```
AuditEvent (v2, extends v1):
  audit_id: string                      # (existing)
  timestamp: string                     # (existing)
  event_type: string                    # (existing)
  actor: string                         # (existing)
  correlation_id: string                 # (existing)
  resource_refs: list | null            # (existing)
  outcome: string                        # (existing)
  reason_code: string | null             # (existing)
  safe_summary: string | null            # (existing) — never hidden chain-of-thought, per the module docstring
  prev_hash: string                      # (added, required) RFC 8785 canonical-JSON hash of the immediately preceding AuditEvent for this tenant
  this_hash: string                      # (added, required) hash of this event's canonicalised fields including prev_hash
  signature: string | null               # (added) present on signed exports only
```

Hash-chaining reuses the `rfc8785` canonicalisation already a runtime dependency (per `01a-BASELINE-DELTA-HEAD.md` §0.3, used by `contracts/warrant.py` and `contracts/aspeii.py`) rather than introducing a second canonicalisation scheme — a single modified historical record breaks the chain at verification time, which is the falsifiable test in REQ-SEC-10 / BM-18.

---

## 11. Action-intent and tool-contract versioning

**Needed by:** REQ-SEC-03, REQ-MEM-01 (propose-not-write promotion), REQ-GOV-01 (promotion workflow parity with memory).
**Extends:** `packages/eoip/contracts/tool.py ToolContract` (`schema_version, name, version, description, risk_level: R0..R4, read_only, reversible, approval_required, timeout_seconds, input_schema` — already implemented, with a validator that forces `approval_required = true` for non-read-only tools above `R1`), `ToolRequest`/`ToolResult`, `packages/eoip/contracts/agent.py AgentBudgets`/`AgentContract` (step/token/recursion budgets, already implemented), and `packages/eoip/contracts/aspeii.py` (RFC 8785 canonical digesting of action intents, `ActionEffectClass: READ_ONLY | ADVISORY | INTERNAL_WRITE | EXTERNAL_WRITE | IRREVERSIBLE`, already implemented for the propose/approve/execute two-phase pattern in `actions/engine.py`, library-only per BL-NB-03).

The reason this family of contracts matters for document 12, not only document 13's API surface, is that **agent memory writes (REQ-MEM-01) and graph-fact promotions (REQ-GOV-01) are specified to go through the same propose-not-write discipline `actions/engine.py` already implements for governed tool actions** — so the schema needs to be shared, not reinvented twice. A memory write or a fact promotion is, structurally, an `ActionIntent` whose `effect_class` is `INTERNAL_WRITE`, digested and bound the same way a tool call's intent is:

```
ActionIntent (packages/eoip/contracts/aspeii.py pattern, reused — not duplicated — by memory/fact promotion):
  action_id: string
  effect_class: ActionEffectClass       # (existing enum) INTERNAL_WRITE for memory/fact promotion
  canonicalization_version: string      # (existing) "rfc8785-jcs-1"
  intent_digest: string                 # (existing) RFC 8785 canonical-JSON hash, domain-separated (ACTION_DOMAIN_SEPARATOR)
  approval: ApprovalState               # (existing) AVAILABLE | CONSUMED | REVOKED | EXPIRED

ToolContract (extended for REQ-SEC-03):
  schema_version: string                 # (existing)
  name: string                           # (existing)
  risk_level: enum[R0,R1,R2,R3,R4]       # (existing)
  read_only: boolean                     # (existing)
  acl_scope: list[string]                # (added, NEW) required principal scope to invoke this tool, same shape as §1 AclPrincipalSet.acl_principals
  manifest_digest: string                 # (added, NEW) RFC 8785 hash of the tool's own definition, re-verified by the MCP client before each call
```

This is the one place the data-contract document and the API/query/security-contract document (13) deliberately overlap: the `ToolContract`/`ActionIntent` shape is defined here because it is a *data* contract consumed by both the mutation gateway (memory and fact promotion) and the MCP tool surface (document 13 §2); document 13 specifies the transport (OAuth 2.1 resource server, per-tool annotation enforcement) that carries this same shape over the wire.

---

## 12. Cross-reference summary

| Contract (file) | New/changed fields | REQ-IDs | Status today |
|---|---|---|---|
| `contracts/graph_mutation.py GraphMutation` | `+acl`, `+tenant_id`, `+epistemic_state`, `+evidence_ref` on payload | SEC-04, TEN-01, GOV-01 | Implemented, additive change |
| `contracts/source_event.py PermissionMetadata` | unchanged shape, now a mandatory upstream input | SEC-04 | Implemented |
| `authz/pdp.py FactPremise`, `PolicyEpochRegistry` | unchanged shape, now mandatory call sites | SEC-05, SEC-07 | Implemented (library) |
| `authz/derivation_acl.py` | unchanged shape, mandatory call sites | SEC-05 | Implemented (library, one caller today) |
| `contracts/tenant_scope.py`, `tenancy/isolation.py` | `+BackendPlacement` (NEW) | TEN-01 | Partial → required |
| `contracts/canonical.py TrustedScope` | unchanged shape, consumed by every protocol call | TEN-01, SEC-07 | Implemented |
| `contracts/canonical.py KnowledgeState` | `+plane`, `+promotion`, `+prediction_meta` (NEW) | GOV-01, ML-03 | Implemented (enum) → extended |
| `contracts/memory.py MemoryRecord` | `+acl_principals`, `+tenant_id`, `+evidence_ref`, `+valid_from/valid_to`, `+epistemic_state`, `+policy_epoch_at_write` | MEM-01 | Implemented v1 → v2 |
| `validation/gate.py` | `+CardinalityConstraint`, `+RoleConstraint`, `+ValueRangeConstraint` (NEW) | GOV-08 | Implemented (label/required-property only) → extended |
| `contracts/evidence.py Evidence`, `canonical.py EvidenceLocator` | `+char_start/char_end` (NEW) | ING-03 | Implemented → extended |
| `contracts/warrant.py Warrant` | unchanged shape | STOR-02 | Implemented |
| `contracts/normalized.py NormalizedEntity/Relationship` | unchanged shape, `+DeterministicIdentityKey` scope (NEW) | ING-05 | Implemented |
| `identity/merger.py IdentityMergeLedger` | `+ProbabilisticMatchCandidate.reviewer_verdict` (NEW) | ING-06 | Implemented (library) |
| `contracts/revision.py RevisionMetadata`, `graph/bitemporal.py` | `+BitemporalIndexEntry` (NEW) | GOV-09 | Implemented → indexed |
| `truth/engine.py TruthStore` | `+ClaimRecord.qualifier/rank`, `+ResolutionDecision` (NEW), now persisted | GOV-03 | Implemented (in-memory) → persisted |
| `contracts/audit.py AuditEvent` | `+prev_hash`, `+this_hash`, `+signature` (NEW) | SEC-10 | Implemented → hash-chained |
| `contracts/tool.py ToolContract`, `contracts/aspeii.py ActionIntent` | `+acl_scope`, `+manifest_digest` (NEW) | SEC-03, MEM-01, GOV-01 | Implemented (library) → required fields, shared with memory/fact promotion |
| `query_plan`/AST schemas | see `13-API-QUERY-AGENT-SECURITY-CONTRACTS.md` §1 | QRY-02, QRY-03, QRY-05, SEC-06 | Covered in document 13 |
