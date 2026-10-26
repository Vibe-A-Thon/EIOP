# C14 Airbyte (Tier B)

| Field | Value |
|---|---|
| Registry ID | T-C14-airbyte |
| Tier | B (connector ecosystem; licence to verify) |
| Versions examined | platform version UNVERIFIED (GitHub Releases page rendered empty); repo LICENSE and docs 2026 |
| Verified on | 2026-10-26 (brief: 2026-10-18) |
| Worker | V27 |

## 1. Identity, current status, tier, and sources
Airbyte, Inc.; ELT platform with a large catalogue of source/destination connectors speaking the Airbyte Protocol. Active (copyright 2026; docs page "last updated" 2026-06-29 on the licence post) [CLAIM-airbyte-01, -04]. Offerings: Airbyte Core self-hosted, Cloud, Enterprise [CLAIM-airbyte-01]. Version and release date: UNVERIFIED, confidence 0.2. Sources: repo README/LICENSE, docs licence page, 2023 licence blog, search summary of the licence FAQ.

## 2. Problem, workloads, workflows
Scheduled/incremental replication from SaaS APIs and databases to warehouses/lakes. EOIP workflow: Airbyte source container reads Jira/Salesforce etc., a custom destination writes `SourceEvent` records to EOIP ingestion (never graph writes, BL-23), state messages become source checkpoints (`source_checkpoint.schema.json`, BL-24).

## 3. Feature inventory
| Feature | Status | Claim |
|---|---|---|
| Source/destination connectors via Airbyte Protocol (stdout JSON messages: RECORD, STATE, LOG) | present (protocol shape from general knowledge, 0.6) | 02 |
| Incremental sync with cursor/state; full refresh; CDC for selected DBs (Debezium-based, general knowledge 0.5) | believed present | 06 |
| Connector Builder / low-code CDK, Python CDK | believed present, UNVERIFIED | 06 |
| UI, API, Terraform, orchestration integrations | believed present, UNVERIFIED | 06 |
| Enterprise: extra security features on top of OSS | enterprise-only [CLAIM-airbyte-01] | 01 |
| Source-ACL propagation (permissions streams) | UNVERIFIED | 06 |
| DLQ | absent as primitive (failed records are logged/failed per sync; reasoned 0.4) | 06 |

## 4. Architecture
```
 [Source connector container] --Airbyte Protocol msgs--> [Platform worker/orchestrator] --> [Destination container]
        ^ state/checkpoint                                   |  metadata DB, Temporal-like workflow engine (UNVERIFIED)
 UI/API/scheduler -----------------------------------------/
```

## 5. Under-the-hood reconstruction
Hypothesis (0.5): each sync launches source and destination as containers connected through a worker; STATE messages emitted by a source are persisted after the destination acknowledges, giving at-least-once with checkpoint-resume. Backfills = reset state + full refresh; rate limits handled inside each connector (CDK backoff, UNVERIFIED). This is the reconstructable pattern: connector = process emitting typed messages + opaque state blob. NOT PUBLICLY VERIFIED beyond the above in this session.

## 6. Requirements inferred
FR: per-stream state, schema discovery, incremental cursors, resettable backfill. NFR: container runtime, metadata DB, container-per-sync overhead.

## 7. Performance and resource model
No benchmark collected. Footprint: multi-component platform with container launches per sync (general knowledge; one-node first is not its design centre; UNVERIFIED). Failure modes: connector API rate limits, schema drift, whole-sync failures.

## 8. Strengths
Breadth of API/database connectors and a stable protocol that EOIP could implement as a *destination* only; state-message checkpoint model. Match: EOIP's own connector SDK already emits `SourceEvent` and checkpoints; the gap is connector breadth, not mechanism.

## 9. Limitations
Licensing (verified, see 10): mixed ELv2/MIT/commercial with contradictory official wording. Operational: container-heavy platform. Friction: row/record shaped output, no entity/ontology semantics, ACL not carried by default (UNVERIFIED). Hosted-service restriction blocks white-label SaaS exposure of Airbyte's UI/API.

## 10. Deployment, licensing, redistribution, operational viability
Findings (all legal-review triggers, no legal conclusion):
- Repo root `LICENSE` text fetched is the Elastic License 2.0 only; `LICENSE_SHORT` is a 2026 Airbyte copyright notice [CLAIM-airbyte-02]. ELv2 forbids providing the software to third parties as a hosted/managed service giving access to substantial functionality, circumventing licence keys, and removing notices [CLAIM-airbyte-02].
- Docs licence page: connectors and everything in public repos except `airbyte-protocol` are ELv2; protocol is MIT; Cloud, Enterprise and Agents need a commercial licence [CLAIM-airbyte-03].
- 2023 licence post: ELv2 extended to named strategic connectors (Oracle, Postgres, MSSQL, MongoDB, MySQL, S3, GCS, Facebook Marketing, Google Ads/GA4/Search Console/Sheets, HubSpot, Marketo, Salesforce, Shopify, Stripe, Zendesk Support; destinations BigQuery, GCS, Redshift, S3, Snowflake); community connectors keep their own licences, mostly MIT [CLAIM-airbyte-04].
- A search-surfaced FAQ text says "Connectors are MIT; Core is ELv2", contradicting the docs page [CLAIM-airbyte-05]; resolution: check each connector's `metadata.yaml`.
Class: source-available / mixed. White-label bundling of Airbyte Core inside a multi-tenant product exposing its UI/API is the high-risk case. Air-gap: partial (self-hosted works; connector images must be mirrored, UNVERIFIED).

