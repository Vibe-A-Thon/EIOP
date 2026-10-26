# C18 Tier C records — batch V32

Verified 2026-10-26 (brief date 2026-10-18 superseded by actual access date). Worker V32. Standards: "licence" = document/IP terms; "air-gap" = usable offline as a file/spec.

### T-C18-skos-std — SKOS (Simple Knowledge Organization System)
| Field | Value |
|---|---|
| Official URL | https://www.w3.org/TR/skos-reference/ |
| Owner | W3C (Semantic Web Deployment WG, concluded) |
| Latest version + date | SKOS Reference, W3C Recommendation, 2009-08-18 |
| Status | published W3C Recommendation; no successor found |
| Licence + class | W3C document licence; royalty-free per W3C policy (not re-read); permissive |
| Deployment / air-gap | vocabulary file; yes |
| Tier reason | narrow vocabulary |

Concept schemes, broader/narrower/related, labels. Relevance: taxonomy interchange (CAP-12), thesaurus governance (CAP-41). SKOS is a lightly axiomatised RDF vocabulary: `skos:broader` is not `rdfs:subClassOf`, and concepts are individuals, so mapping SKOS to LPG labels or OWL classes needs an explicit policy (no implied equivalence). **Decision: REUSE** — import/export SKOS for taxonomies. 
`CLAIM-skos-01 | SKOS Reference 2009-08-18 | W3C Recommendation | Officially documented | https://www.w3.org/TR/skos-reference/ | 2009-08-18 / 2026-10-26 | 0.9 | none`

### T-C18-dcat-schemaorg — DCAT and schema.org
| Field | Value |
|---|---|
| Official URL | https://www.w3.org/TR/vocab-dcat-3/ ; https://schema.org/docs/releases.html |
| Owner | W3C Dataset Exchange WG; schema.org community (Google, Microsoft et al.) |
| Latest version + date | DCAT 3 Rec 2024-08-22; schema.org 30.1, 2026-09-16 |
| Status | DCAT 3 published Recommendation (backward compatible with DCAT 2); schema.org de facto vocabulary, released continuously |
| Licence + class | DCAT: W3C document licence; schema.org: CC BY-SA 3.0 per its site (not re-read this run, conf 0.6); weak-copyleft for the schema.org text, vocabulary terms freely used |
| Deployment / air-gap | vocabulary files; yes |
| Tier reason | catalogue/metadata vocabularies |

Relevance: dataset and data-product metadata (CAP-42) and web-visible markup. DCAT catalogues datasets, not facts; schema.org is a loose, non-OWL-rigorous vocabulary (domainIncludes/rangeIncludes are not RDFS domain/range). **Decision: REUSE** DCAT 3 for catalog export; REFERENCE-ONLY schema.org.
`CLAIM-dcat-01 | DCAT 3 | W3C Recommendation 2024-08-22, supersedes DCAT 2 without obsoleting | Officially documented | https://www.w3.org/TR/vocab-dcat-3/ | 2024-08-22 / 2026-10-26 | 0.9 | none`
`CLAIM-dcat-02 | schema.org 30.1 | latest release 2026-09-16 | Officially documented | https://schema.org/docs/releases.html | 2026-10-26 | 0.8 | page truncated`

### T-C18-graphql — GraphQL
| Field | Value |
|---|---|
| Official URL | https://spec.graphql.org/ |
| Owner | GraphQL Foundation (Linux Foundation) |
| Latest version + date | September 2025 edition (released 2025-09-03); Working Draft 2026-09-28 |
| Status | published specification edition (not a W3C/ISO standard; foundation spec) |
| Licence + class | spec licence not shown on page; UNVERIFIED (OWFa believed, conf 0.4) |
| Deployment / air-gap | yes (libraries separate) |
| Tier reason | API query (BL-58) |

