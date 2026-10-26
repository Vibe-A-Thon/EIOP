# C06 Tier C records - batch V18 (verified 2026-10-26)

Cross-references: DataHub is in `C06-datahub.md` and is not repeated. EOIP capabilities: CAP-40 lineage, CAP-42 catalog.

### T-C06-ovaledge - OvalEdge
| Field | Value |
|---|---|
| Official URL | https://www.ovaledge.com |
| Owner | OvalEdge (private vendor) |
| Latest version + date | SaaS/self-managed; version UNVERIFIED |
| Status | active (listings current for 2026) |
| Licence + class | proprietary |
| Deployment modes | saas, self-hosted (NOT PUBLICLY VERIFIED in detail) |
| Air-gap viable | unknown |
| Tier reason | mid-market catalog, no unique architecture |

Catalog with glossary, lineage, quality, access management, policy; vendor lists 150+ connectors and NL questions [CLAIM-oval-01]. Catalog search plus operational lineage; no evidence of semantic inference. Touches CAP-42, CAP-40. **Decision: REFERENCE-ONLY** - feature checklist only.

CLAIM-oval-01 | OvalEdge / 2026 | six modules, 150+ connectors, masking policies | Vendor claim | ovaledge.com/data-catalog; capterra.com/p/219905/OvalEdge | 2026-10-26 | 0.4 | none

### T-C06-actian-dip - Actian Data Intelligence Platform
| Field | Value |
|---|---|
| Official URL | https://www.actian.com/data-intelligence-platform/ |
| Owner | Actian, a division of HCLSoftware |
| Latest version + date | SaaS; UNVERIFIED |
| Status | active; renamed |
| Licence + class | proprietary |
| Deployment modes | saas, dedicated VPC; hybrid/on-prem connectivity claimed |
| Air-gap viable | no evidence |
| Tier reason | naming resolution; federated KG catalog |

**Naming resolved:** the product is the former Zeenea. HCLSoftware completed its acquisition of Zeenea (Paris) on 2024-09-12 and placed it under Actian [CLAIM-actian-01]; the platform is now "Actian Data Intelligence Platform", described as an active metadata platform "powered by a federated knowledge graph" with MCP and A2A support [CLAIM-actian-02]. No evidence found linking Actian to data.world (that is ServiceNow, see `C06-data-world.md`). Touches CAP-42, CAP-40. **Decision: REFERENCE-ONLY** - federated-in-place idea noted.

CLAIM-actian-01 | 2024-09-12 | HCLSoftware completed Zeenea acquisition; brand kept near term | Third-party report | dbta.com HCLSoftware Acquires Zeenea; aap.com.au cision release | 2026-10-26 | 0.8 | none
CLAIM-actian-02 | 2026 | product name, KG, MCP/A2A, SOC 2 Type II, ISO 27001 | Vendor claim | actian.com/data-intelligence-platform/ | 2026-10-26 | 0.6 | none

### T-C06-egeria - Egeria
| Field | Value |
|---|---|
| Official URL | https://github.com/odpi/egeria |
| Owner | LF AI & Data Foundation (originally ODPi; IBM/ING) |
| Latest version + date | V6.2, 2026-10-06 (page showed day/month; year inferred); V6.1 08-19; V6.0 04-01 |
| Status | active |
| Licence + class | Apache-2.0, permissive [CLAIM-egeria-01] |
| Deployment modes | self-hosted, docker, kubernetes |
| Air-gap viable | yes (inferred) |
| Tier reason | open metadata exchange standard |

Open metadata exchange between catalogs via a shared type system and metadata repositories; has an OpenLineage integration [CLAIM-egeria-02]. Catalog and lineage exchange, not inference. Internals not inspected. Touches CAP-42, CAP-40. **Decision: EXPERIMENT** - evaluate its open types as an interchange vocabulary for catalog imports.

CLAIM-egeria-01 | Egeria | Apache 2.0, origin ODPi, LF AI & Data | Third-party report | linuxfoundation.org ODPi press release; openlineage.io/blog/openlineage-egeria | 2026-10-26 | 0.7 | none
CLAIM-egeria-02 | releases | V6.2 latest 06 Oct | Officially documented | github.com/odpi/egeria/releases | 2026-10-26 | 0.7 | year not shown

### T-C06-amundsen - Amundsen
| Field | Value |
|---|---|
| Official URL | https://github.com/amundsen-io/amundsen |
| Owner | Amundsen community (originated at Lyft; LF AI & Data) |
| Latest version + date | no releases shown on repo page |
| Status | **archived** (read-only) 2026-09-29 |
| Licence + class | Apache-2.0, permissive |
| Deployment modes | self-hosted |
| Air-gap viable | yes, but unmaintained |
| Tier reason | activity verified: archived |

README: "Due to inactivity, this project was archived in September 2026." About 4.8k stars [CLAIM-amund-01]. Search-centric discovery over a graph store plus search index; no further inspection. Touches CAP-42. **Decision: REFERENCE-ONLY** - do not adopt; archived.

CLAIM-amund-01 | repo | archived by owner 2026-09-29, Apache-2.0, 4.8k stars | Officially documented | github.com/amundsen-io/amundsen | 2026-10-26 | 0.9 | none

### T-C06-unity-catalog - Unity Catalog (OSS)
| Field | Value |
|---|---|
| Official URL | https://github.com/unitycatalog/unitycatalog |
| Owner | Databricks-originated; LF AI & Data sandbox project |
| Latest version + date | v0.7.0, 13 Oct (year inferred 2026); v0.6.0 20 Aug; v0.5.1 18 Jul |
| Status | active, pre-1.0 |
| Licence + class | Apache-2.0, permissive |
| Deployment modes | self-hosted server, docker |
| Air-gap viable | yes (inferred) |
| Tier reason | lakehouse catalog, open API |

