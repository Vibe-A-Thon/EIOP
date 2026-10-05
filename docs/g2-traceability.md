# G2 implementation traceability

Updated: 2026-10-05

| Task / requirement | Implementation | Verification | Status |
|---|---|---|---|
| G2-T0001 contract audit | `docs/adr-001-g2-contract-and-revision-model.md` | compatibility table | Complete |
| G2-T0002 SourceEvent v2 | `contracts/source_event.py`, `schemas/source_event_v2.schema.json` | `test_g2_contracts.py` | Complete |
| G2-EKAF-003 exact SourceEvent envelope | `SourceEventV2` carries G2 aliases for `source_id`, `source_type`, `source_record_type`, `observed_time`, `evidence_ref` and `correlation_id` while preserving existing v1/v2 fields | `test_v2_event_exposes_g2_envelope_aliases` | Complete |
| G2-T0003 revision model | `contracts/revision.py`, graph/relationship revision schemas | `test_g2_contracts.py` | Contract complete; engine is G2-P2 |
| G2-T0004 source registry schema | `contracts/source_registry.py`, source registry/checkpoint schemas | `test_source_registry.py` | Complete |
| G2-T0005 capability interfaces | `connectors/base.py` | fake connector protocol test | Complete |
| G2-T0006 traceability | this document | reviewed with phase exit | Complete |
| G2 executable coverage | Gap coverage scanner, CLI and API support both legacy GAP docs and `gaps2-*` heading/range requirements via `doc_set=g2` | `test_gap_coverage.py` | Complete |
| G2-ARCH-001..015 guardrails | Executable architecture profile evaluates acquisition contract, API/event-first rules, deterministic graph mutation, evidence, replayability and source-permission guardrails | `test_gap_coverage.py` | Complete |
| G2-OBS-001..006 observability contract | Required traces and metrics are exposed as a machine-readable contract and validator under `/api/v1/gaps/g2/observability-contract` | `test_gap_coverage.py` | Complete |
| G2 full readiness matrix | `/api/v1/gaps/g2/readiness` maps every `gaps2` requirement to concrete modules, routes, UI files or tests and verifies the surfaces are present | `test_g2_readiness.py` | Complete |
| G2-T0101 registry CRUD | `connectors/registry.py`, `/api/v1/sources` routes | API and persistence tests | Complete |
| G2-T0102 secret references | source registry validators | rejection tests | Complete |
| G2-T0103 capability metadata | `SourceCapabilities` contract | contract and registry tests | Complete |
| G2-T0104 admin registry UI | Admin `Sources & jobs` tab now loads registered sources, shows health/modes/checkpoints, supports enable/disable/delete and queues baseline, dry-run, sync, reconcile and replay operations | `npm run build`; `admin-source-registry.spec.js` added, browser execution pending local Playwright Chromium install | Complete |
| G2-T0110 local scheduler | `connectors/acquisition.py`, source operation API, worker dispatch | `test_acquisition_fabric.py` | Complete |
| G2-T0111 concurrency/rate limits | `AcquisitionPolicy` admission controls | scheduler limit tests | Complete |
| G2-T0112 pause/resume | source schedule/pause/resume API | scheduler state tests | Complete |
| G2-T0120..0123 webhook gateway | HMAC and Standard Webhooks verification, replay-window enforcement, durable receipt, dedup, source dispatch | gateway/API tests | Complete |
| G2-T0130..0135 controlled crawler | `connectors/crawler.py`, `crawl_scope.schema.json` | extraction, redirect and SSRF tests | Complete |
| G2-T0140..0142 DLQ/replay | Existing DLQ plus registered-source replay, exposed in the admin recovery console with event-id replay for all replayable DLQ entries | existing + acquisition tests, `npm run build` | Complete |
| G2-T0150..0153 discovery/dry run | Connector discovery contract, generic connector implementations, catalog-backed source onboarding form, discovery preview, and registry dry-run controls | shared protocol test, `npm run build`; `admin-source-registry.spec.js` added, browser execution pending local Playwright Chromium install | Complete |
| G2-P1 generic connector exit | web and local-file connectors emit SourceEvent v2 through one protocol | `test_generic_web_and_file_connectors_share_source_connector_semantics` | Complete |
| G2-EKAF-017 / G2-EKAF-018 drift controls | `connectors/drift.py` classifies source schema drift as compatible/additive/potentially-breaking/breaking and records mapping-version transitions with replay checkpoints/event IDs | `test_ekaf_drift.py` | Complete for deterministic local controls |
| G2-EKAF-022 source conflict preservation | `connectors/conflicts.py` preserves competing source-owned facts as truth claims and leaves canonical resolution to the truth layer | `test_ekaf_conflicts.py`, `test_truth_claims.py` | Complete for acquisition-to-truth handoff |
| G2-T0201..0203 baseline controller | durable ordered manifest with checkpoint/count/failure state | `test_baseline_controller_persists_ordered_restart_manifest` | Complete |
| G2-T0210..0213 change detector | revision/content comparison and unchanged-event short circuit | graph evolution tests | Complete |
| G2-T0220..0222 evolution lifecycle | entity revisions, relationship expiry/replacement, late-event refusal | `test_graph_evolution.py` | Complete |
| G2-T0223 historical state | `GET /api/v1/graph/as-of` | temporal API/unit tests | Complete |
| G2-T0224 graph diff | `GET /api/v1/graph/diff`, versioned schema | temporal API/unit tests | Complete |
| G2-T0225 late event policy | older observations journaled but do not mutate current graph | late-event test | Complete |
| G2-T0230..0232 change journal | fsynced hash-chain journal, cursor API/replay | integrity and API tests | Complete |
| G2-T0240..0243 semantic event bus | post-journal bus plus independently checkpointed quality, cache-invalidation and admin-timeline consumers | consumer cursor/idempotency tests | Complete for local bus; external broker intentionally deferred pending measured need |
| G2-T0250..0253 reconciliation | baseline comparison by canonical ID/content hash, safe missing/stale repair, orphan reporting and persisted report API | reconciliation unit/integration-path tests | Complete |
| G2-T0320 GitHub adapter | versioned REST discovery/baseline/poll/replay/reconcile connector | `test_github_connector.py`, registered baseline test | Complete without live-credential claim |
| G2-T0321 GitHub webhook | HMAC/delivery/event-header gateway plus worker dispatch | webhook gateway tests and connector webhook tests | Complete |
| G2-T0322 PR/Actions/release mapping | temporal Repository/Branch/Tag/Commit/MergeRequest/WorkItem/PipelineRun/Release graph and evidence | `test_github_ingestion.py` | Complete |
| G2-T0323 Pages/docs | bounded README content and Pages source metadata mapped to Document | connector and ingestion tests | Complete |
| G2-T0310 GitLab adapter | GitLab.com/self-managed v4 REST project/group discovery plus baseline/poll/replay/reconcile | `test_gitlab_connector.py`, registered baseline test | Complete without live-credential claim |
| G2-T0311 GitLab webhook | Standard Webhooks signature/timestamp verification, legacy token compatibility and temporal worker dispatch | acquisition gateway and connector webhook tests | Complete |
| G2-T0312 delivery mapping | temporal repository/MR/commit/file/issue/pipeline/job/artifact/release/deployment mapping and evidence | `test_gitlab_rest_ingestion.py` | Complete |
| G2-T0313 Pages/wiki/docs | bounded wiki/README and Pages API metadata plus allowlisted published-site content crawl | connector and ingestion tests | Complete |
| G2-REQ-34 required data contracts | Required G2 schema files exist under `schemas/`, including telemetry, API contract, capsule, simulation, debt/SLO, ontology proposal, causal hypothesis and process event contracts | `test_required_g2_schema_contracts_exist` | Complete |
| G2-QOP-001 / G2-QOP-004 required query APIs | `/api/v1/query/why` and `/api/v1/query/what-changed` route to existing structured query services | `test_g2_required_query_and_simulation_aliases`, `test_query_operators.py` | Complete |
| G2-QOP-003 required WHAT IF API | `/api/v1/query/what-if` routes to the existing what-if parser and simulation overlay, returning confirmation by default and isolated execution when confirmed | `test_g2_required_query_and_simulation_aliases`, `test_simulation.py` | Complete |
| G2-SIM-001..007 required simulation APIs | `/api/v1/simulations` and `/api/v1/simulations/{id}` alias the existing simulation workspace without mutating the authoritative graph | `test_g2_required_query_and_simulation_aliases`, `test_simulation.py` | Complete |
| G2-KD-001..006 / G2-SLO-001..005 required knowledge APIs | `/api/v1/knowledge-debt` and `/api/v1/knowledge-slos` expose existing debt detection and SLO evaluation services | `test_g2_required_knowledge_aliases`, `test_knowledge_debt.py` | Complete |
| GAP-TEMP-001..005 bitemporal graph queries | `graph/bitemporal.py` supports known-at, valid-at, bitemporal slice reconstruction and first-class diffs; mounted under `/api/v1/graph/bitemporal/*` | `test_bitemporal.py` | Complete |
| GAP-TRUTH-001..010 claim truth model | `truth/models.py` and `truth/engine.py` retain competing claims, score authority/confidence, resolve canonical values, support adjudication, and explain choices | `test_truth_claims.py` | Complete |
| GAP-TAX-001 / GAP-STUDIO-005 SKOS taxonomy support | `ontology/skos.py` manages schemes, concepts, labels, relations, import/export and label conflict validation | `test_skos_taxonomy.py` | Complete |
| GAP-KP-001..005 knowledge product catalog | `catalog/products.py` provides product CRUD, lifecycle transitions, filtering, export/import, deletion and lineage navigation | `test_knowledge_products.py` | Complete |
| GAP-SEARCH-001..002 hybrid/faceted search | `search/facets.py` and `retrieval/vectors.py` provide graph-identity-preserving keyword/vector/faceted search | `test_search_facets.py`, `test_retrieval_vector.py` | Complete |
| GAP-RET-002 / GAP-RET-003 / GAP-RET-006 retrieval quality | `retrieval/service.py` exposes keyword/vector/hybrid retrieval with evidence quality, recency, authority ranking and trace output | `test_retrieval_vector.py`, `test_rag_abstention.py` | Complete |
| GAP-GRAPHTEST-001..011 graph assertion framework | `graphtest/framework.py` loads declarative suites and validates paths, cardinality, ownership, provenance, temporal validity, boundaries and traceability coverage | `test_graphtest_framework.py` | Complete |

No connector is marked complete solely because its source type can be registered. Live adapter
status requires connector contract and integration tests; unavailable enterprise credentials must
use synthetic fixtures and must not be reported as a successful live integration.
