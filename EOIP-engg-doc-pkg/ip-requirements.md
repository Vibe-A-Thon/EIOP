# ip-requirements.md
## KGF / EOIP — Invention, Warrant Engineering and Neural-Fabric Requirements

| Field | Value |
|---|---|
| Document | `ip-requirements.md` |
| Companion | `ip-requirements-implementation-plan.md` (build order, work packages, evidence protocol) |
| Product | EOIP / KnowGridFlow (KGF): multi-tenant, white-label, local-first enterprise ontology, knowledge graph and "living organization brain" |
| Version | 1.1 |
| Date | 2026-10-17 |
| Change log | 1.1 (2026-10-17): added §22 companion disciplines and maturity, §23 Commitment Engineering (Invention 21), §24 Dissent Engineering (Invention 22), §25 Reflex rules (product feature); updated §1, §4.1, §15, §16, §18, §19, §20. 1.0 (2026-10-16): first issue. |
| Audience | Any AI coding agent (and human reviewers) implementing these features inside the existing KGF codebase |
| Status | Approved for implementation. Patent-sensitive: see §3 (IP handling rules) before writing any public artifact. |

---

## 0. How to use this document

1. Read this whole file before writing code. Then read `ip-requirements-implementation-plan.md`, which tells you the order of work and how completion is proven.
2. Every requirement has a stable ID: `REQ-<AREA>-<NNN>`. Use the ID in branch names, commit messages, code comments at the entry point of the implementing module, test names, and evidence folders.
3. Keywords: **MUST** = mandatory for completion. **SHOULD** = mandatory unless a Decision Record (DR, §0.4) explains why not and the owner accepts it. **MAY** = optional.
4. All numeric parameters in this document are **defaults that MUST be implemented as tenant-scoped configuration** with the exact key names given. Do not hard-code them.
5. Where this document gives an exact schema, enum, endpoint, event or metric name, use it exactly.

### 0.1 No-assumption rule

The coding agent MUST NOT invent behaviour that this document does not specify. When the repository lacks something this document needs, follow the **Absent-capability rule** written in the relevant section (each one says what to build). When code and this document disagree:

- If the existing behaviour is documented elsewhere in the repository as a requirement, log a `CONFLICT-IP-NNN` entry in the progress ledger with both citations and stop work on that requirement only. Continue with other work packages.
- Otherwise this document wins.

### 0.2 Completion is proven by evidence, not by code or tests

A requirement is complete **only** when its Evidence Pack (§17) has been produced from a running KGF instance and accepted by an independent verification pass. The following are **never sufficient on their own**:

- a file path, function name, class name or commit hash;
- the existence of a test file, or a test count;
- a green CI badge;
- an agent's statement that something is done.

Status values (use exactly these in the ledger):

| Status | Meaning |
|---|---|
| `NOT-STARTED` | No work yet |
| `IN-PROGRESS` | Being built |
| `CODE-COMPLETE` | Code merged behind its feature flag. **Not done.** |
| `EVIDENCED` | Evidence Pack produced from a running instance |
| `VERIFIED` | Evidence Pack replayed and accepted by an independent verifier. **Only this status counts as done.** |
| `BLOCKED` | Waiting on a named dependency or a `CONFLICT-IP-NNN` |

### 0.3 Glossary

| Term | Meaning in this document |
|---|---|
| Assertion | One fact stored in the KGF graph: a node, an edge, or a property value, with its status, provenance and validity |
| Proposition | One atomic claim produced or consumed by an agent or service at runtime (may or may not be stored as an assertion) |
| Warrant | The justification record attached to a proposition or action (§5) |
| Operator | Any step that transforms propositions: a tool, a query, a rule, a model, a language-model call |
| Checkpoint | A point where warrants are evaluated and work can be blocked: retrieval, rewrite, memory write, handoff, tool call/commit, answer |
| Action | Any operation that changes state inside KGF or in an external system |
| Lease | A time- and version-bound right to rely on a fact (§7) |
| Consequence (κ) | The expected, criticality-weighted impact of an action over the organization graph (§9) |
| Budget | The amount of consequence an agent may spend before human approval is required (§9) |
| Protected fact | A fact that a given principal must not learn, directly or by inference (§10) |
| Meaning release | A versioned ontology change plus the migration of every agent artifact that depends on it (§11) |
| Half-life | Learned time after which a fact of a given ontology type has a 50% chance of having changed (§8) |
| Instance graph / meta-graph / ontology graph | The three graph levels in KGF: entities and relations; types and relation types with counts; formal concepts, axioms and constraints |
| Shadow branch | A copy-on-write branch of a tenant's authoritative graph used for rehearsal and simulation (§13) |
| Principal | A human user, service account, or agent identity that holds permissions |

### 0.4 Decision Records

When this document allows a choice ("SHOULD", "one of", or an absent-capability rule), record a Decision Record in `docs/ip/decisions/DR-IP-NNN.md` with: context, options, decision, consequences, requirement IDs affected. A DR is required evidence for any requirement that relied on it.

---

## 1. Scope

### 1.1 In scope

| Group | Items | Section |
|---|---|---|
| Warrant Engineering core | Warrant model, composition algebra (A1), span-aligned status inheritance (A2), checkpoints, verification tasks | §5, §6 |
| Time | Leases and lease-validated commit (A3); type half-lives (A7) | §7, §8 |
| Consequence | Learned impact propagation (Invention 2); blast-radius budgets (A4) | §9 |
| Inference control | Derivation closure guard (A5) | §10 |
| Meaning migration | Term-to-artifact dependency graph and meaning releases (A6) | §11 |
| Knowledge metabolism | Status-preserving consolidation, metabolism metrics, Brain Health | §12 |
| Shadow branches | Copy-on-write rehearsal | §13 |
| Neural fabric inventions | Inventions 1, 3, 4, 5, 6, 7, 8, 9, 11, 12 | §14 |
| Provenance export | Invention 10, folded into warrants | §6.9 |
| Team processes and metrics | Six governance processes and the discipline metrics | §15, §16 |
| UI | Screens for all of the above | §18 |
| Companion disciplines | Discipline registry, per-discipline metrics, Warrant Engineering maturity level | §22 |
| Commitment Engineering | Warranted commitment ledger for promises agents make (Invention 21) | §23 |
| Dissent Engineering | Independent positions, grounded stance changes and mandatory minority reports (Invention 22) | §24 |
| Reflex rules | Pre-approved deterministic responses without a language model (product feature) | §25 |

### 1.2 Invention register

Tier and verdict come from the prior-art review dated 2026-10-16. The verdict changes **what is claimed and how it is protected**, not whether the feature is built. Every invention below MUST be built.

| Inv | Name | Verdict | Build scope (what this document requires) | Protection | Primary section |
|---|---|---|---|---|---|
| 1 | Neural Ontology Heartbeat | Narrow | Drift detection across three graph levels + drift-type classification + self-healing proposals | Patent (narrowed) | §14.1 |
| 2 | Ontology-constrained neural impact propagation | Keep | Learned per-relation propagation, ontology gates, cross-domain bridges | Patent | §9.1 |
| 3 | Metapath-attention question answering | Keep | Dual deterministic + neural path with ontology validation | Patent | §14.2 |
| 4 | Self-organising ontology (Ontology Advisor) | Narrow | Embedding-cluster type split/merge, relation split, steward queue with impact simulation | Patent (narrowed) | §14.3 |
| 5 | Incident forensics | Rework | Ontology-typed topology-diff fingerprint with graph-diff explanation | Trade secret unless counsel advises otherwise | §14.4 |
| 6 | Cross-tenant federated graph learning | Secret | Opt-in federation with per-classification privacy budgets | Trade secret | §14.5 |
| 7 | Entity survival analysis (Entity Health) | Keep | Vitality vector + survival model + steward feedback | Patent (pending professional search) | §14.6 |
| 8 | Causal layer | Narrow | Separate causal layer + counterfactual path removal on shadow branch | Patent (narrowed) | §14.7 |
| 9 | Smart layout scorer | Secret | Layout recommender with learned aesthetic scorer | Trade secret | §14.8 |
| 10 | Query provenance watermarking | Fold | Signed warrant export and replay verification | Part of Invention 13 | §6.9 |
| 11 | Smart dedup | Narrow | Merge simulation on shadow branch with query/constraint impact | Patent (narrowed) | §14.9 |
| 12 | Semantic zoom | Rework | Abstraction pyramid with cross-level embedding alignment and cross-level query | Low priority patent | §14.10 |
| 13 | Typed warrant propagation | Tier 1 | A1 + A2 + checkpoints | Patent | §5, §6 |
| 14 | Blast-radius budget authorization | Tier 1 | A4 on top of Invention 2 | Patent | §9 |
| 15 | Lease-validated knowledge commit | Tier 1 | A3 + A7 | Patent | §7 |
| 16 | Derivation closure guard | Tier 1 | A5 | Patent | §10 |
| 17 | Meaning migration compiler | Tier 2 | A6 | Patent | §11 |
| 18 | Status-preserving memory consolidation | Tier 2 | Consolidation operator with per-proposition warrants | Patent | §12.1 |
| 19 | Shadow-branch rehearsal | Tier 2 | Copy-on-write branch + simulated tools + impact diff | Patent | §13 |
| 20 | Type half-life re-verification scheduler | Tier 3 | A7 + verification scheduling | Patent with Invention 7 | §8 |
| 21 | Warranted commitment ledger | Tier 2 | Commitments as graph records with authority checks, evidence-based fulfilment, transfer on agent retirement, commit-time conflict checks | Patent (run a professional search first; promise-tracking is discussed publicly in 2026) | §23 |
| 22 | Warranted minority reports | Tier 3 | Independent first-round positions, the no-upgrade rule applied to stance changes, mandatory minority reports with revisit triggers | Patent or defensive publication (research on agent disagreement is very active) | §24 |
| — | Reflex rules | Feature | Deterministic, pre-approved responses on known conditions, through the commit checkpoint | Not claimed | §25 |

### 1.3 Out of scope

