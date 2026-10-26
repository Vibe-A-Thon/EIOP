### T-C07-eclipse-ditto — Eclipse Ditto

| Field | Value |
|---|---|
| Official URL | https://eclipse.dev/ditto/ ; https://github.com/eclipse-ditto/ditto |
| Owner | Eclipse Foundation (Eclipse IoT project) |
| Latest version + date | 3.9.8 (marked "Latest" on GitHub releases, 08 Oct, year not displayed, presumably 2026); 3.8.14 same day; 3.9.7 on 01 Sep |
| Status | Active (frequent releases) |
| Licence + class | Eclipse Public License 2.0 per site footer (licence text not read) - weak-copyleft, file-level |
| Deployment modes | self-hosted, docker, kubernetes |
| Air-gap viable | yes (self-hosted; no cloud dependency identified) |
| Tier reason | Digital-twin framework; comparison to Azure Digital Twins |

**Relevance.** Eclipse Ditto is open-source IoT middleware implementing the digital-twin pattern: each device ("thing") gets a JSON twin with features and attributes, accessible by APIs and connected to AMQP 0.9.1/1.0, Kafka 2.x, HTTP webhooks, MQTT 3.1.1/5, including via Eclipse Hono or Mosquitto [CLAIM-dit-01,02]. It is a thing registry plus event distribution, not a general knowledge graph; no graph query or reasoning found. For EOIP it is a possible edge-ingestion layer for physical-asset tenants (events -> SourceEvents, BL-23) and an air-gap-friendly alternative to Azure Digital Twins. Touches CAP-26, CAP-27, CAP-52 (n/a). WoT Thing Description support, MongoDB storage and whether the project is a CNCF-style neutral governance: not verified here (recall suggests Thing Description and MongoDB support, UNVERIFIED, confidence 0.4).

**Decision:** REFERENCE-ONLY (INTEGRATE later as optional device-edge source if a physical-asset customer appears).

| CLAIM | product/version/date | claim | class | source | pub/access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| dit-01 | Ditto site | Open-source digital-twin IoT middleware; protocols AMQP, Kafka, HTTP, MQTT; EPL 2.0 footer link | Officially documented | https://eclipse.dev/ditto/ | n/d / 2026-10-26 | 0.7 | licence not in body text |
| dit-02 | Ditto releases | Latest 3.9.8; 3.8.14 same day; 3.9.7 on 01 Sep (year not shown) | Officially documented | https://github.com/eclipse-ditto/ditto/releases | 2026 (inferred) / 2026-10-26 | 0.6 | year unconfirmed |

### T-C07-ona — Organisational network analysis (pattern)

| Field | Value |
|---|---|
| Official URL | none (analytic pattern; no single owner) |
| Owner | n/a |
| Latest version + date | n/a |
| Status | established method (literature) |
| Licence + class | n/a (pattern); implementations vary, e.g. network-analysis libraries - not assessed |
| Deployment modes | embedded as graph query/analytics |
| Air-gap viable | yes |
| Tier reason | Graph pattern record for CAP-80 |

**Relevance.** ONA models people/teams as nodes and communication, collaboration, approval and handoff relations as weighted, time-stamped edges, then computes centrality, brokerage, community structure, bottlenecks and silos. In EOIP terms: an overlay computed from SourceEvents (assignments, reviews, comments, approvals), using BL-43 graph algorithms and BL-37 temporal reads, feeding wisdom/decision graph (BL-56) and J3/J15 questions ("who actually decides?", "which teams are affected?"). Risks: employee-surveillance and privacy/works-council issues; must use aggregated or pseudonymised views, PII policy (BL-46), and ACL-aware answers (BL-18 currently absent), and label output as inferred, not fact (CAP-43). Touches CAP-62, CAP-65, CAP-80, CAP-46. No competitor in V19 batch exposes ONA natively; process mining (C07-process-mining) provides handover-of-work analogues. Method literature is the evidence base; no specific citation was retrieved this session, so claims about method are reasoned inference.

**Decision:** EXPERIMENT. Implement as opt-in, pseudonymised analytics template with human-readable explanation; no individual performance scoring.

| CLAIM | product/version/date | claim | class | source | pub/access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| ona-01 | ONA pattern | Weighted temporal interaction graph + centrality/community metrics is a standard ONA approach | Reasoned inference | none retrieved (UNVERIFIED citation) | - / 2026-10-26 | 0.4 | - |
| ona-02 | EOIP baseline | Graph algorithms exist in-process; ACL enforcement absent in retrieval | Observed in baseline doc | 01-SYSTEM-BASELINE.md BL-43, BL-18 | - / 2026-10-26 | 0.8 | - |