## 11. Delta vs baseline
BL-23: EOIP has a SourceEvent connector contract and recent client connectors (Snowflake, Artifactory, Slack, Splunk, etc., NB-06, live-unverified); Airbyte offers hundreds more but under mixed licences. BL-24: checkpoint/replay present at HEAD, including `jobs.py` `DurableJobStore`. BL-60 unaffected.

## 12. Cards
STR-airbyte-01 | Airbyte | protocol-level connector contract (records + state) with a huge catalogue | CLAIM-airbyte-03 | connector breadth | match (protocol only) | implement an Airbyte-protocol-compatible *reader* shim: run MIT-licensed or community connectors as subprocesses and map RECORD/STATE to SourceEvent/checkpoint | test: run a community MIT connector, kill mid-sync, resume from STATE, no duplicates after dedupe.
INV-airbyte-01 | Airbyte | mixed ELv2/MIT licences block redistribution inside a white-label product [CLAIM-airbyte-02..05, proven for text, impact hypothesis] | cause: licensing. A: customer-installed Airbyte beside EOIP (integrate over API); B: EOIP-native connector SDK + protocol shim for MIT connectors only; C: in-house connector marketplace with licence metadata gate. Select B+C. Worse where customers need a ELv2 strategic connector. POC: licence-scan 20 connectors via `metadata.yaml`, auto-classify. Decision ADOPT (licence gate), EXPERIMENT (shim). No seed hypothesis from 10.5 targets Airbyte.

## 13. Decisions
CAP-26 connector breadth: INTEGRATE (customer-run Airbyte via API, never bundled) ; Protocol: REUSE (MIT); platform bundling: REJECT pending legal review; CAP-79 supply chain: BUILD licence gate.

## 14. Tests
Protocol shim contract test; licence classifier test over connector metadata; resume-from-STATE chaos test. Acceptance: ELv2 components never in the redistributed artifact. PROPOSED.

## 15. Risks / questions
Version/cadence unknown; ACL support unknown; official licence docs inconsistent; whether destination-only integration still counts as "providing as service". Legal review needed.

## Appendix A. Dimension coverage
| D | Sections | Summary |
|---|---|---|
| D1 | 1,10 | licence mixed |
| D2 | 2 | ELT |
| D3 | 4 | containers, protocol |
| D4-D7,D12-D14,D16,D19 | N/A | not graph/query |
| D8 | 7 | UNVERIFIED |
| D9 | 3,5 | incremental, backfill, rate limit |
| D10 | 9 | ACL UNVERIFIED |
| D11 | 5 | reset state |
| D15,D17 | 3 | CDK UNVERIFIED |
| D18 | 3 | enterprise |
| D20 | 7 | none |
| D21 | 10 | key |
| D22 | 5 | protocol portable |
| D23 | N/A | none |
| D24 | App. C | conflicting |

## Appendix B. Capability mapping
| CAP | Airbyte | Claim | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-26 | native | 03 | BL-23 Impl | INTEGRATE | P1 |
| CAP-27 | partial | 06 | BL-24 Impl | REUSE (state model) | P3 |
| CAP-46 | unknown | 06 | BL-18 | BUILD | P1 |
| CAP-77 | n/a | 02-05 | BL-22 | BUILD licence gate | P1 |
| CAP-50 | partial | 01 | n/a | EXPERIMENT | P2 |

## Appendix C. Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| airbyte-01 | repo README | MIT and ELv2 badges; Core/Cloud/Enterprise; LICENSE_SHORT 2026 copyright | Officially documented | https://github.com/airbytehq/airbyte | acc 2026-10-26 | 0.7 | Releases empty |
| airbyte-02 | repo LICENSE | text is Elastic License 2.0 | Observed (licence file) | https://raw.githubusercontent.com/airbytehq/airbyte/master/LICENSE | acc 2026-10-26 | 0.85 | docs/FAQ say protocol MIT |
| airbyte-03 | docs | connectors and public repos ELv2 except protocol MIT; Cloud/Enterprise/Agents commercial | Officially documented | https://docs.airbyte.com/community/licenses/ | acc 2026-10-26 | 0.8 | FAQ differs |
| airbyte-04 | 2023-06-30 post | ELv2 extended to listed strategic connectors; community connectors mostly MIT | Officially documented | https://airbyte.com/blog/update-on-airbytes-license | pub 2023-06-30, upd 2026-06-29, acc 2026-10-26 | 0.8 | docs wording |
| airbyte-05 | FAQ | "Connectors MIT, Core ELv2" | Third-party report (search summary) | https://airbyte.com/license-faq | acc 2026-10-26 | 0.4 | contradicts 03 |
| airbyte-06 | n/a | protocol messages, CDK, CDC, containers, ACL | Reasoned inference | n/a | n/a | 0.4 | not fetched |

## Appendix D. Assumptions
No legal conclusion drawn. Version left UNVERIFIED rather than guessed.
