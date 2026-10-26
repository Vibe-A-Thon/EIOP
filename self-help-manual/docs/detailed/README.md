# EOIP Detailed Self-Help Manual

This is the complete, feature-by-feature manual for the EOIP platform. Every chapter is grounded in the actual source code (file:line verified): each feature is documented with **what it does**, **how to access it** (UI path and/or API endpoint), **step-by-step instructions** with a copy-pasteable example, **the expected result**, and **errors and recovery**.

Honesty convention: where a capability exists in code but has not been runtime-certified, or is an External/ADR-gated integration, the chapter says so. Nothing in this manual is marketing.

## Chapters

| # | Chapter | Audience |
|---|---------|----------|
| 00 | [Overview and quickstart](00-overview-and-quickstart.md) — what the platform is, deployment profiles, first connection, demo data, verification, first-run errors | Everyone |
| 01 | [Web application](01-web-application.md) — every UI surface: Knowledge Explorer and lenses, Cognitive Engineering studios, Cognitive Dashboards, Ontology Studio, Administration, Guided demo, Appearance | End users |
| 02 | [API and query languages](02-api-and-query-languages.md) — QueryPlan IR, query endpoints, 12 real query-language parsers (JSONPath, jq, PromQL, Lucene, KQL, XPath, Datalog, SQL, GraphQL, Gremlin, openCypher, SPARQL), suggest engine, faceted search, bitemporal queries, caches | Developers, analysts |
| 03 | [Ingestion and graph construction](03-ingestion-and-graph-construction.md) — connectors, source registry, job lifecycle, DLQ/replay, schema profiler, graph-building algorithms, provenance | Data engineers, admins |
| 04 | [Ontology and semantics](04-ontology-and-semantics.md) — enterprise ontology, versioning/diff/drift, RDF/OWL exports (11 formats), SKOS taxonomies, 8 domain packs, truth/claims model, validation, architecture conformance, graph test DSL | Ontologists, stewards |
| 05 | [RAG and natural language](05-rag-and-natural-language.md) — 17 RAG patterns, 22 ragx architectures, 25 retrieval techniques, abstention/evidence, retrieval strategies, answer modes, reports, model governance | Analysts, AI engineers |
| 06 | [Agents, loops and orchestration](06-agents-loops-and-orchestration.md) — governed agent runtime, 18 specialist agents, agentarch catalog (classical/reasoning/enterprise/org patterns), A2A, 23 execution loops, 15 human-participation patterns, reasoning strategies, durable workflows, MCP server (18 tools) | AI engineers, operators |
| 07 | [Graph intelligence](07-graph-intelligence.md) — centralities, communities, paths, similarity, blast radius, causal analysis, what-if/simulation, anomalies, expertise, knowledge debt, process mining, evolution/temporal, capsules, lenses, playback | Architects, analysts |
| 08 | [Security and governance](08-security-and-governance.md) — token auth, users, RBAC/ABAC, tenancy/quotas/metering, licensing, layered config, egress gateway (S0–S7), branding, privacy/DSAR, compliance packs, knowledge firewall | Security, admins, auditors |
| 09 | [Platform operations](09-platform-operations.md) — preflight, upgrades, support bundles, metrics/OTel, worker HA lease, federation, adapter catalog, marketplace, knowledge products, KGCI pipeline, QA gates, backup/restore, HA/Helm, troubleshooting | Operators, SRE |
| 10 | [Developer surfaces](10-developer-surfaces.md) — VS Code extension (19 commands), MCP tools reference, CLI/scripts, Python SDK, extension points (connector SDK, plugins, packs) | Developers, integrators |

## Using this manual

1. Start with chapter 00 to get a running environment.
2. Use chapter 01 to learn the UI by clicking through it.
3. Use chapters 02–09 as references while working; every section is self-contained.
4. Use chapter 10 when integrating programmatically or extending the platform.

The older high-level help center (../site/) and printable PDF/DOCX manuals remain available for orientation; these chapters are the complete reference.
