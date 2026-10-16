# Assumptions

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Explicit implementation assumptions that must be validated

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Confirmed from the governing specification

- Runtime is local/on-prem and cloud/SaaS is not required.
- Docker is available; Docker Compose is used for MVP.
- Apache HugeGraph is the authoritative graph/ontology store.
- MVP does not implement RBAC and may run in a trusted/single-user/demo environment, while still requiring security controls.
- External LLM endpoints are disabled in MVP.

## Working assumptions introduced by this baseline

- The actual Jira JSON was **not** supplied with the master prompt; the fixture is synthetic and the importer is mapping-driven.
- A local Git working repository is available to the worker for the demo. GitLab-specific MR/pipeline metadata may be supplied by synthetic JSON or an approved on-prem endpoint.
- MVP code parser support is Python and TypeScript/JavaScript; the parser plugin contract is language-neutral.
- One physical HugeGraph graph is sufficient for Phase 1 scale and provides the best direct cross-domain traversal semantics.
- A locally staged model runtime is available for the “local model demonstrated” acceptance step, but model unavailability is a supported degraded mode.
- TLS may terminate at a local reverse proxy or enterprise boundary for a controlled LAN deployment; loopback developer profile may use HTTP. This must be explicit per deployment profile.
- No requirement in this package grants EOIP permission to modify Jira, Git, GitLab, ServiceNow, source code or production systems in Phase 1.

## Validation triggers

Each assumption becomes an ADR/update when actual enterprise samples, capacity targets, authentication/SSO requirements, network topology, language mix or recovery objectives are supplied. None should be silently converted into a product claim.
