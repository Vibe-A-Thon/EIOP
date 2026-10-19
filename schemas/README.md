# JSON Schemas and Contracts

This directory contains versioned contract schemas for source events, graph mutations/results, queries, agents/tools, provenance, memory, temporal records and other domain artifacts. `_common.schema.json` supplies shared definitions and `_catalog.json` indexes schemas.

The runtime also has Python contracts in [packages/eoip/contracts](../packages/eoip/contracts/) and schema/validation logic in the owning domains. The engineering package contains additional specification schemas; do not assume those are the same files consumed at runtime.

## Safe Schema Change

1. Find every loader and producer/consumer of the schema and any matching Pydantic type.
2. Keep required fields, enums, canonical IDs, timestamps, provenance and unknown-field handling consistent.
3. Update the catalog when required by its existing format; do not silently break `$ref` paths.
4. Test valid, invalid and old-version payloads. For stored records, add a migration/replay plan.
5. Update API/client documentation and regenerate the relevant actual contract artifact.

A JSON Schema that validates a synthetic sample does not prove a live API enforces it. Test the real ingestion/query/tool boundary and unauthorized inputs. See [API guide](../docs/api-reference.md), [testing](../docs/testing-guide.md) and [migration](../docs/migration-refactoring-guide.md).