- Filing patents, drafting claims, or legal review (owner's responsibility).
- Replacing the KGF graph databases, vector databases or query languages. All work uses KGF's existing abstraction layers (§4.2).
- Sending any tenant data to an external LLM. All models in this document run locally or on tenant-approved self-hosted endpoints (§4.6).

---

## 2. Product constraints that bind every requirement

| ID | Requirement |
|---|---|
| REQ-PLT-001 | Every new table, collection, node label, edge type, index, cache key, queue topic, file path, metric label and log line MUST carry `tenant_id`. No query may run without a tenant filter applied by the platform layer, not by callers. |
| REQ-PLT-002 | Every feature in this document MUST be behind a tenant-scoped feature flag named in §19.1, default **off**, switchable at runtime without restart. |
| REQ-PLT-003 | Every feature MUST work with no internet access (local-first). Model files, rule engines and libraries are installed with KGF. |
| REQ-PLT-004 | Every feature MUST work on each graph database KGF supports, through KGF's graph abstraction layer. Database-specific code is allowed only inside adapters. |
| REQ-PLT-005 | No feature may send tenant data to an external model endpoint unless the tenant's existing data-sharing policy explicitly permits that data class for that endpoint. The warrant, SASI, derivation-guard and neural components MUST default to local models. |
| REQ-PLT-006 | Every state-changing API MUST write an audit event (§19.4) with actor, tenant, action, target, warrant id (when applicable) and outcome. |
| REQ-PLT-007 | Every API MUST enforce KGF's existing authentication and RBAC. New permissions are listed in §19.3. |
| REQ-PLT-008 | All timestamps are stored in UTC, ISO-8601 with milliseconds. All ids are UUIDv7 unless this document says otherwise. |
| REQ-PLT-009 | All new services MUST expose health (`/healthz`), readiness (`/readyz`) and Prometheus-format metrics (`/metrics`), and propagate OpenTelemetry trace context. |
| REQ-PLT-010 | Turning a feature flag off MUST restore the pre-feature behaviour of KGF exactly (no data loss, no errors). This is tested by the kill-switch control in §17.3. |

---

## 3. IP handling rules (apply to code, docs, packages and repositories)

| ID | Requirement |
|---|---|
| REQ-IPH-001 | Configuration key `ip.public_release_allowed` (platform-level, default `false`). While `false`, CI MUST fail any job that publishes packages to a public registry, pushes to a remote whose visibility is public, or deploys public documentation that contains files under the IP module paths (§4.3). |
| REQ-IPH-002 | Source files implementing Inventions 1–20 MUST carry the repository's existing licence header. If the repository has no licence header convention, add `Proprietary and confidential. All rights reserved by the rights holder named in LICENSE.` and record a DR. |
| REQ-IPH-003 | Trade-secret material for Inventions 5, 6 and 9, and all tuned thresholds and trained weights for every invention, MUST NOT be committed to the source repository. Store them in the model registry (§14.0.4) with encryption at rest, and load them by reference. Repository files contain only default values from this document. |
| REQ-IPH-004 | Code comments, READMEs and API descriptions MUST describe behaviour, not claim novelty. Do not write "patented", "patent pending" or "novel" anywhere until the owner sets `ip.public_release_allowed=true`. |
| REQ-IPH-005 | Each invention module MUST include an `INVENTION.md` file (internal, not published) listing: invention number, requirement IDs implemented, algorithm IDs, the date the first working version produced an Evidence Pack, and the name of the person who directed the work. This supports the owner's dated invention records. |

---

## 4. Architecture

### 4.1 New logical components

| Component | Responsibility | Depends on |
|---|---|---|
| `warrant-service` | Warrant model, A1 composition, operator registry, checkpoint evaluation, warrant persistence, signed export | graph abstraction, policy store |
| `sasi-engine` | A2 proposition extraction and entailment, status inheritance | local NLI model, `warrant-service` |
| `verification-service` | Verification task queue, resolution by observer call or human attestation | `warrant-service` |
| `lease-manager` | Lease issue, revocation on graph change, commit validation (A3) | change stream, `halflife-service` |
| `halflife-service` | A7 fitting per ontology type, freshness, verification scheduling | revision history |
| `impact-engine` | Invention 2 learned propagation with ontology gates and bridges | `neural-service`, ontology |
| `consequence-service` | A4 κ computation, budgets, authorization, escalations | `impact-engine` |
| `derivation-guard` | A5 closure checks, protected-fact registry, minimum redaction | rule engine, ontology, link predictor |
| `meaning-service` | Ontology diff, agent-artifact registry, term dependency graph, A6 propagation, rewrites, regression gate, meaning releases | ontology versioning, eval runner |
| `metabolism-service` | Consolidation operator (Inv 18), metabolism metrics, Brain Health | `warrant-service`, `halflife-service` |
| `branch-service` | Copy-on-write shadow branches, simulated tools, diff, merge/discard (Inv 19) | graph abstraction |
| `neural-service` | Graph snapshot export, feature pipelines, GNN training/inference, embedding store, model registry; hosts Inventions 1, 3, 4, 5, 7, 8, 9, 11, 12 models | snapshots, GPU/CPU runtime |
| `federation-coordinator` | Invention 6 federated rounds (self-hosted) | `neural-service` |
| `governance-processes` | Scheduling, reports and workflows for the six team processes (§15) | all of the above |
| `ip-ui` | Screens in §18 inside the existing KGF front-end | all APIs |
| `commitment-service` | Commitment ledger, extraction, lifecycle scheduler, fulfilment checks, transfer, commit-time conflict checks (§23) | `warrant-service`, `sasi-engine`, change stream |
| `dissent-service` | Deliberation protocol, positions, stance-change grounding, minority reports, revisit triggers (§24) | `warrant-service`, `sasi-engine`, change stream |
| `reflex-engine` | Reflex rule store, event matching, deterministic execution through the commit checkpoint, dry runs (§25) | `warrant-service`, `consequence-service`, `branch-service` |
| `discipline-registry` | Discipline catalogue, discipline metrics, maturity computation (§22) | all metric sources |

### 4.2 Integration with existing KGF layers

| Existing KGF layer | How these components use it | Absent-capability rule |
|---|---|---|
| Graph abstraction layer (multi-DB) | All graph reads and writes, including warrants stored as graph records | If no abstraction layer exists, create `GraphPort` interface with `read`, `write`, `query`, `subscribe_changes`, `snapshot`, `branch` and implement it for every database KGF currently supports. Record DR. |
| Ontology / schema store | Types, relation types, constraints, criticality, impact weights, blast barriers | If the ontology store lacks the properties in §4.4, add them as ontology annotations. |
| Ingestion pipeline | Emits assertions with status `OBSERVED` and grounds of kind `source_record` | Modify the write path so every ingested assertion gets a warrant (REQ-WAR-020). |
| NL query / Ask the Brain | Becomes Invention 3; answers carry warrants | — |
| Agent runtime / tools | Wrapped by checkpoint SDK (§6.6) | If KGF has no agent runtime, the SDK still ships and is used by KGF's internal LLM features (NL query, report generation, auto-detection). |
| Change history / audit | Source of revision history for A7 and change events for A3 | If writes are not evented, implement the Graph Change Publisher with a transactional outbox (REQ-LSE-002). |
| Model abstraction layer | All LLM, NLI and embedding calls | If absent, create `ModelPort` with `generate`, `embed`, `entail`, `classify`, local-only by default. |
| Front-end app shell | Hosts the screens in §18 | Use the existing design system. If `GUI-UIX-requirements.md` exists in the repository, follow its tokens and components. |

### 4.3 Module layout

Create one module (package/folder) per component in §4.1 under the repository's existing backend source root, named exactly as the component (`warrant_service`, `sasi_engine`, … in languages that disallow hyphens). The binding between component names and real paths is recorded in `docs/ip/ip-binding-map.md` (created in WP-00 of the plan). "IP module paths" in §3 means these folders.

### 4.4 Ontology annotations required

| Annotation | On | Type | Default | Used by |
|---|---|---|---|---|
| `kgf:criticality` | entity type, entity | integer 1–5 | 1 | A4 |
| `kgf:impactWeight` | relation type | float 0–1 | 0.5 | Invention 2 prior |
| `kgf:blastBarrier` | relation type or metapath | boolean | false | Invention 2 gates |
| `kgf:domain` | entity type | string | `default` | Invention 2 bridges, Inv 12 |
| `kgf:dataClass` | entity type, property | enum `public`, `internal`, `confidential`, `restricted` | `internal` | A5, Inv 6, REQ-PLT-005 |
| `kgf:halfLifeDays` | entity type | float | from A7, else 30 | A3, A7 |
| `kgf:protected` | entity type, property, relation type | boolean | false | A5 |
| `kgf:observerSource` | source system | boolean | true for systems of record | A1 operator typing |
| `kgf:impactDirection` | relation type | enum `forward`, `reverse`, `both` | `reverse` for dependency-like relations, else `forward` | Invention 2 |

---

## 5. Warrant model (Invention 13 foundation)

### 5.1 Status enumeration

```text
OBSERVED   — read from a system of record by an Observer operator
ATTESTED   — stated by an identified human principal with authority over the fact
PREDICTED  — produced by a versioned model with a calibrated score
GENERATED  — produced by a language model without new observations
HEARSAY    — from an unverified source or another agent's unwarranted claim
UNKNOWN    — no status could be determined
```

Default order (highest first): `OBSERVED > ATTESTED > PREDICTED > GENERATED > HEARSAY > UNKNOWN`.

| ID | Requirement |
|---|---|
| REQ-WAR-001 | The status order MUST be a tenant configuration `warrant.status_order` (array of the six values). Only swapping `OBSERVED` and `ATTESTED` is permitted; any other order is rejected with error `WAR_INVALID_ORDER`. |
| REQ-WAR-002 | `min(σ1, σ2)` and comparisons MUST use the tenant's configured order. |

### 5.2 Warrant schema

The canonical JSON Schema is below. Store it in the repository as `schemas/warrant.schema.json` and generate typed models from it for every language in the codebase.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "kgf://schemas/warrant/1.0",
  "title": "Warrant",
  "type": "object",
  "required": ["warrant_id", "tenant_id", "subject", "grounds", "status", "validity", "authority", "consequence", "operator", "parents", "created_at", "schema_version"],
  "properties": {
    "warrant_id": {"type": "string", "format": "uuid"},
    "tenant_id": {"type": "string"},
    "schema_version": {"const": "1.0"},
    "subject": {
      "type": "object",
      "required": ["kind", "ref"],
      "properties": {
        "kind": {"enum": ["proposition", "assertion", "action", "answer"]},
        "ref": {"type": "string"},
        "text": {"type": "string", "maxLength": 4000},
        "hash": {"type": "string", "description": "sha256 of normalized text or canonical JSON of the subject"}
      }
    },
    "grounds": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["kind", "id"],
        "properties": {
          "kind": {"enum": ["graph_node", "graph_edge", "graph_property", "source_record", "doc_span", "tool_receipt", "attestation", "model_run", "rule"]},
          "id": {"type": "string"},
          "version": {"type": "string"},
          "span": {"type": "object", "properties": {"start": {"type": "integer"}, "end": {"type": "integer"}}},
          "hash": {"type": "string"}
        }
      }
    },
    "status": {"enum": ["OBSERVED", "ATTESTED", "PREDICTED", "GENERATED", "HEARSAY", "UNKNOWN"]},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "validity": {
      "type": "object",
      "required": ["valid_from"],
      "properties": {
        "valid_from": {"type": "string", "format": "date-time"},
        "valid_to": {"type": ["string", "null"], "format": "date-time"},
        "lease_ids": {"type": "array", "items": {"type": "string"}}
      }
    },
    "authority": {
      "type": "object",
      "required": ["principal_id", "scopes", "delegation_chain"],
      "properties": {
        "principal_id": {"type": "string"},
        "scopes": {"type": "array", "items": {"$ref": "#/$defs/scope"}},
        "delegation_chain": {"type": "array", "items": {"type": "string"}}
      }
    },
    "consequence": {
      "type": "object",
      "required": ["kappa"],
      "properties": {
        "kappa": {"type": "number", "minimum": 0},
        "impact_run_id": {"type": ["string", "null"]},
        "action_class": {"enum": ["READ_ONLY", "ADVISORY", "INTERNAL_WRITE", "EXTERNAL_WRITE", "IRREVERSIBLE"]}
      }
    },
    "operator": {
      "type": "object",
      "required": ["operator_id", "class", "version"],
      "properties": {
        "operator_id": {"type": "string"},
        "class": {"enum": ["OBSERVER", "COMPUTATION", "MODEL", "GENERATOR", "HUMAN"]},
        "version": {"type": "string"}
      }
    },
    "parents": {"type": "array", "items": {"type": "string", "format": "uuid"}},
    "created_at": {"type": "string", "format": "date-time"},
    "signature": {"type": ["string", "null"], "description": "Ed25519 signature over canonical JSON without this field; required on export"}
  },
  "$defs": {
    "scope": {
      "type": "object",
      "required": ["action", "resource_type", "selector"],
      "properties": {
        "action": {"type": "string", "description": "e.g. read, write, delete, execute:<tool_id>"},
        "resource_type": {"type": "string", "description": "ontology type IRI or '*'"},
        "selector": {"type": "string", "description": "KGF filter expression; '*' for all"}
      }
    }
  }
}
```

| ID | Requirement |
|---|---|
| REQ-WAR-010 | `warrant-service` MUST validate every warrant against the schema on write and reject invalid ones with `WAR_SCHEMA_INVALID` and the JSON-pointer of the first failure. |
| REQ-WAR-011 | Warrants are immutable. A change produces a new warrant whose `parents` includes the old one. |
| REQ-WAR-012 | Canonical JSON for hashing and signing MUST follow RFC 8785 (JSON Canonicalization Scheme). |
| REQ-WAR-013 | Warrants for stored assertions MUST be persisted in the graph through the graph abstraction layer as a `Warrant` node linked `(:Warrant)-[:JUSTIFIES]->(assertion)` and `(:Warrant)-[:DERIVED_FROM]->(:Warrant)` for parents. Runtime-only warrants (propositions not stored as assertions) MUST be persisted in a warrant store with tenant-configurable retention `warrant.runtime_retention_days` (default 30). |
| REQ-WAR-014 | `GET /warrants/{id}/lineage?depth=N` MUST return the parent DAG to depth N (default 5, max 20) in under 300 ms p95 for depth 5 on a lineage of up to 1,000 warrants. |

### 5.3 Graph record contract extension

Every assertion record in KGF MUST carry the following (extends the existing record contract):

```json
{
  "entity_id": "service:payment-api",
  "entity_type": "ApplicationService",
  "graph_id": "application-topology",
  "ontology_version": "1.0",
  "graph_version": "g-1042",
  "relationship": {"type": "DEPENDS_ON", "target": "database:customer-db"},
  "assertion": {
    "status": "OBSERVED",
    "warrant_id": "0192f1c4-…",
    "source_system": "service-catalog",
    "source_record_id": "catalog-2381",
    "valid_from": "2026-10-10T10:00:00.000Z",
    "recorded_at": "2026-10-10T10:01:00.000Z",
    "valid_to": null
  },
  "security": {"classification": "internal", "access_policy_id": "policy-services"}
}
```

| ID | Requirement |
|---|---|
| REQ-WAR-020 | The ingestion write path MUST create a warrant (operator class `OBSERVER` when `kgf:observerSource=true` for the source, else `HEARSAY`) for every new or changed assertion, in the same transaction or outbox batch as the assertion. |
| REQ-WAR-021 | A one-time migration MUST create warrants for all existing assertions: existing `OBSERVED` → `OBSERVED` with grounds `source_record`; existing `PREDICTED`/inferred → `PREDICTED` with grounds `model_run` (model id `legacy` if unknown); anything else → `UNKNOWN`. The migration is idempotent and resumable, logs counts per status, and has a dry-run mode. |
| REQ-WAR-022 | An assertion with status `PREDICTED`, `GENERATED`, `HEARSAY` or `UNKNOWN` MUST NOT overwrite or delete an assertion with status `OBSERVED` or `ATTESTED` for the same subject. It is stored alongside, and queries return both with their statuses unless the caller filters. Attempted overwrite returns `WAR_STATUS_DOWNGRADE_WRITE`. |
| REQ-WAR-023 | Bitemporal reconstruction: `GET /graph/as-of?valid_at=…&recorded_at=…` MUST return the assertion set as it was valid and recorded at those times, with their warrants. |

---

## 6. Warrant Composition (A1), SASI (A2) and checkpoints

### 6.1 Operator registry

| ID | Requirement |
|---|---|
| REQ-OPR-001 | Every operator (tool, query template, rule, model, LLM prompt, human approval step) used by KGF features or agents MUST be registered with `operator_id`, `class` (`OBSERVER`, `COMPUTATION`, `MODEL`, `GENERATOR`, `HUMAN`), `version`, `owner`, `description`, `action_class` it can perform, and `approved_by`. |
| REQ-OPR-002 | An unregistered operator invoked through the checkpoint SDK MUST be treated as class `GENERATOR` and its output status capped at `GENERATED`; an `OPR_UNREGISTERED` audit event is written. |
| REQ-OPR-003 | Registering or changing an operator's class requires permission `ip.operator.approve` and creates an entry in the Warrant Review process (§15.1). |
| REQ-OPR-004 | `OBSERVER` class is allowed only for operators that read from a source with `kgf:observerSource=true` or from the KGF graph assertions whose own status is `OBSERVED`. Registration validates this. |

### 6.2 Algorithm A1 — Warrant Composition Algebra

Input: operator `f` (registered), input warrants `W1..Wn` (n ≥ 0), the operator's own receipt grounds `G_f`, the invoking principal's authority `α_f`.

Output: warrant `W_out`.

```text
G_out      = G_f ∪ G_1 ∪ … ∪ G_n                      (deduplicate by (kind,id,version))
status_out =
    OBSERVED                         if f.class = OBSERVER
    ATTESTED                         if f.class = HUMAN and principal has authority over subject
    min(status_1..status_n)          if f.class = COMPUTATION   (n=0 → UNKNOWN)
    min(PREDICTED, min(status_i))    if f.class = MODEL          (n=0 → PREDICTED)
    SASI(f, W_1..W_n)                if f.class = GENERATOR      (per proposition, §6.3)
validity_out.valid_from = max(valid_from_i, now if OBSERVER/HUMAN)
validity_out.valid_to   = min(valid_to_i)  (null treated as +∞)
validity_out.lease_ids  = ∪ lease_ids_i
authority_out.scopes    = α_f.scopes ∩ scopes_1 ∩ … ∩ scopes_n
authority_out.delegation_chain = chain of the input with the longest chain + [principal of f]
consequence_out.kappa   = κ(action) if subject.kind = action (from §9), else max(kappa_i)
confidence_out          = min(confidence_i) for COMPUTATION; model calibrated score for MODEL;
                          SASI score for GENERATOR; 1.0 for OBSERVER/HUMAN