Typed API query language, not a graph database language: a query is a tree of field selections against a schema; no path semantics. Relevance: client API over EOIP data (CAP-17); BL-58 is library-only (no server mounted). Mapping from SHACL/ontology to GraphQL types is lossy (unions, `sh:xone`). Security: depth/cost limiting, introspection control, authorization per field. **Decision: EXPERIMENT** — mount behind policy with depth/cost limits.
`CLAIM-gql-api-01 | GraphQL spec | September 2025 latest release, working draft 2026-09-28 | Officially documented | https://spec.graphql.org/ | 2026-10-26 | 0.9 | none`

### T-C18-graph-formats — GraphAr, GraphML, GEXF
| Field | Value |
|---|---|
| Official URL | https://github.com/apache/incubator-graphar ; http://graphml.graphdrawing.org/ (certificate error on fetch) ; https://gexf.net/ |
| Owner | Apache Software Foundation (incubating, since 2024-03-25); GraphML community (Graph Drawing); GEXF Working Group (Gephi) |
| Latest version + date | GraphAr 0.13.0-incubating, 2025-08-19 (earlier 0.12.0, 2024-06-07); GEXF 1.2 (date not shown; 1.3 existence UNVERIFIED); GraphML: spec date UNVERIFIED |
| Status | GraphAr: Apache Incubator project, not graduated (May 2026 board minutes list further ASF-compliant releases still needed) ; GraphML, GEXF: de facto file formats |
| Licence + class | GraphAr Apache-2.0 (permissive); GEXF content CC BY-SA 3.0 (spec text); GraphML UNVERIFIED |
| Deployment / air-gap | files/libraries; yes |
| Tier reason | graph interchange |

GraphAr: Parquet/CSV-chunked vertex/edge tables with adjacency and offset tables for lakehouse graph storage; C++, Spark, Java (FFI no longer updated). GraphML/GEXF: XML graph exchange for visualisation tools; they carry typed attributes but no schema/ontology and no named graph/provenance. Relevance: bulk import/export (CAP-06), exit portability (CAP-52). **Decision: REFERENCE-ONLY GraphAr (EXPERIMENT if lakehouse customers appear); REUSE GraphML/GEXF for visual export.**
`CLAIM-gf-01 | GraphAr | 0.13.0-incubating 2025-08-19, 0.12.0 2024-06-07, incubating since 2024-03-25 | Officially documented | https://release-test.apache.org/api/cle/release/graphar/0.13.0-incubating ; https://whimsy.apache.org/board/minutes/graphar.html | 2026-10-26 | 0.65 | metadata timestamps odd`
`CLAIM-gf-02 | GEXF | version 1.2, CC BY-SA 3.0 | Officially documented | https://gexf.net/ | 2026-10-26 | 0.7 | no date`

### T-C18-tabular-formats — CSV, Parquet, Apache Arrow
| Field | Value |
|---|---|
| Official URL | https://parquet.apache.org/ ; https://arrow.apache.org/ ; RFC 4180 |
| Owner | Apache Software Foundation (Parquet, Arrow); IETF (RFC 4180) |
| Latest version + date | Parquet-java 1.17.0 (2026-01-13); Arrow 24.0.0 (2026-04-21); later versions (Arrow 25.0.1, format 2.13.0) reported only by a vendor blog, UNVERIFIED |
| Status | published standards-like formats; CSV informational RFC (de facto) |
| Licence + class | Apache-2.0 (permissive); RFC 4180 n/a |
| Deployment / air-gap | libraries; yes |
| Tier reason | tabular interchange |

