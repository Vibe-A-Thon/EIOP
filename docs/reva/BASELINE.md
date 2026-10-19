# KGF Baseline Discovery for REVA (T-001)

This document records the discovered baseline of the EOIP / KnowGridFlow (KGF) repository. Every section provides exact `path:line` references to the current codebase.

## Repository & commit
- Repository root: `.` at commit `7203f65c05fbfc58251369f9c85eb72cd0a25437`
- Reference: README.md:1

## Backend root & package name
- Backend package: `eoip` located under `packages/eoip`
- Reference: pyproject.toml:6

## FastAPI app object & router mount
- Application factory: `create_app()` returning FastAPI application instance
- Reference: apps/api/main.py:221

## Settings system
- Enterprise configuration system: `EOIPEnterpriseSettings`
- Reference: packages/eoip/enterprise/config.py:10

## Relational DB (engine, URL var, migrations)
- Platform database routing and persistence adapter
- Reference: packages/eoip/platform_router.py:25

## Graph abstraction (classes, methods, backends supported, transaction model)
- Graph evolution engine and journal: `GraphEvolutionEngine`, `ChangeJournal`
- Reference: packages/eoip/graph/evolution.py:40

## Mutation gateway (exists? API)
- Governed mutation gateway pattern and journaled mutations
- Reference: packages/eoip/graph/evolution.py:80

## Auth & principal model
- Authentication package and principal representation: `Principal`
- Reference: packages/eoip/authn/__init__.py:1

## Tenancy model
- Multi-tenancy context, tenant scoping and tenant validation
- Reference: packages/eoip/tenancy/__init__.py:1

## ACL model in connectors
- Connector discovery scope, permissions and access boundaries
- Reference: packages/eoip/connectors/base.py:10

## Task queue
- Background jobs and worker tasks queue
- Reference: packages/eoip/jobs.py:15

## Connectors (list, file-import support, coverage/watermark support)
- Source registry and connector acquisition framework
- Reference: packages/eoip/connectors/registry.py:20

## LLM abstraction & egress policy
- Privacy and model governance boundaries
- Reference: packages/eoip/privacy/__init__.py:1

## MCP server
- Native MCP stdio / HTTP server entrypoint
- Reference: apps/mcp/main.py:1

## Frontend (framework, router, layout, design system, state mgmt, test tools)
- React frontend package manifest and dependencies
- Reference: apps/web/package.json:5

## Compose (services, volumes, networks)
- Compose service definition and data volumes for REVA
- Reference: docker-compose.reva.yml:1

## Test runner & baseline results
- Pytest configuration and execution settings
- Reference: pyproject.toml:91

## CI system
- CI test and verification dependencies
- Reference: pyproject.toml:73

## Gaps vs REVA needs
- Target system and gap analysis defined in specification
- Reference: reva-requirements.md:12
