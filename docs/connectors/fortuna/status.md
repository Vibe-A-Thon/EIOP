# Fortuna Connector Status & Architectural Decision Notice

*Researched per CRA-009.3, CRA-009.8. Governed by Decision H-06.*

## Status: BLOCKED Pending Decision H-06
- **Adapter State**: `BLOCKED`
- **Blocked By**: `Decision H-06` ("Identify Fortuna product, API, auth and data contract")
- **Missing-Input Reason**: Product identity, API interface/schema, network endpoints, and authentication contracts for "Fortuna" are currently unspecified in enterprise architecture documentation.

## Architectural Boundary Invariant
- The platform strictly refuses to invent an unverified or imaginary Fortuna API.
- Attempting to instantiate or execute product-specific Fortuna operations raises `FortunaConnectorBlockedError`.

## Recommended Alternative
- Teams requiring connectivity to custom internal or third-party enterprise systems in the interim must use `GenericCustomSystemConnector` or `GenericRestApplicationConnector` configured with a verified CML mapping IR.
