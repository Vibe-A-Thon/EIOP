# ServiceNow Table API Connector Specification

*Researched per CRA-008.1, CRA-008.6, CRA-008.9. Complies with ADR-004, ONT-007.*

## Official API Specifications & Pinned Versions
- **ServiceNow**: REST Table API (`/api/now/table/{tableName}`) pinned to Utah/Vancouver release baseline.
  - Core tables: `cmdb_ci`, `cmdb_rel_ci`, `incident`, `change_request`, `problem`, `kb_knowledge`.
  - Relationship types in `cmdb_rel_ci`: `Depends on::Used by`, `Runs on::Hosts`.

## Row/Field ACLs & Domain Separation
- **Domain Separation**: Respects `sys_domain` field on all records. Records belonging to non-global domains receive `RESTRICTED` visibility with principal refs scoped to `servicenow:domain:{domain}`.
- **Least-Privilege Roles**: Role-based principal refs separate CMDB readers (`servicenow:role:cmdb_read`) from operational ITIL agents (`servicenow:role:itil`). Broad service-account rights are avoided.

## CMDB Directed Cycle Detection
- CI dependencies are captured as a directed graph.
- Rather than silently dropping circular relationships to force a Directed Acyclic Graph (DAG), cycles in CMDB relations are identified and emitted as data-quality findings (`CMDB_DEPENDENCY_CYCLE`) with full cycle paths and severity.

## Write-Back Governance
- Automated or direct write-back to ServiceNow is prohibited without an approved GovernedAction warrant (CRA-027).
