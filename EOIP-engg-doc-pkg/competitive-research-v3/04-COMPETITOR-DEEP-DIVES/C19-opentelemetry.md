# C19 — OpenTelemetry, Prometheus, Grafana

| Field | Value |
|---|---|
| Registry ID | T-C19-opentelemetry |
| Tier | B (observability stack) |
| Versions examined | OTel Collector v0.163.0 / core v1.69.0 (14 Oct); Prometheus v3.15.1 (21 Oct 2026); Grafana v13.2.4 (13 Oct). Years not shown for two, 2026 inferred |
| Verified on | 2026-10-26 |
| Worker | V11 |

## 1. Identity, status, sources
| Member | Owner / governance | Licence | Status |
|---|---|---|---|
| OpenTelemetry (spec, SDKs, Collector, OTLP) | CNCF; the CNCF project list fetched shows **Graduated** (accepted 2019-05-07) [CLAIM-ot-01] - conflicts with my prior understanding (Incubating); confidence 0.5, re-check | Apache-2.0 (project knowledge, 0.85) | active |
| Prometheus | CNCF **Graduated** (accepted 2016-05-09) [CLAIM-ot-01] | Apache-2.0 (project knowledge, 0.85) | active, v3.x |
| Grafana | Grafana Labs | **AGPL-3.0-only** (verified); Apache-2.0 exceptions listed in `LICENSING.md` [CLAIM-ot-02]; relicensed from Apache-2.0 on 2021-04-20 [CLAIM-ot-03] | active v13 |
**Flag: Grafana AGPL-3.0 is a legal-review trigger** for bundling/white-labelling/modifying and exposing over a network (record only). Alternatives that avoid it: Prometheus UI, Perses (not examined), customer-supplied Grafana as separate component. Loki/Tempo are also AGPL (announcement, CLAIM-ot-03); not examined further.

## 2. Problem and workflows
Vendor-neutral telemetry (traces, metrics, logs) with correlation, pull-based metrics storage and alerting, and dashboards. Workflow: EOIP API span (carries `X-Correlation-ID`) -> OTLP/HTTP -> Collector (batch, redact, route) -> Prometheus/trace backend -> dashboards; Prometheus scrapes `/metrics`.

## 3. Feature inventory
| Capability | Status |
|---|---|
| OTel API/SDK per language, OTLP, semantic conventions | present |
| Collector (receivers, processors, exporters), tail sampling, attribute redaction | present (processors details not re-verified; 0.7) |
| GenAI semantic conventions for LLM spans | present/in development (UNVERIFIED status) |
| Prometheus TSDB, PromQL, scrape, Alertmanager, remote write | present |
| Grafana dashboards, alerting, data-source plugins | present |
| Per-tenant isolation in metrics | partial (labels; Mimir/Cortex multi-tenancy not examined) |
| Audit-integrity logging | absent (not the purpose) |

## 4. Architecture
```
App (OTel SDK) --OTLP/HTTP--> [Collector: receivers -> processors(batch, redact, sample) -> exporters]
                                  |-> trace backend (Tempo/Jaeger)   |-> Prometheus (remote write)
Prometheus --scrape /metrics--> TSDB (local blocks, WAL) --PromQL--> Grafana / Alertmanager
```

## 5. Under-the-hood reconstruction
- OTel: a Resource (service identity) plus signals; traces are spans with trace/span IDs propagated by W3C `traceparent`; SDK batches spans and exports OTLP; the Collector is a pipeline of components wired by config (public knowledge; docs not fetched this run, 0.7).
- Prometheus: pull model; samples (timestamp, float) in per-series chunks; head block in memory with WAL, compacted into immutable 2-hour blocks, label inverted index; PromQL over instant/range vectors. Cardinality (unique label sets) drives memory. (Public architecture knowledge, 0.75.)
- Grafana: stateless-ish server with a database for dashboards/users, plugin data sources, query proxying; provisioning via files.
- Security: OTLP endpoints and `/metrics` need authn/TLS; span attributes can leak prompts/PII, so redaction in the Collector is mandatory for EOIP (BL-46).

## 6. Requirements inferred
FR: correlation ID on every log/trace; RED metrics per route; per-tenant dimension without raw identifiers; LLM-call spans without prompt text by default. NFR: telemetry never changes graph facts; optional and fail-open (as `otel.py`).

## 7. Performance and resource model
No benchmarks fetched: **UNVERIFIED**. Known drivers (hypothesis): Prometheus RAM scales with active series; trace volume needs sampling; Collector adds one hop. One-node footprint: Prometheus + Grafana + Collector as three optional containers; sizes NOT PUBLICLY VERIFIED here.

## 8. Strengths
Open standards; no vendor lock; wide ecosystem; Prometheus text format already used by EOIP; OTLP permits swap of backend. Match: EOIP already exports Prometheus text and optional OTLP; exceed with LLM/graph-specific semantic attributes.

## 9. Limitations
| Class | Item |
|---|---|
| Licensing | Grafana AGPL-3.0 (and Loki/Tempo) |
| Operational | cardinality explosions; three or four more services; retention tuning |
| Friction | semantic-convention churn, SDK maturity varies by language |
| Security | telemetry as exfiltration channel if exporters point outside the boundary |
| Scope | observability is not audit integrity (CAP-48) |