OpenAPI-specified catalog for tables, volumes, functions and AI assets, compatible with Hive metastore and Iceberg REST APIs [CLAIM-uc-01]. It is a lakehouse access/namespace catalog, not a semantic catalog. Touches CAP-42. **Decision: INTEGRATE** - as a source of table metadata and lineage-adjacent facts.

CLAIM-uc-01 | UC OSS | Apache 2.0, LF AI & Data sandbox, Hive/Iceberg REST compatible; v0.7.0 latest | Officially documented | github.com/unitycatalog/unitycatalog; /releases | 2026-10-26 | 0.7 | none

### T-C06-apache-polaris - Apache Polaris
| Field | Value |
|---|---|
| Official URL | https://polaris.apache.org (repo github.com/apache/polaris) |
| Owner | Apache Software Foundation (donated by Snowflake) |
| Latest version + date | 1.8.0, 28 Sep (2026 per asset timestamps); 1.7.0 02 Aug; 1.6.0 09 Jul |
| Status | active; top-level project since Feb 2026 |
| Licence + class | Apache-2.0, permissive |
| Deployment modes | self-hosted, docker, kubernetes |
| Air-gap viable | yes (inferred) |
| Tier reason | Iceberg REST catalog |

Open implementation of the Iceberg REST catalog with multi-tenancy features (1.4 blog) [CLAIM-polaris-01]. Table-format catalog, not knowledge catalog. Touches CAP-42. **Decision: INTEGRATE** - read Iceberg table metadata for connectors; no rebuild.

CLAIM-polaris-01 | Polaris | TLP graduation Feb 2026; 1.4 April 2026; 1.8.0 latest | Third-party report + releases page | snowflake.com/en/engineering-blog/apache-polaris-1-4-release/; github.com/apache/polaris/releases | 2026-10-26 | 0.7 | release page shows no year

### T-C06-alation - Alation
| Field | Value |
|---|---|
| Official URL | https://www.alation.com |
| Owner | Alation, Inc. (private) |
| Latest version + date | SaaS; UNVERIFIED |
| Status | active |
| Licence + class | proprietary |
| Deployment modes | not stated on homepage; UNVERIFIED |
| Air-gap viable | unknown |
| Tier reason | catalog incumbent |

Now positions "AIOS" (Alation Intelligence Operating System) for governed AI/BI and agent diagnosis; claims analyst recognition [CLAIM-alation-01]. All vendor claims. Catalog and governance plus agent context; no inference evidence. Touches CAP-42, CAP-40. **Decision: REFERENCE-ONLY**.

CLAIM-alation-01 | 2026 | AIOS positioning, five solution areas | Vendor claim | alation.com | 2026-10-26 | 0.4 | none

### T-C06-informatica-claire - Informatica (CLAIRE/IDMC)
| Field | Value |
|---|---|
| Official URL | https://www.informatica.com |
| Owner | Informatica; Salesforce agreed to acquire for about $8B ($25/share), announced May 2025 |
| Latest version + date | IDMC SaaS; UNVERIFIED |
| Status | acquired (closing reported Nov 2025 by a weak secondary source; primary confirmation NOT FOUND) |
| Licence + class | proprietary |
| Deployment modes | saas (IDMC); on-prem legacy |
| Air-gap viable | unknown |
| Tier reason | catalog/MDM suite |

CLAIRE is the AI engine of the Intelligent Data Management Cloud; Salesforce plans to combine catalog, governance and integration with Agentforce/Data 360 [CLAIM-infa-01]. Catalog + MDM (entity matching relevant to CAP-31) + lineage. **Decision: REFERENCE-ONLY**; confirm corporate status via Salesforce filings before any partnership assumption.

CLAIM-infa-01 | 2025-05 | Salesforce to acquire Informatica ~$8B; closing unconfirmed from primary source | Third-party report | hpcwire.com/bigdatawire/2025/05/27/its-official-informatica-agrees-to-be-bought-by-salesforce-for-8-billion/ | 2026-10-26 | 0.6 announce / 0.3 close | one site says Nov 2025

### T-C06-google-dataplex - Google Dataplex
| Field | Value |
|---|---|
| Official URL | https://cloud.google.com/dataplex |
| Owner | Google Cloud |
| Latest version + date | managed service; release notes through 2026-05 seen |
| Status | active; renamed (Dataplex Universal Catalog, now "Knowledge Catalog") |
| Licence + class | proprietary |
| Deployment modes | managed-cloud only |
| Air-gap viable | no |
| Tier reason | cloud catalog and lineage API |

Release notes show the product renamed Knowledge Catalog (API, CLI, IAM names unchanged), a lineage BFS API method (2026-05-29) and a preview lineage MCP server (2026-05-27) [CLAIM-gcp-01]. Lineage graph is queryable by agents, GCP-scoped. Touches CAP-40, CAP-42. **Decision: REFERENCE-ONLY** - lineage-over-MCP is a pattern worth copying.

CLAIM-gcp-01 | 2026-05 | rename; lineage BFS API; lineage MCP preview | Officially documented (via search summary) | docs.cloud.google.com/dataplex/docs/release-notes | 2026-10-26 | 0.7 | dates vary for BigQuery lineage preview (03-30 vs 04-10)