parents                 = [W_1.id … W_n.id]
```

Scope intersection: two scopes intersect when `action` matches (`*` matches all), `resource_type` is equal or one is a subtype of the other in the ontology (result = the more specific), and selectors are combined with logical AND. An empty intersection means no authority.

| ID | Requirement |
|---|---|
| REQ-WCA-001 | `warrant-service` MUST implement A1 exactly as specified, as a pure deterministic function `compose(operator, inputs, receipt_grounds, principal) -> Warrant`, with no I/O except reading the operator registry and ontology subtype relation (both cacheable). |
| REQ-WCA-002 | **No-upgrade rule.** No code path may produce a warrant whose status is higher than allowed by A1. A property-based test MUST generate ≥ 10,000 random operator/input combinations and assert the rule. |
| REQ-WCA-003 | Authority MUST never widen: for every composition, `authority_out.scopes ⊆ α_f.scopes` and `⊆ scopes_i` for each input. Property-based test as above. |
| REQ-WCA-004 | Validity MUST never extend beyond any input's `valid_to`. Property-based test as above. |
| REQ-WCA-005 | `compose` p95 latency < 5 ms in-process for n ≤ 50 inputs and ≤ 200 grounds. |
| REQ-WCA-006 | `POST /warrants/compose` exposes A1 over HTTP for out-of-process agents (request: `operator_id`, `input_warrant_ids[]`, `receipt_grounds[]`, `subject`; response: the stored warrant). |

### 6.3 Algorithm A2 — Span-Aligned Status Inheritance (SASI)

Input: generator output text `y`, input propositions `Q = {q_1..q_r}` each with a warrant.

Steps:

1. **Extract** atomic propositions `p_1..p_m` from `y` using the local model through `ModelPort.generate` with the fixed prompt template `sasi.extract.v1` (stored in the operator registry as a `GENERATOR` operator). Each proposition records its character span in `y`. Max `m` = `sasi.max_propositions` (default 64); if exceeded, the remainder is marked `GENERATED` without checking and a `SASI_TRUNCATED` notice is attached.
2. **Retrieve candidates:** for each `p_j`, select the top `k` = `sasi.candidates_k` (default 5) input propositions by embedding cosine similarity (local embedding model).
3. **Entail:** score `e(q, p_j)` with the local NLI model via `ModelPort.entail` → probability of entailment in [0,1].
4. **Inherit:** `q* = argmax_q e(q, p_j)`. If `e(q*, p_j) ≥ θ` (`sasi.theta`, default 0.85) then `p_j` gets `status(q*)`, the grounds of `q*`, the validity of `q*`, and `confidence = min(conf(q*), e(q*, p_j))`. Otherwise `p_j` gets `GENERATED`, grounds `[model_run]`, confidence `e(q*, p_j)`.
5. **Numbers and dates guard:** if `p_j` contains a number, date, identifier or proper noun that does not appear (after normalization) in `q*`, set `p_j` to `GENERATED` regardless of the entailment score.
6. **Verification tasks:** every `GENERATED` proposition that is later used as a premise of an action with action class `INTERNAL_WRITE` or higher creates a verification task (§6.7).

| ID | Requirement |
|---|---|
| REQ-SAS-001 | `sasi-engine` MUST implement A2 exactly, using only local models by default. Model ids are configuration (`sasi.extract_model`, `sasi.embed_model`, `sasi.nli_model`). |
| REQ-SAS-002 | Every generator call made through the checkpoint SDK MUST pass through SASI before its output leaves the rewrite checkpoint. |
| REQ-SAS-003 | SASI output is a list of `(proposition, span, warrant)`; the UI renders spans coloured by status (§18.2). |
| REQ-SAS-004 | Benchmark dataset `evals/sasi/laundering-v1.jsonl` MUST be created with ≥ 300 hand-checked items: supported paraphrases, unsupported additions, altered numbers, altered names, merged hearsay. Acceptance: on this set, precision of status inheritance ≥ 0.95 (an inherited status is correct) and recall of laundering detection ≥ 0.90 (unsupported propositions marked `GENERATED`). Report both on every model change. |
| REQ-SAS-005 | Latency: p95 < 1.5 s for outputs ≤ 1,500 characters on the reference hardware recorded in DR (CPU-only allowed). Batch NLI calls. |
| REQ-SAS-006 | If the NLI model is unavailable, SASI MUST fail closed: all propositions `GENERATED`, notice `SASI_DEGRADED`, alert raised. |

### 6.4 Action classes and minimum status

| Action class | Examples | Minimum status of every premise | Extra conditions |
|---|---|---|---|
| `READ_ONLY` | Query, view | none | Derivation guard (§10) |
| `ADVISORY` | Answer, report, recommendation | none, but every proposition is labelled with its status | Answer warrant displayed (REQ-CHK-006) |
| `INTERNAL_WRITE` | Write assertion to KGF graph | `PREDICTED` (stored with its own status per REQ-WAR-022) | Leases valid (§7) |
| `EXTERNAL_WRITE` | Tool that changes an external system | `ATTESTED` (i.e., `OBSERVED` or `ATTESTED`) | Leases valid; κ within budget (§9) |
| `IRREVERSIBLE` | Delete, payment, access revocation, production deploy | `OBSERVED` | Leases valid; κ within budget; human approval always |

| ID | Requirement |
|---|---|
| REQ-CHK-001 | The table above MUST be tenant configuration `warrant.min_status_by_action_class`. Changing it requires `ip.policy.admin`. |
| REQ-CHK-002 | Every tool/operator that performs an action MUST declare its action class in the registry. Undeclared → treated as `IRREVERSIBLE`. |

### 6.5 Checkpoints

| Checkpoint | Where | Checks performed (in this order) | On failure |
|---|---|---|---|
| `retrieval` | Any read from KGF graph/vector store into an agent or LLM context | attach warrants; issue leases (§7) for facts used in plans; derivation guard (§10) | withhold fact; audit `DG_BLOCK` |
| `rewrite` | After any GENERATOR operator | SASI (§6.3) | propositions downgraded; never blocked |
| `memory_write` | Agent memory or KGF write of agent output | no-upgrade rule; status-preserving consolidation (§12.1) | reject write `CHK_STATUS_UPGRADE` |
| `handoff` | Agent → agent or agent → sub-agent message | authority intersection; minimum status for the receiver's declared action class | block message `CHK_HANDOFF_DENIED` |
| `commit` | Before any action of class ≥ `INTERNAL_WRITE` executes | minimum status; lease validation (§7); κ vs budget (§9) | block; re-plan or escalate |
| `answer` | Before output to a human or export | attach answer warrant; status labels | never blocked |

| ID | Requirement |
|---|---|
| REQ-CHK-003 | `POST /checkpoints/{checkpoint}/evaluate` (request: `checkpoint`, `subject`, `warrant_ids[]`, `action_class`, `plan_id?`, `principal_id`) returns `{decision: ALLOW|BLOCK|ESCALATE|ALLOW_WITH_DOWNGRADE, reasons[], warrant_out, required_tasks[]}`. |
| REQ-CHK-004 | Every checkpoint evaluation writes a `checkpoint_evaluated` event (§19.2) with decision and reasons, and increments metrics in §16. |
| REQ-CHK-005 | p95 latency of `evaluate` excluding SASI, lease validation and κ: < 20 ms. |
| REQ-CHK-006 | Every answer produced by KGF (NL answers, reports, exports) MUST carry an answer warrant whose grounds list every proposition warrant used, and the UI shows the warrant (§18.2). |

### 6.6 Checkpoint SDK

| ID | Requirement |
|---|---|
| REQ-SDK-001 | Provide an SDK in every language that hosts KGF agents or LLM features (at minimum the backend language). API: `with warrant_context(principal, plan_id): …`, `observe(tool_id, call)`, `compute(operator_id, fn, inputs)`, `model(operator_id, fn, inputs)`, `generate(operator_id, prompt, inputs)`, `handoff(target_agent, message, warrants)`, `commit(action, warrants)`, `answer(text, warrants)`. |
| REQ-SDK-002 | The SDK MUST call checkpoints automatically; callers cannot bypass them except through `ip.warrant.enabled=false` (feature flag). |
| REQ-SDK-003 | All existing KGF LLM features (NL query, query suggestion, report generation, entity auto-detection from JSON) MUST be migrated to the SDK. List each migrated feature in the binding map. |
| REQ-SDK-004 | An MCP-compatible wrapper SHOULD be provided so external agents connected to KGF through MCP receive warrants on every tool result and must present warrants on write tools. |

### 6.7 Verification tasks

| ID | Requirement |
|---|---|
| REQ-VER-001 | A verification task has: `task_id`, `tenant_id`, `proposition`, `warrant_id`, `reason` (`GENERATED_PREMISE`, `LEASE_EXPIRED`, `HALF_LIFE_DUE`, `DRIFT`, `LAUNDERING_AUDIT`), `suggested_observer_ids[]`, `assignee?`, `due_at`, `state` (`OPEN`, `IN_PROGRESS`, `RESOLVED_CONFIRMED`, `RESOLVED_REFUTED`, `EXPIRED`). |
| REQ-VER-002 | Resolution by observer call creates a new `OBSERVED` warrant with new grounds; resolution by a person with authority creates an `ATTESTED` warrant. Refutation marks the original assertion `valid_to = now` and creates a `refuted_by` link. |
| REQ-VER-003 | `GET /verification-tasks` with filters (state, reason, type, assignee, due before), `POST /verification-tasks/{id}/resolve` with `{outcome, observer_id? , note?}`. |

### 6.8 Warrant lineage and laundering detection

| ID | Requirement |
|---|---|
| REQ-LIN-001 | A **laundering event** is any attempted warrant whose status exceeds what A1 allows. The service rejects it and writes `laundering_detected` with the offending operator and inputs. |
| REQ-LIN-002 | The laundering audit job (§15.3) samples `audit.sample_size` (default 200) memory writes and handoffs per tenant per month and re-runs A1/A2 from stored inputs; mismatches are reported. |

### 6.9 Signed warrant export and replay (Invention 10, folded)

| ID | Requirement |
|---|---|
| REQ-EXP-001 | Each tenant has an Ed25519 signing key pair stored in KGF's secret store; rotation supported; public keys published at `GET /warrants/keys`. |
| REQ-EXP-002 | `POST /warrants/{id}/export` returns a bundle: the answer or action, its warrant, the full lineage DAG, the graph snapshot version, model versions, data classes touched, the requesting principal's permissions at the time, and an Ed25519 signature over the RFC 8785 canonical bundle. Formats: JSON, and PDF with the bundle embedded as an attachment and a visible footer showing bundle id and verification URL path. |
| REQ-EXP-003 | `POST /warrants/verify` accepts a bundle, verifies the signature, and optionally replays: re-runs the recorded queries against the recorded `as-of` snapshot (REQ-WAR-023) and reports `MATCH`, `MISMATCH` (with diff) or `NOT_REPLAYABLE` (with reason). |
| REQ-EXP-004 | Exports never include data the requesting principal could not read at export time; the derivation guard runs on the bundle contents. |

---

## 7. Leases and Lease-Validated Commit (A3, Invention 15)

### 7.1 Graph change stream

| ID | Requirement |
|---|---|
| REQ-LSE-001 | KGF MUST publish `kgf.graph.changed` events for every committed assertion create/update/delete: `{tenant_id, assertion_id, subject_id, change_kind, old_version, new_version, recorded_at, warrant_id}`. |
| REQ-LSE-002 | Absent-capability rule: if the graph write path does not emit events, implement a transactional outbox table/collection written in the same transaction as the graph write (or in a compensating step for databases without multi-store transactions, with at-least-once delivery and idempotent consumers). Database-native change-data-capture MAY replace the outbox per database adapter; record DR. |
| REQ-LSE-003 | Event delivery: at-least-once, ordered per `subject_id`, end-to-end lag p95 < 2 s at 1,000 changes/s per tenant. |

### 7.2 Lease model

```json
{
  "lease_id": "uuid",
  "tenant_id": "string",
  "plan_id": "string",
  "holder_principal_id": "string",
  "assertion_id": "string",
  "subject_id": "string",
  "version": "string",
  "issued_at": "date-time",
  "expires_at": "date-time",
  "state": "ACTIVE | REVOKED | EXPIRED | RELEASED",
  "revoked_by_event": "string|null"
}
```

| ID | Requirement |
|---|---|
| REQ-LSE-010 | A lease is issued at the `retrieval` checkpoint for every assertion read inside a `warrant_context` that has a `plan_id`. Expiry = `issued_at + min(kgf:halfLifeDays of the assertion's type × lease.halflife_fraction, lease.max_ttl)`; defaults `lease.halflife_fraction = 0.5`, `lease.max_ttl = 24h`. |
| REQ-LSE-011 | On `kgf.graph.changed` for a subject, all `ACTIVE` leases on that subject with `version ≠ new_version` become `REVOKED` within 2 s p95. |
| REQ-LSE-012 | Leases are stored in a fast store indexed by `(tenant_id, subject_id)` and `(tenant_id, plan_id)`. Expired leases are swept every `lease.sweep_interval` (default 60 s). |

### 7.3 Algorithm A3 — Lease-Validated Commit

Input: action `a`, its warrant `W_a`, plan dependency graph `P` (DAG of plan steps; each step lists the assertion ids it read and the step ids it depends on).

```text
1. L = W_a.validity.lease_ids
2. invalid = { l ∈ L : l.state ≠ ACTIVE or l.expires_at ≤ now }
3. if invalid = ∅ → ALLOW
4. affected_facts = { l.assertion_id : l ∈ invalid }
5. affected_steps = steps in P that read any affected fact, plus all their descendants in P
6. return REPLAN(affected_steps, refreshed facts = current versions with new leases)
7. the caller re-executes only affected_steps; unaffected step outputs and warrants are reused
8. after lvc.max_retries (default 3) consecutive REPLAN results for the same action → ESCALATE
```

| ID | Requirement |
|---|---|
| REQ-LVC-001 | `POST /commits/validate` (request: `action`, `warrant_id`, `plan_graph`) returns `ALLOW`, `REPLAN {affected_steps[], refreshed_assertions[]}` or `ESCALATE`. |
| REQ-LVC-002 | The SDK `commit()` MUST call A3 for every action of class ≥ `INTERNAL_WRITE` and implement step 7 (partial re-planning) for KGF's own agents. |
| REQ-LVC-003 | p95 validation < 50 ms for ≤ 500 leases. |
| REQ-LVC-004 | Metric `kgf_ip_stale_commit_total{tenant,action_class}` counts commits that hit `REPLAN` or `ESCALATE` because of revoked or expired leases. |
| REQ-LVC-005 | Demonstration scenario (part of the Evidence Pack): an agent plans a change using fact F; F is changed by another user before commit; the commit returns `REPLAN` naming only the steps that used F; after re-planning the commit succeeds; the audit log shows the full sequence. |

---

## 8. Type Half-Life Estimation (A7, Invention 20)

### 8.1 Algorithm A7

For each ontology type T (and optionally each property of T):

```text
samples_T = { Δt = time from an assertion's verification (warrant created_at with status OBSERVED or ATTESTED)
              to its next change event (or censoring at now if unchanged) }
fit exponential with right-censoring: λ_T = (#observed changes) / Σ Δt
h_T = ln 2 / λ_T
if #observed changes < halflife.min_events (default 30) → use kgf:halfLifeDays if set, else halflife.default_days (default 30)
goodness of fit: if Kolmogorov–Smirnov p < 0.05 and #events ≥ 100 → fit Weibull(k, λ) and set h_T = λ (ln 2)^(1/k)
freshness f(x,t) = 2^(−(t − t_verified)/h_T)
warrant valid_to for verified facts = t_verified + halflife.k × h_T (default k = 1)
```

| ID | Requirement |
|---|---|
| REQ-HLF-001 | `halflife-service` MUST implement A7, refit nightly (`halflife.refit_cron`, default `0 2 * * *` tenant local time), and store `(tenant_id, type, property?, model, params, h_days, n_events, fitted_at)` history. |
| REQ-HLF-002 | When freshness of an assertion of a type with `kgf:criticality ≥ halflife.min_criticality_for_tasks` (default 3) falls below `halflife.phi` (default 0.5), create a verification task with reason `HALF_LIFE_DUE`. Rate-limit to `halflife.max_tasks_per_day` (default 200) per tenant, highest criticality first. |
| REQ-HLF-003 | `GET /half-lives` lists current values with sample sizes and fit model; `POST /half-lives/refit` triggers a refit (permission `ip.halflife.admin`). |
| REQ-HLF-004 | Unit tests with synthetic exponential and Weibull data MUST recover the true half-life within 10% at n = 500. On the seeded demo tenant, fitted half-lives MUST be within 15% of the planted values for every type with ≥ 100 change events. |

---

## 9. Consequence: learned impact propagation (Invention 2) and Blast-Radius Budgeting (A4, Invention 14)

### 9.1 Invention 2 — Ontology-constrained neural impact propagation

**Inputs:** changed entity set `S` with change type (`ADD`, `MODIFY`, `DELETE`) and property-level change vector; tenant instance graph; ontology annotations (§4.4); trained model (if available).

**Propagation:**

```text
s_v^(0) = 1.0 for v ∈ S, else 0
for hop h = 0 … H−1 (H = impact.max_hops, default 4):
  for each edge (u →r v) with s_u^(h) ≥ ε (impact.epsilon, default 0.01):
      gate(u,r,v) = 0 if r or the metapath ending in r has kgf:blastBarrier=true,
                    0 if tenant(u) ≠ tenant(v), else 1
      w(u,r,v)    = learned attention weight α_r(u,v) from the trained heterogeneous GAT,
                    or kgf:impactWeight(r) if no trained model (prior mode)
      bridge      = B_{dom(u)→dom(v)}(s_u^(h)) if kgf:domain differs (learned MLP, identity in prior mode)
      contribution c = gate · w · bridge · decay_r      (decay_r learned per relation type; 0.7 in prior mode)
      combine into v: s_v^(h+1) = 1 − (1 − s_v^(h+1)) · (1 − c · s_u^(h))     (noisy-OR)
P(v | a) = max_h s_v^(h)
```

Propagation direction follows dependency semantics: each relation type's `kgf:impactDirection` annotation (§4.4) decides whether impact flows along the edge, against it, or both (default `reverse` for dependency-like relations such as `DEPENDS_ON`, `CALLS`, `USES`; `forward` otherwise).

**Training:** heterogeneous GAT (R-GAT or HGT; choose by validation AUPRC, record DR) trained on historical change→affected pairs collected from: incidents linked to changes, test failures linked to commits, deployment rollbacks, and steward-confirmed impact reviews. Positive pairs: (change, affected entity). Negatives: sampled entities within 4 hops not affected. Chronological split (train < validation < test by time; no leakage).

| ID | Requirement |
|---|---|
| REQ-IMP-001 | `impact-engine` MUST implement the propagation exactly as specified, in prior mode from day one and in learned mode once a model passes its gate (REQ-IMP-004). |
| REQ-IMP-002 | `POST /impact/propagate` (request: `changes[]{entity_id, change_type, properties[]}`, `max_hops?`, `include_paths: bool`) returns `impact_run_id`, `entities[]{entity_id, type, probability, hop, criticality, paths[]}`, `test_checklist[]` (entities of types annotated as tests or with `TESTS`/`VERIFIES` relations to impacted entities, ranked by probability × criticality), `summary_text` (generated through SDK, therefore warranted), `mode` (`prior` or `learned`), `model_version`. |
| REQ-IMP-003 | Each response is stored as an impact run with its parameters and is reproducible: re-running with the same snapshot and model version returns identical probabilities (deterministic inference). |
| REQ-IMP-004 | Learned mode is enabled per tenant only when the trained model beats prior mode on the chronological test split by ≥ 5 percentage points AUPRC and has calibration error (ECE) ≤ 0.1; otherwise the tenant stays in prior mode and the UI says so. |
| REQ-IMP-005 | Performance: p95 < 2 s for |S| ≤ 10, H = 4, on a graph of 1,000,000 nodes / 5,000,000 edges (neighbourhood loaded through the abstraction layer with batched hop expansion). |
| REQ-IMP-006 | Blast barriers and tenant boundaries are absolute: a test MUST prove zero probability mass crosses them. |

### 9.2 Algorithm A4 — Blast-Radius Budgeting

```text
κ(a) = Σ_{v ∈ Impacted(a)} P(v | a) · c(v),      Impacted(a) = { v : P(v|a) ≥ budget.p_min (default 0.05) }
c(v) = criticality weight: {1:1, 2:2, 3:4, 4:8, 5:16}[kgf:criticality(v)]  (configurable map budget.criticality_weights)
For a plan with actions a_1..a_k: κ(plan) uses the union of impacted sets with max P per entity (no double counting).

Budget per agent identity (or per agent class when identity has no own budget):
B(t+Δ) = min(B_max, B(t) − κ_spent + ρ·Δ)
defaults by agent class (budget.defaults):
   READ_ONLY_AGENT: B_max = 0
   STANDARD_AGENT:  B_max = 10,  ρ = 10 per 24 h
   ELEVATED_AGENT:  B_max = 50,  ρ = 50 per 24 h
Decision: ALLOW and debit if κ ≤ B(t); else ESCALATE with impact subgraph; IRREVERSIBLE class always ESCALATE.
```

| ID | Requirement |
|---|---|
| REQ-BRB-001 | `consequence-service` MUST implement A4 exactly and be called from the `commit` checkpoint for action classes `EXTERNAL_WRITE` and `IRREVERSIBLE`, and for `INTERNAL_WRITE` when `budget.apply_to_internal_writes=true` (default false). |
| REQ-BRB-002 | `POST /actions/authorize` (request: `action`, `warrant_id`, `agent_id`, `plan_id?`) returns `{decision, kappa, budget_before, budget_after?, impact_run_id, escalation_id?}`. Budget debit and decision are atomic (no double spend under concurrency; test with 100 concurrent requests). |
| REQ-BRB-003 | Escalations: `GET /escalations`, `POST /escalations/{id}/decide` with `{decision: APPROVE|REJECT|APPROVE_WITH_SCOPE, scope?, note}`. Approval creates an `ATTESTED` warrant for the action by the approver, then the action proceeds without debiting the agent budget beyond its current balance (approved κ is logged as `kappa_approved`). |
| REQ-BRB-004 | `GET /budgets`, `PUT /budgets/{agent_class_or_id}` (permission `ip.budget.admin`), budget history per agent. |
| REQ-BRB-005 | Metric `kgf_ip_budget_overrun_total{tenant,agent_class}` counts escalations caused by κ > B. |
| REQ-BRB-006 | Demonstration scenario: a STANDARD_AGENT requests an action on a criticality-5 service with κ > 10 → escalated; approver sees the impact subgraph and approves; action executes; budget unchanged; a second, low-κ action is allowed and debited. |

---

## 10. Derivation Closure Guard (A5, Invention 16)

### 10.1 Protected facts

| ID | Requirement |
|---|---|
| REQ-DCG-001 | Protected-fact registry entries: `{protected_id, tenant_id, pattern, applies_to_principals (role/group/user selectors), except_principals, reason, owner, created_at}`. `pattern` is a graph pattern in KGF's canonical pattern syntax over types, relations and property predicates (e.g., `(p:Person)-[:SUBJECT_OF]->(:LayoffPlan)`), or a single assertion id. Entities, properties or relations annotated `kgf:protected=true` generate registry entries automatically. |
| REQ-DCG-002 | `GET/POST/PUT/DELETE /protected-facts` with permission `ip.protected.admin`; every change audited. |

### 10.2 Algorithm A5

Rules `R` = ontology axioms the rule engine supports (subclass, subproperty, inverse, property chains, transitive properties, SHACL rules / SWRL-style rules defined in the tenant ontology) **plus** link predictions from the tenant's link predictor with probability ≥ `dcg.link_threshold` (default 0.8).

```text
State per session (agent run or user session): K = set of assertions already disclosed to the principal.
On candidate fact f at the retrieval checkpoint:
  1. if f itself matches a protected pattern for the principal → BLOCK
  2. compute Cl = bounded closure of K ∪ {f} under R to depth d (dcg.depth, default 3),
     using semi-naive incremental evaluation from the last closure of K (cached per session)
  3. if Cl ∩ Protected(principal) = ∅ → ALLOW; K := K ∪ {f}
  4. else:
       derivations = all derivation trees (≤ depth d) that produce a protected fact
       H = minimum hitting set over the leaf facts of those derivations, restricted to {f} ∪ (facts not yet disclosed)
       if H = {f} or H is empty → BLOCK f
       else → ALLOW f, mark facts in H as withheld for this session
  5. write derivation_blocked event with protected_id, derivation trees (ids only), and decision
Time budget: dcg.time_budget_ms (default 200). On timeout → BLOCK f (fail closed) and log DCG_TIMEOUT.
```

| ID | Requirement |
|---|---|
| REQ-DCG-010 | `derivation-guard` MUST implement A5 and be invoked at the `retrieval` checkpoint for all agent and LLM reads, and for user-facing NL answers. Direct UI graph browsing by humans MAY bypass it when `dcg.apply_to_human_browse=false` (default true). |
| REQ-DCG-011 | Absent-capability rule: if KGF has no rule engine, embed one that runs locally (e.g., an OWL 2 RL / Datalog engine), loading the tenant ontology's rules; record DR. |
| REQ-DCG-012 | `POST /derivation/check` (request: `principal_id`, `session_id`, `candidate_assertion_ids[]`) returns per candidate `{decision, protected_ids[], derivation_ids[]}`. `GET /derivation/blocks` lists blocks with filters. |
| REQ-DCG-013 | Benchmark `evals/dcg/inference-leak-v1` MUST contain ≥ 50 constructed scenarios where a protected fact is derivable from 2–4 individually permitted facts, and ≥ 50 benign scenarios. Acceptance: 100% of leak scenarios blocked within depth 3; ≤ 5% false blocks on benign scenarios. |
| REQ-DCG-014 | Performance: p95 < 200 ms with |K| ≤ 2,000 and ≤ 500 rules. |

---

## 11. Meaning Migration (A6, Invention 17)

### 11.1 Agent-artifact registry and term dependency graph

| ID | Requirement |
|---|---|
| REQ-MMG-001 | Register every agent artifact: prompts and prompt templates, skills, tool schemas, agent memory records, eval cases, saved queries, report templates, dashboards, cached summaries and embedding indexes. Record `{artifact_id, kind, owner, version, location, content_hash}`. |
| REQ-MMG-002 | Term extraction: for each artifact, extract references to ontology terms (type names, relation names, property names, enum values, synonyms/labels in every configured language) by exact and alias matching against the ontology's labels, plus embedding similarity ≥ `meaning.term_sim` (default 0.9) for free text. Store edges `(:OntologyTerm)-[:USED_BY {count, spans}]->(:AgentArtifact)`. |
| REQ-MMG-003 | Re-extract on artifact change (event-driven) and nightly full sweep. |

### 11.2 Algorithm A6 — Meaning Impact Propagation

```text
Input: ontology diff Δ between version v and v+1:
       RENAME(t→t'), SPLIT(t→{t1..tn}), MERGE({t1..tn}→t), DEPRECATE(t), CONSTRAINT_CHANGE(t), ENUM_CHANGE(t)
1. T_Δ = terms touched by Δ (including subtypes for SPLIT/MERGE/DEPRECATE)
2. A = artifacts reachable from T_Δ via USED_BY
3. score(a) = usage_frequency(a, last 30 days, normalized 0–1) × criticality(a) × change_weight(Δ kind)
     change_weight: RENAME 1, ENUM_CHANGE 2, CONSTRAINT_CHANGE 2, MERGE 3, SPLIT 4, DEPRECATE 4
4. rewrite proposal per artifact:
     RENAME → deterministic token replacement (all labels/aliases)
     SPLIT → language-model proposal choosing among t1..tn per usage, passed through SASI; marked for human review
     MERGE → deterministic replacement to t
     DEPRECATE → removal proposal + replacement if the ontology names a successor
     CONSTRAINT/ENUM → flag for review with the exact constraint diff
5. run regression evals: all eval cases linked to A, before (v) and after (v+1 + rewrites)
6. gate: publish allowed only if pass_rate_after ≥ pass_rate_before − ε (meaning.eps, default 0.02)
         and every SPLIT/DEPRECATE rewrite has a human approval
```

| ID | Requirement |
|---|---|
| REQ-MMG-010 | `meaning-service` MUST implement A6. Meaning release lifecycle: `DRAFT → IMPACT_ANALYZED → REWRITES_PROPOSED → EVALS_RUN → APPROVED → PUBLISHED` (or `REJECTED`). |
| REQ-MMG-011 | APIs: `POST /meaning/releases` (from ontology version pair), `GET /meaning/releases/{id}`, `GET …/impact`, `POST …/rewrites/{artifact_id}/decide`, `POST …/evals/run`, `POST …/publish`, `POST …/rollback`. |
| REQ-MMG-012 | Publishing a release applies ontology v+1 and all approved rewrites atomically from the user's point of view: either all artifacts reference v+1 or the release is rolled back. |
| REQ-MMG-013 | Rollback restores artifacts and ontology to v within 5 minutes for ≤ 10,000 artifacts. |
| REQ-MMG-014 | Metric: orphaned-term count = artifacts referencing terms absent from the active ontology version; target 0 after publish. |
| REQ-MMG-015 | Demonstration scenario: rename a relation type used by 3 prompts, 1 saved query and 5 eval cases; release shows exactly those artifacts; rewrites applied; evals pass; publish; orphaned-term count = 0. Then split a type and show the human-review step blocks publish until approved. |

---

## 12. Knowledge Metabolism

### 12.1 Status-preserving memory consolidation (Invention 18)

| ID | Requirement |
|---|---|
| REQ-MET-001 | Any consolidation (summarizing, deduplicating or compressing agent memory or KGF notes) MUST go through `POST /memory/consolidate` (or the SDK equivalent) which: (a) groups input propositions by status; (b) never produces a single output statement that combines propositions of different status; (c) produces output propositions each with a warrant composed by A1 from only the inputs it summarizes; (d) runs SASI on generated output; (e) creates verification tasks for any output proposition that became `GENERATED` while all its inputs were `OBSERVED`/`ATTESTED` (lost support). |
| REQ-MET-002 | Consolidated memory renders status markers inline (e.g., `[OBSERVED]`, `[PREDICTED]`) when exported as text for LLM context, using the template `metabolism.status_marker_template`. |
| REQ-MET-003 | Benchmark `evals/metabolism/consolidation-v1`: ≥ 100 memory sets mixing observed facts, predictions and hearsay. Acceptance: 0 cases where a consolidated statement has a higher status than its lowest-status input; ≥ 95% of input propositions represented in output (measured by SASI entailment). |

### 12.2 Metabolism metrics and Brain Health

| Metric | Definition | Granularity |
|---|---|---|
| Intake rate | New assertions per day | tenant, domain, type |
| Digestion latency | Median time from assertion intake to first warrant with status ≥ `ATTESTED` (or confirmation via verification) | tenant, domain, type |
| Toxicity rate | Laundering events + refuted assertions per 1,000 assertions per month | tenant, domain |
| Freshness index | Mean A7 freshness of assertions weighted by criticality | tenant, domain |
| Retirement rate | Assertions given `valid_to` per day (expired, refuted, deprecated) | tenant, domain, type |
| Verification backlog | Open verification tasks, and oldest age | tenant, domain |

| ID | Requirement |
|---|---|
| REQ-MET-010 | `metabolism-service` computes the metrics above hourly and stores daily snapshots for ≥ 400 days. |
| REQ-MET-011 | `GET /metabolism/metrics?from&to&domain&type` and `GET /brain-health` (aggregate score and the per-region breakdown that Invention 1 contributes, §14.1). |
| REQ-MET-012 | Brain Health score = weighted mean of normalized freshness index (0.3), 1 − normalized toxicity (0.25), 1 − normalized verification backlog (0.15), 1 − drift hotspot density from Invention 1 (0.2), digestion-latency score (0.1). Weights are configuration `brainhealth.weights`. Normalizations documented in code and in the UI tooltip. |

---

## 13. Shadow-Branch Rehearsal (Invention 19)

| ID | Requirement |
|---|---|
| REQ-SHB-001 | `branch-service` creates copy-on-write branches of a tenant's authoritative graph: `POST /branches {base_version, purpose, ttl}`. Reads on a branch see base + branch deltas; writes go only to branch deltas. Absent-capability rule: implement copy-on-write at the abstraction layer with a delta overlay store keyed by `(branch_id, assertion_id)` when the database has no native branching; record DR. |
| REQ-SHB-002 | Simulated tools: every registered tool of class ≥ `INTERNAL_WRITE` MUST declare a `simulate` implementation that, given the call, returns the assertions it would change (no external side effects). Tools without `simulate` cannot be rehearsed and are listed as such. |
| REQ-SHB-003 | `POST /branches/{id}/execute-plan` runs an agent plan against the branch using simulated tools, then computes `GET /branches/{id}/diff` (added, removed, changed assertions with warrants), impact (Invention 2 on the diff), κ (A4) and SHACL validation results. |
| REQ-SHB-004 | `POST /branches/{id}/merge` requires an approval when κ > the agent's budget or any SHACL violation exists; merge replays the plan against the authoritative graph through the normal commit checkpoint (leases re-validated). `POST /branches/{id}/discard`. Branches expire after `ttl` (default 24 h). |
| REQ-SHB-005 | Branch isolation test: no read of the authoritative graph by any other principal can observe branch deltas. |
| REQ-SHB-006 | Used by Invention 8 (counterfactual path removal), Invention 11 (merge simulation) and Invention 4 (impact simulation). |

---

## 14. Neural-fabric inventions

### 14.0 Shared neural foundation (`neural-service`)

#### 14.0.1 Snapshots and features

| ID | Requirement |
|---|---|
| REQ-NEU-001 | Graph snapshot export per tenant, per level (instance, meta, ontology) into a columnar format (Parquet) with node table (id, type, properties encoded), edge table (src, dst, relation, properties), and snapshot metadata (graph_version, recorded_at, counts). Schedule `neural.snapshot_cron` (default daily 01:00 tenant time) and on demand. |
| REQ-NEU-002 | Feature pipeline: type one-hot (or learned type embeddings), numeric properties standardized, text properties embedded with the local embedding model, degree features, recency features (days since last change). Feature definitions versioned. |
| REQ-NEU-003 | Snapshots respect data classes: restricted-class properties are excluded from features unless `neural.include_restricted=true` for the tenant. |

#### 14.0.2 Training and inference runtime

| ID | Requirement |
|---|---|
| REQ-NEU-010 | Use PyTorch and PyTorch Geometric (heterogeneous graph support) unless the repository already standardizes on another graph-ML library; record DR either way. |
| REQ-NEU-011 | Runs on CPU (mandatory) and uses a GPU when present. Training jobs declare memory needs; jobs exceeding available memory use neighbour sampling (GraphSAGE-style loaders) instead of failing. |
| REQ-NEU-012 | Chronological splits for every temporal task; no future information in training features (leakage test required per model). |
| REQ-NEU-013 | Every model's predictions are warranted: operator class `MODEL`, status ≤ `PREDICTED`, grounds include `model_run` with model id and version. Predictions never overwrite observed assertions (REQ-WAR-022). |

#### 14.0.3 Embedding store

| ID | Requirement |
|---|---|
| REQ-NEU-020 | Embeddings stored per `(tenant, level, model_version, snapshot_version)` in KGF's vector store abstraction, with nearest-neighbour search. |
| REQ-NEU-021 | Embedding alignment across retrains: orthogonal Procrustes alignment on anchor entities (entities unchanged between snapshots, ≥ 1,000 or all if fewer) before any cross-snapshot comparison. Alignment matrix stored with the snapshot. |

#### 14.0.4 Model registry

| ID | Requirement |
|---|---|
| REQ-NEU-030 | Registry records `{model_id, tenant_id (or 'global'), task, version, training snapshot, feature version, hyperparameters, metrics, status (CANDIDATE, ACTIVE, RETIRED), artifact URI (encrypted at rest), created_by, approved_by}`. |
| REQ-NEU-031 | Promotion `CANDIDATE → ACTIVE` only through the gate defined for each task, recorded as an approval. Rollback to the previous ACTIVE version in < 1 minute. |
| REQ-NEU-032 | Absent-capability rule: if no registry exists, use MLflow (self-hosted) or implement the fields above in KGF's metadata store; record DR. |

### 14.1 Invention 1 — Neural Ontology Heartbeat

| ID | Requirement |
|---|---|
| REQ-INV1-001 | Compute embeddings for all three levels at each snapshot (instance: heterogeneous GNN self-supervised link prediction; meta-graph: types and relation types with instance-count features; ontology: concept graph with axiom edges). |
| REQ-INV1-002 | Drift score per entity/type/relation-type: `d_v = 1 − cos(R·z_v^(t−1), z_v^(t))` with Procrustes matrix R (REQ-NEU-021). |
| REQ-INV1-003 | Adaptive threshold per type: flag when `d_v > μ_T + drift.sigma × σ_T` (default 3) over the trailing `drift.window` (default 30 snapshots); minimum 5 snapshots before flagging. |
| REQ-INV1-004 | Drift classification into exactly these classes: `SCHEMA_DATA_MISALIGNMENT`, `INGESTION_CONTAMINATION`, `USAGE_MEANING_DIVERGENCE`, `DEPRECATED_RESURRECTION`, `RELATION_OVERLOADING`, `OTHER`. Phase 1: deterministic rules (documented per class with the signals they use: SHACL violation rate change, share of assertions from a single new source, query-context shift, writes to deprecated types, relation-pair embedding multimodality). Phase 2: a trained classifier replaces rules when ≥ `drift.min_labels` (default 200) steward-labelled events exist and it beats rules on macro-F1 by ≥ 5 points. |
| REQ-INV1-005 | Cross-level correlation: a drift event links to co-occurring drift at other levels (same type at meta/ontology level) and is scored higher when it appears on ≥ 2 levels. |
| REQ-INV1-006 | Self-healing proposals per class (at least): constraint tightening (SHACL shape change), entity split, relation re-typing, ingestion rule amendment (mapping change or source quarantine), deprecation enforcement. Each proposal includes simulated impact: affected entities (Invention 2), queries whose results change (replay of saved queries on a shadow branch, §13), constraint violations before/after. |
| REQ-INV1-007 | Auto-apply only when `drift.auto_apply=true` (default false) AND severity = low AND classifier confidence ≥ 0.9 AND simulated impact touches ≤ 10 entities; everything else goes to the steward queue. |
| REQ-INV1-008 | APIs: `GET /drift/events`, `GET /drift/events/{id}`, `POST /drift/events/{id}/label`, `GET /drift/events/{id}/proposals`, `POST /drift/proposals/{pid}/apply|reject`. Events feed Brain Health (REQ-MET-012). |
| REQ-INV1-009 | Demonstration scenario: inject 300 assertions from a new source that systematically uses `Server` for containers; heartbeat flags `INGESTION_CONTAMINATION` on `Server` within one snapshot cycle, proposes an ingestion rule amendment with simulated impact; steward applies; next cycle clears the hotspot. |

### 14.2 Invention 3 — Metapath-attention question answering (Ask the Brain)

| ID | Requirement |
|---|---|
| REQ-INV3-001 | Question decomposition into sub-questions, each tagged with ontology concepts (entity linking to types and instances), via local LLM through the SDK (warranted). |
| REQ-INV3-002 | Metapath enumeration from the meta-graph up to length `ask.max_metapath_len` (default 4) between tagged types. |
| REQ-INV3-003 | Metapath scoring: semantic-level attention between the sub-question embedding and each metapath embedding (metapath embedding = attention-pooled relation and type embeddings), with hierarchical attention over metapaths sharing prefixes. Select top `ask.top_metapaths` (default 5). Phase 1 may use a training-free scorer (cosine of embeddings + path-length prior) until a trained scorer beats it on the QA eval set (REQ-INV3-008); record the active scorer in each answer. |
| REQ-INV3-004 | Subgraph extraction restricted to instances reachable through selected metapaths, passed through the derivation guard. |
| REQ-INV3-005 | Dual path: (a) deterministic: generate a query in the tenant's configured query language (Cypher, Gremlin, SPARQL, GQL, SQL as supported by KGF) constrained to the selected metapaths, show it to the user, execute; (b) neural: GNN over the subgraph + answer generation through the SDK. |
| REQ-INV3-006 | Fusion: answer claims carry warrants; claims from the deterministic path inherit statuses from the data (A1 COMPUTATION); neural claims are `PREDICTED`; disagreement between paths is shown explicitly ("the query returned X; the model suggests Y"). |
| REQ-INV3-007 | Ontology validation of the fused answer against SHACL/axioms; violations are flagged in the answer with the violated constraint. |
| REQ-INV3-008 | Eval set `evals/ask/kgf-qa-v1` with ≥ 150 questions over a seeded demo tenant, covering the five documented question types (impact of changing a service account, who changed a class, systems changed by a feature, what to test for a rule change, incident cause). Acceptance: exact-match or steward-accepted answers ≥ 80% on deterministic-answerable questions; 100% of answers carry warrants; 0 answers present a `PREDICTED` claim as observed. |
| REQ-INV3-009 | API: `POST /ask {question, mode: auto|deterministic|neural}` streams `{suggested_queries[], selected_metapaths[], deterministic_result, neural_result, fused_answer, warrant_id, violations[]}`; `GET /ask/{id}`. Suggested queries (existing KGF feature) are now generated from selected metapaths. |

### 14.3 Invention 4 — Ontology Advisor (self-organising ontology, narrowed)

| ID | Requirement |
|---|---|
| REQ-INV4-001 | Usage mining: record traversed metapaths from queries and Ask the Brain; propose a new relation type when a metapath of length 2–3 not defined as a direct relation is traversed by ≥ `advisor.min_support` (default 20) distinct queries in 30 days. |
| REQ-INV4-002 | New-type proposal: cluster untyped or generically typed entities in embedding space (HDBSCAN, `min_cluster_size` default 10); propose a type when a cluster is stable across 3 snapshots, with suggested properties = properties present in ≥ 80% of members and suggested parent = nearest existing type centroid. |
| REQ-INV4-003 | Relation-type splitting: for each relation type with ≥ 40 edges, cluster edge embeddings (concatenation of source, relation and target embeddings); propose a split when ≥ 2 clusters each have ≥ 20 edges and silhouette ≥ 0.35; suggested names generated through the SDK and marked `GENERATED`. |
| REQ-INV4-004 | Type refinement: propose subtypes when intra-type dispersion > 2× the median dispersion across types; propose merge when two sibling types have centroid cosine distance < 0.1 and property overlap ≥ 0.8. |
| REQ-INV4-005 | Every proposal runs impact simulation on a shadow branch: entities reclassified, queries and artifacts affected (via Meaning Migration A6), constraint changes; then enters the steward queue. Approved proposals become a meaning release draft (§11), never a direct ontology edit. |
| REQ-INV4-006 | APIs: `GET /ontology/proposals`, `GET /ontology/proposals/{id}`, `POST /ontology/proposals/{id}/approve|reject|defer` with reason (reasons are training labels). |

### 14.4 Invention 5 — Incident forensics (reworked)

| ID | Requirement |
|---|---|
| REQ-INV5-001 | Fingerprint of an incident at time t: (a) ontology-typed topology diff in window `[t − Δ, t]` (`forensics.window`, default 2 h): counts of change events per `(entity type, relation type, change kind)` normalized; (b) embedding of the changed subgraph (TGN-style temporal encoder, or mean-pooled GNN embeddings of changed entities in Phase 1). |
| REQ-INV5-002 | Library of fingerprints for resolved incidents with their recorded root cause (entity ids and change ids). |
| REQ-INV5-003 | Matching: weighted similarity `0.5 × cosine(typed diff vectors) + 0.5 × cosine(embeddings)`; return top 5 with score and a graph-diff explanation: which typed changes match, which differ. |
| REQ-INV5-004 | APIs: `POST /incidents/{id}/fingerprint`, `GET /incidents/{id}/matches`, `POST /incidents/{id}/root-cause` (records the confirmed cause; becomes a library entry). |
| REQ-INV5-005 | Thresholds, weights and the trained encoder are trade secrets (REQ-IPH-003). |
| REQ-INV5-006 | Acceptance: on 20 held-out seeded incidents, the top-5 matches include an incident with the same root-cause type for ≥ 14 of the 20. |

### 14.5 Invention 6 — Cross-tenant federated graph learning (trade secret)

| ID | Requirement |
|---|---|
| REQ-INV6-001 | Opt-in per tenant (`federation.enabled`, default false) and per data class: a tenant chooses which data classes may contribute gradients. `restricted` can never contribute. |
| REQ-INV6-002 | Task: link prediction and entity-resolution scoring models. Each participating tenant trains locally on its own snapshot; only clipped, noised gradients/updates leave the tenant. |
| REQ-INV6-003 | Differential privacy with DP-SGD per data class: per-class ε budgets (defaults `public: 8`, `internal: 4`, `confidential: 1`, δ = 1e-5) tracked with a privacy accountant; a tenant stops contributing a class once its budget is exhausted for the period (`federation.period`, default 90 days). |
| REQ-INV6-004 | Secure aggregation so the coordinator sees only the sum of updates. The coordinator is self-hosted inside the KGF deployment of the platform operator; no third-party service. |
| REQ-INV6-005 | The federated model is offered to each tenant as a CANDIDATE and promoted only if it beats the tenant's local model on the tenant's own validation split. |
| REQ-INV6-006 | Audit: every round logs participating tenants (pseudonymous ids), classes, ε spent; tenants can view their own ledger. |

### 14.6 Invention 7 — Entity Health (survival analysis)

| ID | Requirement |
|---|---|
| REQ-INV7-001 | Vitality vector per entity, recomputed daily: recency of updates, update frequency (30/90 days), query touches (30/90 days), degree and PageRank centrality, neighbourhood change rate, embedding drift rate (from Invention 1), freshness (A7). |
| REQ-INV7-002 | Events: `DEPRECATED`, `ARCHIVED`, `STALE` (no update and no query for `health.stale_days`, default 180), `GOVERNANCE_RISK` (steward-flagged). Model: Cox proportional hazards in Phase 1; switch to a neural survival model only if concordance index improves by ≥ 0.03 on a chronological split. |
| REQ-INV7-003 | Output per entity: predicted median remaining useful life, survival curve at 30/90/180 days, top contributing features. Entities with median < `health.alert_days` (default 30) and criticality ≥ 3 appear in the steward review queue with suggested action (archive, refresh, merge, deprecate). |
| REQ-INV7-004 | Steward decisions are stored as labels and used in the next training cycle. |
| REQ-INV7-005 | APIs: `GET /entities/{id}/vitality`, `GET /entity-health/queue`, `POST /entity-health/queue/{id}/decide`. |
| REQ-INV7-006 | Acceptance: concordance index ≥ 0.70 on the chronological test split of the demo tenant; the evidence includes the evaluation report. |

### 14.7 Invention 8 — Causal layer

| ID | Requirement |
|---|---|
| REQ-INV8-001 | Candidate pairs: entities A, B connected within 2 hops, both with ≥ `causal.min_snapshots` (default 20) snapshots of embedding change magnitudes. |
| REQ-INV8-002 | Granger test: VAR on the change-magnitude series with lag 1–3 (selected by AIC); F-test; Benjamini–Hochberg correction at q = 0.01 across all tested pairs per run. |
| REQ-INV8-003 | Counterfactual check on a shadow branch: remove the A→B connecting paths, re-run the temporal predictor for B's next change; keep the candidate only if predicted change magnitude of B drops by ≥ `causal.min_effect` (default 50%). |
| REQ-INV8-004 | Accepted pairs are stored as `(:Entity)-[:CAUSES {strength, lag, p_value, run_id}]->(:Entity)` in a separate causal layer (distinct label or named graph), status `PREDICTED`, never mixed with observed relations. |
| REQ-INV8-005 | `POST /causal/discover` (job), `GET /causal/edges`, `POST /causal/whatif {changes[]}` returns propagated effects using only CAUSES edges, clearly labelled as predicted. The graph explorer offers a "Causal lens" toggle (§18.10). |
| REQ-INV8-006 | Synthetic validation: on a generated temporal graph with 20 planted causal links and 200 non-causal correlated pairs, recall ≥ 0.7 and precision ≥ 0.8. |

### 14.8 Invention 9 — Smart layout (trade secret)

| ID | Requirement |
|---|---|
| REQ-INV9-001 | Features of the visible subgraph: node and edge counts, density, type distribution entropy, hierarchy depth (longest path in DAG part), number of components, presence of a time property. |
| REQ-INV9-002 | Candidate layouts: force-directed, hierarchical/layered, radial/ego, concentric, circular, grid, timeline (the layouts KGF's front-end supports). |
| REQ-INV9-003 | Phase 1 scorer: weighted sum of normalized stress, edge crossings, node overlap, label overlap and type-cluster cohesion, computed in a Web Worker on a fast preview layout. Phase 2: a learned scorer trained on user ratings (thumbs up/down and layout switches) once ≥ 300 rated layouts exist and it beats Phase 1 on held-out ratings. |
| REQ-INV9-004 | `POST /layout/recommend` returns ranked layouts with parameters; the explorer applies the top one by default ("Smart layout" toggle). |
| REQ-INV9-005 | Learned weights stored in the model registry only (REQ-IPH-003). |

### 14.9 Invention 11 — Smart Dedup (narrowed)

| ID | Requirement |
|---|---|
| REQ-INV11-001 | Candidates: within each type, blocking by normalized name/key tokens and by approximate nearest neighbours in embedding space; pairs with cosine ≥ τ_T (`dedup.tau` per type, default 0.92). |
| REQ-INV11-002 | Merge simulation on a shadow branch: merged entity = union of relations, property conflicts resolved by the type's merge policy (most recent observed value by default), then: replay of saved queries and dashboards touching either entity (result diffs), SHACL validation (new violations), impact of the merge (Invention 2). |
| REQ-INV11-003 | Merge preview in the UI shows the before/after entity, changed query results, violations and impacted entities; steward approves or rejects. Approved merges commit through the normal checkpoint; merges are reversible (split back) within `dedup.undo_days` (default 30). |
| REQ-INV11-004 | Learning: per type, logistic calibration of τ_T from approve/reject decisions once ≥ 50 decisions exist for that type. |
| REQ-INV11-005 | APIs: `GET /dedup/candidates`, `POST /dedup/simulate {a, b}`, `POST /dedup/merge {simulation_id}`, `POST /dedup/unmerge {merge_id}`. |
| REQ-INV11-006 | Acceptance on the seeded set (200 planted duplicate pairs, 200 near-miss non-duplicates) at default τ: precision ≥ 0.95 and recall ≥ 0.85. Unmerge restores the pre-merge state exactly (state hashes match). |

### 14.10 Invention 12 — Semantic zoom (reworked)

| ID | Requirement |
|---|---|
| REQ-INV12-001 | Abstraction pyramid per tenant: L0 full graph; L1 entities grouped by type within Louvain communities; L2 groups of types (by `kgf:domain`); L3 domain summary nodes. Meta-edges between groups carry counts and relation-type breakdowns. Rebuilt after each snapshot. |
| REQ-INV12-002 | Per-level embeddings trained with an alignment loss so that the mean of an L1 group's L0 member embeddings and the group's L1 embedding have cosine ≥ 0.8 (and likewise L1→L2, L2→L3). Report the achieved alignment per level. |
| REQ-INV12-003 | Cross-level query: `POST /abstraction/query {level, question|pattern}` answers at that level (e.g., count of services depending on a database cluster at L2) and returns drill-down handles to L0 entities. |
| REQ-INV12-004 | The explorer switches level by zoom thresholds with animated morphing between summary nodes and members (positions interpolated, never teleported), honouring reduced-motion settings. |
| REQ-INV12-005 | APIs: `GET /abstraction/levels`, `GET /abstraction/{level}/graph?viewport=…`. |

---

## 15. Team processes (tooling required)

Each process needs: a scheduled job or trigger, a work queue, a report, and a UI view (§18.12). Cadences are configuration.

| ID | Process | Trigger (default) | Tooling requirements |
|---|---|---|---|
| REQ-PRC-001 | Warrant Review | New or changed operator registration | Queue of pending operators showing proposed class, action class, sample inputs/outputs; approve/reject with reason; approved changes take effect immediately and are audited |
| REQ-PRC-002 | Meaning Release | New ontology version draft | The meaning release workflow (§11) is the tooling |
| REQ-PRC-003 | Laundering Audit | Monthly (`audit.cron`) | Sample per REQ-LIN-002; report with laundering rate and offending operators; one-click creation of verification tasks |
| REQ-PRC-004 | Budget Calibration | Quarterly | Report per agent class: κ distribution, escalations, approvals, incidents linked to agent actions; proposed new B_max and ρ; apply with approval |
| REQ-PRC-005 | Protected-Fact Review | Quarterly | Registry diff since last review, derivation-block log with top patterns, false-block reports from users; sign-off |
| REQ-PRC-006 | Metabolism Review | Monthly | Metabolism metrics per domain (§12.2), half-life refits, drift hotspots, verification backlog; sign-off |
| REQ-PRC-007 | Commitment Review | Weekly (`commitment.review_cron`) | Commitments at risk, broken and transferred in the period per agent class; kept rate trend; one-click reassignment; sign-off |
| REQ-PRC-008 | Dissent Review | Monthly, and on every minority-report revisit trigger | Decisions with minority reports, triggered revisits, vindicated minorities, ungrounded-shift rate per agent; sign-off |
| REQ-PRC-009 | Reflex Rule Review | Quarterly | Every enabled reflex rule with fire count, blocked fires, false fires reported by users, approver still valid; re-approval or disable |

Each process run produces a signed report (same signing as REQ-EXP-002) stored and listed at `GET /governance/process-runs`.

---

## 16. Discipline metrics

| Metric (Prometheus name) | Formula | Target (default, configurable) |
|---|---|---|
| `kgf_ip_warrant_coverage_ratio` | propositions and actions with a complete warrant (all five parts present) ÷ all propositions and actions passing checkpoints | ≥ 0.99 |
| `kgf_ip_laundering_per_1k_hops` | laundering events ÷ checkpoint evaluations × 1,000 | trending down; alert if > 1 |
| `kgf_ip_stale_commit_ratio` | commits with REPLAN/ESCALATE due to leases ÷ all commits | report only |
| `kgf_ip_budget_overrun_ratio` | escalations due to κ > B ÷ authorizations | report only |
| `kgf_ip_derivation_blocks_total` | count of A5 blocks | report only |
| `kgf_ip_verification_backlog` | open verification tasks | alert if oldest > 14 days |
| `kgf_ip_orphaned_terms` | REQ-MMG-014 | 0 after each publish |
| `kgf_ip_brain_health_score` | REQ-MET-012 | report only |
| `kgf_ip_meaning_release_lead_time_hours` | time from ontology draft to meaning release `PUBLISHED`, per release | report only |
| `kgf_ip_meaning_post_release_regression_ratio` | eval cases failing within 7 days after publish that passed before ÷ eval cases linked to the release | ≤ 0.02 |
| `kgf_ip_protected_coverage_ratio` | assertions whose type or property is classified `confidential` or `restricted` and matched by at least one protected-fact pattern ÷ all such assertions | ≥ 0.95 |
| `kgf_ip_inference_check_coverage_ratio` | agent and LLM retrievals that passed the derivation guard ÷ all agent and LLM retrievals | ≥ 0.99 |
| `kgf_ip_derivation_false_block_ratio` | blocks reported by users as false and confirmed by a steward ÷ all blocks | ≤ 0.05 |
| `kgf_ip_commitment_kept_ratio` | commitments `FULFILLED` on or before `due_at` ÷ commitments that reached a final state | report only; alert if < 0.8 |
| `kgf_ip_commitments_overdue` | `ACTIVE` or `AT_RISK` commitments past `due_at` | alert if > 0 for criticality ≥ 4 |
| `kgf_ip_commitments_orphaned` | `ACTIVE` commitments whose promisor is disabled and that have no successor | 0 |
| `kgf_ip_dissent_preservation_ratio` | non-unanimous deliberations with a stored minority report ÷ non-unanimous deliberations | 1.0 |
| `kgf_ip_homogenization_index` | mean over deliberations of (distinct stances in round 0 − distinct stances in final round) ÷ distinct stances in round 0 | report only |
| `kgf_ip_ungrounded_shift_ratio` | stance changes marked `UNGROUNDED_SHIFT` ÷ all stance changes | trending down |
| `kgf_ip_minority_vindicated_total` | decisions where the owner recorded that the minority view proved right | report only |
| `kgf_ip_reflex_fires_total` | reflex rule executions, by outcome (`EXECUTED`, `BLOCKED`, `ESCALATED`, `RATE_LIMITED`) | report only |

Every metric carries labels `tenant`, and where relevant `domain`, `agent_class`, `action_class`. A "Discipline Metrics" dashboard shows them (§18.13).

---

## 17. Evidence Pack and verification (definition of done)

### 17.1 Evidence Pack contents

For each requirement ID, the folder `evidence/<REQ-ID>/` MUST contain:

| File | Content |
|---|---|
| `README.md` | What was demonstrated, environment (commit, build id, config values used, feature flags), date, who ran it |
| `run.sh` (or `.ps1`) | A script that reproduces the demonstration against a running KGF instance from a clean seeded tenant: API calls, UI automation, or both |
| `transcript/` | Captured HTTP requests and responses (secrets redacted) from the run, with trace ids |
| `state/` | Exported proof of persisted state: graph query outputs, database rows, warrant records, ledger entries |
| `negative/` | At least one negative-path run showing the system refusing or blocking correctly, with the error code |
| `ui/` | Screenshots or a short screen recording for every requirement with a UI element (§18), including empty, loading, error and permission-denied states |
| `metrics/` | Metric scrape excerpt showing the counters/gauges changed by the run |
| `logs/` | Audit events emitted by the run (filtered by trace id) |
| `tests.md` | Test command, pass/fail counts, and the kill-switch control result (§17.3) |
| `benchmarks/` | For requirements with numeric acceptance (latency, precision, recall, AUPRC, concordance): the benchmark command, dataset version and results |

### 17.2 Independent verification

A requirement moves to `VERIFIED` only when a verifier who did not write the code (a separate agent session with no access to the implementing session's conversation, or a human) runs `run.sh` against a fresh deployment, compares outputs with `transcript/` and `state/`, inspects `ui/`, and records the result in the verification report (template in the plan). Mismatches send the requirement back to `IN-PROGRESS`.

### 17.3 Kill-switch control

For every requirement, run its tests twice: with the feature flag on (must pass) and with the flag off or the implementing component replaced by a no-op (the tests that assert the feature's behaviour must fail). A test suite that passes in both runs does not test the feature and is rejected.

### 17.4 Forbidden completion shortcuts

The verifier MUST reject a requirement if any of these is found in the implementing production code path: `TODO`/`FIXME` on the path, `NotImplemented`/`pass`-only bodies, hard-coded return values standing in for computed results, mocks or fakes outside test folders, feature flags hard-wired on in tests only, skipped tests, or models replaced by random/constant outputs.

---

## 18. User interface requirements

All screens live in the existing KGF front-end, follow its design system, are tenant-scoped, keyboard accessible (WCAG 2.2 AA), support light/dark themes, and implement loading, empty, error, offline and permission-denied states. Every screen calls only the APIs in this document or existing KGF APIs.

| # | Screen | Route (suggested; follow app conventions) | Must show / do |
|---|---|---|---|
| 18.1 | Warrant Inspector | `/ip/warrants/:id` | Five parts of the warrant; status badge; grounds list with links to graph entities/documents; validity and lease states; authority scopes and delegation chain; κ and impact link; lineage DAG (expand/collapse); export and verify buttons |
| 18.2 | Status-annotated answer view | inside Ask the Brain and reports | Each proposition span coloured by status with legend (not colour alone: icon + text label); hover shows grounds; "verify this" creates a verification task |
| 18.3 | Verification Tasks | `/ip/verification` | Queue with filters; resolve by running suggested observer or attesting; history |
| 18.4 | Lease Monitor | `/ip/leases` | Active/revoked leases per plan; stale-commit events with re-planned steps |
| 18.5 | Impact Studio | `/ip/impact` | Pick entity and change type → ripple animation by hop with severity colours; ranked "what breaks" list; "what to test" checklist; mode (prior/learned) and model version; export |
| 18.6 | Budgets and Escalations | `/ip/budgets` | Budgets per agent class/identity with refill; escalation queue with impact subgraph, κ, warrant; approve/reject/approve-with-scope |
| 18.7 | Derivation Guard | `/ip/derivation` | Protected-fact registry editor (pattern builder + raw), block log with derivation trees, false-block reporting |
| 18.8 | Meaning Release Studio | `/ip/meaning` | Release list; ontology diff; affected artifacts ranked; rewrite proposals with diff view; eval results before/after; approve/publish/rollback |
| 18.9 | Brain Health and Metabolism | `/ip/brain-health` | Score; metabolism metrics charts; drift hotspots (Invention 1) on a graph overview; drill-down to drift events and proposals |
| 18.10 | Graph explorer additions | existing explorer | Causal lens toggle (Inv 8), Smart layout toggle (Inv 9), semantic zoom levels (Inv 12), entity vitality badge (Inv 7) |
| 18.11 | Ontology Advisor | `/ip/ontology-advisor` | Proposal queue (types, relation splits, merges) with evidence clusters and impact simulation; approve → creates meaning release draft |
| 18.12 | Governance Processes | `/ip/processes` | Six processes with next run, last report, open items, sign-off |
| 18.13 | Discipline Metrics | `/ip/metrics` | Metrics in §16 over time, by tenant/domain/agent class |
| 18.14 | Shadow Branches | `/ip/branches` | Branch list; plan execution; diff view; κ and SHACL results; merge/discard |
| 18.15 | Incident Forensics | `/ip/incidents/:id/forensics` | Fingerprint, top matches with graph-diff explanation, confirm root cause |
| 18.16 | Smart Dedup | `/ip/dedup` | Candidates; merge preview (before/after, query diffs, violations, impact); merge/unmerge |
| 18.17 | Entity Health | `/ip/entity-health` | Review queue with survival curves and suggested actions |
| 18.18 | Federation (platform admin + tenant view) | `/ip/federation` | Opt-in per class, ε ledger, round history, candidate model comparison |
| 18.19 | Operator Registry | `/ip/operators` | Registered operators, classes, action classes, approval workflow |
| 18.20 | Commitments | `/ip/commitments` | Board by state (proposed, active, at risk, fulfilled, broken, transferred); filters by promisor, promisee, entity, due date; commitment detail with statement, source message, warrant, fulfilment evidence; confirm, fulfil, release, transfer actions; per-agent view; kept-rate chart |
| 18.21 | Decisions and Minority Reports | `/ip/decisions/:id` | Question and options; round-0 positions side by side with their warranted grounds; stance changes per round marked grounded or ungrounded; outcome; minority report panel; revisit triggers; vindication action |
| 18.22 | Reflex Rules | `/ip/reflex` | Rule list with trigger, condition, action, approver, budget, fire counts; editor with validation; dry-run on a shadow branch with results; enable/disable; fire log |
| 18.23 | Disciplines | `/ip/disciplines` | One card per discipline (Warrant, Meaning Migration, Inference Control, Knowledge Metabolism, Commitment, Dissent) with its metrics, linked processes and screens; Warrant Engineering maturity level with the criteria met and unmet |

---

## 19. Cross-cutting specifications

### 19.1 Feature flags (tenant-scoped, default off)

`ip.warrant.enabled`, `ip.sasi.enabled`, `ip.lease.enabled`, `ip.halflife.enabled`, `ip.impact.learned.enabled`, `ip.budget.enabled`, `ip.dcg.enabled`, `ip.meaning.enabled`, `ip.metabolism.enabled`, `ip.branch.enabled`, `ip.inv1.enabled`, `ip.inv3.enabled`, `ip.inv4.enabled`, `ip.inv5.enabled`, `ip.inv6.enabled`, `ip.inv7.enabled`, `ip.inv8.enabled`, `ip.inv9.enabled`, `ip.inv11.enabled`, `ip.inv12.enabled`, `ip.export.enabled`, `ip.processes.enabled`, `ip.commitment.enabled`, `ip.dissent.enabled`, `ip.reflex.enabled`, `ip.disciplines.enabled`.

Dependencies (a flag cannot be enabled unless its dependencies are enabled; the admin API rejects with `FLAG_DEPENDENCY`): sasi→warrant; lease→warrant; budget→warrant, impact (prior mode is always available once `ip.warrant.enabled`); dcg→warrant; meaning→warrant; metabolism→warrant, halflife; branch→warrant; inv1→metabolism; inv3→warrant, dcg; inv4→branch, meaning; inv8→branch; inv11→branch; export→warrant; commitment→warrant, sasi, lease; dissent→warrant, sasi; reflex→warrant, budget, branch; disciplines→processes.

### 19.2 Events (topic names)

`kgf.graph.changed`, `kgf.ip.warrant.created`, `kgf.ip.checkpoint.evaluated`, `kgf.ip.laundering.detected`, `kgf.ip.lease.revoked`, `kgf.ip.commit.validated`, `kgf.ip.action.authorized`, `kgf.ip.escalation.created`, `kgf.ip.escalation.decided`, `kgf.ip.derivation.blocked`, `kgf.ip.verification.created`, `kgf.ip.verification.resolved`, `kgf.ip.meaning.release.changed`, `kgf.ip.drift.detected`, `kgf.ip.proposal.created`, `kgf.ip.branch.changed`, `kgf.ip.model.promoted`, `kgf.ip.commitment.changed`, `kgf.ip.deliberation.changed`, `kgf.ip.minority.revisit`, `kgf.ip.reflex.fired`. Every event: `{event_id, tenant_id, occurred_at, trace_id, actor, payload}` with a JSON Schema in `schemas/events/`.

### 19.3 Permissions (added to KGF RBAC)

`ip.warrant.read`, `ip.warrant.export`, `ip.operator.approve`, `ip.policy.admin`, `ip.verification.resolve`, `ip.halflife.admin`, `ip.impact.run`, `ip.budget.admin`, `ip.escalation.decide`, `ip.protected.admin`, `ip.meaning.manage`, `ip.meaning.publish`, `ip.branch.manage`, `ip.branch.merge`, `ip.drift.manage`, `ip.ontology.advise`, `ip.dedup.merge`, `ip.federation.admin`, `ip.processes.signoff`, `ip.model.promote`, `ip.commitment.manage`, `ip.commitment.transfer`, `ip.decision.record`, `ip.dissent.view`, `ip.reflex.manage`, `ip.reflex.approve`, `ip.disciplines.view`.

### 19.4 Audit events

Every state change listed in this document writes an audit record: `{audit_id, tenant_id, at, actor, permission_used, action, target_type, target_id, warrant_id?, request_hash, outcome, error_code?, trace_id}`. Audit records are append-only and hash-chained per tenant (each record stores the hash of the previous one); `GET /audit/verify-chain` validates the chain.

### 19.5 Error codes

| Code | HTTP | Meaning |
|---|---|---|
| `WAR_SCHEMA_INVALID` | 422 | Warrant failed schema validation |
| `WAR_INVALID_ORDER` | 422 | Invalid status order configuration |
| `WAR_STATUS_DOWNGRADE_WRITE` | 409 | Lower-status assertion tried to overwrite observed/attested |
| `OPR_UNREGISTERED` | 200 (notice) | Operator not registered; output capped |
| `CHK_STATUS_UPGRADE` | 409 | No-upgrade rule violated |
| `CHK_HANDOFF_DENIED` | 403 | Authority or minimum status failed at handoff |
| `CHK_MIN_STATUS` | 403 | Premise below minimum status for action class |
| `LVC_REPLAN` | 409 | Leases revoked or expired; re-plan required |
| `LVC_ESCALATE` | 409 | Retries exhausted |
| `BRB_OVER_BUDGET` | 403 | κ exceeds budget; escalation created |
| `DG_BLOCK` | 403 | Derivation guard withheld a fact |
| `DCG_TIMEOUT` | 403 | Closure check timed out; failed closed |
| `MMG_GATE_FAILED` | 409 | Meaning release failed regression gate |
| `SHB_NO_SIMULATE` | 422 | Tool cannot be rehearsed |
| `SASI_DEGRADED` | 200 (notice) | NLI unavailable; all generated |
| `FLAG_DEPENDENCY` | 409 | Feature flag dependency not met |
| `IP_RELEASE_BLOCKED` | CI failure | Public release attempted while `ip.public_release_allowed=false` |
| `CMT_UNAUTHORIZED` | 403 | Promisor lacks authority to make this commitment |
| `CMT_FULFILMENT_UNWARRANTED` | 409 | Fulfilment evidence below the required status |
| `CMT_ORPHANED` | 409 | Agent disable or replacement attempted with active commitments and no successor |
| `CMT_CONFLICT` | 409 | Action would change an entity an active commitment is about, and the plan does not reference that commitment |
| `DIS_INSUFFICIENT_DIVERSITY` | 409 | Deliberation for this action class lacks the required independent participants |
| `DIS_ISOLATION_BREACH` | 409 | A round-0 position was produced with access to another participant's position |
| `RFX_GENERATOR_FORBIDDEN` | 422 | Reflex rule references a GENERATOR or MODEL operator |
| `RFX_RATE_LIMITED` | 429 | Reflex rule exceeded its fire limit; circuit open |

All error bodies: `{code, message, details, trace_id}`.

### 19.6 Configuration keys (complete list with defaults)

| Key | Default |
|---|---|
| `warrant.status_order` | `[OBSERVED, ATTESTED, PREDICTED, GENERATED, HEARSAY, UNKNOWN]` |
| `warrant.runtime_retention_days` | 30 |
| `warrant.min_status_by_action_class` | table §6.4 |
| `sasi.max_propositions` | 64 |
| `sasi.candidates_k` | 5 |
| `sasi.theta` | 0.85 |
| `sasi.extract_model`, `sasi.embed_model`, `sasi.nli_model` | local model ids recorded in DR |
| `lease.halflife_fraction` | 0.5 |
| `lease.max_ttl` | 24h |
| `lease.sweep_interval` | 60s |
| `lvc.max_retries` | 3 |
| `halflife.min_events` | 30 |
| `halflife.default_days` | 30 |
| `halflife.k` | 1 |
| `halflife.phi` | 0.5 |
| `halflife.min_criticality_for_tasks` | 3 |
| `halflife.max_tasks_per_day` | 200 |
| `halflife.refit_cron` | `0 2 * * *` |
| `impact.max_hops` | 4 |
| `impact.epsilon` | 0.01 |
| `budget.p_min` | 0.05 |
| `budget.criticality_weights` | `{1:1,2:2,3:4,4:8,5:16}` |
| `budget.defaults` | §9.2 |
| `budget.apply_to_internal_writes` | false |
| `dcg.link_threshold` | 0.8 |
| `dcg.depth` | 3 |
| `dcg.time_budget_ms` | 200 |
| `dcg.apply_to_human_browse` | true |
| `meaning.term_sim` | 0.9 |
| `meaning.eps` | 0.02 |
| `metabolism.status_marker_template` | `[{status}]` |
| `brainhealth.weights` | §12.2 |
| `audit.sample_size` | 200 |
| `audit.cron` | `0 3 1 * *` |
| `neural.snapshot_cron` | `0 1 * * *` |
| `neural.include_restricted` | false |
| `drift.sigma` | 3 |
| `drift.window` | 30 |
| `drift.min_labels` | 200 |
| `drift.auto_apply` | false |
| `ask.max_metapath_len` | 4 |
| `ask.top_metapaths` | 5 |
| `advisor.min_support` | 20 |
| `forensics.window` | 2h |
| `federation.enabled` | false |
| `federation.period` | 90 days |
| `health.stale_days` | 180 |
| `health.alert_days` | 30 |
| `causal.min_snapshots` | 20 |
| `causal.min_effect` | 0.5 |
| `dedup.tau` | 0.92 per type |
| `dedup.undo_days` | 30 |
| `ip.public_release_allowed` | false |
| `commitment.extract_model` | local model id recorded in DR |
| `commitment.confirm_window` | 10 min |
| `commitment.min_lead_time` | 15 min |
| `commitment.max_open` | 50 per promisor |
| `commitment.at_risk_fraction` | 0.2 |
| `commitment.fulfil_min_status` | `ATTESTED` (i.e., `OBSERVED` or `ATTESTED`) |
| `commitment.review_cron` | `0 9 * * 1` |
| `dissent.min_independent` | 2 |
| `dissent.diversity_key` | `model_family` (alternatives: `context_source`, `principal`) |
| `dissent.max_rounds` | 3 |
| `dissent.required_from_action_class` | `EXTERNAL_WRITE` |
| `reflex.max_fires_per_hour` | 20 per rule |
| `reflex.latency_budget_ms` | 500 |
| `reflex.circuit_reset` | 1 h |
| `disciplines.maturity_window_days` | 90 |

### 19.7 API catalogue

All endpoints are under KGF's API base path, tenant-scoped (`/api/v1/t/{tenant}/…` or the existing KGF tenant convention, recorded in the binding map), JSON, authenticated, paginated with cursor (`?cursor=&limit=`, max 200), and documented in OpenAPI 3.1 at `schemas/openapi/ip.yaml` generated from code.

| Area | Endpoints |
|---|---|
| Warrants | `POST /warrants/compose`, `GET /warrants/{id}`, `GET /warrants/{id}/lineage`, `POST /warrants/{id}/export`, `POST /warrants/verify`, `GET /warrants/keys` |
| Operators | `GET /operators`, `POST /operators`, `PUT /operators/{id}`, `POST /operators/{id}/approve` |
| Checkpoints | `POST /checkpoints/{checkpoint}/evaluate` |
| SASI | `POST /sasi/evaluate` |
| Verification | `GET /verification-tasks`, `POST /verification-tasks/{id}/resolve` |
| Leases | `POST /leases`, `GET /leases`, `GET /leases/{id}`, `POST /commits/validate` |
| Half-lives | `GET /half-lives`, `POST /half-lives/refit` |
| Graph time travel | `GET /graph/as-of` |
| Impact | `POST /impact/propagate`, `GET /impact/runs/{id}` |
| Budgets | `GET /budgets`, `PUT /budgets/{key}`, `POST /actions/authorize`, `GET /escalations`, `POST /escalations/{id}/decide` |
| Derivation | `POST /derivation/check`, `GET /derivation/blocks`, `GET/POST/PUT/DELETE /protected-facts` |
| Meaning | `POST /agent-artifacts`, `GET /agent-artifacts`, `GET /ontology-terms/{term}/dependents`, `POST /meaning/releases`, `GET /meaning/releases/{id}`, `GET /meaning/releases/{id}/impact`, `POST /meaning/releases/{id}/rewrites/{artifact_id}/decide`, `POST /meaning/releases/{id}/evals/run`, `POST /meaning/releases/{id}/publish`, `POST /meaning/releases/{id}/rollback` |
| Metabolism | `POST /memory/consolidate`, `GET /metabolism/metrics`, `GET /brain-health` |
| Branches | `POST /branches`, `GET /branches/{id}`, `POST /branches/{id}/execute-plan`, `GET /branches/{id}/diff`, `POST /branches/{id}/merge`, `POST /branches/{id}/discard` |
| Neural | `POST /ml/snapshots`, `GET /ml/snapshots`, `POST /ml/train/{task}`, `GET /ml/models`, `POST /ml/models/{id}/promote`, `POST /ml/models/{id}/rollback` |
| Inv 1 | `GET /drift/events`, `GET /drift/events/{id}`, `POST /drift/events/{id}/label`, `GET /drift/events/{id}/proposals`, `POST /drift/proposals/{pid}/apply`, `POST /drift/proposals/{pid}/reject` |
| Inv 3 | `POST /ask`, `GET /ask/{id}` |
| Inv 4 | `GET /ontology/proposals`, `GET /ontology/proposals/{id}`, `POST /ontology/proposals/{id}/approve`, `…/reject`, `…/defer` |
| Inv 5 | `POST /incidents/{id}/fingerprint`, `GET /incidents/{id}/matches`, `POST /incidents/{id}/root-cause` |
| Inv 6 | `GET /federation/status`, `PUT /federation/settings`, `GET /federation/ledger`, `POST /federation/rounds` (platform admin) |
| Inv 7 | `GET /entities/{id}/vitality`, `GET /entity-health/queue`, `POST /entity-health/queue/{id}/decide` |
| Inv 8 | `POST /causal/discover`, `GET /causal/edges`, `POST /causal/whatif` |
| Inv 9 | `POST /layout/recommend`, `POST /layout/feedback` |
| Inv 11 | `GET /dedup/candidates`, `POST /dedup/simulate`, `POST /dedup/merge`, `POST /dedup/unmerge` |
| Inv 12 | `GET /abstraction/levels`, `GET /abstraction/{level}/graph`, `POST /abstraction/query` |
| Governance | `GET /governance/process-runs`, `POST /governance/processes/{process}/run`, `POST /governance/process-runs/{id}/signoff` |
| Audit | `GET /audit`, `GET /audit/verify-chain` |
| Flags | `GET /flags`, `PUT /flags/{flag}` |
| Commitments (Inv 21) | `POST /commitments`, `GET /commitments`, `GET /commitments/{id}`, `POST /commitments/{id}/confirm`, `POST /commitments/{id}/retract`, `POST /commitments/{id}/fulfil`, `POST /commitments/{id}/release`, `POST /commitments/{id}/transfer`, `POST /commitments/extract`, `GET /agents/{id}/commitments` |
| Dissent (Inv 22) | `POST /deliberations`, `GET /deliberations/{id}`, `POST /deliberations/{id}/positions`, `POST /deliberations/{id}/advance`, `POST /deliberations/{id}/decide`, `GET /decisions/{id}`, `GET /decisions/{id}/minority-report`, `POST /decisions/{id}/vindication` |
| Reflex rules | `GET /reflex-rules`, `POST /reflex-rules`, `PUT /reflex-rules/{id}`, `POST /reflex-rules/{id}/dry-run`, `POST /reflex-rules/{id}/approve`, `POST /reflex-rules/{id}/enable`, `POST /reflex-rules/{id}/disable`, `GET /reflex-rules/{id}/fires` |
| Disciplines | `GET /disciplines`, `GET /disciplines/{id}/metrics`, `GET /disciplines/warrant/maturity` |

---

## 20. Traceability matrix

| Invention / item | Requirements | Algorithms | Components | Screens | Plan WP |
|---|---|---|---|---|---|
| Warrant core (13) | REQ-WAR-*, REQ-OPR-*, REQ-WCA-*, REQ-CHK-*, REQ-SDK-*, REQ-VER-*, REQ-LIN-* | A1 | warrant-service, verification-service | 18.1, 18.3, 18.19 | WP-02, WP-03 |
| SASI (13) | REQ-SAS-* | A2 | sasi-engine | 18.2 | WP-04 |
| Export (10→13) | REQ-EXP-* | A1 | warrant-service | 18.1 | WP-22 |
| Leases (15) | REQ-LSE-*, REQ-LVC-* | A3 | lease-manager | 18.4 | WP-05 |
| Half-life (20) | REQ-HLF-* | A7 | halflife-service | 18.9 | WP-05 |
| Impact (2) | REQ-IMP-* | — | impact-engine | 18.5 | WP-07 |
| Budgets (14) | REQ-BRB-* | A4 | consequence-service | 18.6 | WP-08 |
| Derivation (16) | REQ-DCG-* | A5 | derivation-guard | 18.7 | WP-09 |
| Consolidation (18) | REQ-MET-001..003 | A1, A2 | metabolism-service | 18.2 | WP-10 |
| Meaning (17) | REQ-MMG-* | A6 | meaning-service | 18.8 | WP-11 |
| Metabolism + Inv 1 | REQ-MET-010..012, REQ-INV1-* | — | metabolism-service, neural-service | 18.9 | WP-12 |
| Branches (19) | REQ-SHB-* | — | branch-service | 18.14 | WP-06b |
| Neural foundation | REQ-NEU-* | — | neural-service | — | WP-06 |
| Inv 3 | REQ-INV3-* | A1 | neural-service | 18.2 | WP-14 |
| Inv 4 | REQ-INV4-* | A6 | neural-service, meaning-service | 18.11 | WP-13 |
| Inv 5 | REQ-INV5-* | — | neural-service | 18.15 | WP-17 |
| Inv 6 | REQ-INV6-* | — | federation-coordinator | 18.18 | WP-21 |
| Inv 7 | REQ-INV7-* | A7 | neural-service | 18.17 | WP-15 |
| Inv 8 | REQ-INV8-* | — | neural-service, branch-service | 18.10 | WP-16 |
| Inv 9 | REQ-INV9-* | — | ip-ui, neural-service | 18.10 | WP-20 |
| Inv 11 | REQ-INV11-* | — | neural-service, branch-service | 18.16 | WP-18 |
| Inv 12 | REQ-INV12-* | — | neural-service, ip-ui | 18.10 | WP-19 |
| Processes | REQ-PRC-* | — | governance-processes | 18.12 | WP-24 |
| Metrics | §16 | — | all | 18.13 | WP-24 |
| Platform | REQ-PLT-*, REQ-IPH-*, §19 | — | all | — | WP-00, WP-01, WP-25 |
| Companion disciplines | REQ-DSC-* | — | discipline-registry | 18.23 | WP-26 |
| Commitments (21) | REQ-CMT-*, REQ-PRC-007 | A1, A2, A3 | commitment-service | 18.20 | WP-27 |
| Dissent (22) | REQ-DIS-*, REQ-PRC-008 | A1, A2 | dissent-service | 18.21 | WP-28 |
| Reflex rules | REQ-RFX-*, REQ-PRC-009 | A1, A4 | reflex-engine | 18.22 | WP-29 |

---

## 21. Global definition of done

The IP programme is complete only when all of the following hold:

1. Every requirement ID in this document is `VERIFIED` in `docs/ip/ip-progress-ledger.md`, with an accepted Evidence Pack.
2. Every benchmark in this document has a recorded result meeting its acceptance threshold, or a `CONFLICT-IP`/DR accepted by the owner.
3. The kill-switch control (§17.3) has been run for every requirement.
4. A full end-to-end scenario run (plan WP-25) on a fresh deployment of the seeded demo tenant passes: ingestion with warrants → Ask the Brain with warranted answer → impact run → agent plan rehearsed on a shadow branch → commit blocked by a revoked lease → re-plan → escalation over budget → approval → commit → derivation-guard block of an inference leak → meaning release with rename and split → Brain Health updated → signed export verified by replay → an agent commitment detected, confirmed, blocked by a conflicting action, transferred on agent retirement and fulfilled with observed evidence → a deliberation that produces a minority report and fires its revisit trigger → a reflex rule fires within budget in under 500 ms → the Disciplines screen shows the resulting maturity level.
5. Turning every flag off returns KGF to pre-feature behaviour with all existing KGF test suites passing.
6. No item in §17.4 exists on any production code path (verified by the stub scan in the plan).
7. CI enforces REQ-IPH-001.

---

## 22. Companion disciplines and maturity

Warrant Engineering has five companion disciplines. Each is a named practice with its own definition, requirements, metrics, process and screen. KGF exposes them as one catalogue so tenants can see how far they have adopted each one.

| Discipline (id) | Definition (canonical text, use verbatim in UI) | Implemented by | Metrics (§16) | Process (§15) | Screen |
|---|---|---|---|---|---|
| Warrant Engineering (`warrant`) | The practice of designing, propagating and enforcing the justification that every claim and every action of an AI agent must carry. | §5–§9, §13, REQ-EXP-* | warrant coverage, laundering rate, stale-commit ratio, budget overrun ratio | REQ-PRC-001, 003, 004 | 18.1–18.6 |
| Meaning Migration Engineering (`meaning`) | The practice of keeping every agent prompt, tool, memory and test correct when an organization's meaning changes. | §11 | orphaned terms, meaning release lead time, post-release regression ratio | REQ-PRC-002 | 18.8 |
| Inference-Control Engineering (`inference`) | The practice of governing what agents can conclude, not only what they can read. | §10 | derivation blocks, protected coverage, inference-check coverage, false-block ratio | REQ-PRC-005 | 18.7 |
| Knowledge Metabolism Engineering (`metabolism`) | The practice of managing how shared knowledge is taken in, confirmed, consolidated, circulated and retired by people and agents. | §8, §12, Inventions 1, 7, 20 | §12.2 metrics, brain health score, verification backlog | REQ-PRC-006 | 18.9, 18.17 |
| Commitment Engineering (`commitment`) | The practice of recording, checking and enforcing the promises AI agents make to people and to each other. | §23 | commitment kept ratio, overdue, orphaned | REQ-PRC-007 | 18.20 |
| Dissent Engineering (`dissent`) | The practice of preserving, grounding and measuring disagreement in decisions made by multiple agents and people. | §24 | dissent preservation ratio, homogenization index, ungrounded shift ratio, minority vindicated | REQ-PRC-008 | 18.21 |

| ID | Requirement |
|---|---|
| REQ-DSC-001 | `discipline-registry` MUST serve the table above from `GET /disciplines` (id, name, definition, requirement groups, metric names with current values, process ids with last run date, screen routes). Definitions are stored as configuration so the owner can update the wording without a code change. |
| REQ-DSC-002 | `GET /disciplines/{id}/metrics?from&to` returns the discipline's metrics as time series at daily granularity for the requested window (max 400 days). |
| REQ-DSC-003 | Warrant Engineering maturity MUST be computed per tenant from live data over the trailing `disciplines.maturity_window_days`, using exactly these criteria (a level requires all criteria of that level and every level below): **L1 Labelled** — ≥ 99% of stored assertions have a warrant and ≥ 99% of answers carry an answer warrant. **L2 Enforced at commit** — `ip.warrant.enabled`, minimum-status checks active for `EXTERNAL_WRITE` and `IRREVERSIBLE`, and zero commits of those classes executed without a checkpoint evaluation in the window. **L3 End to end** — all six checkpoints evaluated at least once per day on ≥ 90% of days; `ip.lease.enabled`, `ip.budget.enabled`, `ip.dcg.enabled`, `ip.sasi.enabled` on; warrant coverage ≥ 0.99. **L4 Self-measuring** — every process REQ-PRC-001..009 that applies to enabled features ran on schedule with sign-off in the window, and `ip.export.enabled` with at least one verified export. Level 0 otherwise. |
| REQ-DSC-004 | `GET /disciplines/warrant/maturity` returns `{level, criteria: [{level, criterion, met, value, threshold}]}`; screen 18.23 shows unmet criteria with links to the screen or setting that fixes each. |
| REQ-DSC-005 | Discipline catalogue entries, definitions and maturity are visible to principals with `ip.disciplines.view`; no tenant data beyond aggregates is shown. |

---

## 23. Commitment Engineering (Invention 21: warranted commitment ledger)

**Problem.** Agents make promises in conversations and handoffs ("I'll reconcile these accounts by Friday", "I will notify the owner after the deploy"). Agent frameworks keep no record of them. Promises are forgotten when context is trimmed, broken silently, contradicted by later actions, or lost when an agent is replaced.

**Mechanism.** Every commitment is a graph record with a warrant. A commitment can only be made within the promisor's authority, can only be fulfilled by evidence of sufficient status, blocks conflicting actions at commit, and must be transferred before its promisor is retired.

### 23.1 Data model

System ontology types (created by the platform in every tenant; not editable by tenants):

```json
{
  "commitment_id": "uuid",
  "tenant_id": "string",
  "promisor": {"kind": "agent|person", "id": "string"},
  "promisees": [{"kind": "agent|person", "id": "string"}],
  "statement": "string (≤ 1000 chars)",
  "kind": "DELIVERABLE | FOLLOW_UP | SLA | CONDITIONAL",
  "about": ["entity ids in the graph"],
  "due_at": "date-time",
  "condition": "KGF pattern expression; required when kind = CONDITIONAL",
  "state": "PROPOSED | ACTIVE | AT_RISK | FULFILLED | BROKEN | RELEASED | TRANSFERRED | RETRACTED",
  "source": {"kind": "message|handoff|tool_call|api", "ref": "string", "span": {"start": 0, "end": 0}},
  "warrant_id": "uuid (warrant of the commitment itself)",
  "fulfilment_warrant_id": "uuid|null",
  "transferred_to": {"kind": "agent|person", "id": "string"} ,
  "parent_commitment_id": "uuid|null",
  "progress": [{"at": "date-time", "note": "string", "warrant_id": "uuid"}],
  "created_at": "date-time",
  "updated_at": "date-time"
}
```

Graph shape: `(promisor)-[:PROMISED]->(:Commitment)-[:TO]->(promisee)`, `(:Commitment)-[:ABOUT]->(entity)`, `(:Commitment)-[:FULFILLED_BY]->(:Warrant)`, `(:Commitment)-[:TRANSFERRED_TO]->(:Commitment)`.

### 23.2 Requirements

| ID | Requirement |
|---|---|
| REQ-CMT-001 | Explicit capture: SDK method `commit_to(promisees, statement, kind, due_at, about[], condition?)` and `POST /commitments` create a commitment in state `ACTIVE` with a warrant composed by A1 from the calling context (status of the commitment warrant = `ATTESTED` when made by a person, `GENERATED` when made by an agent; this records that the promise exists, not that it will be kept). |
| REQ-CMT-002 | Implicit detection: at the `answer` and `handoff` checkpoints, agent outputs pass through the extractor (`POST /commitments/extract`; prompt template `commitment.extract.v1`, a registered GENERATOR operator, local model `commitment.extract_model`). Each detected promissory statement creates a `PROPOSED` commitment with its source span. The promisor agent's runtime must call `confirm` or `retract` within `commitment.confirm_window`; unconfirmed proposals become `ACTIVE` and a notice goes to the agent's owner. |
| REQ-CMT-003 | Extraction benchmark `evals/commitment/extract-v1` with ≥ 200 labelled agent outputs (promises with and without dates, conditional promises, non-promises such as "you could…", reported speech). Acceptance: precision ≥ 0.90 and recall ≥ 0.85 for detecting promises; due-date extraction exact-match ≥ 0.85 on promises that state a date. |
| REQ-CMT-004 | Authority: the promisor's authority scopes (A1) MUST include action `commit:<kind>` on the ontology types of every `about` entity. Otherwise the commitment is rejected with `CMT_UNAUTHORIZED` and an escalation is created for a principal who holds that scope. |
| REQ-CMT-005 | Feasibility at creation: if `due_at − now < commitment.min_lead_time`, or the promisor already holds ≥ `commitment.max_open` open commitments, the commitment is created in state `AT_RISK` and the promisor and its owner are notified. |
| REQ-CMT-006 | Lifecycle scheduler (runs every minute): `ACTIVE → AT_RISK` when remaining time < `commitment.at_risk_fraction` × (due_at − created_at) and no progress entry exists in the last quarter of the window; `ACTIVE|AT_RISK → BROKEN` when `due_at` passes without fulfilment; `CONDITIONAL` commitments become due only when their condition first matches the graph (evaluated on `kgf.graph.changed`). Every transition writes `kgf.ip.commitment.changed` and notifies promisees. |
| REQ-CMT-007 | Evidence-based fulfilment: `POST /commitments/{id}/fulfil {warrant_id}` succeeds only if the referenced warrant has status ≥ `commitment.fulfil_min_status` and its grounds reference at least one entity in `about` (or, for `FOLLOW_UP`, a delivered message to every promisee recorded as an `OBSERVED` tool receipt). Otherwise `CMT_FULFILMENT_UNWARRANTED`. An agent saying "done" (a GENERATED proposition) never fulfils a commitment. |
| REQ-CMT-008 | Commit-time conflict check: at the `commit` checkpoint, if an action modifies or deletes an entity that an `ACTIVE`, `AT_RISK` or due `CONDITIONAL` commitment is `ABOUT`, and the action's plan does not reference that commitment id, the checkpoint returns `ESCALATE` with `CMT_CONFLICT`, listing the commitments and their promisees. |
| REQ-CMT-009 | Retrieval: when an agent works in a `warrant_context` whose task touches entities with open commitments by that agent, the `retrieval` checkpoint adds those commitments (statement, due date, state, warrant) to the context so the agent does not contradict them. |
| REQ-CMT-010 | Transfer on retirement: disabling, deleting or replacing (new version with a different identity) an agent identity with open commitments is refused with `CMT_ORPHANED` unless a successor is named; then every open commitment is copied to a new commitment for the successor (`TRANSFERRED_TO` link, same due date, promisees notified) and the original becomes `TRANSFERRED`. Platform-level configuration MAY name a default human owner per agent class as successor. |
| REQ-CMT-011 | `RELEASED` requires every promisee (or a principal with `ip.commitment.manage` on their behalf) to release the promisor, recorded with an `ATTESTED` warrant. |
| REQ-CMT-012 | APIs per §19.7, cursor-paginated, filterable by state, promisor, promisee, about-entity, kind, due range. |
| REQ-CMT-013 | UI 18.20 and metrics `kgf_ip_commitment_kept_ratio`, `kgf_ip_commitments_overdue`, `kgf_ip_commitments_orphaned`. |
| REQ-CMT-014 | Demonstration scenario: `agent-std-1` tells `bob` "I will rotate the svc-payments credentials by tomorrow 18:00" → `PROPOSED` commitment with the source span, confirmed → `ACTIVE`. `agent-elev-1` plans to delete svc-payments without referencing the commitment → `CMT_CONFLICT`. `agent-std-1` reports "done" in text → fulfilment refused. A credential-rotation tool receipt (`OBSERVED`) is submitted → `FULFILLED`. A second commitment by `agent-std-1` exists when the agent is retired → refused without successor, then transferred to `agent-elev-1`. |

---

## 24. Dissent Engineering (Invention 22: warranted minority reports)

**Problem.** When several agents (and people) deliberate, their views converge quickly, often without new evidence: agents yield to the majority, facts drop out of the discussion, and the final record shows a single confident answer. A correct minority view disappears.

**Mechanism.** The no-upgrade rule is applied to stances: a participant may change its stance only by citing new grounds. First-round positions are produced in isolation and kept. Every non-unanimous decision stores a minority report with its warranted grounds and revisit triggers.

### 24.1 Data model

```json
{
  "deliberation_id": "uuid", "tenant_id": "string",
  "question": "string", "options": [{"id": "string", "label": "string"}],
  "action_class": "READ_ONLY | ADVISORY | INTERNAL_WRITE | EXTERNAL_WRITE | IRREVERSIBLE",
  "participants": [{"kind": "agent|person", "id": "string", "diversity_value": "string"}],
  "rounds": [{"n": 0, "positions": [{
      "position_id": "uuid", "participant_id": "string", "option_id": "string",
      "rationale": [{"text": "string", "warrant_id": "uuid"}],
      "confidence": 0.0, "isolated": true, "seen_position_ids": [],
      "shift": "NONE | GROUNDED_SHIFT | UNGROUNDED_SHIFT", "new_ground_ids": [] }]}],
  "state": "OPEN | DECIDED | CANCELLED",
  "decision": {"option_id": "string", "decided_by": "string", "warrant_id": "uuid", "decided_at": "date-time"},
  "minority_report": {"positions": ["position ids"], "summary": "string", "summary_warrant_id": "uuid",
                      "revisit_triggers": [{"kind": "graph_change|date", "pattern_or_date": "string"}],
                      "vindicated": null}
}
```

### 24.2 Requirements

| ID | Requirement |
|---|---|
| REQ-DIS-001 | SDK `deliberate(question, options, participants, action_class, max_rounds?)` and `POST /deliberations` run the protocol: round 0, each participant produces a position in isolation; rounds 1..`dissent.max_rounds`, participants see all previous positions and may revise. Positions are produced through the checkpoint SDK, so every rationale proposition carries a warrant (SASI applies). |
| REQ-DIS-002 | Isolation: in round 0 the runtime MUST NOT include any other participant's position, rationale or the deliberation's later state in a participant's context; the position records `seen_position_ids = []` and `isolated = true`. A detected breach (any other position id or its text hash present in the context sent to the model) voids the position with `DIS_ISOLATION_BREACH`. |
| REQ-DIS-003 | Diversity: deliberations whose `action_class` ≥ `dissent.required_from_action_class` require ≥ `dissent.min_independent` participants with distinct values of `dissent.diversity_key` (model family, context source, or principal). Otherwise `DIS_INSUFFICIENT_DIVERSITY`. |
| REQ-DIS-004 | Grounded stance changes: when a participant's option differs from its previous round, the change is `GROUNDED_SHIFT` only if its new rationale contains at least one proposition whose warrant grounds include a ground id that the participant had not cited or been shown in any earlier round and whose status is ≥ `PREDICTED`; otherwise `UNGROUNDED_SHIFT`. Restating another participant's rationale is not a new ground. |
| REQ-DIS-005 | Minority report: on `decide`, if round-0 positions were not unanimous, a minority report is mandatory. It contains every round-0 position whose option differs from the decided option (even if the participant later shifted), plus any final-round dissent; a summary generated through the SDK (its propositions keep SASI statuses); and revisit triggers derived automatically from the entities in the dissenting positions' grounds (graph-change triggers) plus an optional date set by the decision owner. A decision without a required minority report is rejected. |
| REQ-DIS-006 | Human approval view: when a decision feeds an escalation or approval (§9.2), the approver sees the minority report and the ungrounded shifts before deciding. |
| REQ-DIS-007 | Revisit triggers: on a matching `kgf.graph.changed` event or date, emit `kgf.ip.minority.revisit` and notify the decision owner with the changed facts. The owner can record `POST /decisions/{id}/vindication {vindicated: true|false, note}` with an `ATTESTED` warrant. |
| REQ-DIS-008 | Metrics per §16: dissent preservation ratio, homogenization index, ungrounded shift ratio, minority vindicated total; per agent and per model family. |
| REQ-DIS-009 | Benchmark `evals/dissent/minority-v1`: ≥ 100 synthetic deliberation tasks over the demo tenant where the correct answer is held by a minority of round-0 positions (planted by giving one participant a decisive fact). Acceptance: the correct minority position appears in the minority report in ≥ 95% of tasks where it appeared in round 0; ungrounded-shift detection precision ≥ 0.9 against hand labels on 100 stance changes. |
| REQ-DIS-010 | UI 18.21 and APIs per §19.7. |
| REQ-DIS-011 | Demonstration scenario: three participants (two model families plus `bob`) decide whether to restart customer-db. One agent's round-0 position cites an observed replication-lag fact and says "do not restart". In round 1 it switches to "restart" without new grounds → `UNGROUNDED_SHIFT`. The decision is "restart"; the minority report keeps the replication-lag position; the approver sees it; a later change to the replication-lag fact fires a revisit notice. |

---

## 25. Reflex rules (product feature, not claimed as an invention)

**Purpose.** Some conditions need an immediate, known response without a language model in the loop (a service account flagged as compromised, a certificate about to expire on a critical service). Reflex rules give a fast path that is still warranted and governed.

| ID | Requirement |
|---|---|
| REQ-RFX-001 | Rule model: `{rule_id, tenant_id, name, trigger_topic, condition (KGF pattern evaluated on the event's subject neighbourhood), action {tool_id, parameter_template}, approver_principal_id, approved_at, budget_class, max_fires_per_hour, enabled, dry_run_report_id}`. |
| REQ-RFX-002 | Validation: the action's tool and every operator in the condition MUST be registered with class `OBSERVER`, `COMPUTATION` or a tool whose action class is declared; any `GENERATOR` or `MODEL` operator is rejected with `RFX_GENERATOR_FORBIDDEN`. |
| REQ-RFX-003 | A rule can be enabled only after a dry run on a shadow branch over the last 7 days of matching events (§13) has been reviewed and the rule approved by a principal with `ip.reflex.approve`; approval creates an `ATTESTED` warrant that becomes the authority of every fire. |
| REQ-RFX-004 | Every fire passes the `commit` checkpoint (minimum status, leases on the condition's facts, κ against the rule's budget class). Fires that fail become escalations; they are never retried automatically. |
| REQ-RFX-005 | Latency: from event publication to commit decision p95 < `reflex.latency_budget_ms` (500 ms) at 100 matching events per second per tenant. |
| REQ-RFX-006 | Rate limit and circuit breaker: more than `max_fires_per_hour` fires opens the circuit (`RFX_RATE_LIMITED`), disables the rule until `reflex.circuit_reset` passes or a person re-enables it, and notifies the approver. |
| REQ-RFX-007 | APIs per §19.7, UI 18.22, metric `kgf_ip_reflex_fires_total`, quarterly review REQ-PRC-009. |
| REQ-RFX-008 | Demonstration scenario: a rule "when a ServiceAccount gets property `compromised=true`, disable its tokens and notify its owner" is dry-run, approved and enabled; setting the property fires it within 500 ms; the warrant shows the approver's authority; a burst of 25 matching events in an hour opens the circuit. |