## 10. Deployment, licensing, viability
Prometheus and OTel: permissive, self-hostable, air-gap viable, no cloud dependency. Grafana: self-hostable but AGPL; EOIP should ship only metrics/trace endpoints plus provisioning JSON dashboards, leaving Grafana as customer-installed (legal review before bundling).

## 11. Delta vs EOIP baseline
BL-49 (Implemented/Partial): `observability/metrics.py` is an in-house registry (Counter, Gauge, Histogram, text exposition, `record_request`); `observability/logging.py` JSON logs; `observability/otel.py` best-effort OTLP/HTTP tracing with correlation header, a documented no-op when SDK missing (optional dependency, not in the lock per baseline); `telemetry_separation.py` (CRA-008.5) separates observed telemetry from inferred causality. Gaps: no Collector config/redaction pipeline, no shipped dashboards or alert rules, no LLM-call or retrieval spans, no tenant-safe metric labelling policy. Unverified: whether tracing is wired in the live app.

## 12. Cards
**STR-ot-01** | OpenTelemetry | vendor-neutral OTLP + Collector redaction | CLAIM-ot-01 | customer-chosen backend, PII-safe spans | integrate | ship Collector config with attribute redaction (prompts/ACL principals dropped); spans for retrieval stages and egress calls | span dump contains no prompt text or principal strings.
**STR-ot-02** | Prometheus | pull metrics and alert rules as code | CLAIM-ot-01 | SRE-ready one-node ops | match | keep in-house exposition (zero dependency), publish `rules.yml` and dashboards-as-JSON | promtool lint passes; alerts fire in fault test.
**INV-ot-01** (Grafana AGPL, licensing, proven) | options: (1) customer-installed Grafana; (2) dashboards as JSON importable to any tool, use Prometheus UI; (3) native admin metrics page (exists in `apps/web` admin, scope UNVERIFIED). Selected 1+2. Decision ADOPT. Defensibility: portability.
**INV-ot-02** (telemetry leakage, hypothesis) | per-tenant labels and ACL strings in attributes expose data to operators; redaction plus tenant-scoped export. Benchmark: leak scan on 1,000 requests. Decision EXPERIMENT.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-75 metrics | REUSE in-house exposition + Prometheus |
| Tracing | INTEGRATE OTel (keep optional) |
| Collector redaction | INTEGRATE (ship config) |
| Grafana | REFERENCE only; do not bundle pending legal review |
| CAP-48 audit integrity | BUILD separately (not OTel) |

## 14. Tests
Scrape contract test; OTLP export to Collector in CI; leak scan of exported spans/logs; cardinality guard (max label set); air-gap run with no outbound telemetry; dashboard JSON validity.

## 15. Risks
OTel maturity-level discrepancy; GenAI conventions unstable; cardinality; AGPL scope interpretation.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | owners, licences |
| D2,D3 | 2,4 | pipeline |
| D4 | 5 | Prometheus TSDB (0.75) |
| D6 | 5 | PromQL only |
| D8 | 5,7 | blocks, WAL |
| D16 | 3 | dashboards |
| D17 | 8 | SDKs |
| D18 | 5,9 | leakage |
| D19 | 3,12 | labels |
| D20 | 7 | UNVERIFIED |
| D21 | 10 | AGPL flag |
| D22 | 8 | OTLP portability |
| D23 | N/A | none found |
| D24 | App C | docs-level |
| D5,D7,D9-D15 | N/A | not applicable |

## Appendix B — Capabilities
| CAP | Native? | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-75 | native | 01 | BL-49 Impl/Partial | REUSE/INTEGRATE | P2 |
| CAP-48 | absent | - | BL-19 | BUILD | P1 |
| CAP-77 | licence | 02,03 | BL-22 | REFERENCE | P2 |
| CAP-49 | partial (redaction) | 01 | BL-45/46 | EXPERIMENT | P2 |

## Appendix C — Evidence
| CLAIM | product | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-ot-01 | CNCF list; Collector v0.163.0; Prometheus v3.15.1 | OTel listed Graduated (2019-05-07), Prometheus Graduated (2016-05-09); release tags | Officially documented | https://www.cncf.io/projects/ ; https://github.com/open-telemetry/opentelemetry-collector/releases/latest ; https://github.com/prometheus/prometheus/releases/latest | 14 and 21 Oct / 2026-10-26 | 0.6 | OTel maturity contradicts prior knowledge |
| CLAIM-ot-02 | Grafana v13.2.4 | distributed under AGPL-3.0-only; Apache exceptions in LICENSING.md | Officially documented | https://github.com/grafana/grafana | 13 Oct / 2026-10-26 | 0.9 | licensor not named on page |
| CLAIM-ot-03 | Grafana | 2021-04-20 move of Grafana, Loki, Tempo from Apache-2.0 to AGPLv3 | Officially documented | https://grafana.com/licensing/ | 2021-04-20 / 2026-10-26 | 0.85 | FAQ answers not rendered |
| CLAIM-ot-04 | EOIP code | metrics.py registry, otel.py optional OTLP, telemetry_separation | Observed in source code | `packages/eoip/observability/*.py` at HEAD 896e06d | n/a / 2026-10-26 | 0.9 | wiring unverified |

## Appendix D — Assumptions
Apache-2.0 for OTel/Prometheus assumed; architecture notes from public knowledge; years inferred.
