# KnowGridFlow (EOIP) API Reference & Contributing Guide (S-04)

## Core REST API Endpoints

- **GET `/health` / `/ready`**: System health and readiness probes (NFR-OPS-001).
- **GET `/metrics`**: Prometheus text-format metrics exposition (MVP-FR-024, NFR-OPS-002).
- **POST `/api/v1/graph/query`**: Execute unified Cypher/Gremlin queries across active graph stores.
- **POST `/api/v1/causal/blast-radius`**: Counterfactual blast-radius evaluation for hypothetical changes.
- **GET `/api/v1/admin/security/posture`**: Enterprise security governance posture and token revocation status.
- **POST `/api/v1/ci/pipeline/run`**: Trigger automated KG CI/CD pipeline validation.

## Contributing Guidelines

1. **Strict Zero Mock Policy**: Never wire mock or demo data into production execution paths.
2. **Schema Invariant Gate**: All graph mutations must conform to `VERTEX_LABELS`, `EDGE_LABELS`, and `PROPERTY_KEYS` in `packages/eoip/ontology/manifest.py`.
3. **Traceability**: All requirements must have passing unit tests explicitly decorated with `@pytest.mark.req("<ID>")`.
4. **Gate Verification**: Verify tests and gate integrity via `pytest tests/unit/test_qa_gate_integrity.py`.
