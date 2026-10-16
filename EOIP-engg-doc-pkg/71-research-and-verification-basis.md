# Research and Verification Basis

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Record current primary sources used for changeable technology claims

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Verification principle

The master prompt requires that HugeGraph capabilities not be invented. This architecture therefore relies on official project documentation for deployment/backend/backup semantics and treats interoperability layers conservatively. Implementation teams must re-check pinned versions before coding or upgrading.

## Primary references checked on 2026-10-01

- Apache HugeGraph — Server Quick Start: https://hugegraph.apache.org/docs/quickstart/hugegraph/hugegraph-server/ — current documentation describes HugeGraph Server, Docker/Compose deployment and supported REST/graph interfaces.
- Apache HugeGraph — RocksDB backend: https://hugegraph.apache.org/docs/config/config-backend-rocksdb/ — describes embedded RocksDB standalone behavior and the distinction from distributed HStore.
- Apache HugeGraph — Backup and Restore: https://hugegraph.apache.org/docs/guides/backup-restore/ — describes JSON schema/graph backup/restore using HugeGraph tools and graph modes.
- Apache HugeGraph — Toolchain / HugeGraph Tools: https://hugegraph.apache.org/docs/quickstart/toolchain/hugegraph-tools/ — operational commands for graph management, Gremlin, backup and restore.
- Tree-sitter documentation: https://tree-sitter.github.io/tree-sitter/ — deterministic incremental parsing foundation used for code graph extraction.
- Model Context Protocol specification: https://modelcontextprotocol.io/specification/ — versioned protocol semantics; pin the implementation SDK/protocol at development time.
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk — local MCP server/client implementation option; pin a tested release.
- Ollama documentation: https://docs.ollama.com/ — optional local model runtime for a demo profile; EOIP model abstraction must also support other approved self-hosted runtimes.

## Claims deliberately not made

- HugeGraph is **not** documented here as a native RDF/OWL/SPARQL database; EOIP uses an adapter/export compatibility layer.
- HugeGraph is **not** assumed to be a vector database for MVP retrieval.
- A particular model runtime, embedding model or vector index is **not** mandatory architecture.
- Performance/scale numbers in this package are engineering targets or benchmark definitions unless explicitly marked as measured results.
