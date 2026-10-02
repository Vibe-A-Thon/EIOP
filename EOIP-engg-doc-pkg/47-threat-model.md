# Threat Model

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Assets, trust boundaries, abuse cases, controls and verification

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Trust boundaries and assets

Assets: connector credentials; enterprise source content; raw capture; graph schema/data; canonical IDs; provenance; local model context; agent/tool capabilities; MCP surface; VS Code workspace; backup archives; audit events. Boundaries: source→connector, uploaded/local file→parser, browser/VS Code/MCP→API, API/worker→HugeGraph, API→local model, container→host volume, administrator→destructive operation.

## Threat register

| Threat | Example | Primary controls | Verification |
|---|---|---|---|
| Credential theft | connector token leaks in logs | secret refs, log redaction, no commit, least privilege | secret scanner + canary-secret log test |
| Prompt injection | malicious document says to call tools | retrieved content treated as data, tool allowlist, QueryPlan policy | adversarial RAG/agent suite |
| Tool injection / confused deputy | model requests unregistered write tool | read-only MVP registry; schema/risk/approval checks later | capability and negative invocation tests |
| Arbitrary Gremlin | NL text produces mutation/query bomb | typed QueryPlan, named templates, depth/result/timeout limits | fuzz/boundary tests |
| Graph poisoning | source injects false cross-domain link | deterministic link rules, evidence, inferred status, validation | poisoned fixture tests |
| Path traversal | connector path escapes configured root | canonical path checks, symlink escape prevention, allowlisted roots | traversal/symlink tests |
| SSRF | configurable connector URL targets local metadata/admin service | endpoint allowlist, scheme/host validation, private endpoint policy | SSRF fixtures |
| Oversized/malicious file | parser exhaustion/archive bomb | size/type limits, bounded parsing, no recursive archive expansion by default | resource-limit tests |
| XSS in UI | source title/document contains script | React escaping, sanitize rendered rich text, CSP, local assets | security UI tests |
| CSRF/admin misuse | browser triggers ingestion/restore | same-site protections, explicit confirmation, auth profile | E2E negative tests |
| Data exfiltration | external model/API receives enterprise text | runtime egress deny, external providers disabled, no fallback | network no-egress test |
| Container escape impact | compromised parser service reaches graph/model | non-root/cap drop/private networks/read-only FS where possible | compose inspection |
| Backup disclosure | archive copied without controls | restrictive permissions, checksum, optional local encryption procedure | restore/access runbook review |
| Supply-chain risk | compromised package/image | locks, hashes/digests, SBOM, license/dependency/image scans | release gate |
| Audit tampering | actor deletes evidence of action | append-oriented restricted audit path, backup/rotation, correlation IDs | permission/coverage tests |

## Residual-risk rule

A local/trusted network is not treated as a complete control. Any exception to a security control is documented in the risk register with owner, expiry, environment and compensating control. Phase 1 does not claim enterprise multi-user authorization because RBAC is intentionally deferred.

## Phase 1 security baseline

- Runtime egress is denied by default; model/images/dependencies are staged before restricted deployment.
- HugeGraph and local-model ports stay on an internal Docker network; only the web/API edge is exposed as configured.
- Non-loopback profiles require local authentication even though RBAC is not implemented.
- Secrets are file-mounted/referenced and redacted from logs; example files contain placeholders only.
- Source paths are allowlisted roots; path traversal/symlink escape/oversized input is rejected.
- Model/retrieved text is untrusted data. It cannot create new tool permissions, arbitrary Gremlin or shell commands.
- QueryPlan bounds and read-only Gremlin templates are enforced for UI, agent and MCP equally.
- Audit events record ingestion, queries, agent/tool calls, admin operations, backup/restore and policy denials; hidden chain-of-thought is never stored.
- Write/destructive MCP/agent tools are not registered in the MVP.