CSV has no types, nulls or encoding guarantee (CSVW Recommendation 2015 adds metadata, prior knowledge). Parquet is columnar storage; Arrow an in-memory columnar format and IPC/Flight. Relevance: connector payloads (CAP-26), bulk loading (CAP-06), analytics export (CAP-62). Tabular → graph requires mapping (BL-33); nothing implies graph structure. **Decision: REUSE** (Arrow/Parquet for bulk paths, CSV for universal import).
`CLAIM-tab-01 | Parquet 1.17.0 | released 2026-01-13 | Third-party report | https://amdatalakehouse.substack.com/p/apache-data-lakehouse-weekly-january | 2026-10-26 | 0.6 | none`
`CLAIM-tab-02 | Arrow 24.0.0 | released 2026-04-21 | Third-party report | https://blogs.apievangelist.com/blogs/apache-arrow-2026-04-21-apache-arrow-24-0-0-release/ | 2026-10-26 | 0.6 | later 25.0.1 claimed by vendor blog`

### T-C18-api-specs — OpenAPI and AsyncAPI
| Field | Value |
|---|---|
| Official URL | https://spec.openapis.org/ ; https://github.com/asyncapi/spec |
| Owner | OpenAPI Initiative (Linux Foundation); AsyncAPI Initiative |
| Latest version + date | OpenAPI 3.2.0 (2025-09-19, per OAI release table) with 3.1.2 patch; AsyncAPI 3.1.0 (2026-01-31); 3.0.0 (2023-12-05) |
| Status | published community specifications (not ISO/W3C) |
| Licence + class | OpenAPI site content Apache-2.0 (spec text licence per repo, not read); AsyncAPI licence UNVERIFIED |
| Deployment / air-gap | documents; yes |
| Tier reason | API description |

Machine-readable HTTP/event API contracts used for SDK and test generation. Relevance: EOIP API contracts (13-API doc), event contracts for ingestion streams (AsyncAPI, CAP-27). An OpenAPI document describes the interface only; it cannot express graph semantics or authorization behaviour. **Decision: REUSE** (publish OpenAPI for the API; AsyncAPI for event contracts if a bus is added, BL-60).
`CLAIM-api-01 | OpenAPI 3.2.0 | dated 2025-09-19, 3.1.2 patch | Third-party/official table via search | https://github.com/OAI/OpenAPI-Specification | 2026-10-26 | 0.7 | search snippet`
`CLAIM-api-02 | AsyncAPI | v3.1.0 2026-01-31 latest; v3.0.0 2023-12-05 | Officially documented | https://github.com/asyncapi/spec/releases | 2026-10-26 | 0.85 | none`

### T-C18-ngsi-ld — NGSI-LD
| Field | Value |
|---|---|
| Official URL | https://uri.etsi.org/ngsi-ld/v1 |
| Owner | ETSI ISG CIM |
| Latest version + date | ETSI GS CIM 009 V1.8.1 (2024-03) is the latest published found; V1.9 only as a public-comment draft (cover V1.8.22, 2025-03); a listing page mentions v1.9 core context |
| Status | published ETSI Group Specification; later version status UNVERIFIED |
| Licence + class | ETSI document terms; UNVERIFIED |
| Deployment / air-gap | yes (brokers e.g. Orion-LD separate) |
| Tier reason | IoT/digital-twin context API |

REST API plus information model (entities, Properties, Relationships) encoded in JSON-LD; its "property graph" is expressed through JSON-LD, with Relationship objects carrying properties. Relevance: twin and IoT sources (C07); data model resembles LPG-in-JSON-LD, so mapping to RDF and LPG each lose something (multi-attribute datasets, temporal representation). **Decision: REFERENCE-ONLY.**
`CLAIM-ngsi-01 | ETSI GS CIM 009 | V1.8.1 (2024-03) latest found; V1.9 draft | Officially documented | https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.08.01_60/gs_CIM009v010801p.pdf | 2026-10-26 | 0.6 | v1.9 publication unconfirmed`

