# Chapter 4 — Ontology and Semantics

How EOIP models meaning: the enterprise ontology constraining every vertex and
edge, ontology versioning and drift review, semantic-web export, the SKOS
taxonomy layer, domain packs, the truth/claims conflict model, the validation
engine, architecture conformance rules, and the graph-test framework.
Everything is grounded in the cited source; anything not verifiable is marked
**[not runtime-verified]**. API examples assume `http://localhost:8000`, with
tenant `t-001`, issue `EOIP-123`, and service `checkout`.

**Section index**

1. [The enterprise ontology](#1-the-enterprise-ontology)
2. [Listing the schema via the API](#2-listing-the-schema-get-apiv1graphschema)
3. [Ontology versioning, semantic diff, and the CI publish verdict](#3-ontology-versioning-semantic-diff-and-the-ci-publish-verdict)
4. [Ontology drift review and evolution proposals](#4-ontology-drift-review-and-evolution-proposals)
5. [Embedding drift](#5-embedding-drift)
6. [Exporting RDF/JSON-LD and format conversion](#6-exporting-rdfjson-ld-and-format-conversion)
7. [SKOS taxonomy: schemes, concepts, mappings, validation, export](#7-skos-taxonomy)
8. [Domain packs](#8-domain-packs)
9. [Truth and claims: contradictions, resolution policies, explain](#9-truth-and-claims)
10. [Validation engine, quality metrics, and the findings workflow](#10-validation-engine-and-quality-metrics)
11. [Architecture conformance rules](#11-architecture-conformance-rules)
12. [The graphtest framework](#12-the-graphtest-framework)

---

## 1. The enterprise ontology

**What it does.** The ontology is a controlled vocabulary: every vertex label
(entity type) and edge label (relationship type) declares a graph domain,
required properties, optional properties, and allowed endpoint types. It is
defined in code at `packages/eoip/ontology/manifest.py` — `ONTOLOGY_VERSION =
"0.4.0"`, `SCHEMA_VERSION = "1.2"`. A starter snapshot also ships as YAML at
`config/ontology/ontology-v0.2.0.yaml` (note: that file is an older `0.2.0`
snapshot with 7 domains and 22 vertex labels; the live manifest in code is the
authoritative, much larger `0.4.0` vocabulary).

The live manifest declares **14 graph domains** (`manifest.py`,
`DOMAINS`):

```
META, WORK, CODE, CICD, KNOWLEDGE, IDENTITY, AGENT,
OPS, TEST, DESIGN, INTEGRATION, DECISION, PROCESS, BUSINESS
```

Key vertex labels by domain (from `VERTEX_LABELS`; ~60 labels total):

- **META** — `DataSource`, `IngestionRun`, `GraphDomain`, `OntologyVersion`, `Evidence`, `ValidationRun`, `ValidationFinding`, `EntityRevision`, `RelationshipRevision`, `GraphVersion`, `SemanticChange`
- **WORK** — `Project`, `WorkItem`, `IssueType`, `Status`, `Version`, `Sprint`, `Comment`, `WorkItemChange`, `Epic`, `Feature`, `UserStory`, `Requirement`
- **CODE** — `Repository`, `Branch`, `Commit`, `File`, `CodeSymbol`, `Dependency`, `Service`, `Database`, `Tag`, `APIService`, `APIEndpoint`, `APIConnection`
- **CICD** — `MergeRequest`, `PipelineRun`, `Release`, `Job`, `Artifact`, `Deployment`, `BuildRecord`
- **KNOWLEDGE** — `Document`, `KnowledgeSpace`, `DocumentSection`, `KBArticle`, `KnowledgeProduct`, `ProdPage`
- **IDENTITY** — `Person`, `Organization`; **AGENT** — `AgentRun`; **INTEGRATION** — `GenericEntity`
- **OPS** — `Incident`, `ChangeRequest`, `ServiceRequest`, `Dashboard`, `MonitorRule`, `AlertEvent`, `Metric`, `LogAggregate`
- **TEST** — `TestCase`, `TestSuite`, `TestCycle`, `TestRun`; **DESIGN** — `DesignFile`, `DesignPage`, `DesignComponent`
- **DECISION** — `Decision`, `Alternative`, `DecisionOutcome`; **PROCESS** — `ProcessFlow`, `ProcessStep`, `ProcessEvent`
- **BUSINESS** — `BusinessObjective`, `BusinessCapability`

Edge labels (from `EDGE_LABELS`, ~60 total) include `CONTAINS`, `PARENT_OF`,
`ASSIGNED_TO`, `AUTHORED_BY`, `HAS_COMMIT`, `MODIFIES`, `DECLARES`, `CALLS`,
`IMPORTS`, `DEPENDS_ON`, `IMPLEMENTS`, `REFERENCES`, `DOCUMENTS`,
`EVIDENCED_BY`, `INGESTED_IN`, `BELONGS_TO_DOMAIN`, `VALIDATED_BY`,
`PRODUCED_BY`, `TRIGGERED_BY`, `MONITORS`, `TESTS`, `RESOLVES`, `TRACES_TO`,
and more. Each edge spec is a tuple `(allowed_out_labels, allowed_in_labels,
properties)` — e.g. `IMPLEMENTS: (["MergeRequest", "Commit"], ["WorkItem"],
[])`. The generic label `RELATED_TO` is deliberately absent (a comment in the
manifest marks it forbidden).

**Errors and recovery.** Any write using an unknown label or an invalid
endpoint pair is blocked before persistence by the hard gate
(`packages/eoip/validation/gate.py`, exception `MutationBlocked`) — see
§10. You do not "fix" a blocked write; you fix the payload to use declared
vocabulary.

---

## 2. Listing the schema: `GET /api/v1/graph/schema`

**What it does.** Returns the full live ontology — versions, domains, every
vertex label with required/optional properties and live instance counts, every
edge label with endpoint constraints, property keys, and index definitions.
Implemented in `apps/api/app.py` via `GraphMetricsEngine.graph_schema()`
(`packages/eoip/graph/metrics.py`).

**Step by step.**

1. Call the endpoint:

   ```bash
   curl -s http://localhost:8000/api/v1/graph/schema | python -m json.tool | head -40
   ```

2. List vertex labels with instance counts, or inspect one edge label:

   ```bash
   curl -s http://localhost:8000/api/v1/graph/schema \
     | python -c "import json,sys; s=json.load(sys.stdin); [print(k, v['domain'], v['instance_count']) for k,v in s['vertex_labels'].items()]"
   curl -s http://localhost:8000/api/v1/graph/schema \
     | python -c "import json,sys; print(json.load(sys.stdin)['edge_labels']['IMPLEMENTS'])"
   # {"source_labels": ["MergeRequest", "Commit"], "target_labels": ["WorkItem"], "properties": []}
   ```

**Response/result.** Key fields: `ontology_version` (`"0.4.0"`),
`schema_version` (`"1.2"`), `domains` (14 entries), `vertex_labels` (map of
label → `{domain, required_properties, optional_properties, instance_count}`),
`edge_labels` (map of label → `{source_labels, target_labels, properties}`),
`property_keys` (name → HugeGraph type: `TEXT|INT|LONG|DOUBLE|BOOLEAN|DATE`),
`indexes` (e.g. `idx_canonical_id` UNIQUE on `canonical_id`).

**Errors and recovery.** No input parameters, so failures are server-side only
(500 if the store is unavailable). A companion `GET /api/v1/graph/statistics`
returns live counts if you only need sizes.

---

## 3. Ontology versioning, semantic diff, and the CI publish verdict

**What it does.** `packages/eoip/ontology/gitops.py` implements "Ontology
GitOps": a *structural* diff between two manifest snapshots, classifying each
change as `additive`, `potentially_breaking`, or `breaking`, plus a CI gate
verdict. (The module also contains branch/PR/review/merge/rollback scaffolding
— that workflow layer is not exposed over HTTP in the routes surveyed;
**[not runtime-verified]** beyond the diff endpoint below.)

**How to access.** `POST /api/v1/ontology/diff` (`apps/api/main.py`).

**Step by step.**

1. A manifest snapshot has the shape produced by `snapshot_manifest()`:
   `{"vertex_labels": {name: {"domain", "required", "optional"}},
   "edge_labels": {name: {"out", "in"}}, "property_keys": {...}}`. You may
   pass the literal string `"current"` for either side to use the live
   manifest.
2. Diff the live manifest against a modified copy:

   ```bash
   curl -s -X POST http://localhost:8000/api/v1/ontology/diff \
     -H 'Content-Type: application/json' \
     -d '{
       "old": "current",
       "new": {
         "vertex_labels": {"WorkItem": {"domain": "WORK",
           "required": ["canonical_id", "issue_key", "summary"],
           "optional": ["status"]}},
         "edge_labels": {"IMPLEMENTS": {"out": ["Commit"], "in": ["WorkItem"]}},
         "property_keys": {"canonical_id": "TEXT"}
       }
     }'
   ```

**Response/result.** A dict with `safe` (bool), `counts` (`total`,
`breaking`, `potentially_breaking`, `additive`), `changes` (list of
`{change_type, subject, detail, classification}` — e.g. `vertex_label_removed`
is `breaking`, `required_property_added` is `potentially_breaking`),
plus `publishable` (true when `safe`) and `verdict`:
`"PUBLISH_OK"` or `"BREAKING_CHANGE_REFUSED"`.

**Errors and recovery.** `422` if `old`/`new` are neither objects nor the
string `"current"`. A `BREAKING_CHANGE_REFUSED` verdict is not an HTTP error —
HTTP 200 is returned; treat the verdict field as the gate signal in CI.

---

## 4. Ontology drift review and evolution proposals

**What it does.** `packages/eoip/ontology/drift.py` scans the graph for
vocabulary in use that is *not* declared in the manifest (unknown vertex
labels, edge labels, property keys). Detection is read-only; nothing is
applied to the manifest automatically.

**How to access.** `GET /api/v1/ontology/drift` and
`POST /api/v1/ontology/proposals` (`apps/api/main.py`).

**Step by step.**

1. Scan for drift:

   ```bash
   curl -s http://localhost:8000/api/v1/ontology/drift
   ```

2. Review findings. Unknown vertex/edge labels are classified
   `potentially_breaking`; unknown property keys are `additive`. Each finding
   carries `kind`, `value`, `occurrences`, and up to 3 `examples`.
3. Turn findings into governed, human-reviewable proposals:

   ```bash
   curl -s -X POST http://localhost:8000/api/v1/ontology/proposals
   ```

   Each finding becomes a `ChangeProposal` (risk level `R2`, proposed by
   `OntologyDriftDetector`) with `operation` one of `ONTOLOGY_VERTEX_LABEL`,
   `ONTOLOGY_EDGE_LABEL`, `ONTOLOGY_PROPERTY_KEY`. Already-pending targets are
   skipped.
4. Review and decide proposals via the agent-proposal endpoints:
   `GET /api/v1/agents/proposals`, then
   `POST /api/v1/agents/proposals/{proposal_id}/approve` or `/reject`.

**Response/result.** Drift: `{"has_drift": bool, "findings": [...]}`.
Proposals: `{"created": n, "proposals": [...], "drift": {...}}`.

**Errors and recovery.** Both endpoints are read-only scans or proposal
creations; an empty findings list means `has_drift: false` and
`created: 0` — this is the healthy state, not an error.

---

## 5. Embedding drift

**What it does.** `packages/eoip/ontology/embedding_drift.py` computes the
cosine distance between baseline and current mean embedding vectors per label
prefix (`label::id` keys) and flags labels whose distance exceeds a threshold
(default `0.1`).

**How to access.** Library function only — `detect_embedding_drift(baseline,
current, threshold)` returns an `EmbeddingDriftReport` with `drift_score`,
`drifted_labels`, `baseline_count`, `current_count`, `timestamp`. No HTTP
endpoint for it was found in the routes surveyed **[not runtime-verified as an
API]**. A related health probe exists: `GET /api/v1/health/embeddings`.

**Step by step.**

```python
from eoip.ontology.embedding_drift import detect_embedding_drift
report = detect_embedding_drift(
    baseline_vectors={"Service::checkout": [0.1, 0.2]},
    current_vectors={"Service::checkout": [0.9, 0.1]},
    threshold=0.1,
)
print(report.to_dict()["drifted_labels"])  # ['Service']
```

**Errors and recovery.** `ValueError: Vector dimension mismatch` if two
vectors differ in length — re-embed with the same model/dimension.

---

## 6. Exporting RDF/JSON-LD and format conversion

**What it does.** `packages/eoip/ontology/rdf.py` exports the ontology plus
graph records as JSON-LD (`export_jsonld`), re-imports JSON-LD
(`import_jsonld`), emits SHACL shapes (`export_shacl_shapes`) and validates
against them. `packages/eoip/graph/format_converter.py` (`FormatConverter`)
serializes the graph into 11 interchange formats.

**How to access.**

- `GET /api/v1/ontology/export?limit=5000` → JSON-LD document
  (`application/ld+json`)
- `POST /api/v1/ontology/import?clear=false` → import a JSON-LD document
- `GET /api/v1/ontology/shacl` → SHACL shapes as JSON-LD
- `GET /api/v1/ontology/validate?limit=5000` → validate the graph against
  those shapes
- `POST /api/v1/ontology/validate/shacl` → SHACL validation with optional
  custom shapes/profile (`profile` default `"shacl-core-2017"`)
- `GET /api/v1/ontology/docs` → generated HTML ontology documentation
- `GET /api/v1/graph/formats` and `GET /api/v1/export/formats` → list formats
- `POST /api/v1/graph/convert` → convert the graph to one format

**The 11 formats** (from `FormatConverter.available_formats()`):

| id | label | ext | use |
|----|-------|-----|-----|
| `rdf` | RDF (Turtle) | `.ttl` | W3C RDF triples, Turtle syntax |
| `rdf_xml` | RDF/XML | `.rdf` | RDF in XML syntax |
| `rdfs` | RDFS Schema | `.ttl` | class/property definitions only |
| `owl` | OWL Ontology | `.owl` | classes + object properties |
| `gremlin` | Gremlin Script | `.groovy` | TinkerPop traversal/load script |
| `cypher` | Cypher Script | `.cypher` | Neo4j `MERGE` statements |
| `opencypher` | OpenCypher Script | `.cypher` | vendor-neutral variant |
| `gql` | GQL Script | `.gql` | ISO GQL `INSERT` statements |
| `sparql` | SPARQL INSERT | `.sparql` | `INSERT DATA` for RDF stores |
| `shacl` | SHACL Shapes | `.ttl` | W3C SHACL node shapes |
| `pgql` | PGQL Script | `.pgql` | Oracle property-graph export |

**Step by step.**

1. Export the whole graph + ontology as JSON-LD:

   ```bash
   curl -s "http://localhost:8000/api/v1/ontology/export?limit=5000" -o ontology.jsonld
   ```

2. Convert the graph to Turtle:

   ```bash
   curl -s -X POST http://localhost:8000/api/v1/graph/convert \
     -H 'Content-Type: application/json' \
     -d '{"format_id": "rdf", "limit": 5000}' -o graph.ttl.json
   ```

3. Import a JSON-LD document (optionally clearing the store first):

   ```bash
   curl -s -X POST "http://localhost:8000/api/v1/ontology/import?clear=false" \
     -H 'Content-Type: application/json' --data-binary @ontology.jsonld
   ```

**Response/result.** `/graph/convert` returns `{format, extension, label,
content, content_length}`. The JSON-LD context maps EOIP terms under
`urn:eoip:ontology:` with `eoip:entity/<Label>` types and
`eoip:relation/<LABEL>` predicates; properties appear as `property_<name>`
terms. `/ontology/import` returns an import summary; `limit` outside 1–10000
raises `ValueError` ("JSON-LD export limit must be between 1 and 10000").

**Errors and recovery.** `422` on malformed import documents or unknown
`format_id` (message lists available formats). `POST
/api/v1/ontology/validate/shacl` returns `422` with `detail:
"SHACL_VIOLATION"` (or `"UNSUPPORTED_CONSTRAINT"`) plus a full `report`; `503`
when the validator is unavailable. Fix violating data or relax the shape and
retry.

---

## 7. SKOS taxonomy

**What it does.** `packages/eoip/ontology/skos.py` is a full SKOS taxonomy
manager: versioned `ConceptScheme`s, multilingual `Concept`s with
pref/alt/hidden labels, broader/narrower hierarchy (with cycle policies),
crosswalk `ConceptMapping`s, integrity validation, and SKOS JSON-LD export.

**How to access** (`apps/api/extended.py`):

- `POST /api/v1/taxonomy/schemes` (201) — create a scheme
- `GET /api/v1/taxonomy/schemes` — list schemes
- `POST /api/v1/taxonomy/concepts` (201) — add a concept
- `GET /api/v1/taxonomy/concepts?scheme=<id>` — list concepts
- `POST /api/v1/taxonomy/mappings` (201) — add a crosswalk mapping
- `GET /api/v1/taxonomy/mappings` — list mappings
- `GET /api/v1/taxonomy/validate?scheme=<id>` — integrity issues + label
  conflicts
- `GET /api/v1/taxonomy/export.rdf` — SKOS JSON-LD (`application/ld+json`)

**Step by step.**

1. Create a scheme:

   ```bash
   curl -s -X POST http://localhost:8000/api/v1/taxonomy/schemes \
     -H 'Content-Type: application/json' \
     -d '{"title": "Service Taxonomy", "description": "Checkout domain services"}'
   # → {"scheme_id": "...", "title": "Service Taxonomy", "version_id": "1.0.0", ...}
   ```

2. Add concepts (request fields per `SkosConceptRequest`: `scheme_id`,
   `pref_label`, optional `concept_id`, `definition`, `notation`,
   `alt_labels`, `hidden_labels`):

   ```bash
   curl -s -X POST http://localhost:8000/api/v1/taxonomy/concepts \
     -H 'Content-Type: application/json' \
     -d '{"scheme_id": "<scheme_id>", "pref_label": "Checkout",
          "definition": "The checkout service domain",
          "alt_labels": ["check-out", "checkout-flow"]}'
   ```

3. Add a mapping. `kind` must be one of `exactMatch`, `closeMatch`,
   `broadMatch`, `narrowMatch`, `relatedMatch` (`MappingKind`):

   ```bash
   curl -s -X POST http://localhost:8000/api/v1/taxonomy/mappings \
     -H 'Content-Type: application/json' \
     -d '{"source_id": "<concept_a>", "target_id": "<concept_b>",
          "kind": "exactMatch"}'
   ```

4. Validate and export:

   ```bash
   curl -s "http://localhost:8000/api/v1/taxonomy/validate?scheme=<scheme_id>"
   curl -s http://localhost:8000/api/v1/taxonomy/export.rdf -o taxonomy.jsonld
   ```

**Response/result.** Validate returns `{"integrity_issues": [{kind, detail,
concept_ids}], "label_conflicts": [{scheme_id, pref_label, concept_ids,
language}]}`. Integrity kinds: `orphan_concept`, `broader_cycle`,
`narrower_cycle`. Broader/narrower links are managed in the library
(`add_broader`, skos.py:519); no HTTP route for hierarchy editing was found
**[not runtime-verified as an API]**.

**Errors and recovery.** Invalid scheme/concept references or duplicate
prefLabels surface as 4xx via `_raise_skos` (`ValueError`/`KeyError` →
HTTP error). Label conflicts are *reported* by `/validate`, not blocked at
write time — run validate after bulk loads.

---

## 8. Domain packs

**What it does.** Domain packs (`packages/eoip/ontology/packs.py`) are
ontology-shaped YAML extensions under `config/domain-packs/<name>/`
(`pack.yaml` metadata + `ontology.yaml` definitions). Packs **extend** the
core ontology — they never replace it; collisions with core terms are
conflicts unless declared with `extends_core: true`.

**The 8 installed packs** (from `config/domain-packs/*/pack.yaml`, all
`version: "1.0.0"`, `extends: core`):

| pack | contents |
|------|----------|
| `bfsi` | trade, account, policy concepts with regulatory traces onto WORK/BUSINESS |
| `compliance` | controls, policies, audit findings, evidence chains (META/DECISION) |
| `cybersecurity` | vulnerabilities, threats, security findings, asset exposure (CODE/OPS) |
| `data-governance` | datasets, data products, lineage (KNOWLEDGE/META) |
| `healthcare` | `Encounter`, `Order`, `Drug`, `Lot`, `Device`, `Protocol`, `Site` (OPS/PROCESS/BUSINESS) |
| `itsm` | ITIL problem, SLA, CMDB relationships extending `Incident`/`ChangeRequest`/`ServiceRequest` |
| `manufacturing` | `Part`, `BOM`, `Supplier`, `Plant`, `WorkOrder`, `QualityEvent` (ISA-95-style tracing) |
| `software-engineering` | agile estimation, code-review, release-quality relationships (WORK/CODE/CICD) |

**How to access.** `GET /api/v1/ontology/packs` and
`GET /api/v1/ontology/packs/{name}` (`apps/api/extended.py`).

**Step by step.**

1. List installed packs:

   ```bash
   curl -s http://localhost:8000/api/v1/ontology/packs
   # {"packs": [{"name": "bfsi", "version": "1.0.0", "extends": "core", ...}, ...]}
   ```

2. Inspect and validate one pack:

   ```bash
   curl -s http://localhost:8000/api/v1/ontology/packs/healthcare
   ```

**Response/result.** `{name, valid, metadata, classes (sorted labels),
extensions, conflicts}`. Validation rules (in `validate_pack`):
`ontology_version`/`schema_version` must equal the core manifest (`0.4.0` /
`1.2`); `extends` must be `"core"`; declared domains must exist; property
types must be one of `TEXT, INT, LONG, DOUBLE, BOOLEAN, DATE`; class/edge
labels matching core require `extends_core: true`; new edge labels must have
non-empty `out`/`in` endpoints drawn from known labels.

**Errors and recovery.** `404` for an unknown pack name. `422` with the full
conflict list when a pack is invalid — fix the pack's YAML (e.g. add
`extends_core: true`, correct a property type) and re-request. Note
`load_all_packs()` raises on any invalid pack, so a broken pack blocks startup
paths that load all packs.

---

## 9. Truth and claims

**What it does.** `packages/eoip/truth/` implements an immutable claim model:
sources assert `Claim`s about a `(subject_id, predicate)` pair; differing
values are contradictions; a resolution policy selects a `CanonicalAssertion`
with a recorded `ResolutionDecision`. Rejected/obsolete claims are retained
for audit — never deleted (TRUTH-009).

**Key fields** (`Claim` in `truth/models.py`): `claim_id` (URN
`urn:eoip:truth:claim:<id>`), `subject_id`, `predicate`, `value`,
`source_id`, `source_authority` (0–1), `extraction_confidence` (0–1),
optional `validation_confidence`, `asserted_at`, `status`
(`pending|accepted|rejected|obsolete`). Ranking uses
`composite_score = source_authority * extraction_confidence * (0.5 + 0.5 * validation_confidence)`.

**How to access** (`apps/api/extended.py`):

- `POST /api/v1/truth/claims` (201) — register a claim
- `GET /api/v1/truth/contradictions` — all conflicting groups
- `POST /api/v1/truth/resolve` — resolve via policy
- `GET /api/v1/truth/assertions/{subject_id}/{predicate}` — canonical fact
- `GET /api/v1/truth/explain/{subject_id}/{predicate}` — why this fact won
- `GET /api/v1/truth/export` — deterministic JSON snapshot

**Step by step.**

1. Two sources disagree about the `checkout` service owner:

   ```bash
   curl -s -X POST http://localhost:8000/api/v1/truth/claims \
     -H 'Content-Type: application/json' -d '{
       "claim_id": "urn:eoip:truth:claim:a1",
       "subject_id": "urn:eoip:code:service:checkout",
       "predicate": "owner", "value": "team-payments",
       "source_id": "urn:eoip:meta:datasource:servicenow",
       "source_authority": 0.9, "extraction_confidence": 0.8}'
   curl -s -X POST http://localhost:8000/api/v1/truth/claims \
     -H 'Content-Type: application/json' -d '{
       "claim_id": "urn:eoip:truth:claim:b2",
       "subject_id": "urn:eoip:code:service:checkout",
       "predicate": "owner", "value": "team-commerce",
       "source_id": "urn:eoip:meta:datasource:jira",
       "source_authority": 0.6, "extraction_confidence": 0.95}'
   ```

2. List contradictions: `curl -s http://localhost:8000/api/v1/truth/contradictions`.

3. Resolve. Policies (`SUPPORTED_POLICIES`): `highest-authority`
   (default), `highest-confidence`, `newest`, `manual`:

   ```bash
   curl -s -X POST http://localhost:8000/api/v1/truth/resolve \
     -H 'Content-Type: application/json' -d '{
       "subject_id": "urn:eoip:code:service:checkout",
       "predicate": "owner", "policy": "highest-authority"}'
   ```

   For manual adjudication add `"policy": "manual",
   "adjudicator": "sindhuja@example.com", "manual_choice":
   "urn:eoip:truth:claim:b2"`.

4. Explain why the fact was selected:

   ```bash
   curl -s http://localhost:8000/api/v1/truth/explain/urn:eoip:code:service:checkout/owner
   ```

**Response/result.** Resolve returns the `ResolutionDecision` (`decision_id`,
`policy`, `chosen_claim_id`, `competing_claim_ids`, human-readable
`rationale`). Explain returns `{canonical, decision, chosen_claim,
competing_claims, explanation}` — the explanation includes the winning claim's
authority/extraction/composite scores. The winner becomes `accepted`, losers
`rejected`; identical-value older claims become `obsolete`.

**Errors and recovery** (all → HTTP 422): unknown/disabled policy; `manual`
without `adjudicator`; `manual_choice` not among competing claims; resolving a
pair with no contradictory claims. `GET .../assertions/...` returns `404` when
no canonical assertion exists yet. The truth store is in-memory with JSON
export/import (`GET /api/v1/truth/export`); restart persistence beyond that
snapshot is **[not runtime-verified]**.

Separately, `packages/eoip/claims/` is a **different** subsystem — a product
claims register (patent candidates, competitor scorecards, standards-clause
mapping, `ClaimRecord`) used for IP/compliance positioning, not the runtime
truth model above.

---

## 10. Validation engine and quality metrics

**What it does.** Two layers (`packages/eoip/validation/`):

- **Hard gate** (`gate.py`): runs *before* every write in both store
  implementations. Blocks unknown vertex/edge labels, empty `canonical_id`,
  unknown property keys, and invalid edge endpoints by raising
  `MutationBlocked` — the fact is never persisted.
- **Soft engine** (`engine.py`, `ValidationEngine.run()`): a post-ingestion
  scan that emits findings and persists them as `ValidationRun` /
  `ValidationFinding` vertices (linked `VALIDATED_BY`).

**Finding rules** (severity): `unknown_vertex_label` (ERROR),
`required_properties` (ERROR), `missing_canonical_id` (ERROR),
`unknown_edge_label` (ERROR), `endpoint_types` (ERROR),
`dangling_endpoint` (ERROR), `invalid_creation_status` (ERROR),
`missing_evidence` (WARNING, for `IMPLEMENTS`/`REFERENCES`/`DOCUMENTS`/
`MODIFIES`/`DECLARES` edges lacking `evidence_key`),
`missing_creation_status` (WARNING), `ambiguous_needs_review` (WARNING, for
`creation_status: AMBIGUOUS`), `orphan_vertex` (WARNING), `deletion_conflict`
(WARNING). Valid `creation_status` values: `DETERMINISTIC`, `INFERRED`,
`AMBIGUOUS`, `MANUAL`, `HUMAN_CONFIRMED`.

**Quality metrics** (`quality.py`, `QualityMetrics`): `total_vertices`,
`total_edges`, `total_findings`, `error_count`, `warning_count`, and seven
ratios — `evidence_coverage`, `provenance_coverage`, `orphan_rate`,
`duplicate_rate`, `freshness` (30-day window), `completeness`,
`schema_compliance`. Each ratio is `None` (not a misleading 0/100%) when its
denominator is empty (FR-VALID-003).

**How to access.** `POST /api/v1/admin/validation` (run now; also writes
`state/validation.json`), `GET /api/v1/validation/runs` (history, newest
first), and async `POST /api/v1/semantic/validations` (202; requires an
`Idempotency-Key` header).

**Step by step.**

1. Run validation:

   ```bash
   curl -s -X POST http://localhost:8000/api/v1/admin/validation
   ```

2. Review run history:

   ```bash
   curl -s "http://localhost:8000/api/v1/validation/runs?limit=10"
   ```

3. For each finding, fix the underlying data (or confirm an `AMBIGUOUS`
   entity via the identity-candidate review endpoints
   `GET /api/v1/identity/candidates` → `POST
   /api/v1/identity/candidates/{id}/decide`), then re-run.

**Response/result.** Run result: `{run_id, started_at, finished_at, findings,
valid, partial, vertices_checked, edges_checked, quality}`. `valid` is false
if any finding has severity `ERROR`; `partial` is true when the scan hit the
10,001 vertex/edge limits (treat results as incomplete on large graphs).

**Errors and recovery.** A write rejected with `mutation blocked for <label>:
<reason>` (HTTP 422 from ingestion routes) means a hard invariant failed —
correct the label/property/endpoint in the payload; there is no override. If
`_persist_run` fails, the run raises after logging
`validation.persistence_failed`.

---

## 11. Architecture conformance rules

**What it does.** `packages/eoip/graph/conformance.py` compiles a declarative
architecture-rule DSL into graph queries and reports violating paths.

**DSL grammar** (from `parse_rules`):

```
RULE <id>: <source> MUST_NOT_DEPEND <target> [SEVERITY <level>] [DEPTH <n>]
RULE <id>: <source> MUST_NOT_ACCESS <target>
RULE <id>: <source> MUST_HAVE <property-or-connected-label>
RULE <id>: <source> MUST_NOT_CROSS <domain>
```

`<source>`/`<target>` resolve to a vertex label, a domain name, or a name
substring. `MUST_NOT_DEPEND` is transitive reachability (BFS, default depth 4,
governance edges excluded); `MUST_NOT_ACCESS` flags a single direct edge;
`MUST_HAVE` requires a property or a connection to the named label;
`MUST_NOT_CROSS` flags edges into the named domain.

**How to access** (`apps/api/app.py`):

- `POST /api/v1/conformance/check` — body accepts `rules_dsl` (DSL text),
  `rules` (list of `{id, kind, source, target, severity?, max_depth?}`), or
  `ruleset` (name of a stored rule set)
- `GET /api/v1/conformance/rules` — list stored rule sets
- `PUT /api/v1/conformance/rules/{name}` — save a rule set
  (`{"rules_dsl": "..."}`)

**Step by step.**

1. Save a rule set:

   ```bash
   curl -s -X PUT http://localhost:8000/api/v1/conformance/rules/payments-boundary \
     -H 'Content-Type: application/json' -d '{"rules_dsl":
       "RULE NO-UI-TO-DB: APIService MUST_NOT_DEPEND Database SEVERITY ERROR DEPTH 4\nRULE SVC-NEEDS-EVIDENCE: Service MUST_HAVE Evidence\nRULE NO-OPS-LEAK: CODE MUST_NOT_CROSS OPS"}'
   ```

2. Run it:

   ```bash
   curl -s -X POST http://localhost:8000/api/v1/conformance/check \
     -H 'Content-Type: application/json' -d '{"ruleset": "payments-boundary"}'
   ```

   Or inline: `{"rules_dsl": "RULE R1: checkout MUST_NOT_ACCESS Database"}`.

**Response/result.** `{rules_checked, findings, total_violations, errors,
warnings, conformant}`. Each finding has `rule_id`, `severity`, `message`,
`violating_path`, `source_file`, `source_symbol`. `conformant` is true only
when there are no ERROR findings.

**Errors and recovery.** `400` if none of `rules_dsl`/`rules`/`ruleset`
given; `404` for an unknown ruleset name; `422` when saving an invalid rule
set. Empty findings with `conformant: true` is success — not a bug.

---

## 12. The graphtest framework

**What it does.** `packages/eoip/graphtest/framework.py` is a declarative,
deterministic (no-LLM) assertion engine: a YAML/JSON suite of assertions run
against the graph, producing a machine-readable report with violating
nodes/edges.

**The 12 assertion types** (`AssertionType`):

`path_exists`, `path_forbidden`, `cardinality`, `required_relationship`,
`no_orphan`, `no_cycle`, `data_type`, `ownership`, `provenance_present`,
`temporal_validity`, `architecture_boundary`, `traceability_coverage`.

Key assertion fields: `source_label`, `target_label`, `label`,
`relationship`, `via` (allowed edge labels), `max_depth` (default 4),
`min_count`/`max_count`, `property` + `expected_type`
(`string|integer|number|boolean|array|object`), `filters` (property
equality), `provenance_edges` (default `EVIDENCED_BY, INGESTED_IN,
PRODUCED_BY`), `ownership_edge` (default `OWNED_BY`), `coverage_threshold`,
`as_of`. Note: the default ownership edge `OWNED_BY` is not a core manifest
edge label — pass `ownership_edge: ASSIGNED_TO` (to `Person`) for core data.

**How to access.** `POST /api/v1/graph-tests/run` (`apps/api/extended.py`) —
always HTTP 200 when the suite is well-formed, even if assertions fail. CLI:
`python -m eoip.graphtest suite.yaml --store memory` (exit code 1 on failure).

**Step by step** — a full example suite for tenant `t-001` data:

```yaml
id: checkout-quality
name: Checkout graph quality gate
description: Structural checks for the checkout service graph
project: EOIP
assertions:
  - id: workitem-implemented
    type: required_relationship
    source_label: WorkItem
    relationship: IMPLEMENTS
    filters: {issue_key: EOIP-123}
  - id: checkout-documented
    type: path_exists
    source_label: Document
    target_label: Service
    via: [DOCUMENTS]
    max_depth: 2
  - id: no-ui-db-path
    type: path_forbidden
    source_label: APIService
    target_label: Database
    max_depth: 4
  - id: one-owner
    type: ownership
    label: Service
    ownership_edge: ASSIGNED_TO
    owner_label: Person
  - id: provenance
    type: provenance_present
    label: WorkItem
  - id: test-coverage
    type: traceability_coverage
    source_label: WorkItem
    target_label: TestCase
    via: [TESTS]
    coverage_threshold: 80.0
  - id: code-acyclic
    type: no_cycle
    label: CodeSymbol
    via: [CALLS]
  - id: schema-types
    type: data_type
    label: TestRun
    property: passed_count
    expected_type: integer
```

Run it:

```bash
curl -s -X POST http://localhost:8000/api/v1/graph-tests/run \
  -H 'Content-Type: application/json' --data-binary @checkout-quality.yaml
```

**Response/result.** `{suite_id, suite_name, total, passed, failed,
conformant, results: [{id, type, passed, message, violating_nodes,
violating_edges, measured}]}` — e.g. `traceability_coverage` reports
`measured: {coverage_pct, linked, total}`; `path_exists` reports
`measured: {sources, reachable}`.

**Errors and recovery.** Malformed suites → `422` (Pydantic `ValidationError`
listing the bad field). An assertion with an unknown `type` fails with message
`Unsupported assertion type` rather than crashing the suite. `path_exists`
fails with "Source or target vertices not found" when a label matches nothing
— check `filters` and label spelling against `GET /api/v1/graph/schema`.

---

*End of chapter. All endpoints and field names above are taken verbatim from
`apps/api/app.py`, `apps/api/main.py`, `apps/api/extended.py`, and the
`packages/eoip/` modules cited inline.*
