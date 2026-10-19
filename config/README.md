# Configuration Directory

Checked-in declarative configuration, not a secret store or a copy of every tenant's runtime state. The root [configuration reference](../docs/configuration-reference.md) explains active environment variables and precedence.

`graph-store.yaml` selects the graph backend; `mappings/` holds source mappings; `query-policies/` holds query policies; `agents/`, `ontology/`, `architecture/`, `domain-packs/`, `benchmarks/` and `verification/` hold domain-specific inputs. `memory-policy.yaml` controls memory behavior and `systems-registry.json` supplies system configuration.

Before editing, find the consuming loader and its validation path with `rg`. Some loaders read once at startup and some use explicit relative paths; `EOIP_CONFIG_DIR` is not a guaranteed override for every module. Configuration presence does not mean a runtime route uses it.

Validate changes with the relevant schema and positive/negative tests. Check canonical IDs, query limits, allowed hosts, data paths, secret references and reload/restart needs. Commit safe defaults/templates only. Use a controlled environment and [migration procedure](../docs/migration-refactoring-guide.md) for changes affecting existing data or permissions.