### T-C18-geosparql-owltime — GeoSPARQL and OWL-Time
| Field | Value |
|---|---|
| Official URL | https://www.ogc.org/standards/geosparql/ ; https://www.w3.org/TR/owl-time/ |
| Owner | OGC (GeoSPARQL); W3C/OGC Spatial Data on the Web WG (OWL-Time) |
| Latest version + date | GeoSPARQL 1.1 (OGC 22-047r1), published January 2024; OWL-Time: latest published version is a Candidate Recommendation Draft dated 2022-11-15 (OGC 16-071r3); the earlier 2017 Recommendation is believed to exist (prior knowledge, conf 0.7) |
| Status | GeoSPARQL 1.1 OGC International Standard; OWL-Time latest = CR Draft (not final) |
| Licence + class | OGC/W3C document licences; UNVERIFIED text |
| Deployment / air-gap | vocabularies/engine functions; yes |
| Tier reason | spatial/temporal vocabularies |

GeoSPARQL adds geometry classes, query functions and SHACL shapes to RDF stores; OWL-Time describes instants, intervals, durations. Relevance: not a bitemporal model — it describes time values and Allen relations but not valid-vs-transaction time (BL-37, CAP-34). GeoSPARQL needs engine support. **Decision: REFERENCE-ONLY** (EXPERIMENT OWL-Time for export of validity intervals).
`CLAIM-geo-01 | GeoSPARQL 1.1 | OGC 22-047r1 International Standard | Officially documented | https://www.ogc.org/standards/geosparql/ | 2024-01 / 2026-10-26 | 0.8 | none`
`CLAIM-geo-02 | OWL-Time | latest published CRD 2022-11-15 | Officially documented | https://www.w3.org/TR/owl-time/ | 2026-10-26 | 0.85 | 2017 Rec not re-fetched`

### T-C18-cloudevents — CloudEvents
| Field | Value |
|---|---|
| Official URL | https://github.com/cloudevents/spec |
| Owner | CNCF CloudEvents project |
| Latest version + date | v1.0.2 marked Latest (release date shown as 06 Feb; year 2022 per prior knowledge, conf 0.7); v1.0.1 (12 Dec); v1.0 (24 Oct) |
| Status | published specification (stable 1.0.x); CNCF status not verified |
| Licence + class | Apache-2.0 per prior knowledge (conf 0.6); permissive |
| Deployment / air-gap | yes |
| Tier reason | event envelope |

Common envelope attributes (id, source, type, specversion, time, datacontenttype) with HTTP/Kafka/AMQP/NATS bindings. Relevance: external bus contract (BL-52, BL-60, CAP-27): the envelope carries identity and source, not idempotency or ordering semantics; EOIP's SourceEvent needs mapping. **Decision: REUSE** envelope for outbound events.
`CLAIM-ce-01 | CloudEvents v1.0.2 | latest release | Officially documented | https://github.com/cloudevents/spec/releases | 2026-10-26 | 0.75 | year not on page`

### T-C18-verifiable-credentials — W3C Verifiable Credentials
| Field | Value |
|---|---|
| Official URL | https://www.w3.org/TR/vc-data-model-2.0/ |
| Owner | W3C Verifiable Credentials WG |
| Latest version + date | VC Data Model v2.0, W3C Recommendation, 2025-05-15 |
| Status | W3C Recommendation; companion securing specs' maturity UNVERIFIED (page truncated) |
| Licence + class | W3C document licence; royalty-free per policy (not re-read) |
| Deployment / air-gap | yes (offline verification with pinned keys) |
| Tier reason | signed provenance |

JSON-LD data model for signed claims (issuer, subject, proof via Data Integrity or JOSE/COSE). Relevance: signed evidence manifests (BL-41, CAP-38, CAP-48); VC proves who asserted a claim, not that the claim is true; DID/status-list infrastructure may need network (air-gap risk). Verification depends on JSON-LD canonicalisation (RDFC) — a JSON-LD processing and context-pinning issue (BL-31). **Decision: EXPERIMENT** for signed evidence export.
`CLAIM-vc-01 | VC Data Model 2.0 | W3C Recommendation 2025-05-15 | Officially documented | https://www.w3.org/TR/vc-data-model-2.0/ | 2025-05-15 / 2026-10-26 | 0.9 | none`
