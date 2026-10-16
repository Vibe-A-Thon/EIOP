# KnowGridFlow (EOIP) Architecture Guide (S-04)

## Architecture Overview

KnowGridFlow is organized around a multi-layered, ontology-driven knowledge mesh:

1. **Ontology & Validation Fabric (`packages/eoip/ontology/`, `packages/eoip/validation/`)**
   - Strictly enforced vertex and edge taxonomy with immutable schemas.
   - Pre-mutation hard gates (`check_vertex`, `check_edge`) blocking invalid schema mutations.
   - Bitemporal tracking (`created_at`, `modified_at`, `observed_at`, `tx_time`).

2. **Graph Storage & Abstraction (`packages/eoip/graph/`)**
   - Pluggable storage engine interface (`GraphStore`).
   - `HugeGraphStore` for distributed production environments.
   - `MemoryGraphStore` for local development, fast unit tests, and CI/CD harnesses.

3. **Cognitive & Intelligence Engines (`packages/eoip/cognition/`, `packages/eoip/moonshot/`)**
   - Causal simulation and counterfactual blast-radius analysis.
   - Continuous Knowledge Immune System and AMIS anti-poisoning defense.
   - Graph Foundation Model host (`G-Reasoner`) and Large Ontology Model fine-tuning runtime.

4. **Multi-Agent Orchestration (`packages/eoip/agents/`)**
   - Mesh supervisor, tool contracts, task decomposition, and MCP bridges.

5. **User Experience & Tooling (`apps/web/`, `apps/vscode-extension/`)**
   - Rich React/Vite web application with WebGL graph canvas and administrative panels.
   - VS Code extension providing in-editor graph exploration, schema validation, and diagnostics.
