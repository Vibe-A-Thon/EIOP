# Documentation Index

Last reviewed: 2026-10-19. These are working-tree guides, not a production certification. Start with the guide for your task; component READMEs link to the same authoritative procedures rather than duplicating them.

## Reading Paths

| Task | Read in this order |
|---|---|
| First local run | [Root README](../README.md), [Getting Started](getting-started.md), [Troubleshooting and operations](operations-runbook.md) |
| Join the engineering team | [Developer guide](developer-maintainer-guide.md), [architecture](architecture-guide.md), [package map](../packages/eoip/README.md), [testing](testing-guide.md) |
| Change a frontend | [Frontend guide](frontend-development.md), [web README](../apps/web/README.md), [alternate frontend](../frontend/README.md) |
| Add or change an API | [API component](../apps/api/README.md), [API reference](api-reference.md), [configuration](configuration-reference.md), [change checklist](migration-refactoring-guide.md) |
| Add ingestion or a connector | [Worker](../apps/worker/README.md), [connectors](../packages/eoip/connectors/README.md), [connector qualification](connectors/qualification.md) |
| Work on REVA | [Component and integration limits](../reva/README.md), [requirements](../reva-requirements.md), [implementation plan](../reva-implementation-plan.md) |
| Deploy, recover or upgrade | [Deployment](../deploy/README.md), [operations](operations-runbook.md), [migration](migration-refactoring-guide.md), [release gates](release-checklist.md) |
| Split into a product suite | [Suite proposal](EOIP-suite-architecture-plan.md), [migration guide](migration-refactoring-guide.md); suite target apps are not yet implemented by that plan |
| Audit or hand over the project | [Review scope and findings](documentation-review-2026-10-18.md), [documentation policy](documentation-policy.md), [generated inventory](generated/README.md) |
| Distribute the software | [Licensing](../LICENSING.md), [third-party notices](../THIRD_PARTY_NOTICES.md), [compliance](../compliance/README.md), release gates |

## Component Entry Points

[Applications](../apps/README.md) covers API, worker, MCP, web and VS Code. The [backend shim](../backend/README.md) and [alternate frontend](../frontend/README.md) are distinct development/preview entry points. [Python packages](../packages/eoip/README.md), [configuration](../config/README.md), [schemas](../schemas/README.md), [scripts](../scripts/README.md), [tests](../tests/README.md), [acceptance tools](../tools/README.md), [benchmarks](../benchmarks/README.md), [data](../data/README.md), [demonstrations](../demo/README.md) and [research](../research/README.md) explain their ownership and limitations.

## Specifications and Status

| Programme | Requirements | Implementation |
|---|---|---|
| Gap closure | [Audit](../gaps-audit-cp.md) | [Plan](../gaps-audit-cp-implementation-plan.md) |
| GUI/UIX | [Requirements](../GUI-UIX-requirements.md) | [Plan](../GUI-UIX-implementation-plan.md) |
| Competitive capabilities | [Requirements](../CRAr_cpccaggcc-requirements.md) | [Implementation](../CRAr_cpccaggcc-implementation.md) |
| Community/IP and CTAR | [Requirements](../community-ip-requirements.md) | [Plan](../community-ip-implementation-plan.md) |
| IP/Warrant | [Requirements](../ip-requirements.md) | [Plan](../ip-requirements-implementation-plan.md) |
| ASPEII | [Requirements](../aspeii-reqirements.md) | [Plan](../aspeii-implementation-plan.md) |
| Graph Neurons | [Requirements](../Graph-Neurons-requirements.md) | [Plan](../Graph-Neurons-implementation-plan.md) |
| Wisdom Graph | [Requirements](../wisdom-graph-requirements.md) | [Plan](../wisdom-graph-implementation-plan.md) |
| REVA | [Requirements](../reva-requirements.md) | [Plan](../reva-implementation-plan.md); [inspected integration limits](../reva/README.md) |

The [engineering package](../EOIP-engg-doc-pkg/README.md) contains earlier specifications and historical research. [Decision records](decisions/) record architectural choices; [neural installation](install-neural.md) records the current optional-tier boundary. Keep normative requirements intact when implementation is incomplete: document the gap, do not rewrite the requirement to match a stub.

## What Counts as Current

Code/configuration establish current implementation; executed, source-bound evidence establishes verified behavior. Specifications establish intended behavior. A module name, OpenAPI route, demo screenshot, generated inventory, task checkbox or passing unit test alone does not establish production completion. Snapshot dates and exact runtime profiles matter.
