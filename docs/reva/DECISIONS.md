# REVA Design Decisions (D-01 through D-24)

| Date | Decision ID | Context found in code | Rule applied | Consequence | Reversible? |
|---|---|---|---|---|---|
| 2026-10-18 | D-01 | Python 3.11 backend in KGF (`packages/eoip`) | Python (KGF backend interpreter) | Pure Python implementation under `reva/` and `packages/eoip/reva/` | No |
| 2026-10-18 | D-02 | Top-level repository layout with `packages/` | `reva/` package exposed at root and in pythonpath | Single import path `reva.*` | No |
| 2026-10-18 | D-03 | Local-first deployment without mandatory PostgreSQL | SQLite WAL mode for local; PostgreSQL schema `reva` when configured | Zero external DB dependency for local verifications | Yes |
| 2026-10-18 | D-04 | Filesystem content-addressed storage available | Filesystem CAS under data directory (`<data>/reva/blobs/sha256/ab/cd/<hex>`) | Robust, portable content addressing | Yes |
| 2026-10-18 | D-05 | In-process jobs and background tasks in KGF | Built-in asyncio worker with durable `reva_jobs` table | Reliable job execution without external message broker | Yes |
| 2026-10-18 | D-06 | Windows/Linux host environment | Process sandbox with resource limits; Docker when daemon reachable | Standard process isolation with resource governance | Yes |
| 2026-10-18 | D-07 | Governed mutation gateway in `packages/eoip/graph/evolution.py` | Governed mutation gateway pattern through GraphPort | Audit trail on all graph writes | No |
| 2026-10-18 | D-08 | Multi-backend graph abstraction | Gremlin / HugeGraph / Neo4j abstraction with capability probes | Backend-neutral queries and projections | No |
| 2026-10-18 | D-09 | Performance considerations for graph storage | Warrants referenced by ID on elements; not projected as graph vertices | Prevents graph vertex bloat | No |
| 2026-10-18 | D-10 | Multi-tenant platform in `packages/eoip/tenancy` | AuthPort principal and tenant scoping; default tenant when unspecified | Full tenant isolation on all tables and blobs | No |
| 2026-10-18 | D-11 | React frontend in `apps/web` | KGF React app integration under `/reva/*` and self-contained tracker | Unified user experience | Yes |
| 2026-10-18 | D-12 | MCP server in `apps/mcp` | Register REVA tools into MCP server and provide stdio CLI | Standards-compliant agent interaction | No |
| 2026-10-18 | D-13 | Local-first model constraint | Deterministic answer generation with local model synthesis | Zero data egress to external LLMs | No |
| 2026-10-18 | D-14 | Python codebase | Built-in AST mutation testing probe | Fast mutant generation without external heavy tools | No |
| 2026-10-18 | D-15 | Cryptographic primitives in `cryptography` | Ed25519 signatures and AES-256-GCM key wrapping | Modern, secure asymmetric signing | No |
| 2026-10-18 | D-16 | Canonical JSON requirements | REVA native RFC 8785 implementation, cross-checked against `rfc8785` | Deterministic cross-platform hashing | No |
| 2026-10-18 | D-17 | Shipped SBOM industry standards | CycloneDX 1.5 JSON and SPDX 2.3 JSON exports | Interoperable supply chain compliance | No |
| 2026-10-18 | D-18 | Enterprise ticketing governance | Jira write-back disabled by default | Non-intrusive observation | Yes |
| 2026-10-18 | D-19 | Air-gapped security posture | Vulnerability matching offline against local mirrored database | Zero runtime network calls | Yes |
| 2026-10-18 | D-20 | Data privacy and integrity | Row sampling disabled by default | No unauthorized data sampling | Yes |
| 2026-10-18 | D-21 | Core scope protection | Forensics extension pack disabled in 1.0 | Eliminates unneeded dynamic instrumentation | Yes |
| 2026-10-18 | D-22 | Declarative specifications | Obligation YAML in `docs/reva/obligations/` with database mirror | Git-versioned proof-of-done definitions | No |
| 2026-10-18 | D-23 | Code coverage measurement | `coverage.py` via pytest-cov with `--cov-context=test` | Context-aware per-obligation coverage tracking | No |
| 2026-10-18 | D-24 | Canonical URL and endpoint paths | `{}` per parameter segment; lowercase method; no trailing slash | Consistent API surface matching | No |
