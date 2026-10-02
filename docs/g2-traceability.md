# G2 implementation traceability

Updated: 2026-10-03

| Task / requirement | Implementation | Verification | Status |
|---|---|---|---|
| G2-T0001 contract audit | `docs/adr-001-g2-contract-and-revision-model.md` | compatibility table | Complete |
| G2-T0002 SourceEvent v2 | `contracts/source_event.py`, `schemas/source_event_v2.schema.json` | `test_g2_contracts.py` | Complete |
| G2-T0003 revision model | `contracts/revision.py`, graph/relationship revision schemas | `test_g2_contracts.py` | Contract complete; engine is G2-P2 |
| G2-T0004 source registry schema | `contracts/source_registry.py`, source registry/checkpoint schemas | `test_source_registry.py` | Complete |
| G2-T0005 capability interfaces | `connectors/base.py` | fake connector protocol test | Complete |
| G2-T0006 traceability | this document | reviewed with phase exit | Complete |
| G2-T0101 registry CRUD | `connectors/registry.py`, `/api/v1/sources` routes | API and persistence tests | Complete |
| G2-T0102 secret references | source registry validators | rejection tests | Complete |
| G2-T0103 capability metadata | `SourceCapabilities` contract | contract and registry tests | Complete |
| G2-T0104 admin registry UI | not started | — | Pending |
| G2-T0110 local scheduler | `connectors/acquisition.py`, source operation API, worker dispatch | `test_acquisition_fabric.py` | Complete |
| G2-T0111 concurrency/rate limits | `AcquisitionPolicy` admission controls | scheduler limit tests | Complete |
| G2-T0112 pause/resume | source schedule/pause/resume API | scheduler state tests | Complete |
| G2-T0120..0123 webhook gateway | HMAC and Standard Webhooks verification, replay-window enforcement, durable receipt, dedup, source dispatch | gateway/API tests | Complete |
| G2-T0130..0135 controlled crawler | `connectors/crawler.py`, `crawl_scope.schema.json` | extraction, redirect and SSRF tests | Complete |
| G2-T0140..0142 DLQ/replay | existing DLQ plus registered-source replay | existing + acquisition tests | Partial: unified console pending |
| G2-T0150..0153 discovery/dry run | connector discovery contract and generic connector implementations | shared protocol test | Partial: onboarding UI pending |
| G2-P1 generic connector exit | web and local-file connectors emit SourceEvent v2 through one protocol | `test_generic_web_and_file_connectors_share_source_connector_semantics` | Complete |
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

No connector is marked complete solely because its source type can be registered. Live adapter
status requires connector contract and integration tests; unavailable enterprise credentials must
use synthetic fixtures and must not be reported as a successful live integration.
